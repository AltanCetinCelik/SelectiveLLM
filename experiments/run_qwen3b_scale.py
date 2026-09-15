#!/usr/bin/env python3
"""Execute the preregistered Qwen2.5-3B causal-capacity scale replication."""

from selectivellm.causal_importance.runner import CausalImportanceRunner

if __name__ == "__main__":
    runner = CausalImportanceRunner("configs/causal_scale_qwen3b_v1.yaml")
    print(runner.run())
