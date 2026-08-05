# PR-readiness selector bug fix

## Reproduction

After refreshing `origin/main`, the PR-equivalent command
`bash scripts/ci.sh --mode pr --base origin/main --head HEAD` stopped during
selector preflight with `unclassified-path` for
`specs/boundary-first-resources.yaml`.

Expected behavior follows `PBS-R026` and `PBS-R027`: the canonical resource
manifest is a boundary-reference surface, so it must select boundary
validation and reference-projection regression without selecting artifact
lifecycle validation solely for that path.

## Root cause

`scripts/validation_selection.py` classified the activation YAML, canonical
Markdown resources, and reference implementation scripts, but omitted the new
canonical resource-manifest YAML from both the general boundary surface and
the boundary-reference surface. The full PR changed set therefore failed
closed before any selected checks ran.

This was an integration mismatch in M3 selector registration. The approved
specification already defined the intended ownership, so no contract or
architecture change was required.

## Regression and fix

The existing boundary-surface matrix now includes
`specs/boundary-first-resources.yaml` and requires both
`boundary_first.validate` and `boundary_first.reference_regression`.
The test failed with the same `unclassified-path` result before the production
change.

The production fix adds the exact manifest path to the two existing boundary
surface predicates. No general YAML fallback or unrelated routing change was
introduced.

## Validation

- Focused regression before the fix: failed as expected for the manifest.
- Focused regression after the fix: passed.
- Explicit manifest selection: passed with category `boundary-first`, no
  blocking result, and exactly the two owned boundary checks.
- `python scripts/test-select-validation.py`: 141 tests passed in 45.98
  seconds.

The complete PR-mode command must pass after independent code review before PR
handoff resumes.
