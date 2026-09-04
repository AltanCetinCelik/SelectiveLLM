"""Versioned benchmark dataset loading."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from selectivellm.schemas import BenchmarkDataset


def load_dataset(path: str | Path) -> BenchmarkDataset:
    with Path(path).expanduser().resolve().open(encoding="utf-8") as handle:
        raw: dict[str, Any] = yaml.safe_load(handle) or {}
    dataset = BenchmarkDataset.model_validate(raw)
    ids = [case.id for case in dataset.cases]
    if len(ids) != len(set(ids)):
        raise ValueError("benchmark case ids must be unique")
    return dataset
