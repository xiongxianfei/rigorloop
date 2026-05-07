# Milestone-Aware Review Handoff

## Status

- accepted

## Problem

The current workflow handoff rule treats a clean `code-review` as a direct handoff to `verify` in workflow-managed full-feature execution. That is correct only when the reviewed implementation slice is the final planned implementation milestone.

For milestone-based plans, this creates a workflow bug: `implement` works one milestone at a time and hands the completed slice to `code-review`, while `code-review` currently assumes a clean review means the whole implementation set is ready for `verify`. A clean review of `M1` can therefore route the workflow past still-planned `M2` or `M3` work.

The result is premature readiness wording, stale plan state, and possible downstream verification before the planned implementation set is actually complete and reviewed.

## Goals

- Make full-feature execution handoff milestone-aware.
- Keep `verify` reserved for the point where all planned implementation milestones are closed or intentionally deferred.
- Make clean milestone review close out the reviewed milestone without implying whole-plan verification readiness.
- Keep review-resolution on the same milestone until findings are closed or explicitly deferred.
- Give plans a clear way to distinguish implementation progress, review status, milestone closeout, and next-stage readiness.
- Align the authoritative workflow contract, operating summary, plan guidance, and affected stage skills.

## Non-goals

- Redesign the whole lifecycle stage order.
- Remove `code-review`, `review-resolution`, `verify`, `explain-change`, or `pr`.
- Add a new lifecycle stage.
- Make every milestone require a separate PR.
- Require all plans to use heavyweight project-management semantics beyond the state needed for workflow routing.
- Solve unrelated stale plan or lifecycle closeout issues.
- Add a standalone `review-resolution` skill in the first slice.
- Add executable plan-state validation in the first slice.
- Hand-edit generated Codex compatibility output under `.codex/skills/`.

## Vision fit

fits the current vision

This change supports RigorLoop's commitment to traceable, reviewable AI-assisted delivery. It makes the implementation-to-review loop reconstructable from tracked artifacts instead of relying on chat memory to know whether `verify` is actually the next valid gate.

## Context

`CONSTITUTION.md` requires the full lifecycle for workflow-stage policy changes and says workflow-governance changes update affected operating and governance guidance or record why a surface is unaffected.

`specs/workflow-stage-autoprogression.md` currently says that in the full-feature lane, once `code-review` is satisfied and no accepted findings remain unresolved, the workflow continues into `verify` unless a stop condition applies. `docs/workflows.md` summarizes this as first-pass `clean-with-notes` continuing to `verify`.

At the same time, `skills/implement/SKILL.md` frames implementation as milestone-based: for each milestone, implementation updates plan evidence, records validation, and hands off to `code-review`. Plan guidance and the workflow summary also treat milestones as reviewable slices with closeout evidence.

Recent learn guidance already captures the invariant: `Ready for verify` is valid only after planned implementation milestones are complete, review-resolution is closed when triggered, and code-review has been conducted. That lesson is useful but not yet encoded in the authoritative handoff rules that drive the skills.

`docs/project-map.md` is absent, so this proposal does not rely on project-map claims.

## Options considered

### Option 1. Keep the current clean-review handoff

Leave `code-review clean-with-notes -> verify` unchanged and rely on contributors to notice whether more milestones remain.

Pros:

- No immediate artifact churn.
- Preserves the current simple autoprogression rule.

Cons:

- Keeps the exact bug that can route past unfinished implementation milestones.
- Leaves plan readiness dependent on chat memory or reviewer vigilance.
- Conflicts with the existing milestone-per-slice implementation model.

### Option 2. Patch only `code-review`

Update `skills/code-review/SKILL.md` so clean review checks for remaining milestones before handing off to `verify`, without changing the workflow spec, plan guidance, or `implement`.

Pros:

- Smallest immediate skill-source edit.
- Directly addresses the most visible bad handoff.

Cons:

- Leaves the approved autoprogression spec saying the older rule.
- Keeps `implement` wording around milestone completion and closeout ambiguous.
- Does not improve plan readiness patterns that reviewers need for evidence.

