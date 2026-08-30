# Architecture registration blocker

Stage: architecture
Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Status: blocked
Blocking code: RL_ARTIFACT_PATH_OWNED
Blocking invariant: cross-change-artifact-ownership
Blocked target: architecture
Blocked path: docs/architecture/system/architecture.md
Current owning change: 2026-08-24-governed-lifecycle-cli
Preserved registered target: adr-consolidated-review-package-topology
Preserved registered identity: sha256:1c69b99ef3d6fac92b60fd0100d576dd0743b1ed09f2b92f0755a6aa986487c9
Restored canonical identity: sha256:78e708c76b5f787e4f54e55d16d7abc827dd16f90ea578b4dec11f06cf93ff67

The lifecycle CLI rejected canonical registration without mutation because it treats an older shared-path registration as a permanent exclusive owner. The attempted canonical and diagram edits were subsequently restored byte-for-byte so architecture content remains unchanged until automatic succession is supported.

ADR-20260828 now removes the proposed handoff receipt, reservation, and transfer operation. Architecture context should provide the prior canonical identity transiently, and successful registration by the authorized current change should establish current ownership automatically while preserving older registrations as historical revision evidence.

The revised ADR is independently valid and remains registered at `review-required`. No canonical or diagram target is currently authored for this change. Canonical authoring remains blocked until automatic canonical succession is implemented; no separate ownership-transfer evidence should be added.
