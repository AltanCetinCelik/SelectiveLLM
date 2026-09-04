# SelectiveLLM

**Semantic Model Paging and Dynamic Expert Routing for Memory-Constrained LLM Inference**

SelectiveLLM is an experimental framework for studying retrieval over model capacity. The v0.1 implementation compares independently defined expert selection and caching strategies under a declared memory budget.

SelectiveLLM does NOT currently turn a dense 70B model into a 7B-memory model.

The default offline backend is a deterministic benchmark control. Its declared expert capacity is simulated and is not evidence of physical VRAM savings or language-model quality. Real Transformers and PEFT experiments use the same backend contract and benchmark methodology when compatible model and adapter paths are supplied.

Full project documentation and verified benchmark results are added after the implementation and validation stages are complete.
