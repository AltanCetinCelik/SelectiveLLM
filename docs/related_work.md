# Related work

SelectiveLLM does not claim that its individual building blocks are new. The closest work spans conditional computation, parameter-efficient adaptation, heterogeneous memory, sparsity, and knowledge localization.

| Technique | What it saves | Routing granularity | Requires training? | Relation to SelectiveLLM |
|---|---|---|---|---|
| [Switch Transformers](https://arxiv.org/abs/2101.03961) | Compute per token relative to total parameter count | Token to one trained expert | Yes | Closest sparse-expert ancestor; experts are architectural and trained together |
| [Expert Choice routing](https://arxiv.org/abs/2202.09368) | Sparse compute with controlled expert capacity | Expert selects token buckets | Yes | Shows routing direction and load balance matter; v0.1 routes prompts to loadable modules |
| [LoRA](https://arxiv.org/abs/2106.09685) | Trainable parameters and optimizer state | Low-rank updates within layers | Yes | Provides the lightweight specialization used as v0.1's real test vehicle |
| [Hugging Face PEFT](https://huggingface.co/docs/transformers/peft) | Adapter storage/training state; supports switching | Named adapters | Yes | Supplies real adapter lifecycle operations; SelectiveLLM adds semantic planning and benchmark controls |
| [Accelerate Big Model Inference](https://huggingface.co/docs/accelerate/usage_guides/big_modeling) | Accelerator residency through CPU/disk offload | Layer/submodule device map | No additional training | Required conventional offload baseline; selection is placement-based, not semantic |
| [DeepSpeed Inference](https://www.deepspeed.ai/inference/) | Per-device memory and latency through parallelism, kernels, quantization | Model partitions/kernels | Usually no | Production systems baseline, especially for multi-GPU inference |
| [FlexGen](https://arxiv.org/abs/2303.06865) | GPU memory through GPU/CPU/disk scheduling | Tensors/layers and cache | No | Demonstrates optimized heterogeneous paging; targets throughput, not semantic expert choice |
| [SparseGPT](https://arxiv.org/abs/2301.00774) | Weight count/storage and potential sparse compute | Individual or semi-structured weights | Calibration, no retraining | Static compression baseline rather than prompt-conditioned selection |
| [DejaVu contextual sparsity](https://arxiv.org/abs/2310.17157) | Inference compute via predicted contextual sparsity | Attention heads and MLP parameters per layer | Predictor training | Closest parameter-level dynamic sparsity direction; stronger evidence than v0.1 adapters |
| [Mixture-of-Depths](https://arxiv.org/abs/2404.02258) | FLOPs by selecting token participation per layer | Token/layer depth | Yes | Dynamically allocates compute, not model storage, but informs budgeted routing |
| [Knowledge Neurons](https://arxiv.org/abs/2104.08696) | Primarily interpretability/editing, not deployment memory | Attributed neurons for facts | Attribution procedure | Motivates localization questions but does not prove page-ready semantic blocks |

## What is actually new here?

In v0.1, the contribution is the unified experimental framing and measurement harness, not a proven new routing algorithm. SelectiveLLM asks whether independently defined capacity can be selected as a retrieved resource under a memory budget and requires the answer to be compared against hostile baselines with backend-specific evidence.

It differs from traditional RAG because it selects model components rather than documents. It overlaps with MoE but does not require a jointly trained sparse architecture or token-level gating. It overlaps most directly with adapter routing in v0.1; adapters are deliberately the first measurable proxy for the broader hypothesis. It differs from conventional offloading because semantic relevance influences which capacity is requested, while placement and eviction remain systems concerns.

## Model and capacity routing systems

SelectiveLLM also overlaps with model-routing and semantic-routing systems, but differs in its primary abstraction.

### RouteLLM

RouteLLM studies request-level routing between language models, typically choosing between stronger and weaker models to optimize cost and quality.

Its primary decision is:

```text
request -> which model?
```

SelectiveLLM treats model selection as one possible form of a broader capacity-selection problem:

```text
request
    ->
which model?
which adapter?
which expert?
how much capacity?
what should remain resident?
```

### Semantic Router

Semantic routing systems map requests to routes, tools, models, or workflows using semantic similarity or learned decision layers.

SelectiveLLM can use semantic routing as a controller, but routing itself is not the complete system.

The framework additionally models:

- capacity dependencies,
- memory constraints,
- loading and unloading,
- cache residency,
- transfer latency,
- rejected relevant capacity,
- backend-specific memory telemetry.

### Adapter routing

Adapter-routing systems choose specialized PEFT or LoRA modules for a request.

SelectiveLLM v0.1 uses adapters for exactly this reason: they are independently loadable capacity units that make runtime selection measurable.

However, adapter routing is treated as the first experimental proxy rather than the final scope of the project.

### SelectLLM

SelectLLM and similarly named model-selection work focus on choosing subsets of independent language models or outputs.

SelectiveLLM instead focuses on **runtime model-capacity selection and residency management**.

The distinction is:

```text
model selection:
request -> choose model

SelectiveLLM:
request -> choose and manage capacity under runtime constraints
```

## Positioning

SelectiveLLM does not claim that semantic routing, adapter routing, Mixture-of-Experts, model selection, or conditional computation are individually new.

Its research framing is:

> Treat independently selectable model capacity as a budgeted runtime resource.

The framework evaluates that capacity across:

```text
relevance
quality
memory
load latency
cache locality
runtime residency
uncertainty
```

The longer-term research question is whether this abstraction can eventually extend from adapters and models to useful internal model capacity.

## Adjacent systems

Quantization, sharding, speculative decoding, model composition, KV-cache management, [llama.cpp memory mapping](https://github.com/ggml-org/llama.cpp), MLX, vLLM, ExLlamaV2, and TensorRT-LLM can complement selective routing. They are not implemented by v0.1 merely because the registry can name future backend types. A credible comparison should combine or contrast them under matching models, workloads, and measurement semantics.
