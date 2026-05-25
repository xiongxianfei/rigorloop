# Installed-Skill Artifact Placement Contract Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainers
- Start date: 2026-05-25
- Last updated: 2026-05-25
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved installed-skill artifact placement contract so skill-only adopters can answer artifact-placement questions from installed skill text, while `docs/workflows.md` remains a synchronized project-local map and validation catches drift.

## Source artifacts

- Proposal: [Installed-Skill Artifact Placement Contract](../proposals/2026-05-25-installed-skill-artifact-placement-contract.md)
- Spec: [Installed-Skill Artifact Placement Contract](../../specs/installed-skill-artifact-placement-contract.md)
- Architecture: not-required; this is a public skill, workflow guide, and validator contract update within existing repository boundaries.
- Test spec: [Installed-Skill Artifact Placement Contract Test Spec](../../specs/installed-skill-artifact-placement-contract.test.md)
- Change metadata: [change.yaml](../changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml)
- Review evidence: [proposal-review-r2](../changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/proposal-review-r2.md), [spec-review-r1](../changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/spec-review-r1.md)

## Context and orientation

Canonical public skill source lives under `skills/`. Generated public adapter output must not be hand-edited. `docs/workflows.md` is the project-local workflow and artifact-location map. The first implementation slice focuses on `proposal-review`, `spec-review`, plan-surface wording needed to remove ambiguity, workflow-map synchronization, deterministic validation, and generated-output proof.

The governing behavior is in `specs/installed-skill-artifact-placement-contract.md`. Related boundaries remain owned by existing contracts:

- review recording shape and receipt behavior: `specs/formal-review-recording.md`
- public skill portability and generated-output boundaries: `specs/rigorloop-workflow.md`, `specs/skill-contract.md`
- artifact-location map behavior: `docs/workflows.md`

## Non-goals

- Do not bulk-migrate historical review records.
- Do not add CLI scaffolding for new change-pack creation.
- Do not redesign review-record schemas, review status, severity, or disposition semantics.
- Do not hand-edit generated adapter output.
- Do not introduce build-time shared partials for placement wording in this slice.
- Do not expand the first slice to every review skill unless plan-review or test-spec explicitly changes scope.

## Requirements covered

- R1-R8: M2, with M1 test coverage and M3 generated-output proof.
- R9-R13: M2, with M1 test coverage for formal review locality and isolated advisory preservation.
- R14-R17: M2, with M1 test coverage for lookup order and partial workflow-guide fallback.
- R18-R19: M2, with M1 test coverage for plan-surface distinctions.
- R20-R23: M2, with M1 tests for workflow-map synchronization and no schema duplication.
- R24-R25: all milestones enforce first-slice boundaries.
- R26-R28: M1 creates and validates deterministic skill/workflow placement checks.
- R29: M3 validates generated installable skill or adapter output.
- R30: M3 records cold-read proof.
- AC1-AC12: M1-M3, final validation, and downstream verify.

## Current Handoff Summary

- Current milestone: M2. Canonical Skill and Workflow Map Wording
- Current milestone state: review-requested
- Last reviewed milestone: M2. Canonical Skill and Workflow Map Wording
- Review status: code-review-m2-r1 changes-requested for SAP-M2-CR1; finding resolved and awaiting rerun code-review
- Remaining in-scope implementation milestones: M2, M3
- Next stage: code-review M2
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M2 is awaiting rerun code-review, M3 has not started, explain-change and final verify are not recorded, and PR handoff is not prepared.

## Milestones

### M1. Placement Contract Validation Scaffolding

- Milestone state: closed
- Goal: Add deterministic tests and validator support for the installed-skill placement contract before changing canonical skill wording.
- Requirements: R26, R27, R28, R30, AC6, AC7, AC9
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
  - `docs/workflows.md` only if needed for fixture alignment
- Dependencies:
  - Plan-review approval.
  - Test spec that maps spec requirements to exact tests.
- Tests to add/update:
  - Skill-validator tests for required review-record path wording in `proposal-review` and `spec-review`.
  - Skill-validator tests for pre-change-pack behavior and isolated advisory carve-out.
  - Skill-validator tests for plan-surface distinctions.
  - Skill/workflow-map drift test for first-slice placement rows.
  - Cold-read fixture or assertion proving placement questions can be answered from skill text.
