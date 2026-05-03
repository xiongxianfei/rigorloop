# Vision Skill Simplification and VISION.md Migration Explain Change

## Summary

M1 adds selector support for the `VISION.md` migration before the root artifact is renamed. The selector now treats root `VISION.md` and legacy root `vision.md` as vision surfaces, selects README vision-marker validation for those paths, and blocks validation when both exact root vision entries exist.

This milestone does not rename `vision.md`, rewrite the project vision, simplify the `vision` skill, or refresh generated skill and adapter output. Those are planned for later milestones.

## Decision Trail

- Proposal: `docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md`
- Spec: `specs/vision-skill-simplification-and-vision-md-migration.md`, especially `R9`-`R12`, `R15`, `R66`-`R69`, `R71`, `R83`, and `AC10`-`AC12`, `AC19`-`AC20`.
- Test spec: `specs/vision-skill-simplification-and-vision-md-migration.test.md` `T9`.
- Plan: `docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md` M1.
- Architecture: none required; this is selector and validation routing only.

## Diff Rationale By Area

| File or area | Change | Reason | Proof |
| --- | --- | --- | --- |
| `scripts/test-select-validation.py` | Added assertions for explicit `VISION.md`, PR-mode `VISION.md`, both-path conflict, and reintroduced legacy `vision.md` after uppercase migration. | Proves migration routing and invalid coexistence before changing selector code. | `python scripts/test-select-validation.py` failed before implementation, then passed after the selector update. |
| `scripts/validation_selection.py` | Added a shared root vision path set, classified `VISION.md` and `vision.md` as vision, selected marker validation through the existing vision path behavior, and added exact-path conflict detection. | Lets repository-owned validation route both migration paths and fail competing canonical/legacy states. | `python scripts/test-select-validation.py`; explicit selector commands for both root vision paths. |
| `docs/changes/...` | Added `change.yaml` and this explanation. | Provides the required durable traceability pack for the non-trivial migration. | `python scripts/validate-change-metadata.py .../change.yaml`. |
| Active plan | Records M1 progress, validation, and the exact-path filesystem discovery. | Keeps the living execution plan current during implementation. | Plan is included in targeted whitespace and selector validation. |

## Tests Added Or Changed

- `test_root_vision_path_selects_marker_validation_without_unclassified_block` now covers both `vision.md` and `VISION.md`.
- `test_root_vision_path_conflict_blocks_validation` proves both exact root vision paths block validation.
- `test_pr_mode_routes_root_vision_without_unclassified_block` now covers PR-mode routing for both root vision names.
- `test_pr_mode_blocks_reintroduced_legacy_vision_without_unclassified_block` proves a legacy lowercase file reintroduced after uppercase migration is classified and blocked as a conflict.

## Scope Control

- Root `vision.md` is not renamed in M1.
- The existing project vision content is not changed.
- Generated `.codex/skills/` and `dist/adapters/` output is not touched in M1.
- The conflict check uses exact root directory entries and Git index paths so case-insensitive filesystems do not falsely report a conflict when only one path is actually present.

## Verification Evidence

Current M1 evidence:

- `python scripts/test-select-validation.py` failed before selector implementation for the newly added uppercase/conflict assertions.
- `python scripts/test-select-validation.py` passed after the selector implementation.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed.
- `python scripts/select-validation.py --mode explicit --path VISION.md` passed and selected `readme.vision_markers`.
- `python scripts/select-validation.py --mode explicit --path vision.md` passed and selected `readme.vision_markers`.
- `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py` passed and selected `selector.regression`.
- `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py` passed.
- `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md` passed as extra evidence for the changed plan and change-local pack.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed for the related lifecycle artifact set.
- `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration` passed.

Final M1 validation is also recorded in `change.yaml` and the active plan.

M1 code review returned `clean-with-notes`. The first verify pass found the selector behavior, tests, metadata, and lifecycle validation credible, then blocked on stale readiness wording in the active plan and test spec. This follow-up updates those readiness surfaces to point at M2 instead of the completed M1 slice.

Follow-up validation for the readiness fix passed:

- `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
- `python scripts/select-validation.py --mode explicit --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md`
- `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md`
- `git diff --check -- docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md specs/vision-skill-simplification-and-vision-md-migration.test.md docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration`
