# Workflow Stage Autoprogression

## Status
- approved

## Related proposal

- [Workflow stage autoprogression](../docs/proposals/2026-04-21-workflow-stage-autoprogression.md)
- [Milestone-aware review handoff](../docs/proposals/2026-05-07-milestone-aware-review-handoff.md)
- [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md)

## Goal and context

This spec defines when the repository workflow should continue automatically to the next downstream stage and when it should stop and wait instead.

The existing workflow contract already defines stage order and stage classification, but it does not define a general continuation rule. That leaves agents pausing after already-complete stages even when the next stage is already known, required by the current workflow state, and does not need a new user decision. This spec closes that gap without broadening into merge, deploy, release, or destructive Git automation.

In v1, this autoprogression contract applies only to:

- standard workflow execution-flow handoffs; and
- authoring-to-review handoffs for `proposal`, `spec`, and `architecture` when those review stages are the next mandatory or triggered downstream step.

Manual skill invocations and bugfix skill invocations remain out of scope for this automation mechanism in v1 unless the user explicitly asks to continue through the standard workflow.

This spec is amended by the milestone-aware review handoff contract for workflow-managed standard workflow changes that use a milestone-based plan. In that case, a clean review of one non-final implementation milestone is not proof that the whole implementation set is ready for final closeout.

This spec is also amended by the single standard workflow contract. After implementation milestones and required review-resolution closeout are complete, the final workflow-managed sequence is `ci-maintenance` when triggered, then `explain-change`, then `verify`, then `pr`.

## Glossary

- `workflow-managed completion flow`: a change flow where the agent is carrying work through its normal downstream stages toward completion under the standard workflow.
- `workflow-managed context`: downstream-continuation context carried from the prior stage or requested explicitly by the user as end-to-end completion, rather than inferred from a direct one-stage invocation alone.
- `isolated stage request`: a user request for the output of one stage only, such as standalone `proposal-review`, `spec-review`, `code-review`, `verify`, or `explain-change`.
- `standard workflow`: the single workflow path for contributed changes, with mandatory, conditional, on-demand, and periodic stages.
- `manual skill invocation`: a user-requested run of one individual skill for focused output. It is isolated by default and does not imply that upstream or downstream workflow stages are complete.
- `current workflow state`: the active stage, triggered conditions, plan state, review state, and user invocation context that determine the next downstream stage.
- `downstream stage`: the next stage or stages that follow from the current workflow state and current stage outcome.
- `stop condition`: a documented reason the agent must not continue automatically.
- `PR-opening prerequisites`: the minimum branch, worktree, and readiness conditions required before the `pr` stage opens a pull request.
- `milestone-based plan`: a concrete execution plan with one or more in-scope implementation milestones that must be implemented, reviewed, and closed before final closeout readiness.
- `in-scope implementation milestone`: a planned milestone whose current scope still includes implementation work for the change.
- `lifecycle-closeout milestone`: a milestone or plan step that contains only downstream lifecycle gates such as `ci-maintenance`, `explain-change`, `verify`, PR handoff, release, deploy, or other closeout work, and not unfinished implementation work.
- `review-requested`: the milestone state after implementation and targeted validation are complete and the milestone has been handed to `code-review`.
- `resolution-needed`: the milestone state after `code-review` produces findings that require review-resolution, fixes, owner decision, or re-review before the milestone can close.

## Examples first

### Example E1: standard workflow implementation continues into review

Given a non-trivial standard workflow change has completed `implement`
When milestone validation passes and no stop condition applies
Then the agent continues into `code-review` without waiting for the user to invoke it manually.

### Example E2: authoring work continues into the matching review gate

Given a change is in a workflow-managed completion flow and `spec` completes successfully
When `spec-review` is the next mandatory or triggered downstream stage
Then the agent continues into `spec-review` without waiting for a redundant user confirmation.

### Example E3: review-only request stops after the requested stage

Given the user asks only for `code-review`
When the review result is returned
Then the agent does not continue into `verify` or `pr` unless the user asks to continue.

### Example E4: code-review findings enter the review-resolution loop

Given a standard workflow change in a workflow-managed completion flow reaches `code-review`
When the findings are accepted for fix
Then the agent resolves them, reruns `code-review`, and only proceeds after the review gate is satisfied.

