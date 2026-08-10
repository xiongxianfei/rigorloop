# M5 Governance Evidence

## Result

`validate-artifact-lifecycle.py` is the public `Governance (lifecycle
consistency)` composition boundary. Its shared implementation now invokes the
focused change-metadata validator's complete schema and semantic contract and the
focused review-artifact parser for every in-scope change root, including when a
review record, review log, or review resolution is the directly changed path.
Change-metadata semantics and workflow-state checks remain composed by the same
entry point.

The focused change-metadata and review-artifact modules remain independently
testable implementation owners. M5 does not merge their data models, introduce
a second public governance route, or remove active cache and selector contracts.

## Test-first evidence

The new composition regression initially passed malformed review evidence
through the public lifecycle validator without a finding. After composition was
added, the same fixture fails with artifact class `review_artifacts`, the field
value `rubber-stamp`, its allowed values, the exact review file and line, and the
governing repair surface.

## Validation

- `python scripts/test-artifact-lifecycle-validator.py` — pass; 170 tests in 18.165 seconds after the M5 R1 correction.
- `python scripts/test-change-metadata-validator.py` — pass; 61 tests in 16.94 seconds.
- `python scripts/test-review-artifact-validator.py` — pass; 103 tests in 3.448 seconds.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml` — pass; five governed artifacts plus change-local review evidence validated through the public entry point.
- `git diff --check` — pass.

The focused suites include fail-closed unknown-value regressions for lifecycle,
change-metadata, and review vocabularies. No target agent runtime, prompt,
transcript, network call, or external mutation was used.

## Metrics and rollback

M5 adds no new script or CLI. It adds two focused composition edges, one stable
owner label, one review-path scope association, and two regression tests. Revert the M5
commit to restore the previous separate invocation behavior; the focused parser
modules and their tests remain intact throughout rollback.

## Code-review R1 correction evidence

`PSR-CR-M5-R1-001` is addressed by opting the public CLI into the focused
change-metadata module's existing `validate_file` contract. Library-level
lifecycle fixtures retain their isolated partial-contract mode, while the public
entry point always composes full metadata validation. The new regression proves
that an invalid artifact key is rejected under `change_metadata` with the exact
field, invalid key, and allowed repair values. Existing stage-owned errors are
deduplicated when both focused and lifecycle checks report the same invariant.
