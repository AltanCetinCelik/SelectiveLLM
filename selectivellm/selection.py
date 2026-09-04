"""Budget-aware conversion of ranked routes into executable capacity plans."""

from __future__ import annotations

from time import perf_counter

from selectivellm.registry import CapacityRegistry
from selectivellm.schemas import PlanDecision, RoutingDecision


class BudgetPlanner:
    def __init__(self, budget_mb: float) -> None:
        self.budget_mb = budget_mb

    def plan(
        self,
        routing: RoutingDecision,
        registry: CapacityRegistry,
        *,
        allow_over_budget: bool = False,
    ) -> PlanDecision:
        started = perf_counter()
        base_ids = [component.id for component in registry.base_components()]
        selected = registry.resolve_dependencies([*base_ids, *routing.selected])
        rejected: dict[str, str] = {}
        required_memory = registry.total_memory_mb(selected)

        if not allow_over_budget and required_memory > self.budget_mb:
            candidate_order = [item.component_id for item in reversed(routing.candidates)]
            protected = set(base_ids)
            for component_id in candidate_order:
                if required_memory <= self.budget_mb:
                    break
                if component_id not in selected or component_id in protected:
                    continue
                dependents = [
                    item.id
                    for item in registry.all()
                    if component_id in item.dependencies and item.id in selected
                ]
                removable = [component_id, *dependents]
                selected = [item for item in selected if item not in removable]
                rejected[component_id] = "memory_budget"
                required_memory = registry.total_memory_mb(selected)

        if required_memory > self.budget_mb and not allow_over_budget:
            raise MemoryError(
                f"required base capacity {required_memory:.1f} MB exceeds budget "
                f"{self.budget_mb:.1f} MB"
            )
        return PlanDecision(
            selected=selected,
            rejected=rejected,
            required_memory_mb=required_memory,
            budget_mb=self.budget_mb,
            latency_ms=(perf_counter() - started) * 1000,
        )
