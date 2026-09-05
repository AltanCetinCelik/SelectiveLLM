"""One-pass MLP activation and objective-gradient measurement."""

from __future__ import annotations

import math
from contextlib import AbstractContextManager
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray

from selectivellm.dense_capacity.benchmark import LABELS, DenseBenchmarkCase
from selectivellm.dense_capacity.scoring import ForcedChoiceScorer

FloatArray = NDArray[np.float32]


class GradientCompatibleScorer(ForcedChoiceScorer):
    """Score through the same MPS execution path used for gradient measurement."""

    def score(self, case: DenseBenchmarkCase) -> dict[str, Any]:
        torch = self.torch
        if set(self.option_token_ids) != set(LABELS):
            raise RuntimeError("validate tokenizer protocol before scoring")
        if any(parameter.requires_grad for parameter in self.model.parameters()):
            raise RuntimeError("gradient-compatible scoring requires frozen model parameters")
        inputs, _ = self.tensors(case)
        with torch.no_grad():
            embeddings = self.model.get_input_embeddings()(inputs["input_ids"])
        embeddings = embeddings.detach().requires_grad_(True)
        with torch.enable_grad():
            output = self.model(
                inputs_embeds=embeddings,
                attention_mask=inputs["attention_mask"],
                use_cache=False,
            )
            final_logits = output.logits[0, -1]
            option_logits = torch.stack(
                [final_logits[self.option_token_ids[label]] for label in LABELS]
            ).float()
            log_probabilities = torch.log_softmax(option_logits, dim=0)
            probabilities = torch.softmax(option_logits, dim=0)
            correct_index = LABELS.index(case.correct_label)
            correct_nll = -log_probabilities[correct_index]

        raw_logits = option_logits.detach().cpu().tolist()
        probability_values = probabilities.detach().cpu().tolist()
        values = [*raw_logits, *probability_values, float(correct_nll.detach().cpu())]
        if not all(math.isfinite(float(value)) for value in values):
            raise FloatingPointError(f"nonfinite gradient-compatible score for {case.id}")
        probability_sum = float(sum(probability_values))
        if not math.isclose(probability_sum, 1.0, rel_tol=0, abs_tol=1e-6):
            raise ValueError(f"option probabilities do not sum to one for {case.id}")
        by_label = {label: float(probability_values[index]) for index, label in enumerate(LABELS)}
        logits_by_label = {label: float(raw_logits[index]) for index, label in enumerate(LABELS)}
        prediction = max(LABELS, key=lambda label: (by_label[label], -LABELS.index(label)))
        return {
            "case_id": case.id,
            "domain": case.domain,
            "split": case.split,
            "correct_label": case.correct_label,
            "option_token_ids": dict(self.option_token_ids),
            "option_logits": logits_by_label,
            "option_probabilities": by_label,
            "probability_sum": probability_sum,
            "correct_probability": by_label[case.correct_label],
            "correct_nll": float(correct_nll.detach().cpu()),
            "prediction": prediction,
            "correct": prediction == case.correct_label,
            "scoring_semantics": "restricted_four_option_softmax",
            "execution_semantics": "detached_inputs_embeds_gradient_enabled_no_backward",
        }


