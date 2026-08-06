# M2 implementation evidence

Milestone: M2 — Checked-revision activation and exact custom-path retirement

Outcome: implemented and ready for code review.

## Implemented behavior

- Replaced history-, tag-, and remote-derived activation decisions with exact
  validation of the checked `pending` or `active` snapshot.
- Kept one internal, read-only
  `derive_grandfathered_specs(root, baseline_revision)` function. It accepts an
  exact 40-character commit identity, returns raw-UTF-8-byte-sorted eligible
  historical spec paths or bounded issues, and writes no repository state.
- Kept normal `--check` independent of derivation, Git history, tags, remotes,
  and network state. Successful output reports only the checked snapshot and
  release intent; it makes no tagged or published claim.
- Preserved exact `v0.3.6` rollback selection and the existing three-adapter
  metadata checks.
- Deleted the three custom activation-publication scripts and removed their
  catalog and path-selection dependencies. The ordinary boundary validator,
  changed-spec routing, selector regression, and routine release selection
  remain in place.

## Test-first evidence

The new checked-revision tests initially failed because the public/internal
derivation function did not exist. After the implementation, pending and active
fixtures validate independently, active validation raises if any Git or
derivation seam is touched, invalid baseline kinds fail closed, and the retired
candidate CLI is rejected.

## Validation

- `python scripts/test-boundary-first-validation.py` — pass, 59 tests.
- `python scripts/test-select-validation.py` — pass.
- `python scripts/validate-boundary-first.py --check` — pass; pending snapshot,
  release intent `-`.
- `python scripts/select-validation.py --mode explicit --path scripts/boundary_first_validation.py --path scripts/validate-boundary-first.py --path scripts/test-boundary-first-validation.py --path scripts/validation_selection.py --path scripts/test-select-validation.py`
  — pass; selects ordinary boundary validation/regression and selector
  regression, with no custom activation-release check.
- `python -m py_compile scripts/boundary_first_validation.py scripts/validate-boundary-first.py scripts/validation_selection.py`
  — pass.
- `git diff --check` — pass.

No tag, publication, push, merge, registry write, network request, or external
state mutation was performed.
