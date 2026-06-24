# Review Resolution: Semantic Source-Line Contract

## Scope

This record tracks material review finding closeout for the semantic source-line contract change.

Closeout status: open

## Resolution Entries

### code-review-m1-r1

Review closeout: open

#### PROSE-M1-CR1

Finding ID: PROSE-M1-CR1
Disposition: accepted
Owner: implementation author
Owning stage: review-resolution
Chosen action: Update the prose validator so explicit Markdown hard breaks are handled before mid-sentence wrap classification and add direct structural-exclusion regression coverage.
Rationale: The approved spec requires explicit Markdown hard breaks to be excluded or separately handled, and the current validator reports them as deterministic mechanical wraps.
Required outcome: Explicit Markdown hard breaks do not produce deterministic prose-wrap errors.
Validation target: Add a failing-before/passing-after fixture for explicit hard breaks and rerun `python scripts/test-documentation-prose-validator.py`, targeted prose validation, review-artifact validation, change metadata validation, artifact lifecycle validation, and whitespace checks.
Status: open

#### PROSE-M1-CR2

Finding ID: PROSE-M1-CR2
Disposition: accepted
Owner: implementation author
Owning stage: review-resolution
Chosen action: Preserve list-item continuation context during segmentation, flag mechanically continued list items, and add paired fail/pass list fixtures.
Rationale: The approved spec requires mechanically continued list items to be deterministic violations, but the current validator misses them.
Required outcome: Mechanically continued list items fail unless they use valid Markdown structure that preserves a semantic unit.
Validation target: Add a failing-before/passing-after fixture for mechanically continued list items and rerun `python scripts/test-documentation-prose-validator.py`, targeted prose validation, review-artifact validation, change metadata validation, artifact lifecycle validation, and whitespace checks.
Status: open
