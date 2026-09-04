from __future__ import annotations

import pytest

from selectivellm.config import SelectiveLLMConfig
from selectivellm.engine import SelectiveLLM


@pytest.mark.parametrize("mode", ["full_model", "offload"])
def test_dense_baseline_modes_do_not_route_experts(
    mode: str, control_config: SelectiveLLMConfig
) -> None:
    control_config.mode = mode
    result = SelectiveLLM.from_config(config=control_config).generate("Implement Python")
    assert result.routing.router == "base_only"
    assert result.plan.selected == ["base"]


def test_unknown_mode_fails_early(control_config: SelectiveLLMConfig) -> None:
    control_config.mode = "unknown"
    with pytest.raises(ValueError, match="unsupported experiment mode"):
        SelectiveLLM.from_config(config=control_config)
