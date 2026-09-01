# Review Resolution: Simplify Final Verification and Retire Explain Change

## Summary

Closeout status: open

Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r1

- Reviews covered: `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m2-r1`
- Findings resolved: 2
- Unresolved findings: 5
- Current result: Code Review M2 R1 requested correction of evidence-surface closure, execution proof, evidence-tail registration, JavaScript/Python parity, and exact basis identity enforcement.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| FV-M1-CR1 | accepted | resolved | Governed, v1 or legacy, and v2 inventories now use parsed semantic lifecycle contracts and fail closed on unknown or unreadable metadata. |
| FV-M1-CR2 | accepted | resolved | Node, Python, and public-wrapper tests directly reject duplicate and unsorted final-verification manifest entries. |
| FV-M2-CR1 | accepted | open | Close and map every evidence proved-surface reference before applicability consistency. |
| FV-M2-CR2 | accepted | open | Bind actual runs, hosted observations, always-current checks, and reuse to exact proof identities. |
| FV-M2-CR3 | accepted | open | Require one exact report plus matching schema-valid content registration for a current evidence tail. |
| FV-M2-CR4 | accepted | open | Make JavaScript and Python reject identical duplicate and empty-content partitions. |
| FV-M2-CR5 | accepted | open | Enforce canonical immutable basis identities before successful readiness. |

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

### code-review-m2-r1

#### FV-M2-CR1

Finding ID: FV-M2-CR1
Disposition: accepted
Status: open
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; apply the bounded correction required by the approved evidence-map contract.
Chosen action: validate every proved-surface reference against the closed impact vocabulary and the classified impact map before freshness or decision consistency.
Rationale: freshness can determine execution but cannot authorize an unclassified evidence surface.
Required outcome: unknown, duplicate, or unmapped proved surfaces fail closed and valid multi-surface evidence remains conservative.
Safe resolution path: add identical JavaScript/Python validation and shared regressions, rerun every M2 command, and return M2 for rereview.
Follow-up: Code Review M2 R2.
Validation target: FV-R10, FV-R11, FV-R14, FV-R18, FV-R22, FV-R38, TG-06, TG-07.
Validation evidence: pending implementation correction and focused rerun.

#### FV-M2-CR2

Finding ID: FV-M2-CR2
Disposition: accepted
Status: open
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; implement the already-approved exact command and observed-result contract.
Chosen action: add execution-kind-specific proof identities for evidence and always-current entries.
Rationale: an execution label alone does not prove that a command ran or hosted evidence was observed.
Required outcome: successful reports bind exact command or observation proof, while cache hits and configured-only commands cannot establish a pass.
Safe resolution path: close entry shapes, update resources/skeleton, add direct negative and successful round-trip tests, and rerun M2 validation.
Follow-up: Code Review M2 R2.
Validation target: FV-R20, FV-R21, FV-R22, FV-R26, TG-08.
Validation evidence: pending implementation correction and focused rerun.

#### FV-M2-CR3

Finding ID: FV-M2-CR3
Disposition: accepted
Status: open
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; close the exact report and lifecycle-registration boundary approved by Design.
Chosen action: require and bind both tail members and exact report content, aligned with the actual lifecycle registration schema.
Rationale: an allow-list over supplied paths cannot detect a missing report or registration and cannot grant readiness after partial persistence.
Required outcome: only one complete report plus its matching content registration is current; every partial, mismatched, duplicated, trailing, or drifted state is non-authoritative.
Safe resolution path: replace the subset predicate with exact tail-state validation and add direct write/read-back/registration/replay/drift tests before M3 integration.
Follow-up: Code Review M2 R2.
Validation target: FV-R31-FV-R34, TG-09, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001.
Validation evidence: pending implementation correction and focused rerun.

#### FV-M2-CR4

Finding ID: FV-M2-CR4
Disposition: accepted
Status: open
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; restore the required cross-language conformance contract.
Chosen action: align exact always-current cardinality and successful explanation non-empty rules through shared fixtures.
Rationale: the runtime and repository validator must not disagree about whether the same report grants readiness.
Required outcome: JavaScript and Python return identical outcomes for duplicate checks, whitespace strings, empty list members, malformed collections, and every closed vocabulary.
Safe resolution path: add one shared fixture matrix and mirror error ordering and content validation in both implementations.
Follow-up: Code Review M2 R2.
Validation target: FV-R19, FV-R27, FV-R38, TG-09, BND-STATE-001.
Validation evidence: pending implementation correction and focused rerun.

#### FV-M2-CR5

Finding ID: FV-M2-CR5
Disposition: accepted
Status: open
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; enforce existing canonical identity types and formats.
Chosen action: validate each normalized basis member with its repository identity, revision, digest, safe-ID, review-ID, or repository-relative path contract.
Rationale: a non-empty scalar is not necessarily an exact immutable identity.
Required outcome: malformed or unresolved basis values cannot support success, while exact current identities continue to round-trip identically.
Safe resolution path: reuse existing validators, add shared invalid-format fixtures, and rerun M2 validation.
Follow-up: Code Review M2 R2.
Validation target: FV-R8, FV-R26, FV-R31, FV-R33, TG-05, BND-AUTH-001, INT-003.
Validation evidence: pending implementation correction and focused rerun.
