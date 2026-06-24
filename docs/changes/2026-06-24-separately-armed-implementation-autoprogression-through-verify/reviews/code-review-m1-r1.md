# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1 profile schema and authorization policy implementation diff
Status: changes-requested

## Review inputs

- Diff/review surface: `schemas/change.schema.json`, `scripts/validate-change-metadata.py`, `scripts/query-change-record.py`, `scripts/test-change-metadata-validator.py`, active plan and change metadata state updates.
- Tracked governing branch state: local branch `proposal/implementation-autoprogression-through-verify`; governing artifacts are present in the working tree for this change.
- Governing artifacts: `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`, `specs/implementation-autoprogression-through-verify.test.md`, `docs/plans/2026-06-24-implementation-autoprogression-through-verify.md`.
- Validation evidence reviewed: M1 notes record passing `python scripts/test-change-metadata-validator.py -k autoprogression_policy`, `python scripts/test-change-metadata-validator.py -k named_autoprogression_policy`, `python scripts/test-change-metadata-validator.py`, change metadata validation, review artifact validation, artifact lifecycle explicit-path validation, and `git diff --check`.

## Diff summary

M1 adds `implementation-through-verify` to the change metadata schema and semantic validator, introduces independent named autoprogression records for authoring and implementation profiles, validates implementation profile `phase` and `state`, rejects forbidden live workflow-state fields inside profile records, exposes named policy records through the query helper, and adds validator/query regression tests. The plan and change metadata were updated to hand M1 to code review.

## Findings

### CR-M1-R1-F1 - Named autoprogression containers can still own live workflow state

Finding ID: CR-M1-R1-F1
Severity: major
Location: `scripts/validate-change-metadata.py:509`
Evidence: In the named-record branch, `validate_autoprogression_policy` iterates only `authoring_through_plan_review` and `implementation_through_verify`, then returns at `scripts/validate-change-metadata.py:530`. The forbidden live-state field check runs only inside `validate_autoprogression_record`, so a container-level `workflow.autoprogression.next_stage` is ignored when named records are present. A direct fixture with `workflow.autoprogression.next_stage: implement M1` plus a valid `implementation_through_verify` record passed `python scripts/validate-change-metadata.py`, even though `specs/rigorloop-workflow.md:407` says profile policy metadata must not own `next stage` and `specs/implementation-autoprogression-through-verify.test.md:81`-`83` requires forbidden live-state fields to remain forbidden.
Required outcome: The semantic validator must reject forbidden live workflow-state fields anywhere inside the autoprogression policy container, including the named-record container shape, and targeted tests must prove that rejection.
Safe resolution path: Add a container-level forbidden-field check before returning from the named-record branch in `validate_autoprogression_policy`, add a regression case where `workflow.autoprogression.next_stage` appears beside `implementation_through_verify`, then rerun the focused autoprogression tests and the full change metadata validator suite.
needs-decision rationale: none

## Checklist coverage

1. Spec alignment: concern. The implementation satisfies closed profile, phase/state, and independent record basics, but misses the live-state boundary for named-record containers (`R7er`).
2. Test coverage: concern. Tests cover forbidden live-state fields inside `implementation_through_verify`, but not at the `workflow.autoprogression` container level for named records.
3. Edge cases: concern. The named-record container edge case is untested and currently passes incorrectly.
4. Error handling: concern. Malformed profile records fail closed, but malformed policy containers with live workflow state do not.
5. Architecture boundaries: pass. The diff stays within change metadata, query, schema, and tests for M1 and does not introduce new orchestration services.
6. Compatibility: pass. Legacy single-record authoring profile behavior remains covered by existing tests, and the query helper preserves legacy output when `profile` is present.
7. Security/privacy: pass. The diff does not add secret-bearing fields, credential reads, or unsafe logging.
8. Derived artifact currency: pass. No generated adapter or derived skill artifact is touched in M1.
9. Unrelated changes: pass. The reviewed M1 diff is scoped to schema/validator/query/tests and required plan/change metadata handoff updates; earlier proposal/spec/architecture artifacts remain part of the broader branch state, not the M1 implementation surface.
10. Validation evidence: concern. The recorded commands are relevant and passing, but they did not cover the container-level forbidden-field regression.

## Direct-proof gaps

- Missing direct proof that `workflow.autoprogression.next_stage`, `current_stage`, `review_status`, `branch_readiness`, or `pr_readiness` are rejected when named records are used.

## Milestone handoff state

- Reviewed milestone: M1. Profile schema and authorization policy
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1, M2, M3, M4, M5
- Next stage: review-resolution M1
- Final closeout readiness: not ready
- Verify readiness: not-claimed
