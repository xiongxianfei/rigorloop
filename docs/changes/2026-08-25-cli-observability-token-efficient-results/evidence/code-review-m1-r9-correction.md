# M1 R9 Retained-Recovery Correction Evidence

Change record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

Milestone: M1

Validation result: passed

- The lifecycle CLI captures a content-addressed snapshot of `change.yaml` and every `.rigorloop-lifecycle-*` entry immediately before transition evaluation.
- Caught post-evaluation failures compare the actual lifecycle-owned path set after the transaction with that invocation-owned baseline.
- Pre-existing live locks remain unchanged and report `state_changed: false`.
- A real fault after recovery preparation retains recovery bytes and reports `state_changed: true`.
- A real fault after replacement restores `change.yaml`, removes recovery/lock state, and reports `state_changed: false`.
- Pre-evaluation failures still omit the field, and detailed compatibility remains unchanged.

Commands run:

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` — 18 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 215 passed, 0 failed.

No publication or unrelated repository mutation occurred.
