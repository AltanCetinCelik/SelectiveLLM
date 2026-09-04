# Post-Run Validity Audit

This audit was performed only after all 108 generations and all preregistered statistics were complete. It does not alter a response, score, label, threshold, tie set, or decision-gate result.

## Formal result

The run passes the preregistered `expert_pool_viable` gate:

- routing opportunity: `0.343`, 95% case-bootstrap interval `[0.111, 0.611]`, `n=9`;
- strict empirical-oracle improvements: `5/9`, above the required `3/9`;
- primary specialist in empirical-best tie set: `5/7` (`71.4%`), above the required `60%`.

This is evidence that the four conditions produce meaningfully different fixed-rubric outcomes and that a behavior-aware selector has measurable upside on this benchmark.

## What the gate does not establish

The evidence for clean domain-aligned specialization is weak:

- specialist lift is `0.048` with interval `[-0.250, 0.286]` (`n=7`);
- specialization margin is `0.062` with interval `[-0.250, 0.396]` (`n=6`);
- the primary specialist is the strict sole winner on only `1/7` labeled cases (`14.3%`);
- label oracle and the frozen semantic router both score `0.443`; their paired gain over base is only `0.037` with interval `[-0.194, 0.231]`.

Therefore, this run supports **expert-condition diversity and empirical routing opportunity** more strongly than it supports the semantic domain labels or the current semantic router.

## Evaluator-sensitive cases

Two cases expose limitations in the frozen deterministic rubric:

1. `math_probability`: the math adapter states the correct answer as `\frac{5}{36}`, but the preregistered numeric parser recognizes plain `5/36` and does not parse LaTeX braced fractions. Its formal score remains `0.0`; the code adapter's plain-text `5/36` remains the sole empirical winner.
2. `irrelevant_python`: base answers `Python bivittatus`, while the accepted-answer list contains `Burmese python` but omits that scientific name. ITIS identifies `Python bivittatus` as the Burmese Python. Its formal base score remains `0.0`; science remains the sole empirical winner.

These are retained negative findings about benchmark validity. They are not corrected post hoc. The second case contributes `1/9 = 0.111` to mean routing opportunity; removing that apparent opportunity would leave `0.231` and `4/9` strict improvements, which would still pass the frozen gate. Correctly recognizing the math adapter would improve label alignment but would not reduce that case's empirical-oracle quality.

Taxonomy reference: [ITIS report for Python bivittatus](https://www.itis.gov/servlet/SingleRpt/SingleRpt?anchorLocation=SubordinateTaxa&credibilitySort=Subordinate+Taxa&print_version=SCR&rankName=Subspecies&search_topic=TSN&search_value=1094050&source=from_print).

## Truncation

The 384-token ceiling was reached in `21/108` generations (`19.4%`): `18/27` base generations and `3/27` math generations. Code and science had no truncations. The larger ceiling substantially reduced the earlier 96-token constraint, but truncation still affects comparisons, especially base. No cell was rerun.

## Multi-capability case

For `rlc_python`, base, code, and math tie at `0.400`; science scores `0.000`. The primary code specialist has zero lift, all three specialists are valid expected labels, and specialization margin is correctly `N/A`. This single-adapter diagnostic does not test composition, so it provides no evidence that multi-expert activation would improve multi-capability output.

## Exact conclusion

**Yes, the pool is worth a larger expert-validation and learned/empirical-routing study under the preregistered gate. No, this run does not yet demonstrate robust domain specialization or a quality benefit from the existing semantic router.** The next evidence step should broaden and repair the benchmark before router optimization; cache, composition, and parameter-paging work remain unjustified by this diagnostic alone.
