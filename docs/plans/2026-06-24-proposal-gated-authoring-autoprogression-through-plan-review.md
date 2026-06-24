# Proposal-Gated Authoring Autoprogression Through Plan Review Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review
- Owner: agent
- Start date: 2026-06-24
- Last updated: 2026-06-24
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved proposal-gated authoring autoprogression contract so a workflow-managed change can explicitly arm `authoring-through-plan-review`, prove the proposal gate from recorded artifacts, run deterministic authoring and review stages through clean `plan-review`, and stop before `test-spec` or implementation. The plan keeps the implementation reviewable by separating policy persistence, routing/state-machine behavior, stage skill guidance, generated adapter alignment, and integration evidence.

## Source artifacts

- Proposal: [Proposal-Gated Authoring Autoprogression Through Plan Review](../proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md)
- Spec: [Workflow Stage Autoprogression](../../specs/workflow-stage-autoprogression.md)
- Workflow spec: [RigorLoop Workflow](../../specs/rigorloop-workflow.md)
- Test spec: [Workflow Stage Autoprogression test spec](../../specs/workflow-stage-autoprogression.test.md)
- Workflow test spec: [RigorLoop Workflow test spec](../../specs/rigorloop-workflow.test.md)
- Architecture: [Canonical System Architecture](../architecture/system/architecture.md)
- ADR: [ADR-20260624 Proposal-Gated Authoring Autoprogression](../adr/ADR-20260624-proposal-gated-authoring-autoprogression.md)
- Change metadata: [change.yaml](../changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml)
- Review log: [review-log.md](../changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md)
- Review resolution: [review-resolution.md](../changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md)
- Proposal review: [proposal-review-r1](../changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/proposal-review-r1.md)
- Spec reviews: [spec-review-r1](../changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/spec-review-r1.md), [spec-review-r2](../changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/spec-review-r2.md)
- Architecture review: [architecture-review-r1](../changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/architecture-review-r1.md)

## Upstream status settlement

- Settlement result: not-needed
- New status: not-applicable
- Settlement blocker: none
- Evidence: proposal status is `accepted`; `specs/workflow-stage-autoprogression.md` and `specs/rigorloop-workflow.md` are `approved`; canonical architecture status is `approved`; ADR status is `accepted`; `spec-review-r2` and `architecture-review-r1` are approved with no material findings; `review-resolution.md` is closed.

## Context and orientation

RigorLoop is an artifact-based workflow kit rather than a deployed service. The implementation surface is therefore the repository workflow contract, canonical skill text under `skills/`, validation scripts under `scripts/`, schema and fixture coverage under `schemas/` and `tests/fixtures/`, and generated adapter validation. Public adapter skill bodies are release archives rather than tracked authored output, so implementation must edit canonical skills and validate generated output through repository scripts rather than hand-editing adapter packages.

The approved architecture defines `authoring-through-plan-review` as a change-local workflow policy profile, not live workflow state. `docs/changes/<change-id>/change.yaml` is the canonical policy persistence surface when the change-metadata contract accepts policy data; `workflow-policy.yaml` is only the fallback. Active planned-initiative live state remains owned by this plan's `Current Handoff Summary`.

## Non-goals

- Do not widen `authoring-through-plan-review` to `test-spec`, implementation, verification, PR, release, deploy, merge, or automatic review-fix loops.
- Do not introduce a repository-wide default for the profile.
- Do not make `change.yaml` or `workflow-policy.yaml` own current stage, next stage, review status, branch readiness, PR readiness, or active plan state.
- Do not change default behavior when the profile is `off`.
- Do not change direct review-only invocation isolation.
- Do not add background processing, external schedulers, services, new persistence engines, or network-dependent workflow execution.
- Do not hand-edit generated public adapter package output.

## Requirements covered

