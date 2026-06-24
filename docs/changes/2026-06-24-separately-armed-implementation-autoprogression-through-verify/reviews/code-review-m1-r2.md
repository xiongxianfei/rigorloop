# Code Review M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M1 profile schema and authorization policy implementation diff after CR-M1-R1-F1 resolution
Status: clean-with-notes

## Review inputs

- Diff/review surface: `schemas/change.schema.json`, `scripts/validate-change-metadata.py`, `scripts/query-change-record.py`, `scripts/test-change-metadata-validator.py`, `tests/fixtures/change-metadata/implementation-autoprogression-container-next-stage/change.yaml`, active plan and change metadata updates.
- Tracked governing branch state: local branch `proposal/implementation-autoprogression-through-verify`; governing artifacts are present in the working tree for this change.
- Governing artifacts: `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`, `specs/implementation-autoprogression-through-verify.test.md`, `docs/plans/2026-06-24-implementation-autoprogression-through-verify.md`.
- Review-resolution evidence: `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/review-resolution.md` records CR-M1-R1-F1 accepted and resolved.
- Validation evidence reviewed/rerun: `python scripts/test-change-metadata-validator.py -k autoprogression_policy`, `python scripts/test-change-metadata-validator.py -k forbidden_live_state`, `python scripts/test-change-metadata-validator.py`, and direct validation of the invalid container-level fixture.

## Diff summary

M1 now supports the `implementation-through-verify` profile in change metadata schema and semantic validation, including independent named profile records, required implementation `phase` and `state`, cancellation fields, query-helper evidence exposure, and fail-closed profile validation. The R1 finding was resolved by centralizing forbidden live workflow-state checks in `reject_autoprogression_live_state_fields`, applying that helper to named containers and per-record validation, closing the schema autoprogression container against unknown sibling keys, and accumulating schema plus semantic validation errors so structural rejection still includes the R7er policy explanation.

## Findings

No blocking or required-change findings.

## Checklist coverage

1. Spec alignment: pass. The implementation covers M1 requirements for closed profile values, independent implementation-profile records, phase/state persistence fields, and the policy/live-state boundary required by `R7er`, `R7et`, and `R7ev`.
2. Test coverage: pass. Focused tests cover valid named records, required implementation fields, invalid phase/state/profile identity, forbidden fields in containers and records, query-helper exposure, and the unrelated top-level `workflow` boundary.
3. Edge cases: pass. The direct fixture `tests/fixtures/change-metadata/implementation-autoprogression-container-next-stage/change.yaml` proves named-record container `next_stage` is rejected; tests also cover the other forbidden fields and all five together.
4. Error handling: pass. Unknown profiles, malformed workflow/autoprogression shapes, missing fields, persistence failures, fallback paths, bad timestamps, and cancellation shape are rejected or validated in the existing and added tests.
5. Architecture boundaries: pass. The diff stays within M1 metadata/schema/query/test surfaces and does not introduce orchestration services, background execution, PR actions, or generated adapter changes.
6. Compatibility: pass. Legacy single-record authoring profile behavior remains covered, and schema compatibility retains existing legacy metadata fields such as `state`, `request`, and persistence fields.
7. Security/privacy: pass. The profile policy surface remains limited to workflow attribution and policy fields; no secret-bearing fields, credential reads, or external effects were added.
8. Derived artifact currency: pass. M1 did not touch generated adapter or generated skill output.
9. Unrelated changes: pass. The reviewed M1 diff is scoped to schema, metadata validation/query helpers, tests/fixture, and lifecycle state records required by the workflow.
10. Validation evidence: pass. Rerun evidence shows the focused and full metadata suites pass, while the previously passing invalid fixture now fails with both structural and semantic diagnostics.

## No-finding rationale

The R1 gap was the only material issue found in the M1 review surface. The fix now checks forbidden live workflow-state fields at the named-record container level and at each nested record, and the regression suite directly proves both rejection and non-overrejection. Existing legacy behavior remains covered, and the resolution artifacts validate in structure and closeout mode.

## Residual risks

M1 only closes profile schema and authorization-policy validation. Activation routing, test-spec settlement, phase execution boundaries, and reviewer-owned correction loops remain open for M2 and M3.

## Milestone handoff state

- Reviewed milestone: M1. Profile schema and authorization policy
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no
- Remaining in-scope implementation milestones: M2, M3, M4, M5
- Next stage: implement M2
- Final closeout readiness: not ready
- Verify readiness: not-claimed
