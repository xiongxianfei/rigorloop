# Explain Change: Semantic Source-Line Contract

## Summary

This change makes review-critical Markdown source lines preserve semantic units instead of arbitrary editor column wraps.
It adds an authoritative documentation source-formatting contract, a non-mutating prose validator with regression fixtures, contributor and formatter guardrails, Tier A README/VISION cleanup, selected-validation routing, and behavior-preservation evidence.

The implementation intentionally keeps enforcement narrow.
`README.md` and `VISION.md` are Tier A enforcement surfaces, `skills/**/SKILL.md` and `docs/changes/**/explain-change.md` are Tier B audit surfaces, and historical or source-of-truth Markdown outside that slice stays out of first-slice prose validation.

## Problem

The accepted proposal records repeated hard-wrap corrections in adopter-facing README/VISION prose, skill prose, and explain-change prose.
Rendered Markdown looked acceptable, but physical source lines split phrases, lifecycle chains, commands, and public positioning in ways that made review harder.

Learn guidance already described semantic line breaks, but it was not an action-owning contract.
The repository lacked a normative formatting spec, a covered-surface taxonomy, deterministic versus warning classification, generated-content ownership rules, regression fixtures, selected validation, and a required source-form review step.

## Decision Trail

The proposal selected Option 5: an authoritative contract, targeted authoring guidance, and bounded validation.
That option was chosen because a fixed line-length rule or automatic Markdown reflow would recreate the defect by optimizing column width instead of reviewability.

The approved spec made the contract concrete through R1-R19.
The central requirements are R1 through R4 for semantic units and first-slice coverage, R8 through R14 for non-mutating validator behavior and diagnostics, R15 for marker ownership, R16 and R17 for contributor and formatter guardrails, R18 for source-form review, and R19 for evidence-based expansion.

Architecture was recorded as not required because the implementation uses existing repository-owned validation scripts and selected-validation routing.
It does not introduce a shared Markdown parser subsystem, a generated-content ownership change, or a new runtime architecture boundary.

The plan split the work into three implementation milestones.
M1 added validator behavior and fixtures.
M2 added contributor guidance, formatter guardrails, and Tier A cleanup.
M3 added selected-validation routing and behavior-preservation evidence.

## Diff Rationale By Area

| Area | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- |
| `specs/documentation-source-formatting.md` | Added the authoritative semantic source-line contract. | Move the rule out of learn guidance and into a normative contract. | Proposal Option 5; R1-R19 | Spec-review R1 approved. |
| `specs/documentation-source-formatting.test.md` | Added traceable tests for validator behavior, routing, guardrails, source review, and preservation. | Make each contract boundary testable before implementation. | R1-R19; AC1-AC15 | Test-spec approved by owner before implementation. |
| `scripts/validate-documentation-prose.py` | Added Markdown block segmentation, audit/enforce modes, deterministic errors, warnings, diagnostics, explicit hard-break handling, list-item continuation handling, and non-mutating behavior. | Catch the documented hard-wrap failures without rewriting prose or treating length as a defect. | R8-R14; EC1-EC10 | `python scripts/test-documentation-prose-validator.py` passed with 14 tests. |
| `tests/fixtures/documentation-prose/**` | Added pass, fail, and warning fixtures for semantic lines, structural exclusions, named regressions, hard breaks, list items, commands, and lifecycle chains. | Lock in the actual recurrence patterns and reviewer-probe failures. | T1-T17 | M1 R2 confirmed explicit hard-break and list-item findings resolved. |
| `CONTRIBUTING.md` | Added concise contributor-facing Markdown source-line guidance and the Tier A validation command. | Put the short policy where GitHub surfaces contribution guidance, without duplicating the full spec. | R16 | M2 code-review passed. |
| `docs/workflows.md` | Added a pointer to `CONTRIBUTING.md` and the normative spec. | Keep workflow guidance aligned while avoiding a second formatting contract. | R16 | Guide-system validation passed. |
| `.prettierrc.json` and `.markdownlint.json` | Added `proseWrap: preserve` and disabled `MD013`. | Prevent common tools from mechanically rewrapping covered prose. | R17 | `test_formatter_guardrails_preserve_markdown_prose_wrapping` passed. |
| `README.md` and `VISION.md` | Cleaned current Tier A source-line violations without broad historical reflow. | Make whole-file Tier A enforcement possible while preserving rendered meaning and marker ownership. | R1-R7, R15, R18 | Tier A enforcement passed with 0 errors and 0 warnings; README marker validation passed. |
| `scripts/validation_selection.py` and `scripts/select-validation.py` | Added `documentation_prose.enforce`, `documentation_prose.audit`, Tier A/Tier B routing, Tier C exclusion behavior, and a `--changed-file` alias. | Compose prose validation into selected validation without displacing existing checks. | R2-R4, R8-R9, R19; T18 | `python scripts/test-select-validation.py` passed with 103 tests. |
| `docs/changes/2026-06-24-semantic-source-line-contract/behavior-preservation.md` | Recorded rendered README, marker ownership, VISION meaning, retired vocabulary, skill behavior, historical documentation, and source reviewability preservation. | Prove the first slice changed source review and validation routing without changing document meaning or ownership boundaries. | R15, R18, AC5, AC11-AC13 | Artifact lifecycle validation passed. |
| Change-local review and plan artifacts | Recorded proposal/spec/plan reviews, M1 material findings, review-resolution, clean M1/M2/M3 code reviews, and milestone handoffs. | Preserve workflow traceability and keep the active plan as the live state owner. | Workflow contract; active plan | Review-artifact validation passed. |

