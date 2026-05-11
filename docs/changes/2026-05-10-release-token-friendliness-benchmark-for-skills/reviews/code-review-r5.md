# Code Review R5

Review ID: code-review-r5
Stage: code-review
Round: 5
Reviewer: Codex code-review
Target: M3 runner and analyzer-summary integration
Status: changes-requested
Date: 2026-05-11

## Review Inputs

- Diff range: `eecfaad..9cf7002`
- Review surface: M3 benchmark runner, analyzer summary output, focused runner/analyzer tests, and lifecycle handoff state.
- Tracked governing branch state: approved spec, test spec, architecture package, active plan, review log, review resolution, and prior code-review records are present in tracked Git state.
- Spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Test spec: `specs/release-token-friendliness-benchmark-for-skills.test.md`
- Plan milestone: `docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md`, M3.
- Architecture: `docs/architecture/system/architecture.md`
- Prior review: `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/code-review-r4.md`
- Validation evidence recorded in the active plan and change metadata.
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Diff Summary

M3 adds `scripts/run-token-cost-benchmarks.py`, extends `scripts/analyze-codex-jsonl.py` with schema version 1 analyzer summaries, and adds focused tests in `scripts/test-token-cost-measurement.py`. The runner reads the tracked benchmark manifest, copies the minimal public fixture into a temp directory, installs public Codex skills from `dist/adapters/codex/.agents/skills/`, supports dry-run execution, writes JSONL and analyzer summaries, and avoids Markdown report generation. The analyzer now writes run identity, usage, tool-output, signal, full-file-read, and verdict sections.

## Findings

### RTF-CR4 - Analyzer summaries written by the runner preserve absolute local JSONL paths

Finding ID: RTF-CR4
Severity: major

Evidence:

- `scripts/run-token-cost-benchmarks.py:227`-`229` resolves the default output directory to an absolute repository path.
- `scripts/run-token-cost-benchmarks.py:172` creates each JSONL path from that absolute output directory.
- `scripts/run-token-cost-benchmarks.py:144`-`153` passes the absolute JSONL path to the analyzer.
- `scripts/analyze-codex-jsonl.py:326` writes `str(jsonl_path)` into `run.jsonl` when raw JSONL is tracked.
- Focused review proof produced `run.jsonl: /home/xiongxianfei/data/20260419-rigorloop/docs/reports/token-cost/runs/review-check/proposal-short-run1.jsonl` in a runner-generated analyzer summary.

Problem:

Durable release evidence should use stable repo-relative paths for tracked run artifacts. Writing an absolute maintainer-local path into a tracked analyzer summary makes the summary machine-local and conflicts with the release evidence/privacy contract.

Required outcome:

Runner-produced analyzer summaries for repository output paths must record repo-relative JSONL evidence paths such as `docs/reports/token-cost/runs/<release>/<benchmark>-run1.jsonl`, not absolute local paths.

Safe resolution:

Convert analyzer summary `run.jsonl` to a repo-relative path when the JSONL path is under the repository root, and add a test that runs the runner with an output directory under `docs/reports/token-cost/runs/<release>/` or another repo-relative output path and asserts the summary does not contain an absolute repository path.

### RTF-CR5 - Repeated same-file read signal misses repeated capped reads

Finding ID: RTF-CR5
Severity: major

Evidence:

- `scripts/analyze-codex-jsonl.py:232`-`238` only counts repeated reads when `is_full_file_read_event(event)` is true.
- `scripts/analyze-codex-jsonl.py:213`-`216` requires a full-file-style command to produce more than 80 lines or at least 8,000 estimated tokens before it is considered a full-file read event.
- Focused review proof with three reads of `docs/workflows.md` using `sed -n '1,20p'` produced `repeated_file_read_count: 0`.
- The test spec names repeated same-file reads as part of T13 signal coverage, and the spec requires analyzer evidence to consider repeated same-file reads under R18a.

Problem:

Repeated same-file reads are a cost signal even when each individual read is capped or below the full-file threshold. By tying repeated-read counting to confirmed full-file events, the analyzer suppresses the repeated-read signal that the report is supposed to expose.

Required outcome:

The analyzer must count repeated reads of the same file independently from confirmed full-file classification. The signal should identify repeated file-read-like commands that touch the same path repeatedly, while still avoiding path-list false positives.

Safe resolution:

Change repeated read detection to count file-read-like events by `command_path` separately from `is_full_file_read_event`, using the spec/test threshold for repeated reads, and add a focused test with repeated capped reads of the same file that expects `repeated_file_read_count` to be non-zero.

### RTF-CR6 - Full-file-read classification cannot represent justified reads

Finding ID: RTF-CR6
Severity: major

Evidence:

- `specs/release-token-friendliness-benchmark-for-skills.md` R18b requires full-file read classification to use `none`, `suspected`, `confirmed`, or `justified`.
- `specs/release-token-friendliness-benchmark-for-skills.md` R18d requires analyzer and validator behavior to avoid false positives for explicitly requested whole-file review targets and justified generated-output validation.
- `specs/release-token-friendliness-benchmark-for-skills.test.md` T13 requires confirmed/suspected/justified/none classification and justified whole-file target metadata when available.
- `scripts/analyze-codex-jsonl.py:275`-`285` only returns `confirmed`, `suspected`, or `none`, and the analyzer CLI has no option or metadata path to mark a whole-file read or generated-output read as justified.

Problem:

The analyzer summary schema has no way to produce the `justified` classification required by the spec and test spec. This leaves justified whole-file reads indistinguishable from ordinary confirmed or suspected reads in release evidence.

Required outcome:

Analyzer summary output must be able to classify a read as `justified` when the benchmark or analyzer invocation records that the whole-file read or generated-output read was explicitly justified.

Safe resolution:

Add a small analyzer option or structured argument for justified paths or justified full-file-read reason, emit `full_file_read.result: justified` when it applies, include the justification in summary evidence if the schema supports it, and add focused tests for justified whole-file/generated-output validation.

## Checklist Coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | concern | RTF-CR4 conflicts with stable release evidence expectations; RTF-CR5 and RTF-CR6 leave R18/T13 signal requirements incomplete. |
| Test coverage | concern | Tests cover dry-run runner behavior and basic analyzer summaries, but do not catch absolute summary paths, repeated capped reads, or justified full-file classifications. |
| Edge cases | concern | Repeated same-file reads and justified whole-file/generated-output reads are named edge cases that are not fully handled. |
| Error handling | pass | Runner rejects `.codex/skills/`, rejects in-repo temp roots, deletes temp dirs by default, and preserves failed temp only when configured. |
| Architecture boundaries | pass | Changes stay inside M3 runner/analyzer/test scope and do not add report generation or release validation integration. |
| Compatibility | pass | Existing analyzer text output remains available and existing token-cost report validation tests pass. |
| Security/privacy | concern | Analyzer summaries can persist maintainer-local absolute paths in release evidence. |
| Derived artifact currency | pass | No generated adapter output or repository-local `.codex/skills/` content was edited. |
| Unrelated changes | pass | The reviewed diff is scoped to M3 implementation and required lifecycle state updates. |
| Validation evidence | concern | Recorded validation passes, but the missing edge coverage means the validation set is not sufficient for M3 closeout. |

## No-Finding Rationale

Not applicable. Material findings were found.

## Residual Risks

- Live Codex execution was not required for M3 validation by design; dry-run coverage is appropriate, but the summary and signal contracts must be corrected before M3 can close.

## Recommended Next Stage

Enter `review-resolution` for RTF-CR4, RTF-CR5, and RTF-CR6, then return fixes to `implement M3`.
