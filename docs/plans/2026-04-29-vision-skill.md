# Vision Skill Execution Plan

- Status: active
- Owner: maintainers
- Start date: 2026-04-29
- Last updated: 2026-04-30
- Related issue or PR: none yet
- Supersedes: none
- broad_smoke_required: true
- broad_smoke_reason: Planned initiative touches governance, public README ownership, canonical skills, generated Codex skill mirrors, generated public adapter packages, lifecycle-managed artifacts, and proposal workflow guidance.

## Purpose / big picture

Implement the approved `vision` skill contract without creating the initial `vision.md` as a side effect. The implementation adds a canonical skill for creating, revising, and mirroring a project vision; aligns proposal and proposal-review guidance around `Vision fit`; records the `vision.md` source-of-truth boundary in governance and workflow docs; and refreshes generated skill and adapter outputs only through existing generators.

The first implementation creates the method and distribution surface. Initial project vision authoring remains a later explicit `vision create` invocation after this skill is accepted and shipped.

## Source artifacts

- Proposal: `docs/proposals/2026-04-29-vision-skill.md`
- Spec: `specs/vision-skill.md`
- Spec review: approved on 2026-04-29 after source-of-truth, marker insertion, normative ID, and exception-recording updates.
- Architecture: not required. The approved spec changes skill, governance, README ownership, and generated distribution surfaces without introducing a service, dependency, persistent data store, runtime boundary, or architecture package change.
- Test spec: `specs/vision-skill.test.md` is active.
- Project map: none exists. Orientation comes from `CONSTITUTION.md`, `AGENTS.md`, `README.md`, `docs/workflows.md`, current skills, validators, and generated adapter layout.

## Context and orientation

- Canonical authored skills live under `skills/`. Generated Codex runtime mirrors under `.codex/skills/` and public adapter packages under `dist/adapters/` must not be hand-edited.
- `skills/vision/SKILL.md` will be a new canonical skill. `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` need targeted guidance for `Vision fit`.
- `CONSTITUTION.md` outranks `vision.md`; the spec requires governance docs to record `vision.md` as the canonical project-vision and proposal-fit reference below the constitution and above generated README front matter.
- `README.md` is public project overview. Its future vision front-matter block is generated from `vision.md`, but this implementation does not create the initial `vision.md` or generated front-matter.
- `docs/workflows.md` documents proposal flow and source ownership; it needs enough guidance to keep `vision` upstream of the per-change lifecycle.
- `scripts/build-skills.py` owns `.codex/skills/` generation. `scripts/build-adapters.py --version 0.1.1` owns public adapter package generation.
- The selector currently treats `README.md` as unclassified. README changes in this initiative use selector inspection plus an explicit manual route instead of pretending selected CI can validate README directly.

## Non-goals

- Create the initial root `vision.md`.
- Insert generated README vision front-matter in this implementation.
- Add `vision` to the normal per-change lifecycle chain.
- Add a README mirror helper script.
- Add validator enforcement for vision prose quality.
- Rewrite existing proposals to add `Vision fit`.
- Change adapter portability rules beyond adding the new canonical skill source and generated copies.
- Hand-edit `.codex/skills/` or `dist/adapters/`.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R4`, `R21`-`R28`, `R56`-`R74` | `skills/vision/SKILL.md` mode contract, vision content rules, README marker contract, reporting, privacy, research, Markdown, and bounded-read guidance |
| `R5`-`R20` | `skills/vision/SKILL.md` create/revise/mirror behavior, existing-vision protection, separate initial vision creation, and change-local revision reminders |
| `R29`-`R39`, `R75`-`R78` | `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` `Vision fit` and conflict-exception guidance |
| `R40`-`R42` | `skills/vision/SKILL.md`, `docs/workflows.md`, and governance wording that keeps `vision` upstream and not a lifecycle stage |
| `R43`-`R45` | `.codex/skills/`, `dist/adapters/`, `dist/adapters/manifest.yaml`, and generated entrypoint refresh through existing generators |
| `R46`-`R55` | `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and README ownership guidance |
| `AC1`-`AC12` | Milestones M1-M4 together |

## Validation command types

This plan uses two validation command types:

- Pass-gate commands are expected to succeed as written and are required for milestone completion.
- Selector inspection / manual-routing proofs are used for unsupported or intentionally unclassified paths. A blocked selector result is expected only when the plan records the manual route that replaces selected CI for that path.

