# Test-Spec Readiness And Skill Workflow Alignment

## Status

- accepted

## Problem

After `spec-review`, the repository needs two different answers:

- what the next repository stage is; and
- whether the reviewed spec is mature enough for eventual `test-spec` authoring.

Today those two ideas are easy to blur together. The workflow order already says non-trivial work normally proceeds through `architecture` when needed, then `plan`, then `plan-review`, then `test-spec`. But the `spec-review` surface still talks about `architecture` and `test-spec` readiness in the same closing shape, while the `test-spec` skill itself depends on an approved spec, spec-review findings, and a concrete plan.

That creates two recurring risks:

- a review output can imply that `test-spec` is the next stage even when required intermediate stages still exist;
- a spec can move forward without anyone clearly stating whether it is precise and testable enough for later proof planning.

More broadly, workflow-facing skills can drift from the approved workflow when stage order, readiness wording, and artifact lifecycle expectations are repeated in multiple places without a clear conformance rule.

## Goals

- Explain why `spec-review` should assess `test-spec` readiness even when `test-spec` is not the immediate next stage.
- Separate next-stage handoff from eventual downstream-artifact readiness.
- Prevent skill outputs from skipping required intermediate stages in repository workflow language.
- Define best practices for keeping workflow-facing skills aligned with the approved workflow contract.
- Keep the current lifecycle order, isolation rules, and artifact model intact.

## Non-goals

- Redesigning the repository stage order.
- Adding review-to-next-authoring autoprogression beyond what the current approved workflow already allows.
- Requiring a separate new orchestration subsystem, persistent workflow state, or second readiness registry.
- Adding a human review requirement for every stage transition.
- Rewriting every domain skill in the repository when the primary issue is workflow-facing skill alignment.

## Context

- `specs/rigorloop-workflow.md` defines the normal full lifecycle as `... -> spec -> spec-review -> architecture -> architecture-review when needed -> plan -> plan-review -> test-spec -> implement ...`.
- `skills/spec-review/SKILL.md` currently asks for an explicit readiness statement for `architecture`, `test-spec`, isolated stop, or blocker state.
- `skills/test-spec/SKILL.md` already assumes stronger prerequisites: an approved feature spec, spec-review findings, and a concrete execution plan.
- `skills/plan-review/SKILL.md` already treats `test-spec` as the next readiness target after plan review, which means the repository implicitly uses `plan-review` as the actual handoff into proof authoring.
- The abandoned proposal [Workflow Stage Handoff Clarity](2026-04-20-workflow-stage-handoff-clarity.md) identified the earlier version of this same problem: generic review wording can accidentally skip required intermediate stages.
- The approved workflow-stage-autoprogression change kept review-to-next-authoring transitions isolated. That solved routing scope, but it did not fully settle how review outputs should talk about downstream readiness versus immediate next-stage readiness.
- The repository already treats lifecycle wording as part of the contract. Past workflow work showed that stale or ambiguous readiness text in active artifacts causes review churn and validator findings even when the underlying implementation is correct.
- The repository needs both a focused follow-up spec and the durable workflow spec for different roles:
  - the focused follow-up spec should define the reviewable feature contract clearly for this change;
  - the final normative workflow invariant should live in `specs/rigorloop-workflow.md`, because this is a workflow-order and stage-handoff rule.

## Options considered

### Option 1: Do nothing and rely on contributors to infer the distinction

- Advantages:
  - no new artifact or wording changes
  - keeps current skill surfaces untouched
- Disadvantages:
  - the same ambiguity has already appeared in prior workflow work
  - contributors still have to infer whether "ready for test-spec" means "next stage is test-spec" or only "the spec is testable enough for later proof design"
  - skill drift remains a review-time surprise instead of a governed rule

### Option 2: Remove `test-spec` readiness from `spec-review` entirely

- Advantages:
  - makes `spec-review` talk only about the immediate next stage
  - reduces the chance of stage-skipping language
- Disadvantages:
  - loses an important quality signal about whether the approved spec is actually ready for proof planning
  - pushes testability problems later into `plan-review` or `test-spec`, where rework is more expensive
  - does not solve the broader skill-conformance problem

### Option 3: Separate next-stage handoff from eventual `test-spec` readiness and align workflow-facing skills to that rule

- Advantages:
  - preserves the current workflow order
  - keeps `spec-review` responsible for judging whether the spec is testable enough for downstream proof design
  - prevents review outputs from implying that `test-spec` skips required intermediate stages
  - gives workflow-facing skills one shared rule for readiness wording
  - fits the existing source-of-truth model without inventing a new router
- Disadvantages:
  - requires careful wording updates across workflow guidance and multiple skills
  - adds one more distinction contributors must learn: next-stage readiness versus downstream-artifact readiness

### Option 4: Add automated linting or routing enforcement for stage-readiness wording first

- Advantages:
  - could catch drift mechanically once rules are settled
  - gives stronger long-term guardrails
- Disadvantages:
  - premature before the wording contract itself is clear
  - risks building automation around an unsettled distinction
  - larger scope than the current governance gap requires

## Recommended direction

Choose Option 3.

