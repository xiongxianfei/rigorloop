# Review Finding Resolution Contract Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/review-finding-resolution-contract.md`
- Plan: `docs/plans/2026-04-25-review-finding-resolution-contract.md`
- Proposal: `docs/proposals/2026-04-24-review-finding-resolution-contract.md`
- Architecture: `docs/architecture/2026-04-24-review-finding-resolution-contract.md`
- Spec-review findings: resolved in `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/spec-review-r2.md`
- Architecture-review findings: resolved in `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/architecture-review-r2.md`
- Plan-review findings: approved with no required edits
- Change-local review resolution: `docs/changes/2026-04-24-review-finding-resolution-contract/review-resolution.md`

## Testing strategy

- Unit tests exercise line-based field extraction, canonical `review-log.md` block parsing, Review ID uniqueness, Finding ID uniqueness, resolution entry parsing, disposition vocabulary, closeout status parsing, and disposition-specific closeout field checks.
- Integration tests use filesystem fixtures under `tests/fixtures/review-artifacts/` to validate complete change roots through `scripts/validate-review-artifacts.py` in both `structure` and `closeout` modes.
- Contract tests inspect workflow docs, governance summaries, canonical skills, generated `.codex/skills/`, and generated public adapters to prove disposition vocabulary, closeout rules, concise PR summary behavior, and generated-output sync remain aligned.
- CI tests verify that `scripts/ci.sh` invokes review-artifact structure validation only for changed or explicitly selected `docs/changes/<change-id>/` roots and does not retroactively fail unrelated historical artifacts.
- Security and privacy checks assert that review-artifact validation uses only local repository files, does not require network access or secrets, and reports paths, line numbers, IDs, mode, and short reasons rather than large copied excerpts.
- Non-smoke validation must run with Python standard library code and repository files only. It must not require installed Codex, Claude Code, OpenCode, network access, hosted CI, or external review tools.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R1d` | `T1`, `T11` | Complete finding guidance and incomplete-finding boundary in review-stage guidance. |
| `R2`-`R2l` | `T2`, `T3`, `T13` | Detailed review metadata, exact-one Review ID, stage scope, stability, and per-change uniqueness. |
| `R2m`, `R2m-exception`, `R2n`, `R2o` | `T2`, `T8`, `T11` | First-pass timing, reconstructed records, append-only review history, and resolution/update surfaces. |
| `R3`-`R3k` | `T3`, `T13` | Required review-log, canonical `### Review entry` blocks, exact-once ledger references, and prose exclusion. |
| `R4`-`R4c` | `T4`, `T8` | Material Finding IDs, uniqueness, stable format, and non-material no-ID path. |
| `R5`-`R5i` | `T4`, `T5`, `T7`, `T11` | Required review-resolution entries, initial entries before fixes, final action, validation target, and suggested-vs-final action split. |
| `R6`-`R6m` | `T6`, `T7`, `T10` | Approved dispositions, final dispositions, `needs-decision` blocker, and top-level closeout status. |
| `R7`-`R7d` | `T6`, `T7` | Disposition-specific action, rationale, follow-up, sub-decision, and evidence records. |
| `R8`-`R8h` | `T7`, `T10`, `T11`, `T14` | Closeout-gated validation for `verify`, `explain-change`, and `pr`, plus blocking review outcome behavior. |
| `R9`-`R9a` | `T12` | Concise `explain-change.md` review-resolution summary and linked detail. |
| `R10`-`R10c` | `T12` | PR review-resolution summary counts, link, no transcript duplication, and no false readiness with `needs-decision`. |
| `R11`-`R11b` | `T2`-`T9`, `T13`, `T15` | Minimal structural validation, closeout mode, actionable failures, and semantic-automation boundary. |
| `R12`-`R12c` | `T16` | Generated `.codex/skills/` and public adapter sync after canonical shipped skill changes. |
| `R13`-`R13b` | `T8`, `T13` | Clean-review lightweight path and `reviews/` still requiring `review-log.md`. |
| `R14`-`R14a` | `T11`, `T12`, `T16` | Workflow contract, stage tables, governance summaries, skills, and generated adapters align with expanded vocabulary. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T1`, `T5` | Complete finding can enter review-resolution. |
| `E2` | `T1` | Incomplete finding cannot drive fix loop. |
| `E3` | `T3`, `T8` | Any `reviews/` directory requires `review-log.md`, even one review file. |
| `E4` | `T6`, `T7` | `needs-decision` blocks downstream closeout. |
| `E5` | `T6`, `T7` | `partially-accepted` closes only with accepted and non-accepted sub-decisions. |
| `E6` | `T12` | PR body stays concise and links review-resolution. |
| `E7` | `T16` | Canonical skill changes regenerate `.codex/skills/` and public adapters. |
| `E8` | `T2`, `T5`, `T11` | First-pass review, review-log, and resolution entries exist before fixes. |
| `E9` | `T7`, `T11`, `T14` | Resolution alone does not replace required re-review or owner closeout. |
| `E10` | `T7` | `Closeout status: open` blocks final closeout. |
| `E11` | `T2` | Reconstructed review records are explicit and preserve evidence/fidelity notes. |
| `E12` | `T3` | Review-log uses canonical line blocks and exact field labels. |

## Edge case coverage

- Edge case 1, single detailed review under `reviews/`: `T3`, `T8`
- Edge case 2, clean review with no material findings: `T8`
- Edge case 3, archival `reviews/` with no material findings: `T8`
- Edge case 4, evidence and required outcome but no safe resolution: `T1`
- Edge case 5, `needs-decision` before closeout: `T6`, `T7`
- Edge case 6, partially accepted without rejected/deferred rationale: `T6`, `T7`
- Edge case 7, deferred without follow-up or no-follow-up reason: `T6`, `T7`
- Edge case 8, review-log references unknown Review ID: `T3`
- Edge case 9, detailed review with two Review IDs: `T2`
- Edge case 10, duplicate Review IDs within a change: `T2`, `T3`, `T13`
- Edge case 11, duplicate Finding IDs within a change: `T4`
- Edge case 12, material Finding ID missing from `review-resolution.md`: `T4`, `T7`
- Edge case 13, maintainer PR comments are not copied into `reviews/`: `T11`, `T14`
- Edge case 14, semantic disagreement is not automated: `T9`, `T15`
- Edge case 15, canonical skill change without generated public adapter output: `T16`
- Edge case 16, first-pass blocking review closed only through review-resolution: `T7`, `T11`, `T14`
- Edge case 17, accepted resolution while top-level closeout remains open: `T7`
- Edge case 18, review-log prose mention of Review ID: `T3`, `T13`
- Edge case 19, late reconstructed review record: `T2`

## Test cases

### T1. Review guidance requires complete material findings

- Covers: `R1`, `R1a`, `R1b`, `R1c`, `R1d`, `R5c`, `E1`, `E2`, edge case 4
- Level: contract
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `specs/rigorloop-workflow.md`
- Steps:
  - Inspect canonical review-stage guidance for material finding requirements.
  - Assert guidance requires evidence, required outcome, and a safe resolution path or decision-needed rationale.
  - Assert guidance treats missing evidence, missing required outcome, and missing resolution or decision-needed rationale as incomplete.
  - Assert no guidance allows a vague finding such as "needs more validation" to drive a fix loop.
- Expected result:
  - Review-stage guidance requires complete, actionable findings before review-resolution or fixes rely on them.
- Failure proves:
  - Implementers can still act on incomplete review findings.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - contract assertions may also live in `scripts/test-skill-validator.py` if shared skill text checks are reused

### T2. Detailed review record parser validates metadata, uniqueness, timing, and reconstructed records

- Covers: `R2`-`R2o`, `R11`, `E8`, `E11`, edge cases 9, 10, 19
- Level: unit, integration
- Fixture/setup:
  - `tests/fixtures/review-artifacts/valid-detailed-review/`
  - `tests/fixtures/review-artifacts/missing-review-fields/`
  - `tests/fixtures/review-artifacts/multiple-review-ids/`
  - `tests/fixtures/review-artifacts/duplicate-review-ids/`
  - `tests/fixtures/review-artifacts/reconstructed-valid/`
  - `tests/fixtures/review-artifacts/reconstructed-missing-metadata/`
- Steps:
  - Parse each detailed review file under `reviews/`.
  - Assert every detailed review file has exactly one `Review ID`, plus `Stage`, `Round`, `Reviewer`, `Target`, and `Status`.
  - Assert Review IDs are stable ASCII identifiers and unique within one change root.
  - Assert valid reconstructed records contain `Record mode: reconstructed`, original source/evidence fields, after-fix timing disclosure, stable Finding IDs, and fidelity-loss notes.
  - Assert reconstructed records missing any required metadata fail structure mode.
  - Assert duplicate Review IDs fail only within the same change root, not across independent fixture roots.
- Expected result:
  - The parser rejects malformed review files and accepts explicit reconstructed records without requiring global Review ID uniqueness.
- Failure proves:
  - Review records cannot reliably identify one review event or distinguish late reconstructed history.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py tests/fixtures/review-artifacts/<fixture>`

