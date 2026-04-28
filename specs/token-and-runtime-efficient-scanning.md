# Token and Runtime Efficient Scanning

## Status

- approved

## Related proposal

- [Token and Runtime Efficient Scanning](../docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md)

## Goal and context

This spec defines the contributor-visible and agent-visible behavior for reducing token volume and repeated scan runtime while preserving RigorLoop's reviewability, traceability, and validation guarantees.

The first reviewable slice covers bounded evidence extraction guidance, normal-mode output budgets with verbose expansion, one named script output-shaping improvement for generated adapter drift checks, manifest-first generated-output inspection, and full-file-read escalation guidance for scan-sensitive skills.

## Glossary

- bounded extraction: collecting only the smallest reliable evidence needed for the task before broadening to larger ranges or full files.
- normal-mode output: default command output when no verbose, debug, or full-detail flag is requested.
- verbose output: explicit expanded command output requested through `--verbose` or an equivalent documented flag.
- routine command output: normal success or failure output from a repository-owned command, excluding externally hosted CI logs and intentionally verbose reruns.
- single excerpt: one contiguous block of source, diff, generated output, or log text shown as evidence.
- output budget: a normal-mode target for output length that guides command and skill behavior without changing validation correctness.
- warning threshold: a normal-mode output size above which a command should make over-budget output visible without changing the validation result.
- summary-first output: output that starts with status, check identity, affected scope, and counts before detailed records.
- failure-focused output: output that emphasizes failing, changed, or explicitly requested records rather than unchanged records.
- diff-focused output: output that reports missing, stale, unexpected, or changed generated files rather than every generated file.
- adapter drift failure category: one of `missing`, `stale`, `unexpected`, `canonical-source-error`, or `manifest-error` when applicable.
- stable ID: a durable identifier for a requirement, check, finding type, or generated-output category that can be cited without pasting long prose.
- manifest-first generated-output scan: generated-output inspection that uses the manifest as the primary inventory before confirming filesystem presence, content, or drift.
- full-file read escalation: a documented condition where a full file read is required because bounded extraction is not enough to support the conclusion.
- scan-sensitive skill: a canonical skill under `skills/` that instructs agents to inspect repository files, review artifacts, validation output, generated output, or command output. The first-slice scan-sensitive skills are `architecture`, `architecture-review`, `bugfix`, `ci`, `code-review`, `explain-change`, `implement`, `plan`, `plan-review`, `pr`, `project-map`, `proposal`, `proposal-review`, `research`, `spec`, `spec-review`, `test-spec`, `verify`, and `workflow`.
- shared parser helper: an in-process helper that reads and parses a file or manifest once so multiple checks can reuse the parsed representation.
- persistent cache: stored scan or parse state reused across separate command invocations.
- first output-shaped script: `python scripts/build-adapters.py --version <version> --check`.

## Examples first

### Example E1: clean adapter drift check stays concise

Given generated public adapter output is in sync with canonical sources
When a contributor runs `python scripts/build-adapters.py --version 0.1.1 --check`
Then the command exits `0`
And normal-mode output reports a concise `adapters.drift` success summary
And normal-mode output does not list every unchanged generated adapter file.

### Example E2: adapter drift failure is summarized before details

Given generated adapter output has 40 stale files, 4 missing files, and 2 unexpected files
When a contributor runs `python scripts/build-adapters.py --version 0.1.1 --check`
Then the command exits with the same failure status as the pre-change drift check
And normal-mode output starts with `adapters.drift`, version, output root, and counts by failure category
And normal-mode output shows affected paths for displayed failures
And normal-mode output tells the contributor how to request complete detail.

### Example E3: verbose adapter drift output preserves complete detail

Given generated adapter output has more drift entries than normal-mode output shows
When a contributor runs `python scripts/build-adapters.py --version 0.1.1 --check --verbose`
Then the command exits with the same status as normal check mode
And verbose output includes every collected failure entry for the invocation
And verbose output remains deterministic.

### Example E4: generated-output inspection reads the manifest first

Given an agent needs to understand generated adapter package coverage
When `dist/adapters/manifest.yaml` exists
Then the agent or repository-owned script uses the manifest as the first inventory of skills, adapters, command aliases, and version
And filesystem traversal is used afterward to confirm missing, stale, extra, or drifted files.

### Example E5: bounded extraction escalates to a full-file read

Given a spec change depends on how requirements, edge cases, non-goals, and acceptance criteria interact across the whole spec
When targeted heading reads cannot prove the relationship safely
Then the agent reads the full spec
And the agent records or reports why bounded extraction was insufficient when the conclusion matters for review.

### Example E6: scan-sensitive skill guidance uses stable IDs