### Example E5: PR creation happens automatically when ready

Given a workflow-managed completion flow reaches `pr`
When the base branch is known, the review branch exists or can be created safely, unrelated changes are excluded, and PR readiness checks pass
Then the agent opens the pull request directly and reports the PR URL.

### Example E6: PR creation stops on branch or scope blockers

Given a change reaches `pr`
When the correct base branch is unknown or unrelated tracked changes are included
Then the agent does not open the pull request and instead reports the blocker explicitly.

### Example E7: explicit user pause overrides autoprogression

Given the user says `stop after code-review`
When the workflow reaches that stage
Then the agent returns the review result and stops there.

### Example E8: direct `pr` still opens the PR when ready

Given the user directly invokes `pr`
When PR-opening prerequisites pass
Then the `pr` stage opens the pull request normally, and isolation only prevents any downstream continuation beyond `pr`.

### Example E9: direct stage invocation stays isolated by default

Given the user directly invokes `verify` on a change
When the request does not also ask to carry the change through completion
Then the invocation is treated as isolated and does not auto-continue into `explain-change` or `pr`.

### Example E10: manual skill and bugfix invocations remain outside v1 autoprogression

Given a manual skill invocation or bugfix skill invocation completes one stage
When one stage completes
Then this v1 autoprogression contract does not itself require automatic continuation into the next stage for that change.

### Example E11: non-final milestone review continues to the next milestone

Given a workflow-managed standard workflow change uses a milestone-based plan
And `code-review` returns clean for a clean non-final implementation milestone
When another in-scope implementation milestone remains open
Then the workflow closes the reviewed milestone and continues to the next in-scope implementation milestone instead of `verify`.

### Example E12: final milestone review continues to final closeout

Given a workflow-managed standard workflow change uses a milestone-based plan
And `code-review` returns clean for a clean final implementation milestone
When all in-scope implementation milestones are closed and no required review-resolution remains open
Then the workflow continues to `ci-maintenance` when triggered; otherwise it continues to `explain-change`, followed by `verify` and `pr`.

### Example E13: milestone findings stay on the reviewed milestone

Given a workflow-managed standard workflow change reaches `code-review` for milestone `M1`
When review findings require review-resolution, fixes, owner decision, or re-review
Then milestone `M1` moves to `resolution-needed` and the workflow does not advance to the next milestone or `verify`.

### Example E14: lifecycle closeout does not block final closeout as implementation work

Given all in-scope implementation milestones are closed
And the remaining plan work is a lifecycle-closeout milestone
When no required review-resolution remains open
Then the workflow may enter final closeout instead of treating the lifecycle closeout as unfinished implementation.

### Example E15: explain-change precedes final verify

Given implementation milestones are closed
And required review-resolution is closed
And no `ci-maintenance` trigger is active
When workflow-managed execution continues
Then the next stage is `explain-change`, followed by `verify`, then `pr`.

### Example E16: CI maintenance precedes explain-change when triggered

Given implementation milestones are closed
And required review-resolution is closed
And hosted workflow automation, validation automation, or related platform configuration must be changed
When workflow-managed execution continues
Then the next stage is `ci-maintenance`, followed by `explain-change`, `verify`, and `pr`.

## Requirements

R1. The workflow MUST distinguish workflow-managed completion flows from isolated stage requests.

R1a. A request that asks only for critique, readiness, audit, or explanation from a single review-oriented stage MUST be treated as an isolated stage request unless the user also asks to continue beyond that stage.

R1b. Isolated stage requests MUST NOT trigger automatic continuation into downstream stages unless the user explicitly asks to continue.

R1c. Direct user invocation of a single review-oriented, verification, or explanation stage MUST be treated as isolated by default unless workflow-managed context is carried from a prior stage or the user explicitly asks for end-to-end continuation.

R1d. Direct user invocation of `pr` remains in scope for v1. Isolation prevents downstream continuation beyond `pr`, but it MUST NOT downgrade the `pr` stage's own normal behavior of opening the pull request when readiness passes.

R2. In a workflow-managed completion flow, when a stage completes successfully, the agent MUST continue to the next mandatory or triggered downstream stage for the current workflow state unless continuation is explicitly waived, blocked, or paused.

