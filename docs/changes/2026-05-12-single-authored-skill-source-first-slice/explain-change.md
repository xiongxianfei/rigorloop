# Single Authored Skill Source First Slice Change Notes

## Status

- preliminary M1 implementation notes

## Summary

M1 changes local Codex mirror validation so `scripts/build-skills.py --check` proves generated output from canonical `skills/` using non-tracked output instead of requiring checked-in `.codex/skills/` files.

The implementation adds `scripts/test-build-skills.py` coverage for explicit `--output-dir` generation, temp-output `--check`, structural validation failures, and the invariant that check mode does not depend on the tracked `.codex/skills/` root. `scripts/validation_selection.py` now exposes `skills.generation_regression` so generator and canonical skill changes select the focused local-mirror proof alongside existing skill validation.

M2 removes `.codex/skills/**` from tracked Git state, adds `.codex/skills/` to `.gitignore`, and updates contributor-facing docs to state that `skills/` is the only authored skill source. It preserves public adapter package tracking under `dist/adapters/` during the compatibility window.

M3 keeps public adapter skill copies tracked and adds `dist/adapters/README.md` as tracked support metadata for current repository-tree install guidance, support-matrix ownership, and the later release-artifact migration path. `scripts/adapter_distribution.py` now permits that README as support metadata while continuing to drift-check generated adapter output.

M3 also tightens token-cost validation so `.codex/skills/` is rejected with an explicit public-source error. Dynamic public-surface benchmark metadata must continue to identify public adapter output such as `dist/adapters/codex/.agents/skills/` while public adapter skill copies remain tracked.

The final `explain-change` stage will replace or expand this preliminary note with full change rationale after implementation milestones and review-resolution, if any, are complete.
