# Test-Spec Readiness And Skill Workflow Alignment

## Status

- approved

## Related proposal

- [Test-Spec Readiness And Skill Workflow Alignment](../docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md)
- [Spec-Review Testability Routing and Output Consolidation](../docs/proposals/2026-05-25-spec-review-testability-routing-output-consolidation.md)

## Goal and context

This spec defines how workflow-facing skills must distinguish the `Immediate next stage` result field from eventual downstream readiness assessments.

The current workflow order already makes `test-spec` follow `architecture` when needed, then `plan`, then `plan-review`. The problem is not stage order. The problem is that review outputs can blur "what happens next" with "is this artifact mature enough for later proof planning." This feature keeps the existing workflow order and isolation rules intact while making that distinction explicit and reviewable.

This focused spec is the change-scoped contract for the feature. The enduring general workflow invariant must ultimately be reflected in `specs/rigorloop-workflow.md` rather than living only here.

This amendment tightens the `spec-review` output contract by separating immediate routing from eventual test-spec readiness with closed fields. It removes the `not-assessed` readiness escape hatch, makes `test-spec` invalid as an immediate next stage from `spec-review`, and binds immediate routing values to review status so the result cannot approve a spec while routing back to revision.

## Glossary

- `Immediate next stage`: the next routed action or repository stage for the current workflow lane, invocation context, and approved workflow order. For `spec-review`, this result field comes from the closed enum `spec revision`, `review-resolution`, `architecture`, `plan`, and `none`.
- `forward repository-stage handoff value`: an `Immediate next stage` value that moves the workflow forward through the repository lifecycle. For `spec-review`, the forward repository-stage handoff values are `architecture` and `plan`.
- `spec revision`: the immediate next-stage value meaning the spec must be revised before downstream reliance.
- `review-resolution`: the immediate next-stage value meaning recorded material findings or blocking outcomes require disposition before the next authoring stage.
- `none`: the immediate next-stage value meaning the review is isolated, inconclusive, blocked by missing inputs, or makes no repository-stage handoff claim.
- `downstream readiness`: an assessment of whether a later stage can be relied on after required intermediate stages complete.
- `eventual test-spec readiness`: the downstream-readiness assessment for later `test-spec` authoring.
- `review outcome`: the workflow-facing spec-review result for this feature: `approved`, `changes-requested`, `blocked`, or `inconclusive`.
- `ready`: eventual `test-spec` readiness status meaning the spec is approved and no known spec-level gap blocks later `test-spec` authoring once required intermediate stages complete.
- `conditionally-ready`: eventual `test-spec` readiness status meaning the spec is approved and testable, but later `test-spec` authoring still depends on explicitly named intermediate stage completion such as `architecture` or `plan`, not on more spec repair.
- `not-ready`: eventual `test-spec` readiness status meaning the spec is not approved for downstream planning because spec defects, contradictions, or missing testable requirements still need upstream repair.
- `workflow-facing skill`: a contributor-visible skill surface that names stage order, handoff, or readiness expectations.
- `review failure mode`: a review outcome where the review cannot safely approve the current artifact for downstream reliance.
- `stop condition`: a documented reason the workflow must stop rather than proceed with downstream reliance or stage continuation.

## Examples first

### Example E1: spec-review with no architecture step names `plan` next and `test-spec` ready later

Given a reviewed spec is precise, testable, and does not require a separate architecture step
When `spec-review` closes successfully
Then it says the immediate next stage is `plan` and separately says eventual `test-spec` readiness is `ready`.

### Example E2: spec-review with architecture dependency uses `conditionally-ready`

Given a reviewed spec is precise enough for later proof design but the workflow still requires `architecture`
When `spec-review` closes successfully
Then it says the immediate next stage is `architecture` and separately says eventual `test-spec` readiness is `conditionally-ready`, naming that dependency.

### Example E3: missing eventual test-spec readiness is a review failure

Given `spec-review` finds the spec too incomplete or ambiguous for later `test-spec` authoring
When the reviewer would otherwise be able to name a next stage
Then the review outcome is `changes-requested` or `blocked`, the immediate next stage is `spec revision` or `review-resolution`, eventual `test-spec` readiness is `not-ready`, and downstream planning stops.

### Example E4: approved plan-review keeps `test-spec` as the immediate next stage

