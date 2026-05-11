# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md
Status: revise
Date: 2026-05-11

## Review Inputs

- `AGENTS.md`
- `CONSTITUTION.md`
- `docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md`
- `specs/release-token-friendliness-benchmark-for-skills.md`
- `docs/architecture/system/architecture.md`
- `docs/architecture/system/diagrams/container.mmd`
- `docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md`
- `docs/plan.md`
- `docs/workflows.md`
- `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md`
- `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md`

## Findings

### RTF-PLR1 - Release validation integration is split across M1 and M5

Finding ID: RTF-PLR1
Severity: material
Dimension: sequencing, milestone size, validation quality, operational readiness

Evidence:

- M1 is titled "Metadata schema and validator", but its likely touched files include `scripts/validate-release.py` and `scripts/release-verify.sh`.
- M1 implementation step 4 says to "Add release-level delegation without requiring token-cost metadata for historical releases unless the release version is in scope for this policy."
- M1 validation commands include `python scripts/validate-release.py --version v0.1.1`, `python -m py_compile scripts/validate-token-cost-report.py scripts/validate-release.py`, and a diff check over `scripts/validate-release.py` and `scripts/release-verify.sh`.
- M1 expected observable result says release validation delegates to the token-cost validator.
- M5 is titled "Release validation integration and documentation", also owns `scripts/validate-release.py` and `scripts/release-verify.sh`, and its steps include deciding governed release scope, delegating from release validation, and updating the release verifier.

Problem:

The plan gives two milestones ownership over the same release-gate integration. That makes implementation sequencing ambiguous: M1 appears to wire release validation before the prompt suite, runner, analyzer summaries, or first report fixture exist, while M5 later repeats that same integration responsibility. This can produce duplicated edits, unstable tests, and unclear milestone review criteria.

Required outcome:

Make milestone ownership unambiguous before test-spec or implementation. Either:

- M1 owns only the standalone token-cost schema validator and its sample metadata tests, while M5 owns `validate-release.py`, `release-verify.sh`, governed-release scope, and release-level delegation; or
- the plan explicitly defines a different non-overlapping split with distinct acceptance criteria and validation commands for each milestone.

Safe resolution:

Revise M1 to remove `scripts/validate-release.py`, `scripts/release-verify.sh`, release-level delegation, and release-level validation commands. Keep M1 focused on `scripts/validate-token-cost-report.py`, parser behavior, schema checks, waiver/incomplete/baseline cases, evidence reference checks, and standalone validator tests. Keep M5 as the integration milestone that delegates from release validation after M1, M2, M3, and M4 provide validator, fixtures, runner/analyzer summaries, and report evidence.

Owner: plan author
Owning stage: plan
Stop state: Plan remains active but is not ready for `test-spec` or implementation until this milestone boundary is clarified.

## Review Dimension Results

| Dimension | Result | Notes |
|---|---|---|
| Self-contained context | pass | The plan gives enough source, context, and orientation for a new contributor. |
| Source alignment | pass | The milestones trace to approved proposal, spec, and architecture requirements. |
| Milestone size | concern | M1 is too broad if it includes both standalone schema validation and release-gate integration. See RTF-PLR1. |
| Sequencing | block | Release validation integration appears before its supporting benchmark and report surfaces exist, then appears again in M5. See RTF-PLR1. |
| Scope discipline | pass | Non-goals protect report generation, token-score hard blockers, generated output, and non-Codex required tooling. |
| Validation quality | concern | M1 validation commands test release integration that should belong to M5 or be replaced by standalone validator fixture checks. |
| TDD readiness | pass | Each milestone names focused test cases and validation commands. |
| Risk coverage | pass | Rollback, Codex availability, raw JSONL privacy, parser limits, and historical release scope are covered. |
| Architecture alignment | pass | The plan follows the architecture split between validator, runner, analyzer summary, metadata, and release validation. |
| Operational readiness | concern | Release readiness behavior is covered, but milestone ownership for wiring it is duplicated. |
| Plan maintainability | pass | Progress, decision log, discoveries, validation notes, and handoff fields are present. |

## Outcome

Verdict: revise

Immediate next stage: plan revision.

`test-spec` readiness: not ready. Resolve RTF-PLR1 first, then rerun plan-review.

Downstream implementation readiness: not ready.

This was an isolated review request. There is no automatic downstream handoff.
