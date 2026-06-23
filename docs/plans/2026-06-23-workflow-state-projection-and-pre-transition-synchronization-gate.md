# Workflow-State Projection and Pre-Transition Synchronization Gate Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate
- Owner: agent
- Start date: 2026-06-23
- Last updated: 2026-06-23
- Related issue or PR: none yet
- Supersedes: none

## Goal

Implement the approved workflow-state projection and pre-transition synchronization contract so planned-initiative live state has one owner, current-state projections are mechanically comparable, review evidence constrains incompatible transitions, and state-sync validation fails before downstream readiness is claimed.

## Why now

The Single Source of Workflow State work settled ownership, but current workflow surfaces can still drift because projections, review summaries, and readiness text are manually synchronized. The approved follow-up spec makes the remaining mirrors deterministic and requires a pre-transition state-sync gate.

## Source artifacts

- Proposal: [Workflow-State Projection and Pre-Transition Synchronization Gate](../proposals/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md)
- Spec: [Single Source of Workflow State](../../specs/single-source-of-workflow-state.md)
- Architecture: [System Architecture](../architecture/system/architecture.md)
- Change metadata: [change.yaml](../changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml)
- Proposal review: [proposal-review-r1](../changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/proposal-review-r1.md)
- Spec reviews: [spec-review-r1](../changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/spec-review-r1.md), [spec-review-r2](../changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/spec-review-r2.md)
- Architecture review: [architecture-review-r1](../changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/architecture-review-r1.md)
- Review resolution: [review-resolution.md](../changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md)
- Review log: [review-log.md](../changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md)

## Scope

### In scope

- Consume the matching test specification for workflow-state synchronization requirements and fixtures before implementation starts.
- Implement exact `Current Handoff Summary` parsing for owner fields, review status grammar, final-closeout reason codes, and readiness pointer enforcement.
- Implement active and blocked `docs/plan.md` projection validation for `Plan`, `State`, `Next stage`, and `Change ID`.
- Implement current milestone-state projection validation and bounded stale-token checks for live-state surfaces.
- Implement review evidence and change metadata consistency checks that block incompatible owner state while material findings remain open.
- Update workflow and directly affected skill guidance so pre-transition state-sync validation is a binding stage precondition.
- Audit and normalize active and blocked plan surfaces required by the approved contract.
- Record behavior-preservation evidence and final lifecycle closeout evidence.

### Out of scope

- Do not migrate historical done, archived, or superseded plans solely to the new live projection format.
- Do not add a projection writer in the first implementation slice.
- Do not change workflow stage order.
- Do not move live next-stage ownership to `docs/plan.md`, `change.yaml`, review logs, review resolutions, verify, or PR artifacts.
- Do not hand-edit generated public adapter output.
- Do not introduce a hosted workflow service, database, or external control plane.

## Constraints

- `Current Handoff Summary` remains the sole owner of live planned-initiative state named by the approved spec.
- `docs/plan.md`, the current milestone-state field, and `Readiness` are projections or pointers; they must not become independent narrative owners.
- Review logs and progress history remain append-only ledgers and may retain historical stage tokens.
- Review-resolution owns material-finding disposition evidence, not live next-stage routing.
- `change.yaml` compact fields are derived consistency checks and must not own current next stage.
- Stage guidance must block downstream handoff output when state-sync validation fails.
- The validator must parse bounded fields and sections rather than infer lifecycle state from arbitrary prose.

## Requirements covered

- R1-R12: M4 updates role guidance and active/blocked plan surfaces without changing ownership.
- R13-R21: M2 and M4 enforce transition synchronization across owner, projections, ledgers, evidence, and metadata.
- R22-R41: M2 and M3 implement deterministic owner/projection/pointer/ledger/evidence validation boundaries.
- R42-R57: M1 and M2 cover exact owner-field syntax, final-closeout reason codes, plan-index projection sources, and milestone-state projection validation.
- R58-R63: M2 and M4 wire state-sync validation into stage preconditions, verify, and CI guidance.
- R64-R75: M3 implements review artifact and change metadata consistency for open material findings.
- R76-R81: M2 and M5 preserve writer boundaries and behavior-preservation evidence.
- AC-WSS-001 through AC-WSS-027: covered across M1 through M5.

