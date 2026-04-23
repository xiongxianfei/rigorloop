# Implement First-Attempt Correctness

## Status

- approved

## Related proposal

- [Implement First-Attempt Correctness](../docs/proposals/2026-04-23-implement-first-attempt-correctness.md)

## Goal and context

This spec defines the workflow-facing contract for first-pass implementation completeness in the repository's `implement` guidance, with aligned wording in the canonical `workflow` guidance for the same slice.

The problem is not that first-pass implementation sometimes receives review comments. The problem is that preventable in-scope misses can survive the first implementation pass because required authored surfaces, required aligned surfaces, required edge cases, or targeted validation were not treated as part of the same slice before handoff to `code-review`.

This focused spec makes first-pass acceptability observable. It defines what must be complete before `implement` may hand off a slice to `code-review`, what kinds of edge cases are required in the first pass, what counts as the smallest scope-complete change, and what later review findings qualify as preventable first-pass misses.

This feature does not change canonical stage order, lane selection, autoprogression, stop conditions, stage ownership, review-only behavior, fast-lane behavior, or bugfix behavior. It changes the implementation-quality contract for the first pass and aligns the `workflow` companion wording for that same contract.

The enduring repo-wide workflow invariant from this feature may later be folded into `specs/rigorloop-workflow.md`. This focused spec is the reviewable change contract for the feature.

## Glossary

### In-scope requirement

A requirement from the approved slice that the first implementation pass is responsible for satisfying before handoff to `code-review`.

### Approved slice

The approved scope for this feature's current implementation pass, as defined by the accepted proposal, this spec, any matching active test spec, and any active plan when one exists.

### Required authored surface

A code, test, documentation, metadata, plan, or skill surface that the approved slice directly requires to be updated or explicitly assessed as unaffected.

### Required aligned surface

A workflow, skill, summary, generated-output, or other companion surface that must stay aligned with the approved slice when a changed authored surface would otherwise make it stale.

### First-pass acceptable result

A first-pass implementation result that satisfies the completeness conditions in `R1`.

### Required edge case

An edge case that must be handled or evidenced in the first pass because it comes from one or more approved or governing sources listed in `R2`.

### Targeted validation set

The required validation commands or proof surfaces for the slice that are sufficient to demonstrate same-slice completeness before handoff to `code-review`.

### Smallest scope-complete change

The smallest change set that satisfies all in-scope requirements and required aligned surfaces for the slice without leaving a known in-scope defect behind.

### Preventable first-pass miss

A later review finding that should have been caught by the slice's required sources, required edge cases, or targeted validation before `code-review`.

### Same-slice fix

A fix that is required for the approved slice to be contract-complete and therefore must not be deferred to later review, later milestone, or later cleanup.

## Examples first

### Example E1: first pass updates both primary and aligned workflow guidance

Given the approved slice changes the implementation-stage wording in `skills/implement/SKILL.md`
When the slice also requires `skills/workflow/SKILL.md` to stay aligned
Then the first pass updates both surfaces, runs the targeted validation set, and may hand off to `code-review`.

### Example E2: locally correct wording fix still fails the first-pass contract

Given a wording change in one governed spec file is locally correct
When the same slice leaves an active plan body or change-local metadata stale relative to that change
Then the first pass is not acceptable, because a required authored or aligned surface was left stale.

### Example E3: required edge case comes from touched failure-path behavior

Given a slice changes workflow wording around stale lifecycle-state handling
When the touched behavior affects a named failure path already governed by spec or validation
Then that failure path is a required edge case for the first pass even if the proposal did not list it separately.

### Example E4: later review comment does not automatically mean first-pass failure

Given `implement` updates all required in-scope surfaces, covers the required edge cases, and runs the targeted validation set
When `code-review` later suggests a non-required improvement or catches a new issue not required by the slice's governing sources
Then the change may still have met the first-pass contract even though review produced comments.

### Example E5: workflow wording aligns without changing routing behavior

Given this slice updates `skills/workflow/SKILL.md`
When the updated wording reflects first-pass acceptability for `implement`
Then the slice still preserves canonical stage order, lane selection, autoprogression, stop conditions, stage ownership, review-only behavior, fast-lane behavior, and bugfix behavior.

### Example E6: missing targeted validation blocks handoff

Given a slice has named targeted validation for required authored or aligned surfaces
When that validation is not run before `implement` reports readiness for `code-review`
Then the first pass is not acceptable and the workflow must not treat the slice as in-scope complete.

