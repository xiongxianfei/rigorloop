# Design Review R1: Compact Current-State Change Record

Review ID: design-review-r1
Stage: design-review
Round: r1
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Reviewed artifact: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Review date: 2026-09-03
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-compact-current-state-change-record.md, spec=specs/compact-current-state-change-record.md, adr-compact-current-state-transaction=docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Upstream review ID: proposal-review-r1
Status: changes-requested
Material findings: CCSR-DR1
Correction targets: spec
Recording status: recorded

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: architecture=`docs/architecture/2026-09-03-compact-current-state-change-record.md`, spec=`specs/compact-current-state-change-record.md`, adr-compact-current-state-transaction=`docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Upstream review ID: proposal-review-r1
- Review ID and round: design-review-r1, r1
- Material findings: CCSR-DR1
- Correction targets: spec, owned by spec
- Recording status: recorded
- Settlement status: withheld pending exact-package CLI settlement of the changes-requested outcome
- Open blockers: CCSR-DR1
- Immediate next stage: specification authoring owner through Workflow correction routing
- Claim limitations: this outcome grants no Design package authority and does not authorize planning, implementation, verification, branch, pull-request, release, or deployment readiness

### Finding CCSR-DR1

Finding ID: CCSR-DR1
Severity: major
Location: `docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md:45,83`; `specs/compact-current-state-change-record.md:71-76,83-98,107-110,315`
Evidence: The ADR explicitly assigns exact compact schemas, recovery file names and bundle encoding, size limits, and fsync policy to Specification. The specification identifies semantic fields and high-level durability outcomes, but its Open Questions section defers all exact serialization details to planning and implementation. It does not establish a machine-parseable serialization contract for stable Markdown review and material-decision records, the exact lifecycle revision coverage encoding, recovery and lock locations and containment, the recovery bundle state machine and format, concrete bounded-size behavior, or the durability point at which success may be reported. Those choices affect interoperability, crash outcomes, security, and whether non-loss can be validated; they are not implementation-neutral details. Delivery would otherwise have to invent observable Design behavior.
Required outcome: Define a versioned, machine-parseable schema contract for each compact surface and transient semantic request/result envelope, plus the externally observable transaction durability and recovery contract. The specification must fix required top-level structure and closed vocabularies, canonical identity and lifecycle-revision calculation inputs, lock and recovery storage boundary, recovery states and decisions, bounded input and recovery limits or a normative configuration rule, and the durability point for reporting success. It may leave byte-level parser/library choices and internal module layout to Delivery.
Safe resolution path: The specification owner should revise only `specs/compact-current-state-change-record.md`, add stable requirements and boundary coverage for the missing contracts, register the exact revision through the lifecycle CLI, record an accepted resolution with validation evidence, return the correction to Design Review, and request a fresh review of the complete changed package.
needs-decision rationale: none
Finding scope: artifact-local
Affected artifact IDs: spec
Owning stages: spec

## Design coherence

The accepted direction is otherwise preserved. The package makes current authoritative state self-sufficient without Git, pull-request history, hosted services, or local logs; keeps semantic authority with stage owners; limits the public CLI to projection, semantic mutation, and recovery capabilities; and uses one pure evaluator with one recoverable persistence path. Stable reviews, promotion-before-replacement, explicit evidence dependencies, final Verify binding, historical read-only compatibility, and coherent activation agree across the proposal, architecture, ADR, and specification.

The formal boundary model structurally passes and classifies all eight dimensions. Its selected interactions cover concurrent finding loss, stale evidence and Verify state, CLI bypass, recovery-path safety, and mixed-version rollout. CCSR-DR1 remains material because exact parse and durability boundaries determine whether those specified outcomes are implementable and directly provable.

## Proposal preservation

The package retains the proposal's compact current-state direction, five applicable surfaces, independent review, current evidence, prospective activation, and explicit non-reliance on Git, pull requests, networks, or local logs. The required correction resolves a Design responsibility already reserved by the proposal and ADR; it does not broaden the approved product scope.

## Independence statement

This review did not edit the proposal, architecture, specification, ADR, authoring evidence, or workflow routing state. CCSR-DR1 is recorded for the specification owner.