Given a skill instructs an agent to review validation evidence
When the skill is updated for this behavior
Then it directs the agent to prefer check IDs, requirement IDs, file paths, counts, and exact line citations before large excerpts
And it includes guidance for when a full-file read is required.

## Requirements

R1. Repository guidance MUST define bounded extraction as the default first evidence-collection behavior for large files, repeated scans, generated output, and validation logs.

R2. Bounded extraction guidance MUST direct contributors and agents to start with inventories, headings, stable IDs, path lists, counts, or matching line numbers before reading broad file content.

R3. Bounded extraction guidance MUST direct contributors and agents to read exact ranges after locating relevant lines, then broaden to neighboring sections or full files only when needed.

R4. Bounded extraction guidance MUST require full-file read escalation when:
- the file itself is the review target;
- the relevant section cannot be isolated safely;
- surrounding context can change the conclusion;
- bounded searches disagree or produce incomplete evidence;
- a behavior-changing edit depends on understanding the whole source-of-truth artifact.

R5. Scan-sensitive skills MUST prefer summary and stable ID based reasoning before raw excerpts.

R6. Scan-sensitive skills MUST include explicit guidance for when a full-file read is required.

R7. Repository-owned normal-mode command output affected by this spec MUST be summary-first, failure-focused, diff-focused where applicable, and expandable with `--verbose` or an equivalent documented escape hatch.

R8. Repository-owned normal-mode command output affected by this spec SHOULD target no more than 40 lines for routine command output.

R9. Repository-owned normal-mode command output affected by this spec MUST emit an over-budget warning when routine command output exceeds 80 lines.

R10. A single normal-mode excerpt SHOULD target no more than 12 lines.

R11. A single normal-mode excerpt MUST emit an over-budget warning when it exceeds 20 lines.

R12. Multi-file normal-mode summaries MUST show no more than one summary line per file by default unless the file is changed, failing, or explicitly requested.

R13. Normal-mode output MUST NOT print every parsed field, every unchanged file, large excerpts, or repeated path lists in multiple sections by default.

R14. Output budgets and warning thresholds MUST NOT change validation semantics, selected check coverage, or command exit behavior.

R15. When normal-mode output omits detail because of output shaping or budgets, it MUST state how to request the omitted detail.

R16. The first output-shaped script MUST be:

```text
python scripts/build-adapters.py --version <version> --check
```

R17. The first output-shaped script MUST support an explicit verbose form:

```text
python scripts/build-adapters.py --version <version> --check --verbose
```

R18. The first output-shaped script MUST keep the existing clean-check success semantics: generated adapter output in sync exits `0`.

R19. The first output-shaped script MUST keep the existing drift failure semantics: missing, stale, unexpected, or invalid canonical source input still fails check mode.

R19a. The first output-shaped script MUST classify every collected failure entry into exactly one of:
- `missing`;
- `stale`;
- `unexpected`;
- `canonical-source-error`;
- `manifest-error`.

R19b. The `missing`, `stale`, and `unexpected` failure categories MUST apply to generated output state.

R19c. The `canonical-source-error` failure category MUST apply when a canonical source artifact needed for generation is invalid, incomplete, or unparsable.

R19d. The `manifest-error` failure category MUST apply when the generated adapter manifest is missing, malformed, inconsistent, or does not match the expected generated-output contract.

R20. The first output-shaped script MUST keep its command exit codes equivalent to the pre-output-shaping behavior for success, drift failure, and invalid input.

R21. Clean normal-mode output for the first output-shaped script MUST include:
- check ID `adapters.drift`;
- requested adapter manifest version;
- generated adapter output root;
- a concise success status.

R22. Drift failure normal-mode output for the first output-shaped script MUST include:
- check ID `adapters.drift`;
- requested adapter manifest version;
- generated adapter output root;
- counts by failure category;
- failure category and affected paths for displayed failures;
- actionable failure detail for displayed failures;
- a verbose rerun instruction when undisplayed failures exist.

R23. Drift failure normal-mode output for the first output-shaped script MUST avoid listing every failure entry when doing so would exceed normal-mode budgets.

R24. Verbose output for the first output-shaped script MUST include every collected failure entry for the invocation, including generated-output, canonical-source, and manifest failures.

R25. Verbose output for the first output-shaped script MUST remain deterministic for the same repository state and command arguments.

R26. The first output-shaped script's tests or verification evidence MUST record before-and-after normal output line counts or byte counts for at least one representative clean case and one representative drift failure case.

R27. Generated-output scans that inspect adapter package coverage MUST read `dist/adapters/manifest.yaml` first when it exists.

R28. Generated-output scans that read the manifest first MUST still check the filesystem second when proving missing, stale, unexpected, or drifted generated files.

