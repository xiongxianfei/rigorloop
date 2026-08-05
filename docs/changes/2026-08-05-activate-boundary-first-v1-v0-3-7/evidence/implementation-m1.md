# M1 implementation evidence

Milestone: M1 — Read-only activation candidate validation

Outcome: implemented, R1 findings corrected, and ready for R2 code review.

## Implemented behavior

- Added the exact opt-in `--check --activation-candidate v0.4.0` command;
  every supplied value, including the empty string, stays in candidate mode and
  fails unless it is exactly `v0.4.0`.
- Preserved ordinary strict validation, including its existing-tag requirement.
- Added fresh `origin` advertisement checks for remote `main` and tag absence.
- Derived and reported full P/B/T/H identities, exact rollback, absent tag state,
  and stable bundle identities without claiming public activation.
- Required a clean reviewed head, exactly one first-parent transition, an exact
  baseline, and immediate v0.3.6 predecessor.
- Inspected each first-parent commit after T relative to its parent, unioned all
  rejected paths, and used a closed lifecycle path policy. Change-and-revert,
  rename, deletion, and arbitrary package payloads therefore remain rejected.
- Composed publication readiness with canonical change-metadata, formal-review,
  and artifact-lifecycle validators plus settled M1-M4 and candidate JSON state.
- Emitted bounded failure context and stable corrective actions. Ordinary safe
  paths remain exact; sensitive or oversized path identities are hashed.
- Made authoritative directory preflight require every existing file or symlink
  descendant to be tracked. Empty, mixed, only-untracked, and symlink directory
  surfaces fail closed.

## Boundary and proof coverage

The fixture matrix covers T1-T6 and T12. It exercises exact, malformed, and
empty releases; pending state; local and remote tag conflicts; unreachable
remote state; strict-default preservation; P/B/T/H identities; zero, multiple,
and merge-parent-only transitions; lifecycle-only history; every-commit drift;
rename/delete and multiple-path unions; appended repair; fresh replacement;
missing or unsettled evidence; determinism; exact file/ref snapshots; bounded
token, OTP, username, hostname, environment, and temporary-path diagnostics;
and non-public output.

T16 is proved by the exact CMD4 selection, a multi-surface selection regression
covering validator, lifecycle, skill, adapter, package, and release owners, and
the selector suite's fail-closed selected-command regression. Candidate mode
changes tag authority only; it does not remove path-owned sibling checks.

## Aligned-surface audit

- `scripts/validation_selection.py` and `scripts/test-select-validation.py` are
  in the approved CMD4 slice because directory preflight needed the all-tracked
  descendant rule and its boundary regressions. No selection route or check
  ownership changed.
- The feature spec, test spec, plan, ADR, activation fixture data, release
  metadata, and published skill text are unaffected: M1 implements their
  approved behavior without changing those contracts or release payloads.

## Validation

- `python scripts/test-boundary-first-validation.py` — pass, 77 tests.
- `python scripts/validate-boundary-first.py --check` — pass.
- `python -m py_compile scripts/validate-boundary-first.py scripts/boundary_first_validation.py scripts/validation_selection.py` — pass.
- `python scripts/select-validation.py --mode explicit --path scripts/validate-boundary-first.py --path scripts/boundary_first_validation.py --path scripts/test-boundary-first-validation.py --path scripts/fixtures/boundary-first/activation --path scripts/validation_selection.py --path scripts/test-select-validation.py` — pass; selected `boundary_first.validate`, `boundary_first.regression`, and `selector.regression`, with no blockers or registration debt.
- `python scripts/test-select-validation.py` — pass, 144 tests.
- `git diff --check` — pass.

No external refs, tags, releases, packages, or public state were mutated.
