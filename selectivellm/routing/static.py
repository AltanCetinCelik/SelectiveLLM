"""Static routing for controlled experiments and manual operation."""

from __future__ import annotations

from time import perf_counter

from selectivellm.registry import CapacityRegistry
from selectivellm.routing.base import Router
from selectivellm.schemas import PromptProfile, RouteCandidate, RoutingDecision


class StaticRouter(Router):
    name = "static"

    def __init__(self, component_ids: list[str]) -> None:
        self.component_ids = component_ids

    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        del profile, expected_experts
        started = perf_counter()
        selected = [registry.get(component_id).id for component_id in self.component_ids]
        return RoutingDecision(
            router=self.name,
            router_version=self.version,
            selected=selected,
            candidates=[RouteCandidate(component_id=item, score=1.0) for item in selected],
            confidence=1.0 if selected else 0.0,
            latency_ms=(perf_counter() - started) * 1000,
            metadata={"configured": True},
        )
