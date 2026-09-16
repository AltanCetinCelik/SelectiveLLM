# Public release audit

Audit date: 2026-09-16

## Status

The tracked repository is published as an Apache-2.0 research prototype at
<https://github.com/AltanCetinCelik/SelectiveLLM>.

The public claim is deliberately narrower than the project name:

- real adapter residency and locality-dependent cache behavior were measured on
  Apple unified memory;
- a focused adapter diagnostic found empirical response diversity but weak
  semantic alignment;
- dense Qwen2.5-1.5B and 3B logical-masking studies both returned the
  preregistered Outcome C;
- parameter paging, dense-model memory reduction, and a reliable quality gain
  from semantic routing have not been demonstrated.

## Repository hygiene

- Apache-2.0 license, citation metadata, contribution guide, security policy,
  code of conduct, issue templates, pull-request template, and CI are present.
- Common credential formats, private-key markers, absolute user paths, and
  personal email strings were scanned in tracked content and Git history.
- No model-weight, checkpoint, archive, cache, virtual-environment, or build
  output is tracked.
- `.env` files, private-key formats, Hugging Face caches, model-weight formats,
  and local result runs are ignored.
- Public result directories contain only intentionally committed evidence.
- Dense-result publication subsets omit two large channel-level tensor archives
  and three resumable progress files per run; their hashes remain in the
  manifests, while raw and normalized block-level arrays are included.
- External model and adapter weights are pinned by revision where used and are
  not redistributed under the project license.

## Verification

The release candidate passed:

```bash
ruff check .
ruff format --check .
mypy selectivellm
pytest --cov=selectivellm --cov-report=term-missing --cov-fail-under=70
python -m build
selectivellm inspect --device cpu
selectivellm demo --seed 42
selectivellm benchmark --router semantic --report --output <temporary-directory>
```

The wheel was installed into a fresh Python 3.12 environment with declared
dependencies and exercised outside the source checkout. Local Markdown links,
YAML/CFF files, package contents, and committed result-manifest hashes were also
validated.

The default CI suite is network-free. Hardware/model integration modules require
external pinned assets and an accelerator; their canonical run manifests retain
the corresponding runtime, invariant, completeness, and provenance checks.

## Publication

The canonical remote is `origin`, the default branch is `main`, and the GitHub
repository is public. Repository URLs and the CI badge are part of the tracked
metadata. Ignored Hugging Face caches and timestamped local run directories were
not uploaded.
