# Single Source of Workflow State

## Status

approved

## Related Proposal

- [Single Source of Workflow State](../docs/proposals/2026-05-09-single-source-of-workflow-state.md)
- [Workflow-State Projection and Pre-Transition Synchronization Gate](../docs/proposals/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md)

## Goal and context

RigorLoop workflow artifacts currently allow the same live state fact to be restated in several places. That makes active plans, change metadata, review-resolution records, explain-change records, verification evidence, and PR handoff text drift from each other.

This spec defines a single-source workflow-state contract for planned initiatives. The active plan owns the live current handoff. Other artifacts own their narrower evidence and may link or summarize, but they must not become competing sources for the current next stage.

This amendment hardens that contract by defining mechanical projections, pointer-only sections, bounded stale-token detection, and a pre-transition synchronization gate that blocks downstream readiness when live-state surfaces disagree.

## Glossary

- `active plan`: the concrete execution plan under `docs/plans/` that currently owns a planned initiative.
- `current handoff summary`: the active plan section named `Current Handoff Summary`.
- `live state`: current milestone, milestone state, review status, next stage, final closeout readiness, and plan lifecycle status.
- `historical note`: dated evidence of what happened earlier, such as progress, validation, review, or decision history.
- `state-sync check`: the stage-transition check that updates every affected state owner and removes stale live-state wording from touched artifacts.
- `planned initiative`: work represented by an active plan body and the plan index.
- `change metadata`: the compact machine-readable `docs/changes/<change-id>/change.yaml` record.
- `owner`: the authoritative source for one mutable workflow-state or evidence fact.
- `projection`: a compact, mechanically comparable mirror of an owner field.
- `pointer`: a reference to the owner that stores no copy of the current live value.
- `ledger`: append-only or event-oriented history, such as progress history or review-log entries.
- `evidence`: stage-owned proof of a bounded outcome, such as review disposition, validation evidence, final rationale, verify evidence, or PR handoff evidence.
- `state-sync gate`: the binding validation and review point that checks owner, projection, pointer, ledger, evidence, and derived-summary agreement before a downstream readiness claim.
- `live-state surface`: a bounded current-state location that may be parsed for owner or projection values, such as `Current Handoff Summary`, the current milestone-state field, `Readiness`, the current plan-index projection row, and compact live-state metadata fields.
- `stale token`: a prior current-state value that should no longer appear as a live claim after an owner transition.

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

### Example E4: PR handoff does not rewrite plan state after repository integration

Given a PR completes the repo-local lifecycle for a planned initiative
When implementation milestones, required review-resolution, explain-change, verify, and PR handoff are complete
Then the plan and plan index move to `Done` inside the PR before review opens
And repository integration is treated as integration of pre-validated state, not as the routine plan-completion event.

### Example E5: synchronized implementation handoff passes the gate

Given M2 implementation has completed its targeted validation
When the active plan `Current Handoff Summary` records M2 as `review-requested`
And the M2 milestone state projection is `review-requested`
And `docs/plan.md` records the same next stage in the active-plan table row
And `Readiness` points to `Current Handoff Summary`
Then the state-sync gate passes for handoff to `code-review M2`.

### Example E6: stale readiness wording blocks review handoff

Given M2 implementation has completed
When `Current Handoff Summary` says `Next stage: code-review M2`
And the `Readiness` section still says `Ready for implement M2`
Then downstream code-review handoff is blocked until the stale `Readiness` live-state wording is removed or replaced with a pointer.

### Example E7: historical tokens remain valid in ledgers

Given a prior `Progress` entry says M1 was ready for `code-review M1`
And `review-log.md` indexes a prior `code-review-r1`
When the current milestone is M2 and the next stage is `review-resolution M2`
Then bounded stale-token detection permits the historical ledger text
And rejects the same stale values only if they appear in live-state surfaces.

### Example E8: unresolved material findings block downstream readiness

