# Benchmark artifacts

`selectivellm benchmark --report` writes immutable runs to `results/<run-id>/` and copies the latest completed run to `results/latest/`.

Generated runs are ignored by Git by default because timings and machine measurements are environment-specific. Publish a run intentionally only after reviewing its manifest, backend label, fingerprint, and measurement semantics.
