# Vision Skill Simplification and VISION.md Migration Explain Change

## Summary

M1 adds selector support for the `VISION.md` migration before the root artifact is renamed. The selector now treats root `VISION.md` and legacy root `vision.md` as vision surfaces, selects README vision-marker validation for those paths, and blocks validation when both exact root vision entries exist.

M2 renames the root vision artifact to `VISION.md` and updates authored governance, specs, README ownership, proposal guidance, proposal-review guidance, and the canonical `vision` skill. The `vision` skill now uses state-based behavior while preserving overwrite protection, README marker safety, substantive/editorial confirmation, and causal-link gating.

M3 refreshes generated `.codex/skills/` and public adapter skill copies from the canonical skills. The generated diff is limited to the expected `vision`, `proposal`, and `proposal-review` skill copies.

CR1-F1 fixes the first code-review finding by making root `vision.md` and root `VISION.md` coexistence block validation globally, even when the selected changed path is unrelated to either vision file.

## Decision Trail

- Proposal: `docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md`
- Spec: `specs/vision-skill-simplification-and-vision-md-migration.md`, especially `R1`-`R83` and `AC1`-`AC21`.
- Test spec: `specs/vision-skill-simplification-and-vision-md-migration.test.md` `T1`-`T13`.
- Plan: `docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md` M1-M3.
- Architecture: none required; this is selector and validation routing only.

## Diff Rationale By Area

| File or area | Change | Reason | Proof |
| --- | --- | --- | --- |
| `scripts/test-select-validation.py` | Added assertions for explicit `VISION.md`, PR-mode `VISION.md`, both-path conflict, and reintroduced legacy `vision.md` after uppercase migration. | Proves migration routing and invalid coexistence before changing selector code. | `python scripts/test-select-validation.py` failed before implementation, then passed after the selector update. |
| `scripts/validation_selection.py` | Added a shared root vision path set, classified `VISION.md` and `vision.md` as vision, selected marker validation through the existing vision path behavior, and added exact-path conflict detection. | Lets repository-owned validation route both migration paths and fail competing canonical/legacy states. | `python scripts/test-select-validation.py`; explicit selector commands for both root vision paths. |
| `scripts/test-select-validation.py`, `scripts/validation_selection.py` CR1-F1 fix | Added an unrelated-path regression and made both-root-vision conflict detection global within `select_validation`. | Ensures repository-owned validation fails invalid coexistence even when the changed path is not `vision.md` or `VISION.md`. | Red/green `python scripts/test-select-validation.py`; selector-selected explicit CI for selector paths. |
| `VISION.md` / `vision.md` | Renamed root `vision.md` to root `VISION.md` with the safe two-step Git rename. | Makes uppercase `VISION.md` the canonical root project-vision artifact while preserving the approved project vision prose. | `git diff --name-status --find-renames HEAD -- vision.md VISION.md` reports `R100 vision.md VISION.md`. |
| `README.md`, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md` | Updated active source-of-truth, README ownership, and lifecycle guidance to reference `VISION.md`. | Removes active lowercase canonical-path drift and keeps README front-matter subordinate to the canonical vision artifact. | `python scripts/test-skill-validator.py`; `python scripts/validate-readme.py README.md --vision-markers`. |
| `specs/vision-skill.md`, `specs/vision-skill.test.md` | Rewrote the active vision skill contract and proof map around `VISION.md`, state-based behavior, and legacy lowercase handling. | Retires approved lower-path and old mode requirements without dropping quality, security, README marker, or proposal-fit rules. | `python scripts/test-skill-validator.py`; artifact lifecycle validation for both files. |
| `skills/vision/SKILL.md` | Replaced user-facing mode table behavior with state-based establishment, update, and README sync guidance. | Simplifies the user interface while preserving no-overwrite, no silent marker insertion, substantive/editorial, and causal-link gates. | `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py`. |
| `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md` | Updated `Vision fit` guidance to use `VISION.md`, status-line values, migration-recognized legacy behavior, and `proposes a vision revision`. | Aligns proposal creation and review with the new canonical artifact and approved status-line contract. | `python scripts/test-skill-validator.py`. |
| `scripts/test-skill-validator.py` | Added focused assertions for active spec retirement, state-based skill behavior, `VISION.md` governance, and proposal `Vision fit` rules. | Ensures the old path and user-facing mode requirements cannot quietly re-enter active surfaces. | Red before M2 authored changes; green after M2 authored changes. |
| `.codex/skills/` generated skill copies | Regenerated local Codex runtime mirrors for `vision`, `proposal`, and `proposal-review`. | Keeps installed/runtime skill output aligned with canonical skill sources after the `VISION.md` migration. | `python scripts/build-skills.py`; `python scripts/build-skills.py --check`. |
| `dist/adapters/` generated skill copies | Regenerated Claude, Codex, and opencode adapter skill copies for `vision`, `proposal`, and `proposal-review`. | Keeps public adapter packages aligned with canonical skill sources after the `VISION.md` migration. | `python scripts/build-adapters.py --version 0.1.1`; `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`. |
| `docs/changes/...` | Added `change.yaml` and this explanation. | Provides the required durable traceability pack for the non-trivial migration. | `python scripts/validate-change-metadata.py .../change.yaml`. |
| Active plan | Records M1-M3 progress, validation, generated-output refresh, and the exact-path filesystem discovery. | Keeps the living execution plan current during implementation. | Plan is included in lifecycle and whitespace validation. |

## Tests Added Or Changed

- `test_root_vision_path_selects_marker_validation_without_unclassified_block` now covers both `vision.md` and `VISION.md`.
- `test_root_vision_path_conflict_blocks_validation` proves both exact root vision paths block validation.
- `test_root_vision_path_conflict_blocks_unrelated_changed_path` proves both root vision files block validation even when the selected changed path is `README.md`.
- `test_pr_mode_routes_root_vision_without_unclassified_block` now covers PR-mode routing for both root vision names.
- `test_pr_mode_blocks_reintroduced_legacy_vision_without_unclassified_block` proves a legacy lowercase file reintroduced after uppercase migration is classified and blocked as a conflict.
- `test_vision_skill_defines_state_based_boundaries_and_readme_marker_contract` now requires state-based `VISION.md` behavior and forbids the old mode interface.
- `test_vision_skill_quality_refinement_contract` now checks still-valid quality and safety rules against `VISION.md`.
- `test_proposal_skills_define_vision_fit_contract` now checks first-line status values, uppercase vision behavior, no-vision behavior, and the migration-recognized legacy path.
- `test_active_vision_spec_retires_lowercase_path_and_user_facing_modes` proves `specs/vision-skill.md`, `specs/vision-skill.test.md`, and `skills/vision/SKILL.md` no longer require the old canonical path or old mode model.

## Scope Control

- Root `vision.md` is not renamed in M1.
- M2 renames root `vision.md` to `VISION.md` without changing project vision prose.
- The existing project vision content is not changed.
- Generated `.codex/skills/` and `dist/adapters/` output is refreshed only in M3 through repository generators.
- M3 generated output did not change adapter manifests or command aliases.
- The conflict check uses exact root directory entries and Git index paths so case-insensitive filesystems do not falsely report a conflict when only one path is actually present.
- Historical proposals, plans, reviews, and change-local records are not mass-rewritten solely for lowercase `vision.md` references.

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

M2 evidence:

- `python scripts/test-skill-validator.py` failed before M2 authored implementation for the new `VISION.md`, state-based behavior, no-user-facing-mode, and proposal `Vision fit` assertions.
- `python scripts/test-skill-validator.py` passed after M2 authored implementation.
- `python scripts/validate-skills.py` passed after M2 authored implementation.
- `python scripts/validate-readme.py README.md --vision-markers` passed after M2 authored implementation.
- `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path README.md --path VISION.md --path vision.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md` passed.
- `python scripts/test-select-validation.py` passed after M2 authored implementation.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/vision-skill.md --path specs/vision-skill.test.md` passed after M2 authored implementation.
- `python scripts/build-skills.py --check` failed as expected before M3 because generated `.codex/skills/` output is stale relative to canonical skills changed in M2.
- `python scripts/build-adapters.py --version 0.1.1 --check` failed as expected before M3 because generated public adapter skill copies are stale relative to canonical skills changed in M2.
- `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path README.md --path VISION.md --path vision.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md` failed as expected at `skills.drift` before M3 generated-output refresh.
- `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md README.md VISION.md vision.md specs/vision-skill.md specs/vision-skill.test.md skills/vision/SKILL.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md scripts/test-skill-validator.py` passed after M2 authored implementation.
- `python scripts/test-change-metadata-validator.py` passed after M2 lifecycle metadata updates.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed after M2 lifecycle metadata updates.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed after M2 lifecycle metadata updates.
- `git diff --name-status --find-renames HEAD -- vision.md VISION.md` reported `R100 vision.md VISION.md`; root directory inspection reported only `./VISION.md`.

