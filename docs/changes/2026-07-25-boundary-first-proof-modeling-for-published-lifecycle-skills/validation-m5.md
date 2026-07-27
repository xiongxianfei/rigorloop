# M5 Validation: Verification Routing and Lifecycle Synchronization

Date: 2026-07-27

Milestone: M5

Result: implementation validation passed; PR-range proof pending committed HEAD

## Root cause

The evidence registry stored an `allowed_root`, but the selector ignored it
when matching evidence. It classified only root-level change files and matched
only their basenames. The boundary initiative legitimately records nested,
typed evidence, so 461 tracked evidence paths fell through to
`manual-routing-required` during PR selection.

The blocked verification also found that the active plan still named
`explain-change` after the explanation had been committed. That was a
lifecycle-state synchronization defect, independent of the checker results.

## Correction

- Match registered evidence against its complete repository path and the
  registration's bounded root.
- Permit safe nested roots under one change or an exact dated change root.
- Keep basename patterns immediate to their registered root; require an
  explicit slash-bearing pattern for descendants.
- Register this initiative's capability report, milestone evidence, runtime
  evidence, adapter parity, preservation, simple-change, and recovery
  evidence against existing semantic checks.
- Bind those registrations to this exact dated change root. A similarly named
  evidence path in another change remains unsupported.
- Synchronize the plan body and plan index through a corrective M5 rather than
  rewriting a closed implementation milestone.

## Failing-first evidence

Before the selector correction, the new focused tests failed in three places:

- a safe bounded nested `allowed_root` was rejected;
- representative nested boundary evidence remained blocked;
- the tracked boundary evidence inventory retained manual-routing debt.

The earlier blocked verification recorded the real PR-range failure against
`origin/main`: 461 paths required manual routing, comprising 455 nested paths
and six root-level unregistered evidence files.

## Focused automated evidence

| Command | Result |
| --- | --- |
| Focused nested-root, representative-family, unknown-sibling, cross-change, inventory, and preservation selector tests | pass; 8 tests |
| `python scripts/test-select-validation.py` | pass; 142 tests |
| `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan-archive.md --path docs/plan.md --path docs/plans/2026-07-25-boundary-first-proof-modeling.md` | pass; pre-existing workflow-spec merge-language warnings only |

The first scoped CI composition run passed the selector regression and guide
checks, then stopped at lifecycle validation because the new handoff initially
used noncanonical plan vocabulary. The plan now uses the closed lifecycle
state, structured review status, and canonical closeout reasons; only that
failed lifecycle check was rerun.

## Evidence reuse

M5 does not change the boundary model, runtime behavior harness, governed
skills, adapter generator, preservation fixtures, or release transaction
logic. The fresh passing evidence recorded by M4 and the blocked verification
for those unaffected dependencies remains applicable:

- boundary model: 115 tests;
- skill validator: 261 tests;
- adapter distribution: 132 tests;
- release transaction: 87 tests;
- preservation pairs: 40;
- selected boundary CI: 14 checks.

Those suites are not rerun for this selector-and-lifecycle correction. The
remaining M5 proof is limited to change metadata, current capability-report
generation/validation, patch integrity, and the actual PR-range selector over
the committed corrective head.