## Requirements

R1. `implement` MUST treat a first-pass acceptable result as the minimum completeness standard before handoff to `code-review` for this feature's slice.

R1a. A first-pass acceptable result MUST satisfy all of the following:
- every in-scope requirement for the slice is addressed;
- every required authored surface in scope is updated, or explicitly marked unaffected with rationale;
- every required aligned surface in scope is updated, or explicitly marked unaffected with rationale;
- no known in-scope defect remains;
- the required targeted validation set passes;
- no required same-slice fix is deferred to later review or later milestone; and
- the change does not rely on later cleanup to become contract-complete.

R1b. A first-pass acceptable result MUST NOT be interpreted as a guarantee of zero later review comments.

R1c. `implement` MUST NOT report readiness for `code-review` when any condition in `R1a` is unsatisfied.

R2. Required edge cases for the first pass MUST come from one or more of the following governing sources:
- approved spec requirements;
- approved test-spec items;
- named regression cases from the motivating incident for the slice;
- changed branch conditions or touched failure paths;
- existing repository tests or fixtures that govern the touched behavior; and
- required aligned workflow or skill wording distinctions for the slice.

R2a. The contract term is `required edge case`. The spec MUST NOT rely on vague wording such as `obvious edge cases` as the normative standard.

R2b. If a touched failure path or changed branch condition creates an edge case under `R2`, that edge case MUST be handled or evidenced in the first pass.

R3. The slice MUST use `smallest scope-complete change` as the completeness target rather than the smallest diff.

R3a. The smallest scope-complete change MUST include every update needed to satisfy all in-scope requirements and required aligned surfaces for the slice.

R3b. A smaller diff that leaves a known in-scope defect, stale required surface, or missing required edge case behind MUST NOT qualify as scope-complete.

R4. Later review findings MUST be distinguished between preventable first-pass misses and other review outcomes.

R4a. A preventable first-pass miss is a review finding that should have been caught by the slice's required sources, required edge cases, or targeted validation before `code-review`.

R4b. Later review comments that do not arise from an ignored in-scope requirement, required surface, required edge case, or skipped targeted validation MUST NOT automatically be treated as a first-pass contract failure.

R5. Before handoff to `code-review`, `implement` MUST identify the full same-slice completeness set for the approved slice.

R5a. That completeness set MUST include:
- in-scope requirements;
- required authored surfaces;
- required aligned surfaces;
- required edge cases; and
- the targeted validation set.

R5b. If a required authored or aligned surface remains unchanged, `implement` MUST explicitly mark it unaffected with rationale in a contributor-visible authoritative surface for the slice.

R5ba. Acceptable authoritative surfaces under `R5b` are:
- the active plan when one exists;
- required change-local artifacts for the slice, such as `docs/changes/<change-id>/change.yaml` or durable reasoning artifacts;
- the active test spec when that surface is part of the slice's governing proof set; or
- another touched lifecycle-managed artifact that is authoritative for the changed area under the repository workflow contract.

R5c. If missing inputs, contradictions, or unresolved scope ambiguity prevent an in-scope complete first pass, `implement` MUST stop and report the blocker instead of handing off to `code-review`.

R6. `workflow` MUST align with this slice in wording without changing routing behavior.

R6a. In this slice, `skills/workflow/SKILL.md` MUST reflect the same first-pass acceptability and smallest scope-complete change concepts that govern `skills/implement/SKILL.md`.

R6b. This slice MUST NOT change:
- canonical stage order;
- lane selection rules;
- autoprogression rules or stop conditions;
- stage ownership;
- review-only lane behavior;
- fast-lane behavior; or
- bugfix workflow behavior.

R6c. This slice MUST preserve the existing ownership split:
- `implement` owns implementation completion and milestone readiness for review;
- `code-review` owns review findings and `clean-with-notes`;
- `verify` owns `branch-ready`; and
- `pr` owns PR-body and PR-opening readiness.

R6d. `workflow` is updated only to align wording for this slice, not to change routing behavior.

R7. The targeted validation set MUST be run before `implement` reports readiness for `code-review`.

R7a. The targeted validation set for the slice MUST come from the approved spec, matching test spec, active plan when one exists, or existing repository-owned validation requirements that govern the touched behavior.

R7b. If required targeted validation is not run, the first pass MUST be treated as unacceptable under `R1`.

