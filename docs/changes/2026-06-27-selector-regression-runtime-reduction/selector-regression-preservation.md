# Selector-Regression Preservation Evidence

Change ID: 2026-06-27-selector-regression-runtime-reduction
Milestone: M1 baseline with M2 fixture-reuse update
Recorded: 2026-06-27
Last updated: 2026-06-27

## Scope

This evidence records the M1 baseline preservation inventory and the M2 fixture-reuse preservation update. M2 introduces reusable repository preflight context for pure selector calls in `ValidationSelectionTests`; it does not change selector routing semantics, CLI-boundary coverage, broad-smoke execution, cache behavior, final verify semantics, branch readiness, PR readiness, or hosted CI claims.

## Summary Matrix

| Surface | Baseline evidence | Revised proof | Result |
| --- | --- | --- | --- |
| selected test IDs | 109 unittest IDs, SHA-256 `5ff607b42e770590fcb15d5dd45ba2b512c9e0486a079d158c54051009f63ec4` | 110 unittest IDs, SHA-256 `a9b79aba3de146846384b7b1f5d00410b84e2682fb65696134085916a50ccb35`; approved test-structure delta adds `ValidationSelectionTests.test_shared_preflight_context_requires_matching_repository_identity` | preserved with approved test-structure delta |
| selected check IDs | `artifact_lifecycle.validate`, `selector.regression` for M1 selector paths after runtime evidence registration | M2 touched-path selector query returns `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `guide_system.validate`, and `selector.regression` with no blockers or registration debt | preserved for touched M2 path set |
| missing-route blockers | `test_unregistered_change_evidence_produces_registration_debt`, `test_unclassified_path_blocks_without_fail_open`, `test_mixed_classified_and_unclassified_paths_block_partial_execution`, `test_diagnostic_broad_smoke_does_not_erase_missing_route_blocker` | retained in default command and targeted `-k selector` validation | preserved |
| registered routes | `test_registered_change_evidence_selects_declared_checks_and_governing_metadata`, `test_selector_runtime_evidence_files_route_without_manual_debt` | retained in default command and targeted `-k selector` validation | preserved |
| CLI behavior | `ScriptOutputContractTests`, `test_cli_outputs_json_for_classified_skill_path`, `test_missing_mode_specific_inputs_return_json_error` | subprocess-backed tests retained; M2 conversion changes only in-process selector preflight reuse | preserved |
| selected-CI wrapper | `test_ci_wrapper_executes_selector_selected_path_and_root_checks`, timeout/signal, execution-flag, selector-fixture, and failure-preservation tests | subprocess-backed selected-CI wrapper tests retained | preserved |
| diagnostics | output-contract tests, missing-route blocker tests, selected-CI failure tests | diagnostics tests retained; no output-shape shortening in M2 | preserved |
| broad-smoke classification | `test_broad_smoke_child_classification_covers_ci_children`, `test_broad_smoke_classification_blocks_unsafe_candidate_claims`, `test_broad_smoke_classification_keeps_runtime_sequential` | retained; M2 does not alter broad-smoke classification or execution | preserved |
| cache boundary | `cache_status: not-applicable` asserted in selector checks and CLI output tests | unchanged; M2 adds no validation cache behavior | preserved |
| final verify | unchanged and outside selector-runtime evidence | unchanged; no final verify, branch readiness, PR readiness, or hosted CI claim | preserved |

## Behavioral Selector Identity

Baseline selector scenarios include:

- selector implementation path changes select `selector.regression`;
- lifecycle and spec paths select lifecycle validation without unclassified fallback;
- registered change evidence selects lifecycle validation;
- selector-runtime evidence files route as registered change evidence without manual-routing debt;
- unknown changed paths block instead of failing open;
- unregistered change evidence creates manual-routing debt unless a complete owner deferral exists;
- broad-smoke diagnostic selection does not erase missing-route blockers;
- cache-boundary metadata remains `not-applicable`;
- broad-smoke classification records required fields and keeps broad-smoke runtime sequential.

## Selected-Check Identity

For the M1 selector path set:

```text
scripts/test-select-validation.py
scripts/validation_selection.py
docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md
docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml
docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md
specs/selector-regression-runtime-reduction.md
specs/selector-regression-runtime-reduction.test.md
docs/plans/2026-06-27-selector-regression-runtime-reduction.md
```

Selected check IDs:

```text
artifact_lifecycle.validate
selector.regression
```

The selector initially blocked on `tracked_authoritative_artifacts` while authoritative artifacts were untracked. After staging the M1 artifact set, selector status is `ok` with no blocking results and no registration debt. Adding the `selector-regression-runtime` evidence class removed the runtime-baseline evidence registration blocker.

## Unittest Identifier Identity

Baseline command used to enumerate IDs:

```bash
python - <<'PY'
import hashlib
import importlib.util
import sys
import unittest
from pathlib import Path
path=Path('scripts/test-select-validation.py')
spec=importlib.util.spec_from_file_location('test_select_validation', path)
module=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=module
assert spec.loader
spec.loader.exec_module(module)
suite=unittest.defaultTestLoader.loadTestsFromModule(module)
ids=[]
def walk(s):
    for item in s:
        if isinstance(item, unittest.TestSuite):
            yield from walk(item)
        else:
            yield item.id().replace('test_select_validation.', '')
