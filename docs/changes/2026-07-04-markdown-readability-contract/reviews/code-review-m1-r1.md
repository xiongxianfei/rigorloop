# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1. Readability Validator and Deterministic Fixtures
Reviewed artifact: commit 7426647f
Review date: 2026-07-04
Reviewed commit: 7426647f
Status: changes-requested
Review status: changes-requested
Material findings: MDREAD-M1-CR1
Recording status: recorded
Recording blocker: none
Reviewed milestone: M1
Milestone closeout: resolution-needed
Required review-resolution: yes
Immediate next stage: review-resolution M1
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-07-04-markdown-readability-contract/reviews/code-review-m1-r1.md
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: MDREAD-M1-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-04-markdown-readability-contract/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-07-04-markdown-readability-contract/review-log.md
- Review resolution: docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md#code-review-m1-r1
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2
- Required review-resolution: yes
- Finding IDs: MDREAD-M1-CR1
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `7426647f M1: add markdown readability validator`.
- Tracked governing branch state: proposal, spec, test spec, plan, test-spec-review, and M1 implementation are tracked through commit `7426647f`.
- Governing artifacts: `specs/markdown-readability-contract.md`, `specs/markdown-readability-contract.test.md`, `docs/plans/2026-07-04-markdown-readability-contract.md`, `docs/changes/2026-07-04-markdown-readability-contract/reviews/test-spec-review-r1.md`.
- Validation evidence: M1 validation notes in `docs/plans/2026-07-04-markdown-readability-contract.md` and `docs/changes/2026-07-04-markdown-readability-contract/change.yaml`.

## Diff summary

M1 adds `scripts/validate-markdown-readability.py`, fixture-driven tests in `scripts/test-markdown-readability-validator.py`, and selector composition through `markdown_readability.validate` in `scripts/validation_selection.py`.
The validator reports stable `MDREAD-*` diagnostics for known semantic hard-wrap splits, audit-only long-line and dense-paragraph warnings, generated-region marker syntax and pairing, generated-document placeholders, and prose-line exclusions for code fences, tables, HTML blocks, link references, and generated regions.
Lifecycle artifacts record the proposal, spec, plan, test spec, upstream reviews, M1 validation evidence, and M1 handoff.

## Findings

### MDREAD-M1-CR1 - Selector-composed README and VISION validation never enables changed-section enforcement

Finding ID: MDREAD-M1-CR1
Severity: major
Location: `scripts/validation_selection.py:722`, `scripts/validation_selection.py:1294`, `scripts/validation_selection.py:1343`
Evidence: The approved spec requires first-slice README and `VISION.md` semantic source-line checks to apply to changed sections only, and the approved test spec maps T3/T13 to changed-section README and `VISION.md` enforcement. The selector adds `markdown_readability.validate` for README and root `VISION.md` paths, but `catalog_command` renders it as `python scripts/validate-markdown-readability.py <paths>` with no `--changed-section` argument. Direct repro confirms the gap: `python scripts/validate-markdown-readability.py README.md` returns exit 0 with `MDREAD-001` as a warning for a split `proposal to spec`, while the same file with `--changed-section README.md:3:4` returns exit 1.
Required outcome: Selector-composed readability validation for README and `VISION.md` changes must preserve changed-section enforcement, or the selector must avoid claiming enforcement it cannot perform and route callers to a command shape that supplies changed-section ranges.
Safe resolution path: Extend selector support and tests so README and `VISION.md` path selections either include changed-section ranges in the selected readability command or expose a deterministic wrapper/check that derives and passes those ranges. Add a regression test where selector-selected readability validation fails a changed README or `VISION.md` hard-wrap fixture, rerun `python scripts/test-markdown-readability-validator.py`, `python scripts/test-select-validation.py`, `python scripts/validate-markdown-readability.py`, change metadata validation, review artifact validation, artifact lifecycle validation, and whitespace checks, then return M1 to `review-requested` for code-review rerun.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | MDREAD-M1-CR1: R32 requires changed-section README and `VISION.md` semantic source-line enforcement, but the composed selector command does not pass changed-section ranges. |
| Test coverage | concern | `scripts/test-markdown-readability-validator.py` covers direct `--changed-section` behavior, but `scripts/test-select-validation.py` only asserts the check ID is selected and does not prove the selected command enforces changed-section failures. |
| Edge cases | block | EC5 requires changed README split phrases to fail and EC6 requires untouched historical text to remain audit-only; the current selector path exercises only the audit-only behavior. |
| Error handling | pass | Direct validator failures for malformed generated-region markers, missing source metadata, placeholders, and invalid changed-section line ranges are bounded and local. |
| Architecture boundaries | pass | M1 stays inside repository-owned scripts and selector routing; no architecture artifact was required by spec-review. |
| Compatibility | concern | Historical Markdown remains audit-only, but the selected README/`VISION.md` route silently weakens first-slice changed-section enforcement. |
| Security/privacy | pass | The validator reads repository-local Markdown and uses repository-relative source/generator marker metadata in tests; no secrets, network state, or machine-local paths are introduced into tracked fixtures. |
| Derived artifact currency | pass | M1 does not touch generated adapter output; M2 owns generated artifact guidance and adapter proof. |
| Unrelated changes | pass | The implementation diff is scoped to lifecycle artifacts, the readability validator, its tests, and selector integration. |
| Validation evidence | concern | Recorded validation commands passed, but they do not prove selector-composed changed-section enforcement for README or `VISION.md`. |

## Recommended next stage

`review-resolution M1` for `MDREAD-M1-CR1`, followed by targeted implementation fixes on M1 and a rerun code-review.

## Milestone handoff

- Reviewed milestone: M1
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1, M2
- Next stage: review-resolution M1
- Final closeout readiness: not ready; M1 has an open material finding and M2 remains unimplemented.
