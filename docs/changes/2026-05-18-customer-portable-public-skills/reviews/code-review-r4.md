# Code Review R4

Review ID: code-review-r4
Stage: code-review
Round: 4
Reviewer: Codex code-review
Target: M3. Measurement, dynamic benchmark, adapters, and lifecycle evidence
Reviewed artifact: docs/plans/2026-05-18-customer-portable-public-skills.md
Review date: 2026-05-18
Recording status: recorded
Status: clean-with-notes

## Review Inputs

- Diff/review surface:
  - `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`
  - `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md`
  - `docs/reports/token-cost/skills/runs/2026-05-18-customer-portable-public-skills/`
  - `docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
  - `docs/changes/2026-05-18-customer-portable-public-skills/review-resolution.md`
  - `docs/plans/2026-05-18-customer-portable-public-skills.md`
- Governing spec: `specs/customer-portable-public-skill-evidence.md`
- Test spec: `specs/customer-portable-public-skill-evidence.test.md`
- Plan milestone: `docs/plans/2026-05-18-customer-portable-public-skills.md`, M3
- Prior finding under review: `CPS-M3-CR1`
- Validation evidence:
  - `codex exec --json --ephemeral --skip-git-repo-check` targeted customer-fixture scenarios
  - `python scripts/analyze-codex-jsonl.py` scenario summaries
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-adapters-m3-live`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-18-customer-portable-public-skills`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `git diff --check --`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`

## Diff Summary

The M3 rerun replaces the rejected static-only dynamic benchmark evidence with live `codex exec` scenario evidence. The dynamic benchmark report now records the live fixture, fixture exclusion command, executed command pattern, per-scenario input tokens, largest command output, full-file reads, broad searches, local guide use, portable-default or ambiguity behavior, attempted reliance on absent RigorLoop internals, result quality, and raw JSONL/analyzer evidence paths. The token report summarizes the same measured runtime fields. The plan, change metadata, and review-resolution entry now record the `CPS-M3-CR1` accepted fix and post-fix validation.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | R32-R36 require targeted customer-fixture dynamic benchmark evidence. The dynamic report now states live `codex exec` mode and fixture exclusions, then records required fields for `proposal`, `proposal-review`, `spec`, `plan`, `implement`, `workflow`, `project-map`, `verify`, and `pr` at `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md:7` and `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md:69`. |
| Test coverage | pass | T9 expects input tokens, largest command output, full-file reads, broad searches, local guide use, portable/default blocking, result quality, and absent-internal reliance. The scenario table records those fields, and per-scenario JSONL/analyzer paths are listed at `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md:90`. |
| Edge cases | pass | The fixture deliberately excludes root `AGENTS.md`, root `CONSTITUTION.md`, internal reports, follow-ups, and `docs/project-map.md`; the exclusion command is recorded as passed at `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md:42` and `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md:53`. `code-review-customer-diff-small` is correctly not run because `skills/code-review/SKILL.md` did not change. |
| Error handling | pass | The live scenarios record portable defaults and ambiguity blocks rather than false success: `proposal` blocks on absent local vision, `plan`/`implement` block on missing approved suffix scope, `verify` refuses validation-pass claims, and `pr` blocks readiness on missing git/verify/validation evidence. |
| Architecture boundaries | pass | The fix stays in benchmark/report/lifecycle evidence. It does not introduce CLI status/validate behavior, workflow YAML, generated workflow docs, hard token gates, a full release benchmark suite, or runtime architecture changes. |
| Compatibility | pass | Local `docs/workflows.md`, local specs, local plans, source, tests, and change-root artifacts remain used in the benchmark; RigorLoop repository internals remain absent from the fixture. |
| Security/privacy | pass | The customer fixture uses synthetic data and the report records no requirement for customer secrets, private keys, tokens, private repository metadata, or unrelated local machine paths. |
| Derived artifact currency | pass | The live benchmark setup generated Codex adapter skills from canonical source, and post-fix validation includes `build-skills --check`, `validate-skills`, and adapter build evidence. Generated adapter bodies were not hand-edited. |
| Unrelated changes | pass | The M3 fix is limited to dynamic benchmark evidence, token report summary, lifecycle state, review-resolution, and validation metadata. |
| Validation evidence | pass | Post-fix metadata, review artifact, lifecycle, diff whitespace, skill validator, canonical skill validation, and generated skill checks all passed, and live analyzer summaries provide measured runtime counters. |

## No-Finding Rationale

`CPS-M3-CR1` required real dynamic evidence or an honest non-pass state. The current reports no longer mark unmeasured runtime fields as passing. They record live scenario execution, measured input tokens, measured largest command output, full-file read counts, broad search counts, local guide usage, portable-default or ambiguity behavior, absent-internal reliance status, and result quality. Broad searches are not hidden: `project-map` records 3 and `verify` records 1, with both called out as pass-with-warning rather than silently clean.

The raw JSONL excerpts and analyzer summaries support the report claims. Scenario final outputs state local guide use and no reliance on absent RigorLoop internals, and the analyzer summaries record input-token counts and search/read counters. The remaining warning-level runtime evidence is expected for repository orientation and bounded verification absence checks, not a recurrence of the rejected static-only benchmark problem.

## Residual Risks

- Some plan history still records the pre-fix static-only benchmark as a chronological discovery, followed by the `CPS-M3-CR1` fix. Current handoff and validation notes are authoritative for the next stage.
- This review does not claim branch readiness, PR readiness, CI status, final verification, or successful downstream closeout.

## Recommended Next Stage

Clean final implementation milestone review. Close M3 and close `CPS-M3-CR1`, then hand off to final closeout starting with `explain-change`.