## Milestones

### M1. Add canonical vision skill

- Goal: Add the canonical `vision` skill with create, revise, and mirror mode guidance while explicitly preventing initial `vision.md` creation during this implementation.
- Requirements: `R1`-`R28`, `R40`-`R42`, `R56`-`R74`, `AC1`, `AC2`, `AC8`, `AC11`.
- Files/components likely touched:
  - `skills/vision/SKILL.md`
  - `scripts/test-skill-validator.py`
  - this plan
- Dependencies:
  - approved `specs/vision-skill.md`
  - no helper script and no root `vision.md`
- Tests to add/update:
  - add focused `scripts/test-skill-validator.py` regression coverage for the `vision` skill mode contract, README marker contract, privacy/research boundaries, and bounded-read guidance
- Implementation steps:
  - Add `skills/vision/SKILL.md` with required metadata and concise operational instructions.
  - Include create, revise, and mirror behavior; existing vision overwrite protection; README marker rules; source-of-truth hierarchy; sensitive-data and external-research boundaries; plain Markdown and 500-word limits; and mode reporting.
  - Confirm no root `vision.md` is created.
  - Update this plan progress and validation notes.
- Validation commands:
  - `python scripts/validate-skills.py skills/vision/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `test ! -e vision.md`
  - `rg -n "create|revise|mirror|vision:start|vision:end|500 words|CONSTITUTION.md|README front-matter" skills/vision/SKILL.md`
  - `git diff --check -- skills/vision/SKILL.md docs/plans/2026-04-29-vision-skill.md`
- Expected observable result: the authored `vision` skill is valid, documents the approved behavior, and does not create `vision.md`.
- Commit message: `M1: add canonical vision skill`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - The skill may become too long or behave like a full project-management stage.
- Rollback/recovery:
  - Remove `skills/vision/SKILL.md`; no generated output should be refreshed until M3.

### M2. Align governance and proposal guidance

- Goal: Record the `vision.md` source-of-truth boundary and make proposal/proposal-review behavior check `Vision fit`.
- Requirements: `R29`-`R42`, `R46`-`R55`, `R75`-`R78`, `AC3`-`AC5`, `AC10`, `AC12`.
- Files/components likely touched:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `README.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - this plan
- Dependencies:
  - M1 complete
  - no `vision.md` creation in this milestone
- Tests to add/update:
  - update skill validator fixtures only if canonical skill guidance changes affect fixture expectations
  - no README mirror helper tests in this milestone
