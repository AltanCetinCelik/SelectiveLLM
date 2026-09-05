# SelectiveLLM Causal Importance Discovery Design

Date: 2026-09-05
Status: Approved for preregistration and implementation

## Research question

Was the previous dense-capacity failure caused by Qwen2.5-1.5B-Instruct lacking
useful separability, or by activation magnitude being a poor proxy for causal
importance?

This milestone changes one experimental variable: the component discovery method.
It compares activation-based and objective-aware gradient-based discovery over
fixed contiguous MLP blocks. It does not add routing, adapters, physical parameter
paging, cache policy, or a VRAM-reduction claim.

- Experiment version: `causal-importance-discovery-1.0.0`
- Discovery schema version: `mlp-block-discovery-1.0.0`
- Mapping schema version: `mlp-contiguous-block-map-1.0.0`
- Metric schema version: `dense-block-causal-nll-1.0.0`

## Immutable prior result

The accepted Dense Capacity Feasibility result is immutable Classification C:
weak or unstable specialization. Its canonical evidence is committed at `93134a1`,
with post-hoc reporting provenance at `a23b1e1`. The input-score hashes are recorded
in `results/real/dense_capacity/latest/posthoc_reporting_audit.json`.

The accepted finding is:

> Activation-magnitude selectivity over individual MLP channels, attention heads,
> and whole layers was not stable enough to produce convincing held-out
> domain-specific causal effects in Qwen2.5-1.5B-Instruct.

This milestone must not edit, replace, reinterpret, or republish those artifacts.
The immutable channel-level activation result is historical context only. It is
not an additional veto in the new decision gate.

## Frozen inputs

- Model and tokenizer: `Qwen/Qwen2.5-1.5B-Instruct`
- Revision: `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`
- Runtime: FP16 model on Apple MPS, evaluation mode, `use_cache=False`
- Adapters: forbidden
- Benchmark: `dense-capacity-mcq-1.0.0`
- Benchmark canonical SHA-256:
  `f4cf067de00d490a036488520768c82a5e0ea7bd0a126946b887fc5fd679d5e0`
- Cases: the same 48 discovery and 32 held-out evaluation questions
- Prompt template and tokenizer-safe option-scoring protocol: unchanged
- Prompt-template SHA-256:
  `91c4e5516b3957c4817b9095c2643dfd21d2c25b1c05d9da6746aa83e149ff74`
- Primary behavioral metric: correct-answer NLL under the restricted four-option
  softmax
- Secondary metric: forced-choice accuracy from those same option scores
- Random seed: 42 unless a baseline-specific seed is listed

The runner verifies all identities and hashes before gradient or causal scoring.
It fails rather than substituting a newer revision, benchmark, tokenizer protocol,
or prompt rendering.

## Preregistration order

1. Commit this specification.
2. Implement deterministic block mappings, discovery, intervention, statistics,
   reporting, and tests without inspecting experimental outputs.
3. Generate the two canonical channel-to-block mapping artifacts and their hashes.
4. Run tests, lint, strict typing, package build, and the invariant-only gradient
   preflight.
5. Commit source and mapping artifacts so the worktree is clean.
6. Execute the complete experiment without inspecting partial importance or held-out
   outcome values.
7. Analyze only after every preregistered cell is present.
8. Publish a canonical `latest` result only from the clean committed source state.

No methodology may change after step 1 unless a stated implementation invariant
genuinely fails. Any required deviation receives a versioned amendment before a
new canonical run; it is not silently patched into an in-progress experiment.

## Scope

Only MLP intermediate capacity is tested. Attention heads and decoder layers are
not repeated. Discovery-time direct block ablation is omitted because thousands
of additional discovery probes would change the research question and materially
expand scope.

The experiment has two block sizes:

- 64 channels: preregistered primary analysis; it alone determines A/B/C.
- 128 channels: mandatory corroborative analysis; it cannot alter A/B/C.

The two block sizes are always reported separately and never pooled. A preferred
block size cannot be selected after held-out results are observed.

## Deterministic contiguous blocks

