from __future__ import annotations

from typing import Any

import pytest

from selectivellm.real_validation.evaluation import (
    RealBenchmarkCase,
    RealEvaluationSpec,
)
from selectivellm.real_validation.expert_quality import (
    CONDITIONS,
    aggregate_diagnostic,
    aggregate_values,
)


def _case(case_id: str, expected_experts: list[str]) -> RealBenchmarkCase:
    return RealBenchmarkCase(
        id=case_id,
        prompt=f"prompt {case_id}",
        domain=["test"],
        expected_experts=expected_experts,
        evaluation=RealEvaluationSpec(type="exact_contains", answers=["answer"]),
    )


def _matrix_rows(
    cases: list[RealBenchmarkCase],
    cell_scores: dict[tuple[str, str], list[float]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for condition in CONDITIONS:
        for case in cases:
            for repetition, quality in enumerate(cell_scores[(case.id, condition)], start=1):
                rows.append(
                    {
                        "case_id": case.id,
                        "condition": condition,
                        "repetition": repetition,
                        "quality": quality,
                        "truncated": False,
                        "eos_completed": True,
                    }
                )
    return rows


def _routes(cases: list[RealBenchmarkCase]) -> list[dict[str, Any]]:
    return [
        {
            "case_id": case.id,
            "selected_experts": list(case.expected_experts[:1]),
        }
        for case in cases
    ]


def test_empirical_oracle_uses_cell_mean_and_preserves_ties() -> None:
    cases = [_case(f"case_{index}", ["code_expert"]) for index in range(9)]
    scores: dict[tuple[str, str], list[float]] = {}
    for case in cases:
        scores[(case.id, "base")] = [0.3, 0.3, 0.3]
        scores[(case.id, "code")] = [0.0, 0.0, 1.0]
        scores[(case.id, "math")] = [0.5, 0.5, 0.5]
        scores[(case.id, "science")] = [0.5, 0.5, 0.5]

    _, analysis, summary = aggregate_diagnostic(_matrix_rows(cases, scores), cases, _routes(cases))

    assert analysis[0]["quality_by_condition"]["code"] == pytest.approx(1 / 3)
    assert analysis[0]["empirical_best"] == ["math", "science"]
    assert analysis[0]["empirical_oracle_quality"] == 0.5
    assert summary["winner_rates"]["tie_inclusive_win_rate"] == 0.0
    assert summary["decision_gate"]["classification"] == "label_or_routing_bottleneck"


def test_multi_label_expected_experts_are_excluded_from_wrong_experts() -> None:
    expected_sets = [
        ["science_expert", "math_expert"],
        ["code_expert", "science_expert", "math_expert"],
        *[["code_expert"] for _ in range(7)],
    ]
    cases = [_case(f"case_{index}", expected) for index, expected in enumerate(expected_sets)]
    scores = {(case.id, condition): [0.8, 0.8, 0.8] for case in cases for condition in CONDITIONS}
    scores[("case_0", "code")] = [0.2, 0.2, 0.2]

    _, analysis, _ = aggregate_diagnostic(_matrix_rows(cases, scores), cases, _routes(cases))

    assert analysis[0]["correct_labeled_expert"] == "science_expert"
    assert analysis[0]["wrong_experts"] == ["code_expert"]
    assert analysis[0]["specialization_margin"] == pytest.approx(0.6)
    assert analysis[1]["wrong_experts"] == []
    assert analysis[1]["specialization_margin"] is None


def test_tie_inclusive_gate_and_sole_winner_rate_are_separate() -> None:
    cases = [_case(f"case_{index}", ["code_expert"]) for index in range(9)]
    scores: dict[tuple[str, str], list[float]] = {}
    for index, case in enumerate(cases):
        base = 0.0 if index < 3 else 0.5
        code = 0.5
        scores[(case.id, "base")] = [base] * 3
        scores[(case.id, "code")] = [code] * 3
        scores[(case.id, "math")] = [code] * 3
        scores[(case.id, "science")] = [0.0] * 3

    _, _, summary = aggregate_diagnostic(_matrix_rows(cases, scores), cases, _routes(cases))

    assert summary["metrics"]["routing_opportunity"]["mean"] == pytest.approx(1 / 6)
    assert summary["decision_gate"]["strict_improvement_case_count"] == 3
    assert summary["winner_rates"]["tie_inclusive_win_rate"] == 1.0
    assert summary["winner_rates"]["strict_sole_winner_rate"] == 0.0
    assert summary["decision_gate"]["classification"] == "expert_pool_viable"


def test_bootstrap_is_deterministic_and_counts_cases() -> None:
    first = aggregate_values([0.0, 0.5, 1.0], bootstrap_resamples=200)
    second = aggregate_values([0.0, 0.5, 1.0], bootstrap_resamples=200)

    assert first == second
    assert first["count"] == 3
    assert first["bootstrap_unit"] == "benchmark_case"
