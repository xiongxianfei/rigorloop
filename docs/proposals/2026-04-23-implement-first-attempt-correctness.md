# Implement First-Attempt Correctness

## Status

- accepted

## Problem

The repository already tells `implement` to read the approved artifacts, write tests first when feasible, stay within scope, avoid unrelated refactors, and stop instead of silently guessing around gaps. That is a solid baseline, but it still leaves one important expectation implicit:

- the first implementation pass should aim to be the right pass, not merely the quickest pass that starts moving code.

Today the skill tells the agent what inputs to read and what loop to follow, but it does not explicitly define what counts as an acceptable first pass before handoff to `code-review`. That gap creates recurring quality risk:

- a required in-scope authored surface can be left incomplete even when the main touched file looks correct;
- a required aligned surface can be left stale while the local edit still appears narrowly correct;
- a required edge case can be omitted from the first pass and only surface later in review;
- targeted validation can be too narrow to prove same-slice completeness;
- "smallest change" can be interpreted too narrowly as the smallest diff instead of the smallest scope-complete change.

This is a workflow-quality problem, not just a style preference. RigorLoop explicitly optimizes for correctness, reviewability, traceability, and trustworthy automation over speed-by-default. The `implement` stage should therefore make first-pass acceptability explicit and observable.

## Goals

- Define a clear first-attempt-correctness posture for the `implement` skill.
- Define observable contract terms for first-pass acceptability, required edge cases, smallest scope-complete change, and preventable first-pass misses.
- Keep `skills/workflow/SKILL.md` aligned in the same first slice so entrypoint guidance does not lag the stage-local `implement` contract.
- Make the first implementation pass aim for the smallest change that fully satisfies the approved slice, not the smallest partial patch.
- Preserve test-first discipline, scope control, and explicit blocker handling.
- Reduce avoidable rework caused by shallow first edits that could have been prevented by better up-front synthesis of the approved context.
- Keep the agent honest when confidence is low: stop, surface the blocker, and avoid speculative implementation.

## Non-goals

- Guaranteeing that every first attempt is perfect or never needs review feedback.
- Replacing `code-review`, `verify`, or other downstream quality gates.
- Turning `implement` into a broad research or architecture phase.
- Encouraging large speculative diffs in the name of "getting it right."
- Blurring the line between careful preparation and silently guessing through ambiguity.
- Building a retry counter, scorecard, or punitive workflow around normal iteration.
- Changing canonical stage order, lane selection, autoprogression, stop conditions, stage ownership, review-only behavior, fast-lane behavior, or bugfix behavior in this slice.

## Context

- `CONSTITUTION.md` says the repository MUST optimize for reviewability, traceability, and trustworthy automation over speed-by-default.
- `CONSTITUTION.md` also says agents MUST NOT silently guess around spec gaps, review findings, or failing validation.
- `AGENTS.md` says implementation should keep diffs scoped, use the smallest relevant validation first, and state a spec gap explicitly instead of silently guessing.
- `skills/implement/SKILL.md` already requires reading the plan, feature spec, test spec, architecture inputs when relevant, neighboring code patterns, and validation commands before editing.
- `skills/implement/SKILL.md` already enforces tests-first, minimal implementation, narrow validation, milestone commits, and plan upkeep.
- What is missing is an explicit requirement that the agent internalize the approved slice before making the first edit:
  - what behavior is actually required;
  - what tests and proof surfaces matter;
  - what neighboring patterns the codebase already expects;
  - what required edge cases are in scope for the slice;
  - what the smallest scope-complete change is, including directly coupled lifecycle-managed or change-local artifacts.
- A recent local workflow-governance follow-up showed the gap in concrete form:
  - the wording fix in `specs/plan-index-lifecycle-ownership.md` and `specs/rigorloop-workflow.md` was itself correct;
  - but the active plan and the change-local metadata were initially stale relative to that local diff;
  - that meant the first pass still fell short of the repository's own verify expectations even though the narrow text edit looked right in isolation.
- This is the kind of miss the proposal is targeting:
  - not "the code was wrong";
  - but "the first attempt was incomplete because it did not carry the obviously coupled proof and bookkeeping surfaces with the implementation change."
