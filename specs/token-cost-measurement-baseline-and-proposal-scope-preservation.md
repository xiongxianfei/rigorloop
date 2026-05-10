# Token Cost Measurement Baseline and Proposal Scope Preservation

## Status

approved

## Related proposal

- [Token Cost Measurement Baseline and Proposal Skill Scope Preservation](../docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md)

## Goal and context

This spec defines the contract for recovering the missing token-cost measurement baseline and preventing future proposals from silently dropping parts of a user's initial request.

The measurement behavior is repository-local and evidence-focused: contributors must be able to measure static skill size, inspect Codex JSONL session cost, identify command-output amplification, rank the largest measured cost drivers, and produce a durable baseline report before making further token-cost optimization decisions.

The proposal behavior is contributor-visible and public-skill-facing: proposal authoring must preserve every initial user goal as in scope, out of scope, deferred follow-up, rejected option, or open question; proposal-review must check that preservation before approving a proposal.

## Glossary

- `initial user goal`: a distinct goal, concern, constraint, requested outcome, or explicit non-goal present in the user's request that starts or materially revises a proposal.
- `scope preservation`: making each initial user goal visible in the proposal with a clear treatment.
- `proposal treatment`: one of `in scope`, `out of scope`, `deferred follow-up`, `rejected option`, or `open question`.
- `silent narrowing`: dropping or materially shrinking an initial user goal without recording where it went.
- `static skill cost`: a local estimate of a skill file's size and token footprint.
- `Codex JSONL session`: an exported Codex session transcript in JSON Lines format.
- `tool-output amplification`: token and context growth caused by tool outputs such as shell commands, searches, validation logs, file reads, or generated-output dumps.
- `baseline report`: a durable Markdown report under `docs/reports/token-cost/` that records comparable token-cost measurements and recommended next actions.
- `warning-only budget`: a threshold that produces report warnings but does not fail CI or block validation by itself.
- `public skill text`: skill instructions shipped to users through local skill mirrors or public adapter packages.

## Examples first

### Example E1: broad request is preserved in a proposal

Given a user asks to measure static skill cost, measure Codex JSONL session cost, identify cost drivers, and optimize proposal-skill scope preservation
When the proposal is drafted
Then the proposal includes `Initial intent preservation`
And each user goal is classified as `in scope`, `out of scope`, `deferred follow-up`, `rejected option`, or `open question`
And proposal-review can see what was kept, removed, deferred, or rejected.

### Example E2: a narrowed proposal is still valid

Given a user asks for token measurement, live command wrapping, and hard CI token-budget gates
When the proposal chooses to measure recorded sessions first and defer live command wrapping and hard gates
Then the proposal records live command wrapping as deferred follow-up or out of scope
And records hard CI token-budget gates as deferred or rejected with rationale
And proposal-review does not fail the proposal solely because it narrowed scope.

### Example E3: proposal-review catches silent narrowing

Given the user's request includes Codex JSONL session analysis
When the proposal has no goal, non-goal, deferred follow-up, rejected option, open question, option, decision-log entry, or next artifact for JSONL analysis
Then proposal-review returns `changes-requested`
And the finding states that an initial goal disappeared.

### Example E4: static skill cost measurement

Given the repository contains canonical skills
When a contributor runs the static skill measurement command
Then the command reports each measured skill path, byte size, line count, estimated token count, and largest sections when section data can be detected
And the command exits successfully unless command input is invalid or a processing error occurs.

### Example E5: Codex JSONL session analysis

Given a Codex JSONL export contains tool calls, command output, and token usage metadata
When a contributor runs the JSONL analyzer
Then the command reports session token usage, command output lines and bytes, estimated command-output tokens, largest outputs, broad searches, full-file reads, high output caps, repeated file reads, and top measured cost drivers.

### Example E6: baseline report is longitudinal

Given the first baseline is produced for this change
When the report is written
Then the primary report path is `docs/reports/token-cost/YYYY-MM-DD-baseline.md`
And change-local artifacts link to the report instead of duplicating it.

## Requirements

R1. The system MUST provide a static skill measurement command for canonical skill files.

