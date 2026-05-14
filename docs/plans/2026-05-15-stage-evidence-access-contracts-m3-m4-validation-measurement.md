# Stage Evidence Access Contracts M3/M4: Static Validation And Measurement

- Status: active
- Owner: maintainers
- Start date: 2026-05-15
- Last updated: 2026-05-15
- Related issue or PR: none yet
- Supersedes: none

## Purpose / Big Picture

Continue the accepted stage evidence access contracts rollout after M1 proposal-side guidance and M2 execution/review guidance are merged.

This plan covers:

- M3 static validation: audit and tighten concept-based static checks only where existing coverage is insufficient to prevent accidental removal of stage evidence access guidance.
- M4 measurement: run static skill token measurement and record whether skill size increased, decreased, or stayed unchanged.

The work is intentionally narrow. M3/M4 should not reopen the evidence-access model, rewrite additional skills, add runtime enforcement, create hard token gates, or introduce dynamic benchmark requirements.

## Source Artifacts

- Proposal: [Stage Evidence Access Contracts for Cost-Bounded Rigor](../proposals/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- Spec: [Stage Evidence Access Contracts for Cost-Bounded Rigor](../../specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- Test spec: [Stage Evidence Access Contracts Test Spec](../../specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md)
- M1 plan: [Stage Evidence Access Contracts for Cost-Bounded Rigor](2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- M2 plan: [Stage Evidence Access Contracts M2: Execution/Review Evidence Access](2026-05-14-stage-evidence-access-contracts-m2-execution-review.md)
- Architecture: not required; this is validation and measurement work for repository guidance and skill contracts, with no runtime architecture change.

## Upstream Status Settlement

- Upstream artifact: `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md`
- Review evidence: `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/reviews/spec-review-r1.md`
- Previous status: approved
- New status: approved
- Settlement result: not-needed
- Settlement blocker: none

## Context and Orientation

- M1 merged in PR #59 and added the shared model to `docs/workflows.md` plus proposal-side evidence guidance.
- M2 merged in PR #60 and added execution/review evidence guidance to `implement` and `code-review`.
- Existing static checks already include:
  - shared workflow evidence access checks;
  - proposal and proposal-review local evidence checks;
  - implement and code-review local evidence checks.
- M1 static measurement recorded 23 skills, 233054 bytes, and 58252 estimated tokens.
- M2 static measurement recorded 23 skills, 235521 bytes, and 58868 estimated tokens.
- M3 should inspect existing validator coverage before adding checks. If current concept checks already protect the relevant sections, implementation should record a no-change rationale instead of adding brittle tests.
- M4 should record diagnostic measurement in the active plan, change metadata, and explain-change. A separate token-cost report is not required unless implementation creates a broader measurement artifact on purpose.

## Non-goals

- Do not update additional skills solely to satisfy M3/M4.
- Do not promote `plan` evidence guidance in this slice.
- Do not add runtime enforcement or semantic read auditing.
- Do not add hard token gates or fail builds on token totals.
- Do not run dynamic token benchmarks unless the test-spec alignment explicitly promotes them.
- Do not implement lifecycle token-cost summaries.
- Do not change release validation, adapter packaging, generated-output source policy, or public adapter artifacts.
- Do not weaken safety-critical review, validation, material-finding, source-of-truth, verify, PR, or release behavior.

## Requirements Covered

- `R30`: static checks, when added, are concept-based and do not require exact long paragraphs across skills.
- `R31`: concept checks may look for evidence-access section presence, default evidence, conditional evidence, reason recording, bounded evidence before broad reads, and full-file-read escape behavior.
- `R32`: no runtime enforcement, semantic read auditing, hard token gates, lifecycle token-cost summary implementation, release validation changes, adapter packaging changes, or generated-output source model changes.
- `R33`: static skill token measurement remains diagnostic and warning-only.
- `R34`: safety-critical formal review, validation, material-finding, source-of-truth, verify, PR, and release rules remain intact.
- Proposal M3: add static checks only if needed to prevent accidental removal; keep checks concept-based.
- Proposal M4: run static token measurement, record whether skill size increased or decreased, and defer dynamic benchmark comparison unless the plan/test-spec requires it.

## Current Handoff Summary

- Current milestone: Planning M3/M4 static validation and measurement
- Current milestone state: planned
- Last reviewed milestone: none for this M3/M4 plan
- Review status: not reviewed
- Remaining in-scope implementation milestones: M0. M3/M4 test-spec alignment; M3. Static validation audit and gap fill; M4. Measurement and size-delta recording
- Next stage: plan-review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: the plan is newly drafted and still needs plan-review, test-spec alignment, implementation, code-review, explain-change, verify, and PR handoff.

## Milestones

### M0. M3/M4 Test-Spec Alignment

- Milestone state: planned
- Goal: Align the active stage evidence access test spec so M3/M4 proof expectations are explicit before validator or measurement work begins.
- Requirements: `R30`-`R34`, proposal M3/M4 rollout.
- Files/components likely touched:
  - `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md`
  - `docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
- Dependencies:
  - plan-review approval for this plan;
  - approved stage evidence access spec;
  - merged M1 and M2 evidence-access slices.
- Tests to add/update:
  - Add or adjust test-spec cases for M3 static validation audit/gap fill.
  - Add or adjust test-spec cases for M4 static measurement and size-delta recording.
  - Preserve M1/M2 proof cases and avoid broadening M3/M4 into `plan` skill guidance or dynamic benchmarks.
- Implementation steps:
  1. Add M3/M4 proof expectations to the active test spec.
  2. Clarify that existing concept checks may be sufficient when implementation records a no-change rationale.
  3. Clarify measurement comparison baselines: current M2 measurement, any M3 canonical skill changes, and final M4 measurement.
  4. Update change metadata and plan validation notes.
- Validation commands:
  - `python scripts/select-validation.py --mode explicit --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `git diff --check -- specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/plan.md docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement`
- Expected observable result:
  - The active test spec names M3/M4 proof without relying on chat-only expectations.
  - M3/M4 remains scoped to validation and measurement.
- Commit message: `M0: align stage evidence access M3 M4 test spec`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Test-spec alignment may duplicate existing T6/T10 coverage.
  - M4 measurement expectations may accidentally become a hard gate.
- Rollback/recovery:
  - Keep new proof cases as references to existing T6/T10/T11/T14 where sufficient.
  - State explicitly that measurement is diagnostic only.

### M3. Static Validation Audit And Gap Fill

- Milestone state: planned
- Goal: Confirm existing stage evidence access static checks protect the M1/M2 evidence guidance and add only missing concept-level checks.
- Requirements: `R30`-`R32`, `R34`, proposal M3.
- Files/components likely touched:
  - `scripts/test-skill-validator.py`
  - `docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md`
  - `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
- Dependencies:
  - M0 test-spec alignment complete;
  - no unresolved plan-review findings.
- Tests to add/update:
  - Add concept-level checks only when existing checks do not cover required evidence-access section presence or stable concepts.
  - Avoid exact long paragraph checks, semantic scoring, or duplicate assertions that add maintenance cost without risk reduction.
- Implementation steps:
  1. Audit current `test_stage_evidence_access_contract_guidance`, `test_stage_evidence_access_proposal_side_skills`, and `test_stage_evidence_access_m2_execution_review_skills`.
  2. Map coverage against M3 concept list: `Evidence access`, default evidence, conditional evidence, reason recording, bounded evidence before broad reads, and full-file escape behavior.
  3. If gaps exist, add focused assertions to `scripts/test-skill-validator.py`.
  4. If no gaps exist, record a no-change rationale in this plan and change metadata.
  5. Run validator regression and selected validation for touched surfaces.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path scripts/test-skill-validator.py --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path scripts/test-skill-validator.py --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `git diff --check -- scripts/test-skill-validator.py specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/plan.md docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement`
- Expected observable result:
  - Static validation either has focused M3 gap-fill checks or a reviewed no-change rationale that current checks are sufficient.
  - No brittle exact long paragraph checks are added.
- Commit message: `M3: validate stage evidence access concepts`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Checks can become brittle if they assert long prose.
  - Duplicated checks can increase maintenance cost without improving safety.
- Rollback/recovery:
  - Remove brittle assertions and keep manual review guidance.
  - Prefer short stable phrases and section presence checks.

### M4. Measurement And Size-Delta Recording

- Milestone state: planned
- Goal: Run static skill token measurement and record whether skill size increased, decreased, or stayed unchanged relative to the current M2 merged baseline.
- Requirements: `R33`, `R34`, proposal M4.
- Files/components likely touched:
  - `docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md`
  - `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md` later in lifecycle
  - optional `scripts/test-skill-validator.py` only if M3 added checks before measurement
- Dependencies:
  - M3 static validation audit/gap fill complete;
  - no unresolved review-resolution blockers.
- Tests to add/update:
  - No new tests expected unless measurement recording exposes a validation gap.
  - Static token measurement remains diagnostic and warning-only.
- Implementation steps:
  1. Run `python scripts/measure-skill-tokens.py`.
  2. Compare the result against the M2 merged baseline: 23 skills, 235521 bytes, 58868 estimated tokens.
  3. If M3 changed canonical skill text, record per-skill deltas for touched skills.
  4. If M3 changed only validator/lifecycle artifacts, record that static skill size is expected to remain unchanged and verify the measurement.
  5. Record measurement in plan validation notes and change metadata; summarize in explain-change later.
- Validation commands:
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `git diff --check -- scripts/test-skill-validator.py specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/plan.md docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement`
- Expected observable result:
  - Measurement is recorded with an increase/decrease/unchanged statement.
  - No hard token threshold or dynamic benchmark requirement is introduced.
- Commit message: `M4: measure stage evidence access skill size`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Measurement may be mistaken for a release gate.
  - Dynamic benchmark work may creep into this slice.
- Rollback/recovery:
  - Keep measurement as recorded diagnostic evidence only.
  - Defer dynamic benchmarks unless a later approved plan/test-spec requires them.

### Lifecycle Closeout

- Milestone type: lifecycle-closeout
- Goal: Complete code-review, explain-change, verify, PR handoff, and final lifecycle state after M3/M4 implementation milestones are closed.
- Requirements: workflow closeout only; no new implementation requirements.
- Dependencies:
  - M0, M3, and M4 closed;
  - required code-review rounds complete;
  - review-resolution closed when material findings exist.
- Validation commands:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - final selected validation named by the active test spec and plan after implementation;
  - `git diff --check -- <changed paths>`.
- Expected observable result:
  - Explain-change records static validation and measurement rationale.
  - Verify establishes branch readiness or records blockers.
  - PR opens only after required gates pass.
- Risks:
  - Plan index and plan body drift.
  - Measurement evidence becomes stale after review-driven changes.
- Rollback/recovery:
  - Re-run measurement after any canonical skill change.
  - Keep the plan active until state is synchronized.

## Validation Plan

- Run lifecycle validation for this plan, the M2 closeout update, and `docs/plan.md` after planning.
- After test-spec alignment, validate the test spec, plan, plan index, and change metadata.
- During M3, run `scripts/test-skill-validator.py` and selected validation for `scripts/test-skill-validator.py` plus lifecycle surfaces.
- During M4, run `scripts/measure-skill-tokens.py` and record the result as diagnostic.
- Run `scripts/validate-skills.py` when canonical skills are touched or as part of final measurement closeout.
- Do not run release validation, dynamic token benchmarks, or adapter packaging validation unless selected validation or a later approved artifact requires it.

## Risks and Recovery

- Static-check brittleness risk: keep checks concept-based and short; remove brittle checks if review finds wording lock-in.
- Scope creep risk: do not promote `plan` skill evidence guidance, runtime enforcement, lifecycle token-cost summaries, release changes, adapter packaging, generated-output source changes, or dynamic benchmarks.
- Measurement interpretation risk: explicitly record static skill token measurement as diagnostic only.
- Drift risk: keep `docs/plan.md`, this plan, change metadata, review log, review-resolution, and downstream evidence synchronized before PR handoff.

## Dependencies

- PR #60 must be merged and M2 lifecycle state must be closed before this plan is relied on for implementation.
- Plan-review must approve this plan before M0 test-spec alignment and M3/M4 implementation.
- M0 test-spec alignment must be active before M3/M4 implementation.
- Code-review must pass M3/M4 implementation before lifecycle closeout.
- Review-resolution is required if material findings are recorded.

## Progress

- [x] 2026-05-15: PR #60 merge and hosted CI success confirmed for M2.
- [x] 2026-05-15: draft M3/M4 plan created.
- [ ] plan-review completed.
- [ ] M0 test-spec alignment completed.
- [ ] M3 static validation completed.
- [ ] M4 measurement completed.
- [ ] code-review completed.
- [ ] explain-change completed.
- [ ] verify completed.
- [ ] PR handoff completed.

## Decision Log

- 2026-05-15: Plan M3/M4 as a separate active plan instead of reopening M1 or M2. Reason: M1 and M2 are merged implementation slices; M3/M4 are narrower validation and measurement follow-through work.
- 2026-05-15: Include M0 test-spec alignment before M3/M4 implementation. Reason: the current test spec names T6/T10 generally, but the active proof surface should explicitly route M3/M4 before implementation.
- 2026-05-15: Treat existing static checks as candidates for no-change rationale before adding new tests. Reason: the proposal says to add static checks only if needed.

## Surprises and Discoveries

- None yet.

## Validation Notes

- Planning validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`

## Outcome and Retrospective

- Pending completion.

## Readiness

- See `Current Handoff Summary`.
