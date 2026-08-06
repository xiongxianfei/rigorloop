# PR-readiness full-gate fixes

## Reproduction

The first complete PR-mode run selected 21 checks. Seventeen passed, including
the 537.68-second broad-smoke check, while four diff-scoped checks failed:

- boundary validation rejected changed feature specs;
- artifact lifecycle validation found two owners for the canonical architecture;
- release validation received `profiles` as a release version; and
- 63 of 117 CLI package tests still used the prior public package fixture.

## Root causes and corrections

- The proof-model bootstrap was not exempted by changed-path validation, and
  the two release specs contained boundary records without their activation
  marker or validator-normalized headings and ownership rows. The bootstrap is
  now explicitly exempt, while both governed specs and proof maps use the
  existing closed boundary-first format. Marker placement now composes with
  stage-owned lifecycle governance: it may follow the normalized owning-change
  pointer instead of requiring the forbidden embedded `Status` section.
- The release path parser treated the directory in
  `docs/releases/profiles/v0.4.0.yaml` as the version. The exact profile path
  shape now derives `v0.4.0` from the filename, with a focused regression.
- The usability-first change registered the shared canonical architecture as a
  second owner. The established stage-owned lifecycle change remains the sole
  owner; the release change keeps its reviewed ADR and related-artifact links.
- The package test fixture remained pinned to `v0.3.4` after the package and
  bundled metadata advanced to `v0.4.0`. The release-fixture values and exact
  bundled metadata assertions now use the prepared package version.

## Validation

- `python scripts/test-boundary-first-validation.py`: 64 passed.
- diff-scoped `python scripts/validate-boundary-first.py --check --path ...`:
  passed for all five selected spec paths.
- `python scripts/test-select-validation.py`: 149 passed.
- `python scripts/validate-release.py --recorded-source-auto --version v0.4.0`:
  passed from recorded source `c7b0babe6e8c91655c2b98f4092197eef5fabc69`.
- PR-selected artifact lifecycle command: passed with five pre-existing
  lifecycle-language warnings.
- `npm test --prefix packages/rigorloop`: 117 passed.

The complete PR-mode gate must pass after independent review before the pull
request opens.
