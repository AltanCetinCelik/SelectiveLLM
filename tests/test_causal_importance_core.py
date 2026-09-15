from __future__ import annotations

import numpy as np
import pytest

from selectivellm.causal_importance.gradient import aggregate_blocks, percentile_rank_blocks
from selectivellm.causal_importance.mappings import build_mapping
from selectivellm.causal_importance.masks import BlockMask, expanded_channels, validate_block_mask


def test_shared_channel_values_aggregate_into_both_block_sizes() -> None:
    channels = np.tile(np.arange(8960, dtype=np.float32), (2, 28, 1))

    blocks64 = aggregate_blocks(channels, 64)
    blocks128 = aggregate_blocks(channels, 128)

    assert blocks64.shape == (2, 28, 140)
    assert blocks128.shape == (2, 28, 70)
    np.testing.assert_allclose(blocks128, blocks64.reshape(2, 28, 70, 2).sum(axis=-1))


def test_percentile_rank_uses_zero_origin_denominator_and_stable_ties() -> None:
    values = np.zeros((1, 28, 70), dtype=np.float32)
    values[:, :, 0] = 2
    values[:, :, 1] = 1

    ranks = percentile_rank_blocks(values)

    assert ranks[0, 0, 2] == pytest.approx(0.0)
    assert ranks[0, 0, 3] == pytest.approx(1 / 69)
    assert ranks[0, 0, 1] == pytest.approx(68 / 69)
    assert ranks[0, 0, 0] == pytest.approx(1.0)


def test_block_mask_enforces_quota_and_expands_contiguous_channels() -> None:
    mapping = build_mapping(128)
    selected = {layer: list(range(mapping.per_layer_quota[layer])) for layer in range(28)}
    mask = BlockMask(
        "gradient_domain_code_128",
        128,
        "gradient",
        "domain_selectivity",
        "code",
        selected,
        mapping.mapping_hash,
        mapping.quota_pattern_hash,
    )

    validate_block_mask(mask, mapping)
    assert expanded_channels(mask, mapping, 0) == list(range(512))
    assert expanded_channels(mask, mapping, 1) == list(range(384))
    assert mask.selected_channel_count == 12_544
    assert "signed" not in " ".join(mask.to_dict()).casefold()


def test_block_mask_rejects_quota_drift() -> None:
    mapping = build_mapping(128)
    selected = {layer: [0, 1, 2] for layer in range(28)}
    mask = BlockMask(
        "bad",
        128,
        "gradient",
        "domain_selectivity",
        "code",
        selected,
        mapping.mapping_hash,
        mapping.quota_pattern_hash,
    )

    with pytest.raises(ValueError, match="frozen per-layer quota"):
        validate_block_mask(mask, mapping)


def test_qwen3b_mask_preserves_model_geometry_and_capacity() -> None:
    mapping = build_mapping(64, intermediate_size=11_008, layer_count=36)
    selected = {layer: list(range(mapping.per_layer_quota[layer])) for layer in range(36)}
    mask = BlockMask(
        "qwen3b_gradient_code",
        64,
        "gradient",
        "domain_selectivity",
        "code",
        selected,
        mapping.mapping_hash,
        mapping.quota_pattern_hash,
        layer_count=36,
        intermediate_size=11_008,
    )

    validate_block_mask(mask, mapping)
    assert mask.selected_channel_count == 19_840
    assert mask.to_dict()["total_fraction"] == pytest.approx(0.05006459948320414)
