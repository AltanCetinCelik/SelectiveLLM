#!/usr/bin/env python3
"""Generate the canonical preregistered contiguous-block mapping artifacts."""

from selectivellm.causal_importance.mappings import write_mapping_artifacts

if __name__ == "__main__":
    for path in write_mapping_artifacts("selectivellm/resources"):
        print(path)
