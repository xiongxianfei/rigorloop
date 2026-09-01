# M6 PR-preflight fixture correction

Stage: implement
Milestone: M6
Validation result: passed
Finding: FV-M6-CR1

The bounded correction updates only `scripts/test-query-change-record.py`: current-behavior fixtures now select `stage-owned-change-local-v3`, and Verify automation fixtures use the current immutable completion rule, `verification passes and the final explanation is recorded`. The production query helper and lifecycle runtime are unchanged; historical v1/v2 progression remains rejected.

## Validation

- `python scripts/test-query-change-record.py` — passed, 26 tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/change.yaml` — passed.
- `git diff --check` — passed.

The authoritative PR-mode gate remains allocated after review closeout so its result covers the reviewed correction revision.
