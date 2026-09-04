from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path

import pytest

from selectivellm.config import SelectiveLLMConfig
from selectivellm.registry import CapacityRegistry


@pytest.fixture
def registry_path() -> Path:
    resource = files("selectivellm.resources").joinpath("registry.yaml")
    with as_file(resource) as path:
        yield Path(path)


@pytest.fixture
def registry(registry_path: Path) -> CapacityRegistry:
    return CapacityRegistry.from_yaml(registry_path)


@pytest.fixture
def control_config(registry_path: Path) -> SelectiveLLMConfig:
    config = SelectiveLLMConfig()
    config.registry_path = str(registry_path)
    return config
