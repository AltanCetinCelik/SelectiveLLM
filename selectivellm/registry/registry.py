"""Versioned YAML registry loading and dependency validation."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

from selectivellm.schemas import CapacityComponent, ComponentType, RegistryDocument


class RegistryError(ValueError):
    """Raised when a capacity registry is invalid."""


class CapacityRegistry:
    def __init__(self, document: RegistryDocument) -> None:
        self.document = document
        self._components = {component.id: component for component in document.components}
        if len(self._components) != len(document.components):
            raise RegistryError("component ids must be unique")
        self._validate_dependencies()

    @classmethod
    def from_yaml(cls, path: str | Path) -> CapacityRegistry:
        registry_path = Path(path).expanduser().resolve()
        with registry_path.open(encoding="utf-8") as handle:
            raw: dict[str, Any] = yaml.safe_load(handle) or {}
        return cls(RegistryDocument.model_validate(raw))

    @property
    def version(self) -> str:
        return self.document.registry_version

    def all(self) -> list[CapacityComponent]:
        return list(self.document.components)

    def get(self, component_id: str) -> CapacityComponent:
        try:
            return self._components[component_id]
        except KeyError as exc:
            raise RegistryError(f"unknown component: {component_id}") from exc

    def base_components(self) -> list[CapacityComponent]:
        return [c for c in self.all() if c.type is ComponentType.BASE_MODEL]

    def routable_components(self) -> list[CapacityComponent]:
        return [
            c
            for c in self.all()
            if c.type
            in {
                ComponentType.EXPERT_MODEL,
                ComponentType.ADAPTER,
                ComponentType.LORA,
                ComponentType.PROMPT_ADAPTER,
            }
        ]

    def total_memory_mb(self, component_ids: Iterable[str] | None = None) -> float:
        components = self.all() if component_ids is None else [self.get(i) for i in component_ids]
        return sum(component.memory_mb for component in components)

    def resolve_dependencies(self, component_ids: Iterable[str]) -> list[str]:
        resolved: list[str] = []
        visiting: set[str] = set()

        def visit(component_id: str) -> None:
            if component_id in resolved:
                return
            if component_id in visiting:
                raise RegistryError(f"dependency cycle includes {component_id}")
            visiting.add(component_id)
            component = self.get(component_id)
            for dependency in component.dependencies:
                visit(dependency)
            visiting.remove(component_id)
            resolved.append(component_id)

        for component_id in component_ids:
            visit(component_id)
        return resolved

    def _validate_dependencies(self) -> None:
        for component in self.all():
            for dependency in component.dependencies:
                if dependency not in self._components:
                    raise RegistryError(
                        f"component {component.id} depends on unknown component {dependency}"
                    )
        self.resolve_dependencies(self._components)
