# Stage Evidence Access Contracts M3/M4: Static Validation And Measurement

- Status: active
- Owner: maintainers
- Start date: 2026-05-15
- Last updated: 2026-05-15
- Related issue or PR: PR #61
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

- Current milestone: Lifecycle closeout
- Current milestone state: PR #61 opened; hosted CI in progress
- Last reviewed milestone: M4. Measurement and size-delta recording
- Review status: code-review-m4-r1 clean-with-notes; no material findings; no review-resolution required
- Remaining in-scope implementation milestones: none
- Next stage: PR review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: PR #61 is open and hosted CI is in progress; final closeout waits for PR review, hosted CI completion, and merge confirmation.

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
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/plan.md docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement`
- Expected observable result:
  - The active test spec names M3/M4 proof without relying on chat-only expectations.
  - M3/M4 remains scoped to validation and measurement.
- Commit message: `M0: align stage evidence access M3 M4 test spec`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Test-spec alignment may duplicate existing T6/T10 coverage.
  - M4 measurement expectations may accidentally become a hard gate.
- Rollback/recovery:
  - Keep new proof cases as references to existing T6/T10/T11/T14 where sufficient.
  - State explicitly that measurement is diagnostic only.

### M3. Static Validation Audit And Gap Fill

- Milestone state: closed
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
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Checks can become brittle if they assert long prose.
  - Duplicated checks can increase maintenance cost without improving safety.
- Rollback/recovery:
  - Remove brittle assertions and keep manual review guidance.
  - Prefer short stable phrases and section presence checks.

### M4. Measurement And Size-Delta Recording

- Milestone state: closed
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
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
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
- [x] 2026-05-15: plan-review R1 approved the M3/M4 plan with no material findings.
- [x] plan-review completed.
- [x] 2026-05-15: M3/M4 test-spec alignment added explicit M3 validator audit/gap-fill and M4 measurement/size-delta proof cases.
- [x] 2026-05-15: M3/M4 test-spec alignment approved by maintainer.
- [x] M0 test-spec alignment completed.
- [x] 2026-05-15: M3 audit found current concept checks sufficient; no `scripts/test-skill-validator.py` changes needed.
- [x] M3 static validation implementation completed and handed to code-review.
- [x] 2026-05-15: code-review M3 R1 recorded clean-with-notes with no material findings.
- [x] 2026-05-15: M4 static measurement recorded 23 skills, 235521 bytes, and 58868 estimated tokens, unchanged from the M2 merged baseline.
- [x] M4 measurement implementation completed and handed to code-review.
- [x] 2026-05-15: code-review M4 R1 recorded clean-with-notes with no material findings.
- [x] code-review completed for all implementation milestones.
- [x] 2026-05-15: explain-change recorded in `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md`.
- [x] explain-change completed.
- [x] 2026-05-15: final local verify passed and branch-ready evidence recorded in `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/verify-report.md`.
- [x] verify completed.
- [x] 2026-05-15: PR #61 opened at `https://github.com/xiongxianfei/rigorloop/pull/61`; hosted CI is in progress and not claimed as passed.
- [x] PR handoff completed.

## Decision Log

- 2026-05-15: Plan M3/M4 as a separate active plan instead of reopening M1 or M2. Reason: M1 and M2 are merged implementation slices; M3/M4 are narrower validation and measurement follow-through work.
- 2026-05-15: Include M0 test-spec alignment before M3/M4 implementation. Reason: the current test spec names T6/T10 generally, but the active proof surface should explicitly route M3/M4 before implementation.
- 2026-05-15: Treat existing static checks as candidates for no-change rationale before adding new tests. Reason: the proposal says to add static checks only if needed.
- 2026-05-15: Update the existing active stage evidence access test spec instead of creating a separate M3/M4 test spec. Reason: the approved spec is unchanged and the existing test spec remains the active proof-planning surface for the same stage evidence access contract.
- 2026-05-15: Maintainer approved the M3/M4 test-spec alignment by direct user request. Reason: the active proof surface is ready to support M3 static validation audit/gap-fill and M4 measurement implementation.
- 2026-05-15: M3 did not change `scripts/test-skill-validator.py`. Reason: `test_stage_evidence_access_contract_guidance`, `test_stage_evidence_access_proposal_side_skills`, and `test_stage_evidence_access_m2_execution_review_skills` already cover `Evidence access`, default evidence, conditional evidence, reason recording, bounded discovery before broad reads, and full-file-read escape behavior.
- 2026-05-15: Close M3 after clean code-review and hand off to M4. Reason: `code-review-m3-r1` recorded no material findings, no review-resolution is required, and M4 is the only remaining implementation milestone.
- 2026-05-15: M4 measurement is unchanged from the M2 merged baseline. Reason: M3 changed only validator/lifecycle evidence and did not change canonical skill text.
- 2026-05-15: Close M4 after clean code-review and hand off to explain-change. Reason: `code-review-m4-r1` recorded no material findings, no review-resolution is required, and no implementation milestones remain.
- 2026-05-15: Record explain-change and hand off to verify. Reason: all implementation milestones have clean code-review evidence and no review-resolution is required.
- 2026-05-15: Record final local verify and hand off to PR. Reason: selected validation, lifecycle validation, review-artifact validation, skill validation, generated-skill checks, static measurement, and diff whitespace checks passed.
- 2026-05-15: Open PR #61 and keep the plan active until hosted CI and merge closeout are observed. Reason: PR handoff is complete, but hosted CI is still in progress and final lifecycle Done is not yet true.

