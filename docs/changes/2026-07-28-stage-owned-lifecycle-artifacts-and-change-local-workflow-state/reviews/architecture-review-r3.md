# Architecture Review R3

Review ID: architecture-review-r3
Stage: architecture-review
Round: 3
Reviewer: independent Codex architecture-review peer
Target: docs/architecture/system/architecture.md and progressive-guidance architecture package
Reviewed artifact: docs/architecture/system/architecture.md
Status: changes-requested
Review date: 2026-08-02
Recording status: recorded
Material findings: AR3-001; AR3-002; AR3-003
Immediate next stage: spec and architecture revision
Automatic downstream handoff: none

## Result

- Review surface: canonical-architecture-update and ADR
- Review status: changes-requested
- Material findings: AR3-001; AR3-002; AR3-003
- Recording status: recorded
- Open blockers: AR3-001; AR3-002; AR3-003
- Plan readiness: not ready

## Material findings

### AR3-001 - Architecture lifecycle metadata contracts conflict

Finding ID: AR3-001
Severity: material
Location: specs/architecture-package-method.md R8; specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md SLA-R002 and SLA-R014; docs/architecture/system/architecture.md owner pointer
Evidence: Architecture method R8 requires lifecycle status metadata in architecture.md, while the active stage-owned contract makes change.yaml the sole mutable lifecycle owner and prohibits mutable status in governed artifacts. The current architecture correctly contains only a stable owner pointer, but the two authoritative specifications remain contradictory.
Required outcome: Define the architecture pointer as stable metadata and the owning change.yaml entry as the only mutable lifecycle state.
Safe resolution path: Amend R8 and its matching test coverage or reciprocal notice under spec ownership; do not restore mutable status to architecture.md.

### AR3-002 - Active ADR decisions are described as pending

Finding ID: AR3-002
Severity: material
Location: docs/architecture/system/architecture.md Architecture Decisions and Readiness summaries
Evidence: The canonical architecture describes the stage-owned ADR as proposed and its effects as occurring on acceptance, while the exact owner record marks the ADR active with approved review and active settlement.
Required outcome: Describe the ADR as active and the prior authority as already superseded or retained where applicable.
Safe resolution path: Update the current Architecture Decisions and Readiness summaries while preserving the accepted ADR's append-only historical wording.

### AR3-003 - Component diagram misstates compact-core loading

Finding ID: AR3-003
Severity: material
Location: docs/architecture/system/diagrams/component-boundary-guidance.mmd
Evidence: The diagram says every governed skill loads the compact core on expansion. PBS-R014/PBS-R017 and the architecture runtime flow require owner families to load compact plus their family resource initially, while downstream stages load compact only when expansion is needed.
Required outcome: Distinguish packaging from runtime loading and show owner-family initial loading versus downstream expansion loading.
Safe resolution path: Split or relabel the relationship while retaining the feature and proof resource arrows.

## Minor correction

The container diagram's schema-v2 label is stale. Schema v3 is the current
write format; schema v2 is legacy compatibility input.

## Clean evidence

C4 context/container coverage, focused component views, arc42 section order,
runtime/deployment/crosscutting treatment, security boundaries, rollback
semantics, progressive ADR alignment, and the single-owner repair are otherwise
sufficient.

## Recommendation

Changes requested. Resolve `AR3-001` under spec ownership and `AR3-002` plus
`AR3-003` under architecture ownership, apply the minor label correction, and
request architecture-review R4.

