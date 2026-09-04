# SelectiveLLM v0.1 Design

Date: 2026-09-04
Status: Approved for implementation

## 1. Objective

SelectiveLLM is a Python 3.11+ research framework for testing whether independently defined model capacity can be selected, loaded, and cached under a fixed memory budget according to prompt requirements.

The v0.1 centerpiece is a reproducible mixed-domain benchmark that answers:

> Under a constrained accelerator-memory budget, can semantic expert routing preserve task quality while keeping less expert capacity resident than an always-loaded system?

The first test vehicle is a shared base model plus specialized experts or PEFT/LoRA adapters. This demonstrates routing and systems behavior over separable capacity. It does not demonstrate semantic parameter paging inside an arbitrary dense transformer.

SelectiveLLM does NOT currently turn a dense 70B model into a 7B-memory model.

## 2. Scientific Claims and Boundaries

### What v0.1 can demonstrate

- Semantic and multi-capability routing accuracy over independently defined experts.
- Quality, memory, and latency tradeoffs against explicit baselines.
- The memory-state and swap behavior of a budget-aware expert cache.
- The latency benefit of caching on repeated mixed-domain workloads.
- Whether correct routing improves generation quality for the configured real or control backend.

### What v0.1 cannot demonstrate

- That dense-model knowledge maps cleanly to semantic parameter blocks.
- That arbitrary dense models can be decomposed without retraining.
- That simulated capacity corresponds to physical VRAM savings.
- That a large model's quality can be reproduced at a small model's memory cost.

The repository will distinguish established techniques, implemented experiments, hypotheses, and future work. Its current contribution is a unified, reproducible experimental framing around treating model capacity as a dynamically retrieved resource.

## 3. Implementation Approach

v0.1 uses an evidence-first hybrid architecture:

1. A deterministic benchmark/control backend runs offline on CPU and exercises the complete methodology without model downloads.
2. Hugging Face Transformers and PEFT use the same interfaces, benchmark cases, routing decisions, runtime events, result schema, and reports.
3. Backend provenance is mandatory in every result row, summary, plot, report, and README result reference.

The control backend provides reproducible routing and systems experiments. It is not evidence of physical accelerator-memory reduction. Real memory and inference claims require runs from a real inference backend.

## 4. System Architecture

```text
Prompt
  -> Prompt Analyzer
  -> Router
  -> Budget-Aware Selection Policy
  -> Capacity Registry
  -> Runtime Loader + Memory-Aware Cache
  -> Inference Backend
  -> Metrics Collector
  -> Reproducibility Recorder
  -> Benchmark Report + Plots + Failure Analysis
           |
           +---- policy feedback inputs for future experiments
```

Each subsystem has a small typed contract and can be replaced independently. The orchestration engine depends on interfaces rather than concrete routers or backends.

### Prompt analyzer

The analyzer emits a typed profile containing detected domains, tasks, programming language, estimated difficulty, required capabilities, confidence, and evidence. The initial implementation combines normalized text features with deterministic hashed embeddings so the default path requires no model download. The interface permits later classifier, small-model, learned, and reinforcement-learning analyzers.

Multi-domain prompts retain multiple capabilities and scores. They are not collapsed to one label.

### Routers

The router contract accepts a prompt profile, registry snapshot, and selection constraints. It returns ranked component candidates, selected components, per-component scores, aggregate confidence, latency, and debug metadata.

Implemented strategies:

- Static router for configured selections.
- Keyword router as a hostile non-semantic baseline.
- Embedding router using cosine similarity.
- Top-k router preserving multiple capabilities.
- Threshold router selecting all candidates above a score threshold.
- Hybrid router combining semantic, keyword, priority, and dependency signals.
- Random router with seeded reproducibility.
- Oracle router using benchmark labels only during evaluation.

### Capacity registry

YAML registries describe components with identifiers, names, types, domains, descriptions, declared capacity, backend, model path, supported tasks, embedding representation, priority, dependencies, and optional parameter counts.

The schema supports base models, expert models, adapters, LoRA adapters, prompt adapters, classifiers, rerankers, tools, and future parameter shards. v0.1 runtime behavior is implemented for the types supported by the selected backend; future types remain schema-level extension points and are labeled accordingly.

### Selection policy

The planner turns ranked candidates into an executable selection while accounting for required base capacity, dependencies, top-k or threshold policy, and memory budget. It records rejected candidates and reasons such as score, budget, unsupported backend, or dependency failure.

### Runtime loader and cache

The runtime owns component lifecycle, placement state, load/unload operations, capacity accounting, and cache policy. A memory-aware LRU cache evicts the least recently used non-required components until the planned selection fits. Cache hits, misses, evictions, swaps, and transfers are structured events.

The runtime distinguishes:

- Declared or simulated component capacity.
- Process resident host RAM.
- Actual accelerator memory allocated and reserved when exposed by the platform.
- Model parameters, adapter capacity, KV cache, and framework overhead when technically measurable.

