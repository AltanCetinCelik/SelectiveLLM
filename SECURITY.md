# Security Policy

## Supported versions

Security fixes target the latest release and the `main` branch.

## Reporting a vulnerability

Use GitHub private vulnerability reporting when available. Do not open a public issue for an unpatched vulnerability. Include affected versions, reproduction steps, impact, and any suggested mitigation. Maintainers should acknowledge a report within seven days.

## Model and runtime safety

- `trust_remote_code` is disabled by default and must remain opt-in.
- SelectiveLLM never executes generated model output.
- Model and adapter paths may point to third-party artifacts; users must review their code, license, and provenance.
- Model weights, credentials, access tokens, and private prompts must not be committed.
- Benchmark reports can contain prompts and generated text. Review artifacts before publishing them.
