# Semantic Source-Line Contract Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-24-semantic-source-line-contract
- Owner: agent
- Start date: 2026-06-24
- Last updated: 2026-06-24
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved documentation source-formatting contract so review-critical Markdown is checked for semantic source-line boundaries instead of arbitrary hard wrapping.
The plan keeps the work reviewable by separating validator behavior and fixtures, contributor guidance and formatter guardrails, and selected-validation integration with behavior-preservation evidence.

## Source artifacts

- Proposal: [Semantic Source-Line Contract](../proposals/2026-06-24-semantic-source-line-contract.md)
- Spec: [Documentation Source Formatting](../../specs/documentation-source-formatting.md)
- Architecture: not required; recorded assessment in [change.yaml](../changes/2026-06-24-semantic-source-line-contract/change.yaml)
- Test spec: [Documentation Source Formatting test spec](../../specs/documentation-source-formatting.test.md)
- Change metadata: [change.yaml](../changes/2026-06-24-semantic-source-line-contract/change.yaml)
- Review log: [review-log.md](../changes/2026-06-24-semantic-source-line-contract/review-log.md)
- Proposal review: [proposal-review-r1](../changes/2026-06-24-semantic-source-line-contract/reviews/proposal-review-r1.md)
- Spec review: [spec-review-r1](../changes/2026-06-24-semantic-source-line-contract/reviews/spec-review-r1.md)

## Upstream status settlement

- Settlement result: not-needed
- New status: not-applicable
- Settlement blocker: none
- Evidence: proposal status is `accepted`; spec status is `approved`; proposal-review-r1 and spec-review-r1 are approved with no material findings; `review-log.md` has no open findings; architecture assessment is recorded as `architecture-not-required`.

## Context and orientation

The change affects repository-owned Markdown validation and contributor guidance, not Markdown rendering.
The validator should live under `scripts/`, fixtures under the existing test fixture layout, and contributor guidance in `CONTRIBUTING.md`.
`docs/workflows.md` may link to `CONTRIBUTING.md` but should not duplicate the full formatting contract.

The existing validation system already includes focused scripts for README, guide-system, skills, artifact lifecycle, and selected validation.
This work should compose with those surfaces instead of duplicating marker, vocabulary, guide-system, or skill-contract checks.

## Non-goals

- Do not implement repository-wide Markdown enforcement.
- Do not create an automatic prose rewriter.
- Do not use fixed-width Markdown line-length validation as the semantic validator.
- Do not migrate historical specs, plans, review records, learn sessions, release evidence, or third-party documentation.
- Do not hand-edit generated README marker content.
- Do not start `test-spec` or implementation before clean `plan-review`.

## Requirements covered

- R1-R7: M1 and M2 define semantic units, allowed long lines, and deliberate clause handling.
- R8-R14: M1 implements non-mutating validator behavior, deterministic errors, warnings, block segmentation, diagnostics, and no auto-fix behavior.
- R15: M1 and M2 preserve generated and marker-owned content ownership.
- R16-R18: M2 adds contributor guidance, formatter guardrails, and source-form review procedure.
- R19: M3 keeps expansion beyond Tier A behind a separate evidence-based decision.
- AC1-AC15: covered across M1 through M3 and the later test spec.

## Current Handoff Summary

- Current milestone: M1. Markdown Block Segmentation, Validator Modes, and Regression Fixtures
- Current milestone state: review-requested
- Latest review evidence: docs/changes/2026-06-24-semantic-source-line-contract/reviews/code-review-m1-r1.md
- Last reviewed milestone: M1
- Review status: review-requested; stage=code-review; round=r2
- Remaining in-scope implementation milestones: M1, M2, M3
- Next stage: code-review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open,implementation-milestones-open,milestone-review-pending,explain-change-pending,verify-pending,pr-handoff-pending — M1 is ready for rerun code-review and later lifecycle gates remain before final closeout.

## Milestones

### M1. Markdown Block Segmentation, Validator Modes, and Regression Fixtures

