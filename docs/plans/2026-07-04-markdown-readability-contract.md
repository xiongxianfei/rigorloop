# Markdown Readability Contract Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Change ID: 2026-07-04-markdown-readability-contract
- Start date: 2026-07-04
- Last updated: 2026-07-04
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved Markdown readability contract in reviewable slices.
The work introduces a dedicated readability validator, fixtures, generated-region marker checks, changed-section README and `VISION.md` enforcement, and aligned generated artifact guidance without mass-reflowing historical Markdown.

## Source artifacts

- Proposal: [docs/proposals/2026-07-04-markdown-readability-contract.md](../../docs/proposals/2026-07-04-markdown-readability-contract.md)
- Spec: [specs/markdown-readability-contract.md](../../specs/markdown-readability-contract.md)
- Architecture: not required; `spec-review-r1` recorded `architecture-not-required`
- Test spec: [specs/markdown-readability-contract.test.md](../../specs/markdown-readability-contract.test.md)

## Context and orientation

The change affects repository-local Markdown authoring and validation surfaces:

- `scripts/validate-markdown-readability.py` is the new owner validator.
- Existing validators may compose the owner validator for relevant paths.
- README and `VISION.md` checks apply only to changed sections in the first slice.
- Generated-region markers use canonical `surface`, `source`, and optional `generator` metadata.
- Historical Markdown remains audit-only unless a separate migration is approved.
- Manual-proof contracts are out of scope.

Likely related existing validation surfaces include `scripts/validate-readme.py`, `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, `scripts/validate-review-artifacts.py`, `scripts/test-*validator.py`, and selector routing in `scripts/select-validation.py`.

## Non-goals

- Do not implement manual-proof contracts.
- Do not impose a fixed line-length limit.
- Do not mass-reflow historical Markdown.
- Do not hand-edit generated public adapter skill bodies.
- Do not require diagrams.
- Do not make subjective prose clarity fail validation by default.

## Requirements covered

- R1-R10: M1 and M2, semantic source-line guidance and generated prose structures.
- R11-R19: M2, skeleton and generated artifact structure guidance.
- R20: M1 and M2, manual-proof exclusion preserved.
- R21-R27: M1, generated-region marker validation and ownership rules.
- R28-R31: M1, owner validator and composition boundary.
- R32-R34: M1, changed-section README and `VISION.md` enforcement.
- R35-R39: M1, historical audit-only and block-type exclusion behavior.
- R40-R44: M1 and test spec, fixtures and cold-read proof.
- R45-R48: M2, diagram guidance.
- R49-R50: M2, generated adapter output proof from canonical sources.

## Current Handoff Summary

- Current milestone: M1. Readability Validator and Deterministic Fixtures
- Current milestone state: review-requested
- Latest review evidence: test-spec-review-r1
- Last reviewed milestone: test-spec
- Review status: approved; stage=test-spec-review; round=r1
- Remaining in-scope implementation milestones: M1, M2
- Next stage: code-review M1
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — M1 implementation is awaiting code-review, M2 has not started, and final validation has not run.

## Milestones

### M1. Readability Validator and Deterministic Fixtures

- Milestone state: review-requested
- Goal: Add the owner readability validator and deterministic checks for the first enforcement slice.
- Requirements: R1-R10, R20-R39, R40-R44
- Files/components likely touched:
  - `scripts/validate-markdown-readability.py`
  - `scripts/test-markdown-readability-validator.py`
  - README and `VISION.md` fixture paths selected by the test spec
  - generated-region marker fixtures selected by the test spec
  - selector or composed validator integration only where the test spec requires it
- Dependencies:
  - Approved spec-review.
  - Approved plan-review.
  - Active test spec and clean test-spec-review before implementation.
- Tests to add/update:
  - Hard-wrap regression fixtures for README and `VISION.md`.
  - Long semantic-line passing fixture.
  - Code fence, table, HTML block, link reference, and generated-region exclusion fixtures.
  - Generated-region marker pairing fixtures.
  - Placeholder fixture where stable skeleton validation applies.
- Implementation steps:
  - Add the owner validator with stable `MDREAD-*` check IDs.
  - Implement changed-section scoping for README and `VISION.md` enforcement.
  - Implement generated-region marker parsing and pairing checks.
  - Implement audit-only diagnostics for long lines and dense paragraphs without failing validation.
  - Compose the validator from existing validators only where the test spec requires it.
- Validation commands:
  - `python scripts/test-markdown-readability-validator.py`
  - `python scripts/validate-markdown-readability.py --help`
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-04-markdown-readability-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/markdown-readability-contract.md --path docs/plans/2026-07-04-markdown-readability-contract.md --path docs/plan.md --path docs/changes/2026-07-04-markdown-readability-contract/change.yaml`
- Expected observable result: Deterministic readability checks exist with representative passing and failing fixtures, and historical Markdown remains audit-only.
- Commit message: `M1: add markdown readability validator`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Validator false positives across Markdown block types.
  - Changed-section detection could overreach into historical content.
