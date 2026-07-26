# Boundary-First Proof Modeling Spec Review R31

Review ID: spec-review-r31
Stage: spec-review
Round: 31
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R30 resolution candidate at 85dae0c5
Reviewed artifact: `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R31-1, BFP-SR-R31-2
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:af709050d9feab71e625c14b1284542fa62a0beac3b8f51a8b981c3d3e8aec2e`

Reviewed test-spec identity: `sha256:2aa7086293674cc986262492138919cc701750c91f1017d0a22eadc68798cf9d`

Reviewed plan identity: `sha256:1cb08b16c39f7a2e18fc221bf4534f5e1a20a5a99243252fc92c392c3ebbe2f7`

## Findings

### BFP-SR-R31-1 - Diagnostic evidence lacks semantic validity predicates

Finding ID: BFP-SR-R31-1
Severity: major
Location: `specs/rigorloop-workflow.md` R28y diagnostic evidence and `specs/rigorloop-workflow.test.md` T52
Evidence: Inline role records constrain field shape but do not close timeout
threshold, unequal runtime identities, schema failure, prohibited-event
membership, or disjoint output-state classification.
Required outcome: Define exact per-role semantic predicates and add equality,
wrong-role, and overlapping-output contrasts.
Safe resolution: Bind every diagnostic record to a closed evaluator and define
output state as a disjoint precedence over required and observed role/path
descriptors.

### BFP-SR-R31-2 - Orphan deletion is not interruption-safe

Finding ID: BFP-SR-R31-2
Severity: blocking
Location: `specs/rigorloop-workflow.md` R28y recovery table and `specs/rigorloop-workflow.test.md` T51
Evidence: Recursive deletion can stop with an authorized, present, partially
deleted orphan that no recovery row accepts. Initial basis write can also leave
a malformed canonical file before fsync.
Required outcome: Atomically install the recovery basis, detach the orphan by
atomic rename, fsync the namespace, record the detached state, and either
preserve quarantine or define subset-safe cleanup. Test basis-temp and
quarantine crash states.
Safe resolution: Use atomic no-clobber basis installation and preserve a
deterministic identity-validated quarantine tree as bounded noncanonical
recovery evidence.

## Prior-finding assessment

| Prior finding | Assessment |
| --- | --- |
| `BFP-SR-R30-1` | Partially resolved; routing passes, exact role validity remains. |
| `BFP-SR-R30-2` | Partially resolved; authority/state split passes, recursive deletion remains. |
| `BFP-SR-R30-3` | Resolved. |

## Review result

The spec remains blocked until R31-1 and R31-2 are resolved and independently
rereviewed.
