# Real-model results

Timestamped runs are local artifacts. `latest/` contains the committed v0.1.1 evidence after a completed model-backed run. Model and adapter weights remain in the Hugging Face cache and are never committed here.

The committed run is `20260904T131326Z`, produced by the real `transformers-peft` backend on Apple M4/MPS. Its compatibility fingerprint is `a24ac14e5122d5681ddf091602c57777897c6a637d578ce6407dc8031fe51b03`.

Start with [the report](latest/report.md), then inspect the [manifest](latest/manifest.json), [raw responses](latest/raw_responses.jsonl), [telemetry](latest/telemetry.jsonl), [RLC matrix](latest/rlc_matrix.jsonl), and [failure analysis](latest/failure_analysis.md). The model and adapter weights are external Hugging Face assets pinned by revision in the manifest.
