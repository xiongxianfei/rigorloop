# Vision Skill Simplification and VISION.md Migration Execution Plan

## Status

- active

- Owner: maintainers
- Start date: 2026-05-01
- Last updated: 2026-05-03
- Related issue or PR: none yet
- Supersedes: none
- broad_smoke_required: false
- broad_smoke_reason: This migration changes governance, specs, skills, selector routing, validators, root Markdown artifacts, and generated outputs. The approved spec requires focused selector, skill, lifecycle, README marker, generated-output, and adapter checks; no runtime service, release packaging, schema, or deployment boundary requires repository broad smoke by default.

## Purpose / Big Picture

Implement the approved migration from lowercase root `vision.md` to uppercase root `VISION.md` and simplify the `vision` skill so contributors use ordinary intent instead of user-facing `create`, `revise`, and `mirror` modes.

The work must preserve the existing safety model: no silent overwrite, no broad README edits, no silent marker insertion during update or sync, explicit substantive/editorial confirmation for meaning-changing updates, and generated `.codex/skills/` plus public adapter output derived only from canonical skill sources.

## Source Artifacts

- Proposal: [Vision Skill Simplification and VISION.md Migration](../proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md), accepted on 2026-05-01.
- Spec: [Vision Skill Simplification and VISION.md Migration](../../specs/vision-skill-simplification-and-vision-md-migration.md), approved after spec-review on 2026-05-01.
- Architecture: not required. The approved change is a workflow-governance, contract, selector, and generated-output migration without a runtime boundary, service boundary, data store, network integration, deployment boundary, or architecture package change.
- Test spec: [Vision Skill Simplification and VISION.md Migration Test Spec](../../specs/vision-skill-simplification-and-vision-md-migration.test.md) is active.
- Project map: none present. Orientation comes from `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `README.md`, `vision.md`, `specs/vision-skill.md`, `specs/vision-skill.test.md`, `skills/vision/SKILL.md`, `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, `scripts/validation_selection.py`, `scripts/test-select-validation.py`, `scripts/test-skill-validator.py`, and generated-output scripts.

## Context and Orientation

- The repository currently has root `vision.md` and README front-matter linking to `vision.md`.
- `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, README ownership guidance, `skills/proposal`, `skills/proposal-review`, `skills/vision`, `specs/vision-skill.md`, and `specs/vision-skill.test.md` still describe lowercase `vision.md` as canonical.
- `skills/vision/SKILL.md` currently exposes `create`, `revise`, and `mirror` as explicit modes. The migration keeps the safety gates but removes those as required user-facing operating modes.
- Selector routing currently classifies root `vision.md` as category `vision` and does not yet classify root `VISION.md`.
- Generated Codex runtime mirror output under `.codex/skills/` and public adapters under `dist/adapters/` must not be hand-edited. They are refreshed through `scripts/build-skills.py` and `scripts/build-adapters.py --version 0.1.1`.
- Case-only renames can be unreliable. Implementation should use the two-step Git rename strategy from the approved spec when migrating `vision.md` to `VISION.md`.

## Non-Goals

- Rewrite the approved project vision content.
- Make `vision` a normal per-change workflow stage.
- Add a README synchronization helper script.
- Create a separate `vision-review` skill.
- Rewrite historical proposals, specs, plans, reviews, change-local artifacts, or PR records solely to replace old `vision.md` references.
- Change adapter portability rules beyond refreshing generated output for changed canonical skill guidance.
- Require specific competitor names in generated or revised vision text.
- Extract or consolidate shared evidence-collection guidance across skills.
- Change the 500-word cap, required vision sections, drafting heuristics, privacy rules, or research boundaries except where wording must refer to `VISION.md`.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R8`, `AC1`-`AC4`, `AC15` | `vision.md` to `VISION.md` rename, README front-matter link update, governance and workflow path references, historical-reference scope guard |
| `R9`-`R15`, `AC1`-`AC2`, `AC11`, `AC20` | two-step Git rename, coexistence invalid-state handling, rollback guidance, validation for both-path conflict and reintroduced legacy path |
| `R16`-`R27`, `AC5`-`AC7` | `skills/vision/SKILL.md` state-based interface and focused skill-validator assertions |
| `R28`-`R40`, `AC6`-`AC7`, `AC18` | vision establishment, update, sync, overwrite, substantive/editorial, and causal-link safety behavior in skill guidance and tests |
| `R41`-`R49`, `AC4`, `AC6`, `AC18` | README marker behavior in skill guidance, README ownership wording, and marker validation checks |
| `R50`-`R62`, `AC8`-`AC9`, `AC21` | `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, focused skill-validator assertions, and proposal `Vision fit` status-line behavior |
| `R63`-`R75`, `AC3`, `AC10`-`AC14`, `AC16` | governance/workflow/README updates, selector routing, repository validation, generated `.codex/skills/`, and public adapters |
| `R76`-`R83`, `AC17`-`AC20` | retirement or rewrite of old `vision.md` and mode requirements in `specs/vision-skill.md`, `specs/vision-skill.test.md`, canonical skill guidance, selector routing, and generated outputs |

## Immediate Test-Spec Handoff

After `plan-review` approval, the immediate next stage is focused `test-spec`, not implementation.

The test spec must create `specs/vision-skill-simplification-and-vision-md-migration.test.md`, map every `MUST` requirement and `AC1`-`AC21` to concrete proof, and identify the focused selector, skill-validator, README marker, generated-output, adapter, lifecycle, and metadata checks required by the implementation milestones.

Implementation milestone M1 must not start until the focused test spec is active. Within each implementation milestone, add or update the relevant assertions before implementation, but close the milestone only after the paired implementation makes the milestone validation pass.

## Milestones

### M1. Add Selector and Validation Support for Vision Paths

- Goal: Make repository-owned validation recognize root `VISION.md`, migration-time legacy root `vision.md`, and invalid coexistence before the canonical rename lands.
- Requirements: `R9`-`R12`, `R15`, `R66`-`R71`, `R83`, `AC10`-`AC12`, `AC19`-`AC20`.
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - possibly `scripts/validate-readme.py` if marker or coexistence checks are implemented there instead of selector-side checks
  - `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
  - `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md`
  - this plan
