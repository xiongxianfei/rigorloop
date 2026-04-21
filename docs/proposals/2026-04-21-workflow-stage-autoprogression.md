# Workflow Stage Autoprogression

## Status
- accepted

## Problem

The repository's workflow contract defines which stages are required, but it does not clearly define when the agent should continue automatically versus stop and wait for the user to invoke the next obvious stage.

That gap creates avoidable pauses between stages even when:

- the next stage is already required by the workflow;
- no new user decision is needed;
- no blocker or spec gap exists; and
- the next action is a normal review handoff rather than a destructive operation.

Two recurring examples are already visible:

1. after `implement`, the agent waits for the user to trigger `code-review` even though `code-review` is the necessary next gate for non-trivial work;
2. after `pr`, the agent may stop after drafting PR material instead of opening the PR directly, even though the user can review the resulting PR on GitHub and PR creation is the whole purpose of that stage.

The result is workflow friction rather than better review. The user is forced to act as a stage router for steps the repository already knows are mandatory, which adds latency, chat noise, and avoidable opportunities for partial or stale handoff state.

## Goals

- Remove unnecessary user-confirmation pauses between mandatory or default downstream stages.
- Make stage continuation rules explicit and deterministic.
- Preserve human control where a real decision, destructive action, or external risk exists.
- Keep review, verification, and traceability gates intact rather than bypassing them.
- Reduce chat churn caused by redundant "continue?" prompts.

## Non-goals

- Auto-merging pull requests.
- Auto-deploying, auto-releasing, auto-tagging, or publishing packages.
- Removing `code-review`, `verify`, `explain-change`, or `pr` as stages.
- Forcing end-to-end autonomy when the user explicitly asks for a checkpoint or pause.
- Replacing explicit user intent for destructive Git actions such as branch deletion, history rewrites, or rollback commands.
- Automatically continuing review-only or explicitly isolated stage requests such as standalone `proposal-review`, `spec-review`, `code-review`, `verify`, or `explain-change` when the user did not ask to continue beyond that stage.

## Context

- `specs/rigorloop-workflow.md` already defines stage classifications (`advice`, `default`, `enforced`) and the full lifecycle order.
- `implement`, `verify`, and `pr` are already enforced for non-trivial work, and `code-review` is the normal next gate after implementation.
- The workflow contract already distinguishes routine CI validation from the `ci` stage and already allows verify-time lifecycle closeout before PR when the outcome is known on-branch.
- The repository now relies on durable artifacts, plan state, and verification evidence to determine readiness. That means waiting for a user to manually invoke an already-required next stage does not add truth; it just delays execution.
- PR creation is reviewable and reversible in a way merge, deploy, and release are not. The real publication and branch-protection gate is merge, not the mere existence of a PR.
- Recent work on plan and artifact lifecycle ownership showed the agent can keep lifecycle bookkeeping truthful across multiple downstream stages without requiring user re-confirmation at each step.

## Options considered

### Option 1. Keep explicit user-driven handoff between every stage

Require the user to trigger each stage manually, even when the next step is already known.

- Pros:
  - maximum visible user control
  - minimal workflow-rule change
- Cons:
  - keeps the user acting as a manual router for predictable transitions
  - creates redundant chat prompts
  - increases latency without improving correctness
  - makes partial stage completion more likely

### Option 2. Patch only the two identified cases

Special-case `implement -> code-review` and `pr -> open PR`, but leave the rest of the workflow undefined.

- Pros:
  - small immediate change
  - addresses the current pain quickly
- Cons:
  - solves symptoms, not the policy gap
  - leaves future stage handoffs inconsistent
  - creates a growing list of ad hoc exceptions

### Option 3. Add a general autoprogression policy with explicit stop conditions

Define that the agent continues automatically into the next required or default downstream stage when prerequisites are satisfied, unless a documented stop condition applies. In v1, apply that policy only to full-feature execution flow and authoring-to-review handoffs, not to fast-lane or bugfix execution flow.

- Pros:
  - solves the general routing problem instead of only two cases
  - keeps review and verification gates intact
  - makes pause behavior predictable
  - reduces unnecessary chat traffic while preserving safety
