# Code Review R3

Review ID: code-review-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review skill
Target: `origin/main..HEAD`
Status: changes-requested

## Scope

This first-pass implementation review covered the completed review finding resolution contract branch after M4 lifecycle closeout.

## Findings

### CR3-F1: Closeout validation accepts stale open findings in review-log.md

Finding ID: CR3-F1

Evidence: `specs/review-finding-resolution-contract.md` requires `review-log.md` to show whether review findings remain open, and closeout validation passed a manual probe where `review-resolution.md` was `Closeout status: closed` but `review-log.md` still listed `Open findings: CR1-F1`.

Required outcome: Closeout validation must fail when any review-log entry still lists open findings during a closed handoff.

Suggested resolution: In closeout mode, reject any non-empty `Open findings:` set in `review-log.md`, and add focused regression coverage.

### CR3-F2: Resolution links in review-log.md are parsed but not validated

Finding ID: CR3-F2

Evidence: The canonical review-log block includes `Resolution: review-resolution.md#<Review ID>`, but `scripts/review_artifact_validation.py` stored that field without checking the target path, anchor, or referenced review-resolution section. A manual probe changing the anchor to `#wrong-review` still passed structure validation.

Required outcome: Structural validation must fail when a review-log `Resolution:` field is missing, malformed, targets any file other than `review-resolution.md`, uses an anchor that does not match the entry Review ID, or points to a Review ID not represented in `review-resolution.md` when that artifact exists.

Suggested resolution: Validate `Resolution:` as exactly `review-resolution.md#<Review ID>`, validate the anchor against `review-resolution.md` headings when the artifact exists, and add focused regression coverage.

### CR3-F3: CI changed-root test is too shallow for T13

Finding ID: CR3-F3

Evidence: `specs/review-finding-resolution-contract.test.md` T13 describes a changed-root CI discovery test, but the implemented test only checks that `scripts/ci.sh` contains expected strings.

Required outcome: Either add direct changed-root CI discovery proof or record an owner decision that the current lighter coverage is sufficient for v1.

Suggested resolution: Add an integration-style temporary git or controlled changed-path test, unless the maintainer decides that the additional test weight is not needed for this version.
