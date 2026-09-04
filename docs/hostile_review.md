# Hostile review of v0.1

This review uses the committed deterministic-control run in `results/latest`. Its benchmark fingerprint is `3792ea55c906065d90f9a79b15b301169e929817fad7fde76491f9c751a6a34d`. All quantitative statements below are limited to that backend, authored workload, registry, and measurement semantics.

## Is this merely adapter routing?

The v0.1 real-model test vehicle is adapter/expert routing. That is intentional and not presented as a new algorithm. The broader engineering contribution is a backend-independent experiment contract joining multi-label analysis, hostile routing baselines, budget planning, lifecycle/cache management, separated memory semantics, validity fingerprints, and failure reporting. Whether that framework leads beyond adapter routing is unproven.

Evidence: adapters and experts share the capacity schema and backend lifecycle; the semantic paging type remains unsupported; the [related-work comparison](related_work.md) positions adapter routing as the closest v0.1 description.

## Is this merely Mixture-of-Experts?

No, although it overlaps with conditional computation. Conventional MoE models usually train architectural experts together and route tokens during a forward pass. SelectiveLLM v0.1 routes whole prompts to independently loadable modules before generation and includes placement, eviction, and load latency in the experiment. It does not claim to improve MoE training or token-level load balancing.

Evidence: the router operates on prompt profiles and registry components; the runtime emits load/unload/cache events; no MoE layer or token gate is implemented.

## Is the memory reduction real or simulated?

The included memory reduction is simulated declared capacity. Semantic routing used a mean declared peak of 857.8 MB versus 1580.0 MB all-resident, a 45.7% reduction in registry capacity. Accelerator memory was unavailable and serialized as `null`. Host RSS was observed, but it is not evidence that declared experts occupied physical memory.

Evidence: `manifest.json` identifies `deterministic-control`; every raw row contains `measurement_semantics`; the primary plot says declared capacity and simulated control; the real backend has not produced the included run.

## Does better routing actually improve output quality?

It improves only the control backend's synthetic capability-coverage score. Mean semantic routing F1 was 0.696, versus 0.198 for keyword and 0.150 for random. Corresponding control scores were 0.801, 0.503, and 0.514; base-only scored 0.431 and oracle 1.000. This relationship is partly mechanical because control quality is defined from required-capability coverage. It does not show that a real model generates better answers.

The real hypothesis remains open. A compatible Transformers/PEFT run with task-specific evaluation must show that routing gains transfer to output quality.

## What happens when prompts require multiple experts?

The analyzer and router retain multiple labels. For “Use Python to simulate an RLC circuit and plot the transient response,” the benchmark expects Python, electrical engineering, and mathematics. Semantic routing ranked all three, but the 900 MB budget admitted two experts with the 500 MB base and rejected `math_expert` as `memory_budget`. The control score was 0.783 versus oracle 1.000.

Across the workload, top-1 semantic routing retained 0.767 control quality while multi-label semantic routing retained 0.801. This control result exposes both the benefit of multi-label routing and the quality loss when the capacity plan cannot fit every requested expert. Real adapter composition may introduce additional incompatibility and interference.

## What is the latency cost of swapping?

On this control implementation, uncached semantic routing performed 80 expert misses and 80 unloads across 80 observations. Mean load-stage latency was about 0.363 ms and end-to-end p95 was about 1.654 ms. All-resident performed six cold expert loads, no swaps, and had about 0.450 ms p95 end-to-end latency.

These are measured wall-clock control costs, not forecasts for model transfers. The real cost depends on adapter size, storage, interconnect, device synchronization, framework behavior, and generation length.

## Under what workload does caching help?

The benchmark repeats a mixed-domain sequence with local clusters. Under that order, semantic caching served 30 of 80 expert requests as hits, reduced misses from 80 to 50 and swaps from 80 to 48, lowered mean control load time from about 0.363 ms to 0.236 ms, and lowered p95 end-to-end latency from about 1.654 ms to 1.354 ms without changing selected capacity or control quality.

Caching helps when repeated requests reuse experts before eviction and load cost is material. It may not help under low-locality, adversarial, or rapidly shifting workloads. A future real study must randomize and parameterize workload order rather than generalize from this sequence.

## What evidence supports each conclusion?

- Routing conclusions: 80 observations per method in `raw_results.jsonl`, with multi-label precision, recall, F1, top-1 accuracy, and top-k recall.
- Capacity conclusions: versioned registry declarations and runtime resident sets, explicitly marked simulated for control.
- Latency conclusions: synchronized stage timers for the active backend and p50/p95 aggregates.
- Cache conclusions: structured hits, misses, loads, evictions, and swaps in routing decisions and raw rows.
- Failure conclusions: `routing_failures.md` retains expected/selected experts, scores, confidence, quality, and reason categories.
- Comparability: content hashes, versions, source commit, clean/dirty state, device class, seed policy, and one compatibility fingerprint in the run manifest.
- Real LLM quality or VRAM conclusions: none yet.

## What experiment would falsify the central hypothesis?

Pre-register a held-out multi-domain workload and use a real shared base with independently validated compatible adapters. Under equal decoding settings and a fixed physical accelerator-memory budget, compare base-only, random, keyword, oracle, semantic, cached semantic, all-resident, and conventional offload across repeated seeds and workload orders.

The hypothesis is falsified for that setup if semantic routing does not beat keyword/random on held-out routing, if better routing does not retain task quality against oracle/all-resident, or if loading and transfer overhead removes every useful quality-memory-latency operating point.

## What precedes credible semantic parameter paging?

Dense-model importance units must be causally localized, stable across prompts and generation steps, composable across domains, superior to random/pruning baselines, and aligned with contiguous or structured blocks that real kernels can skip. A learned router must generalize to held-out tasks. Finally, a runtime must demonstrate measured physical memory or compute savings after routing, transfer, and sparse-kernel overhead. Until then, parameter paging remains a research agenda, not an implemented feature.

## Review fixes incorporated

- Expert-cache metrics exclude the pinned base model.
- Oracle routing can exceed the normal declared budget to remain a true upper bound.
- Three-capability prompts preserve all requested labels before budget planning.
- Missing relative controls produce `N/A`, not fabricated zero values.
- The primary plot reports quality retention versus memory reduction.
- Failure reports include candidate scores and budget-related rejection reasons.
- Manifests hash benchmark, registry, and routing content in addition to versions.
- Memory snapshots separate declared base/expert capacity and explicitly mark unavailable tensor/KV/framework attribution.