## Current Handoff Summary

- Current milestone: M4. Workflow Guidance, Active Audit, and Projection Normalization
- Current milestone state: review-requested
- Latest review evidence: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m4-r1.md
- Review status: review-requested; stage=code-review; round=r2
- Remaining in-scope implementation milestones: M4, M5
- Next stage: code-review M4
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — WSS-CR4 resolution is ready for code-review M4 R2, M5 remains open, and final closeout gates remain.

## Milestones

### M1. Parser Fixture Harness and Owner-State Tests

- Milestone state: closed
- Goal: Consume the completed test spec and add the first failing or fixture-backed validator tests plus parser scaffolding for owner-field and projection synchronization.
- Requirements: R42-R57, R64-R75, R76-R81, AC-WSS-017 through AC-WSS-027
- Files/components likely touched:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-change-metadata-validator.py`
  - lifecycle validator fixtures under `tests/fixtures/`
- Dependencies:
  - Approved spec and architecture.
  - Revised plan must pass plan-review.
  - Matching `test-spec` stage must complete `specs/single-source-of-workflow-state.test.md` before M1 implementation starts.
- Tests to add/update:
  - Implement the approved `TWSS-OWNER-*`, `TWSS-REASON-*`, and `TWSS-PROJ-*` fixture cases from the completed test spec.
  - stale-token boundary fixture pair for live surfaces versus historical ledgers
  - positive fixture for valid bounded owner-field text
  - review consistency fixtures for open, resolved, and reopened material findings
- Implementation steps:
  - Read the completed test spec and preserve its requirement-to-test mapping.
  - Add fixture-backed failing tests for plan lifecycle state versus current milestone state, active/blocked plan-index projection sources, bounded owner-field syntax, readiness pointer enforcement, and stale-token boundaries.
  - Add parser scaffolding only as needed to make the first owner-field and projection fixture set executable through artifact-lifecycle validation.
  - Keep review consistency fixture implementation bounded to test cases needed by the completed test spec; broader consistency enforcement remains in M3.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/single-source-of-workflow-state.test.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/plan.md`
  - `git diff --check -- scripts/lifecycle_state_sync.py scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py scripts/test-review-artifact-validator.py scripts/test-change-metadata-validator.py tests/fixtures docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md docs/plan.md`
- Expected observable result: The completed test spec is represented by executable failing or passing fixtures, and the first parser scaffolding can detect owner-field and projection drift through artifact-lifecycle validation.
- Commit message: `M1: add workflow-state sync parser fixtures`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - validation notes updated
  - hand off to code-review for M1
  - material findings resolved or explicitly dispositioned before M2 starts

### M2. Parser and Lifecycle State-Sync Validator

- Milestone state: closed
- Goal: Implement reusable workflow-state parsing and state-sync validation through the artifact-lifecycle validation boundary.
- Requirements: R22-R63, R76-R81, AC-WSS-001 through AC-WSS-006, AC-WSS-009 through AC-WSS-027
- Files/components likely touched:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - lifecycle validator fixtures under `tests/fixtures/`
- Dependencies:
  - Completed test spec and M1 parser fixture harness.
  - Approved architecture that keeps the state-sync checks inside artifact-lifecycle validation.
- Tests to add/update:
  - Owner parse success and failure tests for required `Current Handoff Summary` fields.
  - Readiness pointer rejection for current-stage, review-round, milestone-state, next-stage, and final-readiness restatements.
  - Active and blocked `docs/plan.md` table projection checks.
  - Current milestone-state projection checks.
  - Parser-scoped stale-token detection tests with historical-ledger exclusions.
