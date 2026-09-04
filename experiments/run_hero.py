"""Programmatic entry point for the versioned hero benchmark."""

from pathlib import Path

from selectivellm.benchmarking import BenchmarkRunner
from selectivellm.config import SelectiveLLMConfig

config = SelectiveLLMConfig.from_yaml(Path("configs/default.yaml"))
run_path = BenchmarkRunner(config).run(report=True)
print(run_path)
