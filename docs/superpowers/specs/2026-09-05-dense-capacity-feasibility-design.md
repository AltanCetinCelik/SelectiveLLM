# SelectiveLLM Dense-Capacity Feasibility Design

Date: 2026-09-05
Status: Approved for preregistration and benchmark construction

## Research question

Is there stable, causally useful, prompt-dependent capacity inside one dense pretrained transformer at a granularity that could plausibly be routed later?

This milestone is a feasibility experiment, not a routing framework or memory benchmark. It adds no adapters, training, physical parameter paging, cache policy, or VRAM-reduction claim.

## Preregistration order

The execution order is fixed:

1. Commit this experimental specification.
2. Create the complete 80-question benchmark without running the model or tokenizer.
3. Validate answer correctness, domain assignments, option-position balance, split separation, and duplicate-template constraints.
4. Version and hash the benchmark and validation report, then commit both.
5. Test the exact rendered prompt against the pinned tokenizer and commit the resolved option token IDs in the run manifest.
6. Only then run model scoring, trace activations, calculate selectivity, create masks, or inspect model outputs.

After step 4, questions, options, domains, split assignments, template families, and expected answers are immutable.

Before this sequence was requested, a design-only feasibility check loaded the pinned model and timed one synthetic binary-search multiple-choice prompt. It printed token count, literal option token IDs, timing, and allocated memory. No logits or activation values were printed, inspected, or retained. The future benchmark must exclude that question and close variants.

## Frozen model and environment

- Model and tokenizer: `Qwen/Qwen2.5-1.5B-Instruct`
- Immutable revision: `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`
- Architecture: Qwen2 causal language model, 28 decoder layers, hidden size 1,536, intermediate size 8,960, 12 query heads per layer, head dimension 128
- Runtime: PyTorch inference mode, FP16, Apple MPS, `use_cache=False`
- Adapters: none; the runner must fail if it observes a PEFT wrapper or loaded adapter
- Random seed: 42 unless a baseline-specific seed is listed below

Package versions, hardware, source commit, source-dirty state, model revision, tokenizer revision, benchmark hash, metric schema, and all mask definitions are recorded in the run manifest and benchmark fingerprint.

## Frozen benchmark design

The benchmark has 80 independent four-option questions:

| Domain | Discovery | Held-out evaluation | Total |
|---|---:|---:|---:|
| Code | 12 | 8 | 20 |
| Mathematics | 12 | 8 | 20 |
| Electrical/scientific reasoning | 12 | 8 | 20 |
| General/control | 12 | 8 | 20 |
| **Total** | **48** | **32** | **80** |

Within every domain and split, correct answer positions are exactly balanced: each of A, B, C, and D occurs three times in discovery and twice in evaluation. Option order is frozen in the benchmark.

Every case stores a unique ID, split, domain, question, four options, correct label, concise rationale, and template-family ID. Discovery and evaluation may cover related skills but may not share numerical substitutions, code snippets, named scenarios, distinctive wording, or template-family IDs.

Exactly eight evaluation cases, the first two canonical case IDs in each domain, are marked as numerical-stability sentinels before the benchmark commit. Sentinel membership cannot depend on model behavior.

### Pre-model benchmark validation

Validation runs without importing Transformers or loading the tokenizer or model. It must verify:

- exactly 80 unique IDs and the fixed domain/split counts;
- exactly four nonempty options and one valid answer per case;
- exact answer-position balance in each domain and split;
- no repeated template-family ID across discovery and evaluation;
- no normalized duplicate question or question-plus-options text;
- no cross-split pair above a preregistered token 5-gram Jaccard threshold of `0.65` after removing the fixed answer instruction;
- every rationale explicitly identifies why the keyed answer is correct;
- deterministic answer checks for executable code-output and arithmetic cases where applicable;
- a recorded manual correctness review for scientific and general-knowledge cases.

The benchmark version is `dense-capacity-mcq-1.0.0`. Its canonical JSON representation and validation report receive SHA-256 hashes. Both hashes are committed before any tokenizer or model operation.

## Tokenizer-safe forced-choice protocol

Every condition uses the identical question and options. The only user message is rendered as:

```text
Choose the correct answer.

{question}

A. {option_a}
B. {option_b}
C. {option_c}
D. {option_d}

Respond with exactly one option label: A, B, C, or D.
```

The pinned tokenizer renders this message with its exact chat template and `add_generation_prompt=True`. At the resulting scored position, the evaluator appends each candidate label separately and verifies that:

- the candidate encoding extends the exact rendered prefix by one token;
- the four appended token IDs are distinct;
- no candidate retokenizes the prefix boundary;
- the tokenized prefix matches the IDs used for the model forward pass.

Failure of any invariant aborts the experiment. The four resolved token IDs and rendered-template hash are saved in the manifest. Token IDs are never inferred from context-free `encode("A")` calls.

For one model forward pass, the evaluator reads the four candidate logits at the final prefix position and applies a restricted four-option softmax. It records all four raw logits, all four normalized probabilities, and their sum check.

