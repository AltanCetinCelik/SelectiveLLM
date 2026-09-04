"""Dependency-aware component loading under a declared memory budget."""

from __future__ import annotations

from time import perf_counter

from selectivellm.backends.base import InferenceBackend
from selectivellm.registry import CapacityRegistry
from selectivellm.runtime.cache import LRUCapacityCache
from selectivellm.runtime.memory import MemoryMeter
from selectivellm.schemas import CapacityComponent, MemorySnapshot, RuntimeEvent


class RuntimeLoader:
    def __init__(
        self,
        registry: CapacityRegistry,
        backend: InferenceBackend,
        *,
        budget_mb: float,
        cache_enabled: bool,
    ) -> None:
        self.registry = registry
        self.backend = backend
        self.budget_mb = budget_mb
        self.cache_enabled = cache_enabled
        self.cache = LRUCapacityCache()
        self.resident: dict[str, CapacityComponent] = {}
        self.meter = MemoryMeter(backend.device)

    @property
    def resident_memory_mb(self) -> float:
        return sum(component.memory_mb for component in self.resident.values())

    def prepare(
        self, component_ids: list[str], *, allow_over_budget: bool = False
    ) -> list[RuntimeEvent]:
        requested = self.registry.resolve_dependencies(component_ids)
        protected = set(requested)
        events: list[RuntimeEvent] = []
        for component_id in requested:
            component = self.registry.get(component_id)
            if component_id in self.resident:
                self.cache.touch(component_id)
                events.append(RuntimeEvent(action="hit", component_id=component_id))
                continue
            events.append(RuntimeEvent(action="miss", component_id=component_id))
            while (
                not allow_over_budget
                and self.resident_memory_mb + component.memory_mb > self.budget_mb
            ):
                candidate = self.cache.eviction_candidate(protected)
                if candidate is None:
                    raise MemoryError(
                        f"cannot load {component_id}: {component.memory_mb:.1f} MB component with "
                        f"{self.resident_memory_mb:.1f} MB resident exceeds {self.budget_mb:.1f} MB budget"
                    )
                events.extend(self._unload(candidate, detail="LRU eviction"))
            started = perf_counter()
            self.backend.load_component(component)
            self.backend.synchronize()
            duration = (perf_counter() - started) * 1000
            self.resident[component_id] = component
            self.cache.touch(component_id)
            self.meter.snapshot(self.resident_memory_mb)
            events.append(
                RuntimeEvent(
                    action="load",
                    component_id=component_id,
                    duration_ms=duration,
                    from_location="disk_or_host",
                    to_location=self.backend.device,
                )
            )
        return events

    def release_after_request(self, active_ids: list[str]) -> list[RuntimeEvent]:
        if self.cache_enabled:
            return []
        base_ids = {component.id for component in self.registry.base_components()}
        events: list[RuntimeEvent] = []
        for component_id in reversed(active_ids):
            if component_id not in base_ids and component_id in self.resident:
                events.extend(self._unload(component_id, detail="cache disabled"))
        return events

    def clear(self) -> list[RuntimeEvent]:
        events: list[RuntimeEvent] = []
        for component_id in reversed(list(self.resident)):
            events.extend(self._unload(component_id, detail="runtime clear"))
        return events

    def memory_snapshot(self) -> MemorySnapshot:
        snapshot = self.meter.snapshot(self.resident_memory_mb)
        base_ids = {component.id for component in self.registry.base_components()}
        base_capacity = sum(
            component.memory_mb
            for component_id, component in self.resident.items()
            if component_id in base_ids
        )
        return snapshot.model_copy(
            update={
                "declared_base_capacity_mb": base_capacity,
                "declared_expert_capacity_mb": self.resident_memory_mb - base_capacity,
                "breakdown_unavailable_reason": (
                    "Backend does not yet expose tensor-level model, adapter, KV-cache, "
                    "and framework allocation attribution"
                ),
            }
        )

    def _unload(self, component_id: str, detail: str) -> list[RuntimeEvent]:
        component = self.resident.pop(component_id)
        started = perf_counter()
        self.backend.unload_component(component)
        self.backend.synchronize()
        duration = (perf_counter() - started) * 1000
        self.cache.remove(component_id)
        return [
            RuntimeEvent(
                action="unload",
                component_id=component_id,
                duration_ms=duration,
                from_location=self.backend.device,
                to_location="host_or_disk",
                detail=detail,
            )
        ]
