"""Discovery-only selectivity, masks, overlap, and stability calculations."""

from __future__ import annotations

import itertools
from collections.abc import Sequence
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray

from selectivellm.dense_capacity.benchmark import DenseBenchmarkCase
from selectivellm.dense_capacity.interventions import LogicalMask, validate_mask_structure

DOMAINS = ("code", "mathematics", "science", "general")
GRANULARITIES = ("mlp", "head", "layer")
WIDTHS = {"mlp": 8960, "head": 12, "layer": 28}
QUOTAS = {"mlp": 448, "head": 1, "layer": 7}
FloatArray = NDArray[np.float32]
Float64Array = NDArray[np.float64]


def percentile_ranks(values: FloatArray) -> FloatArray:
    if values.ndim == 3:
        order = np.argsort(values, axis=-1, kind="stable")
        ranks = np.empty_like(order, dtype=np.float32)
        rank_values = np.broadcast_to(np.arange(values.shape[-1], dtype=np.float32), order.shape)
        np.put_along_axis(ranks, order, rank_values, axis=-1)
        return cast(FloatArray, ranks / max(1, values.shape[-1] - 1))
    if values.ndim == 2:
        order = np.argsort(values, axis=-1, kind="stable")
        ranks = np.empty_like(order, dtype=np.float32)
        rank_values = np.broadcast_to(np.arange(values.shape[-1], dtype=np.float32), order.shape)
        np.put_along_axis(ranks, order, rank_values, axis=-1)
        return cast(FloatArray, ranks / max(1, values.shape[-1] - 1))
    raise ValueError(f"unsupported activity shape: {values.shape}")


def selectivity(normalized: FloatArray, domains: Sequence[str], target_domain: str) -> FloatArray:
    target = normalized[np.asarray([domain == target_domain for domain in domains])]
    other = normalized[np.asarray([domain != target_domain for domain in domains])]
    numerator = target.mean(axis=0) - other.mean(axis=0)
    denominator = np.sqrt(0.5 * (target.var(axis=0) + other.var(axis=0)) + 1e-6)
    return cast(FloatArray, (numerator / denominator).astype(np.float32))


def selected_indices(scores: FloatArray, granularity: str, quota: int) -> dict[int, list[int]]:
    if granularity in {"mlp", "head"}:
        return {
            layer: np.argsort(scores[layer], kind="stable")[-quota:][::-1].astype(int).tolist()
            for layer in range(28)
        }
    layers = np.argsort(scores, kind="stable")[-quota:][::-1].astype(int).tolist()
    return {layer: [0] for layer in layers}


def _selected_set(selected: dict[int, list[int]], granularity: str) -> set[int]:
    width = WIDTHS[granularity]
    if granularity == "layer":
        return set(selected)
    return {layer * width + index for layer, indices in selected.items() for index in indices}


