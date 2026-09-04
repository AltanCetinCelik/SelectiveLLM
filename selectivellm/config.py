"""Versioned application configuration loading."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


class AnalyzerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = "deterministic_embedding"
    dimension: int = Field(default=256, ge=32)


class RouterConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str = "1.0.0"
    type: str = "hybrid"
    top_k: int = Field(default=3, ge=1)
    threshold: float = Field(default=0.18, ge=0, le=1)
    static_components: list[str] = Field(default_factory=list)
    keyword_weight: float = Field(default=0.35, ge=0, le=1)
    embedding_weight: float = Field(default=0.65, ge=0, le=1)


class RuntimeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    memory_budget_mb: float = Field(default=900, gt=0)
    cache_policy: str = "lru"
    cache_enabled: bool = True


class BackendConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str = "deterministic"
    model_path: str | None = None
    tokenizer_path: str | None = None
    trust_remote_code: bool = False
    max_new_tokens: int = Field(default=128, ge=1)
    device: str = "auto"
    device_map: str | None = "auto"
    max_memory: dict[str, str] | None = None


class SelectiveLLMConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0.0"
    mode: str = "semantic_routing"
    seed: int = 42
    registry_path: str | None = None
    benchmark_path: str | None = None
    analyzer: AnalyzerConfig = Field(default_factory=AnalyzerConfig)
    router: RouterConfig = Field(default_factory=RouterConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    backend: BackendConfig = Field(default_factory=BackendConfig)

    @classmethod
    def from_yaml(cls, path: str | Path) -> SelectiveLLMConfig:
        config_path = Path(path).expanduser().resolve()
        with config_path.open(encoding="utf-8") as handle:
            raw: dict[str, Any] = yaml.safe_load(handle) or {}
        config = cls.model_validate(raw)
        for field in ("registry_path", "benchmark_path"):
            value = getattr(config, field)
            if value and not Path(value).is_absolute():
                setattr(config, field, str((config_path.parent / value).resolve()))
        return config