## Tests Added Or Changed

T1 through T17 are implemented in `scripts/test-documentation-prose-validator.py` and fixture files.
They prove mechanical wraps fail, long semantic lines pass, sentence-per-line paragraphs pass, command and lifecycle splits fail, structural Markdown is excluded, diagnostics are actionable, and the validator is non-mutating.

M1 review added explicit reviewer-probe coverage.
`test_explicit_hard_break_two_space_passes_enforce`, `test_explicit_hard_break_backslash_passes_enforce`, and `test_mechanical_wrap_without_hard_break_still_fails_enforce` prove explicit Markdown hard breaks are intentional boundaries while ordinary wraps still fail.
`test_mechanically_continued_list_item_fails_enforce` and `test_nested_list_structure_passes_enforce` prove mechanically continued list items are caught while valid nested structure remains allowed.

T22 is covered by `test_formatter_guardrails_preserve_markdown_prose_wrapping`.
It proves the root Prettier and markdownlint configuration preserves prose wrapping and disables fixed line-length enforcement.

T18 is covered by `scripts/test-select-validation.py`.
The selected-validation tests prove Tier A routes to enforcement without losing README marker or guide checks, Tier B routes to audit without repository failure, and Tier C does not select first-slice prose validation.

T19 and T20 are covered by README marker validation and behavior-preservation evidence.
The README generated marker block remains owned by `VISION.md`, and corrections to generated vision wording belong in the canonical source.

## Validation Evidence Available Before Final Verify

The following validation has already passed during implementation and code review:

- `python scripts/test-documentation-prose-validator.py`
- `python scripts/validate-documentation-prose.py --mode enforce --path README.md --path VISION.md`
- `python scripts/validate-readme.py`
- `python scripts/validate-readme.py README.md --vision-markers`
- `python scripts/validate-guide-system.py`
- `python scripts/test-select-validation.py`
- `python scripts/select-validation.py --mode explicit --changed-file README.md --changed-file VISION.md`
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-semantic-source-line-contract/`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- scoped `git diff --check` commands for the touched implementation and lifecycle surfaces

No hosted CI result has been observed in this stage.
Final verification, branch readiness, PR-body readiness, and PR-open readiness are not claimed here.

## Review Resolution Summary

Code-review M1 R1 recorded two material findings.
Both were accepted and resolved in [review-resolution.md](review-resolution.md): `PROSE-M1-CR1` for explicit Markdown hard breaks and `PROSE-M1-CR2` for mechanically continued list items.

The final review-resolution state is closed.
There are two material findings, two closed findings, zero open findings, and no `needs-decision` dispositions.

Code-review M1 R2, M2 R1, and M3 R1 were clean with no material findings.
M3 R1 closed the final implementation milestone and handed the change to this explain-change stage.

## Alternatives Rejected

Fixed Markdown line-length enforcement was rejected because it would recreate the original problem by treating long lines as defects and splitting semantic units.

Automatic Markdown reflow was rejected because it can rewrite reviewer-sensitive prose, create noisy diffs, and conflict with generated marker ownership.

Learn guidance alone was rejected because the recurrence happened after learn guidance already existed.

Repository-wide Markdown enforcement was rejected for the first slice because existing Markdown contains unknown baseline debt and the proposal explicitly requires an evidence-based expansion decision.

Direct edits to generated README marker content were rejected because marker-owned content must be fixed in `VISION.md` or the synchronization mechanism.

## Scope Control

The change does not impose an 80-, 88-, 100-, or other fixed-column prose limit.
It does not require every Markdown paragraph to be physically one line.
It does not reflow all Markdown, migrate historical documentation, or enforce prose validation across specs, plans, review records, learn artifacts, or release evidence.

The validator is non-mutating and does not auto-fix prose.
It emits diagnostics and leaves joining, rewriting, or restructuring to authors and reviewers.

The selected-validation integration preserves existing README, marker, guide-system, skill, lifecycle, and review-artifact checks.
It adds prose validation routing instead of replacing existing validators.

## Risks And Follow-Ups

False positives remain the main long-term risk.
The first slice mitigates that by failing only deterministic Tier A cases, warning for ambiguous cases, and keeping Tier B audit-only.

Tier B audit findings still need human disposition when those files change.
Future enforcement for canonical skills or explain-change artifacts should require a separate evidence-based proposal.

Behavior preservation is recorded for the first slice, but final verify still needs to check artifact coherence, validation currency, and PR readiness.
The active plan remains active because `verify` and `pr` have not run.
