"""Paired block-causal statistics, signed diagnostics, and frozen primary gate."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np
from numpy.typing import NDArray

from selectivellm.dense_capacity.analysis import bootstrap_interval

DOMAINS = ("code", "mathematics", "science", "general")
METHODS = ("activation", "gradient")
FloatArray = NDArray[np.float64]
SCALE_METRICS = (
    "same_damage",
    "same_minus_random",
    "same_minus_wrong",
    "same_minus_global_high",
    "gradient_same_minus_activation_same",
)


def _mean(rows: Sequence[dict[str, Any]], field: str) -> float:
    return float(np.mean([float(row[field]) for row in rows]))


def _metric_summary(rows: Sequence[dict[str, Any]], field: str) -> dict[str, Any]:
    return bootstrap_interval(
        [float(row[field]) for row in rows],
        [str(row["domain"]) for row in rows],
    )


def analyze_causal_matrix(
    full_rows: list[dict[str, Any]],
    masked_rows: list[dict[str, Any]],
    stability: dict[str, Any],
    validity: dict[str, Any],
) -> dict[str, Any]:
    full = {str(row["case_id"]): row for row in full_rows}
    if len(full) != 32 or len(full_rows) != 32:
        raise ValueError("causal analysis requires exactly 32 unique full-model rows")
    if len(masked_rows) != 1152:
        raise ValueError(f"causal analysis requires 1,152 masked rows, found {len(masked_rows)}")
    enriched = [
        {
            **row,
            "full_correct_nll": float(full[str(row["case_id"])]["correct_nll"]),
            "causal_damage": float(row["correct_nll"])
            - float(full[str(row["case_id"])]["correct_nll"]),
        }
        for row in masked_rows
    ]
    paired_rows: list[dict[str, Any]] = []
    results: dict[str, Any] = {}
    for block_size in (64, 128):
        size_rows = [row for row in enriched if int(row["block_size"]) == block_size]
        if len(size_rows) != 576:
            raise ValueError(f"block size {block_size} has an incomplete causal matrix")
        results[str(block_size)] = {}
        for method in METHODS:
            method_paired: list[dict[str, Any]] = []
            for case_id, baseline in full.items():
                case_rows = [row for row in size_rows if row["case_id"] == case_id]
                domain = str(baseline["domain"])
                domain_rows = [
                    row
                    for row in case_rows
                    if row["discovery_method"] == method
                    and row["mask_source"] == "domain_selectivity"
                ]
                same = [row for row in domain_rows if row["source_domain"] == domain]
                wrong = [row for row in domain_rows if row["source_domain"] != domain]
                random = [row for row in case_rows if row["mask_source"] == "random"]
                high = [
                    row
                    for row in case_rows
                    if row["discovery_method"] == method and row["mask_source"] == "global_high"
                ]
                low = [
                    row
                    for row in case_rows
                    if row["discovery_method"] == method and row["mask_source"] == "global_low"
                ]
                activation_same = [
                    row
                    for row in case_rows
                    if row["discovery_method"] == "activation"
                    and row["mask_source"] == "domain_selectivity"
                    and row["source_domain"] == domain
                ]
                if not (
                    len(same) == 1
                    and len(wrong) == 3
                    and len(random) == 5
                    and len(high) == 1
                    and len(low) == 1
                    and len(activation_same) == 1
                ):
                    raise ValueError(f"invalid causal controls for {block_size}/{method}/{case_id}")
                same_damage = float(same[0]["causal_damage"])
                wrong_damage = _mean(wrong, "causal_damage")
                random_damage = _mean(random, "causal_damage")
                high_damage = float(high[0]["causal_damage"])
                low_damage = float(low[0]["causal_damage"])
                activation_damage = float(activation_same[0]["causal_damage"])
                method_paired.append(
                    {
                        "case_id": case_id,
                        "domain": domain,
                        "block_size": block_size,
                        "discovery_method": method,
                        "full_correct_nll": float(baseline["correct_nll"]),
                        "same_correct_nll": float(same[0]["correct_nll"]),
                        "same_accuracy": float(bool(same[0]["correct"])),
                        "same_damage": same_damage,
                        "wrong_damage": wrong_damage,
                        "random_damage": random_damage,
                        "global_high_damage": high_damage,
                        "global_low_damage": low_damage,
                        "same_minus_random": same_damage - random_damage,
                        "same_minus_wrong": same_damage - wrong_damage,
                        "same_minus_global_high": same_damage - high_damage,
                        "same_minus_global_low": same_damage - low_damage,
                        "gradient_same_minus_activation_same": (
                            same_damage - activation_damage if method == "gradient" else 0.0
                        ),
                    }
                )
            paired_rows.extend(method_paired)
            metrics = [
                "same_damage",
                "wrong_damage",
                "random_damage",
                "global_high_damage",
                "global_low_damage",
                "same_minus_random",
                "same_minus_wrong",
                "same_minus_global_high",
                "same_minus_global_low",
            ]
            if method == "gradient":
                metrics.append("gradient_same_minus_activation_same")
            pooled = {metric: _metric_summary(method_paired, metric) for metric in metrics}
            domains: dict[str, Any] = {}
            for domain in DOMAINS:
                domain_rows = [row for row in method_paired if row["domain"] == domain]
                domains[domain] = {
                    metric: _metric_summary(domain_rows, metric) for metric in metrics
                }
                domains[domain]["same_exceeds_all_controls"] = bool(
                    all(
                        float(domains[domain][metric]["mean"]) > 0
                        for metric in (
                            "same_minus_random",
                            "same_minus_wrong",
                            "same_minus_global_high",
                            "same_minus_global_low",
                        )
                    )
                )
            results[str(block_size)][method] = {
                "pooled": pooled,
                "domains": domains,
                "same_condition": {
                    "correct_nll": _metric_summary(method_paired, "same_correct_nll"),
                    "accuracy": float(np.mean([row["same_accuracy"] for row in method_paired])),
                },
            }

    decision = apply_primary_gate(results["64"], stability["64"], validity)
    concordance = build_concordance(results)
    return {
        "analysis_schema_version": "dense-block-causal-nll-1.0.0",
        "experimental_unit": "held_out_question",
        "bootstrap_repetitions": 10_000,
        "bootstrap_seed": 42,
        "full_model": {
            "correct_nll": bootstrap_interval(
                [float(row["correct_nll"]) for row in full_rows],
                [str(row["domain"]) for row in full_rows],
            ),
            "accuracy": float(np.mean([bool(row["correct"]) for row in full_rows])),
            "case_count": 32,
        },
        "validity": validity,
        "block_sizes": results,
        "primary_decision": decision,
        "corroborative_concordance": concordance,
        "paired_rows": paired_rows,
    }


def analyze_scale_comparison(
    current_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    current_stability: dict[str, Any],
    prior_stability: dict[str, Any],
    *,
    current_model: str,
    prior_model: str,
    current_classification: str,
    prior_classification: str,
) -> dict[str, Any]:
    """Compare model scales by paired held-out case without pooling model identities."""

    def primary_gradient(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        selected = {
            str(row["case_id"]): row
            for row in rows
            if int(row["block_size"]) == 64 and row["discovery_method"] == "gradient"
        }
        if len(selected) != 32:
            raise ValueError("scale comparison requires 32 primary gradient rows per model")
        return selected

    current = primary_gradient(current_rows)
    prior = primary_gradient(prior_rows)
    if set(current) != set(prior):
        raise ValueError("scale comparison case identities differ")
    delta_rows: list[dict[str, Any]] = []
    for case_id in sorted(current):
        if current[case_id]["domain"] != prior[case_id]["domain"]:
            raise ValueError(f"scale comparison domain changed for {case_id}")
        delta_rows.append(
            {
                "case_id": case_id,
                "domain": current[case_id]["domain"],
                **{
                    metric: float(current[case_id][metric]) - float(prior[case_id][metric])
                    for metric in SCALE_METRICS
                },
            }
        )
    return {
        "schema_version": "causal-model-scale-comparison-1.0.0",
        "experimental_unit": "paired_held_out_question",
        "models_pooled": False,
        "current_model": current_model,
        "prior_model": prior_model,
        "classification_transition": f"{prior_classification}->{current_classification}",
        "scale_rescue": current_classification in {"A", "B"},
        "metrics": {metric: _metric_summary(delta_rows, metric) for metric in SCALE_METRICS},
        "stability": {
            "prior_gradient_stable_domains": prior_stability["64"]["gradient"][
                "stable_domain_count"
            ],
            "current_gradient_stable_domains": current_stability["64"]["gradient"][
                "stable_domain_count"
            ],
            "prior_activation_stable_domains": prior_stability["64"]["activation"][
                "stable_domain_count"
            ],
            "current_activation_stable_domains": current_stability["64"]["activation"][
                "stable_domain_count"
            ],
        },
        "rows": delta_rows,
    }


def apply_primary_gate(
    primary: dict[str, Any], stability: dict[str, Any], validity: dict[str, Any]
) -> dict[str, Any]:
    gradient = primary["gradient"]
    pooled = gradient["pooled"]
    gradient_stability = stability["gradient"]
    domain_wins = sum(
        bool(item["same_exceeds_all_controls"]) for item in gradient["domains"].values()
    )
    a_checks = {
        "validity_passed": bool(validity.get("passed")),
        "gradient_stable_at_least_three_domains": gradient_stability["stable_domain_count"] >= 3,
        "improved_stability": bool(stability["improved_gradient_vs_activation"]),
        "same_damage_at_least_0_10": float(pooled["same_damage"]["mean"]) >= 0.10,
        "same_minus_random_threshold": float(pooled["same_minus_random"]["mean"]) >= 0.05,
        "same_minus_random_ci_positive": float(pooled["same_minus_random"]["ci95_low"]) > 0,
        "same_minus_wrong_threshold": float(pooled["same_minus_wrong"]["mean"]) >= 0.05,
        "same_minus_wrong_ci_positive": float(pooled["same_minus_wrong"]["ci95_low"]) > 0,
        "same_minus_global_high_positive": float(pooled["same_minus_global_high"]["mean"]) > 0,
        "same_minus_global_high_ci_positive": float(pooled["same_minus_global_high"]["ci95_low"])
        > 0,
        "same_exceeds_all_controls_in_three_domains": domain_wins >= 3,
        "gradient_minus_activation_threshold": float(
            pooled["gradient_same_minus_activation_same"]["mean"]
        )
        >= 0.05,
        "gradient_minus_activation_ci_positive": float(
            pooled["gradient_same_minus_activation_same"]["ci95_low"]
        )
        > 0,
    }
    if all(a_checks.values()):
        return {
            "classification": "A",
            "label": "objective_aware_discovery_succeeds",
            "qualifier": None,
            "a_checks": a_checks,
            "b_checks": None,
        }

    same_damage = float(pooled["same_damage"]["mean"])
    wrong_ratio = float(pooled["wrong_damage"]["mean"]) / same_damage if same_damage else 0.0
    global_ratio = float(pooled["global_high_damage"]["mean"]) / same_damage if same_damage else 0.0
    overlap = float(stability["domain_mask_overlap"]["gradient"]["mean_pairwise_jaccard"])
    b_checks = {
        "validity_passed": bool(validity.get("passed")),
        "gradient_stable_at_least_three_domains": gradient_stability["stable_domain_count"] >= 3,
        "same_damage_at_least_0_10": same_damage >= 0.10,
        "same_minus_random_threshold": float(pooled["same_minus_random"]["mean"]) >= 0.03,
        "same_minus_random_ci_positive": float(pooled["same_minus_random"]["ci95_low"]) > 0,
        "outcome_a_failed": True,
        "shared_core_indicator": bool(
            wrong_ratio >= 0.75 or global_ratio >= 0.75 or overlap >= 0.20
        ),
    }
    if all(b_checks.values()):
        return {
            "classification": "B",
            "label": "stable_but_mostly_shared_importance",
            "qualifier": None,
            "a_checks": a_checks,
            "b_checks": b_checks,
            "shared_core_ratios": {
                "wrong_over_same": wrong_ratio,
                "global_high_over_same": global_ratio,
                "domain_mask_overlap": overlap,
            },
        }
    return {
        "classification": "C",
        "label": "still_weak_or_unstable",
        "qualifier": None if validity.get("passed") else "validity_failure",
        "a_checks": a_checks,
        "b_checks": b_checks,
    }


def build_concordance(results: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = (
        "same_minus_random",
        "same_minus_wrong",
        "same_minus_global_high",
        "same_minus_global_low",
        "gradient_same_minus_activation_same",
    )
    rows: list[dict[str, Any]] = []
    for metric in metrics:
        primary = results["64"]["gradient"]["pooled"][metric]
        secondary = results["128"]["gradient"]["pooled"][metric]
        primary_mean = float(primary["mean"])
        secondary_mean = float(secondary["mean"])
        rows.append(
            {
                "metric": metric,
                "primary_64": primary,
                "corroborative_128": secondary,
                "same_point_estimate_sign": bool(np.sign(primary_mean) == np.sign(secondary_mean)),
            }
        )
    return rows


def _average_ranks(values: FloatArray) -> FloatArray:
    order = np.argsort(values, kind="stable")
    sorted_values = values[order]
    ranks = np.empty(values.size, dtype=np.float64)
    start = 0
    while start < values.size:
        stop = start + 1
        while stop < values.size and sorted_values[stop] == sorted_values[start]:
            stop += 1
        ranks[order[start:stop]] = (start + stop - 1) / 2
        start = stop
    return ranks


def analyze_signed_diagnostics(
    signed_rows: list[dict[str, Any]], masked_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    if len(signed_rows) != 1088:
        raise ValueError(f"expected 1,088 signed diagnostic rows, found {len(signed_rows)}")
    observed = {
        (str(row["mask_name"]), str(row["case_id"])): float(row["causal_damage"])
        if "causal_damage" in row
        else float(row["correct_nll"]) - float(row["full_correct_nll"])
        for row in masked_rows
        if row["mask_source"] != "noop"
    }
    enriched: list[dict[str, Any]] = []
    for row in signed_rows:
        key = (str(row["mask_name"]), str(row["case_id"]))
        if key not in observed:
            raise ValueError(f"signed diagnostic has no causal observation: {key}")
        enriched.append({**row, "observed_damage": observed[key]})
    summaries: dict[str, Any] = {}
    for block_size in (64, 128):
        rows = [row for row in enriched if int(row["block_size"]) == block_size]
        predicted = np.asarray([row["predicted_taylor_damage"] for row in rows], dtype=np.float64)
        actual = np.asarray([row["observed_damage"] for row in rows], dtype=np.float64)
        nonzero = (predicted != 0) & (actual != 0)
        sign_agreement = float(np.mean(np.sign(predicted[nonzero]) == np.sign(actual[nonzero])))
        pearson = float(np.corrcoef(predicted, actual)[0, 1])
        spearman = float(np.corrcoef(_average_ranks(predicted), _average_ranks(actual))[0, 1])
        if not all(np.isfinite(value) for value in (sign_agreement, pearson, spearman)):
            raise FloatingPointError("signed diagnostic association is nonfinite")
        summaries[str(block_size)] = {
            "row_count": len(rows),
            "nonzero_pair_count": int(nonzero.sum()),
            "predicted_zero_count": int((predicted == 0).sum()),
            "observed_zero_count": int((actual == 0).sum()),
            "sign_agreement": sign_agreement,
            "spearman_association": spearman,
            "pearson_association": pearson,
            "classification_input": False,
        }
    return {
        "diagnostic_schema_version": "signed-ablation-diagnostics-1.0.0",
        "taylor_quantity": "predicted_taylor_damage",
        "normalized_quantity": "normalized_signed_attribution",
        "classification_input": False,
        "block_sizes": summaries,
        "rows": enriched,
    }
