"""Reports and plots for completed real-model validation runs."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from selectivellm.metrics import aggregate

METRICS = (
    "quality",
    "quality_delta_base",
    "quality_delta_oracle",
    "routing_precision",
    "routing_recall",
    "routing_f1",
    "false_activations",
    "routing_ms",
    "planning_ms",
    "loading_ms",
    "unloading_ms",
    "activation_ms",
    "synchronization_ms",
    "first_token_ms",
    "generation_ms",
    "end_to_end_ms",
    "tokens_per_second",
    "cache_hit_rate",
    "adapter_loads",
    "adapter_evictions",
    "resident_adapter_count",
    "active_adapter_count",
    "host_rss_before_generation_mb",
    "mps_current_before_generation_mb",
    "mps_current_peak_generation_mb",
    "mps_driver_before_generation_mb",
    "mps_driver_peak_generation_mb",
)


def summarize(rows: list[dict[str, Any]], manifest: dict[str, Any]) -> dict[str, Any]:
    policies = sorted({row["policy"] for row in rows})

    def group(phase: str | None) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for policy in policies:
            observations = [
                row
                for row in rows
                if row["policy"] == policy and (phase is None or row["phase"] == phase)
            ]
            output[policy] = {
                metric: aggregate(
                    [float(row[metric]) for row in observations if row.get(metric) is not None]
                ).model_dump(mode="json")
                for metric in METRICS
            }
        return output

    return {
        "run_id": manifest["run_id"],
        "backend": manifest["backend"],
        "backend_kind": "real",
        "benchmark_fingerprint": manifest["benchmark_fingerprint"],
        "quality_semantics": "fixed_deterministic_rubric",
        "methods": group(None),
        "warm_methods": group("warm"),
    }


def write_summary_csv(summary: dict[str, Any], path: Path) -> None:
    rows: list[dict[str, Any]] = []
    for phase_key in ("methods", "warm_methods"):
        for policy, metrics in summary[phase_key].items():
            row: dict[str, Any] = {"phase": phase_key, "policy": policy}
            for metric, stats in metrics.items():
                for name, value in stats.items():
                    row[f"{metric}_{name}"] = value
            rows.append(row)
    columns = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _mean(summary: dict[str, Any], policy: str, metric: str) -> float:
    value = summary["warm_methods"][policy][metric]["mean"]
    return float(value) if value is not None else 0.0


def _format_mean(metrics: dict[str, Any], key: str) -> str:
    value = metrics[key]["mean"]
    return "N/A" if value is None else f"{value:.3f}"


def generate_plots(summary: dict[str, Any], plots: Path) -> None:
    plots.mkdir(parents=True, exist_ok=True)
    policies = list(summary["warm_methods"])
    labels = [item.replace("semantic_", "sem ").replace("_", " ") for item in policies]
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, axis = plt.subplots(figsize=(13, 6))
    quality = [_mean(summary, item, "quality") for item in policies]
    axis.bar(labels, quality, color="#247BA0")
    axis.set_ylim(0, 1.05)
    axis.set_ylabel("Mean fixed-rubric quality")
    axis.set_title(
        "Real model response quality by policy\nQwen2.5-1.5B-Instruct + pinned LoRI adapters"
    )
    axis.tick_params(axis="x", rotation=28)
    fig.tight_layout()
    fig.savefig(plots / "real_quality.png", dpi=180)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(13, 6))
    routing = [_mean(summary, item, "routing_f1") for item in policies]
    axis.bar(labels, routing, color="#70C1B3")
    axis.set_ylim(0, 1.05)
    axis.set_ylabel("Mean multi-label routing F1")
    axis.set_title("Routing quality on the real-model workload")
    axis.tick_params(axis="x", rotation=28)
    fig.tight_layout()
    fig.savefig(plots / "real_routing.png", dpi=180)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(13, 6))
    live = [_mean(summary, item, "mps_current_before_generation_mb") for item in policies]
    peak = [_mean(summary, item, "mps_current_peak_generation_mb") for item in policies]
    x = np.arange(len(policies))
    width = 0.38
    axis.bar(x - width / 2, live, width, label="MPS live before generation", color="#247BA0")
    axis.bar(x + width / 2, peak, width, label="MPS sampled generation peak", color="#FF7B6B")
    axis.set_ylabel("MPS current tensor allocation (MB), not VRAM")
    axis.set_title("Observed live tensor allocation")
    axis.set_xticks(x, labels, rotation=28)
    axis.legend()
    fig.tight_layout()
    fig.savefig(plots / "real_mps_live_memory.png", dpi=180)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(13, 6))
    stages = ("routing_ms", "planning_ms", "loading_ms", "activation_ms", "generation_ms")
    stage_labels = ("Route", "Plan", "Load", "Activate", "Generate")
    colors = ("#247BA0", "#70C1B3", "#F3C677", "#A78BFA", "#FF7B6B")
    bottom = np.zeros(len(policies))
    for metric, label, color in zip(stages, stage_labels, colors, strict=True):
        values = np.array([_mean(summary, item, metric) for item in policies])
        axis.bar(labels, values, bottom=bottom, label=label, color=color)
        bottom += values
    axis.set_ylabel("Synchronized mean latency (ms)")
    axis.set_title("Real inference latency breakdown")
    axis.tick_params(axis="x", rotation=28)
    axis.legend()
    fig.tight_layout()
    fig.savefig(plots / "real_latency.png", dpi=180)
    plt.close(fig)

    cache_policies = [item for item in policies if item.startswith("semantic_cache")]
    fig, axis = plt.subplots(figsize=(11, 6))
    hits = [_mean(summary, item, "cache_hit_rate") for item in cache_policies]
    loads = [_mean(summary, item, "adapter_loads") for item in cache_policies]
    x = np.arange(len(cache_policies))
    axis.bar(x - 0.2, hits, 0.4, label="Hit rate", color="#70C1B3")
    second = axis.twinx()
    second.bar(x + 0.2, loads, 0.4, label="Loads/request", color="#FF7B6B")
    axis.set_ylim(0, 1.05)
    axis.set_ylabel("Cache hit rate")
    second.set_ylabel("Adapter loads per request")
    axis.set_xticks(
        x, [item.replace("semantic_", "").replace("_", " ") for item in cache_policies], rotation=20
    )
    axis.set_title("Cache locality and capacity")
    handles, names = axis.get_legend_handles_labels()
    handles2, names2 = second.get_legend_handles_labels()
    axis.legend(handles + handles2, names + names2, loc="upper right")
    fig.tight_layout()
    fig.savefig(plots / "real_cache.png", dpi=180)
    plt.close(fig)


def write_report(summary: dict[str, Any], manifest: dict[str, Any], path: Path) -> None:
    lines = [
        "# SelectiveLLM v0.1.1 Real-Model Report",
        "",
        f"**Backend:** `{manifest['backend']}` (`real`)",
        f"**Base:** `{manifest['model_identity']}` at `{manifest['model_revision']}`",
        f"**Device:** `{manifest['device']['accelerator']}` / `{manifest['device']['device_class']}`",
        f"**Benchmark:** `{manifest['benchmark_version']}`",
        f"**Fingerprint:** `{manifest['benchmark_fingerprint']}`",
        "",
        "> MPS current allocation, MPS driver allocation, and host RSS are separate unified-memory signals. None is labeled discrete VRAM.",
        "",
        "## Warm repeated workload",
        "",
        "| Policy | n | Quality | vs base | vs oracle | Routing F1 | MPS live MB | Driver MB | Load ms | First token ms | End-to-end ms | Hit rate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for policy, metrics in summary["warm_methods"].items():
        lines.append(
            f"| {policy} | {metrics['quality']['count']} | {_format_mean(metrics, 'quality')} | {_format_mean(metrics, 'quality_delta_base')} | {_format_mean(metrics, 'quality_delta_oracle')} | {_format_mean(metrics, 'routing_f1')} | {_format_mean(metrics, 'mps_current_before_generation_mb')} | {_format_mean(metrics, 'mps_driver_before_generation_mb')} | {_format_mean(metrics, 'loading_ms')} | {_format_mean(metrics, 'first_token_ms')} | {_format_mean(metrics, 'end_to_end_ms')} | {_format_mean(metrics, 'cache_hit_rate')} |"
        )
    lines.extend(
        [
            "",
            "Cold-workload observations and full variability statistics are retained in `summary.json` and `summary.csv`; the table above does not pool them with warm repetitions.",
            "",
            "## Plots",
            "",
            "![Real quality](plots/real_quality.png)",
            "",
            "![MPS live memory](plots/real_mps_live_memory.png)",
            "",
            "![Real latency](plots/real_latency.png)",
            "",
            "![Real routing](plots/real_routing.png)",
            "",
            "![Cache behavior](plots/real_cache.png)",
            "",
            "## Measurement boundaries",
            "",
            "- Quality is a fixed deterministic rubric, not synthetic routing coverage and not an LLM judge.",
            "- All-resident means all adapter tensors were loaded; active adapters are recorded separately.",
            "- MPS live tensor allocation excludes allocator caches. Metal driver allocation includes caches and framework allocations.",
            "- Host RSS overlaps conceptually with accelerator use on Apple unified memory and must not be added to MPS figures.",
            "- Generation peaks are sampled because MPS exposes no CUDA-equivalent peak allocator counter.",
            "- Negative and adapter-degraded results are retained.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