- Milestone state: review-requested
- Goal: Add the non-mutating prose validator with Markdown block segmentation, deterministic Tier A errors, audit warnings, and regression fixtures.
- Requirements: R1-R15, AC1-AC10, AC12, AC15
- Files/components likely touched:
  - `scripts/validate-documentation-prose.py`
  - `scripts/test-documentation-prose-validator.py`
  - `tests/fixtures/documentation-prose/`
  - `docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`
- Dependencies:
  - Clean plan-review.
  - Approved test spec after plan-review.
- Tests to add/update:
  - Mechanical mid-sentence wraps fail in Tier A.
  - Long complete source lines pass.
  - Sentence-per-line paragraphs pass.
  - Fenced commands, tables, URLs, link definitions, frontmatter, and code blocks are excluded or handled separately.
  - `AI agents`, `proposal to spec`, lifecycle-chain, command-split, and editor/tool rewrap fixtures fail.
  - Tier B suspicious cases warn without repository failure.
  - Validator leaves input files unchanged.
- Implementation steps:
  - Implement Markdown block segmentation before prose analysis.
  - Add `--mode audit`, `--mode enforce`, and `--path` selection.
  - Implement diagnostic shape with file, line range, suspected unit, reason, severity, and suggested actions.
  - Add positive-list clause break handling and warning fallback for ambiguous cases.
  - Add paired pass/fail fixtures for the boundary matrix.
- Validation commands:
  - `python scripts/test-documentation-prose-validator.py`
  - `python scripts/validate-documentation-prose.py --mode audit --path README.md --path VISION.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`
  - `git diff --check -- scripts/validate-documentation-prose.py scripts/test-documentation-prose-validator.py tests/fixtures/documentation-prose docs/changes/2026-06-24-semantic-source-line-contract`
- Expected observable result: The validator distinguishes deterministic mechanical wraps from long valid semantic lines and emits bounded non-mutating diagnostics.
- Commit message: `M1: add documentation prose validator`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M2 starts
- Risks:
  - A regex-only approach could misclassify Markdown structures.
  - False failures could erode trust in the gate.
- Rollback/recovery:
  - Remove validator routing first, then revert validator script and fixtures together.

### M2. Contributor Guidance, Formatter Guardrails, and Tier A Cleanup

- Milestone state: planned
- Goal: Add concise authoring guidance, prevent formatter reflow, and clean only current Tier A source-line violations needed for enforcement.
- Requirements: R1-R7, R15-R18, AC2-AC5, AC11-AC13
- Files/components likely touched:
  - `CONTRIBUTING.md`
  - `docs/workflows.md`
  - formatter or lint configuration files if present or added
  - `README.md`
  - `VISION.md`
  - `docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`
- Dependencies:
  - M1 validator and fixtures.
  - Generated-marker ownership check before editing README marker-owned sections.
- Tests to add/update:
  - Formatter configuration preserves prose wrapping for covered files.
  - Existing README marker and vocabulary validation still pass.
  - Tier A cleanup preserves rendered meaning and marker ownership.
  - Contributor guidance points to the spec without duplicating the full contract.
- Implementation steps:
  - Add concise source-formatting guidance and validation command to `CONTRIBUTING.md`.
  - Add only a link or short pointer from `docs/workflows.md` when needed.
  - Configure markdownlint or Prettier guardrails only where tooling exists or is introduced by the plan.
  - Clean current `README.md` and `VISION.md` source-line violations without broad reflow.
  - Validate generated marker ownership before and after README-related changes.
- Validation commands:
  - `python scripts/validate-documentation-prose.py --mode enforce --path README.md --path VISION.md`
  - `python scripts/validate-readme.py`
  - `python scripts/validate-guide-system.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/documentation-source-formatting.md --path docs/workflows.md --path docs/plans/2026-06-24-semantic-source-line-contract.md --path docs/plan.md --path docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`
  - `git diff --check -- CONTRIBUTING.md docs/workflows.md README.md VISION.md docs/plans/2026-06-24-semantic-source-line-contract.md docs/plan.md docs/changes/2026-06-24-semantic-source-line-contract`