R2a. Autoprogression MUST follow the current workflow state's next mandatory or triggered downstream stage, not a universal stage pair.

R2b. In v1, this autoprogression contract applies only to standard workflow execution flow and authoring-to-review handoffs. It MUST NOT change manual skill invocation or bugfix skill invocation downstream behavior by implication.

R2ba. In v1, standard workflow execution-flow autoprogression begins at `implement` and continues through `pr`.

R2c. When the current workflow state includes `proposal-review` as the next mandatory or triggered downstream stage, successful `proposal` completion MUST continue into `proposal-review` unless a stop condition applies.

R2d. When the current workflow state includes `spec-review` as the next mandatory or triggered downstream stage, successful `spec` completion MUST continue into `spec-review` unless a stop condition applies.

R2e. When the current workflow state includes `architecture-review` as the next mandatory or triggered downstream stage, successful `architecture` completion MUST continue into `architecture-review` unless a stop condition applies.

R2f. Upstream of `implement`, v1 covers only these authoring-to-review handoffs:
- `proposal -> proposal-review`
- `spec -> spec-review`
- `architecture -> architecture-review`

R2g. Review-to-next-authoring-stage transitions such as `proposal-review -> spec`, `spec-review -> architecture`, or `architecture-review -> plan` remain out of scope unless a later approved change adds them.

R3. In the standard workflow execution flow, successful `implement` completion MUST continue into `code-review` unless a stop condition applies.

R3a. In the standard workflow execution flow, if `code-review` finds issues that can be resolved without a new user decision, the workflow MUST enter the `review-resolution` loop for the reviewed scope and rerun `code-review` before proceeding.

R3b. In the standard workflow execution flow, once `code-review` is satisfied and no accepted findings remain unresolved, the workflow MUST continue to the next mandatory or triggered downstream stage for the current workflow state and active plan rather than assuming `verify` is always next.

R3ba. In a milestone-based plan, a clean non-final implementation milestone MUST close the reviewed milestone and continue to the next in-scope implementation milestone, not `verify`.

R3bb. In a milestone-based plan, a clean final implementation milestone MUST close the reviewed milestone and continue to final closeout only when all in-scope implementation milestones are closed and no required review-resolution remains open.

R3bc. In a milestone-based plan, when `code-review` produces findings that require review-resolution, fixes, owner decision, or re-review, the reviewed milestone MUST move to `resolution-needed` and the workflow MUST NOT advance to the next implementation milestone or final closeout until the required review-resolution loop is closed.

R3bd. In a milestone-based plan, if the reviewed milestone, remaining in-scope implementation milestones, review status, or required review-resolution state cannot be determined from the active plan and review output, the workflow MUST stop as inconclusive or require a plan update instead of handing off to final closeout.

R3be. A lifecycle-closeout milestone MUST NOT be treated as an unfinished implementation milestone for final closeout readiness decisions. A mixed milestone that still contains implementation work remains an in-scope implementation milestone until that implementation work is closed or the plan is revised.

R3c. After successful final implementation-milestone review and required review-resolution closeout, the workflow MUST continue to `ci-maintenance` when triggered; otherwise it MUST continue to `explain-change`.

R3d. In the standard workflow execution flow, `ci-maintenance` MUST be triggered only when hosted workflow automation, validation automation, or related platform configuration must be created or changed for the change.

R3e. In the standard workflow execution flow, after successful `ci-maintenance`, the downstream stage MUST be `explain-change` unless a stop condition applies.

R3f. In the standard workflow execution flow, after successful `explain-change`, the downstream stage MUST be `verify` unless a stop condition applies.

R3g. In the standard workflow execution flow, after successful `verify`, the downstream stage MUST be `pr` unless a stop condition applies.

R5. The workflow MUST treat the following as stop conditions:
- an explicit user instruction to stop, pause, or inspect before the next stage;
- a spec gap, architecture conflict, failing validation result, or review finding that requires a real user decision;
- an explicit checkpoint or separately reviewable boundary defined by the governing spec or active plan;
- missing repository permissions, network failures, or tool limitations that prevent safe continuation;
- a next action that is destructive, irreversible, or externally publishing in a stronger sense than PR creation.