The Qwen MLP intermediate dimension is 8,960 channels in each of 28 layers.
Channels use zero-based half-open intervals.

### 64-channel primary blocks

- Blocks per layer: 140
- Block `b`: channels `[64*b, 64*(b+1))`
- Per-layer selected-block quota: `[7, 7, ..., 7]` with 28 entries
- Selected blocks: 196 total
- Selected channels: `196 * 64 = 12,544`
- Fraction of all MLP layer-channels: `12,544 / 250,880 = 0.05`

### 128-channel corroborative blocks

- Blocks per layer: 70
- Block `b`: channels `[128*b, 128*(b+1))`
- Zero-based even layers: select exactly 4 blocks
- Zero-based odd layers: select exactly 3 blocks
- Per-layer quota vector: `[4, 3, 4, 3, ..., 4, 3]` with 28 entries
- Selected blocks: `14*4 + 14*3 = 98`
- Selected channels: `98 * 128 = 12,544`
- Fraction of all MLP layer-channels: `12,544 / 250,880 = 0.05`

The 4/3 assignment is fixed by layer parity before importance exists. No domain,
discovery method, gradient, activation, or model output may change it.

Each mapping artifact contains its schema version, block size, every channel range,
the exact quota vector, total candidate blocks, total selected blocks, total
selected channels, total fraction, and mask semantics. Its hash is SHA-256 over
canonical JSON encoded with sorted keys and compact separators. Validation requires
that every channel belongs to exactly one block with no gap or overlap.

Every same-domain, wrong-domain, random, activation-selected, gradient-informed,
global-high, and global-low mask at a given block size has exactly the same
per-layer quota vector. Each mask records its mapping hash and quota-pattern hash.

## Forced-choice objective

The user prompt, chat rendering, candidate token IDs, and restricted four-option
softmax are identical to the immutable experiment. For option logits `z` and the
correct label `y`:

```text
correct_nll = -log_softmax(z[A], z[B], z[C], z[D])[y]
```

The four option logits are cast to FP32 before `log_softmax`. Lower correct NLL is
better. Forced-choice prediction is the deterministic argmax of these same four
scores. No answer is generated or separately graded.

## Gradient path and captured tensor

The exact intervention target remains the tensor entering each decoder layer's
`mlp.down_proj`, after gated MLP activation and before output projection. The
gradient must be taken with respect to that exact tensor.

For each prompt:

1. Compute input embeddings, detach them, and enable gradients on the detached
   embedding tensor.
2. Keep every model parameter frozen with `requires_grad=False`.
3. Forward with `inputs_embeds`, the ordinary attention mask, and `use_cache=False`.
4. Capture and retain gradients for the input to all 28 `down_proj` modules.
5. Compute the same correct-answer NLL and perform exactly one backward pass.
6. Read activation and gradient tensors without accumulating parameter gradients.

Before discovery, this path must reproduce ordinary `input_ids` scoring within
`1e-4` for each option logit and correct NLL and must preserve the prediction. The
model remains in evaluation mode.

For every discovery prompt and layer, the captured activation and gradient must:

- have identical shape;
- have batch size 1 and the exact prompt sequence length;
- have channel dimension exactly 8,960;
- contain only finite values.

Any violation aborts the case and therefore the run. Tensors are never reshaped or
reinterpreted to make a failed invariant pass.

## Eligible tokens

The eligible-token mask is exactly the immutable discovery definition: every
non-padding, non-special prompt token from the rendered prompt participates. The
answer label is not appended. The eligible mask must match the captured sequence
dimension exactly.

## Raw channel summaries

Model activations and gradients are cast to FP32 before multiplication and
aggregation. No clipping, replacement, smoothing, or gradient normalization is
applied.

For prompt `p`, layer `l`, eligible token `t`, and channel `j`, preserve these raw
per-channel summaries:

```text
activation_channel[p,l,j] = mean_t(abs(a[p,l,t,j]))

gradient_absolute_channel[p,l,j] =
  mean_t(abs(a[p,l,t,j] * d(correct_nll)/d(a[p,l,t,j])))

gradient_signed_channel[p,l,j] =
  mean_t(-a[p,l,t,j] * d(correct_nll)/d(a[p,l,t,j]))
```