- `R2h`-`R2q`, `R7ea`-`R7ej`: M2 and M3 implement the closed profile, user-facing mapping, gate activation, bounded sequence, completion boundary, and no-test-spec/no-implementation rule.
- `R2r`-`R2t`, `R7er`: M1 implements mandatory durable authorization persistence, canonical/fallback policy surfaces, malformed-record handling, and `authorization-not-persisted`.
- `R2u`-`R2w`, `R7es`: M2 and M5 preserve explicit resume and require separate proposals for future profile expansion.
- `R2x`-`R2aa`, `R7ek`-`R7el`: M2 and M3 implement recorded architecture assessment outcomes and routing.
- `R2ab`-`R2ad`, `R7em`: M3 preserves independent formal review invocations and evidence before downstream action.
- `R2ae`-`R2ah`, `R7en`-`R7eo`: M2 and M5 enforce stop conditions, stop-result reporting, idempotent resume, and safe handling of contradictory state.
- `R2ai`-`R2aj`, `R7ep`: M2 enforces the six-slot transition budget and explicit rereview formula.
- `R2ak`-`R2al`, `R7eq`: M5 records the audit trail and verifies behavior preservation.
- `APGA-001`-`APGA-037`, `T11`, `T12`, and `T37`: covered across M1 through M5.

## Current Handoff Summary

- Current milestone: M5. Integration, Behavior Preservation, and Lifecycle Closeout Evidence
- Current milestone state: closed
- Latest review evidence: code-review-m5-r1
- Last reviewed milestone: M5. Integration, Behavior Preservation, and Lifecycle Closeout Evidence
- Review status: approved; stage=code-review; round=r1
- Remaining in-scope implementation milestones: none
- Next stage: pr
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: pr-handoff-pending — implementation milestones, explain-change, and verify are complete, but PR handoff remains.

## Milestones

### M1. Profile Policy Persistence and Metadata Validation

- Milestone state: closed
- Goal: Make change-local profile authorization persistence concrete, validated, and fail-closed before activation.
- Requirements: `R2h`-`R2t`, `R2ae`, `R2ag`, `R7ea`-`R7eg`, `R7er`, `APGA-001`-`APGA-006`, `APGA-031`-`APGA-036`
- Files/components likely touched:
  - `schemas/change.schema.json`
  - `scripts/validate-change-metadata.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/query-change-record.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/change-metadata/`
  - `docs/workflows.md`
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- Dependencies:
  - Approved spec and architecture.
  - Completed plan-review before implementation starts.
- Tests to add/update:
  - Valid `workflow.autoprogression.profile: authoring-through-plan-review` with `authorized_by`, authorization timestamp, and matching change ID.
  - Unknown profile fails closed.
  - Missing, malformed, partial, or failed durable authorization is represented as `authorization-not-persisted`.
  - Pre-pack arming is not treated as durable authorization.
  - Cancellation requires durable policy update before profile is treated as `off`.
  - Fallback `workflow-policy.yaml` is valid only when the change-metadata contract rejects policy data and records fallback evidence.
- Implementation steps:
  - Add or formalize the `workflow.autoprogression` policy shape while preserving `additionalProperties` compatibility where required.
  - Add semantic validation for closed profile values, required authorization fields, matching change ID, timestamp shape, and malformed/partial records.
  - Add fixture-backed validator coverage for APGA-031 through APGA-036.
  - Ensure query helpers expose policy metadata only as policy evidence, not live next-stage state.
  - Update workflow guidance for canonical policy placement and fallback behavior.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path schemas/change.schema.json --path docs/workflows.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `git diff --check -- schemas/change.schema.json scripts/validate-change-metadata.py scripts/change_metadata_semantics.py scripts/query-change-record.py scripts/test-change-metadata-validator.py tests/fixtures/change-metadata docs/workflows.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review`