R5a. Default autoprogression MUST NOT include merge, deploy, release, tag publication, branch deletion, history rewrites, or rollback actions unless the user explicitly requests them.

R6. The `pr` stage in a workflow-managed completion flow MUST prepare and open the pull request directly when PR-opening prerequisites are satisfied.

R6a. PR-opening prerequisites MUST include:
- all required upstream stages for the current workflow state are complete;
- required validation for the change has passed;
- lifecycle closeout is truthful where required by the active plan or other authoritative lifecycle-managed artifacts;
- the correct base branch is known;
- the review branch exists or can be created safely;
- no unrelated tracked changes are included in the PR scope;
- unrelated untracked drafts remain out of scope.

R6b. If any PR-opening prerequisite is not satisfied, the `pr` stage MUST NOT open the pull request and MUST report the blocking condition explicitly.

R6c. Hosted CI MAY still be pending when the PR is opened, provided that the repository's local readiness checks have passed and the PR body does not falsely claim hosted CI already passed.

R7. Review stages in workflow-managed completion flows MUST be treated as workflow gates rather than user-confirmation gates.

R7a. The workflow MUST NOT require a redundant user confirmation merely to enter the already-known next required review stage.

R8. The workflow MUST provide an explicit user-controlled pause path without reintroducing stage-by-stage confirmation as the default.

R8a. For v1, an explicit user instruction in chat is sufficient to request a pause.

R8b. The workflow MAY later add a structured `pause-after` or `checkpoint` mechanism, but v1 MUST NOT require such a mechanism for safe operation.

R8c. Advice-only stages MUST NOT auto-run by default. They MAY run only when the user explicitly requests them or a later approved rule elevates them for the active change.

R8d. `learn` remains advice-only and MUST NOT auto-run by default under this v1 contract.

R9. Stage outputs and readiness text SHOULD reflect actual workflow progression rather than implying that the agent is merely waiting for the user to invoke an already-known next stage.

R9a. When automatic continuation stops because of a blocker or pause condition, the reported state MUST name the next blocked or paused stage and the reason continuation stopped.

R10. This feature MUST preserve the existing lifecycle stage order and enforcement model unless those artifacts are explicitly updated by a later approved change.

R10a. This feature MUST NOT remove or weaken `code-review`, `explain-change`, `verify`, `pr`, or `learn`.

## Inputs and outputs

Inputs:

- the current workflow state for the change
- the current completed stage and its outcome
- whether workflow-managed context is present
- explicit user stop or continue instructions
- current validation and review results
- branch and worktree state relevant to `pr`
- governing spec, plan, and workflow artifacts when they define checkpoints or blockers

Outputs:

- the next downstream stage entered automatically, when continuation is allowed
- a blocker or pause result when continuation stops
- for `pr`, either an opened PR URL or an explicit readiness blocker
- updated readiness wording in the relevant tracked artifacts when workflow state changes

## State and invariants

- The workflow never skips a required or enforced stage for the current workflow state.
- The workflow never applies standard execution-flow next-stage pairs to manual skill invocations, bugfix skill invocations, or review-only work by default.
- In v1, manual skill invocations and bugfix skill invocations do not gain automatic downstream continuation through this feature unless a later approved change expands the scope.
- In v1, standard workflow execution-flow autoprogression begins at `implement` and ends at `pr`.
- In a milestone-based plan, `implement` sets the current implementation milestone to `review-requested` when implementation and targeted validation are complete and review handoff occurs.
- In a milestone-based plan, `code-review` sets the reviewed milestone to `closed` when review is clean and no review-resolution is required, or to `resolution-needed` when findings require review-resolution, fixes, owner decision, or re-review.
- In a milestone-based plan, final closeout is available only after all in-scope implementation milestones are closed and no required review-resolution remains open.
- In v1, review-to-next-authoring-stage transitions remain outside the autoprogression contract.
- Review-only and explicitly isolated stage requests remain isolated unless the user asks to continue.
- Automatic continuation never expands into merge, release, deploy, or destructive Git behavior by default.
- When a stop condition applies, the workflow stops before the next stage and reports why.

## Error and boundary behavior

