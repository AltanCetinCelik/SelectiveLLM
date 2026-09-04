"""Composable top-k and threshold policy wrappers."""

from __future__ import annotations

from selectivellm.registry import CapacityRegistry
from selectivellm.routing.base import Router, select_candidates
from selectivellm.schemas import PromptProfile, RoutingDecision


class TopKRouter(Router):
    name = "topk"

    def __init__(self, inner: Router, top_k: int) -> None:
        self.inner = inner
        self.top_k = top_k

    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        decision = self.inner.route(profile, registry, expected_experts=expected_experts)
        decision.router = f"topk({decision.router})"
        decision.selected = [
            candidate.component_id for candidate in decision.candidates[: self.top_k]
        ]
        decision.metadata["top_k"] = self.top_k
        return decision


class ThresholdRouter(Router):
    name = "threshold"

    def __init__(self, inner: Router, threshold: float, top_k: int = 100) -> None:
        self.inner = inner
        self.threshold = threshold
        self.top_k = top_k

    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        decision = self.inner.route(profile, registry, expected_experts=expected_experts)
        decision.router = f"threshold({decision.router})"
        decision.selected = select_candidates(
            decision.candidates, top_k=self.top_k, threshold=self.threshold
        )
        decision.metadata["threshold"] = self.threshold
        return decision
