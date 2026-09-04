from __future__ import annotations

import pytest

from selectivellm.metrics import aggregate
from selectivellm.provenance import assert_compatible, benchmark_fingerprint
from selectivellm.schemas import RunManifest


def _manifest(run_id: str, fingerprint: str) -> RunManifest:
    return RunManifest(
        run_id=run_id,
        status="completed",
        backend="deterministic-control",
        backend_kind="control",
        model_identity="control-v1",
        adapter_set=["python_expert"],
        benchmark_version="hero-1.0.0",
        benchmark_content_hash="benchmark-hash",
        registry_version="1.0.0",
        registry_content_hash="registry-hash",
        routing_config_version="1.0.0",
        routing_config_hash="router-hash",
        seed_policy="fixed:42",
        device_class="cpu",
        measurement_semantics="declared",
        benchmark_fingerprint=fingerprint,
        configuration_fingerprint="config",
    )


def test_aggregate_reports_variability_and_confidence_interval() -> None:
    stats = aggregate([1, 2, 3, 4])
    assert stats.count == 4
    assert stats.mean == 2.5
    assert stats.median == 2.5
    assert stats.p95 is not None
    assert stats.standard_deviation is not None and stats.standard_deviation > 0
    assert stats.confidence_interval_95 is not None


def test_single_sample_does_not_claim_confidence_interval() -> None:
    stats = aggregate([1])
    assert stats.standard_deviation == 0
    assert stats.confidence_interval_95 is None


def test_fingerprint_is_order_stable() -> None:
    fields = {
        "backend": "deterministic-control",
        "backend_kind": "control",
        "model_identity": "control-v1",
        "adapter_set": ["a"],
        "benchmark_version": "1",
        "benchmark_content_hash": "benchmark-hash",
        "registry_version": "1",
        "registry_content_hash": "registry-hash",
        "routing_config_version": "1",
        "routing_config_hash": "router-hash",
        "metric_schema_version": "1",
        "seed_policy": "fixed",
        "device_class": "cpu",
        "measurement_semantics": "declared",
    }
    assert benchmark_fingerprint(**fields) == benchmark_fingerprint(
        **dict(reversed(list(fields.items())))
    )


def test_validity_guard_rejects_incompatible_runs() -> None:
    with pytest.raises(ValueError, match="incompatible benchmark fingerprints"):
        assert_compatible([_manifest("one", "a"), _manifest("two", "b")])