ids=list(walk(suite))
print(len(ids))
print('sha256=' + hashlib.sha256('\n'.join(ids).encode()).hexdigest())
PY
```

Baseline result:

- Count: 109
- SHA-256: `5ff607b42e770590fcb15d5dd45ba2b512c9e0486a079d158c54051009f63ec4`

M2 result:

- Count: 110
- SHA-256: `a9b79aba3de146846384b7b1f5d00410b84e2682fb65696134085916a50ccb35`
- Approved test-structure delta: M2 adds `ValidationSelectionTests.test_shared_preflight_context_requires_matching_repository_identity` to prove reusable preflight context cannot be applied to a different repository root.

## M2 Runtime-Reducer Preservation

M2 adds `build_repository_preflight_context(repo_root)` and an optional `preflight_context` on `SelectionRequest`. The default selector API behavior is unchanged when no context is provided. `ValidationSelectionTests.select(...)` now reuses one immutable `RepositoryPreflightContext` for pure selector calls against `ROOT`, avoiding repeated `git rev-parse`, `git status`, and `git ls-files` work for the representative selector table.

Identity guard:

```text
ValidationSelectionTests.test_shared_preflight_context_requires_matching_repository_identity
```

This test proves a cached preflight context raises `ValueError` when used with a different repository root. The context is frozen and contains the resolved repository root, worktree-presence flag, tracked paths, and unmerged path state, so table-driven pure selector fixtures cannot mutate it or silently reuse it for a different repository identity.

Representative table timing evidence:

```bash
/usr/bin/time -p python scripts/test-select-validation.py -k first_slice_representative_categories_route_or_block_safely
```

M1 per-test timing: about `105.804s`.

M2 targeted run: passed in `0.57s` test time, `real 1.05s`.

## Failure-Sensitivity Fixtures

| Fixture | Baseline check | Expected behavior |
| --- | --- | --- |
| unknown changed path | `test_unclassified_path_blocks_without_fail_open` | blocked with `unclassified-path` |
| mixed known and unknown paths | `test_mixed_classified_and_unclassified_paths_block_partial_execution` | blocked; selected known checks do not permit partial execution |
| unregistered change evidence | `test_unregistered_change_evidence_produces_registration_debt` | blocked with `manual-routing-required` |
| broad-smoke plus missing route | `test_diagnostic_broad_smoke_does_not_erase_missing_route_blocker` | broad-smoke selected, missing-route blocker remains |
| registered change evidence | `test_registered_change_evidence_selects_declared_checks_and_governing_metadata` | passes and selects expected lifecycle checks |
| selector runtime evidence | `test_selector_runtime_evidence_files_route_without_manual_debt` | passes and selects lifecycle validation without registration debt |

## Baseline Commands Run

```bash
python scripts/test-select-validation.py -k selector_preservation_surface_keeps_selected_check_identity
python scripts/test-select-validation.py -k unregistered_change_evidence_produces_registration_debt
python scripts/test-select-validation.py -k broad_smoke_child_classification_covers_ci_children
python scripts/test-select-validation.py -k selector_runtime_evidence_files_route_without_manual_debt
python scripts/test-select-validation.py -k change_evidence_registry_entries_are_complete_and_stable
python scripts/test-select-validation.py -k registered_change_evidence_patterns_and_exact_names_match_once
```

All listed baseline preservation commands passed during M1.

## M2 Commands Run

```bash
python scripts/test-select-validation.py -k shared_preflight_context_requires_matching_repository_identity
/usr/bin/time -p python scripts/test-select-validation.py -k first_slice_representative_categories_route_or_block_safely
python scripts/select-validation.py --mode explicit --path scripts/test-select-validation.py --path scripts/validation_selection.py --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md --path docs/plan.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml
```

All listed M2 preservation commands passed before full milestone validation.
