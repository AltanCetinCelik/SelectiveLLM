"""Memory-aware LRU bookkeeping independent of backend implementation."""

from __future__ import annotations

from collections import OrderedDict


class LRUCapacityCache:
    def __init__(self) -> None:
        self._entries: OrderedDict[str, None] = OrderedDict()

    def __contains__(self, component_id: str) -> bool:
        return component_id in self._entries

    def touch(self, component_id: str) -> None:
        if component_id in self._entries:
            self._entries.move_to_end(component_id)
        else:
            self._entries[component_id] = None

    def remove(self, component_id: str) -> None:
        self._entries.pop(component_id, None)

    def eviction_candidate(self, protected: set[str]) -> str | None:
        return next((item for item in self._entries if item not in protected), None)

    def entries(self) -> list[str]:
        return list(self._entries)
