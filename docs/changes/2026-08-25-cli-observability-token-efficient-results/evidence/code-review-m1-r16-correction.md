# M1 R16 Log-Format Boundary Correction Evidence

Change record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

Milestone: M1

Validation result: passed

- Log inspection now accepts only its documented R18 `human` and `json` formats.
- `logs path/show --format detailed-json` fail closed with `RL_INVALID_REQUEST` and no stdout.
- Common semantic-result projections continue through the finalized renderer with observability.

Commands run:

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js packages/rigorloop/test/cli-invocation-observability.test.js` — 39 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 218 passed, 0 failed.
