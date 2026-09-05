"""Versioned benchmark schema and model-free preregistration validation."""

from __future__ import annotations

import ast
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

Domain = Literal["code", "mathematics", "science", "general"]
Split = Literal["discovery", "evaluation"]
AnswerLabel = Literal["A", "B", "C", "D"]
LABELS: tuple[AnswerLabel, ...] = ("A", "B", "C", "D")


class CorrectnessCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["verified"]
    method: Literal["manual", "numeric_expression"]
    expression: str | None = None
    expected_numeric: float | None = None

    @model_validator(mode="after")
    def validate_numeric_fields(self) -> CorrectnessCheck:
        if self.method == "numeric_expression":
            if self.expression is None or self.expected_numeric is None:
                raise ValueError("numeric checks require expression and expected_numeric")
        elif self.expression is not None or self.expected_numeric is not None:
            raise ValueError("manual checks cannot contain numeric fields")
        return self


class DenseBenchmarkCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^dense_(code|math|science|general)_(discovery|eval)_\d{2}$")
    split: Split
    domain: Domain
    question: str = Field(min_length=12)
    options: dict[AnswerLabel, str]
    correct_label: AnswerLabel
    rationale: str = Field(min_length=12)
    template_family: str = Field(pattern=r"^[a-z][a-z0-9_]+$")
    stability_sentinel: bool = False
    correctness: CorrectnessCheck

    @model_validator(mode="after")
    def validate_options(self) -> DenseBenchmarkCase:
        if set(self.options) != set(LABELS) or len(self.options) != 4:
            raise ValueError("options must contain A, B, C, and D exactly once")
        if any(not option.strip() for option in self.options.values()):
            raise ValueError("options cannot be empty")
        if len({option.casefold().strip() for option in self.options.values()}) != 4:
            raise ValueError("options must be distinct")
        return self


class DenseBenchmarkDataset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str
    benchmark_version: str
    name: str
    description: str
    cases: list[DenseBenchmarkCase]

    @classmethod
    def from_yaml(cls, path: str | Path) -> DenseBenchmarkDataset:
        with Path(path).open(encoding="utf-8") as handle:
            return cls.model_validate(yaml.safe_load(handle))

    def canonical_hash(self) -> str:
        payload = json.dumps(
            self.model_dump(mode="json"), sort_keys=True, separators=(",", ":")
        ).encode()
        return hashlib.sha256(payload).hexdigest()


def _normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.casefold()))


def _five_grams(text: str) -> set[tuple[str, ...]]:
    tokens = _normalize(text).split()
    return {tuple(tokens[index : index + 5]) for index in range(max(0, len(tokens) - 4))}


def _case_text(case: DenseBenchmarkCase) -> str:
    return " ".join([case.question, *(case.options[label] for label in LABELS)])


def _jaccard(left: set[tuple[str, ...]], right: set[tuple[str, ...]]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def _safe_numeric(expression: str) -> float:
    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name) and node.id == "pi":
            return math.pi
        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                return float(left**right)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        raise ValueError(f"unsupported numeric expression: {expression}")

    return evaluate(ast.parse(expression, mode="eval"))


