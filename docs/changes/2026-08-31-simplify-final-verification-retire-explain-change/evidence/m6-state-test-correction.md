# M6 workflow-state test correction

Stage: implement
Milestone: M6
Validation result: passed
Finding: FV-M6-CR4

The correction is confined to current fixtures in `scripts/test-workflow-automation-state.py`: the registry omits retired stages, default package reviews use v3, v2/v3 Delivery packages are plan-only while the explicit v1 branch retains its historical test spec, current migration uses v3 and the current Verify completion rule. Historical read and rejection cases remain unchanged.

## Validation

- `python scripts/test-workflow-automation-state.py` — passed, 70 tests.
- `python scripts/test-workflow-automation-policy.py` — passed, 20 tests.
- `python scripts/test-workflow-code-state.py` — passed, 19 tests.
- `python scripts/test-query-change-record.py` — passed, 26 tests.
- `git diff --check` — passed.

Production workflow state code is unchanged. The authoritative PR-mode gate remains allocated after targeted rereview.
