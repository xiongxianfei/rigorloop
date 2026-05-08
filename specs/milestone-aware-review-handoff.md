# Milestone-Aware Review Handoff

## Status

- approved

## Related proposal

- [Milestone-Aware Review Handoff](../docs/proposals/2026-05-07-milestone-aware-review-handoff.md)

## Goal and context

This spec defines milestone-aware handoff behavior for workflow-managed standard workflow execution when a concrete plan contains multiple implementation milestones.

The current standard workflow routes a clean final implementation milestone into final closeout: `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`. This spec narrows milestone behavior so a clean review of a non-final implementation milestone closes the reviewed milestone and routes to the next in-scope implementation milestone.

This is a workflow-stage policy change. It amends the behavior described by `specs/workflow-stage-autoprogression.md` and `specs/rigorloop-workflow.md` for milestone-based standard workflow flows. It does not change manual skill invocation, bugfix, review-only, merge, release, deploy, or PR-opening behavior.

## Glossary

- `milestone-based plan`: a concrete execution plan that defines one or more implementation milestones.
- `implementation milestone`: a planned milestone that changes authored source, tests, workflow guidance, generated-output source, or other in-scope implementation surfaces.
- `lifecycle-closeout milestone`: a planned milestone or section that tracks downstream gates such as `ci-maintenance`, `explain-change`, `verify`, and PR handoff without adding implementation scope.
- `in-scope implementation milestone`: an implementation milestone that still belongs to the current change after any approved plan revision.
- `Milestone state`: the single authoritative state field for an implementation milestone.
- `milestone handoff summary`: contributor-visible plan or review output that states the reviewed milestone, its state, remaining implementation milestones, next stage, and final closeout readiness.
- `clean review`: a `code-review` result of `clean-with-notes` with no required review-resolution.
- `required review-resolution`: review-resolution triggered by material findings, required-change findings, non-final dispositions, owner decisions, or another approved review-resolution trigger.
- `final closeout readiness`: whether the current workflow state may enter the final closeout sequence.

## Examples first

### Example E1: clean non-final milestone routes to the next milestone

Given a workflow-managed standard workflow change has planned implementation milestones `M1`, `M2`, and `M3`
And `implement M1` has completed targeted validation and handed the slice to `code-review`
When `code-review M1` returns `clean-with-notes`
Then `M1` is marked `closed`
And the next stage is `implement M2`
And final closeout readiness is `not ready` because implementation milestones remain.

### Example E2: clean final milestone routes to final closeout

Given a workflow-managed standard workflow change has planned implementation milestones `M1`, `M2`, and `M3`
And `M1` and `M2` are already `closed`
And `implement M3` has completed targeted validation and handed the slice to `code-review`
When `code-review M3` returns `clean-with-notes`
Then `M3` is marked `closed`
And the next stage is `ci-maintenance` when triggered; otherwise it is `explain-change`
And final closeout readiness is `ready` because all in-scope implementation milestones are closed and code-review is complete.

### Example E3: findings stay on the same milestone

Given `implement M1` handed the slice to `code-review`
When `code-review M1` returns `changes-requested`
Then `M1` is marked `resolution-needed`
And the next stage is `review-resolution M1`
And the workflow does not advance to `M2` or final closeout until findings are dispositioned, required fixes are validated, and required re-review or explicit review closeout is complete.

### Example E4: ambiguous remaining milestones block final closeout

Given `code-review M1` is clean
And the active plan does not clearly show whether additional in-scope implementation milestones remain
When deciding the next stage
Then the workflow does not hand off to final closeout
And the output requires a plan update or returns `inconclusive`.

### Example E5: removed milestone requires plan revision first

Given `M2` is still listed as an implementation milestone
And the contributor believes `M2` no longer belongs in the current change
When `M1` review is clean
Then the workflow does not skip `M2` to make final closeout available
And the plan must be revised before handoff
And final closeout may proceed only if no in-scope implementation milestone remains open or unresolved after that revision.

### Example E6: lifecycle-closeout milestone does not block final closeout

Given all implementation milestones are `closed`
And the plan also has a lifecycle-closeout milestone for `ci-maintenance`, `explain-change`, `verify`, and PR handoff
When the final implementation milestone review is clean
Then final closeout readiness is `ready`
And the lifecycle-closeout milestone is not treated as an unfinished implementation milestone.