### T3. Review-log parser counts only canonical review entry blocks

- Covers: `R3`-`R3k`, `R11`, `E3`, `E12`, edge cases 1, 3, 8, 10, 18
- Level: unit, integration
- Fixture/setup:
  - `tests/fixtures/review-artifacts/valid-review-log/`
  - `tests/fixtures/review-artifacts/missing-review-log/`
  - `tests/fixtures/review-artifacts/log-missing-review-id/`
  - `tests/fixtures/review-artifacts/log-unknown-review-id/`
  - `tests/fixtures/review-artifacts/log-duplicate-review-id/`
  - `tests/fixtures/review-artifacts/log-prose-review-id-only/`
  - `tests/fixtures/review-artifacts/log-missing-required-field/`
- Steps:
  - Validate a change root with one detailed review and a matching canonical `review-log.md` block.
  - Validate a change root with `reviews/` and no `review-log.md`.
  - Validate canonical blocks missing `Review ID`, `Stage`, `Round`, `Status`, `Detailed record`, `Resolution`, `Material findings`, or `Open findings`.
  - Validate a log with duplicate `Review ID:` lines inside canonical `### Review entry` blocks.
  - Validate a log with a Review ID mentioned only in prose outside a canonical block.
  - Validate a log that references an unknown detailed review file.