- Rollback/recovery:
  - Remove the validator integration and fixtures from the milestone while preserving the approved spec and plan for replanning.

### M2. Generated Artifact Guidance and Integration Proof

- Milestone state: planned
- Goal: Align high-value generated artifact guidance, skeletons, and generated-output proof with the readability contract.
- Requirements: R11-R20, R45-R50
- Files/components likely touched:
  - affected `skills/*/SKILL.md` files identified by the test spec
  - affected skill assets or templates identified by the test spec
  - generated-output build and validation surfaces
  - `docs/workflows.md` only if the implementation changes workflow-level guidance
- Dependencies:
  - M1 complete or explicitly not required for the selected integration proof.
  - Test spec coverage for selected artifact classes.
- Tests to add/update:
  - Asset or skeleton shape checks for selected artifact classes.
  - Generated adapter inclusion proof where affected skill output changes.
  - Representative cold-read proof for generated documents.
  - Diagram guidance checks only where guidance text is touched.
- Implementation steps:
  - Update selected skill or skeleton guidance so generated artifacts start from status/result blocks, stable IDs, tables, and source-owner rules.
  - Ensure manual-proof contracts remain excluded.
  - Rebuild or validate generated adapter output from canonical authored sources.
  - Record representative cold-read evidence.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-markdown-readability.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-markdown-readability-contract`
- Expected observable result: Generated artifact guidance and output proof align with the readability contract without hand-editing generated adapter bodies.
- Commit message: `M2: align generated markdown surfaces`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Over-updating too many skills in one slice.
  - Skeleton text could drift into policy ownership.
- Rollback/recovery:
  - Revert selected skill/skeleton updates and regenerated output proof, then narrow the artifact-class scope.

## Validation plan

- `python scripts/validate-change-metadata.py docs/changes/2026-07-04-markdown-readability-contract/change.yaml`: validate change metadata and autoprogression state.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-markdown-readability-contract`: validate review log and resolution records.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/markdown-readability-contract.md --path docs/plans/2026-07-04-markdown-readability-contract.md --path docs/plan.md --path docs/changes/2026-07-04-markdown-readability-contract/change.yaml`: validate lifecycle-managed artifacts and plan index state.
- `python scripts/test-markdown-readability-validator.py`: validate M1 readability fixture behavior.
- `python scripts/validate-markdown-readability.py`: validate selected readability checks after implementation.
- `python scripts/validate-skills.py`: validate affected skill guidance after M2.
- `python scripts/build-skills.py --check`: prove generated skill output is current after M2.
- `python scripts/test-build-skills.py`: validate skill build behavior after M2.
- `python scripts/test-adapter-distribution.py`: validate adapter output after M2.
- `git diff --check --`: validate whitespace before handoffs.

## Risks and recovery

- Risk: The readability validator becomes a subjective prose judge.
  - Recovery: Keep subjective checks audit-only and require fixture-backed deterministic behavior before failure.
- Risk: README or `VISION.md` changed-section enforcement scans historical text.
  - Recovery: Narrow selector logic or temporarily demote the check to audit-only for historical files.
- Risk: Marker syntax enforcement conflicts with existing generated markers.
  - Recovery: Support old markers as audit-only during the first slice or record migration separately.
- Risk: Generated artifact guidance grows too broad.
  - Recovery: Limit M2 to high-value artifact classes named by the test spec.

## Dependencies

- Accepted proposal and approved proposal-review R2.
- Approved spec-review R1.
- Recorded `architecture-not-required` assessment.
- Clean plan-review before test-spec authoring.
- Active test spec and clean test-spec-review before implementation.

## Progress

- 2026-07-04: plan created after approved spec-review R1.
- 2026-07-04: plan-review R1 approved the plan with no material findings.
- 2026-07-04: test spec authored and handed to test-spec-review.
- 2026-07-04: test-spec-review R1 approved the proof map and allowed implementation handoff.
- 2026-07-04: M1 implementation started.
- 2026-07-04: M1 implementation completed and handed to code-review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-04 | Split implementation into validator/fixtures and generated-surface alignment milestones. | This keeps deterministic validation separate from broader skill and generated-output updates. | One large implementation milestone. |
| 2026-07-04 | Keep architecture not required. | Spec-review R1 recorded no new runtime, persistence, deployment, external integration, or hard-to-reverse architecture decision. | Add architecture artifact by default. |
| 2026-07-04 | Compose readability validation through the validation selector for README and `VISION.md`. | This gives existing validation routing a single owner script without duplicating readability policy inside guide or README validators. | Embed readability checks directly in `validate-readme.py`. |

## Surprises and discoveries

- None yet.

## Validation notes

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-04-markdown-readability-contract.md --path specs/markdown-readability-contract.md --path docs/plans/2026-07-04-markdown-readability-contract.md --path docs/plan.md --path docs/changes/2026-07-04-markdown-readability-contract/change.yaml --path docs/changes/2026-07-04-markdown-readability-contract/review-log.md --path docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r1.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r2.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/spec-review-r1.md`: passed before plan-review.
- Test spec authoring completed for `specs/markdown-readability-contract.test.md`; focused lifecycle validation passed before test-spec-review.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-04-markdown-readability-contract/change.yaml`: passed after test-spec authoring.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-04-markdown-readability-contract.md --path specs/markdown-readability-contract.md --path specs/markdown-readability-contract.test.md --path docs/plans/2026-07-04-markdown-readability-contract.md --path docs/plan.md --path docs/changes/2026-07-04-markdown-readability-contract/change.yaml --path docs/changes/2026-07-04-markdown-readability-contract/review-log.md --path docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r1.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r2.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/spec-review-r1.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/plan-review-r1.md`: passed after test-spec authoring.
- `git diff --check -- docs/proposals/2026-07-04-markdown-readability-contract.md specs/markdown-readability-contract.md specs/markdown-readability-contract.test.md docs/plans/2026-07-04-markdown-readability-contract.md docs/plan.md docs/changes/2026-07-04-markdown-readability-contract`: passed after test-spec authoring.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-markdown-readability-contract`: passed after test-spec-review R1.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-04-markdown-readability-contract/change.yaml`: passed after test-spec-review R1.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-04-markdown-readability-contract.md --path specs/markdown-readability-contract.md --path specs/markdown-readability-contract.test.md --path docs/plans/2026-07-04-markdown-readability-contract.md --path docs/plan.md --path docs/changes/2026-07-04-markdown-readability-contract/change.yaml --path docs/changes/2026-07-04-markdown-readability-contract/review-log.md --path docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r1.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r2.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/spec-review-r1.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/plan-review-r1.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/test-spec-review-r1.md`: passed after test-spec-review R1.
- `git diff --check -- docs/proposals/2026-07-04-markdown-readability-contract.md specs/markdown-readability-contract.md specs/markdown-readability-contract.test.md docs/plans/2026-07-04-markdown-readability-contract.md docs/plan.md docs/changes/2026-07-04-markdown-readability-contract`: passed after test-spec-review R1.
- `python scripts/test-markdown-readability-validator.py`: passed after M1 implementation.
- `python scripts/validate-markdown-readability.py --help`: passed after M1 implementation.
- `python scripts/validate-markdown-readability.py`: passed after M1 implementation with audit-only warning summary `MDREAD-002=63, MDREAD-003=5`.
- `python scripts/test-select-validation.py`: passed after M1 selector integration.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-04-markdown-readability-contract/change.yaml`: passed after M1 implementation.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-04-markdown-readability-contract.md --path specs/markdown-readability-contract.md --path specs/markdown-readability-contract.test.md --path docs/plans/2026-07-04-markdown-readability-contract.md --path docs/plan.md --path docs/changes/2026-07-04-markdown-readability-contract/change.yaml --path docs/changes/2026-07-04-markdown-readability-contract/review-log.md --path docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r1.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r2.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/spec-review-r1.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/plan-review-r1.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/test-spec-review-r1.md`: passed after M1 implementation.
- `git diff --check -- scripts/validate-markdown-readability.py scripts/test-markdown-readability-validator.py scripts/validation_selection.py scripts/test-select-validation.py docs/plans/2026-07-04-markdown-readability-contract.md docs/plan.md docs/changes/2026-07-04-markdown-readability-contract specs/markdown-readability-contract.test.md`: passed after M1 implementation.

## Outcome and retrospective

- Pending final lifecycle closeout.

## Readiness

- See `Current Handoff Summary`.
- Downstream lifecycle state is owned by `Current Handoff Summary`.
