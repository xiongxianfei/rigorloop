# Dated Change-Root Convention

## Summary

This change makes the workflow-managed change-root convention explicit for skill-driven usage that does not call `rigorloop new-change`.

New workflow-managed change roots default to `docs/changes/YYYY-MM-DD-slug/`, while historical numbered, undated, or project-customized roots remain valid legacy records until touched, migrated, or superseded.

## Rationale

The prior guidance used `docs/changes/<change-id>/` without defining how agents should choose `<change-id>`. Other workflow artifacts already use dated names, so agents could create undated change roots while still following the placeholder literally.

The fix records the convention at the workflow-spec level, projects it into `docs/workflows.md`, and teaches `workflow` and `implement` to select or confirm the dated ID before writing a missing change root.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-07-04-dated-change-root-convention/change.yaml` passed.
- `python scripts/test-skill-validator.py` passed.
- `python scripts/validate-skills.py` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/implement/SKILL.md --path scripts/test-skill-validator.py --path docs/changes/2026-07-04-dated-change-root-convention/change.yaml --path docs/changes/2026-07-04-dated-change-root-convention/explain-change.md` passed with pre-existing lifecycle-language warnings in `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`.
- `git diff --check --` passed.
- `bash scripts/ci.sh --mode explicit --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/implement/SKILL.md --path scripts/test-skill-validator.py --path docs/changes/2026-07-04-dated-change-root-convention/change.yaml --path docs/changes/2026-07-04-dated-change-root-convention/explain-change.md` passed. Selected checks: `skills.validate`, `skills.regression`, `skills.generation_regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `guide_system.validate`, and `selector.regression`.
