# Code Review M2 R2: Workflow Profile Routing, Gate Evaluation, and Resume Semantics

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M2. Workflow Profile Routing, Gate Evaluation, and Resume Semantics
Reviewed artifact: implementation diff for CR-M2-001 and CR-M2-002 review-resolution
Review date: 2026-06-24
Recording status: recorded
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m2-r2.md, docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md, docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md, docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md, docs/plan.md, docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml
- Open blockers: none
- Next stage: implement M3
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m2-r2.md
- Review log: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md
- Review resolution: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md#code-review-m2-r2
- Reviewed milestone: M2. Workflow Profile Routing, Gate Evaluation, and Resume Semantics
- Milestone closeout: closed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: `git diff -- scripts/lifecycle_state_sync.py scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- Tracked governing branch state: approved workflow-stage autoprogression spec, approved RigorLoop workflow spec, active test spec, approved architecture, accepted ADR, active plan, review log, review-resolution record, and change metadata in the current worktree.
- Governing artifacts: `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.test.md`, `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`, the M2 section of `docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`, and `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md#code-review-m2-r1`.
- Validation evidence: `python scripts/test-artifact-lifecycle-validator.py` passed 108 tests; `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/ && python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/` passed; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml` passed; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md --path skills/workflow/SKILL.md --path docs/workflows.md --path scripts/lifecycle_state_sync.py --path scripts/artifact_lifecycle_validation.py --path scripts/test-artifact-lifecycle-validator.py` passed; scoped `git diff --check` passed.

## Diff Summary

The resolution adds terminal authoring-profile state handling to `evaluate_authoring_autoprogression_route`, so `off`, `paused`, `completed`, and unknown profile states no longer fall through to active routing. It also adds durable resume/cancel route fixtures, hardens active plan handoff parsing so unparseable or missing handoff sections fail loudly for active/blocked plans, and normalizes the active plan handoff to the structured state-sync schema.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `scripts/lifecycle_state_sync.py` now stops paused, completed, and unknown profile states before durable authorization and route continuation, matching `R2ah` and the completed-profile boundary. Active/blocked plan handoff parsing now fails on missing or unparseable handoff state, supporting contradictory-state prevention. |
| Test coverage | pass | `scripts/test-artifact-lifecycle-validator.py` adds direct tests for paused, completed, unknown state, durable resume, in-memory resume, cancellation, prose-only handoff failure, canonical handoff pass, missing active handoff failure, and `contradictory-workflow-state`; the suite passed 108 tests. |
| Edge cases | pass | The named CR-M2-001 and CR-M2-002 edge cases have direct regression coverage, including completed resume rejection and active plan/index next-stage drift. |
| Error handling | pass | Unknown profile state returns `unhandled-profile-state` with profile state `paused`; unparseable handoff returns `structured-handoff-not-parseable`; incomplete handoff fields return `structured-handoff-incomplete`. |
| Architecture boundaries | pass | The change remains in repository validation/routing helpers and lifecycle artifacts; it introduces no service, scheduler, background worker, generated output edit, or new persistence engine. |
| Compatibility | pass | Terminal archived plans are not forced into live workflow state-sync; active/blocked plans are stricter, which matches the accepted review-resolution requirement. |
| Security/privacy | pass | The diff adds no secret handling, credential output, auth bypass, network access, or private runtime data exposure. |
| Derived artifact currency | not-applicable | Generated adapter alignment remains scheduled for M4 and no generated public adapter output is touched in M2. |
| Unrelated changes | pass | The reviewed R2 diff is scoped to route/state-sync helpers, route/state-sync tests, and lifecycle evidence for M2. |
| Validation evidence | pass | The named M2 review-resolution validation commands passed and were recorded in `change.yaml` and the active plan. |

## No-Finding Rationale

CR-M2-001 is resolved because `profile_state` is now an explicit terminal gate before normal routing: paused profiles stop without a durable resume record, completed profiles stop or reject resume, and unknown states fail closed as paused. CR-M2-002 is resolved because active/blocked plan rows no longer skip state-sync when a handoff is missing or not parseable, and the actual active plan handoff was normalized and validated. The regression tests directly exercise the review findings rather than relying on code-shape inference.

## Direct-Proof Gaps

None for M2 R2. The implementation profile remains a fixture-backed repository validator helper rather than a deployed runtime service.

## Milestone Handoff State

- Reviewed milestone: M2. Workflow Profile Routing, Gate Evaluation, and Resume Semantics
- Milestone state after review: closed
- Required review-resolution: no
- Remaining in-scope implementation milestones: M3, M4, M5
- Next stage: implement M3
- Final closeout readiness: not-ready; implementation milestones M3 through M5, explain-change, verify, and PR handoff remain.

## Residual Risks

- The route evaluator is a validation/helper surface for the repository workflow; M3 still needs to align the individual stage skills with the now-reviewed routing terms and review-independence boundary.
