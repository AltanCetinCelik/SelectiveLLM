"""Structurally matched contiguous-block masks and reversible MLP ablation."""

from __future__ import annotations

import hashlib
import json
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Any, Literal

from selectivellm.causal_importance.mappings import LAYER_COUNT, BlockMapping

DiscoveryMethod = Literal["activation", "gradient", "shared_control"]
MaskSource = Literal[
    "domain_selectivity",
    "global_high",
    "global_low",
    "random",
    "noop",
]


@dataclass(frozen=True)
class BlockMask:
    name: str
    block_size: int
    discovery_method: DiscoveryMethod
    source: MaskSource
    source_domain: str | None
    selected_blocks_by_layer: dict[int, list[int]]
    mapping_sha256: str
    quota_pattern_sha256: str
    mask_semantics: Literal["ABLATE_SELECTED"] = "ABLATE_SELECTED"
    seed: int | None = None

    @property
    def selected_block_count(self) -> int:
        return sum(len(blocks) for blocks in self.selected_blocks_by_layer.values())

    @property
    def selected_channel_count(self) -> int:
        return self.selected_block_count * self.block_size

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "block_size": self.block_size,
            "discovery_method": self.discovery_method,
            "source": self.source,
            "source_domain": self.source_domain,
            "source_split": "discovery"
            if self.source in {"domain_selectivity", "global_high", "global_low"}
            else None,
            "selected_blocks_by_layer": {
                str(layer): sorted(blocks)
                for layer, blocks in sorted(self.selected_blocks_by_layer.items())
            },
            "per_layer_counts": {
                str(layer): len(self.selected_blocks_by_layer.get(layer, []))
                for layer in range(LAYER_COUNT)
            },
            "selected_block_count": self.selected_block_count,
            "selected_channel_count": self.selected_channel_count,
            "total_fraction": self.selected_channel_count / (LAYER_COUNT * 8960),
            "mapping_sha256": self.mapping_sha256,
            "quota_pattern_sha256": self.quota_pattern_sha256,
            "mask_semantics": self.mask_semantics,
            "seed": self.seed,
        }
        payload["mask_sha256"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return payload


def validate_block_mask(mask: BlockMask, mapping: BlockMapping) -> None:
    if mask.block_size != mapping.block_size:
        raise ValueError(f"mask {mask.name} block size does not match mapping")
    if mask.mapping_sha256 != mapping.mapping_hash:
        raise ValueError(f"mask {mask.name} mapping hash does not match")
    if mask.quota_pattern_sha256 != mapping.quota_pattern_hash:
        raise ValueError(f"mask {mask.name} quota hash does not match")
    if mask.mask_semantics != "ABLATE_SELECTED":
        raise ValueError(f"mask {mask.name} has ambiguous semantics")
    if mask.source == "noop":
        if mask.selected_blocks_by_layer or mask.selected_channel_count:
            raise ValueError("no-op mask must select zero blocks")
        return
    if set(mask.selected_blocks_by_layer) != set(range(LAYER_COUNT)):
        raise ValueError(f"mask {mask.name} must specify all 28 layers")
    observed_quota = tuple(
        len(mask.selected_blocks_by_layer[layer]) for layer in range(LAYER_COUNT)
    )
    if observed_quota != mapping.per_layer_quota:
        raise ValueError(f"mask {mask.name} violates the frozen per-layer quota")
    for layer, blocks in mask.selected_blocks_by_layer.items():
        if len(blocks) != len(set(blocks)):
            raise ValueError(f"mask {mask.name} repeats a block in layer {layer}")
        if any(block < 0 or block >= mapping.blocks_per_layer for block in blocks):
            raise ValueError(f"mask {mask.name} has an invalid block in layer {layer}")
    if mask.selected_channel_count != 12_544:
        raise ValueError(f"mask {mask.name} does not select exactly five percent")


def expanded_channels(mask: BlockMask, mapping: BlockMapping, layer: int) -> list[int]:
    channels: list[int] = []
    for block_index in mask.selected_blocks_by_layer.get(layer, []):
        block = mapping.blocks[block_index]
        channels.extend(range(block.start_channel, block.stop_channel))
    return channels


class BlockIntervention(AbstractContextManager["BlockIntervention"]):
    def __init__(self, model: Any, mask: BlockMask, mapping: BlockMapping) -> None:
        self.model = model
        self.mask = mask
        self.mapping = mapping
        self.handles: list[Any] = []
        self.events: list[dict[str, Any]] = []

    def __enter__(self) -> BlockIntervention:
        validate_block_mask(self.mask, self.mapping)
        for layer_index, layer in enumerate(self.model.model.layers):
            channels = expanded_channels(self.mask, self.mapping, layer_index)
            self.handles.append(
                layer.mlp.down_proj.register_forward_pre_hook(self._hook(layer_index, channels))
            )
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        del exc_type, exc_value, traceback
        for handle in self.handles:
            handle.remove()
        self.handles.clear()

    def _hook(self, layer_index: int, channels: list[int]) -> Any:
        def hook(module: Any, args: tuple[Any, ...]) -> tuple[Any, ...] | None:
            del module
            if not channels:
                return None
            tensor = args[0]
            if tensor.shape[-1] != 8960:
                raise ValueError("MLP intervention target width is not 8,960")
            indices = tensor.new_tensor(channels).long()
            masked = tensor.index_fill(-1, indices, 0)
            self.events.append(
                {
                    "layer": layer_index,
                    "block_count": len(channels) // self.mapping.block_size,
                    "channel_count": len(channels),
                    "shape": list(tensor.shape),
                    "dtype": str(tensor.dtype),
                    "device": str(tensor.device),
                }
            )
            return (masked, *args[1:])

        return hook
