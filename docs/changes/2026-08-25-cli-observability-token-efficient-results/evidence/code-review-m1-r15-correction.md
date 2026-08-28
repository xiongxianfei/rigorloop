# M1 R15 New-Projection Observability Correction Evidence

Change record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

Milestone: M1

Validation result: passed

- One closed-vocabulary validator now supplies `recorded`, `degraded`, or `disabled` to every new projection.
- Explicit `detailed-json` materializes the finalized state without changing legacy `json`.
- Concise-human includes a compact `observability=<state>` fact and remains within its line bound.
- T10 compares every legacy fact after removing only documented additive detailed fields and separately asserts them.
- Unknown observability values fail closed in detailed and concise-human projection.

Commands run:

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` — 20 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 217 passed, 0 failed.
