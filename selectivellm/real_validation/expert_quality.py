"""Preregistered case-level analysis for the expert-quality diagnostic."""

from __future__ import annotations

import csv
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from selectivellm.real_validation.evaluation import RealBenchmarkCase

CONDITIONS = ("base", "code", "math", "science")
EXPERT_TO_CONDITION = {
    "code_expert": "code",
    "math_expert": "math",
    "science_expert": "science",
}
TIE_TOLERANCE = 1e-12
BOOTSTRAP_SEED = 42
BOOTSTRAP_RESAMPLES = 10_000


def _percentile(values: list[float], quantile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires at least one value")
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def aggregate_values(
    values: list[float],
    *,
    bootstrap_seed: int = BOOTSTRAP_SEED,
    bootstrap_resamples: int = BOOTSTRAP_RESAMPLES,
) -> dict[str, Any]:
    """Aggregate independent case values and bootstrap their mean over cases."""
    if not values:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "standard_deviation": None,
            "p50": None,
            "p95": None,
            "confidence_interval_95": None,
        }
    rng = random.Random(bootstrap_seed)
    count = len(values)
    bootstrap_means = [
        statistics.fmean(values[rng.randrange(count)] for _ in range(count))
        for _ in range(bootstrap_resamples)
    ]
    return {
        "count": count,
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "standard_deviation": statistics.stdev(values) if count > 1 else 0.0,
        "p50": _percentile(values, 0.50),
        "p95": _percentile(values, 0.95),
        "confidence_interval_95": [
            _percentile(bootstrap_means, 0.025),
            _percentile(bootstrap_means, 0.975),
        ],
        "bootstrap_unit": "benchmark_case",
        "bootstrap_seed": bootstrap_seed,
        "bootstrap_resamples": bootstrap_resamples,
    }


