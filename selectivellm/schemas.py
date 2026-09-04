"""Shared typed contracts for routing, runtime, generation, and benchmarks."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

METRIC_SCHEMA_VERSION = "1.0.0"


class ComponentType(StrEnum):
    BASE_MODEL = "base_model"
    EXPERT_MODEL = "expert_model"
    ADAPTER = "adapter"
    LORA = "lora"
    PROMPT_ADAPTER = "prompt_adapter"
    CLASSIFIER = "classifier"
    RERANKER = "reranker"
    TOOL = "tool"
    FUTURE_PARAMETER_SHARD = "future_parameter_shard"


class CapacityComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z][a-z0-9_\-]*$")
    name: str
    type: ComponentType
    domain: list[str] = Field(default_factory=list)
    description: str
    memory_mb: float = Field(gt=0)
    backend: str
    model_path: str | None = None
    supported_tasks: list[str] = Field(default_factory=list)
    embedding: list[float] | None = None
    priority: int = 0
    dependencies: list[str] = Field(default_factory=list)
    parameter_count: int | None = Field(default=None, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class RegistryDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str
    registry_version: str
    components: list[CapacityComponent]


class PromptProfile(BaseModel):
    prompt: str
    domain_scores: dict[str, float]
    task_scores: dict[str, float]
    capabilities: list[str]
    programming_language: str | None = None
    difficulty: Literal["low", "medium", "high"] = "medium"
    confidence: float = Field(ge=0, le=1)
    evidence: dict[str, list[str]] = Field(default_factory=dict)


class RouteCandidate(BaseModel):
    component_id: str
    score: float
    reasons: list[str] = Field(default_factory=list)


class RoutingDecision(BaseModel):
    router: str
    router_version: str
    selected: list[str]
    candidates: list[RouteCandidate]
    confidence: float = Field(ge=0, le=1)
    latency_ms: float = Field(ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PlanDecision(BaseModel):
    selected: list[str]
    rejected: dict[str, str]
    required_memory_mb: float = Field(ge=0)
    budget_mb: float = Field(gt=0)
    latency_ms: float = Field(ge=0)


class RuntimeEvent(BaseModel):
    action: Literal["load", "unload", "hit", "miss", "transfer", "reject"]
    component_id: str
    duration_ms: float = Field(default=0, ge=0)
    from_location: str | None = None
    to_location: str | None = None
    detail: str | None = None


class MemorySnapshot(BaseModel):
    measurement_semantics: str
    declared_resident_capacity_mb: float = Field(ge=0)
    declared_peak_capacity_mb: float = Field(ge=0)
    host_rss_mb: float | None = Field(default=None, ge=0)
    accelerator_allocated_mb: float | None = Field(default=None, ge=0)
    accelerator_reserved_mb: float | None = Field(default=None, ge=0)
    accelerator_peak_allocated_mb: float | None = Field(default=None, ge=0)
    accelerator_measurement_available: bool
    unavailable_reason: str | None = None


class StageMetrics(BaseModel):
    metric_schema_version: str = METRIC_SCHEMA_VERSION
    routing_ms: float = Field(default=0, ge=0)
    planning_ms: float = Field(default=0, ge=0)
    loading_ms: float = Field(default=0, ge=0)
    inference_ms: float = Field(default=0, ge=0)
    orchestration_ms: float = Field(default=0, ge=0)
    first_token_ms: float | None = Field(default=None, ge=0)
    end_to_end_ms: float = Field(default=0, ge=0)
    tokens_per_second: float | None = Field(default=None, ge=0)
    cache_hits: int = Field(default=0, ge=0)
    cache_misses: int = Field(default=0, ge=0)
    expert_swaps: int = Field(default=0, ge=0)
    transfers: int = Field(default=0, ge=0)
    active_parameters: int | None = Field(default=None, ge=0)
    resident_parameters: int | None = Field(default=None, ge=0)


class BackendOutput(BaseModel):
    text: str
    token_count: int = Field(ge=0)
    first_token_ms: float | None = Field(default=None, ge=0)
    generation_ms: float = Field(ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class GenerationResult(BaseModel):
    text: str
    backend: str
    backend_kind: Literal["control", "real"]
    model_identity: str
    profile: PromptProfile
    routing: RoutingDecision
    plan: PlanDecision
    runtime_events: list[RuntimeEvent]
    resident_components: list[str]
    memory: MemorySnapshot
    metrics: StageMetrics


class BenchmarkCase(BaseModel):
    id: str
    prompt: str
    domain: list[str]
    expected_experts: list[str]
    reference: str
    tags: list[str] = Field(default_factory=list)
    evaluation: Literal["control_capability", "exact_match", "token_f1"] = "control_capability"


class BenchmarkDataset(BaseModel):
    schema_version: str
    benchmark_version: str
    name: str
    description: str
    cases: list[BenchmarkCase]


class AggregateStats(BaseModel):
    count: int = Field(ge=0)
    mean: float | None = None
    median: float | None = None
    standard_deviation: float | None = None
    p50: float | None = None
    p95: float | None = None
    confidence_interval_95: tuple[float, float] | None = None


class RunManifest(BaseModel):
    run_id: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    status: Literal["running", "completed", "failed"]
    backend: str
    backend_kind: Literal["control", "real"]
    model_identity: str
    adapter_set: list[str]
    benchmark_version: str
    benchmark_content_hash: str
    registry_version: str
    registry_content_hash: str
    routing_config_version: str
    routing_config_hash: str
    metric_schema_version: str = METRIC_SCHEMA_VERSION
    seed_policy: str
    device_class: str
    measurement_semantics: str
    benchmark_fingerprint: str
    configuration_fingerprint: str
    git_commit: str | None = None
    source_dirty: bool = False
