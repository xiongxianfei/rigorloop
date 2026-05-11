# Code Review R7

Review ID: code-review-r7
Stage: code-review
Round: 7
Reviewer: Codex code-review
Target: M4 first baseline report and release report template
Status: changes-requested
Date: 2026-05-11

## Review Inputs

- Diff range: `d9b5024..f5471f1`
- Review surface: M4 baseline report, release metadata, sanitized analyzer summaries, release-notes link, runner command change, focused runner test, and lifecycle handoff state.
- Tracked governing branch state: approved spec, test spec, architecture package, active plan, review log, review resolution, and prior code-review records are present in tracked Git state.
- Spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Test spec: `specs/release-token-friendliness-benchmark-for-skills.test.md`
- Plan milestone: `docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md`, M4.
- Architecture: `docs/architecture/system/architecture.md`
- Prior review: `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/code-review-r6.md`
- Validation evidence recorded in the active plan and change metadata.
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Diff Summary

M4 adds the first `v0.1.1` Token-Friendliness Markdown report and YAML metadata, adds seven sanitized per-run analyzer summaries under `docs/reports/token-cost/runs/v0.1.1/`, links the report from the `v0.1.1` release notes, and records the implementation handoff in the active plan and change metadata. The runner is also updated to invoke `codex exec --json --ephemeral --skip-git-repo-check` so live benchmarks can run from disposable temp fixtures outside a trusted Git worktree, with focused test coverage for the printed command.

## Findings

### RTF-CR7 - Analyzer summaries miss current Codex command output events

Finding ID: RTF-CR7
Severity: major

Evidence:

- `scripts/analyze-codex-jsonl.py:106`-`114` extracts command output only from keys named `output`, `stdout`, `stderr`, `content`, or `text`.
- Current Codex `command_execution` JSONL events can carry command output as `aggregated_output` under an `item.completed` event. Focused review proof with an event shaped as `{"type":"item.completed","item":{"type":"command_execution","command":"sed -n '1,220p' /tmp/example/SKILL.md","aggregated_output":"alpha\nbeta\n"}}` produced `tool_calls: 0`, `command_output_lines: 0`, `estimated_command_output_tokens: 0`, and `unknown_records: 1`.
- The M4 baseline analyzer summaries report zero tool output for every run, for example `docs/reports/token-cost/runs/v0.1.1/proposal-short-run1.analysis.yaml:17`-`24` records `total_estimated_tokens: 0`, `kind: none`, `lines: 0`, and `estimated_tokens: 0`.
- The human report repeats that zero-output conclusion for all benchmarks at `docs/reports/token-cost/releases/v0.1.1.md:41`-`51`.
- The spec requires command-output amplification to be measured from Codex JSONL analyzer evidence in the first implementation (`R17`) and requires reports to identify the largest command or output source, line count, and estimated tokens (`R17a`).

Problem:

The baseline report depends on analyzer summaries that do not parse the current Codex command-output field. This makes the durable release evidence under-report command-output amplification and can incorrectly claim that no command output was observed.

Required outcome:

Analyzer summaries used by the M4 baseline must account for current Codex `command_execution` output fields, including `aggregated_output`, before the report can be accepted as release evidence.

Safe resolution:

Update `scripts/analyze-codex-jsonl.py` to recognize current Codex command execution events and `aggregated_output`, add focused analyzer test coverage for that JSONL shape, rerun the `v0.1.1` benchmark analysis or regenerate the sanitized summaries from a corrected run, and update `docs/reports/token-cost/releases/v0.1.1.md` plus `v0.1.1.yaml` so command-output amplification reflects corrected analyzer evidence.

## Checklist Coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | concern | RTF-CR7 leaves `R17`/`R17a` command-output amplification evidence unreliable. |
| Test coverage | concern | Existing analyzer tests cover older `output`/`result.output` fixture shapes but not current Codex `item.completed` `command_execution` events with `aggregated_output`. |
| Edge cases | concern | Current Codex JSONL event shape is a named release-run evidence path and is not parsed for command-output amplification. |
| Error handling | pass | Runner temp fixture execution now uses `--skip-git-repo-check` and M4 validation records the initial failure and corrected command. |
| Architecture boundaries | pass | Changes stay inside M4 report evidence, runner command behavior, tests, and lifecycle state; no release-level validation integration was added. |
| Compatibility | concern | Existing analyzer text output remains callable, but current Codex JSONL compatibility is incomplete for command output. |
| Security/privacy | pass | Raw JSONL is omitted and tracked summaries contain no local temp paths. |
| Derived artifact currency | pass | No generated adapter output or repository-local `.codex/skills/` content was edited. |
| Unrelated changes | pass | The reviewed diff is scoped to M4 and the same-slice runner command fix needed to execute the benchmark from temp fixtures. |
| Validation evidence | concern | Recorded validation passed, but it does not prove current Codex `aggregated_output` command-output parsing. |

## No-Finding Rationale

Not applicable. A material finding was found.

## Residual Risks

- The raw JSONL was intentionally omitted for privacy, so corrected M4 evidence should rely on regenerated sanitized analyzer summaries after the analyzer can parse the current event shape.

## Recommended Next Stage

Enter `review-resolution` for RTF-CR7, then return fixes to `implement M4`.