### Option 3. Add a milestone-aware handoff rule across the workflow contract and affected skills

Amend the autoprogression contract so clean `code-review` inspects the active plan in milestone-based flows. If another implementation milestone remains, the next stage is `implement <next milestone>`; if none remains and review-resolution is not required, the next stage is `verify`.

Pros:

- Fixes the behavior at the source of truth and in the skills that execute it.
- Preserves autoprogression while making it lane-aware and milestone-aware.
- Aligns plan readiness with implementation and review evidence.
- Gives reviewers a clear closeout output for the reviewed milestone.

Cons:

- Touches several workflow infrastructure surfaces.
- Requires careful wording so lifecycle-closeout milestones are not mistaken for unfinished implementation work.

### Option 4. Add validator enforcement for milestone states now

Add machine validation that rejects plan readiness claiming `Ready for verify` while implementation milestones remain open.

Pros:

- Stronger long-term enforcement.
- Could catch stale readiness before PR review.

Cons:

- Overbuilds the first fix before the policy shape is settled.
- Requires parsing plan semantics that may not be uniform yet.
- Can follow later once the plan state vocabulary is approved.

## Recommended direction

Choose Option 3.

The workflow should treat milestone implementation as a loop:

```text
implement milestone
-> code-review milestone
-> review-resolution for that milestone, when triggered
-> implement fixes for that milestone, when needed
-> code-review rerun for that milestone, when needed
-> close milestone
-> implement next milestone, when another implementation milestone remains
```

`verify` should follow only after the planned implementation set is complete and reviewed.

The core policy should be:

- `implement` completes or prepares implementation handoff evidence for the current milestone and hands off to `code-review` for that milestone.
- `implement` does not set whole-plan readiness to `Ready for verify`.
- `code-review` determines whether the reviewed milestone is the final planned implementation milestone before recommending the next stage.
- A clean review of a non-final milestone closes that milestone and hands off to the next implementation milestone.
- A clean review of the final planned implementation milestone closes that milestone and hands off to `verify`, assuming review-resolution is not required and no stop condition applies.
- Review-resolution findings stay attached to the reviewed milestone until the milestone can move out of `resolution-needed`.
- Plans distinguish implementation progress from review closeout and make current handoff explicit.

### Milestone state vocabulary

Each milestone has exactly one `Milestone state`.

Allowed states:

| State | Meaning | Owner |
|---|---|---|
| `planned` | Milestone exists but implementation has not started. | plan |
| `implementing` | Implementation is in progress. | `implement` |
| `review-requested` | Implementation and targeted validation are complete, and the milestone has been handed to `code-review`. | `implement` |
| `resolution-needed` | Review produced findings that require review-resolution, fixes, owner decision, or re-review. | `code-review` / review-resolution |
| `closed` | The milestone has clean review or resolved findings, required evidence is reconciled, and it no longer blocks the next stage. | `code-review` when no findings; review-resolution / plan when findings existed |

`implementation-complete` and `review-clean` are evidence descriptions, not milestone states.

The preferred post-implement milestone state is `review-requested`.

### Milestone transition rules

`implement` transitions:

- `planned` -> `implementing`
- `implementing` -> `review-requested`

`code-review` transitions:

- `review-requested` -> `closed` when review is clean and no review-resolution is required
- `review-requested` -> `resolution-needed` when review findings require review-resolution, fixes, owner decision, or re-review
- `review-requested` remains `review-requested` when review is inconclusive and more review evidence is needed

`review-resolution` and fix loops keep the workflow on the same milestone until findings are dispositioned and required fixes are validated.

A clean review of a non-final milestone closes that milestone and hands off to the next in-scope implementation milestone.

A clean review of the final in-scope implementation milestone closes that milestone and hands off to `verify`.

### No milestone postponement

Milestones are not postponed to make `verify` available.

If a planned milestone no longer belongs in the current change, revise the plan before handoff.

After plan revision, `verify` may proceed only when no in-scope implementation milestone remains open or unresolved.