The negative sign in the signed quantity represents the local first-order change
from setting the activation to zero. The signed quantity is diagnostic only.

One backward pass produces the underlying channel values used by both block-size
experiments. Separate gradient measurements by block size are forbidden.

## Raw block aggregation

For either mapping, raw block scores are sums of their raw channel summaries:

```text
activation_block[p,l,b] = sum_j_in_block activation_channel[p,l,j]

gradient_absolute_block[p,l,b] =
  sum_j_in_block gradient_absolute_channel[p,l,j]

gradient_signed_block[p,l,b] =
  sum_j_in_block gradient_signed_channel[p,l,j]
```

Thus the primary gradient score is exactly:

```text
mean_over_eligible_tokens(
  sum_over_block_channels(abs(activation * gradient(correct_nll)))
)
```

The activation baseline is the parallel quantity:

```text
mean_over_eligible_tokens(sum_over_block_channels(abs(activation)))
```

Raw channel and raw block values are preserved before normalization.

## Shared percentile normalization

Activation and absolute gradient block discovery share one implementation. For
every prompt and layer independently:

- 64-channel analysis ranks its 140 raw block scores.
- 128-channel analysis ranks its 70 raw block scores.
- The lowest block has rank origin 0.
- Stable ascending sort uses block index to break exact ties.
- Percentile is `rank / (block_count - 1)`.
- The result therefore lies in `[0, 1]`.

Percentile ranking happens only after channel contributions are aggregated into
blocks. Raw magnitudes cannot influence another layer. Held-out data cannot
influence normalization, ranking, or tie resolution.

The signed diagnostic is not normalized for selection and never enters any
ranking, mask, threshold, or gate.

## Discovery rankings

Only the 48 discovery prompts contribute to rankings. Activation discovery uses
normalized `activation_block`; gradient discovery uses normalized
`gradient_absolute_block`.

For discovery method `m`, domain `d`, and layer-local block `c`:

```text
selectivity(m,d,c) =
  (mean_rank(m,d,c) - mean_rank(m,not_d,c))
  / sqrt(0.5 * (variance(m,d,c) + variance(m,not_d,c)) + 1e-6)
```

The domain-selectivity contrast is retained exactly as calculated and may be
positive or negative. No absolute value is applied after contrast. Higher positive
values identify blocks disproportionately important or active for the target
domain. This contrast is distinct from the diagnostic-only signed first-order
quantity.

Global importance for each method and block size is the mean normalized block rank
over all 48 discovery prompts. Global-high selects the highest scores and
global-low selects the lowest scores under the same per-layer quota.

Stable sorting and block index break ranking ties. No held-out outcome enters a
ranking or mask.

## Discovery stability

The same 20 stratified split-halves and seed 42 are used for both methods and both
block sizes. Each repetition uses the same split assignment across all four
method-size combinations. Every domain's 12 discovery prompts are divided into two
groups of six.

For every method, size, and domain report:

- all split-half top-mask Jaccards and their median;
- all split-half full-ranking Spearmans and their median;
- mean prompt-level top-mask overlap within domain;
- mean prompt-level top-mask overlap across domains;
- within-minus-across overlap;
- pairwise overlap among the four domain masks;
- selected-block layer histogram.

A domain is stable only when all hold:

- median split-half top-mask Jaccard is at least `0.20`;
- median split-half ranking Spearman is at least `0.30`;
- within-minus-across prompt-level Jaccard is at least `0.05`.

A method-size combination is stable when at least three of four domains are stable.

For the primary 64-channel analysis, gradient discovery has improved stability
relative to activation discovery when at least one holds:

1. gradient has a strictly higher stable-domain count; or
2. stable-domain counts are equal, and both:
   - the median across the four domain-level median split-half Jaccards is strictly
     higher for gradient;
   - the median across the four domain-level median ranking Spearmans is strictly
     higher for gradient.

The immutable channel-level activation stability is shown as historical context
but is not part of this Boolean or any A/B/C veto.