No simulated quantity is labeled VRAM. Unsupported measurements are null with an explicit availability reason, never zero or estimated silently.

### Inference backends

All backends implement the same lifecycle and generation contract: inspect capabilities, load base, load expert, unload expert, generate, synchronize, and report measurable memory.

The deterministic backend emits reproducible task-conditioned answers and controlled timing/capacity events for methodology validation. Reports identify it as `deterministic-control`.

The Transformers/PEFT backend supports local or explicitly configured Hugging Face models and adapters, automatic device selection in CUDA -> MPS -> CPU order, optional quantization where supported, and safe defaults. `trust_remote_code` is false unless explicitly enabled. Model weights are never committed.

Future llama.cpp, MLX, vLLM, ExLlamaV2, and TensorRT-LLM backends fit the same contract but are not claimed as implemented in v0.1.

### Metrics and provenance

Each generation records backend, device, router, policy, selected experts, resident set, routing time, planning time, loading time, inference time, first-token latency, total latency, throughput, host RAM, available accelerator measurements, declared capacity, cache events, swaps, and output quality.

The additive latency model is:

```text
T_total = T_route + T_plan + T_load + T_inference + measured orchestration overhead
```

Environment manifests record configuration, seed, operating system, CPU, total RAM, accelerator, reported VRAM, CUDA version, PyTorch version, MPS availability, Python version, dependency versions, and Git commit.

Benchmark-level aggregates report sample count and, where meaningful, mean, median, standard deviation, p50, and p95. Repeated runs can report confidence intervals and retain their individual observations so a single run is not presented as universal evidence.

Every completed run stores a benchmark fingerprint derived from the backend, model identity, adapter set, benchmark version, seed policy, device class, measurement semantics, registry version, routing configuration version, and metric schema version. Results may share a comparison table or plot only when those compatibility fields match, except for the intentionally varied experimental method. Comparison tooling rejects or visibly separates incompatible runs.

Benchmark datasets, registry configurations, routing configurations, and metric schemas carry explicit versions. Changes to cases, labels, evaluation logic, component definitions, routing semantics, or metric meanings require a version change and therefore cannot silently inherit comparability with older artifacts.

## 5. Hero Experiment

The primary workload contains general knowledge, Python, mathematics, electrical engineering, reasoning, ambiguous prompts, irrelevant-domain prompts, and multi-domain prompts such as Python-based RLC simulation.

Every example contains a prompt, expected capability set, expected expert set, reference, quality-evaluation method, and tags.

Methods compared:

- Base only.
- Random routing.
- Keyword routing.
- Oracle routing.
- Semantic routing.
- Semantic routing plus memory-aware cache.
- All-resident experts where the backend and budget make this meaningful.

Primary metrics:

- Task quality and quality retention relative to oracle.
- Routing precision, recall, F1, top-1 accuracy, and top-k recall.
- False and unnecessary expert activations.
- Declared resident capacity and capacity reduction.
- Actual peak accelerator memory where measurable.
- Host RAM.
- Average, p50, and p95 latency.
- Routing, planning, load, first-token, and generation latency.
- Tokens per second.
- Cache hit rate and expert swaps.

The primary plot is quality retention versus memory saved. It may only compare measurements with compatible backend, model, device, workload, and measurement semantics. Deterministic-control and real-backend results are never presented as one undifferentiated series.

### Ablations

- No routing/base only.
- Random, keyword, embedding, and hybrid routing.
- Different top-k values.
- Different thresholds.
- Different cache budgets and effective cache sizes.
- Cold-cache and warm-cache workloads.

### Failure analysis

Each run saves:

- Misrouted prompts.
- Low-confidence decisions.
- Missing required experts.
- Unnecessary activations.
- Budget-rejected relevant experts.
- Correctly routed prompts whose output did not improve over base-only.

Failure records include the prompt, expected and selected experts, scores, confidence, runtime state, baseline quality, routed quality, and a deterministic reason category where one can be derived. Reports do not hide or discard failures.

### Negative-result principle

Negative and null results are first-class evidence. If semantic routing does not outperform keyword or random routing, correct routing does not improve generation quality, or loading overhead overwhelms the memory benefit, the run and its failure analysis are preserved and documented. Benchmark cases and evaluation logic are not tuned solely to make SelectiveLLM appear successful.

## 6. Result Artifacts

Each benchmark writes an immutable run directory under `results/<run-id>/` containing:

```text
config.yaml
environment.json
raw_results.jsonl
routing_decisions.jsonl
summary.json
summary.csv
report.md
routing_failures.md
plots/
```

`results/latest` points to or mirrors the latest completed run in a cross-platform-safe manner. Partial or failed runs remain identifiable and never replace the latest completed result.

Plots are generated only from available observations:

- `quality_vs_memory.png`
- `routing_accuracy.png`
- `latency_breakdown.png`
- `cache_hit_rate.png`
- `expert_selection_confusion_matrix.png`

Missing metrics produce an annotated omission in the report, not fabricated points.

## 7. CLI and Python API

The Rich-based CLI provides:

- `selectivellm demo`
- `selectivellm run`
- `selectivellm inspect`
- `selectivellm profile`
- `selectivellm benchmark`
- `selectivellm benchmark --report`
- `selectivellm registry list`
- `selectivellm registry inspect <id>`

Commands support deterministic seeds, verbosity, explicit backend and router selection, memory budgets, and output locations. The five-minute default demo uses the deterministic-control backend and labels it prominently.

The Python API centers on `SelectiveLLM.from_config(...)` and `generate(...)`, returning typed text, routing, runtime, backend, and metric results.

## 8. Errors and Safety

Configuration and registry errors fail early with field-level messages. Runtime budget failures explain required capacity, available budget, and non-evictable components. Backend capability errors distinguish unavailable dependencies, unsupported devices, missing model paths, incompatible adapters, and unsupported measurements.

Benchmark errors are recorded per case when recovery is possible. Fatal configuration or provenance failures stop the run to avoid publishing misleading results.

The project never executes generated code. Remote-code trust is opt-in. Paths are validated, model licenses remain external to the Apache-2.0 project license, secrets are not logged, and no model weights are stored in the repository.

## 9. Testing and Verification

Tests require no network and no large model downloads. They cover:

- Registry validation and dependency resolution.
- Single- and multi-domain analysis.
- Router ranking, thresholds, top-k, seeded randomness, and oracle isolation.
- Budget planning and rejection reasons.
- LRU hit, miss, eviction, and impossible-budget behavior.
- Metric availability and unit labeling.
- Aggregate statistics, repeated-run confidence intervals, and small-sample behavior.
- Compatibility fingerprints and rejection of invalid cross-run comparisons.
- Dataset, registry, routing, and metric-schema version propagation.
- Backend parity through shared contract tests.
- Benchmark baselines, quality metrics, failure classification, report schemas, and plot generation.
- CLI smoke tests and Python API integration.
- CUDA, MPS, and CPU device-selection logic through mocks.
- Security defaults and reproducibility metadata.

An optional integration marker exercises user-supplied tiny Transformers/PEFT models. CI runs formatting/linting, type checking, unit/integration-control tests, and package build checks on CPU.

Before release, the documented quickstart, demo, benchmark report, plots, install flow, lint, type checks, and tests are run in a clean environment where practical.

## 10. Repository and Documentation

The repository includes only purposeful code and documents. Required public-project files include Apache-2.0 licensing, contribution and conduct guides, security policy, citation metadata, changelog, pre-commit configuration, CI, issue templates, pull-request template, examples, benchmark data, experiment configuration, and v0.1.0 release notes.

The README leads with the research question, experimental status, current evidence, architecture, and result section before installation. It includes both Mermaid and compact text architecture views, backend labels on every result, explicit limitations, research questions, quickstart, CLI and API examples, roadmap, related work, citation, and model-license separation.

Research documentation covers concepts, architecture, benchmarking, roadmap, related work using primary papers and official repositories, research questions and hypothesis matrix, semantic parameter paging, and a living paper-style technical report.

If only deterministic-control results exist, the README states that exactly. Real-backend result tables remain pending until reproducible runs are completed.

## 11. Implementation Order

1. Package foundation, typed schemas, configuration, and device inspection.
2. Analyzer, registry, routers, planner, runtime, cache, and metric contracts.
3. Deterministic-control backend and end-to-end engine.
4. Hero benchmark, hostile baselines, ablations, failure analysis, reports, and plots.
5. Transformers/PEFT backend through the same contracts.
6. Rich CLI, Python API, examples, and experiment scripts.
7. Tests, static analysis, package build, and CI.
8. Research documentation, README, release material, and contribution templates.
9. Execute available benchmarks and preserve genuine artifacts.
10. Perform a hostile external-review pass and fix credibility, usability, and scientific-framing issues.

## 12. v0.1 Completion Criteria

v0.1 is complete when a fresh CPU-only installation can run the deterministic-control demo and hero benchmark, generate all applicable artifacts and plots, and quantitatively compare the required baselines without mislabeled memory claims. The same benchmark methodology must be executable through the real Transformers/PEFT backend when compatible model and adapter paths are supplied.

The repository's defensible conclusion should be:

> We demonstrated that semantic routing can select independently defined specialized model capacity under a fixed memory budget, measured the quality/memory/latency tradeoff against oracle, random, base-only, keyword, and all-resident baselines, and quantified the benefit of caching. Parameter-level semantic paging inside arbitrary dense models remains an open research problem.

The strength of that conclusion is limited to the backend, models, adapters, workload, and measurements recorded in each reproducible run.