- Implementation steps:
  - Update `CONSTITUTION.md` source-of-truth order and governance guidance for `vision.md`.
  - Update `AGENTS.md` and `docs/workflows.md` with concise operational routing: `vision` is upstream, not a normal lifecycle stage; proposals include `Vision fit` after adoption.
  - Update README ownership guidance so future marker-bounded front-matter is generated from `vision.md` and not independently authoritative.
  - Update `skills/proposal/SKILL.md` to require `Vision fit` for new or substantively revised proposals after adoption.
  - Update `skills/proposal-review/SKILL.md` to request missing `Vision fit` and classify conflicts as revise proposal, revise vision, or explicit exception.
  - Update this plan progress and validation notes.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`
  - `python scripts/select-validation.py --mode explicit --path README.md` as selector inspection; expected result is blocked with `unclassified-path`, and the manual route is `git diff --check -- README.md` plus review of README ownership wording against `R51`, `R54`, `R55`, and `AC10`.
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md README.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md docs/plans/2026-04-29-vision-skill.md`
- Expected observable result: contributors and agents have a single source-of-truth story for vision, README front-matter, proposal fit, and exception handling.
- Commit message: `M2: align vision governance and proposal guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Governance wording could accidentally reorder behavior specs below vision for behavior contracts.
  - README changes are not selector-classified.
- Rollback/recovery:
  - Revert the authored guidance changes. Generated outputs are still not refreshed until M3.

### M3. Refresh generated skill and adapter outputs

- Goal: Propagate canonical skill changes to `.codex/skills/` and public adapter packages through existing generators only.
- Requirements: `R43`-`R45`, generated-output portions of `AC6` and `AC7`.
- Files/components likely touched:
  - `.codex/skills/vision/SKILL.md`
  - `.codex/skills/proposal/SKILL.md`
  - `.codex/skills/proposal-review/SKILL.md`
  - `dist/adapters/manifest.yaml`
  - `dist/adapters/codex/AGENTS.md`
  - `dist/adapters/claude/CLAUDE.md`
  - `dist/adapters/opencode/AGENTS.md`
  - `dist/adapters/codex/.agents/skills/vision/SKILL.md`
  - `dist/adapters/codex/.agents/skills/proposal/SKILL.md`
  - `dist/adapters/codex/.agents/skills/proposal-review/SKILL.md`
  - `dist/adapters/claude/.claude/skills/vision/SKILL.md`
  - `dist/adapters/claude/.claude/skills/proposal/SKILL.md`
  - `dist/adapters/claude/.claude/skills/proposal-review/SKILL.md`
  - `dist/adapters/opencode/.opencode/skills/vision/SKILL.md`
  - `dist/adapters/opencode/.opencode/skills/proposal/SKILL.md`
  - `dist/adapters/opencode/.opencode/skills/proposal-review/SKILL.md`
  - this plan
- Dependencies:
  - M1 and M2 complete
- Tests to add/update:
  - no new generator behavior expected; update regression tests only if adding `vision` changes expected inventories
- Implementation steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Inspect generated manifest and adapter output for `vision` inclusion and no opencode command alias unless existing command-alias policy includes it.
  - Update this plan progress and validation notes.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/select-validation.py --mode explicit --path .codex/skills/vision/SKILL.md --path .codex/skills/proposal/SKILL.md --path .codex/skills/proposal-review/SKILL.md --path dist/adapters/manifest.yaml --path dist/adapters/codex/AGENTS.md --path dist/adapters/claude/CLAUDE.md --path dist/adapters/opencode/AGENTS.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/proposal/SKILL.md --path dist/adapters/codex/.agents/skills/proposal-review/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/proposal/SKILL.md --path dist/adapters/claude/.claude/skills/proposal-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal-review/SKILL.md`
  - `git diff --check -- .codex/skills dist/adapters docs/plans/2026-04-29-vision-skill.md`
- Expected observable result: generated Codex and public adapter outputs include the new `vision` skill and updated proposal/review skill copies with no drift.
- Commit message: `M3: refresh generated vision skill outputs`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Generated output may include broad adapter entrypoint changes from updated skill inventory.
- Rollback/recovery:
  - Revert generated outputs and canonical skill changes together, then rerun `python scripts/build-skills.py --check` and `python scripts/build-adapters.py --version 0.1.1 --check`.

### M4. Change-local closeout and full validation handoff

- Goal: Prepare the implemented change for code-review by adding required change-local metadata, proving lifecycle consistency, and running final validation including plan-required broad smoke.
- Requirements: all requirements and `AC1`-`AC12`.
- Files/components likely touched:
  - `docs/changes/2026-04-29-vision-skill/change.yaml`
  - `docs/plans/2026-04-29-vision-skill.md`
  - `docs/plan.md`
  - any files changed in M1-M3
- Dependencies:
  - M1-M3 complete
  - active matching test spec exists before implementation proceeds
- Tests to add/update:
  - as defined by the matching test spec
