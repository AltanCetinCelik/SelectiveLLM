"""Adapter residency and lifecycle telemetry for real-model validation."""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable, Iterable
from datetime import UTC, datetime
from time import perf_counter
from typing import Any, Protocol

import psutil

from selectivellm.schemas import CapacityComponent, RuntimeEvent


class AdapterBackend(Protocol):
    loaded_adapters: set[str]
    active_adapters: list[str]

    def load_component(self, component: CapacityComponent) -> None: ...

    def unload_component(self, component: CapacityComponent) -> None: ...

    def synchronize(self) -> None: ...

    def memory_metrics(self) -> dict[str, float | None]: ...


def memory_checkpoint(
    label: str,
    backend: AdapterBackend | None,
    *,
    policy: str | None = None,
    case_id: str | None = None,
    phase: str | None = None,
) -> dict[str, Any]:
    metrics = (
        backend.memory_metrics()
        if backend is not None
        else {
            "mps_current_allocated_mb": None,
            "mps_driver_allocated_mb": None,
            "mps_recommended_max_mb": None,
        }
    )
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "label": label,
        "policy": policy,
        "case_id": case_id,
        "phase": phase,
        "host_rss_mb": psutil.Process().memory_info().rss / (1024 * 1024),
        **metrics,
        "resident_adapters": sorted(backend.loaded_adapters) if backend else [],
        "active_adapters": list(backend.active_adapters) if backend else [],
    }


class AdapterResidencyManager:
    """LRU residency manager where cache capacity and active adapters are distinct."""

    def __init__(
        self,
        backend: AdapterBackend,
        components: dict[str, CapacityComponent],
        *,
        cache_size: int,
        checkpoint: Callable[[str], None] | None = None,
    ) -> None:
        if cache_size < 0:
            raise ValueError("cache_size must be non-negative")
        self.backend = backend
        self.components = components
        self.cache_size = cache_size
        self.lru: OrderedDict[str, None] = OrderedDict()
        self.checkpoint = checkpoint

    @property
    def resident(self) -> list[str]:
        return list(self.lru)

    def ensure(self, requested: Iterable[str], *, retain_all: bool = False) -> list[RuntimeEvent]:
        requested_ids = list(dict.fromkeys(requested))
        events: list[RuntimeEvent] = []
        protected = set(requested_ids)
        transient_limit = max(self.cache_size, len(requested_ids))
        for component_id in requested_ids:
            if component_id in self.lru:
                self.lru.move_to_end(component_id)
                events.append(RuntimeEvent(action="hit", component_id=component_id))
                continue
            events.append(RuntimeEvent(action="miss", component_id=component_id))
            while not retain_all and len(self.lru) >= transient_limit:
                candidate = next((item for item in self.lru if item not in protected), None)
                if candidate is None:
                    break
                events.extend(self._unload(candidate, "LRU capacity eviction"))
            started = perf_counter()
            self.backend.load_component(self.components[component_id])
            self.backend.synchronize()
            duration = (perf_counter() - started) * 1000
            self.lru[component_id] = None
            events.append(
                RuntimeEvent(
                    action="load",
                    component_id=component_id,
                    duration_ms=duration,
                    from_location="huggingface_cache",
                    to_location="mps",
                )
            )
            if self.checkpoint:
                self.checkpoint(f"adapter_loaded:{component_id}")
        return events

    def release(self, active: Iterable[str], *, retain_all: bool = False) -> list[RuntimeEvent]:
        for component_id in active:
            if component_id in self.lru:
                self.lru.move_to_end(component_id)
        if retain_all:
            return []
        events: list[RuntimeEvent] = []
        while len(self.lru) > self.cache_size:
            events.extend(self._unload(next(iter(self.lru)), "post-request cache trim"))
        return events

    def clear(self) -> list[RuntimeEvent]:
        events: list[RuntimeEvent] = []
        for component_id in list(self.lru):
            events.extend(self._unload(component_id, "explicit policy reset"))
        return events

    def _unload(self, component_id: str, detail: str) -> list[RuntimeEvent]:
        started = perf_counter()
        self.backend.unload_component(self.components[component_id])
        self.backend.synchronize()
        duration = (perf_counter() - started) * 1000
        self.lru.pop(component_id, None)
        if self.checkpoint:
            self.checkpoint(f"adapter_evicted:{component_id}")
        return [
            RuntimeEvent(
                action="unload",
                component_id=component_id,
                duration_ms=duration,
                from_location="mps",
                to_location="released_or_allocator_cache",
                detail=detail,
            )
        ]
