from __future__ import annotations

from copy import deepcopy
from importlib.resources import as_file, files
from pathlib import Path

import pytest

from selectivellm.dense_capacity.benchmark import DenseBenchmarkDataset, validate_benchmark

FROZEN_CANONICAL_SHA256 = "f4cf067de00d490a036488520768c82a5e0ea7bd0a126946b887fc5fd679d5e0"


def _dataset() -> DenseBenchmarkDataset:
    resource = files("selectivellm.resources").joinpath("dense_capacity_mcq_v1.yaml")
    with as_file(resource) as path:
        return DenseBenchmarkDataset.from_yaml(Path(path))


def test_frozen_dense_benchmark_is_valid_and_hash_stable() -> None:
    dataset = _dataset()
    report = validate_benchmark(dataset)

    assert report["status"] == "valid"
    assert report["case_count"] == 80
    assert report["benchmark_sha256"] == FROZEN_CANONICAL_SHA256
    assert report["maximum_cross_split_five_gram_jaccard"] < 0.65


def test_dense_benchmark_rejects_cross_split_template_reuse() -> None:
    dataset = _dataset()
    modified = deepcopy(dataset)
    discovery = next(case for case in modified.cases if case.split == "discovery")
    evaluation = next(case for case in modified.cases if case.split == "evaluation")
    evaluation.template_family = discovery.template_family

    with pytest.raises(ValueError, match="template families cross splits"):
        validate_benchmark(modified)


def test_dense_benchmark_rejects_design_smoke_test_topic() -> None:
    dataset = _dataset()
    modified = deepcopy(dataset)
    modified.cases[0].question = "What is the time complexity of binary search?"

    with pytest.raises(ValueError, match="excluded design-smoke-test topic"):
        validate_benchmark(modified)