## Surprises and Discoveries

- M3 audit found the M1/M2 static validator work already satisfies the M3 concept list, so adding new assertions would duplicate existing coverage without reducing risk.

## Validation Notes

- Planning validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
- Plan-review R1 recorded no material findings in `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/plan-review-r1.md`.
- M3/M4 test-spec alignment validation passed:
  - `python scripts/select-validation.py --mode explicit --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/plan.md docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement`
- M3/M4 test-spec alignment approved by maintainer on 2026-05-15.
- M3 static validation audit and gap-fill validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path scripts/test-skill-validator.py --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path scripts/test-skill-validator.py --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `git diff --check -- scripts/test-skill-validator.py specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/plan.md docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement`

## M3 Static Validation Audit

| Concept | Existing proof | Result |
|---|---|---|
| Evidence access section presence | `test_stage_evidence_access_proposal_side_skills` and `test_stage_evidence_access_m2_execution_review_skills` assert `## Evidence access` in each participating skill. | Covered |
| Default evidence | The proposal-side and M2 skill tests assert `Default evidence:` plus required stage-local default categories. | Covered |
| Conditional evidence | The proposal-side and M2 skill tests assert `Conditional evidence:` plus required trigger-based conditional categories. | Covered |
| Reason recording | The proposal-side and M2 skill tests assert compact reason recording only for substantive out-of-set reads. | Covered |
| Bounded discovery / bounded evidence before broad reads | `test_stage_evidence_access_contract_guidance` asserts bounded discovery examples and broad authoritative-document search limits; each participating skill asserts bounded discovery is not evidence expansion. | Covered |
| Full-file-read escape behavior | `test_stage_evidence_access_contract_guidance` asserts full-file reads remain allowed; participating skill tests assert full-file language is present. | Covered |

M3 no-change rationale: current concept checks are sufficient and passed. No `scripts/test-skill-validator.py` edits were made because additional checks would be duplicative or phrase-locking.
- Code-review M3 R1 recorded clean-with-notes with no material findings in `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m3-r1.md`.
- M4 static measurement validation passed:
  - `python scripts/measure-skill-tokens.py` recorded 23 skills, 235521 bytes, and 58868 estimated tokens.
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `git diff --check -- scripts/test-skill-validator.py specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/plan.md docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement`

## M4 Static Measurement

| Measurement | M2 merged baseline | M4 result | Delta |
|---|---:|---:|---:|
| Skills measured | 23 | 23 | 0 |
| Total bytes | 235521 | 235521 | 0 |
| Estimated tokens | 58868 | 58868 | 0 |

M4 measurement interpretation: unchanged. M3 did not edit canonical skill text, so static skill size was expected to remain unchanged. This measurement is diagnostic and warning-only; it does not introduce a hard token gate, dynamic benchmark requirement, release validation change, adapter packaging change, or generated-output source-model change.
- Code-review M4 R1 recorded clean-with-notes with no material findings in `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m4-r1.md`.
- Explain-change recorded in `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md`.
- Explain-change validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/`
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md --path docs/plan.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/plan.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/review-log.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m3-r1.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m4-r1.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement`
- Final local verify passed and recorded in `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/verify-report.md`.
- Verify validation passed:
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/review-log.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/plan-review-r1.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m3-r1.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m4-r1.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/review-log.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m3-r1.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m4-r1.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/plan-review-r1.md --path docs/plan.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement`
- PR handoff completed:
  - PR #61 opened: `https://github.com/xiongxianfei/rigorloop/pull/61`
  - Hosted CI status at handoff: `ci` in progress; not claimed as passed.
- CI follow-up:
  - PR #61 hosted CI failed because `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/pr.md` was classified as `change-local-unsupported`.
  - The unsupported tracked PR body artifact was removed; the GitHub PR body remains the PR review surface.

## Outcome and Retrospective

- Local branch content is branch-ready and PR #61 is open for review.
- Hosted CI for this branch is in progress and not claimed as passed.

## Readiness

- See `Current Handoff Summary`.
