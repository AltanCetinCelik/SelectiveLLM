"""End-to-end SelectiveLLM orchestration engine."""

from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path
from time import perf_counter

from selectivellm.analyzers import DeterministicEmbeddingAnalyzer
from selectivellm.backends.base import InferenceBackend
from selectivellm.backends.deterministic import DeterministicBackend
from selectivellm.config import SelectiveLLMConfig
from selectivellm.registry import CapacityRegistry
from selectivellm.routing import Router, create_router
from selectivellm.routing.baselines import BaseOnlyRouter
from selectivellm.runtime.loader import RuntimeLoader
from selectivellm.schemas import GenerationResult, StageMetrics
from selectivellm.selection import BudgetPlanner


def _resource_path(name: str) -> Path:
    resource = files("selectivellm.resources").joinpath(name)
    with as_file(resource) as path:
        return Path(path)


class SelectiveLLM:
    def __init__(
        self,
        config: SelectiveLLMConfig,
        registry: CapacityRegistry,
        analyzer: DeterministicEmbeddingAnalyzer,
        router: Router,
        backend: InferenceBackend,
    ) -> None:
        self.config = config
        self.registry = registry
        self.analyzer = analyzer
        self.router = router
        self.backend = backend
        self.planner = BudgetPlanner(config.runtime.memory_budget_mb)
        self.runtime = RuntimeLoader(
            registry,
            backend,
            budget_mb=config.runtime.memory_budget_mb,
            cache_enabled=config.runtime.cache_enabled,
        )

    @classmethod
    def from_config(
        cls,
        path: str | Path | None = None,
        *,
        config: SelectiveLLMConfig | None = None,
        router: Router | None = None,
    ) -> SelectiveLLM:
        if config is None:
            config = (
                SelectiveLLMConfig.from_yaml(path)
                if path is not None
                else SelectiveLLMConfig.from_yaml(_resource_path("default.yaml"))
            )
        registry_path = (
            Path(config.registry_path) if config.registry_path else _resource_path("registry.yaml")
        )
        registry = CapacityRegistry.from_yaml(registry_path)
        analyzer = DeterministicEmbeddingAnalyzer(config.analyzer.dimension)
        if router is not None:
            active_router = router
        elif config.mode in {"full_model", "offload"}:
            active_router = BaseOnlyRouter()
        elif config.mode == "semantic_routing":
            active_router = create_router(
                config.router, seed=config.seed, dimension=config.analyzer.dimension
            )
        else:
            raise ValueError(f"unsupported experiment mode: {config.mode}")
        if config.backend.type == "deterministic":
            backend: InferenceBackend = DeterministicBackend(seed=config.seed)
        elif config.backend.type in {"transformers", "transformers_peft"}:
            from selectivellm.backends.transformers import TransformersPeftBackend

            backend = TransformersPeftBackend(config.backend)
        else:
            raise ValueError(f"unsupported backend: {config.backend.type}")
        return cls(config, registry, analyzer, active_router, backend)

    def generate(
        self,
        prompt: str,
        *,
        expected_experts: list[str] | None = None,
        allow_over_budget: bool = False,
    ) -> GenerationResult:
        total_started = perf_counter()
        profile = self.analyzer.analyze(prompt)
        routing = self.router.route(profile, self.registry, expected_experts=expected_experts)
        plan = self.planner.plan(routing, self.registry, allow_over_budget=allow_over_budget)
        load_started = perf_counter()
        events = self.runtime.prepare(plan.selected, allow_over_budget=allow_over_budget)
        loading_ms = (perf_counter() - load_started) * 1000
        active = [self.registry.get(item) for item in plan.selected]
        output = self.backend.generate(prompt, active)
        memory = self.runtime.memory_snapshot()
        resident_at_generation = list(self.runtime.resident)
        events.extend(self.runtime.release_after_request(plan.selected))
        end_to_end = (perf_counter() - total_started) * 1000
        base_ids = {component.id for component in self.registry.base_components()}
        cache_hits = sum(
            event.action == "hit" and event.component_id not in base_ids for event in events
        )
        cache_misses = sum(
            event.action == "miss" and event.component_id not in base_ids for event in events
        )
        swaps = sum(event.action == "unload" for event in events)
        transfers = sum(event.action == "transfer" for event in events)
        known_parameters = [component.parameter_count for component in active]
        active_parameters = (
            sum(value for value in known_parameters if value is not None)
            if all(value is not None for value in known_parameters)
            else None
        )
        resident_parameter_values = [
            component.parameter_count for component in self.runtime.resident.values()
        ]
        resident_parameters = (
            sum(value for value in resident_parameter_values if value is not None)
            if all(value is not None for value in resident_parameter_values)
            else None
        )
        metrics = StageMetrics(
            routing_ms=routing.latency_ms,
            planning_ms=plan.latency_ms,
            loading_ms=loading_ms,
            inference_ms=output.generation_ms,
            orchestration_ms=max(
                0.0,
                end_to_end
                - routing.latency_ms
                - plan.latency_ms
                - loading_ms
                - output.generation_ms,
            ),
            first_token_ms=output.first_token_ms,
            end_to_end_ms=end_to_end,
            tokens_per_second=(
                output.token_count / (output.generation_ms / 1000)
                if output.generation_ms > 0
                else None
            ),
            cache_hits=cache_hits,
            cache_misses=cache_misses,
            expert_swaps=swaps,
            transfers=transfers,
            active_parameters=active_parameters,
            resident_parameters=resident_parameters,
        )
        return GenerationResult(
            text=output.text,
            backend=self.backend.name,
            backend_kind=self.backend.kind,
            model_identity=self.backend.model_identity,
            profile=profile,
            routing=routing,
            plan=plan,
            runtime_events=events,
            resident_components=resident_at_generation,
            memory=memory,
            metrics=metrics,
        )
