# Dense Capacity Feasibility

**Backend:** real dense `Qwen/Qwen2.5-1.5B-Instruct` at the pinned revision, no adapters.

**Intervention:** logical inference-time masking. No parameters were unloaded, no physical memory was saved, and this experiment makes no VRAM-reduction claim.

## Decision

**Classification C: weak or unstable specialization.** No convincing evidence at the tested granularities. The valid result did not satisfy the preregistered causal specialization gates.

Full-model held-out accuracy: **65.6%** on **32** independent questions. Full-model correct NLL: **1.6137 [0.9491, 2.3413]** (mean and case-bootstrap 95% interval).

The completed matrix contains 48 discovery traces, 32 full-model held-out scores, 992 causal scores, and 96 zero-size no-op scores. Pooled intervals use 32 questions; domain intervals use eight questions.

## Causal Results

Positive values mean the intervention harmed the correct answer. Intervals bootstrap held-out questions, stratified by domain.

| Granularity | Same damage | Random damage | Wrong damage | Same - random | Same - wrong | Stable domains |
|---|---:|---:|---:|---:|---:|---:|
| MLP | 0.2565 [-0.4160, 0.9589] | -0.1678 [-0.4599, 0.1221] | -0.1109 [-0.4906, 0.2426] | 0.4243 [-0.2115, 1.0798] | 0.3674 [-0.2924, 1.0435] | 1/4 |
| HEAD | -0.0433 [-0.7139, 0.6179] | 0.0346 [-0.5556, 0.5858] | 0.0193 [-0.3693, 0.4272] | -0.0779 [-0.6525, 0.4727] | -0.0626 [-0.6408, 0.5231] | 1/4 |
| LAYER | 0.2157 [-0.6261, 1.0064] | 0.3113 [-0.4460, 1.0050] | 0.3846 [-0.4858, 1.1858] | -0.0956 [-0.5088, 0.3068] | -0.1689 [-0.6880, 0.3483] | 0/4 |

The MLP point estimate favored same-domain masks over random and wrong-domain masks, but both pooled intervals crossed zero and only one of four domain selections passed the discovery-stability gate. Head and layer pooled same-domain advantages were negative. The domain-level positives are therefore retained as leads, not promoted to evidence of generalizable routed capacity.

Discovery stability requires all three criteria to meet threshold.

| Granularity | Domain | Top-mask Jaccard | Rank Spearman | Within - across | Stable |
|---|---|---:|---:|---:|---:|
| HEAD | code | 0.1429 | 0.4548 | -0.0122 | False |
| HEAD | general | 0.1548 | 0.5906 | 0.0336 | False |
| HEAD | mathematics | 0.2174 | 0.6763 | 0.0989 | True |
| HEAD | science | 0.1200 | 0.4430 | 0.0098 | False |
| LAYER | code | 0.4000 | 0.5862 | 0.0000 | False |
| LAYER | general | 0.3364 | 0.6160 | 0.0000 | False |
| LAYER | mathematics | 0.7500 | 0.9152 | 0.0000 | False |
| LAYER | science | 0.5556 | 0.7994 | 0.0000 | False |
| MLP | code | 0.2522 | 0.5825 | 0.0387 | False |
| MLP | general | 0.1849 | 0.6205 | 0.0889 | False |
| MLP | mathematics | 0.2726 | 0.6642 | 0.1113 | True |
| MLP | science | 0.2059 | 0.5621 | 0.0259 | False |

Absolute condition scores (lower NLL and higher accuracy are better):

