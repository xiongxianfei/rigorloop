# Spec and Test-Spec Structural Hygiene Execution Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-19
- Last updated: 2026-05-19
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved structural-hygiene contract for the skill contract and its matching test spec. The work is navigation-only: it makes the existing slice structure visible without changing clause text, acceptance-criterion text, test-case bodies, fixtures, or coverage rows.

## Source artifacts

- Proposal: [Spec and Test-Spec Structural Hygiene](../proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md)
- Proposal review: [proposal-review-r1](../changes/2026-05-19-spec-and-test-spec-structural-hygiene/reviews/proposal-review-r1.md)
- Spec: [Skill Contract](../../specs/skill-contract.md)
- Spec review: [spec-review-r1](../changes/2026-05-19-spec-and-test-spec-structural-hygiene/reviews/spec-review-r1.md)
- Test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md), to be amended after plan-review
- Architecture: not required; this is a documentation structure change with no component, data-flow, runtime, deployment, or security architecture impact.

## Context and orientation

- `specs/skill-contract.md` is the canonical skill-contract spec.
- `specs/skill-contract.test.md` is the matching proof-planning surface.
- `docs/proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md` owns the accepted direction.
- `docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/` owns change-local review and validation evidence.
- `docs/plan.md` is the lifecycle index; this file is the plan body.
- The approved spec amendment keeps the Examples section flat because examples can be cross-cutting.

## Non-goals

- Do not change existing R-clause IDs, R-clause text, or numbering.
- Do not change existing acceptance-criterion text.
- Do not change existing test-case IDs, bodies, fixtures, or coverage rows.
- Do not split `specs/skill-contract.md` or `specs/skill-contract.test.md`.
- Do not modify skills, adapters, validators, generated output, or build scripts.
- Do not add structural-fingerprint enforcement for specs.
- Do not move operational detail from spec into test-spec or plan in this change.

## Requirements covered

- Structural navigation in `specs/skill-contract.md`: implemented by the approved spec amendment and preserved through validation.
- Structural hygiene invariant in `specs/skill-contract.md`: implemented by `Spec growth strategy`, state invariants, boundary behavior, non-goals, and observability text.
- Matching test-spec grouping in `specs/skill-contract.test.md`: planned for M1 after plan-review.
- Content preservation: proved by R-clause, acceptance-criterion, example-ID, and test-spec preservation checks.

## Current Handoff Summary

- Current milestone: M1. Test-spec structural grouping
- Current milestone state: review-requested
- Last reviewed milestone: M1 code-review R1 requested changes; accepted finding resolved
- Review status: `CR-M1-001` resolved and ready for code-review rerun
- Remaining in-scope implementation milestones: M1
- Next stage: code-review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: code-review rerun, explain-change, verify, and PR handoff remain open.

## Milestones

### M1. Test-spec structural grouping

- Milestone state: review-requested
- Goal: mirror the approved skill-contract slice grouping in `specs/skill-contract.test.md` without changing existing test semantics.
- Requirements:
  - Preserve every existing test-case ID, body, fixture reference, and coverage row.
  - Add slice headers to the Requirement coverage map, Acceptance criteria coverage map, and Test cases section.
  - Keep the test spec aligned with the four spec slice bands: Foundational R1-R7, Baseline normalization first slice R8-R26, Published-skill design pilot R27-R36, and Assets-first plan pilot R37-R45.
- Files/components likely touched:
  - `specs/skill-contract.test.md`
  - `docs/plans/2026-05-19-spec-and-test-spec-structural-hygiene.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/change.yaml`
- Dependencies:
  - Plan-review approval: satisfied by `plan-review-r1`.
  - Test-spec stage must amend `specs/skill-contract.test.md` before implementation relies on the grouping: satisfied by this test-spec amendment.
- Tests to add/update:
  - No new executable tests expected.
  - Update `specs/skill-contract.test.md` structure only.
- Implementation steps:
  - During `test-spec`, insert four slice headers in the Requirement coverage map without changing any row text.
  - Insert the same four slice headers in the Acceptance criteria coverage map without changing any row text.
  - Insert the same four slice headers in Test cases and place existing `T1`-`T36` subsections under the correct slice.
  - Record preservation checks for test-case headings, coverage rows, and relevant fixture references.
- Validation commands:
  - `git diff --check -- specs/skill-contract.test.md docs/plans/2026-05-19-spec-and-test-spec-structural-hygiene.md docs/plan.md docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plans/2026-05-19-spec-and-test-spec-structural-hygiene.md --path docs/plan.md --path docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/change.yaml --path docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/review-log.md --path docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/review-resolution.md --path docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/reviews/spec-review-r1.md --path docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/reviews/plan-review-r1.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene`
  - Preservation checks comparing existing `specs/skill-contract.test.md` test-case headings and coverage rows before and after grouping.
- Expected observable result: a reader can locate skill-contract proof coverage by slice in `specs/skill-contract.test.md`, and existing proof content remains unchanged.
- Commit message: `M1: group skill contract test spec by slice`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - A test case or coverage row could be placed under the wrong slice header while preserving text.
  - A preservation check could accidentally ignore a changed body line.
