# M5 Milestone, Migration, and Repair Evidence

## Delivered

- `start-milestone` enforces exact current selection, implementation kind, planned state, and closed predecessors.
- `complete-milestone` requires the exact approved milestone review and a stage-owned passing proof before closing and updating the remaining projection.
- `migrate` supports only the enumerated legacy coordination schema and deterministically creates the version-one coordination block.
- `repair` exposes only `clear-orphaned-lock` and `reconcile-interrupted-replace`, with dry-run observation, current-revision validation, live-owner refusal, identity reconciliation, and no arbitrary state edits.
- Milestone operations leave workflow routing fields unchanged.

## Validation

- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-milestone.test.js packages/rigorloop/test/lifecycle-migration-repair.test.js`: passed, 26 tests.
- `npm test --prefix packages/rigorloop`: passed, 156 tests.
- `python3 scripts/test-workflow-automation-state.py`: passed, 65 tests.
- `python3 scripts/validate-npm-package.py`: passed.

## Recovery boundary

Clearing an orphan never changes `change.yaml` and refuses a live owner or outstanding recovery bundle. Interrupted replacement accepts only known prior/candidate identities and either finishes the candidate or restores verified prior bytes.
