# Explain Change: Workflow-State Projection and Pre-Transition Synchronization Gate

Change ID: 2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate
Status: explain-change complete
Date: 2026-06-23

## Summary

This change hardens the existing Single Source of Workflow State contract. It keeps the active plan `Current Handoff Summary` as the live planned-initiative state owner, turns remaining repeated current-state values into parseable projections or pointers, and adds validation so contradictory owner, projection, review, and change-metadata surfaces fail before downstream readiness is claimed.

The implementation adds exact workflow-state owner parsing, `docs/plan.md` active/blocked table projection validation, current milestone-state projection checks, pointer-only `Readiness` checks, review evidence and `change.yaml` consistency checks, binding workflow guidance, active/blocked audit handling, and behavior-preservation evidence.

It does not claim final verification, branch readiness, PR readiness, or hosted CI status. Those remain owned by `verify` and `pr`.

## Problem

The prior Single Source of Workflow State work established the owner, but enforcement was incomplete. Live lifecycle facts could still be manually copied into `docs/plan.md`, plan milestone sections, `Readiness`, review artifacts, and change metadata. That left room for stale next-stage, review-round, milestone-state, and finding-closeout claims to survive until a reviewer noticed drift.

The accepted proposal framed the problem as an artifact-role and tooling gap rather than a contributor-discipline issue: write live state once, project it mechanically, preserve ledgers as history, and validate synchronization before handoff.

## Decision Trail

| Decision point | Outcome | Source |
| --- | --- | --- |
| Proposal | Chose owner/projection/pointer/ledger/evidence roles and bounded validation instead of manual sync or broad prose inference. | `docs/proposals/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md` |
| Spec | Added requirements R1-R87 for owner fields, projections, review-evidence consistency, stale-token boundaries, enforcement scope, and shared parser ownership. | `specs/single-source-of-workflow-state.md` |
| Spec review | WSS-SR1 and WSS-SR2 required deterministic owner-field syntax and projection sources; both were accepted and resolved before implementation. | `review-resolution.md` |
| Architecture | Kept workflow-state synchronization inside artifact-lifecycle validation, with no service, storage, API, deployment, or new parser authority. | `docs/architecture/system/architecture.md` |
| Plan | Split implementation into M1-M5 after plan-review moved test-spec authoring out of M1. | `docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md` |
| Test spec | Mapped owner parsing, plan-index projection, readiness pointer, review evidence, stale-token, enforcement-scope, and behavior-preservation cases to T12-T22. | `specs/single-source-of-workflow-state.test.md` |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- |
| `specs/single-source-of-workflow-state.md` | Amended the contract with role taxonomy, exact owner fields, closed vocabularies, projection-source rules, state-sync gates, review consistency, stale-token scope, and enforcement scope. | Make the existing owner model deterministic and enforceable. | Proposal goals; WSS-SR1; WSS-SR2 | Spec-review R2; T12-T22 |
| `specs/single-source-of-workflow-state.test.md` | Added traceable tests T12-T22. | Keep every new contract rule testable before implementation. | R37-R87, AC-WSS-001 through AC-WSS-027 | Test-spec approval; validator suites |
| `docs/architecture/system/architecture.md` | Recorded workflow-state synchronization as bounded lifecycle validation and documented no new ADR requirement. | Preserve the existing architecture boundary. | Architecture review R1 | Architecture review and lifecycle validation |
| `scripts/lifecycle_state_sync.py` | Added shared parsing and comparison helpers for handoff owner fields, plan state, plan-index projections, index-to-owner resolution, milestone-state projection, `Readiness`, review-summary constraints, and change-metadata association by key. | Centralize state-sync semantics so all lifecycle validation paths agree. | R43-R63, R73-R86 | `test_workflow_state_*`, multi-active tests, all-active audit |
| `scripts/artifact_lifecycle_validation.py` | Composed workflow-state validation into artifact-lifecycle validation and made `docs/plan.md` in scope resolve linked owners before comparison. | Ensure any in-scope owner or projection surface drives synchronization. | R58-R61, R84-R86; WSS-CR1 | `test_workflow_state_index_only_catches_next_stage_drift` |
| `scripts/review_artifact_validation.py` | Added `finding_closure_state()` and routed review summary plus closeout-mode validation through one positive-evidence predicate. | Keep material findings open until all required review evidence is present. | R64-R65b; WSS-CR2; WSS-CR3 | predicate parity and closeout evidence tests |
| `scripts/validate-change-metadata.py` | Checked review counts against review-artifact summaries and rejected next-stage-like metadata. | Keep `change.yaml` derived-only. | R9, R70-R72 | review-summary metadata tests |
| Validator tests | Added owner-field, reason-code, plan-index, readiness, review-evidence, index-only, legacy-plan, dedupe, and multi-active fixtures. | Prove live-state drift fails and historical or legacy cases remain compatible. | T12-T19, T21-T22 | full lifecycle, review, and metadata test suites |
| Workflow docs and skills | Added binding state-sync gate wording to workflow and stage guidance while keeping public skill wording portable. | Move enforcement from advice to stage precondition. | R58-R63, R32-R33 | `test_workflow_state_sync_gate_is_binding_guidance`, skill validation/build checks |
| `docs/plan.md` and active plan bodies | Normalized active/blocked projection rows and synchronized plan-body `Change ID` fields where active enforcement required it. | Make the live index mechanically comparable and satisfy active/blocked scope. | R53-R55b, R81 | all-active lifecycle audit |
| Change-local artifacts | Recorded proposal, reviews, review-resolution, change metadata, behavior preservation, and this explanation. | Preserve durable traceability instead of chat-only state. | Workflow contract and explain-change skill | review-artifact and change-metadata validation |