- Expected result:
  - Structure mode counts exactly one `Review ID: <id>` line inside each canonical block and rejects missing, duplicate, dangling, or incomplete ledger entries.
- Failure proves:
  - The review-log cannot serve as an exact, parseable ledger.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py tests/fixtures/review-artifacts/<fixture>`

### T4. Finding ID parser and resolution links enforce material finding traceability

- Covers: `R4`-`R5b`, `R5d`, `R8d`, `R8e`, `R11`, edge cases 11, 12
- Level: unit, integration
- Fixture/setup:
  - `tests/fixtures/review-artifacts/valid-material-findings/`
  - `tests/fixtures/review-artifacts/duplicate-finding-ids/`
  - `tests/fixtures/review-artifacts/missing-resolution-file/`
  - `tests/fixtures/review-artifacts/missing-resolution-entry/`
  - `tests/fixtures/review-artifacts/unknown-resolution-finding/`
- Steps:
  - Parse every `Finding ID:` in detailed review files as material.
  - Assert Finding IDs are stable ASCII identifiers with no whitespace and unique within the change root.
  - Assert every material Finding ID appears exactly once in `review-resolution.md`.
  - Assert `review-resolution.md` references only known Finding IDs.
  - Assert positive notes, nits, or informational observations without `Finding ID:` do not require resolution entries.
- Expected result:
  - Material findings are traceable from review record to resolution, and non-material notes remain lightweight.
- Failure proves:
  - Findings can be lost, duplicated, or resolved without a corresponding review record.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py tests/fixtures/review-artifacts/<fixture>`

### T5. Review-resolution structure records initial decisions, final actions, and validation targets

- Covers: `R5c`, `R5e`, `R5f`, `R5g`, `R5h`, `R5i`, `R6f`, `E1`, `E8`
- Level: unit, integration
- Fixture/setup:
  - `tests/fixtures/review-artifacts/valid-open-resolution/`
  - `tests/fixtures/review-artifacts/resolution-missing-owner/`
  - `tests/fixtures/review-artifacts/resolution-missing-owning-stage/`
  - `tests/fixtures/review-artifacts/resolution-missing-validation-target/`
  - `tests/fixtures/review-artifacts/resolution-final-action-differs/`
