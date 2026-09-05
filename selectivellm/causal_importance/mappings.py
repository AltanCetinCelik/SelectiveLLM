"""Canonical contiguous-channel mappings and frozen five-percent quotas."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

BlockSize = Literal[64, 128]
MAPPING_SCHEMA_VERSION = "mlp-contiguous-block-map-1.0.0"
INTERMEDIATE_SIZE = 8960
LAYER_COUNT = 28
TOTAL_LAYER_CHANNELS = INTERMEDIATE_SIZE * LAYER_COUNT
SELECTED_CHANNELS = 12_544


def stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class BlockRange:
    block_index: int
    start_channel: int
    stop_channel: int

    def to_dict(self) -> dict[str, int]:
        return {
            "block_index": self.block_index,
            "start_channel": self.start_channel,
            "stop_channel": self.stop_channel,
        }


@dataclass(frozen=True)
class BlockMapping:
    block_size: BlockSize
    blocks: tuple[BlockRange, ...]
    per_layer_quota: tuple[int, ...]

    @property
    def blocks_per_layer(self) -> int:
        return len(self.blocks)

    @property
    def total_candidate_blocks(self) -> int:
        return self.blocks_per_layer * LAYER_COUNT

    @property
    def total_selected_blocks(self) -> int:
        return sum(self.per_layer_quota)

    @property
    def total_selected_channels(self) -> int:
        return self.total_selected_blocks * self.block_size

    @property
    def quota_pattern_hash(self) -> str:
        return stable_hash(
            {
                "schema_version": MAPPING_SCHEMA_VERSION,
                "block_size": self.block_size,
                "per_layer_quota": self.per_layer_quota,
            }
        )

    @property
    def mapping_hash(self) -> str:
        return stable_hash(self._payload())

    def _payload(self) -> dict[str, Any]:
        return {
            "schema_version": MAPPING_SCHEMA_VERSION,
            "block_size": self.block_size,
            "intermediate_size": INTERMEDIATE_SIZE,
            "layer_count": LAYER_COUNT,
            "blocks_per_layer": self.blocks_per_layer,
            "blocks": [block.to_dict() for block in self.blocks],
            "per_layer_quota": list(self.per_layer_quota),
            "total_candidate_blocks": self.total_candidate_blocks,
            "total_selected_blocks": self.total_selected_blocks,
            "total_selected_channels": self.total_selected_channels,
            "total_layer_channels": TOTAL_LAYER_CHANNELS,
            "total_fraction": self.total_selected_channels / TOTAL_LAYER_CHANNELS,
            "mask_semantics": "ABLATE_SELECTED",
            "quota_pattern_sha256": self.quota_pattern_hash,
        }

    def to_dict(self) -> dict[str, Any]:
        payload = self._payload()
        payload["mapping_sha256"] = stable_hash(payload)
        return payload

    @classmethod
    def from_json(cls, path: str | Path) -> BlockMapping:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        mapping = cls(
            block_size=int(payload["block_size"]),  # type: ignore[arg-type]
            blocks=tuple(
                BlockRange(
                    block_index=int(item["block_index"]),
                    start_channel=int(item["start_channel"]),
                    stop_channel=int(item["stop_channel"]),
                )
                for item in payload["blocks"]
            ),
            per_layer_quota=tuple(int(value) for value in payload["per_layer_quota"]),
        )
        validate_mapping(mapping)
        if payload != mapping.to_dict():
            raise ValueError(f"mapping artifact is noncanonical or modified: {path}")
        return mapping


def build_mapping(block_size: BlockSize) -> BlockMapping:
    if INTERMEDIATE_SIZE % block_size:
        raise ValueError(f"block size {block_size} does not partition {INTERMEDIATE_SIZE}")
    blocks = tuple(
        BlockRange(index, index * block_size, (index + 1) * block_size)
        for index in range(INTERMEDIATE_SIZE // block_size)
    )
    quota = (
        (7,) * LAYER_COUNT
        if block_size == 64
        else tuple(4 if layer % 2 == 0 else 3 for layer in range(LAYER_COUNT))
    )
    mapping = BlockMapping(block_size, blocks, quota)
    validate_mapping(mapping)
    return mapping


def validate_mapping(mapping: BlockMapping) -> None:
    if mapping.block_size not in {64, 128}:
        raise ValueError(f"unsupported block size: {mapping.block_size}")
    if len(mapping.per_layer_quota) != LAYER_COUNT:
        raise ValueError("quota vector must contain exactly 28 layers")
    if mapping.block_size == 64 and mapping.per_layer_quota != (7,) * LAYER_COUNT:
        raise ValueError("64-channel quota must select seven blocks in every layer")
    expected_128 = tuple(4 if layer % 2 == 0 else 3 for layer in range(LAYER_COUNT))
    if mapping.block_size == 128 and mapping.per_layer_quota != expected_128:
        raise ValueError("128-channel quota must be four in even and three in odd layers")
    expected_ranges = [
        (index, index * mapping.block_size, (index + 1) * mapping.block_size)
        for index in range(INTERMEDIATE_SIZE // mapping.block_size)
    ]
    observed_ranges = [
        (block.block_index, block.start_channel, block.stop_channel) for block in mapping.blocks
    ]
    if observed_ranges != expected_ranges:
        raise ValueError("block mapping must cover channels contiguously in index order")
    coverage = [0] * INTERMEDIATE_SIZE
    for block in mapping.blocks:
        for channel in range(block.start_channel, block.stop_channel):
            coverage[channel] += 1
    if set(coverage) != {1}:
        raise ValueError("channel mapping contains a gap or overlap")
    if mapping.total_selected_channels != SELECTED_CHANNELS:
        raise ValueError("mapping does not ablate exactly 12,544 channels")
    if mapping.total_selected_channels / TOTAL_LAYER_CHANNELS != 0.05:
        raise ValueError("mapping does not ablate exactly five percent")


def write_mapping_artifacts(directory: str | Path) -> list[Path]:
    output = Path(directory)
    output.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for block_size in (64, 128):
        mapping = build_mapping(block_size)
        path = output / f"causal_importance_block{block_size}_v1.json"
        path.write_text(
            json.dumps(mapping.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        paths.append(path)
    return paths
