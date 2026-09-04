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

## Adjacent systems

Quantization, sharding, speculative decoding, model composition, KV-cache management, [llama.cpp memory mapping](https://github.com/ggml-org/llama.cpp), MLX, vLLM, ExLlamaV2, and TensorRT-LLM can complement selective routing. They are not implemented by v0.1 merely because the registry can name future backend types. A credible comparison should combine or contrast them under matching models, workloads, and measurement semantics.