- Steps:
  - Validate initial resolution entries with Finding ID, disposition, owner, owning stage, chosen action or stop state, rationale when known, and validation target.
  - Assert structure mode accepts `Closeout status: open` for in-progress review-resolution records.
  - Assert structure mode fails when required initial resolution labels are missing.
  - Assert entries can distinguish reviewer-suggested resolution text from final action when they differ.
- Expected result:
  - Review-resolution records can be created before fixes and expanded during revision without pretending they are final closeout.
- Failure proves:
  - The resolution artifact cannot support safe review-driven revision work.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`

### T6. Disposition vocabulary and final-disposition records are validated

- Covers: `R6`-`R7d`, `E4`, `E5`, edge cases 5, 6, 7
- Level: unit, integration
- Fixture/setup:
  - `tests/fixtures/review-artifacts/valid-dispositions/`
  - `tests/fixtures/review-artifacts/unsupported-disposition/`
  - `tests/fixtures/review-artifacts/needs-decision-valid-open/`
  - `tests/fixtures/review-artifacts/partial-missing-subdecision/`
  - `tests/fixtures/review-artifacts/deferred-missing-followup/`
  - `tests/fixtures/review-artifacts/rejected-missing-rationale/`
- Steps:
  - Validate each approved disposition value: `accepted`, `rejected`, `deferred`, `partially-accepted`, and `needs-decision`.
  - Assert unsupported dispositions fail structure mode.
  - Assert `needs-decision` records identify decision owner, decision needed, and owning stage.
  - Assert `partially-accepted` records identify accepted portion, rejected or deferred portion, rationale, and validation evidence for the accepted portion.
  - Assert deferred and rejected records include their required rationale and follow-up or no-follow-up fields where applicable.
- Expected result:
  - The validator accepts only the approved vocabulary and can distinguish non-final `needs-decision` from final dispositions.
- Failure proves:
  - Review-resolution can silently use unsupported or under-specified disposition states.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`

### T7. Closeout mode blocks unresolved review-resolution records

- Covers: `R6a`-`R6m`, `R7`-`R8h`, `E4`, `E5`, `E9`, `E10`, edge cases 5, 6, 7, 12, 16, 17
- Level: integration
- Fixture/setup:
  - `tests/fixtures/review-artifacts/valid-closed-resolution/`
  - `tests/fixtures/review-artifacts/open-closeout-status/`
  - `tests/fixtures/review-artifacts/needs-decision-open/`
  - `tests/fixtures/review-artifacts/accepted-missing-action/`
  - `tests/fixtures/review-artifacts/accepted-missing-evidence/`
  - `tests/fixtures/review-artifacts/deferred-missing-rationale/`
  - `tests/fixtures/review-artifacts/partial-missing-accepted-evidence/`
  - `tests/fixtures/review-artifacts/blocking-review-without-rerun/`
- Steps:
  - Run `python scripts/validate-review-artifacts.py --mode closeout` against a fully closed fixture.
  - Run closeout mode against fixtures with `Closeout status: open`, unresolved `needs-decision`, missing material resolution entries, accepted entries without action or evidence, deferred/rejected entries without rationale, and partial entries missing sub-decision fields.
  - Assert a first-pass `revise`, `changes-requested`, or `blocked` review outcome remains blocking unless same-stage re-review or explicit reviewer or owner closeout is represented in the change root.
- Expected result:
  - Closeout mode accepts only `Closeout status: closed` with final dispositions and all required disposition-specific closeout records.
