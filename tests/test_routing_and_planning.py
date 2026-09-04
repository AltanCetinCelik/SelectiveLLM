from __future__ import annotations

import pytest

from selectivellm.analyzers import DeterministicEmbeddingAnalyzer
from selectivellm.config import RouterConfig
from selectivellm.registry import CapacityRegistry
from selectivellm.routing import create_router
from selectivellm.routing.baselines import OracleRouter, RandomRouter
from selectivellm.selection import BudgetPlanner

PROMPT = "Use Python to simulate an RLC circuit and plot the transient response."


def test_hybrid_router_can_express_multiple_capabilities(
    registry: CapacityRegistry,
) -> None:
    profile = DeterministicEmbeddingAnalyzer().analyze(PROMPT)
    config = RouterConfig(type="hybrid", top_k=3, threshold=0.1)
    decision = create_router(config, seed=42).route(profile, registry)
    assert len(decision.selected) >= 2
    assert "python_expert" in decision.selected
    assert "electrical_engineering_expert" in decision.selected


def test_budget_planner_records_rejected_multi_domain_capacity(
    registry: CapacityRegistry,
) -> None:
    profile = DeterministicEmbeddingAnalyzer().analyze(PROMPT)
    decision = OracleRouter().route(
        profile,
        registry,
        expected_experts=["python_expert", "electrical_engineering_expert", "math_expert"],
    )
    plan = BudgetPlanner(900).plan(decision, registry)
    assert plan.required_memory_mb <= 900
    assert len(plan.rejected) == 1
    assert len([item for item in plan.selected if item != "base"]) == 2


def test_oracle_requires_ground_truth(registry: CapacityRegistry) -> None:
    profile = DeterministicEmbeddingAnalyzer().analyze("Explain a circuit")
    with pytest.raises(ValueError, match="expected_experts"):
        OracleRouter().route(profile, registry)


def test_random_router_is_seeded_per_prompt(registry: CapacityRegistry) -> None:
    profile = DeterministicEmbeddingAnalyzer().analyze("Explain a circuit")
    first = RandomRouter(seed=7, top_k=2).route(profile, registry)
    second = RandomRouter(seed=7, top_k=2).route(profile, registry)
    assert first.selected == second.selected
    assert [item.score for item in first.candidates] == [item.score for item in second.candidates]