Given `plan-review` approves a concrete plan
When it reports readiness
Then it names `test-spec` as the immediate next stage, and any mention of implementation readiness is clearly downstream rather than replacing that handoff.

### Example E5: test-spec authoring still requires approved spec and plan context

Given a spec review did not produce an approved spec with eventual `test-spec` readiness of `ready` or `conditionally-ready`
When `test-spec` authoring is attempted
Then the workflow treats that as an upstream contract problem rather than authoring the active proof surface from an unready spec.

### Example E6: missing reviewer input produces `Immediate next stage: none`

Given the reviewer lacks required upstream inputs to assess the spec
When `spec-review` closes
Then the result is:

```text
Review status: inconclusive
Immediate next stage: none
Eventual test-spec readiness: not-ready
Stop condition: missing reviewer input
```

### Example E7: approved spec-review cannot route backward

Given `spec-review` approves a spec
When the result reports its immediate next stage
Then the immediate next stage is `architecture` or `plan`
And the result does not use `spec revision`, `review-resolution`, `none`, `test-spec`, or `ready for test-spec` as the immediate next stage.

## Requirements

R1. `spec-review` outputs MUST separate immediate routing from eventual `test-spec` readiness.

The `Immediate next stage` field is the routing field. It MUST use exactly one of:

```text
spec revision
review-resolution
architecture
plan
none
```

`test-spec` MUST NOT be an `Immediate next stage` value.

The values `architecture` and `plan` are forward repository-stage handoff values. The values `spec revision`, `review-resolution`, and `none` are routing or no-handoff values and MUST NOT be described as forward repository stages.

R1a. Generic workflow stage-order derivation applies only when `Immediate next stage` is a forward repository-stage handoff value.

When `Immediate next stage` is:

```text
architecture
plan
```

the skill MUST respect the governing workflow order.

When `Immediate next stage` is:

```text
spec revision
review-resolution
none
```

the field records revision, disposition, or no-handoff routing. These values are not forward repository-stage handoffs.

R1b. Downstream readiness MAY assess a later stage, but it MUST NOT be phrased as the immediate next stage when required intermediate stages still exist.

R1c. The enduring general workflow invariant for this distinction MUST be recorded in `specs/rigorloop-workflow.md`.

R1d. This focused spec MUST act as the reviewable change contract for the feature, not the permanent long-term home for the general workflow invariant.

R2. `spec-review` output MUST distinguish:
- the immediate next stage; and
- eventual `test-spec` readiness.

R2a. `spec-review` output MUST report a review outcome using exactly one of:
- `approved`;
- `changes-requested`;
- `blocked`; or
- `inconclusive`.

R2b. The immediate next stage field MUST use exactly one of:
- `spec revision`;
- `review-resolution`;
- `architecture`;
- `plan`; or
- `none`.

R2c. The immediate next stage field MUST NOT use pseudo-routing states such as `blocker handling`, `missing-context resolution`, `test-spec`, `ready for test-spec`, or similar non-enum labels.

R2d. When the review outcome is `approved` and a separate architecture step is required, `Immediate next stage` MUST be `architecture`.

R2e. When the review outcome is `approved` and no separate architecture step is required, `Immediate next stage` MUST be `plan`.

R2f. When the review outcome is `changes-requested`, the immediate next stage MUST be `spec revision` or `review-resolution`.

R2g. When the review outcome is `blocked`, the immediate next stage MUST be `review-resolution` or `none`.

R2h. When the review outcome is `inconclusive`, the immediate next stage MUST be `none`, and the stop condition MUST record the missing required input.

R2i. An `approved` review outcome MUST NOT pair with immediate next stage `spec revision`, `review-resolution`, or `none`.

R2j. A `changes-requested`, `blocked`, or `inconclusive` review outcome MUST NOT pair with immediate next stage `architecture` or `plan`.

R3. `spec-review` output MUST report eventual `test-spec` readiness using exactly one of:
- `ready`; or
- `conditionally-ready`; or
- `not-ready`.

R3a. `approved` review outcome MUST be paired only with:
- `ready`; or
- `conditionally-ready`.

R3b. `approved` review outcome MUST NOT be paired with:
- `not-ready`.

R3c. `conditionally-ready` MUST name the required intermediate dependency or dependencies that remain before `test-spec` authoring begins.

R3d. `changes-requested` and `blocked` review outcomes MUST be paired with `not-ready`.

R3e. `inconclusive` review outcome MUST be paired with `not-ready`.

