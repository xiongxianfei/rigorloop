# Review Resolution: Semantic Source-Line Contract

## Scope

This record tracks material review finding closeout for the semantic source-line contract change.

Closeout status: closed

## Resolution Entries

### code-review-m1-r1

Review closeout: closed

#### PROSE-M1-CR1

Finding ID: PROSE-M1-CR1
Disposition: accepted
Owner: implementation author
Owning stage: review-resolution
Chosen action: Update the prose validator so explicit Markdown hard breaks are handled before mid-sentence wrap classification and add direct structural-exclusion regression coverage.
Rationale: The approved spec requires explicit Markdown hard breaks to be excluded or separately handled, and the current validator reports them as deterministic mechanical wraps.
Required outcome: Explicit Markdown hard breaks do not produce deterministic prose-wrap errors.
Validation target: Add a failing-before/passing-after fixture for explicit hard breaks and rerun `python scripts/test-documentation-prose-validator.py`, targeted prose validation, review-artifact validation, change metadata validation, artifact lifecycle validation, and whitespace checks.
Validation evidence: Added `explicit-hard-break.md`, `explicit-hard-break-backslash.md`, and `no-hard-break-mechanical-wrap.md` fixtures plus named regression tests. `python scripts/test-documentation-prose-validator.py` passed with 13 tests. `python scripts/validate-documentation-prose.py --mode enforce --path tests/fixtures/documentation-prose/pass/explicit-hard-break.md` passed with 0 errors and 0 warnings.
Status: resolved; pending code-review rerun

#### PROSE-M1-CR2

Finding ID: PROSE-M1-CR2
Disposition: accepted
Owner: implementation author
Owning stage: review-resolution
Chosen action: Preserve list-item continuation context during segmentation, flag mechanically continued list items, and add paired fail/pass list fixtures.
Rationale: The approved spec requires mechanically continued list items to be deterministic violations, but the current validator misses them.
Required outcome: Mechanically continued list items fail unless they use valid Markdown structure that preserves a semantic unit.
Validation target: Add a failing-before/passing-after fixture for mechanically continued list items and rerun `python scripts/test-documentation-prose-validator.py`, targeted prose validation, review-artifact validation, change metadata validation, artifact lifecycle validation, and whitespace checks.
Validation evidence: Added `list-item-mechanical-continuation.md`, `list-item-nested-structure.md`, `list-item-single-line.md`, and `list-item-with-fenced-code.md` fixtures plus named regression tests. `python scripts/test-documentation-prose-validator.py` passed with 13 tests. `python scripts/validate-documentation-prose.py --mode enforce --path tests/fixtures/documentation-prose/fail/list-item-mechanical-continuation.md` returned the expected enforcement failure with 1 `mechanically continued list item` error.
Status: resolved; pending code-review rerun

## Baseline Audit Delta

Before the M1 review-resolution fix, `python scripts/validate-documentation-prose.py --mode audit --path README.md --path VISION.md` reported 0 errors and 10 warnings.
After the fix, the same command reports 6 errors and 10 warnings.
The warning count did not change; the 6 new audit-mode errors are existing README mechanically continued list items now detected by the accepted `PROSE-M1-CR2` fix.
