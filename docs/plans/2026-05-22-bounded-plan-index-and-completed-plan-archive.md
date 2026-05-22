# Bounded Plan Index and Completed-Plan Archive

## Status

active

Plan lifecycle state: active
Terminal disposition: none

## Purpose / big picture

This plan sequences the accepted bounded plan-index archive contract into reviewable work. The change keeps `docs/plan.md` focused on active orientation, creates `docs/plan-archive.md` for older terminal history, preserves every completed plan entry, and adds validator-owned rules for terminal plan conservation and active supersession context.

## Source artifacts

- Proposal: `docs/proposals/2026-05-22-bounded-plan-index-and-completed-plan-archive.md`
- Spec: `specs/plan-index-lifecycle-ownership.md`
- Architecture: not required; this is a repository workflow and validation contract change with no new runtime architecture boundary.
- Test spec: `specs/plan-index-lifecycle-ownership.test.md`
- Proposal review: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/proposal-review-r1.md`
- Spec review: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/spec-review-r2.md`
- Review resolution: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-resolution.md`

## Context and orientation

`docs/plan.md` is currently the common-read plan index and still contains the full historical `Done` list. The accepted spec now treats `docs/plan.md` and `docs/plan-archive.md` as plan index surfaces. `docs/plan.md` remains the first-read orientation file for complete Active and Blocked sections, recent Done history, and active supersession context. `docs/plan-archive.md` stores older terminal history.

The main implementation surfaces are:

- `docs/plan.md`
- `docs/plan-archive.md`
- `docs/plans/*.md` plan-body lifecycle markers
- `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md`
- `specs/plan-index-lifecycle-ownership.test.md`
- `scripts/artifact_lifecycle_validation.py`
- `scripts/artifact_lifecycle_contracts.py`
- `scripts/test-artifact-lifecycle-validator.py`
- `scripts/validation_selection.py`
- `scripts/test-select-validation.py`
- `docs/workflows.md`, `AGENTS.md`, and `skills/plan/SKILL.md` if guidance needs to describe archive maintenance
- generated skill/adapters only if canonical skill text changes

## Non-goals

- Do not delete completed plan records.
- Do not remove plan files from `docs/plans/`.
- Do not change milestone, review, verification, PR, or closeout semantics.
- Do not implement a generated plan-index registry.
- Do not add CLI or scaffolding support for plan index maintenance.
- Do not bulk-rewrite unrelated plan bodies except for lifecycle markers and index/archive migration surfaces needed by this contract.
- Do not make `docs/plan-archive.md` the first-read orientation file.

## Requirements covered

- `R1`, `R2`, `R2a`: M1, M4
- `R3`, `R3a`-`R3p`: M1, M2, M3
- `R4`, `R5`, `R6`, `R6a`, `R6b`: M4, M5
- `R7`, `R7a`: M2, M5
- `R8`, `R8a`: M1, M4
- `R9`: M3
- `R10`, `R10a`: M2, M3
- `R11`, `R11a`, `R12`: M2, M3
- `R13`, `R14`: M2, M3
- `R15`, `R15a`-`R15d`: M2
- `R16`: M3
- `R17`, `R17a`-`R17i`: M2, M3

## Current Handoff Summary

- Current milestone: M5. Selection and CI routing
- Current milestone state: planned
- Last reviewed milestone: M4. Contributor guidance and skill alignment
- Review status: code-review M4 R2 clean-with-notes; no open findings
- Remaining in-scope implementation milestones: M5, M6
- Next stage: implement M5
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation milestones, code review, review-resolution if triggered, explain-change, verify, and PR handoff remain.

## Milestones

### M1. Test-spec refresh

- Milestone state: closed
- Goal: Update the archived plan-index lifecycle test spec into an active proof map for the archive contract before implementation.
- Requirements: `R1`, `R2`, `R2a`, `R3`, `R3a`-`R3p`, `R8`, `R8a`, `R10`, `R10a`, `R15`, `R15a`-`R15d`, `R16`, `R17`, `R17a`-`R17i`
- Files/components likely touched:
  - `specs/plan-index-lifecycle-ownership.test.md`
  - `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-log.md` only if review evidence changes
- Dependencies:
  - Approved spec status and clean `spec-review-r2`
- Tests to add/update:
  - Test cases for lifecycle marker parsing, terminal conservation, archive cap, archive links, active-work archive rejection, migration proof, and supersession markers.
- Implementation steps:
  - Normalize the test spec status out of archived state for this amendment.
  - Add coverage for `BPIX-T-STATE-*` and `BPIX-T-SUPER-*` cases from the accepted review-resolution guidance.
  - Map every new `MUST` in the spec to test or manual proof coverage.
  - Keep old lifecycle ownership tests that still apply, updating terminology from single plan index to plan index surfaces.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md`
  - `git diff --check --`
- Expected observable result: test spec is ready for `spec-review` or, if this milestone is handled as `test-spec`, ready for downstream implementation proof.
- Commit message: `M1: refresh plan index archive test spec`
- Milestone closeout:
  - validation passed on 2026-05-22
  - progress updated
  - decision log unchanged
  - validation notes updated
  - milestone not committed in this working tree
- Risks:
  - Risk: test spec misses a new validator-owned requirement.
- Rollback/recovery:
  - Restore the previous test spec and stop for spec/test-spec reconciliation.

### M2. Validator contract and fixtures

- Milestone state: closed
- Goal: Implement structural validation for plan index surfaces, explicit plan-body lifecycle markers, terminal-plan conservation, recent Done cap, one-line terminal entries, and active supersession markers.
- Requirements: `R3`, `R3a`-`R3p`, `R7`, `R7a`, `R10`, `R10a`, `R11`, `R11a`, `R12`, `R13`, `R14`, `R15`, `R15a`-`R15d`, `R17`, `R17a`-`R17i`
- Files/components likely touched:
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/artifact_lifecycle_contracts.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/artifact-lifecycle/**`
- Dependencies:
  - M1 test-spec refresh or equivalent approved proof map
- Tests to add/update:
  - Valid terminal marker fixture.
  - Valid active marker fixture.
  - Invalid contradictory marker fixture.
  - Unknown marker value fixture.
  - Legacy prose-only no-inference fixture.
  - Terminal missing from both recent and archive fixture.
  - Terminal duplicated across recent and archive fixture.
  - Valid active supersession fixture.
  - Missing replacement link, missing `active-context:`, blank rationale, and archived `active-context:` fixtures.
- Implementation steps:
  - Add parser support for top-level `## Status` lifecycle marker fields without prose matching.
  - Add plan index/archive parsing for `Done (recent)` and `Done (archive)`.
  - Add terminal conservation checks for explicit lifecycle markers.
  - Add cap, link, one-line shape, archive-only nonterminal, duplicate, and active supersession structural checks.
  - Keep semantic quality of summaries and active-context rationale review-owned.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md`
  - `python -m py_compile scripts/artifact_lifecycle_validation.py scripts/artifact_lifecycle_contracts.py`
  - `git diff --check --`
- Expected observable result: validator accepts valid index/archive state and rejects missing, duplicate, malformed, contradictory, and archive-placement failures with stable diagnostics.
- Commit message: `M2: validate plan index archive contract`
- Milestone closeout:
  - validation passed on 2026-05-22
  - progress updated
  - decision log updated
  - validation notes updated
  - milestone commit included in M2 handoff commit
- Risks:
  - Risk: parser overfits current prose-heavy plan bodies.
- Rollback/recovery:
  - Revert validator changes and fixtures together; keep the spec/test-spec pending until a deterministic parser path is restored.

### M3. Index/archive migration and preservation proof

- Milestone state: closed
- Goal: Create `docs/plan-archive.md`, compact `docs/plan.md`, move older terminal history, add plan-body lifecycle markers where needed, and record migration proof.
- Requirements: `R3c`, `R3d`, `R3e`, `R3f`, `R3g`-`R3p`, `R9`, `R10`, `R10a`, `R11`, `R11a`, `R12`, `R13`, `R14`, `R16`, `R17`, `R17a`-`R17i`
- Files/components likely touched:
  - `docs/plan.md`
  - `docs/plan-archive.md`
  - relevant `docs/plans/*.md` lifecycle marker surfaces
  - `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md`
- Dependencies:
  - M2 validator support, so migration can be checked structurally
- Tests to add/update:
  - Migration proof table with pre/post counts, link preservation, duplicate status, terminal disposition, and new location.
- Implementation steps:
  - Inventory pre-migration Done entries and plan links.
  - Create `docs/plan-archive.md` with older terminal history in newest-first order.
  - Keep at most 10 Done entries in `docs/plan.md`.
  - Add archive pointer and index policy comment to `docs/plan.md`.
  - Add explicit lifecycle-state markers to plan bodies required by the migration and active plan updates.
  - Record `plan-index-migration.md` with count conservation and link validation.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `git diff --check --`
- Expected observable result: every pre-migration Done entry is present in either `docs/plan.md` recent Done or `docs/plan-archive.md`, no terminal entry is duplicated, and active/blocked work remains in `docs/plan.md`.
- Commit message: `M3: migrate completed plan history to archive`
- Milestone closeout:
  - validation passed on 2026-05-22
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed in `ab69942`
  - code-review M3 R1 clean-with-notes
- Risks:
  - Risk: a dense historical Done entry loses useful disposition during compaction.
- Rollback/recovery:
  - Move archived entries back to `docs/plan.md` from the migration proof and remove `docs/plan-archive.md` only after count conservation is restored.

### M4. Contributor guidance and skill alignment

- Milestone state: closed
- Goal: Make archive maintenance, lifecycle markers, and active supersession structure discoverable in contributor-facing guidance.
- Requirements: `R4`, `R5`, `R6`, `R6a`, `R6b`, `R8`, `R8a`, `R17`, `R17a`-`R17i`
- Files/components likely touched:
  - `docs/workflows.md`
  - `AGENTS.md`
  - `docs/examples/plans/example-plan.md`
  - `skills/plan/SKILL.md`
  - generated skill/adapters only if canonical skill text changes
- Dependencies:
  - M2 validator behavior and M3 migration shape, so guidance matches actual accepted structure
- Tests to add/update:
  - Skill validation or generated-output checks if `skills/plan/SKILL.md` changes.
  - Artifact lifecycle explicit-path checks for touched guidance.
- Implementation steps:
  - Update workflow and root guidance only where the new archive contract changes contributor behavior.
  - Update example plan status marker if needed.
  - Update `plan` skill wording if archive maintenance becomes part of plan-index bookkeeping.
  - Rebuild or validate generated artifacts only when canonical skill changes require it.
- Validation commands:
  - `python scripts/validate-skills.py skills/plan/SKILL.md` if `skills/plan/SKILL.md` changes
  - `python scripts/validate-skills.py` if any skill changes
  - `python scripts/build-skills.py --check` if any skill changes
  - `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>` if public adapter output needs proof
  - `python scripts/validate-adapters.py --root <tmpdir> --version <version>` if adapter output needs proof
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path AGENTS.md --path docs/examples/plans/example-plan.md`
  - `git diff --check --`
- Expected observable result: contributors can discover when to update `docs/plan.md`, when to update `docs/plan-archive.md`, and how to mark plan lifecycle state without chat history.
- Commit message: `M4: document plan archive maintenance`
- Milestone closeout:
  - validation passed on 2026-05-22
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed in `2d7dd3c`
  - BPIX-M4-CR1 fix committed in `26332f1`
  - code-review M4 R2 clean-with-notes
- Risks:
  - Risk: guidance duplicates too much spec detail.
- Rollback/recovery:
  - Revert guidance changes and leave the normative contract in the spec until concise wording is ready.

### M5. Selection and CI routing

- Milestone state: planned
- Goal: Ensure selected validation routes changes to `docs/plan-archive.md`, lifecycle markers, migration proof, and plan-index changes through the right local checks.
- Requirements: `R7`, `R7a`, `R15`, `R15a`-`R15d`, `R16`
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - possibly `scripts/ci.sh` only if selected-CI routing requires wrapper recognition
- Dependencies:
  - M2 validator command surface
  - M3 migration proof path
- Tests to add/update:
  - Selector cases for `docs/plan-archive.md`.
  - Selector cases for `docs/changes/<change-id>/plan-index-migration.md`.
  - Selector cases ensuring `docs/plan.md` and archive changes include lifecycle validation.
- Implementation steps:
  - Add or adjust artifact classification for `docs/plan-archive.md`.
  - Add migration-proof routing if needed.
  - Preserve existing selected check semantics for unrelated artifacts.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/ci.sh --select-only` if available and relevant
  - `git diff --check --`
- Expected observable result: changed plan index/archive surfaces select the validator checks needed to enforce the archive contract.
- Commit message: `M5: route plan archive validation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Risk: selector changes accidentally broaden CI for unrelated docs.
- Rollback/recovery:
  - Revert selector changes and require explicit validation commands in the plan until routing is corrected.

### M6. Lifecycle closeout and handoff evidence

- Milestone state: planned
- Goal: Complete explanation, final validation, lifecycle state synchronization, and PR handoff without claiming Done before required gates are complete.
- Requirements: `R3`, `R3a`-`R3p`, `R4`, `R5`, `R7`, `R7a`, `R8`, `R8a`, `R15`, `R15a`-`R15d`
- Files/components likely touched:
  - `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/explain-change.md`
  - `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/change.yaml` if change metadata is introduced by implementation
  - this plan
  - `docs/plan.md`
- Dependencies:
  - M1-M5 closed or explicitly removed with rationale
  - all required code reviews and review-resolution closed
- Tests to add/update:
  - Final selected validation and broad smoke as required by active test spec and plan.
- Implementation steps:
  - Record explain-change.
  - Run final validation commands from the active test spec and this plan.
  - Synchronize `docs/plan.md` and this plan's current handoff state before PR handoff.
  - Prepare PR handoff evidence.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md`
  - `bash scripts/ci.sh` unless the approved test spec names a narrower final scope
  - `git diff --check --`
- Expected observable result: final handoff evidence names commands run, remaining gates, lifecycle state, and PR readiness only after verify owns branch readiness.
- Commit message: `M6: record plan archive closeout evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Risk: final lifecycle state between `docs/plan.md` and this plan drifts.
- Rollback/recovery:
  - Restore the last synchronized Active state and rerun lifecycle validation before handoff.

## Validation plan

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-bounded-plan-index-and-completed-plan-archive.md --path specs/plan-index-lifecycle-ownership.md --path docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md --path docs/plan.md`: validate proposal, spec, active plan, and plan index surfaces.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive`: validate recorded review closeout.
- `python scripts/test-artifact-lifecycle-validator.py`: validate artifact lifecycle behavior after validator changes.
- `python scripts/test-select-validation.py`: validate selected-CI routing after archive routing changes.
- `python scripts/validate-skills.py` and `python scripts/build-skills.py --check`: run only if canonical skill text changes.
- `bash scripts/ci.sh`: final broad validation unless the approved test spec names a narrower final scope.
- `git diff --check --`: whitespace and patch hygiene.

## Risks and recovery

- Risk: migration drops a historical Done entry.
  - Recovery: use `plan-index-migration.md` count conservation to restore missing entries before validation can pass.
- Risk: validator infers lifecycle state from prose despite the spec.
  - Recovery: add a failing legacy prose-only fixture and remove broad prose matching.
- Risk: active or blocked work moves to the archive.
  - Recovery: restore the entry to `docs/plan.md`, add fixture coverage, and rerun lifecycle validation.
- Risk: guidance and validator contract diverge.
  - Recovery: keep the spec as source of truth, update guidance, and rerun artifact lifecycle and skill validation.
- Risk: generated output becomes stale after skill edits.
  - Recovery: rebuild or validate generated skill/adapters from canonical `skills/` before review.

## Dependencies

- Approved proposal and approved spec are present.
- Test-spec refresh must happen before implementation relies on new validator behavior.
- Plan-review must approve sequencing before implementation starts.
- Code review is required for each implementation milestone.
- Review-resolution runs if material findings are raised.
- Final closeout waits for all in-scope implementation milestones and required review-resolution to close.

## Progress

- 2026-05-22: Proposal created and accepted after proposal-review.
- 2026-05-22: Spec amended for archive contract, deterministic lifecycle markers, and active supersession structure.
- 2026-05-22: Spec-review R1 findings `BPIX-SR1` and `BPIX-SR2` resolved; spec-review R2 approved.
- 2026-05-22: Execution plan created and indexed as Active.
- 2026-05-22: Plan-review R1 approved the execution plan.
- 2026-05-22: Test spec refreshed from archived historical baseline to active proof map for the archive contract.
- 2026-05-22: Maintainer approved the active test spec for M2 implementation.
- 2026-05-22: Began M2 implementation.
- 2026-05-22: Added artifact-lifecycle validator support and tests for plan-body lifecycle markers, `docs/plan-archive.md`, terminal conservation, recent Done cap, terminal entry links, archive-only nonterminal rejection, and active supersession markers.
- 2026-05-22: M2 implementation reached `review-requested`; next stage is code-review for M2 before M3 migration begins.
- 2026-05-22: Code-review M2 R1 found BPIX-M2-CR1; terminal conservation does not run for plan-body-only explicit terminal marker changes.
- 2026-05-22: Resolved BPIX-M2-CR1 by adding the plan-body-only terminal conservation regression and extending the conservation trigger to scoped explicit terminal plan bodies.
- 2026-05-22: Code-review M2 R2 passed clean-with-notes; M2 closed and M3 is next.
- 2026-05-22: Began M3 migration, compacted `docs/plan.md` to Active, Blocked, Done (recent), and Superseded, created `docs/plan-archive.md`, and recorded `plan-index-migration.md`.
- 2026-05-22: Preserved all 75 pre-migration Done entries: 10 remain in `docs/plan.md` Done (recent), 65 moved to `docs/plan-archive.md`, and the migration table records every link with duplicate status.
- 2026-05-22: M3 implementation reached `review-requested`; next stage is code-review for M3 before contributor guidance work begins.
- 2026-05-22: Code-review M3 R1 passed clean-with-notes; M3 closed and M4 is next.
- 2026-05-22: Began M4 guidance alignment, updated workflow guidance, root agent guidance, the example plan, and the `plan` skill with archive maintenance, explicit lifecycle marker, and active supersession wording.
- 2026-05-22: M4 implementation reached `review-requested`; next stage is code-review for M4 before validation selector routing work begins.
- 2026-05-22: Code-review M4 R1 found BPIX-M4-CR1; plan guidance does not explicitly cover all R8a ownership bullets.
- 2026-05-22: Resolved BPIX-M4-CR1 by adding the missing R8a ownership bullets to `skills/plan/SKILL.md` and strengthening T14 to require direct per-surface ownership checks.
- 2026-05-22: Code-review M4 R2 passed clean-with-notes; M4 closed and M5 is next.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-22 | Sequence test-spec refresh before validator implementation. | The approved spec introduced new terminal-marker and supersession contracts that need traceable tests before code changes. | Implement validator first and infer tests afterward. |
| 2026-05-22 | Split validator implementation from index/archive migration. | The migration should run against an implemented proof mechanism rather than depending on manual inspection alone. | Migrate first, then add validator support. |
| 2026-05-22 | Keep guidance updates after validator and migration shape are known. | Contributor guidance should describe the actual accepted surfaces and avoid premature wording churn. | Update skills before the archive shape is validated. |
| 2026-05-22 | Count active supersession context as a valid terminal superseded location for validator purposes. | The approved spec allows superseded entries to remain in `docs/plan.md` only when they carry structural active context; otherwise they move to the archive. | Require all superseded terminal plans to appear only in Done recent/archive. |

## Surprises and discoveries

- PR #84 changed lifecycle validation internals before this plan was authored; the branch was synced to `origin/main` before planning.
- Existing `specs/plan-index-lifecycle-ownership.test.md` is archived and needs a focused refresh for the archive contract.
- Legacy prose-only completed plan bodies were not bulk-edited with lifecycle markers in M3; preservation for historical Done entries is recorded in the migration proof as required by EC10.
- M4 did not change generated adapter source in-tree; adapter proof used a temporary output directory for build/validation instead.

## Validation notes

- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-bounded-plan-index-and-completed-plan-archive.md --path specs/plan-index-lifecycle-ownership.md --path docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md --path docs/plan.md` passed with existing lifecycle-language warnings for merge-state wording in the touched spec and then-archived test spec.
- 2026-05-22: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive` passed.
- 2026-05-22: `git diff --check --` passed.
- 2026-05-22: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive` passed after plan-review recording.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md --path docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md --path docs/plan.md` passed after test-spec refresh with the existing lifecycle-language warning for merge-state wording in the spec.
- 2026-05-22: `git diff --check --` passed after test-spec refresh.
- 2026-05-22: `python scripts/test-artifact-lifecycle-validator.py -k plan_archive_contract -k plan_lifecycle_marker -k plan_supersession` failed before implementation for the expected archive/marker/supersession gaps, then passed after implementation.
- 2026-05-22: `python scripts/test-artifact-lifecycle-validator.py` passed after M2 implementation.
- 2026-05-22: `python -m py_compile scripts/artifact_lifecycle_validation.py scripts/artifact_lifecycle_contracts.py` passed after M2 implementation.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md` passed after M2 implementation with the existing lifecycle-language warning for merge-state wording in the spec.
- 2026-05-22: `python scripts/validate-change-metadata.py docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/change.yaml` passed after adding change metadata.
- 2026-05-22: `git diff --check --` passed after M2 implementation.
- 2026-05-22: Code-review M2 R1 direct probe showed `validate_repository(... paths=["docs/plans/2026-05-03-done-plan.md"])` returned no blocker for an explicit terminal plan missing from recent/archive.
- 2026-05-22: `python scripts/test-artifact-lifecycle-validator.py -k plan_body_terminal_marker_alone_requires_done_location -k plan_lifecycle_marker_does_not_infer_terminal_state_from_prose` passed after BPIX-M2-CR1 fix.
- 2026-05-22: `python scripts/test-artifact-lifecycle-validator.py` passed after BPIX-M2-CR1 fix.
- 2026-05-22: `python -m py_compile scripts/artifact_lifecycle_validation.py scripts/artifact_lifecycle_contracts.py` passed after BPIX-M2-CR1 fix.
- 2026-05-22: `git diff --check --` passed after BPIX-M2-CR1 fix.
- 2026-05-22: Code-review M2 R2 recorded clean-with-notes after reviewing the fix and validation evidence.
- 2026-05-22: `python - <<'PY' ... migration proof count/link assertion` passed after M3 migration, confirming 10 recent entries, 65 archived entries, 75 proof rows, and 75 unique linked plan files.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md` passed after M3 migration.
- 2026-05-22: `python scripts/test-artifact-lifecycle-validator.py` passed after M3 migration.
- 2026-05-22: `python scripts/validate-change-metadata.py docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/change.yaml` passed after M3 migration.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md` passed after M3 handoff state update with the existing lifecycle-language warning for merge-state wording in the spec.
- 2026-05-22: `git diff --check --` passed after M3 migration.
- 2026-05-22: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive` passed after code-review M3 R1 recording.
- 2026-05-22: `python scripts/validate-change-metadata.py docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/change.yaml` passed after code-review M3 R1 recording.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md` passed after code-review M3 R1 recording with the existing lifecycle-language warning for merge-state wording in the spec.
- 2026-05-22: `git diff --check --` passed after code-review M3 R1 recording.
- 2026-05-22: `python - <<'PY' ... M4 guidance audit` passed after M4 guidance updates, confirming archive, lifecycle marker, and active-context guidance appears in `docs/workflows.md`, `AGENTS.md`, `docs/examples/plans/example-plan.md`, and `skills/plan/SKILL.md`.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path AGENTS.md --path docs/examples/plans/example-plan.md` passed after M4 guidance updates.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md` passed after M4 plan-index state update.
- 2026-05-22: `python scripts/validate-skills.py skills/plan/SKILL.md` passed after M4 guidance updates.
- 2026-05-22: `python scripts/validate-skills.py` passed after M4 guidance updates.
- 2026-05-22: `python scripts/build-skills.py --check` passed after M4 guidance updates.
- 2026-05-22: `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir> && python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5` passed after M4 guidance updates.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md` passed after M4 handoff state update with the existing lifecycle-language warning for merge-state wording in the spec.
- 2026-05-22: `git diff --check --` passed after M4 guidance updates.
- 2026-05-22: `python - <<'PY' ... R8a direct ownership audit` passed after BPIX-M4-CR1 fix, confirming every R8a ownership point appears in `docs/workflows.md` and `skills/plan/SKILL.md`.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path AGENTS.md --path docs/examples/plans/example-plan.md --path specs/plan-index-lifecycle-ownership.test.md` passed after BPIX-M4-CR1 fix.
- 2026-05-22: `python scripts/validate-skills.py skills/plan/SKILL.md` passed after BPIX-M4-CR1 fix.
- 2026-05-22: `python scripts/validate-skills.py` passed after BPIX-M4-CR1 fix.
- 2026-05-22: `python scripts/build-skills.py --check` passed after BPIX-M4-CR1 fix.
- 2026-05-22: `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir> && python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5` passed after BPIX-M4-CR1 fix.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md` passed after BPIX-M4-CR1 fix.
- 2026-05-22: `git diff --check --` passed after BPIX-M4-CR1 fix.
- 2026-05-22: `python - <<'PY' ... R8a direct ownership audit` passed during code-review M4 R2, confirming every R8a ownership point appears in `docs/workflows.md` and `skills/plan/SKILL.md`.
- 2026-05-22: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive` passed during code-review M4 R2.
- 2026-05-22: `python scripts/validate-change-metadata.py docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/change.yaml` passed during code-review M4 R2.
- 2026-05-22: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md` passed during code-review M4 R2 with the existing lifecycle-language warning for merge-state wording in the spec.

## Outcome and retrospective

- Pending.

## Readiness

- See `Current Handoff Summary`.
- Ready for M5 implementation; not ready for final closeout.