R1a. Static skill measurement MUST report, at minimum, path, byte size, line count, estimated token count, and whether the skill is measured successfully.

R1b. Static skill measurement SHOULD report the largest skill sections when Markdown headings can be detected.

R1c. Static skill measurement MUST be dependency-light and runnable with the repository's normal Python environment.

R1d. Static skill measurement MUST warn rather than fail when an estimated token budget threshold is exceeded.

R1e. Static skill measurement MUST NOT require hosted telemetry, external services, or network access.

R2. The system MUST provide a Codex JSONL session analyzer.

R2a. The JSONL analyzer MUST accept a path to a Codex JSONL export.

R2b. The JSONL analyzer MUST report session token usage when usage fields are present.

R2c. The JSONL analyzer MUST report that token usage is unavailable when usage fields are absent instead of failing solely for missing usage metadata.

R2d. The JSONL analyzer MUST report tool calls, command-output lines, command-output bytes, estimated command-output tokens, largest outputs, broad searches, full-file reads, high `max_output_tokens` values, repeated file reads, and top measured cost drivers when those signals are present.

R2e. The JSONL analyzer MUST tolerate unknown JSONL event shapes by skipping or summarizing unknown records with a warning.

R2f. The JSONL analyzer MUST fail with a clear error for a missing file, unreadable file, or malformed JSONL record that prevents safe analysis.

R3. Command-output amplification MUST start inside the Codex JSONL analyzer.

R3a. The first implementation slice MUST NOT require a separate live command wrapper.

R3b. A separate command-output measurement script MAY be added later only if live command wrapping becomes useful for local shell command budgeting, validator output measurement, pre-commit checks, or command wrappers around tools such as `rg`, `sed`, or `git diff`.

R4. Baseline reports MUST be stored under `docs/reports/token-cost/`.

R4a. The first baseline report path SHOULD use `docs/reports/token-cost/YYYY-MM-DD-baseline.md`.

R4b. A baseline report MUST include summary, static skill cost, Codex session cost, tool-output amplification, top cost drivers, comparison to previous report, conclusions, and next actions.

R4c. When no previous report exists, the comparison section MUST state that no previous baseline exists.

R4d. Change-local artifacts MUST link to a baseline report produced by the change instead of duplicating the report body.

R5. Token-cost measurement MUST be warning-only in the first slice.

R5a. Token budget warnings MUST NOT be hard CI gates in the first slice.

R5b. Measurement commands MUST return a successful exit code when the only issue is a warning-only budget threshold.

R5c. Hard token-budget CI gates MAY be proposed later after baseline data exists.

R6. Proposal authoring MUST preserve initial user intent.

R6a. Before drafting or materially revising a proposal, the proposal skill MUST instruct agents to extract the user's initial goals, concerns, constraints, and requested outcomes.

R6b. Every initial user goal MUST be visible in the proposal as one of `in scope`, `out of scope`, `deferred follow-up`, `rejected option`, or `open question`.

R6c. Broad or multi-part proposals MUST include an `Initial intent preservation` section or equivalent table.

R6d. The table, when used, MUST include columns equivalent to `Initial user goal`, `Proposal treatment`, and `Where recorded`.

R6e. A proposal MAY narrow the user's request, but it MUST NOT silently drop any part of it.

R7. Proposal narrowing MUST be recorded in the appropriate proposal surface.

R7a. In-scope goals MUST be recorded in `Goals`, `Recommended direction`, workstream sections, or equivalent proposal sections.

R7b. Out-of-scope goals MUST be recorded in `Non-goals` or equivalent scope-control sections.

R7c. Deferred goals MUST be recorded in `Next artifacts`, `Follow-on artifacts`, a named follow-up, or equivalent downstream planning surface.

R7d. Rejected goals MUST be recorded in `Options considered`, `Decision log`, or equivalent rationale sections.

R7e. Open goals MUST be recorded in `Open questions`.

R8. Proposal-review MUST check scope preservation.

R8a. Proposal-review MUST compare the user's initial request with the proposal.

R8b. Proposal-review MUST return `changes-requested` when any initial user goal disappears.

