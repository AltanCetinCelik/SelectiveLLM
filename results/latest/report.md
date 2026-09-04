# SelectiveLLM Benchmark Report

**Backend:** `deterministic-control` (`control`)
**Model identity:** `selectivellm-control-v1`
**Benchmark:** `hero-1.0.0`
**Fingerprint:** `3792ea55c906065d90f9a79b15b301169e929817fad7fde76491f9c751a6a34d`
**Device class:** `cpu`

> Deterministic-control results validate routing and benchmark methodology. They do not demonstrate physical VRAM savings or language-model quality.

## Hardware and software

```json
{
  "accelerator": null,
  "accelerator_memory_mb": null,
  "architecture": "arm64",
  "cpu": "arm",
  "cuda_version": null,
  "device": "cpu",
  "device_class": "cpu",
  "git_commit": "e5ccfb62c3c2cfdc2aaf240dd4bcf8fd28202b15",
  "logical_cpus": 10,
  "mps_available": false,
  "os": "Darwin",
  "os_version": "25.5.0",
  "packages": {
    "matplotlib": "3.11.1",
    "numpy": "2.2.6",
    "peft": null,
    "psutil": "7.2.2",
    "pydantic": "2.13.5",
    "selectivellm": "0.1.0",
    "torch": null,
    "transformers": null
  },
  "platform": "macOS-26.5.2-arm64-arm-64bit",
  "python_version": "3.12.14",
  "source_dirty": true,
  "torch_version": null,
  "total_ram_gb": 16.0
}
```

## Methods and results

| Method | n | Quality | Quality retention | Routing F1 | Declared peak MB | Declared reduction | Latency p50 ms | Latency p95 ms | Cache hit rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base_only | 80 | 0.431 | 43.1% | 0.125 | 500.0 | 68.4% | 0.305 | 0.373 | 0.000 |
| random | 80 | 0.514 | 51.4% | 0.150 | 860.0 | 45.6% | 0.978 | 1.098 | 0.000 |
| keyword | 80 | 0.503 | 50.3% | 0.198 | 680.0 | 57.0% | 0.314 | 0.647 | 0.000 |
| oracle | 80 | 1.000 | 100.0% | 1.000 | 1019.8 | 35.5% | 0.940 | 1.278 | 0.000 |
| embedding | 80 | 0.757 | 75.7% | 0.571 | 857.8 | 45.7% | 1.151 | 1.486 | 0.000 |
| semantic_top1 | 80 | 0.764 | 76.4% | 0.594 | 680.0 | 57.0% | 1.176 | 1.268 | 0.000 |
| semantic | 80 | 0.797 | 79.7% | 0.633 | 857.8 | 45.7% | 1.171 | 1.517 | 0.000 |
| semantic_threshold_high | 80 | 0.516 | 51.6% | 0.217 | 842.0 | 46.7% | 0.844 | 1.507 | 0.000 |
| semantic_cache | 80 | 0.797 | 79.7% | 0.633 | 857.8 | 45.7% | 1.161 | 1.339 | 0.312 |
| semantic_cache_small | 80 | 0.764 | 76.4% | 0.594 | 680.0 | 57.0% | 1.148 | 1.296 | 0.312 |
| all_resident | 80 | 0.963 | 96.2% | 0.368 | 1580.0 | 0.0% | 0.321 | 0.367 | 0.988 |

Statistics include count, mean, median, standard deviation, p50, p95, and a normal-approximation 95% confidence interval where more than one observation exists. Case-level observations are not independent repeated training runs; intervals characterize this workload only.

## Plots

![Quality retention versus memory reduction](plots/quality_vs_memory.png)

![Routing accuracy](plots/routing_accuracy.png)

![Latency breakdown](plots/latency_breakdown.png)

![Cache hit rate](plots/cache_hit_rate.png)

![Expert selection matrix](plots/expert_selection_confusion_matrix.png)

## Interpretation

Semantic routing changed the backend-specific quality score by +0.366 relative to base-only. Its mean routing F1 differed from keyword routing by +0.435. Caching changed mean control-backend load time by -0.124 ms (cached minus uncached). These observations support conclusions only for the labeled backend, workload, configuration, and measurement semantics.

## Limitations

- Declared capacity is registry metadata. For the deterministic-control backend it is simulated and is not observed VRAM.
- Control task quality is synthetic capability coverage, not natural-language answer quality.
- Routing performance on this small authored workload may not generalize.
- Wall-clock timings describe this backend and machine; they are not model-loading forecasts.
- A real Transformers/PEFT run is required for physical accelerator-memory and model-quality conclusions.

## Negative-result policy

Null and negative outcomes are retained. The benchmark is not tuned after inspection solely to favor semantic routing.
