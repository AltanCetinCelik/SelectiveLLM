from __future__ import annotations

from typing import Any

import pytest

from selectivellm.causal_importance.analysis import analyze_scale_comparison, apply_primary_gate


def _metric(mean: float, low: float = 0.01) -> dict[str, float]:
    return {"mean": mean, "ci95_low": low, "ci95_high": mean + 0.1}


def _primary() -> dict[str, Any]:
    domains = {
        domain: {"same_exceeds_all_controls": True}
        for domain in ("code", "mathematics", "science", "general")
    }
    return {
        "activation": {},
        "gradient": {
            "pooled": {
                "same_damage": _metric(0.2),
                "wrong_damage": _metric(0.05),
                "random_damage": _metric(0.05),
                "global_high_damage": _metric(0.05),
                "global_low_damage": _metric(0.01),
                "same_minus_random": _metric(0.15),
                "same_minus_wrong": _metric(0.15),
                "same_minus_global_high": _metric(0.15),
                "same_minus_global_low": _metric(0.19),
                "gradient_same_minus_activation_same": _metric(0.1),
            },
            "domains": domains,
        },
    }


def _stability() -> dict[str, Any]:
    return {
        "gradient": {"stable_domain_count": 3},
        "activation": {"stable_domain_count": 2},
        "improved_gradient_vs_activation": True,
        "domain_mask_overlap": {"gradient": {"mean_pairwise_jaccard": 0.05}},
    }


def test_primary_gate_classifies_objective_aware_success() -> None:
    result = apply_primary_gate(_primary(), _stability(), {"passed": True})

    assert result["classification"] == "A"
    assert all(result["a_checks"].values())


def test_primary_gate_cannot_read_signed_diagnostics() -> None:
    primary = _primary()
    primary["gradient"]["pooled"]["predicted_taylor_damage"] = _metric(-999)
    primary["gradient"]["pooled"]["normalized_signed_attribution"] = _metric(-999)

    result = apply_primary_gate(primary, _stability(), {"passed": True})

    assert result["classification"] == "A"


def test_shared_core_gate_is_b_when_a_fails() -> None:
    primary = _primary()
    primary["gradient"]["pooled"]["gradient_same_minus_activation_same"] = _metric(0.0, -0.1)
    primary["gradient"]["pooled"]["wrong_damage"] = _metric(0.18)

    result = apply_primary_gate(primary, _stability(), {"passed": True})

    assert result["classification"] == "B"


def test_unstable_result_is_c() -> None:
    stability = _stability()
    stability["gradient"]["stable_domain_count"] = 2

    result = apply_primary_gate(_primary(), stability, {"passed": True})

    assert result["classification"] == "C"


def test_scale_comparison_pairs_cases_without_pooling_models() -> None:
    domains = ("code", "mathematics", "science", "general")
    prior: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    for index in range(32):
        base = {
            "case_id": f"case-{index:02d}",
            "domain": domains[index // 8],
            "block_size": 64,
            "discovery_method": "gradient",
            "same_damage": 0.1,
            "same_minus_random": 0.05,
            "same_minus_wrong": 0.04,
            "same_minus_global_high": 0.03,
            "gradient_same_minus_activation_same": 0.02,
        }
        prior.append(base)
        current.append(
            {
                **base,
                "same_damage": 0.2,
                "same_minus_random": 0.15,
                "same_minus_wrong": 0.14,
                "same_minus_global_high": 0.13,
                "gradient_same_minus_activation_same": 0.12,
            }
        )
    stability = {
        "64": {
            "gradient": {"stable_domain_count": 3},
            "activation": {"stable_domain_count": 1},
        }
    }

    result = analyze_scale_comparison(
        current,
        prior,
        stability,
        stability,
        current_model="3B",
        prior_model="1.5B",
        current_classification="A",
        prior_classification="C",
    )

    assert result["models_pooled"] is False
    assert result["classification_transition"] == "C->A"
    assert result["scale_rescue"] is True
    assert result["metrics"]["same_damage"]["mean"] == pytest.approx(0.1)
