# PR-readiness research selector bug fix

## Reproduction

After refreshing `origin/main`, the PR selector stopped with an
`unclassified-path` result for
`docs/research/2026-08-05-boundary-first-v1-activation-release.md`.

The expected behavior follows the canonical output contract in the research
skill: dated Markdown records under `docs/research/` are governed research
artifacts and should select the repository's documentation checks.

## Root cause

`scripts/validation_selection.py` had no category for the canonical
`docs/research/YYYY-MM-DD-slug.md` output path. The selector therefore failed
closed before any selected PR checks ran.

This was a selector integration omission. The research skill already defines
the path and no specification or architecture change is required.

## Regression and fix

A focused regression now requires a research artifact to be classified as
`research-artifact`, produce no blocking result, and select exactly
`documentation_prose.audit` and `markdown_readability.validate`.
The regression failed with the reproduced unclassified-path result before the
production change.

The production fix adds the exact Markdown path family and routes it to the
two existing documentation checks. It does not add a general documentation
fallback or change another category.

## Validation

- Focused regression before the fix: failed as expected.
- Focused regression after the fix: passed.
- Explicit research-artifact selection: passed with category
  `research-artifact`, no blocking result, and exactly the two documentation
  checks.
- `python scripts/test-select-validation.py`: 148 tests passed.
- `python scripts/validate-markdown-readability.py docs/research/2026-08-05-boundary-first-v1-activation-release.md`:
  passed with three non-blocking warnings.
- `python scripts/validate-documentation-prose.py --mode audit --path docs/research/2026-08-05-boundary-first-v1-activation-release.md`:
  completed in report-only audit mode with eight errors and ten warnings.
- `python scripts/select-validation.py --mode pr --base origin/main --head HEAD`:
  selection passed with 21 checks and no blocking result.

The complete PR-mode command must pass after independent code review before PR
handoff resumes.
