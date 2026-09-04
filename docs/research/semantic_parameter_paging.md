# Semantic parameter paging

## Status

Semantic parameter paging is a research direction, not a v0.1 implementation. The current system routes independently defined adapters or experts. It does not discover or page semantic regions of arbitrary dense checkpoints.

## Candidate workflow

1. Collect layer-by-layer activation traces across pre-registered domains, tasks, paraphrases, and controls.
2. Estimate causal importance for neurons, MLP channels, attention heads, layers, and hardware-friendly weight blocks.
3. Cluster importance patterns and measure overlap, stability, and complementarity across domains.
4. Construct sparse masks with explicit resident and transfer costs.
5. Evaluate quality under masks against the dense model, magnitude pruning, contextual sparsity, and random masks.
6. Map stable masks to block layouts that kernels can skip or page efficiently.
7. Train a prompt- or activation-conditioned router without leaking evaluation labels.
8. Measure physical accelerator memory, transfers, latency, throughput, and quality under realistic request sequences.

## Evidence required before viability

- **Localization:** held-out tasks consistently use distinguishable capacity beyond noise and prompt wording.
- **Causality:** removing predicted-irrelevant blocks preserves quality, while removing predicted-relevant blocks degrades it.
- **Stability:** masks remain useful across paraphrases, sequence positions, generation steps, and model checkpoints.
- **Composability:** multi-domain masks can be combined without destructive interference or unbounded growth.
- **Hardware alignment:** selected units map to contiguous or structured blocks that real kernels and memory systems can skip.
- **Amortization:** routing and transfer overhead is smaller than the memory or compute benefit under target workloads.
- **Generalization:** learned selection works on held-out domains and does not merely memorize benchmark prompts.
- **Safety:** paging does not selectively remove alignment, uncertainty, or refusal behavior in unpredictable ways.

## Why knowledge localization is insufficient by itself

Correlating a neuron with factual expression does not establish that a compact, independent semantic module exists. Features can be polysemantic, distributed, redundant, layer-dependent, and causally entangled. Even a good mask may reduce FLOPs without reducing physical memory if hardware still fetches dense blocks.

## Proposed interfaces

A future `future_parameter_shard` registry entry may describe block coordinates, layout, mask provenance, dependency graph, measured size, compatible kernel, and model hash. Backends must reject this type until they implement genuine sparse execution and placement. Adapter lifecycle code must not be relabeled as parameter paging.

## Go/no-go criterion

Proceed to a paging prototype only after importance masks beat matched random and pruning baselines on held-out tasks, remain stable enough to route, and align with a block-sparse layout whose physical memory and latency can be measured. Otherwise, adapter/expert routing remains the honest scope.