```text
correct_nll = -log(restricted_probability(correct_label))
prediction = deterministic argmax of the same four option scores
causal_damage(mask, case) = correct_nll(masked) - correct_nll(full_model)
```

Lower absolute NLL is better. Positive causal damage means the intervention hurt the correct answer. Forced-choice accuracy is secondary and comes from the same option scores; no answer is separately generated or graded.

## Discovery activity tracing

Tracing uses only the 48 discovery prompts with no answer label appended. All non-padding, non-special prompt tokens participate. The fixed instruction and options remain part of every prompt and therefore cannot vary by intervention.

### MLP channels

At each layer, a pre-hook on `mlp.down_proj` observes the gated intermediate tensor `silu(gate_proj(x)) * up_proj(x)`. Per-channel activity is mean absolute activation over eligible prompt tokens. There are 8,960 channels per layer and 250,880 layer-channel components.

### Attention-head outputs

At each layer, a pre-hook on `self_attn.o_proj` observes the concatenated post-attention query-head outputs. The tensor is reshaped into 12 heads of dimension 128. Per-head activity is RMS output over eligible prompt tokens and head dimensions. There are 336 layer-head components.

The runner validates the observed last dimension as `12 x 128 = 1,536`; otherwise head experiments fail rather than reinterpret the tensor.

### Decoder layers

Pre- and post-hooks measure each decoder layer's residual update. Activity is the RMS of `layer_output - layer_input` over eligible tokens and hidden dimensions. There are 28 layer components.

### Normalization and selectivity

For MLP channels and heads, raw activity is converted to percentile rank within each prompt and layer. Layer activity is percentile-ranked across the 28 layers within each prompt. This prevents absolute scale differences among layers or component types from creating apparent specialization.

For component `c` and domain `d`, discovery-only selectivity is:

```text
selectivity(d, c) =
  (mean_rank_activity(d, c) - mean_rank_activity(not_d, c))
  / sqrt(0.5 * (variance(d, c) + variance(not_d, c)) + 1e-6)
```

Global importance is mean within-group activity percentile over all 48 discovery prompts. Held-out scores and intervention outcomes never enter rankings or masks.

## Stability analysis

Twenty deterministic stratified split-halves use seed 42. Every split divides each domain's 12 discovery prompts into two groups of six and recomputes selectivity independently.

For each domain and granularity, report:

- split-half top-mask Jaccard distribution and median;
- split-half full-ranking Spearman distribution and median;
- mean pairwise prompt-level top-mask Jaccard within the domain;
- mean prompt-level top-mask Jaccard across domains;
- within-minus-across overlap;
- selected-component layer histogram;
- pairwise overlap among the four domain masks.

A domain selection is stable when all hold:

- median split-half top-mask Jaccard is at least `0.20`;
- median split-half Spearman is at least `0.30`;
- within-minus-across prompt-level Jaccard is at least `0.05`.

A granularity is stable when at least three of four domains are stable.

## Initial causal ablation

Initial interventions always mean `ABLATE_SELECTED`: selected components are removed while all unselected capacity remains active.

- MLP: zero selected coordinates in each `down_proj` input. Select exactly 448 of 8,960 channels in every layer, for 12,544 total channels or 5% per layer.
- Heads: zero selected 128-dimensional slices in each `o_proj` input. Select exactly one of 12 heads in every layer, for 28 heads total.
- Layers: replace each selected layer output with its original residual input. Select exactly 7 of 28 complete layers.

Every mask artifact contains `mask_semantics: ABLATE_SELECTED`, granularity, source, domain if applicable, source split, exact indices, per-layer counts, component count, fraction, and content hash.

### Equal-structure causal conditions

For every held-out question and granularity, score:

1. Full model
2. Same-domain discovery-selected ablation
3. Each of the three other-domain discovery-selected ablations
4. Five random ablations with seeds 42 through 46
5. Globally low-importance ablation
6. For MLP only, globally high-importance ablation as an additional exploratory baseline
7. Zero-size no-op ablation

Wrong-domain damage is reported separately for all three masks and summarized as their per-question mean. Random damage is reported for all five masks and summarized as its per-question mean.

Structure is exactly matched:

- every MLP mask selects 448 channels in every layer;
- every head mask selects one head in every layer;
- every layer mask selects seven complete layers;
- random masks are sampled under those same per-layer quotas;
- low- and high-importance masks use the same quotas;
- wrong-domain masks inherit the identical quota of their granularity.

The high-global-importance MLP baseline is not part of the A/B/C gate. It tests whether domain selectivity differs from generic importance.

## Statistical protocol

The held-out question is the primary experimental unit. All causal comparisons are paired against that question's full-model NLL:

```text
same_minus_random = damage(same_domain) - mean_damage(five_random_masks)
same_minus_wrong = damage(same_domain) - mean_damage(three_wrong_domain_masks)
same_minus_low = damage(same_domain) - damage(low_importance)
```

Report absolute NLL and accuracy for every condition, paired damage for every observation, domain-level effects, pooled effects, effect distributions, and all three paired comparisons. Use 10,000 percentile bootstrap resamples with seed 42. Pooled intervals use stratified resampling within each domain; domain intervals resample that domain's eight held-out questions.

