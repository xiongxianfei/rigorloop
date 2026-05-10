# Token Cost Measurement Baseline and Proposal Scope Preservation Test Spec

## Status

- active

## Related spec and plan

- Spec: [Token Cost Measurement Baseline and Proposal Scope Preservation](token-cost-measurement-baseline-and-proposal-scope-preservation.md), approved.
- Proposal: [Token Cost Measurement Baseline and Proposal Skill Scope Preservation](../docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md), accepted.
- Plan: [Token Cost Measurement Baseline and Proposal Scope Preservation Execution Plan](../docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md), active.
- Architecture: [Canonical system architecture](../docs/architecture/system/architecture.md), updated and approved by architecture-review R1 for repository-local measurement scripts and durable token-cost reports.
- Change metadata: [change.yaml](../docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml).
- Review records:
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/reviews/proposal-review-r2.md`
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/reviews/spec-review-r1.md`
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/reviews/plan-review-r1.md`
- Related proof surfaces:
  - `scripts/measure-skill-tokens.py`
  - `scripts/analyze-codex-jsonl.py`
  - `scripts/test-token-cost-measurement.py`
  - `scripts/skill_validation.py`
  - `scripts/validate-skills.py`
  - `scripts/test-skill-validator.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`

## Testing strategy

- Use focused script tests for static skill measurement, JSONL parsing, command-output amplification summaries, warning-only thresholds, malformed inputs, and missing-input errors.
- Use contract/static validation for proposal and proposal-review skill wording because scope preservation is a guidance and review-surface contract, not a runtime router.
- Use generated-output drift checks after canonical skill edits to prove local Codex skill mirrors remain deterministic derived output.
- Use adapter drift and adapter validation with version `0.1.1` because this repository's adapter validation currently requires a version.
- Use durable report review plus lightweight structure checks for the first baseline report because exact measurements vary by repository state and benchmark input.
- Use lifecycle, review-artifact, and change-metadata validation to prove the plan, spec, test spec, architecture, review records, and change evidence remain coherent.
- Do not test exact tokenizer parity, hosted telemetry, live command wrapping, hard budget gates, or PR #39 behavior beyond the explicit non-reopen boundary.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`-`R1e` | `T1`, `T2`, `T3`, `T21` | unit, smoke | Static skill measurement reports required fields, stays dependency-light, warns instead of failing on budget thresholds, and avoids network access. |
| `R2`, `R2a`-`R2f` | `T4`, `T5`, `T6`, `T7`, `T8`, `T21` | unit, smoke | JSONL analyzer handles usage, absent usage, malformed input, unknown records, command-output amplification, and cost-driver summaries. |
| `R3`, `R3a`, `R3b` | `T8`, `T9`, `T23` | unit, manual | Command-output amplification starts inside the JSONL analyzer and no separate live wrapper is required in this slice. |
| `R4`, `R4a`-`R4d` | `T10`, `T11`, `T21` | manual, integration | Baseline report lives under `docs/reports/token-cost/` and change-local artifacts link to it. |
| `R5`, `R5a`-`R5c` | `T3`, `T16`, `T21` | unit, integration | Thresholds are warnings only and hard CI gates remain out of scope. |
| `R6`, `R6a`-`R6e` | `T12`, `T13`, `T14`, `T16` | integration, manual | Proposal skill preserves initial user intent and requires visible treatment of every initial goal. |
| `R7`, `R7a`-`R7e` | `T13`, `T14`, `T16` | integration, manual | Narrowing is recorded in the appropriate proposal surface. |
| `R8`, `R8a`-`R8f` | `T15`, `T16` | integration, manual | Proposal-review checks for silent narrowing and requests revision without rewriting the proposal. |
| `R9`, `R9a`, `R9b` | `T17`, `T19`, `T20` | integration, manual | Public skill wording stays portable while maintainer validation remains internal. |
| `R10`, `R10a`-`R10e` | `T16` | integration | Static validation uses narrow checks for scope preservation and silent-narrowing review behavior. |
| `R11`, `R11a`-`R11d` | `T18`, `T19`, `T20`, `T21` | smoke, integration | Generated skill and adapter output remain derived and validated with the active version source. |
| `R12`, `R12a`, `R12b` | `T11`, `T21`, `T23` | manual, integration | This change recovers missing work as new work and does not reopen PR #39. |

