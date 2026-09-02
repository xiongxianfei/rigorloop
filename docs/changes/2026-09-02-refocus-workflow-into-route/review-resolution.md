# Review Resolution: Refocus Workflow into the Route Skill

## Summary

Closeout status: open

Review closeout: code-review-m1-r1
Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`, `code-review-m1-r1`
- Findings resolved: 0
- Unresolved findings: 3
- Current result: M1 Code Review R1 requested bounded corrections before milestone closeout or M2 implementation.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| RFR-M1-CR1 | accepted | open | Preserve distinct formal-review ownership in workflow location configuration and projection. |
| RFR-M1-CR2 | accepted | open | Bound every projected collection and identifier and prevent private absolute-value disclosure. |
| RFR-M1-CR3 | accepted | open | Normalize filesystem failures, restore exact-read isolation, and complete TG-05 direct proof. |

## Finding Details

### proposal-review-r1

No material findings.

### code-review-m1-r1

#### RFR-M1-CR1

Finding ID: RFR-M1-CR1
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Replace the generic code-review-owned review location with a closed representation that preserves each formal review owner's authority and exposes deterministic review outputs.
Rationale: Location resolution is structural and cannot transfer proposal-review, design-review, or delivery-review evidence ownership to code-review.
Required outcome: Every formal-review location is represented without ownership collapse and has direct correct-owner and wrong-owner proof.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: RT-R4, RT-R8, BND-AUTH-001, TG-02, TG-03.
Validation evidence: pending correction and rereview.

#### RFR-M1-CR2

Finding ID: RFR-M1-CR2
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Add deterministic collection, identifier, and encoded-output bounds and fail-safe redaction or rejection for invalid lifecycle values.
Rationale: Allowlisting some automation scalars does not bound candidate, milestone, package, receipt, or human output and does not protect raw lifecycle fields.
Required outcome: Large or malformed projections remain bounded, actionable, structural-only, and free of private absolute values.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: RT-R7, RT-R8, RT-R35, RT-R36, BND-INPUT-001, BND-ENV-001, TG-01, TG-02, TG-04.
Validation evidence: pending correction and rereview.

#### RFR-M1-CR3

Finding ID: RFR-M1-CR3
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Add a normalized filesystem-failure boundary, restore requested-change read isolation, and directly prove all TG-05 outcomes over the complete relevant tree.
Rationale: A generic process error and a one-file byte snapshot do not satisfy the approved recovery, retry, non-mutation, or freshness contract.
Required outcome: Success, failure, ambiguity, retry, interruption, and post-mutation stale identity produce bounded deterministic results without changing governed or configuration files.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: RT-R12, RT-R34, RT-R38, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001, INT-005, TG-05.
Validation evidence: pending correction and rereview.
