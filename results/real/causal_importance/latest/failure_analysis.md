# Failure Analysis

Real dense-model NLL under logical contiguous-block masking; no memory claim.

| Case | Domain | Blocks | Gradient - activation | Same - random | Same - wrong |
|---|---|---:|---:|---:|---:|
| dense_general_eval_07 | general | 64 | -5.8343 | -3.0876 | -1.9136 |
| dense_code_eval_01 | code | 64 | -4.7248 | -0.2373 | -0.6483 |
| dense_math_eval_02 | mathematics | 128 | -3.2293 | 0.6294 | 0.5214 |
| dense_math_eval_06 | mathematics | 128 | -3.1512 | -1.5440 | -3.2886 |
| dense_math_eval_02 | mathematics | 64 | -2.8401 | -4.5332 | -4.4491 |
| dense_math_eval_08 | mathematics | 128 | -2.8028 | -1.4008 | -0.2981 |
| dense_math_eval_03 | mathematics | 64 | -2.7892 | -1.6241 | -0.2959 |
| dense_math_eval_08 | mathematics | 64 | -1.8155 | -0.2337 | -0.6424 |
| dense_code_eval_04 | code | 128 | -1.5413 | 0.0189 | 0.0196 |
| dense_code_eval_05 | code | 64 | -1.5029 | -0.3590 | -0.7694 |
| dense_math_eval_05 | mathematics | 128 | -1.4213 | -3.3482 | -1.2003 |
| dense_math_eval_06 | mathematics | 64 | -0.9967 | 2.2394 | 2.0562 |
| dense_code_eval_05 | code | 128 | -0.5396 | -0.3292 | -0.1277 |
| dense_code_eval_03 | code | 128 | -0.4074 | 0.5364 | -0.2069 |
| dense_code_eval_03 | code | 64 | -0.3387 | -1.3978 | -1.4135 |
| dense_math_eval_07 | mathematics | 64 | -0.2581 | -0.0013 | -0.0005 |
| dense_math_eval_03 | mathematics | 128 | -0.1570 | 1.2777 | 1.7334 |
| dense_math_eval_04 | mathematics | 128 | -0.0947 | 2.2922 | 2.9082 |
| dense_science_eval_01 | science | 128 | -0.0390 | -0.2031 | -0.9231 |
| dense_code_eval_04 | code | 64 | -0.0104 | -0.2526 | -0.1576 |
| dense_math_eval_07 | mathematics | 128 | -0.0040 | -0.0007 | -0.0002 |
| dense_science_eval_08 | science | 64 | -0.0022 | -0.0013 | 0.0005 |
| dense_science_eval_07 | science | 128 | -0.0018 | -0.0029 | -0.0010 |
| dense_science_eval_07 | science | 64 | -0.0015 | -0.0003 | -0.0005 |
| dense_general_eval_06 | general | 128 | -0.0008 | 0.0000 | 0.0000 |
| dense_general_eval_04 | general | 128 | -0.0003 | -0.0001 | -0.0000 |
| dense_science_eval_04 | science | 64 | -0.0002 | 0.0015 | 0.0018 |
| dense_general_eval_03 | general | 128 | -0.0002 | -0.0001 | -0.0000 |
| dense_science_eval_06 | science | 128 | -0.0001 | 0.0000 | 0.0000 |
| dense_code_eval_07 | code | 64 | -0.0001 | -0.0001 | -0.0000 |
| dense_general_eval_08 | general | 64 | -0.0001 | -0.0000 | -0.0000 |
| dense_science_eval_04 | science | 128 | -0.0001 | 0.0001 | 0.0000 |
