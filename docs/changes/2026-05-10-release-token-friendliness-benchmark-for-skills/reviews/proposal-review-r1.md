# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`
- Related specs: `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md`, `specs/skill-token-cost-optimization.md`, `specs/multi-agent-adapters-first-public-release.md`
- Existing baseline: `docs/reports/token-cost/2026-05-10-baseline.md`

## Findings

### RTF1 - Dynamic benchmark waiver semantics conflict with "benchmark suite was not run"

Finding ID: RTF1
Severity: major
Evidence: The proposal says release verification blocks when "the benchmark suite was not run" or dynamic runtime measurement is omitted, while also allowing final public release dynamic benchmarks to be `pass` or explicitly `waived` with maintainer approval and evidence.
Required outcome: Make the gate rule unambiguous.
Safe resolution: Change the blocking rule to "the dynamic benchmark suite was not run and no valid waiver exists" and define final release dynamic status as `pass` or `waived` with required waiver evidence.

### RTF2 - Raw JSONL tracking and sanitized-summary behavior need one contract

Finding ID: RTF2
Severity: major
Evidence: The proposal says raw JSONL benchmark runs live under `docs/reports/token-cost/runs/<release-version>/`, but also says raw JSONL may be omitted when too large or sensitive. The schema currently shows a direct `jsonl` path for each run.
Required outcome: Add explicit raw and sanitized evidence fields so missing JSONL can be distinguished from intentional sanitized-summary evidence.
Safe resolution: Add per-run `evidence` metadata with `raw_jsonl_tracked`, `jsonl`, `analysis`, `sanitized_summary`, and `raw_omission_reason`, and validate raw JSONL or analyzer/sanitized summary evidence.

### RTF3 - Analyzer summary format is required by the runner but not specified enough

Finding ID: RTF3
Severity: major
Evidence: The proposal says the benchmark runner invokes `analyze-codex-jsonl.py` and stores per-run summaries next to JSONL outputs, but it does not define the summary file format or required fields.
Required outcome: Define a minimal analyzer summary schema.
Safe resolution: Add a `schema_version: 1` analyzer summary shape with run identity, usage, tool output, signals, and verdict fields.

### RTF4 - Benchmark-relevant change detection needs a release-owner decision surface

Finding ID: RTF4
Severity: major
Evidence: The proposal defines benchmark-relevant changes between RC and final release, but RC reuse metadata does not require a checked-by owner or checked surface.
Required outcome: Add a required RC-reuse decision field in metadata.
Safe resolution: Add `rc_reuse.checked_by`, `rc_reuse.checked_surface`, and rationale fields, and require a new run or waiver when benchmark-relevant changes occurred.

### RTF5 - First implementation may be too large without milestone boundaries

Finding ID: RTF5
Severity: concern
Evidence: The acceptance criteria include report format, structured metadata, release guidance, baseline report, static and dynamic measurement, command-output amplification, portability, prompt fixtures, manifest, minimal fixture, runner, temp policy, analyzer invocation, metadata validation, and release validation delegation.
Required outcome: Ensure the later plan slices implementation into reviewable milestones.
Safe resolution: Add milestone guidance: M1 metadata schema and validator, M2 benchmark fixture and prompt suite, M3 runner and analyzer-summary integration, M4 first baseline report, and M5 release validation integration.

### RTF6 - "Hard warning" phrasing may confuse release gates

Finding ID: RTF6
Severity: concern
Evidence: The proposal suggests "hard warning" thresholds while also saying warning thresholds are not hard release blockers in the first slice.
Required outcome: Rename severity labels so warning severities do not sound like blockers.
Safe resolution: Use `warning`, `high-warning`, and `blocker`; state that warning and high-warning do not block release in the first slice.

## Checklist coverage

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal states the release-level token-friendliness problem clearly. |
| User value | pass | Release evidence and downstream skill usability are concrete user value. |
| Option diversity | pass | Static-only, dynamic-only, and combined measurement are compared. |
| Decision rationale | pass | The chosen combined model follows from measured runtime amplification risk. |
| Scope control | concern | RTF5 asks the follow-on plan to slice the broad first implementation. |
| Architecture awareness | pass | Release validation, benchmark fixtures, scripts, reports, and public adapter paths are visible. |
| Testability | changes-requested | RTF1, RTF2, RTF3, and RTF4 affect release-gate testability. |
| Risk honesty | concern | RTF6 clarifies warning language to avoid release-gate ambiguity. |
| Rollout realism | changes-requested | RTF1 and RTF4 clarify final release and RC reuse semantics. |
| Readiness for spec | changes-requested | Resolve RTF1 through RTF6 before spec authoring relies on the proposal. |

## Recommended next stage

Revise the proposal to resolve RTF1 through RTF6, update `review-resolution.md`, then rerun proposal-review or proceed only after owner acceptance of the resolutions.
