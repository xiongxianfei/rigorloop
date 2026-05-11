# Review skill recording and status output guardrail

- Status: done
- Owner: maintainer
- Start date: 2026-05-12
- Last updated: 2026-05-12
- Related issue or PR: PR #44
- Supersedes: none

## Purpose / big picture

Implement the approved formal review output guardrail so every formal lifecycle review skill reports review status, recording status, and status sync separately, records material findings durably before claiming completion, and synchronizes clean or approving review outcomes to the reviewed artifact's owned lifecycle surface when the target is clear and edits are allowed.

## Why now

The accepted proposal records repeated evidence that review skills can report material findings without completing the durable recording action. The approved spec amendment also adds a related lifecycle sync rule: clean or approving review results must not leave the reviewed artifact's tracked status stale when the update target is clear.

## Scope

### In scope

- Update the matched test spec for `specs/formal-review-recording.md`.
- Update the five formal review skills:
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
- Add static skill-validator coverage for the recording-status and status-sync output contracts.
- Preserve or update the shared `## Isolation and Recording` policy block without mixing stage-specific output wording into it.
- Regenerate `.codex/skills/` and public adapter output from canonical sources.
- Keep the change-local pack current:
  - `docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
  - durable reasoning/evidence under `docs/changes/2026-05-12-review-skill-recording-output-guardrail/`
- Run targeted validation, adapter checks, review-artifact checks, change metadata validation, final explain-change, verify, and PR handoff.

### Out of scope

- Creating a new review stage.
- Adding semantic validation that decides whether a review finding should have been material.
- Requiring detailed review files for clean reviews with no material findings and no detailed-record trigger.
- Changing review-resolution disposition vocabulary.
- Changing artifact-specific lifecycle vocabulary such as proposal `accepted` or spec `approved`.
- Treating status sync as downstream workflow continuation.
- Editing reviewed artifact content beyond minimal lifecycle/status/readiness/follow-on/closeout fields.
- Hand-editing generated `.codex/skills/` or `dist/adapters/` output.

## Constraints

- Follow `specs/formal-review-recording.md`; it is the governing approved spec for this plan.
- Preserve `CONSTITUTION.md` and `AGENTS.md` rules that isolation stops downstream handoff, not material-finding recording.
- Keep shipped skill text user-facing; maintainer-only details about generated paths and validator mechanics belong in contributor or governance surfaces, not public skill prose.
- Use repository-owned validation scripts and versioned adapter validation commands.
- Do not proceed to implementation until `plan-review` and `test-spec` are complete unless the maintainer explicitly requests an isolated implementation.

## Source artifacts

- Proposal: [Review Skill Recording and Status Output Guardrail](../proposals/2026-05-12-review-skill-recording-output-guardrail.md), accepted.
- Spec: [Formal Review Recording](../../specs/formal-review-recording.md), approved.
- Test spec: [Formal Review Recording Test Spec](../../specs/formal-review-recording.test.md), active and updated for `R24`-`R33`.
- Architecture: no architecture impact recorded in `docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`; architecture-review approved the no-impact rationale.
- Change metadata: `docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`.
- Learn evidence: [Review Approval Status Sync](../learn/sessions/2026-05-12-review-approval-status-sync.md).

## Context and orientation

The existing formal review recording contract already owns stage-neutral durable review records, the shared `## Isolation and Recording` block, and review artifact validation. This initiative adds an output-flow guardrail above that policy:

- Review verdict, recording status, and status sync are separate fields.
- `Recording status` is `not-required`, `recorded`, or `blocked`.
- Material findings require complete durable shape: Finding ID, Severity, Location, Evidence, Required outcome, and Safe resolution path or `needs-decision` rationale.
- `Status sync` is `not-required`, `updated`, or `blocked`.
- Clean or approving review outcomes update only the reviewed artifact's owned status/readiness/closeout surface when clear and allowed.

Likely implementation surfaces:

