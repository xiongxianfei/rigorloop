# M1 R8 Post-Evaluation Correction Evidence

Change record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

Milestone: M1

Validation result: passed

- The lifecycle CLI now tracks whether a governed mutation reached transition evaluation.
- Caught evaluation/transaction failures receive an internal authoritative `state_changed: false` fact.
- Pre-evaluation request and stale-input failures still omit the field.
- A public live-lock probe proves `RL_OPERATION_BUSY`, unchanged bytes, and `state_changed: false`.
- An injected transaction failure proves rollback/unchanged projection.
- A missing-request probe proves pre-evaluation omission.
- The fact remains non-enumerable, preserving detailed JSON compatibility.

Commands run:

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` — 18 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 215 passed, 0 failed.

No publication or unrelated repository mutation occurred.
