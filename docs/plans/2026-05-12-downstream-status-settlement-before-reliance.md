# Downstream Status Settlement Before Reliance Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-12
- Last updated: 2026-05-12
- Related proposal: [Downstream Status Settlement Before Reliance](../proposals/2026-05-12-downstream-status-settlement-before-reliance.md)
- Supersedes: none

## Purpose / big picture

Implement the approved downstream status settlement before reliance contract for the first slice. The change teaches `spec`, `architecture`, and `plan` to settle stale upstream lifecycle/status metadata before relying on upstream artifacts, while keeping review skills independent and blocking on unresolved or ambiguous evidence.

## Source artifacts

- Proposal: [Downstream Status Settlement Before Reliance](../proposals/2026-05-12-downstream-status-settlement-before-reliance.md), accepted.
- Spec: [Downstream Status Settlement Before Reliance](../../specs/downstream-status-settlement-before-reliance.md), approved.
- Spec-review records: [spec-review-r1](../changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/reviews/spec-review-r1.md), [spec-review-r2](../changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/reviews/spec-review-r2.md).
- Review resolution: [review-resolution](../changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-resolution.md), closed.
- Change metadata: [change.yaml](../changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml).
- Architecture: no separate architecture artifact expected; this is a workflow contract and skill guidance change with no runtime architecture change.
- Test spec: [Downstream Status Settlement Before Reliance Test Spec](../../specs/downstream-status-settlement-before-reliance.test.md), active.

## Context and orientation

The first slice is limited to `spec`, `architecture`, and `plan`. Later slices may extend settlement to `test-spec`, `implement`, `explain-change`, `verify`, and `pr`, but this plan must not implement those later-slice skills.

Canonical skill files live under `skills/`. Generated local Codex mirrors under `.codex/skills/` and public adapters under `dist/adapters/` must be regenerated from canonical skill text, not hand-edited.

The likely implementation surfaces are:

- `skills/spec/SKILL.md`
- `skills/architecture/SKILL.md`
- `skills/plan/SKILL.md`
- `skills/workflow/SKILL.md`, only if routing/summary guidance needs a short cross-reference
- `scripts/test-skill-validator.py`
- generated `.codex/skills/`
- generated `dist/adapters/`

## Current Handoff Summary

- Current milestone: lifecycle-closeout
- Current milestone state: planned
- Last reviewed milestone: M2
- Review status: code-review M2 clean-with-notes; no material findings
- Remaining in-scope implementation milestones: none
- Next stage: verify
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: durable explain-change is complete; verify and PR handoff remain.

## Non-goals

- Do not implement settlement in `test-spec`, `implement`, `explain-change`, `verify`, or `pr`.
- Do not add review-side artifact-status sync.
- Do not add lifecycle-validator stale-status enforcement in this slice.
- Do not bulk-migrate historical artifact statuses.
- Do not rewrite substantive upstream artifact content during settlement.
- Do not change formal review recording rules.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.

## Requirements covered

- `R1`-`R4`: first-slice scope and isolation behavior.
- `R5`-`R8`: settlement permission and edit boundary.
- `R9`-`R10`: clear review evidence and blocked settlement.
- `R11`-`R17a`: initial settlement mappings and unknown-target behavior.
- `R18`-`R24a`: settlement output fields and blocker semantics.
- `R25`-`R27`: later-slice notes and lifecycle-validator deferral.

## Milestones

### M1. Canonical Skill Guidance And Static Proof

- Milestone state: closed
- Goal: update canonical downstream skills and static checks for first-slice upstream status settlement.
- Requirements: `R1`-`R24a`
- Files/components likely touched:
  - `skills/spec/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/workflow/SKILL.md`, only if needed for short routing cross-reference
  - `scripts/test-skill-validator.py`
  - `docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml`
- Dependencies: approved spec, approved plan-review, active test spec.
- Tests to add/update:
  - Static validator coverage that `spec`, `architecture`, and `plan` include upstream status settlement guidance.
  - Static coverage that the first slice excludes `test-spec`, `implement`, `explain-change`, `verify`, and `pr` from operational settlement.
  - Static coverage for settlement output vocabulary: `updated`, `blocked`, `not-needed`, `New status`, `not-applicable`, and `Settlement blocker`.