- `specs/formal-review-recording.test.md`
- `scripts/test-skill-validator.py`
- `scripts/validate-skills.py` if static validation logic needs helper checks
- `templates/shared/review-isolation-and-recording.md` only if the shared policy block itself must change
- five formal review skill files
- generated `.codex/skills/`
- generated `dist/adapters/`
- `docs/workflows.md`, `AGENTS.md`, or `CONSTITUTION.md` only if implementation finds them stale against the approved spec
- change-local evidence and closeout surfaces under `docs/changes/2026-05-12-review-skill-recording-output-guardrail/`

## Non-goals

- Do not broaden the first slice into runtime review-output validation.
- Do not add new artifact directories or schemas unless an approved follow-up requires them.
- Do not replace the existing review artifact validator model.
- Do not migrate historical review outputs or historical generated adapter output unless touched, generated, or relied on as current authoritative guidance.

## Requirements covered

- `R1`-`R6b`: preserve stage-neutral detailed-record triggers, initial review roots, material finding recording before fixes, and no-empty-resolution behavior.
- `R14`-`R14e`: preserve artifact-local source-of-truth boundaries.
- `R15`-`R16b`: keep canonical review-stage skill guidance and structural validation consistent.
- `R17`-`R21d`: preserve isolation-versus-recording behavior and byte-identical shared recording policy.
- `R22`-`R23`: align affected governance/operating guidance or record unaffected rationale; keep first-slice validation structural/static.
- `R24`-`R28a`: add formal review output recording-status fields, blocker semantics, complete material-finding shape, and change ID selection.
- `R29`-`R31b`: add artifact-status sync fields, blocker semantics, edit-permission rule, and artifact-specific target table.
- `R32`-`R33a`: update formal review skill final output shape consistently and regenerate generated skill/adapters after canonical skill changes.

## Dependencies

- Plan-review must approve this plan before test-spec and implementation.
- The formal review recording test spec must be updated for `R24`-`R33` before implementation.
- Code-review must run for each implementation milestone before it closes.
- Required review-resolution must close before final explain-change, verify, or PR handoff.
- Generated `.codex/skills/` and public adapter output depend on canonical skill edits and must be regenerated through repository scripts.

## Validation plan

- Start with focused static proof:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
- Validate change-local evidence throughout:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`
- After canonical skill edits, validate generated outputs:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
- Before PR handoff, run closeout and explicit touched-surface validation:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-skill-recording-output-guardrail`
  - `bash scripts/ci.sh --mode explicit specs/formal-review-recording.md specs/formal-review-recording.test.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md skills/architecture-review/SKILL.md skills/plan-review/SKILL.md skills/code-review/SKILL.md scripts/test-skill-validator.py scripts/validate-skills.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
  - `git diff --check --`

## Risks and recovery

- Risk: the five review skills drift in wording. Recovery: keep a concise common pattern and enforce stable terms through `scripts/test-skill-validator.py`.
- Risk: stage-specific output guidance is accidentally inserted inside the shared `## Isolation and Recording` block. Recovery: preserve the shared block byte-for-byte or update the template and all copies in one reviewed change.
- Risk: status sync oversteps isolated review behavior. Recovery: keep sync limited to the reviewed artifact's owned lifecycle/status/readiness/closeout surface and use `Status sync: blocked` for no-edit instructions or ambiguous owners.
- Risk: generated outputs drift or are hand-edited. Recovery: regenerate from canonical sources with repository scripts and validate with versioned adapter commands.
- Risk: another material review finding appears during this plan. Recovery: record it under the change-local review pack before review-driven fixes, then close it through `review-resolution.md`.

## Current Handoff Summary

- Current milestone: final closeout
- Current milestone state: done
- Last reviewed milestone: M3. Generated output, closeout evidence, and PR readiness
- Review status: code-review M3 clean-with-notes with no material findings on 2026-05-12
- Remaining in-scope implementation milestones: none
- Next stage: none
- Final closeout readiness: ready
- Reason final closeout is or is not ready: all in-scope implementation milestones are closed, review-resolution is closed, final explain-change and verify are complete, and PR #44 is open.

## Milestones

