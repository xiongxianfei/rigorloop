# Record every formal review execution plan

- Status: active
- Owner: maintainer
- Start date: 2026-05-12
- Last updated: 2026-05-12
- Related issue or PR: none yet
- Supersedes: none

## Purpose / Big Picture

Implement the approved Record Every Formal Review contract so every supported formal lifecycle review creates durable review evidence or reports blocked recording.

The implementation must preserve the existing material-finding model while changing clean formal reviews from artifact-local-only evidence to lightweight review receipts indexed in `review-log.md`.

## Source Artifacts

- Proposal: [Record Every Formal Review](../proposals/2026-05-12-record-every-formal-review.md), accepted.
- Spec: [Formal Review Recording](../../specs/formal-review-recording.md), approved.
- Architecture: [System Architecture](../architecture/system/architecture.md), approved.
- Test spec: [Formal Review Recording Test Spec](../../specs/formal-review-recording.test.md), active and must be amended for this proposal before implementation.
- Review evidence: [record-every-formal-review change root](../changes/2026-05-12-record-every-formal-review-review-recording/change.yaml).

## Context and Orientation

The current executable review artifact model lives in:

- `scripts/review_artifact_validation.py`
- `scripts/validate-review-artifacts.py`
- `scripts/test-review-artifact-validator.py`
- `tests/fixtures/review-artifacts/`

The formal review contract is exposed to operators through:

- `templates/shared/review-isolation-and-recording.md`
- `skills/proposal-review/SKILL.md`
- `skills/spec-review/SKILL.md`
- `skills/architecture-review/SKILL.md`
- `skills/plan-review/SKILL.md`
- `skills/code-review/SKILL.md`

Generated local Codex runtime output under `.codex/skills/` is not authored or tracked. Public adapter package output under `dist/adapters/` remains tracked generated installable output during the compatibility window and must be refreshed when canonical skill text changes.

## Non-goals

- Do not add a new formal review stage or a dedicated `pr-review` stage.
- Do not create empty `review-resolution.md` files for clean reviews with no findings.
- Do not move artifact lifecycle/status settlement into review files.
- Do not backfill durable review files for old clean reviews unless a later scoped change requires it.
- Do not add semantic review-quality judgment to structural validators.

## Requirements Covered

- `R1`-`R5`: formal review scope, clean receipt trigger, artifact-local settlement boundary, minimal clean receipt root.
- `R8`-`R8f`: `review-log.md` indexing and clean receipt log entry fields.
- `R10`-`R10c`: `change.yaml.review` aggregate metadata boundary.
- `R14`-`R14e`: reviewed artifact status remains artifact-local.
- `R15`-`R15a`: review skill guidance and generated output alignment.
- `R16`-`R16b`: structural validator reuse.
- `R21`-`R21d`: shared `## Isolation and Recording` block consistency.
- `R24`-`R31p`: recording status vocabulary, artifact path output, complete finding shape, change-ID selection, concise skills.
- `R32`-`R32f`: examples remain non-normative and outside active lifecycle state.

## Current Handoff Summary

- Current milestone: M2. Review artifact and metadata validation
- Current milestone state: review-requested
- Last reviewed milestone: M2. Review artifact and metadata validation
- Review status: M2 code-review changes-requested; CR-M2-002 accepted and fixed, rerun review required
- Remaining in-scope implementation milestones: M2, M3, M4, M5
- Next stage: code-review M2 rerun
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M1 is closed and M2 is ready for code-review rerun, but M2-M5 remain open, explain-change and verify evidence do not exist, and PR handoff is not prepared.

## Milestones

### M1. Test spec and clean receipt fixtures

- Milestone state: closed
- Goal: Update the test spec and fixtures so the approved clean formal review receipt contract is testable before implementation.
- Requirements: `R2c`-`R5`, `R8d`-`R8f`, `R24`-`R26e`, `R31m`-`R31p`.
- Files/components likely touched:
  - `specs/formal-review-recording.test.md`
  - `tests/fixtures/review-artifacts/`
  - `docs/examples/formal-review-recording/`
- Dependencies: approved spec and architecture.
- Tests to add/update:
  - Add test-spec cases for isolated clean receipt roots, no `review-resolution.md`, `review-log.md` indexing, minimal `change.yaml.review`, blocked recording for ambiguous change ID, concise receipt shape, and examples as non-normative surfaces.
  - Add or update clean receipt fixtures used by validator tests.