## Mask families

All causal masks have `mask_semantics: ABLATE_SELECTED`: selected block channels
are zeroed at the exact `down_proj` input while unselected channels remain active.

For each block size construct:

- four activation-selectivity domain masks;
- activation global-high and global-low masks;
- four gradient-selectivity domain masks;
- gradient global-high and global-low masks;
- five structurally matched random masks with seeds 42 through 46;
- one zero-size no-op mask.

Random and no-op controls are shared between discovery methods at a block size.
Global masks are method-specific. For 128-channel masks, every family uses the
fixed even-layer 4 / odd-layer 3 quota. Random sampling occurs independently within
each layer under the frozen quota.

Each mapping therefore has 18 unique masks: 12 method-specific, five random, and
one no-op. Every one of the 32 held-out cases is scored under every mask, yielding
576 masked rows per size and 1,152 masked rows total, plus 32 newly scored full-model
rows.

## Held-out causal evaluation

The 32 held-out questions are scored only after mappings, discovery values,
rankings, stability results, and masks are complete and saved. Mask definitions
cannot be revised after held-out scoring begins.

For each held-out question, block size, and discovery method compare:

- full model;
- same-domain discovery mask;
- each of the three wrong-domain masks;
- all five shared random masks;
- method-specific global-high mask;
- method-specific global-low mask;
- no-op.

Every score preserves all four logits, normalized probabilities, correct NLL,
prediction, correctness, latency, method, block size, mapping hash, quota hash,
mask hash, source domain, and mask semantics.

For mask `k` and case `i`:

```text
damage[k,i] = correct_nll[k,i] - correct_nll[full,i]
```

Positive damage means ablation harmed the correct answer.

Before benchmark aggregation, calculate per-question control means:

```text
wrong_damage[i] = mean(damage of three wrong-domain masks)
random_damage[i] = mean(damage of five random masks)
```

Primary paired quantities are:

```text
same_minus_random = gradient_same_damage - random_damage
same_minus_wrong = gradient_same_damage - gradient_wrong_damage
same_minus_global_high = gradient_same_damage - gradient_global_high_damage
same_minus_global_low = gradient_same_damage - gradient_global_low_damage
gradient_same_minus_activation_same =
  gradient_same_damage - activation_same_damage
```

Activation-method versions of the control comparisons are also reported. Absolute
NLL and forced-choice accuracy are reported for every condition.

## Statistical protocol

The held-out question is the primary experimental unit. The three wrong masks and
five random seeds are technical controls, not independent benchmark samples.

Use 10,000 percentile bootstrap resamples with seed 42:

- pooled intervals resample eight questions within each of the four domains and
  concatenate the stratified samples;
- domain intervals resample that domain's eight questions;
- direct activation-versus-gradient intervals resample paired per-question
  differences, never independent method samples.

Report sample count, mean, median, standard deviation, p50, p95, and 95% interval
where meaningful. Report the complete effect distributions. No result is pooled
across 64- and 128-channel mappings.

## Signed first-order held-out diagnostic

After discovery masks are frozen, perform one gradient pass for each held-out
question using the same correct-NLL objective and tensor invariants. Aggregate:

```text
predicted_signed_damage[mask,case] =
  mean_over_eligible_tokens(
    sum_over_selected_channels(-activation * gradient(correct_nll))
  )
```

The already frozen selected masks are used. No signed value may change selection,
tie-breaking, normalization, thresholding, causal results, or classification.
There are 17 non-noop masks per block size, so the signed diagnostic contains
`17 * 2 * 32 = 1,088` mask-case rows derived from exactly 32 held-out backward
passes.

Compare predicted signed damage with observed ablation damage using:

- sign agreement rate, with exact zeros reported separately;
- Spearman rank association;
- Pearson linear association.

These are diagnostics of a local linear approximation, not independent causal
evidence. Agreement or disagreement cannot reinterpret a failed gate.

## Calibration and validity gates

The run is interpretable only if all hold:

