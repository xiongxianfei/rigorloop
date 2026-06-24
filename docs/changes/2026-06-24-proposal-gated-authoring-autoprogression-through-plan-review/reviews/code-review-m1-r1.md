# Code Review M1 R1: Profile Policy Persistence and Metadata Validation

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1. Profile Policy Persistence and Metadata Validation
Reviewed artifact: implementation diff for M1 policy persistence validation
Review date: 2026-06-24
Recording status: recorded
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m1-r1.md, docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md, docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md, docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md, docs/plan.md, docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml
- Open blockers: none
- Next stage: implement M2
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md
- Review resolution: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md#code-review-m1-r1
- Reviewed milestone: M1. Profile Policy Persistence and Metadata Validation
- Milestone closeout: closed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: `git diff -- schemas/change.schema.json scripts/validate-change-metadata.py scripts/query-change-record.py scripts/test-change-metadata-validator.py docs/workflows.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- Tracked governing branch state: approved specs, active test spec, approved architecture, accepted ADR, active plan, review log, and change metadata in the current worktree.
- Governing artifacts: `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.test.md`, `specs/rigorloop-workflow.test.md`, `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`, and the M1 section of `docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`.
- Validation evidence: `python scripts/test-change-metadata-validator.py` passed 26 tests; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml` passed; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path schemas/change.schema.json --path docs/workflows.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml` validated 5 artifact files; `git diff --check -- schemas/change.schema.json scripts/validate-change-metadata.py scripts/change_metadata_semantics.py scripts/query-change-record.py scripts/test-change-metadata-validator.py tests/fixtures/change-metadata docs/workflows.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review` passed.

## Diff Summary

M1 adds `workflow.autoprogression` as optional change metadata, validates durable profile policy fields semantically, exposes profile policy from the query helper as evidence only, and adds validator/query coverage for the named policy-persistence edge cases. The workflow guide now names the canonical policy location and fallback boundary. The active plan and plan index were updated to request this code review.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `schemas/change.schema.json` defines optional `workflow.autoprogression` with closed `profile` values `off` and `authoring-through-plan-review`; `scripts/validate-change-metadata.py` enforces durable fields and non-ownership rules required by `R2h`-`R2t`, `R2ae`, `R2ag`, and `R7er`. |
| Test coverage | pass | `scripts/test-change-metadata-validator.py` covers valid `authoring-through-plan-review`, valid `off`, unknown profile, missing fields, mismatched change ID, malformed shape, invalid timestamp, session-only arming, failed persistence, invalid fallback, and query evidence-only output. |
| Edge cases | pass | The named M1 edge cases in `T13` are directly covered by `test_autoprogression_policy_record_required_fields_fail`, `test_autoprogression_policy_non_durable_records_fail`, and `test_query_summary_exposes_autoprogression_policy_as_evidence_only`. |
| Error handling | pass | Invalid, partial, non-durable, failed, and fallback-invalid policy records fail closed with validator errors including `authorization-not-persisted` for failed persistence. |
| Architecture boundaries | pass | The implementation changes repository validation and workflow guidance only; no service, background worker, or live workflow-state owner is introduced. |
| Compatibility | pass | Existing legacy and compact metadata fixtures still pass under the full `python scripts/test-change-metadata-validator.py` run; absent policy remains valid metadata for the default-off path. |
| Security/privacy | pass | The diff adds no secret handling, credential output, external calls, or auth bypass. |
| Derived artifact currency | pass | No generated public adapter output is touched in M1; generated adapter alignment remains scheduled for M4. |
| Unrelated changes | pass | The reviewed M1 diff is limited to schema, metadata validator, query helper, tests, workflow guidance, and lifecycle evidence for this milestone. |
| Validation evidence | pass | The M1 validation commands named in the plan passed and were recorded in `change.yaml`. |

## No-Finding Rationale

The implementation converts the approved durable profile-policy contract into an optional schema shape plus fail-closed semantic validation without making policy metadata a live-state owner. The tests provide direct proof for the named valid, malformed, partial, non-durable, failed-persistence, fallback, cancellation-as-`off`, and query-evidence cases. The active change metadata remains valid without a policy record, preserving the default-off compatibility path until workflow routing is implemented in M2.

## Direct-Proof Gaps

None for M1. Runtime activation routing for missing durable records, proposal-gate evaluation, transition budget, and resume behavior remains intentionally assigned to M2.

## Milestone Handoff State

- Reviewed milestone: M1. Profile Policy Persistence and Metadata Validation
- Milestone state after review: closed
- Required review-resolution: no
- Remaining in-scope implementation milestones: M2, M3, M4, M5
- Next stage: implement M2
- Final closeout readiness: not-ready; implementation milestones M2 through M5, code-review, explain-change, verify, and PR handoff remain.

## Residual Risks

- M1 validates and exposes policy metadata but does not implement runtime profile activation or stop-result routing; that is the approved M2 scope.