- Implementation steps:
  - Add failing or fixture-backed assertions for the required placement strings and headings.
  - Add deterministic checks in skill validation for the first-slice skill set.
  - Keep checks string/path based where possible to avoid broad semantic overreach.
  - Confirm checks fail on controlled negative fixtures and pass once canonical skill wording is updated.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py tests/fixtures/skills`
- Expected observable result: Validator coverage exists for missing placement contract wording, pre-change-pack behavior, plan-surface ambiguity, and skill/workflow placement drift.
- Commit message: `M1: add placement contract validator coverage`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated
  - validation notes updated
  - milestone committed
  - code-review-m1-r1 requested changes for SAP-M1-CR1
  - code-review-m1-r2 closed M1
- Risks:
  - Validator overfits prose and blocks harmless wording improvements.
  - Test fixtures accidentally encode repository-internal details as adopter-facing contract.
- Rollback/recovery:
  - Narrow checks to stable headings and path strings.
  - Move semantic judgments to review notes if deterministic validation becomes brittle.

### M2. Canonical Skill and Workflow Map Wording

- Milestone state: review-requested
- Goal: Update first-slice public skill wording and `docs/workflows.md` so installed skills carry concise placement contracts and the project-local map stays synchronized.
- Requirements: R1-R25, AC1-AC8, AC11, AC12
- Files/components likely touched:
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md` if plan-surface ambiguity appears there
  - `skills/implement/SKILL.md` or `skills/verify/SKILL.md` only if required for first-slice plan-surface disambiguation
  - `docs/workflows.md`
- Dependencies:
  - M1 validator support merged or in the same branch and ready to enforce the contract.
- Tests to add/update:
  - Update fixtures or expected strings from M1 to match final concise wording.
  - Confirm `docs/workflows.md` first-slice rows match skill-stated defaults.
- Implementation steps:
  - Add concise `Artifact placement` blocks to `proposal-review` and `spec-review`.
  - State formal review record path, review-log path, conditional review-resolution path, pre-change-pack behavior, and isolated advisory behavior.
  - Clarify workflow-guide precedence per artifact and portable-default fallback.
  - Disambiguate plan-surface references where first-slice skills use ambiguous plan wording.
  - Update `docs/workflows.md` to explain that the workflow guide summarizes/customizes placement and does not replace owning skill placement contracts.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md --path specs/installed-skill-artifact-placement-contract.md`
  - `git diff --check -- skills/proposal-review/SKILL.md skills/spec-review/SKILL.md skills/plan/SKILL.md docs/workflows.md`
- Expected observable result: Skill-only users can read first-slice skills and answer review placement and plan-surface questions; `docs/workflows.md` matches those defaults.
- Commit message: `M2: state installed skill placement contracts`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
  - code-review-m2-r1 requested changes for SAP-M2-CR1
  - SAP-M2-CR1 resolved and returned to code-review
- Risks:
  - Skill text becomes too verbose.
  - Workflow guide and skill wording disagree after edits.
  - Plan-surface wording touches more skills than expected.
- Rollback/recovery:
  - Use concise per-skill placement blocks and leave exact schemas to specs/validators.
  - Limit plan-surface wording to directly ambiguous first-slice occurrences.
  - Restore previous workflow rows if validation proves the sync rule wrong.

### M3. Generated Output Proof and Cold-Read Evidence

- Milestone state: planned
- Goal: Prove generated installable skill output contains the revised canonical skill bodies and record behavior-preservation/cold-read evidence.
- Requirements: R29, R30, AC9, AC10, AC11, AC12
- Files/components likely touched:
  - `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/behavior-preservation.md`
  - `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`
  - temporary adapter output under `/tmp` only
  - generated-output validation scripts only if existing checks cannot cover the required proof
- Dependencies:
  - M2 canonical skill wording complete.
- Tests to add/update:
  - Generated skill or adapter validation proof from canonical `skills/`.
  - Cold-read proof that installed skill text alone answers the three target questions.
  - Behavior-preservation matrix from the proposal.
- Implementation steps:
  - Run `python scripts/build-skills.py --check`.
  - Run adapter build and validation into a temporary output directory using the current version selected by repository release guidance or active plan/test spec.
  - Record cold-read proof and behavior-preservation evidence under the change pack.
  - Update `change.yaml` validation events and changed files.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>`
  - `python scripts/validate-adapters.py --root <tmpdir> --version <version>`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/installed-skill-artifact-placement-contract.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/behavior-preservation.md`
  - `git diff --check -- docs/changes/2026-05-25-installed-skill-artifact-placement-contract docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md docs/plan.md`
- Expected observable result: Generated output validation and cold-read proof show the installed-skill contract travels beyond this repository.
- Commit message: `M3: prove installed skill placement contract output`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Local adapter version selection is unclear.
  - Adapter validation requires tools unavailable locally.
  - Cold-read proof becomes subjective.
- Rollback/recovery:
  - Use repository-owned adapter validation commands and temporary output.
  - Record blocked generated-output proof with the exact missing command or version if repository guidance is insufficient.
  - Keep cold-read proof tied to exact questions and quoted path strings.

## Validation plan

- `python scripts/test-skill-validator.py`: validates deterministic placement contract checks.
- `python scripts/validate-skills.py`: validates canonical skill structure and policy checks.
- `python scripts/build-skills.py --check`: proves generated local skill mirrors are in sync with canonical skills.
- `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>`: builds installable adapter output from canonical skill sources.
- `python scripts/validate-adapters.py --root <tmpdir> --version <version>`: validates generated adapter output.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract`: validates review records and logs.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`: validates change metadata.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <touched lifecycle artifact> [...]`: validates touched lifecycle artifacts.
- `git diff --check -- <touched files>`: catches whitespace errors.