def _jaccard(left: set[int], right: set[int]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def _ordinal_ranks(values: FloatArray) -> Float64Array:
    order = np.argsort(values.reshape(-1), kind="stable")
    ranks = np.empty_like(order, dtype=np.float64)
    ranks[order] = np.arange(len(order), dtype=np.float64)
    return ranks


def _spearman(left: FloatArray, right: FloatArray) -> float:
    left_rank = _ordinal_ranks(left)
    right_rank = _ordinal_ranks(right)
    if left_rank.std() == 0 or right_rank.std() == 0:
        return 0.0
    return float(np.corrcoef(left_rank, right_rank)[0, 1])


def _pairwise_overlap(sets: list[set[int]]) -> float:
    pairs = list(itertools.combinations(sets, 2))
    return float(np.mean([_jaccard(left, right) for left, right in pairs])) if pairs else 0.0


def build_discovery(
    raw: dict[str, FloatArray], cases: list[DenseBenchmarkCase]
) -> tuple[dict[str, FloatArray], list[LogicalMask], dict[str, Any]]:
    if len(cases) != 48 or any(case.split != "discovery" for case in cases):
        raise ValueError("discovery analysis requires exactly 48 discovery cases")
    domains = [case.domain for case in cases]
    granularities = tuple(name for name in GRANULARITIES if name in raw)
    if not {"mlp", "layer"}.issubset(granularities):
        raise ValueError("MLP and layer discovery activities are required")
    normalized = {name: percentile_ranks(raw[name]) for name in granularities}
    rankings: dict[str, FloatArray] = {}
    masks: list[LogicalMask] = []

    for granularity in granularities:
        for domain in DOMAINS:
            scores = selectivity(normalized[granularity], domains, domain)
            rankings[f"{granularity}_{domain}_selectivity"] = scores
            mask = LogicalMask(
                name=f"{granularity}_domain_{domain}",
                granularity=granularity,  # type: ignore[arg-type]
                mask_semantics="ABLATE_SELECTED",
                source="domain_selectivity",
                source_domain=domain,
                selected_by_layer=selected_indices(scores, granularity, QUOTAS[granularity]),
                fraction=QUOTAS[granularity] / WIDTHS[granularity],
            )
            validate_mask_structure(mask)
            masks.append(mask)

        importance = normalized[granularity].mean(axis=0)
        rankings[f"{granularity}_global_importance"] = importance
        low = selected_indices(-importance, granularity, QUOTAS[granularity])
        low_mask = LogicalMask(
            name=f"{granularity}_global_low",
            granularity=granularity,  # type: ignore[arg-type]
            mask_semantics="ABLATE_SELECTED",
            source="global_low_importance",
            source_domain=None,
            selected_by_layer=low,
            fraction=QUOTAS[granularity] / WIDTHS[granularity],
        )
        validate_mask_structure(low_mask)
        masks.append(low_mask)
        if granularity == "mlp":
            high_mask = LogicalMask(
                name="mlp_global_high",
                granularity="mlp",
                mask_semantics="ABLATE_SELECTED",
                source="global_high_importance",
                source_domain=None,
                selected_by_layer=selected_indices(importance, granularity, QUOTAS[granularity]),
                fraction=QUOTAS[granularity] / WIDTHS[granularity],
            )
            validate_mask_structure(high_mask)
            masks.append(high_mask)
        for seed in range(42, 47):
            rng = np.random.default_rng(seed)
            if granularity in {"mlp", "head"}:
                selected = {
                    layer: sorted(
                        rng.choice(WIDTHS[granularity], QUOTAS[granularity], replace=False)
                        .astype(int)
                        .tolist()
                    )
                    for layer in range(28)
                }
            else:
                selected = {
                    int(layer): [0] for layer in sorted(rng.choice(28, 7, replace=False).tolist())
                }
            random_mask = LogicalMask(
                name=f"{granularity}_random_{seed}",
                granularity=granularity,  # type: ignore[arg-type]
                mask_semantics="ABLATE_SELECTED",
                source="random",
                source_domain=None,
                selected_by_layer=selected,
                fraction=QUOTAS[granularity] / WIDTHS[granularity],
                seed=seed,
            )
            validate_mask_structure(random_mask)
            masks.append(random_mask)

    stability = stability_analysis(normalized, domains)
    stability["mask_overlap"] = mask_overlap(masks)
    stability["selected_component_layer_histograms"] = {
        granularity: {
            domain: {
                str(layer): len(
                    next(
                        mask
                        for mask in masks
                        if mask.granularity == granularity
                        and mask.source_domain == domain
                        and mask.source == "domain_selectivity"
                    ).selected_by_layer.get(layer, [])
                )
                for layer in range(28)
            }
            for domain in DOMAINS
        }
        for granularity in granularities
    }
    return rankings, masks, stability


def stability_analysis(normalized: dict[str, FloatArray], domains: Sequence[str]) -> dict[str, Any]:
    rng = np.random.default_rng(42)
    indices_by_domain = {
        domain: np.asarray([index for index, item in enumerate(domains) if item == domain])
        for domain in DOMAINS
    }
    output: dict[str, Any] = {"split_seed": 42, "split_count": 20, "granularities": {}}
    for granularity in (item for item in GRANULARITIES if item in normalized):
        values = normalized[granularity]
        quota = QUOTAS[granularity]
        domain_output: dict[str, Any] = {}
        prompt_sets = [
            _selected_set(selected_indices(values[index], granularity, quota), granularity)
            for index in range(len(domains))
        ]
        for target_domain in DOMAINS:
            jaccards: list[float] = []
            spearmans: list[float] = []
            for _ in range(20):
                halves: dict[str, tuple[NDArray[np.int64], NDArray[np.int64]]] = {}
                for domain in DOMAINS:
                    permuted = rng.permutation(indices_by_domain[domain])
                    halves[domain] = (permuted[:6], permuted[6:])
                half_scores: list[FloatArray] = []
                for half_index in (0, 1):
                    target_indices = halves[target_domain][half_index]
                    other_indices = np.concatenate(
                        [
                            halves[domain][half_index]
                            for domain in DOMAINS
                            if domain != target_domain
                        ]
                    )
                    target = values[target_indices]
                    other = values[other_indices]
                    score = (target.mean(axis=0) - other.mean(axis=0)) / np.sqrt(
                        0.5 * (target.var(axis=0) + other.var(axis=0)) + 1e-6
                    )
                    half_scores.append(cast(FloatArray, score.astype(np.float32)))
                sets = [
                    _selected_set(selected_indices(score, granularity, quota), granularity)
                    for score in half_scores
                ]
                jaccards.append(_jaccard(sets[0], sets[1]))
                spearmans.append(_spearman(half_scores[0], half_scores[1]))

            within_sets = [
                prompt_sets[index]
                for index in indices_by_domain[target_domain].astype(int).tolist()
            ]
            other_sets = [
                prompt_sets[index]
                for index, domain in enumerate(domains)
                if domain != target_domain
            ]
            within_overlap = _pairwise_overlap(within_sets)
            across_overlap = float(
                np.mean([_jaccard(left, right) for left in within_sets for right in other_sets])
            )
            jaccard_median = float(np.median(jaccards))
            spearman_median = float(np.median(spearmans))
            advantage = within_overlap - across_overlap
            domain_output[target_domain] = {
                "split_half_jaccard": jaccards,
                "split_half_jaccard_median": jaccard_median,
                "split_half_spearman": spearmans,
                "split_half_spearman_median": spearman_median,
                "prompt_top_mask_within_domain_jaccard": within_overlap,
                "prompt_top_mask_across_domain_jaccard": across_overlap,
                "within_minus_across_jaccard": advantage,
                "stable": bool(
                    jaccard_median >= 0.20 and spearman_median >= 0.30 and advantage >= 0.05
                ),
            }
        stable_count = sum(bool(item["stable"]) for item in domain_output.values())
        output["granularities"][granularity] = {
            "domains": domain_output,
            "stable_domain_count": stable_count,
            "granularity_stable": stable_count >= 3,
        }
    return output


def build_retention_masks(rankings: dict[str, FloatArray], granularity: str) -> list[LogicalMask]:
    """Build the frozen conditional retention matrix without using held-out outcomes."""
    if granularity not in GRANULARITIES:
        raise ValueError(f"unsupported granularity: {granularity}")
    counts = {
        "mlp": {1.0: 8960, 0.75: 6720, 0.5: 4480, 0.25: 2240},
        "head": {1.0: 12, 0.75: 9, 0.5: 6, 0.25: 3},
        "layer": {1.0: 28, 0.75: 21, 0.5: 14, 0.25: 7},
    }[granularity]
    masks: list[LogicalMask] = []
    for fraction, count in counts.items():
        for domain in DOMAINS:
            scores = rankings[f"{granularity}_{domain}_selectivity"]
            masks.append(
                LogicalMask(
                    name=f"{granularity}_retain_{domain}_{int(fraction * 100)}",
                    granularity=granularity,  # type: ignore[arg-type]
                    mask_semantics="RETAIN_SELECTED",
                    source="domain_selectivity",
                    source_domain=domain,
                    selected_by_layer=selected_indices(scores, granularity, count),
                    fraction=fraction,
                )
            )
        importance = rankings[f"{granularity}_global_importance"]
        masks.append(
            LogicalMask(
                name=f"{granularity}_retain_global_{int(fraction * 100)}",
                granularity=granularity,  # type: ignore[arg-type]
                mask_semantics="RETAIN_SELECTED",
                source="global_importance",
                source_domain=None,
                selected_by_layer=selected_indices(importance, granularity, count),
                fraction=fraction,
            )
        )
        for seed in range(42, 47):
            rng = np.random.default_rng(seed)
            if granularity in {"mlp", "head"}:
                selected = {
                    layer: sorted(
                        rng.choice(WIDTHS[granularity], count, replace=False).astype(int).tolist()
                    )
                    for layer in range(28)
                }
            else:
                selected = {
                    int(layer): [0]
                    for layer in sorted(rng.choice(28, count, replace=False).tolist())
                }
            masks.append(
                LogicalMask(
                    name=f"{granularity}_retain_random_{seed}_{int(fraction * 100)}",
                    granularity=granularity,  # type: ignore[arg-type]
                    mask_semantics="RETAIN_SELECTED",
                    source="random",
                    source_domain=None,
                    selected_by_layer=selected,
                    fraction=fraction,
                    seed=seed,
                )
            )
    for mask in masks:
        validate_mask_structure(mask)
    return masks


def mask_overlap(masks: list[LogicalMask]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    available = {mask.granularity for mask in masks}
    for granularity in (item for item in GRANULARITIES if item in available):
        domain_masks = {
            mask.source_domain: _selected_set(mask.selected_by_layer, granularity)
            for mask in masks
            if mask.granularity == granularity and mask.source == "domain_selectivity"
        }
        pairs: dict[str, float] = {}
        for left, right in itertools.combinations(DOMAINS, 2):
            pairs[f"{left}__{right}"] = _jaccard(domain_masks[left], domain_masks[right])
        output[granularity] = {
            "pairwise_jaccard": pairs,
            "mean_pairwise_jaccard": float(np.mean(list(pairs.values()))),
        }
    return output
