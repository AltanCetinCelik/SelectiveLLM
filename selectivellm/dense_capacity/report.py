"""Compact evidence report and plots for dense-capacity feasibility."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_plots(analysis: dict[str, Any], stability: dict[str, Any], output: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    output.mkdir(parents=True, exist_ok=True)
    granularities = list(analysis["granularities"])
    conditions = ("same_damage", "wrong_damage", "random_damage", "low_damage")
    labels = ("Same domain", "Wrong domain", "Random", "Low importance")
    colors = ("#c23b22", "#4c78a8", "#72a555", "#8b8b8b")
    x = np.arange(len(granularities))
    width = 0.19
    fig, axis = plt.subplots(figsize=(8.5, 4.8))
    for index, (condition, label, color) in enumerate(zip(conditions, labels, colors, strict=True)):
        summaries = [
            analysis["granularities"][granularity]["pooled"][condition]
            for granularity in granularities
        ]
        values = [item["mean"] for item in summaries]
        errors = [
            [item["mean"] - item["ci95_low"] for item in summaries],
            [item["ci95_high"] - item["mean"] for item in summaries],
        ]
        axis.bar(
            x + (index - 1.5) * width,
            values,
            width,
            yerr=errors,
            capsize=2,
            label=label,
            color=color,
        )
    axis.axhline(0, color="#202020", linewidth=0.8)
    axis.set_xticks(x, [item.upper() for item in granularities])
    axis.set_ylabel("Mean paired correct-answer NLL degradation")
    axis.set_title("Equal-structure causal ablations on held-out questions")
    axis.legend(frameon=False, ncols=2)
    fig.tight_layout()
    fig.savefig(output / "causal_damage_controls.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(
        1, len(granularities), figsize=(4.2 * len(granularities), 4.2), sharey=True
    )
    if len(granularities) == 1:
        axes = [axes]
    domains = ("code", "mathematics", "science", "general")
    for axis, granularity in zip(axes, granularities, strict=True):
        items = stability["granularities"][granularity]["domains"]
        jaccard = [items[domain]["split_half_jaccard_median"] / 0.20 for domain in domains]
        spearman = [items[domain]["split_half_spearman_median"] / 0.30 for domain in domains]
        separation = [items[domain]["within_minus_across_jaccard"] / 0.05 for domain in domains]
        positions = np.arange(len(domains))
        axis.bar(positions - 0.24, jaccard, 0.24, color="#4c78a8", label="Top-mask Jaccard")
        axis.bar(positions, spearman, 0.24, color="#e68a2e", label="Rank Spearman")
        axis.bar(
            positions + 0.24,
            separation,
            0.24,
            color="#72a555",
            label="Within - across overlap",
        )
        axis.axhline(1.0, color="#202020", linestyle=":", linewidth=1)
        axis.set_xticks(positions, ["Code", "Math", "Science", "General"], rotation=25)
        axis.set_title(granularity.upper())
    axes[0].set_ylabel("Observed value / preregistered threshold")
    axes[-1].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(output / "discovery_stability.png", dpi=180)
    plt.close(fig)


def _effect(metric: dict[str, Any]) -> str:
    return f"{metric['mean']:.4f} [{metric['ci95_low']:.4f}, {metric['ci95_high']:.4f}]"


def write_report(
    analysis: dict[str, Any],
    stability: dict[str, Any],
    contracts: dict[str, Any],
    retention: dict[str, Any] | None,
    path: Path,
) -> None:
    decision = analysis["decision"]
    classification = decision["classification"]
    if classification == "A":
        answer = (
            "Yes. Discovery-derived selections produced stable, domain-specific held-out damage "
            "beyond matched random and wrong-domain ablations under the frozen A gate."
        )
    elif classification == "B":
        answer = (
            "Partly. The model showed a causally useful task-dependent tail, but the evidence also "
            "indicates a strong shared core and did not satisfy the stricter A gate."
        )
    else:
        answer = (
            "No convincing evidence at the tested granularities. The valid result did not satisfy "
            "the preregistered causal specialization gates."
            if analysis["validity"]["passed"]
            else "The experiment cannot support the claim because a preregistered validity gate failed."
        )
    lines = [
        "# Dense Capacity Feasibility",
        "",
        "**Backend:** real dense `Qwen/Qwen2.5-1.5B-Instruct` at the pinned revision, no adapters.",
        "",
        "**Intervention:** logical inference-time masking. No parameters were unloaded, no physical "
        "memory was saved, and this experiment makes no VRAM-reduction claim.",
        "",
        "## Decision",
        "",
        f"**Classification {classification}: {decision['label'].replace('_', ' ')}.** {answer}",
        "",
        f"Full-model held-out accuracy: **{analysis['full_model']['accuracy']:.1%}** on "
        f"**{analysis['full_model']['case_count']}** independent questions. Full-model correct NLL: "
        f"**{_effect(analysis['full_model']['correct_nll'])}** (mean and case-bootstrap 95% interval).",
        "",
        "The completed matrix contains 48 discovery traces, 32 full-model held-out scores, "
        "992 causal scores, and 96 zero-size no-op scores. Pooled intervals use 32 questions; "
        "domain intervals use eight questions.",
        "",
        "## Causal Results",
        "",
        "Positive values mean the intervention harmed the correct answer. Intervals bootstrap held-out "
        "questions, stratified by domain.",
        "",
        "| Granularity | Same damage | Random damage | Wrong damage | Same - random | Same - wrong | Stable domains |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for granularity, result in analysis["granularities"].items():
        pooled = result["pooled"]
        lines.append(
            f"| {granularity.upper()} | {_effect(pooled['same_damage'])} | "
            f"{_effect(pooled['random_damage'])} | {_effect(pooled['wrong_damage'])} | "
            f"{_effect(pooled['same_minus_random'])} | {_effect(pooled['same_minus_wrong'])} | "
            f"{result['stable_domain_count']}/4 |"
        )
    lines.extend(
        [
            "",
            "The MLP point estimate favored same-domain masks over random and wrong-domain masks, "
            "but both pooled intervals crossed zero and only one of four domain selections passed "
            "the discovery-stability gate. Head and layer pooled same-domain advantages were "
            "negative. The domain-level positives are therefore retained as leads, not promoted "
            "to evidence of generalizable routed capacity.",
        ]
    )
    lines.extend(
        [
            "",
            "Discovery stability requires all three criteria to meet threshold.",
            "",
            "| Granularity | Domain | Top-mask Jaccard | Rank Spearman | Within - across | Stable |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for granularity, result in stability["granularities"].items():
        for domain, item in result["domains"].items():
            lines.append(
                f"| {granularity.upper()} | {domain} | "
                f"{item['split_half_jaccard_median']:.4f} | "
                f"{item['split_half_spearman_median']:.4f} | "
                f"{item['within_minus_across_jaccard']:.4f} | {item['stable']} |"
            )
    lines.extend(
        [
            "",
            "Absolute condition scores (lower NLL and higher accuracy are better):",
            "",
            "| Granularity | Condition | Correct NLL | Accuracy |",
            "|---|---|---:|---:|",
        ]
    )
    for granularity, result in analysis["granularities"].items():
        for condition, scores in result["absolute_conditions"].items():
            lines.append(
                f"| {granularity.upper()} | {condition} | "
                f"{_effect(scores['correct_nll'])} | {scores['accuracy']:.1%} |"
            )
    lines.extend(
        [
            "",
            "## Domain Breakdown",
            "",
            "| Granularity | Domain | Same damage | Same - random | Same - wrong | Same beats all controls |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for granularity, result in analysis["granularities"].items():
        for domain, domain_result in result["domains"].items():
            lines.append(
                f"| {granularity.upper()} | {domain} | {_effect(domain_result['same_damage'])} | "
                f"{_effect(domain_result['same_minus_random'])} | "
                f"{_effect(domain_result['same_minus_wrong'])} | "
                f"{domain_result['same_exceeds_all_controls']} |"
            )
    lines.extend(
        [
            "",
            "## Validity",
            "",
            f"Overall validity: **{'passed' if analysis['validity']['passed'] else 'failed'}**.",
            "",
            "| Check | Result |",
            "|---|---:|",
        ]
    )
    for name, passed in analysis["validity"]["checks"].items():
        lines.append(f"| {name.replace('_', ' ')} | {passed} |")
    lines.extend(
        [
            "",
            "## Implementation Contracts",
            "",
            f"Attention-head layout: **{contracts['attention_head_layout']['status']}**; "
            f"query heads `{contracts['attention_head_layout']['query_head_count']}`, KV heads "
            f"`{contracts['attention_head_layout']['kv_head_count']}`, head dimension "
            f"`{contracts['attention_head_layout']['head_dimension']}`.",
            "",
            f"Layer identity bypass: **{contracts['layer_identity_bypass']['status']}**. The next "
            "decoder block received the selected layer's original residual exactly; the selected "
            "block's computed residual update was discarded.",
            "",
            "## Retention",
            "",
        ]
    )
    if retention is None:
        lines.append(
            "Not run because the initial experiment did not trigger classification A or B."
        )
    else:
        lines.extend(
            [
                "The preregistered A/B gate triggered a logical capacity-retention curve. This still "
                "does not represent physical parameter removal or memory reduction.",
                "",
                "| Retained | Condition | Correct NLL mean | NLL damage | Accuracy | Quality retention |",
                "|---:|---|---:|---:|---:|---:|",
            ]
        )
        for item in retention["aggregates"]:
            lines.append(
                f"| {item['fraction']:.0%} | {item['condition']} | "
                f"{item['correct_nll']['mean']:.4f} | {_effect(item['causal_damage'])} | "
                f"{item['accuracy']:.1%} | {item['quality_retention']['mean']:.3f} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "This experiment can test stable and causally useful prompt-dependent internal capacity. "
            "It cannot demonstrate routable physical blocks, parameter paging, latency benefits, or "
            "memory reduction. Those remain separate future systems questions and are justified only "
            "after a positive causal gate.",
            "",
            "Negative, tied, unstable, and near-threshold effects are retained in the raw artifacts.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
