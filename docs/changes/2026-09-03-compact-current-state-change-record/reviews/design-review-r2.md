# Design Review R2: Compact Current-State Change Record

Review ID: design-review-r2
Stage: design-review
Round: r2
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Reviewed artifact: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Review date: 2026-09-04
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-compact-current-state-change-record.md, spec=specs/compact-current-state-change-record.md, adr-compact-current-state-transaction=docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Upstream review ID: proposal-review-r1
Status: changes-requested
Material findings: CCSR-DR2
Correction targets: spec
Recording status: recorded

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: architecture=`docs/architecture/2026-09-03-compact-current-state-change-record.md`, spec=`specs/compact-current-state-change-record.md`, adr-compact-current-state-transaction=`docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Upstream review ID: proposal-review-r1
- Review ID and round: design-review-r2, r2
- Material findings: CCSR-DR2
- Correction targets: spec, owned by spec
- Recording status: recorded
- Settlement status: withheld pending exact-package CLI settlement of the changes-requested outcome
- Open blockers: CCSR-DR2
- Immediate next stage: specification authoring owner through Workflow correction routing
- Claim limitations: this outcome grants no Design package authority and does not authorize planning, implementation, verification, branch, pull-request, release, or deployment readiness

### Finding CCSR-DR2

Finding ID: CCSR-DR2
Severity: major
Location: `specs/compact-current-state-change-record.md:126-134,174-189`
Evidence: SR-37 through SR-45 add schema identities, serialization restrictions, recovery phases, size limits, and a durability boundary, but the Compact schema tables define only top-level field names and prose summaries for most nested entries. They do not fix collection representation, scalar types, nullability, cardinality, exact nested field names, or absence encoding for core structures such as `artifacts`, `reviews`, `active_work`, findings, subjects, dependencies, blockers, expected files, and recovery affected-file rows. The lifecycle-revision rule likewise does not define the canonical manifest's exact key and row shape or how the parsed `lifecycle_revision` scalar is reserialized before coordinator hashing. Consequently two independent implementations can satisfy the prose while emitting incompatible records or different lifecycle revisions, contradicting AC-11 and leaving observable interoperability choices to Delivery.
Required outcome: Define complete v1 structural schemas for every authoritative surface, operation/result envelope, and recovery record, including container types, required and optional nested fields, scalar types, null and absence rules, cardinalities, exact closed vocabularies or one exact versioned vocabulary reference, and cross-reference shapes. Define the exact canonical lifecycle-revision manifest object and coordinator normalization so independently implemented readers and writers produce identical identities.
Safe resolution path: The specification owner should revise only `specs/compact-current-state-change-record.md`, replace the summary-only schema table with exact field and nested-entry definitions or normative embedded schemas, correct the example-ownership range to SR-01 through SR-45, validate the complete boundary record, register the exact revision, record an accepted resolution with evidence, return the correction to Design Review, and request a fresh review of the unchanged architecture and ADR with the corrected specification.
needs-decision rationale: none
Finding scope: artifact-local
Affected artifact IDs: spec
Owning stages: spec

## Prior finding reconciliation

CCSR-DR1 is substantively improved: the corrected specification now fixes the schema identities, safe serialization family, transaction root, permissions, limits, recovery phases, and post-sync success boundary. CCSR-DR2 narrows the remaining issue to the structural detail still required for independent implementations to agree; it does not reopen the already-satisfied durability and non-reliance parts of CCSR-DR1.

## Design coherence

The architecture, ADR, and behavioral requirements otherwise remain coherent. They preserve the accepted compact working set, promotion-before-replacement, explicit evidence dependencies, current-state-only projections, pure evaluator boundary, recoverable multi-file persistence, independent review, historical read-only compatibility, and no reliance on Git, pull-request history, network services, or local logs. All eight boundary dimensions are classified, and the selected interactions cover the material concurrency, recovery, authority, stale-evidence, and compatibility hazards.

## Independence statement

This review did not edit the proposal, architecture, specification, ADR, authoring evidence, or workflow routing state. CCSR-DR2 is recorded for the specification owner.