R7c. This feature MUST NOT require broader repository-wide validation when the governing artifacts for the slice only require narrower targeted proof before `code-review`.

R8. Required authored and aligned surfaces MUST stay truthful for the slice.

R8a. A required in-scope surface left stale is a first-pass failure.

R8b. A required aligned surface left stale without an explicit out-of-scope or unaffected rationale is a first-pass failure.

R8c. In the first implementation slice for this feature, `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` MUST be updated together.

R8d. In the first implementation slice for this feature, `docs/workflows.md` MUST be updated when the changed canonical skill wording would otherwise leave the short operational workflow summary stale.

R8e. In the first implementation slice for this feature, generated `.codex/skills/` output MUST be regenerated when the changed canonical `skills/` wording would otherwise leave generated adapter guidance stale.

R9. This feature MUST preserve existing tests-first and scope-control expectations.

R9a. This feature MUST NOT weaken the existing requirement that tests or other proof surfaces are written or updated first when feasible for the slice.

R9b. This feature MUST NOT authorize unrelated refactors in the name of first-pass completeness.

R9c. This feature MUST NOT turn `implement` into `code-review`, architecture design, or broad exploratory work when the approved slice is already clear.

R10. This focused spec MUST remain the reviewable change contract for the feature.

R10a. The enduring repo-wide workflow invariant from this feature MUST ultimately live in `specs/rigorloop-workflow.md` if the repository decides the rule is part of the durable generic workflow contract.

R10b. This first feature slice MUST stay focused on `implement` plus aligned `workflow` wording. Extending the same vocabulary to `bugfix` and other implementation-adjacent skills is deferred to a later approved change.

## Inputs and outputs

Inputs:

- the accepted proposal for this feature;
- approved upstream artifacts for the slice, including the relevant feature spec, test spec, architecture inputs when relevant, and active plan when one exists;
- the touched authored surfaces and any workflow or generated surfaces that must remain aligned with them;
- governing repository tests, fixtures, and changed failure paths relevant to the slice;
- the required targeted validation set for the slice.

Outputs:

- `implement` guidance that defines first-pass acceptability in observable terms;
- aligned `workflow` guidance for the same implementation-stage expectation;
- contributor-visible handling for required authored surfaces and required aligned surfaces, including unaffected rationale when applicable;
- contributor-visible first-pass outcomes that either:
  - hand off a scope-complete slice to `code-review`; or
  - stop with an explicit blocker when first-pass acceptability cannot be satisfied.

## State and invariants

- First-pass acceptability is a pre-handoff completeness standard, not a zero-comment guarantee.
- Required authored surfaces and required aligned surfaces are distinct but equally part of first-pass completeness when they are in scope.
- Required edge cases come from governing sources, not intuition alone.
- Smallest scope-complete change is not the same as the smallest diff.
- A preventable first-pass miss is a failure of same-slice completeness, not merely an unfortunate review comment.
- This slice preserves canonical stage order, lane selection, autoprogression, stop conditions, stage ownership, review-only behavior, fast-lane behavior, and bugfix behavior.
- `implement`, `code-review`, `verify`, and `pr` continue to own different claim types.

## Error and boundary behavior

- If a required in-scope requirement is missing, the first pass fails.
- If a required authored surface is stale, the first pass fails unless that surface is explicitly marked unaffected with rationale under `R5b`.
- If a required aligned surface is stale, the first pass fails unless that surface is explicitly marked unaffected with rationale under `R5b`.
- If a required edge case is not handled or evidenced in the first pass, the first pass fails.
- If the targeted validation set is not run, the first pass fails.
- If the change depends on later cleanup to become in-scope complete, the first pass fails.
- If approved artifacts conflict or omit necessary information, `implement` must stop with a blocker instead of handing off an incomplete slice to `code-review`.
- If later `code-review` identifies an issue that was not required by the slice's governing sources or targeted validation, that finding does not automatically invalidate the first-pass contract.

## Compatibility and migration

- This feature is a workflow-contract change, not a product runtime migration.
- It does not change canonical stage order, lane selection, autoprogression, stop conditions, stage ownership, review-only lane behavior, fast-lane behavior, or bugfix behavior.
- It does not replace `code-review`, `verify`, or `pr`.
- It does not require a new workflow stage, new persistence, or a new orchestration subsystem.
- It does not require validator-backed scoring in the first slice.
- Existing implementation wording that permits handoff after a smaller but in-scope incomplete diff becomes incompatible once this feature lands.

