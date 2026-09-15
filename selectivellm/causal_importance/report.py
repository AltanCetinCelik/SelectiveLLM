"""Evidence report and plots for causal-importance discovery."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _effect(metric: dict[str, Any]) -> str:
    return f"{metric['mean']:.4f} [{metric['ci95_low']:.4f}, {metric['ci95_high']:.4f}]"


def generate_plots(analysis: dict[str, Any], stability: dict[str, Any], output: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    output.mkdir(parents=True, exist_ok=True)
    metrics = ("same_minus_random", "same_minus_wrong", "same_minus_global_high")
    labels = ("Same - random", "Same - wrong", "Same - global high")
    colors = {"activation": "#4c78a8", "gradient": "#c23b22"}
    for block_size in (64, 128):
        fig, axis = plt.subplots(figsize=(8.2, 4.8))
        x = np.arange(len(metrics))
        for offset, method in ((-0.18, "activation"), (0.18, "gradient")):
            summaries = [
                analysis["block_sizes"][str(block_size)][method]["pooled"][metric]
                for metric in metrics
            ]
            means = [item["mean"] for item in summaries]
            errors = [
                [item["mean"] - item["ci95_low"] for item in summaries],
                [item["ci95_high"] - item["mean"] for item in summaries],
            ]
            axis.bar(
                x + offset,
                means,
                0.36,
                yerr=errors,
                capsize=3,
                color=colors[method],
                label=method.title(),
            )
        axis.axhline(0, color="#202020", linewidth=0.8)
        axis.set_xticks(x, labels)
        axis.set_ylabel("Paired correct-answer NLL damage advantage")
        axis.set_title(f"{block_size}-channel blocks: held-out causal controls")
        axis.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(output / f"causal_comparison_block{block_size}.png", dpi=180)
        plt.close(fig)

        fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4), sharey=True)
        domains = ("code", "mathematics", "science", "general")
        for axis, method in zip(axes, ("activation", "gradient"), strict=True):
            items = stability[str(block_size)][method]["domains"]
            values = (
                [items[domain]["split_half_jaccard_median"] / 0.20 for domain in domains],
                [items[domain]["split_half_spearman_median"] / 0.30 for domain in domains],
                [items[domain]["within_minus_across_jaccard"] / 0.05 for domain in domains],
            )
            positions = np.arange(4)
            for index, (series, label, color) in enumerate(
                zip(
                    values,
                    ("Top-mask Jaccard", "Rank Spearman", "Within - across"),
                    ("#4c78a8", "#e68a2e", "#72a555"),
                    strict=True,
                )
            ):
                axis.bar(positions + (index - 1) * 0.24, series, 0.24, label=label, color=color)
            axis.axhline(1, color="#202020", linestyle=":", linewidth=1)
            axis.set_xticks(positions, ("Code", "Math", "Science", "General"), rotation=20)
            axis.set_title(method.title())
        axes[0].set_ylabel("Observed value / preregistered threshold")
        axes[1].legend(frameon=False, fontsize=8)
        fig.suptitle(f"{block_size}-channel discovery stability")
        fig.tight_layout()
        fig.savefig(output / f"stability_block{block_size}.png", dpi=180)
        plt.close(fig)


def write_report(
    analysis: dict[str, Any],
    stability: dict[str, Any],
    signed: dict[str, Any],
    manifest: dict[str, Any],
    path: Path,
    *,
    scale_comparison: dict[str, Any] | None = None,
) -> None:
    decision = analysis["primary_decision"]
    classification = decision["classification"]
    conclusions = {
        "A": (
            "Objective-aware discovery succeeded under the frozen primary gate. The prior failure "
            "is attributable to activation magnitude being a poor causal-importance proxy in this test."
        ),
        "B": (
            "Gradient discovery found stable consequential capacity, but wrong-domain or global "
            "controls indicate mostly shared importance rather than semantic separability."
        ),
        "C": (
            "Objective-aware contiguous-block discovery also failed the frozen primary gate. The "
            "evidence does not support more discovery tuning on this model; model scale is next."
        ),
    }
    if scale_comparison is not None and classification == "C":
        conclusions["C"] = (
            "The same-family 3B scale increase also failed the frozen primary gate. Nearby model "
            "scale did not rescue stable causal specialization under this protocol."
        )
    lines = [
        "# Causal Importance Discovery",
        "",
        f"**Backend:** real dense `{manifest['model_identity']}`, pinned revision, no adapters.",
        "",
        "**Boundary:** logical MLP masking only. No weights were unloaded and no VRAM reduction "
        "was measured or claimed.",
        "",
        "## Primary Decision",
        "",
        f"**Outcome {classification}: {decision['label'].replace('_', ' ')}.** "
        f"{conclusions[classification]}",
        "",
        f"Full-model held-out accuracy was **{analysis['full_model']['accuracy']:.1%}** on 32 "
        f"questions; correct NLL was **{_effect(analysis['full_model']['correct_nll'])}**.",
        "",
        "Only the 64-channel analysis determines this classification. The 128-channel analysis is "
        "corroborative and is never pooled with it.",
        "",
        "## Causal Evidence",
        "",
        "Values are mean paired NLL effects with 95% case-bootstrap intervals. Positive values "
        "favor the discovery-derived same-domain mask.",
        "",
        "| Blocks | Method | Same damage | Same - random | Same - wrong | Same - global high | Same - global low |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for block_size in (64, 128):
        for method in ("activation", "gradient"):
            pooled = analysis["block_sizes"][str(block_size)][method]["pooled"]
            lines.append(
                f"| {block_size} | {method} | {_effect(pooled['same_damage'])} | "
                f"{_effect(pooled['same_minus_random'])} | {_effect(pooled['same_minus_wrong'])} | "
                f"{_effect(pooled['same_minus_global_high'])} | "
                f"{_effect(pooled['same_minus_global_low'])} |"
            )
    lines.extend(
        [
            "",
            "Direct objective-aware advantage:",
            "",
            "| Blocks | Gradient same - activation same |",
            "|---:|---:|",
        ]
    )
    for block_size in (64, 128):
        metric = analysis["block_sizes"][str(block_size)]["gradient"]["pooled"][
            "gradient_same_minus_activation_same"
        ]
        lines.append(f"| {block_size} | {_effect(metric)} |")

    lines.extend(
        [
            "",
            "## Discovery Stability",
            "",
            "| Blocks | Method | Stable domains | Median Jaccard | Median Spearman | Gradient improved |",
            "|---:|---|---:|---:|---:|---:|",
        ]
    )
    for block_size in (64, 128):
        size = stability[str(block_size)]
        for method in ("activation", "gradient"):
            item = size[method]
            lines.append(
                f"| {block_size} | {method} | {item['stable_domain_count']}/4 | "
                f"{item['median_domain_jaccard']:.4f} | {item['median_domain_spearman']:.4f} | "
                f"{size['improved_gradient_vs_activation'] if method == 'gradient' else '-'} |"
            )

    lines.extend(
        [
            "",
            "## Primary Gate Audit",
            "",
            "| Criterion | Passed |",
            "|---|---:|",
        ]
    )
    for name, passed in decision["a_checks"].items():
        lines.append(f"| A: {name.replace('_', ' ')} | {passed} |")
    if decision.get("b_checks"):
        for name, passed in decision["b_checks"].items():
            lines.append(f"| B: {name.replace('_', ' ')} | {passed} |")

    lines.extend(
        [
            "",
            "## 128-Channel Concordance",
            "",
            "This table is descriptive only and cannot change the primary result.",
            "",
            "| Metric | 64-channel | 128-channel | Same sign |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in analysis["corroborative_concordance"]:
        lines.append(
            f"| {row['metric']} | {_effect(row['primary_64'])} | "
            f"{_effect(row['corroborative_128'])} | {row['same_point_estimate_sign']} |"
        )

    lines.extend(
        [
            "",
            "## Signed Diagnostics",
            "",
            "`predicted_taylor_damage` uses a token sum and is compared with observed NLL damage. "
            "`normalized_signed_attribution` uses a token mean and is preserved separately. Neither "
            "quantity enters discovery or classification.",
            "",
            "| Blocks | Rows | Sign agreement | Spearman | Pearson |",
            "|---:|---:|---:|---:|---:|",
        ]
    )
    for block_size in (64, 128):
        item = signed["block_sizes"][str(block_size)]
        lines.append(
            f"| {block_size} | {item['row_count']} | {item['sign_agreement']:.3f} | "
            f"{item['spearman_association']:.3f} | {item['pearson_association']:.3f} |"
        )

    if scale_comparison is not None:
        lines.extend(
            [
                "",
                "## Paired Scale Comparison",
                "",
                f"Models remain separate; values are paired 3B-minus-1.5B case effects. "
                f"Classification transition: **{scale_comparison['classification_transition']}**. "
                f"Scale rescue: **{scale_comparison['scale_rescue']}**.",
                "",
                "| Metric | Paired scale delta |",
                "|---|---:|",
            ]
        )
        for metric, summary in scale_comparison["metrics"].items():
            lines.append(f"| {metric.replace('_', ' ')} | {_effect(summary)} |")
        scale_stability = scale_comparison["stability"]
        lines.extend(
            [
                "",
                "Primary gradient-stable domains changed from "
                f"**{scale_stability['prior_gradient_stable_domains']}/4** to "
                f"**{scale_stability['current_gradient_stable_domains']}/4**. Models are never "
                "pooled, and this comparison cannot replace the current model's primary gate.",
            ]
        )

    lines.extend(
        [
            "",
            "## Validity And Provenance",
            "",
            f"Validity: **{'passed' if analysis['validity']['passed'] else 'failed'}**. "
            f"Source commit: `{manifest['git_commit']}`; clean worktree: "
            f"`{not manifest['source_dirty']}`.",
            "",
            "| Check | Passed |",
            "|---|---:|",
        ]
    )
    for name, passed in analysis["validity"]["checks"].items():
        lines.append(f"| {name.replace('_', ' ')} | {passed} |")
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "This experiment tests discovery statistics over contiguous logical blocks. It does not "
            "demonstrate physical block independence, residency, transfer latency, paging, or memory "
            "reduction. Negative and contradictory effects remain in the evidence artifacts.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