- Implementation steps:
  - Create `docs/changes/2026-04-29-vision-skill/change.yaml` with proposal, spec, plan, test spec, canonical skill, governance, README, and generated-output artifacts.
  - Update this plan's progress, validation notes, and decision log as needed.
  - Keep `docs/plan.md` synchronized with this plan body.
  - Do not write final `explain-change.md` in this milestone; the `explain-change` stage owns that after verify.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-vision-skill/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-29-vision-skill/change.yaml`
  - `bash scripts/ci.sh --mode broad-smoke`
  - `python scripts/select-validation.py --mode explicit --path README.md` as selector inspection; expected result is blocked with `unclassified-path`, and the manual route is `git diff --check -- README.md` plus documented review of README ownership wording against `R51`, `R54`, `R55`, and `AC10`.
  - `git diff --check -- .`
- Expected observable result: all authored, generated, lifecycle, and change-local surfaces are coherent and ready for code-review; PR/explain readiness still depends on downstream `code-review`, `verify`, and `explain-change`.
- Commit message: `M4: close vision skill implementation`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] broad smoke passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Final validation can expose stale generated output or lifecycle mismatches across proposal, spec, plan, and change metadata.
- Rollback/recovery:
  - Revert the M4 change-local metadata and plan-index updates if earlier milestones need to be reopened.

## Progress

- 2026-04-29: plan created from accepted proposal and approved spec.
- 2026-04-29: plan index updated and plan-creation validation passed.
- 2026-04-30: matching test spec created at `specs/vision-skill.test.md`.
- 2026-04-30: M1 added focused skill-validator regression coverage first, then added `skills/vision/SKILL.md`.
- 2026-04-30: M1 code-review fix clarified that missing README markers stop `mirror` and `revise` before file modification unless explicit handling is authorized.
- 2026-04-30: M2 added `Vision fit` proposal/proposal-review guidance and aligned governance, workflow, and README ownership surfaces around `vision.md`.
- 2026-04-30: CR-M2-F1 tightened absent-root-vision `Vision fit` handling so proposals must use exactly `no vision exists yet` and proposal-review must request revision for nonexistent-vision claims.
- 2026-04-30: M3 refreshed generated `.codex/skills/` and public adapter output through `scripts/build-skills.py` and `scripts/build-adapters.py --version 0.1.1`.

## Decision log

- 2026-04-29: no separate architecture artifact required because the approved spec changes workflow guidance, skills, README ownership, and generated distribution output without a new architecture boundary.
- 2026-04-29: broad smoke required by this plan because the initiative touches governance, README ownership, canonical skills, generated skills, and generated public adapters.
- 2026-04-29: README selector blocking is treated as selector inspection with manual routing because `README.md` is unclassified by the current selector.
- 2026-04-30: M1 intentionally leaves generated `.codex/skills/` and `dist/adapters/` refresh to M3, as planned; selector inspection for the changed canonical skill identifies generated drift checks that are not M1 pass gates.
- 2026-04-30: M2 canonical proposal and proposal-review skill edits also leave generated `.codex/skills/` and `dist/adapters/` refresh to M3, as planned.
- 2026-04-30: M3 did not add an opencode `vision` command alias; opencode command aliases remain limited to the existing curated lifecycle command set while the full `vision` skill is present under opencode skills.

## Surprises and discoveries

- none yet

## Validation notes

- 2026-04-29 plan creation:
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md` selected `artifact_lifecycle.validate` and `broad_smoke.repo`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md` passed, including plan-required broad smoke.
  - `git diff --check -- docs/plan.md docs/plans/2026-04-29-vision-skill.md docs/proposals/2026-04-29-vision-skill.md specs/vision-skill.md` passed.
- 2026-04-30 test spec creation:
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md --path specs/vision-skill.test.md` selected `artifact_lifecycle.validate` and `broad_smoke.repo`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md --path specs/vision-skill.test.md` passed.
  - `git diff --check -- docs/plans/2026-04-29-vision-skill.md specs/vision-skill.test.md` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md --path specs/vision-skill.test.md` passed, including plan-required broad smoke.
- 2026-04-30 M1 implementation:
  - `python scripts/test-skill-validator.py` failed before implementation because `skills/vision/SKILL.md` did not exist after adding the `vision` skill regression test.
  - `python scripts/select-validation.py --mode explicit --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-04-29-vision-skill.md` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, and `broad_smoke.repo`; generated drift and adapter drift checks are deferred to M3 by the approved milestone split.
  - `python scripts/validate-skills.py skills/vision/SKILL.md` passed.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/test-skill-validator.py` passed.
  - `test ! -e vision.md` passed.
  - `rg -n "create|revise|mirror|vision:start|vision:end|500 words|CONSTITUTION.md|README front-matter" skills/vision/SKILL.md` passed.
- 2026-04-30 M1 code-review fix:
  - `python scripts/test-skill-validator.py` failed before the skill edit because the new regression required explicit create-only marker insertion and `mirror`/`revise` stop behavior.
  - `python scripts/test-skill-validator.py` passed after the skill edit.
  - `python scripts/validate-skills.py skills/vision/SKILL.md` passed.
  - `python scripts/validate-skills.py` passed.
  - `test ! -e vision.md` passed.
  - `rg -n "create|revise|mirror|vision:start|vision:end|500 words|CONSTITUTION.md|README front-matter" skills/vision/SKILL.md` passed.
  - `python scripts/select-validation.py --mode explicit --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-04-29-vision-skill.md` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, and `broad_smoke.repo`; generated drift and adapter drift checks remain deferred to M3 by the approved milestone split.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md --path specs/vision-skill.test.md` passed.
  - `git diff --check -- skills/vision/SKILL.md scripts/test-skill-validator.py docs/plans/2026-04-29-vision-skill.md` passed.
