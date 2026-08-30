# Review Resolution: Lightweight Requirement-to-Delivery Model

## Summary

Closeout status: closed

- Reviews covered: `design-review-r1`, `delivery-review-r1`, `code-review-m1-r1`
- Findings resolved: 4
- Unresolved findings: 0
- Current result: RTD-M1-CR1 is corrected and ready for independent M1 Code Review R2.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| RTD-DR1 | accepted | resolved | The active boundary-contract marker and valid example ownership are recorded; rereview the exact design package. |
| RTD-DLR1 | accepted | resolved | All ten acceptance criteria now have explicit test-case ownership. |
| RTD-DLR2 | accepted | resolved | M3 owns RTD-R20 and every multi-milestone proof row names its complete timing. |
| RTD-M1-CR1 | accepted | resolved | Added and directly proved a concise many-to-many allocation example in both mapping directions. |

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
Disposition: accepted
Status: resolved
Owner: test-specification author
Owning stage: test-spec
Decision owner: test-specification author
Decision needed: none; the bounded traceability correction is accepted.
Chosen action: Add RTD-AC2, RTD-AC3, RTD-AC5, RTD-AC7, RTD-AC9, and RTD-AC10 to the existing direct test cases that prove their outcomes.
Rationale: The test specification claims complete acceptance coverage but does not identify proof owners for `RTD-AC2`, `RTD-AC3`, `RTD-AC5`, `RTD-AC7`, `RTD-AC9`, or `RTD-AC10`.
Required outcome: Every acceptance criterion maps to existing direct proof or an explicit justified gap.
Safe resolution path: Add the missing criterion identities to the appropriate existing test cases, register the revised test specification, validate its trace, and request Delivery Review R2.
Follow-up: Delivery Review R2 over the corrected exact package.
Validation target: The union of test-case `Covers` fields includes `RTD-AC1` through `RTD-AC10`.
Validation evidence: The union of RTD-T01 through RTD-T08 now cites RTD-AC1 through RTD-AC10, and boundary-first validation passes for the exact feature/test-spec pair at test-spec identity `sha256:5616ca914618d9bbde256f80acf61447a19cd62fe8f0dda4a488bffe614bdeb2`.

#### RTD-DLR2

Finding ID: RTD-DLR2
Disposition: accepted
Status: resolved
Owner: plan and test-specification authors
Owning stage: plan, test-spec
Decision owner: plan and test-specification authors
Decision needed: none; the bounded allocation and timing correction is accepted.
Chosen action: Add RTD-R20 to M3 allocation; set PRF-002 to M1 and M2, PRF-003 through PRF-005 to M2 and M3, and PRF-009 to M1 and M2.
Rationale: M3 proves `RTD-R20` without plan allocation, and five proof rows name tests and evidence from later milestones than their single recorded required milestone.
Required outcome: Plan requirement allocation, required proof milestones, test cases, and evidence timing agree.
Safe resolution path: Add `RTD-R20` to M3 allocation, list every required milestone on `PRF-002` through `PRF-005` and `PRF-009`, register both revisions, validate the exact pair, and request Delivery Review R2.
Follow-up: Delivery Review R2 over the corrected exact package.
Validation target: Every proof row's required milestones cover all named test and evidence milestones, and the plan allocates every requirement exercised by each milestone.
Validation evidence: The plan at `sha256:0c912fc274d278329690401c91df7380aad3a06e2a605af1d5fd283cb73f839f` allocates RTD-R20 to M3, the exact revised proof map records every named milestone, and boundary-first validation passes.

### code-review-m1-r1

#### RTD-M1-CR1

Finding ID: RTD-M1-CR1
Disposition: accepted
Status: resolved
Owner: implementation owner
Owning stage: implement M1
Decision owner: implementation owner
Decision needed: none; the bounded correction is accepted.
Chosen action: Add a concrete two-line mapping example to the canonical source and four identical M1 copies, and require both directions in the focused regression.
Rationale: The shared reference states that SR/work mappings may be many-to-many but does not include the concrete larger example required by RTD-AC4, the approved M1 plan, and RTD-T03/RTD-T04; the focused test checks only phrases.
Required outcome: The published M1 package demonstrates both one-SR-to-multiple-work and multiple-SR-to-one-work allocation, and focused proof detects loss of either direction without requiring a new artifact or complete hierarchy.
Safe resolution path: Add one concise example to the canonical source and four identical M1 copies, strengthen `RequirementDeliveryModelM1Tests`, rerun the M1 command set, update M1 evidence, and request independent Code Review R2.
Follow-up: independent Code Review R2 over the corrected M1 implementation.
Validation target: RTD-AC4, RTD-T03, RTD-T04, CMD-001, CMD-002, CMD-003, and CMD-007.
Validation evidence: `python scripts/test-skill-validator.py -k RequirementDeliveryModelM1Tests` failed on both missing mapping directions before the correction and passes 3/3 afterward; the full skill validator passes 364 tests, all four authoring skills validate, the temporary build check passes, the prose audit reports 0 errors and 0 warnings, and canonical-to-four-copy byte comparison passes.