R8c. Proposal-review MUST return `changes-requested` when a deferred goal has no follow-up.

R8d. Proposal-review MUST return `changes-requested` when a rejected goal has no rationale.

R8e. Proposal-review MUST return `changes-requested` when the proposal narrows scope but does not say why.

R8f. Proposal-review MUST NOT rewrite the proposal as part of the review stage unless the user explicitly asks it to edit.

R9. Public skill wording MUST remain portable.

R9a. Published proposal and proposal-review skill text MUST NOT require downstream users to know this repository's internal source paths, generated mirror paths, adapter paths, selector path constraints, drift-check mechanics, or shared-block implementation mechanics.

R9b. Repository-maintainer validation commands and generated-output procedures MAY remain in internal specs, plans, tests, contributor docs, and change-local evidence.

R10. Static validation MUST cover proposal scope preservation.

R10a. Repository-owned validation MUST check that the proposal skill contains scope-preservation guidance.

R10b. Repository-owned validation MUST check that the proposal skill requires every initial user goal to be classified.

R10c. Repository-owned validation MUST check that proposal-review checks for silent narrowing.

R10d. Repository-owned validation MUST check that proposal-review requests revision when initial goals disappear.

R10e. Static validation MUST use narrow section, phrase, or stable-ID checks rather than broad natural-language scoring.

R11. Generated skill output and public adapters MUST remain deterministic derived output.

R11a. Canonical skill changes MUST be checked against generated local skill output.

R11b. Public adapter output MUST receive adapter drift check and adapter validation when public skill text changes.

R11c. For ordinary pre-release skill wording changes, validation SHOULD use unversioned adapter commands when the repository scripts support them.

R11d. If repository adapter scripts require a version, or if adapter release metadata or manifest versioning is touched, validation MUST use the active planned adapter version and record the version source.

R12. The implementation MUST NOT reopen or relitigate PR #39.

R12a. PR #39 MUST remain treated as a completed bounded-evidence guidance slice.

R12b. This change MUST recover the missing measurement baseline and scope-preservation guardrail as new work.

## Inputs and outputs

Inputs:

- accepted proposal for token cost measurement baseline and proposal scope preservation;
- canonical skill files;
- optional Codex JSONL export files supplied by contributors;
- proposal and proposal-review skill text;
- validation scripts and generated-output checks;
- existing change-local artifacts and report links.

Outputs:

- static skill measurement command output;
- Codex JSONL analysis command output;
- token-cost baseline report under `docs/reports/token-cost/`;
- updated proposal and proposal-review skill behavior;
- static validation covering proposal scope preservation;
- regenerated or checked generated skill output and public adapters when canonical skills change;
- change-local links to any produced baseline report.

## State and invariants

- A proposal may narrow scope, but every removed idea must be visible as out of scope, rejected, deferred, or open.
- Proposal resolves uncertainty; architecture records accepted design; ADR records durable decisions.
- Token-cost measurement is evidence for optimization decisions, not a substitute for required validation or review.
- Measurement thresholds are warning-only in the first slice.
- Baseline reports are longitudinal artifacts under `docs/reports/token-cost/`.
- Change-local artifacts link to baseline reports rather than duplicating them.
- Public skill text remains project-portable.
- Generated skill mirrors and public adapter packages remain derived output.

## Error and boundary behavior

- If a proposal lacks enough user context to identify initial goals, proposal authoring MUST record the missing context as an open question or stop for clarification.
- If a user's initial request is extremely broad, proposal authoring MAY group closely related goals, but the grouping MUST preserve the user's distinct requested outcomes.
- If JSONL usage metadata is absent, the analyzer MUST still report available tool-output amplification signals.
- If JSONL parsing fails, the analyzer MUST identify the failing line or record when available.
- If no command-output events are found, the analyzer MUST report zero observed command-output amplification rather than inventing a cost driver.
- If no canonical skills are found, static skill measurement MUST fail with a clear error.
- If adapter validation requires a version, the plan or change evidence MUST identify the version source.

## Compatibility and migration