The repository should treat `test-spec` readiness after `spec-review` as a distinct quality judgment, not as shorthand for the next workflow step.

The key answer to the user's "why" is:

- `spec-review` is the last contract-quality gate before downstream proof design depends on the spec;
- `test-spec` authoring should not begin from an ambiguous, incomplete, or weakly testable spec;
- therefore `spec-review` should explicitly say whether the spec is mature enough for eventual `test-spec` authoring, even if the next repository stage is still `architecture` or `plan`.

That distinction should be made explicit in workflow-facing skills and workflow documentation:

- `spec-review` should report:
  - the next repository stage: `architecture` when needed, otherwise `plan`;
  - a separate `test-spec` readiness assessment for eventual proof authoring after required intermediate stages are complete.
- if `spec-review` can name the next repository stage but cannot honestly mark eventual `test-spec` readiness as ready or conditionally-ready, that is a review failure mode:
  - the spec is not approved;
  - downstream planning stops;
  - the workflow returns to spec revision, missing-context resolution, or blocker handling.
- `plan-review` should remain the stage that declares `test-spec` as the immediate next step in the normal repository workflow.
- `test-spec` should continue to require an approved spec, spec-review findings, and a concrete plan before it is authored as the active proof surface.
- the focused follow-up spec should act as the reviewable change contract for this feature;
- `specs/rigorloop-workflow.md` should remain the durable authoritative source for the long-term workflow invariant;
- the focused follow-up spec should reference the durable workflow rule instead of remaining the long-term normative home for the invariant.

The best-practice rule for skills should be:

- workflow order comes from the approved workflow spec, not from individual skill wording;
- workflow-facing skills may assess downstream readiness, but they must not describe a downstream artifact as the next stage when required intermediate stages still exist;
- any skill that emits readiness or handoff language should distinguish:
  - immediate next-stage readiness;
  - downstream-artifact readiness when that assessment is useful;
  - isolated-stop or blocker state.

To keep all skills working according to the workflow, the repository should adopt these best practices:

- Keep one governing workflow order in `specs/rigorloop-workflow.md`, with `docs/workflows.md` and stage skills as derived operating surfaces.
- Use consistent readiness vocabulary across workflow-facing skills instead of letting each skill invent its own closing shape.
- Update workflow docs, affected skills, generated `.codex/skills/`, and test-proof surfaces together whenever workflow wording changes.
- Start with the surfaces directly involved in the observed problem: `workflow`, `spec-review`, `plan-review`, and `test-spec`, instead of normalizing every review-stage skill in one pass.
- Keep `plan-review` in first-pass scope only to align handoff wording:
  - after approved `plan-review`, `test-spec` is the immediate next stage;
  - implementation readiness is downstream readiness, not the immediate handoff;
  - if no wording defect is actually present there, remove `plan-review` from the first-pass implementation scope rather than widening the slice by default.
- Validate both authored skill sources and generated output drift with repo-owned scripts.
- Treat readiness wording as contract surface, not optional prose. If it is stale or misleading, fix it as a real workflow defect.
- Stop downstream authoring when a review can say "next stage is X" but cannot honestly say the downstream artifact is ready; that should return to the appropriate earlier gate instead of silently continuing.
- Defer repository-owned validator enforcement for readiness-wording patterns until the wording contract stabilizes; for v1, use specs, test-spec coverage, and review of the touched workflow-facing skills.

This direction preserves current workflow discipline while making the distinction between handoff and readiness explicit enough to review and teach.

## Expected behavior changes

- `spec-review` outputs will stop using `test-spec` readiness as ambiguous shorthand for the immediate next workflow stage.
- `spec-review` outputs will explicitly distinguish:
  - next repository stage;
  - eventual `test-spec` readiness;
  - blocker or isolated-stop cases.
- `plan-review` will remain the normal handoff point into `test-spec`.
- A spec that is not ready or conditionally-ready for eventual `test-spec` authoring will return to revision or blocker handling instead of continuing downstream as if it were fully approved.
- Workflow-facing skills will have a clearer shared rule for how to describe readiness without competing with the approved workflow order.
- Reviewers and future agents will have a stronger explanation for why test-spec readiness is assessed before test-spec authoring begins.

## Architecture impact

This is a workflow-governance and skill-alignment change, not a runtime architecture change.

Likely touched surfaces:

- focused follow-up spec for this change
- `specs/rigorloop-workflow.md`
- `docs/workflows.md`
- `skills/spec-review/SKILL.md`
- `skills/plan-review/SKILL.md` only if its handoff wording actually needs alignment
- `skills/test-spec/SKILL.md`
- `skills/workflow/SKILL.md`
- regenerated `.codex/skills/` output if canonical `skills/` change

No new persistence, runtime service, router, or CI subsystem is expected for the first slice.

## Testing and verification strategy

- Write a focused spec that defines:
  - the distinction between next-stage readiness and downstream-artifact readiness;
  - why `spec-review` assesses eventual `test-spec` readiness;
  - the negative case where missing eventual `test-spec` readiness blocks spec approval and sends the workflow back upstream;
  - which workflow-facing skills must follow the shared wording rule.