- Failure proves:
  - `verify`, `explain-change`, or `pr` can proceed with unresolved material review findings.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout tests/fixtures/review-artifacts/<fixture>`

### T8. Clean-review and no-material-finding paths stay lightweight

- Covers: `R4c`, `R13`, `R13a`, `R13b`, `E3`, edge cases 1, 2, 3
- Level: integration
- Fixture/setup:
  - `tests/fixtures/review-artifacts/no-review-artifacts/`
  - `tests/fixtures/review-artifacts/clean-review-with-log/`
  - `tests/fixtures/review-artifacts/reviews-with-no-findings-missing-log/`
- Steps:
  - Validate a change root without `reviews/`, `review-log.md`, or `review-resolution.md`.
  - Validate a clean review record under `reviews/` with no `Finding ID:` lines and a matching `review-log.md` entry.
  - Assert no empty `review-resolution.md` is required when there are no material findings.
  - Assert `reviews/` still requires `review-log.md` even when no material findings exist.
- Expected result:
  - Clean-review changes avoid empty boilerplate while independently created `reviews/` directories remain indexed.
- Failure proves:
  - The feature either overburdens clean reviews or loses review history.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`

### T9. Validator output is actionable and remains structural only

- Covers: `R11`, `R11a`, `R11b`, edge case 14
- Level: unit, integration
- Fixture/setup:
  - representative invalid review-artifact fixtures
  - fixture with weak but structurally present rationale text
- Steps:
  - Run the validator against invalid fixtures.
  - Assert failures include repo-relative path, line number when available, Review ID or Finding ID when available, validation mode, and short reason.
  - Assert the validator does not fail a record only because the rationale or evidence is subjectively weak when required fields are present.
  - Assert output does not dump large review excerpts.
- Expected result:
  - Failures are actionable without becoming semantic review-quality automation.
- Failure proves:
  - The validator is either too vague to fix or too broad for the approved semantic boundary.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`

### T10. Closeout mode is available to downstream workflow stages

- Covers: `R6a`-`R6m`, `R8`-`R8h`
- Level: contract, integration
- Fixture/setup:
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `scripts/validate-review-artifacts.py`
- Steps:
  - Inspect `verify`, `explain-change`, and `pr` skill guidance for closeout checks when material review artifacts exist.
  - Assert those stages name closeout blockers: `Closeout status: open`, `needs-decision`, missing material Finding IDs, missing accepted evidence, and missing rationale for rejected/deferred portions.
  - Assert the CLI supports `--mode closeout`.
- Expected result:
  - Downstream stage guidance has a concrete validator mode to rely on for final handoff.
- Failure proves:
  - The validator exists but workflow stages can bypass the final closeout contract.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --help`

### T11. Workflow guidance records first-pass timing and re-review requirements

- Covers: `R1`-`R2o`, `R5e`, `R5h`, `R8f`, `R8g`, `R14`, `R14a`, `E8`, `E9`, edge cases 13, 16
- Level: contract
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - canonical review-stage skills
- Steps:
  - Assert current workflow guidance names first-pass review recording before fixes.
  - Assert material findings must receive initial resolution entries before review-driven fixes begin.
  - Assert first-pass review files are not rewritten to hide or replace material findings.
  - Assert corrections, decisions, fixes, and evidence are recorded in `review-resolution.md`, later review rounds, or explicit closeout artifacts.
  - Assert blocking review outcomes require same-stage re-review or explicit reviewer/owner closeout before advancing.
  - Assert maintainer PR review comments are not required in `reviews/` for this version.
- Expected result:
  - Contributors can follow the timing and re-review contract without relying on chat memory.
- Failure proves:
  - The process can silently replace review history with after-the-fact cleanup.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - text checks may be grouped with skill validator fixtures if appropriate

### T12. Explain-change and PR guidance summarize review resolution without duplicating findings

- Covers: `R9`, `R9a`, `R10`, `R10a`, `R10b`, `R10c`, `E6`
- Level: contract
- Fixture/setup:
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - generated `.codex/skills/explain-change/SKILL.md`
  - generated `.codex/skills/pr/SKILL.md`
  - generated public adapter skill files for `explain-change` and `pr` when included
- Steps:
  - Assert `explain-change` guidance tells authors to summarize review-driven changes concisely and link to `review-resolution.md`.
  - Assert PR guidance requires counts by disposition and a link to `docs/changes/<change-id>/review-resolution.md` when present.
  - Assert PR guidance prohibits duplicating every detailed finding and suggested solution.
  - Assert PR guidance does not allow PR handoff readiness while `needs-decision` remains.
- Expected result:
  - Final reviewer-facing text is concise while durable artifacts carry detailed resolution history.