R29. Manifest-first behavior MUST NOT make `dist/adapters/manifest.yaml` an authored source of truth; canonical skill sources, adapter templates, and generator code remain authoritative for generated adapter output.

R30. Shared parser helpers MAY be introduced in the first slice only when they are needed for the selected script family.

R31. Shared parser helpers introduced under this spec MUST be in-process helpers rather than persistent cross-command caches.

R32. Persistent cache behavior MUST NOT be introduced under this first spec.

R33. If future work introduces persistent cache behavior, that work MUST update or supersede this spec before implementation.

R34. The change MUST update contributor-visible workflow guidance when the new behavior affects how contributors or agents collect evidence.

R35. The change MUST update canonical skill guidance for every first-slice scan-sensitive skill named in this spec.

R36. Generated `.codex/skills/` and public adapter package output MUST be refreshed only through existing generation commands when canonical skill guidance changes.

R37. The implementation MUST NOT add a new external dependency for output shaping, manifest-first scanning, or bounded extraction guidance.

## Inputs and outputs

Inputs:

- contributor or agent requests that require reading large files, generated output, validation output, or repeated evidence from the same file;
- command arguments for repository-owned scripts, including `--check`, `--version`, and `--verbose` where supported;
- generated adapter manifest data under `dist/adapters/manifest.yaml`;
- canonical skill sources and adapter templates used to render generated adapter output;
- changed paths, failing paths, failure categories, and check IDs produced by repository-owned validation.

Outputs:

- updated workflow and skill guidance for bounded extraction, stable ID reasoning, and full-file read escalation;
- normal-mode command output shaped around status, check ID, counts, affected paths, and actionable failures;
- verbose command output that exposes complete diagnostic detail;
- validation evidence that records before-and-after output size for the selected first script;
- unchanged validation results, selected check coverage, and exit behavior.

## State and invariants

- Canonical authored workflow content remains under `docs/`, `specs/`, `skills/`, `schemas/`, and `scripts/`.
- Generated `.codex/skills/` and `dist/adapters/` output remains derived output.
- Output shaping never changes whether a validation check passes or fails.
- Normal-mode brevity never removes the ability to obtain complete diagnostic detail.
- Manifest-first generated-output inspection never treats the manifest as more authoritative than canonical sources.
- Persistent cache state is not part of the first-slice behavior.

## Error and boundary behavior

- Invalid command arguments MUST continue to fail with a non-zero exit status and a clear error message.
- `--verbose` on the first output-shaped script MUST be accepted only for command forms where verbose detail is meaningful.
- If normal-mode output exceeds the warning threshold, the command MUST report an over-budget warning and include a verbose expansion path.
- If there are more drift entries than normal mode displays, the command MUST report the omitted count or otherwise make clear that more detail exists.
- If the adapter manifest is missing, malformed, or stale, manifest-first inspection MUST report that condition and continue to use canonical sources and filesystem checks required for drift correctness.
- If output shaping cannot safely preserve actionable failure detail, the command MUST prefer correctness and complete failure evidence over meeting the target output budget.
- If a skill cannot determine whether bounded extraction is sufficient, it MUST escalate to broader context rather than relying on an unsupported conclusion.

## Compatibility and migration

- Existing invocations of `python scripts/build-adapters.py --version <version> --check` remain valid.
- Existing CI, release, and selector check IDs continue to call the same generated adapter drift command.
- Adding `--verbose` is backward-compatible because existing callers do not need to pass it.
- The first slice must not require contributors to install new tools.
- Rollback is possible by restoring prior normal output while keeping validation logic and generated output unchanged.
- Generated adapter output remains deterministic and reproducible from canonical sources.

## Observability

- Normal-mode output for affected commands must expose the check ID, status, affected scope, and failure counts when failures exist.
- Over-budget normal output must identify that it exceeded a threshold and name the verbose expansion path.
- Implementation evidence must include output size measurements for the selected first script before and after output shaping.
- Review, verification, or change-local artifacts should cite stable requirement IDs and commands instead of pasting large logs.

## Security and privacy

- Output shaping MUST NOT expose secrets, credentials, tokens, private keys, or machine-local debug paths.
- Verbose output MUST NOT expose data outside the repository paths that the command already inspects.
- Bounded extraction guidance MUST NOT encourage hiding security-sensitive failures by summarizing away actionable detail.
- No authentication or authorization behavior changes are introduced by this spec.

## Accessibility and UX

This change does not introduce a graphical UI. The command-line experience must remain readable in plain text, and verbose expansion instructions must be explicit enough for contributors and agents to rerun the command without guessing.

## Performance expectations

