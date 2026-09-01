# Review Resolution: Simplify Final Verification and Retire Explain Change

## Summary

Closeout status: open

Review closeout: code-review-m1-r1

- Reviews covered: `code-review-m1-r1`
- Findings resolved: 0
- Unresolved findings: 2
- Current result: Code Review M1 R1 requested correction of semantic inventory discovery and direct final-manifest ordering proof.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| FV-M1-CR1 | accepted | open | Parse lifecycle contracts semantically when building governed and final-verification compatibility inventories. |
| FV-M1-CR2 | accepted | open | Add direct Node, Python, and public-boundary proof for duplicate and unsorted final-verification manifest entries. |

## Finding Details

### code-review-m1-r1

#### FV-M1-CR1

Finding ID: FV-M1-CR1
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: M1 implementer
Decision needed: none; apply the bounded correction required by the approved contract.
Chosen action: replace raw lifecycle-contract substring discovery with parsed semantic classification for governed records and the frozen v2 inventory.
Rationale: valid YAML representation must not change lifecycle identity, and comments or unrelated text must not select a contract.
Required outcome: wrapper inventory, Node runtime, and Python classifiers agree for quoted, ordinary, unknown, absent, commented, listed, and unlisted contract states.
Safe resolution path: reuse the safe YAML loader and shared classifier, add public wrapper regressions, rerun all M1 commands, and return the corrected M1 diff to Code Review.
Follow-up: Code Review M1 R2 after implementation correction.
Validation target: FV-R5, FV-R6, TG-01, TG-03, BND-COMPAT-001, INT-004.
Validation evidence: pending implementation correction and focused rerun.

#### FV-M1-CR2

Finding ID: FV-M1-CR2
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: M1 implementer
Decision needed: none; add the direct proof already allocated by M1.
Chosen action: add duplicate and raw-UTF-8 ordering regressions for the final-verification activation manifest at helper and public boundaries.
Rationale: passing older-manifest ordering tests does not directly prove the newly introduced manifest validator.
Required outcome: duplicate and unsorted new-manifest entries fail directly in Node and Python, and malformed active inventory cannot pass the public wrapper.
Safe resolution path: add named regressions, retain unknown-value-first behavior, rerun all M1 commands, and return the corrected M1 diff to Code Review.
Follow-up: Code Review M1 R2 after implementation correction.
Validation target: TG-02, FV-R5, FV-R6, FV-R38, BND-COMPAT-001.
Validation evidence: pending implementation correction and focused rerun.
