from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path

import pytest

from selectivellm.backends.transformers import TransformersPeftBackend
from selectivellm.benchmarking.evaluation import routing_scores
from selectivellm.config import BackendConfig
from selectivellm.real_validation.assets import validate_compatibility_report
from selectivellm.real_validation.evaluation import (
    RealBenchmarkCase,
    RealBenchmarkDataset,
    RealEvaluationSpec,
    score_response,
)
from selectivellm.real_validation.report import CACHE_REQUEST_HIT_RATE, METRICS, summarize
from selectivellm.real_validation.runtime import AdapterResidencyManager, memory_checkpoint
from selectivellm.schemas import CapacityComponent, ComponentType


class FakeAdapterBackend:
    def __init__(self) -> None:
        self.loaded_adapters: set[str] = set()
        self.active_adapters: list[str] = []

    def load_component(self, component: CapacityComponent) -> None:
        self.loaded_adapters.add(component.id)

    def unload_component(self, component: CapacityComponent) -> None:
        self.loaded_adapters.discard(component.id)

    def synchronize(self) -> None:
        return None

    def memory_metrics(self) -> dict[str, float | None]:
        return {
            "mps_current_allocated_mb": 100.0 + 10 * len(self.loaded_adapters),
            "mps_driver_allocated_mb": 125.0 + 10 * len(self.loaded_adapters),
            "mps_recommended_max_mb": 1024.0,
        }


def _component(component_id: str) -> CapacityComponent:
    return CapacityComponent(
        id=component_id,
        name=component_id,
        type=ComponentType.LORA,
        domain=[component_id],
        description=component_id,
        memory_mb=1,
        backend="fake",
    )


@pytest.mark.parametrize(
    ("case", "response", "expected"),
    [
        (
            RealBenchmarkCase(
                id="exact",
                prompt="p",
                domain=["general"],
                expected_experts=[],
                evaluation=RealEvaluationSpec(type="exact_contains", answers=["Tokyo"]),
            ),
            "Tokyo",
            1.0,
        ),
        (
            RealBenchmarkCase(
                id="numeric",
                prompt="p",
                domain=["mathematics"],
                expected_experts=["math_expert"],
                evaluation=RealEvaluationSpec(
                    type="numeric", expected_number=5 / 36, tolerance=1e-6
                ),
            ),
            "There are five outcomes, so the answer is 5/36.",
            1.0,
        ),
        (
            RealBenchmarkCase(
                id="concepts",
                prompt="p",
                domain=["science"],
                expected_experts=["science_expert"],
                evaluation=RealEvaluationSpec(
                    type="concept_coverage",
                    concept_groups=[["gate charge", "gate capacitance"], ["switching loss"]],
                ),
            ),
            "Gate capacitance must move quickly to reduce switching loss.",
            1.0,
        ),
    ],
)
def test_real_response_scoring_is_fixed_and_deterministic(
    case: RealBenchmarkCase, response: str, expected: float
) -> None:
    score, details = score_response(case, response)
    assert score == expected
    assert details["type"] == case.evaluation.type


def test_real_dataset_orders_are_complete() -> None:
    resource = files("selectivellm.resources").joinpath("real_hero_v1.yaml")
    with as_file(resource) as path:
        dataset = RealBenchmarkDataset.from_yaml(Path(path))
    assert len(dataset.cases) == 9
    assert {case.id for case in dataset.ordered("high")} == {
        case.id for case in dataset.ordered("low")
    }
    assert any(not case.expected_experts for case in dataset.cases)


def test_compatibility_validation_rejects_mixed_lora_signatures() -> None:
    report = {
        "base": {
            "repo_id": "base",
            "requested_revision": "a",
            "resolved_revision": "a",
            "license": "apache-2.0",
            "vocab_size": 10,
        },
        "tokenizer": {
            "repo_id": "base",
            "resolved_revision": "a",
            "vocab_size": 9,
            "max_token_id": 8,
        },
        "adapters": [
            {
                "repo_id": "one",
                "requested_revision": "b",
                "resolved_revision": "b",
                "license": "apache-2.0",
                "base_model_name_or_path": "base",
                "peft_type": "LORA",
                "peft_signature_hash": "rank-8",
            },
            {
                "repo_id": "two",
                "requested_revision": "c",
                "resolved_revision": "c",
                "license": "apache-2.0",
                "base_model_name_or_path": "base",
                "peft_type": "LORA",
                "peft_signature_hash": "rank-16",
            },
        ],
    }
    with pytest.raises(ValueError, match="rank, alpha"):
        validate_compatibility_report(report)


def test_residency_is_distinct_from_activation_and_obeys_cache_size() -> None:
    backend = FakeAdapterBackend()
    components = {item: _component(item) for item in ("code", "math", "science")}
    manager = AdapterResidencyManager(backend, components, cache_size=1)

    events = manager.ensure(["code", "science"])
    assert backend.loaded_adapters == {"code", "science"}
    assert backend.active_adapters == []
    assert sum(event.action == "load" for event in events) == 2

    manager.release(["code", "science"])
    assert len(backend.loaded_adapters) == 1
    checkpoint = memory_checkpoint("after_release", backend)
    assert checkpoint["mps_current_allocated_mb"] == 110.0
    assert checkpoint["mps_driver_allocated_mb"] == 135.0


def test_all_resident_policy_does_not_imply_multi_active() -> None:
    backend = FakeAdapterBackend()
    components = {item: _component(item) for item in ("code", "math", "science")}
    manager = AdapterResidencyManager(backend, components, cache_size=3)
    manager.ensure(components, retain_all=True)

    assert set(manager.resident) == set(components)
    assert backend.active_adapters == []


def test_shared_routing_scores_map_to_real_metric_names() -> None:
    scores = routing_scores(["code_expert"], ["code_expert"])
    real_fields = {
        "routing_precision": scores["precision"],
        "routing_recall": scores["recall"],
        "routing_f1": scores["f1"],
    }
    assert real_fields == {
        "routing_precision": 1.0,
        "routing_recall": 1.0,
        "routing_f1": 1.0,
    }


def test_transformers_backend_unwraps_when_last_adapter_is_evicted() -> None:
    class Base:
        def eval(self) -> None:
            return None

    base = Base()

    class Wrapped:
        def unload(self) -> Base:
            return base

    backend = TransformersPeftBackend(BackendConfig(device="cpu"))
    backend.model = Wrapped()
    backend.loaded_adapters = {"code_expert"}
    backend.active_adapters = ["code_expert"]

    backend.unload_component(_component("code_expert"))

    assert backend.model is base
    assert backend.loaded_adapters == set()
    assert backend.active_adapters == []


def test_real_summary_uses_request_weighted_cache_hit_rate() -> None:
    rows = [
        {
            "policy": "semantic",
            "phase": "warm",
            "cache_hits": 2,
            "cache_misses": 0,
            **{metric: 0.0 for metric in METRICS},
        },
        {
            "policy": "semantic",
            "phase": "warm",
            "cache_hits": 0,
            "cache_misses": 1,
            **{metric: 0.0 for metric in METRICS},
        },
    ]
    summary = summarize(
        rows,
        {
            "run_id": "test",
            "backend": "transformers-peft",
            "benchmark_fingerprint": "fingerprint",
        },
    )

    stats = summary["warm_methods"]["semantic"][CACHE_REQUEST_HIT_RATE]
    assert stats["count"] == 3
    assert stats["mean"] == pytest.approx(2 / 3)
