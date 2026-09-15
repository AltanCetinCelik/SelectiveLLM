"""Discovery-only block aggregation, ranking, masks, and stability."""

from __future__ import annotations

import itertools
from collections.abc import Sequence
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray

from selectivellm.causal_importance.gradient import aggregate_blocks, percentile_rank_blocks
from selectivellm.causal_importance.mappings import BlockMapping
from selectivellm.causal_importance.masks import BlockMask, validate_block_mask
from selectivellm.dense_capacity.benchmark import DenseBenchmarkCase

DOMAINS = ("code", "mathematics", "science", "general")
METHODS = ("activation", "gradient")
FloatArray = NDArray[np.float32]
Float64Array = NDArray[np.float64]


def domain_selectivity(
    normalized: FloatArray, domains: Sequence[str], target_domain: str
) -> FloatArray:
    target_mask = np.asarray([domain == target_domain for domain in domains])
    other_mask = ~target_mask
    target = normalized[target_mask]
    other = normalized[other_mask]
    numerator = target.mean(axis=0) - other.mean(axis=0)
    denominator = np.sqrt(0.5 * (target.var(axis=0) + other.var(axis=0)) + 1e-6)
    return cast(FloatArray, (numerator / denominator).astype(np.float32))


def select_blocks(
    scores: FloatArray, mapping: BlockMapping, *, highest: bool = True
) -> dict[int, list[int]]:
    if scores.shape != (mapping.layer_count, mapping.blocks_per_layer):
        raise ValueError(f"ranking shape does not match block mapping: {scores.shape}")
    indices = np.arange(mapping.blocks_per_layer)
    selected: dict[int, list[int]] = {}
    for layer, quota in enumerate(mapping.per_layer_quota):
        order = (
            np.lexsort((indices, -scores[layer]))
            if highest
            else np.lexsort((indices, scores[layer]))
        )
        selected[layer] = order[:quota].astype(int).tolist()
    return selected


def _selected_set(selected: dict[int, list[int]], mapping: BlockMapping) -> set[int]:
    return {
        layer * mapping.blocks_per_layer + block
        for layer, blocks in selected.items()
        for block in blocks
    }


