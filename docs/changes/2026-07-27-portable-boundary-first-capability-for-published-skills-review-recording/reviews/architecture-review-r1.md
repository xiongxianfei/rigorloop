# Portable Boundary-First Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Reviewer: Independent architecture review
Target: docs/architecture/system/architecture.md
Companion scope: docs/adr/ADR-20260727-portable-boundary-first-reference-projection-and-activation.md
Status: changes-requested
Material findings: PBF-AR1, PBF-AR2
Immediate next stage: review-resolution

## Result

- Review surface: canonical-architecture-update
- Review status: changes-requested
- Material findings: PBF-AR1, PBF-AR2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/architecture-review-r1.md
- Review log: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md
- Review resolution: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md#architecture-review-r1
- Open blockers: PBF-AR1, PBF-AR2
- Required canonical updates: settle activation ownership and deterministic digest algorithms
- Required ADR updates: revise the new projection and activation ADR
- Next stage: review-resolution

## Finding PBF-AR1

Finding ID: PBF-AR1
Finding: Activation ownership and grandfathering eligibility are ambiguous.
Location: docs/adr/ADR-20260727-portable-boundary-first-reference-projection-and-activation.md, Decision; docs/architecture/system/architecture.md, Portable boundary-first reference
Severity: material
Evidence: The architecture stores activation state in both the approved proof-model spec and activation YAML without naming the authoritative owner. It also inventories existing top-level feature-contract paths without limiting grandfathering to accepted historical artifacts, so a draft present at activation could bypass adoption later.
Required outcome: Define one activation-state owner, make the YAML a mechanical evidence projection, grandfather only durable accepted or approved historical feature specs, and define how nonterminal in-flight specs are handled at activation.
Recommendation: Keep the proof-model spec's activation field authoritative; require YAML state parity; include only accepted or approved historical specs in the grandfathered inventory; require every nonterminal in-flight behavior spec to opt in before test-spec approval or block activation.
Safe resolution path: Amend the ADR, canonical crosscutting section, runtime flow, and risk table with those exact ownership and eligibility rules.
needs-decision rationale: none

## Finding PBF-AR2

Finding ID: PBF-AR2
Finding: The activation and projection digest identities are named but not reproducible.
Location: docs/adr/ADR-20260727-portable-boundary-first-reference-projection-and-activation.md, Decision
Severity: material
Evidence: `projection_sha256` and `grandfathered_inventory_sha256` are required fields, but the design does not define serialization, ordering, path separators, or hash input. Different implementations could produce incompatible identities over identical files.
Required outcome: Define deterministic digest algorithms for governed projections and the grandfathered inventory.
Recommendation: Use UTF-8 records sorted by POSIX path, each serialized as `<path>\\0<raw-byte-sha256>\\n`, and SHA-256 the concatenated record bytes; define projection records over the ten projected paths and inventory records over eligible historical spec paths.
Safe resolution path: Add the algorithm to the ADR and canonical crosscutting architecture and require one shared helper for generator and validator use.
needs-decision rationale: none

## Review Dimensions

| Review dimension | Verdict |
| --- | --- |
| Spec alignment | concern |
| Package shape | pass |
| Boundary clarity | concern |
| Data ownership | block |
| Interface safety | concern |
| Runtime and failure handling | pass |
| Deployment and execution boundaries | pass |
| Security/privacy | pass |
| Quality and operations | concern |
| Testing feasibility | block |
| Complexity discipline | pass |
| ADR quality | concern |
| Plan readiness | block |

## Recommendation

Preserve the selected source path, raw-byte projection, existing package flow,
and activation-record approach.
Resolve PBF-AR1 and PBF-AR2 and perform architecture-review R2 before planning.
