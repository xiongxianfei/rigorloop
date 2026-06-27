# Selector-Regression Preservation Baseline

Change ID: 2026-06-27-selector-regression-runtime-reduction
Milestone: M1. Baseline, Profile, and Identity Inventory
Recorded: 2026-06-27

## Scope

This is the M1 baseline preservation inventory. It records the behavior that M2 and M3 must preserve when reducing selector-regression runtime. Revised evidence is intentionally pending until after runtime-reducing changes exist.

## Summary Matrix

| Surface | Baseline evidence | Revised proof | Result |
| --- | --- | --- | --- |
| selected test IDs | 109 unittest IDs, SHA-256 `5ff607b42e770590fcb15d5dd45ba2b512c9e0486a079d158c54051009f63ec4` | pending M2/M3 | baseline recorded |
| selected check IDs | `artifact_lifecycle.validate`, `selector.regression` for M1 selector paths after runtime evidence registration | pending M2/M3 | baseline recorded |
| missing-route blockers | `test_unregistered_change_evidence_produces_registration_debt`, `test_unclassified_path_blocks_without_fail_open`, `test_mixed_classified_and_unclassified_paths_block_partial_execution`, `test_diagnostic_broad_smoke_does_not_erase_missing_route_blocker` | pending M2/M3 | baseline recorded |
| registered routes | `test_registered_change_evidence_selects_declared_checks_and_governing_metadata`, `test_selector_runtime_evidence_files_route_without_manual_debt` | pending M2/M3 | baseline recorded |
| CLI behavior | `ScriptOutputContractTests`, `test_cli_outputs_json_for_classified_skill_path`, `test_missing_mode_specific_inputs_return_json_error` | pending M2/M3 | baseline recorded |
| selected-CI wrapper | `test_ci_wrapper_executes_selector_selected_path_and_root_checks`, timeout/signal, execution-flag, selector-fixture, and failure-preservation tests | pending M2/M3 | baseline recorded |
| diagnostics | output-contract tests, missing-route blocker tests, selected-CI failure tests | pending M2/M3 | baseline recorded |
| broad-smoke classification | `test_broad_smoke_child_classification_covers_ci_children`, `test_broad_smoke_classification_blocks_unsafe_candidate_claims`, `test_broad_smoke_classification_keeps_runtime_sequential` | pending M2/M3 | baseline recorded |
| cache boundary | `cache_status: not-applicable` asserted in selector checks and CLI output tests | pending M2/M3 | baseline recorded |
| final verify | unchanged and outside selector-runtime evidence | pending M3 boundary check | baseline recorded |

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