- Expected observable result: A profile cannot activate from absent, malformed, partial, unknown, non-durable, or failed policy persistence, and validated policy metadata remains distinct from live workflow state.
- Commit message: `M1: validate profile policy persistence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M2 starts
- Risks:
  - Metadata validation could accidentally reject legacy change records.
  - Policy fields could be mistaken for live next-stage state.
- Rollback/recovery:
  - Revert the semantic validation and fixtures together, leaving profile behavior off by default and preserving existing change metadata validation.

### M2. Workflow Profile Routing, Gate Evaluation, and Resume Semantics

- Milestone state: closed
- Goal: Implement the workflow-managed `authoring-through-plan-review` state machine, including activation, gate readiness, transition budget, idempotent resume, and stop-result reporting.
- Requirements: `R2h`-`R2q`, `R2u`-`R2aa`, `R2ae`-`R2aj`, `R7ea`-`R7el`, `R7en`-`R7ep`, `APGA-001`-`APGA-021`, `APGA-025`-`APGA-030`, `APGA-037`
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - `scripts/lifecycle_state_sync.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - workflow-state fixtures under `tests/fixtures/artifact-lifecycle/`
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- Dependencies:
  - M1 durable policy shape and validator behavior.
- Tests to add/update:
  - Profile default `off` preserves existing behavior.
  - `armed && gate-ready && durable authorization persisted` starts `spec`.
  - Gate readiness fails when proposal status, proposal-review approval, recording, findings, open blockers, scope, standing gates, change ID, or placement evidence is missing.
  - `spec-review` routes through recorded architecture assessment.
  - `architecture-required`, `architecture-not-required`, and `architecture-ambiguous` route or pause as specified.
  - Transition budget is six slots and unused architecture slots cannot run other stages.
  - Resume skips reliably completed stages and pauses on ambiguous partial completion.
- Implementation steps:
  - Add workflow routing instructions and helper validation coverage for profile states `off`, `armed`, `active`, `paused`, and `completed`.
  - Define tracked-artifact gate evaluation inputs and stop reasons in workflow guidance.
  - Add recorded architecture-assessment handling to the workflow-managed route.
  - Ensure direct review-only and bugfix/manual paths stay isolated unless workflow-managed resume is explicit.
  - Add lifecycle validation fixtures that catch contradictory profile state, missing evidence, duplicate stage execution, and transition-budget exhaustion.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/workflow/SKILL.md --path docs/workflows.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `git diff --check -- skills/workflow/SKILL.md docs/workflows.md scripts/lifecycle_state_sync.py scripts/artifact_lifecycle_validation.py scripts/validate-artifact-lifecycle.py scripts/test-artifact-lifecycle-validator.py tests/fixtures/artifact-lifecycle docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review`
- Expected observable result: Workflow-managed routing can explain exactly why the profile starts, pauses, resumes, completes, or remains off without duplicate stage execution or hidden implementation handoff.
- Commit message: `M2: route authoring autoprogression profile`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M3 starts
- Risks:
  - Routing text could over-authorize isolated review requests.
  - Resume rules could infer completion from file existence alone.
- Rollback/recovery:
  - Restore previous workflow routing guidance and leave profile policy recognized but inactive until routing is corrected.

### M3. Stage Skill Alignment and Review Independence

- Milestone state: closed
- Goal: Align proposal-review, spec, spec-review, architecture, architecture-review, plan, and plan-review guidance with the approved profile while preserving independent recorded reviews.
- Requirements: `R2l`-`R2q`, `R2x`-`R2ae`, `R2ak`, `R7eh`-`R7em`, `R7eq`, `APGA-007`-`APGA-018`, `APGA-023`, `APGA-024`
- Files/components likely touched:
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - stage skill assets under `skills/*/assets/` when needed
  - `scripts/test-skill-validator.py`
  - `docs/workflows.md`
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- Dependencies:
  - M2 workflow routing terms and stop reasons.
- Tests to add/update:
  - Proposal-review can expose deterministic gate result and immediate next stage without making direct reviews auto-continue.
  - Spec and architecture authoring stages still hand to their matching reviews in workflow-managed flows.
  - Spec-review records architecture assessment outcome before profile-driven downstream action.
  - Review stages reset to tracked artifact, governing sources, formal criteria, and prior findings instead of relying on author hidden reasoning.
  - Plan-review completion reports `test-spec` next and profile completed without invoking `test-spec`.
