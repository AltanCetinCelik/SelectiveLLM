# SelectiveLLM v0.1.1 Real-Model Validation Design

Date: 2026-09-04
Status: Approved for implementation

## Objective

Run the existing evidence-first methodology against real independently produced PEFT capacity and answer:

> Can semantic expert routing reduce resident specialized model capacity while preserving useful task quality under a constrained memory budget?

The result may be negative. The experiment will not change adapters, benchmark cases, or evaluation criteria after method-level results are inspected.

## Fixed Assets

All assets use Apache-2.0 metadata and are pinned by immutable Hugging Face revision.

| Role | Repository | Revision |
|---|---|---|
| Base and tokenizer | `Qwen/Qwen2.5-1.5B-Instruct` | `989aa7980e4cf806f80c7fef2b1adb7bc71aa306` |
| Code expert | `uditjain/lori-qwen2.5-1.5b-code` | `e937bbd728f28a441163f94b60ea5a119513e351` |
| Mathematics expert | `uditjain/lori-qwen2.5-1.5b-math` | `f992ab536c07761c67bd46e35c787bb68ea97657` |
| Science/technical expert | `uditjain/lori-qwen2.5-1.5b-science` | `398cf3cc78a3ff8c78c84c3a424da3ba994bdd6f` |

The preflight must download metadata before weights and reject any adapter whose base identifier, PEFT type, rank, alpha, target modules, tokenizer/base relationship, revision, or license is incompatible. It writes `compatibility_report.json` into the run.

## Hardware and Measurement Semantics

The target is the available Apple M4 MacBook Air: arm64, 10 CPU cores, 16 GB unified memory, 8-core Apple M4 GPU, Metal 4, no CUDA, and MPS when the installed PyTorch build exposes it.

Memory is sampled at process start, after base load, after every adapter load, immediately before generation, during generation where supported, immediately after generation, after adapter eviction, and after intentional synchronization or cold-run cleanup.

Measurements remain separate:

- `host_rss_mb`: process resident memory in unified system memory.
- `mps_current_allocated_mb`: live tensor allocation reported by the MPS allocator; this excludes allocator cache pools.
- `mps_driver_allocated_mb`: total Metal-driver allocation for the process; this includes allocator caches and framework allocations.
- Adapter file bytes, parameter counts, and registry capacity metadata.

No MPS metric is called VRAM. Ordinary warm runs do not clear allocator caches. Deliberate cold-run cleanup is labeled.

## Backend and Runtime Changes

The existing backend contract remains shared with deterministic control, but the real implementation gains:

- Immutable model, tokenizer, and adapter revisions.
- Chat-template prompt formatting.
- Dtype and MPS placement metadata.
- Adapter activation separate from adapter residency.
- Persistent all-resident loading without reconstruction between requests.
- Multi-adapter activation with an explicit `multi-active` label.
- Synchronized load, activation, first-token, generation, and lifecycle measurements.
- Structured compatibility and provenance metadata.

`all-resident` means all adapter tensors are loaded. It does not mean all adapters are active. `multi-active` means two or more adapters participate in one inference. Each raw row records both resident and active sets.

## Benchmark

A versioned real subset derived from the hero workload will cover:

- Straightforward and harder Python/code prompts.
- Straightforward and harder mathematics prompts.
- Electronics/scientific prompts.
- Base-sufficient general prompts.
- Lexical traps and ambiguous prompts.
- Multi-domain RC/RLC prompts.
- Explicit `no-specialist-needed` expectations.

The RLC case is also run as a focused matrix: base only, code only, science only, code plus science if supported, semantic selection, and oracle selection.

Primary routing methods are base-only, random, keyword, oracle, semantic, semantic with cache, and all-resident. All-resident keeps all adapters loaded but activates only the policy-selected adapter set for a quality-comparable residency baseline. A separate multi-active method tests composition behavior.

The repeated cache experiment reuses identical prompts, order, and seeds for effective capacities 0, 1, and 3 under both high-locality and adversarial low-locality orderings. Cold start, warm-up, and measured repetitions are labeled separately.

## Fixed Quality Evaluation

Real quality never uses synthetic capability coverage. Before generation, each case defines one of:

- Normalized exact-answer matching.
- Numeric answer extraction with a declared tolerance.
- Deterministic concept coverage, with predeclared groups of acceptable phrases.
- A conservative structured rubric composed only of those checks.

Generated code is not executed. Open-ended text is scored only against fixed observable concepts, and raw text remains available for inspection. Each row records absolute quality, delta from base for the same case, and delta from oracle for the same case. Oracle is not treated as a guaranteed upper bound.

Failure outputs explicitly retain oracle-worse-than-base, correct-route-quality-drop, random-wins, unnecessary activation, general-capability damage, routing errors, composition degradation, and budget rejection.

## Timing

MPS synchronization occurs at timing boundaries. Raw and aggregate output separates:

- Router latency.
- Planner latency.
- Adapter load and unload latency.
- Adapter activation latency.
- Synchronization latency.
- First-token latency from a token streamer where technically reliable.
- Total generation latency.
- End-to-end latency.

Aggregates report count, mean, median, sample standard deviation, p50, p95, and 95% confidence intervals where meaningful. Cold and warm observations are never silently pooled.

## Artifacts and Comparability

Real artifacts live under `results/real/<run-id>/` and `results/real/latest/`. Deterministic artifacts remain separate.

Each real run preserves compatibility report, configuration, environment, manifest, raw responses, raw telemetry checkpoints, routing decisions, evaluation outputs, summary JSON/CSV, plots, failure analysis, and report.

The real-run fingerprint includes exact model/tokenizer/adapter revisions, PEFT configuration hashes, benchmark and evaluation versions/hashes, router configuration, runtime/cache policy, dependency versions, and device/platform identity. Incompatible fingerprints cannot share a comparison table or plot.

Large model and adapter weights remain in the Hugging Face cache and are not committed.

## Verification and Interpretation

Unit tests cover compatibility rejection, rubric scoring, residency versus activation, MPS metric semantics, lifecycle checkpoint ordering, cache workload identity, fingerprint inputs, and artifact completeness. The final gate includes pre-commit, Ruff, mypy, pytest with coverage, package build, and clean-wheel smoke testing.

The written conclusion answers all twenty requested experimental questions, reports contradictions without tuning them away, and recommends the next experiment based on the observed bottleneck: routing, prefetch, composition, pool size, expert training, or activation tracing.