- The defect is not that first-pass implementation sometimes receives review comments.
- The defect is that preventable first-pass misses across required authored or aligned surfaces can survive until later `code-review`.
- The repository already treats stage-local skill wording as important contract surface. Earlier workflow work repeatedly found that when an expectation stays implicit, contributors and generated guidance drift even if the top-level intent is reasonable.
- The existing `bugfix` skill already starts with understanding expected behavior and reproducing the failure before editing. `implement` has the necessary inputs, but not yet the same explicit "understand before changing" posture.

## Options considered

### Option 1: Do nothing and rely on the current `implement` checklist plus downstream review

- Advantages:
  - no new wording to maintain
  - keeps the existing skill shorter
  - assumes TDD, review, and verification already catch bad first attempts
- Disadvantages:
  - leaves an important quality expectation implicit
  - still allows shallow first edits that are mechanically compliant but predictably incomplete
  - treats avoidable churn as acceptable even when the approved context already contained enough information to do better

### Option 2: Treat "do the right thing on the first attempt" as a hard success guarantee

- Advantages:
  - strongest possible ambition
  - easy to say in principle
- Disadvantages:
  - not truthful as a repository contract
  - risks encouraging overclaiming, hidden uncertainty, or reluctance to stop when the contract is incomplete
  - conflates a quality posture with an impossible outcome guarantee
  - could punish normal review feedback instead of improving first-pass reasoning

### Option 3: Add an explicit first-attempt-correctness posture to `implement` and align `workflow` in the same first slice

- Advantages:
  - operationalizes the user's direction without pretending perfection is guaranteed
  - strengthens the skill at the place where the behavior actually matters
  - keeps the workflow entrypoint and stage-local implementation guidance synchronized from the start
  - complements the existing TDD, scope, and no-guessing rules instead of replacing them
  - keeps the first slice relatively small and reviewable
- Disadvantages:
  - adds more judgment-oriented wording to the skill
  - still requires care so `workflow` stays supportive of `implement` rather than broadening the feature into a general skill rewrite

### Option 4: Add validator or automation enforcement for shallow first attempts

- Advantages:
  - would create stronger executable guardrails later
  - could detect some forms of drift once the contract is stable
- Disadvantages:
  - the repository does not yet have a crisp, automatable definition of a "bad first attempt"
  - bigger scope than the wording gap the user identified
  - risks building tooling before the behavior contract is clearly specified

## Recommended direction

Choose Option 3.

The repository should add a first-attempt-correctness posture to `implement` using observable contract terms rather than internal confidence language.

At minimum, the follow-up spec should define:

- what makes a first-pass implementation result acceptable;
- which edge cases are required in the first pass for the slice;
- what counts as the smallest scope-complete change;
- what makes a later review finding a preventable first-pass miss.

The first implementation slice should update these two canonical skills together:

- `skills/implement/SKILL.md` as the primary behavior-defining surface;
- `skills/workflow/SKILL.md` as the routing and workflow-summary companion surface that should reflect the same expectation in a narrower form.

The key distinction is:

- first-pass acceptability is the standard;
- zero review comments is not the standard.

This proposal should therefore define first-attempt correctness as an implementation-quality contract, not as a perfection guarantee.

In practical terms, the `implement` skill should teach the agent to front-load the checks needed to produce a first-pass acceptable result:

- confirm every in-scope requirement for the slice;
- identify every required authored surface in scope;
- identify every required aligned surface in scope;
- identify required edge cases from approved artifacts, changed branch conditions, touched failure paths, existing governing tests or fixtures, and required wording distinctions in the slice;
- run required targeted validation before handoff to `code-review`;
- stop when a spec gap, architecture gap, or conflicting signal prevents an in-scope complete first pass.

This posture should remain tightly bounded:

- it does not authorize broader design work once the approved artifacts are already clear;
- it does not weaken tests-first behavior;
- it does not turn `implement` into `code-review`;
- it does not license unrelated refactors in the name of thoroughness.

If the repository accepts this direction, the follow-up change should encode it as a reviewable contract first and only then update the stage-local skill wording. If the resulting rule is treated as a durable expectation for implementation-stage behavior across the repository, it should also be reflected in `specs/rigorloop-workflow.md` rather than living only in a focused one-off spec.

That first slice should stay focused on `implement` plus `workflow`. Aligning `bugfix` and other implementation-adjacent skills to the same vocabulary is a reasonable later follow-up, but it should not expand the first change by default.

## Observable Contract Terms

### First-pass acceptable result

A first-pass implementation result is acceptable when all of the following are true:

