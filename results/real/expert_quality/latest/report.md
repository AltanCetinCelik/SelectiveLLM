# Expert-Quality Diagnostic

**Backend:** real `transformers-peft` on `mps`. No deterministic or simulated quality results appear in this report.

**Decision:** `expert_pool_viable`. The fixed expert pool passes the preregistered gate for a larger routing-validation study: it has strong empirical upside and primary labeled specialists usually occur among the best tie sets.

Passing this gate demonstrates response-quality diversity, not clean domain specialization. Specialist lift, specialization margin, sole-winner rate, and evaluator validity must be read alongside the gate.

## Aggregate quality

All intervals are 95% percentile bootstraps over the nine benchmark cases. Repetitions are averaged within each case-condition cell first.

| Condition or policy | Mean [95% CI] |
|---|---:|
| base | 0.406 [0.156, 0.672] (n=9) |
| code | 0.526 [0.302, 0.767] (n=9) |
| math | 0.415 [0.211, 0.637] (n=9) |
| science | 0.370 [0.166, 0.611] (n=9) |
| label_oracle | 0.443 [0.220, 0.683] (n=9) |
| semantic_router | 0.443 [0.220, 0.683] (n=9) |
| empirical_oracle | 0.748 [0.543, 0.933] (n=9) |

## Diagnostic metrics

| Metric | Mean [95% CI] |
|---|---:|
| Specialist lift | 0.048 [-0.250, 0.286] (n=7) |
| Specialization margin | 0.062 [-0.250, 0.396] (n=6) |
| Routing opportunity | 0.343 [0.111, 0.611] (n=9) |

Empirical oracle strictly improved over base on **5/9** cases. The primary labeled specialist was in the best tie set on **5/7** labeled cases (71.4%) and was the sole winner on **1/7** (14.3%).

## Termination and repetition stability

The fixed 384-token ceiling was reached by **21/108** generations (19.4%). Exact quality-score agreement occurred in **36/36** cells (100.0%); mean within-cell sample standard deviation was `0.0000` and the maximum was `0.0000`.

## Expert-specialization matrix

| Case | Expected | Base | Code | Math | Science | Empirical best | Opportunity |
|---|---|---:|---:|---:|---:|---|---:|
| py_binary_search | code_expert | 0.500 | 1.000 | 0.250 | 0.250 | code | 0.500 |
| py_fastapi | code_expert | 1.000 | 0.250 | 0.750 | 0.250 | base | 0.000 |
| math_probability | math_expert | 0.000 | 1.000 | 0.000 | 0.000 | code | 1.000 |
| math_proof | math_expert | 0.750 | 0.500 | 0.750 | 0.250 | base, math | 0.000 |
| ee_mosfet | science_expert | 0.000 | 0.250 | 0.250 | 0.250 | code, math, science | 0.250 |
| ee_filter | science_expert, math_expert | 0.000 | 0.333 | 0.333 | 0.333 | code, math, science | 0.333 |
| general_capital | base | 1.000 | 1.000 | 1.000 | 1.000 | base, code, math, science | 0.000 |
| irrelevant_python | base | 0.000 | 0.000 | 0.000 | 1.000 | science | 1.000 |
| rlc_python | code_expert, science_expert, math_expert | 0.400 | 0.400 | 0.400 | 0.000 | base, code, math | 0.000 |

## Label mismatches

- `py_fastapi`: primary `code_expert`; empirical best `['base']`; qualities `{'base': 1.0, 'code': 0.25, 'math': 0.75, 'science': 0.25}`.
- `math_probability`: primary `math_expert`; empirical best `['code']`; qualities `{'base': 0.0, 'code': 1.0, 'math': 0.0, 'science': 0.0}`.

## Limits

This is a nine-case, fixed-rubric diagnostic of one pinned base and three public LoRAs on one Apple MPS device. The rubric measures requested concepts, not broad human preference. Technical repetitions measure inference/evaluation stability and are not independent benchmark samples. The empirical oracle is post-generation and estimates available opportunity; it is not a deployable routing policy. Negative and tied results are retained.

The post-run [validity audit](validity_audit.md) documents evaluator-sensitive cases, truncation concentration, multi-capability evidence, and the distinction between empirical diversity and domain specialization. It does not alter the formal result.
