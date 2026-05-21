# Output Contract Red-Test Proof

Change ID: `2026-05-21-script-output-optimization`
Milestone: M2 output contract tests
Finding: `SRO-M2-CR1`

## Purpose

M2 adds output-contract tests before M3 implements the formatter. The required formatter behavior must be visible as failing proof against the old output, but ordinary M2 validation must remain runnable so the test-only milestone can hand off to code-review.

## Ordinary M2 Validation

Command:

```bash
python scripts/test-select-validation.py
```

Expected before M3:

- exits `0`;
- excludes `ScriptOutputContractTests` from the default unittest suite;
- includes `ValidationSelectionTests.test_output_contract_red_tests_are_unmasked_and_separate`, which fails if the required contract tests are hidden behind `@unittest.expectedFailure`.

## Explicit Red-Test Proof

Command:

```bash
python scripts/test-select-validation.py ScriptOutputContractTests
```

Expected before M3:

- exits nonzero;
- fails for old formatter behavior;
- keeps required output-contract failures visible instead of counting them as passing validation.

Observed M2 pre-M3 result:

```text
FAILED (failures=9)
```

Failing cases:

| Test ID | Covers |
| --- | --- |
| `ScriptOutputContractTests.test_output_contract_default_success_is_single_summary_line` | TSRO-002 |
| `ScriptOutputContractTests.test_output_contract_default_failure_expands_failures_only` | TSRO-003 |
| `ScriptOutputContractTests.test_output_contract_quiet_success_is_silent` | TSRO-005 quiet success |
| `ScriptOutputContractTests.test_output_contract_quiet_failure_remains_actionable` | TSRO-005 quiet failure |
| `ScriptOutputContractTests.test_output_contract_conflicting_output_flags_fail_before_tests_run` | TSRO-006 |
| `ScriptOutputContractTests.test_output_contract_zero_executed_tests_fail_with_summary` | TSRO-007 |
| `ScriptOutputContractTests.test_output_contract_reliable_failure_includes_scoped_rerun` | TSRO-008 reliable rerun |

The failure count is `9` because the quiet-success and conflicting-flag tests each contain two subtests.

Passing cases:

| Test ID | Covers |
| --- | --- |
| `ScriptOutputContractTests.test_output_contract_verbose_success_preserves_full_pass_detail` | TSRO-004 |
| `ScriptOutputContractTests.test_output_contract_unreliable_failure_omits_misleading_scoped_rerun` | TSRO-008 unreliable rerun guard |
| `ScriptOutputContractTests.test_output_contract_json_support_is_not_added_in_first_slice` | TSRO-009 |

## Post-M3 Expectation

After M3 implements output shaping:

- `python scripts/test-select-validation.py ScriptOutputContractTests` must exit `0`;
- the output-contract tests must remain ordinary tests, not `expectedFailure` tests;
- ordinary validation must not be able to pass if required output-contract tests are still masked.

M3 must update behavior-preservation evidence with the post-change proof.
