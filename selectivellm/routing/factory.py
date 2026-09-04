"""Router construction from versioned configuration."""

from __future__ import annotations

from selectivellm.config import RouterConfig
from selectivellm.routing.base import Router
from selectivellm.routing.baselines import (
    AllResidentRouter,
    BaseOnlyRouter,
    KeywordRouter,
    OracleRouter,
    RandomRouter,
)
from selectivellm.routing.embedding import EmbeddingRouter
from selectivellm.routing.hybrid import HybridRouter
from selectivellm.routing.static import StaticRouter
from selectivellm.routing.topk import ThresholdRouter, TopKRouter


def create_router(config: RouterConfig, *, seed: int, dimension: int = 256) -> Router:
    router_type = config.type.lower()
    if router_type == "static":
        return StaticRouter(config.static_components)
    if router_type == "embedding":
        return EmbeddingRouter(dimension=dimension, top_k=config.top_k, threshold=config.threshold)
    if router_type == "keyword":
        return KeywordRouter(top_k=config.top_k, threshold=config.threshold)
    if router_type == "random":
        return RandomRouter(seed=seed, top_k=config.top_k)
    if router_type == "oracle":
        return OracleRouter()
    if router_type == "base_only":
        return BaseOnlyRouter()
    if router_type == "all_resident":
        return AllResidentRouter()
    if router_type == "hybrid":
        return HybridRouter(
            dimension=dimension,
            top_k=config.top_k,
            threshold=config.threshold,
            embedding_weight=config.embedding_weight,
            keyword_weight=config.keyword_weight,
        )
    if router_type == "topk":
        return TopKRouter(EmbeddingRouter(dimension=dimension, threshold=0), config.top_k)
    if router_type == "threshold":
        return ThresholdRouter(
            EmbeddingRouter(dimension=dimension, threshold=0),
            threshold=config.threshold,
            top_k=config.top_k,
        )
    raise ValueError(f"unsupported router type: {config.type}")
