# Causal Importance Discovery

**Backend:** real dense `Qwen/Qwen2.5-3B-Instruct`, pinned revision, no adapters.

**Boundary:** logical MLP masking only. No weights were unloaded and no VRAM reduction was measured or claimed.

## Primary Decision

**Outcome C: still weak or unstable.** The same-family 3B scale increase also failed the frozen primary gate. Nearby model scale did not rescue stable causal specialization under this protocol.

Full-model held-out accuracy was **78.1%** on 32 questions; correct NLL was **2.8329 [0.9788, 5.0149]**.

Only the 64-channel analysis determines this classification. The 128-channel analysis is corroborative and is never pooled with it.

## Causal Evidence

Values are mean paired NLL effects with 95% case-bootstrap intervals. Positive values favor the discovery-derived same-domain mask.

| Blocks | Method | Same damage | Same - random | Same - wrong | Same - global high | Same - global low |
|---:|---|---:|---:|---:|---:|---:|
| 64 | activation | 0.9767 [-0.1743, 2.4603] | 0.3978 [-0.6359, 1.6322] | 0.0795 [-0.8904, 1.1130] | -0.7296 [-2.2335, 0.6786] | 0.7966 [-0.4650, 2.3783] |
| 64 | gradient | 1.3016 [-0.0077, 2.9763] | 0.7227 [-0.3634, 2.0460] | 0.9913 [-0.0164, 2.1970] | 1.2728 [-0.0361, 2.8638] | 0.9929 [-0.1457, 2.2243] |
| 128 | activation | 1.0779 [0.2252, 2.1625] | 0.5683 [-0.1052, 1.3136] | 0.7337 [-0.1679, 1.9201] | -0.3612 [-1.3923, 0.4863] | 1.0796 [0.1373, 2.1911] |
| 128 | gradient | 1.2091 [0.1830, 2.4553] | 0.6995 [-0.1426, 1.5241] | 0.8120 [-0.0060, 1.5987] | 0.7057 [-0.0584, 1.4387] | 1.0946 [-0.3815, 2.6311] |

Direct objective-aware advantage:

| Blocks | Gradient same - activation same |
|---:|---:|
| 64 | 0.3249 [-0.6985, 1.2962] |
| 128 | 0.1312 [-0.6637, 0.8328] |

## Discovery Stability

| Blocks | Method | Stable domains | Median Jaccard | Median Spearman | Gradient improved |
|---:|---|---:|---:|---:|---:|
| 64 | activation | 1/4 | 0.2058 | 0.6472 | - |
| 64 | gradient | 1/4 | 0.1066 | 0.4809 | False |
| 128 | activation | 1/4 | 0.2004 | 0.6419 | - |
| 128 | gradient | 1/4 | 0.0917 | 0.4822 | False |

## Primary Gate Audit

| Criterion | Passed |
|---|---:|
| A: validity passed | True |
| A: gradient stable at least three domains | False |
| A: improved stability | False |
| A: same damage at least 0 10 | True |
| A: same minus random threshold | True |
| A: same minus random ci positive | False |
| A: same minus wrong threshold | True |
| A: same minus wrong ci positive | False |
| A: same minus global high positive | True |
| A: same minus global high ci positive | False |
| A: same exceeds all controls in three domains | True |
| A: gradient minus activation threshold | True |
| A: gradient minus activation ci positive | False |
| B: validity passed | True |
| B: gradient stable at least three domains | False |
| B: same damage at least 0 10 | True |
| B: same minus random threshold | True |
| B: same minus random ci positive | False |
| B: outcome a failed | True |
| B: shared core indicator | False |

## 128-Channel Concordance

This table is descriptive only and cannot change the primary result.

| Metric | 64-channel | 128-channel | Same sign |
|---|---:|---:|---:|
| same_minus_random | 0.7227 [-0.3634, 2.0460] | 0.6995 [-0.1426, 1.5241] | True |
| same_minus_wrong | 0.9913 [-0.0164, 2.1970] | 0.8120 [-0.0060, 1.5987] | True |
| same_minus_global_high | 1.2728 [-0.0361, 2.8638] | 0.7057 [-0.0584, 1.4387] | True |
| same_minus_global_low | 0.9929 [-0.1457, 2.2243] | 1.0946 [-0.3815, 2.6311] | True |
| gradient_same_minus_activation_same | 0.3249 [-0.6985, 1.2962] | 0.1312 [-0.6637, 0.8328] | True |

## Signed Diagnostics

`predicted_taylor_damage` uses a token sum and is compared with observed NLL damage. `normalized_signed_attribution` uses a token mean and is preserved separately. Neither quantity enters discovery or classification.

| Blocks | Rows | Sign agreement | Spearman | Pearson |
|---:|---:|---:|---:|---:|
| 64 | 544 | 0.601 | 0.181 | 0.276 |
| 128 | 544 | 0.633 | 0.320 | 0.520 |

## Paired Scale Comparison

Models remain separate; values are paired 3B-minus-1.5B case effects. Classification transition: **C->C**. Scale rescue: **False**.

| Metric | Paired scale delta |
|---|---:|
| same damage | 1.9057 [0.4973, 3.6474] |
| same minus random | 1.0787 [-0.0490, 2.4195] |
| same minus wrong | 1.3492 [0.2126, 2.6570] |
| same minus global high | 1.1758 [-0.1222, 2.6342] |
| gradient same minus activation same | 0.9138 [-0.0280, 1.9519] |

Primary gradient-stable domains changed from **0/4** to **1/4**. Models are never pooled, and this comparison cannot replace the current model's primary gate.

## Validity And Provenance

Validity: **passed**. Source commit: `43efe65c34cc54d89fb6089a6a08b14923b644f6`; clean worktree: `True`.

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
