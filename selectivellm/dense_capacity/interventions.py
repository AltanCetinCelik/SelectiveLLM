"""Typed logical masks and reversible inference-time interventions."""

from __future__ import annotations

import hashlib
import inspect
import json
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Any, Literal

Granularity = Literal["mlp", "head", "layer"]
MaskSemantics = Literal["ABLATE_SELECTED", "RETAIN_SELECTED"]


@dataclass(frozen=True)
class LogicalMask:
    name: str
    granularity: Granularity
    mask_semantics: MaskSemantics
    source: str
    source_domain: str | None
    selected_by_layer: dict[int, list[int]]
    fraction: float
    seed: int | None = None

    @property
    def component_count(self) -> int:
        if self.granularity == "layer":
            return len(self.selected_by_layer)
        return sum(len(indices) for indices in self.selected_by_layer.values())

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "granularity": self.granularity,
            "mask_semantics": self.mask_semantics,
            "source": self.source,
            "source_split": (
                "discovery"
                if self.source
                in {
                    "domain_selectivity",
                    "global_low_importance",
                    "global_high_importance",
                    "global_importance",
                }
                else None
            ),
            "source_domain": self.source_domain,
            "selected_by_layer": {
                str(layer): sorted(indices)
                for layer, indices in sorted(self.selected_by_layer.items())
            },
            "per_layer_counts": {
                str(layer): len(indices)
                for layer, indices in sorted(self.selected_by_layer.items())
            },
            "component_count": self.component_count,
            "fraction": self.fraction,
            "seed": self.seed,
        }
        payload["content_sha256"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return payload


def validate_mask_structure(mask: LogicalMask, *, layer_count: int = 28) -> None:
    if any(layer < 0 or layer >= layer_count for layer in mask.selected_by_layer):
        raise ValueError(f"mask {mask.name} contains invalid layer")
    if mask.granularity == "mlp":
        counts = [len(mask.selected_by_layer.get(layer, [])) for layer in range(layer_count)]
        if len(set(counts)) != 1:
            raise ValueError(f"MLP mask {mask.name} does not preserve per-layer quotas")
        if any(
            index < 0 or index >= 8960
            for items in mask.selected_by_layer.values()
            for index in items
        ):
            raise ValueError(f"MLP mask {mask.name} contains invalid channel")
    elif mask.granularity == "head":
        counts = [len(mask.selected_by_layer.get(layer, [])) for layer in range(layer_count)]
        if len(set(counts)) != 1:
            raise ValueError(f"head mask {mask.name} does not preserve per-layer quotas")
        if any(
            index < 0 or index >= 12 for items in mask.selected_by_layer.values() for index in items
        ):
            raise ValueError(f"head mask {mask.name} contains invalid head")
    elif any(indices != [0] for indices in mask.selected_by_layer.values()):
        raise ValueError(f"layer mask {mask.name} must use one identity marker per layer")
    if any(len(indices) != len(set(indices)) for indices in mask.selected_by_layer.values()):
        raise ValueError(f"mask {mask.name} contains duplicate indices")


class Intervention(AbstractContextManager["Intervention"]):
    def __init__(self, model: Any, mask: LogicalMask) -> None:
        self.model = model
        self.mask = mask
        self.handles: list[Any] = []
        self.layer_inputs: dict[int, Any] = {}
        self.events: list[dict[str, Any]] = []

    def __enter__(self) -> Intervention:
        validate_mask_structure(self.mask)
        if self.mask.granularity == "mlp":
            for layer_index, layer in enumerate(self.model.model.layers):
                selected = self._suppressed_indices(layer_index, 8960)
                self.handles.append(
                    layer.mlp.down_proj.register_forward_pre_hook(
                        self._projection_hook(layer_index, selected, "mlp")
                    )
                )
        elif self.mask.granularity == "head":
            for layer_index, layer in enumerate(self.model.model.layers):
                selected_heads = self._suppressed_indices(layer_index, 12)
                selected = [
                    index
                    for head in selected_heads
                    for index in range(head * 128, (head + 1) * 128)
                ]
                self.handles.append(
                    layer.self_attn.o_proj.register_forward_pre_hook(
                        self._projection_hook(layer_index, selected, "head")
                    )
                )
        else:
            selected_layers = set(self._suppressed_layer_indices())
            for layer_index in selected_layers:
                layer = self.model.model.layers[layer_index]
                self.handles.append(
                    layer.register_forward_pre_hook(self._layer_pre_hook(layer_index))
                )
                self.handles.append(layer.register_forward_hook(self._layer_hook(layer_index)))
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        del exc_type, exc_value, traceback
        for handle in self.handles:
            handle.remove()
        self.handles.clear()
        self.layer_inputs.clear()

    def _suppressed_indices(self, layer: int, width: int) -> list[int]:
        selected = set(self.mask.selected_by_layer.get(layer, []))
        if self.mask.mask_semantics == "ABLATE_SELECTED":
            return sorted(selected)
        return [index for index in range(width) if index not in selected]

    def _suppressed_layer_indices(self) -> list[int]:
        selected = set(self.mask.selected_by_layer)
        if self.mask.mask_semantics == "ABLATE_SELECTED":
            return sorted(selected)
        return [index for index in range(28) if index not in selected]

    def _projection_hook(self, layer_index: int, selected: list[int], granularity: str) -> Any:
        def hook(module: Any, args: tuple[Any, ...]) -> tuple[Any, ...] | None:
            del module
            if not selected:
                return None
            tensor = args[0]
            indices = self.model.device.type
            index_tensor = tensor.new_tensor(selected).long()
            masked = tensor.index_fill(-1, index_tensor, 0)
            self.events.append(
                {
                    "granularity": granularity,
                    "layer": layer_index,
                    "suppressed_count": len(selected),
                    "shape": list(tensor.shape),
                    "dtype": str(tensor.dtype),
                    "device": str(tensor.device),
                    "model_device_type": indices,
                }
            )
            return (masked, *args[1:])

        return hook

    def _layer_pre_hook(self, layer_index: int) -> Any:
        def hook(module: Any, args: tuple[Any, ...]) -> None:
            del module
            self.layer_inputs[layer_index] = args[0]

        return hook

    def _layer_hook(self, layer_index: int) -> Any:
        def hook(module: Any, args: tuple[Any, ...], output: Any) -> Any:
            del module, args
            residual = self.layer_inputs.pop(layer_index)
            if not hasattr(output, "shape"):
                raise TypeError(
                    f"pinned use_cache=False layer output must be a tensor, got {type(output)}"
                )
            if output.shape != residual.shape:
                raise ValueError("layer identity bypass shape mismatch")
            if output.dtype != residual.dtype or output.device != residual.device:
                raise ValueError("layer identity bypass dtype/device mismatch")
            self.events.append(
                {
                    "granularity": "layer",
                    "layer": layer_index,
                    "suppressed_count": 1,
                    "input_shape": list(residual.shape),
                    "output_shape": list(output.shape),
                    "dtype": str(residual.dtype),
                    "device": str(residual.device),
                    "return_structure": type(output).__name__,
                }
            )
            return residual

        return hook


def validate_attention_contract(model: Any, observed: Any) -> dict[str, Any]:
    config = model.config
    attention = model.model.layers[0].self_attn
    source = inspect.getsource(type(attention).forward)
    query_heads = int(config.num_attention_heads)
    head_dim = int(attention.head_dim)
    expected_width = query_heads * head_dim
    source_contract = all(
        fragment in source
        for fragment in (
            "attn_output.reshape(*input_shape, -1).contiguous()",
            "attn_output = self.o_proj(attn_output)",
        )
    )
    runtime_width = int(observed.shape[-1])
    heads = observed.reshape(*observed.shape[:-1], query_heads, head_dim)
    reconstructed = heads.reshape_as(observed)
    reconstruction_exact = bool(model.device.type and reconstructed.equal(observed))
    valid = bool(
        query_heads == 12
        and head_dim == 128
        and expected_width == 1536
        and runtime_width == 1536
        and observed.is_contiguous()
        and reconstruction_exact
        and source_contract
    )
    return {
        "status": "valid" if valid else "unsupported",
        "query_head_count": query_heads,
        "kv_head_count": int(config.num_key_value_heads),
        "head_dimension": head_dim,
        "expected_o_proj_input_width": expected_width,
        "observed_o_proj_input_shape": list(observed.shape),
        "observed_contiguous": bool(observed.is_contiguous()),
        "contiguous_slice_reconstruction_exact": reconstruction_exact,
        "implementation_source_contract": source_contract,
        "attention_forward_source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "kv_heads_interpreted_as_output_heads": False,
    }
