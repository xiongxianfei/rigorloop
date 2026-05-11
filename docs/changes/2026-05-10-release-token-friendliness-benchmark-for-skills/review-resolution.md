# Review Resolution: Release Token-Friendliness Benchmark For Skills

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: code-review-r1
Review closeout: code-review-r2
Review closeout: code-review-r3
Review closeout: code-review-r4
Review closeout: code-review-r5
Review closeout: code-review-r6
Review closeout: code-review-r7

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `plan-review-r1`, `plan-review-r2`, `code-review-r1`, `code-review-r2`, `code-review-r3`, `code-review-r4`, `code-review-r5`, `code-review-r6`, `code-review-r7`
- Findings resolved: 16
- Unresolved findings: 1
- Final result: Proposal-review R1 requested changes for release-gate semantics, run evidence, analyzer summaries, RC reuse, milestone slicing, and warning severity wording; all accepted proposal-review findings were resolved in the proposal. Proposal-review R2 approved the revised proposal with no material findings. Spec-review R1 requested changes for analyzer summary raw-omission compatibility, incomplete non-final dynamic metadata, and first-baseline comparison metadata; all accepted spec-review findings were resolved in the spec. Plan-review R1 requested a milestone-boundary revision; M1 now owns standalone token-cost metadata validation and M5 owns release validation integration. Plan-review R2 approved the revised plan with no material findings. Code-review R1 requested M1 fixes for RC reuse metadata validation and Markdown report metadata-link validation; both findings were resolved in the standalone validator and tests. Code-review R2 requested an M1 fix for partial RC reuse checked-surface validation; RTF-CR3 was resolved in the standalone validator and tests. Code-review R3 found no material findings and closed M1. Code-review R4 found no material findings and closed M2. Code-review R5 requested M3 fixes for analyzer summary path stability, repeated same-file read signals, and justified full-file-read classification; all three findings were resolved in M3 runner/analyzer tests and implementation. Code-review R6 found no material findings and closed M3. Code-review R7 requested an M4 fix for current Codex command-output event parsing; RTF-CR7 is open.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| RTF1 | accepted | resolved | Made dynamic benchmark gate wording waiver-aware. |
| RTF2 | accepted | resolved | Added raw JSONL versus sanitized-summary run evidence metadata. |
| RTF3 | accepted | resolved | Added a minimal analyzer summary schema. |
| RTF4 | accepted | resolved | Added RC reuse decision metadata and rerun-or-waiver rule. |
| RTF5 | accepted | resolved | Added follow-on implementation milestone guidance. |
| RTF6 | accepted | resolved | Replaced `hard warning` with `high-warning` and clarified blocker semantics. |
| RTF-SR1 | accepted | resolved | Aligned analyzer summary schema with raw JSONL omission and sanitized evidence. |
| RTF-SR2 | accepted | resolved | Defined exact metadata fields for non-final blocked/not-run dynamic benchmark states. |
| RTF-SR3 | accepted | resolved | Defined first-baseline comparison metadata when no previous release report exists. |
| RTF-PLR1 | accepted | resolved | Separated standalone token-cost validator work from release validation integration. |
| RTF-CR1 | accepted | resolved | Added RC reuse metadata validation and fixtures to the standalone token-cost validator. |
| RTF-CR2 | accepted | resolved | Validated that the Markdown report names or links the YAML metadata file. |
| RTF-CR3 | accepted | resolved | Validator now requires all RC reuse checked-surface categories. |
| RTF-CR4 | accepted | resolved | Analyzer summaries written by the runner now use stable repo-relative JSONL paths for repository outputs. |
| RTF-CR5 | accepted | resolved | Analyzer repeated-read signals now count repeated same-file reads independently from confirmed full-file classification. |
| RTF-CR6 | accepted | resolved | Analyzer full-file-read classification now supports justified reads when justification metadata is provided. |
| RTF-CR7 | accepted | open | Analyzer must parse current Codex `command_execution` `aggregated_output` events and M4 summaries/report must be regenerated from corrected evidence. |

## Common Resolution Metadata

- Owner: proposal author
- Owning stage: proposal
- Validation target: proposal text and change-local review artifacts
- Validation evidence: `git diff --check -- docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`; `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`

## Finding Details

### proposal-review-r1

#### RTF1 - Dynamic benchmark waiver semantics conflict with "benchmark suite was not run"

Finding ID: RTF1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Updated the release-gate wording to block missing dynamic benchmark runs only when no valid waiver exists, and clarified that final public release dynamic status must be `pass` or valid `waived`.
Rationale: Final-release waivers need to be compatible with the gate wording.
Validation target: Proposal release-gate section distinguishes `pass` and valid `waived` final-release dynamic statuses.
Validation evidence: Shared validation evidence.

### proposal-review-r2

No material findings.

### spec-review-r1

#### RTF-SR1 - Analyzer summary schema conflicts with sanitized raw-JSONL omission