## Tests Added Or Changed

| Test area | What it proves |
| --- | --- |
| T12 owner-field parsing | Exact `Current Handoff Summary` labels, closed review-status grammar, and fail-closed parsing. |
| T13 final-closeout reasons | Readiness and reason-code consistency with normative ordering. |
| T14 plan-index projection | `docs/plan.md` cells match named authoritative sources and duplicates or wrong sections fail. |
| T15 readiness and milestone projections | `Readiness` remains a pointer and current milestone state matches the owner. |
| T16 binding gate | Partial transitions fail before downstream handoff, and the validator path is shared. |
| T17 review evidence | Material findings remain open until the shared closure predicate sees positive evidence across log, resolution, validation, and later reviews. |
| T18 stale-token boundary | Live-surface stale tokens fail while historical ledgers remain valid. |
| T19 active/blocked enforcement | Active and blocked plan scope is enforced without migrating unrelated historical plans. |
| T20 writer boundary | No projection writer ships in this slice; future writer behavior is constrained. |
| T21 parser ownership | Artifact-lifecycle validation uses the shared parser/comparison helper. |
| T22 behavior preservation | The full slice preserves ownership boundaries while synchronized transitions pass and incomplete transitions fail. |

## Validation Evidence Available Before Final Verify

Validation recorded during implementation and code review includes:

- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/test-review-artifact-validator.py`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/test-build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
- `python scripts/validate-guide-system.py`
- `python scripts/test-select-validation.py`
- explicit-path artifact lifecycle validation over active plan, plan index, spec, test spec, architecture, change metadata, review log, review-resolution, and review records
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
- all-active explicit-path lifecycle audit over `docs/plan.md` and active plan bodies
- `git diff --check` over touched workflow-state surfaces

Hosted CI, final verification, branch readiness, PR-body readiness, and PR-open readiness are not claimed here.

## Review Resolution Summary

Review-resolution is recorded at `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md`.

Material findings:

- Total material findings: 7
- Accepted and resolved: 7
- Open: 0
- Needs decision: 0

Resolved findings: WSS-SR1, WSS-SR2, WSS-PLAN1, WSS-CR1, WSS-CR2, WSS-CR3, and WSS-CR4.

Clean review receipts approved M1 R2, M2 R1, M3 R3, M4 R2, and M5 R1.

## Alternatives Rejected

| Alternative | Why rejected |
| --- | --- |
| Keep manual synchronization with clearer guidance | This repeats the drift failure mode and leaves review as the first reliable synchronization check. |
| Parse arbitrary prose across the repository | It risks false positives against historical ledgers and encourages validators to infer authority from narrative text. |
| Make `docs/plan.md` or `change.yaml` the live next-stage owner | That would create a competing owner instead of preserving `Current Handoff Summary`. |
| Ship a projection writer in the first slice | The validator contract needed to stabilize first. |
| Use raw repository grep as the gate | Raw grep cannot distinguish live surfaces from historical review and progress text. |
| Add a new service, database, or external control plane | The approved architecture keeps enforcement inside repository artifacts and lifecycle validation. |
| Migrate all historical plans | The risk is active/blocked lifecycle drift; historical plans remain evidence unless reopened or touched. |

## Scope Control

The implementation preserves the approved non-goals: no workflow stage order change, no new live-state owner outside `Current Handoff Summary`, no broad prose inference, no automatic rewriting of review evidence or finding dispositions, no branch-readiness or PR-readiness inference from plan state, no hosted state service, no first-slice projection writer, no historical-plan migration solely for the new format, and no hand-edited generated public adapter output.

## Risks And Follow-Ups

- The post-rollout success metric should track workflow-state drift findings across the next 10 formal reviews or 30 days.
- Future projection-writer work must preserve the dry-run default, writer scope limits, and hand-authored golden fixtures from R77-R80.
- Any new derived readiness, closure, or drift boolean should reuse a shared predicate and fail closed on missing, ambiguous, or unparseable evidence.
- Final `verify` still needs to run the required validation set and own branch-readiness evidence.
- PR handoff still needs to summarize the verified change without becoming the live-state owner.

## Readiness

Explain-change is complete. The active plan should now route to `verify`.

This artifact does not claim final verification, branch readiness, PR readiness, hosted CI success, or merge readiness.