- Implementation steps:
  - Update stage handoff wording to name the new profile as the only review-to-next-authoring exception.
  - Add review-independence and recording preconditions to affected review skills.
  - Add architecture-assessment output guidance to `spec-review` or workflow-owned routing as appropriate.
  - Update plan and plan-review guidance for profile completion and stop-before-test-spec boundary.
  - Add skill-validator assertions for new required phrases and isolation guardrails.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/proposal-review/SKILL.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path docs/workflows.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `git diff --check -- skills/proposal-review/SKILL.md skills/spec/SKILL.md skills/spec-review/SKILL.md skills/architecture/SKILL.md skills/architecture-review/SKILL.md skills/plan/SKILL.md skills/plan-review/SKILL.md scripts/test-skill-validator.py docs/workflows.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review`
- Expected observable result: Every affected stage states the same bounded profile contract, formal review stages remain independently recorded, and direct review invocations remain isolated.
- Commit message: `M3: align authoring profile stage skills`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M4 starts
- Risks:
  - User-facing skill text could become too internal or too repository-maintainer-specific.
  - Different skills could describe subtly different profile boundaries.
- Rollback/recovery:
  - Revert affected skill text as one unit and restore prior isolation wording until a smaller alignment slice is ready.

### M4. Generated Adapter and Distribution Guidance Alignment

- Milestone state: closed
- Goal: Prove canonical skill changes generate and validate consistently across supported adapter surfaces without hand-editing generated output.
- Requirements: `R2ak`, `R7eq`, `APGA-018`, `APGA-019`, `APGA-029`, `APGA-030`
- Files/components likely touched:
  - `scripts/build-skills.py`
  - `scripts/test-build-skills.py`
  - `scripts/test-adapter-distribution.py`
  - `dist/adapters/README.md`
  - `dist/adapters/manifest.yaml`
  - adapter templates under `scripts/adapter_templates/` when routing guidance requires it
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- Dependencies:
  - M3 canonical skill changes.
- Tests to add/update:
  - `build-skills --check` remains deterministic after profile guidance changes.
  - Adapter manifest and public adapter support surfaces remain aligned with canonical skill availability.
  - No generated public adapter package body is hand-edited or tracked as source.
  - Direct review aliases or adapter commands do not imply workflow-managed autoprogression.
