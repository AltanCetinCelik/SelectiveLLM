"""Paired causal analysis and preregistered A/B/C decision gates."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np
from numpy.typing import NDArray

from selectivellm.dense_capacity.discovery import DOMAINS, GRANULARITIES

FloatArray = NDArray[np.float64]


def _summary(values: Sequence[float]) -> dict[str, float | int]:
    array = np.asarray(values, dtype=np.float64)
    return {
        "n": int(array.size),
        "mean": float(array.mean()),
        "median": float(np.median(array)),
        "std": float(array.std(ddof=1)) if array.size > 1 else 0.0,
        "p50": float(np.percentile(array, 50)),
        "p95": float(np.percentile(array, 95)),
    }


def bootstrap_interval(
    values: Sequence[float],
    domains: Sequence[str],
    *,
    repetitions: int = 10_000,
    seed: int = 42,
) -> dict[str, Any]:
    """Percentile interval resampling cases, stratified by domain when pooled."""
    array = np.asarray(values, dtype=np.float64)
    domain_array = np.asarray(domains)
    if array.size != domain_array.size or array.size == 0:
        raise ValueError("bootstrap values and domains must have the same nonzero size")
    groups = [np.flatnonzero(domain_array == domain) for domain in DOMAINS]
    groups = [group for group in groups if group.size]
    rng = np.random.default_rng(seed)
    means = np.empty(repetitions, dtype=np.float64)
    for repetition in range(repetitions):
        sampled = np.concatenate([rng.choice(group, group.size, replace=True) for group in groups])
        means[repetition] = array[sampled].mean()
    return {
        **_summary(values),
        "ci95_low": float(np.percentile(means, 2.5)),
        "ci95_high": float(np.percentile(means, 97.5)),
        "bootstrap_repetitions": repetitions,
        "bootstrap_seed": seed,
        "experimental_unit": "held_out_question",
        "pooled_resampling": "stratified_by_domain" if len(groups) > 1 else "within_domain",
    }


def _index_unique(
    rows: Sequence[dict[str, Any]], key: Callable[[dict[str, Any]], str]
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        item_key = key(row)
        if item_key in output:
            raise ValueError(f"duplicate causal result row: {item_key}")
        output[item_key] = row
    return output


def analyze_causal_rows(
    full_rows: Sequence[dict[str, Any]],
    masked_rows: Sequence[dict[str, Any]],
    stability: dict[str, Any],
    validity: dict[str, Any],
) -> dict[str, Any]:
    full = _index_unique(full_rows, lambda row: str(row["case_id"]))
    if len(full) != 32:
        raise ValueError(f"expected 32 full-model rows, found {len(full)}")
    enriched: list[dict[str, Any]] = []
    for row in masked_rows:
        case_id = str(row["case_id"])
        if case_id not in full:
            raise ValueError(f"masked row has no full baseline: {case_id}")
        enriched.append(
            {
                **row,
                "full_correct_nll": full[case_id]["correct_nll"],
                "causal_damage": float(row["correct_nll"]) - float(full[case_id]["correct_nll"]),
            }
        )

    expected_sources = {
        "domain_selectivity": 4,
        "random": 5,
        "global_low_importance": 1,
    }
    by_granularity: dict[str, Any] = {}
    paired_rows: list[dict[str, Any]] = []
    available = tuple(
        granularity
        for granularity in GRANULARITIES
        if any(row.get("granularity") == granularity for row in enriched)
    )
    for granularity in available:
        subset = [row for row in enriched if row["granularity"] == granularity]
        grouped: dict[str, list[dict[str, Any]]] = {case_id: [] for case_id in full}
        for row in subset:
            grouped[str(row["case_id"])].append(row)
        for case_id, rows in grouped.items():
            counts = {
                source: sum(row["mask_source"] == source for row in rows)
                for source in expected_sources
            }
            if counts != expected_sources:
                raise ValueError(f"incomplete {granularity} matrix for {case_id}: {counts}")
            domain = str(full[case_id]["domain"])
            domain_rows = [row for row in rows if row["mask_source"] == "domain_selectivity"]
            same = [row for row in domain_rows if row["source_domain"] == domain]
            wrong = [row for row in domain_rows if row["source_domain"] != domain]
            random_rows = [row for row in rows if row["mask_source"] == "random"]
            low = [row for row in rows if row["mask_source"] == "global_low_importance"]
            if len(same) != 1 or len(wrong) != 3 or len(random_rows) != 5 or len(low) != 1:
                raise ValueError(f"invalid equal-structure conditions for {granularity}/{case_id}")
            same_damage = float(same[0]["causal_damage"])
            wrong_damage = float(np.mean([float(row["causal_damage"]) for row in wrong]))
            random_damage = float(np.mean([float(row["causal_damage"]) for row in random_rows]))
            low_damage = float(low[0]["causal_damage"])
            paired_rows.append(
                {
                    "case_id": case_id,
                    "domain": domain,
                    "granularity": granularity,
                    "full_correct_nll": float(full[case_id]["correct_nll"]),
                    "same_damage": same_damage,
                    "wrong_damage": wrong_damage,
                    "random_damage": random_damage,
                    "low_damage": low_damage,
                    "same_correct_nll": float(same[0]["correct_nll"]),
                    "wrong_correct_nll": float(
                        np.mean([float(row["correct_nll"]) for row in wrong])
                    ),
                    "random_correct_nll": float(
                        np.mean([float(row["correct_nll"]) for row in random_rows])
                    ),
                    "low_correct_nll": float(low[0]["correct_nll"]),
                    "same_accuracy": float(bool(same[0]["correct"])),
                    "wrong_accuracy": float(np.mean([bool(row["correct"]) for row in wrong])),
                    "random_accuracy": float(
                        np.mean([bool(row["correct"]) for row in random_rows])
                    ),
                    "low_accuracy": float(bool(low[0]["correct"])),
                    "same_minus_wrong": same_damage - wrong_damage,
                    "same_minus_random": same_damage - random_damage,
                    "same_minus_low": same_damage - low_damage,
                }
            )

        granularity_rows = [row for row in paired_rows if row["granularity"] == granularity]
        metrics = (
            "same_damage",
            "wrong_damage",
            "random_damage",
            "low_damage",
            "same_minus_wrong",
            "same_minus_random",
            "same_minus_low",
        )
        pooled = {
            metric: bootstrap_interval(
                [float(row[metric]) for row in granularity_rows],
                [str(row["domain"]) for row in granularity_rows],
            )
            for metric in metrics
        }
        domain_results: dict[str, Any] = {}
        for domain in DOMAINS:
            domain_rows = [row for row in granularity_rows if row["domain"] == domain]
            domain_results[domain] = {
                metric: bootstrap_interval(
                    [float(row[metric]) for row in domain_rows],
                    [domain] * len(domain_rows),
                )
                for metric in metrics
            }
            domain_results[domain]["same_exceeds_all_controls"] = bool(
                all(
                    float(domain_results[domain][metric]["mean"]) > 0
                    for metric in ("same_minus_random", "same_minus_wrong", "same_minus_low")
                )
            )
        by_granularity[granularity] = {
            "pooled": pooled,
            "absolute_conditions": {
                condition: {
                    "correct_nll": bootstrap_interval(
                        [float(row[f"{condition}_correct_nll"]) for row in granularity_rows],
                        [str(row["domain"]) for row in granularity_rows],
                    ),
                    "accuracy": float(
                        np.mean([float(row[f"{condition}_accuracy"]) for row in granularity_rows])
                    ),
                }
                for condition in ("same", "wrong", "random", "low")
            },
            "domains": domain_results,
            "stable_domain_count": stability["granularities"][granularity]["stable_domain_count"],
            "granularity_stable": stability["granularities"][granularity]["granularity_stable"],
        }

    decision = apply_decision_gate(by_granularity, stability, validity)
    return {
        "analysis_schema_version": "dense-causal-analysis-1.0.0",
        "full_model": {
            "correct_nll": bootstrap_interval(
                [float(row["correct_nll"]) for row in full_rows],
                [str(row["domain"]) for row in full_rows],
            ),
            "accuracy": float(np.mean([bool(row["correct"]) for row in full_rows])),
            "case_count": len(full_rows),
        },
        "validity": validity,
        "granularities": by_granularity,
        "decision": decision,
        "paired_rows": paired_rows,
    }


def apply_decision_gate(
    granularities: dict[str, Any], stability: dict[str, Any], validity: dict[str, Any]
) -> dict[str, Any]:
    validity_passed = bool(validity.get("passed"))
    additional_positive = {
        granularity: float(result["pooled"]["same_minus_random"]["mean"]) > 0
        for granularity, result in granularities.items()
    }
    a_candidates: list[str] = []
    for granularity in (item for item in ("mlp", "head") if item in granularities):
        result = granularities[granularity]
        pooled = result["pooled"]
        domain_wins = sum(
            bool(item["same_exceeds_all_controls"]) for item in result["domains"].values()
        )
        second_granularity = any(
            positive for other, positive in additional_positive.items() if other != granularity
        )
        if all(
            (
                validity_passed,
                bool(result["granularity_stable"]),
                float(pooled["same_damage"]["mean"]) >= 0.10,
                float(pooled["same_minus_random"]["mean"]) >= 0.05,
                float(pooled["same_minus_wrong"]["mean"]) >= 0.05,
                float(pooled["same_minus_random"]["ci95_low"]) > 0,
                float(pooled["same_minus_wrong"]["ci95_low"]) > 0,
                domain_wins >= 3,
                second_granularity,
            )
        ):
            a_candidates.append(granularity)
    if a_candidates:
        a_chosen = next(item for item in ("mlp", "head") if item in a_candidates)
        return {
            "classification": "A",
            "label": "stable_causal_specialization",
            "qualifier": None,
            "trigger_granularity": a_chosen,
            "all_qualifying_granularities": a_candidates,
            "retention_triggered": True,
        }

    b_candidates: list[str] = []
    for b_granularity in (item for item in GRANULARITIES if item in granularities):
        result = granularities[b_granularity]
        pooled = result["pooled"]
        overlap = float(stability["mask_overlap"][b_granularity]["mean_pairwise_jaccard"])
        shared_core = (
            float(pooled["wrong_damage"]["mean"]) >= 0.5 * float(pooled["same_damage"]["mean"])
            or overlap >= 0.20
        )
        if all(
            (
                validity_passed,
                float(pooled["same_damage"]["mean"]) >= 0.05,
                float(pooled["same_minus_random"]["mean"]) >= 0.03,
                float(pooled["same_minus_random"]["ci95_low"]) > 0,
                float(pooled["same_minus_wrong"]["mean"]) > 0,
                shared_core,
            )
        ):
            b_candidates.append(b_granularity)
    if b_candidates:
        b_chosen = next(item for item in GRANULARITIES if item in b_candidates)
        return {
            "classification": "B",
            "label": "shared_core_with_specialized_tail",
            "qualifier": None,
            "trigger_granularity": b_chosen,
            "all_qualifying_granularities": b_candidates,
            "retention_triggered": True,
        }

    return {
        "classification": "C",
        "label": "weak_or_unstable_specialization",
        "qualifier": None if validity_passed else "validity_failure",
        "trigger_granularity": None,
        "all_qualifying_granularities": [],
        "retention_triggered": False,
    }


def analyze_retention_rows(
    full_rows: Sequence[dict[str, Any]], retention_rows: Sequence[dict[str, Any]]
) -> dict[str, Any]:
    full = _index_unique(full_rows, lambda row: str(row["case_id"]))
    paired: list[dict[str, Any]] = []
    for row in retention_rows:
        baseline = full[str(row["case_id"])]
        paired.append(
            {
                **row,
                "full_correct_nll": float(baseline["correct_nll"]),
                "causal_damage": float(row["correct_nll"]) - float(baseline["correct_nll"]),
                "quality_retention": float(row["correct_probability"])
                / max(float(baseline["correct_probability"]), 1e-12),
            }
        )
    aggregates: list[dict[str, Any]] = []
    fractions = sorted({float(row["fraction"]) for row in paired}, reverse=True)
    for fraction in fractions:
        fraction_rows = [row for row in paired if float(row["fraction"]) == fraction]
        for condition in ("same", "wrong", "random", "global"):
            values_by_case: dict[str, list[dict[str, Any]]] = {}
            for row in fraction_rows:
                domain = str(row["domain"])
                if row["mask_source"] == "domain_selectivity":
                    row_condition = "same" if row["source_domain"] == domain else "wrong"
                elif row["mask_source"] == "random":
                    row_condition = "random"
                else:
                    row_condition = "global"
                if row_condition == condition:
                    values_by_case.setdefault(str(row["case_id"]), []).append(row)
            case_rows = [
                {
                    "case_id": case_id,
                    "domain": rows[0]["domain"],
                    "damage": float(np.mean([float(row["causal_damage"]) for row in rows])),
                    "nll": float(np.mean([float(row["correct_nll"]) for row in rows])),
                    "retention": float(np.mean([float(row["quality_retention"]) for row in rows])),
                    "accuracy": float(np.mean([bool(row["correct"]) for row in rows])),
                }
                for case_id, rows in values_by_case.items()
            ]
            if len(case_rows) != 32:
                raise ValueError(
                    f"incomplete retention matrix at {fraction}/{condition}: {len(case_rows)}"
                )
            aggregates.append(
                {
                    "fraction": fraction,
                    "condition": condition,
                    "correct_nll": _summary([row["nll"] for row in case_rows]),
                    "causal_damage": bootstrap_interval(
                        [row["damage"] for row in case_rows],
                        [str(row["domain"]) for row in case_rows],
                    ),
                    "quality_retention": _summary([row["retention"] for row in case_rows]),
                    "accuracy": float(np.mean([row["accuracy"] for row in case_rows])),
                }
            )
    return {
        "analysis_schema_version": "dense-retention-analysis-1.0.0",
        "logical_masking_only": True,
        "measured_vram_reduction": False,
        "aggregates": aggregates,
        "paired_rows": paired,
    }