- Failure proves:
  - PR bodies can become the durable review transcript or can overclaim readiness.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-skills.py`

### T13. CI validates changed review-artifact roots without retroactive historical migration

- Covers: `R3`-`R3k`, `R11`, `R13b`, edge cases 1, 3, 8, 10, 18
- Level: integration
- Fixture/setup:
  - `scripts/ci.sh`
  - temporary git fixture or controlled changed-path list
  - valid and invalid `docs/changes/<change-id>/` roots
- Steps:
  - Create a fixture with a changed `docs/changes/current-change/reviews/` root and run the CI discovery logic.
  - Assert `scripts/ci.sh` invokes `python scripts/validate-review-artifacts.py docs/changes/current-change`.
  - Assert unrelated historical change roots are not validated merely because they exist.
  - Assert duplicate Review IDs inside canonical review-log blocks fail for the changed root.
  - Assert Review ID prose outside canonical blocks does not count as a ledger reference.
- Expected result:
  - CI enforces the new structure where it is relevant without forcing a repository-wide historical migration.
- Failure proves:
  - Review-artifact validation either misses changed roots or blocks unrelated old artifacts.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `bash scripts/ci.sh`

### T14. Final lifecycle validation catches stale plan, review, and artifact state

- Covers: `R8f`, `R8g`, `R8h`, implementation closeout behavior
- Level: integration, contract
- Fixture/setup:
  - active plan
  - `docs/plan.md`
  - `docs/changes/<change-id>/change.yaml`
  - `review-log.md`
  - `review-resolution.md`
- Steps:
  - Validate a fixture where a plan body is `done` but `docs/plan.md` still lists it under Active.
  - Validate a fixture where review-resolution remains `open` during final closeout.
  - Validate a fixture where a blocking review outcome has no re-review or owner closeout.
  - Assert the final validation command set from the plan includes review-artifact closeout, change metadata, artifact lifecycle, generated skill drift, adapter drift, adapter validation, and CI.
- Expected result:
  - Final handoff cannot claim PR readiness with stale lifecycle state or unresolved review findings.
- Failure proves:
  - The change can pass implementation without the artifact state required by the workflow.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`

### T15. Review-artifact validation is local, deterministic, and safe

- Covers: `R11`, `R11a`, `R11b`, security/privacy, observability, performance
- Level: unit, integration
- Fixture/setup:
  - validator module and CLI
  - representative small and larger review-artifact fixtures
- Steps:
  - Inspect the validator for standard-library-only file parsing.
  - Run validation without network access, secrets, hosted CI, or external review tools.
  - Assert validation time scales with selected change-root Markdown files and does not build a repository-wide index by default.
  - Assert failure output avoids large excerpts and reports only path, line, ID, mode, and reason.
- Expected result:
  - Validation is safe to run locally and in CI without exposing sensitive content or requiring external services.
- Failure proves:
  - The implementation violates the approved security, privacy, or performance boundary.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`

### T16. Canonical skill updates regenerate Codex and public adapter outputs

- Covers: `R12`, `R12a`, `R12b`, `R12c`, `R14`, `R14a`, `E7`, edge case 15
- Level: integration, contract
- Fixture/setup:
  - canonical `skills/`
  - generated `.codex/skills/`
  - generated `dist/adapters/`
  - `dist/adapters/manifest.yaml`
- Steps:
  - Update canonical skill guidance for review-resolution behavior during implementation.
  - Run `python scripts/build-skills.py` and `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version 0.1.1` and `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Assert generated skill and adapter outputs contain the updated portable guidance and no unsupported tool-specific metadata leaks.
- Expected result:
  - Canonical review-resolution skill changes are reflected in all generated consumers or fail validation.
