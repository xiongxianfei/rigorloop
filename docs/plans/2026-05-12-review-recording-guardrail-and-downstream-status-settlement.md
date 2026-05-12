# Review Recording Guardrail and Examples Cleanup Plan

- Status: done
- Owner: maintainers
- Start date: 2026-05-12
- Last updated: 2026-05-12
- Related proposal: [Review Recording Guardrail and Downstream Status Settlement](../proposals/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md)
- Supersedes: none

## Purpose / big picture

Implement the approved formal review recording output guardrail and examples cleanup amendment. The change makes material-finding recording observable in formal review skill output, keeps review skills concise, moves illustrative examples out of active lifecycle directories, and preserves downstream upstream-status settlement as follow-up scope.

## Source artifacts

- Proposal: [Review Recording Guardrail and Downstream Status Settlement](../proposals/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md), accepted.
- Spec: [Formal Review Recording](../../specs/formal-review-recording.md), approved.
- Test spec: [Formal Review Recording Test Spec](../../specs/formal-review-recording.test.md), active.
- Spec-review records: [spec-review-r1](../changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/reviews/spec-review-r1.md), [spec-review-r2](../changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/reviews/spec-review-r2.md).
- Change metadata: [change.yaml](../changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml).
- Architecture: no runtime architecture change expected; this is workflow guidance, examples, validation, and generated-output work.

## Context and orientation

Canonical formal review skills live under `skills/proposal-review`, `skills/spec-review`, `skills/architecture-review`, `skills/plan-review`, and `skills/code-review`. Generated local Codex mirrors under `.codex/skills/` and public adapters under `dist/adapters/` must be regenerated from canonical skill text, not hand-edited.

The existing shared review-recording block lives at `templates/shared/review-isolation-and-recording.md`. The new amendment adds an output-level `Recording status` contract and a deterministic change-ID selection rule without expanding review skills into artifact-status sync owners.

Example artifacts currently live in active-looking paths such as `docs/plans/0000-00-00-example-plan.md` and `docs/changes/0001-skill-validator/`. The implementation should move examples to `docs/examples/**` when references can be updated safely, or explicitly retain the skill-validator pack with fixture-coupling rationale.

## Current Handoff Summary

- Current milestone: M3. Generated Output Refresh And Final Static Proof
- Current milestone state: closed
- Last reviewed milestone: M2. Formal Review Skill Recording Output Guardrail
- Review status: M3 code-review clean-with-notes; no material findings
- Remaining in-scope implementation milestones: none
- Next stage: PR review
- Final closeout readiness: PR #45 opened
- Reason final closeout is or is not ready: M1, M2, and M3 are closed with no open review-resolution, durable explain-change is complete, generated output is in sync, adapter validation passed, final local verification passed, and PR #45 is open; hosted CI is in progress and not yet claimed as passed.

## Non-goals

- Do not implement downstream upstream-status settlement in this slice.
- Do not add standardized review-side `Status sync`, `Status artifact`, `Status sync blocker`, or `Status settlement recommendation` fields.
- Do not add semantic review-quality validation.
- Do not create a new review stage such as `pr-review`.
- Do not require detailed review files for clean reviews with no detailed-record trigger.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not rewrite substantive lifecycle artifact content while moving examples.

## Requirements covered

- `R24`-`R26b`: recording-status vocabulary, review artifact paths, blocked status, and no-empty-resolution behavior.
- `R27`-`R28a`: complete material-finding shape including `Location`, and create-or-block output flow.
- `R29`-`R30b`: concise formal review skill guidance and no standardized status-sync fields.
- `R31`-`R31l`: deterministic change-ID selection, generated fallback, collision behavior, and blocked-recording behavior.
- `R31m`-`R32f`: long examples stay out of skills; examples live under `docs/examples/**`; selectors and lifecycle validation do not treat examples as active lifecycle state.
- `R33`-`R33b`: downstream upstream-status settlement remains follow-up scope.

## Milestones

### M1. Examples Surface And Validator Routing

