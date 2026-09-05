# Causal Importance Discovery

**Backend:** real dense `Qwen/Qwen2.5-1.5B-Instruct`, pinned revision, no adapters.

**Boundary:** logical MLP masking only. No weights were unloaded and no VRAM reduction was measured or claimed.

## Primary Decision

**Outcome C: still weak or unstable.** Objective-aware contiguous-block discovery also failed the frozen primary gate. The evidence does not support more discovery tuning on this model; model scale is next.

Full-model held-out accuracy was **65.6%** on 32 questions; correct NLL was **1.6128 [0.9495, 2.3373]**.

Only the 64-channel analysis determines this classification. The 128-channel analysis is corroborative and is never pooled with it.

## Causal Evidence

Values are mean paired NLL effects with 95% case-bootstrap intervals. Positive values favor the discovery-derived same-domain mask.

| Blocks | Method | Same damage | Same - random | Same - wrong | Same - global high | Same - global low |
|---:|---|---:|---:|---:|---:|---:|
| 64 | activation | -0.0152 [-0.6086, 0.5771] | 0.2329 [-0.2431, 0.7228] | 0.3309 [-0.2549, 0.9054] | 0.1126 [-0.7555, 0.9943] | -0.0434 [-0.5726, 0.4811] |
| 64 | gradient | -0.6041 [-1.1517, -0.0668] | -0.3561 [-0.7998, 0.0528] | -0.3579 [-0.8056, 0.0203] | 0.0969 [-0.3539, 0.6070] | -0.2347 [-0.7448, 0.2390] |
| 128 | activation | 0.2681 [-0.0488, 0.5928] | 0.2549 [-0.1415, 0.6446] | 0.5930 [0.2056, 0.9776] | 0.3606 [-0.3438, 1.0439] | -0.0299 [-0.4379, 0.3600] |
| 128 | gradient | 0.0975 [-0.2460, 0.4416] | 0.0842 [-0.2761, 0.4767] | 0.1076 [-0.2530, 0.4532] | 0.2590 [-0.4390, 1.0271] | 0.4490 [-0.0739, 1.0875] |

Direct objective-aware advantage:

| Blocks | Gradient same - activation same |
|---:|---:|
| 64 | -0.5890 [-1.1267, -0.1543] |
| 128 | -0.1707 [-0.5423, 0.2383] |

## Discovery Stability

| Blocks | Method | Stable domains | Median Jaccard | Median Spearman | Gradient improved |
|---:|---|---:|---:|---:|---:|
| 64 | activation | 1/4 | 0.2055 | 0.6502 | - |
| 64 | gradient | 0/4 | 0.0958 | 0.4137 | False |
| 128 | activation | 1/4 | 0.1951 | 0.6459 | - |
| 128 | gradient | 0/4 | 0.0904 | 0.3959 | False |

## Primary Gate Audit

| Criterion | Passed |
|---|---:|
| A: validity passed | True |
| A: gradient stable at least three domains | False |
| A: improved stability | False |
| A: same damage at least 0 10 | False |
| A: same minus random threshold | False |
| A: same minus random ci positive | False |
| A: same minus wrong threshold | False |
| A: same minus wrong ci positive | False |
| A: same minus global high positive | True |
| A: same minus global high ci positive | False |
| A: same exceeds all controls in three domains | False |
| A: gradient minus activation threshold | False |
| A: gradient minus activation ci positive | False |
| B: validity passed | True |
| B: gradient stable at least three domains | False |
| B: same damage at least 0 10 | False |
| B: same minus random threshold | False |
| B: same minus random ci positive | False |
| B: outcome a failed | True |
| B: shared core indicator | True |

## 128-Channel Concordance

This table is descriptive only and cannot change the primary result.

| Metric | 64-channel | 128-channel | Same sign |
|---|---:|---:|---:|
| same_minus_random | -0.3561 [-0.7998, 0.0528] | 0.0842 [-0.2761, 0.4767] | False |
| same_minus_wrong | -0.3579 [-0.8056, 0.0203] | 0.1076 [-0.2530, 0.4532] | False |
| same_minus_global_high | 0.0969 [-0.3539, 0.6070] | 0.2590 [-0.4390, 1.0271] | True |
| same_minus_global_low | -0.2347 [-0.7448, 0.2390] | 0.4490 [-0.0739, 1.0875] | False |
| gradient_same_minus_activation_same | -0.5890 [-1.1267, -0.1543] | -0.1707 [-0.5423, 0.2383] | True |

## Signed Diagnostics

`predicted_taylor_damage` uses a token sum and is compared with observed NLL damage. `normalized_signed_attribution` uses a token mean and is preserved separately. Neither quantity enters discovery or classification.

| Blocks | Rows | Sign agreement | Spearman | Pearson |
|---:|---:|---:|---:|---:|
| 64 | 544 | 0.539 | 0.229 | 0.329 |
| 128 | 544 | 0.601 | 0.396 | 0.406 |

## Validity And Provenance

Validity: **passed**. Source commit: `ac3c0d9384ab9474900ef5930bc12b66d888971e`; clean worktree: `True`.

| Check | Passed |
|---|---:|
| gradient preflight passed | True |
| full model accuracy at least 50 percent | True |
| answer positions balanced | True |
| repeated scoring stable | True |
| mapping and mask structure valid | True |
| all values finite | True |
| all probability sums valid | True |
| complete full matrix | True |
| complete causal matrix | True |
| complete signed matrix | True |
| noop equivalent | True |
| signed diagnostics excluded from masks | True |

## Interpretation Boundary

This experiment tests discovery statistics over contiguous logical blocks. It does not demonstrate physical block independence, residency, transfer latency, paging, or memory reduction. Negative and contradictory effects remain in the evidence artifacts.