- Implementation steps:
  - Run generated-skill drift checks after canonical skill edits.
  - Update adapter support documentation or manifest only when canonical changes require it.
  - Add or adjust adapter regression coverage if adapter templates expose stale stage-order or isolation language.
  - Record unaffected-with-rationale if adapter surfaces require no content change.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py`
  - `git diff --check -- scripts/build-skills.py scripts/test-build-skills.py scripts/test-adapter-distribution.py scripts/adapter_templates dist/adapters docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md`
- Expected observable result: Generated and adapter-facing guidance stays synchronized with canonical skills, and public adapters do not gain broader autoprogression semantics by accident.
- Commit message: `M4: validate generated profile guidance`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M5 starts
- Risks:
  - Adapter tests may reveal unrelated baseline drift.
  - Generated-output checks may require broader validation than the changed source appears to need.
- Rollback/recovery:
  - Revert adapter-support edits and keep canonical skill behavior guarded by M3 until generated alignment can be repaired.

### M5. Integration, Behavior Preservation, and Lifecycle Closeout Evidence

- Milestone state: closed
- Goal: Prove the complete first slice preserves default behavior, exercises the new profile paths, and leaves reviewable closeout evidence before final verification and PR handoff.
- Requirements: all approved `authoring-through-plan-review` requirements and acceptance criteria, including `APGA-001`-`APGA-037`
- Files/components likely touched:
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/behavior-preservation.md`
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/explain-change.md`
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/verify-report.md` when verify requires a standalone report
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`
  - `docs/plan.md`
  - any fixtures or validation scripts touched by M1-M4
- Dependencies:
  - M1 through M4 closed with clean code-review or resolved findings.
  - Required review-resolution closeout remains closed.
- Tests to add/update:
  - End-to-end fixture-backed simulation for flag off.
  - End-to-end fixture-backed simulation for flag on with no architecture required.
  - End-to-end fixture-backed simulation for flag on with architecture required.
  - Stop-path fixtures for non-clean review, ambiguous architecture, missing persistence, direct review isolation, pause/cancel, duplicate resume, and transition-budget exhaustion.
  - Behavior-preservation matrix stays aligned with the accepted proposal.
- Implementation steps:
  - Add integration fixtures or manual-proof records that exercise the APGA matrix across the implemented surfaces.
  - Update behavior-preservation evidence for final implementation behavior.
  - Run selected validation first, then broaden to repository-owned validation required by the plan and touched surfaces.
  - Create explain-change after implementation and code-review close.
  - Run verify and update plan lifecycle state only after all in-scope milestones and required review-resolution are closed.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md`
  - `bash scripts/ci.sh --mode explicit --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path skills/workflow/SKILL.md --path docs/workflows.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `git diff --check -- .`
- Expected observable result: The feature is implemented with durable audit evidence, no default behavior regression, no skipped required architecture path, no auto-started `test-spec` or implementation, and no stale active-plan state.
- Commit message: `M5: prove authoring profile behavior`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - all material findings closed before explain-change, verify, or PR handoff
- Risks:
  - Integration evidence could accidentally rely on chat-only behavior rather than tracked fixtures.
  - Broad validation may surface unrelated baseline warnings that need classification.
- Rollback/recovery:
  - Disable the profile by keeping closed profile recognition but treating activation as paused until failing evidence is resolved; preserve produced artifacts and review records.

## Validation plan

- `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`: review structure remains valid.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`: review closeout remains valid.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`: change metadata remains valid after plan and implementation evidence updates.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`: active plan state, index state, and change metadata stay synchronized.
- `python scripts/test-change-metadata-validator.py`: policy persistence and metadata fixtures.
- `python scripts/test-artifact-lifecycle-validator.py`: workflow-state, routing, and lifecycle fixture coverage.
- `python scripts/test-skill-validator.py`: canonical skill text and workflow guidance assertions.
- `python scripts/validate-skills.py`: canonical skill schema validation.
- `python scripts/build-skills.py --check`: generated local skill output remains deterministic.
- `python scripts/test-build-skills.py`: build behavior regression coverage.
- `python scripts/test-adapter-distribution.py`: adapter support and archive/guidance regression coverage.
- `bash scripts/ci.sh --mode explicit --path <changed path>...`: selected repository validation before final verify.
- `git diff --check -- <changed path>...`: whitespace and patch hygiene.

## Risks and recovery

- Risk: The profile changes direct review behavior by accident.
  - Recovery: Keep direct review tests and skill wording in every affected milestone; revert routing changes before broadening stage guidance.
- Risk: Policy metadata becomes a competing live-state owner.
  - Recovery: Keep metadata validators and workflow guidance limited to policy fields; state-sync validation must continue to compare live state against the active plan owner.
- Risk: Architecture routing is skipped in the no-architecture path.
  - Recovery: Require a recorded architecture assessment even when the outcome is `architecture-not-required`.
- Risk: Review independence collapses because stages run consecutively.
  - Recovery: Make independent review context and formal recording a continuation precondition; stop on missing review evidence.
- Risk: Generated adapter guidance drifts from canonical skills.
  - Recovery: Run build and adapter checks after canonical skill edits; do not hand-edit generated public adapter output.
- Risk: The implementation starts `test-spec` or implementation as part of the first profile.
  - Recovery: Keep no-test-spec/no-implementation tests in M2 and M5; reject any handoff language that claims more than `test-spec` next.

## Dependencies

- `plan-review` must approve this plan before implementation starts.
- `test-spec` must run after clean `plan-review` and before implementation unless an explicitly isolated manual implementation request is recorded.
- M1 must land before M2 because workflow routing depends on durable policy shape and failure modes.
- M2 must land before M3 because stage skills need stable profile routing terms and stop reasons.
- M3 must land before M4 because generated adapter validation depends on canonical skill text.
- M5 depends on all implementation milestones and required code-review/review-resolution closeout.

## Progress

