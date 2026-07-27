# Boundary-First Proof Modeling Plan Review R16

Review ID: plan-review-r16
Stage: plan-review
Round: 16
Reviewer: Codex plan-review skill with context-separated independent reviewer
Target: docs/plans/2026-07-25-boundary-first-proof-modeling.md
Reviewed artifact: capability-projected M2 execution plan at 385f5026
Status: changes-requested
Review status: changes-requested
Material findings: BFP-PL16-1, BFP-PL16-2
Immediate next stage: plan revision
Plan readiness: not-ready
Recording status: recorded
Review date: 2026-07-27
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed commit: `385f50260ca59e863f01a111f4c5d75e1015ecb6`

Reviewed plan identity:
`sha256:2a96824b96d7f7203cbe252786abfcad9f88641027aa4ba8e65495fc3625d855`

## Result

Changes requested. The plan correctly replaces version-only trust with an
exact-runtime capability projection, common production-dispatch conformance,
capability-specific proof branches, and v3 evidence. Two sequencing and
recovery gaps remain before the test specification can safely operationalize
the plan.

## Review invocation manifest

| Field | Value |
| --- | --- |
| Review target | `docs/plans/2026-07-25-boundary-first-proof-modeling.md` |
| Candidate commit | `385f50260ca59e863f01a111f4c5d75e1015ecb6` |
| Governing spec | `specs/rigorloop-workflow.md` R28-R28z, approved by R48 |
| Governing spec identity | `sha256:c34ce7291f7a2df9deec56e8d364514f05905136656dcec00af4787435353eff` |
| Architecture | `docs/architecture/system/architecture.md`, approved by R22 |
| Architecture identity | `sha256:ed5a12592117adc3a8c2ddfea77e41c1e819086467dd9b5928ab7e7e5ed25042` |
| Capability-projection ADR | `ADR-20260727-capability-projected-file-change-control`, accepted |
| ADR identity | `sha256:b9d75ea29d528ef0e1f835ab796d6aa6936d362520ce1a424f5f0bb1112568ef` |
| Open implementation findings | `BFP-CR-M2-1`, `BFP-CR-M2-7`, `BFP-CR-M2-8` |
| Matching test specs | Present but stale; they predate R48/R22 |
| Review mode | Independent workflow-managed plan review |
| Context separation | Separate agent; reviewed tracked artifacts without editing |

## Findings

### BFP-PL16-1 — Handler conformance is not explicitly validated before capability branching

Finding ID: BFP-PL16-1
Severity: major
Location: M2 tests and implementation steps

Evidence: The plan runs the complete conformance policy before selecting a
capability branch, but defers pure-model validation of the result until before
v3 attestation assembly. That ordering permits live-probe or non-exposure work
to begin before conformance schema, identity, ordering, completeness, and
aggregate outcome have passed the R22 validation boundary.

Required outcome: In preflight and generation, install the production
dispatcher, execute the complete conformance policy, validate the policy and
result through `boundary_proof_model`, and stop with bounded failure evidence
on any invalid result before either capability branch can execute.

Safe resolution: Move pure-model conformance validation immediately after the
runner and add invocation-counter tests proving missing, failed, malformed,
stale, reordered, or identity-inconsistent results execute neither branch,
canary, governed lifecycle turn, nor successful attestation.

### BFP-PL16-2 — M2 rollback does not restore a coherent authority and evidence state

Finding ID: BFP-PL16-2
Severity: major
Location: M2 publication, migration, and rollback/recovery

Evidence: M2 changes the fixed current manifest, v3 preflight evidence, model,
harness, fixtures, template, five skill packages, immutable runs, current
pointer, and publication transaction state. The rollback names only the skill
packages and pointer. It can therefore leave a current evidence record bound
to code or package identities that no longer exist.

Required outcome: Define a phase-aware rollback that leaves exactly one
coherent current authority state and no unresolved publication transaction.

Safe resolution: Acquire the publisher lock; reconcile or fail closed on any
prepared receipt; restore or remove the current pointer from a previously
validated state; restore the exact registered opaque-v1 manifest bytes or
leave no current manifest; revert the model, harness, fixtures, template, and
five skill packages as one compatibility unit; retain v3 immutable runs only
as non-current history; and revalidate history, publication state, skill
parity, and absence of dangling v3 authority.

## Review dimensions

| Dimension | Result |
| --- | --- |
| Self-contained context | pass |
| Source alignment | concern |
| Milestone size | pass |
| Sequencing | block |
| Scope discipline | pass |
| Validation quality | concern |
| TDD readiness | concern |
| Risk coverage | concern |
| Architecture alignment | block |
| Operational readiness | block |
| Plan maintainability | pass |

## Readiness

The active test specifications correctly remain stale downstream inputs. Revise
the plan first, then rerun plan review. After approval, revise both test specs
to the R48/R22 v3 contract and independently review them before M2
implementation resumes.
