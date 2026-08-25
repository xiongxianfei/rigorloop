# Execution Plan: Workflow-Routed Upstream Corrections

## Owning change record

`docs/changes/2026-08-25-workflow-routed-upstream-corrections/change.yaml`

## Governing artifacts

- Proposal: `docs/proposals/2026-08-25-workflow-routed-upstream-corrections.md`
- Spec: `specs/workflow-routed-upstream-corrections.md`
- Architecture: `docs/architecture/2026-08-25-workflow-routed-upstream-corrections.md`
- ADR: `docs/adr/ADR-20260825-workflow-routed-correction-and-artifact-ownership.md`
- Test spec: pending downstream authoring

## Objective and scope

Implement the approved lifecycle CLI schema, read model, correction operations, scoped settlement, cross-change ownership protection, guarded architecture/ADR withdrawal, concise diagnostics, and minimal workflow/skill integration. Apply the capability to the blocked observability branch only after this change verifies.

## Dependencies and assumptions

- Reuse the existing Node lifecycle engine, YAML parser, serializer, lock, recovery, and CLI renderers.
- Preserve the existing Python validators until parity proof is recorded.
- Add no external services, runtime dependencies, or semantic artifact mutation.
- Author tests before or with each production slice and use isolated repository fixtures.

## Milestone M1: Versioned state and ownership read model

Deliver lifecycle CLI schema version 2, explicit v1-to-v2 migration, closed route and withdrawal vocabularies, stored-state validation, owning-change pointer parsing, and cross-change normalized ownership indexing. Reject new cross-change artifact creation collisions while preserving same-entry revision.

Validation:

- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-migration-repair.test.js packages/rigorloop/test/lifecycle-artifact-revision.test.js packages/rigorloop/test/lifecycle-ownership.test.js`
- `npm test --prefix packages/rigorloop`

Recovery: revert the M1 implementation slice; version-1 fixtures and records remain unchanged because no new operation is yet consumed.

## Milestone M2: Correction route, scoped settlement, and return

Deliver `route-correction` and `return-correction`, exact source snapshots, permission overlay, route evidence parsing, deterministic IDs, exact review-occurrence settlement, bounded context diagnostics, idempotency, and transaction fault proof.

Validation:

- `node --test packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-evidence.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-transaction.test.js`
- `npm test --prefix packages/rigorloop`

Recovery: revert M2 code while retaining M1 migration support; no published skill requests route operations until M3.

## Milestone M3: Guarded withdrawal and consumer migration

Deliver `withdraw-artifact-registration`, exact canonical-owner proof, non-owning receipts, repository validation, human and JSON parity, minimal workflow routing guidance, authoring-skill route-required handling, and end-to-end fixtures for the current duplicate-architecture scenario.

Validation:

- `node --test packages/rigorloop/test/lifecycle-withdrawal.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-contract.test.js`
- `npm test --prefix packages/rigorloop`
- `python scripts/validate-change-metadata.py docs/changes/2026-08-25-workflow-routed-upstream-corrections/change.yaml`
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-25-workflow-routed-upstream-corrections`
- `python scripts/validate-documentation-prose.py --mode audit --path specs/workflow-routed-upstream-corrections.md --path specs/workflow-routed-upstream-corrections.test.md --path docs/architecture/2026-08-25-workflow-routed-upstream-corrections.md --path docs/adr/ADR-20260825-workflow-routed-correction-and-artifact-ownership.md --path docs/plans/2026-08-25-workflow-routed-upstream-corrections.md`
- `python scripts/validate-boundary-first.py --path specs/workflow-routed-upstream-corrections.test.md`
- `bash scripts/ci.sh --mode broad-smoke`

Recovery: revert consumer text and withdrawal operation together; version-2 readers continue to fail closed on retained route or receipt state.

## Review and closeout sequence

Each milestone runs focused proof, implementation, and code review before the next starts. Material findings route through review resolution and rereview. After M3, explain the change, run final repository-wide verification, then prepare PR. The release-tag gate remains deferred to an actual release checkpoint because it validates immutable published-version metadata. Applying operations to the observability branch is a later isolated consumption step and is not part of this branch's implementation diff.

## Risks and controls

| Risk | Control |
| --- | --- |
| old client drops new state | explicit schema version 2 and fail-closed migration tests |
| repository scan misclassifies ownership | normalize once, cross-check projections, fail closed, and test ambiguity and symlinks |
| route weakens downstream findings | immutable source snapshot and exact-operation permission tests |
| settlement regains global blocking | review-occurrence fixtures with unrelated open findings |
| withdrawal deletes evidence | byte-identity assertions for every semantic and historical file |
| skill text regains lifecycle mechanics | small literal guidance and package validation |

## Next artifacts

- Independent plan review.
- Test specification after plan approval.

## Follow-on artifacts

- None yet.

## Readiness

Ready for plan review after CLI registration; not test-spec-ready, implementation-ready, verified, or PR-ready.
