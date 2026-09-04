"""Markdown, CSV, and scientific plot generation for completed runs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

METHOD_LABELS = {
    "base_only": "base",
    "random": "random",
    "keyword": "keyword",
    "oracle": "oracle",
    "embedding": "embedding",
    "semantic_top1": "semantic top-1",
    "semantic": "semantic",
    "semantic_threshold_high": "high threshold",
    "semantic_cache": "semantic + cache",
    "semantic_cache_small": "small cache",
    "all_resident": "all resident",
}

QUALITY_LABEL_OFFSETS = {
    "semantic": (6, 10),
    "semantic_top1": (6, 10),
    "embedding": (6, -10),
    "random": (6, -16),
    "semantic_threshold_high": (6, 10),
}

QUALITY_LABELS = {
    "semantic": "semantic / semantic + cache",
    "semantic_top1": "semantic top-1 / small cache",
}

QUALITY_LABEL_SKIPS = {"semantic_cache", "semantic_cache_small"}


def write_summary_csv(summary: dict[str, Any], path: Path) -> None:
    rows: list[dict[str, Any]] = []
    for method, metrics in summary["methods"].items():
        row: dict[str, Any] = {
            "backend": summary["backend"],
            "backend_kind": summary["backend_kind"],
            "method": method,
        }
        for metric, stats in metrics.items():
            if isinstance(stats, dict) and "count" in stats:
                for name, value in stats.items():
                    row[f"{metric}_{name}"] = value
            else:
                row[metric] = stats
        rows.append(row)
    columns = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def _mean(summary: dict[str, Any], method: str, metric: str) -> float:
    value = summary["methods"][method][metric]["mean"]
    return float(value) if value is not None else 0.0


def generate_plots(summary: dict[str, Any], rows: list[dict[str, Any]], plots: Path) -> None:
    plots.mkdir(parents=True, exist_ok=True)
    methods = list(summary["methods"])
    label = f"Backend: {summary['backend']} ({summary['backend_kind']})"
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, axis = plt.subplots(figsize=(10, 6))
    memory_metric = (
        "accelerator_memory_reduction"
        if any(
            summary["methods"][method]["accelerator_memory_reduction"]["count"] > 0
            for method in methods
        )
        else "declared_memory_reduction"
    )
    plotted = 0
    for method in methods:
        if (
            summary["methods"][method][memory_metric]["count"] == 0
            or summary["methods"][method]["quality_retention"]["count"] == 0
        ):
            continue
        x = 100 * _mean(summary, method, memory_metric)
        y = 100 * _mean(summary, method, "quality_retention")
        axis.scatter(x, y, s=70)
        if method not in QUALITY_LABEL_SKIPS:
            axis.annotate(
                QUALITY_LABELS.get(method, METHOD_LABELS.get(method, method)),
                (x, y),
                xytext=QUALITY_LABEL_OFFSETS.get(method, (6, 6)),
                textcoords="offset points",
                fontsize=8,
            )
        plotted += 1
    if plotted == 0:
        axis.text(
            0.5,
            0.5,
            "Unavailable: include oracle and all_resident controls",
            ha="center",
            va="center",
            transform=axis.transAxes,
        )
    axis.set_xlabel(
        "Observed accelerator-memory reduction vs all-resident (%)"
        if memory_metric == "accelerator_memory_reduction"
        else "Declared-capacity reduction vs all-resident (%; simulated for control)"
    )
    axis.set_ylabel("Quality retention vs oracle (%)")
    axis.set_title(f"Quality retention vs memory reduction\n{label}")
    fig.tight_layout()
    fig.savefig(plots / "quality_vs_memory.png", dpi=180)
    plt.close(fig)

    display_methods = [METHOD_LABELS.get(method, method) for method in methods]
    fig, axis = plt.subplots(figsize=(12, 6))
    values = [_mean(summary, method, "routing_f1") for method in methods]
    axis.bar(display_methods, values, color="#247BA0")
    axis.set_ylim(0, 1.05)
    axis.set_ylabel("Mean multi-label routing F1")
    axis.set_title(f"Routing quality\n{label}")
    axis.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(plots / "routing_accuracy.png", dpi=180)
    plt.close(fig)

    stages = ["routing_ms", "planning_ms", "loading_ms", "inference_ms"]
    stage_labels = ["Route", "Plan", "Load", "Inference"]
    fig, axis = plt.subplots(figsize=(12, 6))
    bottom = np.zeros(len(methods))
    colors = ["#247BA0", "#70C1B3", "#F3FFBD", "#FF7B6B"]
    for stage, stage_label, color in zip(stages, stage_labels, colors, strict=True):
        stage_values = np.array([_mean(summary, method, stage) for method in methods])
        axis.bar(display_methods, stage_values, bottom=bottom, label=stage_label, color=color)
        bottom += stage_values
    axis.set_ylabel("Mean measured wall-clock latency (ms)")
    axis.set_title(f"Latency breakdown\n{label}")
    axis.legend()
    axis.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(plots / "latency_breakdown.png", dpi=180)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(12, 6))
    values = [_mean(summary, method, "cache_hit_rate") for method in methods]
    axis.bar(display_methods, values, color="#70C1B3")
    axis.set_ylim(0, 1.05)
    axis.set_ylabel("Cache hit rate")
    axis.set_title(f"Runtime cache behavior\n{label}")
    axis.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(plots / "cache_hit_rate.png", dpi=180)
    plt.close(fig)

    experts = sorted(
        {
            expert
            for row in rows
            if row["method"] == "semantic"
            for expert in [*row["expected_experts"], *row["selected_experts"]]
        }
    )
    matrix = np.zeros((len(experts), len(experts)), dtype=int)
    index = {expert: position for position, expert in enumerate(experts)}
    for row in rows:
        if row["method"] != "semantic":
            continue
        for expected in row["expected_experts"]:
            for selected in row["selected_experts"]:
                matrix[index[expected], index[selected]] += 1
    fig, axis = plt.subplots(figsize=(8, 7))
    image = axis.imshow(matrix, cmap="Blues")
    short = [item.replace("_expert", "").replace("_", "\n") for item in experts]
    axis.set_xticks(range(len(experts)), short, fontsize=7)
    axis.set_yticks(range(len(experts)), short, fontsize=7)
    axis.set_xlabel("Selected expert")
    axis.set_ylabel("Expected expert")
    axis.set_title(f"Semantic-router multi-label co-selection\n{label}")
    for row_index in range(len(experts)):
        for column_index in range(len(experts)):
            value = matrix[row_index, column_index]
            axis.text(
                column_index,
                row_index,
                str(value),
                ha="center",
                va="center",
                fontsize=7,
                color="white" if value > matrix.max() / 2 else "#1F2937",
            )
    fig.colorbar(image, ax=axis)
    fig.tight_layout()
    fig.savefig(plots / "expert_selection_confusion_matrix.png", dpi=180)
    plt.close(fig)


def write_report(
    summary: dict[str, Any], manifest: dict[str, Any], environment: dict[str, Any], path: Path
) -> None:
    methods = summary["methods"]
    lines = [
        "# SelectiveLLM Benchmark Report",
        "",
        f"**Backend:** `{summary['backend']}` (`{summary['backend_kind']}`)",
        f"**Model identity:** `{manifest['model_identity']}`",
        f"**Benchmark:** `{manifest['benchmark_version']}`",
        f"**Fingerprint:** `{manifest['benchmark_fingerprint']}`",
        f"**Device class:** `{manifest['device_class']}`",
        "",
        "> Deterministic-control results validate routing and benchmark methodology. They do not demonstrate physical VRAM savings or language-model quality.",
        "",
        "## Hardware and software",
        "",
        "```json",
        json.dumps(environment, indent=2, sort_keys=True),
        "```",
        "",
        "## Methods and results",
        "",
        "| Method | n | Quality | Quality retention | Routing F1 | Declared peak MB | Declared reduction | Latency p50 ms | Latency p95 ms | Cache hit rate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for method, metrics in methods.items():
        retention = metrics["quality_retention"]["mean"]
        reduction = metrics["declared_memory_reduction"]["mean"]
        lines.append(
            "| {method} | {count} | {quality:.3f} | {retention} | {routing:.3f} | {memory:.1f} | {reduction} | {p50:.3f} | {p95:.3f} | {cache:.3f} |".format(
                method=method,
                count=metrics["quality"]["count"],
                quality=metrics["quality"]["mean"] or 0,
                retention=f"{retention:.1%}" if retention is not None else "N/A",
                routing=metrics["routing_f1"]["mean"] or 0,
                memory=metrics["declared_peak_capacity_mb"]["mean"] or 0,
                reduction=f"{reduction:.1%}" if reduction is not None else "N/A",
                p50=metrics["end_to_end_ms"]["p50"] or 0,
                p95=metrics["end_to_end_ms"]["p95"] or 0,
                cache=metrics["cache_hit_rate"]["mean"] or 0,
            )
        )
    lines.extend(
        [
            "",
            "Statistics include count, mean, median, standard deviation, p50, p95, and a normal-approximation 95% confidence interval where more than one observation exists. Case-level observations are not independent repeated training runs; intervals characterize this workload only.",
            "",
            "## Plots",
            "",
            "![Quality retention versus memory reduction](plots/quality_vs_memory.png)",
            "",
            "![Routing accuracy](plots/routing_accuracy.png)",
            "",
            "![Latency breakdown](plots/latency_breakdown.png)",
            "",
            "![Cache hit rate](plots/cache_hit_rate.png)",
            "",
            "![Expert selection matrix](plots/expert_selection_confusion_matrix.png)",
            "",
            "## Interpretation",
            "",
            _interpret(summary),
            "",
            "## Limitations",
            "",
            "- Declared capacity is registry metadata. For the deterministic-control backend it is simulated and is not observed VRAM.",
            "- Control task quality is synthetic capability coverage, not natural-language answer quality.",
            "- Routing performance on this small authored workload may not generalize.",
            "- Wall-clock timings describe this backend and machine; they are not model-loading forecasts.",
            "- A real Transformers/PEFT run is required for physical accelerator-memory and model-quality conclusions.",
            "",
            "## Negative-result policy",
            "",
            "Null and negative outcomes are retained. The benchmark is not tuned after inspection solely to favor semantic routing.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _interpret(summary: dict[str, Any]) -> str:
    methods = summary["methods"]
    semantic = methods.get("semantic")
    base = methods.get("base_only")
    keyword = methods.get("keyword")
    cached = methods.get("semantic_cache")
    if not semantic or not base:
        return "The configured method set is insufficient for the central comparison."
    statements = []
    quality_delta = (semantic["quality"]["mean"] or 0) - (base["quality"]["mean"] or 0)
    statements.append(
        f"Semantic routing changed the backend-specific quality score by {quality_delta:+.3f} relative to base-only."
    )
    if keyword:
        routing_delta = (semantic["routing_f1"]["mean"] or 0) - (keyword["routing_f1"]["mean"] or 0)
        statements.append(
            f"Its mean routing F1 differed from keyword routing by {routing_delta:+.3f}."
        )
    if cached:
        load_delta = (semantic["loading_ms"]["mean"] or 0) - (cached["loading_ms"]["mean"] or 0)
        statements.append(
            f"Caching changed mean control-backend load time by {-load_delta:+.3f} ms (cached minus uncached)."
        )
    statements.append(
        "These observations support conclusions only for the labeled backend, workload, configuration, and measurement semantics."
    )
    return " ".join(statements)
