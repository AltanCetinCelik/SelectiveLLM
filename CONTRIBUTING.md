# Contributing to SelectiveLLM

SelectiveLLM welcomes reproducible experiments, router implementations, backend integrations, measurement corrections, and documentation improvements.

## Development setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest
ruff check .
mypy selectivellm
```

Optional real-model work uses `pip install -e ".[dev,hf]"`. Tests submitted to the default suite must not download model weights or require an accelerator.

## Research contributions

Experiment results must include the complete run directory, backend identity, model and adapter licensing information, benchmark fingerprint, hardware manifest, seed policy, and any failures. Do not merge incompatible fingerprints into one result table. Negative results are welcome and must not be suppressed.

Pull requests should explain the hypothesis or defect, baseline, metric, expected comparability impact, tests, and reproducibility steps. Changes to benchmark cases, registry semantics, routing behavior, or metric definitions require a version increment.

By participating, you agree to the [Code of Conduct](CODE_OF_CONDUCT.md). Contributions are licensed under Apache-2.0.
