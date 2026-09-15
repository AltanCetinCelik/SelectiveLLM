# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) principles. This project uses semantic versioning for software and independent explicit versions for benchmark, registry, routing, and metric schemas.

## [Unreleased]

### Added

- Preregistered 108-generation expert-quality diagnostic with case-bootstrap uncertainty, empirical-oracle opportunity, label-mismatch analysis, and a separate evaluator sensitivity audit.
- Dense Qwen2.5-1.5B activation/head/layer feasibility study with held-out logical interventions and structurally matched controls.
- Objective-aware contiguous-MLP-block causal experiment on Qwen2.5-1.5B plus a strict same-family Qwen2.5-3B scale replication.
- Clean-source provenance, immutable-input verification, mapping hashes, signed Taylor diagnostics, failure artifacts, and paired model-scale comparison.

### Research result

- The expert pool has measurable empirical response diversity, but robust domain specialization and a semantic-router quality gain were not established.
- Both dense causal experiments returned preregistered Outcome C. The 3B model increased several causal point estimates but did not rescue discovery stability or matched-control confidence intervals.
- No dense experiment unloaded parameters or measured physical-memory reduction; semantic parameter paging remains unimplemented.

## [0.1.1] - 2026-09-05

### Added

- Completed pinned Qwen2.5-1.5B-Instruct real-model validation with public same-base code, math, and science LoRA adapters on Apple M4/MPS.
- Programmatic adapter compatibility and license preflight with exact revisions, PEFT configuration hashes, tokenizer checks, and archived registry/benchmark inputs.
- 396-observation hostile policy matrix plus an 18-observation RLC multi-adapter matrix, fixed deterministic answer rubrics, raw responses, lifecycle telemetry, failure analysis, statistics, and plots.
- Real adapter residency, loading, unloading, activation, synchronization, first-token, generation, cache, host RSS, MPS live allocation, and Metal driver allocation measurements.

### Changed

- Real-run manifests now include registry and metric-schema fingerprints in the compatibility hash.
- Cache hit reporting is weighted over actual adapter requests rather than averaging prompt-level ratios.

### Fixed

- Unwrap the PEFT model after evicting its final source adapter so later loads do not inherit an empty stale wrapper.
- Preserve multi-adapter composition as an explicit weighted-linear derived-adapter mode and keep it distinct from all-resident source capacity.

### Research result

- Dynamic routing reduced mean MPS live tensor allocation by 286.427 MB versus all-resident, and cache benefits tracked workload locality.
- Semantic routing improved multi-label F1 but did not beat random on aggregate answer quality; RLC composition degraded quality. The negative result is preserved as the v0.1.1 conclusion.

## [0.1.0] - 2026-09-04

### Added

- Typed prompt analysis, routing, registry, selection, runtime, backend, and metric contracts.
- Static, keyword, random, oracle, embedding, top-k, threshold, and hybrid routers.
- Budget-aware LRU component loading with separated declared, host, and accelerator memory measurements.
- Deterministic-control and optional Transformers/PEFT backends behind one lifecycle API.
- Versioned mixed-domain hero benchmark with hostile baselines, ablations, statistical summaries, compatibility fingerprints, failure analysis, reports, and plots.
- Rich CLI, Python API, hardware inspection, tests, CI, and research documentation.