- immutable model, revision, benchmark, split, prompt, and tokenizer hashes match;
- no PEFT wrapper or adapter is present;
- full-model accuracy is at least 50%;
- correct answer positions remain exactly balanced;
- gradient-mode option logits and correct NLL reproduce ordinary scoring within
  `1e-4`, with identical predictions;
- repeated ordinary scoring of the eight immutable sentinels is stable within
  `1e-4` and preserves predictions;
- activation and gradient shapes are identical and end in 8,960 channels at all
  28 layers for every gradient case;
- all raw, normalized, logit, probability, NLL, damage, and signed values are
  finite;
- every probability distribution has four entries summing to one within `1e-6`;
- both mappings cover all 8,960 channels per layer exactly once;
- every non-noop mask selects exactly its frozen per-layer quota and 12,544 total
  channels;
- every no-op mask reproduces all 32 full-model NLL values within `1e-4` and
  preserves predictions;
- the discovery matrix, 32 full rows, 1,152 masked rows, 1,088 signed diagnostic
  rows, and all required method-size-control combinations are complete;
- signed diagnostics are absent from every mask-construction and gate input.

A scientific validity failure is preserved and classified C with qualifier
`validity_failure`. Infrastructure failure, nonfinite gradients, structural
mismatch, missing cells, or ambiguous provenance marks the run `failed` and
prevents interpretation.

## Primary 64-channel decision gate

Thresholds are diagnostic conventions for this preregistered experiment, not
universal significance claims. Continuous effects and near-threshold results remain
primary evidence.

Only the 64-channel experiment determines A/B/C.

### Outcome A: objective-aware discovery succeeds

All must hold:

- every validity gate passes;
- gradient discovery is stable in at least three of four domains;
- gradient discovery has improved stability relative to 64-channel activation
  discovery under the frozen rule above;
- pooled gradient same-domain damage is at least `0.10` NLL;
- pooled gradient same-minus-random is at least `0.05`, with its 95% interval lower
  bound strictly above zero;
- pooled gradient same-minus-wrong is at least `0.05`, with its 95% interval lower
  bound strictly above zero;
- pooled gradient same-minus-global-high is positive, with its 95% interval lower
  bound strictly above zero;
- gradient same-domain mean damage exceeds random, wrong, gradient global-high,
  and gradient global-low mean damage in at least three of four domains;
- pooled gradient-selected same-domain damage exceeds activation-selected
  same-domain damage by at least `0.05`, with its 95% interval lower bound strictly
  above zero.

Outcome A supports both that objective-aware discovery is better than activation
magnitude and that the discovered capacity is domain-specific rather than merely
globally important. The next milestone may expand validation and investigate a
shared core or physically plausible block residency, but it still does not prove
memory reduction.

### Outcome B: stable but mostly shared importance

All must hold:

- every validity gate passes;
- 64-channel gradient discovery is stable in at least three of four domains;
- pooled gradient same-domain damage is at least `0.10` NLL;
- pooled gradient same-minus-random is at least `0.03`, with its 95% interval lower
  bound strictly above zero;
- Outcome A fails;
- at least one shared-core indicator holds:
  - wrong-domain mean damage is at least 75% of same-domain mean damage;
  - gradient global-high mean damage is at least 75% of same-domain mean damage;
  - mean pairwise overlap among gradient domain masks is at least `0.20`.

Outcome B supports stable objective-aware importance but not semantic paging. The
next research step is a shared-resident core plus a smaller dynamic tail.

### Outcome C: still weak or unstable

Any valid primary result satisfying neither A nor B is Outcome C. A scientific
validity failure is C with `validity_failure`.

If C occurs, discovery-method tuning on Qwen2.5-1.5B stops. The next controlled
variable is model scale, using the strongest preregistered discovery method on a
larger dense model that fits available hardware. No pager is built.

## Corroborative 128-channel interpretation

The complete 128-channel experiment reports the same discovery, stability, causal,
control, and signed-diagnostic metrics separately. It has no A/B/C vote and no
implicit rescue gate.

Its effect-by-effect concordance table shows 64- and 128-channel point estimates,
intervals, and signs for all primary quantities. Narrative terms such as
`corroborating`, `weakening`, or `contradictory` are descriptive summaries of that
table only:

