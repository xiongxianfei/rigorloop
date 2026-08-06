# Test-Spec Authoring Evidence R2: Usability-First Boundary-First v0.4.0 Release

Stage: test-spec
Date: 2026-08-06
Owning change: `docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
Artifact ID: `test-spec`
Artifact path: `specs/usability-first-boundary-release.test.md`
Completion status: complete
Review basis: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/test-spec-review-r1.md`
Review request: `test-spec-review-r2`

## Result

- Status: updated.
- Finding addressed: `UBR-TSR1-001`.
- Open blockers: none in authoring scope.
- Next stage: test-spec-review R2.

## Revision

T23 remains the direct fail-closed mutation proof for AC-UBR-012 and continues to use CMD06.
It now belongs to M2, where CMD06 is owned and first required.
M1 retains T4 as its direct UBR-R005 and formal-versus-informal ownership proof.

The revision changes no requirement, test behavior, command, fixture, milestone sequence, or implementation scope.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/usability-first-boundary-release.test.md --path docs/changes/2026-08-06-usability-first-boundary-release/change.yaml --path docs/changes/2026-08-06-usability-first-boundary-release/evidence/test-spec-authoring-r2.md`
- `python scripts/validate-markdown-readability.py specs/usability-first-boundary-release.test.md docs/changes/2026-08-06-usability-first-boundary-release/evidence/test-spec-authoring-r2.md`
- `python scripts/validate-boundary-first.py --path specs/usability-first-boundary-release.test.md`
- `git diff --check` over test-spec-owned artifacts.

## Handoff

The revised proof map is ready for test-spec-review R2. No test implementation, production implementation, validation success, branch readiness, PR readiness, or public release is claimed.
