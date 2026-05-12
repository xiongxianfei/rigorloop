# Single Authored Skill Source First Slice Change Notes

## Status

- preliminary M1 implementation notes

## Summary

M1 changes local Codex mirror validation so `scripts/build-skills.py --check` proves generated output from canonical `skills/` using non-tracked output instead of requiring checked-in `.codex/skills/` files.

The implementation adds `scripts/test-build-skills.py` coverage for explicit `--output-dir` generation, temp-output `--check`, structural validation failures, and the invariant that check mode does not depend on the tracked `.codex/skills/` root. `scripts/validation_selection.py` now exposes `skills.generation_regression` so generator and canonical skill changes select the focused local-mirror proof alongside existing skill validation.

The final `explain-change` stage will replace or expand this preliminary note with full change rationale after implementation milestones and review-resolution, if any, are complete.