- Expected observable result: Contributors see the concise rule, tools do not mechanically rewrap covered prose, and Tier A enforcement can run on a clean baseline.
- Commit message: `M2: document source-line guardrails`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M3 starts
- Risks:
  - Guidance could duplicate the spec and drift.
  - README marker-owned content could be edited directly by mistake.
- Rollback/recovery:
  - Revert guidance and formatter changes with the Tier A cleanup, preserving canonical marker sources.

### M3. Selected Validation Integration and Behavior Preservation Evidence

- Milestone state: planned
- Goal: Integrate prose validation into selected validation for covered paths and record behavior-preservation evidence for first-slice enforcement.
- Requirements: R8-R19, AC6-AC15
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/select-validation.py`
  - `scripts/test-select-validation.py`
  - `docs/changes/2026-06-24-semantic-source-line-contract/behavior-preservation.md`
  - `docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`
  - `docs/plans/2026-06-24-semantic-source-line-contract.md`
  - `docs/plan.md`
- Dependencies:
  - M1 validator command.
  - M2 clean Tier A baseline and guidance.
- Tests to add/update:
  - Tier A file changes select enforcing prose validation.
  - Tier B file changes select audit prose validation.
  - Excluded Tier C paths do not select first-slice enforcement.
  - Existing README, guide-system, skill, and marker checks remain selected where applicable.
  - Behavior preservation matrix covers rendered README, marker ownership, VISION meaning, retired vocabulary, skill behavior, historical docs, and source reviewability.
- Implementation steps:
  - Add selected-validation catalog entry or routing for documentation prose validation.
  - Add path-selection tests for Tier A, Tier B, and Tier C.
  - Record behavior-preservation evidence.
  - Update change metadata and plan validation notes.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-documentation-prose-validator.py`
  - `python scripts/select-validation.py --changed-file README.md --changed-file VISION.md`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-semantic-source-line-contract/`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/documentation-source-formatting.md --path docs/plans/2026-06-24-semantic-source-line-contract.md --path docs/plan.md --path docs/changes/2026-06-24-semantic-source-line-contract/change.yaml --path docs/changes/2026-06-24-semantic-source-line-contract/behavior-preservation.md`
  - `git diff --check -- scripts/validation_selection.py scripts/select-validation.py scripts/test-select-validation.py docs/changes/2026-06-24-semantic-source-line-contract docs/plans/2026-06-24-semantic-source-line-contract.md docs/plan.md`
