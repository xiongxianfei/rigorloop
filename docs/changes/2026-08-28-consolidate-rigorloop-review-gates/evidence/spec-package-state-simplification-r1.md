# Specification Revision: Lightweight Review Packages

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Artifact path: specs/consolidated-review-gates.md
Artifact identity: sha256:9284fbeacd3aaaf1fc330f477e5c171c860b864435ea5eb7fec5be9ec9a99ad5
Authoring result: complete

The specification now uses explicit artifact ID-to-path member maps, upstream review IDs, review IDs, and package status. It removes aggregate revisions, package content hashing, per-document package hashes, byte-derived staleness, and hash-based replay. Governed authoring transitions invalidate affected package approval; direct edits outside that workflow are an accepted first-slice limitation.