## Observability

- A reviewer MUST be able to tell whether `implement` treated the first pass as acceptable for the slice before handoff to `code-review`.
- A reviewer MUST be able to tell which required authored surfaces and required aligned surfaces were updated or explicitly marked unaffected with rationale.
- A reviewer MUST be able to tell which required edge cases were handled or evidenced for the slice.
- A reviewer MUST be able to tell which targeted validation commands or proof surfaces were used before handoff to `code-review`.
- A reviewer MUST be able to tell when `implement` stopped because missing or contradictory inputs prevented a scope-complete first pass.
- Workflow-facing guidance surfaces touched by the slice SHOULD use consistent vocabulary for first-pass acceptable result, required edge cases, smallest scope-complete change, and preventable first-pass miss.

## Security and privacy

- This feature MUST NOT introduce new secret, credential, or network requirements.
- This feature MUST NOT weaken existing review or verification gates for security-sensitive changes.
- Contributor-visible outputs for first-pass completeness MUST NOT expose secrets or private runtime data while describing blockers, unaffected rationale, or validation evidence.

## Accessibility and UX

- No end-user UI or accessibility contract changes are involved in this feature.
- Contributor-facing workflow wording SHOULD use the defined glossary terms rather than subjective synonyms when describing first-pass completeness.

## Performance expectations

- No product runtime performance change is expected.
- This feature SHOULD reduce avoidable review churn caused by preventable first-pass misses.
- This feature MUST NOT add a new mandatory repository stage.
- This feature MUST NOT require broader-than-needed validation when narrower targeted validation already satisfies the governing slice contract.

## Edge cases

1. A required authored surface may remain unchanged and still satisfy the contract only when it is explicitly marked unaffected with rationale.
2. A required aligned surface may remain unchanged and still satisfy the contract only when it is explicitly marked unaffected with rationale.
3. A locally correct wording or code fix still fails the first-pass contract if it leaves an in-scope plan body, change-local metadata surface, or other required authored or aligned surface stale.
4. A later review comment does not automatically prove first-pass failure when the issue was not required by the slice's governing sources, required edge cases, or targeted validation.
5. A touched failure path can create a required edge case even when the proposal or summary prose did not list that case separately.
6. Updating `skills/workflow/SKILL.md` for this slice must not alter stage order, routing behavior, or the ownership split between `implement`, `code-review`, `verify`, and `pr`.
7. If required targeted validation for a narrow slice passes, this feature does not require broader validation solely because the feature is workflow-facing.
8. If approved artifacts are too ambiguous to determine the required authored surfaces, required aligned surfaces, or required edge cases for the slice, the correct behavior is to stop with a blocker instead of handing off to `code-review`.

## Non-goals

- guaranteeing that every first attempt is perfect or review-comment-free
- replacing `code-review`, `verify`, or `pr`
- broadening this slice into bugfix-lane changes
- changing stage order, autoprogression, or routing behavior
- authorizing unrelated refactors in the name of completeness
- building validator-backed scoring of implementation quality in the first slice

## Acceptance criteria

- A reviewer can tell from the updated spec and touched workflow guidance what counts as a first-pass acceptable result before handoff to `code-review`.
- A reviewer can tell which sources define required edge cases for the slice.
- A reviewer can distinguish the smallest scope-complete change from the smallest diff.
- A reviewer can determine whether a later review finding is a preventable first-pass miss under this contract.
- A reviewer can confirm that `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` are both in the first implementation slice.
- A reviewer can confirm that this slice preserves stage order, lane selection, autoprogression, stop conditions, stage ownership, review-only behavior, fast-lane behavior, and bugfix behavior.

## Open questions

- None at spec stage.

## Next artifacts

- implementation under `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
- change-local artifacts under `docs/changes/2026-04-23-implement-first-attempt-correctness/`

## Follow-on artifacts

- `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
- `specs/implement-first-attempt-correctness.test.md`

## Readiness

Spec review feedback is incorporated.

This spec is approved.

No separate architecture artifact is expected for this slice.

A concrete execution plan now exists at `docs/plans/2026-04-23-implement-first-attempt-correctness.md`.

The active test spec and required change-local artifacts now exist.

`M1` implementation, first-pass `code-review`, `verify`, and `explain-change` are complete under the tracked plan and change-local artifacts.

The next stage is `pr`.
