"""Hostile benchmark baselines: keyword, random, oracle, and base-only."""

from __future__ import annotations

import random
from time import perf_counter

from selectivellm.analyzers import contains_term
from selectivellm.registry import CapacityRegistry
from selectivellm.routing.base import Router, select_candidates
from selectivellm.schemas import PromptProfile, RouteCandidate, RoutingDecision


class KeywordRouter(Router):
    name = "keyword"

    def __init__(self, *, top_k: int = 2, threshold: float = 0.01) -> None:
        self.top_k = top_k
        self.threshold = threshold

    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        del expected_experts
        started = perf_counter()
        prompt = profile.prompt.lower()
        candidates: list[RouteCandidate] = []
        for component in registry.routable_components():
            terms = [*component.domain, *component.supported_tasks]
            hits = [term for term in terms if contains_term(prompt, term)]
            score = min(1.0, len(hits) / max(1, len(terms)))
            candidates.append(RouteCandidate(component_id=component.id, score=score, reasons=hits))
        candidates.sort(key=lambda item: (-item.score, item.component_id))
        selected = select_candidates(candidates, top_k=self.top_k, threshold=self.threshold)
        return RoutingDecision(
            router=self.name,
            router_version=self.version,
            selected=selected,
            candidates=candidates,
            confidence=candidates[0].score if candidates else 0.0,
            latency_ms=(perf_counter() - started) * 1000,
            metadata={"top_k": self.top_k, "threshold": self.threshold},
        )


class RandomRouter(Router):
    name = "random"

    def __init__(self, *, seed: int, top_k: int = 1) -> None:
        self.seed = seed
        self.top_k = top_k

    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        del expected_experts
        started = perf_counter()
        prompt_seed = sum(profile.prompt.encode("utf-8"))
        generator = random.Random(self.seed + prompt_seed)
        components = registry.routable_components()
        generator.shuffle(components)
        candidates = [
            RouteCandidate(component_id=component.id, score=generator.random())
            for component in components
        ]
        candidates.sort(key=lambda item: (-item.score, item.component_id))
        selected = [item.component_id for item in candidates[: self.top_k]]
        return RoutingDecision(
            router=self.name,
            router_version=self.version,
            selected=selected,
            candidates=candidates,
            confidence=candidates[0].score if candidates else 0.0,
            latency_ms=(perf_counter() - started) * 1000,
            metadata={"seed": self.seed, "top_k": self.top_k},
        )


class OracleRouter(Router):
    name = "oracle"

    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        del profile
        started = perf_counter()
        if expected_experts is None:
            raise ValueError("oracle routing requires benchmark expected_experts")
        selected = [registry.get(item).id for item in expected_experts]
        return RoutingDecision(
            router=self.name,
            router_version=self.version,
            selected=selected,
            candidates=[RouteCandidate(component_id=item, score=1.0) for item in selected],
            confidence=1.0,
            latency_ms=(perf_counter() - started) * 1000,
            metadata={"uses_ground_truth": True},
        )


class BaseOnlyRouter(Router):
    name = "base_only"

    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        del profile, registry, expected_experts
        return RoutingDecision(
            router=self.name,
            router_version=self.version,
            selected=[],
            candidates=[],
            confidence=1.0,
            latency_ms=0.0,
            metadata={},
        )


class AllResidentRouter(Router):
    name = "all_resident"

    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        del profile, expected_experts
        started = perf_counter()
        selected = [component.id for component in registry.routable_components()]
        return RoutingDecision(
            router=self.name,
            router_version=self.version,
            selected=selected,
            candidates=[RouteCandidate(component_id=item, score=1.0) for item in selected],
            confidence=1.0,
            latency_ms=(perf_counter() - started) * 1000,
            metadata={"all_capacity": True},
        )
