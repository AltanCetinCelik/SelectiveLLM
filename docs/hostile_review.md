# Hostile review of v0.1.1

This review leads with the completed real-model run in `results/real/latest`. Its compatibility fingerprint is `a24ac14e5122d5681ddf091602c57777897c6a637d578ce6407dc8031fe51b03`. The deterministic-control run remains separate in `results/latest` and is never used as physical-memory or model-quality evidence.

## Is this merely adapter routing?

At v0.1.1, yes: the real test vehicle is prompt-level routing over three independently trained LoRA adapters. SelectiveLLM does not claim that adapter routing itself is novel. The contribution under test is a backend-independent systems methodology joining multi-label selection, residency budgets, lifecycle/cache control, hostile baselines, separated memory semantics, versioned validity guards, and failure-preserving reports.

That broader framing has not yet produced evidence for retrieval over arbitrary dense-model parameters. Calling the current implementation semantic parameter paging would be false.

## Is this merely Mixture-of-Experts?

It overlaps with conditional computation but is not a trained token-level MoE architecture. The adapters were trained independently, whole prompts are routed before generation, capacity can be loaded or evicted between requests, and transfer/lifecycle costs are included. There is no MoE layer, token gate, expert load-balancing objective, or claim about MoE training.

The closest honest description is a model-backed prompt-level adapter-routing and residency experiment.

## Is the memory reduction real or simulated?

Both kinds of evidence exist and are labeled separately.

- `results/latest` is deterministic control. Its capacity reduction is simulated registry metadata. Accelerator memory is unavailable.
- `results/real/latest` is real Qwen/PEFT inference on Apple M4. The base occupied 2968.777 MB of MPS current live tensor allocation. All three source adapters raised the lifecycle checkpoint to 3396.121 MB, an actual 427.344 MB increase.
- During warm generation, dynamic semantic cache-0 averaged 3125.732 MB versus 3412.159 MB all-resident, 286.427 MB lower. This is a real MPS live-tensor difference in Apple unified memory, not declared capacity and not discrete VRAM.
- Metal driver allocation and host RSS are retained separately. Driver allocation stayed high after eviction because it includes allocator cache and framework memory. Host RSS overlaps conceptually with MPS and cannot be added to it.

## Does better routing actually improve output quality?

Not reliably in this run. The semantic hybrid reached 0.830 routing F1 versus 0.611 keyword and 0.278 random, but random and oracle both averaged 0.370 quality. Semantic policies averaged 0.370 to 0.378, with broadly overlapping descriptive intervals.

Oracle specialization improved binary search, MOSFET, RC filter, and proof responses relative to base. It tied base on several cases and reduced RLC quality from 0.400 to 0.000. The aggregate routing-quality gain therefore did not establish a causal output-quality gain.

The fixed 96-token cap reached 45.8% of warm responses and often truncated the dice answer before its exact fraction. The score remains reproducible under the registered contract, but a longer-decoding replication is required before judging adapter specialization cleanly.

## What happens when prompts require multiple experts?

The analyzer and router preserve multiple labels. Semantic routing selected code plus science for the RLC prompt and missed math under the configured two-expert limit. PEFT direct list activation was unsupported, so the backend constructed a weighted-linear derived adapter from compatible source adapters.

Composition worked technically but failed the quality test: base and code-only scored 0.400; code plus science and semantic scored 0.067; three-source oracle scored 0.000. Two-source composition also averaged 1279.9 ms activation and created roughly another adapter-sized live allocation. Multi-source residency and multi-active composition remain distinct throughout the artifacts.

## What is the latency cost of swapping?

Across warm load events, code averaged 899.1 ms, math 793.9 ms, and science 925.2 ms. Unloads averaged 114.5 to 120.0 ms. Dynamic semantic cache-0 paid 796.9 ms mean load time per prompt in the low-locality order and 1086.2 ms in the high-locality run.

Single-adapter activation averaged 10.3 ms. Weighted composition was much more expensive: 1279.9 ms for two sources and 1547.2 ms for three. Generation still dominated end-to-end latency.

## Under what workload does caching actually help?

With cache size 1, the high-locality order produced a 55.6% request hit rate, reduced loads and evictions from 27 to 12, and recovered 564.7 ms of mean load-stage work per prompt. The adversarial low-locality order produced only 11.1% hits, reduced loads from 27 to 24, and recovered 41.1 ms.

Cache size 3 reached 100% warm hits and zero warm loads, but it retained all source adapters and therefore gave up the residency benefit. Caching helps when reuse occurs before eviction and capacity remains below the full pool. This run cannot assign all end-to-end latency differences to caching because policy order was not counterbalanced and process-level MPS state persisted.

## What evidence supports each conclusion?

- Compatibility: exact model, tokenizer, adapter revisions, licenses, base identity, rank, alpha, target modules, file size, and hashes in `compatibility_report.json`.
- Comparability: benchmark, registry, evaluation, metric, router, runtime, package, platform, device, and asset inputs in `manifest.json` and the fingerprint payload.
- Quality: every raw response plus its fixed evaluator output in `raw_responses.jsonl` and `evaluation_outputs.jsonl`.
- Routing: expected/selected sets, scores, confidence, candidates, and lifecycle events in `routing_decisions.jsonl`.
- Memory: consistent process/base/load/pre-generation/post-generation/eviction/cleanup checkpoints in `telemetry.jsonl`, plus per-observation values in `raw_results.jsonl`.
- Cache and latency: request hits/misses, loads, evictions, stage timings, synchronization, first token, generation, and throughput in raw results and `summary.json`.
- Multi-domain behavior: 18 preserved observations in `rlc_matrix.jsonl`.
- Negative evidence: misroutes, unnecessary activation, no-improvement cases, oracle regressions, random wins, low confidence, and token-cap diagnostics in `failure_analysis.md`.

## What experiment would falsify the central hypothesis?

Pre-register a larger held-out task suite and first prove that each expert beats the base on its own domain under an adequate decoding budget. Then compare base, random, keyword, oracle, semantic, cached semantic, and all-resident under a fixed physical memory budget, randomized policy order, multiple process-level runs, and identical decoding.

The hypothesis is falsified for that adapter family and workload if semantic routing does not beat random/keyword on held-out routing, oracle capacity does not improve quality over base/random, or loading and composition overhead removes every useful quality-memory-latency operating point. The current run already fails the quality portion, but its small authored suite and truncation rate prevent a broad family-level conclusion.

## What must precede credible semantic parameter paging?

1. Independently validated specialization must yield repeatable quality gains under correct routing.
2. Multi-capability composition must preserve those gains without adapter-sized derived-state overhead dominating the budget.
3. A learned router must generalize on held-out and out-of-distribution prompts and calibrate no-specialist decisions.
4. Dense-model importance units must be causally localized and stable across prompts, paraphrases, and generation steps.
5. Selected units must map to hardware-efficient contiguous or structured blocks and beat random, pruning, MoE, and conventional offload baselines.
6. Physical memory or compute savings must survive routing, transfer, cache, and sparse-kernel overhead.

Until those gates pass, parameter paging is a research agenda.

## Review fixes incorporated

- Registry and metric-schema content now participate in the real-run fingerprint, and the exact benchmark/registry inputs are archived.
- Cache hit rate is weighted over actual expert requests, excluding prompts that requested no adapter.
- Failure analysis now records low-confidence and token-cap diagnostics, candidate scores, evaluator details, and completed-but-degraded RLC composition.
- Completed run directories no longer publish redundant partial checkpoints.
- README and release documentation state the negative quality result before future-looking claims.
- The recommended next step changed from finer-grained routing to expert-quality validation and composition diagnosis.
