# Bounded Plan Index and Completed-Plan Archive Explain Change

## Status

M6 implementation explanation recorded; final verify and PR handoff remain downstream.

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

## M4 contributor guidance and skill alignment

M4 makes the archive contract discoverable in contributor-facing surfaces.

`docs/workflows.md` now names `docs/plan-archive.md` in artifact locations and planned-work guidance, explains the recent Done window, points terminal history to the archive, and names the explicit plan-body lifecycle marker and active supersession fields.

`AGENTS.md` now distinguishes `docs/plan.md` from `docs/plan-archive.md`, warns that nonterminal work must not be archived, and records the lifecycle marker and active supersession rules in the plan file policy.

`docs/examples/plans/example-plan.md` now includes the explicit `## Status` marker and points closeout updates to the plan index surfaces rather than only `docs/plan.md`.

`skills/plan/SKILL.md` now tells plan authors to keep the index bounded, update the archive when archiving terminal history, use explicit lifecycle marker fields, and keep active supersession context structurally labeled.

BPIX-M4-CR1 was resolved by adding the three missing R8a ownership points to `skills/plan/SKILL.md`: `implement` owns ongoing plan-body progress, decision, discovery, and validation-note updates; final lifecycle closeout owns lifecycle state transitions across plan index surfaces and the plan body; and `verify` challenges stale lifecycle state before `branch-ready`.

T14 was strengthened so future guidance checks must verify each R8a ownership point in each named surface, rather than accepting keyword or marker presence alone.

## M5 selection and CI routing

M5 makes selected validation understand the new archive surfaces.

`scripts/validation_selection.py` now classifies both `docs/plan.md` and `docs/plan-archive.md` as plan-index surfaces. A change to either surface selects `artifact_lifecycle.validate` with both surfaces, so routine archival validates the recent/archive union rather than only the edited file.

The selector now treats `docs/changes/<change-id>/plan-index-migration.md` as a change-local lifecycle artifact and adds `docs/plan.md`, `docs/plan-archive.md`, and the governing `change.yaml` to the lifecycle validation command. This keeps migration proof checks tied to the index/archive state they prove.

`scripts/test-select-validation.py` adds regression coverage for archive-surface routing, migration-proof routing, representative path classification, and the larger workflow surface set. The CI wrapper did not need a code change because `scripts/ci.sh --mode explicit` already executes the selected `artifact_lifecycle.validate` and `selector.regression` checks.

## M6 lifecycle closeout and handoff evidence

M6 records final implementation evidence without moving the initiative to Done or claiming PR readiness.

The active plan and `docs/plan.md` remain in Active state. The current handoff is for M6 code-review, and final closeout remains blocked on M6 review, downstream verify, and PR handoff.

Final validation for the implementation slice includes lifecycle validator fixtures, selector fixtures, review-artifact closeout validation, explicit lifecycle validation for the plan index surfaces and governing spec/test spec, and broad smoke through `bash scripts/ci.sh`.

The implementation does not add a generated registry, background synchronization, CLI scaffolding, fake merge state, fake CI state, or host-only state.

## Validation

- `python scripts/test-artifact-lifecycle-validator.py` passed.
- `python - <<'PY' ... R8a direct ownership audit` passed after BPIX-M4-CR1 fix.
- `python - <<'PY' ... M4 guidance audit` passed after M4 guidance updates.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path AGENTS.md --path docs/examples/plans/example-plan.md --path specs/plan-index-lifecycle-ownership.test.md` passed after BPIX-M4-CR1 fix.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md` passed after M4 plan-index state update.
- `python scripts/validate-skills.py skills/plan/SKILL.md` passed after M4 guidance updates.
- `python scripts/validate-skills.py` passed after M4 guidance updates.
- `python scripts/build-skills.py --check` passed after M4 guidance updates.
- `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir> && python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5` passed after M4 guidance updates.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md` passed after M4 handoff state update with the existing lifecycle-language warning in the spec.
- `python - <<'PY' ... migration proof count/link assertion` passed after M3 migration.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md` passed after M3 migration.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/change.yaml` passed after M3 migration.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md` passed with the existing lifecycle-language warning in the spec.
- `python -m py_compile scripts/artifact_lifecycle_validation.py scripts/artifact_lifecycle_contracts.py` passed.
- `python scripts/test-select-validation.py ValidationSelectionTests.test_plan_index_surfaces_select_lifecycle_validation_with_both_surfaces ValidationSelectionTests.test_plan_index_migration_proof_routes_with_metadata_and_index_surfaces ValidationSelectionTests.test_first_slice_representative_categories_route_or_block_safely ValidationSelectionTests.test_workflow_refactor_surface_set_selects_expected_checks` passed after M5 implementation.
- `python scripts/test-select-validation.py` passed after M5 implementation.
- `python -m py_compile scripts/validation_selection.py` passed after M5 implementation.
- `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plan-archive.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md` selected `selector.regression` and `artifact_lifecycle.validate` with `docs/plan.md`, `docs/plan-archive.md`, the migration proof, and its `change.yaml`.
- `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plan-archive.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md` passed after M5 implementation.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive` passed during M6 implementation.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md` passed during M6 implementation with the existing lifecycle-language warning in the spec.
- `bash scripts/ci.sh` passed during M6 implementation.
- `git diff --check --` passed.