- Implementation steps:
  - Add concise upstream status settlement guidance to `spec`, `architecture`, and `plan`.
  - Preserve review-skill independence; do not add standardized status-sync fields to review skills.
  - Add or update static skill-validator tests before or with canonical skill changes.
  - Update change metadata with validation evidence.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording`
  - `git diff --check -- skills scripts docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md docs/plan.md`
- Expected observable result: canonical first-slice skills tell downstream agents how to settle or block before relying on upstream artifacts, and static tests prove the guidance exists.
- Commit message: `M1: add upstream status settlement skill guidance`
- Milestone closeout:
  - validation passed: yes
  - progress updated: yes
  - decision log updated if needed: no new decision needed
  - validation notes updated: yes
  - milestone committed: yes
- Risks:
  - Guidance becomes too verbose for public skills.
  - Later-slice skills accidentally gain operational settlement behavior.
- Rollback/recovery:
  - Revert canonical skill guidance and tests for this milestone only; keep proposal/spec/review artifacts as historical evidence.

### M2. Generated Output Refresh And Final Static Proof

- Milestone state: closed
- Goal: regenerate generated skill mirrors and public adapter output from canonical skill changes, then validate drift and adapter structure.
- Requirements: generated-output consistency for `R1`-`R24a`
- Files/components likely touched:
  - `.codex/skills/spec/SKILL.md`
  - `.codex/skills/architecture/SKILL.md`
  - `.codex/skills/plan/SKILL.md`
  - generated `dist/adapters/**` skill files
  - `docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml`
- Dependencies: M1 closed.
- Tests to add/update:
  - No new tests expected unless generation exposes missing static coverage.
- Implementation steps:
  - Run generated-output check first and record expected drift if M1 changed canonical skills.
  - Regenerate local Codex skill mirrors.
  - Regenerate adapter output for version `0.1.1`.
  - Validate generated output and adapter structure.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording`
  - `git diff --check -- .codex/skills dist/adapters docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md docs/plan.md`
- Expected observable result: generated local and public skill output reflects canonical settlement guidance and adapter validation passes.
- Commit message: `M2: refresh generated settlement skill output`
- Milestone closeout:
  - validation passed: yes
  - progress updated: yes
  - decision log updated if needed: no new decision needed
  - validation notes updated: yes
  - milestone committed: yes
- Risks:
  - Generated output drift is broader than expected.
  - Adapter validation exposes stale package metadata.
- Rollback/recovery:
  - Revert generated output and revisit M1 canonical changes if drift is unexpected.

## Validation plan

Run milestone-specific validation first. Before final PR handoff, run:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/test-adapter-distribution.py
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording
python scripts/validate-change-metadata.py docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.md --path docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md --path docs/plan.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-log.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-resolution.md
git diff --check -- skills .codex/skills dist/adapters scripts docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md specs/downstream-status-settlement-before-reliance.md docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md docs/plan.md docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording
```

## Risks and recovery

- If plan-review finds milestone scope too broad, split M1 into separate skill guidance and validator milestones before implementation.
- If settlement guidance conflicts with the approved spec, update the spec before implementation.
- If generated output check fails before regeneration, record the expected drift and regenerate from canonical skills.
- If adapter validation fails after regeneration, stop and fix the generated-output or adapter metadata issue before final closeout.

## Dependencies

- Proposal is accepted.
- Spec is approved.
- Spec-review R2 is approved with no material findings.
- Review-resolution is closed.
- Plan-review must pass before test-spec.
- Test-spec must be active before implementation starts.
- M2 depends on M1.

## Progress

- [x] 2026-05-12: proposal accepted.
- [x] 2026-05-12: spec drafted.
- [x] 2026-05-12: spec-review R1 recorded material finding `SR-001`.
- [x] 2026-05-12: `SR-001` accepted and resolved in the spec.
- [x] 2026-05-12: spec-review R2 approved the amended spec.
- [x] 2026-05-12: plan-review approved the execution plan with no material findings.
- [x] 2026-05-12: test-spec created active proof-planning surface for M1-M2.
- [x] M1. Canonical Skill Guidance And Static Proof - closed after clean code-review rerun
- [x] M2. Generated Output Refresh And Final Static Proof - closed after clean code-review
- [x] 2026-05-12: explain-change recorded durable rationale and handed off to verify.

## Decision log

- 2026-05-12: Keep first implementation slice limited to `spec`, `architecture`, and `plan`. Rationale: the approved proposal and spec reserve later downstream skills for future slices.
- 2026-05-12: No separate architecture artifact is planned. Rationale: the approved spec defines a workflow/skill guidance contract and no runtime architecture boundary changes.
- 2026-05-12: Use the existing change-local review-recording pack as this initiative's change root. Rationale: spec-review R1 generated the deterministic change ID and the pack now owns review evidence, resolution, and metadata.
- 2026-05-12: Kept M1 generated-output surfaces untouched. Rationale: the plan reserves `.codex/skills/` and `dist/adapters/` regeneration for M2.

## Surprises and discoveries

- M1 implementation did not require `skills/workflow/SKILL.md`; the settlement contract is local to the three first-slice downstream skills plus static validator proof.

## Validation notes

- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording` passed after spec-review R2.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml` passed after spec-review R2.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-log.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-resolution.md` passed after spec-review R2.
- `git diff --check -- specs/downstream-status-settlement-before-reliance.md docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording` passed after spec-review R2.
- Plan-review approved the execution plan without material findings; no detailed plan-review record was required.
- M1 red proof: `python scripts/test-skill-validator.py` failed before skill edits because `spec`, `architecture`, and `plan` lacked the upstream status settlement contract.
- M1 validation: `python scripts/test-skill-validator.py` passed after adding static coverage and canonical first-slice skill guidance.
- M1 validation: `python scripts/validate-skills.py` passed after canonical skill updates.
- M1 validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml` passed after metadata update.
- M1 validation: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording` passed with 2 review records, 1 finding, 2 log entries, and 1 resolution entry.
- M1 validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.test.md --path docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md --path docs/plan.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-log.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-resolution.md` passed with the existing unrelated `docs/plan.md` lifecycle-language warning.
- M1 validation: `git diff --check -- skills scripts docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md docs/plan.md` passed.
- Code-review R1 found material finding `CR-001`: static proof and skill guidance omit required blocked-settlement and edit-permission semantics. Review record: `docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/reviews/code-review-r1.md`.
- Review-resolution for `CR-001` accepted the finding and fixed M1 by tightening skill guidance and validator assertions.
- M1 fix validation: `python scripts/test-skill-validator.py` passed after the `CR-001` fix.
- M1 fix validation: `python scripts/validate-skills.py` passed after the `CR-001` fix.
- Code-review M1 rerun returned `clean-with-notes` with no material findings. No detailed clean review record was required.
- M2 pre-generation check: `python scripts/build-skills.py --check` failed with expected stale generated local Codex skill mirrors for `architecture`, `plan`, and `spec`.
- M2 pre-generation check: `python scripts/build-adapters.py --version 0.1.1 --check` failed with expected stale generated adapter skill files for `architecture`, `plan`, and `spec` across Claude, Codex, and opencode adapters.
- M2 generation: `python scripts/build-skills.py` synced generated local Codex skills.
- M2 generation: `python scripts/build-adapters.py --version 0.1.1` synced generated adapter output.
- M2 validation: `python scripts/build-skills.py --check` passed after generation.
- M2 validation: `python scripts/build-adapters.py --version 0.1.1 --check` passed after generation.
- M2 validation: `python scripts/validate-adapters.py --version 0.1.1` passed.
- M2 validation: `python scripts/test-adapter-distribution.py` passed.
- M2 validation: `python scripts/test-skill-validator.py` passed.
- M2 validation: `python scripts/validate-skills.py` passed.
- M2 validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml` passed.
- M2 validation: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording` passed with 3 review records, 2 findings, 3 log entries, and 2 resolution entries.
- M2 validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.test.md --path docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md --path docs/plan.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-log.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-resolution.md` passed with the existing unrelated `docs/plan.md` lifecycle-language warning.
- M2 validation: `git diff --check -- .codex/skills dist/adapters docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md docs/plan.md` passed.
- Code-review M2 returned `clean-with-notes` with no material findings. No detailed clean review record was required.
- Explain-change recorded the durable rationale at `docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/explain-change.md`.
- Explain-change validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml` passed.
- Explain-change validation: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording` passed.
- Explain-change validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.test.md --path docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md --path docs/plan.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-log.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-resolution.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/explain-change.md` passed with the existing unrelated `docs/plan.md` lifecycle-language warning.
- Explain-change validation: `git diff --check -- docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md docs/plan.md` passed.

## Outcome and retrospective

- Pending implementation and downstream lifecycle closeout.

## Readiness

- See `Current Handoff Summary`.