Given a formal review record contains an unresolved material finding
When review-log, review-resolution, or change metadata still shows that finding as open
Then the active plan owner records `Current milestone state: resolution-needed`
And final-closeout readiness remains `not ready`
And a downstream lifecycle gate such as `verify` or PR handoff is blocked.

### Example E9: bounded owner fields use structured values

Given the active plan is handing M2 to code review
When `Current Handoff Summary` is updated
Then `Review status` uses `review-requested; stage=code-review; round=r1`
And final closeout reason uses ordered closed reason codes:

```md
## Current Handoff Summary

- Current milestone: M2. Cross-Surface Validation
- Current milestone state: review-requested
- Latest review evidence: none
- Review status: review-requested; stage=code-review; round=r1
- Remaining in-scope implementation milestones: M2, M3
- Next stage: code-review M2
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — M2 is awaiting review and M3 plus final closeout gates remain.
```

### Example E10: plan-index projection sources are deterministic

Given a plan body contains:

```md
- Plan lifecycle state: active
- Change ID: 2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate
```

And `Current Handoff Summary` contains:

```md
- Next stage: spec revision
```

Then the active plan-index projection uses the plan body for `State` and `Change ID`, and the handoff owner for `Next stage`:

```md
| Plan | State | Next stage | Change ID |
|---|---|---|---|
| [Workflow State Projection](plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md) | active | spec revision | `2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate` |
```

## Requirements

R1. The workflow MUST define exactly one primary owner for each live workflow-state fact used by a planned initiative.

R2. For planned initiatives, the active plan's `Current Handoff Summary` MUST be the authoritative live state block for current milestone, current milestone state, review status, remaining in-scope implementation milestones, next stage, final closeout readiness, and the reason final closeout is or is not ready.

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

R31. Repository integration itself MUST NOT be treated as the normal plan-completion event.

R32. Published skill wording for this contract MUST use portable terms such as project workflow guide, local workflow contract, project validation command, active plan, and change metadata.

R33. Published skill wording MUST NOT expose RigorLoop repository-internal source paths, validator script details, generated adapter internals, or local examples as universal downstream requirements.

R34. The implementation MUST NOT infer live state from arbitrary prose. Structured validation MAY parse exact owner fields, projection fields, review-artifact fields, and bounded live-state surfaces.

R35. When canonical skill wording changes, generated skill mirrors and public adapter outputs MUST be refreshed through the repository-owned generation path and checked for drift.

R36. Public-skill changes MUST run adapter drift check plus adapter validation. In this repository, the expected adapter validation commands are `python scripts/build-adapters.py --version 0.1.1 --check` and `python scripts/validate-adapters.py --version 0.1.1`.

R37. The workflow MUST classify workflow-state and review surfaces as owner, projection, pointer, ledger, or evidence.

R38. A projection MUST be mechanically comparable to its owner field and MUST NOT paraphrase the current live value.

R39. A pointer MUST refer readers to the owner without restating the current live value.

R40. A ledger MAY retain historical stage names, review rounds, milestone states, and next-stage values, but MUST NOT be consulted as owner for the active plan's current next stage.

R41. Evidence MAY support or constrain live state, but MUST NOT own the active plan's current next stage unless this spec assigns that fact to that evidence surface.

R42. `Last reviewed milestone` MUST be derived from formal review evidence and `review-log.md`, not maintained as an independent owner field in `Current Handoff Summary`.

R43. `Current Handoff Summary` MUST use exact required bullet labels for `Current milestone`, `Current milestone state`, `Latest review evidence`, `Review status`, `Remaining in-scope implementation milestones`, `Next stage`, `Final closeout readiness`, and `Reason final closeout is or is not ready`.

R44. A state-sync validator MUST fail closed when required `Current Handoff Summary` fields are missing, duplicated, or unparseable.

R45. `Current milestone state` MUST be one of `planned`, `implementing`, `review-requested`, `resolution-needed`, or `closed`.

R46. `Final closeout readiness` MUST be one of `ready` or `not ready`.

R47. `Review status` MUST use the exact syntax `<status>; stage=<review-stage>; round=<round-token>`.

