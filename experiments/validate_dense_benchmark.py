"""Validate and fingerprint the dense-capacity benchmark without model access."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from selectivellm.dense_capacity.benchmark import DenseBenchmarkDataset, validate_benchmark

BENCHMARK = Path("selectivellm/resources/dense_capacity_mcq_v1.yaml")
REPORT = Path("selectivellm/resources/dense_capacity_mcq_v1.validation.json")
HASHES = Path("selectivellm/resources/dense_capacity_mcq_v1.hashes.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    dataset = DenseBenchmarkDataset.from_yaml(BENCHMARK)
    report = validate_benchmark(dataset)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    hashes = {
        "benchmark_version": dataset.benchmark_version,
        "benchmark_file_sha256": sha256(BENCHMARK),
        "benchmark_canonical_sha256": dataset.canonical_hash(),
        "validation_report_sha256": sha256(REPORT),
    }
    HASHES.write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