R3f. If `spec-review` cannot honestly assess eventual `test-spec` readiness as `ready` or `conditionally-ready`, that is a review failure mode.

R3g. In that failure mode, the spec MUST NOT be treated as approved.

R3h. In that failure mode, downstream planning MUST stop.

R3i. When eventual `test-spec` readiness is `not-ready`, the output MUST either:
- state that the spec is not approved for downstream planning, name the required upstream fix surface as `spec revision` or `review-resolution`, and identify the blocking defect category, such as missing testable requirements or contradictory requirements; or
- for inconclusive reviews, state that readiness cannot be certified, use immediate next stage `none`, and identify the stop condition.

R3j. `spec-review` MUST NOT use `not-assessed` as an eventual `test-spec` readiness value. A review that lacks required inputs to certify testability MUST use review outcome `inconclusive`, `Immediate next stage: none`, eventual `test-spec` readiness `not-ready`, and an explicit stop condition.

R3k. `spec-review` MUST NOT describe `test-spec` as the immediate next stage.

R4. This feature MUST preserve existing stage-order and autoprogression boundaries unless an authoritative workflow artifact is explicitly updated by the same change.

R4a. This feature MUST NOT imply `spec-review -> architecture`, `spec-review -> plan`, or `spec-review -> test-spec` autoprogression beyond the current approved workflow contract.

R4b. This feature MUST preserve `plan-review` as the normal immediate handoff point into `test-spec`.

R4c. Direct or review-only `spec-review` requests MUST remain isolated unless a higher-priority approved workflow rule changes that behavior.

R5. If `plan-review` reports both immediate next stage and later-stage fitness, it MUST distinguish them.

R5a. After approved `plan-review`, the immediate next stage MUST be `test-spec`.

R5b. If `plan-review` mentions implementation readiness, it MUST present that as downstream readiness rather than replacing or obscuring the immediate `test-spec` handoff.

R6. `test-spec` authoring MUST continue to require:
- an approved feature spec;
- spec-review findings; and
- a concrete execution plan; and
- approved architecture or ADR inputs when relevant to the changed boundaries.

R6a. `test-spec` authoring MUST NOT rely on a spec-review outcome that explicitly failed eventual `test-spec` readiness under `R3`.

R6b. When upstream review context shows the spec is not approved or lacks the required readiness, `test-spec` authoring MUST return that work to the appropriate upstream gate instead of silently continuing.

R7. The first implementation pass for this feature MUST align the directly affected workflow-facing skill surfaces:
- `workflow`;
- `spec-review`;
- `test-spec`; and
- `plan-review` only when its existing wording actually conflicts with `R5`.

R7a. This first pass MUST NOT require broader normalization of all review-stage skills.

R8. The repository MUST add or update validation and fixture coverage for the closed `spec-review` routing and readiness fields where deterministic structural checks are feasible.

R8a. Validation MUST reject `Immediate next stage: test-spec` for `spec-review` result skeleton or fixture coverage.

R8b. Validation MUST reject `Review status: approved` paired with `Eventual test-spec readiness: not-ready` where the result fields are structurally inspectable.

R8c. Validation MUST reject status-to-routing contradictions where the result fields are structurally inspectable.

R8d. Validation SHOULD check structural single ownership for the complete material-finding field-label set: `assets/material-finding.md` owns the complete label set, while `SKILL.md` may reference the fields but must not re-enumerate the full labeled set.

R8e. Recorded review-artifact validation for these result fields MAY be deferred until the review-artifact parser can inspect result-field values.

## Inputs and outputs

Inputs:

- approved workflow stage order and lane rules;
- invocation context for isolated versus workflow-managed behavior;
- `spec-review` outcome, eventual `test-spec` readiness, and whether architecture remains required;
- `plan-review` outcome when the plan-review handoff wording is in scope;
- approved spec, spec-review findings, concrete plan, and approved architecture or ADR inputs when relevant for `test-spec` authoring;
- stop conditions such as missing required reviewer inputs.

Outputs:

- explicit `Immediate next stage` wording in workflow-facing review outputs;
- explicit eventual `test-spec` readiness wording in `spec-review` output;
- explicit negative output shapes for `not-ready`;
- explicit stop-condition behavior when required inputs are missing;
- `test-spec` authoring guidance that continues to require approved spec, plan, and relevant architecture or ADR context.

## State and invariants