- Cons:
  - requires tightening workflow language across the workflow spec and stage skills
  - needs careful stop-condition wording so automation does not become surprising

### Option 4. Make the workflow fully autonomous through merge or release

Continue automatically through all stages, including merge, release, or other external publication actions.

- Pros:
  - minimal human intervention
  - fastest possible path from implementation to published result
- Cons:
  - too aggressive for a public project workflow
  - collapses meaningful human review and release intent boundaries
  - increases risk from mistaken or premature external actions

## Recommended direction

Choose Option 3.

The repository should adopt a general workflow autoprogression policy:

1. When a stage completes successfully, the agent should continue to the next required or default downstream stage unless explicitly waived, blocked, or paused.
2. Review stages are workflow gates, not user-confirmation gates. The user should not need to manually re-invoke a known mandatory next review step.
3. The agent should stop only when a documented stop condition applies.

The core best practice is to separate:

- **required workflow progression**
  - what the repository says must happen next; from
- **explicit user checkpoints**
  - where the user wants to inspect, redirect, or approve before a further step runs.

Applicability:

- autoprogression applies to workflow-managed completion flows where the agent is carrying a change through its normal downstream stages;
- it does not apply to review-only or explicitly isolated stage requests unless the user asks to continue beyond that stage.
- in v1, autoprogression follows the current lane's next required or default downstream stage only for full-feature execution flow and authoring-to-review handoffs. Fast-lane and bugfix execution flow stay on the repository's existing explicit-step behavior unless a later approved change broadens the scope.

The repository should treat the following as normal autoprogression examples:

- `implement -> code-review`
- `proposal -> proposal-review`
- `spec -> spec-review`
- `architecture -> architecture-review` when that review stage is the next required or default downstream step
- `code-review -> review-resolution` when findings exist
- `review-resolution -> code-review` rerun when fixes were made
- `code-review -> verify` once the implementation is approved
- `verify -> explain-change` for non-trivial work
- `explain-change -> pr`
- `pr -> open PR` when readiness checks pass

The repository should treat the following as outside v1 autoprogression scope:

- fast-lane execution handoffs such as `implement -> verify`
- bugfix-lane execution handoffs such as `verify blast radius -> explain-change -> pr`

The repository should treat the following as stop conditions:

- the user explicitly asks to stop, pause, or inspect before the next stage;
- a spec gap, architecture conflict, failing validation, or review finding requires a real user decision;
- the next action is destructive, irreversible, or externally publishing in a stronger sense than PR creation, such as merge, deploy, release, tag publication, or branch deletion;
- repository permissions, network failures, or tool limitations prevent safe continuation;
- the active plan or spec explicitly defines a human checkpoint or separately reviewable boundary that should not be crossed automatically.

Under this model:

- `pr` should mean "prepare and submit the pull request when ready," not merely "draft PR text and wait for confirmation";
- `implement` should mean "complete the milestone implementation and proceed into the next required review gate," not "stop after coding and wait for the user to ask for code review";
- `learn` should remain advice-oriented rather than automatic by default, because durable lessons often depend on merge results, review feedback, or whether a real lesson actually emerged.
- fast-lane and bugfix lanes should remain on the existing explicit-step model in v1 so this change stays small and focused on the high-friction full-feature path.

Automatic PR creation is allowed only when:

- the correct base branch is known;
- the review branch already exists or can be created safely;
- no unrelated tracked changes are included;
- unrelated untracked drafts remain out of scope;
- the normal PR readiness checks have already passed.

To preserve user control without reintroducing default pauses, the workflow should also allow an explicit pause mechanism such as:

- a direct user instruction in chat, for example "stop after code-review";
- or a documented `pause-after` / `checkpoint` convention if the spec later wants one.

## Expected behavior changes

- After `implement` completes a milestone and records its validation evidence, the agent continues directly into `code-review` instead of waiting for another user prompt.
- If `code-review` finds clearly actionable issues, the agent resolves them and reruns the review loop until the implementation is approved or a real blocker is reached.
- After `verify` succeeds for non-trivial work, the agent continues into `explain-change` and then `pr` unless a stop condition applies.
- When the `pr` stage is reached and readiness checks pass, the agent opens the PR directly instead of only drafting PR material.
- Workflow outputs and plan readiness text become more truthful because "next expected stage" reflects actual workflow progression rather than "waiting for the user to type the next skill."

