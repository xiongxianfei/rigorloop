# M6 workflow-policy test correction

Stage: implement
Milestone: M6
Validation result: passed
Finding: FV-M6-CR3

The correction is confined to `scripts/test-workflow-automation-policy.py`. Current policy tests now assert the exact nine-stage v3 sequence, reject retired v1/v2 selectors and transitions, check removed stages by value rather than nonexistent enum members, and retain the final-holistic review as the sole internal final occurrence. Historical-read tests elsewhere remain unchanged.

## Validation

- `python scripts/test-workflow-automation-policy.py` — passed, 20 tests.
- `python scripts/test-workflow-code-state.py` — passed, 19 tests.
- `python scripts/test-query-change-record.py` — passed, 26 tests.
- `git diff --check` — passed.

Production workflow policy code is unchanged. The authoritative PR-mode gate remains allocated after targeted rereview.