- Dependencies:
  - active focused test spec
- Tests to add/update:
  - explicit-mode selection for `VISION.md`
  - explicit-mode and PR-mode selection for deletion/rename of root `vision.md`
  - conflict case where both root `vision.md` and `VISION.md` exist
  - reintroduced legacy root `vision.md` after migration classified as legacy or conflict, not ignored
- Implementation steps:
  - Create the baseline change-local artifact pack for durable implementation traceability.
  - Add or update selector assertions before changing selector implementation within this milestone.
  - Extend path classification so root `VISION.md` and legacy root `vision.md` both classify deterministically.
  - Ensure `VISION.md` changes select README vision-marker validation or equivalent vision/README consistency proof.
  - Add repository-owned conflict handling for both root vision files existing.
  - Keep PR-mode and explicit-mode behavior aligned through fixture tests.
  - Close the milestone only after the paired selector implementation makes the selector assertions and selected validation pass.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path VISION.md`
  - `python scripts/select-validation.py --mode explicit --path vision.md`
  - `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration`
- Expected observable result: root `VISION.md` and legacy root `vision.md` are both classified, README marker validation is selected for the vision surface, and coexistence blocks or fails through repository-owned validation.
- Commit message: `M1: route VISION.md validation`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Coexistence checks can make the deliberate rename sequence hard to validate if the temporary state is not handled carefully.
  - Selector changes can accidentally broaden validation scope beyond the approved path migration.
- Rollback/recovery:
  - Revert selector and selector-test changes together, then rerun selector regression and explicit selection for the current root `vision.md`.

### M2. Migrate Authored Vision, Governance, Specs, and Skills

- Goal: Rename the root vision artifact and update active authored surfaces so no approved contract or canonical skill requires lowercase `vision.md` or user-facing vision modes.
- Requirements: `R1`-`R65`, `R70`, `R75`-`R82`, `AC1`-`AC9`, `AC15`-`AC18`, `AC21`.
- Files/components likely touched:
  - `vision.md` deleted through safe rename
  - `VISION.md` added through safe rename
  - `README.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/vision-skill.md`
  - `specs/vision-skill.test.md`
  - `skills/vision/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `scripts/test-skill-validator.py`
  - this plan and change-local artifacts
- Dependencies:
  - active focused test spec
  - M1 selector support for both root vision paths
- Tests to add/update:
  - skill-validator assertions for VISION.md references, no required user-facing modes, preserved safety gates, and new `Vision fit` status-line values
  - lifecycle/test-spec coverage updates proving old `vision.md` and mode requirements are retired or rewritten
