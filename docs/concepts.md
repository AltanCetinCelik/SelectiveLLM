# Concepts and scientific framing

## The hypothesis

SelectiveLLM studies whether model capacity can be treated as a dynamically retrieved resource under a strict memory budget.

The primary hypothesis is that many requests do not require every independently available specialization to be resident or active simultaneously. The secondary hypothesis is that, when capability has been decomposed into sufficiently independent reusable components, a router can select a useful subset under a memory constraint.

The major open problem is that knowledge and reasoning in dense transformers are highly distributed. Semantic concepts may not map cleanly to contiguous weights, neurons, heads, channels, or layers. SelectiveLLM v0.1 therefore uses adapters and expert modules as an experimentally tractable proxy. Follow-up logical-masking studies tested dense internal components directly but failed their frozen stable-causal-specialization gates. The project does not claim that arbitrary dense checkpoints can be split by domain.

## Retrieval over model capacity

Traditional retrieval-augmented generation retrieves external context and then runs a model. SelectiveLLM retrieves a capacity plan: which independently loadable modules should participate, where they should reside, and which components should be evicted under budget.

This description is conceptual. The retrieved object in v0.1 is registry-defined expert capacity, not hidden knowledge extracted from a dense network.

## Evidence levels

| Level | Meaning | v0.1 example |
|---|---|---|
| Established technique | Demonstrated in prior work | LoRA, MoE routing, CPU/GPU offload |
| Implemented experiment | Executable and measured here | Multi-label routing and declared-capacity LRU caching |
| Hypothesis | Falsifiable but not yet established | Semantic routing can retain real-model quality under a tighter resident-memory budget |
| Feasibility experiment | Real dense model, logical masking only | Qwen2.5-1.5B and 3B causal studies; both Outcome C |
| Future research | Requires positive causal evidence and new systems engineering | Physical prompt-conditioned paging of parameter blocks inside a dense transformer |

## What v0.1 measures

The deterministic-control backend tests methodology and component behavior. Its capacity values are registry declarations, its quality metric is synthetic capability coverage, and its timings are real wall-clock measurements of the control implementation. These quantities are useful for validating the experiment pipeline, not for making claims about LLM quality or physical VRAM.

The Transformers/PEFT backend uses the same engine and benchmark runner. A real run can measure host and accelerator memory where the platform exposes them and can evaluate generated text against references. Such evidence remains specific to the selected base model, adapters, device, workload, and measurement semantics.

## Negative results

A null result is informative. The central hypothesis is weakened when semantic routing fails to beat simple baselines, when better routing does not improve output quality, or when transfer and loading latency erases the value of lower resident capacity. These outcomes are preserved in raw observations and failure reports; benchmark cases are not edited after inspection merely to improve the headline.
