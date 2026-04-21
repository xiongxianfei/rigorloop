# Workflow Stage Autoprogression

## Status
- approved

## Related proposal

- [Workflow stage autoprogression](../docs/proposals/2026-04-21-workflow-stage-autoprogression.md)

## Goal and context

This spec defines when the repository workflow should continue automatically to the next downstream stage and when it should stop and wait instead.

The existing workflow contract already defines stage order and stage classification, but it does not define a general continuation rule. That leaves agents pausing after already-complete stages even when the next stage is already known, required by the active lane, and does not need a new user decision. This spec closes that gap without broadening into merge, deploy, release, or destructive Git automation.

In v1, this autoprogression contract applies only to:

- full-feature execution flow handoffs; and
- authoring-to-review handoffs for `proposal`, `spec`, and `architecture` when those review stages are the next required or default downstream step.

Fast-lane and bugfix execution flows remain out of scope for this automation mechanism in v1.

## Glossary

- `workflow-managed completion flow`: a change flow where the agent is carrying work through its normal downstream stages toward completion under the active lane.
- `workflow-managed context`: downstream-continuation context carried from the prior stage or requested explicitly by the user as end-to-end completion, rather than inferred from a direct one-stage invocation alone.
- `isolated stage request`: a user request for the output of one stage only, such as standalone `proposal-review`, `spec-review`, `code-review`, `verify`, or `explain-change`.
- `current lane`: the active workflow path for the change, such as full-feature, fast-lane, bugfix, or review-only.
- `downstream stage`: the next stage or stages that follow from the current lane and the current stage outcome.
- `stop condition`: a documented reason the agent must not continue automatically.
- `PR-opening prerequisites`: the minimum branch, worktree, and readiness conditions required before the `pr` stage opens a pull request.

## Examples first

### Example E1: full-feature implementation continues into review

Given a non-trivial full-feature change has completed `implement`
When milestone validation passes and no stop condition applies
Then the agent continues into `code-review` without waiting for the user to invoke it manually.

### Example E2: authoring work continues into the matching review gate

Given a change is in a workflow-managed completion flow and `spec` completes successfully
When `spec-review` is the next required or default downstream stage
Then the agent continues into `spec-review` without waiting for a redundant user confirmation.

### Example E3: review-only request stops after the requested stage

Given the user asks only for `code-review`
When the review result is returned
Then the agent does not continue into `verify` or `pr` unless the user asks to continue.

### Example E4: code-review findings enter the review-resolution loop

Given a full-feature change in a workflow-managed completion flow reaches `code-review`
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

### Example E10: fast-lane and bugfix flows remain outside v1 autoprogression

Given a change is in the fast lane or bugfix lane
When one stage completes
Then this v1 autoprogression contract does not itself require automatic continuation into the next stage for that lane.

## Requirements

R1. The workflow MUST distinguish workflow-managed completion flows from isolated stage requests.

R1a. A request that asks only for critique, readiness, audit, or explanation from a single review-oriented stage MUST be treated as an isolated stage request unless the user also asks to continue beyond that stage.

R1b. Isolated stage requests MUST NOT trigger automatic continuation into downstream stages unless the user explicitly asks to continue.

R1c. Direct user invocation of a single review-oriented, verification, or explanation stage MUST be treated as isolated by default unless workflow-managed context is carried from a prior stage or the user explicitly asks for end-to-end continuation.

R1d. Direct user invocation of `pr` remains in scope for v1. Isolation prevents downstream continuation beyond `pr`, but it MUST NOT downgrade the `pr` stage's own normal behavior of opening the pull request when readiness passes.

R2. In a workflow-managed completion flow, when a stage completes successfully, the agent MUST continue to the next required or default downstream stage for the current lane unless continuation is explicitly waived, blocked, or paused.

R2a. Autoprogression MUST follow the current lane's next required or default downstream stage, not a universal stage pair.

R2b. In v1, this autoprogression contract applies only to full-feature execution flow and authoring-to-review handoffs. It MUST NOT change fast-lane or bugfix downstream behavior by implication.

R2ba. In v1, full-feature execution-flow autoprogression begins at `implement` and continues through `pr`.

