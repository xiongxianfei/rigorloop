# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2 review-fix driver routing, preflight, and target bounds implementation diff
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/code-review-m2-r1.md; docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-log.md; docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-resolution.md; docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md; docs/plan.md; docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR-RFA-M2-1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-log.md
- Review resolution: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-resolution.md#code-review-m2-r1
- Reviewed milestone: M2. Review-Fix Driver Routing, Preflight, and Target Bounds
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CR-RFA-M2-1
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `8d3f251b` M2 implementation and lifecycle artifacts, especially `scripts/lifecycle_state_sync.py`, `scripts/test-artifact-lifecycle-validator.py`, `docs/workflows.md`, `skills/workflow/SKILL.md`, active plan handoff, plan index, and change metadata.
- Tracked governing branch state: `specs/review-fix-autoprogression.md`, `specs/review-fix-autoprogression.test.md`, `docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md`, and `docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml` are present in tracked branch state.
- Governing artifacts inspected: `specs/review-fix-autoprogression.md` requirements `R9a`-`R9f`, `R11`-`R22g`, `R37`, `R39`-`R40`, and `R43`; `specs/review-fix-autoprogression.test.md` `T2`-`T5`, `T8`, `T12`, and `T15`; the active plan M2 section; `docs/workflows.md`; and `skills/workflow/SKILL.md`.
- Validation evidence reviewed: `python scripts/test-artifact-lifecycle-validator.py -k review_fix`, `python scripts/test-artifact-lifecycle-validator.py -k autoprogression`, `python scripts/test-artifact-lifecycle-validator.py`, explicit-path artifact lifecycle validation, change metadata validation, and `git diff --check` recorded by M2.

## Diff summary

M2 adds a dedicated `evaluate_review_fix_autoprogression_route` route evaluator with the closed `bounded-review-fix` profile, closed proposal-side target stages through `test-spec-review`, direct-review isolation, durable authorization checks, proposal-gate checks, preflight stops for missing change ID, ambiguous artifact placement, missing review evidence, stale artifact state, contradictory workflow state, paused resume cursor mismatch, target-boundary completion, and architecture assessment routing for `architecture-required`, `architecture-not-required`, `architecture-ambiguous`, missing assessment, invalid assessment, and `target-not-applicable`. The tests add focused review-fix/autoprogression cases, and workflow guidance now documents the command shape, target enum, activation gates, architecture assessment, and out-of-scope operations.

## Findings

### CR-RFA-M2-1 - Review-fix route can continue without approved current review status

Finding ID: CR-RFA-M2-1
Severity: major
Location: `scripts/lifecycle_state_sync.py:941`
Evidence: `evaluate_review_fix_autoprogression_route` only stops when `latest_review_status` is one of `changes-requested`, `blocked`, or `inconclusive`. Any other value, including `not-started`, `not-required`, `None`, or an unsupported status string, passes this check and can advance to `_review_fix_next_stage` when `review_recording` is `recorded`, `current_gate_clean` is true, and no material findings are set.
Required outcome: Review-fix routing must fail closed unless the current review status is exactly approved before downstream continuation.
Safe resolution path: Add targeted tests for `latest_review_status` values such as `not-started`, missing, and an unsupported value. Update `evaluate_review_fix_autoprogression_route` to stop before routing unless `latest_review_status == "approved"` after recorded/current/no-open-finding checks pass. Use a deterministic stop reason such as `current-review-not-approved` or the existing `current-gate-not-clean`, then rerun the M2 validation commands.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `R20` requires the current review to be approved, recorded, current, and free of open material findings before continuation. The implementation checks recording, freshness, and material findings, but does not require `latest_review_status == "approved"`. |
| Test coverage | block | M2 tests cover non-clean statuses indirectly through other profiles and review-fix target/architecture behavior, but no review-fix test proves that missing, unknown, `not-started`, or `not-required` current review status stops before routing. |
| Edge cases | block | Test spec `T3` and `T8` require missing review evidence, stale review, open findings, and invalid continuation combinations to stop. The current route can continue with a non-approved review status when other boolean evidence fields are set. |
| Error handling | concern | Unknown review statuses are not fail-closed inside the route evaluator; they are treated as routable unless they happen to match the non-clean status set. |
| Architecture boundaries | pass | The diff keeps review-fix routing inside lifecycle validation helpers and does not add runtime services, background work, implementation, verify, PR, release, network, destructive, or external-state operations. |
| Compatibility | pass | Existing `authoring-through-plan-review` and `implementation-through-verify` functions were not modified, and the full artifact lifecycle test suite passed. |
| Security/privacy | pass | The diff adds no secret handling, credential output, network behavior, destructive command execution, or external-state behavior. |
| Derived artifact currency | pass | M2 changes canonical workflow guidance only; no generated adapter output is touched in this milestone. |
| Unrelated changes | pass | The reviewed diff is scoped to M2 route evaluation, focused tests, workflow guidance, and lifecycle bookkeeping. |
| Validation evidence | concern | The recorded validation commands are relevant and passed, but the selected test set misses the non-approved review-status route gap. |

## No-finding rationale

Not applicable. The review found one material implementation defect.

## Direct-proof gaps

- Direct proof is missing for `R20` approval gating on review-fix routes: there is no test that verifies the evaluator stops when `latest_review_status` is missing, unknown, `not-started`, or `not-required`.

## Milestone handoff state

- Reviewed milestone: M2. Review-Fix Driver Routing, Preflight, and Target Bounds
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M2, M3, M4, M5
- Next stage: review-resolution for CR-RFA-M2-1, then implementation fix and rerun code-review for M2
- Final closeout readiness: not ready
- Verify readiness: not-claimed