def aggregate_diagnostic(
    rows: list[dict[str, Any]],
    cases: list[RealBenchmarkCase],
    semantic_routes: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Build cell means, derived policies, and the frozen decision gate."""
    expected_row_count = len(cases) * len(CONDITIONS) * 3
    if len(rows) != expected_row_count:
        raise ValueError(f"expected {expected_row_count} generations, found {len(rows)}")
    case_by_id = {case.id: case for case in cases}
    route_by_id = {route["case_id"]: route for route in semantic_routes}
    if set(route_by_id) != set(case_by_id):
        raise ValueError("semantic routes must contain every benchmark case exactly once")

    grouped: defaultdict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["case_id"]), str(row["condition"]))].append(row)

    cells: list[dict[str, Any]] = []
    cell_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for case in cases:
        for condition in CONDITIONS:
            repetitions = sorted(
                grouped[(case.id, condition)], key=lambda item: int(item["repetition"])
            )
            if [item["repetition"] for item in repetitions] != [1, 2, 3]:
                raise ValueError(f"invalid repetitions for {case.id}/{condition}")
            repetition_qualities = [float(item["quality"]) for item in repetitions]
            cell = {
                "case_id": case.id,
                "condition": condition,
                "expected_experts": list(case.expected_experts),
                "correct_labeled_expert": (
                    case.expected_experts[0] if case.expected_experts else None
                ),
                "repetition_count": 3,
                "quality_mean": statistics.fmean(repetition_qualities),
                "quality_median": statistics.median(repetition_qualities),
                "quality_standard_deviation": statistics.stdev(repetition_qualities),
                "quality_min": min(repetition_qualities),
                "quality_max": max(repetition_qualities),
                "quality_range": max(repetition_qualities) - min(repetition_qualities),
                "exact_score_agreement": len(set(repetition_qualities)) == 1,
                "eos_count": sum(bool(item["eos_completed"]) for item in repetitions),
                "truncation_count": sum(bool(item["truncated"]) for item in repetitions),
            }
            cells.append(cell)
            cell_by_key[(case.id, condition)] = cell

    case_analysis: list[dict[str, Any]] = []
    for case in cases:
        qualities = {
            condition: float(cell_by_key[(case.id, condition)]["quality_mean"])
            for condition in CONDITIONS
        }
        maximum = max(qualities.values())
        empirical_best = [
            condition
            for condition in CONDITIONS
            if math.isclose(qualities[condition], maximum, rel_tol=0, abs_tol=TIE_TOLERANCE)
        ]
        primary = case.expected_experts[0] if case.expected_experts else None
        primary_condition = EXPERT_TO_CONDITION.get(primary) if primary else None
        wrong_experts = [
            expert for expert in EXPERT_TO_CONDITION if expert not in case.expected_experts
        ]
        wrong_conditions = [EXPERT_TO_CONDITION[expert] for expert in wrong_experts]
        label_condition = primary_condition or "base"

        route = route_by_id[case.id]
        selected = list(route["selected_experts"])
        semantic_condition = EXPERT_TO_CONDITION[selected[0]] if selected else "base"
        specialist_lift = (
            qualities[primary_condition] - qualities["base"] if primary_condition else None
        )
        specialization_margin = None
        if primary_condition and wrong_conditions:
            specialization_margin = qualities[primary_condition] - statistics.fmean(
                qualities[condition] for condition in wrong_conditions
            )
        case_analysis.append(
            {
                "case_id": case.id,
                "prompt": case.prompt,
                "expected_experts": list(case.expected_experts),
                "correct_labeled_expert": primary,
                "wrong_experts": wrong_experts,
                "quality_by_condition": qualities,
                "label_oracle_condition": label_condition,
                "label_oracle_quality": qualities[label_condition],
                "semantic_selected_experts": selected,
                "semantic_router_condition": semantic_condition,
                "semantic_router_quality": qualities[semantic_condition],
                "empirical_best": empirical_best,
                "empirical_oracle_quality": maximum,
                "specialist_lift": specialist_lift,
                "specialization_margin": specialization_margin,
                "routing_opportunity": maximum - qualities["base"],
                "primary_tie_inclusive_win": (
                    primary_condition in empirical_best if primary_condition else None
                ),
                "primary_sole_win": (
                    empirical_best == [primary_condition] if primary_condition else None
                ),
            }
        )

    direct = {
        condition: aggregate_values(
            [float(cell_by_key[(case.id, condition)]["quality_mean"]) for case in cases]
        )
        for condition in CONDITIONS
    }
    policy_values = {
        "label_oracle": [float(item["label_oracle_quality"]) for item in case_analysis],
        "semantic_router": [float(item["semantic_router_quality"]) for item in case_analysis],
        "empirical_oracle": [float(item["empirical_oracle_quality"]) for item in case_analysis],
    }
    policies = {name: aggregate_values(values) for name, values in policy_values.items()}
    base_values = [float(item["quality_by_condition"]["base"]) for item in case_analysis]
    policy_deltas = {
        name: aggregate_values(
            [value - base for value, base in zip(values, base_values, strict=True)]
        )
        for name, values in policy_values.items()
    }
    specialist_lifts = [
        float(item["specialist_lift"])
        for item in case_analysis
        if item["specialist_lift"] is not None
    ]
    specialization_margins = [
        float(item["specialization_margin"])
        for item in case_analysis
        if item["specialization_margin"] is not None
    ]
    opportunities = [float(item["routing_opportunity"]) for item in case_analysis]
    labeled = [item for item in case_analysis if item["correct_labeled_expert"] is not None]
    tie_wins = sum(bool(item["primary_tie_inclusive_win"]) for item in labeled)
    sole_wins = sum(bool(item["primary_sole_win"]) for item in labeled)
    strict_improvements = sum(value > TIE_TOLERANCE for value in opportunities)
    opportunity_stats = aggregate_values(opportunities)
    strong = bool(float(opportunity_stats["mean"]) >= 0.10 and strict_improvements >= 3)
    tie_rate = tie_wins / len(labeled) if labeled else 0.0
    usually_wins = tie_rate >= 0.60
    if not strong:
        classification = "expert_pool_bottleneck"
    elif usually_wins:
        classification = "expert_pool_viable"
    else:
        classification = "label_or_routing_bottleneck"

    cell_stdevs = [float(cell["quality_standard_deviation"]) for cell in cells]
    cell_ranges = [float(cell["quality_range"]) for cell in cells]
    summary = {
        "experiment_version": "expert-quality-diagnostic-1.0.0",
        "backend": "transformers-peft",
        "backend_kind": "real",
        "statistical_unit": "benchmark_case",
        "technical_repetitions_per_cell": 3,
        "generation_count": len(rows),
        "case_count": len(cases),
        "cell_count": len(cells),
        "conditions": direct,
        "policies": policies,
        "policy_delta_base": policy_deltas,
        "metrics": {
            "specialist_lift": aggregate_values(specialist_lifts),
            "specialization_margin": aggregate_values(specialization_margins),
            "routing_opportunity": opportunity_stats,
        },
        "winner_rates": {
            "labeled_case_count": len(labeled),
            "tie_inclusive_win_count": tie_wins,
            "tie_inclusive_win_rate": tie_rate,
            "strict_sole_winner_count": sole_wins,
            "strict_sole_winner_rate": sole_wins / len(labeled) if labeled else 0.0,
        },
        "decision_gate": {
            "classification": classification,
            "strong_advantage": strong,
            "mean_routing_opportunity_threshold": 0.10,
            "strict_improvement_case_threshold": 3,
            "strict_improvement_case_count": strict_improvements,
            "primary_tie_inclusive_threshold": 0.60,
            "primary_usually_wins": usually_wins,
        },
        "completion": {
            "expected_generations": expected_row_count,
            "expected_cells": len(cases) * len(CONDITIONS),
            "complete": len(rows) == expected_row_count and len(cells) == len(cases) * 4,
        },
        "termination": {
            "truncated_count": sum(bool(row["truncated"]) for row in rows),
            "truncation_rate": sum(bool(row["truncated"]) for row in rows) / len(rows),
            "eos_completed_count": sum(bool(row["eos_completed"]) for row in rows),
        },
        "technical_repetition_variability": {
            "cell_count": len(cells),
            "exact_score_agreement_count": sum(
                bool(cell["exact_score_agreement"]) for cell in cells
            ),
            "exact_score_agreement_rate": sum(bool(cell["exact_score_agreement"]) for cell in cells)
            / len(cells),
            "mean_within_cell_standard_deviation": statistics.fmean(cell_stdevs),
            "max_within_cell_standard_deviation": max(cell_stdevs),
            "mean_within_cell_score_range": statistics.fmean(cell_ranges),
            "max_within_cell_score_range": max(cell_ranges),
        },
    }
    return cells, case_analysis, summary


def write_matrix(case_analysis: list[dict[str, Any]], path: Path) -> None:
    columns = [
        "case_id",
        "expected_experts",
        "base",
        "code",
        "math",
        "science",
        "label_oracle",
        "semantic_router",
        "empirical_oracle",
        "empirical_best",
        "specialist_lift",
        "specialization_margin",
        "routing_opportunity",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for item in case_analysis:
            qualities = item["quality_by_condition"]
            writer.writerow(
                {
                    "case_id": item["case_id"],
                    "expected_experts": ";".join(item["expected_experts"]),
                    **{condition: qualities[condition] for condition in CONDITIONS},
                    "label_oracle": item["label_oracle_quality"],
                    "semantic_router": item["semantic_router_quality"],
                    "empirical_oracle": item["empirical_oracle_quality"],
                    "empirical_best": ";".join(item["empirical_best"]),
                    "specialist_lift": item["specialist_lift"],
                    "specialization_margin": item["specialization_margin"],
                    "routing_opportunity": item["routing_opportunity"],
                }
            )


def generate_heatmap(case_analysis: list[dict[str, Any]], path: Path) -> None:
    values = [
        [float(item["quality_by_condition"][condition]) for condition in CONDITIONS]
        for item in case_analysis
    ]
    figure, axis = plt.subplots(figsize=(7.2, 5.6))
    image = axis.imshow(values, vmin=0, vmax=1, cmap="viridis", aspect="auto")
    axis.set_xticks(range(len(CONDITIONS)), [item.title() for item in CONDITIONS])
    axis.set_yticks(range(len(case_analysis)), [str(item["case_id"]) for item in case_analysis])
    axis.set_title("Real expert-quality matrix (cell means, n=3 technical repetitions)")
    for row_index, row in enumerate(values):
        for column_index, value in enumerate(row):
            color = "white" if value < 0.55 else "black"
            axis.text(
                column_index, row_index, f"{value:.2f}", ha="center", va="center", color=color
            )
    figure.colorbar(image, ax=axis, label="Fixed-rubric quality")
    figure.tight_layout()
    figure.savefig(path, dpi=180)
    plt.close(figure)


def write_report(
    summary: dict[str, Any],
    case_analysis: list[dict[str, Any]],
    manifest: dict[str, Any],
    path: Path,
) -> None:
    def format_stat(stat: dict[str, Any]) -> str:
        interval = stat["confidence_interval_95"]
        return f"{stat['mean']:.3f} [{interval[0]:.3f}, {interval[1]:.3f}] (n={stat['count']})"

    classification = str(summary["decision_gate"]["classification"])
    conclusions = {
        "expert_pool_viable": "The fixed expert pool is worth routing: it has strong empirical upside and primary labeled specialists usually occur among the best conditions.",
        "label_or_routing_bottleneck": "The fixed expert pool has useful quality diversity, but preregistered labels and routing are not aligned with which condition actually performs best.",
        "expert_pool_bottleneck": "The fixed expert pool is not worth router optimization under this benchmark: its empirical-oracle advantage does not clear the preregistered gate.",
    }
    lines = [
        "# Expert-Quality Diagnostic",
        "",
        f"**Backend:** real `{summary['backend']}` on `{manifest['device']['device_class']}`. No deterministic or simulated quality results appear in this report.",
        "",
        f"**Decision:** `{classification}`. {conclusions[classification]}",
        "",
        "## Aggregate quality",
        "",
        "All intervals are 95% percentile bootstraps over the nine benchmark cases. Repetitions are averaged within each case-condition cell first.",
        "",
        "| Condition or policy | Mean [95% CI] |",
        "|---|---:|",
    ]
    for name in CONDITIONS:
        lines.append(f"| {name} | {format_stat(summary['conditions'][name])} |")
    for name in ("label_oracle", "semantic_router", "empirical_oracle"):
        lines.append(f"| {name} | {format_stat(summary['policies'][name])} |")
    lines.extend(
        [
            "",
            "## Diagnostic metrics",
            "",
            "| Metric | Mean [95% CI] |",
            "|---|---:|",
            f"| Specialist lift | {format_stat(summary['metrics']['specialist_lift'])} |",
            f"| Specialization margin | {format_stat(summary['metrics']['specialization_margin'])} |",
            f"| Routing opportunity | {format_stat(summary['metrics']['routing_opportunity'])} |",
            "",
            f"Empirical oracle strictly improved over base on **{summary['decision_gate']['strict_improvement_case_count']}/9** cases. The primary labeled specialist was in the best tie set on **{summary['winner_rates']['tie_inclusive_win_count']}/{summary['winner_rates']['labeled_case_count']}** labeled cases ({summary['winner_rates']['tie_inclusive_win_rate']:.1%}) and was the sole winner on **{summary['winner_rates']['strict_sole_winner_count']}/{summary['winner_rates']['labeled_case_count']}** ({summary['winner_rates']['strict_sole_winner_rate']:.1%}).",
            "",
            "## Termination and repetition stability",
            "",
            f"The fixed 384-token ceiling was reached by **{summary['termination']['truncated_count']}/{summary['generation_count']}** generations ({summary['termination']['truncation_rate']:.1%}). Exact quality-score agreement occurred in **{summary['technical_repetition_variability']['exact_score_agreement_count']}/{summary['cell_count']}** cells ({summary['technical_repetition_variability']['exact_score_agreement_rate']:.1%}); mean within-cell sample standard deviation was `{summary['technical_repetition_variability']['mean_within_cell_standard_deviation']:.4f}` and the maximum was `{summary['technical_repetition_variability']['max_within_cell_standard_deviation']:.4f}`.",
            "",
            "## Expert-specialization matrix",
            "",
            "| Case | Expected | Base | Code | Math | Science | Empirical best | Opportunity |",
            "|---|---|---:|---:|---:|---:|---|---:|",
        ]
    )
    for item in case_analysis:
        quality = item["quality_by_condition"]
        lines.append(
            f"| {item['case_id']} | {', '.join(item['expected_experts']) or 'base'} | "
            f"{quality['base']:.3f} | {quality['code']:.3f} | {quality['math']:.3f} | "
            f"{quality['science']:.3f} | {', '.join(item['empirical_best'])} | "
            f"{item['routing_opportunity']:.3f} |"
        )
    mismatches = [
        item
        for item in case_analysis
        if item["correct_labeled_expert"] is not None
        and not bool(item["primary_tie_inclusive_win"])
    ]
    lines.extend(["", "## Label mismatches", ""])
    if mismatches:
        for item in mismatches:
            lines.append(
                f"- `{item['case_id']}`: primary `{item['correct_labeled_expert']}`; empirical best `{item['empirical_best']}`; qualities `{item['quality_by_condition']}`."
            )
    else:
        lines.append("No primary-label mismatch was observed under the tie-inclusive rule.")
    lines.extend(
        [
            "",
            "## Limits",
            "",
            "This is a nine-case, fixed-rubric diagnostic of one pinned base and three public LoRAs on one Apple MPS device. The rubric measures requested concepts, not broad human preference. Technical repetitions measure inference/evaluation stability and are not independent benchmark samples. The empirical oracle is post-generation and estimates available opportunity; it is not a deployable routing policy. Negative and tied results are retained.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
