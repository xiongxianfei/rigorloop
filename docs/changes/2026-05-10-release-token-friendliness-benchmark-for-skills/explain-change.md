# Explain Change: Release Token-Friendliness Benchmark for Skills

## Summary

This change adds a release-level Token-Friendliness benchmark surface for public RigorLoop skills. It makes token cost reviewable at release time by combining human-readable Markdown reports, structured YAML metadata, fixture-backed Codex benchmark prompts, analyzer summaries, and release validation delegation.

The implementation intentionally uses a report-required gate, not a score-required gate. Missing or invalid report evidence can block a governed release, while token growth and command-output amplification remain warning/high-warning signals in this first slice.

## Problem

RigorLoop publishes skills for downstream projects. Skill cost is not limited to static `SKILL.md` size: skill guidance can cause broad searches, repeated reads, generated-output scans, full-file reads, and large command output. The accepted proposal identified that static measurement alone does not answer whether public skills remain usable within a reasonable context budget during real agent use.

The proposal selected Option 3: measure both static skill size and dynamic runtime behavior, then store release-comparable evidence. The spec turned that decision into a release contract with Markdown plus YAML reports, fixture-backed benchmarks, analyzer summaries, raw-or-sanitized evidence, waiver handling, and release validation integration.

## Decision Trail

| Source | Decision or requirement | Implementation result |
|---|---|---|
| Proposal | Use both static and dynamic Token-Friendliness measures; require a durable release report. | Added release report artifacts under `docs/reports/token-cost/releases/` and run summaries under `docs/reports/token-cost/runs/v0.1.1/`. |
| Proposal | Reports are for humans, metadata is for gates, prompts are fixtures. | Added Markdown report, YAML metadata, prompt fixtures, and standalone YAML validation. |
| Spec `R1`-`R4` | Public releases include Markdown and YAML report evidence. | Added `v0.1.1.md`, `v0.1.1.yaml`, and Markdown/YAML pairing validation. |
| Spec `R6`-`R7` | Dynamic runtime is required for final release unless a valid waiver exists. | Validator enforces final `pass`/`waived`, waiver fields, non-final incomplete metadata, and invalid waiver reasons. |
| Spec `R8`-`R13` | Benchmarks use tracked prompts, a minimal fixture, a runner, temp directories, public Codex skills, and analyzer invocation. | Added `benchmarks/token-cost/`, `scripts/run-token-cost-benchmarks.py`, temp-copy behavior, public adapter skill installation, and analyzer summary output. |
| Spec `R14`-`R18` | Runtime evidence must support raw JSONL omission, analyzer summaries, command-output amplification, and compound full-file-read signals. | Added analyzer summary schema, raw-or-sanitized evidence handling, current Codex command-output parsing, repeated-read detection, and justified-read classification. |
| Spec `R19`-`R20` | Portability and runner metadata are part of release metadata. | YAML validation checks portability status and runner/suite/run evidence agreement. |
| Spec `R21`-`R23` | First release is a baseline; RC reuse decisions are explicit. | Added baseline comparison shape and RC reuse checked-surface validation. |
| Spec `R24`-`R26` | Token-cost validator owns schema; release validation delegates when policy requires. | Added `scripts/validate-token-cost-report.py`; wired `validate_release_output()` and `release-verify.sh` for governed `v0.1.1`. |
| Spec `R27`-`R30` | Thresholds are warning-only; no report generator in the first implementation. | Report is manually authored; validation treats warnings separately from blockers. |
| Spec `R31` | Implementation is milestone-sliced. | M1-M5 split validator, fixtures, runner/analyzer, baseline report, and release integration. |
| Spec `R32` | Release notes link the Token-Friendliness report. | Updated `docs/releases/v0.1.1/release-notes.md`. |
| Spec `R33` | Do not hand-edit generated adapter output. | Public adapter output is measured and validated through generated-output checks; no generated adapter files are hand-edited. |

