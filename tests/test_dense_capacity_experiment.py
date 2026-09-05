from __future__ import annotations

import numpy as np
import pytest

from selectivellm.dense_capacity.analysis import apply_decision_gate, bootstrap_interval
from selectivellm.dense_capacity.discovery import (
    DOMAINS,
    build_retention_masks,
    percentile_ranks,
    selected_indices,
)
from selectivellm.dense_capacity.interventions import LogicalMask, validate_mask_structure


def test_percentile_ranks_are_normalized_within_last_dimension() -> None:
    values = np.asarray([[[4.0, 1.0, 3.0, 2.0]]], dtype=np.float32)

    observed = percentile_ranks(values)

    np.testing.assert_allclose(observed, [[[1.0, 0.0, 2 / 3, 1 / 3]]])


def test_structural_masks_reject_unequal_per_layer_counts() -> None:
    mask = LogicalMask(
        name="bad_mlp",
        granularity="mlp",
        mask_semantics="ABLATE_SELECTED",
        source="test",
        source_domain=None,
        selected_by_layer={0: [1]},
        fraction=0.05,
    )

    with pytest.raises(ValueError, match="per-layer quotas"):
        validate_mask_structure(mask)


def test_layer_mask_uses_identity_markers() -> None:
    valid = LogicalMask(
        "layers",
        "layer",
        "ABLATE_SELECTED",
        "test",
        None,
        {0: [0], 7: [0]},
        2 / 28,
    )
    invalid = LogicalMask(
        "layers_bad",
        "layer",
        "ABLATE_SELECTED",
        "test",
        None,
        {0: [1]},
        1 / 28,
    )

    validate_mask_structure(valid)
    with pytest.raises(ValueError, match="identity marker"):
        validate_mask_structure(invalid)


def test_retention_masks_have_fixed_counts_and_semantics() -> None:
    rankings = {
        **{
            f"head_{domain}_selectivity": np.tile(np.arange(12, dtype=np.float32), (28, 1))
            for domain in DOMAINS
        },
        "head_global_importance": np.tile(np.arange(12, dtype=np.float32), (28, 1)),
    }

    masks = build_retention_masks(rankings, "head")

    assert len(masks) == 40
    assert {mask.fraction for mask in masks} == {1.0, 0.75, 0.5, 0.25}
    assert all(mask.mask_semantics == "RETAIN_SELECTED" for mask in masks)
    for mask in masks:
        validate_mask_structure(mask)
        assert {len(items) for items in mask.selected_by_layer.values()} == {
            int(12 * mask.fraction)
        }


def test_selected_layers_are_top_scoring_and_equal_size() -> None:
    scores = np.arange(28, dtype=np.float32)

    selected = selected_indices(scores, "layer", 7)

    assert list(selected) == [27, 26, 25, 24, 23, 22, 21]
    assert all(marker == [0] for marker in selected.values())


def test_bootstrap_resamples_cases_and_reports_frozen_metadata() -> None:
    values = [float(index) for index in range(8)]
    result = bootstrap_interval(values, ["code"] * 8, repetitions=100, seed=42)

    assert result["n"] == 8
    assert result["mean"] == pytest.approx(3.5)
    assert result["experimental_unit"] == "held_out_question"
    assert result["pooled_resampling"] == "within_domain"
    assert result["bootstrap_repetitions"] == 100


def test_decision_gate_uses_fixed_priority_not_largest_effect() -> None:
    def metric(mean: float, low: float = 0.01) -> dict[str, float]:
        return {"mean": mean, "ci95_low": low, "ci95_high": mean + 0.1}

    domain = {
        "same_exceeds_all_controls": True,
    }
    granularities = {
        "mlp": {
            "granularity_stable": True,
            "pooled": {
                "same_damage": metric(0.11),
                "wrong_damage": metric(0.02),
                "same_minus_random": metric(0.06),
                "same_minus_wrong": metric(0.06),
            },
            "domains": {name: dict(domain) for name in DOMAINS},
        },
        "head": {
            "granularity_stable": True,
            "pooled": {
                "same_damage": metric(0.50),
                "wrong_damage": metric(0.02),
                "same_minus_random": metric(0.40),
                "same_minus_wrong": metric(0.40),
            },
            "domains": {name: dict(domain) for name in DOMAINS},
        },
        "layer": {
            "granularity_stable": False,
            "pooled": {
                "same_damage": metric(0.01),
                "wrong_damage": metric(0.01),
                "same_minus_random": metric(0.01),
                "same_minus_wrong": metric(0.0),
            },
            "domains": {name: {"same_exceeds_all_controls": False} for name in DOMAINS},
        },
    }
    stability = {"mask_overlap": {name: {"mean_pairwise_jaccard": 0.0} for name in granularities}}

    decision = apply_decision_gate(granularities, stability, {"passed": True})

    assert decision["classification"] == "A"
    assert decision["trigger_granularity"] == "mlp"
    assert decision["all_qualifying_granularities"] == ["mlp", "head"]