- Implementation steps:
  - Add or update skill-validator assertions before changing authored skill guidance within this milestone.
  - Use a safe two-step Git rename: `git mv vision.md .vision.tmp`, then `git mv .vision.tmp VISION.md`.
  - Update README front-matter link and ownership wording to point to `VISION.md`.
  - Update `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` source-of-truth guidance.
  - Rewrite active `specs/vision-skill.md` and `specs/vision-skill.test.md` portions that require lowercase `vision.md` or user-facing `create`, `revise`, and `mirror` modes.
  - Simplify `skills/vision/SKILL.md` to state-based behavior while preserving safety and quality rules.
  - Update `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` to read `VISION.md` and enforce status-line `Vision fit`.
  - Confirm the approved project vision content itself is unchanged except path-sensitive references or generated README front-matter.
  - Close the milestone only after the paired authored-surface implementation makes the skill, README, lifecycle, selector-selected, and whitespace validation pass.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-readme.py README.md --vision-markers`
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path README.md --path VISION.md --path vision.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path README.md --path VISION.md --path vision.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md README.md VISION.md vision.md specs/vision-skill.md specs/vision-skill.test.md skills/vision/SKILL.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md`
- Expected observable result: root `VISION.md` is the only canonical vision file, active authored guidance names `VISION.md`, old mode requirements are gone, and safety rules remain present.
- Commit message: `M2: migrate vision contract to VISION.md`
- Milestone closeout:
  - [x] M2 authored-surface validation passed; generated drift checks are selected and deferred to M3 by design
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - A broad search-and-replace could rewrite historical artifacts or alter project vision content, both out of scope.
  - Removing mode words could accidentally remove safety gates that those modes previously carried.
- Rollback/recovery:
  - Restore exactly one root vision artifact path. If reverting the migration, restore lowercase `vision.md`, update README and guidance references, rerun skill and selector validation, and do not leave both root files.

### M3. Refresh Generated Output and Final Lifecycle Evidence

- Goal: Propagate canonical skill changes to generated runtime and adapter surfaces and close the initiative for review.
- Requirements: `R72`-`R74`, `R77`, `AC13`-`AC14`, plus final proof for all requirements.
- Files/components likely touched:
  - `.codex/skills/vision/SKILL.md`
  - `.codex/skills/proposal/SKILL.md`
  - `.codex/skills/proposal-review/SKILL.md`
  - generated public adapter skill copies under `dist/adapters/`
  - generated adapter manifests or command files only if generator output changes them
  - `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
  - `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md`
  - this plan
  - `docs/plan.md` when final lifecycle state changes
- Dependencies:
  - M1 through M2 complete
- Tests to add/update:
  - no new generator behavior expected unless the generator output inventory changes; generated-output proof uses existing generator and adapter checks
- Implementation steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Inspect generated skill and adapter diffs for expected path and skill-guidance changes only.
  - Update change-local metadata, this plan's progress, validation notes, surprises, and decision log.
  - Keep `docs/plan.md` synchronized with this plan body when lifecycle state changes.
  - Close the milestone only after generated-output, adapter, lifecycle, selected CI, and whitespace validation pass.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-readme.py README.md --vision-markers`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path README.md --path VISION.md --path vision.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
  - `git diff --check -- .`
- Expected observable result: generated outputs match canonical skills, lifecycle artifacts are coherent, targeted validation passes, and the change is ready for first-pass `code-review`.
- Commit message: `M3: refresh generated VISION.md migration output`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Generated output can include larger-than-expected churn if adjacent generated entrypoints derive from changed skill metadata.
  - Lifecycle closeout can become stale if downstream review findings require more edits.
- Rollback/recovery:
  - Revert generated output first, rerun generator checks, then reopen the plan body and change-local metadata if earlier milestones need correction.

## Validation Plan

Validation proceeds from focused to broad-enough:

