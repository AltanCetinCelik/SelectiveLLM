"""Router contract and shared selection helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from selectivellm.registry import CapacityRegistry
from selectivellm.schemas import PromptProfile, RouteCandidate, RoutingDecision


class Router(ABC):
    name = "router"
    version = "1.0.0"

    @abstractmethod
    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        """Rank and select capacity for one analyzed prompt."""


def select_candidates(
    candidates: list[RouteCandidate], *, top_k: int, threshold: float
) -> list[str]:
    eligible = [candidate for candidate in candidates if candidate.score >= threshold]
    return [candidate.component_id for candidate in eligible[:top_k]]
