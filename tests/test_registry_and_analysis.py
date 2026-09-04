from __future__ import annotations

from pathlib import Path

import pytest

from selectivellm.analyzers import DeterministicEmbeddingAnalyzer, stable_embedding
from selectivellm.registry import CapacityRegistry
from selectivellm.registry.registry import RegistryError


def test_registry_resolves_base_before_expert(registry: CapacityRegistry) -> None:
    assert registry.resolve_dependencies(["python_expert"]) == ["base", "python_expert"]
    assert registry.version == "hero-control-1.0.0"


def test_registry_rejects_dependency_cycle(tmp_path: Path) -> None:
    path = tmp_path / "cycle.yaml"
    path.write_text(
        """schema_version: '1.0.0'
registry_version: test
components:
  - id: a
    name: A
    type: adapter
    description: A
    memory_mb: 1
    backend: test
    dependencies: [b]
  - id: b
    name: B
    type: adapter
    description: B
    memory_mb: 1
    backend: test
    dependencies: [a]
""",
        encoding="utf-8",
    )
    with pytest.raises(RegistryError, match="dependency cycle"):
        CapacityRegistry.from_yaml(path)


def test_analyzer_preserves_three_capabilities_for_rlc_simulation() -> None:
    profile = DeterministicEmbeddingAnalyzer().analyze(
        "Use Python to simulate an RLC circuit and plot the transient response."
    )
    assert {"python", "electrical_engineering", "mathematics"} <= set(profile.capabilities)
    assert profile.difficulty == "high"


def test_stable_embedding_is_deterministic_and_normalized() -> None:
    first = stable_embedding("identical text", 64)
    second = stable_embedding("identical text", 64)
    assert first == second
    assert sum(value * value for value in first) == pytest.approx(1.0)
