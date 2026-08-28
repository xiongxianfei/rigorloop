# M1 R13 Detailed-Projection Correction Evidence

Change record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

Milestone: M1

Validation result: passed

- Legacy `json` continues serializing only the existing enumerable v0.4.x contract.
- Explicit `detailed-json` uses a separate complete projection that materializes applicable authoritative `state_changed` facts.
- Concise and detailed projections agree for retained recovery (`true`), verified rollback (`false`), and no-write post-evaluation failure (`false`).
- Pre-evaluation results omit the fact in both projections.
- T10 removes only the documented new detailed mutation fact before comparing every legacy compatibility fact.

Commands run:

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` — 19 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 216 passed, 0 failed.
