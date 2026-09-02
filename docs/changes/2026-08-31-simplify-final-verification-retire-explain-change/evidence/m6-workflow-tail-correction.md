# M6 workflow-tail fixture correction

Stage: implement
Milestone: M6
Validation result: passed
Finding: FV-M6-CR2

The bounded correction changes only v3 test expectations in `scripts/test-workflow-code-state.py`. A final-review-only tail is accepted; legacy review-to-explanation tails are rejected. Test names now describe those outcomes. Production workflow code is unchanged.

## Validation

- `python scripts/test-workflow-code-state.py` — passed, 19 tests.
- `python scripts/test-query-change-record.py` — passed, 26 tests.
- `git diff --check` — passed.

The authoritative PR-mode gate remains allocated after targeted rereview.
