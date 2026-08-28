# M1 R5 Compatibility Correction Evidence

Change record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

Milestone: M1

Validation result: passed

- Added a checked-in normalized compatibility corpus with 27 cases bound to exact pre-feature branch base `fcbbfda44a89945ee06cfa0c1b16dcbd39984036`.
- Covered applicable top-level human/JSON and lifecycle human/JSON success and failure, including lifecycle mutation success/failure.
- Compared each legacy JSON case with explicit `detailed-json`.
- The new proof exposed an enumerable `state_changed` compatibility leak in lifecycle detailed JSON; the fact is now authoritative but non-enumerable, so concise projection can use it without changing the v0.4.x schema.
- Disabled file logging in non-observability CLI tests to prevent a shared user log store from coupling otherwise isolated parallel tests.

Commands run:

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` — 15 passed, 0 failed.
- `node --test packages/rigorloop/test/cli.test.js` — 117 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 212 passed, 0 failed.

The corpus was generated mechanically from the bound pre-feature revision and then proved against the current CLI. No publication or repository lifecycle mutation occurred during the proof.
