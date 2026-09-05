"""Prompt-level activation tracing at the three preregistered granularities."""

from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Any

import numpy as np
from numpy.typing import NDArray

from selectivellm.dense_capacity.benchmark import DenseBenchmarkCase
from selectivellm.dense_capacity.scoring import ForcedChoiceScorer


class ActivationTracer(AbstractContextManager["ActivationTracer"]):
    def __init__(self, model: Any, *, trace_heads: bool = True) -> None:
        self.model = model
        self.trace_heads = trace_heads
        self.handles: list[Any] = []
        self.eligible: Any | None = None
        self.mlp: list[Any] = []
        self.head: list[Any] = []
        self.layer: list[Any] = []
        self.layer_inputs: dict[int, Any] = {}

    def __enter__(self) -> ActivationTracer:
        for layer_index, layer in enumerate(self.model.model.layers):
            self.handles.append(
                layer.mlp.down_proj.register_forward_pre_hook(self._mlp_hook(layer_index))
            )
            if self.trace_heads:
                self.handles.append(
                    layer.self_attn.o_proj.register_forward_pre_hook(self._head_hook(layer_index))
                )
            self.handles.append(layer.register_forward_pre_hook(self._layer_pre_hook(layer_index)))
            self.handles.append(layer.register_forward_hook(self._layer_hook(layer_index)))
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        del exc_type, exc_value, traceback
        for handle in self.handles:
            handle.remove()
        self.handles.clear()
        self.layer_inputs.clear()

    def trace(
        self, scorer: ForcedChoiceScorer, case: DenseBenchmarkCase
    ) -> dict[str, NDArray[np.float32]]:
        inputs, eligible = scorer.tensors(case)
        self.eligible = scorer.torch.tensor(eligible, dtype=scorer.torch.bool, device=scorer.device)
        self.mlp = [None] * 28
        self.head = [None] * 28 if self.trace_heads else []
        self.layer = [None] * 28
        self.layer_inputs.clear()
        with scorer.torch.inference_mode():
            scorer.model(**inputs, use_cache=False)
        if any(value is None for value in [*self.mlp, *self.head, *self.layer]):
            raise RuntimeError(f"incomplete activation trace for {case.id}")
        output: dict[str, NDArray[np.float32]] = {
            "mlp": np.stack([value for value in self.mlp]).astype(np.float32),
            "layer": np.asarray(self.layer, dtype=np.float32),
        }
        if self.trace_heads:
            output["head"] = np.stack([value for value in self.head]).astype(np.float32)
        if output["mlp"].shape != (28, 8960):
            raise ValueError(f"unexpected MLP trace shape: {output['mlp'].shape}")
        if self.trace_heads and output["head"].shape != (28, 12):
            raise ValueError(f"unexpected head trace shape: {output['head'].shape}")
        if output["layer"].shape != (28,):
            raise ValueError(f"unexpected layer trace shape: {output['layer'].shape}")
        return output

    def _tokens(self, tensor: Any) -> Any:
        if self.eligible is None or tensor.shape[1] != self.eligible.shape[0]:
            raise ValueError("tracing token mask does not match activation sequence")
        return tensor[:, self.eligible, :]

    def _mlp_hook(self, layer_index: int) -> Any:
        def hook(module: Any, args: tuple[Any, ...]) -> None:
            del module
            values = self._tokens(args[0]).float().abs().mean(dim=(0, 1))
            self.mlp[layer_index] = values.detach().cpu().numpy()

        return hook

    def _head_hook(self, layer_index: int) -> Any:
        def hook(module: Any, args: tuple[Any, ...]) -> None:
            del module
            tensor = self._tokens(args[0]).float()
            if tensor.shape[-1] != 1536:
                raise ValueError("attention output width changed during tracing")
            heads = tensor.reshape(tensor.shape[0], tensor.shape[1], 12, 128)
            values = heads.square().mean(dim=(0, 1, 3)).sqrt()
            self.head[layer_index] = values.detach().cpu().numpy()

        return hook

    def _layer_pre_hook(self, layer_index: int) -> Any:
        def hook(module: Any, args: tuple[Any, ...]) -> None:
            del module
            self.layer_inputs[layer_index] = args[0]

        return hook

    def _layer_hook(self, layer_index: int) -> Any:
        def hook(module: Any, args: tuple[Any, ...], output: Any) -> None:
            del module, args
            before = self._tokens(self.layer_inputs.pop(layer_index)).float()
            after = self._tokens(output).float()
            value = (after - before).square().mean().sqrt()
            self.layer[layer_index] = float(value.detach().cpu())

        return hook