## Requirements

R1. The milestone-aware handoff rule MUST apply to workflow-managed standard workflow execution when the active plan is milestone-based.

R1a. The rule MUST NOT change isolated `code-review`, isolated `verify`, review-only, manual skill invocation, or bugfix handoff behavior.

R1b. The rule MUST NOT add merge, deploy, release, tag publication, branch deletion, rollback, or other destructive or externally publishing actions to default autoprogression.

R2. Each in-scope implementation milestone MUST have exactly one `Milestone state` when milestone state is recorded or updated under this contract.

R2a. The allowed `Milestone state` values are exactly:
- `planned`
- `implementing`
- `review-requested`
- `resolution-needed`
- `closed`

R2b. `implementation-complete` and `review-clean` MUST NOT be used as `Milestone state` values.

R2c. Implementation completion, targeted validation, clean review, review ID, and review-resolution status MAY be recorded as milestone evidence fields or validation notes.

R3. `implement` MUST transition a started milestone from `planned` to `implementing` when implementation work begins.

R3a. After implementation and targeted validation complete, `implement` MUST hand the milestone to `code-review` and transition the milestone to `review-requested` when no stop condition applies.

R3b. `implement` MUST NOT set plan readiness to `Ready for final closeout` while any in-scope implementation milestone remains unreviewed, unresolved, or open.

R4. `code-review` MUST identify the reviewed milestone and inspect the active plan before choosing a next stage in a workflow-managed milestone-based flow.

R4a. If review is `clean-with-notes` and no review-resolution is required, `code-review` MUST transition the reviewed milestone from `review-requested` to `closed`.

R4b. If a clean reviewed milestone is not the final in-scope implementation milestone, the next stage MUST be `implement <next in-scope implementation milestone>`, not `verify`.

R4c. If a clean reviewed milestone is the final in-scope implementation milestone, the next stage MUST be `ci-maintenance` when triggered; otherwise it MUST be `explain-change`, unless another stop condition applies.

R4d. If `code-review` cannot edit the active plan, its output MUST explicitly require the milestone state and handoff summary update before downstream routing relies on that state.

R5. If `code-review` produces findings that require review-resolution, fixes, owner decision, or re-review, the reviewed milestone MUST transition to `resolution-needed`.

R5a. While a milestone is `resolution-needed`, the workflow MUST NOT advance to the next implementation milestone or final closeout.

R5b. `review-resolution` and implementation fixes MUST stay attached to the same reviewed milestone until findings are dispositioned, required fixes are validated, and required re-review or explicit review closeout is complete.

R5c. When accepted fixes require re-review, the milestone MUST return to `review-requested` for the same milestone before the rerun `code-review`.

R5d. A `resolution-needed` milestone MAY transition to `closed` only after findings are dispositioned, required fixes are validated, and re-review is clean or explicitly not required by the review contract.

R5e. A `needs-decision` disposition or equivalent owner-decision blocker MUST stop downstream routing until resolved or explicitly deferred by an authorized owner under the governing review-resolution rules.

R6. If `code-review` is inconclusive because evidence is missing, the milestone MUST remain `review-requested` unless a different stop condition requires a stronger state.

R6a. An inconclusive milestone review MUST NOT hand off to final closeout.

R6b. An inconclusive milestone review MUST name the missing evidence or required plan update.

R7. Milestones MUST NOT be postponed solely to make final closeout available.

R7a. If a planned implementation milestone no longer belongs in the current change, the plan MUST be revised before downstream handoff relies on its removal from scope.

R7b. After plan revision, final closeout MAY proceed only when no in-scope implementation milestone remains open or unresolved.

R8. Milestone-based plans and milestone review outputs MUST expose a current handoff summary when implementation or review changes milestone readiness.

R8a. The handoff summary MUST include:
- current milestone
- current milestone state
- last reviewed milestone, when one exists
- review status, when review has occurred
- remaining in-scope implementation milestones
- next stage
- final closeout readiness
- reason final closeout is or is not ready

R8b. For a non-final clean reviewed milestone, the handoff summary MUST state that final closeout readiness is `not ready` and must name remaining in-scope implementation milestones.

R8c. For a final clean reviewed milestone, the handoff summary MUST state that final closeout readiness is `ready` and that all in-scope implementation milestones are closed and code-review is complete.

