# Review Resolution: Refocus Workflow into the Route Skill

## Summary

Closeout status: closed

Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3
Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m1-r3`
- Findings resolved: 5
- Unresolved findings: 0
- Current result: M1 Code Review R3 found the complete corrected workflow-context slice clean with no remaining material findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| RFR-M1-CR1 | accepted | resolved | Formal review locations now preserve their four distinct stage owners. |
| RFR-M1-CR2 | accepted | resolved | Variable projections are capped and unsafe lifecycle values are not disclosed. |
| RFR-M1-CR3 | accepted | resolved | Exact reads are isolated and TG-05 failure, retry, interruption, and freshness proof is complete. |
| RFR-M1-CR4 | accepted | resolved | Human output exposes candidate count, truncation, and exact-selection guidance. |
| RFR-M1-CR5 | accepted | resolved | Unexpected read and interrupted public invocation tests prove non-mutation directly. |

## Finding Details

### proposal-review-r1

No material findings.

### code-review-m1-r1

#### RFR-M1-CR1

Finding ID: RFR-M1-CR1
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Replace the generic code-review-owned review location with a closed representation that preserves each formal review owner's authority and exposes deterministic review outputs.
Rationale: Location resolution is structural and cannot transfer proposal-review, design-review, or delivery-review evidence ownership to code-review.
Required outcome: Every formal-review location is represented without ownership collapse and has direct correct-owner and wrong-owner proof.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: RT-R4, RT-R8, BND-AUTH-001, TG-02, TG-03.
Validation evidence: Code Review M1 R2 inspected `47a87bb8..a8ec338c`; all four configured review-record kinds have their exact review-stage owner and wrong-owner overrides fail directly in the 174-test plan-selected suite.

#### RFR-M1-CR2

Finding ID: RFR-M1-CR2
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Add deterministic collection, identifier, and encoded-output bounds and fail-safe redaction or rejection for invalid lifecycle values.
Rationale: Allowlisting some automation scalars does not bound candidate, milestone, package, receipt, or human output and does not protect raw lifecycle fields.
Required outcome: Large or malformed projections remain bounded, actionable, structural-only, and free of private absolute values.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: RT-R7, RT-R8, RT-R35, RT-R36, BND-INPUT-001, BND-ENV-001, TG-01, TG-02, TG-04.
Validation evidence: Code Review M1 R3 inspected the complete correction through `063bd6e5`; capped project/change projections, invalid-stage redaction, human truncation disclosure, and the complete planned test set passed.

#### RFR-M1-CR3

Finding ID: RFR-M1-CR3
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Add a normalized filesystem-failure boundary, restore requested-change read isolation, and directly prove all TG-05 outcomes over the complete relevant tree.
Rationale: A generic process error and a one-file byte snapshot do not satisfy the approved recovery, retry, non-mutation, or freshness contract.
Required outcome: Success, failure, ambiguity, retry, interruption, and post-mutation stale identity produce bounded deterministic results without changing governed or configuration files.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: RT-R12, RT-R34, RT-R38, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001, INT-005, TG-05.
Validation evidence: Code Review M1 R3 confirmed exact-read isolation, full governed/config snapshots, identical retry, stale-after-mutation identity, deterministic `RL_CONTEXT_READ_FAILED`, and interrupted public-process non-mutation proof.

### code-review-m1-r2

#### RFR-M1-CR4

Finding ID: RFR-M1-CR4
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Render existing candidate count and truncation facts in human output with an exact-selection instruction.
Rationale: Bounded output is actionable only when a human can see that entries were omitted and how to proceed.
Required outcome: Public human output reports total candidates, truncation, and exact `--change` selection when the project list is capped.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R3.
Validation target: RT-R35, RT-R36, TG-04.
Validation evidence: Code Review M1 R3 confirmed public human output reports `Candidate count: 41` and `showing 32; use --change <id>` for a capped project result.

#### RFR-M1-CR5

Finding ID: RFR-M1-CR5
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Add a narrow deterministic read-fault seam and public interruption proof using the existing complete-tree snapshot.
Rationale: Ordinary configuration rejection does not execute the unexpected-read boundary or prove interruption behavior.
Required outcome: Direct unexpected-read and interrupted-invocation tests return or terminate safely and leave all governed/config bytes unchanged.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R3.
Validation target: RT-R38, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001, TG-05.
Validation evidence: Code Review M1 R3 confirmed the direct read-fault result contains `RL_CONTEXT_READ_FAILED` without private details and the FIFO-blocked public process terminates without changing governed state or its input.

### code-review-m1-r3

No material findings.