## Acceptance criteria coverage

| Acceptance criterion | Covered by |
| --- | --- |
| `AC1` | `T1`, `T2`, `T21` |
| `AC2` | `T4`, `T5`, `T7`, `T8`, `T21` |
| `AC3` | `T10`, `T11` |
| `AC4` | `T12`, `T13`, `T14`, `T16` |
| `AC5` | `T15`, `T16` |
| `AC6` | `T16` |
| `AC7` | `T18`, `T19`, `T20`, `T21` |
| `AC8` | `T3`, `T16`, `T21` |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T12`, `T13`, `T14`, `T15` | Broad requests become visible through initial intent preservation and proposal-review checks. |
| `E2` | `T13`, `T15` | Narrowed scope remains valid when deferred or rejected goals have a visible surface and rationale. |
| `E3` | `T15`, `T16` | Silent loss of JSONL analysis causes proposal-review changes-requested behavior. |
| `E4` | `T1`, `T2`, `T3` | Static measurement reports required fields and warning-only threshold behavior. |
| `E5` | `T4`, `T5`, `T7`, `T8` | JSONL analysis reports usage and command-output amplification signals. |
| `E6` | `T10`, `T11` | Durable baseline report path and change-local links preserve longitudinal comparison. |

## Edge case coverage

- EC1, user request includes an explicit non-goal: `T12`, `T13`, `T15`.
- EC2, overlapping goals may be grouped without losing distinct outcomes: `T12`, `T14`, `T15`.
- EC3, deferred goal needs a named follow-up: `T13`, `T15`.
- EC4, rejected goal needs rationale: `T13`, `T15`.
- EC5, JSONL export lacks token usage metadata: `T5`.
- EC6, malformed JSONL fails clearly: `T6`.
- EC7, huge command output is ranked without full raw embedding: `T8`, `T22`.
- EC8, no previous baseline exists: `T10`.
- EC9, adapter scripts require a version: `T20`, `T21`.
- EC10, downstream public skill users use different paths: `T17`, `T19`.

## Test cases

### T1. Static skill measurement reports required fields

- Covers: `R1`, `R1a`, `R1c`, `AC1`, `E4`
- Level: unit, smoke
- Fixture/setup:
  - Temporary canonical-skill fixture files or the repository's canonical `skills/*/SKILL.md` files.
  - `scripts/measure-skill-tokens.py`.
- Steps:
  - Run the static skill measurement command against a controlled skill fixture or the repository's canonical skills.
  - Assert each measured skill includes path, byte size, line count, estimated token count, and success status.
  - Assert the command runs with the repository's normal Python environment and no extra service dependency.
- Expected result:
  - The command exits successfully and prints a reviewable per-skill summary with the required fields.
- Failure proves:
  - Static skill cost cannot be measured as required by the approved spec.
- Automation location:
  - `scripts/test-token-cost-measurement.py`
  - `python scripts/measure-skill-tokens.py`

### T2. Static measurement reports largest Markdown sections and missing-skill errors

- Covers: `R1b`, error behavior "no canonical skills are found"
- Level: unit
- Fixture/setup:
  - Temporary skill fixture with Markdown headings.
  - Temporary empty skill root.
- Steps:
  - Run static measurement against the heading fixture.
  - Assert the largest sections are reported when headings can be detected.
  - Run static measurement against an empty skill root.
  - Assert the command fails with a clear no-canonical-skills error.
- Expected result:
  - Section reporting appears when possible, and an empty input surface fails clearly.
- Failure proves:
  - The command either loses section-level cost evidence or silently succeeds with no measured skills.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T3. Static measurement budget thresholds are warning-only and offline

- Covers: `R1d`, `R1e`, `R5`, `R5a`, `R5b`, `R5c`, `AC8`, `E4`
- Level: unit, manual
- Fixture/setup:
  - Temporary skill fixture whose estimated token count exceeds a configured warning threshold.
  - Network access disabled by design; no network fixtures.
- Steps:
  - Run static measurement with a low token warning threshold.
  - Assert the command prints a warning and exits successfully when the only issue is threshold exceedance.
  - Inspect implementation to confirm it does not call hosted telemetry, external services, or network APIs.
- Expected result:
  - Budget exceedance is visible but non-blocking in the first slice.
- Failure proves:
  - Token-cost measurement became a hard gate or depends on external services.
- Automation location:
  - `scripts/test-token-cost-measurement.py`
  - manual review during M1

### T4. JSONL analyzer reports usage and tool-call summaries

- Covers: `R2`, `R2a`, `R2b`, `R2d`, `AC2`, `E5`
- Level: unit, smoke
- Fixture/setup:
  - Minimal Codex JSONL fixture containing usage metadata, tool calls, and command output.
  - `scripts/analyze-codex-jsonl.py`.
- Steps:
  - Run the analyzer against the fixture.
  - Assert session token usage is reported when usage fields are present.
  - Assert tool calls, command output lines, command output bytes, and estimated command-output tokens are reported.
- Expected result:
  - The analyzer answers what the session cost and why, using available recorded-session evidence.
- Failure proves:
  - The analyzer cannot recover the baseline measurement signals named in the spec.
- Automation location:
  - `scripts/test-token-cost-measurement.py`
  - `python scripts/analyze-codex-jsonl.py <fixture>.jsonl`

### T5. JSONL analyzer handles absent usage metadata

- Covers: `R2c`, edge case 5
- Level: unit
- Fixture/setup:
  - JSONL fixture with command-output events but no token usage metadata.
- Steps:
  - Run the analyzer against the fixture.
  - Assert it reports token usage as unavailable.
  - Assert it still reports available tool-output amplification signals.
- Expected result:
  - Missing usage metadata does not block analysis of recorded command-output amplification.
- Failure proves:
  - The analyzer is too brittle for partial Codex exports.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T6. JSONL analyzer fails clearly for missing, unreadable, or malformed input

- Covers: `R2f`, edge case 6
- Level: unit
- Fixture/setup:
  - Missing path.
  - Malformed JSONL fixture with a known failing line.
  - Unreadable file case when supported by the platform.
- Steps:
  - Run the analyzer for each invalid input.
  - Assert it exits non-zero.
  - Assert the error identifies the missing file, unreadable file, or failing JSONL line or record.
- Expected result:
  - Unsafe analysis failures are explicit and reviewable.
- Failure proves:
  - The analyzer can produce misleading partial output or opaque failures.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T7. JSONL analyzer tolerates unknown event shapes and no-output sessions

- Covers: `R2e`, error behavior "no command-output events"
- Level: unit
- Fixture/setup:
  - JSONL fixture with unknown event shapes.
  - JSONL fixture with valid records but no command-output events.
- Steps:
  - Run the analyzer against unknown-shape fixture.
  - Assert unknown records are skipped or summarized with a warning.
  - Run the analyzer against the no-output fixture.
  - Assert zero observed command-output amplification is reported.
- Expected result:
  - Unknown shapes and quiet sessions are handled without invented cost drivers.
- Failure proves:
  - The analyzer either breaks on future export shapes or fabricates amplification evidence.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T8. JSONL analyzer identifies amplification cost drivers

- Covers: `R2d`, `R3`, `R3a`, `AC2`, `E5`, edge case 7
- Level: unit
- Fixture/setup:
  - JSONL fixture with large command output, broad searches, full-file reads, high `max_output_tokens`, and repeated file reads.
- Steps:
  - Run the analyzer against the fixture.
  - Assert largest outputs are ranked.
  - Assert broad searches, full-file reads, high output caps, repeated file reads, and top measured cost drivers are reported when present.
  - Assert the report summarizes large output rather than embedding the whole raw output body.
- Expected result:
  - Runtime tool-output amplification is measured from recorded sessions inside the JSONL analyzer.
- Failure proves:
  - The first measurement slice misses the largest runtime cost-driver signals.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T9. No live command wrapper is required in the first slice

- Covers: `R3a`, `R3b`
- Level: manual, contract
- Fixture/setup:
  - Active spec and plan.
  - Repository `scripts/` tree after M1.
- Steps:
  - Confirm the plan and implementation do not require a standalone live command wrapper for M1.
  - Confirm any future `scripts/measure-command-output.py` idea remains deferred unless a later approved scope adds live command wrapping.
- Expected result:
  - Recorded sessions are analyzed first; live command wrapping remains out of scope for this slice.
- Failure proves:
  - Implementation expanded beyond the approved measurement direction.
- Automation location:
  - Manual review during M1 and M5.

### T10. Baseline report has durable longitudinal structure

- Covers: `R4`, `R4a`, `R4b`, `R4c`, `AC3`, `E6`, edge case 8
- Level: manual, integration
- Fixture/setup:
  - `docs/reports/token-cost/2026-05-10-baseline.md`.
  - M1 measurement command output.
- Steps:
  - Confirm the report path is under `docs/reports/token-cost/`.
  - Confirm the report includes summary, static skill cost, Codex session cost, tool-output amplification, top cost drivers, comparison to previous report, conclusions, and next actions.
  - Confirm the comparison section states no previous baseline exists when this is the first baseline.
- Expected result:
  - The first report can be compared with future reports.
- Failure proves:
  - Baseline evidence is change-local only or lacks stable comparison structure.
- Automation location:
  - Manual review during M2.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/reports/token-cost/2026-05-10-baseline.md`

### T11. Change-local evidence links to the baseline and preserves PR #39 boundary

- Covers: `R4d`, `R12`, `R12a`, `R12b`, `E6`
- Level: manual, integration
- Fixture/setup:
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`.
  - Optional `explain-change.md` or milestone evidence created during M2/M5.
- Steps:
  - Confirm change-local artifacts link to the token-cost baseline report instead of duplicating its full body.
  - Confirm evidence treats PR #39 as completed bounded-evidence guidance and does not reopen or relitigate it.
- Expected result:
  - The report is durable and the change scope remains new work.
- Failure proves:
  - The change either duplicates longitudinal evidence into one PR pack or retroactively expands a completed PR.
- Automation location:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - manual review during M2 and M5

### T12. Proposal skill extracts and classifies initial intent

- Covers: `R6`, `R6a`, `R6b`, `R6e`, `E1`, edge cases 1 and 2
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`.
  - `scripts/test-skill-validator.py`.
- Steps:
  - Assert proposal guidance instructs agents to extract initial goals, concerns, constraints, and requested outcomes before drafting or materially revising a proposal.
  - Assert every initial user goal must be visible as `in scope`, `out of scope`, `deferred follow-up`, `rejected option`, or `open question`.
  - Manually confirm grouped goals preserve distinct requested outcomes.
- Expected result:
  - Proposal narrowing remains allowed but no part of the user's initial request disappears silently.
- Failure proves:
  - The proposal skill can repeat the scope-loss failure.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`

### T13. Proposal skill records narrowing in the correct proposal surfaces

- Covers: `R7`, `R7a`-`R7e`, `E2`, edge cases 3 and 4
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`.
  - `scripts/test-skill-validator.py`.
- Steps:
  - Assert in-scope goals route to goals, recommended direction, workstreams, or equivalent sections.
  - Assert out-of-scope goals route to non-goals or equivalent scope-control sections.
  - Assert deferred goals route to next artifacts, follow-on artifacts, named follow-up, or equivalent downstream surface.
  - Assert rejected goals route to options considered, decision log, or equivalent rationale sections.
  - Assert open goals route to open questions.
- Expected result:
  - Reviewers can locate what was kept, removed, deferred, rejected, or left open.
- Failure proves:
  - Narrowing can remain invisible even if classification language exists.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M3

### T14. Broad proposals include initial intent preservation table or equivalent section

- Covers: `R6c`, `R6d`, `E1`
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`.
- Steps:
  - Assert broad or multi-part proposals require an `Initial intent preservation` section or equivalent table.
  - Assert the table, when used, includes columns equivalent to `Initial user goal`, `Proposal treatment`, and `Where recorded`.
  - Manually confirm the guidance remains concise enough for public skill use.
- Expected result:
  - Broad requests expose scope preservation in a reviewable table without making every small proposal heavy.
- Failure proves:
  - Proposal-review lacks a reliable surface for broad-request scope checks.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M3

### T15. Proposal-review detects silent narrowing and requests revision

- Covers: `R8`, `R8a`-`R8f`, `E1`, `E2`, `E3`
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal-review/SKILL.md`.
  - `scripts/test-skill-validator.py`.
- Steps:
  - Assert proposal-review compares the user's initial request with the proposal.
  - Assert it returns `changes-requested` when an initial goal disappears.
  - Assert it returns `changes-requested` when a deferred goal has no follow-up, a rejected goal has no rationale, or a narrowed proposal does not say why.
  - Assert proposal-review does not rewrite the proposal unless the user explicitly asks it to edit.
- Expected result:
  - Proposal-review catches silent scope loss without taking over proposal authoring.
- Failure proves:
  - Review can approve the same silent narrowing failure again.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M3

### T16. Static validation protects proposal scope preservation

- Covers: `R5`, `R5a`, `R10`, `R10a`-`R10e`, `AC4`, `AC5`, `AC6`, `AC8`
- Level: integration
- Fixture/setup:
  - `scripts/skill_validation.py`.
  - `scripts/test-skill-validator.py`.
  - `skills/proposal/SKILL.md`.
  - `skills/proposal-review/SKILL.md`.
- Steps:
  - Add or update narrow section, phrase, or stable-ID checks for proposal scope-preservation guidance.
  - Assert the validator checks that every initial goal must be classified.
  - Assert the validator checks that proposal-review catches silent narrowing and requests revision when initial goals disappear.
  - Assert validation does not add broad natural-language semantic scoring.
  - Confirm no token-budget hard CI gate is introduced by the validation change.
- Expected result:
  - Scope preservation is covered by repo-owned static validation without brittle semantic scoring.
- Failure proves:
  - The skill contract can drift without automated detection or validation can become too subjective.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`

### T17. Public skill wording remains portable

- Covers: `R9`, `R9a`, `R9b`, edge case 10
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`.
  - `skills/proposal-review/SKILL.md`.
  - Generated public skill output after M4.
- Steps:
  - Inspect public skill wording for repository-maintainer-only paths, generated mirror paths, adapter paths, selector path constraints, drift-check mechanics, and shared-block implementation mechanics.
  - Confirm internal validation commands remain in specs, plans, tests, contributor docs, or change-local evidence rather than published skill guidance.
- Expected result:
  - Downstream public skill users can apply the guidance without knowing this repository's internal layout.
- Failure proves:
  - Public skill text leaks contributor-only mechanics.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M3 and M4

### T18. Generated local skill output matches canonical skills

- Covers: `R11`, `R11a`, `AC7`
- Level: smoke
- Fixture/setup:
  - Canonical skill files under `skills/`.
  - Generated local Codex skill mirror under `.codex/skills/`.
- Steps:
  - Run the generated local skill drift check after canonical skill changes.
  - Confirm any generated diffs come from the generator, not hand edits.
- Expected result:
  - Local generated skill output remains deterministic derived output.
- Failure proves:
  - Canonical and generated skill behavior have drifted.
- Automation location:
  - `python scripts/build-skills.py --check`

### T19. Public adapter output matches canonical public skill text

- Covers: `R9`, `R11`, `R11b`, `AC7`, edge case 10
- Level: smoke, integration
- Fixture/setup:
  - Canonical skills.
  - Generated public adapter packages under `dist/adapters/`.
- Steps:
  - Run adapter drift check after canonical proposal/proposal-review skill changes.
  - Run adapter distribution tests if public adapter output changes.
  - Inspect generated public skill text for portability leakage.
- Expected result:
  - Public adapters carry the new behavior without stale generated output or internal path leakage.
- Failure proves:
  - Public users receive stale or repository-specific skill behavior.
- Automation location:
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/test-adapter-distribution.py`

### T20. Adapter validation uses the active version source

- Covers: `R11c`, `R11d`, edge case 9
- Level: integration
- Fixture/setup:
  - Adapter validation scripts.
  - Active plan and change evidence.
- Steps:
  - Run adapter validation with version `0.1.1`.
  - Confirm the plan or change evidence records that `0.1.1` is used because the repository adapter validator currently requires `--version`.
- Expected result:
  - Adapter validation is explicit and tied to the repository's active version requirement.
- Failure proves:
  - Adapter validation is skipped, uses an arbitrary version, or fails to record the version source.
- Automation location:
  - `python scripts/validate-adapters.py --version 0.1.1`

### T21. Lifecycle and change metadata remain coherent through milestones

- Covers: `R1`-`R12`, `AC1`-`AC8`
- Level: integration
- Fixture/setup:
  - Active proposal, spec, test spec, architecture, plan, plan index, change metadata, review log, and review-resolution artifacts.
- Steps:
  - Run review-artifact closeout validation after each review loop when records change.
  - Run change-metadata validation after milestone evidence updates.
  - Run artifact-lifecycle validation over the explicit changed lifecycle-managed artifacts.
  - Run `git diff --check --` on the scoped changed paths for each milestone.
- Expected result:
  - Artifact state matches the actual workflow state and validation evidence stays reviewable.
- Failure proves:
  - Implementation evidence, lifecycle state, or review records have drifted.
- Automation location:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md --path docs/architecture/system/architecture.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `git diff --check -- .`

### T22. Baseline reporting avoids excessive raw transcript content

- Covers: security/privacy requirements, edge case 7
- Level: manual
- Fixture/setup:
  - `docs/reports/token-cost/2026-05-10-baseline.md`.
  - JSONL analyzer output from M1.
- Steps:
  - Confirm the baseline summarizes command-output amplification instead of embedding unnecessary raw transcript content.
  - Confirm large outputs are represented by counts, estimates, ranks, command summaries, or bounded excerpts.
  - Confirm no intentional collection of secrets, credentials, private keys, or private user data is added.
- Expected result:
  - The report is useful for optimization decisions without overexposing raw session data.
- Failure proves:
  - Measurement evidence creates avoidable privacy or review-volume risk.
- Automation location:
  - Manual review during M2 and M5.

### T23. Non-goal and rollback boundaries stay intact

- Covers: `R3b`, `R12`, `R12a`, `R12b`
- Level: manual
- Fixture/setup:
  - Spec, plan, implementation diff, and final explain-change evidence.
- Steps:
  - Confirm no hosted telemetry, hard token-budget CI gate, live command wrapper, all-skill rewrite, or PR #39 reopening enters the implementation.
  - Confirm rollback can remove scripts, tests, report, skill text, generated output, and validation changes without data migration.
- Expected result:
  - The implemented scope remains the approved lightweight first slice.
- Failure proves:
  - The change exceeded the accepted proposal and approved spec.
- Automation location:
  - Manual review during code-review and verify.

## Fixtures and data

- Script tests may create temporary skill and JSONL fixtures inside `scripts/test-token-cost-measurement.py` to keep the first slice lightweight.
- Tracked fixtures may be added only if they make JSONL shape coverage easier to review; prefer small synthetic fixtures over real transcript excerpts.
- JSONL fixtures should cover usage-present, usage-absent, unknown event shape, malformed line, no command output, large command output, broad search, full-file read, high output cap, and repeated file read cases.
- The baseline report may use a local Codex JSONL export when available. If no suitable export is available, it must state the benchmark source and any unavailable session-token evidence.
- Do not commit full raw Codex transcript exports unless the content has been intentionally reviewed for privacy and size.

## Mocking/stubbing policy

- Do not mock filesystem reads for static skill measurement when temporary fixture directories can exercise real paths.
- Do not mock JSON parsing for the analyzer; use small JSONL fixture records.
- Do not mock generated-output checks in final validation; run the repository-owned generator drift and adapter validation commands.
- Network calls should not exist. If a test needs to prove no network dependency, prefer code inspection or dependency-free design rather than network interception.

## Migration or compatibility tests

- Existing proposals and learn records are historical and do not need migration tests.
- New and substantively revised broad proposals after implementation must follow scope preservation; static validation covers the skill guidance, not historical artifact rewrites.
- Generated skill mirrors and public adapters must be regenerated or checked only after canonical skill changes.
- Adapter validation must use `0.1.1` for this plan unless a later approved release artifact changes the active version source.
- Rollback compatibility is manual: the change has no runtime data migration and can revert scripts, tests, report, skill text, generated output, and validation changes together.

## Observability verification

- Measurement commands must print human-readable summaries suitable for review evidence.
- JSONL analyzer output must make unavailable token usage explicit rather than silent.
- Baseline report must include benchmark source, repository state, top cost drivers, conclusions, and next actions.
- Validation failures must identify missing scope-preservation or adapter validation conditions.
- Review and verify artifacts must cite the exact commands run.

## Security/privacy verification

- Measurement commands must not require network access, hosted telemetry, or external services.
- Measurement commands must not intentionally collect secrets, credentials, private keys, or private user data.
- JSONL analyzer and baseline report output must summarize large or sensitive command output instead of embedding unnecessary raw transcript content.
- Public skill text must not expose repository-maintainer-only internal paths or release mechanics.

## Performance checks

- Static skill measurement should complete within a few seconds for the repository's canonical skills on a typical contributor machine.
- JSONL analysis should stream or process records incrementally enough that large session exports do not require loading the whole file into memory.
- Token estimates are approximate and must be labeled as estimates.
- Performance checks are sanity checks, not hard benchmarks, in the first slice.

## Manual QA checklist

- Confirm M1 commands report measurement data without telemetry or hard budget gates.
- Confirm M2 report has the required durable structure and links from change-local evidence.
- Confirm M3 skill wording is concise, public-portable, and preserves every initial user goal visibly.
- Confirm M4 generated output was produced by generators and validates for adapter version `0.1.1`.
- Confirm M5 final lifecycle closeout waits until M1-M4 each pass implementation handoff, code-review, and review closeout.
- Confirm final PR evidence names the exact commands run and any unavailable benchmark evidence.

## What not to test and why

- Do not test exact tokenizer parity with proprietary tokenizers; the first slice uses estimates and labels them as estimates.
- Do not add hosted telemetry or network tests; external services are out of scope.
- Do not add a live command wrapper test; live command wrapping is deferred until separately approved.
- Do not add hard CI budget-gate tests; thresholds are warning-only in the first slice.
- Do not run broad semantic scoring over proposal text; validation must use narrow section, phrase, or stable-ID checks.
- Do not migrate historical proposals or PR #39 artifacts; they remain valid historical evidence.
- Do not require downstream public skill users to use this repository's internal paths.

## Uncovered gaps

None.

## Next artifacts

- implement M1
- code-review M1
- implement M2 after M1 review closeout
- code-review M2
- implement M3 after M2 review closeout
- code-review M3
- implement M4 after M3 review closeout
- code-review M4
- M5 final lifecycle closeout after M1-M4 review loops pass
- explain-change
- verify
- PR handoff

## Follow-on artifacts

None yet.

## Readiness

Active.

This test spec is ready to guide implementation of M1. M1 should return to code-review only after targeted validation passes and the active plan marks M1 `review-requested`.
