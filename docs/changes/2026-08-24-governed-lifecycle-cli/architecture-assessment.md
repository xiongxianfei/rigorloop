# Architecture Assessment: Governed Lifecycle CLI

Stage: architecture-assessment
Assessment receipt ID: architecture-assessment-r1
Assessment mode: workflow-managed
Applicability: required
Route: architecture-required
Action: assessment-only
Assembly: AA0-assessment
Spec: `specs/governed-lifecycle-cli.md`
Spec identity: `sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`
Approving spec review: `spec-review-r2`
Spec review identity: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/spec-review-r2.md`
Assessment date: 2026-08-24

## Rationale

The approved specification introduces a canonical executable interpreter and guarded mutation owner shared by humans, skills, adapters, workflow, and CI. It changes the long-lived boundary among the Node CLI, existing Python validators, stage-authored semantic artifacts, `change.yaml`, transient recovery state, Git, and generated skill packages.

Safe implementation requires architecture to define:

- one reusable lifecycle engine and how existing validators delegate or converge without competing authorities;
- repository discovery, snapshot loading, artifact identity, dependency edges, and lifecycle-revision calculation;
- command/request/result boundaries for human, agent, adapter, and CI callers;
- the same-directory recovery-bundle and durable replacement protocol;
- stale operation, idempotent replay, and process-concurrency handling;
- versioned schema, migration, repair, and enforcement activation seams; and
- how skills remove mechanical lifecycle procedure while retaining semantic guidance and portable behavior.

These decisions affect persistence, compatibility, recovery, packaging, and authority across multiple components. They add no hosted service, external database, autonomous runner, semantic decision owner, or distributed transaction.

## Architecture trigger scan

| Trigger | Result | Evidence |
| --- | --- | --- |
| Cross-component runtime boundary | yes | CLI, Python validation, skills, adapters, workflow, and CI must share one interpretation. |
| New durable identity model | yes | Artifact identities, dependency sets, and lifecycle revision govern freshness and concurrency. |
| New mutation and recovery protocol | yes | Guarded replacement and interrupted transaction reconciliation become product behavior. |
| New compatibility and migration seam | yes | CLI, repository schema, JSON contracts, and packaged skills require coordinated versions. |
| New authority owner | yes | The CLI becomes mandatory for governed lifecycle mutation after activation. |
| New hosted service or database | no | Repository artifacts and Git remain durable truth. |
| New semantic decision owner | no | Skills and humans retain semantic judgment; workflow retains routing. |

## Required architecture surface

Update the canonical system architecture to add the lifecycle CLI/engine data flow and package boundary. Add one ADR for canonical interpretation, guarded single-record mutation, recovery, and phased enforcement. Existing stage-owned lifecycle and validation ADRs remain governing context and must not be rewritten.

## Result

- Targets: canonical architecture and one new ADR
- Architecture artifacts changed: pending architecture authoring
- ADRs changed: pending new governed-lifecycle CLI transaction-boundary ADR
- Recording status: recorded
- Blockers: none
- Claim limitations: this assessment does not approve architecture, plan, test-spec, implementation, verification, branch readiness, or PR readiness
- Next stage: architecture
