# Review Resolution: Lightweight Requirement-to-Delivery Model

## Summary

Closeout status: open

- Reviews covered: `design-review-r1`, `delivery-review-r1`
- Findings resolved: 1
- Unresolved findings: 2
- Current result: Design Review is approved; Delivery Review R1 requests bounded plan and test-specification corrections.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| RTD-DR1 | accepted | resolved | The active boundary-contract marker and valid example ownership are recorded; rereview the exact design package. |
| RTD-DLR1 | needs-decision | open | Six acceptance criteria lack explicit test-case ownership. |
| RTD-DLR2 | needs-decision | open | Plan allocation and multi-milestone proof timing do not agree. |

## Finding Details

### design-review-r1

#### RTD-DR1

Finding ID: RTD-DR1
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: specification author
Decision needed: none; the focused validator establishes the required structural correction.
Chosen action: Add `boundary_contract: boundary-first-v1` to the specification preamble and align each example's formal ownership row with every boundary it cites.
Rationale: New feature specifications must explicitly activate their complete boundary-first record; the current document contains the record but omits its activation marker.
Required outcome: The specification declares the active boundary contract and its feature record passes focused structural validation.
Safe resolution path: Add the marker, align the activated example ownership rows, register the revised specification through its authoring lifecycle operation, run focused feature-record validation, record the correction return and validation evidence, and request Design Review R2. The matching proof map remains owned by Delivery and is not fabricated during Design.
Follow-up: Design Review R2 over the revised exact architecture/specification package.
Validation target: `validate_feature_record` from `scripts/boundary_first_validation.py` returns no issues for `specs/lightweight-requirement-delivery-model.md`.
Validation evidence: Passed after registration at `sha256:6bc2d07d0a026201d52060ab9966ad850cf37b1d0f61203a8fc4512aa44d71a6`. The full changed-spec command now reports only `BFR-PROOF-MAP-MISSING` for the test specification that Delivery has not yet authored; it reports no feature-record defect.

### delivery-review-r1

#### RTD-DLR1

Finding ID: RTD-DLR1
Disposition: needs-decision
Status: open
Owner: test-specification author
Owning stage: test-spec
Decision owner: test-specification author
Decision needed: Accept the bounded traceability correction or explain why the six acceptance criteria do not require explicit test-case ownership.
Chosen action: pending
Rationale: The test specification claims complete acceptance coverage but does not identify proof owners for `RTD-AC2`, `RTD-AC3`, `RTD-AC5`, `RTD-AC7`, `RTD-AC9`, or `RTD-AC10`.
Required outcome: Every acceptance criterion maps to existing direct proof or an explicit justified gap.
Safe resolution path: Add the missing criterion identities to the appropriate existing test cases, register the revised test specification, validate its trace, and request Delivery Review R2.
Follow-up: Delivery Review R2 over the corrected exact package.
Validation target: The union of test-case `Covers` fields includes `RTD-AC1` through `RTD-AC10`.
Validation evidence: pending

#### RTD-DLR2

Finding ID: RTD-DLR2
Disposition: needs-decision
Status: open
Owner: plan and test-specification authors
Owning stage: plan, test-spec
Decision owner: plan and test-specification authors
Decision needed: Accept the bounded allocation and proof-timing correction or identify a different coherent milestone ownership model.
Chosen action: pending
Rationale: M3 proves `RTD-R20` without plan allocation, and five proof rows name tests and evidence from later milestones than their single recorded required milestone.
Required outcome: Plan requirement allocation, required proof milestones, test cases, and evidence timing agree.
Safe resolution path: Add `RTD-R20` to M3 allocation, list every required milestone on `PRF-002` through `PRF-005` and `PRF-009`, register both revisions, validate the exact pair, and request Delivery Review R2.
Follow-up: Delivery Review R2 over the corrected exact package.
Validation target: Every proof row's required milestones cover all named test and evidence milestones, and the plan allocates every requirement exercised by each milestone.
Validation evidence: pending
