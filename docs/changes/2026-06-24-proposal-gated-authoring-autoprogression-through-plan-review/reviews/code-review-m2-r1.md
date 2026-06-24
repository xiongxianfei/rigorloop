# Code Review M2 R1: Workflow Profile Routing, Gate Evaluation, and Resume Semantics

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M2. Workflow Profile Routing, Gate Evaluation, and Resume Semantics
Reviewed artifact: implementation diff for M2 workflow profile routing and lifecycle validation
Review date: 2026-06-24
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m2-r1.md, docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md, docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md, docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md, docs/plan.md, docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml
- Open blockers: material findings require review-resolution before M3
- Next stage: review-resolution M2
- Review status: changes-requested
- Material findings: CR-M2-001, CR-M2-002
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md
- Review resolution: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md#code-review-m2-r1
- Reviewed milestone: M2. Workflow Profile Routing, Gate Evaluation, and Resume Semantics
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 review-resolution, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CR-M2-001, CR-M2-002
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: `git diff -- skills/workflow/SKILL.md docs/workflows.md scripts/lifecycle_state_sync.py scripts/test-artifact-lifecycle-validator.py docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- Governing artifacts: `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.test.md`, `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`, and the M2 section of `docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`.
- Prior review evidence: `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m1-r1.md`.
- Validation evidence reviewed: `python scripts/test-artifact-lifecycle-validator.py` passed 102 tests; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/workflow/SKILL.md --path docs/workflows.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml` passed with the existing lifecycle-language warning in `specs/rigorloop-workflow.md`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml` passed; `git diff --check -- skills/workflow/SKILL.md docs/workflows.md scripts/lifecycle_state_sync.py scripts/artifact_lifecycle_validation.py scripts/validate-artifact-lifecycle.py scripts/test-artifact-lifecycle-validator.py tests/fixtures/artifact-lifecycle docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review` passed.

## Diff Summary

M2 adds authoring-profile route evaluation helpers, route tests for gate activation, architecture assessment, non-clean review pauses, transition budget, resume idempotence, and plan-review completion, plus workflow guidance in `skills/workflow/SKILL.md` and `docs/workflows.md`. It also updates active lifecycle handoff state to request M2 code-review.

## Findings

### CR-M2-001 - Paused and completed profile states can restart automatically

Finding ID: CR-M2-001
Severity: major
Status: open
Evidence: `scripts/lifecycle_state_sync.py:403` reads `profile_state`, but the route evaluator proceeds through durable authorization and proposal-gate checks to current-stage routing at `scripts/lifecycle_state_sync.py:447` without stopping when `profile_state` is `paused` or `completed`. The final return at `scripts/lifecycle_state_sync.py:468` can convert those states back to `active`.

Why this matters: The approved contract requires paused profiles to require explicit resume and completed profiles not to restart automatically. A fixture with `profile_state: paused`, durable authorization, a clean proposal gate, and `current_stage: proposal-review` can route to `spec` without explicit resume. A completed profile can similarly restart from an earlier stage.

Required outcome: The route evaluator must keep a paused profile stopped unless explicit resume authorization is represented and accepted, and it must keep a completed profile stopped rather than restarting. Add regression tests for paused-without-resume, completed-no-restart, and any explicit-resume path the implementation chooses to support in M2.

Safe resolution path: Add profile-state guards before route continuation, update `scripts/test-artifact-lifecycle-validator.py`, and rerun the M2 validation commands.

### CR-M2-002 - M2 state-sync validation skips the active plan handoff

Finding ID: CR-M2-002
Severity: major
Status: open
Evidence: `scripts/lifecycle_state_sync.py:13` requires `Latest review evidence` in structured handoff summaries, while the active plan records `Last reviewed milestone` at `docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md:74` and a prose review status at `docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md:75`. Because the handoff is not in the validator's recognized structured shape, the M2 validation command can pass without checking that the plan body owns and agrees with the current next-stage state.

Why this matters: M2 is specifically responsible for workflow-state validation that prevents contradictory or duplicate transitions. The recorded validation evidence claims state-sync coverage, but the active plan's live handoff is not actually being parsed as structured workflow state.

Required outcome: Either update the active plan handoff to the structured schema the validator expects or intentionally extend the validator to accept the repository's active handoff schema. Then rerun lifecycle validation and record evidence that the active plan handoff is parsed and checked.

Safe resolution path: Align the plan handoff fields and/or validator tests in one resolution patch. The resolved state should still route M2 to review-resolution until both findings are fixed and rereviewed.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | fail | CR-M2-001 violates explicit paused/completed profile semantics; CR-M2-002 weakens required contradictory-state validation evidence. |
| Test coverage | fail | Existing route tests cover non-clean statuses, resume, and budget but not paused/completed profile-state restart prevention; lifecycle validation does not prove the active handoff was parsed. |
| Edge cases | fail | Paused profile without explicit resume and completed profile restart are untested and currently route onward. |
| Error handling | pass-with-findings | Several stop reasons are handled, but profile-state stop handling is incomplete. |
| Architecture boundaries | pass | The implementation remains within repository validation and workflow guidance; no service or background worker is introduced. |
| Compatibility | pass-with-findings | Default-off and isolated-invocation cases are covered, but resume/completion compatibility is incomplete. |
| Security/privacy | pass | The diff adds no secret handling, credentials, or external calls. |
| Derived artifact currency | not-applicable | Generated adapter alignment remains scheduled for M4. |
| Unrelated changes | pass | The reviewed diff is scoped to M2 routing, lifecycle validation, workflow guidance, and lifecycle evidence. |
| Validation evidence | fail | The test command passes, but the missing paused/completed cases and skipped active-plan handoff make the evidence insufficient for M2 closeout. |

## Milestone Handoff State

- Reviewed milestone: M2. Workflow Profile Routing, Gate Evaluation, and Resume Semantics
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Open findings: CR-M2-001, CR-M2-002
- Remaining in-scope implementation milestones: M2 review-resolution, M3, M4, M5
- Next stage: review-resolution M2
- Final closeout readiness: not-ready; M2 material findings, later implementation milestones, explain-change, verify, and PR handoff remain.

## Residual Risks

- Until CR-M2-001 is fixed, route evaluation can violate the profile's explicit pause and completion boundaries.
- Until CR-M2-002 is fixed, state-sync validation evidence can overstate what the active plan handoff actually proved.