R8d. For a findings review, the handoff summary MUST state that final closeout readiness is `not ready` and that review findings remain unresolved or require owner decision.

R9. Lifecycle-closeout milestones MUST be distinguishable from implementation milestones for final-closeout readiness decisions.

R9a. A lifecycle-closeout milestone for `ci-maintenance`, `explain-change`, `verify`, PR handoff, or final plan closeout MUST NOT be treated as an open implementation milestone blocking entry into final closeout.

R9b. A milestone that still contains implementation work MUST be treated as an implementation milestone even if it also mentions downstream lifecycle gates.

R10. The milestone-aware handoff contract MUST preserve the existing standard workflow downstream stages: `code-review`, `review-resolution` when triggered, `ci-maintenance` when triggered, `explain-change`, `verify`, and `pr`.

R10a. The contract MUST NOT remove or weaken required review-resolution closeout before final `explain-change`, `verify`, or `pr`.

R11. The first implementation slice for this contract MUST use guidance and static wording checks only.

R11a. The first implementation slice MUST NOT add executable plan-state validation.

R11b. The first implementation slice MUST NOT add a standalone `review-resolution` skill.

## Inputs and outputs

Inputs:

- workflow lane and invocation context
- active plan and current milestone
- milestone state and milestone evidence
- current `implement`, `code-review`, and review-resolution results
- remaining in-scope implementation milestones
- targeted validation evidence
- explicit user pause or stop instructions
- stop conditions from governing workflow, review, or plan artifacts

Outputs:

- updated or required milestone state
- milestone handoff summary
- next stage or stop reason
- final closeout readiness and reason
- required plan update when the acting stage cannot edit the plan
- review-resolution requirement when findings exist

## State and invariants

- A milestone has one `Milestone state`.
- `review-requested` is the post-implementation handoff state.
- `closed` is the clean-review or resolved-findings state.
- `implementation-complete` and `review-clean` are evidence descriptions, not milestone states.
- A clean review of one milestone does not imply the whole plan is ready for final closeout.
- Final closeout is ready only when every in-scope implementation milestone is `closed` and no required review-resolution remains open.
- Findings, fixes, and re-review stay on the same milestone until that milestone can close or stop for owner decision.
- Direct or review-only stage requests remain isolated unless the user asks to continue.

## Error and boundary behavior

- If the active plan is missing when milestone-aware routing depends on it, the workflow MUST stop or return `inconclusive` rather than infer final closeout readiness.
- If the plan does not clearly distinguish remaining in-scope implementation milestones from lifecycle-closeout work, the workflow MUST require a plan update before handing off to final closeout.
- If the reviewed milestone cannot be identified, `code-review` MUST return `inconclusive` or require a plan update.
- If targeted validation fails during `implement`, the workflow MUST stop before `code-review`.
- If `code-review` findings require product, spec, architecture, ADR, scope, or owner decisions, the workflow MUST stop under the governing stop-condition rules rather than advance to the next milestone.
- If an explicit user pause applies after a milestone review, the workflow MUST report the correct next stage and stop before entering it.
- If local tool permissions prevent plan updates, the acting stage MUST report the required update instead of claiming the state is already reconciled.

## Compatibility and migration

- This change is a workflow-behavior clarification for milestone-based standard workflow flows.
- Existing untouched plans are not invalid solely because they lack the new handoff summary or milestone-state vocabulary.
- Plans touched by this change or later relied on for milestone-aware routing should adopt the single-state vocabulary and handoff summary when milestone readiness changes.
- Existing lifecycle-closeout guidance remains valid when it distinguishes downstream gates from implementation milestones.
- Existing review-resolution artifact rules, disposition values, and closeout blockers remain valid.
- Existing manual skill invocation, bugfix, and isolated-stage behavior remains unchanged.
- Rollback restores the previous `clean-with-notes -> final closeout` behavior for all workflow-managed standard workflow `code-review` handoffs.

## Observability

- Milestone state transitions are observable through active plan updates or explicit required-update text in stage output.
- `code-review` output should expose the reviewed milestone, review status, milestone state after review, remaining in-scope implementation milestones, next stage, final closeout readiness, and reason.
- `implement` output should expose targeted validation evidence and the `review-requested` handoff.
- Final closeout readiness remains observable through active plan state, review-resolution closeout, and the verify stage output.
- No new logs, metrics, traces, or audit events are required in the first implementation slice.

