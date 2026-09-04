"""Embedding-based routing over component descriptions."""

from __future__ import annotations

from time import perf_counter

from selectivellm.analyzers import cosine_similarity, stable_embedding
from selectivellm.registry import CapacityRegistry
from selectivellm.routing.base import Router, select_candidates
from selectivellm.schemas import PromptProfile, RouteCandidate, RoutingDecision


class EmbeddingRouter(Router):
    name = "embedding"

    def __init__(self, *, dimension: int = 256, top_k: int = 2, threshold: float = 0.12) -> None:
        self.dimension = dimension
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
        prompt_embedding = stable_embedding(profile.prompt, self.dimension)
        candidates: list[RouteCandidate] = []
        for component in registry.routable_components():
            component_text = " ".join(
                [
                    component.name,
                    component.description,
                    *component.domain,
                    *component.supported_tasks,
                ]
            )
            component_embedding = component.embedding or stable_embedding(
                component_text, self.dimension
            )
            score = max(0.0, cosine_similarity(prompt_embedding, component_embedding))
            domain_overlap = sum(
                profile.domain_scores.get(domain, 0.0) for domain in component.domain
            )
            score = min(1.0, 0.65 * score + 0.35 * min(1.0, domain_overlap))
            candidates.append(
                RouteCandidate(
                    component_id=component.id,
                    score=score,
                    reasons=["feature-hash cosine similarity", "analyzer domain overlap"],
                )
            )
        candidates.sort(key=lambda item: (-item.score, item.component_id))
        selected = select_candidates(candidates, top_k=self.top_k, threshold=self.threshold)
        confidence = candidates[0].score if candidates else 0.0
        return RoutingDecision(
            router=self.name,
            router_version=self.version,
            selected=selected,
            candidates=candidates,
            confidence=confidence,
            latency_ms=(perf_counter() - started) * 1000,
            metadata={
                "embedding": "deterministic-feature-hash",
                "dimension": self.dimension,
                "top_k": self.top_k,
                "threshold": self.threshold,
            },
        )
