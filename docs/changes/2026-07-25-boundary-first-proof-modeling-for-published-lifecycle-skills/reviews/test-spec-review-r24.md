# Boundary-First Proof Modeling Test-Spec Review R24

Review ID: test-spec-review-r24

Stage: test-spec-review

Round: 24

Reviewer: Codex test-spec-review skill

Target: specs/rigorloop-workflow.test.md

Reviewed artifact: focused publisher-recovery proof-map amendment at
`0e145316`

Status: changes-requested

Review status: changes-requested

Material findings: BFP-TSR24-1

Recording status: recorded

Review date: 2026-07-27

Context separation mechanism: tracked-artifact and governing-contract reset

Reviewed commit: `0e145316`

Reviewed test-spec identity:
`sha256:ab2300eed696c6f283a7b04a324dc95bb162953e18cbed1b6d7915e048af8ae0`

Immediate next stage: test-spec revision

Implementation handoff: not-allowed

## Result

The eight direct property obligations correctly expose the properties omitted
by the implementation, including exact publisher identity, lease durability,
root binding, global discovery, closed publication states, uninterrupted
publisher authority, receipt equality, and manual recovery.

One execution-order contradiction remains in T51, so implementation handoff is
not yet safe.

## Finding

### BFP-TSR24-1 - T51 steps begin working-run mutation before the lease

Finding ID: BFP-TSR24-1

Severity: blocker

Auto-fix class: declared-safe

Location: `specs/rigorloop-workflow.test.md`, T51 Steps

Evidence:

- `T51-LEASE-BEFORE-STAGE` requires the valid fsynced publisher lease and
  deterministic working root before the first lifecycle invocation.
- T51's expected result now begins with exclusive lease creation and
  durability.
- T51's executable Steps still begin with “Build and fsync the working run,”
  leaving the old unleased ordering available to implementers.

Required outcome:

Make the executable steps begin with lock acquisition, global discovery,
fresh publisher/run identity allocation, exact lease creation/fsync, and
deterministic working-root creation/fsync. Instrument the first lifecycle
invocation and require those durable prerequisites to exist before it.

Safe resolution:

This is a direct projection of approved R28y and requires no product,
architecture, or owner decision. Correct only T51 ordering and current input
identity text, then rerun test-spec review.

## Other dimensions

All other review dimensions pass. The property rows are closed, each requires
separately named executable proof, negative mutation obligations are explicit,
the crash and recovery states remain exhaustive, T51 is owned by M2, and the
named validation commands remain current.

## Handoff

Revise T51's executable order and rerun test-spec review. M2 implementation
remains blocked.
