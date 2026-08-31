# Design Review R1: Retire the Standalone Test-Spec Stage

Review ID: design-review-r1
Stage: design-review
Round: r1
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-verification-ownership`
Reviewed artifact: design package `architecture`, `spec`, `adr-verification-ownership`
Review date: 2026-08-31
Package kind: design
Package members: architecture=docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md, spec=specs/retire-standalone-test-spec-stage.md, adr-verification-ownership=docs/adr/ADR-20260831-verification-ownership-without-test-spec-stage.md
Upstream review ID: proposal-review-r3
Status: changes-requested
Material findings: RTS-DR1
Correction targets: architecture, adr-verification-ownership
Recording status: recorded

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: architecture=`docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md`, spec=`specs/retire-standalone-test-spec-stage.md`, adr-verification-ownership=`docs/adr/ADR-20260831-verification-ownership-without-test-spec-stage.md`
- Upstream review ID: proposal-review-r3
- Review ID and round: design-review-r1, r1
- Material findings: RTS-DR1
- Correction targets: architecture and adr-verification-ownership, both owned by architecture
- Recording status: recorded
- Settlement status: withheld pending exact-package CLI settlement of the changes-requested outcome
- Open blockers: RTS-DR1
- Immediate next stage: architecture authoring owner through Workflow correction routing
- Claim limitations: this outcome grants no Design package authority and does not authorize planning, implementation, verification, branch, PR, release, or deployment readiness

### Finding RTS-DR1

Finding ID: RTS-DR1
Severity: major
Location: `docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md` Runtime View and Compatibility crosscutting concept; `docs/adr/ADR-20260831-verification-ownership-without-test-spec-stage.md` Decision
Evidence: RTS-R20 through RTS-R23 require tooling to distinguish newly governed active state, prior-contract in-flight state, accepted historical state, removed active values, and wholly unknown values. The architecture and ADR say the change's “registered lifecycle contract” selects prior behavior, but every current governed change uses the same `lifecycle_contract: stage-owned-change-local-v1`; neither artifact selects a durable contract-version field, a frozen grandfathered inventory, or another unambiguous repository-contained discriminator. Created dates, artifact presence, and current stage are unsafe inferences because they are mutable or overlap. Delivery planning therefore cannot implement or prove the required compatibility behavior without making a new architecture decision.
Required outcome: Define one durable, repository-contained, fail-closed discriminator for prior-contract changes versus newly governed post-activation changes, including how new-change creation records it, how existing eligible changes are identified at activation, how readers classify completed historical records, how explicit migration changes the discriminator, and how unknown or contradictory discriminator state blocks without rewriting history.
Safe resolution path: The architecture owner should revise the ADR decision and architecture runtime, state, compatibility, deployment, and rollback boundaries with one exact mechanism; register both revised artifacts through the lifecycle CLI; record an accepted resolution with validation evidence; return the correction to Design Review; and request a fresh review of the complete changed package.
needs-decision rationale: none
Finding scope: cross-artifact
Affected artifact IDs: architecture, adr-verification-ownership
Owning stages: architecture

## Design coherence

The package otherwise preserves the accepted ownership direction. Specification owns observable SR behavior, architecture owns realization, plan owns engineering-led allocation plus milestone and change-level verification, Delivery Review jointly judges sequence and proof adequacy, and implementation and Verify retain their downstream roles. No replacement test-spec artifact, one-test-per-SR hierarchy, or test-driven milestone rule is introduced.

The specification's formal boundary model classifies all eight dimensions exactly once, defines each boundary once, selects material composed hazards, and keeps example behavior requirement-owned. The architecture addresses canonical skill sources, progressive disclosure, lifecycle and package enforcement, supported adapter projection, coherent activation and rollback, historical readability, and fail-closed validation. The ADR is applicable and included.

RTS-DR1 prevents approval because compatibility and migration are central accepted constraints and the missing discriminator changes lifecycle schema, activation, migration, and rollback design rather than merely delivery sequencing.

## Proposal preservation

The package retains the proposal's goals, scope, governing principle, trade-offs, predecessor dependency, and vision alignment. The required correction narrows an unresolved compatibility mechanism already demanded by the proposal; it does not broaden product scope.

## Independence statement

This review did not edit the proposal, architecture, specification, ADR, authoring evidence, or workflow routing state. The finding is recorded for the architecture owner.
