# Test-spec package-state simplification R1

Change: `2026-08-28-consolidate-rigorloop-review-gates`
Stage: test-spec
Artifact ID: test-spec
Artifact path: specs/consolidated-review-gates.test.md
Prior artifact identity: sha256:83d0d7f584e7ca73aa06390234fb317ffcda3f2ef533e491f712617c019340ec
Artifact identity: sha256:0f3a235de400f568eb7fa57c4a97f94a8b1dcb9d9c5459958aa32fdce3398b6a
Authoring result: complete

## Proof-map revision

- Replaced aggregate vectors and member-byte freshness cases with explicit ID-to-path map assertions and governed invalidation events.
- Added direct proof for upstream-review replacement, stale lifecycle rejection, identical replay with refreshed context, and the accepted unrecorded-direct-edit limitation.
- Required status output to show member paths, upstream and package review IDs, package status, blockers, correction targets, and next operation.
- Retained atomic settlement, outcome authority, finding attribution, interruption recovery, cutover, and generated-parity proof.
- Updated governing review identities and normalized the proof-map structure to the active `boundary-first-v1` contract.

## Authoring validation

`python scripts/validate-boundary-first.py --check --path specs/consolidated-review-gates.md` passed.