No mask is selected, rejected, or revised using held-out NLL.

## Calibration and validity gates

Before interpreting interventions:

- full-model accuracy over 32 held-out questions must be at least `50%`, materially above random-choice accuracy of 25%;
- answer positions must remain exactly balanced;
- three repeated unmasked scores for eight fixed sentinel evaluation cases must agree within `1e-4` correct-answer NLL and must produce identical forced-choice predictions;
- the zero-size no-op mask must reproduce every held-out baseline within `1e-4` NLL and preserve every prediction;
- each option distribution must contain four finite probabilities summing to one within `1e-6`;
- every completed run must contain all preregistered cases and mask conditions.

A failed validity gate is preserved and reported. It prevents classification A and produces classification C with a `validity_failure` qualifier unless the failure is infrastructural, in which case the run is failed rather than interpreted.

## Diagnostic decision gate

Thresholds are diagnostic conventions for this experiment, not universal significance estimates. Continuous effects and near-threshold results remain primary evidence.

### A: Stable causal specialization

All must hold:

- validity gates pass;
- MLP or attention-head masks are stable in at least three domains;
- pooled same-domain causal damage is at least `0.10` NLL;
- pooled same-minus-random and same-minus-wrong damage are each at least `0.05` NLL;
- the paired 95% bootstrap interval for each of those two advantages excludes zero on the positive side;
- same-domain mean damage exceeds random, wrong-domain, and low-importance mean damage in at least three of four domains;
- one additional granularity has positive pooled same-minus-random damage.

If A holds, the next milestone may investigate grouping the implicated components into physically pageable blocks.

### B: Strong shared core plus some specialized tail

All must hold:

- validity gates pass;
- at least one MLP, attention-head, or layer granularity has pooled same-domain damage of at least `0.05` NLL;
- its pooled same-minus-random damage is at least `0.03` NLL with a paired 95% interval excluding zero on the positive side;
- its pooled same-minus-wrong point estimate is positive, but A is not satisfied;
- either wrong-domain mean damage is at least 50% of same-domain mean damage or mean pairwise overlap among domain masks is at least `0.20`.

A layer-only signal can support B but cannot support A. If B holds, a later milestone should test a shared-resident core plus a smaller selectable tail.

### C: Weak or unstable specialization

Any valid result not satisfying A or B is C. A validity failure is C with a qualifier. No physical pager is built from C; the next step must change granularity, model, benchmark, or methodology.

If multiple granularities differ, report each result separately. The overall classification follows these rules without selecting the largest held-out effect post hoc.

## Conditional capacity-retention curve

Run this stage only if the initial causal result is A or B. Select the granularity by fixed priority among those meeting the relevant signal requirements: MLP, then heads, then layers. Do not select the granularity by largest held-out effect.

Retention interventions always mean `RETAIN_SELECTED`: selected components remain active and the complement at that granularity is suppressed. Retention masks are separate artifacts and types from ablation masks. Every artifact records `mask_semantics: RETAIN_SELECTED`.

Test retained fractions 100%, 75%, 50%, and 25%:

- MLP retains 8,960, 6,720, 4,480, or 2,240 channels per layer;
- heads retain 12, 9, 6, or 3 heads per layer;
- layers retain 28, 21, 14, or 7 complete layers.

At each fraction compare full or no-op capacity, same-domain selectivity, each wrong-domain selection, five structurally matched random selections, and global-importance selection. Report absolute NLL, paired NLL degradation, forced-choice accuracy, and quality retention. Logical masking is not VRAM reduction.

## Artifacts and failure handling

The run writes a separate real-backend result directory containing:

- manifest, benchmark fingerprint, environment, exact config, and tokenizer validation;
- compressed discovery activation summaries;
- selectivity rankings, masks, stability distributions, overlap matrices, and layer histograms;
- every full and masked four-option logit/probability row;
- absolute NLL, accuracy, paired causal damage, bootstrap intervals, and domain breakdowns;
- retention artifacts only when triggered;
- plots, failure analysis, and a report answering the research question;
- explicit `real dense model`, `logical masking`, and `no measured VRAM reduction` labels.

Missing cases, nonfinite values, structural mismatches, ambiguous mask semantics, adapter presence, tokenizer invariant failures, or partial causal matrices fail the run. Negative, tied, unstable, and near-threshold results are never dropped or tuned away.

## Estimated runtime and storage

The measured design-time MPS forward latency for a representative 90-token prompt with MLP tracing hooks was approximately 0.185 seconds after warmup. Allowing for longer benchmark prompts, all three hook families, synchronization, artifact writing, and repeated baselines:

- benchmark construction and offline validation: 1 to 2 hours;
- initial discovery tracing and causal experiment: approximately 15 to 30 minutes;
- conditional retention curve: approximately 15 to 25 additional minutes;
- expected stored artifacts: approximately 60 to 150 MB, dominated by compressed discovery activation summaries;
- expected model allocation: approximately 3 GB of unified MPS tensor memory, reported as real MPS allocation and never as discrete VRAM savings.
