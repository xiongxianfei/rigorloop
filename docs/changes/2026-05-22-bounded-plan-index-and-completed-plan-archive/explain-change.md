# Bounded Plan Index and Completed-Plan Archive Explain Change

## Status

M2 implementation notes; final explain-change is completed in M6.

## M2 validator contract and fixtures

M2 adds structural validation for the approved plan-index archive contract before the historical migration runs.

The validator now detects explicit plan-body lifecycle markers, checks terminal plan conservation across `Done (recent)` and `Done (archive)`, rejects archive-only nonterminal plans, enforces the recent Done cap, validates terminal entry links, and enforces active supersession fields.

The test suite adds fixture-driven coverage for valid and invalid archive states, lifecycle marker contradictions and unknown values, legacy prose-only status with no terminal inference, and active supersession context.

## M3 index/archive migration

M3 applies the approved archive split to the real plan index.

`docs/plan.md` now keeps Active and Blocked first, adds the index policy comment, points to `docs/plan-archive.md`, and keeps only the 10 most recent completed plans in `Done (recent)`.

`docs/plan-archive.md` stores the older 65 completed-plan entries newest-first as compact one-line terminal summaries.

`docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md` records the preservation proof: 75 pre-migration Done entries, 10 recent entries, 65 archived entries, no duplicates, and every pre-migration entry marked preserved.

Legacy prose-only completed plan bodies were not bulk-edited with lifecycle markers in this migration. Per the approved compatibility rule, the initial migration preserves those historical terminal entries through the migration table instead of prose-based terminal inference.

## Validation

- `python scripts/test-artifact-lifecycle-validator.py` passed.
- `python - <<'PY' ... migration proof count/link assertion` passed after M3 migration.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md` passed after M3 migration.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/change.yaml` passed after M3 migration.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md` passed with the existing lifecycle-language warning in the spec.
- `python -m py_compile scripts/artifact_lifecycle_validation.py scripts/artifact_lifecycle_contracts.py` passed.
- `git diff --check --` passed.
