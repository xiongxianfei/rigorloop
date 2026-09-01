# Review Resolution: Simplify Final Verification and Retire Explain Change

## Summary

Closeout status: closed

Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2

- Reviews covered: `code-review-m1-r1`, `code-review-m1-r2`
- Findings resolved: 2
- Unresolved findings: 0
- Current result: Code Review M1 R2 confirmed semantic inventory discovery and direct final-manifest ordering proof; both R1 findings are resolved.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| FV-M1-CR1 | accepted | resolved | Governed, v1 or legacy, and v2 inventories now use parsed semantic lifecycle contracts and fail closed on unknown or unreadable metadata. |
| FV-M1-CR2 | accepted | resolved | Node, Python, and public-wrapper tests directly reject duplicate and unsorted final-verification manifest entries. |

## Finding Details

### code-review-m1-r1

#### FV-M1-CR1

Finding ID: FV-M1-CR1
Disposition: accepted
Status: resolved
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
Validation evidence: Code Review M1 R2 inspected `311b2f3b..17067726`; quoted v2 and v3, misleading-comment, unknown-contract, and public inventory regressions pass. Reviewer probes also proved unrelated scalar text does not select a contract, malformed metadata fails explicitly, and quoted v1 plus unversioned inventory remains valid. The 71-test Node suite, 87-test change-metadata suite, 167-test artifact-lifecycle suite, and 16-test governed-wrapper suite passed.

#### FV-M1-CR2

Finding ID: FV-M1-CR2
Disposition: accepted
Status: resolved
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
Validation evidence: Code Review M1 R2 confirmed direct duplicate, raw-UTF-8-unsorted, and unknown-value-first final-manifest tests in Node and Python, plus duplicate and ordering failures at the public wrapper boundary. The complete planned M1 command set passed.

### code-review-m1-r2

No material findings.
