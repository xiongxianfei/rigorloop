# Boundary-First Proof Modeling Spec Review R30

Review ID: spec-review-r30
Stage: spec-review
Round: 30
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R29 resolution candidate at c392226b
Reviewed artifact: `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R30-1, BFP-SR-R30-2, BFP-SR-R30-3
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:d700d485d986fa5eb163f03770c3d90ed1b5960a79eb6e6da67109fa18f4694b`

Reviewed test-spec identity: `sha256:f3c2ed44f9ed08e10b70540efddd1bcaa5e2da1db0e6e21a84ec26bc49088c14`

Reviewed plan identity: `sha256:ce11a6c92d407e7092d1c09a7595d0e45240fcf3205be096385cc47b88385426`

## Findings

### BFP-SR-R30-1 - Diagnostic precedence makes retry unreachable

Finding ID: BFP-SR-R30-1
Severity: blocking
Location: `specs/rigorloop-workflow.md` R28y transport diagnostics and `specs/rigorloop-workflow.test.md` T52
Evidence: Absent output precedes timeout and therefore becomes primary, while
the matrix permits retry only when timeout is primary. The contract also
requires current references for negative or inline observations without
defining an evidence artifact that can carry them.
Required outcome: Route using the complete diagnostic set; define exact timeout
plus output combinations; define bounded inline or external evidence roles for
every diagnostic; and test missing, extra, and self-referential evidence.
Safe resolution: Make the ordered diagnostic tuple, not its first member, the
routing key and embed an exact role-keyed diagnostic evidence record in each
transport row.

### BFP-SR-R30-2 - Manual recovery is not total or immutable

Finding ID: BFP-SR-R30-2
Severity: blocking
Location: `specs/rigorloop-workflow.md` R28y publisher and recovery state machines and `specs/rigorloop-workflow.test.md` T51
Evidence: Lease-only recovery has no orphan parent to fsync, recovery
replacement can change non-state authority/basis fields, working-root minimum
validity is undefined, input validation is ambiguous, and the generating route
depends on an unrecorded live-owner fact.
Required outcome: Define the lease-only parent, byte-stable recovery
replacement, lease-bound rather than current-input cleanup validation,
minimum-valid working state, an explicit same-live-publisher observer fact, and
all mutation contrasts.
Safe resolution: Use the simple-change root as the lease-only durability
parent, freeze every non-state recovery field, bind cleanup to the lease and
snapshot, and add a closed live-owner observer boolean.

### BFP-SR-R30-3 - Test-spec lifecycle evidence is stale

Finding ID: BFP-SR-R30-3
Severity: major
Location: `specs/rigorloop-workflow.test.md` input identities and `docs/plans/2026-07-25-boundary-first-proof-modeling.md`
Evidence: The test spec still identifies R28 as latest and leaves the
resolution-needed plan identity pending.
Required outcome: Bind the draft test spec to the latest recorded spec review
and synchronized plan identity, and clarify that the approved baseline remains
normative while focused R28y text is draft.
Safe resolution: Update the review row after R30 recording, stabilize the plan,
then hash and bind that plan without claiming implementation readiness.

## Prior-finding assessment

| Prior finding | Assessment |
| --- | --- |
| `BFP-SR-R29-1` | Partially resolved; compound representation passes, routing and evidence remain. |
| `BFP-SR-R29-2` | Resolved. |
| `BFP-SR-R29-3` | Partially resolved; publisher lock/lease passes, recovery closure remains. |

## Review result

The spec remains blocked until R30-1 through R30-3 are resolved and
independently rereviewed.
