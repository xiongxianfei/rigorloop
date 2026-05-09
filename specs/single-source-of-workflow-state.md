# Single Source of Workflow State

## Status

approved

## Related Proposal

- [Single Source of Workflow State](../docs/proposals/2026-05-09-single-source-of-workflow-state.md)

## Goal and context

RigorLoop workflow artifacts currently allow the same live state fact to be restated in several places. That makes active plans, change metadata, review-resolution records, explain-change records, verification evidence, and PR handoff text drift from each other.

This spec defines a single-source workflow-state contract for planned initiatives. The active plan owns the live current handoff. Other artifacts own their narrower evidence and may link or summarize, but they must not become competing sources for the current next stage.

## Glossary

- `active plan`: the concrete execution plan under `docs/plans/` that currently owns a planned initiative.
- `current handoff summary`: the active plan section named `Current Handoff Summary`.
- `live state`: current milestone, milestone state, review status, next stage, final closeout readiness, and plan lifecycle status.
- `historical note`: dated evidence of what happened earlier, such as progress, validation, review, or decision history.
- `state-sync check`: the stage-transition check that updates every affected state owner and removes stale live-state wording from touched artifacts.
- `planned initiative`: work represented by an active plan body and the plan index.
- `change metadata`: the compact machine-readable `docs/changes/<change-id>/change.yaml` record.

## Examples First

### Example E1: active plan owns the next stage

Given an active milestone-based plan is in M2 implementation
When M2 targeted validation passes and implementation hands off for review
Then the active plan's `Current Handoff Summary` records M2 as `review-requested` and names `code-review` as the next stage
And `Readiness` points to `Current Handoff Summary` instead of restating a separate next-stage sentence.

### Example E2: review-resolution owns finding closeout, not plan readiness

Given code-review finds a material issue in M2
When review-resolution is opened for that finding
Then `review-resolution.md` records finding disposition and closeout status
And the active plan records the milestone as `resolution-needed`
And `review-resolution.md` does not independently claim the next implementation or verification stage.

### Example E3: final closeout starts only after implementation milestones close

Given a planned initiative has M1 through M4 as in-scope implementation milestones
When M1, M2, M3, and M4 have each passed their milestone review loop
And required review-resolution is closed
Then final lifecycle closeout may proceed through final rationale, verification, and PR handoff
And the plan does not claim final closeout readiness while any implementation milestone is still `planned`, `implementing`, `review-requested`, or `resolution-needed`.

### Example E4: PR handoff does not rewrite plan state after merge

Given a PR completes the repo-local lifecycle for a planned initiative
When implementation milestones, required review-resolution, explain-change, verify, and PR handoff are complete
Then the plan and plan index move to `Done` inside the PR before review opens
And merge is treated as integration of pre-validated state, not as the routine plan-completion event.

## Requirements

R1. The workflow MUST define exactly one primary owner for each live workflow-state fact used by a planned initiative.

R2. For planned initiatives, the active plan's `Current Handoff Summary` MUST be the authoritative live state block for current milestone, current milestone state, last reviewed milestone, review status, remaining in-scope implementation milestones, next stage, final closeout readiness, and the reason final closeout is or is not ready.

R3. Active plan sections outside `Current Handoff Summary` MUST NOT independently state live next-stage claims unless the statement is explicitly historical.

R4. The active plan `Readiness` section MUST point to `Current Handoff Summary` for current live state instead of duplicating the current next stage.

R5. `Progress` MUST record dated history rather than current next-stage authority.

R6. `Decision log` MUST record decisions rather than current next-stage authority.

R7. `Validation notes` MUST record validation evidence rather than current next-stage authority.

R8. `Outcome`, `Retrospective`, or equivalent final sections MUST be final-only or explicitly historical, and MUST NOT conflict with `Current Handoff Summary`.

R9. Change metadata MUST store compact status, unresolved finding counts, validation records, and artifact pointers, but MUST NOT be the authoritative owner of the current next stage.

R10. `review-resolution.md` MUST own material-finding disposition and closeout status when review-resolution is triggered, but MUST NOT own plan readiness or current next-stage routing.

R11. `review-log.md` MUST index formal review events and open findings, but MUST NOT own the active plan's current next stage.

R12. `explain-change.md` MUST own final change rationale when present, but MUST NOT claim final verification, branch readiness, PR readiness, or current plan next-stage authority.

R13. Final `verify` output or a verify report MUST own final validation proof and branch-readiness evidence, but MUST NOT be the PR body or the active plan's current-state owner.

R14. PR handoff text MAY summarize current readiness for reviewers, but MUST NOT back-propagate new live state into the active plan except through final lifecycle closeout.

