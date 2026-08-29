# Architecture ADR revision evidence R4

Artifact path: docs/adr/ADR-20260828-consolidated-review-package-topology.md
Artifact identity: sha256:0a694e636e980dcae4376d74e0175d25caf0e31c53c3b46f7990ca69bb9f5282
Authoring result: complete
Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Artifact ID: adr-consolidated-review-package-topology
Artifact kind: adr
Artifact role: supporting
Stage authority: architecture
Prior artifact identity: sha256:78276b47a616f1a67e5f7f788eae69887b17d24c4d8260ef432901de81612243
Spec identity: sha256:ae8b9452fc028fadb9cdd616f3d6d07ce312847951ee178e874aab753a1c357c

The revision adds a workflow-owned `advance-stage` lifecycle operation. It validates closed topology edges and exact source-stage completion authority, synchronizes routing projections atomically, adds no separate completion receipt, and keeps settlement separate from continuation so direct reviews remain isolated.
