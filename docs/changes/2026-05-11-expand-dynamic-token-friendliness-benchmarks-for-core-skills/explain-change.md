# Explain Change

## Summary

This change expands RigorLoop's token-cost benchmark from the original `skill-token-runtime-v1` baseline to `skill-token-runtime-v2`.

The implementation adds required core benchmark prompts for the standard workflow, introduces a first optional `architecture-review` scenario fixture, teaches token-cost validation and release validation about v2 coverage/result-quality gates, preserves the existing v1 report as pre-transition evidence, and creates the canonical `v0.1.1` v2 transition report with sanitized dynamic analyzer summaries.

## Problem

The first release Token-Friendliness benchmark proved that static skill size alone is not enough. Runtime measurement showed full skill-file reads and high input-token behavior that would not be visible from static token counts.

The v1 suite was also too narrow: it covered some important skills, but not the full user-facing delivery path. The v2 expansion needed to add core workflow coverage without making every optional or extended skill release-blocking immediately, while preserving the already-tracked v1 `v0.1.1` evidence.

## Decision Trail

| Source | Decision or requirement | How the diff implements it |
|---|---|---|
| Proposal | Use `skill-token-runtime-v2`, keep required core small, and keep extended coverage optional. | `benchmarks/token-cost/manifest.yaml` declares v2 groups and keeps optional benchmarks separate from the flat required run list. |
| Spec `R1`-`R4` | Define v2 suite identity, required core suite, transition carryover, and optional extended coverage. | M1 updates the manifest and prompt fixtures; M5 records coverage groups in `docs/reports/token-cost/releases/v0.1.1.yaml`. |
| Spec `R5`-`R6` | Add `architecture-review` as the first optional extended benchmark using a separate scenario fixture. | M2 adds `benchmarks/token-cost/prompts/architecture-review.md` and `benchmarks/token-cost/fixtures/minimal-public-project-architecture-review/`. |
| Spec `R7`-`R9` | Release metadata must include benchmark coverage, manual result-quality review, and role-scoped waiver rules. | M3 adds v2 validator support and M5 records per-run `result_quality`. |
| Spec `R10`-`R13` | Release validation owns changed-surface detection and passes required benchmark context to token-cost validation. | M4 adds required benchmark context generation and `validate-release.py` changed-path inputs. |
| Spec `R14` | Preserve pre-transition v1 evidence when v2 uses the same release version. | M5 creates `v0.1.1-skill-token-runtime-v1-pretransition.{md,yaml}` before making `v0.1.1.{md,yaml}` the v2 report. |
| Spec `R15`-`R17` | Optional warning codes stay stable, non-Codex runners remain optional, and token thresholds remain warning-only. | M3 enforces optional warning behavior; M5 records `implement-handoff` token amplification as `high-warning`, not a blocker. |
| Architecture | YAML gates, Markdown explains, release validation decides required benchmarks, token-cost validation proves the report. | The implementation separates report schema validation from release changed-surface detection and keeps Markdown/YAML paired. |
| Plan M1-M5 | Implement in reviewable slices: prompts, optional fixture, validator, release integration, report evidence. | Each milestone has its own implementation commit and clean code-review record. |

## Diff Rationale By Area

| Area | Files | What changed | Reason |
|---|---|---|---|
| V2 manifest and required prompts | `benchmarks/token-cost/manifest.yaml`, `benchmarks/token-cost/prompts/workflow-route.md`, `plan-handoff.md`, `explain-change-summary.md`, `pr-handoff.md` | Declared `skill-token-runtime-v2`, required core benchmarks, transition carryover benchmarks, and bounded no-edit prompt shapes. | Covers the normal workflow path while keeping the required suite small and stable. |
| Optional architecture-review benchmark | `benchmarks/token-cost/prompts/architecture-review.md`, `benchmarks/token-cost/fixtures/minimal-public-project-architecture-review/` | Added a separate downstream-style scenario fixture with canonical architecture docs, ADR-not-required note, change metadata, explain-change, and diagrams. | Tests the first optional extended review-heavy skill without growing the base fixture or making it release-required. |
| Measurement tests | `scripts/test-token-cost-measurement.py` | Added fixture/manifest tests for v2 grouping, required prompt existence, optional prompt fixture, no-edit wording, and dry-run behavior. | Proves the benchmark suite can be inspected before live Codex runs and guards fixture shape. |
| Token-cost validator | `scripts/validate-token-cost-report.py`, `scripts/test-token-cost-report-validation.py` | Added v2 coverage metadata validation, `result_quality`, required benchmark context support, waiver role checks, claimed optional gates, optional warning checks, and optional coverage/run quality reconciliation. | Makes YAML the release gate and prevents coverage metadata from hiding failed or inconclusive run quality. |
| Release validation | `scripts/adapter_distribution.py`, `scripts/validate-release.py`, `scripts/test-adapter-distribution.py` | Added required benchmark context generation, canonical/generated skill path mapping, generated trace metadata, token-cost validator delegation, and `--changed-path` / `--changed-paths-file`. | Keeps changed-surface ownership in release validation and makes the maintainer-facing release command enforce v2 context. |
| V2 release evidence | `docs/reports/token-cost/releases/v0.1.1.{md,yaml}` | Replaced the canonical report with the first v2 transition report, including coverage groups, manual result quality, comparison metadata, and warning-only token-cost signals. | Creates the machine-checkable and human-readable v2 baseline required by M5. |
| Preserved v1 evidence | `docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.{md,yaml}` | Preserved the existing v1 report under an explicit historical path. | Satisfies the report identity requirement and avoids silently overwriting historical measurement evidence. |
| Analyzer summaries | `docs/reports/token-cost/runs/v0.1.1/*-run1.analysis.yaml` | Regenerated sanitized analyzer summaries for all ten required v2 transition runs. | Provides durable dynamic evidence without committing raw JSONL containing local temp paths and full command output. |
| Workflow/change artifacts | `docs/plans/...`, `docs/plan.md`, `docs/changes/.../change.yaml`, review records, this file | Kept milestone state, validation notes, review closeout, and rationale current. | Maintains the repository's traceability contract for non-trivial planned work. |
| Final verify test drift | `scripts/test-adapter-distribution.py` | Updated two v2 final-release tests to pass explicit empty changed-surface input when validating repository `v0.1.1` artifacts. | Final verify found these tests still used the old v1-style command path after `skill-token-runtime-v2` made changed-surface input mandatory for final releases. |

