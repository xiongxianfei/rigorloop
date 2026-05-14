# Stage Evidence Access Contracts for Cost-Bounded Rigor

- Status: active
- Owner: maintainers
- Start date: 2026-05-14
- Last updated: 2026-05-14
- Related issue or PR: none yet
- Supersedes: none

## Purpose / Big Picture

Implement the approved M1 contract for stage evidence access guidance without expanding into M2 execution/review guidance.

The plan turns the approved spec into a small reviewable slice: add the shared operational model to `docs/workflows.md`, add concise stage-local evidence-access guidance to `proposal` and `proposal-review`, update `spec` only if the implementation confirms immediate proposal-to-spec handoff needs it, and validate the changed guidance without selecting deferred M2 paths.

## Source Artifacts

- Proposal: [Stage Evidence Access Contracts for Cost-Bounded Rigor](../proposals/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- Spec: [Stage Evidence Access Contracts for Cost-Bounded Rigor](../../specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- Architecture: not required; the approved spec defines workflow/skill guidance only and no runtime architecture change.
- Test spec: [Stage Evidence Access Contracts Test Spec](../../specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md)
- Proposal-review evidence: [proposal-review-r3](../changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/reviews/proposal-review-r3.md)
- Spec-review evidence: [spec-review-r1](../changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/reviews/spec-review-r1.md)
- Change metadata: [change.yaml](../changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/change.yaml)

## Context and Orientation

- `docs/workflows.md` owns the full operational evidence-access model and bounded-read lookup behavior.
- `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` own concise local evidence-access guidance for M1.
- `skills/spec/SKILL.md` is conditional M1 scope only if implementation confirms the immediate proposal-to-spec handoff needs the same local rule.
- `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, and `skills/plan/SKILL.md` are out of M1 scope.
- `scripts/test-skill-validator.py` is the likely static proof surface when implementation adds stable concept checks.
- `scripts/select-validation.py` must be exercised with M1 paths only; M2 paths are validated only when M2 runs.
- Existing related specs already cover cost-bounded rigor M1/M2, selected skill reminders, and normalized skill-contract evidence-reading behavior. This plan implements only the newer stage-evidence-access contract.

## Non-goals

- Do not implement M2 `implement` or `code-review` evidence guidance in M1.
- Do not update `plan` in M1.
- Do not rewrite every skill.
- Do not add runtime enforcement or semantic read auditing.
- Do not add hard token gates.
- Do not implement lifecycle token-cost summaries.
- Do not implement full progressive-loading work.
- Do not change validation-selector behavior beyond scoped selected validation guidance.
- Do not change release validation, adapter packaging, generated-output source policy, or public adapter artifacts.
- Do not replace stage artifacts with chat-only summaries.

## Requirements Covered

- `R1`: M1 shared model in `docs/workflows.md`.
- `R2`: concise evidence-access guidance in `proposal` and `proposal-review`.
- `R3`: optional `spec` guidance only when immediate handoff needs it.
- `R4`: no M1 edits to `implement`, `code-review`, or `plan`.
- `R5`-`R15`: model shape, bounded discovery, expansion recording, broad-search avoidance, full-file-read escape, and do-not-under-read behavior.
- `R16`-`R18`: input-contract preservation and migration rationale for touched skills.
- `R19`-`R24`: stage-specific evidence guidance for `proposal`, `proposal-review`, and optional `spec`.
- `R25`-`R29`: future-slice boundaries and M1/M2 validation separation.
- `R30`-`R31`: concept-based static checks when added.
- `R32`-`R34`: non-goals, diagnostic token measurement, and safety-critical rule preservation.

## Current Handoff Summary

- Current milestone: M1. Proposal-side stage evidence access guidance
- Current milestone state: closed
- Last reviewed milestone: M1. Proposal-side stage evidence access guidance
- Review status: `code-review-m1-r2` clean-with-notes with no open material findings
- Remaining in-scope implementation milestones: none
- Next stage: explain-change
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M1 is closed after clean code-review and closed review-resolution, but explain-change and final verify have not run, and PR handoff is not prepared.

## Milestones

### M1. Proposal-Side Stage Evidence Access Guidance

- Milestone state: closed
- Goal: Implement the M1 stage evidence access contract in shared workflow guidance and proposal-side skills without selecting deferred M2 surfaces.
- Requirements: `R1`-`R24`, `R27`-`R34`
- Files/components likely touched:
  - `docs/workflows.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md` only if immediate proposal-to-spec handoff needs it
  - `scripts/test-skill-validator.py` only if stable concept checks are needed
  - change-local evidence under `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/`
- Dependencies:
  - accepted proposal;
  - approved spec;
  - approved plan-review before implementation;
  - active test spec before implementation.
- Tests to add/update:
  - Add or update focused static checks only for stable evidence-access concepts if implementation adds testable wording.
  - Avoid broad natural-language scoring or exact long paragraph checks.
- Implementation steps:
  1. Audit current `docs/workflows.md`, `proposal`, and `proposal-review` wording for existing bounded-evidence and full-file-read guidance.
  2. Add the shared stage evidence access model to `docs/workflows.md`.
  3. Add concise local default/conditional/expansion evidence guidance to `proposal`.
  4. Add concise local default/conditional/expansion evidence guidance to `proposal-review`.
  5. Decide whether `spec` needs an M1 local rule for immediate proposal-to-spec handoff. If yes, update it and include the path in selected validation; if no, record no-change rationale.
  6. Record input-classification or migration rationale for each touched skill when input guidance is removed, downgraded, or reclassified.
  7. Add concept-level static checks only if stable enough to avoid brittle wording locks.
  8. Run targeted M1 validation and static token measurement.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`
  - If `skills/spec/SKILL.md` changes, add `--path skills/spec/SKILL.md` to the selected validation command.
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/change.yaml`
  - `git diff --check -- docs/workflows.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md skills/spec/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md docs/plan.md docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording`
- Expected observable result:
  - The shared model is visible in `docs/workflows.md`.
  - `proposal` and `proposal-review` contain concise evidence-access guidance.
  - `spec` is either updated with scoped rationale or explicitly left unchanged with rationale.
  - Validation stays scoped to M1 paths and does not select `implement` or `code-review`.
- Commit message: `M1: add proposal-side stage evidence access guidance`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Skill wording grows too much.
  - Static checks become brittle.
  - Input obligations are accidentally downgraded.
  - Selected validation pulls in M2 paths.
- Rollback/recovery:
  - Move shared wording back to `docs/workflows.md` if skills grow too large.
  - Remove brittle static checks and rely on review evidence if concept checks are unstable.
  - Restore any downgraded input guidance unless a reviewed rationale supports the change.
  - Split accidental M2 edits into a later plan revision or remove them from M1.

### Lifecycle Closeout

- Milestone type: lifecycle-closeout
- Goal: Complete required post-implementation evidence and handoff after all implementation milestones are closed.
- Requirements: workflow closeout only; no new implementation requirements.
- Dependencies:
  - M1 closed;
  - any code-review findings resolved or explicitly dispositioned.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/change.yaml`
  - final selected validation named by the test spec or active plan after implementation
  - `git diff --check -- <changed paths>`
- Expected observable result:
  - Explain-change records the actual diff rationale and validation evidence.
  - Verify passes or records blockers.
  - PR handoff is prepared only after required gates pass.
- Risks:
  - Plan index and plan body drift.
  - Review-resolution closeout is stale after code-review.
- Rollback/recovery:
  - Keep the plan active until state is synchronized.
  - Do not claim PR readiness until verify checks all touched lifecycle surfaces.

## Validation Plan

- Run the smallest relevant proof first: skill validator and explicit selected validation for M1 paths.
- Add `skills/spec/SKILL.md` to selected validation only if the implementation touches it.
- Run static token measurement after canonical skill changes.
- Run review-artifact, change-metadata, and artifact-lifecycle validation when change-local or lifecycle artifacts are touched.
- Do not run release or adapter validation unless selected validation, the test spec, or implementation changes release/adapter surfaces.

## Risks and Recovery

- Under-reading risk: preserve full-file-read escape and do-not-under-read wording; restore broader evidence permissions if review finds unsafe narrowing.
- Bureaucracy risk: do not require `Evidence expansion` output for bounded discovery or normal default/conditional evidence.
- Scope creep risk: reject or defer `implement`, `code-review`, `plan`, runtime enforcement, lifecycle token summaries, progressive-loading, release, and adapter work from M1.
- Drift risk: keep `docs/plan.md`, this plan, change metadata, review log, review-resolution, and downstream evidence synchronized before PR handoff.

## Dependencies

- Spec status must be approved before planning reliance. Completed in this planning change.
- Plan-review must approve this plan before test-spec authoring or implementation.
- A test spec must be active before implementation.
- M1 implementation must pass code-review before lifecycle closeout.

## Progress

- [x] 2026-05-14: accepted proposal settled from proposal-review evidence.
- [x] 2026-05-14: draft spec authored.
- [x] 2026-05-14: spec-review approved with no material findings.
- [x] 2026-05-14: spec status settled to approved for planning.
- [x] 2026-05-14: draft execution plan created.
- [x] 2026-05-14: plan-review approved with no material findings.
- [x] 2026-05-14: test spec created and activated.
- [x] 2026-05-14: M1 implementation started.
- [x] 2026-05-14: added concept-level static checks for the shared evidence-access model and proposal-side skill guidance.
- [x] 2026-05-14: added shared stage evidence access guidance to `docs/workflows.md`.
- [x] 2026-05-14: added concise evidence-access sections to `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md`.
- [x] 2026-05-14: left `skills/spec/SKILL.md` unchanged with no-change rationale recorded below.
- [x] M1 implemented.
- [x] 2026-05-14: code-review M1 R1 recorded `SEA-M1-CR1-1` for an unrelated M5 plan-index transition in the implementation commit.
- [x] 2026-05-14: fixed `SEA-M1-CR1-1` by restoring the M5 `docs/plan.md` entry to its pre-M1 state in this milestone's committed diff while leaving the unrelated dirty M5 plan body outside M1.
- [x] 2026-05-14: code-review M1 R2 completed clean-with-notes with no open material findings.
- [x] M1 code-review completed.
- [ ] explain-change completed.
- [ ] verify completed.
- [ ] PR handoff completed.

## Decision Log

- 2026-05-14: Keep M1 to proposal-side evidence access guidance. Reason: the approved spec defers `implement`, `code-review`, and `plan` to avoid repeating workflow amplification.
- 2026-05-14: Treat architecture as not required. Reason: the approved spec changes workflow/skill guidance only and has no runtime architecture change.
- 2026-05-14: Keep static checks conditional and concept-based. Reason: exact prose checks would be brittle and could turn the evidence model into wording ceremony.
- 2026-05-14: Do not update `skills/spec/SKILL.md` in M1. Reason: immediate proposal-to-spec handoff is already governed by upstream status settlement and existing bounded evidence guidance; M1 can satisfy the accepted proposal-side scope without adding another local rule to `spec`.

## Surprises and Discoveries

- `scripts/select-validation.py` selects generated-skill mirror and adapter archive smoke checks for canonical skill edits, so M1 validation included those checks even though release and adapter packaging behavior did not change.

## Input Classification and Migration Notes

No mandatory operating input was removed. The touched skills now separate standing operating instructions from task evidence.

| Skill | Existing input | New classification | Rationale |
|---|---|---|---|
| `proposal` | `AGENTS.md` | standing operating instructions | Preserved as operating context before task evidence. |
| `proposal` | `CONSTITUTION.md` | standing operating instructions and default task evidence when governance, source-of-truth, workflow, or release-policy changes matter | Preserves governance gates while avoiding routine reads when not relevant. |
| `proposal` | `docs/project-map.md` | conditional task evidence | Read only when architecture or repository orientation matters. |
| `proposal` | related specs, architecture docs, or ADRs | conditional task evidence | Read when the proposal changes their direction. |
| `proposal` | exploration, research, issues, incidents, or user feedback | default or conditional task evidence depending on whether they carry the user request or are relied on by the proposal | Preserves proposal intent without requiring broad historical reads. |
| `proposal` | root `VISION.md` | default task evidence when proposal fit matters | Preserves the vision-fit gate. |
| `proposal-review` | proposal under review | default task evidence | The proposal is the review target. |
| `proposal-review` | linked exploration and research artifacts | conditional task evidence | Read when the proposal relies on them. |
| `proposal-review` | `AGENTS.md` | standing operating instructions | Preserved as operating context. |
| `proposal-review` | `CONSTITUTION.md` | standing operating instructions and default task evidence when standing gates or vision fit matter | Preserves governance and source-of-truth checks. |
| `proposal-review` | `docs/project-map.md` | conditional task evidence | Read when architecture impact or repository orientation matters. |
| `proposal-review` | related specs, ADRs, or plans | conditional task evidence | Read when the proposal relies on them. |

`skills/spec/SKILL.md` is unaffected in M1. No-change rationale: M1 does not need `spec` skill edits to support immediate proposal-to-spec handoff because the current `spec` skill already requires accepted proposal input, upstream status settlement, review-resolution handling, and bounded evidence/full-file-read behavior.

## Validation Notes

- Test-first proof:
  - `python scripts/test-skill-validator.py` failed before guidance edits because the new stage evidence access checks were not yet satisfied.
- Review-driven fix proof:
  - `code-review-m1-r1` found `SEA-M1-CR1-1`.
  - Restored the unrelated M5 plan-index transition out of the M1 diff.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/change.yaml --path docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/review-log.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/review-resolution.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/reviews/code-review-m1-r1.md` passed.
  - `git diff --check -- docs/plan.md docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording docs/plans/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md` passed.
- M1 validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`
  - `python scripts/test-select-validation.py`
  - `python scripts/measure-skill-tokens.py`
- Static token measurement: 23 skills, 233054 bytes, 58252 estimated tokens. `proposal` measured 3047 estimated tokens; `proposal-review` measured 3110 estimated tokens. Measurement is diagnostic only.

## Outcome and Retrospective

- M1 implementation and code-review are complete. Final lifecycle closeout remains blocked until explain-change, verify, and PR handoff complete.

## Readiness

- See `Current Handoff Summary`.
