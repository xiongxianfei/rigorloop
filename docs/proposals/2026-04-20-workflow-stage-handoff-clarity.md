# Workflow Stage Handoff Clarity

## Status
- abandoned

## Problem

The repository already defines a lifecycle order for non-trivial work, but the handoff language between review stages and subsequent stages is still too implicit.

In practice, the repository workflow says non-trivial work proceeds through `spec -> spec-review -> architecture when needed -> plan -> plan-review -> test-spec`, but a recent `spec-review` response incorrectly said the change was ready for `test-spec` directly. That happened because the repo's workflow order is clear in `docs/workflows.md` and `AGENTS.md`, while the `spec-review` skill still frames its closing readiness statement around `architecture` and `test-spec` rather than the next workflow stage in this repository.

The result is not a code bug. It is workflow-governance ambiguity: a reviewer can describe a spec as mature enough for test planning in the abstract while still skipping the repository's required `plan -> plan-review` sequence.

## Goals

- Make stage handoff expectations explicit after review stages.
- Prevent agents from recommending a downstream stage that skips required intermediate stages.
- Keep repository-specific workflow order authoritative over generic skill wording.
- Preserve the current lifecycle order, including conditional `architecture`, without redesigning the workflow.
- Make the correct next stage easy to state in review outputs without requiring maintainers to infer it from multiple artifacts.

## Non-goals

- Redesign the repository lifecycle order.
- Remove the optional `architecture` stage where it is still useful.
- Introduce automation that tries to infer lifecycle state from chat history alone.
- Rewrite every skill when only a small set of review-stage handoffs needs clarification.
- Change the meaning of `test-spec`; this proposal only changes when it is the correct next step.

## Context

- `docs/workflows.md` already documents the full lifecycle as `spec -> spec-review -> architecture -> plan -> plan-review -> test-spec -> implement ...`, with `architecture` conditional when needed.
- `AGENTS.md` already says execution usually proceeds through `plan -> plan-review -> test-spec` once proposal, spec, and architecture are settled.
- The current repo problem is not missing order; it is missing handoff guidance.
- The generic `spec-review` skill asks for an explicit readiness statement for `architecture` and `test-spec`, which is broad enough to be misread as permission to skip planning in this repository.
- This ambiguity is most visible in `spec-review`, but the same class of problem can recur anywhere a review-stage closeout names a later stage without anchoring to the repository's actual workflow order.

## Options considered

### Option 1. Do nothing and rely on contributors to remember the order

Keep the current workflow docs and treat incorrect stage recommendations as one-off execution mistakes.

- Pros:
  - no workflow artifact changes
  - no skill updates needed
- Cons:
  - the repository already produced a wrong next-stage recommendation
  - contributors still have to reconcile generic skill wording with repo-specific workflow order
  - the same mistake can repeat in later review stages

### Option 2. Patch only the `spec-review` skill wording

Update the `spec-review` skill so its readiness statement points to `plan` instead of `test-spec` for this repository.

- Pros:
  - directly addresses the observed failure
  - small change surface
- Cons:
  - treats one symptom instead of the broader handoff rule
  - leaves similar ambiguity possible in other review stages
  - keeps the repository workflow contract itself implicit about how review outputs should announce the next stage

### Option 3. Define a repository-level stage-handoff rule and align review skills to it

Add an explicit workflow rule that review-stage outputs should declare readiness for the next repository stage or next allowed branch in the workflow order, not for a downstream stage that skips required intermediate steps. Then align the affected review skills and workflow guidance to that rule.

- Pros:
  - fixes the actual governance gap rather than a single phrasing bug
  - keeps repo workflow order authoritative over generic skill defaults
  - scales to `proposal-review`, `spec-review`, `architecture-review`, and `plan-review`
  - gives later spec, test-spec, and implementation work a clearer contract
- Cons:
  - touches both workflow docs and skill guidance
  - requires choosing how broad the initial alignment should be

### Option 4. Add automation or linting for invalid stage recommendations

Introduce validation or CI checks that try to detect when a review artifact recommends the wrong next stage.

- Pros:
  - stronger long-term enforcement
  - can catch drift after docs are updated
- Cons:
  - overbuilt for the current problem
  - hard to validate chat and narrative artifacts reliably
  - adds automation before the workflow rule itself is fully explicit

## Recommended direction

Choose Option 3.

The repository should define a simple stage-handoff rule: when a review stage closes, it should state readiness for the next repository stage or the next allowed branch in the documented workflow order, not for an abstract later stage that would skip required intermediate work.

Applied to the current failure:

