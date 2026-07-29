# Stage-Owned Change Query Compatibility Rationale

## Summary

The bounded change-record query now reads valid
`stage-owned-change-local-v1` metadata without applying the retired unified
automation schema. The compatibility path is explicitly read-only, validates
the stage-owned contract, preserves canonical change identity, and projects
only information owned by the stage-owned record.

## Problem

After stage-owned lifecycle metadata became authoritative,
`scripts/query-change-record.py` still loaded every change record through the
legacy workflow-automation state contract. Valid stage-owned records therefore
failed before the query could return their bounded summary. Treating the new
record as legacy metadata would also risk allowing old writers or old review
projections to claim authority they no longer own.

## Decision trail

The governing specification,
`specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`,
places lifecycle state with stage-owned artifacts and compact change-local
coordination metadata. The bounded-read specification and test specification
require repository queries to return stable, side-effect-free projections.
The system architecture and
`ADR-20260729-stage-owned-change-local-lifecycle-state.md` preserve this
ownership boundary.

The implementation consequently adds a narrow compatibility read rather than
reviving unified automation state. It does not add a writer, migration,
selector, validator command, or new lifecycle field.

## File-by-file rationale

### `scripts/workflow_automation_state.py`

`WorkflowAutomationStateStore.read` accepts stage-owned metadata only when the
caller explicitly requests a read-only compatibility read. It validates the
stage-owned closed vocabularies, checks that the stored change ID matches the
canonical directory, and returns before any retired automation validation.
Existing store users, including all mutation methods, continue to reject
stage-owned records by default.

### `scripts/query-change-record.py`

The query opts into that read boundary and recognizes the stage-owned metadata
shape. Its summary exposes declared artifact paths, workflow routing state,
blockers, and compact automation policy without changing the source file.
Review projection uses only `workflow_state.planned_work.latest_review`; when
that routing evidence is absent, review status and unresolved-item count remain
unknown rather than falling back to the legacy top-level review summary.

### `scripts/test-query-change-record.py`

The new regressions prove that a valid stage-owned record is queryable and
unchanged after the read, ordinary legacy-store access remains prohibited,
unknown lifecycle vocabulary fails closed, and a substituted change ID cannot
be queried under another canonical directory.

### Change-local review records

`change.yaml`, the review ledger, detailed review records, and review
resolution preserve the formal review trail. They record two accepted first
round findings, their validation evidence, a clean second code review, and an
unchanged-spec approval.

## Review resolution

`SOQ-CR1` found that the first implementation returned a stage-owned snapshot
before checking canonical change identity. The fix moved identity validation
ahead of the compatibility return and added a mismatch regression.

`SOQ-CR2` found that the first query projection inferred zero unresolved
findings from routing state. The fix leaves that value unknown unless an
authoritative stage-owned source provides it and adds a regression against the
overclaim.

Both findings are accepted and closed in `review-resolution.md`. Code review
R2 has no material findings.

## Alternatives rejected

- Validating stage-owned records as retired unified automation was rejected
  because the schemas have different owners and meanings.
- Allowing the legacy store to read stage-owned metadata implicitly was
  rejected because mutation callers share that store.
- Reconstructing review closeout from legacy top-level fields was rejected
  because those fields are not authoritative under the stage-owned contract.
- Adding another selector or standalone validation mechanism was rejected
  because existing contract validation and focused tests are sufficient.

## Scope control and residual risk

This isolated bug fix has no active execution plan or implementation
milestones. It changes only the bounded query, its guarded compatibility read,
tests, and durable review evidence. It does not migrate records, alter writers,
or change published skill behavior.

The remaining risk is projection drift if the stage-owned schema later adds or
renames queryable fields. The fail-closed validator and focused query tests
make that drift visible. Hosted CI status is not asserted by this rationale;
final readiness is determined by the subsequent `verify` stage.

