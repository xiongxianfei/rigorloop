# Test-Spec Authoring Evidence: Boundary Marker Placement

Stage: test-spec
Date: 2026-08-06
Artifact ID: test-spec
Test spec: `specs/usability-first-boundary-release.test.md`
Approved spec input: `spec-review-r5`
Trigger: `UBR-PRFG-CR1-001`

## Authoring result

- Updated the proof scope and input identity from UBR-R001-R020/spec-review R3 to UBR-R001-R021/spec-review R5.
- Added one focused T24 contract case for the authorized stage-owned owner-pointer form, retained non-stage-owned status form, and before-pointer, outside-section, and duplicate failures.
- Extended PRF-007, AC-UBR-012, AC-UBR-013, EC11, and the existing M2 proof row without adding a validation command or implementation milestone.
- Reused CMD06 and the existing boundary validator fixtures because marker placement is already owned by that suite.

## Scenario stop rule

T24 covers the two distinct authorized outcomes and all three named invalid placement classes. Additional combinations would repeat the same ownership or cardinality outcome and are intentionally omitted.

## Authoring checks

- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml` — pass.
- `git diff --check` — pass.
- Proof commands were not executed during test-spec authoring; CMD06 remains reviewable as the existing configured owner and runs during implementation correction validation.

## Handoff

The `test-spec` artifact entry is `review-required`. This authoring record does not claim implemented test success, code-review approval, verification, release, or PR readiness.