Finding ID: RTF-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Updated analyzer summary schema so `run.jsonl` is required only when raw JSONL is tracked. Added `run.raw_jsonl_tracked`, `run.sanitized_source`, `run.sanitized_summary`, and `run.raw_omission_reason` fields.
Rationale: Durable release evidence must not require private or untracked local raw JSONL paths.
Validation target: R15 and related examples explicitly support raw omitted runs without requiring `run.jsonl` to point at untracked raw JSONL.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/spec-review-r1.md`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`; `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`; `git diff --check -- specs/release-token-friendliness-benchmark-for-skills.md docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`

#### RTF-SR2 - Non-final blocked/not-run dynamic metadata is required but not shaped

Finding ID: RTF-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Added `dynamic_runtime.incomplete` with `reason`, `owner`, `environment`, `follow_up`, and boolean `release_may_proceed`.
Rationale: Non-final blocked/not-run states must be reviewable and testable.
Validation target: R6, R2d, and metadata requirements define the required reason, owner, environment, follow-up, and release-proceed fields.
Validation evidence: Shared spec-review R1 resolution validation evidence.

#### RTF-SR3 - First-baseline comparison metadata is ambiguous

Finding ID: RTF-SR3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Added a first-baseline comparison shape with `baseline: true`, null previous fields, `comparable: false`, `deltas: null`, and a rationale. Numeric deltas are required only when a previous comparable report exists.
Rationale: The first report has no prior release and should not fabricate comparison deltas.
Validation target: R21 and comparison metadata define a first-baseline shape that validators can check without guessing.
Validation evidence: Shared spec-review R1 resolution validation evidence.

#### RTF2 - Raw JSONL tracking and sanitized-summary behavior need one contract

Finding ID: RTF2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added per-run evidence fields for raw JSONL, analyzer summary, sanitized summary, and omission reason.
Rationale: Release validation needs to distinguish missing evidence from intentionally sanitized evidence.
Validation target: Proposal metadata schema includes raw or sanitized run evidence contract.
Validation evidence: Shared validation evidence.

#### RTF3 - Analyzer summary format is required by the runner but not specified enough

Finding ID: RTF3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added a minimal analyzer summary schema with run, usage, tool output, signals, and verdict fields.
Rationale: Release metadata and validator logic need stable per-run analyzer summary fields.
Validation target: Proposal defines required analyzer summary fields.
Validation evidence: Shared validation evidence.

#### RTF4 - Benchmark-relevant change detection needs a release-owner decision surface

Finding ID: RTF4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added RC reuse metadata with `checked_by`, `checked_surface`, and rationale fields, plus a rerun-or-waiver rule when benchmark-relevant changes occurred.
Rationale: RC reuse is a release decision and should be attributable.
Validation target: Proposal requires release-owner decision metadata for RC reuse.
Validation evidence: Shared validation evidence.

#### RTF5 - First implementation may be too large without milestone boundaries

Finding ID: RTF5
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: plan
Chosen action: Added milestone slicing guidance for the follow-on execution plan.
Rationale: The proposal is coherent but the first implementation touches enough surfaces to require reviewable milestones.
Validation target: Proposal rollout guidance lists milestone boundaries.
Validation evidence: Shared validation evidence.

#### RTF6 - "Hard warning" phrasing may confuse release gates

Finding ID: RTF6
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Replaced `hard warning` wording with `high-warning` and distinguished warnings from blockers.
Rationale: Severity terms should not imply that warning-only token thresholds block the first slice.
Validation target: Proposal warning thresholds use `warning`, `high-warning`, and `blocker` consistently.
Validation evidence: Shared validation evidence.

### plan-review-r1

#### RTF-PLR1 - Release validation integration is split across M1 and M5