- 2026-06-24: Created plan after accepted proposal, approved specs, approved architecture, accepted ADR, and clean architecture-review.
- 2026-06-24: Plan-review R1 approved the plan with no material findings; test-spec updated the active proof surface and routed the current handoff to M1 implementation.
- 2026-06-24: User approved the active test spec for M1 implementation reliance.
- 2026-06-24: Started M1 implementation; updating policy persistence validation before workflow routing changes.
- 2026-06-24: M1 implemented schema, validator, query-helper, and workflow-guidance support for durable profile policy records; handed to code-review.
- 2026-06-24: Code-review M1 R1 returned `clean-with-notes`; M1 closed and next stage is `implement M2`.
- 2026-06-24: Started M2 implementation; adding workflow-managed profile routing and stop/resume validation before workflow guidance updates.
- 2026-06-24: M2 implemented authoring-profile route evaluation coverage and aligned workflow routing guidance; handed to code-review.
- 2026-06-24: Code-review M2 R1 returned `changes-requested` for CR-M2-001 and CR-M2-002; M2 requires review-resolution before M3.
- 2026-06-24: Resolved CR-M2-001 and CR-M2-002 by adding terminal profile-state gates, durable resume/cancel route semantics, fail-loud active handoff parsing, and regression coverage; handed M2 back to code-review R2.
- 2026-06-24: Code-review M2 R2 returned `clean-with-notes`; M2 closed and next stage is `implement M3`.
- 2026-06-24: Started M3 implementation; aligning canonical stage-skill guidance for the bounded authoring profile and review-independence preconditions.
- 2026-06-24: M3 aligned affected canonical stage skills, workflow guidance, and skill-validator assertions for the bounded authoring profile; handed to code-review.
- 2026-06-24: Code-review M3 R1 returned `clean-with-notes`; M3 closed and next stage is `implement M4`.
- 2026-06-24: Started M4 implementation; validating generated-skill and adapter-facing guidance after the M3 canonical skill changes.
- 2026-06-24: M4 generated-skill and adapter validation passed. `scripts/build-skills.py`, `scripts/test-build-skills.py`, `scripts/test-adapter-distribution.py`, `scripts/adapter_templates/`, `dist/adapters/README.md`, and `dist/adapters/manifest.yaml` remain unchanged with rationale: the existing generator and adapter support surfaces already preserve direct-review isolation, avoid tracked generated public adapter bodies, and do not imply broader autoprogression.
- 2026-06-24: Code-review M4 R1 returned `clean-with-notes`; M4 closed and next stage is `implement M5`.
- 2026-06-24: Started M5 implementation; updating integrated behavior-preservation proof before running final milestone validation.
- 2026-06-24: M5 integrated behavior-preservation proof updated and milestone validation passed; M5 moved to `review-requested` for code-review.
- 2026-06-24: Code-review M5 R1 returned `clean-with-notes`; M5 closed and next stage is `explain-change`.
- 2026-06-24: Explain-change recorded durable rationale for the full authoring-profile implementation and routed next stage to `verify`.
- 2026-06-24: Verify recorded branch-ready evidence and routed next stage to `pr`.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-24 | Split metadata persistence before workflow routing. | Activation safety depends on durable authorization evidence; routing should not be implemented against an advisory or undefined policy shape. | Implement routing first and add persistence validation later. |
| 2026-06-24 | Keep stage-skill alignment separate from core workflow routing. | Review independence and direct-review isolation need focused review across several user-facing skills. | Fold all skill changes into one broad routing milestone. |
| 2026-06-24 | Treat generated adapter alignment as its own milestone. | Canonical skill changes can affect generated or adapter-facing surfaces, and repository policy forbids hand-editing generated public adapter packages. | Leave adapter validation to final broad smoke only. |

## Surprises and discoveries

- None yet.

## Validation notes

