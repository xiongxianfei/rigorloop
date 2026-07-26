# Boundary-First Proof Modeling Spec Review R35

Review ID: spec-review-r35
Stage: spec-review
Round: 35
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R34 resolution candidate at 6a9be4d9
Reviewed artifact: `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R35-1, BFP-SR-R35-2, BFP-SR-R35-3
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:523f767e5f3bf311a734228ada28bafc858f08aec4d5ea4cd82dba515d23b68a`

Reviewed test-spec identity: `sha256:2a13e5f1e863eddda3da80091a55f779c04bf279a8e3cb72383c4281c28589ef`

Reviewed plan identity: `sha256:0ca274bb41a4fc588547ef1b47dcf4ae00c46d1b9d749bc005882c931fa2acfb`

## Findings

### BFP-SR-R35-1 - Conditional policy failure is absent from preflight results

Finding ID: BFP-SR-R35-1
Severity: blocking
Location: R28y preflight diagnostic table and T49
Evidence: Unsafe schema-valid remote-control values emit
`protocol-conditional-policy-violation`, while the exhaustive preflight
diagnostic table omits that value and rejects unknown diagnostic IDs.
Required outcome: Make conditional-policy failure a deterministic in-turn
preflight result without retaining raw environment values.
Safe resolution: Add the diagnostic with phase `in-turn` to the closed table
and prove all four boolean combinations.

### BFP-SR-R35-2 - Runtime checkpoints lack deterministic phase mapping

Finding ID: BFP-SR-R35-2
Severity: major
Location: R28y preflight phase table and runtime-identity evidence
Evidence: Eight checkpoints are closed, but the preflight table permits three
phases using only the phrase “matching the checkpoint.”
Required outcome: Bind every checkpoint to exactly one preflight phase and
reject missing, duplicate, unknown, or cross-phase combinations.
Safe resolution: Add an exhaustive checkpoint-to-phase table and direct
contrast proof.

### BFP-SR-R35-3 - Transport policy is omitted from complete manifest selection

Finding ID: BFP-SR-R35-3
Severity: blocking
Location: R28y operation registry, canonical validation, and T48
Evidence: The behavior manifest declares a normative transport policy, but its
complete current input selector and validation algorithm omit the policy.
Required outcome: Include the exact policy in generation and semantic
validation, recompute its identity, and prove manifest-closure contrast cases.
Safe resolution: Add the transport policy to the operation selector,
validation algorithm, and T48 exact manifest fixture.

## Review dimensions

| Dimension | Result |
| --- | --- |
| Proposal and goal alignment | pass |
| Scope and ownership | pass |
| Normative language | concern |
| Closed-vocabulary completeness | block |
| Internal consistency | block |
| Testability and proof mapping | block |
| Recovery and concurrency | pass |
| Security and privacy | pass |
| Compatibility | pass |
| Observability and diagnostics | concern |
| Architecture readiness | not ready |

## Review result

The spec remains blocked until R35-1 through R35-3 are resolved and
independently rereviewed. R34-2 is resolved; R34-1, R34-3, and R34-4 require
the focused consistency corrections above.
