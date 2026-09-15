# Roadmap

The roadmap is evidence-gated. A milestone is not complete because an interface exists; its stated experiment must run and report limitations.

## v0.1 - Research framework

- Typed analyzer, routers, capacity registry, planner, runtime cache, metrics, and hardware inspection.
- Deterministic-control and Transformers/PEFT backend contract.
- Reproducible mixed-domain hero benchmark with baselines, ablations, failure analysis, reports, and plots.
- CPU-safe CLI, Python API, tests, CI, and research documentation.

## v0.1.1 - First real adapter evidence

- Completed a pinned Qwen2.5/LoRA matrix on Apple M4/MPS.
- Measured real live tensor residency, driver allocation, host RSS, load/eviction latency, composition, and cache locality.
- Preserved the negative result: better routing did not beat random quality, and RLC composition degraded output.

## Completed follow-up - Expert-pool diagnostic

- Completed 108 generations at a fixed 384-token ceiling across base and all three adapters.
- Found empirical-oracle quality 0.748 versus 0.406 base and routing opportunity 0.343 [0.111, 0.611].
- Passed the frozen pool-viability gate, including its post-hoc evaluator sensitivity check.
- Did not establish robust domain specialization: sole labeled-specialist wins were 1/7 and specialist intervals crossed zero.
- Paused router, cache, and composition optimization pending a larger repaired held-out benchmark.

## Completed follow-up - Dense-capacity feasibility

- Completed activation, attention-head, and layer discovery on dense Qwen2.5-1.5B with held-out matched logical ablations: Outcome C.
- Completed objective-aware 64/128-channel block discovery on Qwen2.5-1.5B: Outcome C.
- Repeated the frozen block protocol on Qwen2.5-3B and computed paired scale effects: Outcome C, classification transition C to C.
- Did not measure or claim physical parameter removal, paging, or memory reduction.

## Next controlled evidence

- Repair and enlarge the adapter benchmark before training a learned or empirical router.
- Change one dense-model variable beyond nearby Qwen scale, such as model family or substantially larger scale on appropriate hardware.
- Pre-register any new discovery granularity before inspecting held-out outcomes.
- Preserve the current negative results as immutable controls.

## Systems work after positive evidence

- Add a conventional CPU/GPU offload baseline with transfer instrumentation.
- Compare cache and prefetch policies only for an expert pool with validated quality gains.
- Test composition only after single-expert specialization is established on held-out data.

## Semantic parameter paging research

- Prototype block layouts and sparse kernels only after localization evidence is strong enough.
- Compare learned masks with pruning, contextual sparsity, MoE, and conventional offloading.
- Demonstrate physical memory reduction and retained quality on held-out tasks before using the term semantic parameter paging for an implementation.
