# Benchmarking methodology

## Hero experiment

The `hero-1.0.0` dataset contains 16 authored prompts across Python, mathematics, electrical engineering, reasoning, scientific writing, general knowledge, lexical traps, and multi-domain requests. The RLC simulation case requires three capabilities and can exceed the default two-expert capacity budget after planning.

Run the complete control experiment:

```bash
selectivellm benchmark --report --repetitions 3 --seed 42
```

Run one method:

```bash
selectivellm benchmark --router semantic --report
```

## Required baselines

| Method | Purpose |
|---|---|
| `base_only` | Measures capability without any expert |
| `random` | Tests whether routing itself matters |
| `keyword` | Tests whether semantics beats a transparent lexical rule |
| `oracle` | Uses expected expert labels as an upper-bound routing control |
| `embedding` | Isolates deterministic feature-hash similarity |
| `semantic_top1` | Measures single-expert routing loss |
| `semantic` | Hybrid multi-label routing under budget |
| `semantic_threshold_high` | Tests sensitivity to routing threshold |
| `semantic_cache` | Measures reuse under the default cache budget |
| `semantic_cache_small` | Measures a one-expert cache constraint |
| `all_resident` | Measures all declared experts resident where meaningful |

For `oracle` and `all_resident`, the runner allows declared capacity above the normal budget so they can serve as controls. Their memory rows reveal that difference.

## Measurement semantics

Three memory concepts remain separate:

1. Declared resident capacity: component registry metadata used by the planner and control experiment.
2. Host RSS: observed process resident memory, including interpreter and framework overhead.
3. Accelerator memory: observed allocated/reserved/peak values only when the active runtime exposes them.

An unavailable accelerator measurement is serialized as `null` with a reason. It is never converted to zero. Deterministic-control load and inference latency are measured wall-clock time for the control implementation, not estimates of adapter transfer or LLM generation time.

## Statistics

Aggregate metrics include sample count, mean, median, sample standard deviation, p50, p95, and a normal-approximation 95% confidence interval when more than one observation exists. The interval describes the observed workload samples. It is not a claim about unseen models or deployments.

Use repeated benchmark runs and independent seeds for stronger uncertainty estimates. Preserve each run rather than averaging away run-to-run variation. Real latency studies should include warmup, enough repetitions, and device synchronization.

## Validity guard

Each run stores two SHA-256 values:

- `benchmark_fingerprint` covers backend and kind, model identity, adapter set, benchmark/registry/router/metric versions, seed policy, device class, and measurement semantics.
- `configuration_fingerprint` adds the methods and repetition count.

Only runs with compatible benchmark fingerprints may share an undifferentiated table or plot. The method under comparison is intentionally excluded from the compatibility hash. Changes to cases, labels, evaluation logic, registry components, routing semantics, or metric meanings require a version increment.

## Quality evaluation

The control backend uses `synthetic_capability_coverage_v1`: a documented score derived from required expert coverage with a base floor. It proves only that the pipeline responds correctly to capacity sufficiency. It is not language-model accuracy.

Real backends use case-declared exact match or token F1 in v0.1. Those simple metrics are insufficient for open-ended generation, so a serious real-model study should add task-specific tests, code execution in an isolated evaluator, human evaluation, or a separately reported judge. LLM-as-judge is optional and never the sole primary metric.

## Failure analysis

`routing_failures.md` records missing experts, unnecessary activations, low-confidence routes, budget rejections in raw rows, and cases where correct routing does not improve quality. A future report revision should group these by cause and include confidence calibration.

## Reproducing a run

Use the saved `config.yaml`, match the environment and model/adapter assets recorded in `manifest.json`, and rerun against the same benchmark version. Compare fingerprints before combining results. Model weights are external and remain governed by their own licenses.
