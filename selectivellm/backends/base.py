"""Backend lifecycle contract shared by control and real inference."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

from selectivellm.schemas import BackendOutput, CapacityComponent


class InferenceBackend(ABC):
    name: str
    kind: Literal["control", "real"]
    model_identity: str
    device: str

    @abstractmethod
    def load_component(self, component: CapacityComponent) -> None:
        """Make a registry component available for generation."""

    @abstractmethod
    def unload_component(self, component: CapacityComponent) -> None:
        """Release a component when supported."""

    @abstractmethod
    def generate(self, prompt: str, active_components: list[CapacityComponent]) -> BackendOutput:
        """Generate using the currently active component set."""

    def synchronize(self) -> None:
        """Wait for asynchronous accelerator work before timing boundaries."""
        return None
