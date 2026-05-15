# Stage Evidence Access Contracts M2: Execution/Review Evidence Access

- Status: done
- Owner: maintainers
- Start date: 2026-05-14
- Last updated: 2026-05-15
- Related issue or PR: PR #60
- Supersedes: none

## Purpose / Big Picture

Implement the approved M2 slice of the stage evidence access contract for execution and review skills.

M1 added the shared evidence access model to `docs/workflows.md` and proposal-side evidence guidance to `proposal` and `proposal-review`. M2 applies the same model to `implement` and `code-review` without changing `plan`, `spec`, runtime enforcement, semantic read auditing, release behavior, adapter packaging, generated-output source policy, or hard token gates.

The goal is to make high-cost execution/review stages start from a smallest sufficient evidence set while preserving implementation safety, independent review rigor, source-of-truth order, validation evidence, and material-finding behavior.

## Source Artifacts

- Proposal: [Stage Evidence Access Contracts for Cost-Bounded Rigor](../proposals/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- Spec: [Stage Evidence Access Contracts for Cost-Bounded Rigor](../../specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- Test spec: [Stage Evidence Access Contracts Test Spec](../../specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md)
- Architecture: not required; the approved spec changes workflow and skill guidance only and has no runtime architecture change.
- M1 plan: [Stage Evidence Access Contracts for Cost-Bounded Rigor](2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- M1 change evidence: `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/`

## Upstream Status Settlement

- Upstream artifact: `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md`
- Review evidence: `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/reviews/spec-review-r1.md`
- Previous status: approved
- New status: approved
- Settlement result: not-needed
- Settlement blocker: none

## Context and Orientation

- `docs/workflows.md` already owns the shared `Stage Evidence Access` model:
  - default evidence;
  - conditional evidence;
  - expansion evidence;
  - bounded discovery;
  - reason recording for substantive out-of-set reads;
  - full-file-read and do-not-under-read escape behavior;
  - separate M1 and M2 validation guidance.
- `skills/implement/SKILL.md` currently has `Quick operating guide`, `Inputs to read`, handoff inspection budget, validation layering, first-pass completeness, and milestone handoff rules.
- `skills/code-review/SKILL.md` currently has `Quick operating guide`, `Inputs to read`, independent-review mode, first-pass checklist coverage, review surface rules, material finding rules, and milestone-aware handoff.
- `scripts/test-skill-validator.py` already contains M1 concept checks for the shared model and proposal-side skills. M2 should add concept checks only for stable `implement` and `code-review` guidance.
- `docs/plan.md` is the lifecycle index. This plan body owns live M2 state once reviewed and activated.

## Non-goals

- Do not update `skills/plan/SKILL.md` in M2.
- Do not update `skills/spec/SKILL.md` unless a later approved spec/test-spec change explicitly promotes it.
- Do not rewrite every skill.
- Do not duplicate the full shared model inside `implement` or `code-review`.
- Do not remove or weaken mandatory implementation or review inputs.
- Do not weaken `code-review`, formal review recording, review-resolution, material-finding, verify, PR, source-of-truth, or release rules.
- Do not add runtime enforcement, semantic read auditing, hard token gates, lifecycle token-cost summary implementation, dynamic benchmark comparison, release validation changes, adapter packaging changes, generated-output source model changes, or public adapter artifact changes.

## Requirements Covered

- `R5`-`R15`: apply the default/conditional/expansion model, bounded discovery boundary, reason recording, full-file-read escape, and do-not-under-read invariant to participating M2 skills.
- `R16`-`R18`: classify existing `implement` and `code-review` inputs and record migration rationale for any removed, downgraded, or reclassified guidance.
- `R26`: keep `implement` and `code-review` evidence guidance in M2 scope rather than M1.
- `R29`: run M2 selected validation against `skills/implement/SKILL.md` and `skills/code-review/SKILL.md`.
- `R30`-`R31`: keep static checks concept-based and avoid exact long paragraph locks.
- `R32`: avoid runtime enforcement, semantic read auditing, hard token gates, lifecycle token-cost summaries, release, adapter, or generated-output source changes.
- `R33`: run static skill token measurement as diagnostic evidence only.
- `R34`: preserve safety-critical review, validation, material-finding, source-of-truth, verify, PR, and release behavior.
- Accepted proposal stage guidance for `implement`: default evidence starts from active plan `Current Handoff Summary`, current milestone section, approved spec, test spec, code/tests named by the milestone, and milestone validation commands; conditional evidence includes architecture/ADR, review-resolution, workflow docs, constitution, and neighboring files when their triggers apply.
- Accepted proposal stage guidance for `code-review`: default evidence starts from actual diff or changed files, approved spec, test spec, current plan milestone, validation evidence, and relevant tests; conditional evidence includes architecture/ADR, review-resolution, change metadata, constitution, and related code paths when their triggers apply.

## Current Handoff Summary

- Current milestone: M2. Implement execution/review evidence guidance
- Current milestone state: closed
- Last reviewed milestone: M2. Implement execution/review evidence guidance
- Review status: `code-review-m2-r1` clean-with-notes with no material findings
- Remaining in-scope implementation milestones: none
- Next stage: none
- Final closeout readiness: complete
- Reason final closeout is or is not ready: PR #60 merged on 2026-05-14 with hosted CI passing; M2 lifecycle closeout is complete.

## Milestones

### M1. M2 Test-Spec Alignment

- Milestone state: planned
- Goal: Update the active stage evidence access test spec so M2 has direct proof requirements for `implement` and `code-review` evidence guidance before skill edits begin.
- Requirements: `R5`-`R18`, `R26`, `R29`-`R34`, accepted proposal `implement` and `code-review` stage guidance.
- Files/components likely touched:
  - `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md`
  - `docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md`
  - `docs/plan.md`
  - change-local metadata under `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/`
- Dependencies:
  - plan-review approval for this plan;
  - approved stage evidence access spec;
  - accepted proposal.
- Tests to add/update:
  - Add M2 test cases or amend existing cases for `implement` and `code-review` local evidence guidance.
  - Add proof expectations for input classification/migration notes for both touched skills.
  - Add selected-validation expectation for `skills/implement/SKILL.md` and `skills/code-review/SKILL.md`.
  - Preserve M1 proof and clarify which checks are M1-only versus M2.
- Implementation steps:
  1. Amend the test spec with M2 `implement` evidence guidance checks.
  2. Amend the test spec with M2 `code-review` evidence guidance checks.
  3. Add M2 validation commands and change-local lifecycle proof expectations.
  4. Create or update `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`.
  5. Update plan progress and validation notes.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `git diff --check -- specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plan.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`
- Expected observable result:
  - The test spec names M2 proof for `implement` and `code-review`.
  - Implementation can proceed without relying on chat-only M2 test expectations.
- Commit message: `M1: align stage evidence access M2 test spec`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [ ] milestone committed
- Risks:
  - The test spec may overfit wording instead of stable concepts.
  - M2 test updates may accidentally broaden into `plan` or `spec` skill edits.
- Rollback/recovery:
  - Keep M2 test cases concept-based.
  - Defer ambiguous semantic proof to manual review instead of brittle validators.

### M2. Implement Execution/Review Evidence Guidance

- Milestone state: planned
- Goal: Add concise evidence-access guidance to `implement` and `code-review`, with concept-level static proof and review-visible input classification.
- Requirements: `R5`-`R18`, `R26`, `R29`-`R34`, accepted proposal `implement` and `code-review` stage guidance.
- Files/components likely touched:
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/`
- Dependencies:
  - M1 closed;
  - active M2 test spec;
  - plan-review approval;
  - no unresolved review-resolution blockers.
- Tests to add/update:
  - Add or update concept checks for `implement` evidence access.
  - Add or update concept checks for `code-review` evidence access.
  - Avoid exact long paragraph checks and broad natural-language scoring.
- Implementation steps:
  1. Add `implement` evidence-access guidance using the accepted proposal's default, conditional, and expansion sets.
  2. Preserve `implement` standing operating instructions, handoff inspection, validation layering, first-pass completeness, plan-update ownership, and milestone handoff rules.
  3. Add `code-review` evidence-access guidance using the accepted proposal's default, conditional, and expansion sets.
  4. Preserve `code-review` independent-review mode, actual-diff grounding, material-finding requirements, review-resolution handoff, and checklist coverage.
  5. Record input classification/migration notes for both touched skills in this plan or change-local evidence.
  6. Add concept-level validator checks only for stable M2 evidence-access concepts.
  7. Run selected M2 validation and static token measurement.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path skills/implement/SKILL.md --path skills/code-review/SKILL.md`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `git diff --check -- skills/implement/SKILL.md skills/code-review/SKILL.md scripts/test-skill-validator.py specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plan.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`
- Expected observable result:
  - `implement` and `code-review` contain concise evidence-access sections.
  - Both skills direct default evidence first, conditional evidence by trigger, and compact reason recording only for substantive out-of-set reads.
  - Existing mandatory operating inputs are preserved or reclassified with rationale.
  - M2 validation covers `implement` and `code-review` without selecting unrelated `plan` or `spec` skill edits.
- Commit message: `M2: add execution review evidence guidance`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Skill wording grows too much.
  - Evidence-access guidance accidentally weakens implementation or review input obligations.
  - Static checks become brittle.
  - Selected validation pulls unrelated surfaces into M2.
- Rollback/recovery:
  - Move shared wording back to `docs/workflows.md` and keep only local default/conditional sets in skills.
  - Restore any downgraded mandatory input unless a reviewed rationale supports the change.
  - Remove brittle validator checks and rely on review-visible manual proof when needed.

### Lifecycle Closeout

- Milestone type: lifecycle-closeout
- Goal: Complete post-implementation review, explanation, verification, and PR handoff after all implementation milestones are closed.
- Requirements: workflow closeout only; no new implementation requirements.
- Dependencies:
  - M1 and M2 closed;
  - required code-review rounds complete;
  - review-resolution closed when material findings exist.
- Validation commands:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - final selected validation named by the active test spec and plan after implementation;
  - `git diff --check -- <changed paths>`.
- Expected observable result:
  - Explain-change records actual diff rationale and validation evidence.
  - Verify establishes branch readiness or records blockers.
  - PR opens only after required gates pass.
- Risks:
  - Plan index and plan body drift.
  - Review-resolution closeout becomes stale after review-driven fixes.
- Rollback/recovery:
  - Keep the plan active until state is synchronized.
  - Do not claim PR readiness until verify checks touched lifecycle surfaces.

## Validation Plan

- Run lifecycle validation for the plan and index after planning.
- After test-spec alignment, validate the test spec, plan, plan index, and change metadata.
- During skill implementation, run the targeted M2 selected validation for `skills/implement/SKILL.md` and `skills/code-review/SKILL.md`.
- Run static skill token measurement after canonical skill changes and record it as diagnostic only.
- Run generated-skill mirror and adapter archive smoke checks if selected validation requires them for canonical skill edits.
- Do not run release validation or adapter packaging validation unless selected validation, the test spec, or implementation changes release/adapter surfaces.

## Risks and Recovery

- Under-reading risk: preserve full-file-read escape and do-not-under-read wording; restore broader evidence permissions if review finds unsafe narrowing.
- Review rigor risk: preserve actual-diff grounding, independent-review mode, material-finding shape, review-resolution handoff, and checklist coverage in `code-review`.
- Implementation safety risk: preserve active-plan handoff inspection, first-pass completeness, validation layering, and plan-update ownership in `implement`.
- Bureaucracy risk: require `Evidence expansion` only when substantive out-of-set evidence is read, not for bounded discovery or default/triggered evidence.
- Scope creep risk: keep `plan`, `spec`, runtime enforcement, lifecycle token summaries, release, adapter, and generated-output source changes out of M2.
- Drift risk: keep `docs/plan.md`, this plan, change metadata, review log, review-resolution, and downstream evidence synchronized before PR handoff.

## Dependencies

- Plan-review must approve this plan before M2 test-spec alignment and implementation.
- M2 test-spec alignment must be active before skill implementation.
- Code-review must pass each implementation milestone before lifecycle closeout.
- Review-resolution is required if material findings are recorded.

## Progress

- [x] 2026-05-14: M1 PR #59 merged; proposal-side evidence access guidance is complete.
- [x] 2026-05-14: draft M2 plan created.
- [x] 2026-05-14: plan-review R1 approved the M2 plan with no material findings.
- [x] plan-review completed.
- [x] 2026-05-14: M2 test-spec alignment added direct proof cases for `implement`, `code-review`, and M2 selected validation/lifecycle coherence.
- [x] 2026-05-14: maintainer approved the M2 test-spec alignment by direct user request.
- [x] M2 test-spec alignment completed.
- [x] 2026-05-14: added concept-level static checks for M2 `implement` and `code-review` evidence-access guidance.
- [x] 2026-05-14: added concise evidence-access sections to `skills/implement/SKILL.md` and `skills/code-review/SKILL.md`.
- [x] 2026-05-14: recorded input classification and migration notes for both touched skills.
- [x] M2 implementation completed.
- [x] 2026-05-14: code-review M2 R1 completed clean-with-notes with no material findings.
- [x] M2 code-review completed.
- [x] 2026-05-14: explain-change recorded durable rationale in `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/explain-change.md`.
- [x] explain-change completed.
- [x] 2026-05-14: final local verify passed selector-backed validation and confirmed branch-ready local evidence. Hosted CI has not been observed yet and is not claimed as passed.
- [x] verify completed.
- [x] 2026-05-14: PR #60 opened at `https://github.com/xiongxianfei/rigorloop/pull/60`. Hosted CI is pending and not claimed as passed.
- [x] 2026-05-15: PR #60 merge confirmed at `87101ec42582fde020cfe600193ebfea183669e0`; hosted CI passed.
- [x] PR handoff completed.

## Decision Log

- 2026-05-14: Start M2 as a separate plan instead of reopening the completed M1 plan. Reason: M1 intentionally closed proposal-side scope and deferred execution/review evidence access.
- 2026-05-14: Include a test-spec alignment milestone before skill edits. Reason: the current test spec is M1-centered and should name M2 proof before implementation changes `implement` and `code-review`.
- 2026-05-14: Keep `plan` as future-slice design context. Reason: the approved spec says `plan` remains future-slice unless later promoted.
- 2026-05-14: Update the existing active stage evidence access test spec instead of creating a separate M2 test spec. Reason: the approved spec is unchanged and the existing test spec remains the active proof-planning surface for the same stage evidence access contract.

## Surprises and Discoveries

- None yet.

## Input Classification and Migration Notes

No mandatory operating input was removed. The touched skills now separate standing operating instructions from task evidence.

| Skill | Existing input | Expected classification | Rationale |
|---|---|---|---|
| `implement` | `AGENTS.md` | standing operating instructions | Preserves repository operating context. |
| `implement` | `CONSTITUTION.md` | standing operating instructions and conditional governance/source-of-truth evidence | Preserves governance while avoiding routine broad reads when not triggered. |
| `implement` | active plan/current milestone | default task evidence | Owns implementation scope and current handoff. |
| `implement` | feature spec and test spec | default task evidence | Owns contract and proof obligations. |
| `implement` | code/tests listed in milestone | default task evidence | Needed to implement the approved slice. |
| `implement` | architecture/ADR | conditional task evidence | Read when milestone touches architecture boundaries. |
| `implement` | neighboring files | conditional task evidence | Read when needed to follow existing patterns. |
| `code-review` | actual diff or changed files | default task evidence | Owns review surface. |
| `code-review` | spec, test spec, plan milestone, validation evidence, relevant tests | default task evidence | Needed for independent implementation review. |
| `code-review` | architecture/ADR, review-resolution, change metadata, constitution, related code paths | conditional task evidence | Read when touched, reviewing fixes, lifecycle state matters, governance matters, or diff depends on related paths. |

## Validation Notes

- Planning validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md`
  - `git diff --check -- docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plan.md`
- Plan-review R1 recorded no material findings in `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/reviews/plan-review-r1.md`.
- M2 test-spec alignment validation passed:
  - `python scripts/select-validation.py --mode explicit --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `git diff --check -- specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plan.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`
- M2 test-spec alignment approval recorded in `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md`.
- Test-first proof:
  - `python scripts/test-skill-validator.py` failed before M2 skill edits because the new `test_stage_evidence_access_m2_execution_review_skills` checks were not yet satisfied.
- M2 implementation validation passed:
  - `python scripts/select-validation.py --mode explicit --path skills/implement/SKILL.md --path skills/code-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path scripts/test-skill-validator.py --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/measure-skill-tokens.py`
  - `git diff --check -- skills/implement/SKILL.md skills/code-review/SKILL.md scripts/test-skill-validator.py specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plan.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`
- Static token measurement: 23 skills, 235521 bytes, 58868 estimated tokens. `implement` measured 4268 estimated tokens; `code-review` measured 5054 estimated tokens. Measurement is diagnostic only.
- Code-review M2 R1 recorded `clean-with-notes` with no material findings in `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/reviews/code-review-m2-r1.md`. No review-resolution is required.
- Post-review recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/review-log.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/reviews/code-review-m2-r1.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`
- Explain-change recorded the durable rationale for the M2 branch diff and handed off to `verify`.
- Post-explain-change validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/explain-change.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`
- Final local verify passed:
  - `python scripts/select-validation.py --mode explicit --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/explain-change.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/explain-change.md --path docs/plan.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path skills/code-review/SKILL.md --path skills/implement/SKILL.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md`
  - `python scripts/measure-skill-tokens.py`
  - `git diff --check -- specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md skills/implement/SKILL.md skills/code-review/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plan.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`
- Final selector selected `skills.validate`, `skills.regression`, `skills.generation_regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`; `broad_smoke_required` was `false`.
- CI workflow scope reviewed in `.github/workflows/ci.yml`. Hosted CI has not been observed in this local verify and is not claimed as passed.
- No standalone `verify-report.md` was added. No required manual proof was used; automated proof is recorded in this plan, `change.yaml`, and `explain-change.md`.
- PR handoff completed:
  - PR #60 opened: `https://github.com/xiongxianfei/rigorloop/pull/60`
  - Hosted CI is pending and not claimed as passed.
- PR #60 merge closeout:
  - PR #60 merged on 2026-05-14 at `87101ec42582fde020cfe600193ebfea183669e0`.
  - Hosted CI `ci` completed successfully before merge.

## Outcome and Retrospective

- Done. PR #60 merged on 2026-05-14 after hosted CI passed. M2 added execution/review evidence access guidance to `implement` and `code-review`, concept-level static proof, durable review/explain/verify evidence, and PR handoff without updating `plan`, `spec`, runtime enforcement, hard token gates, release behavior, adapter packaging, generated-output source policy, or dynamic benchmarks.

## Readiness

- See `Current Handoff Summary`.
