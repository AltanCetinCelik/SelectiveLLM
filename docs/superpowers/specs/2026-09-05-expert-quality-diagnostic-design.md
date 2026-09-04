# SelectiveLLM v0.1.2 Expert-Quality Diagnostic Design

Date: 2026-09-05
Status: Approved for preregistration

## Question

Does the existing pinned Qwen2.5/LoRI expert pool contain enough measurable specialization and quality diversity for routing to have meaningful upside?

This diagnostic isolates expert quality from routing, caching, and composition. It does not optimize or expand any of those systems.

## Frozen assets

- Base: `Qwen/Qwen2.5-1.5B-Instruct` at `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`
- Code: `uditjain/lori-qwen2.5-1.5b-code` at `e937bbd728f28a441163f94b60ea5a119513e351`
- Math: `uditjain/lori-qwen2.5-1.5b-math` at `f992ab536c07761c67bd46e35c787bb68ea97657`
- Science: `uditjain/lori-qwen2.5-1.5b-science` at `398cf3cc78a3ff8c78c84c3a424da3ba994bdd6f`
- Benchmark cases and evaluator: the nine cases in `real-hero-1.0.0` with `deterministic-rubric-1.0.0`
- Router: the existing `real-hybrid-1.0.0` configuration, unchanged

The existing compatibility preflight must pass before generation. No asset, label, evaluator rule, router setting, or prompt may change after outputs are inspected.

## Generation matrix

Generate every benchmark prompt under four conditions:

1. Base with adapters disabled
2. Code adapter only
3. Math adapter only
4. Science adapter only

Run three technical repetitions per prompt-condition cell for `9 x 4 x 3 = 108` total generations. Use greedy decoding and a fixed ceiling of 384 new tokens for every generation. Do not rerun individual cells based on their outputs.

Conditions run in the fixed order base, code, math, science. Within each condition, cases retain benchmark-definition order and repetitions run 1 through 3. Only one source adapter may be loaded and active in adapter conditions. No multi-adapter composition, cache-policy comparison, prefetching, or routing-controlled generation is permitted.

A generation is `truncated` when it produces exactly 384 new tokens. Because the backend has no other terminating criterion, a shorter generation is recorded as `eos_completed`. Preserve token count and both flags in every raw row.

## Frozen label semantics

- `expected_experts` is the complete ordered expert set from the versioned benchmark and is stored in every row.
- `correct_labeled_expert` is the first member of `expected_experts`.
- Secondary expected experts remain valid and are excluded from `wrong_experts`.
- `wrong_experts` contains only available specialists absent from the full expected set.
- A no-specialist case has no correct labeled expert and uses base for `label_oracle`.
- Label ordering is never modified from observed quality.

## Cell aggregation

The three repetitions are technical repetitions, not independent benchmark samples. First aggregate the three quality scores within each prompt-condition cell. The preregistered cell quality is the arithmetic mean. Also report repetition median, sample standard deviation, minimum, maximum, exact score agreement, EOS count, and truncation count.

All policy lookups and empirical-best decisions use cell-mean quality. No policy may cherry-pick a single repetition.

## Derived policies

- `label_oracle`: primary labeled expert; base for no-specialist cases.
- `semantic_router`: first selected expert from the unchanged router; base on abstention. Preserve the complete selected set and candidate scores separately.
- `empirical_oracle`: maximum cell-mean quality among base, code, math, and science for that case.
- `empirical_best`: preserve every condition tied for the empirical-oracle maximum. Base is a valid winning condition because abstention is part of the routing decision.

Use exact floating-point equality within an absolute tolerance of `1e-12` for empirical-best ties.

## Case-level metrics

For each case with a primary labeled expert:

```text
specialist_lift = quality(primary labeled expert) - quality(base)
```

For each case with at least one wrong expert:

```text
specialization_margin = quality(primary labeled expert) - mean(quality(wrong experts))
```

If all available specialists occur in the expected set, `specialization_margin = N/A`.

For every case:

```text
routing_opportunity = quality(empirical_oracle) - quality(base)
```

Report base, each specialist, label-oracle, semantic-router, and empirical-oracle quality as means over the nine case-level values. Specialist lift is averaged over cases with a primary labeled expert. Specialization margin is averaged only where defined.

## Statistical reporting

The prompt/case is the primary experimental unit. Benchmark-level standard deviation and confidence intervals operate on case-level cell means or case-level paired differences, never on 108 repeated generations.

Use a deterministic percentile bootstrap with seed 42 and 10,000 resamples over cases for 95% confidence intervals. Bootstrap paired case-level differences for specialist lift, specialization margin, routing opportunity, and policy comparisons. Report the sample count used by every aggregate.

Report technical repetition variability separately through within-cell standard deviations, agreement rate, and score range. Do not interpret repeated generations as added benchmark coverage.

## Preregistered decision gate

`empirical_oracle` has a **strong advantage** only if both conditions hold:

- mean routing opportunity is at least `0.10` absolute quality;
- empirical oracle strictly improves over base on at least 3 of 9 cases.

The primary labeled specialist **usually wins** when it appears in the empirical-best tie set for at least 60% of cases that have a primary labeled expert.

Classify the result as:

- **Expert pool viable:** strong empirical-oracle advantage and primary labeled specialists usually win.
- **Label/routing bottleneck:** strong empirical-oracle advantage but primary labeled specialists do not usually win.
- **Expert pool bottleneck:** empirical-oracle advantage is not strong.

The thresholds are diagnostic conventions for this small fixed rubric, not universal research standards.

## Outputs

Write a separate versioned result directory containing:

- manifest and compatibility report;
- exact config and benchmark snapshots;
- 108 raw responses with expected labels, token counts, EOS/truncation, and evaluator details;
- prompt-condition cell aggregates;
- derived policy decisions and empirical-best tie sets;
- summary JSON/CSV with case-level statistics and case-bootstrap intervals;
- a compact expert-specialization matrix and heatmap;
- mismatch examples where the primary labeled specialist is not empirically best;
- a Markdown report answering the decision question and stating limitations.

The implementation is one focused experiment entry point plus pure aggregation helpers and tests. It adds no public CLI/API, router, cache, composition, or paging behavior.

## Failure handling

Compatibility or generation failure fails the diagnostic rather than silently dropping a cell. The run is complete only with exactly 108 raw generations and 36 prompt-condition cells. All null, tied, negative-lift, unexpected-winner, and truncated results are retained.
