"""Hybrid router combining embedding and transparent lexical/domain signals."""

from __future__ import annotations

from time import perf_counter

from selectivellm.registry import CapacityRegistry
from selectivellm.routing.base import Router, select_candidates
from selectivellm.routing.baselines import KeywordRouter
from selectivellm.routing.embedding import EmbeddingRouter
from selectivellm.schemas import PromptProfile, RouteCandidate, RoutingDecision


class HybridRouter(Router):
    name = "hybrid"

    def __init__(
        self,
        *,
        dimension: int = 256,
        top_k: int = 2,
        threshold: float = 0.18,
        embedding_weight: float = 0.65,
        keyword_weight: float = 0.35,
    ) -> None:
        self.top_k = top_k
        self.threshold = threshold
        self.embedding_weight = embedding_weight
        self.keyword_weight = keyword_weight
        self.embedding = EmbeddingRouter(dimension=dimension, top_k=top_k, threshold=0)
        self.keyword = KeywordRouter(top_k=top_k, threshold=0)

    def route(
        self,
        profile: PromptProfile,
        registry: CapacityRegistry,
        *,
        expected_experts: list[str] | None = None,
    ) -> RoutingDecision:
        del expected_experts
        started = perf_counter()
        semantic = self.embedding.route(profile, registry)
        lexical = self.keyword.route(profile, registry)
        semantic_scores = {item.component_id: item.score for item in semantic.candidates}
        lexical_scores = {item.component_id: item.score for item in lexical.candidates}
        candidates: list[RouteCandidate] = []
        for component in registry.routable_components():
            domain_score = max(
                (profile.domain_scores.get(domain, 0.0) for domain in component.domain),
                default=0.0,
            )
            score = min(
                1.0,
                self.embedding_weight * semantic_scores.get(component.id, 0.0)
                + self.keyword_weight * lexical_scores.get(component.id, 0.0)
                + 0.2 * domain_score,
            )
            candidates.append(
                RouteCandidate(
                    component_id=component.id,
                    score=score,
                    reasons=[
                        f"embedding={semantic_scores.get(component.id, 0.0):.3f}",
                        f"keyword={lexical_scores.get(component.id, 0.0):.3f}",
                        f"domain={domain_score:.3f}",
                    ],
                )
            )
        candidates.sort(key=lambda item: (-item.score, item.component_id))
        selected = select_candidates(candidates, top_k=self.top_k, threshold=self.threshold)
        return RoutingDecision(
            router=self.name,
            router_version=self.version,
            selected=selected,
            candidates=candidates,
            confidence=candidates[0].score if candidates else 0.0,
            latency_ms=(perf_counter() - started) * 1000,
            metadata={
                "top_k": self.top_k,
                "threshold": self.threshold,
                "embedding_weight": self.embedding_weight,
                "keyword_weight": self.keyword_weight,
            },
        )
