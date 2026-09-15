# SelectiveLLM: a living technical report

## Abstract

SelectiveLLM is an experimental inference framework for studying whether model capacity can be treated as a dynamically retrieved resource under a memory constraint. Version 0.1.1 implements multi-label prompt analysis, hostile routers, a versioned capacity registry, budget-aware planning, LRU expert lifecycle management, deterministic control, and real Transformers/PEFT inference. A pinned Apple M4 run demonstrates real adapter residency, loading, composition, and locality-dependent cache behavior, but not a reliable answer-quality gain from better routing. A follow-up expert diagnostic found empirical diversity without robust semantic alignment. Preregistered logical-masking studies of dense Qwen2.5-1.5B and 3B models both returned Outcome C: weak or unstable causal specialization. Parameter-level semantic paging remains open and unimplemented.

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

The included deterministic-control experiment contains 80 observations per method. Semantic routing reached 0.696 mean multi-label F1 versus 0.198 keyword and 0.150 random. Its synthetic capability-coverage score was 0.801 versus 0.431 base-only and 1.000 oracle, while using 45.7% less declared peak capacity than all-resident. Caching preserved selection and control quality while serving 30 of 80 expert requests as hits and reducing swaps from 80 to 48 in the repeated mixed-domain order. These are not model-quality or physical-memory results. Consult `results/latest/report.md` for machine-specific timings, confidence summaries, and limitations, and [the hostile review](hostile_review.md) for the evidence boundary.

Version 0.1.1 adds a real Qwen2.5-1.5B-Instruct experiment with three pinned, same-base LoRA adapters. Across 27 warm observations per policy, semantic routing reached 0.830 F1 versus 0.611 keyword and 0.278 random. Dynamic semantic routing averaged 3125.732 MB MPS live tensor allocation versus 3412.159 MB all-resident. The 286.427 MB difference is a real Apple unified-memory allocator measurement, not simulated capacity or discrete VRAM.

The quality result was negative. Random and oracle both averaged 0.370 fixed-rubric quality; semantic ranged from 0.370 to 0.378. The RLC case scored 0.400 for base and code-only, 0.067 for code-plus-science, and 0.000 for three-expert oracle. A fixed 96-token cap affected 45.8% of warm outputs.

A preregistered 384-token diagnostic then generated base, code, math, and science responses for nine cases with three technical repetitions per cell. Empirical-oracle quality was 0.748 [0.543, 0.933] versus 0.406 [0.156, 0.672] for base, producing routing opportunity 0.343 [0.111, 0.611]. The pool passed its viability gate, but the labeled specialist was the sole empirical winner for only 1/7 labeled cases. A post-hoc evaluator sensitivity audit preserved the broad viability conclusion while confirming evaluator sensitivity. This supports exploitable response diversity, not robust domain specialization.

The dense-capacity milestone removed adapters entirely. Discovery statistics were computed on 48 questions and fixed masks were causally tested on 32 held-out questions using correct-answer NLL. At the primary 64-channel granularity, Qwen2.5-1.5B had gradient stability in 0/4 domains and Qwen2.5-3B had 1/4. Both failed the frozen A/B gates and were classified C. The 3B same-domain damage point estimate increased to 1.3016 [-0.0077, 2.9763], but matched-control intervals crossed zero and stability remained insufficient. The paired classification transition was C to C. These experiments used logical masking only and measured no memory reduction.

Consult the [complete real analysis](real_model_evidence.md), [expert diagnostic](../results/real/expert_quality/latest/report.md), [1.5B causal report](../results/real/causal_importance/latest/report.md), [3B causal report](../results/real/causal_scale_qwen3b/latest/report.md), and [hostile review](hostile_review.md).

## 7. Limitations

- The authored benchmark is small and may reflect its taxonomy.
- Feature-hash routing is not a learned semantic encoder.
- Control quality is defined by capability coverage and is therefore not independent model evidence.
- The adapter studies contain only nine authored cases; the original policy matrix used sequential order and substantial response truncation.
- PEFT weighted-linear composition allocated derived state and degraded the multi-domain hero response.
- MPS exposes less memory telemetry than CUDA.
- Prompt-level adapter routing is not parameter-level paging.
- The dense studies contain 32 held-out questions per model, highly skewed effects, and weak discovery stability.
- Logical masking does not prove physical block independence, routability, or memory savings.

## 8. Future work

The LoRA line should next use a larger, repaired held-out benchmark before learned or empirical routing is optimized. The dense line should stop nearby same-family scale escalation on this machine and change one controlled variable, such as model family or substantially larger scale on suitable hardware, under a new preregistration. Physical paging work remains gated on stable, domain-specific causal evidence.

## 9. Conclusion

SelectiveLLM v0.1.1 shows that independently defined adapter capacity can be retrieved and managed with a measurable live-memory/cache tradeoff on real hardware. The follow-up diagnostic found a pool with empirical upside but weak semantic alignment. Neither the 1.5B nor the 3B dense logical-masking experiment found stable causal specialization under its frozen gate. The systems mechanism works; quality-aware semantic routing and dense parameter paging remain unproven.