### Current handoff summary

For milestone-based plans, update this summary whenever implementation or review changes milestone readiness:

- Current milestone:
- Current milestone state:
- Last reviewed milestone:
- Review status:
- Remaining in-scope implementation milestones:
- Next stage:
- Verify readiness:
- Reason verify is or is not ready:

Non-final milestone example:

```md
- Current milestone: M1
- Current milestone state: closed
- Last reviewed milestone: M1
- Review status: clean-with-notes
- Remaining in-scope implementation milestones: M2, M3
- Next stage: implement M2
- Verify readiness: not ready
- Reason verify is not ready: implementation milestones remain
```

Final milestone example:

```md
- Current milestone: M3
- Current milestone state: closed
- Last reviewed milestone: M3
- Review status: clean-with-notes
- Remaining in-scope implementation milestones: none
- Next stage: verify
- Verify readiness: ready
- Reason verify is ready: all in-scope implementation milestones are closed and code-review is complete
```

## Expected behavior changes

- After `implement M1`, the workflow hands off to `code-review M1`, not to whole-plan verification.
- After clean `code-review M1`, the milestone state becomes `closed`. If `M2` remains, the next stage is `implement M2`.
- If `code-review M1` finds material or required-change findings, `review-resolution M1` runs before any move to `M2`.
- A milestone is not considered closed before clean review and required review-resolution closeout.
- `Ready for verify` appears only when no in-scope implementation milestone remains open or unresolved and the final implementation milestone is `closed`.
- Lifecycle-closeout work such as `verify`, `explain-change`, and PR handoff is labeled separately from unfinished implementation milestones.

## Architecture impact

This is a workflow-infrastructure change, not product runtime architecture.

Expected affected authored surfaces:

- `specs/workflow-stage-autoprogression.md` and matching test spec
- `specs/rigorloop-workflow.md` and matching test spec
- review-recording or review-resolution specs if the same-milestone finding closeout rule needs normative coverage there
- `docs/workflows.md`
- `skills/implement/SKILL.md`
- `skills/code-review/SKILL.md`
- `skills/plan/SKILL.md`
- `AGENTS.md` only if contributor-facing root guidance is affected
- skill validator or fixture tests when skill wording is structurally checked

Generated Codex skill mirrors and public adapter package output may need regeneration from canonical sources, but they should not be edited by hand.

No new storage model, external service, runtime data flow, or deployment boundary is expected. An architecture artifact is probably unnecessary because the first slice should include only guidance and static wording checks, not executable workflow routing or plan-state parsing.

## Testing and verification strategy

- Update the feature spec and test spec to cover milestone-aware `code-review` handoff.
- Add scenario coverage for:
  - clean review of a non-final milestone routes to the next implementation milestone;
  - clean review of the final implementation milestone routes to `verify`;
  - findings route through review-resolution for the same milestone;
  - ambiguous plan state produces `inconclusive` or a required plan update instead of `verify`;
  - lifecycle-closeout milestones do not block verify as if they were unfinished implementation milestones.
- Add static skill validation or existing skill-validator assertions for the new `implement`, `code-review`, and `plan` guidance if the current validator pattern supports wording checks.
- Do not add executable plan-state validation in the first implementation slice; defer that until the guidance has settled and plan structure is uniform enough to parse safely.
- Validate generated-output drift after canonical skill updates.
- Run selector-selected explicit validation for the touched proposal/spec/test-spec/workflow and skill paths before PR readiness.

## Rollout and rollback

Roll out by first updating the authoritative spec and test spec, then aligning the operational summary, plan guidance, affected skills, static wording checks, and generated outputs.

Existing in-flight plans may continue if their tracked readiness is already truthful. Plans touched by this change should adopt the new current-handoff pattern when they next update milestone state.

Rollback is straightforward for guidance-only implementation: revert the spec and skill wording to the prior `clean-with-notes -> verify` behavior. If later validator enforcement is added in a follow-up, rollback also removes or relaxes those plan-state checks.