1. M1. Recording-status guardrail across formal review skills
   - Milestone state: closed
   - Goal: Make material-finding recording completion observable in all five formal review skills.
   - Requirements: `R1`-`R6b`, `R15`-`R28a`, `R32`-`R33a`
   - Files/components likely touched:
     - `specs/formal-review-recording.test.md`
     - `skills/proposal-review/SKILL.md`
     - `skills/spec-review/SKILL.md`
     - `skills/architecture-review/SKILL.md`
     - `skills/plan-review/SKILL.md`
     - `skills/code-review/SKILL.md`
     - `scripts/test-skill-validator.py`
     - `scripts/validate-skills.py` if needed
     - `docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
     - durable evidence under `docs/changes/2026-05-12-review-skill-recording-output-guardrail/`
   - Dependencies:
     - Plan-review approval.
     - Test-spec update for `R24`-`R28a`, `R32`, and relevant existing recording requirements.
   - Tests to add/update:
     - Static assertions that all five formal review skills include `Review status`, `Recording status`, `Recording blocker`, `not-required`, `recorded`, `blocked`, material finding shape fields, and required review artifact path labels.
     - Static assertions that `Recording status` is explicitly distinct from the review verdict.
     - Static assertions that recording blockers name the blocker and smallest action when blocked.
   - Implementation steps:
     - Update `specs/formal-review-recording.test.md` with test cases for output recording status and complete material-finding shape.
     - Add or update validator coverage first where feasible.
     - Add concise recording-status output guidance to each formal review skill outside the shared `## Isolation and Recording` block.
     - Preserve the shared policy block byte-for-byte unless the test spec explicitly requires changing the shared template and all copies.
     - Update change metadata and durable evidence surfaces for what changed and what remained unaffected.
   - Validation commands:
     - `python scripts/test-skill-validator.py`
     - `python scripts/validate-skills.py`
     - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
     - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`
     - `git diff --check -- specs/formal-review-recording.test.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md skills/architecture-review/SKILL.md skills/plan-review/SKILL.md skills/code-review/SKILL.md scripts/test-skill-validator.py scripts/validate-skills.py docs/changes/2026-05-12-review-skill-recording-output-guardrail`
   - Expected observable result: each formal review skill tells the reviewer to record material findings or report `Recording status: blocked`, and static validation proves the required output vocabulary and material finding shape are present.
   - Commit message: `M1: add review recording status guardrail`
   - Milestone closeout:
     - [x] targeted validation passed
     - [x] progress updated
     - [x] decision log updated if needed
     - [x] validation notes updated
     - [x] milestone committed
     - [x] hand off to code-review for M1
   - Risks:
     - Skill text becomes repetitive or too long.
     - Stage-specific text accidentally enters the shared policy block.
   - Rollback/recovery:
     - Revert M1 skill and validator changes while keeping already-valid review records as historical evidence.

2. M2. Artifact-status sync guardrail for clean or approving outcomes
   - Milestone state: closed
   - Goal: Make clean or approving formal review outcomes update the reviewed artifact's owned lifecycle/status/readiness/closeout surface when clear and allowed, or report `Status sync: blocked`.
   - Requirements: `R24`-`R24b`, `R29`-`R31b`, `R32`-`R33a`
   - Files/components likely touched:
     - `specs/formal-review-recording.test.md`
     - five formal review skill files
     - `scripts/test-skill-validator.py`
     - `scripts/validate-skills.py` if needed
     - lifecycle validation tests or fixtures only if existing validators can check clear status-sync cases without semantic review judgment
     - `docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
     - durable evidence under `docs/changes/2026-05-12-review-skill-recording-output-guardrail/`
   - Dependencies:
     - M1 complete or intentionally integrated without weakening recording-status coverage.
     - Test-spec coverage for status sync examples and `R29`-`R31b`.
   - Tests to add/update:
     - Static assertions that all five formal review skills include `Status sync`, `updated`, `Status artifact`, `Status sync blocker`, and the required status-sync blocker semantics.
     - Static assertions that status sync is distinct from the review verdict and from recording status.
     - Static assertions or manual test-spec coverage for artifact-specific target table behavior.
     - Existing lifecycle validator coverage only if clear artifact-status cases can be checked without guessing review semantics.
   - Implementation steps:
     - Update formal review skill expected output blocks to include status-sync fields.
     - Add artifact-specific target guidance for `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.
     - Add no-edit and ambiguous-target blocker guidance.
     - Record unaffected rationale for any governance or workflow surface that remains aligned and does not need text changes.
   - Validation commands:
     - `python scripts/test-skill-validator.py`
     - `python scripts/validate-skills.py`
     - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
     - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`
     - `git diff --check -- specs/formal-review-recording.test.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md skills/architecture-review/SKILL.md skills/plan-review/SKILL.md skills/code-review/SKILL.md scripts/test-skill-validator.py scripts/validate-skills.py docs/changes/2026-05-12-review-skill-recording-output-guardrail`
   - Expected observable result: approving or clean review outputs cannot silently leave status sync unreported; the skills update the reviewed artifact status surface when clear and allowed or report a concrete blocker.
   - Commit message: `M2: add review status sync guardrail`
   - Milestone closeout:
     - [x] targeted validation passed
     - [x] progress updated
     - [ ] decision log updated if needed
     - [x] validation notes updated
     - [x] milestone committed
     - [x] hand off to code-review for M2
   - Risks:
     - Review skills might over-edit artifacts during isolated reviews.
     - Artifact-specific status mapping may be too vague for plan and code-review cases.
   - Rollback/recovery:
     - Revert status-sync skill and validator additions while preserving the M1 recording-status guardrail if it remains valid.

