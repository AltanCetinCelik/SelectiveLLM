# Research questions and hypothesis matrix

## Research questions

**RQ1:** Can semantic routing accurately predict which specialized model capacity a prompt requires?

**RQ2:** How much resident memory can dynamic expert loading save compared with keeping all experts resident?

**RQ3:** What latency penalty is introduced by swapping capacity?

**RQ4:** Under which locality and budget regimes can caching recover that latency?

**RQ5 (future research):** Does task specialization permit useful parameter-level paging inside dense transformers?

## Hypothesis matrix

| Hypothesis | Status | Evidence or falsification |
|---|---|---|
| A semantic router can select independently defined adapters reliably | Testable now | Hero routing precision/recall/F1 versus keyword and random |
| Dynamic adapter loading reduces resident accelerator memory | Requires real backend | Falsified if compatible real runs show no peak-memory reduction versus all-resident |
| Cache reuse reduces swap overhead | Testable now; physical magnitude requires real backend | Mixed-domain repeated workload, cold/warm load latency, hits, and swaps |
| Better routing improves generation quality | Requires real backend for model claim | Oracle/semantic quality versus base, random, and keyword; falsified if routing gains do not transfer to task quality |
| Multi-domain composition retains quality within budget | Partially testable | Three-capability cases, budget rejections, composition compatibility, and quality loss |
| Dense-model knowledge cleanly maps to parameter blocks | Unknown | Future causal localization, mask stability, overlap, and sparse execution experiments |
| 70B-quality can run at 7B memory cost | Unsupported | Not claimed; would require broad quality parity and measured physical memory across representative workloads |

## Central falsification experiment

Use a held-out, pre-registered multi-domain benchmark and a real shared base model with independently validated compatible adapters. Compare semantic, keyword, random, oracle, base-only, all-resident, and standard offload under equal generation settings and a fixed physical memory budget. Repeat across seeds and workload orders.

The central routing hypothesis is falsified for that setup if semantic routing does not improve held-out routing metrics over keyword/random, does not retain quality relative to oracle/all-resident, or incurs enough load and transfer latency that no useful quality-memory-latency operating point remains.