- Implementation steps:
  - Add a reusable parser module for `Current Handoff Summary`, milestone-state blocks, readiness sections, and plan-index table projections.
  - Compose the parser through `validate-artifact-lifecycle.py` without creating a competing authoritative command.
  - Fail closed on missing, duplicate, or unparseable required owner fields.
  - Compare active/blocked plan-index projection rows against plan-body lifecycle state, plan-body `Change ID`, and owner `Next stage`.
  - Reject `Readiness` current-state restatements and live-surface stale tokens while allowing ledgers to preserve history.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md`
  - `git diff --check -- scripts/lifecycle_state_sync.py scripts/artifact_lifecycle_validation.py scripts/validate-artifact-lifecycle.py scripts/test-artifact-lifecycle-validator.py tests/fixtures docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md docs/plan.md`
- Expected observable result: An incomplete or contradictory live-state transition fails in artifact-lifecycle validation before review, verify, or PR handoff.
- Commit message: `M2: add workflow-state sync validator`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - validation notes updated
  - hand off to code-review for M2
  - material findings resolved or explicitly dispositioned before M3 starts

### M3. Review Evidence and Change Metadata Consistency

- Milestone state: closed
- Goal: Make review records, `review-log.md`, `review-resolution.md`, and `change.yaml` derived summaries constrain incompatible owner state without becoming live-state owners.
- Requirements: R64-R75, R10-R12, AC-WSS-007, AC-WSS-008, AC-WSS-012, AC-WSS-025
- Files/components likely touched:
  - `scripts/review_artifact_validation.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-change-metadata-validator.py`
  - review and metadata fixtures under `tests/fixtures/`
- Dependencies:
  - M2 parser and state-sync helpers for owner-state comparison.
  - Existing review artifact validation and change metadata validation contracts.
- Tests to add/update:
  - Open accepted material finding blocks downstream-ready owner state.
  - Open finding count in `change.yaml` must match review artifacts.
  - Resolved findings require final dispositions and validation evidence before `review-requested` reroutes to rereview.
  - `resolved-pending-rereview` style states do not advance to downstream gates without a clean rereview outcome.
  - `change.yaml.change_id` mismatch with plan-body `Change ID` fails as a consistency check.
- Implementation steps:
  - Reuse or expose review-artifact parsing needed by lifecycle state-sync validation.
  - Compare open material findings across detailed review records, `review-log.md`, `review-resolution.md`, and change metadata.
  - Enforce `resolution-needed` and `not ready` owner values while accepted material findings remain open.
  - Preserve review-resolution ownership of finding disposition and validation evidence.
  - Keep `change.yaml` review and validation summaries derived-only.
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
  - `git diff --check -- scripts/review_artifact_validation.py scripts/change_metadata_semantics.py scripts/validate-review-artifacts.py scripts/validate-change-metadata.py scripts/test-review-artifact-validator.py scripts/test-change-metadata-validator.py scripts/test-artifact-lifecycle-validator.py tests/fixtures docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate`
- Expected observable result: Review evidence and compact change metadata cannot drift from each other or from owner states that claim downstream readiness.
- Commit message: `M3: enforce review evidence state consistency`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - validation notes updated
  - hand off to code-review for M3
  - material findings resolved or explicitly dispositioned before M4 starts

### M4. Workflow Guidance, Active Audit, and Projection Normalization

- Milestone state: review-requested
- Goal: Update canonical workflow guidance and active/blocked lifecycle surfaces so contributors and validators use the state-sync gate at transition points.
- Requirements: R1-R21, R58-R63, R76-R81, AC-WSS-001 through AC-WSS-016
- Files/components likely touched:
  - `docs/workflows.md`
  - `docs/plan.md`
  - active and blocked plan files under `docs/plans/`
  - `skills/workflow/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - adapter generation or validation inputs when canonical skills change
- Dependencies:
  - M2 lifecycle state-sync validator.
  - M3 review evidence consistency checks.
- Tests to add/update:
  - Skill text and workflow guidance checks that require the pre-transition state-sync gate before downstream readiness claims.
  - Active/blocked audit fixtures proving legacy plans can be normalized without touching historical done or archived plans.
  - Adapter validation or generated-skill parity checks when canonical skill changes require regeneration.
- Implementation steps:
  - Update workflow guidance to name the state-sync validator as a stage precondition.
  - Update affected skills so failed state-sync blocks downstream handoff language.
  - Normalize active and blocked `docs/plan.md` projections to the approved table format.
  - Audit currently active and blocked plans and add exact owner/projection fields needed for enforcement.
  - Regenerate and validate generated skill or adapter surfaces only when canonical skill changes require it.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
  - `git diff --check -- docs/workflows.md docs/plan.md docs/plans skills docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate`
