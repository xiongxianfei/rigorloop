# Boundary-First M4 Code Review R1

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: two independent Codex code reviewers
Target: commit 59b56fec
Reviewed artifact: commit 59b56fec
Review date: 2026-07-28
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: PBF-M4-CR1, PBF-M4-CR2
Immediate next stage: review-resolution
Implementation handoff: not-allowed

## Finding

### PBF-M4-CR1

Finding ID: PBF-M4-CR1
Severity: blocker
Location: rollback selection and production activation validation
Evidence: The rollback matrix helper trusts caller-supplied activation data,
has no production caller, and returns no selected release. An active production
validation can therefore omit rollback metadata, while a caller can select a
release when the authoritative manifest is pending.
Required outcome: Read and validate the fixed activation manifest, derive the
rollback release only from it, enforce selection during active production
validation, and output the selected release with the ordered matrix.
Safe resolution path: Keep an internal matrix helper, add an authoritative
selector/result, integrate it into active validation and CLI output, and use an
isolated authoritative active fixture.
needs-decision rationale: none

### PBF-M4-CR2

Finding ID: PBF-M4-CR2
Severity: major
Location: rollback containment and non-mutation tests
Evidence: No direct test exercises unsafe manifest/metadata paths, and negative
cases snapshot only two files rather than the complete relevant fixture tree
and outside targets.
Required outcome: Prove missing, non-regular, and symlinked authoritative
paths fail; prove containment and complete before/after non-mutation.
Safe resolution path: Add local temporary-root regressions and outside
sentinels without any installer or publication hook.
needs-decision rationale: none

## Confirmed behavior

Package/install parity for all 28 included pairs, adapter-owned exclusions,
archive diagnostics, negative metadata matrices, and excluded-scope behavior
are otherwise sound.
