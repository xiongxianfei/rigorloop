# M1 R6 Repair-State Correction Evidence

Change record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

Milestone: M1

Validation result: passed

- Repair state change now comes from a closed, fail-closed mapping of actual repair outcomes.
- `cleared-orphaned-lock`, `restored-prior`, `committed-candidate`, and `abandoned-prepared` report `true` because lifecycle-owned bytes were persisted, removed, or restored.
- `already-clear` and `nothing-to-reconcile` report `false`.
- Dry-run remains `false` without entering repair mutation.
- The public concise regression proves both lock deletion/`true` and already-clear/`false`; the closed-vocabulary test covers every recovery status and rejects unknown values.
- The authoritative fact remains non-enumerable in the detailed result, preserving the revision-bound compatibility corpus.

Commands run:

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` — 17 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 214 passed, 0 failed.

No publication or unrelated repository mutation occurred.
