# Boundary-First Proof Modeling Architecture Review R28

Review ID: architecture-review-r28

Stage: architecture-review

Round: 28

Reviewer: Codex architecture-review skill

Review surface: canonical-architecture-update

Target: docs/architecture/system/architecture.md

Reviewed artifact: correction-authority and scenario-expectation architecture candidate at 4573e506

Status: changes-requested

Review status: changes-requested

Material findings: BFP-AR28-1

Recording status: recorded

Review date: 2026-07-27

Context separation mechanism: tracked-artifact and governing-contract reset

Reviewed commit: `4573e506b778e20c6ce5ee1cf4fd1a3d3fcc63c5`

Reviewed architecture identity:
`sha256:775788f53bfb0a9f772b4837d0906bad3f2ffcf9f005ef619773de7c0749553f`

Required canonical updates: make the scenario request the only child-readable
scenario value and retain `expected_branch` and `corrected_role` exclusively
in the parent comparison boundary.

Required ADR updates: none

Open blockers: BFP-AR28-1

Next stage: architecture revision

## Result

The correction-authority, durable stop, discard-only recovery, unchanged-input
rejection, and post-observation comparison directions are sound. One material
boundary contradiction prevents approval.

## Material findings

### BFP-AR28-1 - Scenario expectations remain ambiguously child-readable

Finding ID: BFP-AR28-1

Finding: The workspace assembler still describes the complete authoritative
scenario input as child-readable even though the approved spec and new quality
scenario require comparison expectations to remain parent-only.

Location: `docs/architecture/system/architecture.md`, Building Block View,
`Isolated workspace assembler`; `Scenario expectation non-influence`

Severity: material

Evidence: The assembler responsibility says it copies “the authoritative
scenario input into a fresh child-readable workspace.” The approved R57
contract says the harness derives events and observed results before reading
`expected_branch` or `corrected_role`, and changing either value may affect
only the final expectation comparison. The architecture's own quality scenario
says the child receives only the request. These statements allow two
incompatible implementations.

Required outcome: Define one unambiguous data boundary in which the parent
parses and retains the complete scenario record, passes only the non-empty
`request` value into child lifecycle invocations, and exposes neither
expectation field, its path, nor its bytes to the child workspace or request.

Safe resolution path: Revise the assembler responsibility, Runtime View, and
component relationship labels to distinguish the parent-owned scenario record
from the request-only child projection. Require the post-trace evaluator to
read expectations only after observed branch and corrected role are derived.
No new ADR or component is required.

## Review dimensions

| Dimension | Verdict |
| --- | --- |
| Spec alignment | block |
| Package shape | pass |
| Boundary clarity | concern |
| Data ownership | block |
| Interface safety | concern |
| Runtime and failure handling | pass |
| Deployment and execution boundaries | pass |
| Security/privacy | pass |
| Quality and operations | pass |
| Testing feasibility | pass after correction |
| Complexity discipline | pass |
| ADR quality | pass |
| Plan readiness | block |

## Handoff

Revise only the scenario data boundary and rerun architecture review. Planning,
test-spec revision, and implementation remain blocked until the canonical
package has one consistent request-only child projection.
