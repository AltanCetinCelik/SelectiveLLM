#!/usr/bin/env python3
"""Run the invariant-only Qwen2.5-3B scale-replication preflight."""

from selectivellm.causal_importance.runner import CausalImportanceRunner

if __name__ == "__main__":
    runner = CausalImportanceRunner("configs/causal_scale_qwen3b_v1.yaml")
    print(runner.preflight())