R47a. `<status>` MUST be exactly one of `not-started`, `not-required`, `review-requested`, `approved`, `changes-requested`, `blocked`, or `inconclusive`.

R47b. `<review-stage>` MUST be exactly one of `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `code-review`, or `none`.

R47c. `<round-token>` MUST be `none` or match `r[1-9][0-9]*`.

R47d. `not-started` and `not-required` MUST use `stage=none; round=none`.

R47e. Every other review status MUST name a formal review stage and a positive round token.

R47f. The structured `Review status` value MUST NOT contain narrative review history. Historical detail belongs in `Progress`, review artifacts, or dated plan history.

R48. `review-requested` review status MUST NOT permit downstream lifecycle gates until the requested review records an approving or otherwise lifecycle-compatible outcome.

R49. `Reason final closeout is or is not ready` MUST use the exact syntax `<reason-code-list> — <bounded detail>`.

R50. Each final-closeout reason code MUST be exactly one of `ready`, `lifecycle-gates-open`, `implementation-milestones-open`, `milestone-review-pending`, `review-findings-open`, `explain-change-pending`, `verify-pending`, `pr-handoff-pending`, `plan-index-sync-pending`, or `external-completion-event-pending`.

R50a. `Final closeout readiness: ready` MUST use the sole final-closeout reason code `ready`.

R50b. `Final closeout readiness: not ready` MUST use one or more non-`ready` reason codes and MUST NOT include `ready`.

R50c. Final-closeout reason codes MUST be unique and MUST appear in the normative order listed in R50.

R51. The active plan `Readiness` section MUST be a pointer to `Current Handoff Summary` for current milestone, next stage, and final-closeout readiness.

R52. The active plan `Readiness` section MUST NOT restate a live current stage, current review round, current milestone state, next stage, or final-closeout readiness value.

R53. `docs/plan.md` active and blocked entries MUST use a Markdown table projection with the exact columns `Plan`, `State`, `Next stage`, and `Change ID`, in that order.

R53a. The `Plan` cell MUST contain a repository-relative Markdown link whose target resolves to the projected plan file. Link text is display-only and MUST be non-empty.

R53b. The projected plan MUST contain exactly one `Plan lifecycle state` field with one of `active`, `blocked`, `done`, or `superseded`.

R53c. The projected plan MUST contain exactly one non-empty `Change ID` field.

R54. The `State` cell MUST equal the plan-body `Plan lifecycle state` field. It MUST NOT be derived from the current milestone state or only from the index section.

R54a. The `Next stage` cell MUST equal the active plan `Current Handoff Summary` `Next stage` value after whitespace normalization.

R54b. The `Change ID` cell MUST equal the plan-body `Change ID` value.

R54c. When governing change metadata exists, top-level `change_id` MUST equal the plan-body `Change ID`; this is a consistency check and does not transfer ownership to `change.yaml`.

R55. The row's index section MUST agree with the plan lifecycle state: `active` in `Active`, `blocked` in `Blocked`, `done` in `Done (recent)` or the plan archive under the existing archive contract, and `superseded` in `Superseded`.

R55a. Active and blocked plans MUST have exactly one live projection row.

R55b. Duplicate plan targets or duplicate `Change ID` values MUST fail.

R56. The current milestone's `Milestone state` projection MUST match `Current Handoff Summary` `Current milestone state`.

R57. Closed previous milestone states MUST remain historical and MUST NOT be rewritten solely to satisfy the current milestone-state projection rule.

R58. A state-sync gate MUST run after stage-owned evidence is updated and before downstream readiness is claimed, review is requested, `verify` runs, or PR handoff starts.

R59. A failed state-sync gate MUST block the next-stage handoff sentence in stage skill output.

R60. `verify` MUST treat a failed state-sync gate as blocking branch readiness for touched, referenced, active, or blocked workflow-state artifacts.

R61. Repository-owned CI validation MUST run the same artifact-lifecycle state-sync checks for PRs that touch active plans, `docs/plan.md`, change metadata, review artifacts, workflow guidance, or the state-sync validator.

R62. Local pre-commit hooks MAY run state-sync checks as contributor convenience, but MUST NOT be the only enforcement point.

R63. On gate failure, an agent MUST either revert its own in-progress owner/projection edits before handoff or record the failure as the current blocker with enough detail for the next agent to rerun the gate and resolve the named inconsistency.

R64. Review-artifact consistency validation MUST compare open material findings across formal review records, `review-log.md`, `review-resolution.md`, and derived change metadata counts when those artifacts exist.

R65. A material finding MUST be treated as open until review-log indexes it, review-resolution records a final disposition, required corrective action or an accepted exception is present, required validation evidence is recorded, and no later review reopens it.

R66. While accepted material findings remain open, `Current milestone state` MUST be `resolution-needed`.

R67. While accepted material findings remain open, `Final closeout readiness` MUST be `not ready`.

R68. `review-requested` MUST NOT be used while required dispositions remain unresolved.

R69. A closed milestone MUST NOT be the current `resolution-needed` milestone.

R70. `change.yaml` MAY store derived review summaries, unresolved finding counts, latest validation state, and artifact pointers.

R71. `change.yaml` MUST NOT directly author the live planned-initiative next stage.

R72. A validator-recognized next-stage-like field in `change.yaml` MUST be treated as derived-only and rejected when it acts as a competing live next-stage owner.

R73. Bounded stale-token detection MUST scan live-state surfaces and MUST exclude ledgers and historical review evidence.

R74. Bounded stale-token detection MUST report stale live-state tokens with path, line, expected owner value, and replacement guidance.

R75. Bounded stale-token detection MUST include stale prior next stage, milestone state, review round, review result, final-readiness value, and retired lifecycle labels when those tokens can be derived from the previous owner state.

R76. Raw repository grep MAY be used as a diagnostic aid, but MUST NOT be authoritative for state-sync gate decisions.

R77. A projection writer, if introduced, MUST default to dry-run.

R78. A projection writer, if introduced, MUST be allowed to edit only `docs/plan.md` projections, the current milestone-state projection, and `Readiness` pointer shape.

R79. A projection writer MUST NOT modify ledgers, review records, review-resolution records, validation evidence, finding dispositions, verify evidence, or PR evidence.

R80. Projection-writer tests MUST include hand-authored golden fixtures for before/after projection edits, not only proof that writer output passes the validator.

R81. The first enforcement scope MUST include active and blocked plans plus any plan whose lifecycle state changes after this contract lands.

R82. Reopening an archived plan back to active MUST count as a lifecycle state change and MUST place that plan under enforcement.

R83. Done and archived plans that are not reopened, touched, generated, or relied on MUST remain historical and MUST NOT be migrated solely for this contract.

R84. The implementation MUST expose a shared state-sync parser/comparison module through `validate-artifact-lifecycle.py` or an equivalent repository-owned lifecycle validator.

R85. Any dedicated state-sync command MUST be a thin wrapper around the same parser and comparison module used by lifecycle validation.

R86. The implementation MUST NOT create independent parsers that can produce conflicting state-sync answers.

R87. A post-rollout success measurement SHOULD track state-drift findings across proposal-review, plan-review, code-review, verify, and PR handoff for active or blocked workflow-state transitions.

## Inputs and Outputs

Inputs:

- active plan body and plan index;
- active plan `Current Handoff Summary`;
- active plan current milestone section;
- formal review records, review-log, and review-resolution artifacts when present;
- change metadata for non-trivial changes;
- explain-change and verify evidence when present;
- PR handoff text when the PR stage is reached;
- canonical skill text and generated skill or adapter output when skill wording changes.
- previous owner state when bounded stale-token detection compares a transition.

Outputs:

- synchronized active plan `Current Handoff Summary`;
- plan-body `Plan lifecycle state` and `Change ID` owner fields;
- milestone state using the allowed state vocabulary;
- `docs/plan.md` table projection for active and blocked plans;
- pointer-only `Readiness` text;
- compact change metadata that points to owning artifacts;
- review-resolution closeout state when findings exist;
- state-sync validation result;
- stale-token diagnostics for bounded live-state surfaces;
- generated skill and adapter output when canonical skill wording changes;
- validation evidence for touched workflow-state surfaces.

## State and Invariants

- Write current state once; link to it everywhere else.
- The active plan owns live planned-initiative handoff state.
- Other artifacts own their scoped evidence and may summarize without becoming competing current-state owners.
- Projections mirror owner fields mechanically and do not paraphrase.
- Pointers store no current live value.
- Ledgers preserve history and are excluded from stale-token rejection.
- Every handoff that changes workflow state updates the live owner before downstream readiness is claimed.
- Every handoff that changes workflow state passes the state-sync gate before downstream readiness is claimed.
- Final closeout is unavailable while in-scope implementation milestones remain open or required review-resolution remains open.
- Branch readiness remains owned by `verify`.
- PR readiness remains owned by `pr`.
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

EB8. If required `Current Handoff Summary` owner fields are missing, duplicated, or unparseable, downstream readiness is blocked until the owner is corrected.

EB9. If the current milestone-state projection disagrees with `Current Handoff Summary`, downstream readiness is blocked until the projection or owner is corrected.

EB10. If the `docs/plan.md` projection row is missing, duplicated, or disagrees with the owner, downstream readiness is blocked until the projection is corrected.

EB11. If `Readiness` restates current live state instead of pointing to `Current Handoff Summary`, downstream readiness is blocked until the section is converted to a pointer or made explicitly historical.

EB12. If review evidence contains unresolved material findings and the owner is not `resolution-needed`, downstream readiness is blocked until owner state and review evidence agree.

EB13. If review evidence contains unresolved material findings and final-closeout readiness is not `not ready`, downstream readiness is blocked until owner state and review evidence agree.

EB14. If a stale token appears in a live-state surface after transition, downstream readiness is blocked until the stale token is removed or replaced.

EB15. If a stale token appears only in `Progress`, `review-log.md`, `review-resolution.md`, or historical review records, the state-sync gate must not fail solely because that historical text remains.

EB16. If an agent partially updates owner or projection fields and the gate fails, the failed transition must be recorded as a blocker or the agent's own partial edits must be reverted before handoff.

## Compatibility and Migration

- Existing historical plans do not require migration solely because this spec is adopted.
- Active and blocked plans must be normalized before first-slice enforcement is enabled.
- Active, blocked, touched, generated, or relied-on workflow artifacts must be normalized when downstream stages rely on them.
- Any plan whose lifecycle state changes after this contract lands must be normalized as part of that transition.
- An archived plan reopened to active must be normalized as part of reopening.
- Existing milestone evidence phrases such as `implementation-complete` or `review-clean` may remain as historical descriptions, but new milestone state fields must use the allowed vocabulary.
- Historical ledgers and completed review records must not be rewritten solely to remove old stage names or review-round tokens.
- Rollout may start with a read-only validator before a projection writer exists.
- If a projection writer is later added, rollback may remove the writer while keeping the read-only validator.
- Rollback may restore previous workflow and skill guidance, but truthfully corrected state should not be made stale again.
- The contract does not change the standard workflow stage order or introduce a new lifecycle stage.

## Observability

- Reviewers must be able to locate current planned-initiative state from the active plan `Current Handoff Summary`.
- Reviewers must be able to compare `Current Handoff Summary`, the current milestone-state projection, and the `docs/plan.md` projection.
- Reviewers must be able to locate review finding closeout from `review-resolution.md` when findings exist.
- Reviewers must be able to inspect compact status and validation traceability from `change.yaml`.
- State-sync validation output must identify owner parse failures, projection mismatches, pointer violations, review-evidence mismatches, and stale live-state tokens with file paths and actionable messages.
- Stale-token diagnostics must identify the expected owner value.
- Validation output must name the checks run for skill validation, adapter drift, adapter validation, review artifacts, change metadata, and diff cleanliness when those surfaces are touched.

## Security and Privacy

- This contract does not introduce new secret, credential, authentication, or authorization handling.
- Workflow artifacts must not add machine-local sensitive paths or private operational details unless they are intentionally part of a reviewed example.
- Published skills must avoid leaking maintainer-only repository internals as downstream user requirements.
- State-sync validation must not require secrets, credentials, external services, or hosted state.
- State-sync diagnostics must not print machine-local sensitive paths unless those paths are part of the reviewed repository artifact text.

## Accessibility and UX

No UI behavior is involved.

## Performance Expectations

- The first implementation slice should avoid broad semantic validation that would make routine workflow edits slow or brittle.
- Static wording checks and generated-output drift checks should remain bounded enough for normal contributor validation.
- Evidence collection should follow bounded-output guidance when reviewing or validating workflow-state artifacts.
- State-sync validation should parse bounded sections and exact fields so runtime is linear in the size of the provided artifacts.
- Normal validator output should summarize pass/fail status and print detailed field dumps only in an explicit verbose mode.

## Edge Cases

EC1. A plan may include a `lifecycle-closeout` milestone for downstream gates, but that milestone does not count as an open implementation milestone for final closeout readiness.

EC2. A direct manual skill invocation may report its local result, but it must not claim the full planned initiative state unless the active plan and required evidence support that claim.

EC3. A clean review with no material findings may settle artifact-locally when no detailed-review trigger applies, but milestone state still changes only through the active plan's state owner.

EC4. A material finding from an isolated review still requires durable review records, but isolation stops automatic downstream handoff.

EC5. A true downstream event may keep a plan active after PR handoff only when the event is named and cannot be made true by the PR tree itself.

EC6. Public adapter packages may use different project paths downstream, so public skill text must describe portable concepts rather than RigorLoop-specific source locations.

EC7. A state-sync check may be recorded in a plan, review-resolution, change metadata, or skill result, but the live next-stage value remains owned by `Current Handoff Summary` for planned initiatives.

EC8. A clean review with no material findings updates review evidence and may close a milestone only when owner state, milestone projection, and plan-index projection are synchronized.

EC9. A `review-requested` owner state after review-resolution means rereview is pending; it does not permit downstream lifecycle gates until the requested rereview records a lifecycle-compatible outcome.

EC10. A plan with `Readiness is not Done` and no current-stage restatement is valid because it is stable explanatory text, not a live-state copy.

EC11. A `change.yaml` field named or shaped like next-stage metadata is valid only when it is derived evidence and not a competing owner of the active plan's next stage.

EC12. A raw `rg` scan may find stale-looking tokens in historical records; that result is diagnostic only until the parser-scoped gate confirms the token is in a live-state surface.

EC13. A projection writer that proposes changes to review evidence, finding dispositions, validation records, verify evidence, or PR evidence must fail before writing.

EC14. A missing optional local pre-commit hook does not weaken enforcement because stage handoff, verify, and CI validation own the binding gate.

## Test-spec coverage notes

The matching test spec must cover these owner-field and projection-source cases:

| Test ID | Scenario | Expected |
| --- | --- | --- |
| `TWSS-OWNER-001` | Valid `review-requested; stage=code-review; round=r1` | pass |
| `TWSS-OWNER-002` | Unknown review status | fail |
| `TWSS-OWNER-003` | `not-started` with a non-`none` stage | fail |
| `TWSS-OWNER-004` | Review status with prose suffix | fail |
| `TWSS-OWNER-005` | Invalid round token `round=1` | fail |
| `TWSS-REASON-001` | `ready` readiness with sole `ready` code | pass |
| `TWSS-REASON-002` | `ready` readiness with `verify-pending` | fail |
| `TWSS-REASON-003` | `not ready` with no reason code | fail |
| `TWSS-REASON-004` | Unknown reason code | fail |
| `TWSS-REASON-005` | Duplicate or incorrectly ordered codes | fail |
| `TWSS-PROJ-001` | State matches plan-body lifecycle state | pass |
| `TWSS-PROJ-002` | State incorrectly uses milestone state | fail |
| `TWSS-PROJ-003` | Next stage differs from owner | fail |
| `TWSS-PROJ-004` | Change ID differs from plan body | fail |
| `TWSS-PROJ-005` | `change.yaml.change_id` differs from plan body | fail |
| `TWSS-PROJ-006` | Active plan row appears under Blocked | fail |
| `TWSS-PROJ-007` | Duplicate plan link or change ID | fail |
| `TWSS-PROJ-008` | Missing plan-body Change ID | fail |

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
- Inferring live state from arbitrary narrative prose.
- Making raw repository grep authoritative for lifecycle-state decisions.
- Making `change.yaml` the live next-stage owner.
- Automatically rewriting ledgers, review findings, review dispositions, validation evidence, verify evidence, or PR evidence.
- Requiring local pre-commit hooks as the sole enforcement mechanism.
- Adding hosted workflow-state storage or an external control plane.

## Acceptance criteria

- A contributor can identify the current milestone, milestone state, review status, next stage, and final closeout readiness from one active-plan section.
- A reviewer can tell that `Readiness`, `Progress`, `Validation notes`, `review-resolution.md`, `change.yaml`, and `explain-change.md` do not own competing live next-stage claims.
- A reviewer can tell that milestone state uses only `planned`, `implementing`, `review-requested`, `resolution-needed`, or `closed`.
- A reviewer can tell that final closeout is blocked while implementation milestones or required review-resolution remain open.
- A reviewer can verify that a state-changing handoff performed a state-sync check across the active plan, review-resolution, review-log, change metadata, and plan index when those surfaces are affected.
- A validator can parse required `Current Handoff Summary` fields exactly once and fail closed on missing, duplicated, or unparseable fields.
- A validator can compare current milestone state against the active milestone-state projection.
- A validator can compare `docs/plan.md` active and blocked table projections against the active plan owner.
- A validator can reject `Readiness` sections that restate current live state.
- A validator can allow historical tokens in ledgers while rejecting the same stale tokens in live-state surfaces.
- A validator can reject downstream-ready owner states while accepted material findings remain open.
- A validator can reject directly authored live next-stage authority in `change.yaml`.
- A validator can prove a `review-requested` rereview-pending state does not route to downstream lifecycle gates without lifecycle-compatible rereview evidence.
- A projection writer, if shipped later, is constrained by golden fixtures and cannot modify ledger or evidence files.
- A reviewer can verify that published skill wording uses portable concepts and does not present RigorLoop internal paths as universal downstream requirements.
- A reviewer can verify that generated skill mirrors and adapter outputs are refreshed and validated when canonical skills change.
- The proposal's prior adapter-validation finding remains closed because the spec requires runnable versioned adapter validation for this repository.
- AC-WSS-017: `Review status` has one exact parseable grammar.
- AC-WSS-018: Review status, stage, and round use closed vocabularies.
- AC-WSS-019: Review history is not embedded in the owner field.
- AC-WSS-020: Final-closeout reason uses closed reason codes.
- AC-WSS-021: Readiness and reason codes are mutually consistent.
- AC-WSS-022: Every `docs/plan.md` projection cell has one named authoritative source.
- AC-WSS-023: Plan lifecycle state is distinguished from milestone state.
- AC-WSS-024: Change ID is owned by an exact plan-body field.
- AC-WSS-025: `change.yaml.change_id` is a consistency check, not a next-stage or plan-state owner.
- AC-WSS-026: Active and blocked plans have exactly one matching index projection.
- AC-WSS-027: Duplicate plan rows and conflicting change IDs fail.

## Open Questions

None.

## Next Artifacts

- execution plan
- test spec

## Follow-on Artifacts

None yet

## Readiness

Approved by spec-review-r2. Ready for downstream planning and test-spec authoring when requested; no architecture, implementation, verification, branch-readiness, or PR-readiness handoff is claimed by this spec approval.
