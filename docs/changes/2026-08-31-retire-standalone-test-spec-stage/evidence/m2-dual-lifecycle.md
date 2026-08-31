## Result

Milestone: M2
Validation result: passed

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Added the inactive v2 lifecycle graph, plan-only Delivery Review package, contract-keyed correction ownership, v2 context rejection for retired stages, v1 compatibility behavior, and aligned Node/Python/schema validation.
- Artifacts changed: lifecycle contract, CLI, read, package, operation, automation-policy, automation-state, metadata, artifact-lifecycle, review-artifact, and schema surfaces; focused Node and Python fixtures; the exact-output compatibility fixture; and this M2 evidence.
- Tests added or updated: TS-003, TS-004, TS-005, TS-006, TS-010, and TS-015 coverage for direct `plan -> delivery-review`, exact plan-only membership, settlement/advancement separation, plan-owned correction, retired stage/artifact/review/package-member rejection, wholly unknown vocabulary, active-manifest v2 interpretation, and unchanged v1 package/routing behavior.
- Validation performed: CMD-01 through CMD-06, change-local metadata validation, explicit-path artifact-lifecycle validation, and `git diff --check`.
- Validation result: CMD-01 passed 189 Node tests; CMD-02 passed 310 Node tests with 2 pre-existing skips; CMD-03 passed 77 Python tests; CMD-04 passed 166 Python tests; CMD-05 passed 77 workflow-automation, 18 policy, and 69 state tests; CMD-06 passed 109 Python tests. Change metadata, explicit-path lifecycle consistency, and whitespace validation passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: the repository remains in manifest `preactivation`; new-change still emits v1; canonical skill retirement, documentation/publication parity, activation-manifest population, default v2 creation, rollback proof, and adapter publication remain M3-M5 work.

## Planned milestone

- Change ID: `2026-08-31-retire-standalone-test-spec-stage`
- Plan identity: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`, sha256 `727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938`.
- Milestone ID: M2.
- Milestone state: implementation complete; ready for the guarded `review-requested` transition.
- Baseline or change-pack status: Delivery Review package `delivery-review-r3` remains current and granted under this change's registered v1 contract; M2 adds only inactive v2 behavior selected by an explicit v2 record under an active fixture manifest.
- Milestone validation evidence: this file.
- Commit status: the M2 implementation commit is the Code Review target; its exact identity is supplied by Git history and the workflow handoff rather than self-referenced here.
- Code-review handoff: review contract-keyed graph closure, exact package authority, retired-surface diagnostics, correction ownership, v1 isolation, transaction safety, and Node/Python policy parity.

## Test-first record

The first v2 stage test failed because `plan -> delivery-review` was absent and the attempted retired `plan -> test-spec` transition reached post-validation instead of being rejected at the edge. The contract-keyed stage matrix and plan-only package composition made those tests pass. Follow-on negative tests then covered active artifact and review state, public context, plan correction, mixed package membership, and closed-vocabulary diagnostics.

The first full package run exposed a stale observability fixture: M1 had changed `new-change` to emit explicit v1 lifecycle fields, while the exact-output fixture still represented the older unversioned output. The repository-owned fixture update mode regenerated that deterministic fixture, after which the full package suite passed.

## Compatibility and unchanged surfaces

- `specs/lifecycle-contract-activation.yaml` remains unchanged in `preactivation`; M2 does not activate v2 or populate the frozen compatibility set.
- `packages/rigorloop/dist/lib/new-change.js` remains unchanged and continues to create v1 records until M5.
- `scripts/lifecycle_state_sync.py` remains unchanged because its authoring/review-fix profile helpers are legacy v1 compatibility projections; current contract-keyed automation routing is owned by `workflow_automation_policy.py`, `workflow_automation.py`, and `workflow_automation_state.py`.
- No migration operation was added. Manifest-bound v1 records keep their registered graph, package membership, stage status, and downstream authority.
- No skill, template, documentation, or generated adapter was removed or republished in M2; those coherent publication changes are allocated to M3-M5.

## Validation note

Node lifecycle commands used `TMPDIR=/dev/shm` to isolate temporary repository fixtures from an unrelated ambient `/tmp/docs/changes/dead-end` directory discovered by parent-directory lookup. This changes only test-fixture placement, not selected tests or runtime behavior.