## Risks and recovery

- Risk: Placement wording duplicates schema or review-resolution details.
  - Recovery: Move field-level details back to specs/schemas/validators and keep skill text to placement and recording boundary.
- Risk: Skill validation becomes brittle.
  - Recovery: Restrict deterministic checks to headings, stable path strings, required plan-surface names, and fixture-backed negative cases.
- Risk: Existing project-local customization is weakened.
  - Recovery: Preserve lookup order and add tests for workflow-guide per-artifact precedence.
- Risk: Generated output proof cannot run locally.
  - Recovery: Record the blocker in `change.yaml`, keep canonical skill validation complete, and route adapter proof through the repository-owned command when available.
- Risk: First-slice scope expands into every review skill.
  - Recovery: Keep additional review-skill updates as follow-up unless a first-slice requirement or failing validator demands the change.

## Dependencies

- The approved spec remains the governing contract for this plan.
- `plan-review` must approve sequencing before implementation.
- `test-spec` must map R1-R30 and AC1-AC12 before implementation starts.
- Existing review-recording and workflow specs remain authoritative for exact review artifact shape and lifecycle ordering.
- Generated adapter validation depends on repository-owned adapter build and validation commands.

## Progress

- 2026-05-25: Plan created after proposal acceptance and clean spec-review.
- 2026-05-25: Clean plan-review recorded and active test spec created; next stage is implement M1.
- 2026-05-25: M1 implemented validator helper coverage for first-slice review placement contracts, workflow-map drift checks, and plan-surface disambiguation fixtures; next stage is code-review M1.
- 2026-05-25: `code-review-m1-r1` requested changes for `SAP-M1-CR1`; M1 moved to `resolution-needed`.
- 2026-05-25: Implemented the accepted `SAP-M1-CR1` fix by adding stage-owned record-type helper coverage, correcting the `spec-review` fixture, and adding wrong-stage negative fixtures; M1 returned to `review-requested`.
- 2026-05-25: `code-review-m1-r2` closed M1 cleanly; next stage is implement M2.
- 2026-05-25: M2 updated canonical `proposal-review` and `spec-review` placement blocks, added plan-surface wording to `plan`, synchronized `docs/workflows.md` precedence text, and wired the placement helpers into canonical skill validation; next stage is code-review M2.
- 2026-05-25: `code-review-m2-r1` requested changes for `SAP-M2-CR1`; M2 moved to `resolution-needed`.
- 2026-05-25: Resolved `SAP-M2-CR1` by synchronizing the plan readiness footer with the active rerun state; M2 returned to `review-requested`.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-25 | Use three implementation milestones: validator coverage, skill/workflow wording, generated-output proof. | Separates proof scaffolding, user-facing contract text, and installable-output evidence into reviewable slices. | One large implementation milestone; updating all review skills in the first slice. |
| 2026-05-25 | Treat architecture as not required for this slice. | The approved spec changes established skill, workflow-guide, and validator behavior without introducing new components, persistence, APIs, or deployment topology. | Creating an architecture artifact solely for wording and validator updates. |
| 2026-05-25 | Keep M1 placement helpers fixture-backed and do not wire them into canonical skill validation until M2. | Canonical `proposal-review`, `spec-review`, and plan-surface skill wording is intentionally updated in M2; enforcing the new checks in M1 would make unchanged canonical skills fail before their planned edit slice. | Wiring helper checks into `validate_skill_file` before the public skill wording changes. |
| 2026-05-25 | Wire placement-contract checks only for canonical first-slice skill surfaces in M2. | The helper now has public skill text to validate, while fixture and unrelated skill validation should not be broadened by this slice. | Applying the helper to generated output before M3; applying plan-surface enforcement to every plan-related skill in M2. |

## Surprises and discoveries

- M1 needed helper-level validation rather than immediate canonical enforcement so `python scripts/validate-skills.py` remains green until M2 updates public skill text.
- The published-skill portability validator treats command-style lines that name repository paths as required root dependencies, so the review-resolution path wording uses a label-plus-condition form instead of a `Use <path>` command line.

## Validation notes

