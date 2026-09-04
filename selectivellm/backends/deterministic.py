"""Offline control backend for methodology and systems-path validation."""

from __future__ import annotations

import hashlib
from time import perf_counter
from typing import Literal

from selectivellm.backends.base import InferenceBackend
from selectivellm.schemas import BackendOutput, CapacityComponent, ComponentType


class DeterministicBackend(InferenceBackend):
    name = "deterministic-control"
    kind: Literal["control"] = "control"
    model_identity = "selectivellm-control-v1"
    device = "cpu"

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed
        self.loaded: set[str] = set()

    def _measured_work(self, label: str, rounds: int) -> str:
        value = f"{self.seed}:{label}".encode()
        for _ in range(rounds):
            value = hashlib.sha256(value).digest()
        return value.hex()[:12]

    def load_component(self, component: CapacityComponent) -> None:
        self._measured_work(component.id, max(250, int(component.memory_mb * 8)))
        self.loaded.add(component.id)

    def unload_component(self, component: CapacityComponent) -> None:
        self.loaded.discard(component.id)

    def generate(self, prompt: str, active_components: list[CapacityComponent]) -> BackendOutput:
        started = perf_counter()
        digest = self._measured_work(prompt, 800)
        experts = [
            component
            for component in active_components
            if component.type is not ComponentType.BASE_MODEL
        ]
        capabilities = sorted({domain for component in experts for domain in component.domain})
        text = (
            "[deterministic-control output] "
            f"capabilities={','.join(capabilities) or 'base-only'}; trace={digest}. "
            "This output validates benchmark methodology, not language-model quality."
        )
        elapsed = (perf_counter() - started) * 1000
        token_count = len(text.split())
        return BackendOutput(
            text=text,
            token_count=token_count,
            first_token_ms=elapsed * 0.25,
            generation_ms=elapsed,
            metadata={
                "quality_semantics": "synthetic capability coverage",
                "physical_vram_claim": False,
            },
        )

    def synchronize(self) -> None:
        return None