## Security and privacy

- This change does not alter authentication, authorization, secrets handling, or data exposure.
- Plan updates, review outputs, and handoff summaries MUST NOT include secrets, credentials, tokens, private keys, or host-specific sensitive data.

## Accessibility and UX

No user interface is involved.

## Performance expectations

No runtime performance behavior is involved.

The workflow should continue to use bounded evidence reads and static wording checks for the first implementation slice. The first implementation slice must not add plan-state parsing that could create new validation-runtime costs.

## Edge cases

EC1. Clean non-final milestone review: covered by `R4a`, `R4b`, and `R8b`.

EC2. Clean final milestone review: covered by `R4a`, `R4c`, and `R8c`.

EC3. Review findings on a non-final milestone: covered by `R5`, `R5a`, `R5b`, and `R8d`.

EC4. Accepted fixes requiring re-review: covered by `R5c`.

EC5. Findings closed without re-review when explicitly allowed by the review contract: covered by `R5d`.

EC6. Inconclusive review due to missing evidence: covered by `R6`, `R6a`, and `R6b`.

EC7. Ambiguous remaining implementation milestones: covered by `R6b` and error behavior.

EC8. Milestone removed from current scope: covered by `R7`, `R7a`, and `R7b`.

EC9. Lifecycle-closeout milestone after final implementation milestone: covered by `R9` and `R9a`.

EC10. Mixed implementation and lifecycle-closeout milestone: covered by `R9b`.

EC11. Isolated direct `code-review`: covered by `R1a`.

EC12. Explicit user pause after clean milestone review: covered by error and boundary behavior.

EC13. Stage cannot edit the active plan: covered by `R4d`.

EC14. Existing untouched plan lacks the new handoff summary: covered by compatibility and migration.

## Non-goals

- Adding executable plan-state validation in the first implementation slice.
- Adding a standalone `review-resolution` skill.
- Requiring every milestone to be a separate PR.
- Changing manual skill invocation, bugfix, review-only, direct `pr`, merge, release, deploy, or destructive Git behavior.
- Replacing review-resolution artifact rules or disposition values.
- Hand-editing generated Codex compatibility output or generated public adapter package output.
- Creating a new storage model, hosted service, runtime data flow, API, UI, or schema.

## Acceptance criteria

AC1. The updated workflow contract states that clean `code-review` of a non-final implementation milestone closes that milestone and routes to the next in-scope implementation milestone, not `verify`.

AC2. The updated workflow contract states that clean `code-review` of the final in-scope implementation milestone closes that milestone and routes to final closeout.

AC3. The updated workflow contract defines exactly one `Milestone state` field with the allowed values `planned`, `implementing`, `review-requested`, `resolution-needed`, and `closed`.

AC4. The updated workflow contract states that `implementation-complete` and `review-clean` are evidence descriptions, not milestone states.

AC5. The affected skills guide `implement`, `code-review`, and `plan` to use same-milestone handoff, same-milestone review-resolution, and current handoff summaries.

AC6. Static wording checks or equivalent test-spec proof covers the new milestone-aware guidance without adding executable plan-state validation in the first implementation slice.

AC7. Generated Codex and adapter output is regenerated or proven in sync when canonical skill sources change.

AC8. Validation evidence proves that touched proposal/spec/workflow/skill/generated-output surfaces satisfy selector-selected checks and do not introduce generated-output drift.

## Open questions

None.

## Next artifacts

- Current consuming implementation: `code-review M2` after M2 implementation handoff under the active single-workflow-lane execution plan.
- Continue the active consuming plan's milestone loop with M3 through M5 until all in-scope implementation milestones are closed.

## Follow-on artifacts

- `plan`: [Milestone-Aware Review Handoff Execution Plan](../docs/plans/2026-05-07-milestone-aware-review-handoff.md)
- `test-spec`: [Milestone-Aware Review Handoff Test Spec](milestone-aware-review-handoff.test.md)

## Readiness

Approved.

Original follow-on execution plan is done. The matching test spec remains active as the regression surface for current consuming workflow-governance plans. No spec-stage blocker remains.