R2c. When the current lane or active workflow classification includes `proposal-review` as the next required or default downstream stage, successful `proposal` completion MUST continue into `proposal-review` unless a stop condition applies.

R2d. When the current lane or active workflow classification includes `spec-review` as the next required or default downstream stage, successful `spec` completion MUST continue into `spec-review` unless a stop condition applies.

R2e. When the current lane or active workflow classification includes `architecture-review` as the next required or default downstream stage, successful `architecture` completion MUST continue into `architecture-review` unless a stop condition applies.

R2f. Upstream of `implement`, v1 covers only these authoring-to-review handoffs:
- `proposal -> proposal-review`
- `spec -> spec-review`
- `architecture -> architecture-review`

R2g. Review-to-next-authoring-stage transitions such as `proposal-review -> spec`, `spec-review -> architecture`, or `architecture-review -> plan` remain out of scope unless a later approved change adds them.

R3. In the full-feature lane, successful `implement` completion MUST continue into `code-review` unless a stop condition applies.

R3a. In the full-feature lane, if `code-review` finds issues that can be resolved without a new user decision, the workflow MUST enter the `review-resolution` loop and rerun `code-review` before proceeding.

R3b. In the full-feature lane, once `code-review` is satisfied and no accepted findings remain unresolved, the workflow MUST continue into `verify` unless a stop condition applies.

R3c. After successful `verify`, the workflow MUST continue into the next required or default downstream stage for the current lane unless a stop condition applies.

R3d. In the full-feature lane, if the governing workflow contract elevates `ci` for the change, the downstream stage after successful `verify` MUST be `ci`; otherwise the downstream stage MUST be `explain-change`.

R3e. In the full-feature lane, after successful `ci`, the downstream stage MUST be `explain-change` unless a stop condition applies.

R3f. In the full-feature lane, after successful `explain-change`, the downstream stage MUST be `pr` unless a stop condition applies.

R5. The workflow MUST treat the following as stop conditions:
- an explicit user instruction to stop, pause, or inspect before the next stage;
- a spec gap, architecture conflict, failing validation result, or review finding that requires a real user decision;
- an explicit checkpoint or separately reviewable boundary defined by the governing spec or active plan;
- missing repository permissions, network failures, or tool limitations that prevent safe continuation;
- a next action that is destructive, irreversible, or externally publishing in a stronger sense than PR creation.

R5a. Default autoprogression MUST NOT include merge, deploy, release, tag publication, branch deletion, history rewrites, or rollback actions unless the user explicitly requests them.

R6. The `pr` stage in a workflow-managed completion flow MUST prepare and open the pull request directly when PR-opening prerequisites are satisfied.

R6a. PR-opening prerequisites MUST include:
- all required upstream stages for the current lane are complete;
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

R10. This feature MUST preserve the existing lifecycle stage order, enforcement model, and lane definitions unless those artifacts are explicitly updated by a later approved change.

R10a. This feature MUST NOT remove or weaken `code-review`, `verify`, `explain-change`, `pr`, or `learn`.

## Inputs and outputs

Inputs:

- the current lane for the change
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

- The workflow never skips a required or enforced stage for the active lane.
- The workflow never applies a full-feature next-stage pair to fast-lane, bugfix, or review-only work by default.
- In v1, fast-lane and bugfix work do not gain automatic downstream continuation through this feature unless a later approved change expands the scope.
- In v1, full-feature execution-flow autoprogression begins at `implement` and ends at `pr`.
- In v1, review-to-next-authoring-stage transitions remain outside the autoprogression contract.
- Review-only and explicitly isolated stage requests remain isolated unless the user asks to continue.
- Automatic continuation never expands into merge, release, deploy, or destructive Git behavior by default.
- When a stop condition applies, the workflow stops before the next stage and reports why.

## Error and boundary behavior

