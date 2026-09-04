"""Real-model validation assets, evaluation, runtime, and runner."""

from selectivellm.real_validation.assets import ASSETS, verify_compatibility
from selectivellm.real_validation.evaluation import (
    RealBenchmarkCase,
    RealBenchmarkDataset,
    score_response,
)

__all__ = [
    "ASSETS",
    "RealBenchmarkCase",
    "RealBenchmarkDataset",
    "score_response",
    "verify_compatibility",
]