| Granularity | Condition | Correct NLL | Accuracy |
|---|---|---:|---:|
| MLP | same | 1.8702 [1.2953, 2.4281] | 53.1% |
| MLP | wrong | 1.5028 [0.8982, 2.1841] | 66.7% |
| MLP | random | 1.4459 [0.9018, 2.0409] | 64.4% |
| MLP | low | 1.6216 [1.0507, 2.2389] | 59.4% |
| HEAD | same | 1.5704 [1.0709, 2.1132] | 50.0% |
| HEAD | wrong | 1.6330 [1.1335, 2.1848] | 55.2% |
| HEAD | random | 1.6483 [1.2110, 2.1716] | 59.4% |
| HEAD | low | 1.0751 [0.5511, 1.6978] | 71.9% |
| LAYER | same | 1.8294 [1.4347, 2.2154] | 28.1% |
| LAYER | wrong | 1.9983 [1.6705, 2.3332] | 27.1% |
| LAYER | random | 1.9250 [1.7295, 2.1191] | 28.7% |
| LAYER | low | 4.8220 [3.5229, 6.1576] | 25.0% |

## Domain Breakdown

| Granularity | Domain | Same damage | Same - random | Same - wrong | Same beats all controls |
|---|---|---:|---:|---:|---:|
| MLP | code | -0.2337 [-1.2374, 0.7281] | -0.1941 [-0.9992, 0.6140] | -0.3239 [-1.3840, 0.6228] | False |
| MLP | mathematics | 1.7485 [-0.0398, 3.9737] | 2.1704 [0.2374, 4.3394] | 1.9855 [0.0169, 4.2690] | True |
| MLP | science | 0.6020 [-0.1155, 1.4129] | 0.6411 [0.0208, 1.3378] | 0.6177 [0.1334, 1.1528] | True |
| MLP | general | -1.0908 [-2.7170, 0.0114] | -0.9202 [-2.2202, 0.0064] | -0.8096 [-1.9053, 0.0103] | False |
| HEAD | code | 1.3781 [0.2100, 2.6884] | 0.3937 [0.0108, 0.7637] | 0.7151 [-0.0040, 1.5537] | True |
| HEAD | mathematics | -1.0927 [-1.7973, -0.3509] | -0.1791 [-1.0607, 0.7428] | -0.4778 [-1.3769, 0.1491] | False |
| HEAD | science | 0.7207 [-0.6796, 2.4868] | 0.6020 [-0.4868, 2.1259] | 0.4820 [-0.7494, 2.2092] | True |
| HEAD | general | -1.1795 [-2.9275, 0.1026] | -1.1282 [-2.7683, -0.0782] | -0.9699 [-2.3538, 0.0628] | False |
| LAYER | code | 1.2157 [-0.4190, 2.6654] | -0.0527 [-0.9482, 0.8145] | 0.3211 [-0.5991, 1.2022] | False |
| LAYER | mathematics | -2.0564 [-3.6600, -0.3172] | -0.1696 [-0.7166, 0.4350] | -0.5899 [-1.1799, -0.0147] | False |
| LAYER | science | 1.3678 [0.2030, 2.5424] | 0.0039 [-1.1743, 1.1919] | -0.1618 [-1.8398, 1.5644] | False |
| LAYER | general | 0.3357 [-1.8499, 2.0689] | -0.1640 [-0.4959, 0.1350] | -0.2449 [-0.6836, 0.2362] | False |

## Validity

Overall validity: **passed**.

| Check | Result |
|---|---:|
| full model accuracy at least 50 percent | True |
| answer positions balanced | True |
| repeated scoring stable | True |
| noop nll within tolerance | True |
| noop predictions identical | True |
| all probability sums valid | True |
| complete full model matrix | True |
| complete causal matrix | True |
| complete noop matrix | True |
| causal semantics unambiguous | True |

## Implementation Contracts

Attention-head layout: **valid**; query heads `12`, KV heads `2`, head dimension `128`.

Layer identity bypass: **valid**. The next decoder block received the selected layer's original residual exactly; the selected block's computed residual update was discarded.

## Retention

Not run because the initial experiment did not trigger classification A or B.

## Interpretation Boundary

This experiment can test stable and causally useful prompt-dependent internal capacity. It cannot demonstrate routable physical blocks, parameter paging, latency benefits, or memory reduction. Those remain separate future systems questions and are justified only after a positive causal gate.

Negative, tied, unstable, and near-threshold effects are retained in the raw artifacts.