## Tests Added Or Changed

| Test surface | What it proves |
|---|---|
| `scripts/test-token-cost-measurement.py` | The v2 manifest declares required core, transition carryover, and optional extended coverage; prompts and fixtures exist; dry-run enumeration remains stable. |
| `scripts/test-token-cost-report-validation.py` | V2 reports require coverage metadata, manual `result_quality`, required benchmark context, waiver role validation, claimed optional coverage gating, optional warning behavior, and analyzer evidence references. |
| `scripts/test-adapter-distribution.py` | Release validation builds required benchmark context from changed canonical and generated skill paths, delegates to token-cost validation, and the real `validate-release.py` CLI forwards changed-surface inputs. |

The tests are at the right level because the change is mostly release-process contract behavior: schema validation belongs in the token-cost validator tests, changed-surface ownership belongs in release-validation integration tests, and fixture/prompt shape belongs in measurement tests.

## Validation Evidence

Representative validation evidence recorded in the active plan and change metadata:

- `python scripts/test-token-cost-measurement.py` passed with 24 tests.
- `python scripts/test-token-cost-report-validation.py` passed with 16 tests.
- `python scripts/test-adapter-distribution.py` passed with 68 tests after M4.
- `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.yaml docs/reports/token-cost/releases/v0.1.1.yaml` passed.
- `python scripts/validate-release.py --version v0.1.1 --changed-paths-file /tmp/rigorloop-empty-changed-paths.txt` passed.
- `python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex --output-dir /tmp/rigorloop-token-v2-runs-v0.1.1` passed and produced live raw JSONL outside the repository.
- Sanitized analyzer summaries were regenerated from those raw JSONL files and tracked under `docs/reports/token-cost/runs/v0.1.1/`.
- Selected CI passed with concrete report/analyzer paths, selecting `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `token_cost.regression`, and `token_cost.report_validate`.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills` passed after code-review M5 R1.
- Final verify reran `python scripts/test-adapter-distribution.py`; it first exposed the stale v2 final-release test command path, then passed with 68 tests after the test fix.
- Final verify selected CI passed with `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `token_cost.regression`, and `token_cost.report_validate`.

Known validation note: the original selected CI command that used directory path `benchmarks/token-cost` was blocked by the v1 selector as an unclassified directory path. The plan records the replacement concrete-path selected CI command and its passing checks.

## Review Resolution Summary

Durable review disposition lives in `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/review-resolution.md`.

- Proposal-review findings resolved: `EDTF-PR1`, `EDTF-PR2`.
- Spec-review findings resolved: `EDTF-SR1`, `EDTF-SR2`.
- Plan-review findings resolved: `EDTF-PL1`, `EDTF-PL2`.
- Code-review findings resolved: `EDTF-CR1`, `EDTF-CR2`.
- Clean code-review closeout: M1, M2, M3 R2, M4 R2, and M5 R1.
- Open findings: none.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Benchmark every public skill immediately. | Too expensive and noisy for a release-required first expansion; the approved proposal uses required core plus optional extended coverage. |
| Drop `architecture-no-impact` and `learn-no-durable-lesson` immediately. | That would break continuity with the v1 baseline; the transition release keeps them as required carryover evidence. |
| Overwrite the existing v1 `v0.1.1` report without preserving it. | Spec `R14` requires historical pre-transition evidence to remain linked and reviewable. |
| Automate semantic result-quality checks now. | The approved first slice uses manual structured result-quality review; expected-output automation is deferred until stable patterns emerge. |
| Add automatic release diff discovery in M4. | The accepted first-slice fix uses explicit changed-path input because it is simpler, testable, CI-friendly, and avoids guessing the release diff range. |
| Commit raw Codex JSONL. | Raw JSONL includes disposable local temp paths and full command output; durable release evidence uses sanitized analyzer summaries. |

## Scope Control

The change intentionally does not:

- optimize skill text for lower token cost;
- make optional extended benchmarks release-blocking unless claimed or required by changed-skill policy;
- require Claude Code or opencode dynamic benchmark runs;
- add hosted telemetry;
- introduce shared fixture overlays before the duplication trigger;
- validate waiver approvers against GitHub collaborator data;
- add hard token regression gates.

## Risks And Follow-Ups

- `implement-handoff` produced a high-warning command-output amplification case: one broad search output was estimated at 20,738 tokens. This is a strong candidate for a later optimization slice, but it is warning-only under R17.
- Full-file skill reads still appear across required dynamic runs. Later reports should determine whether shorter activation paths or bounded excerpts are warranted.
- Automatic release diff-range detection remains a future release-validation enhancement.
- The selected CI directory path issue is recorded; future selector work could classify benchmark directories directly.
- Final `verify` passed locally. Current active plan state points to `pr` next; PR handoff has not run yet.