- 2026-06-24: Plan creation validation passed for review artifacts, change metadata, artifact lifecycle, and whitespace checks as recorded in `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`.
- 2026-06-24: Test-spec update validation passed for change metadata, artifact lifecycle, and whitespace checks as recorded in `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`.
- 2026-06-24: M1 validation passed: `python scripts/test-change-metadata-validator.py`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path schemas/change.schema.json --path docs/workflows.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `git diff --check -- schemas/change.schema.json scripts/validate-change-metadata.py scripts/change_metadata_semantics.py scripts/query-change-record.py scripts/test-change-metadata-validator.py tests/fixtures/change-metadata docs/workflows.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review`.
- 2026-06-24: Code-review M1 R1 recorded a clean review receipt and updated lifecycle handoff state; post-review validation recorded in `change.yaml`.
- 2026-06-24: M2 validation passed: `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/workflow/SKILL.md --path docs/workflows.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml` with the existing lifecycle-language warning in `specs/rigorloop-workflow.md`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `git diff --check -- skills/workflow/SKILL.md docs/workflows.md scripts/lifecycle_state_sync.py scripts/artifact_lifecycle_validation.py scripts/validate-artifact-lifecycle.py scripts/test-artifact-lifecycle-validator.py tests/fixtures/artifact-lifecycle docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review`.
- 2026-06-24: Code-review M2 R1 recorded two material findings and routed the milestone to review-resolution.
- 2026-06-24: Code-review M2 R1 recording validation passed: `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m2-r1.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `git diff --check -- docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m2-r1.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`.
- 2026-06-24: Review-resolution M2 regression test validation passed: `python scripts/test-artifact-lifecycle-validator.py` passed 108 tests. The first post-hardening lifecycle validation parsed the active plan handoff and blocked stale `Readiness` wording, proving the handoff is no longer skipped.
- 2026-06-24: Review-resolution M2 closeout validation passed: `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/ && python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md --path skills/workflow/SKILL.md --path docs/workflows.md --path scripts/lifecycle_state_sync.py --path scripts/artifact_lifecycle_validation.py --path scripts/test-artifact-lifecycle-validator.py`.
- 2026-06-24: Code-review M2 R2 recorded a clean review receipt and updated lifecycle handoff state; post-review validation recorded in `change.yaml`.
- 2026-06-24: Code-review M2 R2 recording validation passed: `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/ && python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m2-r2.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `git diff --check -- docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m2-r2.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`.
- 2026-06-24: M3 validation passed: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/proposal-review/SKILL.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path docs/workflows.md --path scripts/test-skill-validator.py --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `git diff --check -- skills/proposal-review/SKILL.md skills/spec/SKILL.md skills/spec-review/SKILL.md skills/architecture/SKILL.md skills/architecture-review/SKILL.md skills/plan/SKILL.md skills/plan-review/SKILL.md scripts/test-skill-validator.py docs/workflows.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`.
- 2026-06-24: Code-review M3 R1 recorded a clean review receipt and updated lifecycle handoff state; post-review validation passed: `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/ && python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m3-r1.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `git diff --check -- docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m3-r1.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`.
- 2026-06-24: M4 validation passed: `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py` passed 129 tests; `python scripts/validate-skills.py`; `git diff --check -- scripts/build-skills.py scripts/test-build-skills.py scripts/test-adapter-distribution.py scripts/adapter_templates dist/adapters docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md`.
- 2026-06-24: Code-review M4 R1 recorded a clean review receipt and updated lifecycle handoff state; post-review validation passed: `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/ && python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m4-r1.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `git diff --check -- docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/code-review-m4-r1.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`.
- 2026-06-24: M5 validation passed: `python scripts/test-change-metadata-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-skill-validator.py`; `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py`; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/ && python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`; `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/behavior-preservation.md`; `bash scripts/ci.sh --mode explicit --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path skills/workflow/SKILL.md --path docs/workflows.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`.
- 2026-06-24: Code-review M5 R1 recorded a clean review receipt and updated lifecycle handoff state; post-review validation recorded in `change.yaml`.
- 2026-06-24: Explain-change validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/explain-change.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md`; `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/ && python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`; `git diff --check -- docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/explain-change.md docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md docs/plan.md docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`.
- 2026-06-24: Verify validation passed: `python scripts/test-change-metadata-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-skill-validator.py`; `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py`; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/ && python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`; full changed-file selected CI; `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped`.
- 2026-06-24: Post-verify handoff validation passed: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/verify-report.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md`.

## Outcome and retrospective

- Pending implementation and downstream lifecycle gates.

## Readiness

- See `Current Handoff Summary`.
- Readiness is not Done.