- Milestone state: closed
- Goal: establish `docs/examples/**` as the non-normative examples surface and update validation/routing proof for moved examples.
- Requirements: `R31m`-`R32f`
- Files/components likely touched:
  - `docs/examples/README.md`
  - `docs/examples/plans/example-plan.md`
  - `docs/examples/formal-review-recording/change-id-selection-examples.md`
  - `docs/examples/formal-review-recording/material-finding-location-examples.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `docs/changes/0001-skill-validator/**`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `docs/workflows.md`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/test-select-validation.py`
  - `scripts/test-change-metadata-validator.py`
- Dependencies: approved spec and active test spec.
- Tests to add/update:
  - Selector/lifecycle coverage that `docs/examples/**` is not active lifecycle state.
  - Path fixture updates for the moved example plan.
  - Change-metadata fixture updates if `docs/changes/0001-skill-validator/` moves.
- Implementation steps:
  - Add `docs/examples/README.md` explaining examples are illustrative and non-normative.
  - Move `docs/plans/0000-00-00-example-plan.md` to `docs/examples/plans/example-plan.md`.
  - Update guidance references that currently point to the old plan example path.
  - Move `docs/changes/0001-skill-validator/` to `docs/examples/changes/skill-validator/` if validator references are straightforward; otherwise record explicit fixture-coupling rationale in the plan and change metadata.
  - Add formal review recording example files for change-ID selection and Location examples.
  - Update tests/selectors/validators to route or ignore `docs/examples/**` consistently.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml`
  - `git diff --check -- docs/examples docs/plans docs/changes/0001-skill-validator AGENTS.md CONSTITUTION.md docs/workflows.md scripts docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md docs/plan.md`
- Expected observable result: examples are under `docs/examples/**`, old active-looking example paths are removed or explicitly retained with rationale, and tests prove examples are not active lifecycle state.
- Commit message: `M1: move examples to non-normative docs examples surface`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Existing tests may be coupled to `docs/changes/0001-skill-validator/`.
  - Guidance may still point to the old example plan path.
- Rollback/recovery:
  - Restore moved examples and keep `docs/examples/README.md` only if routing breaks unexpectedly.
  - If the change-pack example cannot move safely, keep it in place with explicit rationale and a follow-up note.

### M2. Formal Review Skill Recording Output Guardrail

- Milestone state: closed
- Goal: update canonical formal review skills with concise `Recording status` output guidance, complete finding shape, deterministic change-ID selection pointer, and status-sync exclusions.
- Requirements: `R24`-`R31l`, `R33`-`R33b`
- Files/components likely touched:
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `templates/shared/review-isolation-and-recording.md` only if the shared isolation block must reference output obligations
  - `scripts/test-skill-validator.py`
- Dependencies: M1 closed or explicitly scoped away if examples are not needed for skill text.
- Tests to add/update:
  - Static assertions for `Recording status`, `not-required`, `recorded`, `blocked`, `Recording blocker`, complete material-finding shape, and required artifact paths.
  - Negative exact field checks for `- Status settlement recommendation:`, `- Status sync:`, `- Status artifact:`, and `- Status sync blocker:`.
  - Static check or manual proof that review skills point to the formal review recording change-ID selection rule instead of embedding the whole algorithm.
- Implementation steps:
  - Add concise recording-status output guidance to all five formal review skills.
  - Preserve the existing shared `## Isolation and Recording` behavior.
  - Require review outputs to create/update required artifacts or report `Recording status: blocked`.
  - Require complete material-finding shape including `Location`.
  - Add the short change-ID selection pointer to the formal review recording rule.
  - Keep status-sync fields out of review skill output shapes.
  - Update `scripts/test-skill-validator.py` for the stable terms and negative exact field checks.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml`
  - `git diff --check -- skills templates scripts docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md docs/plan.md`
- Expected observable result: canonical formal review skills expose the recording guardrail and tests prevent status-sync fields from returning.
- Commit message: `M2: add formal review recording status guidance`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Adding output obligations may make public skills longer than necessary.
  - Shared-block changes could force broader review-skill text updates.
- Rollback/recovery:
  - Revert to a shorter skill-local pointer while preserving spec-owned rules.
  - Keep existing shared block unchanged if output guidance works outside it.

### M3. Generated Output Refresh And Final Static Proof

- Milestone state: closed
- Goal: regenerate local Codex skill mirrors and public adapters from canonical skill changes, then validate generated drift and adapter packages.
- Requirements: `R15a`, `R29a`, generated-output obligations from the approved workflow.
- Files/components likely touched:
  - `.codex/skills/proposal-review/SKILL.md`
  - `.codex/skills/spec-review/SKILL.md`
  - `.codex/skills/architecture-review/SKILL.md`
  - `.codex/skills/plan-review/SKILL.md`
  - `.codex/skills/code-review/SKILL.md`
  - `dist/adapters/**`
  - `docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/**`
- Dependencies: M1 and M2 closed.
- Tests to add/update: no new tests expected unless generated-output validation reveals drift in adapter manifests.
- Implementation steps:
  - Run skill generation from canonical sources.
  - Run adapter generation for version `0.1.1`.
  - Validate generated output and adapter package structure.
  - Confirm generated public review skills include recording-status guidance and do not include status-sync fields.
- Validation commands:
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml`
  - `git diff --check -- .codex/skills dist/adapters docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md docs/plan.md`
- Expected observable result: generated local and public skill output matches canonical formal review skill guidance and adapter validation passes.
- Commit message: `M3: refresh generated review skill output`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Generated output drift may include more adapter files than expected.
  - Adapter validation may expose unrelated baseline issues.
- Rollback/recovery:
  - Regenerate after canonical rollback if M2 guidance changes.
  - If adapter validation exposes unrelated baseline debt, record it separately and keep this change scoped to generated review skills.

## Validation plan

Run milestone-specific validation first. Before final PR handoff, run:

```bash
python scripts/test-artifact-lifecycle-validator.py
python scripts/test-select-validation.py
python scripts/test-change-metadata-validator.py
python scripts/test-review-artifact-validator.py
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/test-adapter-distribution.py
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement
python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml
```

Also run explicit artifact lifecycle validation over the proposal, spec, test spec, plan index, plan body, and change-local artifacts after every lifecycle-state update.

## Risks and recovery

- Example relocation may break path-coupled tests. Recovery: keep the shipped change-pack example in place with rationale and defer only that move.
- Skill guidance may become too verbose. Recovery: move examples to `docs/examples/**` and keep only the concise pointer in skills.
- Generated output may drift unexpectedly. Recovery: regenerate from canonical sources and validate; do not hand-edit generated files.
- Review artifact closeout may become stale during implementation. Recovery: run structure and closeout validation before each milestone handoff.

## Dependencies

- Spec-review is complete and `SR-001` is resolved.
- Plan-review must pass before implementation begins.
- M3 depends on canonical skill edits in M2.
- Final closeout depends on all implementation milestones reaching `closed` and review-resolution remaining closed.

## Progress

- [x] 2026-05-12: proposal accepted.
- [x] 2026-05-12: spec amendment drafted.
- [x] 2026-05-12: spec-review R1 recorded material finding `SR-001`.
- [x] 2026-05-12: `SR-001` accepted and resolved in the spec/test-spec amendments.
- [x] 2026-05-12: spec-review R2 approved the amended spec.
- [x] 2026-05-12: plan-review approved the execution plan with no material findings.
- [x] 2026-05-12: test-spec readiness checked; existing active test spec covers the approved amendment and current plan.
- [x] 2026-05-12: M1 moved the plan example to `docs/examples/plans/example-plan.md`, added formal review recording examples, taught selector routing to classify `docs/examples/**` as non-lifecycle examples, and updated active guidance references.
- [x] 2026-05-12: M1 retained `docs/changes/0001-skill-validator/` as a validator fixture and historical proof pack because it remains referenced by existing validator tests, README-facing specs, and workflow compatibility specs.
- [x] 2026-05-12: M1 code-review returned `clean-with-notes` with no material findings; no detailed review record was required.
- [x] 2026-05-12: M2 added static validator coverage for formal review `Recording status` output and updated the five formal review skills plus the shared isolation/recording block.
- [x] 2026-05-12: M2 code-review returned `clean-with-notes` with no material findings; no detailed review record was required.
- [x] 2026-05-12: M3 regenerated local Codex skill mirrors and public adapters for version `0.1.1`, then validated generated-output drift and adapter structure.
- [x] 2026-05-12: M3 code-review returned `clean-with-notes` with no material findings; no detailed review record was required.
- [x] 2026-05-12: explain-change created `docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/explain-change.md`.
- [x] 2026-05-12: verify passed final local validation and marked the branch ready for PR handoff.
- [x] 2026-05-12: PR #45 opened for review; hosted CI was in progress at PR handoff.
- [x] M1. Examples Surface And Validator Routing - closed
- [x] M2. Formal Review Skill Recording Output Guardrail - closed
- [x] M3. Generated Output Refresh And Final Static Proof - closed

## Decision log

- 2026-05-12: Keep downstream upstream-status settlement out of this implementation slice. Rationale: the proposal and spec reserve it as follow-up scope.
- 2026-05-12: Keep the normative change-ID selection rule directly in `specs/formal-review-recording.md`. Rationale: implementation and tests need one source of truth.
- 2026-05-12: Use `docs/examples/**` as the examples surface. Rationale: active lifecycle directories should not contain illustrative examples that selectors or validators can mistake for current state.
- 2026-05-12: Retain `docs/changes/0001-skill-validator/` in the first slice. Rationale: the pack is still a repo-owned validator fixture and historical proof example with many compatibility-spec references, so moving it would exceed M1's safe routing cleanup.

## Surprises and discoveries

- none yet

## Validation notes

- Pre-plan artifact lifecycle validation passed for the accepted proposal, approved spec amendment, and active test spec amendment.
- Spec-review artifacts for `SR-001` validate in structure and closeout mode after R2 approval.
- Plan-review approved the execution plan without material findings; no detailed plan-review record was required.
- Test-spec check updated the active proof-planning surface to reference this current plan and confirmed implementation proof coverage for M1-M3.
- `python scripts/test-artifact-lifecycle-validator.py` passed after adding proof that `docs/examples/plans/example-plan.md` is not active lifecycle state.
- `python scripts/test-select-validation.py` passed after adding `docs/examples/**` classification as non-lifecycle examples.
- `python scripts/test-change-metadata-validator.py` passed with `docs/changes/0001-skill-validator/` retained as the shipped validator example.
- `python scripts/test-skill-validator.py` passed after moving the governance-guidance fixture read to `docs/examples/plans/example-plan.md`.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md --path docs/plan.md` passed with the existing unrelated `docs/plan.md` lifecycle-language warning.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement` passed after M1.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml` passed after M1.
- `git diff --check -- docs/examples docs/plans docs/changes/0001-skill-validator AGENTS.md CONSTITUTION.md README.md docs/workflows.md scripts specs/rigorloop-workflow.test.md specs/plan-index-lifecycle-ownership.test.md specs/single-source-of-workflow-state.test.md docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement docs/plan.md` passed after M1.
- M1 code-review reran `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/test-select-validation.py`, and `python scripts/test-skill-validator.py`; all passed.
- M1 code-review checked stale old plan-example references with `rg -n "docs/plans/0000-00-00-example-plan|0000-00-00-example-plan" README.md AGENTS.md CONSTITUTION.md docs/workflows.md scripts specs`; remaining hits are only the governing spec/test-spec migration assertions.
- M2 first added failing static coverage in `scripts/test-skill-validator.py` for formal review `Recording status` output, complete material-finding shape, review artifact path fields, negative exact status-sync fields, and the short change-ID selection pointer.
- `python scripts/test-skill-validator.py` passed after updating the shared isolation/recording block and the five canonical formal review skill expected-output shapes.
- `python scripts/validate-skills.py` passed after M2 canonical skill updates.
- M2 code-review reran `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement`, `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml`, and `git diff --check -- skills templates scripts docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md docs/plan.md`; all passed.
- M3 pre-generation drift checks failed as expected: `python scripts/build-skills.py --check` reported five stale local Codex skill mirrors, and `python scripts/build-adapters.py --version 0.1.1 --check` reported 15 stale adapter skill files.
- `python scripts/build-skills.py` regenerated local Codex skill mirrors.
- `python scripts/build-adapters.py --version 0.1.1` regenerated public adapter output.
- `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/test-adapter-distribution.py`, `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement`, `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml`, and `git diff --check -- .codex/skills dist/adapters docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md docs/plan.md` passed after M3 generation.
- Manual generated-output proof found `Recording status output`, `Review resolution: <path | not-required | blocked>`, and the formal review recording change-ID pointer in generated local Codex, Claude, Codex adapter, and opencode adapter review skills; exact status-sync fields were absent.
- M3 code-review reran `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/test-adapter-distribution.py`, `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement`, `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml`, and `git diff --check -- .codex/skills dist/adapters docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md docs/plan.md`; all passed.
- `docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/explain-change.md` records the durable rationale linking the proposal, `R15a`, `R24`-`R31m`, `R33`, `T12`, `T21`-`T26`, M1-M3, review outcomes, and validation evidence to the actual diff.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement`, `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml`, and `git diff --check -- docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/explain-change.md docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md docs/plan.md` passed after explain-change.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/explain-change.md --path docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml --path docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md --path docs/plan.md` passed after explain-change with the existing unrelated `docs/plan.md` lifecycle-language warning.
- Final verify passed: `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/test-select-validation.py`, `python scripts/test-change-metadata-validator.py`, `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/test-adapter-distribution.py`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement`, `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml`, and scoped `git diff --check -- ...`.
- Final explicit artifact lifecycle validation passed for the proposal, spec, test spec, plan body, plan index, change metadata, explain-change, review log, and review resolution with the existing unrelated `docs/plan.md` lifecycle-language warning.

## Outcome and retrospective

- Implemented formal review recording-status output, complete material-finding shape, deterministic review-recording change-ID selection, non-normative examples routing, validator coverage, and generated public skill refresh.
- Opened PR #45 for review after final local verification; hosted CI was in progress at handoff.

## Readiness

- See `Current Handoff Summary`.
- This plan is closed locally and handed off to PR #45 for review.
