# Spec Authoring Evidence: Stage-Owned Boundary Marker Placement

Stage: spec
Date: 2026-08-06
Artifact ID: spec
Spec: `specs/usability-first-boundary-release.md`
Trigger: `UBR-PRFG-CR1-001`

## Authoring result

- Added UBR-R021 as the narrow stage-owned replacement for standing PBF-R002 marker placement.
- Kept the literal marker, exact-one cardinality, and fail-closed placement mandatory.
- Required the marker after the normalized owning-change pointer and rejected before-pointer, outside-section, and duplicate forms.
- Preserved the standing `## Status` marker form for feature specs outside `stage-owned-change-local-v1`.
- Extended BND-COMPAT-001 with the focused marker compatibility partition and added EC11 and AC-UBR-013 without introducing a new interaction.

## Boundary selection

The change has one distinct compatibility outcome: stage-owned and non-stage-owned feature specs use different authorized metadata locations while preserving identical marker identity and fail-closed cardinality. BND-COMPAT-001 owns that outcome alongside its existing adoption and historical-compatibility partitions; additional boundaries or scenario combinations would repeat it.

Spec-review R4 found that splitting one normalized compatibility applicability row across two boundaries with different requirement subsets violated the proof-model serializer. The R5 candidate uses one BND-COMPAT-001 row with the exact applicability requirement set.

## Validation

- `python scripts/test-change-metadata-validator.py` — pass, 61 tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml` — pass.
- `python scripts/validate-boundary-first.py --check --path specs/usability-first-boundary-release.md` — expected single `BFR-PROOF-MODEL-MISMATCH`: the feature boundary record is structurally valid after the R4 correction, while the downstream test spec still has the previously approved R001-R020 scope and must be refreshed by `test-spec` after spec approval.
- `git diff --check` — pass.

## Handoff

The `spec` artifact entry is `review-required`. The amendment makes no implementation, test-spec, verification, release, or PR-readiness claim.