- Immediate next stage and downstream readiness remain distinct concepts.
- `spec-review` does not approve a spec that fails eventual `test-spec` readiness.
- `plan-review` remains the normal immediate handoff into `test-spec`.
- `test-spec` does not become the immediate next stage directly from `spec-review`.
- Missing context and blocker details are stop conditions, not substitutes for the `Immediate next stage` enum.
- Missing context uses `Immediate next stage: none`, not an omitted field or `not-assessed` readiness value.
- This focused spec is the change vehicle; `specs/rigorloop-workflow.md` remains the durable authoritative workflow rule after the change is folded in.
- Deterministic validator enforcement is required for the closed field contract where the current parser or skill validator can inspect the relevant fields.

## Error and boundary behavior

- If `spec-review` can identify an immediate next stage but cannot honestly assess eventual `test-spec` readiness as `ready` or `conditionally-ready`, the review is not successful.
- If `conditionally-ready` is used without naming the remaining intermediate dependency, the readiness output is incomplete.
- If `plan-review` mentions implementation readiness in a way that obscures `test-spec` as the immediate next stage, the handoff wording is invalid.
- If `test-spec` authoring is attempted from an unapproved spec, from missing spec-review findings, without a concrete plan, or without relevant approved architecture or ADR inputs, the workflow must return to the appropriate upstream stage instead of proceeding as if prerequisites were satisfied.
- If `spec-review` is isolated or review-only, the output still distinguishes immediate next stage from downstream readiness, but it does not auto-continue by implication.
- If required reviewer inputs are missing, the workflow records a stop condition rather than inventing a pseudo-stage.
- If `spec-review` reports `Review status: approved` with immediate next stage `spec revision`, `review-resolution`, or `none`, the result is internally inconsistent and invalid.
- If `spec-review` reports `Review status: changes-requested`, `blocked`, or `inconclusive` with immediate next stage `architecture` or `plan`, the result is internally inconsistent and invalid.
- If `spec-review` reports eventual `test-spec` readiness as `not-assessed`, the result is invalid.

## Compatibility and migration

- This feature is a workflow-governance clarification, not a product runtime change.
- It preserves the existing lifecycle order and existing review-to-next-authoring isolation rules.
- It does not add a new orchestration subsystem, persistent state store, or second readiness registry.
- It does not broaden autoprogression beyond the current approved workflow contract.
- It requires deterministic validator or fixture coverage for the closed field contract where feasible, while allowing recorded review-artifact result-field enforcement to wait for parser support.
- Existing wording that uses `test-spec` as shorthand for the immediate next stage after `spec-review` becomes incompatible once this feature lands.

## Observability

- `spec-review` output MUST make the immediate next stage explicit.
- `spec-review` output MUST make eventual `test-spec` readiness explicit.
- `conditionally-ready` output MUST identify the remaining intermediate dependency.
- `not-ready` output MUST either say that the spec is not approved for downstream planning and identify the upstream fix surface, or say that readiness cannot be certified because an inconclusive review hit a stop condition.
- When `plan-review` wording is in scope, the output MUST make `test-spec` visible as the immediate next stage.
- Workflow-facing skill guidance and workflow summary guidance SHOULD use consistent vocabulary for immediate next stage, downstream readiness, and review failure.

## Security and privacy

- This feature MUST NOT introduce any new secret, credential, or network dependency.
- No new externally publishing or destructive workflow action is introduced by this feature.
- The wording change MUST NOT weaken higher-priority repository policies for security-sensitive workflow decisions.

## Accessibility and UX

This amendment has no graphical UI, screen-reader-specific interface, keyboard navigation surface, color contrast surface, or visual interaction flow.

The user-facing UX surface is Markdown skill output and review-record wording. This spec improves that surface by making the `Immediate next stage` field and `Eventual test-spec readiness` field distinct, closed, and readable.

The accessibility-relevant requirement is clarity for text-only review readers: the output must not require readers to infer whether `test-spec` is a routing target, whether `none` means a missing field, or whether `architecture` and `plan` are the only forward repository-stage handoff values.

## Performance expectations

- No runtime product performance change is expected.
- The wording contract SHOULD reduce review churn caused by ambiguous handoff language, but it MUST NOT add new mandatory workflow stages.

## Edge cases