- Failure proves:
  - Public adapter packages or local Codex output can become stale after workflow guidance changes.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`

## Fixtures and data

Planned fixture root:

```text
tests/fixtures/review-artifacts/
```

Fixture families:

- valid structure fixtures: `valid-detailed-review`, `valid-review-log`, `valid-material-findings`, `valid-open-resolution`, `valid-closed-resolution`, `clean-review-with-log`, `no-review-artifacts`
- review record failures: `missing-review-fields`, `multiple-review-ids`, `duplicate-review-ids`, `reconstructed-missing-metadata`
- review-log failures: `missing-review-log`, `log-missing-review-id`, `log-unknown-review-id`, `log-duplicate-review-id`, `log-prose-review-id-only`, `log-missing-required-field`
- finding/resolution failures: `duplicate-finding-ids`, `missing-resolution-file`, `missing-resolution-entry`, `unknown-resolution-finding`, `unsupported-disposition`
- closeout failures: `open-closeout-status`, `needs-decision-open`, `accepted-missing-action`, `accepted-missing-evidence`, `deferred-missing-rationale`, `deferred-missing-followup`, `rejected-missing-rationale`, `partial-missing-subdecision`, `partial-missing-accepted-evidence`, `blocking-review-without-rerun`

Fixtures should use small Markdown files with the canonical labels from the spec and architecture. They should not contain secrets, private keys, host-specific paths, real credentials, or large copied review transcripts.

## Mocking/stubbing policy

- Use filesystem fixtures and temporary directories rather than mocks for parser and CLI behavior.
- Stub no external agent tools because non-smoke validation must not invoke them.
- Use controlled temporary git repositories or isolated changed-path fixtures for CI scope behavior when shell-level CI testing requires git state.
- Avoid snapshot-only tests. Assertions should check IDs, paths, status values, dispositions, required field presence, and exact failure reasons.

## Migration or compatibility tests

- Existing historical review artifacts must not be validated repository-wide by default. `T13` covers changed-root scoping.
- Existing loose table examples do not become accepted parser input for new artifacts. Parser fixtures should require label-based canonical forms.
- Review ID uniqueness is scoped to one change root. `T2` covers duplicate IDs across independent roots remaining valid.
- Generated public adapter package layout remains unchanged. `T16` covers sync without changing adapter package roots.
- Rollback compatibility is covered by keeping the validator isolated from change metadata and artifact lifecycle validators; reverting the new scripts must not break existing `change.yaml` or lifecycle validation.

## Observability verification

- `T9` asserts failure output includes path, line where available, Review ID or Finding ID where available, validation mode, and short reason.
- `T15` asserts output avoids large excerpts and remains deterministic.
- Successful validator runs may report counts for detailed reviews, findings, review-log entries, resolution entries, closeout status, and disposition counts. Tests may assert those counts when implemented, but count output is not required for the first passing validator if failure output is actionable.

## Security/privacy verification

- `T15` asserts validation uses local files only and requires no network, secrets, hosted CI, or external review tools.
- Fixture content must not include secrets, credentials, private keys, or sensitive runtime values.
- `T16` reuses adapter security validation to prove generated adapter updates do not add tool permissions, shell execution, model overrides, approval behavior, or unsupported metadata leaks.

## Performance checks

- `T15` should include a small stress fixture with multiple review files and findings to confirm validation is linear in selected change-root Markdown files.
- No cache, database, repository-wide index, or parallel worker is required for this version.
- CI tests should prove validation scope is selected by changed or explicit change roots rather than scanning all historical review artifacts.

## Manual QA checklist

- No manual QA is required for parser, validator, docs, or generated-output drift behavior.
- Manual review during `code-review` should inspect at least one real change-local review artifact created during this initiative to confirm the guidance is usable.
- Manual maintainer decisions remain required for any future `needs-decision` finding; automation only checks the recorded structure.

## What not to test

- Do not test whether review evidence is persuasive, whether a suggested solution is best, or whether a rationale is substantively correct. The spec explicitly defers semantic review-quality automation.
- Do not test real Codex, Claude Code, or OpenCode runtime behavior for this change. Public adapter generation is covered by existing adapter validation and generated-output checks.
- Do not require every historical change under `docs/changes/` to pass the new validator.
- Do not require empty review artifacts for clean reviews.
- Do not snapshot entire generated adapter packages; use deterministic generation and drift checks instead.

## Uncovered gaps

- None. All requirements have an automated or contract-test proof path.

## Next artifacts

- implement
- code-review
- verify
- explain-change
- pr

## Follow-on artifacts

- None yet.

## Readiness

- Active proof surface for M1 execution under `docs/plans/2026-04-25-review-finding-resolution-contract.md`.
