# Real-model results

Timestamped runs are local artifacts. `latest/` contains the committed v0.1.1 evidence after a completed model-backed run. Model and adapter weights remain in the Hugging Face cache and are never committed here.

The committed run is `20260904T131326Z`, produced by the real `transformers-peft` backend on Apple M4/MPS. Its compatibility fingerprint is `a24ac14e5122d5681ddf091602c57777897c6a637d578ce6407dc8031fe51b03`.

Start with [the report](latest/report.md), then inspect the [manifest](latest/manifest.json), [raw responses](latest/raw_responses.jsonl), [telemetry](latest/telemetry.jsonl), [RLC matrix](latest/rlc_matrix.jsonl), and [failure analysis](latest/failure_analysis.md). The model and adapter weights are external Hugging Face assets pinned by revision in the manifest.

Follow-up evidence is published separately so incompatible experiments cannot be
mistaken for one benchmark series:

- [Expert-pool diagnostic](expert_quality/latest/report.md): 108 real generations;
  viable empirical diversity, weak semantic alignment.
- [Dense-capacity feasibility](dense_capacity/latest/report.md): activation,
  attention-head, and layer logical interventions on Qwen2.5-1.5B; Outcome C.
- [Objective-aware 1.5B study](causal_importance/latest/report.md): contiguous MLP
  block discovery and held-out ablation; Outcome C.
- [Qwen2.5-3B scale replication](causal_scale_qwen3b/latest/report.md): strict
  same-family replication and paired scale comparison; Outcome C.

The dense studies do not unload parameters and make no memory-reduction claim.