1. `spec-review` can approve a spec and still say the next stage is `architecture`, with eventual `test-spec` readiness marked `conditionally-ready`.
2. `spec-review` cannot approve a spec whose requirements are too incomplete for later `test-spec` authoring even if a likely next stage could be guessed.
3. `plan-review` may mention downstream implementation readiness, but only after preserving `test-spec` as the immediate next handoff.
4. Direct or review-only `spec-review` remains isolated even when its output names the immediate next stage and eventual downstream readiness.
5. `test-spec` authoring does not proceed from an unapproved spec or from a spec-review outcome that explicitly failed eventual `test-spec` readiness.
6. The first implementation slice may find that `plan-review` already satisfies `R5`; in that case no `plan-review` edit is required.
7. Missing reviewer inputs produce `inconclusive`, immediate next stage `none`, eventual `test-spec` readiness `not-ready`, and an explicit stop condition.
8. A result that says `approved` and `Immediate next stage: spec revision` is invalid because routing contradicts review status.
9. A result that says `Immediate next stage: test-spec` is invalid even if eventual readiness is `ready`.

## Non-goals

- Redesigning the repository stage order.
- Broadening review-to-next-authoring autoprogression.
- Rewriting every review-stage skill in one pass.
- Adding broad natural-language validator scoring for readiness wording.
- Adding `not-assessed` as an eventual readiness value.
- Allowing `test-spec` as an immediate next-stage value from `spec-review`.
- Creating a second readiness registry separate from the workflow contract and workflow-facing skills.

## Acceptance criteria

AC-SRTR-ROUTE-001. The spec consistently names the result field `Immediate next stage`.

AC-SRTR-ROUTE-002. The `Immediate next stage` enum is:
- `spec revision`;
- `review-resolution`;
- `architecture`;
- `plan`; and
- `none`.

AC-SRTR-ROUTE-003. The spec does not describe `spec revision`, `review-resolution`, or `none` as forward repository stages.

AC-SRTR-ROUTE-004. Generic stage-order derivation applies only to the forward stage values `architecture` and `plan`.

AC-SRTR-ROUTE-005. Examples for missing inputs use `Immediate next stage: none`, not an empty or missing immediate-stage field.

AC-SRTR-UX-001. The spec includes an `Accessibility and UX` section.

AC-SRTR-UX-002. The section states that the amendment has no graphical UI surface.

AC-SRTR-UX-003. The section identifies Markdown output clarity as the user-facing UX surface.

AC-SRTR-UX-004. The section ties UX clarity to the distinct `Immediate next stage` and `Eventual test-spec readiness` fields.

- A reviewer can see the distinction between immediate next stage and downstream readiness.
- A reviewer can see that successful `spec-review` must report immediate next stage plus eventual `test-spec` readiness.
- A reviewer can see that eventual `test-spec` readiness is limited to `ready` or `conditionally-ready` in successful `spec-review`.
- A reviewer can see that failure to mark eventual `test-spec` readiness is a review failure that blocks approval and downstream planning.
- A reviewer can see the exact negative output shape for `not-ready`.
- A reviewer can see that `Immediate next stage` values use the closed enum and never pseudo-routing states.
- A reviewer can see that `spec-review` never uses `test-spec` as immediate next stage.
- A reviewer can see that `approved` review status only pairs with immediate next stage `architecture` or `plan`.
- A reviewer can see that `plan-review` preserves `test-spec` as the immediate next handoff when both immediate and downstream readiness are mentioned.
- A reviewer can see that `test-spec` still requires approved spec, spec-review findings, concrete plan context, and relevant architecture or ADR context when applicable.
- A reviewer can see that this feature does not change stage order or broaden autoprogression.
- A reviewer can see that the durable general invariant belongs in `specs/rigorloop-workflow.md`, while this focused spec serves as the reviewable change contract.
- A reviewer can see which validator enforcement is required now and which recorded-artifact enforcement may be deferred pending parser support.

## Open questions

- None.

## Next artifacts

- spec-review for this amendment under `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/`
- plan for `docs/proposals/2026-05-25-spec-review-testability-routing-output-consolidation.md`
- matching test-spec amendment if spec-review approves this contract

## Follow-on artifacts

- `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
- `specs/test-spec-readiness-and-skill-workflow-alignment.test.md`
- `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/`

## Readiness

Spec review feedback for the 2026-05-25 amendment is incorporated.

This spec is approved after clean `spec-review-r2`.

The amended R2, R3, and R8 clauses may be used for downstream planning and matching test-spec amendment work.