class GradientMeasurement(AbstractContextManager["GradientMeasurement"]):
    def __init__(self, scorer: ForcedChoiceScorer) -> None:
        self.scorer = scorer
        self.model = scorer.model
        self.handles: list[Any] = []
        self.activations: list[Any] = []
        self.original_requires_grad: list[bool] = []

    def __enter__(self) -> GradientMeasurement:
        self.original_requires_grad = [
            bool(parameter.requires_grad) for parameter in self.model.parameters()
        ]
        for parameter in self.model.parameters():
            parameter.requires_grad_(False)
        for layer_index, layer in enumerate(self.model.model.layers):
            self.handles.append(
                layer.mlp.down_proj.register_forward_pre_hook(self._capture(layer_index))
            )
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        del exc_type, exc_value, traceback
        for handle in self.handles:
            handle.remove()
        self.handles.clear()
        for parameter, requires_grad in zip(
            self.model.parameters(), self.original_requires_grad, strict=True
        ):
            parameter.requires_grad_(requires_grad)
        self.activations.clear()

    def measure(self, case: DenseBenchmarkCase) -> dict[str, Any]:
        torch = self.scorer.torch
        if set(self.scorer.option_token_ids) != set(LABELS):
            raise RuntimeError("validate tokenizer protocol before gradient measurement")
        inputs, eligible = self.scorer.tensors(case)
        with torch.no_grad():
            embeddings = self.model.get_input_embeddings()(inputs["input_ids"])
        embeddings = embeddings.detach().requires_grad_(True)
        self.activations = [None] * 28
        self.model.zero_grad(set_to_none=True)
        with torch.enable_grad():
            output = self.model(
                inputs_embeds=embeddings,
                attention_mask=inputs["attention_mask"],
                use_cache=False,
            )
            final_logits = output.logits[0, -1]
            option_logits = torch.stack(
                [final_logits[self.scorer.option_token_ids[label]] for label in LABELS]
            ).float()
            log_probabilities = torch.log_softmax(option_logits, dim=0)
            correct_index = LABELS.index(case.correct_label)
            correct_nll = -log_probabilities[correct_index]
            correct_nll.backward()

        if any(activation is None for activation in self.activations):
            raise RuntimeError(f"incomplete MLP activation capture for {case.id}")
        eligible_tensor = torch.tensor(eligible, dtype=torch.bool, device=self.scorer.device)
        summaries: dict[str, list[FloatArray]] = {
            "activation": [],
            "gradient_absolute": [],
            "gradient_signed_sum": [],
            "gradient_signed_mean": [],
        }
        shape_records: list[dict[str, Any]] = []
        for layer_index, activation in enumerate(self.activations):
            gradient = activation.grad
            if gradient is None:
                raise RuntimeError(f"missing MLP gradient for {case.id}/layer {layer_index}")
            if activation.shape != gradient.shape:
                raise ValueError(
                    f"activation/gradient shape mismatch for {case.id}/layer {layer_index}"
                )
            if activation.ndim != 3 or activation.shape[0] != 1 or activation.shape[-1] != 8960:
                raise ValueError(f"invalid MLP tensor shape for {case.id}/layer {layer_index}")
            if activation.shape[1] != eligible_tensor.shape[0]:
                raise ValueError(f"eligible-token shape mismatch for {case.id}/layer {layer_index}")
            selected_activation = activation[:, eligible_tensor, :].float()
            selected_gradient = gradient[:, eligible_tensor, :].float()
            product = selected_activation * selected_gradient
            tensors = {
                "activation": selected_activation.abs().mean(dim=(0, 1)),
                "gradient_absolute": product.abs().mean(dim=(0, 1)),
                "gradient_signed_sum": (-product).sum(dim=(0, 1)),
                "gradient_signed_mean": (-product).mean(dim=(0, 1)),
            }
            for name, tensor in tensors.items():
                if not bool(torch.isfinite(tensor).all().item()):
                    raise FloatingPointError(f"nonfinite {name} for {case.id}/layer {layer_index}")
                summaries[name].append(tensor.detach().cpu().numpy().astype(np.float32))
            shape_records.append(
                {
                    "layer": layer_index,
                    "activation_shape": list(activation.shape),
                    "gradient_shape": list(gradient.shape),
                    "eligible_token_count": int(eligible_tensor.sum().item()),
                    "finite": True,
                }
            )

        probabilities = torch.softmax(option_logits.detach(), dim=0).cpu().tolist()
        raw_logits = option_logits.detach().cpu().tolist()
        if not all(math.isfinite(float(value)) for value in [*probabilities, *raw_logits]):
            raise FloatingPointError(f"nonfinite gradient-mode score for {case.id}")
        prediction_index = max(range(4), key=lambda index: (probabilities[index], -index))
        result = {
            "case_id": case.id,
            "domain": case.domain,
            "eligible_token_count": int(eligible_tensor.sum().item()),
            "option_logits": {
                label: float(raw_logits[index]) for index, label in enumerate(LABELS)
            },
            "option_probabilities": {
                label: float(probabilities[index]) for index, label in enumerate(LABELS)
            },
            "correct_nll": float(correct_nll.detach().cpu()),
            "prediction": LABELS[prediction_index],
            "shape_records": shape_records,
            "summaries": {
                name: np.stack(values).astype(np.float32) for name, values in summaries.items()
            },
        }
        self.activations.clear()
        self.model.zero_grad(set_to_none=True)
        return result

    def _capture(self, layer_index: int) -> Any:
        def hook(module: Any, args: tuple[Any, ...]) -> None:
            del module
            activation = args[0]
            if not activation.requires_grad:
                raise RuntimeError("captured MLP activation is not connected to gradient graph")
            activation.retain_grad()
            self.activations[layer_index] = activation

        return hook


def aggregate_blocks(channels: FloatArray, block_size: int) -> FloatArray:
    if channels.shape[-2:] != (28, 8960):
        raise ValueError(f"expected (..., 28, 8960), found {channels.shape}")
    if 8960 % block_size or block_size not in {64, 128}:
        raise ValueError(f"unsupported block size: {block_size}")
    shape = (*channels.shape[:-1], 8960 // block_size, block_size)
    return cast(
        FloatArray,
        channels.reshape(shape).sum(axis=-1, dtype=np.float32).astype(np.float32),
    )


def percentile_rank_blocks(values: FloatArray) -> FloatArray:
    if values.ndim != 3 or values.shape[1] != 28 or values.shape[2] not in {70, 140}:
        raise ValueError(f"invalid block activity shape: {values.shape}")
    order = np.argsort(values, axis=-1, kind="stable")
    ranks = np.empty_like(order, dtype=np.float32)
    rank_values = np.broadcast_to(np.arange(values.shape[-1], dtype=np.float32), order.shape)
    np.put_along_axis(ranks, order, rank_values, axis=-1)
    return (ranks / (values.shape[-1] - 1)).astype(np.float32)
