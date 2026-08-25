# M3 Withdrawal and Consumer Evidence

Milestone: M3
Validation result: passed

- `node --test packages/rigorloop/test/lifecycle-withdrawal.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-transaction.test.js`: passed with 42 tests before the final regression additions.
- `npm test --prefix packages/rigorloop`: passed with 178 tests.
- `python scripts/build-skills.py --check`: passed.
- `python scripts/validate-skills.py`: passed for 24 canonical skills.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-25-workflow-routed-upstream-corrections/change.yaml`: passed after settlement-projection normalization.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-25-workflow-routed-upstream-corrections`: passed before this receipt was added.
- `python scripts/validate-boundary-first.py --path specs/workflow-routed-upstream-corrections.test.md`: passed.
- `bash scripts/ci.sh --mode broad-smoke --jobs 2`: passed 11 checks in 447 seconds.

The proof covers guarded duplicate withdrawal, durable non-owning receipts, concise human and JSON diagnostics, minimal workflow routing guidance, authoring-skill handback, exact settlement projection, and repository-wide feature validation. The tag-specific release gate remains correctly deferred to release preparation.