- Fold the durable normative rule into `specs/rigorloop-workflow.md` so the workflow-order invariant does not live only in the focused follow-up spec.
- Add a matching test spec that covers:
  - `spec-review` naming `architecture` or `plan` as the next step without skipping required stages;
  - `spec-review` separately reporting eventual `test-spec` readiness;
  - `spec-review` treating missing eventual `test-spec` readiness as a failure mode rather than a successful handoff;
  - `plan-review` remaining the immediate handoff to `test-spec`;
  - `test-spec` continuing to require approved-spec plus plan context;
  - generated skill drift staying in sync when canonical skills change.
- Use manual contract review across the touched workflow and skill surfaces to confirm they say the same thing.
- Run repo-owned validation for skills, generated drift, and artifact lifecycle on touched artifacts once follow-on work exists.
- Defer a dedicated readiness-wording validator until the wording pattern has stabilized through spec and test-spec-backed usage.

## Rollout and rollback

Rollout:

- settle the direction in proposal review;
- write a focused follow-up spec and fold the durable invariant into `specs/rigorloop-workflow.md`;
- update the affected workflow summary and workflow-facing skills;
- regenerate `.codex/skills/`;
- validate the changed artifact set with repo-owned checks.

Rollback:

- revert the distinction if it proves more confusing than useful;
- keep any truthful corrections that prevent stage-skipping language, even if broader wording is simplified later.

## Risks and mitigations

- Risk: contributors see two readiness concepts and find them harder to use.
  - Mitigation: keep the terms explicit and narrow: "next stage" versus "eventual `test-spec` readiness".
- Risk: the change still drifts because only one skill is updated.
  - Mitigation: define the rule at workflow-contract level and update the directly affected workflow-facing skills in the same slice.
- Risk: the focused spec and `specs/rigorloop-workflow.md` duplicate each other and drift.
  - Mitigation: keep the focused spec as the reviewable change vehicle and fold the enduring invariant into `specs/rigorloop-workflow.md` as the long-term source of truth.
- Risk: the proposal grows into a general skill-governance rewrite.
  - Mitigation: scope the first slice to readiness and handoff wording for workflow-facing skills only.
- Risk: maintainers try to add automation before the contract is stable.
  - Mitigation: keep enforcement document-first and test-spec-backed before adding linting or orchestration logic.
- Risk: review outputs become overly verbose.
  - Mitigation: standardize the distinction in concise closing wording rather than expanding every review into a long template.

## Open questions

- None at proposal stage.

## Decision log

- 2026-04-22: Rejected doing nothing. Reason: the repository has already seen recurring ambiguity around review-stage handoff wording.
- 2026-04-22: Rejected removing `test-spec` readiness from `spec-review` entirely as the preferred direction. Reason: it would hide an important testability judgment instead of clarifying it.
- 2026-04-22: Chose explicit separation between next-stage handoff and eventual `test-spec` readiness as the leading direction. Reason: it preserves workflow order while still preventing weak specs from reaching proof design unnoticed.
- 2026-04-22: Deferred automation-first enforcement. Reason: the wording contract should be settled in specs and skills before validators or routers try to enforce it.
- 2026-04-22: Settled that the change should use both a focused follow-up spec and `specs/rigorloop-workflow.md`. Reason: the focused spec is the reviewable change contract, while the durable normative invariant belongs in the authoritative workflow spec.
- 2026-04-22: Settled that the first implementation pass should start with `skills/spec-review/SKILL.md`, `skills/plan-review/SKILL.md`, `skills/test-spec/SKILL.md`, and `skills/workflow/SKILL.md`. Reason: these are the surfaces directly involved in the observed problem; broader review-skill normalization can wait.
- 2026-04-22: Settled that validator enforcement is a later follow-up, not part of v1. Reason: the wording pattern should stabilize through spec, test-spec, and review coverage before the repository encodes it in a validator.
- 2026-04-22: Settled that inability to mark eventual `test-spec` readiness is a review failure mode rather than a soft warning. Reason: downstream proof planning must not rely on a spec that is still too weak or incomplete for test design.
- 2026-04-22: Narrowed `plan-review` scope to handoff-wording alignment only, and only if that defect is actually present. Reason: the first pass should stay focused on directly observed workflow-facing wording drift.

## Next artifacts

- `proposal-review`
- likely a focused spec for test-spec readiness and workflow-facing skill alignment
- workflow-spec update so the durable rule lands in `specs/rigorloop-workflow.md`
- matching test spec if the proposal is accepted
- plan only if the follow-up touches multiple workflow and skill surfaces
- architecture only if the scope expands beyond guidance and skill behavior

## Follow-on artifacts

- `specs/test-spec-readiness-and-skill-workflow-alignment.md`
- `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
- `specs/test-spec-readiness-and-skill-workflow-alignment.test.md`

## Readiness

- This proposal is accepted.
- The focused follow-up spec now exists and is approved.
- The active execution plan now exists.
- The active test spec now exists.
- No separate architecture artifact is expected for this slice.
- No further `proposal-review` action is pending.
- The next stage is `implement`.