R15. Planned implementation milestone state MUST use one of these values: `planned`, `implementing`, `review-requested`, `resolution-needed`, or `closed`.

R16. Planned implementation milestone state MUST NOT use `implementation-complete` or `review-clean` as state values. Those phrases MAY appear only as evidence descriptions.

R17. Milestone state transitions MUST follow the defined lifecycle: `planned -> implementing`, `implementing -> review-requested`, `review-requested -> closed`, `review-requested -> resolution-needed`, `resolution-needed -> review-requested`, or `resolution-needed -> closed`.

R18. A clean non-final milestone review MUST route to the next in-scope implementation milestone when one remains.

R19. A clean final implementation milestone review MUST route to final closeout only when all in-scope implementation milestones are `closed` and required review-resolution is closed.

R20. A milestone with unresolved review findings MUST be `resolution-needed` until the accepted findings are fixed or explicitly dispositioned.

R21. Every workflow stage transition that changes live state MUST perform a state-sync check.

R22. A state-sync check MUST update the active plan `Current Handoff Summary` when the planned initiative's current milestone, milestone state, review status, remaining implementation milestones, next stage, or final closeout readiness changes.

R23. A state-sync check MUST update the current milestone state when the milestone state changes.

R24. A state-sync check MUST update `review-resolution.md` closeout status when required review-resolution findings change.

R25. A state-sync check MUST update `review-log.md` open findings when formal review records change.

R26. A state-sync check MUST update `change.yaml` compact review/status summary when change metadata is touched or the unresolved finding count changes.

R27. A state-sync check MUST update `docs/plan.md` when plan lifecycle state changes.

R28. A state-sync check MUST remove or correct stale live next-stage wording in touched artifacts before downstream readiness is claimed.

R29. Plans SHOULD move to `Done` inside the PR when implementation milestones are closed, required review-resolution is closed, explain-change is complete, verify is complete, and PR handoff is complete.

R30. Plans MUST remain `Active` when completion depends on a true downstream event such as release, deploy, package publication, external migration, or observed hosted result.

R31. Merge itself MUST NOT be treated as the normal plan-completion event.

R32. Published skill wording for this contract MUST use portable terms such as project workflow guide, local workflow contract, project validation command, active plan, and change metadata.

R33. Published skill wording MUST NOT expose RigorLoop repository-internal source paths, validator script details, generated adapter internals, or local examples as universal downstream requirements.

R34. The first implementation slice SHOULD use guidance and static wording checks rather than broad semantic plan-state validation.

R35. When canonical skill wording changes, generated skill mirrors and public adapter outputs MUST be refreshed through the repository-owned generation path and checked for drift.

R36. Public-skill changes MUST run adapter drift check plus adapter validation. In this repository, the expected adapter validation commands are `python scripts/build-adapters.py --version 0.1.1 --check` and `python scripts/validate-adapters.py --version 0.1.1`.

## Inputs and Outputs

Inputs:

- active plan body and plan index;
- formal review records, review-log, and review-resolution artifacts when present;
- change metadata for non-trivial changes;
- explain-change and verify evidence when present;
- PR handoff text when the PR stage is reached;
- canonical skill text and generated skill or adapter output when skill wording changes.

Outputs:

- synchronized active plan `Current Handoff Summary`;
- milestone state using the allowed state vocabulary;
- compact change metadata that points to owning artifacts;
- review-resolution closeout state when findings exist;
- generated skill and adapter output when canonical skill wording changes;
- validation evidence for touched workflow-state surfaces.

## State and Invariants

- Write current state once; link to it everywhere else.
- The active plan owns live planned-initiative handoff state.
- Other artifacts own their scoped evidence and may summarize without becoming competing current-state owners.
- Every handoff that changes workflow state updates the live owner before downstream readiness is claimed.
- Final closeout is unavailable while in-scope implementation milestones remain open or required review-resolution remains open.
- The standard workflow order remains unchanged.
- `explain-change -> verify -> pr` remains the final closeout order.

## Error and Boundary Behavior

EB1. If `Current Handoff Summary` and another touched artifact disagree about the current next stage, downstream readiness MUST be considered blocked until state-sync resolves the contradiction.

EB2. If an active plan has no `Current Handoff Summary` after this contract applies, the next plan or implementation update MUST add one before claiming milestone or final closeout readiness.

EB3. If a touched `Readiness` section duplicates stale next-stage wording, the stage MUST revise it to point to `Current Handoff Summary` or make it explicitly historical.

EB4. If change metadata shows a stale unresolved finding count, downstream handoff MUST stop until the compact review/status summary matches the review artifacts.

EB5. If review-resolution is open, final `explain-change`, `verify`, and `pr` MUST stop unless a higher-priority artifact explicitly defers that review-resolution with an accepted disposition.