## Risks and mitigations

- Risk: the workflow loses useful autoprogression momentum.
  - Mitigation: keep automatic continuation, but route to the next valid milestone instead of stopping or jumping to `verify`.
- Risk: milestone state vocabulary becomes too heavy.
  - Mitigation: use the state set only for workflow routing and evidence, not as a broader task-management system.
- Risk: lifecycle-closeout milestones are treated as unfinished implementation.
  - Mitigation: label lifecycle-closeout separately and define that `verify` readiness depends on implementation milestones, not downstream closeout gates.
- Risk: evidence descriptions are mistaken for milestone states.
  - Mitigation: use exactly one milestone state field and treat implementation completion or clean review as evidence descriptions.
- Risk: generated adapter output drifts from canonical skill sources.
  - Mitigation: include generated-output drift checks and regenerate derived output through repository-owned scripts.
- Risk: plans without clear milestone typing block downstream handoff.
  - Mitigation: make ambiguous plan state a review output blocker or required plan update rather than guessing.

## Open questions

None currently blocking.

Resolved direction:

- Use exactly one `Milestone state` field with allowed values `planned`, `implementing`, `review-requested`, `resolution-needed`, and `closed`.
- Treat `implementation-complete` and `review-clean` as evidence descriptions, not state values.
- A clean review without required review-resolution transitions the milestone directly from `review-requested` to `closed`.
- The first implementation should include guidance and static wording checks only, not executable plan-state validation.
- Do not add a standalone `review-resolution` skill for this slice. Put normative rules in the workflow and review-resolution specs, contributor summaries in `docs/workflows.md`, local handoff guidance in `skills/code-review/SKILL.md`, implementation fix-loop guidance in `skills/implement/SKILL.md`, and milestone-loop guidance in `skills/plan/SKILL.md`.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-07 | Treat this as a workflow-governance bug, not a one-off execution mistake. | The incorrect handoff is encoded in the current clean-review rule. | Do nothing; rely on contributor vigilance. |
| 2026-05-07 | Recommend a milestone-aware handoff rule across the workflow contract and affected skills. | The fix needs the source of truth, implementation handoff, code-review output, and plan readiness to agree. | Skill-only patch; validator-first enforcement. |
| 2026-05-07 | Keep `verify` after all implementation milestones are closed or deferred. | This matches the durable learn guidance and prevents `Ready for verify` from skipping unfinished planned implementation work. | Treat every clean milestone review as whole-plan verify readiness. |
| 2026-05-07 | Collapse milestone state to a single field with values `planned`, `implementing`, `review-requested`, `resolution-needed`, and `closed`. | One authoritative state field is easier for agents, contributors, and reviewers to reason about than parallel routing and evidence states. | Keep `implementation-complete` and `review-clean` as state values. |
| 2026-05-07 | Let clean `code-review` close the reviewed milestone directly when no review-resolution is required. | A clean review closes the reviewed milestone, and no useful intermediate `review-clean` state is needed. | Add a separate clean-review state before closeout. |
| 2026-05-07 | Limit the first implementation to guidance and static wording checks. | The policy should settle before executable plan-state parsing is introduced. | Add plan-state validator enforcement immediately. |
| 2026-05-07 | Keep review-resolution guidance local to existing specs, workflow docs, and affected skills. | The first slice does not need a new lifecycle skill. | Add a standalone `review-resolution` skill now. |

## Next artifacts

- `proposal-review`
- spec amendment for milestone-aware autoprogression
- matching test-spec update
- architecture note only if executable routing or plan-state parsing is introduced
- execution plan after proposal/spec/test-spec settlement

## Follow-on artifacts

- `spec`: [Milestone-Aware Review Handoff](../../specs/milestone-aware-review-handoff.md)
- `plan`: [Milestone-Aware Review Handoff Execution Plan](../plans/2026-05-07-milestone-aware-review-handoff.md)

## Readiness

Accepted.

Follow-on spec is approved and the execution plan is active. No proposal-stage blocker remains.
