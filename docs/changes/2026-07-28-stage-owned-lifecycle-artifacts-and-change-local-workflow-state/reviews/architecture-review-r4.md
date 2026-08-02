# Architecture Review R4

Review ID: architecture-review-r4
Stage: architecture-review
Round: 4
Reviewer: independent Codex architecture-review peer
Target: docs/architecture/system/architecture.md and diagram package
Reviewed artifact: docs/architecture/system/architecture.md
Status: changes-requested
Review date: 2026-08-02
Recording status: recorded
Material findings: AR4-001, AR4-002
Immediate next stage: architecture revision
Automatic downstream handoff: none

## R3 reconciliation

- `AR3-001`: resolved through approved architecture-method spec and test-spec
  amendments, templates, and skill guidance.
- `AR3-003`: resolved by distinguishing owner-family initial loading from
  downstream expansion loading.
- Minor schema label: resolved in the container diagram.
- `AR3-002`: partially resolved; active ADR and direct supersession wording is
  corrected, but contradictory pending-state summaries remain.

## Material findings

### AR4-001 - Historical automation ADRs still appear to await supersession

Finding ID: AR4-001
Severity: material
Location: docs/architecture/system/architecture.md Architecture Decisions summaries
Evidence: The package says the stage-owned ADR is active and supersedes ADR-20260721 while four predecessor summaries still say proposed for supersession.
Required outcome: Consistently classify former profile and consolidation ADRs as superseded historical decisions while naming retained constraints accurately.
Safe resolution path: Replace only the four stale summaries; preserve ADR bodies as append-only history.

### AR4-002 - CLI white-box view still specifies schema-v2 writes

Finding ID: AR4-002
Severity: material
Location: docs/architecture/system/architecture.md CLI Building Block View and historical schema summaries
Evidence: The serializer responsibility says it writes schema-v2 generated adapter entries, while the current contract and other canonical sections require schema-v3 writes and schema-v1/v2 compatibility reads.
Required outcome: State schema-v3 current writes and schema-v1/v2 compatibility reads or migrations unambiguously.
Safe resolution path: Correct the serializer responsibility and clarify historical schema-v2 goal/scenario wording without changing ADRs.

## Recommendation

Changes requested. Apply the two bounded current-state corrections and request
architecture-review R5. All other review dimensions pass.