Finding ID: RTF-PLR1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Revised M1 to remove `scripts/validate-release.py`, `scripts/release-verify.sh`, release-level delegation, and release-level validation commands. M1 now focuses on `scripts/validate-token-cost-report.py`, parser behavior, schema checks, waiver/incomplete/baseline cases, evidence reference checks, and standalone validator tests. M5 remains the release validation integration milestone.
Rationale: The current plan assigns `scripts/validate-release.py`, `scripts/release-verify.sh`, release-level delegation, and release-level validation commands to both M1 and M5, which makes implementation sequencing and test-spec mapping ambiguous.
Validation target: Revised plan has non-overlapping M1/M5 ownership and remains ready for a plan-review rerun before test-spec.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`; `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/plan-review-r1.md`; `git diff --check -- docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`

### plan-review-r2

No material findings.

### code-review-r1

#### RTF-CR1 - RC reuse metadata is not validated

Finding ID: RTF-CR1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement M1
Chosen action: Added standalone validator coverage for `rc_reuse` metadata when final metadata waives based on RC benchmark evidence. Added passing and failing tests for missing `rc_reuse`, required fields, checked-surface rationale, and benchmark-relevant-change true/false cases.
Rationale: The approved spec and test spec require RC reuse metadata to make benchmark-relevant-change decisions attributable and testable.
Validation target: Validator rejects RC-based final waiver metadata without required `rc_reuse` fields and accepts valid true/false RC reuse fixtures.
Validation evidence: `python scripts/test-token-cost-report-validation.py`; `python scripts/validate-token-cost-report.py tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml`; `python -m py_compile scripts/validate-token-cost-report.py`; `python scripts/test-token-cost-measurement.py`; `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md`

#### RTF-CR2 - Markdown report link/name requirement is not validated

Finding ID: RTF-CR2
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement M1
Chosen action: Updated the validator to read `report.report_markdown` and require the Markdown report to name or link the expected YAML metadata file. Added a negative test where Markdown exists but omits the YAML metadata reference.
Rationale: The approved spec requires Markdown human evidence and YAML gate metadata to be visibly paired.
Validation target: Validator rejects metadata whose `report.report_markdown` points to Markdown that does not name or link the YAML metadata file.
Validation evidence: Shared code-review R1 resolution validation evidence.

### code-review-r3

No material findings.

### code-review-r4

No material findings.

### code-review-r5

#### RTF-CR4 - Analyzer summaries written by the runner preserve absolute local JSONL paths

Finding ID: RTF-CR4
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement M3
Chosen action: Convert analyzer summary `run.jsonl` to a repo-relative path when the JSONL path is under the repository root, and add focused runner/analyzer coverage that rejects absolute repository paths in durable summaries.
Rationale: Release evidence must be stable and must not persist maintainer-local absolute paths.
Validation target: Runner-produced analyzer summaries under `docs/reports/token-cost/runs/<release>/` use repo-relative `run.jsonl` values.
Validation evidence: `python scripts/test-token-cost-measurement.py`; `python -m py_compile scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py`; `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl`; `python scripts/test-token-cost-report-validation.py`; `git diff --check -- scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py scripts/test-token-cost-measurement.py tests/fixtures/token-cost docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md`

#### RTF-CR5 - Repeated same-file read signal misses repeated capped reads

Finding ID: RTF-CR5
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement M3
Chosen action: Count repeated file-read-like commands by path independently from confirmed full-file events, and add focused coverage for repeated capped reads of the same file.
Rationale: Repeated same-file reads are a runtime cost signal even when each individual read is capped.
Validation target: Analyzer summaries report a non-zero repeated-read signal when the same file is read repeatedly below full-file thresholds.
Validation evidence: Shared code-review R5 resolution validation evidence.

#### RTF-CR6 - Full-file-read classification cannot represent justified reads

Finding ID: RTF-CR6
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement M3
Chosen action: Add analyzer support for justified full-file/generated-output read classification when justification metadata is provided, and add focused tests for the `justified` classification.
Rationale: The spec and test spec require `justified` as part of the full-file-read classification contract.
Validation target: Analyzer summary can emit `full_file_read.result: justified` for explicitly justified reads.
Validation evidence: Shared code-review R5 resolution validation evidence.

### code-review-r6

No material findings.

### code-review-r7

#### RTF-CR7 - Analyzer summaries miss current Codex command output events

Finding ID: RTF-CR7
Disposition: accepted
Status: open
Owner: implementer
Owning stage: implement M4
Chosen action: Update the analyzer to recognize current Codex command execution events that carry command output in `aggregated_output`, add focused analyzer coverage for that event shape, and regenerate the M4 sanitized summaries plus Markdown/YAML report values from corrected analyzer evidence.
Rationale: The first baseline report must measure command-output amplification from Codex JSONL analyzer evidence. If the analyzer treats current command execution events as unknown records, release evidence can incorrectly report zero command output.
Validation target: Analyzer tests cover `item.completed` `command_execution` events with `aggregated_output`, and the `v0.1.1` analyzer summaries plus report no longer under-report command-output amplification from current Codex JSONL.
Validation evidence: Pending M4 review-resolution implementation.

### code-review-r2

#### RTF-CR3 - RC reuse surface coverage accepts an incomplete checked-surface rationale

Finding ID: RTF-CR3
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement M1
Chosen action: Update `scripts/validate-token-cost-report.py` so `benchmark_relevant_changes_since_rc: false` requires all R22c benchmark-relevant surface categories to be addressed across `rc_reuse.checked_surface` and `rc_reuse.rationale`.
Rationale: A final-release RC reuse decision must be reviewable. Mentioning only one surface does not prove the release owner checked public skills, adapter output, workflow guide, benchmark prompts, analyzer, fixture, model/tool version, and release packaging.
Validation target: Validator should reject partial RC reuse checked-surface rationale and accept rationale covering all R22c surface categories.
Validation evidence: `python scripts/test-token-cost-report-validation.py`; `python scripts/validate-token-cost-report.py tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml`; `python -m py_compile scripts/validate-token-cost-report.py`; `python scripts/test-token-cost-measurement.py`; `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md`

## Shared Validation Evidence

| Validation area | Result | Notes |
|---|---|---|
| Proposal and review formatting | pass | `git diff --check -- docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills` |
| Review artifact closeout | pass | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills` |
| Change metadata | pass | `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml` |

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action or stop state.
- [x] Every rejected finding has rationale.
- [x] Every deferred finding has follow-up or explicit no-follow-up rationale.
- [x] Every `needs-decision` finding is resolved or blocks closeout.
- [x] Validation evidence is recorded for spec-review findings.
- [x] Validation evidence is recorded for plan-review findings.
- [x] Validation evidence is recorded for code-review findings.
- [ ] Closeout status is correct.
