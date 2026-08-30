# Specification package-state simplification R2

Change: `2026-08-28-consolidate-rigorloop-review-gates`
Stage: spec
Artifact ID: spec
Artifact path: specs/consolidated-review-gates.md
Prior artifact identity: sha256:9284fbeacd3aaaf1fc330f477e5c171c860b864435ea5eb7fec5be9ec9a99ad5
Artifact identity: sha256:7405ae69fb0b2868079408102d9bd24e1e8c213bea106306a8291af5dbfccc1b
Authoring result: complete

## Revision

- Replaced the byte-inspection invariant with two explicit invalidation events: a governed member revision and replacement upstream-review settlement.
- Made the artifact ID-to-path member map directly visible in lifecycle state and bound by each package review record.
- Clarified idempotent review replay: callers refresh the lifecycle revision while retaining identical review data; stale lifecycle revisions still fail.
- Preserved the explicit first-slice limitation that unrecorded direct edits are not automatically detected and do not justify content hashing.

## Finding addressed

`CRG-SR5` is addressed by one consistent no-hash invalidation boundary. Same-stage Spec Review remains required before approval.
