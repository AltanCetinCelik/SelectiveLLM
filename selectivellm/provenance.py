"""Benchmark fingerprinting and validity guards."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from selectivellm.schemas import RunManifest

COMPATIBILITY_FIELDS = (
    "backend",
    "backend_kind",
    "model_identity",
    "adapter_set",
    "benchmark_version",
    "benchmark_content_hash",
    "registry_version",
    "registry_content_hash",
    "routing_config_version",
    "routing_config_hash",
    "metric_schema_version",
    "seed_policy",
    "device_class",
    "measurement_semantics",
)


def stable_fingerprint(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


def benchmark_fingerprint(**fields: Any) -> str:
    return stable_fingerprint({field: fields[field] for field in COMPATIBILITY_FIELDS})


def assert_compatible(manifests: list[RunManifest]) -> None:
    if not manifests:
        return
    expected = manifests[0].benchmark_fingerprint
    incompatible = [item.run_id for item in manifests[1:] if item.benchmark_fingerprint != expected]
    if incompatible:
        raise ValueError(
            "incompatible benchmark fingerprints; separate these runs before comparison: "
            + ", ".join(incompatible)
        )
