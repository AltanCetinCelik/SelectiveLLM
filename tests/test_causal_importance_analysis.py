from __future__ import annotations

from typing import Any

from selectivellm.causal_importance.analysis import apply_primary_gate


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
