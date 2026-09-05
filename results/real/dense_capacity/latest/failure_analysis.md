# Failure Analysis

These are real dense-model scores under logical masking, not memory savings.

## Cases where the discovery-derived mask did not beat random

| Case | Domain | Granularity | Same - random NLL damage | Same - wrong |
|---|---|---|---:|---:|
| dense_general_eval_07 | general | head | -6.5264 | -5.3559 |
| dense_general_eval_05 | general | mlp | -3.9305 | -4.3628 |
| dense_general_eval_07 | general | mlp | -3.4582 | -2.1569 |
| dense_science_eval_02 | science | layer | -2.7108 | -2.8945 |
| dense_code_eval_03 | code | layer | -2.4195 | -1.9753 |
| dense_code_eval_05 | code | mlp | -2.0177 | -3.2905 |
| dense_math_eval_06 | mathematics | mlp | -1.8787 | -0.9142 |
| dense_science_eval_06 | science | layer | -1.8466 | -0.8838 |
| dense_code_eval_03 | code | mlp | -1.7126 | -1.0564 |
| dense_science_eval_02 | science | head | -1.7035 | -1.3908 |
| dense_math_eval_01 | mathematics | head | -1.6930 | -0.5042 |
| dense_math_eval_07 | mathematics | head | -1.6782 | -3.3646 |
| dense_math_eval_08 | mathematics | layer | -1.3339 | -1.6208 |
| dense_general_eval_03 | general | head | -1.3257 | 0.0728 |
| dense_math_eval_02 | mathematics | head | -1.2333 | -0.0463 |
| dense_science_eval_07 | science | layer | -1.1461 | -3.4959 |
| dense_math_eval_06 | mathematics | head | -1.0687 | 0.0462 |
| dense_general_eval_05 | general | head | -0.9999 | -2.6158 |
| dense_general_eval_05 | general | layer | -0.9685 | -0.7494 |
| dense_math_eval_04 | mathematics | layer | -0.9304 | -1.0690 |
