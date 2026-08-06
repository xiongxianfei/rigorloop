# Plan Authoring Evidence: Usability-First Boundary-First v0.4.0 Release

Stage: plan
Date: 2026-08-06
Owning change: `docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
Artifact ID: `plan`
Artifact path: `docs/plans/2026-08-06-usability-first-boundary-release.md`
Completion status: complete
Review request: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/plan-review-r1.md`

## Result

- Status: created.
- Milestones: four implementation milestones plus the required test-proof gate and external release handoff.
- Plan index: updated to replace the cancelled custom candidate/atomic-publication plan with the current plan reference.
- Mutable planned-work state: initialized exactly once because this stage registered the new primary plan; M1 through M4 start `planned`, and workflow owns every later transition.
- Open blockers: none.
- Next stage: plan-review.

## Planning decisions

- M1 owns automatic concise skill behavior and semantic E1-E3 journeys.
- M2 owns current-file activation, the internal derivation function, exact custom-path retirement, selector preservation, and rollback proof.
- M3 owns the complete routine `v0.4.0` payload while activation remains pending.
- M4 consumes one exact reviewed M3 pending revision, freezes its inventory, and runs integrated checked-revision and routine release proof.
- Public tagging and publication remain an explicit post-merge maintainer action, not a lifecycle milestone.

## Boundary coverage

All eight approved boundary IDs and INT-001 through INT-003 map to affected surfaces, dependencies, rollback units, and proof timing in the plan. No new boundary, interaction, behavior, public command, or release mechanism was introduced.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-08-06-usability-first-boundary-release.md --path docs/plan.md --path docs/changes/2026-08-06-usability-first-boundary-release/change.yaml --path docs/changes/2026-08-06-usability-first-boundary-release/evidence/plan-authoring.md`
- `python scripts/validate-markdown-readability.py docs/plans/2026-08-06-usability-first-boundary-release.md docs/plan.md docs/changes/2026-08-06-usability-first-boundary-release/evidence/plan-authoring.md`
- `python scripts/validate-boundary-first.py --path specs/usability-first-boundary-release.md`
- `git diff --check` over plan-owned artifacts.

## Handoff

The plan carries stable execution intent only. It does not claim plan-review approval, test-spec readiness, implementation completion, verification, branch readiness, PR readiness, or public release.