Architecture records the same flow: a maintainer runs measurement and benchmarks, the runner installs public Codex adapter skills into an isolated temp fixture, analyzer summaries become durable evidence, the Markdown/YAML report is authored, and release validation delegates to the token-cost validator before release readiness is claimed.

## Diff Rationale by Area

| Area / files | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md` | Added the accepted proposal defining the release benchmark obligation and preserved user intent. | Establish why release token-friendliness matters and why both static and dynamic measures are needed. | Proposal goals and Option 3. | Proposal-review R2 approved after R1 findings were resolved. |
| `specs/release-token-friendliness-benchmark-for-skills.md` | Added the approved contract for report files, YAML schema, runner behavior, analyzer evidence, waiver rules, baseline comparison, warning semantics, and release validation. | Make release behavior testable instead of prose-only. | Requirements `R1`-`R33`. | Spec-review R1 findings resolved; test spec maps requirements. |
| `specs/release-token-friendliness-benchmark-for-skills.test.md` | Added traceable tests `T1`-`T18`, including T16 release-validation delegation and RTF-CR8 failure propagation. | Convert spec requirements and edge cases into concrete proof surfaces. | Test spec strategy and coverage map. | Validator, runner/analyzer, report, release, and lifecycle tests. |
| `docs/architecture/system/architecture.md`, `docs/architecture/system/diagrams/container.mmd` | Added release Token-Friendliness benchmark flow, data ownership, risks, and validation boundaries. | Record the long-lived design for benchmark evidence without adding a separate ADR. | Architecture flow steps 1-8. | Architecture-review accepted no separate ADR needed. |
| `benchmarks/token-cost/manifest.yaml`, `benchmarks/token-cost/prompts/*.md` | Added the first seven benchmark prompts for workflow, proposal, implement, code-review, verify, architecture, and learn. | Make runtime benchmark prompts executable fixtures instead of doc prose. | `R8`, `R8c`, `T6`. | `python scripts/test-token-cost-measurement.py`. |
| `benchmarks/token-cost/fixtures/minimal-public-project/` | Added a clean downstream-style fixture with `AGENTS.md`, `VISION.md`, `README.md`, `docs/workflows.md`, `docs/changes/.gitkeep`, and `src/example.txt`. | Measure public skill behavior in a small user-like project, not in the RigorLoop repo. | `R9`, `E5`. | Fixture tests and no generated-skill-source checks. |
| `scripts/validate-token-cost-report.py` | Added standalone schema and semantic validation for release token-cost YAML. | Keep token-cost metadata validation reusable and separate from release readiness. | `R24a`, plan M1. | `python scripts/test-token-cost-report-validation.py`. |
| `tests/fixtures/token-cost/reports/**` | Added valid and raw-omitted report fixtures plus per-run evidence fixtures. | Test schema validation without needing live Codex or release artifacts. | `R14`-`R16`, `R21`, `R22`. | `python scripts/test-token-cost-report-validation.py`. |
| `scripts/analyze-codex-jsonl.py` | Added schema version 1 summaries, raw-omission fields, command-output extraction, full-file/read-signal classification, repeated-read tracking, and justified-read handling. | Turn Codex JSONL into stable, privacy-aware release evidence. | `R15`, `R17`, `R18`. | `python scripts/test-token-cost-measurement.py`; RTF-CR4 through RTF-CR7 resolutions. |
| `scripts/run-token-cost-benchmarks.py` | Added the benchmark runner with fixture copy, public Codex skill installation, temp cleanup policy, Codex command construction, analyzer invocation, and dry-run support. | Make benchmark execution repeatable and avoid measuring repository-local mirrors. | `R10`-`R13`. | Runner tests and live `v0.1.1` benchmark run. |
| `scripts/test-token-cost-measurement.py` | Added tests for prompt/fixture contracts, runner setup, analyzer output, path normalization, repeated reads, justified reads, and current Codex `aggregated_output`. | Provide deterministic proof for runner/analyzer behavior without requiring Codex for ordinary tests. | `T6`-`T13`, `T18`. | Passed during M2-M4 and review-resolution validation. |
| `docs/reports/token-cost/releases/v0.1.1.md`, `docs/reports/token-cost/releases/v0.1.1.yaml` | Added the first release Token-Friendliness baseline report and structured metadata. | Establish the first comparable public release report. | `R1`, `R4`, `R21`, `E9`. | `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`. |
| `docs/reports/token-cost/runs/v0.1.1/*.analysis.yaml` | Added sanitized per-run analyzer summaries for the seven benchmark prompts. | Preserve dynamic runtime and command-output evidence without tracking raw local JSONL. | `R14`, `R15`, `E3`, `E3a`. | Regenerated after RTF-CR7 so command-output amplification is non-zero and current Codex events are parsed. |
| `docs/releases/v0.1.1/release-notes.md`, `docs/releases/v0.1.1/release.yaml` | Linked release notes to the report and added `validation.token_cost_report: pass`. | Make token-friendliness evidence part of release artifacts. | `R32`, M4/M5. | `python scripts/validate-release.py --version v0.1.1`. |
| `scripts/adapter_distribution.py`, `scripts/release-verify.sh`, `scripts/test-adapter-distribution.py` | Delegated governed `v0.1.1` release validation to the token-cost validator, required `validation.token_cost_report`, added release verifier invocation, and added integration tests for missing and invalid token-cost metadata. | Enforce the report-required release gate while keeping historical releases out of scope. | `R24b`, `R26`, `T16`, RTF-CR8. | `python scripts/test-adapter-distribution.py`; `bash scripts/release-verify.sh v0.1.1`. |
| `docs/workflows.md` | Added token-cost validation command and release-verifier description. | Keep contributor-facing release guidance aligned with the new gate. | `R24b`, `R32`, M5. | Lifecycle validation and release verifier validation. |
| `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/**`, `docs/plan.md`, `docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md` | Recorded proposal/spec/plan/code reviews, material findings, resolutions, validation, and milestone state. | Preserve workflow evidence and state ownership across M1-M5. | Workflow and plan policy. | Review artifact, change metadata, and lifecycle validators. |

## Tests Added or Changed

| Test surface | What it proves | Why this level is appropriate |
|---|---|---|
| `scripts/test-token-cost-report-validation.py` | Standalone YAML schema, required fields, enum values, waiver/incomplete states, raw-or-sanitized evidence, first baseline, RC reuse, portability, runner metadata, and warning behavior. | Unit-style fixture validation is faster and clearer than driving release validation for every schema case. |
| `scripts/test-token-cost-measurement.py` | Benchmark prompt/fixture shape, runner dry-run behavior, analyzer summary schema, command-output parsing, full-file-read signals, repeated-read detection, justified reads, and current Codex `aggregated_output`. | Runner/analyzer behavior needs deterministic local tests that do not require every contributor to install Codex. |
| `scripts/test-adapter-distribution.py` | Release validation requires token-cost report evidence for governed `v0.1.1`, does not backfill the gate onto historical `v0.1.0`, invokes the token-cost validator from `release-verify.sh`, and propagates invalid metadata failures. | Integration tests prove release-level delegation without duplicating every standalone validator negative case. |
| `docs/reports/token-cost/releases/v0.1.1.yaml` validation | The first release report metadata is machine-checkable and linked to Markdown/report evidence. | Release metadata is the actual gate artifact, so it must pass the standalone validator. |
| `bash scripts/release-verify.sh v0.1.1` | The release-owned gate runs adapter checks, release metadata checks, and token-cost report validation for the governed release. | This is the release command maintainers will run before publishing. |

## Validation Evidence Available Before Final Verify

Commands recorded during the implementation and review-resolution loops include:

- `python scripts/test-token-cost-report-validation.py`
- `python scripts/test-token-cost-measurement.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/measure-skill-tokens.py`
- `python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex`
- `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
- `python scripts/validate-release.py --version v0.1.1`
- `bash scripts/release-verify.sh v0.1.1`
- `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.0`
- `python -m py_compile scripts/validate-release.py scripts/validate-token-cost-report.py scripts/adapter_distribution.py`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `git diff --check --`

Known validation note: `python scripts/validate-release.py --version v0.1.0` fails against the current repository-generated `dist/adapters/manifest.yaml` because the working tree holds `0.1.1` adapter output. Historical token-cost gate scope is still covered by fixture-backed release validation and `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.0`.

Lifecycle validation currently reports existing lifecycle-language warnings in `docs/plan.md` and `docs/workflows.md`. Those warnings are recorded as warnings, not blockers for this change.

## Review Resolution Summary

`docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md` is closed.

- Reviews covered: 15
- Material findings resolved: 18
- Unresolved findings: 0

The material review findings shaped the implementation:

- Proposal review clarified waiver-aware gates, raw/sanitized evidence, analyzer summaries, RC reuse metadata, milestone slicing, and warning labels.
- Spec review clarified raw JSONL omission, non-final incomplete dynamic states, and first-baseline comparison metadata.
- Plan review moved release validation integration out of M1 and into M5.
- Code review findings added RC reuse validation, Markdown/YAML pairing checks, full RC reuse surface coverage, stable analyzer paths, repeated-read signals, justified reads, current Codex `aggregated_output` parsing, and release-level invalid-metadata propagation.
- Code-review R10 closed M5 with no material findings.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Static-size-only release gate | It would miss runtime amplification from broad searches, full-file reads, repeated reads, and command output. |
| Dynamic-only release gate | It would obscure oversized static skill text and make release comparison harder to explain. |
| Parse Markdown prose for release gating | Markdown is for humans; structured YAML is the machine-checkable gate. |
| Add a full report generator immediately | The report shape is still proving itself; the approved spec defers generation until repeated manual-report errors or three comparable stable reports. |
| Commit installed Codex skills inside the benchmark fixture | That would drift from actual public adapter output. The runner installs current public Codex adapter skills into a temporary fixture instead. |
| Require Claude Code and opencode dynamic benchmarks in v1 | Their noninteractive runners and comparable reports are not yet stable; they remain optional first. |
| Backfill token-cost release gates onto older releases | M5 scopes the first required gate to `v0.1.1`; historical releases keep existing adapter/release checks. |
| Track raw JSONL unconditionally | Raw JSONL can contain local paths or too much output. Sanitized analyzer summaries provide durable evidence when raw data is omitted. |

## Scope Control

The change preserves the approved non-goals:

- It does not make token score the only release-quality measure.
- It does not remove safety-critical skill guidance to reduce tokens.
- It does not add hosted telemetry infrastructure.
- It does not require contributors to install every supported agent tool locally for ordinary validation.
- It does not make warning-only token regressions hard release blockers.
- It does not hand-edit generated adapter output to reduce measured size.
- It does not optimize every skill in the same change.
- It does not require Claude Code or opencode dynamic benchmark reports in v1.

## Risks and Follow-Ups

- The first release report is a baseline, so token regression thresholds remain warning-only until comparable history exists.
- Codex runtime evidence can vary. The first suite uses stable prompts and durable summaries, but later reports should compare cautiously.
- Raw JSONL remains omitted for the `v0.1.1` baseline because sanitized summaries are the durable release evidence.
- Claude Code and opencode dynamic reports remain optional until stable noninteractive runners and comparable evidence exist.
- A report generator remains deferred until repeated manual-report errors occur or three comparable stable reports exist.
- Final workflow closeout still needs `verify` and PR handoff after this explanation.

## Readiness

The implementation and code-review loops for M1-M5 are closed, review-resolution is closed, and this explanation records the rationale for the actual diff. The next stage is `verify`; this artifact does not claim final verification, branch readiness, PR-body readiness, or PR-open readiness.
