# Code Review M1 R1: Semantic Source-Line Contract

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1. Markdown Block Segmentation, Validator Modes, and Regression Fixtures
Reviewed artifact: implementation commit `7418656b`
Review date: 2026-06-24
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-24-semantic-source-line-contract/reviews/code-review-m1-r1.md`, `docs/changes/2026-06-24-semantic-source-line-contract/review-log.md`, `docs/changes/2026-06-24-semantic-source-line-contract/review-resolution.md`, `docs/plans/2026-06-24-semantic-source-line-contract.md`, `docs/plan.md`, `docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: PROSE-M1-CR1, PROSE-M1-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-24-semantic-source-line-contract/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-06-24-semantic-source-line-contract/review-log.md`
- Review resolution: `docs/changes/2026-06-24-semantic-source-line-contract/review-resolution.md`
- Reviewed milestone: M1. Markdown Block Segmentation, Validator Modes, and Regression Fixtures
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: PROSE-M1-CR1, PROSE-M1-CR2
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `7418656b` (`M1: add documentation prose validator`).
- Tracked governing branch state: committed proposal, approved spec, active test spec, active plan, change metadata, review log, and M1 implementation are tracked on `feature/semantic-source-line-contract`.
- Governing artifacts:
  - `specs/documentation-source-formatting.md`
  - `specs/documentation-source-formatting.test.md`
  - `docs/plans/2026-06-24-semantic-source-line-contract.md`
  - `docs/changes/2026-06-24-semantic-source-line-contract/change.yaml`
- Validation evidence reviewed:
  - `python scripts/test-documentation-prose-validator.py` passed with 8 tests.
  - `python scripts/validate-documentation-prose.py --mode audit --path README.md --path VISION.md` passed in audit mode with 0 errors and 10 warnings.
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-24-semantic-source-line-contract/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/documentation-source-formatting.md --path specs/documentation-source-formatting.test.md --path docs/plans/2026-06-24-semantic-source-line-contract.md --path docs/plan.md --path docs/changes/2026-06-24-semantic-source-line-contract/change.yaml` passed.
  - `git diff --check -- scripts/validate-documentation-prose.py scripts/test-documentation-prose-validator.py tests/fixtures/documentation-prose docs/plans/2026-06-24-semantic-source-line-contract.md docs/plan.md docs/changes/2026-06-24-semantic-source-line-contract` passed.
- Additional reviewer probes:
  - `python scripts/validate-documentation-prose.py --mode enforce --path <explicit-hard-break-fixture>` failed with a mechanical-wrap error.
  - `python scripts/validate-documentation-prose.py --mode enforce --path <list-continuation-fixture>` passed with 0 errors.

## Diff Summary

M1 adds `scripts/validate-documentation-prose.py`, a non-mutating Markdown prose validator with block segmentation, CLI modes, path selection, diagnostics, deterministic source-line findings, and warnings for ambiguous breaks.
It adds fixture-backed tests and pass/fail/warn fixtures under `tests/fixtures/documentation-prose/`.
The commit also records the proposal, spec, test spec, plan, review evidence, and implementation validation for the workflow-managed change.

## Findings

### PROSE-M1-CR1: Explicit Markdown hard breaks are reported as mechanical wraps

Finding ID: PROSE-M1-CR1
Severity: major
Location: `scripts/validate-documentation-prose.py:169`, `scripts/validate-documentation-prose.py:236`
Evidence: Requirement R11 says explicit Markdown hard breaks must be excluded or separately handled. The segmentation logic does not detect two-space or backslash hard-break endings before prose classification. A reviewer probe with `This line uses an explicit Markdown hard break  ` followed by `with continuation.` returned exit code 1 and reported `error: mechanical mid-sentence wrap`. That is a false deterministic failure for a Markdown structure the spec says must not be misclassified as prose wrapping.
Required outcome: Explicit Markdown hard breaks must be handled before mid-sentence wrap classification so they do not produce deterministic prose-wrap errors.
Safe resolution path: Add a hard-break detector for two trailing spaces and trailing backslash before `strip()` removes the signal, split or skip the hard-break pair as a Markdown structure, and add a fixture-backed regression test under the structural exclusion coverage.
needs-decision rationale: none

### PROSE-M1-CR2: Mechanically continued list items are not detected

Finding ID: PROSE-M1-CR2
Severity: major
Location: `scripts/validate-documentation-prose.py:177`
Evidence: Requirement R12 says deterministic violations must include mechanically continued list items. The current segmentation flushes a list marker into a single one-line `list-item` block, then treats the following two-space continuation as an unrelated paragraph line. A reviewer probe with `- This list item is` followed by `  mechanically continued.` returned exit code 0 with `errors=0 warnings=0`, so the named deterministic violation is missed.
Required outcome: Mechanically continued list items must be classified and reported as deterministic violations unless they use valid Markdown structure that preserves a semantic unit.
Safe resolution path: Preserve list-item continuation context during segmentation, flag plain continuation lines that mechanically complete the item, and add a regression fixture showing the bad continuation fails while a structured nested list or complete one-line item passes.
needs-decision rationale: none

## Checklist Coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | PROSE-M1-CR1 violates R11 structural handling; PROSE-M1-CR2 violates R12 deterministic list-continuation coverage. |
| Test coverage | concern | The 8 tests cover core regressions, commands, lifecycle chains, generated-marker skips, tables, URLs, frontmatter, and non-mutation, but they miss explicit hard breaks and mechanically continued list items. |
| Edge cases | block | Explicit Markdown hard breaks and mechanically continued list items are named contract edges and fail reviewer probes. |
| Error handling | pass | The CLI exits nonzero only for errors in enforce mode and audit mode remains non-failing; no unsafe exception path was found in reviewed probes. |
| Architecture boundaries | pass | M1 is a leaf validator and fixture addition; no shared Markdown parsing subsystem or generated-content ownership change was introduced. |
| Compatibility | concern | The false hard-break error would make a valid Markdown construct incompatible with enforcement mode. |
| Security/privacy | pass | The validator reads Markdown as text, does not execute content, and does not follow links or process active document objects. |
| Derived artifact currency | pass | Generated README marker blocks are skipped and no generated outputs are edited in M1. |
| Unrelated changes | pass | The diff is scoped to the approved proposal/spec/test/plan/change artifacts and the M1 validator/tests/fixtures. |
| Validation evidence | concern | Recorded validation commands are relevant and passed, but they did not cover the two failing reviewer probes. |

## No-Finding Rationale

Not applicable. PROSE-M1-CR1 and PROSE-M1-CR2 require resolution before M1 can close.

## Residual Risks

The Tier A cleanup, contributor guidance, formatter guardrails, and selected-validation routing remain planned for M2 and M3.
This review does not evaluate those future milestones.

## Milestone Handoff

M1 moves to `resolution-needed`.
The next stage is `review-resolution` for PROSE-M1-CR1 and PROSE-M1-CR2, then an M1 fix and rerun `code-review`.
Do not start M2 until both findings are resolved and M1 passes re-review.
