# Plan Authoring Evidence R2: Usability-First Boundary-First v0.4.0 Release

Stage: plan
Date: 2026-08-06
Owning change: `docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
Artifact ID: `plan`
Artifact path: `docs/plans/2026-08-06-usability-first-boundary-release.md`
Completion status: complete
Review basis: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/plan-review-r1.md`
Review request: `plan-review-r2`

## Result

- Status: updated.
- Finding addressed: `UBR-PR1-001`.
- Open blockers: none.
- Next stage: plan-review R2.

## Revision

M3 now executes both repository-owned release gates after `v0.4.0` support exists and before code-review handoff or baseline selection:

- `bash scripts/ci.sh --mode release --release-version v0.4.0` executes the release-selected validation bundle.
- `bash scripts/release-verify.sh v0.4.0` executes the separate standing full gate for generated archives, package integrity, and packed installation proof.

The plan distinguishes the two proof points: M3 proves the reviewed pending baseline, while M4 reruns the gates after activation changes the checked state. No milestone, release mechanism, or public action was added.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-08-06-usability-first-boundary-release.md --path docs/changes/2026-08-06-usability-first-boundary-release/change.yaml --path docs/changes/2026-08-06-usability-first-boundary-release/evidence/plan-authoring-r2.md`
- `python scripts/validate-markdown-readability.py docs/plans/2026-08-06-usability-first-boundary-release.md docs/changes/2026-08-06-usability-first-boundary-release/evidence/plan-authoring-r2.md`
- `python scripts/validate-boundary-first.py --path specs/usability-first-boundary-release.md`
- `git diff --check` over the revised plan-owned artifacts.

## Handoff

The revision is ready for plan-review R2. It does not claim review approval, implementation readiness, verification, branch readiness, PR readiness, or public release.
