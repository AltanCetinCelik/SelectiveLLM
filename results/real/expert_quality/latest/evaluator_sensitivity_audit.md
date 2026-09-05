# Post-Hoc Evaluator Sensitivity Audit

This audit re-scores the existing 108 generations only. It performs no generation,
does not change the preregistered evaluator, and does not modify any formal score,
winner set, manifest, threshold, or decision artifact.

## Alternative evaluator

The sensitivity evaluator makes exactly two semantic corrections identified in the
accepted post-run validity audit:

1. It recognizes the explicit LaTeX answer `\\frac{5}{36}` as the exact numeric
   answer for `math_probability`.
2. It recognizes `Python bivittatus` as a valid Burmese Python answer for
   `irrelevant_python`.

These rules change 9 of 108 generation-level scores: all three math-adapter
repetitions for `math_probability`, and all three base plus all three math-adapter
repetitions for `irrelevant_python`. No other score changes.

## Sensitivity Results

All intervals are 95% case-bootstrap intervals with benchmark case as the
experimental unit and 10,000 resamples at seed 42.

| Quantity | Formal preregistered result | Sensitivity evaluator |
|---|---:|---:|
| Base quality | 0.406 [0.156, 0.672] | 0.517 [0.250, 0.783] |
| Code-adapter quality | 0.526 [0.302, 0.767] | 0.526 [0.302, 0.767] |
| Math-adapter quality | 0.415 [0.211, 0.637] | 0.637 [0.433, 0.839] |
| Science-adapter quality | 0.370 [0.166, 0.611] | 0.370 [0.166, 0.611] |
| Label-oracle quality | 0.443 [0.220, 0.683] | 0.665 [0.452, 0.878] |
| Semantic-router quality | 0.443 [0.220, 0.683] | 0.554 [0.317, 0.793] |
| Empirical-oracle quality | 0.748 [0.543, 0.933] | 0.748 [0.543, 0.933] |
| Specialist lift (`n=7`) | 0.048 [-0.250, 0.286] | 0.190 [-0.179, 0.548] |
| Specialization margin (`n=6`) | 0.062 [-0.250, 0.396] | 0.229 [-0.042, 0.500] |
| Routing opportunity (`n=9`) | 0.343 [0.111, 0.611] | 0.231 [0.056, 0.463] |

Under the sensitivity evaluator, empirical best strictly improves on base in
`4/9` cases, the primary labeled specialist belongs to the empirical-best tie set
in `6/7` labeled cases (85.7%), and it is the sole winner in `1/7` (14.3%).

## Conclusion

The broad conclusion survives. The alternative evaluator still passes the frozen
expert-pool viability thresholds: routing opportunity exceeds 0.10, its interval
remains positive, strict improvements exceed 3 of 9, and the tie-inclusive primary
win rate exceeds 60%.

The interpretation becomes more favorable to label alignment and less favorable
to total routing opportunity, exactly as expected from correcting these two rubric
false negatives. It still does not establish robust domain specialization or a
quality gain from the existing semantic router. The formal preregistered result
remains the result of record; this table is evaluator sensitivity evidence only.