- Implementation steps:
  - Amend requirement and example coverage maps so clean receipts no longer appear artifact-local-only.
  - Add test IDs for clean receipt roots and receipt log entries.
  - Add non-normative filled examples for a clean receipt root when useful.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/formal-review-recording.test.md --path specs/formal-review-recording.md`
  - `git diff --check -- specs/formal-review-recording.test.md tests/fixtures/review-artifacts docs/examples/formal-review-recording`
- Expected observable result: the test spec names concrete executable and manual checks for every new clean-receipt requirement.
- Commit message: `M1: add clean review receipt test coverage`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] hand off to code-review for M1
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone state updated before starting M2
- Risks: fixture shape may not match current validator parsing.
- Rollback/recovery: revert the fixture additions and keep the amended test spec as the guide for M2 if fixture implementation needs to move with validator code.

### M2. Review artifact and metadata validation

- Milestone state: review-requested
- Goal: Teach repository validation to accept and reject clean receipt roots according to the approved spec.
- Requirements: `R4h`-`R4l`, `R8d`-`R8f`, `R10`-`R10c`, `R16`-`R16b`, `R24`-`R26e`.
- Files/components likely touched:
  - `scripts/review_artifact_validation.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/change-metadata/`
- Dependencies: M1 test cases and fixtures.
- Tests to add/update:
  - Positive clean receipt root with `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md`.
  - Negative clean receipt root with missing log entry, nonzero material count, missing required receipt metadata, or unexpected empty `review-resolution.md` when no trigger exists.
  - Metadata validation for reviewed artifact, review-log path, review status, and unresolved item count `0`.
- Implementation steps:
  - Reuse the existing review artifact parser and avoid a second review-record model.
  - Add structural recognition for clean receipt entries and concise required fields.
  - Preserve existing material-finding closeout behavior unchanged.
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-record-every-formal-review-review-recording`
  - `git diff --check -- scripts tests/fixtures`
- Expected observable result: clean receipt roots validate structurally without requiring `review-resolution.md`, while malformed or ambiguous clean receipt evidence fails.
- Commit message: `M2: validate clean formal review receipts`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] hand off to code-review for M2
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone state updated before starting M3
- Risks: tightening `review-log.md` parsing could break historical review records.
- Rollback/recovery: keep new checks fixture-scoped first; if historical records fail, document the compatibility rule and add explicit legacy handling rather than weakening new clean receipt validation.

### M3. Formal review skill and governance alignment

- Milestone state: planned
- Goal: Update formal review skills and governing guidance so operators create clean receipts for every formal review and reserve `not-required` for non-formal requests.
- Requirements: `R14`-`R15a`, `R21`-`R31p`.
- Files/components likely touched:
  - `templates/shared/review-isolation-and-recording.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`
- Dependencies: M1 and M2 clarify executable vocabulary.
- Tests to add/update:
  - Static skill validation that formal review output uses `recorded | blocked`, does not use `not-required` for formal lifecycle review invocations, points to the central spec for long rules, and keeps the shared block byte-equal across formal review skills.
  - Static checks that governance no longer states clean formal reviews may settle artifact-locally without a receipt.
