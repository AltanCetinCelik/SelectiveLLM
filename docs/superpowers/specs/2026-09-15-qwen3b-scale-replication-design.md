# Qwen2.5-3B Causal-Capacity Scale Replication

Date: 2026-09-15

Status: Approved for implementation by delegated investigator judgment

## Question

Does increasing model scale from Qwen2.5-1.5B-Instruct to the same-family
Qwen2.5-3B-Instruct reveal stable, causally useful, prompt-dependent MLP capacity
under the already frozen discovery and intervention protocol?

This is a scale replication, not a new discovery-method search. The immutable 1.5B
Outcome C and its artifacts remain unchanged.

## Controlled variable

The sole intended scientific variable is model scale:

- model: `Qwen/Qwen2.5-3B-Instruct`;
- revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`;
- backend: real Hugging Face Transformers dense model, no adapters;
- runtime dtype: float16 on Apple MPS;
- architecture invariants: 36 decoder layers, 11,008 MLP intermediate channels,
  hidden size 2,048, 16 query heads, and 2 KV heads;
- scoring: the same frozen-parameter, detached-input-embedding,
  gradient-enabled forward protocol validated in the 1.5B experiment.

The 7B model is excluded because it would require quantization or offload on the
available 16 GB host, changing precision or placement together with scale. Other
model families are excluded because architecture and training would also change.

## Immutable inputs and methods

Reuse without modification:

- benchmark `dense-capacity-mcq-1.0.0`, all 80 questions, option order, and hash
  `f4cf067de00d490a036488520768c82a5e0ea7bd0a126946b887fc5fd679d5e0`;
- 48 discovery and 32 held-out cases;
- tokenizer-safe restricted four-option scoring;
- correct-answer NLL primary metric and forced-choice accuracy secondary metric;
- activation and absolute gradient x activation discovery formulas;
- raw-score preservation and within-prompt, within-layer percentile ranks;
- discovery-only domain contrasts and the same 20 split halves at seed 42;
- same-domain, wrong-domain, five random, global-high, global-low, and no-op masks;
- paired held-out causal damage and 10,000 stratified case-bootstrap resamples at
  seed 42;
- token-summed `predicted_taylor_damage` and token-mean
  `normalized_signed_attribution` as diagnostic-only quantities;
- the exact 64-channel A/B/C gate from the committed 1.5B specification;
- 128-channel evidence as mandatory corroboration with no classification vote;
- logical masking only and no physical-memory, paging, or VRAM-reduction claim.

No held-out result may influence discovery, normalization, masks, or thresholds.
No partial scientific output is inspected during canonical execution.

## Block mappings and capacity

The 3B MLP contains `36 * 11,008 = 396,288` layer-channel positions. Exact 5%
capacity is 19,814.4 channels and therefore cannot be represented by integer
channels or complete 64/128-channel blocks.

Both granularities use the same nearest common block-valid footprint:

- selected channels: 19,840;
- fraction: `19,840 / 396,288 = 0.050064599...` (5.0065%);
- absolute deviation from 5%: 0.0065 percentage points.

### Primary 64-channel mapping

- 172 contiguous blocks per layer;
- 310 selected blocks total;
- quota for zero-based layer `l`:
  `floor((l + 1) * 310 / 36) - floor(l * 310 / 36)`;
- frozen quota vector:
  `[8, 9, 8, 9, 9, 8, 9, 8, 9, 9, 8, 9, 8, 9, 9, 8, 9, 9,
  8, 9, 8, 9, 9, 8, 9, 8, 9, 9, 8, 9, 8, 9, 9, 8, 9, 9]`.

### Corroborative 128-channel mapping

- 86 contiguous blocks per layer;
- 155 selected blocks total;
- quota for zero-based layer `l`:
  `floor((l + 1) * 155 / 36) - floor(l * 155 / 36)`;
- frozen quota vector:
  `[4, 4, 4, 5, 4, 4, 5, 4, 4, 5, 4, 4, 4, 5, 4, 4, 5, 4,
  4, 5, 4, 4, 5, 4, 4, 4, 5, 4, 4, 5, 4, 4, 5, 4, 4, 5]`.

The quota formula is architecture-derived and independent of prompts, gradients,
activations, labels, and model outputs. Every control at a block size uses exactly
the same per-layer quota. Mapping and quota hashes are committed before model
scoring.

## Execution matrix

The complete experiment contains:

- 48 discovery backward passes shared by both block sizes;
- 32 newly scored full-model held-out rows;
- 18 masks per block size and 1,152 held-out masked rows total;
- 32 held-out backward passes for signed diagnostics;
- 1,088 signed mask-case diagnostic rows.

Runtime invariants fail closed on model revision, architecture dimensions, adapter
absence, mapping coverage, quota totals, activation/gradient shape equality,
finiteness, tokenizer protocol, ordinary/gradient scoring equivalence, complete
cells, repeated scoring, and no-op equivalence.

## Primary classification

The 64-channel result alone uses the already frozen A/B/C gate:

- A: objective-aware discovery succeeds;
- B: stable but mostly shared importance;
- C: weak or unstable specialization.

No threshold changes. The 128-channel analysis is reported separately and cannot
rescue or overturn the primary classification.

## Scale comparison

The 1.5B and 3B runs are never pooled and are always labeled with model identity and
their distinct fingerprints. Because they use the same benchmark cases and causal
definitions, report a paired descriptive scale delta for each held-out case for:

- gradient same-domain damage;
- same-minus-random;
- same-minus-wrong;
- same-minus-global-high;
- gradient-same-minus-activation-same.

For each delta, subtract the immutable 1.5B case value from the 3B case value and
report mean, median, standard deviation, p50, p95, and a 10,000-resample stratified
case-bootstrap 95% interval at seed 42. These deltas describe the controlled model
change but do not replace the 3B A/B/C gate.

Scale is considered a causal-capacity rescue only if the valid 3B primary result is
A or B. If the valid 3B result is C, nearby model-scale escalation stops on this
machine. The next research design must change model family, training, granularity,
or methodology explicitly rather than silently tuning this benchmark.

## Provenance and artifacts

Canonical execution must begin from a clean committed source state. Preserve the
source commit, dirty flag, model and tokenizer revision, package versions, hardware,
benchmark hash, mapping hashes, quota hashes, metric schemas, all raw and derived
evidence, plots, report, failure analysis, and artifact checksums.

Failed runs retain their manifest and partial artifacts when possible and never
publish to `latest`. A successful run publishes only from a clean start.

## Preflight and resource bound

Before canonical execution:

- run all repository tests, Ruff, strict mypy, and package build;
- verify deterministic mapping regeneration;
- download only the pinned 3B model assets;
- run an invariant-only preflight that may inspect shapes, hashes, finiteness,
  equivalence tolerances, memory availability, and hook counts, but no scientific
  ranking or held-out effect.

Expected download is approximately 6.2 GB. Expected full-run storage is 250 to
500 MB. Expected M4 runtime is 25 to 60 minutes. An out-of-memory preflight is an
infrastructure limitation, not a scientific C result.

## Public-release follow-through

After immutable evidence is produced, perform a separate publication pass:

- update README and research documentation with the 3B result and all boundaries;
- preserve every negative or contradictory result;
- scan tracked files and history for credentials, private keys, tokens, absolute
  user paths, accidental model weights, and oversized files;
- verify license, citation, contribution, security, issue-template, and CI files;
- verify the default quickstart and deterministic benchmark from a clean checkout
  state without requiring private assets;
- run tests, lint, typing, coverage, and package build;
- leave the worktree clean with public evidence committed, but do not create a
  remote repository or push without an explicit request.

Model weights are never committed. External model and adapter licenses remain
separate from the repository's Apache-2.0 source license.