- after `spec-review`, the correct next step is `architecture` when needed, otherwise `plan`
- after `architecture-review`, the correct next step is `plan`
- after `plan-review`, the correct next step is `test-spec`

This change should live in the repository workflow contract and contributor-facing workflow summary, then be reflected in the relevant review skills so their output shape reinforces the repository order instead of competing with it.

This is the smallest durable fix because it preserves the current lifecycle, avoids over-automation, and addresses the actual ambiguity that caused the wrong recommendation.

## Expected behavior changes

- Review outputs will stop declaring readiness for stages that skip required intermediate workflow steps.
- `spec-review` outputs in this repository will say a reviewed spec is ready for `architecture` when needed, otherwise `plan`, instead of jumping directly to `test-spec`.
- `plan-review` outputs will remain the point where `test-spec` becomes the correct next stage.
- Contributors will have a clearer rule for interpreting review-stage closeouts without needing to reconcile conflicting generic skill language.

## Architecture impact

This is a workflow/governance change, not a runtime architecture change.

Likely affected artifact types:

- the workflow contract in `specs/`
- the workflow summary in `docs/workflows.md`
- possibly `AGENTS.md` if it should reinforce the handoff rule
- canonical skill guidance for review stages under `skills/`
- regenerated `.codex/skills/` output if canonical review skills change

No product behavior, runtime data flow, or storage boundary is expected to change.

## Testing and verification strategy

Likely proof surfaces:

- manual review that the workflow contract and workflow summary define stage handoff explicitly
- test-spec coverage for:
  - `spec-review` handing off to `architecture` when needed, otherwise `plan`
  - `plan-review` handing off to `test-spec`
  - repository-specific workflow order overriding more generic skill wording when they differ
- review of the affected canonical skills to confirm their closeout language matches the repository rule
- regenerated `.codex/skills/` sync check if canonical skill files are updated

## Rollout and rollback

Rollout:

- add the repository-level handoff rule to the workflow contract
- update contributor-facing workflow guidance to summarize it
- align the affected canonical review skills to that rule
- regenerate `.codex/skills/` if canonical skills change

Rollback:

- revert the new handoff wording if it proves confusing
- preserve any truthful corrections to workflow examples or skill wording that remove obviously wrong stage jumps

## Risks and mitigations

- Risk: the change becomes a broad rewrite of all skill outputs.
  - Mitigation: start with the review stages that can actually skip required intermediate steps.
- Risk: contributors interpret the handoff rule as forcing `architecture` for every reviewed spec.
  - Mitigation: state explicitly that `architecture` remains conditional and that `plan` is the default next step once architecture is settled or not needed.
- Risk: repo workflow docs and skill guidance diverge again later.
  - Mitigation: make the repository workflow contract the authority and treat skill wording as a derived operating surface.
- Risk: maintainers try to solve the issue with automation before the rule is stable.
  - Mitigation: defer automation and keep this change documentation-first.

## Open questions

- Should the first change align only `spec-review` and `plan-review`, or should it also update `proposal-review` and `architecture-review` in the same pass?
- Should `AGENTS.md` restate the handoff rule explicitly, or is `specs/` plus `docs/workflows.md` enough?

## Decision log

- 2026-04-20: Rejected doing nothing. Reason: the repository already produced a wrong next-stage recommendation in normal use.
- 2026-04-20: Rejected a `bugfix` framing as the primary response. Reason: the underlying issue is workflow-governance ambiguity, not a code defect.
- 2026-04-20: Rejected a skill-only patch as the preferred direction. Reason: the repository needs a governing handoff rule, not just one corrected skill.
- 2026-04-20: Chose repository-level handoff clarification with aligned skill guidance as the leading direction. Reason: it fixes the durable source of ambiguity with minimal scope.

## Next artifacts

- spec
- test-spec
- plan

## Follow-on artifacts

- [Workflow Stage Autoprogression](2026-04-21-workflow-stage-autoprogression.md): partially addressed the broader workflow-routing pain by defining bounded autoprogression for workflow-managed execution and authoring-to-review handoffs.
- Remaining review-handoff wording ambiguity for isolated review outputs is deferred. If the same problem recurs, create a new proposal that references this artifact instead of reactivating it in place.

## Readiness

This proposal is abandoned.

Its main pain was partly addressed by [Workflow Stage Autoprogression](2026-04-21-workflow-stage-autoprogression.md).

No further `proposal-review` action is pending for this artifact.

If the same review-handoff wording problem recurs, open a new proposal that references this artifact rather than reactivating it in place.