def validate_benchmark(dataset: DenseBenchmarkDataset) -> dict[str, object]:
    errors: list[str] = []
    expected_counts: dict[tuple[Domain, Split], int] = {
        (domain, split): 12 if split == "discovery" else 8
        for domain in ("code", "mathematics", "science", "general")
        for split in ("discovery", "evaluation")
    }
    counts = Counter((case.domain, case.split) for case in dataset.cases)
    if len(dataset.cases) != 80:
        errors.append(f"expected 80 cases, found {len(dataset.cases)}")
    if len({case.id for case in dataset.cases}) != len(dataset.cases):
        errors.append("case IDs are not unique")
    if counts != Counter(expected_counts):
        errors.append(f"domain/split counts differ: {dict(counts)}")

    balances: dict[str, dict[str, int]] = {}
    for key, expected_count in expected_counts.items():
        domain, split = key
        group = [case for case in dataset.cases if (case.domain, case.split) == key]
        label_counts = Counter(case.correct_label for case in group)
        expected_per_label = expected_count // 4
        balances[f"{domain}/{split}"] = {label: label_counts[label] for label in LABELS}
        if any(label_counts[label] != expected_per_label for label in LABELS):
            errors.append(f"unbalanced answers for {domain}/{split}: {dict(label_counts)}")

    families_by_split: dict[str, set[str]] = {
        split: {case.template_family for case in dataset.cases if case.split == split}
        for split in ("discovery", "evaluation")
    }
    family_overlap = families_by_split["discovery"] & families_by_split["evaluation"]
    if family_overlap:
        errors.append(f"template families cross splits: {sorted(family_overlap)}")

    normalized = [_normalize(_case_text(case)) for case in dataset.cases]
    if len(set(normalized)) != len(normalized):
        errors.append("normalized duplicate question/options text found")
    if any("binary search" in text for text in normalized):
        errors.append("benchmark contains excluded design-smoke-test topic")

    discovery = [case for case in dataset.cases if case.split == "discovery"]
    evaluation = [case for case in dataset.cases if case.split == "evaluation"]
    maximum_similarity = 0.0
    maximum_pair: tuple[str, str] | None = None
    for left in discovery:
        left_grams = _five_grams(_case_text(left))
        for right in evaluation:
            similarity = _jaccard(left_grams, _five_grams(_case_text(right)))
            if similarity > maximum_similarity:
                maximum_similarity = similarity
                maximum_pair = (left.id, right.id)
    if maximum_similarity > 0.65:
        errors.append(
            f"cross-split 5-gram Jaccard {maximum_similarity:.3f} exceeds 0.65: {maximum_pair}"
        )

    expected_sentinels = {
        case.id
        for domain in ("code", "mathematics", "science", "general")
        for case in sorted(
            [item for item in evaluation if item.domain == domain],
            key=lambda item: item.id,
        )[:2]
    }
    actual_sentinels = {case.id for case in dataset.cases if case.stability_sentinel}
    if actual_sentinels != expected_sentinels:
        errors.append(
            f"sentinels must be first two evaluation IDs per domain: {sorted(expected_sentinels)}"
        )

    numeric_checks = 0
    for case in dataset.cases:
        check = case.correctness
        if check.method == "numeric_expression":
            assert check.expression is not None
            assert check.expected_numeric is not None
            numeric_checks += 1
            observed = _safe_numeric(check.expression)
            if not math.isclose(observed, check.expected_numeric, rel_tol=0, abs_tol=1e-9):
                errors.append(
                    f"numeric correctness failed for {case.id}: {observed} != {check.expected_numeric}"
                )

    report: dict[str, object] = {
        "status": "valid" if not errors else "invalid",
        "schema_version": dataset.schema_version,
        "benchmark_version": dataset.benchmark_version,
        "benchmark_sha256": dataset.canonical_hash(),
        "case_count": len(dataset.cases),
        "domain_split_counts": {
            f"{domain}/{split}": counts[(domain, split)] for domain, split in expected_counts
        },
        "answer_position_counts": balances,
        "unique_id_count": len({case.id for case in dataset.cases}),
        "unique_template_family_count": len({case.template_family for case in dataset.cases}),
        "cross_split_template_family_overlap": sorted(family_overlap),
        "maximum_cross_split_five_gram_jaccard": maximum_similarity,
        "maximum_similarity_pair": list(maximum_pair) if maximum_pair else None,
        "stability_sentinels": sorted(actual_sentinels),
        "manual_correctness_reviews": sum(
            case.correctness.status == "verified" for case in dataset.cases
        ),
        "numeric_expression_checks": numeric_checks,
        "excluded_smoke_test_topic_present": any("binary search" in text for text in normalized),
        "errors": errors,
    }
    if errors:
        raise ValueError("; ".join(errors))
    return report
