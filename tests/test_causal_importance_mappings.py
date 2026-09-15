from __future__ import annotations

import json

import pytest

from selectivellm.causal_importance.mappings import (
    INTERMEDIATE_SIZE,
    BlockMapping,
    BlockRange,
    build_mapping,
    validate_mapping,
)


@pytest.mark.parametrize("block_size,blocks_per_layer", [(64, 140), (128, 70)])
def test_mapping_covers_every_channel_once(block_size: int, blocks_per_layer: int) -> None:
    mapping = build_mapping(block_size)  # type: ignore[arg-type]

    assert mapping.blocks_per_layer == blocks_per_layer
    assert mapping.blocks[0] == BlockRange(0, 0, block_size)
    assert mapping.blocks[-1].stop_channel == INTERMEDIATE_SIZE
    covered = [
        channel
        for block in mapping.blocks
        for channel in range(block.start_channel, block.stop_channel)
    ]
    assert covered == list(range(INTERMEDIATE_SIZE))


def test_mappings_select_exactly_same_five_percent_capacity() -> None:
    mapping64 = build_mapping(64)
    mapping128 = build_mapping(128)

    assert mapping64.per_layer_quota == (7,) * 28
    assert mapping128.per_layer_quota == tuple(4 if layer % 2 == 0 else 3 for layer in range(28))
    assert mapping64.total_selected_blocks == 196
    assert mapping128.total_selected_blocks == 98
    assert mapping64.total_selected_channels == mapping128.total_selected_channels == 12_544
    assert mapping64.to_dict()["total_fraction"] == mapping128.to_dict()["total_fraction"] == 0.05


def test_mapping_and_quota_hashes_are_stable() -> None:
    first = build_mapping(128)
    second = build_mapping(128)

    assert first.mapping_hash == second.mapping_hash
    assert first.quota_pattern_hash == second.quota_pattern_hash
    assert first.to_dict()["mapping_sha256"] == first.mapping_hash
    assert build_mapping(64).mapping_hash == (
        "c7d55beae21124b7b3e3d96857ad9aec5d92ddc03d616e829d15bcd8d3b8bb73"
    )
    assert first.mapping_hash == "540d63699a469a54b86d9bd5d07df9110fc1266791b0c8c1b1636412d0c1018a"
    json.dumps(first.to_dict(), sort_keys=True)


def test_qwen3b_mappings_use_frozen_nearest_five_percent_footprint() -> None:
    mapping64 = build_mapping(64, intermediate_size=11_008, layer_count=36)
    mapping128 = build_mapping(128, intermediate_size=11_008, layer_count=36)

    expected64 = tuple(((layer + 1) * 310) // 36 - (layer * 310) // 36 for layer in range(36))
    expected128 = tuple(((layer + 1) * 155) // 36 - (layer * 155) // 36 for layer in range(36))
    assert mapping64.per_layer_quota == expected64
    assert mapping128.per_layer_quota == expected128
    assert mapping64.blocks_per_layer == 172
    assert mapping128.blocks_per_layer == 86
    assert mapping64.total_selected_channels == mapping128.total_selected_channels == 19_840
    assert mapping64.total_layer_channels == mapping128.total_layer_channels == 396_288
    assert mapping64.to_dict()["total_fraction"] == pytest.approx(0.05006459948320414)


def test_modified_quota_is_rejected() -> None:
    mapping = build_mapping(128)
    invalid = BlockMapping(mapping.block_size, mapping.blocks, (3,) * 28)

    with pytest.raises(ValueError, match="preregistered model geometry"):
        validate_mapping(invalid)
