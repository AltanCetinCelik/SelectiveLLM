from __future__ import annotations

import numpy as np

from selectivellm.causal_importance.discovery import (
    DOMAINS,
    build_masks,
    domain_selectivity,
    select_blocks,
    split_assignments,
)
from selectivellm.causal_importance.mappings import build_mapping


def test_select_blocks_respects_variable_128_quota_and_low_index_ties() -> None:
    mapping = build_mapping(128)
    scores = np.zeros((28, 70), dtype=np.float32)

    selected = select_blocks(scores, mapping)

    assert selected[0] == [0, 1, 2, 3]
    assert selected[1] == [0, 1, 2]
    assert tuple(len(selected[layer]) for layer in range(28)) == mapping.per_layer_quota


def test_domain_selectivity_keeps_signed_contrast() -> None:
    domains = [domain for domain in DOMAINS for _ in range(12)]
    values = np.zeros((48, 28, 140), dtype=np.float32)
    values[:12, :, 0] = 1.0
    values[:12, :, 1] = -1.0

    scores = domain_selectivity(values, domains, "code")

    assert np.all(scores[:, 0] > 0)
    assert np.all(scores[:, 1] < 0)


def test_split_assignments_are_shared_deterministic_and_stratified() -> None:
    domains = [domain for domain in DOMAINS for _ in range(12)]

    first = split_assignments(domains)
    second = split_assignments(domains)

    assert first == second
    assert len(first) == 20
    for repetition in first:
        for domain in DOMAINS:
            left, right = repetition[domain]
            assert len(left) == len(right) == 6
            assert set(left).isdisjoint(right)


def test_build_masks_produces_exact_frozen_matrix() -> None:
    mapping = build_mapping(64)
    scores = np.tile(np.arange(140, dtype=np.float32), (28, 1))
    rankings = {
        **{
            f"{method}_{domain}_selectivity": scores
            for method in ("activation", "gradient")
            for domain in DOMAINS
        },
        "activation_global_importance": scores,
        "gradient_global_importance": scores,
    }

    masks = build_masks(rankings, mapping)

    assert len(masks) == 18
    assert sum(mask.source == "domain_selectivity" for mask in masks) == 8
    assert sum(mask.source == "random" for mask in masks) == 5
    assert sum(mask.source == "noop" for mask in masks) == 1
    assert all(mask.selected_channel_count == 12_544 for mask in masks if mask.source != "noop")