- Rollback/recovery:
  - Remove added test-spec headers and restore prior flat structure from Git.
  - If a row or test case is found in the wrong slice, move only the header boundary or test section placement; do not edit test text.

## Validation plan

- Plan-stage validation:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md --path specs/skill-contract.md --path docs/plans/2026-05-19-spec-and-test-spec-structural-hygiene.md --path docs/plan.md --path docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/change.yaml --path docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/review-log.md --path docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/review-resolution.md --path docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/reviews/spec-review-r1.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene`
  - `git diff --check -- docs/proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md specs/skill-contract.md docs/plans/2026-05-19-spec-and-test-spec-structural-hygiene.md docs/plan.md docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene`
- M1 validation: use the milestone validation commands above.
- Final verification: run the plan-selected explicit lifecycle, change metadata, review artifact, preservation, and whitespace checks before `explain-change` and `verify`.

## Risks and recovery

- Risk: structural grouping creates a false sense that content changed. Recovery: preserve text exactly and record preservation checks.
- Risk: test-spec grouping diverges from spec grouping. Recovery: use the Slice terminology bands and the spec navigation table as the source for grouping.
- Risk: another active plan changes `specs/skill-contract.test.md`. Recovery: inspect current diff before M1 implementation and update this plan if overlap appears.
- Risk: lifecycle state drifts between this plan and `docs/plan.md`. Recovery: update both surfaces in the same change whenever plan lifecycle state changes.

## Dependencies

- `proposal-review-r1` approved the proposal with no material findings.
- `spec-review-r1` approved the draft spec amendment with no material findings.
- `plan-review` must approve this plan before test-spec work relies on it.
- `test-spec` must amend `specs/skill-contract.test.md` before implementation claims the test-spec grouping is complete.

## Progress

- [x] 2026-05-19: Proposal authored.
- [x] 2026-05-19: Proposal-review approved with no material findings.
- [x] 2026-05-19: Proposal status settled to `accepted`.
- [x] 2026-05-19: Spec amended and spec-review approved with no material findings.
- [x] 2026-05-19: Plan-review approved with no material findings.
- [x] 2026-05-19: Test-spec amended with slice grouping.
- [x] 2026-05-19: Test-spec approved by maintainer.
- [x] 2026-05-19: M1 implementation completed and handed to code-review.
- [x] Resolve `CR-M1-001`.
- [ ] Code-review.
- [ ] Explain-change.
- [ ] Verify.
- [ ] PR handoff.

## Decision log

- 2026-05-19: No architecture artifact is required because the change affects documentation structure only and does not alter runtime behavior, data flow, persistence, deployment, or security boundaries.
- 2026-05-19: Use one implementation milestone because only the test-spec structure remains after approved spec amendment.
- 2026-05-19: Preserve the flat Examples section; the spec already records that examples can be cross-cutting.

## Surprises and discoveries

- None yet.

## Validation notes

- 2026-05-19 spec-stage validation passed `validate-artifact-lifecycle`, `validate-change-metadata`, `validate-review-artifacts --mode closeout`, `git diff --check`, `validate-skills.py`, and `test-skill-validator.py`.
- 2026-05-19 preservation checks passed for existing R-clause lines, acceptance-criterion bullets, and example IDs.
- 2026-05-19 test-spec stage inserted slice headers in the Requirement coverage map, Acceptance criteria coverage map, and Test cases section while preserving existing coverage rows and test-case heading text.
- 2026-05-19 test-spec preservation checks passed for Requirement coverage rows, Acceptance criteria coverage rows, normalized test-case heading text, and non-heading nonblank test-case body lines.
- 2026-05-19 test-spec-stage validation passed `git diff --check`, `validate-artifact-lifecycle`, `validate-change-metadata`, and `validate-review-artifacts --mode closeout`.
- 2026-05-19 maintainer approved the amended active test spec for implementation reliance.
- 2026-05-19 implementation-stage preservation checks passed for Requirement coverage rows, Acceptance criteria coverage rows, normalized test-case heading text, and non-heading nonblank test-case body lines.
- 2026-05-19 implementation-stage validation passed `git diff --check`, `validate-artifact-lifecycle`, `validate-change-metadata`, and `validate-review-artifacts --mode closeout`.
- 2026-05-19 code-review M1 R1 recorded `CR-M1-001`: three baseline acceptance criteria were grouped under the Foundational header in `specs/skill-contract.md`.
- 2026-05-19 resolved `CR-M1-001` by moving only the three accepted criteria to `### Baseline normalization first slice (R8-R26)` in `specs/skill-contract.md`.
- 2026-05-19 post-resolution preservation checks passed for sorted spec acceptance-criterion text, test-spec Requirement coverage rows, test-spec Acceptance criteria coverage rows, normalized test-case heading text, and non-heading nonblank test-case body lines.
- 2026-05-19 post-resolution validation passed `git diff --check`, `validate-artifact-lifecycle`, `validate-change-metadata`, and `validate-review-artifacts --mode closeout`.

## Outcome and retrospective

- Pending.

## Readiness

- See `Current Handoff Summary`.

## Risks and follow-ups

- Follow-up proposal candidates remain owned by the accepted proposal: operational-detail relocation, structural fingerprints for specs, broader slice grouping for other specs, future spec splitting if ownership pain develops, and a closed-enum verb set for specs.
