"""Fixed deterministic evaluation for the v0.1.1 real-model benchmark."""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field


class RealEvaluationSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["exact_contains", "numeric", "concept_coverage"]
    answers: list[str] = Field(default_factory=list)
    expected_number: float | None = None
    tolerance: float = Field(default=1e-6, ge=0)
    concept_groups: list[list[str]] = Field(default_factory=list)


class RealBenchmarkCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    prompt: str
    domain: list[str]
    expected_experts: list[str]
    tags: list[str] = Field(default_factory=list)
    evaluation: RealEvaluationSpec


class RealBenchmarkDataset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str
    benchmark_version: str
    evaluation_schema_version: str
    name: str
    description: str
    cases: list[RealBenchmarkCase]
    high_locality_order: list[str]
    low_locality_order: list[str]

    @classmethod
    def from_yaml(cls, path: str | Path) -> RealBenchmarkDataset:
        with Path(path).open(encoding="utf-8") as handle:
            dataset = cls.model_validate(yaml.safe_load(handle))
        ids = [case.id for case in dataset.cases]
        if sorted(dataset.high_locality_order) != sorted(ids):
            raise ValueError("high-locality order must contain every case exactly once")
        if sorted(dataset.low_locality_order) != sorted(ids):
            raise ValueError("low-locality order must contain every case exactly once")
        return dataset

    def ordered(self, locality: str) -> list[RealBenchmarkCase]:
        order = self.high_locality_order if locality == "high" else self.low_locality_order
        by_id = {case.id: case for case in self.cases}
        return [by_id[case_id] for case_id in order]


def _normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9+#./()^-]+", text.lower()))


def _numbers(text: str) -> list[float]:
    numbers: list[float] = []
    for numerator, denominator in re.findall(r"(?<!\d)(-?\d+)\s*/\s*(\d+)(?!\d)", text):
        if int(denominator) != 0:
            numbers.append(float(Fraction(int(numerator), int(denominator))))
    for raw in re.findall(r"(?<![\w/])-?(?:\d+\.\d+|\d+)(?![\w/])", text):
        numbers.append(float(raw))
    return numbers


def score_response(case: RealBenchmarkCase, response: str) -> tuple[float, dict[str, object]]:
    spec = case.evaluation
    normalized = _normalize(response)
    if spec.type == "exact_contains":
        matched_answers = [answer for answer in spec.answers if _normalize(answer) in normalized]
        return float(bool(matched_answers)), {
            "type": spec.type,
            "matched_answers": matched_answers,
        }
    if spec.type == "numeric":
        assert spec.expected_number is not None
        values = _numbers(response)
        matched_numbers = [
            value for value in values if abs(value - spec.expected_number) <= spec.tolerance
        ]
        return float(bool(matched_numbers)), {
            "type": spec.type,
            "expected": spec.expected_number,
            "tolerance": spec.tolerance,
            "extracted": values,
            "matched": matched_numbers,
        }
    matched_groups: list[list[str]] = []
    for alternatives in spec.concept_groups:
        matches = [item for item in alternatives if _normalize(item) in normalized]
        if matches:
            matched_groups.append(matches)
    denominator = len(spec.concept_groups)
    score = len(matched_groups) / denominator if denominator else 0.0
    return score, {
        "type": spec.type,
        "matched_group_count": len(matched_groups),
        "group_count": denominator,
        "matched_groups": matched_groups,
    }
