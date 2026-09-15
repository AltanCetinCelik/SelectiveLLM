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
QWEN3B_INTERMEDIATE_SIZE = 11_008
QWEN3B_LAYER_COUNT = 36


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
    intermediate_size: int = INTERMEDIATE_SIZE
    layer_count: int = LAYER_COUNT

    @property
    def blocks_per_layer(self) -> int:
        return len(self.blocks)

    @property
    def total_candidate_blocks(self) -> int:
        return self.blocks_per_layer * self.layer_count

    @property
    def total_selected_blocks(self) -> int:
        return sum(self.per_layer_quota)

    @property
    def total_selected_channels(self) -> int:
        return self.total_selected_blocks * self.block_size

    @property
    def total_layer_channels(self) -> int:
        return self.intermediate_size * self.layer_count

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
            "intermediate_size": self.intermediate_size,
            "layer_count": self.layer_count,
            "blocks_per_layer": self.blocks_per_layer,
            "blocks": [block.to_dict() for block in self.blocks],
            "per_layer_quota": list(self.per_layer_quota),
            "total_candidate_blocks": self.total_candidate_blocks,
            "total_selected_blocks": self.total_selected_blocks,
            "total_selected_channels": self.total_selected_channels,
            "total_layer_channels": self.total_layer_channels,
            "total_fraction": self.total_selected_channels / self.total_layer_channels,
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
            intermediate_size=int(payload["intermediate_size"]),
            layer_count=int(payload["layer_count"]),
        )
        validate_mapping(mapping)
        if payload != mapping.to_dict():
            raise ValueError(f"mapping artifact is noncanonical or modified: {path}")
        return mapping


def _balanced_quota(total_blocks: int, layer_count: int) -> tuple[int, ...]:
    return tuple(
        ((layer + 1) * total_blocks) // layer_count - (layer * total_blocks) // layer_count
        for layer in range(layer_count)
    )


def _frozen_quota(
    block_size: BlockSize, intermediate_size: int, layer_count: int
) -> tuple[int, ...]:
    geometry = (intermediate_size, layer_count)
    if geometry == (INTERMEDIATE_SIZE, LAYER_COUNT):
        return (
            (7,) * LAYER_COUNT
            if block_size == 64
            else tuple(4 if layer % 2 == 0 else 3 for layer in range(LAYER_COUNT))
        )
    if geometry == (QWEN3B_INTERMEDIATE_SIZE, QWEN3B_LAYER_COUNT):
        selected_blocks = 310 if block_size == 64 else 155
        return _balanced_quota(selected_blocks, QWEN3B_LAYER_COUNT)
    raise ValueError(f"no preregistered quota for model geometry {geometry}")


def build_mapping(
    block_size: BlockSize,
    *,
    intermediate_size: int = INTERMEDIATE_SIZE,
    layer_count: int = LAYER_COUNT,
) -> BlockMapping:
    if intermediate_size % block_size:
        raise ValueError(f"block size {block_size} does not partition {intermediate_size}")
    blocks = tuple(
        BlockRange(index, index * block_size, (index + 1) * block_size)
        for index in range(intermediate_size // block_size)
    )
    quota = _frozen_quota(block_size, intermediate_size, layer_count)
    mapping = BlockMapping(block_size, blocks, quota, intermediate_size, layer_count)
    validate_mapping(mapping)
    return mapping


def validate_mapping(mapping: BlockMapping) -> None:
    if mapping.block_size not in {64, 128}:
        raise ValueError(f"unsupported block size: {mapping.block_size}")
    if len(mapping.per_layer_quota) != mapping.layer_count:
        raise ValueError(f"quota vector must contain exactly {mapping.layer_count} layers")
    expected_quota = _frozen_quota(
        mapping.block_size, mapping.intermediate_size, mapping.layer_count
    )
    if mapping.per_layer_quota != expected_quota:
        raise ValueError("quota vector does not match the preregistered model geometry")
    expected_ranges = [
        (index, index * mapping.block_size, (index + 1) * mapping.block_size)
        for index in range(mapping.intermediate_size // mapping.block_size)
    ]
    observed_ranges = [
        (block.block_index, block.start_channel, block.stop_channel) for block in mapping.blocks
    ]
    if observed_ranges != expected_ranges:
        raise ValueError("block mapping must cover channels contiguously in index order")
    coverage = [0] * mapping.intermediate_size
    for block in mapping.blocks:
        for channel in range(block.start_channel, block.stop_channel):
            coverage[channel] += 1
    if set(coverage) != {1}:
        raise ValueError("channel mapping contains a gap or overlap")
    expected_channels = (
        12_544
        if (mapping.intermediate_size, mapping.layer_count) == (INTERMEDIATE_SIZE, LAYER_COUNT)
        else 19_840
    )
    if mapping.total_selected_channels != expected_channels:
        raise ValueError("mapping does not match the preregistered capacity footprint")


def write_mapping_artifacts(
    directory: str | Path,
    *,
    intermediate_size: int = INTERMEDIATE_SIZE,
    layer_count: int = LAYER_COUNT,
    filename_prefix: str = "causal_importance",
) -> list[Path]:
    output = Path(directory)
    output.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for block_size in (64, 128):
        mapping = build_mapping(
            block_size, intermediate_size=intermediate_size, layer_count=layer_count
        )
        path = output / f"{filename_prefix}_block{block_size}_v1.json"
        path.write_text(
            json.dumps(mapping.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        paths.append(path)
    return paths