- 2026-05-25: Test spec authored at `specs/installed-skill-artifact-placement-contract.test.md`; targeted lifecycle validation pending after metadata update.
- 2026-05-25: `python scripts/test-skill-validator.py` initially failed with seven expected `AttributeError` errors because the new M1 fixture tests called missing placement helper APIs.
- 2026-05-25: `python scripts/test-skill-validator.py` passed after adding fixture-backed placement, workflow-map drift, and plan-surface helper checks.
- 2026-05-25: `python scripts/validate-skills.py` passed, validating 23 canonical skill files while M1 helper checks remain detached from canonical enforcement until M2.
- 2026-05-25: `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py tests/fixtures/skills` passed.
- 2026-05-25: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed.
- 2026-05-25: `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml` passed.
- 2026-05-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-25-installed-skill-artifact-placement-contract.md --path specs/installed-skill-artifact-placement-contract.md --path specs/installed-skill-artifact-placement-contract.test.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/proposal-review-r1.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/proposal-review-r2.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/spec-review-r1.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/plan-review-r1.md` passed.
- 2026-05-25: `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md docs/plan.md docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed.
- 2026-05-25: `code-review-m1-r1` recorded `SAP-M1-CR1`; post-review lifecycle validation pending after review artifact updates.
- 2026-05-25: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed after `code-review-m1-r1` recording with reviews=5, findings=1, log_entries=5, resolution_entries=1.
- 2026-05-25: `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml` passed after `code-review-m1-r1` recording.
- 2026-05-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-25-installed-skill-artifact-placement-contract.md --path specs/installed-skill-artifact-placement-contract.md --path specs/installed-skill-artifact-placement-contract.test.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/proposal-review-r1.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/proposal-review-r2.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/spec-review-r1.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/plan-review-r1.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m1-r1.md` passed after `code-review-m1-r1` recording.
- 2026-05-25: `git diff --check -- docs/changes/2026-05-25-installed-skill-artifact-placement-contract docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md docs/plan.md` passed after `code-review-m1-r1` recording.
- 2026-05-25: `python scripts/test-skill-validator.py` passed with 170 tests after `SAP-M1-CR1` fix.
- 2026-05-25: `python scripts/validate-skills.py` passed with 23 skill files after `SAP-M1-CR1` fix.
- 2026-05-25: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed after `SAP-M1-CR1` fix.
- 2026-05-25: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed after `SAP-M1-CR1` fix.
- 2026-05-25: `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml` passed after `SAP-M1-CR1` fix.
- 2026-05-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md` passed after `SAP-M1-CR1` fix.
- 2026-05-25: `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md docs/plan.md docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed after `SAP-M1-CR1` fix.
- 2026-05-25: Rerun review validation for `code-review-m1-r2`: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-installed-skill-artifact-placement-contract`, and `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml` passed before recording the clean review.
- 2026-05-25: Post-recording validation for `code-review-m1-r2`: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-installed-skill-artifact-placement-contract`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m1-r1.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m1-r2.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md`, and `git diff --check -- docs/changes/2026-05-25-installed-skill-artifact-placement-contract docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md docs/plan.md` passed.
- 2026-05-25: `python scripts/test-skill-validator.py` initially failed with three expected canonical M2 assertion failures before canonical skill wording was updated: missing `proposal-review` and `spec-review` placement contracts and missing explicit plan-surface paths in `plan`.
- 2026-05-25: `python scripts/test-skill-validator.py` passed with 172 tests after canonical M2 wording and validator wiring.
- 2026-05-25: `python scripts/validate-skills.py` passed after M2, validating 23 canonical skill files with placement-contract checks wired for first-slice surfaces.
- 2026-05-25: `python scripts/build-skills.py --check` passed after M2, validating generated skills from canonical sources using a temporary output directory.
- 2026-05-25: `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml` passed after M2 metadata update.
- 2026-05-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md --path specs/installed-skill-artifact-placement-contract.md` passed after M2, validating 1 artifact file in explicit-paths mode.
- 2026-05-25: `git diff --check -- skills/proposal-review/SKILL.md skills/spec-review/SKILL.md skills/plan/SKILL.md docs/workflows.md` passed after M2.
- 2026-05-25: Code-review M2 reran `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md --path specs/installed-skill-artifact-placement-contract.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`; it passed with 3 artifact files before recording `SAP-M2-CR1`.
- 2026-05-25: Post-recording validation for `code-review-m2-r1`: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m2-r1.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md`, and `git diff --check -- docs/changes/2026-05-25-installed-skill-artifact-placement-contract docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md docs/plan.md` passed.

## Outcome and retrospective

- Pending completion.

## Readiness

- See `Current Handoff Summary`.
- Ready for `code-review M2`; readiness is not Done.
