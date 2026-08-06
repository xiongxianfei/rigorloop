# Test-Spec Authoring Evidence: Usability-First Boundary-First v0.4.0 Release

Stage: test-spec
Date: 2026-08-06
Owning change: `docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
Artifact ID: `test-spec`
Artifact path: `specs/usability-first-boundary-release.test.md`
Completion status: complete
Review request: `test-spec-review-r1`

## Result

- Status: created.
- Requirements mapped: UBR-R001 through UBR-R020.
- Boundaries mapped: all eight approved BND IDs and INT-001 through INT-003.
- Test cases: T1 through T23.
- Validation commands: CMD01 through CMD18.
- Uncovered gaps: none.
- Next stage: test-spec-review.

## Proof decisions

- M1 uses three representative semantic journeys and rejects exact prose or scenario-count assertions.
- M2 proves pending and active snapshots independently, one-time read-only derivation, current-file-only validation, exact cleanup, historical compatibility, and rollback.
- M3 executes release-mode CI and the separate standing full gate while activation remains pending.
- M4 reruns those gates after activation changes the checked state.
- Public release mechanisms are proved through safe local fixtures and static workflow checks; lifecycle work never performs external publication.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/usability-first-boundary-release.test.md --path docs/changes/2026-08-06-usability-first-boundary-release/change.yaml --path docs/changes/2026-08-06-usability-first-boundary-release/evidence/test-spec-authoring.md`
- `python scripts/validate-markdown-readability.py specs/usability-first-boundary-release.test.md docs/changes/2026-08-06-usability-first-boundary-release/evidence/test-spec-authoring.md`
- `python scripts/validate-boundary-first.py --path specs/usability-first-boundary-release.test.md`
- `git diff --check` over test-spec-owned artifacts.

## Handoff

The proof map is ready for test-spec-review. No test or production implementation, validation success, branch readiness, PR readiness, or public release is claimed.
