# Roadmap

The roadmap is evidence-gated. A milestone is not complete because an interface exists; its stated experiment must run and report limitations.

## v0.1 - Research framework

- Typed analyzer, routers, capacity registry, planner, runtime cache, metrics, and hardware inspection.
- Deterministic-control and Transformers/PEFT backend contract.
- Reproducible mixed-domain hero benchmark with baselines, ablations, failure analysis, reports, and plots.
- CPU-safe CLI, Python API, tests, CI, and research documentation.

## v0.1.1 - First real adapter evidence

- Completed a pinned Qwen2.5/LoRI matrix on Apple M4/MPS.
- Measured real live tensor residency, driver allocation, host RSS, load/eviction latency, composition, and cache locality.
- Preserved the negative result: better routing did not beat random quality, and RLC composition degraded output.

## v0.2 - Expert quality and composition validation

- Pre-register a larger held-out domain suite and a decoding budget that avoids systematic truncation.
- Validate each adapter alone against base before using it in a routing experiment.
- Compare weighted-linear composition with interference-aware alternatives and independent multi-active support.
- Randomize policy order across process-level runs to isolate end-to-end cache latency.
- Add a conventional offload baseline and repeat on CUDA when available.

## v0.3 - Paging and cache policies

- Add an explicit Accelerate CPU/GPU offload baseline with transfer instrumentation.
- Compare LRU, LFU, recency-frequency, and workload-aware prefetching.
- Separate cold start, steady state, and bursty workload regimes.
- Measure KV-cache and framework overhead independently where possible.

## v0.4 - Learned routing and composition

- Train and calibrate a multi-label router on held-out prompts.
- Test expert interference, composition order, and confidence-aware fallback.
- Evaluate workload drift and out-of-distribution routing.

## v0.5 - Activation and importance experiments

- Collect activation traces on dense and modular models.
- Compare neuron, MLP-channel, attention-head, and layer importance across tasks.
- Measure cross-domain overlap, stability across paraphrases, and causal effects of masks.

## v0.6+ - Semantic parameter paging research

- Prototype block layouts and sparse kernels only after localization evidence is strong enough.
- Compare learned masks with pruning, contextual sparsity, MoE, and conventional offloading.
- Demonstrate physical memory reduction and retained quality on held-out tasks before using the term semantic parameter paging for an implementation.