- If the current workflow state is ambiguous, the workflow MUST stop and ask for clarification or re-route through workflow classification rather than guessing.
- If validation fails after `implement`, the workflow MUST stop before downstream review stages and report the failing proof surface.
- If workflow-managed context is absent for a directly invoked stage, the workflow MUST treat the invocation as isolated rather than inferring automatic downstream continuation. Direct `pr` still performs the `pr` stage itself when readiness passes.
- If `code-review` findings require a design choice, scope change, or spec change rather than a straightforward fix, the workflow MUST stop and surface that decision point.
- If a milestone-based plan does not clearly show whether more in-scope implementation milestones remain, the workflow MUST stop for plan clarification or plan update instead of routing a clean review to final closeout.
- If a planned implementation milestone no longer belongs in the current change, the plan MUST be revised before downstream handoff. Milestones MUST NOT be postponed or hidden solely to make final closeout available.
- If `pr` is reached with an unknown base branch, missing review branch, or unrelated tracked changes, the workflow MUST stop and report the exact blocker.
- If network or GitHub tooling is unavailable during `pr`, the workflow MUST stop with a clear PR-creation failure instead of claiming the PR was opened.
- If unrelated untracked drafts are present, they MAY remain in the working tree, but they MUST stay out of the PR scope.

## Compatibility and migration

- This change is a workflow-behavior clarification, not a product-runtime compatibility change.
- Existing stage order remains intact; the change affects default continuation behavior between stages, not which stages exist.
- Review-only requests remain compatible because they stay isolated unless the user asks to continue.
- Existing milestone-free plans remain compatible with the ordinary standard workflow continuation sequence. Touched milestone-based plans MUST use milestone-aware handoff wording and the `explain-change -> verify -> pr` final order when current review or readiness state changes.
- Existing open PRs or feature branches are unaffected until the workflow guidance and skills are updated to use this contract.
- Rollback is straightforward: restore the prior explicit-stop-after-stage behavior in the workflow contract and affected skills.

## Observability

- The agent SHOULD announce when it is continuing automatically into the next stage.
- When continuation stops, the agent SHOULD state whether the reason is user pause, blocker, missing prerequisite, or external-tool limitation.
- `pr` output MUST make clear whether a PR was actually opened or only deemed ready.
- Workflow-managed readiness text in plans or related artifacts SHOULD identify the actual next stage rather than implying manual re-invocation is required.
- When a directly invoked stage is treated as isolated, the output SHOULD make that classification explicit instead of implying that downstream continuation was forgotten.

## Security and privacy

- Automatic continuation MUST NOT expand into destructive or externally publishing actions beyond PR creation by default.
- PR creation output MUST NOT falsely claim hosted CI passed when only local checks were observed.
- PR preparation and opening MUST continue to respect the repository rule against including secrets, credentials, or unrelated local files.

## Performance expectations

- The workflow SHOULD reduce unnecessary chat turns caused by redundant "continue?" pauses between already-known downstream stages.
- Any additional continuation logic SHOULD remain lightweight enough that it does not materially delay normal stage execution.

## Edge cases

EC1. A user asks only for `verify` on an existing change. The workflow returns the verify result and stops unless the user asks to continue.

EC2. A successful `spec` in a workflow-managed completion flow continues into `spec-review` when `spec-review` is the next mandatory or triggered downstream stage.

EC3. A standard workflow change completes `implement`. The workflow continues to `code-review`.

EC4. `code-review` finds fixable issues with no new user decision required. The workflow resolves them and reruns the review loop.

EC5. `code-review` finds issues that require a product or design decision. The workflow stops and surfaces the decision point.

EC6. `pr` is reached while unrelated tracked changes are present. The workflow does not open the PR.

EC7. `pr` is reached while unrelated untracked drafts are present but out of scope. The workflow may still open the PR if all tracked readiness checks pass.

EC8. Hosted CI has not run yet. The workflow may open the PR with CI pending, but it must not claim hosted CI passed.

EC9. The user says `stop after code-review`. The workflow honors the pause even if downstream stages would normally be automatic.

EC10. A standard workflow change closes final implementation review and required review-resolution. The workflow continues to `ci-maintenance` when triggered; otherwise it continues to `explain-change`, then `verify`, then `pr`.