- Existing proposals remain valid historical artifacts unless they are substantively revised after this spec is approved.
- Existing historical learn records and PR #39 artifacts do not need migration.
- New and substantively revised broad proposals after implementation must follow scope preservation.
- Existing generated outputs must be regenerated or checked only when canonical skill text changes.
- Rollback may revert the spec, tests, skill text, generated-output changes, and measurement scripts together because no runtime data migration is involved.

## Observability

- Measurement commands MUST print human-readable summaries suitable for review evidence.
- Measurement commands SHOULD support machine-readable output only if the implementation can keep it lightweight.
- Baseline reports MUST include enough context to compare later reports, including benchmark source, repository state, and top cost drivers.
- Validation failures MUST identify the missing scope-preservation or adapter validation condition.
- Review and verify artifacts MUST cite the exact commands run.

## Security and privacy

- Measurement commands MUST NOT require network access or hosted telemetry.
- Measurement commands MUST NOT intentionally collect secrets, credentials, private keys, or private user data.
- JSONL reports SHOULD summarize command content when full command output would expose sensitive or excessive data.
- Baseline reports MUST avoid embedding unnecessary raw transcript content.
- Public skill text MUST NOT expose repository-maintainer-only internal paths or release mechanics.

## Accessibility and UX

No UI behavior is in scope.

## Performance expectations

- Static skill measurement SHOULD complete within a few seconds for the current repository's canonical skill set on a typical contributor machine.
- Codex JSONL analysis SHOULD stream or process records incrementally so large session exports do not require loading the entire file into memory.
- Measurement estimates MAY be approximate, but the report MUST label them as estimates.

## Edge cases

1. A user request includes an explicit non-goal. The proposal must preserve it as out of scope, rejected, or another visible treatment.
2. A user request contains overlapping goals. The proposal may group them if the grouped row still preserves the distinct outcomes.
3. A proposal intentionally defers a goal. The deferred goal must have a named follow-up or downstream artifact surface.
4. A proposal rejects a goal. The rejection must include rationale.
5. A JSONL export lacks token usage metadata. The analyzer still reports tool-output amplification and states token usage is unavailable.
6. A JSONL export contains malformed JSON. The analyzer fails clearly instead of producing partial misleading output.
7. A command output is extremely large. The analyzer ranks it as a top cost driver without embedding the full output in the report.
8. No previous baseline exists. The report comparison section states that this is the first baseline.
9. Adapter scripts require a version. Validation uses the active planned version and records the version source.
10. A downstream project uses different architecture or docs paths. Public skill wording stays project-portable and does not require RigorLoop internal paths.

## Non-goals

- Do not reopen PR #39.
- Do not add hosted telemetry infrastructure.
- Do not add hard token-budget CI gates in the first slice.
- Do not add a live command wrapper in the first slice.
- Do not rewrite all skills.
- Do not make proposal-review responsible for editing proposals directly.
- Do not replace required validation, review, or workflow gates with token-cost measurement.
- Do not require downstream public skill users to know this repository's internal generated-output or adapter paths.

## Acceptance criteria

- AC1. A static skill measurement command reports path, byte size, line count, and estimated tokens for canonical skills.
- AC2. A Codex JSONL analyzer reports session usage when available and tool-output amplification signals when present.
- AC3. The first token-cost baseline report can be written under `docs/reports/token-cost/`.
- AC4. Proposal skill guidance requires initial user goals to be classified.
- AC5. Proposal-review guidance requests revision when initial user goals disappear.
- AC6. Static validation covers proposal scope preservation and proposal-review silent-narrowing checks.
- AC7. Canonical skill changes can be checked against generated skill output and public adapter output with the appropriate adapter validation command form.
- AC8. No hard token-budget CI gate is introduced in the first slice.

## Open questions

None.

## Next artifacts

- spec-review
- architecture no-impact rationale or architecture review surface if required by the workflow
- execution plan
- test spec
- implementation

## Follow-on artifacts

- Canonical architecture update: `docs/architecture/system/architecture.md`
- Test spec: `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md`

## Readiness

Approved.

The contract defines measurable behavior, proposal-scope preservation, validation expectations, compatibility boundaries, and non-goals without requiring implementation details or live telemetry infrastructure.