- a positive 128-channel result cannot rescue a failed 64-channel primary result;
- a negative 128-channel result cannot automatically invalidate a positive
  64-channel result;
- every disagreement must be stated explicitly;
- no combined effect estimate or post-hoc preferred block size is permitted.

## Artifacts

A separate real-backend result directory stores:

- manifest, benchmark fingerprint, environment, source commit, source-dirty state,
  package versions, and exact config;
- immutable-input verification and tokenizer validation;
- mapping definitions, channel ranges, quota vectors, mapping hashes, and
  quota-pattern hashes;
- gradient-path equivalence and runtime preflight validation;
- raw FP32 per-prompt channel summaries for activation, absolute gradient, and
  signed gradient contribution;
- raw 64- and 128-channel block aggregates before normalization;
- normalized values, activation and gradient rankings, masks, hashes, and layer
  histograms;
- split-half assignments, stability distributions, and overlap matrices;
- every full and masked held-out logit, probability, NLL, prediction, and latency;
- paired causal effects, control means, direct method differences, descriptive
  statistics, and bootstrap samples or reproducible bootstrap metadata;
- signed first-order diagnostic rows and association summaries;
- separate 64- and 128-channel tables and plots;
- failure analysis and a report answering the research question;
- explicit labels: `real dense model`, `logical masking`, and
  `no measured VRAM reduction`.

Raw channel arrays may use compressed NumPy storage, but case order, shape, dtype,
and semantic keys must be explicit and hashed.

## Provenance and publication

The run manifest records the exact source Git commit and whether the worktree was
clean at execution start. A canonical publishable run must originate from a clean,
committed source state.

If the worktree is dirty:

- preserve `dirty=true` and the status output in provenance;
- allow diagnostic execution only;
- never publish that run as canonical `latest` evidence.

Completed summaries compare only artifacts with compatible backend, model revision,
benchmark hash, prompt hash, mapping hash, quota hash, discovery schema, metric
schema, seed policy, device class, and measurement semantics.

## Failure handling

The runner creates a timestamped run directory and a `running` manifest before
model access. When technically possible, failures preserve the manifest, completed
preflight records, progress counters, partial artifact hashes, exception type, and
error message. Failed or incomplete runs are never silently removed, never included
in completed-result summaries, and never published to `latest`.

Partial scientific output is not interpreted. A rerun receives a new run ID.

## Testing and preflight

Before the canonical run:

- unit-test mapping coverage, boundaries, nonoverlap, and stable hashes;
- unit-test both quota vectors and exact 12,544-channel totals;
- unit-test channel-to-block aggregation for both mappings from one shared tensor;
- unit-test percentile denominator, zero-based rank origin, and stable tie behavior;
- unit-test discovery contrasts, structurally matched masks, and random seeds;
- unit-test paired control averaging, bootstrap case units, improved-stability rule,
  and A/B/C gates;
- unit-test that signed diagnostics cannot enter mask or gate schemas;
- run repository tests, Ruff, strict mypy, and package build;
- run one invariant-only gradient preflight on the first canonical discovery case.

The preflight may inspect only equivalence tolerances, tensor shapes, finiteness,
mapping coverage, and hook event counts. It does not inspect or retain domain
rankings or held-out outcomes.

## Estimated runtime and storage

The design uses 48 discovery backward passes, 32 held-out diagnostic backward
passes, 32 full-model scores, and 1,152 masked held-out scores. Expected runtime on
the recorded Apple MPS environment is approximately 20 to 40 minutes.

Expected artifacts are approximately 150 to 300 MB, dominated by compressed raw
channel summaries. Memory telemetry describes real unified-memory allocation only.
Logical masks do not unload weights and are never reported as VRAM savings.

## Required conclusion

The final report must answer only:

> Was the previous failure caused by the model lacking useful separability, or by
> activation magnitude being a poor proxy for causal importance?

Negative, tied, unstable, contradictory, and near-threshold results are preserved.
The benchmark and thresholds are never tuned to obtain a positive conclusion.
