# Failure Analysis

Real dense-model NLL under logical contiguous-block masking; no memory claim.

| Case | Domain | Blocks | Gradient - activation | Same - random | Same - wrong |
|---|---|---:|---:|---:|---:|
| dense_science_eval_01 | science | 128 | -9.1561 | -1.1324 | -6.4791 |
| dense_math_eval_03 | mathematics | 64 | -8.7344 | -2.5812 | -3.6510 |
| dense_code_eval_01 | code | 64 | -6.5257 | -1.8399 | -1.7113 |
| dense_code_eval_01 | code | 128 | -3.6056 | -3.9399 | -3.8887 |
| dense_general_eval_04 | general | 128 | -2.6867 | -5.0352 | -1.6300 |
| dense_code_eval_05 | code | 64 | -1.5057 | -2.8330 | -1.1513 |
| dense_code_eval_03 | code | 64 | -0.3125 | -0.6569 | 2.4756 |
| dense_math_eval_04 | mathematics | 64 | -0.0550 | -2.1635 | -0.0006 |
| dense_science_eval_02 | science | 64 | -0.0001 | -0.0009 | 0.0000 |
| dense_science_eval_02 | science | 128 | -0.0000 | -0.0002 | -0.0000 |
| dense_science_eval_08 | science | 64 | -0.0000 | -0.0000 | -0.0000 |
| dense_general_eval_07 | general | 128 | -0.0000 | -0.0000 | -0.0002 |
| dense_science_eval_08 | science | 128 | -0.0000 | -0.0000 | -0.0000 |
| dense_code_eval_06 | code | 64 | -0.0000 | 0.0000 | 0.0000 |
| dense_general_eval_03 | general | 64 | -0.0000 | 0.0000 | 0.0000 |
| dense_code_eval_02 | code | 64 | -0.0000 | -0.0000 | -0.0000 |
| dense_code_eval_07 | code | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_general_eval_01 | general | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_general_eval_02 | general | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_general_eval_05 | general | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_general_eval_06 | general | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_general_eval_08 | general | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_math_eval_07 | mathematics | 64 | 0.0000 | -0.0219 | -0.0000 |
| dense_science_eval_03 | science | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_science_eval_04 | science | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_science_eval_05 | science | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_science_eval_06 | science | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_science_eval_07 | science | 64 | 0.0000 | 0.0000 | 0.0000 |
| dense_code_eval_07 | code | 128 | 0.0000 | 0.0000 | 0.0000 |
| dense_code_eval_08 | code | 128 | 0.0000 | 0.0000 | 0.0000 |
| dense_general_eval_01 | general | 128 | 0.0000 | 0.0000 | 0.0000 |
| dense_general_eval_02 | general | 128 | 0.0000 | 0.0000 | 0.0000 |