3. M3. Generated output, closeout evidence, and PR readiness
   - Milestone state: closed
   - Goal: Refresh generated outputs, validate the full touched surface, record durable reasoning, and prepare PR handoff after implementation reviews are closed.
   - Requirements: `R15a`, `R21d`, `R22`-`R23`, `R33a`
   - Files/components likely touched:
     - `.codex/skills/`
     - `dist/adapters/`
     - `docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
     - `docs/changes/2026-05-12-review-skill-recording-output-guardrail/explain-change.md`
     - `docs/changes/2026-05-12-review-skill-recording-output-guardrail/verify-report.md` if verify creates a durable report
     - this plan and `docs/plan.md`
   - Dependencies:
     - M1 and M2 implemented, reviewed, and closed.
     - Required review-resolution closed if code-review creates material findings.
   - Tests to add/update:
     - No new behavioral tests unless code-review or verify identifies a gap.
     - Generated-output drift checks and adapter validation are required.
   - Implementation steps:
     - Run `python scripts/build-skills.py` after canonical skill edits.
     - Run `python scripts/build-adapters.py --version 0.1.1` after generated skill updates.
     - Update change metadata and durable reasoning/evidence surfaces.
     - Run final validation, explain-change, verify, and PR handoff.
     - Before PR, synchronize this plan and `docs/plan.md` if lifecycle state changes.
   - Validation commands:
     - `python scripts/test-skill-validator.py`
     - `python scripts/validate-skills.py`
     - `python scripts/build-skills.py --check`
     - `python scripts/build-adapters.py --version 0.1.1 --check`
     - `python scripts/validate-adapters.py --version 0.1.1`
     - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
     - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-skill-recording-output-guardrail`
     - `bash scripts/ci.sh --mode explicit --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path scripts/test-skill-validator.py --path scripts/validate-skills.py --path docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
     - `git diff --check --`
   - Expected observable result: generated outputs match canonical skills, adapter validation passes with version `0.1.1`, change metadata and review artifacts validate, durable reasoning explains the change, verify passes, and PR handoff is ready.
   - Commit message: `M3: refresh review skill generated outputs`
   - Milestone closeout:
     - [x] targeted validation passed
     - [x] generated output refreshed
     - [x] progress updated
     - [ ] decision log updated if needed
     - [x] validation notes updated
     - [x] milestone committed
     - [x] final explain-change completed
     - [x] verify completed
     - [x] PR handoff prepared
   - Risks:
     - Generated adapter drift check exposes unrelated stale output.
     - Review-resolution may be required if code-review finds material issues.
   - Rollback/recovery:
     - Regenerate from canonical skills after any rollback; do not hand-edit generated output.

## Progress

- 2026-05-12: accepted proposal, approved spec amendment, learn session, change metadata, proposal-review records, and spec-review records exist.
- 2026-05-12: architecture-review approved the no-architecture-impact rationale with no material findings.
- 2026-05-12: execution plan created and registered in `docs/plan.md`.
- 2026-05-12: plan-review approved with no material findings; next stage is `test-spec`.
- 2026-05-12: test spec updated for the review output recording/status-sync guardrail; next stage is `implement M1`.
- 2026-05-12: M1 implemented recording-status output guidance in all five formal review skills and added static skill-validator coverage; next stage is `code-review M1`.
- 2026-05-12: code-review M1 returned clean-with-notes with no material findings; M1 closed and next stage is `implement M2`.
- 2026-05-12: M2 implemented status-sync output guidance in all five formal review skills, including status-sync vocabulary, blocker semantics, per-review artifact-specific targets, and static skill-validator coverage; next stage is `code-review M2`.
- 2026-05-12: code-review M2 returned clean-with-notes with no material findings; M2 closed and next stage is `implement M3`.
- 2026-05-12: M3 refreshed generated Codex skills and public adapters from canonical review skills, added durable change explanation, and validated generated-output drift and adapter output; next stage is `code-review M3`.
- 2026-05-12: code-review M3 returned clean-with-notes with no material findings; M3 closed and next stage is `explain-change`.
- 2026-05-12: final explain-change refreshed `docs/changes/2026-05-12-review-skill-recording-output-guardrail/explain-change.md` with actual diff rationale, review-resolution summary, validation evidence, and remaining risks; next stage is `verify`.
- 2026-05-12: final verify passed selected CI, broad smoke, generated-output drift checks, adapter validation, change metadata validation, review-artifact closeout validation, and lifecycle validation; branch-ready and next stage is `pr`.
- 2026-05-12: PR #44 opened for final review at https://github.com/xiongxianfei/rigorloop/pull/44.

## Decision log

- 2026-05-12: split implementation into M1 recording-status guardrail and M2 artifact-status sync guardrail -> proposal review requested distinct milestones to keep the slice reviewable.
- 2026-05-12: keep generated-output refresh in M3 -> canonical skill edits should be reviewed before generated mirrors and adapters are finalized.
- 2026-05-12: require versioned adapter validation commands with `--version 0.1.1` -> matches repository workflow guidance and the accepted proposal's validation strategy.
- 2026-05-12: keep first-slice validation structural/static -> approved spec `R23` excludes semantic edit-reference flagging in this slice.
- 2026-05-12: M1 updated canonical skills only and deferred generated output refresh to M3 -> the active plan separates canonical review-skill changes from generated-output closeout.
- 2026-05-12: M2 kept status-sync validation static -> approved test spec `T22` covers vocabulary, blockers, no-edit behavior, and artifact-specific targets without adding semantic review-output parsing.
- 2026-05-12: M3 added `docs/changes/2026-05-12-review-skill-recording-output-guardrail/explain-change.md` as the required durable Markdown reasoning surface; the formal final explain-change stage remains downstream after implementation review closes.
- 2026-05-12: final verify restored `partially-accepted` in `workflow` review-resolution guidance -> broad smoke showed the workflow skill must preserve the same disposition vocabulary as the review-resolution contract.

## Surprises and discoveries

- none yet

## Validation notes

- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed after the no-architecture-impact rationale was recorded.
- 2026-05-12: `git diff --check -- docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed after the no-architecture-impact rationale was recorded.
- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed after the test spec update.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed after the test spec update.
- 2026-05-12: `git diff --check -- specs/formal-review-recording.test.md docs/plan.md docs/plans/2026-05-12-review-skill-recording-output-guardrail.md docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed after the test spec update.
- 2026-05-12: `python scripts/test-skill-validator.py` passed after M1 skill and validator updates.
- 2026-05-12: `python scripts/validate-skills.py` passed after M1 skill updates.
- 2026-05-12: `python scripts/test-skill-validator.py` passed after M2 status-sync skill and validator updates.
- 2026-05-12: `python scripts/validate-skills.py` passed after M2 status-sync skill updates.
- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed after M2 status-sync updates.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed after M2 status-sync updates.
- 2026-05-12: `git diff --check -- specs/formal-review-recording.test.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md skills/architecture-review/SKILL.md skills/plan-review/SKILL.md skills/code-review/SKILL.md scripts/test-skill-validator.py scripts/validate-skills.py docs/changes/2026-05-12-review-skill-recording-output-guardrail docs/plans/2026-05-12-review-skill-recording-output-guardrail.md docs/plan.md` passed after M2 status-sync updates.
- 2026-05-12: `python scripts/build-skills.py` synced generated Codex skills after M3.
- 2026-05-12: `python scripts/build-adapters.py --version 0.1.1` synced generated adapter output after M3.
- 2026-05-12: `python scripts/test-skill-validator.py` passed after M3 generated-output refresh.
- 2026-05-12: `python scripts/validate-skills.py` passed after M3 generated-output refresh.
- 2026-05-12: `python scripts/build-skills.py --check` passed after M3 generated-output refresh.
- 2026-05-12: `python scripts/build-adapters.py --version 0.1.1 --check` passed after M3 generated-output refresh.
- 2026-05-12: `python scripts/validate-adapters.py --version 0.1.1` passed after M3 generated-output refresh.
- 2026-05-12: `bash scripts/ci.sh --mode explicit specs/formal-review-recording.md specs/formal-review-recording.test.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md skills/architecture-review/SKILL.md skills/plan-review/SKILL.md skills/code-review/SKILL.md scripts/test-skill-validator.py scripts/validate-skills.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` failed with usage error because `ci.sh` requires `--path` before explicit paths; plan command corrected before rerun.
- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed after M3 generated-output refresh.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed after M3 generated-output refresh.
- 2026-05-12: `git diff --check --` passed after M3 generated-output refresh.
- 2026-05-12: corrected explicit CI rerun initially failed `artifact_lifecycle.validate` because the accepted proposal heading used `## Recommended Direction`; normalized it to `## Recommended direction`.
- 2026-05-12: `bash scripts/ci.sh --mode explicit --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path scripts/test-skill-validator.py --path scripts/validate-skills.py --path docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed after the proposal heading fix.
- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed after final explain-change refresh.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed after final explain-change refresh.
- 2026-05-12: `git diff --check -- docs/changes/2026-05-12-review-skill-recording-output-guardrail/explain-change.md` passed after final explain-change refresh.
- 2026-05-12: `python scripts/test-skill-validator.py` passed during final verify.
- 2026-05-12: `python scripts/validate-skills.py` passed during final verify.
- 2026-05-12: `python scripts/build-skills.py --check` passed during final verify.
- 2026-05-12: `python scripts/build-adapters.py --version 0.1.1 --check` passed during final verify.
- 2026-05-12: `python scripts/validate-adapters.py --version 0.1.1` passed during final verify.
- 2026-05-12: `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed during final verify.
- 2026-05-12: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed during final verify.
- 2026-05-12: `git diff --check --` passed during final verify.
- 2026-05-12: `bash scripts/ci.sh --mode explicit --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path scripts/test-skill-validator.py --path scripts/validate-skills.py --path docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed during final verify.
- 2026-05-12: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path docs/plans/2026-05-12-review-skill-recording-output-guardrail.md --path docs/plan.md --path docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed during final verify with an unrelated lifecycle-language warning in `docs/plan.md`.
- 2026-05-12: first `bash scripts/ci.sh --mode broad-smoke` run failed because `skills/workflow/SKILL.md` missed `partially-accepted`; after workflow guidance and generated output refresh, `python scripts/test-review-artifact-validator.py`, generated-output drift checks, adapter validation, and `bash scripts/ci.sh --mode broad-smoke` passed.

## Outcome and retrospective

- Done. M1 through M3 are closed with validation evidence, clean milestone code reviews, closed review-resolution status, passing final verify, durable explain-change, and opened PR #44. No true downstream completion event remains in this plan, so the plan index and plan body are synchronized as Done in this branch for PR review.

## Readiness

- See `Current Handoff Summary`.

## Risks and follow-ups

- The active formal review test spec currently predates `R24`-`R33`; update it before implementation.
- If runtime review-output omissions recur after this static guidance slice, create a follow-up proposal for runtime or output validation.
- If lifecycle validation cannot check clear status-sync cases without semantic review judgment, record that limitation and keep enforcement in skill guidance plus static checks for this slice.