- If the active lane is ambiguous, the workflow MUST stop and ask for clarification or re-route through workflow classification rather than guessing.
- If validation fails after `implement`, the workflow MUST stop before downstream review stages and report the failing proof surface.
- If workflow-managed context is absent for a directly invoked stage, the workflow MUST treat the invocation as isolated rather than inferring automatic downstream continuation. Direct `pr` still performs the `pr` stage itself when readiness passes.
- If `code-review` findings require a design choice, scope change, or spec change rather than a straightforward fix, the workflow MUST stop and surface that decision point.
- If `pr` is reached with an unknown base branch, missing review branch, or unrelated tracked changes, the workflow MUST stop and report the exact blocker.
- If network or GitHub tooling is unavailable during `pr`, the workflow MUST stop with a clear PR-creation failure instead of claiming the PR was opened.
- If unrelated untracked drafts are present, they MAY remain in the working tree, but they MUST stay out of the PR scope.

## Compatibility and migration

- This change is a workflow-behavior clarification, not a product-runtime compatibility change.
- Existing stage order remains intact; the change affects default continuation behavior between stages, not which stages exist.
- Review-only requests remain compatible because they stay isolated unless the user asks to continue.
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

EC2. A successful `spec` in a workflow-managed completion flow continues into `spec-review` when `spec-review` is the next required or default downstream stage.

EC3. A full-feature change completes `implement`. The workflow continues to `code-review`.

EC4. `code-review` finds fixable issues with no new user decision required. The workflow resolves them and reruns the review loop.

EC5. `code-review` finds issues that require a product or design decision. The workflow stops and surfaces the decision point.

EC6. `pr` is reached while unrelated tracked changes are present. The workflow does not open the PR.

EC7. `pr` is reached while unrelated untracked drafts are present but out of scope. The workflow may still open the PR if all tracked readiness checks pass.

EC8. Hosted CI has not run yet. The workflow may open the PR with CI pending, but it must not claim hosted CI passed.

EC9. The user says `stop after code-review`. The workflow honors the pause even if downstream stages would normally be automatic.

EC10. A full-feature change completes `verify`. The workflow continues to `ci` when its trigger applies; otherwise it continues to `explain-change`, and then to `pr`.

EC11. A directly invoked `pr` request opens the PR when readiness passes, and then stops because no downstream stage follows `pr`.

EC12. A directly invoked `verify` request without workflow-managed context returns the verify result and stops.

EC13. A change reaches `pr` with required upstream stages incomplete or lifecycle closeout still stale. The workflow does not open the PR.

EC14. A fast-lane or bugfix change completes a stage. This v1 autoprogression contract does not require automatic continuation for that lane.

## Non-goals

- Auto-merging pull requests.
- Auto-deploying, auto-releasing, auto-tagging, or publishing packages.
- Changing the repository's stage order outside the autoprogression rules defined here.
- Enabling v1 autoprogression for fast-lane or bugfix execution flow.
- Turning review-only lane requests into implicit completion flows.
- Introducing a mandatory structured checkpoint syntax in v1.

## Acceptance criteria

- The workflow contract clearly distinguishes workflow-managed completion flows from isolated stage requests.
- The spec makes clear that v1 autoprogression applies to full-feature execution flow and authoring-to-review handoffs, not to fast-lane or bugfix execution flow.
- The spec makes clear that direct `$pr` remains in scope for v1 and still opens the PR when readiness passes.
- The spec makes lane-specific next-stage behavior explicit enough that full-feature and review-only flows cannot inherit the wrong stage pair by accident.
- The spec defines explicit stop conditions and explicit PR-opening prerequisites.
- The spec makes clear that advice-only stages, including `learn`, do not auto-run by default.
- The spec preserves review, verification, and PR gates while removing redundant user-confirmation pauses.
- The spec leaves merge, release, deploy, and destructive Git actions outside default autoprogression.

## Open questions

- Should a future revision add a structured `pause-after` or `checkpoint` syntax, or remain chat-instruction-only?
- If the repository later adds executable workflow orchestration, should that live in repo-owned scripts or in skill guidance only?

These questions do not block spec review for the v1 contract.

## Next artifacts

- `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`
- `architecture-review`
- `specs/workflow-stage-autoprogression.test.md`
- update `specs/rigorloop-workflow.md` and matching workflow/skill guidance
- `docs/plans/YYYY-MM-DD-workflow-stage-autoprogression.md` if implementation requires multiple milestones

## Follow-on artifacts

- `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`

## Readiness

- This spec is approved.
- Architecture design is tracked in `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`.
- No further `spec-review` action is pending.