- Implementation steps:
  - Update the shared review-skill block once, then copy it into the formal review skills.
  - Keep public skill wording concise and refer to `specs/formal-review-recording.md` for detailed receipt shape and change-ID selection.
  - Update governance and workflow summaries only where they conflict with the approved spec.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/formal-review-recording.md`
  - `git diff --check -- templates/shared skills CONSTITUTION.md AGENTS.md docs/workflows.md scripts`
- Expected observable result: formal review skills and governing docs consistently require a receipt or blocked recording for every formal lifecycle review.
- Commit message: `M3: align formal review skills with receipt recording`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] hand off to code-review for M3
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] milestone state updated before starting M4
- Risks: copied shared sections can drift across skills.
- Rollback/recovery: regenerate copied blocks from the shared template and use the static validator to identify the exact divergent skill.

### M4. Generated outputs and adapter validation

- Milestone state: planned
- Goal: Refresh generated skill outputs after canonical skill changes and validate local and public adapter packages.
- Requirements: `R15a`.
- Files/components likely touched:
  - `.codex/skills/` generated local runtime output, untracked
  - `dist/adapters/` tracked generated public adapter output
- Dependencies: M3 canonical skill edits.
- Tests to add/update: no new tests expected; run existing generation and adapter validation.
- Implementation steps:
  - Regenerate local Codex runtime mirror with the repository script when useful for local execution.
  - Regenerate tracked public adapter output after canonical skill updates.
  - Validate generated output and adapter packaging.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `git diff --check -- dist/adapters`
- Expected observable result: generated local Codex mirror is reproducible and tracked public adapters match canonical skill text.
- Commit message: `M4: refresh generated review skill adapters`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] hand off to code-review for M4
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] milestone state updated before starting M5
- Risks: adapter generation may update unrelated generated files due to prior drift.
- Rollback/recovery: inspect generated diffs before keeping them; if unrelated drift appears, isolate the cause and do not hand-edit generated output.

### M5. Lifecycle state, explanation, verification, and PR readiness

- Milestone state: planned
- Goal: Close the planned initiative only after all implementation milestones, reviews, resolution records, explanation, and final verification are synchronized.
- Requirements: all touched requirements, with emphasis on lifecycle consistency.
- Files/components likely touched:
  - `docs/changes/2026-05-12-record-every-formal-review-review-recording/`
  - `docs/plans/2026-05-12-record-every-formal-review.md`
  - `docs/plan.md`
- Dependencies: M1-M4 closed.
- Tests to add/update: none expected; this is lifecycle closeout.
- Implementation steps:
  - Record `explain-change` evidence after implementation and review resolution.
  - Run final `verify`.
  - Update the active plan and plan index consistently before PR handoff.
  - Prepare PR summary from the real diff and validation evidence.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-record-every-formal-review-review-recording`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-record-every-formal-review.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-12-record-every-formal-review.md --path docs/plan.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml --path docs/changes/2026-05-12-record-every-formal-review-review-recording/review-log.md`
  - `bash scripts/ci.sh --mode explicit --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path scripts/review_artifact_validation.py --path scripts/test-review-artifact-validator.py --path templates/shared/review-isolation-and-recording.md --path skills/spec-review/SKILL.md --path skills/code-review/SKILL.md --path dist/adapters`
  - `git diff --check`
- Expected observable result: all review-recording artifacts, lifecycle state, generated output, and validation evidence are coherent and ready for PR handoff.
- Commit message: `M5: close record-every-formal-review lifecycle`
- Milestone closeout:
  - [ ] final validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] explain-change recorded
  - [ ] verify recorded
  - [ ] plan body and plan index synchronized
  - [ ] PR handoff prepared
- Risks: final closeout can become stale if review-resolution or plan state changes after verify.
- Rollback/recovery: rerun review artifact and lifecycle validation after any closeout metadata edit before PR handoff.

## Validation Plan

Use the milestone validation commands above. The minimum final validation target is:

- focused unit tests for review artifact and change metadata validation;
- skill validation for canonical formal review skills;
- skill generation and adapter validation after canonical skill changes;
- explicit-path lifecycle validation for touched lifecycle artifacts;
- review artifact closeout validation for the active change root;
- `git diff --check`.

Broader `scripts/ci.sh` runs are not required unless plan-review, code-review, changed selectors, or maintainer direction expand the validation surface.

## Risks and Recovery

- Historical review records may not match the new clean receipt log shape. Recovery: keep new stricter checks scoped to clean receipt records while preserving existing material record compatibility.
- Formal review skill wording may grow too long. Recovery: centralize normative details in `specs/formal-review-recording.md` and filled examples under `docs/examples/formal-review-recording/`.
- Generated public adapters may show broad drift. Recovery: regenerate from canonical `skills/`, inspect drift, and do not hand-edit `dist/adapters/`.
- Lifecycle status may drift between `docs/plan.md`, this plan, and change-local metadata. Recovery: validate explicit paths and synchronize lifecycle surfaces before review and PR handoff.

## Dependencies

- Plan-review must approve or request changes before implementation starts.
- Test-spec updates must precede validator or skill implementation.
- Generated output refresh depends on canonical skill edits.
- Final PR readiness depends on code-review closeout for each implementation milestone, explain-change evidence, final verify, and synchronized plan state.

## Progress

- 2026-05-12: Created execution plan after accepted proposal, approved spec, approved architecture update, and clean architecture review.
- 2026-05-12: Plan-review approved the plan with no material findings.
- 2026-05-12: Updated `specs/formal-review-recording.test.md` for the record-every-formal-review clean receipt implementation slice.
- 2026-05-12: Implemented M1 by adding the clean receipt root fixture and non-normative clean receipt example, then handed M1 to code-review.
- 2026-05-12: Code-review M1 passed with no material findings and M1 moved to closed.
- 2026-05-12: Implemented M2 by adding clean receipt review-log table parsing, no-empty-resolution validation for clean roots, and minimal `change.yaml.review` semantic checks.
- 2026-05-12: Code-review M2 found material finding `CR-M2-001`; M2 moved to resolution-needed.
- 2026-05-12: Implemented the accepted `CR-M2-001` fix by adding shared clean receipt root metadata semantics and negative validator coverage; M2 returned to review-requested.
- 2026-05-12: Code-review M2 rerun found material finding `CR-M2-002`; M2 moved to resolution-needed.
- 2026-05-12: Implemented the accepted `CR-M2-002` fix by requiring `review.status: clean` for clean-root-shaped metadata; M2 returned to review-requested.

## Decision Log

- 2026-05-12: Split implementation into test-spec, validation, skill/governance, generated-output, and lifecycle-closeout milestones so each slice has a coherent review boundary.
- 2026-05-12: Treat `specs/formal-review-recording.test.md` as stale for the new amendment and update it before code changes.

## Surprises and Discoveries

- The existing shared review-skill block still allows `Recording status: not-required` for formal reviews. M3 must remove that formal-review path while preserving `not-required` only for non-formal review-like requests if still documented elsewhere.
- The existing test spec still includes old clean-review artifact-local-only coverage and must be amended before validator implementation.
- The new clean receipt root fixture intentionally exposes the current review-artifact parser gap: it fails structure validation because table-based clean receipt log entries are not parsed yet. M2 owns that validator support.
- `python scripts/test-review-artifact-validator.py` exposed a pre-existing alignment gap: `skills/workflow/SKILL.md` named `needs-decision` but not the supported `partially-accepted` disposition. M2 fixed the smallest canonical wording mismatch so the existing contract-alignment test passes.
- `CR-M2-001` showed the positive clean receipt fixture was insufficient proof for the minimal `change.yaml.review` contract. The fix adds negative tests for missing or invalid clean receipt root metadata.
- `CR-M2-002` showed invalid status still passes: a validator-identified clean receipt root with `review.status: approved` is accepted. The next M2 fix must require `review.status: clean` under strict clean-root validation.
- The `CR-M2-002` fix needed a narrower trigger than any metadata with `review_log`; active change metadata can legitimately carry `review_log` while not being a clean receipt root.

## Validation Notes

- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml` passed.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-record-every-formal-review-review-recording` passed with 3 reviews, 1 finding, 3 log entries, and 1 resolution entry.
- 2026-05-12: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-record-every-formal-review.md --path specs/formal-review-recording.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-12-record-every-formal-review.md --path docs/plan.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml --path docs/changes/2026-05-12-record-every-formal-review-review-recording/review-log.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/review-resolution.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/reviews/spec-review-r1.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/reviews/spec-review-r2.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/reviews/architecture-review-r1.md` passed after removing an unrelated lifecycle-language warning in `docs/plan.md`.
- 2026-05-12: `git diff --check -- docs/plan.md docs/plans/2026-05-12-record-every-formal-review.md docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml` passed.
- 2026-05-12: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/formal-review-recording.test.md --path specs/formal-review-recording.md --path docs/plans/2026-05-12-record-every-formal-review.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml` passed after test-spec update.
- 2026-05-12: `git diff --check -- specs/formal-review-recording.test.md docs/plans/2026-05-12-record-every-formal-review.md docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml` passed after test-spec update.
- 2026-05-12: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/formal-review-recording.test.md --path specs/formal-review-recording.md` passed for M1.
- 2026-05-12: `python scripts/validate-change-metadata.py tests/fixtures/review-artifacts/valid-clean-receipt-root/change.yaml` passed for the clean receipt root fixture.
- 2026-05-12: `git diff --check -- specs/formal-review-recording.test.md tests/fixtures/review-artifacts docs/examples/formal-review-recording` passed for M1.
- 2026-05-12: `wc -w tests/fixtures/review-artifacts/valid-clean-receipt-root/reviews/spec-review-r1.md docs/examples/formal-review-recording/clean-review-receipt-root.md` reported 66 words for the clean receipt fixture and 183 words for the example file.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode structure tests/fixtures/review-artifacts/valid-clean-receipt-root` failed as expected before M2 with `Review ID missing from review-log.md`; current parser does not yet support table-based clean receipt log entries.
- 2026-05-12: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-record-every-formal-review.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-12-record-every-formal-review.md --path docs/plan.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml --path docs/changes/2026-05-12-record-every-formal-review-review-recording/review-log.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/review-resolution.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/reviews/spec-review-r1.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/reviews/spec-review-r2.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/reviews/architecture-review-r1.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/reviews/plan-review-r1.md` passed for M1.
- 2026-05-12: `code-review M1` recorded clean-with-notes with no material findings.
- 2026-05-12: `python scripts/test-review-artifact-validator.py` passed for M2 with 34 tests.
- 2026-05-12: `python scripts/test-change-metadata-validator.py` passed for M2 with 6 tests.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-record-every-formal-review-review-recording` passed for M2 with 5 reviews, 1 finding, 5 log entries, and 1 resolution entry.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode structure tests/fixtures/review-artifacts/valid-clean-receipt-root` passed for M2 with 1 review, 0 findings, 1 log entry, and 0 resolution entries.
- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml tests/fixtures/review-artifacts/valid-clean-receipt-root/change.yaml` passed for M2.
- 2026-05-12: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/formal-review-recording.test.md --path specs/formal-review-recording.md --path docs/plans/2026-05-12-record-every-formal-review.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml` passed for M2 state sync.
- 2026-05-12: `git diff --check -- scripts tests/fixtures docs/examples/formal-review-recording skills/workflow/SKILL.md` passed for M2.
- 2026-05-12: `code-review M2` recorded material finding `CR-M2-001`: clean receipt root metadata validation accepts missing `review.reviewed_artifact` and nonzero `review.unresolved_items`.
- 2026-05-12: `python scripts/test-review-artifact-validator.py` passed for the `CR-M2-001` fix with 35 tests.
- 2026-05-12: `python scripts/test-change-metadata-validator.py` passed for the `CR-M2-001` fix with 7 tests.
- 2026-05-12: `python scripts/validate-change-metadata.py tests/fixtures/review-artifacts/valid-clean-receipt-root/change.yaml` passed for the `CR-M2-001` fix.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode structure tests/fixtures/review-artifacts/valid-clean-receipt-root` passed for the `CR-M2-001` fix with 1 review, 0 findings, 1 log entry, and 0 resolution entries.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-record-every-formal-review-review-recording` passed for the `CR-M2-001` fix with 6 reviews, 2 findings, 6 log entries, and 2 resolution entries.
- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml tests/fixtures/review-artifacts/valid-clean-receipt-root/change.yaml` passed for the `CR-M2-001` fix.
- 2026-05-12: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/formal-review-recording.test.md --path specs/formal-review-recording.md --path docs/plans/2026-05-12-record-every-formal-review.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml` passed for the `CR-M2-001` fix state sync.
- 2026-05-12: `git diff --check --` passed for the `CR-M2-001` fix.
- 2026-05-12: `code-review M2 rerun` recorded material finding `CR-M2-002`: clean receipt root metadata validation accepts `review.status: approved`.
- 2026-05-12: `python scripts/test-review-artifact-validator.py` passed for the `CR-M2-002` fix with 35 tests.
- 2026-05-12: `python scripts/test-change-metadata-validator.py` passed for the `CR-M2-002` fix with 7 tests.
- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml tests/fixtures/review-artifacts/valid-clean-receipt-root/change.yaml` passed for the `CR-M2-002` fix.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode structure tests/fixtures/review-artifacts/valid-clean-receipt-root` passed for the `CR-M2-002` fix with 1 review, 0 findings, 1 log entry, and 0 resolution entries.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-record-every-formal-review-review-recording` passed for the `CR-M2-002` fix with 7 reviews, 3 findings, 7 log entries, and 3 resolution entries.
- 2026-05-12: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/formal-review-recording.test.md --path specs/formal-review-recording.md --path docs/plans/2026-05-12-record-every-formal-review.md --path docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml` passed for the `CR-M2-002` fix state sync.
- 2026-05-12: `git diff --check --` passed for the `CR-M2-002` fix.

## Outcome and Retrospective

- Not started. Fill after all implementation milestones, reviews, final verification, and PR handoff are complete.

## Readiness

- See `Current Handoff Summary`.

## Risks and Follow-ups

- A later workflow change may add `test-spec-review` as a formal lifecycle review stage, but this plan intentionally does not add or validate that stage.
