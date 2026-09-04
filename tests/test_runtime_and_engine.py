from __future__ import annotations

from selectivellm.config import SelectiveLLMConfig
from selectivellm.engine import SelectiveLLM
from selectivellm.routing.baselines import OracleRouter


def test_engine_separates_declared_capacity_from_accelerator_memory(
    control_config: SelectiveLLMConfig,
) -> None:
    engine = SelectiveLLM.from_config(config=control_config)
    result = engine.generate("Implement a Python function")
    assert result.backend == "deterministic-control"
    assert result.backend_kind == "control"
    assert result.memory.declared_resident_capacity_mb > 0
    assert result.memory.declared_base_capacity_mb == 500
    assert result.memory.declared_expert_capacity_mb > 0
    assert result.memory.accelerator_peak_allocated_mb is None
    assert not result.memory.accelerator_measurement_available
    assert result.memory.kv_cache_memory_mb is None
    assert result.memory.breakdown_unavailable_reason is not None
    assert result.backend_metadata["physical_vram_claim"] is False


def test_cache_hit_counts_experts_not_pinned_base(
    control_config: SelectiveLLMConfig,
) -> None:
    control_config.router.type = "oracle"
    engine = SelectiveLLM.from_config(config=control_config, router=OracleRouter())
    first = engine.generate("Python", expected_experts=["python_expert"])
    second = engine.generate("Python again", expected_experts=["python_expert"])
    assert first.metrics.cache_misses == 1
    assert first.metrics.cache_hits == 0
    assert second.metrics.cache_hits == 1
    assert second.metrics.cache_misses == 0


def test_cache_disabled_unloads_expert_after_request(
    control_config: SelectiveLLMConfig,
) -> None:
    control_config.runtime.cache_enabled = False
    engine = SelectiveLLM.from_config(config=control_config, router=OracleRouter())
    result = engine.generate("Python", expected_experts=["python_expert"])
    assert any(event.action == "unload" for event in result.runtime_events)
    assert list(engine.runtime.resident) == ["base"]


def test_lru_evicts_unprotected_expert_under_budget(
    control_config: SelectiveLLMConfig,
) -> None:
    engine = SelectiveLLM.from_config(config=control_config, router=OracleRouter())
    engine.generate("Python", expected_experts=["python_expert"])
    result = engine.generate(
        "Math and circuits",
        expected_experts=["math_expert", "electrical_engineering_expert"],
    )
    assert any(
        event.action == "unload" and event.component_id == "python_expert"
        for event in result.runtime_events
    )
    assert result.memory.declared_resident_capacity_mb <= control_config.runtime.memory_budget_mb
