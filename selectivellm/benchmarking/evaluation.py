"""Routing and output-quality evaluation with explicit score semantics."""

from __future__ import annotations

import re
from collections import Counter

from selectivellm.schemas import BenchmarkCase

WORD_RE = re.compile(r"\w+")


def routing_scores(expected: list[str], selected: list[str]) -> dict[str, float]:
    expected_set = set(expected)
    selected_set = set(selected)
    true_positive = len(expected_set & selected_set)
    precision = true_positive / len(selected_set) if selected_set else float(not expected_set)
    recall = true_positive / len(expected_set) if expected_set else float(not selected_set)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    top1 = float(bool(expected_set) and bool(selected) and selected[0] in expected_set)
    if not expected_set:
        top1 = float(not selected)
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "top1_accuracy": top1,
        "topk_recall": recall,
        "false_activations": float(len(selected_set - expected_set)),
    }


def token_f1(prediction: str, reference: str) -> float:
    predicted = Counter(token.lower() for token in WORD_RE.findall(prediction))
    expected = Counter(token.lower() for token in WORD_RE.findall(reference))
    overlap = sum((predicted & expected).values())
    if not predicted or not expected:
        return float(predicted == expected)
    precision = overlap / sum(predicted.values())
    recall = overlap / sum(expected.values())
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def output_quality(
    case: BenchmarkCase,
    prediction: str,
    selected_experts: list[str],
    *,
    backend_kind: str,
) -> tuple[float, str]:
    if backend_kind == "control":
        required = set(case.expected_experts)
        selected = set(selected_experts)
        if not required:
            score = 1.0 if not selected else max(0.0, 1.0 - 0.05 * len(selected))
        else:
            coverage = len(required & selected) / len(required)
            score = 0.35 + 0.65 * coverage
        return score, "synthetic_capability_coverage_v1"
    if case.evaluation == "exact_match":
        return float(prediction.strip().lower() == case.reference.strip().lower()), "exact_match"
    return token_f1(prediction, case.reference), "token_f1"