M3 evidence:

- `python scripts/build-skills.py` passed and refreshed generated `.codex/skills/` output.
- `python scripts/build-adapters.py --version 0.1.1` passed and refreshed generated public adapter output.
- `git diff --name-status --find-renames` showed only generated `vision`, `proposal`, and `proposal-review` skill copies under `.codex/skills/` and `dist/adapters/`.
- `python scripts/validate-skills.py` passed.
- `python scripts/test-skill-validator.py` passed.
- `python scripts/test-select-validation.py` passed.
- `python scripts/build-skills.py --check` passed.
- `python scripts/test-adapter-distribution.py` passed.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- `python scripts/validate-adapters.py --version 0.1.1` passed.
- `python scripts/validate-readme.py README.md --vision-markers` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed.
- `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path README.md --path VISION.md --path vision.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed.
- `git diff --check -- .` passed.

CR1-F1 evidence:

- `python scripts/test-select-validation.py` failed before the selector fix for `test_root_vision_path_conflict_blocks_unrelated_changed_path`.
- `python scripts/test-select-validation.py` passed after the selector fix.
- `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py` passed after the selector fix and selected `selector.regression`.
- `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py` passed after the selector fix.
- `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py` passed after the selector fix.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration` passed after recording code-review-r1 and its resolution.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration` passed after closing CR1-F1.
- `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/review-log.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/review-resolution.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/reviews/code-review-r1.md` passed after CR1-F1 evidence updates.

## Outcome and Retrospective

M1 is implemented, committed, code-reviewed, and has had verify-readiness wording corrected. M2 authored-surface implementation was code-reviewed with no blocking findings. M3 generated-output refresh is implemented. code-review-r1 found CR1-F1, and the accepted selector fix is implemented. Do not treat the overall initiative as branch-ready until follow-up code-review, verify, explain-change, and PR handoff complete.

## Readiness

Ready for follow-up `code-review` after the accepted CR1-F1 selector fix.