- Lifecycle proof for proposal, approved spec, active test spec, plan, and change-local metadata.
- Skill proof through `python scripts/validate-skills.py` and `python scripts/test-skill-validator.py`.
- Selector proof through `python scripts/test-select-validation.py`, explicit selection for root `VISION.md`, explicit selection for legacy root `vision.md`, and targeted `bash scripts/ci.sh --mode explicit`.
- README marker proof through `python scripts/validate-readme.py README.md --vision-markers`.
- Generated-output proof through `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, and `python scripts/validate-adapters.py --version 0.1.1`.
- Final whitespace proof through `git diff --check -- .`.

Repository broad smoke is not planned by default. If plan-review, test-spec, selector output, review-resolution, or another authoritative artifact later requires broad smoke, record the trigger in this plan and run `bash scripts/ci.sh --mode broad-smoke`.

## Risks and Recovery

- Risk: Case-only rename is not recorded reliably.
  Recovery: use the two-step `git mv` strategy from the spec and validate the final branch has exactly one root vision file.
- Risk: Old mode wording remains in active contracts or generated skill output.
  Recovery: focused skill-validator assertions and generated-output drift checks must fail until old required mode wording is removed from active surfaces.
- Risk: Historical artifacts are rewritten unnecessarily.
  Recovery: restrict path-reference updates to active governance, README, specs, skills, selector, validators, generated output, and this initiative's lifecycle artifacts.
- Risk: Selector conflict checks block the deliberate migration sequence.
  Recovery: implement selector behavior before the rename and test legacy-only, uppercase-only, and both-file states separately.
- Risk: README marker update edits author-owned content.
  Recovery: update only the marker block or ownership wording explicitly in scope, then run README marker validation and inspect the diff.
- Risk: Generated output is hand-edited.
  Recovery: regenerate from canonical skills and rerun drift checks; do not patch `.codex/skills/` or `dist/adapters/` manually.

## Dependencies

- `plan-review` approval is required before test-spec authoring and implementation.
- A focused test spec must be active before implementation changes begin.
- M1 selector support should land before the root rename in M2 so validation can classify both the legacy and new root paths.
- Existing generators must remain the only path for `.codex/skills/` and `dist/adapters/` output.
- No external services, new dependencies, release packaging changes, or architecture package are required.

## Progress

- 2026-05-01: plan created from the accepted proposal and approved spec.
- 2026-05-01: plan authoring validation passed for the plan, plan index, proposal, and spec lifecycle surfaces.
- 2026-05-01: plan-review findings addressed by moving test-spec creation to the immediate `test-spec` stage, making implementation milestones test-first and green by closeout, and removing the invalid multi-target `validate-skills.py` command.
- 2026-05-01: focused test spec created and marked active for implementation.
- 2026-05-01: M1 selector assertions were added before implementation. The red phase failed on uppercase root `VISION.md` classification, both-path conflict handling, and legacy reintroduction after uppercase migration.
- 2026-05-01: M1 selector implementation classified root `VISION.md` and legacy root `vision.md`, selected README vision-marker validation through the existing vision path behavior, and added a repository-owned both-path conflict block.
- 2026-05-01: M1 baseline change-local artifact pack created under `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/`.
- 2026-05-03: M1 code-review returned `clean-with-notes`; verify found no selector behavior blockers and only blocked on stale readiness wording after M1 completion.
- 2026-05-03: M1 readiness wording corrected so the active plan points to M2 instead of the already-completed M1 implementation slice.
- 2026-05-03: M2 focused skill-validator assertions were added before authored guidance changes. The red phase failed on active lowercase `vision.md` canonical guidance, old user-facing mode requirements, missing state-based skill guidance, and old `Vision fit` status wording.
- 2026-05-03: M2 renamed root `vision.md` to `VISION.md` with the safe two-step Git rename, leaving project vision prose unchanged.
- 2026-05-03: M2 updated README, governance, workflow guidance, active vision specs/test specs, `vision`, `proposal`, and `proposal-review` skills, and focused skill-validator coverage for `VISION.md`, state-based behavior, safety gates, and proposal `Vision fit` status lines.

## Decision Log

- 2026-05-01: Architecture is not required because the change is a governance, spec, skill, selector, README, and generated-output migration without a runtime or deployment design boundary.
- 2026-05-01: Selector support is planned before the root rename so `VISION.md` and legacy `vision.md` can be validated during migration instead of blocking as unclassified paths.
- 2026-05-01: Repository broad smoke is not required by default; targeted lifecycle, selector, skill, README, generated-output, and adapter checks cover the approved change surfaces.
- 2026-05-01: M1 conflict detection uses exact root directory entries plus Git index paths instead of `Path.is_file()` alone so case-insensitive filesystems do not report false coexistence when only one root vision entry exists.
- 2026-05-03: M2 leaves generated `.codex/skills/` and `dist/adapters/` drift unresolved intentionally because M3 owns generator runs. Selector-selected generated drift is recorded as expected until M3.

## Surprises and Discoveries

- 2026-05-01: The implementation workspace resolves `VISION.md` and `vision.md` to the same filesystem entry even though Git tracks only `vision.md`; selector conflict detection must therefore distinguish exact directory or index names from path aliases.

## Validation Notes

- 2026-05-01: `python scripts/test-select-validation.py` failed before M1 selector implementation for the newly added uppercase root `VISION.md`, both-path conflict, and reintroduced legacy-path assertions.
- 2026-05-01: `python scripts/test-select-validation.py` passed after M1 selector implementation.
- 2026-05-01: `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed.
- 2026-05-01: `python scripts/select-validation.py --mode explicit --path VISION.md` passed and selected `readme.vision_markers`.
- 2026-05-01: `python scripts/select-validation.py --mode explicit --path vision.md` passed and selected `readme.vision_markers`.
- 2026-05-01: `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py` passed and selected `selector.regression`.
- 2026-05-01: `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py` passed.
- 2026-05-01: `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration` passed.
- 2026-05-01: `python scripts/select-validation.py --mode explicit --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md` passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `readme.vision_markers`.
- 2026-05-01: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md` passed.
- 2026-05-01: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed.
- 2026-05-01: `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md` passed.
- 2026-05-01: `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md` passed.
- 2026-05-01: `git diff --check -- docs/plan.md docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md specs/vision-skill-simplification-and-vision-md-migration.md` passed.
- 2026-05-01: the same three commands passed again after the plan-review revisions.
- 2026-05-01: `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md` passed.
- 2026-05-01: `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md` passed.
- 2026-05-01: `git diff --check -- docs/plan.md docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md specs/vision-skill-simplification-and-vision-md-migration.md specs/vision-skill-simplification-and-vision-md-migration.test.md` passed.
- 2026-05-03: `verify` for M1 passed functional selector, metadata, lifecycle, and selected CI checks, but blocked on stale plan and test-spec readiness wording.
- 2026-05-03: `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed after the M1 verify-readiness fix.
- 2026-05-03: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed after the M1 verify-readiness fix.
- 2026-05-03: `python scripts/select-validation.py --mode explicit --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md` passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `readme.vision_markers`.
- 2026-05-03: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md` passed after the M1 verify-readiness fix.
- 2026-05-03: `git diff --check -- docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md specs/vision-skill-simplification-and-vision-md-migration.test.md docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration` passed after the M1 verify-readiness fix.
- 2026-05-03: `python scripts/test-skill-validator.py` failed before M2 authored implementation for the new `VISION.md`, state-based behavior, no-user-facing-mode, and proposal `Vision fit` assertions.
- 2026-05-03: `python scripts/test-skill-validator.py` passed after M2 authored implementation.
- 2026-05-03: `python scripts/validate-skills.py` passed after M2 authored implementation.
- 2026-05-03: `python scripts/validate-readme.py README.md --vision-markers` passed after M2 authored implementation.
- 2026-05-03: `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path README.md --path VISION.md --path vision.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md` passed after M2 authored implementation and selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `readme.validate`, `readme.vision_markers`, and `selector.regression`.
- 2026-05-03: `python scripts/test-select-validation.py` passed after M2 authored implementation.
- 2026-05-03: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/vision-skill.md --path specs/vision-skill.test.md` passed after M2 authored implementation.
- 2026-05-03: `python scripts/build-skills.py --check` failed as expected before M3 because `.codex/skills/proposal`, `.codex/skills/proposal-review`, and `.codex/skills/vision` are stale relative to canonical skills changed in M2.
- 2026-05-03: `python scripts/build-adapters.py --version 0.1.1 --check` failed as expected before M3 because nine generated public adapter skill copies are stale relative to canonical skills changed in M2.
- 2026-05-03: `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path README.md --path VISION.md --path vision.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md` failed as expected at selected check `skills.drift` before M3 generated-output refresh.
- 2026-05-03: `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md README.md VISION.md vision.md specs/vision-skill.md specs/vision-skill.test.md skills/vision/SKILL.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md scripts/test-skill-validator.py` passed after M2 authored implementation.
- 2026-05-03: `python scripts/test-change-metadata-validator.py` passed after M2 lifecycle metadata updates.
- 2026-05-03: `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed after M2 lifecycle metadata updates.
- 2026-05-03: `python scripts/validate-readme.py README.md` passed after M2 authored implementation.
- 2026-05-03: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` passed after approved-spec readiness wording was normalized to avoid stale downstream-stage claims.
- 2026-05-03: `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path README.md --path VISION.md --path vision.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md` passed after M2 lifecycle metadata updates.
- 2026-05-03: `git diff --name-status --find-renames HEAD -- vision.md VISION.md` reported `R100 vision.md VISION.md`, and root directory inspection reported only `./VISION.md`.

## Outcome and Retrospective

M1 is implemented, committed, code-reviewed, and has had verify-readiness wording corrected. M2 authored-surface implementation is complete and ready for code-review. Do not treat the overall initiative as branch-ready until M2 code-review/verify, M3 generated-output refresh, final validation, explain-change, and PR handoff complete.

## Readiness

Ready for `code-review` on M2 authored `VISION.md` migration surfaces. M3 generated-output refresh remains intentionally unstarted until M2 review and verification complete.