- every in-scope requirement for the slice is addressed
- every required authored surface in scope is updated, or explicitly marked unaffected with rationale
- every required aligned surface in scope is updated, or explicitly marked unaffected with rationale
- no known in-scope defect remains
- required targeted validation passes
- no required same-slice fix is deferred to later review or later milestone
- the change does not rely on later cleanup to become contract-complete

A first-pass acceptable result does not mean the change is guaranteed to receive zero review comments.

### Required edge cases

Required edge cases are the edge cases that must be handled or evidenced in the first pass because they come from one or more of:

- approved spec requirements
- approved test-spec items
- named regression cases from the motivating incident
- changed branch conditions or touched failure paths
- existing repository tests or fixtures that govern the touched behavior
- required aligned workflow or skill wording distinctions for this slice

`Obvious edge cases` is not the contract term.

### Smallest scope-complete change

The smallest scope-complete change is the smallest change set that satisfies all in-scope requirements and required aligned surfaces for the slice without leaving a known in-scope defect behind.

This is not the same as the smallest diff.
It is the smallest complete change that meets the slice contract.

### Preventable first-pass miss

A preventable first-pass miss is a review finding that should have been caught by the slice's required sources, required edge cases, or targeted validation before `code-review`.

## Success Criteria

This slice succeeds when:

- the first implementation pass updates all required in-scope surfaces
- the first implementation pass covers or explicitly addresses required edge cases
- the targeted validation set passes before `code-review`
- later `code-review` may still find issues, but not because a required in-scope surface or required edge case was ignored
- workflow-facing wording stays aligned across the touched skill and summary surfaces

## Failure Criteria

This slice fails when any of the following occurs:

- a required in-scope surface is left stale
- a required aligned surface is left stale without an explicit out-of-scope decision
- a required edge case is missing from the first pass
- targeted validation required by the slice is not run
- the change depends on later cleanup to become in-scope complete

## Workflow Behaviors That Do Not Change In This Slice

This slice does not change:

- canonical stage order
- lane selection rules
- autoprogression rules or stop conditions
- stage ownership
- review-only lane behavior
- fast-lane behavior
- bugfix workflow behavior
- the existing ownership split between `implement`, `code-review`, `verify`, and `pr`

Specifically:

- `implement` still owns implementation completion and milestone readiness for review
- `code-review` still owns review findings and `clean-with-notes`
- `verify` still owns `branch-ready` conclusions
- `pr` still owns PR-body and PR-opening readiness
- `workflow` is updated only to align wording for this slice, not to change routing behavior

## Expected behavior changes

- `implement` guidance will explicitly require a first-pass acceptable result before handoff to `code-review`.
- `workflow` guidance will mirror that same requirement in routing and summary wording, so the entrypoint does not describe a looser posture than `implement`.
- The skills will distinguish the smallest scope-complete change from a smaller but incomplete diff.
- First-pass implementation behavior will explicitly account for required authored surfaces, required aligned surfaces, required edge cases, and targeted validation for the slice.
- When the approved context is insufficient or contradictory, `implement` will stop and surface the blocker instead of handing off a change that is not in-scope complete.
- Review comments may still happen later, but preventable first-pass misses should no longer survive merely because a required surface or required edge case was ignored.

## Architecture impact

This is a workflow-contract and stage-guidance change, not a runtime architecture change.

Likely touched surfaces if the proposal is accepted:

- a focused follow-up spec for `implement` first-attempt correctness
- `specs/rigorloop-workflow.md` if the repository treats this as a durable implementation-stage invariant
- a matching test spec
- `skills/implement/SKILL.md`
- `skills/workflow/SKILL.md`
- `docs/workflows.md` only where the short operational summary would otherwise become stale
- regenerated `.codex/skills/` output after canonical skill changes

This first slice should not require:

- a new orchestration subsystem
- new persistence or metadata
- CI redesign
- architecture docs or ADR work unless the scope later expands beyond stage guidance

## Testing and verification strategy

- Write a focused follow-up spec that defines what first-attempt correctness means for `implement` without turning it into a perfection guarantee.
- Keep that focused contract centered on `implement`, while requiring `workflow` to stay aligned where it summarizes or routes the same implementation-stage expectation.
- Add a matching test spec that covers:
  - the observable contract terms defined in this proposal
  - success criteria and failure criteria for the slice
  - preservation of tests-first and scope-control rules
  - recognizing when a locally correct wording or code fix still requires coupled plan or change-local artifact updates to be a complete first pass
  - stopping on spec or architecture ambiguity instead of handing off an in-scope incomplete change
  - `skills/workflow/SKILL.md` and `skills/implement/SKILL.md` expressing compatible first-pass expectations in the first implementation slice
  - non-changing workflow boundaries for stage order, routing, autoprogression, stage ownership, fast-lane, review-only, and bugfix behavior
  - avoiding wording that implies review or verification already happened