- 2026-04-30 M2 implementation:
  - `python scripts/test-skill-validator.py` failed before the M2 edits because the new regression required `Vision fit` and `vision.md` source-of-truth guidance that was not yet present.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/test-skill-validator.py` passed.
  - `test ! -e vision.md` passed.
  - `python scripts/test-select-validation.py` passed.
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, and `selector.regression`; generated drift and adapter drift checks remain deferred to M3 by the approved milestone split.
  - `python scripts/select-validation.py --mode explicit --path README.md` blocked with `unclassified-path` as expected; manual route is README ownership wording review plus `git diff --check -- README.md`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md --path specs/vision-skill.test.md` passed.
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md README.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md docs/plans/2026-04-29-vision-skill.md scripts/test-skill-validator.py` passed.
- 2026-04-30 CR-M2-F1 code-review fix:
  - `python scripts/test-skill-validator.py` failed before the skill edits because the new regression required exact absent-root-vision `Vision fit` behavior.
  - `python scripts/test-skill-validator.py` passed after the skill edits.
  - `python scripts/validate-skills.py` passed.
  - `test ! -e vision.md` passed.
  - `python scripts/test-select-validation.py` passed.
  - `python scripts/select-validation.py --mode explicit --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-04-29-vision-skill.md` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, and `broad_smoke.repo`; generated drift, adapter drift, and broad smoke remain deferred until M3 refreshes generated output.
  - `git diff --check -- skills/proposal/SKILL.md skills/proposal-review/SKILL.md scripts/test-skill-validator.py docs/plans/2026-04-29-vision-skill.md` passed.
- 2026-04-30 M3 implementation:
  - `python scripts/build-skills.py --check` failed before generation because generated proposal and proposal-review skills were stale and `.codex/skills/vision/SKILL.md` was missing.
  - `python scripts/build-adapters.py --version 0.1.1 --check` failed before generation because the manifest omitted `vision`, generated adapter skill files for `vision` were missing, and generated proposal/proposal-review adapter skill files were stale.
  - `python scripts/test-adapter-distribution.py` failed before generation because repository generated adapter output was stale.
  - `python scripts/build-skills.py` passed and refreshed generated `.codex/skills/` output.
  - `python scripts/build-adapters.py --version 0.1.1` passed and refreshed generated public adapter output under `dist/adapters/`.
  - Manifest and file inspection confirmed `vision` is included for codex, claude, and opencode adapters; `.codex/skills/vision/SKILL.md` exists; adapter `vision` skill files exist; opencode command aliases do not include `vision`.
  - `python scripts/build-skills.py --check` passed.
  - `python scripts/test-adapter-distribution.py` passed.
  - `python scripts/build-adapters.py --version 0.1.1 --check` passed.
  - `python scripts/validate-adapters.py --version 0.1.1` passed.
  - `python scripts/select-validation.py --mode explicit --path .codex/skills/vision/SKILL.md --path .codex/skills/proposal/SKILL.md --path .codex/skills/proposal-review/SKILL.md --path dist/adapters/manifest.yaml --path dist/adapters/codex/AGENTS.md --path dist/adapters/claude/CLAUDE.md --path dist/adapters/opencode/AGENTS.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/proposal/SKILL.md --path dist/adapters/codex/.agents/skills/proposal-review/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/proposal/SKILL.md --path dist/adapters/claude/.claude/skills/proposal-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal-review/SKILL.md` selected `skills.drift`, `adapters.regression`, `adapters.drift`, and `adapters.validate`; all selected commands passed.
  - `git diff --check -- .codex/skills dist/adapters docs/plans/2026-04-29-vision-skill.md` passed.
  - `bash scripts/ci.sh --mode broad-smoke` passed.

## Outcome and retrospective

- Active. M1, M2, and M3 are complete; M4 remains pending.

## Readiness

- M1, M2, and M3 are complete.
- The immediate next implementation milestone is M4, `Change-local closeout and full validation handoff`.
