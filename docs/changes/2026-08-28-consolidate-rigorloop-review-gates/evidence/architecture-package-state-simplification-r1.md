# Architecture package-state simplification R1

Change: `2026-08-28-consolidate-rigorloop-review-gates`
Stage: architecture
Artifact ID: adr-consolidated-review-package-topology
Artifact path: docs/adr/ADR-20260828-consolidated-review-package-topology.md
Prior artifact identity: sha256:9ed91387e9b1199f095a18fadfb7f8bf44021e72702bd0451b7b606129c589ca
Artifact identity: sha256:91098e622d577b2e1c8fb7c93fd860a08f6d4fd1f5fd9fb28954da0abf88a92a
Authoring result: complete

## Decision refinement

- Store and display the explicit `artifact ID -> repository-relative path` map for each design and delivery package.
- Bind package authority with the upstream review ID, package review ID and round, outcome, status, correction targets, and evidence path.
- Remove aggregate package revisions and member content hashes from package calculation, storage, status, validation, and retry semantics.
- Invalidate approval only when governed authoring records a member revision or upstream review settlement replaces the bound review ID.
- Retain the existing lifecycle transaction, review independence, atomic settlement, and workflow-owned routing boundaries.

## Concrete result

The ADR now includes a compact YAML example in which users can directly see the exact architecture, specification, ADR, plan, and test-specification paths represented by each package.
