# Token Cost Measurement Baseline and Proposal Scope Preservation Change Explanation

## Status

in progress

## Scope

This change implements the approved token-cost measurement baseline and proposal scope-preservation initiative. It is milestone-based; this explanation is updated as implementation milestones complete.

## M1. Measurement scripts and parser tests

M1 adds the local measurement commands required by the approved spec:

- `scripts/measure-skill-tokens.py` measures canonical skill Markdown files and reports path, byte size, line count, estimated token count, success status, and largest Markdown sections when headings are available.
- `scripts/analyze-codex-jsonl.py` analyzes recorded Codex JSONL sessions and reports token usage when present, unavailable token usage when absent, tool calls, command-output lines and bytes, estimated command-output tokens, largest outputs, broad searches, full-file reads, high output caps, repeated file reads, and top measured cost drivers.
- `scripts/test-token-cost-measurement.py` covers M1 static measurement and JSONL analyzer behavior before downstream report generation uses these commands.
- `tests/fixtures/token-cost/sample-codex-session.jsonl` provides a small non-private direct-validation fixture for the analyzer command.

The M1 implementation intentionally does not add hosted telemetry, hard token-budget CI gates, or a live command wrapper. Command-output amplification starts inside `scripts/analyze-codex-jsonl.py`, matching the approved first-slice contract.

## M2. Durable baseline report and change evidence

M2 adds the first durable token-cost baseline report:

- `docs/reports/token-cost/2026-05-10-baseline.md` records static skill cost, Codex JSONL session cost, tool-output amplification, top cost drivers, first-baseline comparison, conclusions, and next actions.
- `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml` links to the report under `reports.token_cost_baseline`.
- `scripts/test-token-cost-measurement.py` now includes a lightweight report-shape and change-link test so the durable report does not silently disappear.

The report links from change-local evidence rather than duplicating the report body in this change explanation. The benchmark source is the checked-in non-private JSONL fixture from M1; the report states that later baselines should use representative exported sessions when privacy review permits.

## Validation

Milestone validation is recorded in the active plan and `change.yaml`.
