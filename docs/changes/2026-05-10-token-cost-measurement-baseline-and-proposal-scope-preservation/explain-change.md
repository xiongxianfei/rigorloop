# Token Cost Measurement Baseline and Proposal Scope Preservation Change Explanation

## Status

final closeout review requested

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

## M3. Proposal scope preservation skill and validator updates

M3 updates the canonical proposal and proposal-review skills so broad user requests cannot silently lose goals during proposal narrowing:

- `skills/proposal/SKILL.md` now requires proposal authors to extract initial goals, concerns, constraints, and requested outcomes before drafting or materially revising a proposal.
- `skills/proposal/SKILL.md` now requires every initial user goal to be visibly treated as in scope, out of scope, deferred follow-up, rejected option, or open question.
- `skills/proposal/SKILL.md` now includes an `Initial intent preservation` table shape for broad or multi-part requests.
- `skills/proposal-review/SKILL.md` now requires scope preservation review and `changes-requested` outcomes when goals disappear, deferred goals have no follow-up, rejected goals lack rationale, or narrowed scope has no explanation.
- `skills/proposal-review/SKILL.md` now uses unified review status vocabulary in its expected output: `approved`, `changes-requested`, `blocked`, or `inconclusive`.
- `scripts/test-skill-validator.py` now contains narrow phrase checks for the new proposal and proposal-review guidance.
- `scripts/test-skill-validator.py` now checks that proposal-review expected output includes `changes-requested` and a scope-preservation result so the output contract cannot drift from the scope-preservation rule again.

The canonical skill text keeps repository-maintainer validation and generated-output mechanics out of the published guidance.

## M4. Generated skill and adapter refresh

M4 refreshes generated output from the canonical M3 skill changes:

- `.codex/skills/proposal/SKILL.md` and `.codex/skills/proposal-review/SKILL.md` now match the canonical proposal and proposal-review skills.
- Public adapter packages for Claude, Codex, and opencode now include the proposal scope-preservation guidance and proposal-review unified review status output.

The generated files were produced with repository generators, not hand edits. Public adapter validation uses version `0.1.1`, matching the active version requirement in the plan.

## M5. Final lifecycle closeout

M5 records final lifecycle evidence after M1-M4 each passed their milestone review loop:

- M1-M4 implementation milestones are closed.
- Review-resolution is closed with no unresolved findings.
- `docs/plan.md` remains active because verify and PR handoff have not completed, but it now reflects that implementation milestones are closed and M5 final lifecycle closeout is in review.
- Final validation evidence is recorded in the active plan and `change.yaml`.

This closeout does not claim PR readiness. A final M5 code-review, verify, and PR handoff still need to run.

## Validation

Milestone validation is recorded in the active plan and `change.yaml`.