- Expected observable result: Changed covered Markdown paths route to the prose validator with correct enforce/audit behavior, and preservation evidence shows the first slice did not alter rendered meaning or ownership boundaries.
- Commit message: `M3: route documentation prose validation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before final closeout
- Risks:
  - Selected validation could over-select broad Markdown paths.
  - Behavior evidence could become another source of truth if it duplicates the spec.
- Rollback/recovery:
  - Disable selected-validation routing before reverting behavior evidence and validator integration.

## Validation plan

- `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-semantic-source-line-contract/`: validate formal review recording.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`: validate change metadata and profile authorization.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-24-semantic-source-line-contract.md --path specs/documentation-source-formatting.md --path docs/plans/2026-06-24-semantic-source-line-contract.md --path docs/plan.md --path docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`: validate lifecycle-managed artifacts.
- `git diff --check -- docs/proposals/2026-06-24-semantic-source-line-contract.md specs/documentation-source-formatting.md docs/plans/2026-06-24-semantic-source-line-contract.md docs/plan.md docs/changes/2026-06-24-semantic-source-line-contract`: validate whitespace.

## Risks and recovery

- Risk: validator false positives block legitimate prose.
  - Recovery: keep deterministic failures narrow, route ambiguous cases to warnings, and add regression fixtures before enabling enforcement.
- Risk: formatter configuration reintroduces a line-length rule.
  - Recovery: keep formatter guardrails explicit in the spec and test configuration behavior.
- Risk: Tier A cleanup becomes broad documentation reflow.
  - Recovery: limit edits to current README and VISION violations needed for enforcement and record behavior preservation.
- Risk: selected validation expands beyond the approved first slice.
  - Recovery: keep Tier C excluded and require a separate proposal for expansion.

## Dependencies

- Approved proposal and spec.
- Clean recorded proposal-review and spec-review.
- Recorded architecture assessment.
- Clean plan-review before test-spec and implementation.
- Active test spec before implementation.

## Progress

- 2026-06-24: Proposal accepted, spec approved, architecture assessment recorded as not required, and plan created for review.
- 2026-06-24: Plan-review R1 approved the plan with no material findings; workflow-managed authoring through plan-review completed.
- 2026-06-24: Test spec created and activated; ready for M1 implementation.
- 2026-06-24: Owner approved the active test spec for M1 implementation.
- 2026-06-24: M1 implementation added the non-mutating documentation prose validator, regression fixtures, and validator tests; handed to code-review R1.
- 2026-06-24: Code-review M1 R1 requested changes for `PROSE-M1-CR1` and `PROSE-M1-CR2`; M1 moved to `resolution-needed`.
- 2026-06-24: Review-resolution implemented fixes for `PROSE-M1-CR1` and `PROSE-M1-CR2`; M1 returned to `review-requested` for code-review R2.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-24 | Split implementation into validator, guidance, and selected-validation milestones. | The risk profiles differ and each slice can be reviewed independently. | One large implementation milestone. |
| 2026-06-24 | Treat architecture as not required for the first slice. | The plan uses existing repo-owned validation patterns and does not introduce a shared parser subsystem or generated-content ownership change. | Create an ADR for a leaf validator addition. |

## Surprises and discoveries

- M1 baseline audit found 10 warning-only source-line findings in current `README.md` and `VISION.md`; Tier A cleanup remains deferred to M2 as planned.
- Code-review M1 R1 found that explicit Markdown hard breaks are misclassified as mechanical wraps and mechanically continued list items are missed.
- Review-resolution changed the Tier A audit baseline from 0 errors and 10 warnings to 6 errors and 10 warnings by detecting existing README mechanically continued list items.

## Validation notes

- 2026-06-24: Plan-review R1 approved the plan with no material findings.
- 2026-06-24: Test spec created at `specs/documentation-source-formatting.test.md`.
- 2026-06-24: Owner approved the active test spec for implementation reliance.
- 2026-06-24: `python scripts/test-documentation-prose-validator.py` passed with 8 tests.
- 2026-06-24: `python scripts/validate-documentation-prose.py --mode audit --path README.md --path VISION.md` passed in audit mode with 0 errors and 10 warnings.
- 2026-06-24: `python scripts/validate-change-metadata.py docs/changes/2026-06-24-semantic-source-line-contract/change.yaml` passed.
- 2026-06-24: `git diff --check -- scripts/validate-documentation-prose.py scripts/test-documentation-prose-validator.py tests/fixtures/documentation-prose docs/changes/2026-06-24-semantic-source-line-contract` passed.
- 2026-06-24: Code-review M1 R1 recorded material findings `PROSE-M1-CR1` and `PROSE-M1-CR2`; review-resolution is open.
- 2026-06-24: `python scripts/test-documentation-prose-validator.py` passed with 13 tests after review-resolution fixes.
- 2026-06-24: `python scripts/validate-documentation-prose.py --mode enforce --path tests/fixtures/documentation-prose/pass/explicit-hard-break.md` passed with 0 errors and 0 warnings.
- 2026-06-24: `python scripts/validate-documentation-prose.py --mode enforce --path tests/fixtures/documentation-prose/fail/list-item-mechanical-continuation.md` returned the expected enforcement failure with 1 error.
- 2026-06-24: `python scripts/validate-documentation-prose.py --mode audit --path README.md --path VISION.md` passed in audit mode with 6 errors and 10 warnings.

## Outcome and retrospective

- Pending.

## Readiness

- See `Current Handoff Summary`.
- Downstream routing is owned by `Current Handoff Summary`.