## Architecture impact

- Primary impact is on workflow policy and stage-skill behavior, not on product runtime code.
- Expected touched surfaces:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - canonical `workflow`, `implement`, `code-review`, `verify`, `explain-change`, `pr`, and possibly `learn` skills
  - generated `.codex/skills/` output after canonical skill regeneration
- A separate architecture artifact may not be necessary if the resulting change remains a documentation-and-skill behavior update. If the repository wants executable workflow orchestration logic beyond skill guidance, architecture may become necessary at spec time.

## Testing and verification strategy

- Use a feature spec to define the normative autoprogression and stop-condition rules.
- Add a test spec that maps stage-transition rules, pause conditions, and external-action boundaries to concrete proof surfaces.
- Validate the resulting workflow change with:
  - targeted doc/skill consistency checks;
  - manual scenario review for key flows such as `implement -> code-review` and `verify -> explain-change -> pr`;
  - executable tests or fixtures if the repository later adds a workflow router or stage-transition validator.
- Verify that PR creation is automatic only when readiness checks pass, and that merge/release/deploy actions remain explicitly gated.

## Rollout and rollback

- Roll out as a workflow contract change first, then align the affected stage skills and operational summary.
- If implementation remains guidance-only, adoption is immediate once the workflow spec and skills agree.
- If the repository later adds executable orchestration, that can follow as a separate change once the policy is stable.
- Rollback is straightforward: restore the prior explicit-pause behavior in the workflow spec and skills if autoprogression proves too surprising or too broad.

## Risks and mitigations

- Risk: autoprogression feels surprising or too aggressive.
  - Mitigation: define stop conditions explicitly and preserve user-requested checkpoints.
- Risk: the agent opens a PR when the user expected a dry run.
  - Mitigation: define `pr` as a submit stage by default and provide an explicit pause or dry-run path for exceptions.
- Risk: automatic review-resolution loops hide meaningful design disagreements.
  - Mitigation: require the agent to stop when findings require user choice, not just implementation fixes.
- Risk: the change broadens into merge or release automation by implication.
  - Mitigation: explicitly exclude merge, deploy, release, and destructive Git actions from default autoprogression.
- Risk: plan and readiness surfaces become confusing during transition.
  - Mitigation: update plan and workflow wording so "next expected stage" means actual next workflow step, not implicit user confirmation.

## Open questions

- Should the spec define a formal `pause-after` / `checkpoint` mechanism, or is explicit user instruction in chat enough?
- Should `review-resolution` be documented as an automatic internal loop after `code-review`, or only as a stage that may be entered automatically when findings exist?
- Should `learn` remain advice-only after PR creation, or should large or surprising changes auto-run `learn` after the PR is opened?

None of these questions block writing the spec.

## Decision log

- 2026-04-21: rejected stage-by-stage user confirmation as the default model. Reason: it makes the user a manual workflow router for already-known mandatory transitions.
- 2026-04-21: rejected a two-case patch limited to `implement -> code-review` and `pr -> open PR`. Reason: the underlying problem is the lack of a general continuation policy.
- 2026-04-21: selected explicit autoprogression with stop conditions. Reason: it preserves review and safety gates while removing unnecessary pauses.
- 2026-04-21: rejected full autonomy through merge or release. Reason: PR creation is a normal review handoff, but merge, deploy, and release remain materially different external actions.

## Next artifacts

- `specs/workflow-stage-autoprogression.md`
- update `specs/rigorloop-workflow.md` if the repository prefers to keep this inside the main workflow contract instead of a separate feature spec
- conditional architecture artifact only if implementation grows beyond docs-and-skill behavior
- `docs/plans/YYYY-MM-DD-workflow-stage-autoprogression.md` if implementation requires multiple milestones
- `specs/workflow-stage-autoprogression.test.md`

## Follow-on artifacts

- `specs/workflow-stage-autoprogression.md`
- `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`

## Readiness

- This proposal is accepted.
- Spec work is now tracked in `specs/workflow-stage-autoprogression.md`.
- No further `proposal-review` action is pending.