- Review the touched workflow-facing surfaces together so the canonical `implement` skill, any related workflow summary text, and generated `.codex/skills/` output say the same thing.
- Run the repository-owned skill and artifact validation commands after implementation lands.
- Defer automation that tries to score or detect first-attempt quality until the wording contract is stable enough to enforce.

## Rollout and rollback

Rollout:

- settle the proposal in `proposal-review`;
- write the focused spec and matching test spec;
- decide whether the durable invariant also belongs in `specs/rigorloop-workflow.md`;
- update `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` together;
- update any directly affected canonical workflow summary guidance;
- regenerate `.codex/skills/`;
- validate the changed artifact set with repo-owned checks.

Rollback:

- revert the focused contract and related skill-wording changes together if the new posture proves unclear or too subjective;
- keep existing tests-first, blocker, and scope rules even if the explicit first-attempt wording is later simplified.

## Risks and mitigations

- Risk: contributors read this as a promise that the first attempt must be perfect.
  - Mitigation: define it explicitly as a first-pass acceptable result, not as a zero-comment or perfect-outcome guarantee.
- Risk: the change encourages over-analysis and slows straightforward milestones.
  - Mitigation: keep the expectation tied to required in-scope surfaces, required edge cases, and required targeted validation rather than broad pre-implementation research.
- Risk: "smallest complete change" becomes an excuse for broader edits.
  - Mitigation: define the target as the smallest scope-complete change for the approved slice, not the broadest defensible cleanup.
- Risk: the wording drifts across `implement`, workflow guidance, and generated skill output.
  - Mitigation: update `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` together in the first slice, then regenerate and validate derived output in the same change.
- Risk: maintainers later try to automate enforcement before the contract is stable.
  - Mitigation: keep validator or scoring ideas explicitly deferred to a later proposal if experience shows they are needed.

## Open questions

- None at proposal stage.

## Decision log

- 2026-04-23: Rejected doing nothing. Reason: the repository already has the needed inputs and discipline surfaces, but the desired first-attempt posture is still implicit and therefore easy to under-enforce.
- 2026-04-23: Rejected a hard first-attempt success guarantee. Reason: that would be a misleading contract and could encourage bluffing through ambiguity instead of surfacing blockers.
- 2026-04-23: Chose an explicit first-attempt-correctness posture for `implement` as the leading direction. Reason: it operationalizes the user's request while staying compatible with TDD, scope control, and honest blocker handling.
- 2026-04-23: Deferred validator or scoring enforcement. Reason: the repository should settle the wording contract before trying to automate judgments about first-attempt quality.
- 2026-04-23: Settled that the first implementation slice updates `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` together. Reason: the stage-local contract and the workflow entrypoint should not drift on the same implementation expectation.
- 2026-04-23: Deferred `bugfix` and other implementation-adjacent skills to a future follow-up. Reason: the first slice should stay focused on `implement`, with `workflow` aligned at the same time, rather than broadening immediately into every adjacent skill.
- 2026-04-23: Replaced subjective terms such as `obvious edge cases` and `high-confidence first pass` with observable contract terms and explicit workflow non-change boundaries. Reason: the proposal needed spec-ready, testable language rather than intent-based review language.

## Next artifacts

- `proposal-review`
- likely a focused spec for `implement` first-attempt correctness with first-slice alignment requirements for `workflow`
- matching test spec if the proposal is accepted
- update to `specs/rigorloop-workflow.md` if review decides this should become a durable repository-wide implementation-stage invariant
- plan if the accepted follow-up touches enough workflow and skill surfaces to require milestone sequencing
- future follow-up proposal if maintainers want to extend the same vocabulary to `bugfix` and other implementation-adjacent skills

## Follow-on artifacts

- `specs/implement-first-attempt-correctness.md`
- `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
- `specs/implement-first-attempt-correctness.test.md`

## Readiness

- Proposal review is complete. This proposal is accepted.
- The focused spec, active plan, and active test spec now exist for this slice.
- `M1` implementation, first-pass `code-review`, and `verify` are complete under the active plan.
- The next stage is `explain-change`.