def _jaccard(left: set[int], right: set[int]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def _ordinal_ranks(values: FloatArray) -> Float64Array:
    flattened = values.reshape(-1)
    order = np.lexsort((np.arange(flattened.size), flattened))
    ranks = np.empty_like(order, dtype=np.float64)
    ranks[order] = np.arange(order.size, dtype=np.float64)
    return ranks


def _spearman(left: FloatArray, right: FloatArray) -> float:
    left_ranks = _ordinal_ranks(left)
    right_ranks = _ordinal_ranks(right)
    if left_ranks.std() == 0 or right_ranks.std() == 0:
        return 0.0
    return float(np.corrcoef(left_ranks, right_ranks)[0, 1])


def split_assignments(domains: Sequence[str]) -> list[dict[str, tuple[list[int], list[int]]]]:
    if any(sum(item == domain for item in domains) != 12 for domain in DOMAINS):
        raise ValueError("stability requires exactly 12 discovery prompts per domain")
    by_domain = {
        domain: np.asarray([index for index, item in enumerate(domains) if item == domain])
        for domain in DOMAINS
    }
    rng = np.random.default_rng(42)
    assignments: list[dict[str, tuple[list[int], list[int]]]] = []
    for _ in range(20):
        repetition: dict[str, tuple[list[int], list[int]]] = {}
        for domain in DOMAINS:
            permuted = rng.permutation(by_domain[domain]).astype(int).tolist()
            repetition[domain] = (permuted[:6], permuted[6:])
        assignments.append(repetition)
    return assignments


def stability_analysis(
    normalized: FloatArray,
    domains: Sequence[str],
    mapping: BlockMapping,
    assignments: list[dict[str, tuple[list[int], list[int]]]],
) -> dict[str, Any]:
    prompt_sets = [
        _selected_set(select_blocks(normalized[index], mapping), mapping)
        for index in range(len(domains))
    ]
    domain_results: dict[str, Any] = {}
    for target_domain in DOMAINS:
        jaccards: list[float] = []
        spearmans: list[float] = []
        for assignment in assignments:
            half_scores: list[FloatArray] = []
            for half_index in (0, 1):
                target_indices = assignment[target_domain][half_index]
                other_indices = [
                    index
                    for domain in DOMAINS
                    if domain != target_domain
                    for index in assignment[domain][half_index]
                ]
                target = normalized[np.asarray(target_indices)]
                other = normalized[np.asarray(other_indices)]
                numerator = target.mean(axis=0) - other.mean(axis=0)
                denominator = np.sqrt(0.5 * (target.var(axis=0) + other.var(axis=0)) + 1e-6)
                half_scores.append(cast(FloatArray, (numerator / denominator).astype(np.float32)))
            sets = [
                _selected_set(select_blocks(scores, mapping), mapping) for scores in half_scores
            ]
            jaccards.append(_jaccard(sets[0], sets[1]))
            spearmans.append(_spearman(half_scores[0], half_scores[1]))

        within_indices = [index for index, domain in enumerate(domains) if domain == target_domain]
        other_indices = [index for index, domain in enumerate(domains) if domain != target_domain]
        within_pairs = list(itertools.combinations(within_indices, 2))
        within = float(
            np.mean(
                [_jaccard(prompt_sets[left], prompt_sets[right]) for left, right in within_pairs]
            )
        )
        across = float(
            np.mean(
                [
                    _jaccard(prompt_sets[left], prompt_sets[right])
                    for left in within_indices
                    for right in other_indices
                ]
            )
        )
        jaccard_median = float(np.median(jaccards))
        spearman_median = float(np.median(spearmans))
        separation = within - across
        domain_results[target_domain] = {
            "split_half_jaccard": jaccards,
            "split_half_jaccard_median": jaccard_median,
            "split_half_spearman": spearmans,
            "split_half_spearman_median": spearman_median,
            "prompt_mask_within_domain_jaccard": within,
            "prompt_mask_across_domain_jaccard": across,
            "within_minus_across_jaccard": separation,
            "stable": bool(
                jaccard_median >= 0.20 and spearman_median >= 0.30 and separation >= 0.05
            ),
        }
    stable_count = sum(bool(result["stable"]) for result in domain_results.values())
    return {
        "domains": domain_results,
        "stable_domain_count": stable_count,
        "stable": stable_count >= 3,
        "median_domain_jaccard": float(
            np.median([result["split_half_jaccard_median"] for result in domain_results.values()])
        ),
        "median_domain_spearman": float(
            np.median([result["split_half_spearman_median"] for result in domain_results.values()])
        ),
    }


def _domain_mask_overlap(
    masks: list[BlockMask], mapping: BlockMapping, method: str
) -> dict[str, Any]:
    sets = {
        mask.source_domain: _selected_set(mask.selected_blocks_by_layer, mapping)
        for mask in masks
        if mask.discovery_method == method and mask.source == "domain_selectivity"
    }
    pairs = {
        f"{left}__{right}": _jaccard(sets[left], sets[right])
        for left, right in itertools.combinations(DOMAINS, 2)
    }
    return {
        "pairwise_jaccard": pairs,
        "mean_pairwise_jaccard": float(np.mean(list(pairs.values()))),
    }


def build_masks(rankings: dict[str, FloatArray], mapping: BlockMapping) -> list[BlockMask]:
    masks: list[BlockMask] = []
    for method in METHODS:
        for domain in DOMAINS:
            masks.append(
                BlockMask(
                    name=f"block{mapping.block_size}_{method}_domain_{domain}",
                    block_size=mapping.block_size,
                    discovery_method=method,  # type: ignore[arg-type]
                    source="domain_selectivity",
                    source_domain=domain,
                    selected_blocks_by_layer=select_blocks(
                        rankings[f"{method}_{domain}_selectivity"], mapping
                    ),
                    mapping_sha256=mapping.mapping_hash,
                    quota_pattern_sha256=mapping.quota_pattern_hash,
                    layer_count=mapping.layer_count,
                    intermediate_size=mapping.intermediate_size,
                )
            )
        global_scores = rankings[f"{method}_global_importance"]
        for source, highest in (("global_high", True), ("global_low", False)):
            masks.append(
                BlockMask(
                    name=f"block{mapping.block_size}_{method}_{source}",
                    block_size=mapping.block_size,
                    discovery_method=method,  # type: ignore[arg-type]
                    source=source,  # type: ignore[arg-type]
                    source_domain=None,
                    selected_blocks_by_layer=select_blocks(global_scores, mapping, highest=highest),
                    mapping_sha256=mapping.mapping_hash,
                    quota_pattern_sha256=mapping.quota_pattern_hash,
                    layer_count=mapping.layer_count,
                    intermediate_size=mapping.intermediate_size,
                )
            )
    for seed in range(42, 47):
        rng = np.random.default_rng(seed)
        selected = {
            layer: sorted(
                rng.choice(mapping.blocks_per_layer, quota, replace=False).astype(int).tolist()
            )
            for layer, quota in enumerate(mapping.per_layer_quota)
        }
        masks.append(
            BlockMask(
                name=f"block{mapping.block_size}_random_{seed}",
                block_size=mapping.block_size,
                discovery_method="shared_control",
                source="random",
                source_domain=None,
                selected_blocks_by_layer=selected,
                mapping_sha256=mapping.mapping_hash,
                quota_pattern_sha256=mapping.quota_pattern_hash,
                seed=seed,
                layer_count=mapping.layer_count,
                intermediate_size=mapping.intermediate_size,
            )
        )
    masks.append(
        BlockMask(
            name=f"block{mapping.block_size}_noop",
            block_size=mapping.block_size,
            discovery_method="shared_control",
            source="noop",
            source_domain=None,
            selected_blocks_by_layer={},
            mapping_sha256=mapping.mapping_hash,
            quota_pattern_sha256=mapping.quota_pattern_hash,
            layer_count=mapping.layer_count,
            intermediate_size=mapping.intermediate_size,
        )
    )
    for mask in masks:
        validate_block_mask(mask, mapping)
    if len(masks) != 18 or len({mask.name for mask in masks}) != 18:
        raise RuntimeError("each block mapping must produce exactly 18 unique masks")
    return masks


def build_discovery(
    channel_summaries: dict[str, FloatArray],
    cases: list[DenseBenchmarkCase],
    mappings: Sequence[BlockMapping],
) -> dict[str, Any]:
    if len(cases) != 48 or any(case.split != "discovery" for case in cases):
        raise ValueError("discovery requires the immutable 48-case split")
    geometries = {(mapping.layer_count, mapping.intermediate_size) for mapping in mappings}
    if len(geometries) != 1:
        raise ValueError("both block mappings must describe the same model geometry")
    layer_count, intermediate_size = next(iter(geometries))
    expected = (48, layer_count, intermediate_size)
    if set(channel_summaries) != {
        "activation",
        "gradient_absolute",
        "gradient_signed_sum",
        "gradient_signed_mean",
    }:
        raise ValueError("channel summaries do not match the frozen discovery schema")
    if any(values.shape != expected for values in channel_summaries.values()):
        raise ValueError("channel summaries have an invalid shape")
    if any(not np.isfinite(values).all() for values in channel_summaries.values()):
        raise FloatingPointError("channel summaries contain a nonfinite value")

    domains = [case.domain for case in cases]
    assignments = split_assignments(domains)
    output: dict[str, Any] = {
        "split_assignments": assignments,
        "block_sizes": {},
    }
    for mapping in mappings:
        raw_blocks = {
            name: aggregate_blocks(values, mapping.block_size)
            for name, values in channel_summaries.items()
        }
        normalized = {
            "activation": percentile_rank_blocks(raw_blocks["activation"]),
            "gradient": percentile_rank_blocks(raw_blocks["gradient_absolute"]),
        }
        rankings: dict[str, FloatArray] = {}
        stability: dict[str, Any] = {}
        for method in METHODS:
            for domain in DOMAINS:
                rankings[f"{method}_{domain}_selectivity"] = domain_selectivity(
                    normalized[method], domains, domain
                )
            rankings[f"{method}_global_importance"] = cast(
                FloatArray, normalized[method].mean(axis=0).astype(np.float32)
            )
            stability[method] = stability_analysis(
                normalized[method], domains, mapping, assignments
            )
        masks = build_masks(rankings, mapping)
        stability["improved_gradient_vs_activation"] = bool(
            stability["gradient"]["stable_domain_count"]
            > stability["activation"]["stable_domain_count"]
            or (
                stability["gradient"]["stable_domain_count"]
                == stability["activation"]["stable_domain_count"]
                and stability["gradient"]["median_domain_jaccard"]
                > stability["activation"]["median_domain_jaccard"]
                and stability["gradient"]["median_domain_spearman"]
                > stability["activation"]["median_domain_spearman"]
            )
        )
        stability["domain_mask_overlap"] = {
            method: _domain_mask_overlap(masks, mapping, method) for method in METHODS
        }
        output["block_sizes"][str(mapping.block_size)] = {
            "raw_blocks": raw_blocks,
            "normalized": normalized,
            "rankings": rankings,
            "stability": stability,
            "masks": masks,
        }
    return output