EB6. If the plan lifecycle state changes but `docs/plan.md` and the plan body disagree, `verify` MUST treat branch readiness as blocked for that planned initiative.

EB7. If published skill text contains repository-internal paths or validator commands as universal public requirements, the public-skill portability check MUST fail or produce a material review finding.

## Compatibility and Migration

- Existing historical plans do not require migration solely because this spec is adopted.
- Active, touched, generated, or relied-on workflow artifacts must be normalized when downstream stages rely on them.
- Existing milestone evidence phrases such as `implementation-complete` or `review-clean` may remain as historical descriptions, but new milestone state fields must use the allowed vocabulary.
- Rollback may restore previous workflow and skill guidance, but truthfully corrected state should not be made stale again.
- The contract does not change the standard workflow stage order or introduce a new lifecycle stage.

## Observability

- Reviewers must be able to locate current planned-initiative state from the active plan `Current Handoff Summary`.
- Reviewers must be able to locate review finding closeout from `review-resolution.md` when findings exist.
- Reviewers must be able to inspect compact status and validation traceability from `change.yaml`.
- Validation output must name the checks run for skill validation, adapter drift, adapter validation, review artifacts, change metadata, and diff cleanliness when those surfaces are touched.

## Security and Privacy

- This contract does not introduce new secret, credential, authentication, or authorization handling.
- Workflow artifacts must not add machine-local sensitive paths or private operational details unless they are intentionally part of a reviewed example.
- Published skills must avoid leaking maintainer-only repository internals as downstream user requirements.

## Accessibility and UX

No UI behavior is involved.

## Performance Expectations

- The first implementation slice should avoid broad semantic validation that would make routine workflow edits slow or brittle.
- Static wording checks and generated-output drift checks should remain bounded enough for normal contributor validation.
- Evidence collection should follow bounded-output guidance when reviewing or validating workflow-state artifacts.

## Edge Cases

EC1. A plan may include a `lifecycle-closeout` milestone for downstream gates, but that milestone does not count as an open implementation milestone for final closeout readiness.

EC2. A direct manual skill invocation may report its local result, but it must not claim the full planned initiative state unless the active plan and required evidence support that claim.

EC3. A clean review with no material findings may settle artifact-locally when no detailed-review trigger applies, but milestone state still changes only through the active plan's state owner.

EC4. A material finding from an isolated review still requires durable review records, but isolation stops automatic downstream handoff.

EC5. A true downstream event may keep a plan active after PR handoff only when the event is named and cannot be made true by the PR tree itself.

EC6. Public adapter packages may use different project paths downstream, so public skill text must describe portable concepts rather than RigorLoop-specific source locations.

EC7. A state-sync check may be recorded in a plan, review-resolution, change metadata, or skill result, but the live next-stage value remains owned by `Current Handoff Summary` for planned initiatives.

## Non-goals

- Redesigning the standard workflow stage order.
- Reintroducing a fast lane or small-change lane.
- Creating a new lifecycle stage.
- Making every artifact carry a full workflow-state table.
- Making `change.yaml` a long-form state tracker.
- Making `review-resolution.md` own plan readiness.
- Making `verify` own PR readiness.
- Adding broad semantic plan-state validation in the first implementation slice.
- Migrating historical plans that are not active, touched, generated, or relied on.

## Acceptance criteria

- A contributor can identify the current milestone, milestone state, review status, next stage, and final closeout readiness from one active-plan section.
- A reviewer can tell that `Readiness`, `Progress`, `Validation notes`, `review-resolution.md`, `change.yaml`, and `explain-change.md` do not own competing live next-stage claims.
- A reviewer can tell that milestone state uses only `planned`, `implementing`, `review-requested`, `resolution-needed`, or `closed`.
- A reviewer can tell that final closeout is blocked while implementation milestones or required review-resolution remain open.
- A reviewer can verify that a state-changing handoff performed a state-sync check across the active plan, review-resolution, review-log, change metadata, and plan index when those surfaces are affected.
- A reviewer can verify that published skill wording uses portable concepts and does not present RigorLoop internal paths as universal downstream requirements.
- A reviewer can verify that generated skill mirrors and adapter outputs are refreshed and validated when canonical skills change.
- The proposal's prior adapter-validation finding remains closed because the spec requires runnable versioned adapter validation for this repository.

## Open Questions

None.

## Next Artifacts

- spec-review
- architecture no-impact rationale or architecture update if review identifies architecture impact
- execution plan
- test spec

## Follow-on Artifacts

- Plan: `docs/plans/2026-05-09-single-source-of-workflow-state.md`

## Readiness

Approved after spec-review. Ready for architecture/no-impact assessment and plan-review.