- The first output-shaped script SHOULD avoid additional full generated-output scans solely to render both summary and verbose views in one invocation.
- The first output-shaped script SHOULD derive normal and verbose output from the same collected drift result where practical.
- Output shaping SHOULD reduce normal-mode output size for multi-file drift failures compared with the pre-change unshaped drift list.
- Shared parser helpers should reduce repeated reads inside a command or validation family, but persistent cross-command caching remains out of scope.

## Edge cases

EC1. Clean generated adapter output produces one concise normal-mode success summary and no unchanged file list.

EC2. One stale generated adapter file appears in normal-mode failure output with check ID, affected path, and actionable detail.

EC3. Many missing, stale, and unexpected generated adapter files produce counts by category and a bounded displayed subset in normal mode.

EC4. Verbose mode for many generated adapter failure entries shows the full deterministic failure list.

EC5. A malformed adapter manifest is reported as a manifest problem while filesystem and canonical-source checks still protect drift correctness.

EC6. A generated-output scan needs package coverage only; it uses the manifest as inventory and avoids filesystem traversal until confirmation is needed.

EC7. A generated-output scan needs drift proof; it uses manifest evidence where useful and still confirms filesystem state.

EC8. A bounded search finds a requirement ID but neighboring sections can change interpretation; the agent escalates to the surrounding section or full file.

EC9. A full-file read is required because the whole artifact is the review target.

EC10. Normal-mode output exceeds the hard warning threshold because every displayed failure is needed for actionable diagnosis; the command reports the over-budget condition and preserves failure detail.

EC11. A script is invoked through `scripts/ci.sh`; output shaping in the child command must not make the wrapper misreport pass/fail status.

EC12. Canonical skill guidance changes; generated `.codex/skills/` and public adapter output are refreshed through existing generation commands rather than hand edits.

EC13. A canonical skill source is invalid; normal output reports `canonical-source-error` with an affected path and actionable detail, and verbose output includes the complete collected failure entry.

EC14. The generated adapter manifest is missing, malformed, inconsistent, or mismatched; normal output reports `manifest-error` with the affected manifest path and actionable detail, and verbose output includes the complete collected failure entry.

## Non-goals

- Weakening required validation, review gates, lifecycle traceability, or generated-output drift checks.
- Changing validation semantics, selected check coverage, or command exit behavior while shaping output.
- Replacing full-file reads when a full contract review requires them.
- Adding a persistent cache, long-running indexing service, database, or heavyweight dependency in the first slice.
- Rewriting unrelated validators or generators solely for performance.
- Changing hosted CI behavior except through existing repository-owned commands consuming shaped output.
- Making output budgets hard correctness failures before a later approved spec explicitly does so.

## Acceptance criteria

- AC1. `docs/workflows.md` or another authoritative workflow surface documents bounded extraction, output budgets, verbose expansion, and full-file-read escalation.
- AC2. Every first-slice scan-sensitive canonical skill named in this spec includes summary or stable ID based reasoning guidance and full-file-read escalation guidance.
- AC3. `python scripts/build-adapters.py --version 0.1.1 --check` supports normal-mode shaped output and preserves existing success and failure exit behavior.
- AC4. `python scripts/build-adapters.py --version 0.1.1 --check --verbose` exposes complete drift details.
- AC5. Tests or verification evidence record before-and-after normal output line counts or byte counts for representative clean and drift cases.
- AC6. Generated-output inspection uses adapter manifest evidence before filesystem confirmation where a manifest exists.
- AC7. The change includes tests proving concise failure output preserves check ID, affected path, and actionable failure detail.
- AC8. The change includes tests proving verbose output preserves complete diagnostic detail.
- AC9. The change includes tests or verification proving selected check coverage and command exit behavior are unchanged.
- AC10. The change includes tests proving generated-output, canonical-source, and manifest failures are classified into the required failure categories.
- AC11. Artifact lifecycle validation passes for the proposal and this spec.

## Open questions

- None.

## Next artifacts

- `spec-review` for ambiguity, completeness, compatibility, and testability review.
- Architecture only if the follow-on design introduces a shared parser boundary that affects multiple validation families.
- Plan after spec review and any required architecture work.
- Test spec before implementation.

## Follow-on artifacts

- [Token and Runtime Efficient Scanning execution plan](../docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md)
- [Token and Runtime Efficient Scanning test spec](token-and-runtime-efficient-scanning.test.md)
- `spec-review`: approved on 2026-04-28 after failure taxonomy and lifecycle-readiness corrections; no material findings remain open.
- `plan-review`: approved on 2026-04-28 after validation command type and manifest-error milestone-boundary revisions.

## Readiness

Spec review is complete and this spec is approved.

Current follow-on artifacts: the linked execution plan and active test spec.
Immediate next repository stage: `implement`.
Implementation readiness: ready to begin against the linked active test spec and execution plan.