- Expected observable result: Active and blocked workflow-state surfaces can be cold-read and mechanically validated without narrative current-state drift.
- Commit message: `M4: bind workflow state-sync guidance`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - validation notes updated
  - hand off to code-review for M4
  - material findings resolved or explicitly dispositioned before M5 starts

### M5. Integration, Behavior Preservation, and Closeout Evidence

- Milestone state: planned
- Goal: Prove the whole workflow-state synchronization slice preserves existing ownership boundaries while catching representative incomplete transitions before handoff.
- Requirements: all approved workflow-state synchronization requirements and acceptance criteria
- Files/components likely touched:
  - `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/behavior-preservation.md`
  - `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
  - `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md`
  - `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md`
  - `docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md`
  - `docs/plan.md`
- Dependencies:
  - M1 through M4 complete with clean code reviews or accepted dispositions.
  - No open material findings.
- Tests to add/update:
  - End-to-end lifecycle validation fixture covering implementation-to-review, changes-requested-to-resolution, resolution-to-rereview, clean non-final milestone advance, and final closeout routing.
  - Behavior-preservation evidence matrix required by the proposal.
- Implementation steps:
  - Add behavior-preservation evidence.
  - Run the representative cold transition exercises named by the approved proposal.
  - Confirm no branch or PR readiness is inferred from plan state.
  - Update change metadata with final validation evidence and artifact pointers.
  - Prepare the final handoff to explain-change after implementation and review closeout are complete.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path docs/architecture/system/architecture.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
  - `git diff --check -- docs/plan.md docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md specs scripts docs/workflows.md skills docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate`
- Expected observable result: A fully synchronized transition passes, a representative incomplete transition fails before handoff, and behavior-preservation evidence shows no competing state owner was introduced.
- Commit message: `M5: prove workflow state-sync closeout`
- Milestone closeout:
  - full targeted validation passed
  - progress updated
  - behavior-preservation evidence recorded
  - validation notes updated
  - hand off to code-review for M5
  - material findings resolved or explicitly dispositioned before explain-change starts

## Progress

- 2026-06-23: Proposal accepted after proposal-review R1; no material findings.
- 2026-06-23: Spec approved after spec-review R2 resolved WSS-SR1 and WSS-SR2.
- 2026-06-23: Architecture update approved after architecture-review R1; no material findings.
- 2026-06-23: Execution plan created; plan-review R1 requested revision for WSS-PLAN1.
- 2026-06-23: Plan revised so test-spec authoring is outside implementation milestones and M1 consumes the completed test spec.
- 2026-06-23: Plan-review R2 approved the revised plan and closed WSS-PLAN1; next lifecycle stage is test-spec.
- 2026-06-23: Test spec updated for workflow-state projection enforcement; next lifecycle stage is implement M1.
- 2026-06-23: Test spec approved by maintainer; M1 may consume the active test spec.
- 2026-06-23: M1 implementation started; owner-field, reason-code, and plan-index projection parser fixtures are in scope first.
- 2026-06-23: M1 added shared workflow-state parser scaffolding plus executable owner-field, final-reason, plan-index projection, and readiness/stale-token boundary tests; targeted validation passed and M1 is ready for code-review.
- 2026-06-23: Code-review M1 R1 requested changes for WSS-CR1; M1 remains open in review-resolution.
- 2026-06-23: WSS-CR1 resolved by adding index-to-owner resolution through the shared parser; M1 is ready for code-review R2.
- 2026-06-23: Code-review M1 R2 approved the WSS-CR1 resolution with no material findings; M1 is closed and the next stage is implement M2.
- 2026-06-23: M2 implementation started; scope is current milestone-state projection validation, stricter `Readiness` live-route rejection, and artifact-lifecycle state-sync coverage.
- 2026-06-23: M2 added current milestone-state projection validation, missing-current-milestone detection, and stricter `Readiness` rejection for stale lifecycle route claims; targeted validation passed and M2 is ready for code-review.
- 2026-06-23: Code-review M2 R1 approved the parser and lifecycle state-sync validator slice with no material findings; M2 is closed and the next stage is implement M3.
- 2026-06-23: M3 implementation started; scope is review evidence summary derivation, change metadata review count consistency, and owner-state blocking while material findings remain open.
- 2026-06-23: M3 added review-evidence summary derivation, change metadata review count checks, next-stage-like metadata rejection, and lifecycle owner-state constraints for open material findings; targeted validation passed and M3 is ready for code-review.
- 2026-06-23: Code-review M3 R1 requested changes for WSS-CR2; M3 remains open in review-resolution.
- 2026-06-23: WSS-CR2 resolved by routing review evidence summaries and closeout-mode validation through a shared finding closure predicate; M3 is ready for code-review R2.
- 2026-06-23: Code-review M3 R2 confirmed WSS-CR2 resolution and requested changes for WSS-CR3; M3 remains open in review-resolution.
- 2026-06-23: WSS-CR3 resolved by converting the shared finding closure predicate to positive-evidence closeout semantics and adding invalid-disposition, missing-closeout-status, parity, change metadata, and lifecycle regression coverage; M3 is ready for code-review R3.
- 2026-06-23: Code-review M3 R3 approved the WSS-CR3 resolution with no material findings; M3 is closed and the next stage is implement M4.
- 2026-06-23: M4 implementation started; workflow guidance, skill handoff wording, and active/blocked projection audit surfaces are in scope.
- 2026-06-23: M4 added binding state-sync gate wording to workflow guidance and canonical stage skills, added static regression coverage, normalized the missing active plan `Change ID` projection source for the Evidence-Bound Project Map plan, and handed M4 to code-review.
- 2026-06-23: Code-review M4 R1 requested changes for WSS-CR4; M4 remains open in review-resolution until active/blocked enforcement scope passes or the governing contract is revised.
- 2026-06-23: WSS-CR4 resolved by changing lifecycle state-sync metadata association from cross-product comparison to `change_id`/`artifacts.plan` keyed pairing, adding multi-active-plan regression coverage, and rerunning the all-active audit cleanly; M4 is ready for code-review R2.

## Decision log

- 2026-06-23: Keep the first implementation slice read-only for projection enforcement; defer any projection writer until validator fixtures and golden outputs are stable.
- 2026-06-23: Compose lifecycle state-sync through artifact-lifecycle validation rather than introducing a separate authoritative parser command.
- 2026-06-23: Treat active and blocked plan normalization as implementation work, with historical plans preserved under the existing conservation contract.
- 2026-06-23: Keep `test-spec` as a separate lifecycle stage after plan-review; implementation milestones consume the completed test spec rather than authoring it.

## Surprises and discoveries

- Existing active plans predate the new exact `Current Handoff Summary` grammar, so M4 includes the active/blocked audit and normalization required before enforcement is enabled.
- Plan-review R1 exposed that test-spec authoring had been folded into M1; the revision keeps lifecycle sequencing aligned with the standard workflow.
- M1 state-sync enforcement is guarded to plans already carrying the structured `Latest review evidence` handoff field so legacy active plans remain compatible until the M4 audit and normalization milestone.
- M2 found that owner-field and plan-index projection parsing were already present from M1 and WSS-CR1 resolution, so the remaining parser gap was the current milestone-state projection plus stale lifecycle route claims in `Readiness`.
- M3 reused the existing review artifact parser and kept change metadata as a derived consistency surface; no live next-stage ownership moved into `change.yaml`.
- WSS-CR2 confirmed that derived lifecycle booleans need one shared predicate; the review evidence summary and closeout-mode review validator now share `finding_closure_state()`.
- M4 found that this repo has no authored `skills/review-resolution/SKILL.md`; review-resolution routing is covered by `code-review`, review artifacts, and workflow guidance rather than a separate canonical skill file.
- M4 active/blocked audit found no blocked plans and one safe active projection-source normalization: `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md` now carries the same `Change ID` already projected in `docs/plan.md` and `change.yaml`.
- WSS-CR4 traced the failed all-active audit to validator association logic, not bad plan data: the Evidence-Bound plan body and `change.yaml` already had matching `Change ID` values, while state-sync compared each in-scope `change.yaml` against every structured plan.
- The WSS-CR4 resolution keeps legacy active plans under the existing structured-marker grandfather rule and skips their linked metadata consistently; truly orphaned in-scope change metadata still blocks.

## Validation notes

- 2026-06-23: `git diff --check -- specs/single-source-of-workflow-state.test.md docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md docs/plan.md docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml` passed after test-spec update.
- 2026-06-23: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml` passed after test-spec update.
- 2026-06-23: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/` passed after test-spec update.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path docs/architecture/system/architecture.md --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/plan-review-r2.md` passed after test-spec update.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py -k workflow_state` failed before parser implementation because owner-field, reason-code, plan-index projection, and readiness stale-token fixtures were not enforced.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py -k workflow_state` passed after M1 parser implementation.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py` passed after M1 parser implementation.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/single-source-of-workflow-state.test.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/plan.md` passed after M1 parser implementation.
- 2026-06-23: `git diff --check -- scripts/lifecycle_state_sync.py scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py scripts/test-review-artifact-validator.py scripts/test-change-metadata-validator.py tests/fixtures docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md docs/plan.md` passed after M1 parser implementation.
- 2026-06-23: `python scripts/test-review-artifact-validator.py` passed after M1 parser implementation.
- 2026-06-23: `python scripts/test-change-metadata-validator.py` passed after M1 parser implementation.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py -k workflow_state` passed after WSS-CR1 resolution.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py` passed after WSS-CR1 resolution.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md` passed against the repository state after WSS-CR1 resolution.
- 2026-06-23: Direct drift-fixture validation with `paths=["docs/plan.md"]` produced one blocker on the stale `docs/plan.md` `Next stage` projection after WSS-CR1 resolution.
- 2026-06-23: Code-review M1 R2 found no material findings in commit `cb57b8db`; review evidence and lifecycle handoff now route to implement M2.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py -k workflow_state` failed before M2 implementation for missing current milestone-state projection and stale `Readiness` route checks, then passed after implementation.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py` passed after M2 implementation.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md` passed after M2 implementation.
- 2026-06-23: `git diff --check -- scripts/lifecycle_state_sync.py scripts/artifact_lifecycle_validation.py scripts/validate-artifact-lifecycle.py scripts/test-artifact-lifecycle-validator.py tests/fixtures docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md docs/plan.md` passed after M2 implementation.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml` passed after M2 handoff state-sync.
- 2026-06-23: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml` passed after M2 handoff state-sync.
- 2026-06-23: `git diff --check -- scripts/lifecycle_state_sync.py scripts/artifact_lifecycle_validation.py scripts/validate-artifact-lifecycle.py scripts/test-artifact-lifecycle-validator.py tests/fixtures docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md docs/plan.md docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml` passed after M2 handoff state-sync.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py -k multi_active`, `python scripts/test-artifact-lifecycle-validator.py -k audit_pairs`, and `python scripts/test-artifact-lifecycle-validator.py -k workflow_state` passed after WSS-CR4 resolution.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md` passed after WSS-CR4 resolution.
- 2026-06-23: Code-review M2 R1 found no material findings in commit `8e786154`; review evidence and lifecycle handoff now route to implement M3.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py -k open_review` failed before M3 implementation for open review findings with `review-requested` owner state, then passed after implementation.
- 2026-06-23: `python scripts/test-change-metadata-validator.py -k review_summary` failed before M3 implementation for review count drift and next-stage-like metadata, then passed after implementation.
- 2026-06-23: `python scripts/test-review-artifact-validator.py` passed after M3 implementation.
- 2026-06-23: `python scripts/test-change-metadata-validator.py` passed after M3 implementation.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py` passed after M3 implementation.
- 2026-06-23: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/` passed after M3 implementation.
- 2026-06-23: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/` passed after synchronizing resolved finding open-status projections in `review-log.md`.
- 2026-06-23: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml` passed after M3 implementation.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md` passed after M3 implementation.
- 2026-06-23: `git diff --check -- scripts/review_artifact_validation.py scripts/change_metadata_semantics.py scripts/validate-review-artifacts.py scripts/validate-change-metadata.py scripts/test-review-artifact-validator.py scripts/test-change-metadata-validator.py scripts/test-artifact-lifecycle-validator.py tests/fixtures docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md docs/plan.md` passed after M3 implementation.
- 2026-06-23: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/` passed after code-review M3 R1 recording.
- 2026-06-23: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml` passed after code-review M3 R1 recording.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m3-r1.md` passed after code-review M3 R1 recording.
- 2026-06-23: `git diff --check -- docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m3-r1.md docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md docs/plan.md docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml` passed after code-review M3 R1 recording.
- 2026-06-23: `python scripts/test-review-artifact-validator.py` passed after WSS-CR2 resolution.
- 2026-06-23: `python scripts/test-change-metadata-validator.py` passed after WSS-CR2 resolution.
- 2026-06-23: `python scripts/test-artifact-lifecycle-validator.py` passed after WSS-CR2 resolution.
- 2026-06-23: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/` passed after WSS-CR2 resolution.
- 2026-06-23: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml` passed after WSS-CR2 resolution.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m3-r1.md` passed after WSS-CR2 resolution.
- 2026-06-23: `git diff --check -- specs/single-source-of-workflow-state.md specs/single-source-of-workflow-state.test.md scripts/review_artifact_validation.py scripts/validate-change-metadata.py scripts/test-review-artifact-validator.py scripts/test-change-metadata-validator.py scripts/test-artifact-lifecycle-validator.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md docs/plan.md` passed after WSS-CR2 resolution.
- 2026-06-23: `python scripts/test-review-artifact-validator.py`, `python scripts/test-change-metadata-validator.py`, and `python scripts/test-artifact-lifecycle-validator.py` passed during code-review M3 R2.
- 2026-06-23: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`, `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`, and explicit-path artifact lifecycle validation passed before recording code-review M3 R2.
- 2026-06-23: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`, `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`, explicit-path artifact lifecycle validation, and `git diff --check` passed after code-review M3 R2 recording.
- 2026-06-23: `python scripts/test-review-artifact-validator.py`, `python scripts/test-change-metadata-validator.py`, and `python scripts/test-artifact-lifecycle-validator.py` passed after WSS-CR3 resolution.
- 2026-06-23: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`, `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`, explicit-path artifact lifecycle validation, and `git diff --check` passed after WSS-CR3 resolution and handoff synchronization.
- 2026-06-23: `python scripts/test-review-artifact-validator.py`, `python scripts/test-change-metadata-validator.py`, `python scripts/test-artifact-lifecycle-validator.py`, change-local review artifact validation, change metadata validation, explicit-path artifact lifecycle validation, and `git diff --check` passed during code-review M3 R3.
- 2026-06-23: `python scripts/test-skill-validator.py -k workflow_state_sync_gate_is_binding_guidance` failed before M4 guidance updates because the binding validator/timing/failure wording was absent, then passed after docs and skill updates.
- 2026-06-23: `python scripts/validate-skills.py`, `python scripts/test-build-skills.py`, and `python scripts/build-skills.py --check` initially failed because repository-local script paths were embedded in public skill text; M4 revised public skill wording to portable project-local validation language and the commands passed.
- 2026-06-23: `python scripts/test-skill-validator.py`, `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`, `python scripts/validate-guide-system.py`, and `python scripts/test-select-validation.py` passed after M4 guidance updates.
- 2026-06-23: Active/blocked audit command over all active plan rows exposed preexisting legacy active-plan debt and a cross-plan change-metadata association blocker; M4 kept that outside this guidance slice and validated the current initiative's owner/projection surfaces directly.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md` passed after M4 handoff state-sync.
- 2026-06-23: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`, `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`, and `git diff --check -- docs/workflows.md docs/plan.md docs/plans skills scripts/test-skill-validator.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate` passed after M4 handoff state-sync.
- 2026-06-23: Code-review M4 R1 reproduced the all-active audit failure with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md`; the command failed on cross-plan change metadata association and supports WSS-CR4.
- 2026-06-23: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`, `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`, explicit-path artifact lifecycle validation, and `git diff --check` passed after recording code-review M4 R1.

## Outcome and retrospective

- Pending. This section stays historical while the plan is active and does not own the current next stage.

## Readiness

- See `Current Handoff Summary`.
- Readiness is not Done.

## Risks and follow-ups

- Active-plan normalization may uncover stale preexisting lifecycle wording; M4 must either update it as part of enforcement or record a named blocker.
- Review-artifact consistency can fail closed when older review evidence lacks the detail needed for deterministic comparison; M3 should keep enforcement scoped to active/blocked and lifecycle-changing plans.
- Skill guidance changes may require generated adapter validation; M4 owns that check only when canonical skill text changes.
