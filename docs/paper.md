# SelectiveLLM: a living technical report

## Abstract

SelectiveLLM is an experimental inference framework for studying whether model capacity can be treated as a dynamically retrieved resource under a memory constraint. Version 0.1 implements multi-label prompt analysis, semantic and baseline routers, a versioned capacity registry, budget-aware planning, LRU expert lifecycle management, a deterministic methodology-control backend, and a common Transformers/PEFT backend interface. Its hero experiment compares base-only, random, keyword, oracle, semantic, cached, ablated, and all-resident strategies. The initial included measurements are control-backend results and do not establish physical VRAM savings or language-model quality. Parameter-level semantic paging inside arbitrary dense models remains open.

## 1. Introduction

LLM inference commonly keeps a fixed model resident or uses placement policies that move layers and tensors across devices. Conditional-computation models instead train explicit experts and route tokens among them. SelectiveLLM investigates a systems question between these areas: when independently loadable specializations exist, can prompt-level semantic routing request only the useful capacity and manage it under a strict budget?

## 2. Motivation

Keeping many adapters or specialized models resident wastes capacity when workloads exhibit domain locality. Loading on every request reduces residency but can create unacceptable latency. A router and cache may expose an operating point between those extremes. Whether it does is empirical and workload-dependent.

## 3. Related work

The project builds on MoE routing, LoRA and PEFT, Accelerate/DeepSpeed offload, FlexGen, contextual sparsity, pruning, and knowledge localization. [The related-work survey](related_work.md) compares their granularity and claims. The current novelty is a unified, falsifiable benchmark framing rather than a new sparse architecture.

## 4. System design

Prompts pass through a multi-label analyzer, router, budget planner, registry, runtime loader/cache, and backend. Metrics record stage-separated latency and distinct declared, host, and accelerator memory semantics. Control and real backends share the same lifecycle and benchmark contracts. Run fingerprints prevent incompatible evidence from being silently combined.

## 5. Experimental setup

The versioned hero dataset includes 16 single-domain, multi-domain, ambiguous, and irrelevant-domain cases. Required controls include base-only, random, keyword, oracle, all-resident, semantic, and semantic-plus-cache. Ablations vary router family, top-k, threshold, and cache budget. Each observation retains raw routing, quality, runtime, and provenance fields.

## 6. Evaluation

The included deterministic-control experiment contains 80 observations per method. Semantic routing reached 0.633 mean multi-label F1 versus 0.198 keyword and 0.150 random. Its synthetic capability-coverage score was 0.797 versus 0.431 base-only and 1.000 oracle, while using 45.7% less declared peak capacity than all-resident. Caching preserved selection and control quality while serving 30 of 85 expert requests as hits and reducing swaps from 85 to 53 in the repeated mixed-domain order. These are not model-quality or physical-memory results. Consult `results/latest/report.md` for machine-specific timings, confidence summaries, and limitations, and [the hostile review](hostile_review.md) for the evidence boundary.

A publishable real-backend evaluation remains pending compatible, license-reviewed base and adapter assets. It must measure actual accelerator memory, task-specific generation quality, loading/transfers, cold and warm latency, and repeated workload orders.

## 7. Limitations

- The authored benchmark is small and may reflect its taxonomy.
- Feature-hash routing is not a learned semantic encoder.
- Control quality is defined by capability coverage and is therefore not independent model evidence.
- PEFT adapter compatibility and composition vary by architecture and training setup.
- MPS exposes less memory telemetry than CUDA.
- Prompt-level adapter routing is not parameter-level paging.
- The benchmark does not prove that dense-model capabilities are modular.

## 8. Future work

The immediate priority is a pre-registered real adapter study with held-out prompts and task-specific evaluation. Subsequent work should compare cache policies and conventional offload, calibrate a learned router, test composition interference, and collect causal activation/importance evidence before attempting hardware-aligned parameter blocks.

## 9. Conclusion

SelectiveLLM v0.1 provides the machinery to test capacity routing without conflating control evidence with real inference. The central question remains open until real runs demonstrate a useful quality-memory-latency tradeoff. Negative outcomes are valid results and are preserved.