EC11. A directly invoked `pr` request opens the PR when readiness passes, and then stops because no downstream stage follows `pr`.

EC12. A directly invoked `verify` request without workflow-managed context returns the verify result and stops.

EC13. A change reaches `pr` with required upstream stages incomplete or lifecycle closeout still stale. The workflow does not open the PR.

EC14. A manual skill invocation or bugfix skill invocation completes a stage. This v1 autoprogression contract does not require automatic continuation for that invocation.

EC15. A clean non-final implementation milestone review closes the reviewed milestone and routes to the next in-scope implementation milestone, not `verify`.

EC16. A clean final implementation milestone review routes to `ci-maintenance` when triggered, or otherwise `explain-change`, only when all in-scope implementation milestones are closed and no required review-resolution remains open.

EC17. A milestone review with findings moves the reviewed milestone to `resolution-needed` and keeps the workflow on that same milestone until findings are resolved, deferred with rationale, rejected, or otherwise closed under the governing review contract.

EC18. A milestone-based plan with ambiguous remaining implementation scope blocks final closeout and requires plan clarification or update.

EC19. A lifecycle-closeout milestone after closed implementation milestones does not block entry into final closeout; a mixed milestone containing implementation work remains an implementation milestone.

## Non-goals

- Auto-merging pull requests.
- Auto-deploying, auto-releasing, auto-tagging, or publishing packages.
- Changing the repository's stage order outside the autoprogression rules defined here.
- Enabling v1 autoprogression for manual skill invocation or bugfix execution flow.
- Turning manual review-only requests into implicit completion flows.
- Introducing a mandatory structured checkpoint syntax in v1.

## Acceptance criteria

- The workflow contract clearly distinguishes workflow-managed completion flows from isolated stage requests.
- The spec makes clear that v1 autoprogression applies to standard workflow execution flow and authoring-to-review handoffs, not to manual skill invocation or bugfix execution flow.
- The spec makes clear that direct `$pr` remains in scope for v1 and still opens the PR when readiness passes.
- The spec makes workflow-state-specific next-stage behavior explicit enough that standard execution and review-only flows cannot inherit the wrong stage pair by accident.
- The spec defines explicit stop conditions and explicit PR-opening prerequisites.
- The spec makes clear that advice-only stages, including `learn`, do not auto-run by default.
- The spec preserves review, verification, and PR gates while removing redundant user-confirmation pauses.
- The spec leaves merge, release, deploy, and destructive Git actions outside default autoprogression.
- The spec qualifies clean `code-review` routing so non-final milestone reviews continue to the next implementation milestone and final clean implementation milestone reviews enter final closeout only after all in-scope implementation milestones are closed.
- The spec routes final closeout through `ci-maintenance` when triggered, then `explain-change`, then `verify`, then `pr`.
- The spec keeps `ci-maintenance` scoped to automation or platform configuration changes rather than validation execution.
- The spec keeps direct `verify` isolated by default and does not auto-continue to `pr` unless workflow-managed context or explicit continuation exists.

## Open questions

- Should a future revision add a structured `pause-after` or `checkpoint` syntax, or remain chat-instruction-only?
- If the repository later adds executable workflow orchestration, should that live in repo-owned scripts or in skill guidance only?

These questions do not block the approved v1 contract.

## Next artifacts

- `code-review M2` under [Single Workflow Lane, Explain-Change Before Verify Execution Plan](../docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md) after M2 implementation handoff.
- Continue the approved milestone loop with M3 through M5 until all in-scope implementation milestones are closed.

## Follow-on artifacts

- `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`
- `proposal`: [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md)
- `spec-review`: approved in [spec-review-r5](../docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r5.md)
- `plan`: [Single Workflow Lane, Explain-Change Before Verify Execution Plan](../docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md)
- `plan-review`: approved in [plan-review-r2](../docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/plan-review-r2.md)
- `test-spec`: [Workflow stage autoprogression test spec](workflow-stage-autoprogression.test.md) confirms the active autoprogression proof map.

## Readiness

- Approved amendment for the single standard workflow and `explain-change -> verify -> pr` final order.
- Architecture design remains tracked in `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`.
- The active execution plan may rely on this approved spec for M2 implementation and review handoff.
