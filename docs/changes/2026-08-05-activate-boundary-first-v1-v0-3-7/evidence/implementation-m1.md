# M1 implementation evidence

Milestone: M1 — Read-only activation candidate validation

Outcome: implemented and ready for code review.

## Implemented behavior

- Added the exact opt-in `--check --activation-candidate v0.4.0` command.
- Preserved ordinary strict validation, including its existing-tag requirement.
- Added fresh `origin` advertisement checks for remote `main` and tag absence.
- Derived and reported full P/B/T/H identities, exact rollback, absent tag state,
  and stable bundle identities without claiming public activation.
- Required a clean reviewed head, one first-parent transition, an exact baseline,
  immediate v0.3.6 predecessor and lifecycle-only paths after T.
- Added a separate publication-readiness evidence check so M2 can block external
  mutation without making M4 candidate generation depend on its own later
  review evidence.
- Reported each rejected post-T path directly while keeping untrusted values
  redacted.
- Made authoritative fixture-directory selection recognize tracked descendants,
  which is required by the approved CMD4 directory path.

## Boundary and proof coverage

The fixture matrix covers T1-T6 and T12. T16 is covered by the exact selector
command plus the directory-preflight regression. Tests exercise exact and
invalid releases, pending state, local and remote tag conflicts, unreachable
remote state, strict-default preservation, P/B/T/H identities, lifecycle-only
history, post-T skill drift, missing evidence, determinism, clean-tree
authority, side-effect absence, and non-public output.

## Aligned-surface audit

- `scripts/validation_selection.py` and `scripts/test-select-validation.py` were
  added to the implementation slice because the approved CMD4 directory path
  otherwise failed as an untracked artifact even though its contents are
  tracked. No selection routes or check ownership changed.
- The feature spec, test spec, plan, ADR, activation fixture data, release
  metadata, and published skill text are unaffected: M1 implements their
  approved behavior without changing those contracts or release payloads.

## Validation

- `python scripts/test-boundary-first-validation.py` — pass, 70 tests.
- `python scripts/validate-boundary-first.py --check` — pass.
- `python -m py_compile scripts/validate-boundary-first.py scripts/boundary_first_validation.py` — pass.
- `python scripts/select-validation.py --mode explicit --path scripts/validate-boundary-first.py --path scripts/boundary_first_validation.py --path scripts/test-boundary-first-validation.py --path scripts/fixtures/boundary-first/activation` — pass; selected `boundary_first.validate` and `boundary_first.regression`, no blockers or registration debt.
- `python scripts/test-select-validation.py` — pass, 142 tests.
- `python -m py_compile scripts/validation_selection.py` — pass.
- `git diff --check` — pass.

No external refs, tags, releases, packages, or public state were mutated.
