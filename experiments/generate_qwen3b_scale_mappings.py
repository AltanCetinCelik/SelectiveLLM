#!/usr/bin/env python3
"""Generate preregistered Qwen2.5-3B contiguous-block mappings."""

from selectivellm.causal_importance.mappings import write_mapping_artifacts

if __name__ == "__main__":
    for path in write_mapping_artifacts(
        "selectivellm/resources",
        intermediate_size=11_008,
        layer_count=36,
        filename_prefix="causal_scale_qwen3b",
    ):
        print(path)
