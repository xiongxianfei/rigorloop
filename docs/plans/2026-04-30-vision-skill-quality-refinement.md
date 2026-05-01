# Vision Skill Quality Refinement Execution Plan

- Status: active
- Owner: maintainers
- Start date: 2026-04-30
- Last updated: 2026-05-01
- Related issue or PR: none yet
- Supersedes: none
- broad_smoke_required: false
- broad_smoke_reason: The first refinement is limited to the vision skill contract, matching proof map, focused skill-validator assertions, and generated skill or adapter output. Existing structural and selector-selected checks cover those surfaces without repository broad smoke.

## Purpose / big picture

Implement the approved quality refinement for the already-shipped `vision` skill. The work should make future vision drafts stronger on the first pass, reduce repeated edit-authorization wording inside the skill, make substantive revision traceability enforceable, and keep workflow-fit guidance visible before detailed mode mechanics.

The plan preserves the approved project vision, README marker contract, source-of-truth order, proposal-fit model, 500-word cap, and required `vision.md` section order.

## Source artifacts

- Proposal: `docs/proposals/2026-04-30-vision-skill-quality-refinement.md`
- Spec: `specs/vision-skill.md`, approved on 2026-04-30 after spec-review found no material findings once R81 and R91 were made testable.
- Architecture: not required. The approved proposal and spec change skill guidance, tests, generated output, and lifecycle artifacts without adding a service, dependency, persistent data store, runtime boundary, or architecture package change.
- Test spec: `specs/vision-skill.test.md` is active for this refinement after the 2026-04-30 update covering R19, R81-R94, and AC13-AC19.
- Project map: none required. Orientation comes from `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `skills/vision/SKILL.md`, `specs/vision-skill.test.md`, `scripts/test-skill-validator.py`, and generated-output scripts.

## Context and orientation

- Canonical authored skills live under `skills/`. Generated Codex runtime mirrors under `.codex/skills/` and public adapter packages under `dist/adapters/` must not be hand-edited.
- `skills/vision/SKILL.md` currently has separate `Source Of Truth`, prose `Modes`, `Existing Vision Protection`, and late `Workflow Fit` sections. The approved refinement consolidates edit authorization, moves workflow fit near the top, and converts mode behavior to one Markdown table.
- The current revise-mode guidance says to remind contributors about change-local traceability. The approved refinement requires the causal link before finalizing when a substantive revision is tied to an existing or required change-local pack.
- The existing test spec and `scripts/test-skill-validator.py` already cover the original vision skill behavior. They need focused updates for drafting heuristics, enforceable traceability, workflow-fit placement, and the mode table.
- Root `vision.md` and README front-matter are out of scope for this refinement. Do not revise the approved project vision as part of this plan.

## Non-goals

- Revise the approved root `vision.md`.
- Change README marker behavior or add a README mirror helper script.
- Add `vision` to the normal per-change lifecycle.
- Require naming specific competitor tools.
- Change the 500-word cap or required `vision.md` section order.
- Extract or consolidate shared evidence-collection guidance across portable skills.
- Hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Broaden proposal, proposal-review, governance, or README ownership behavior unless implementation reveals direct drift from the approved spec.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R19`, `R94`, `AC18` | `skills/vision/SKILL.md` revise-mode traceability gate and output reporting; focused test assertions |
| `R81`, `AC15` | `skills/vision/SKILL.md` section order, with workflow-fit guidance immediately after opening purpose/scope paragraphs and before detailed mechanics |
| `R82`-`R90`, `AC13`-`AC14` | `skills/vision/SKILL.md` drafting heuristics phrased as authoring questions or checks, including alternative class or specific tool, pain points, checkable commitments, observable falsifiability, audience fit, and refusals |
| `R91`, `AC16` | one Markdown table for `create`, `revise`, and `mirror`, with exactly the required columns and one row per mode |
| `R92`-`R93`, `AC17` | one edit-authorization section that states source-of-truth order, authorized edit paths, and overwrite protection |
| `R79`-`R80`, `AC9` | selector coverage for `README.md`, root `vision.md`, and README vision-marker validation |
| `R43`-`R45`, `AC6`-`AC7` | generated `.codex/skills/` and `dist/adapters/` output refreshed through existing generators |
| `AC19` | scope control through no shared evidence-boilerplate extraction |

## Validation plan

- Use focused content assertions in `scripts/test-skill-validator.py` to prove the new skill-contract wording that static validation cannot infer.
- Use `python scripts/validate-skills.py` and `python scripts/test-skill-validator.py` for canonical skill validity and contract assertions.
- Use `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, and `python scripts/validate-adapters.py --version 0.1.1` after generated output is refreshed.
- Use selector-selected validation for changed lifecycle, spec, test-spec, skill, generated-output, and change-local paths.
- Use `bash scripts/ci.sh --mode explicit --path ...` for final targeted proof over the changed authoritative paths.

## Milestones

### M1. Update proof map, tests, and canonical vision skill

- Goal: Update the matching test spec and focused assertions first, then revise `skills/vision/SKILL.md` to satisfy the approved quality-refinement contract.
- Requirements: `R19`, `R81`-`R94`, `AC13`-`AC19`.
- Files/components likely touched:
  - `specs/vision-skill.test.md`
  - `scripts/test-skill-validator.py`
  - `skills/vision/SKILL.md`
  - `docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md`
  - this plan
- Dependencies:
  - approved `specs/vision-skill.md`
  - plan-review approval before test-spec and implementation proceed
- Tests to add/update:
  - update the test spec coverage maps for `E8`-`E11`, `R81`-`R94`, and `AC13`-`AC19`
  - add focused assertions for workflow-fit placement, drafting heuristics, one mode table with exact columns and rows, consolidated edit authorization, and enforceable causal-link wording
- Implementation steps:
  - Revise `specs/vision-skill.test.md` after plan approval so it is the active proof map for this refinement.
  - Add or update `scripts/test-skill-validator.py` assertions before changing the skill text.
  - Move workflow-fit guidance immediately after the opening purpose/scope paragraphs.
  - Replace prose mode subsections with one Markdown table for `create`, `revise`, and `mirror`.
  - Consolidate source-of-truth, mode authorization, and overwrite protection into one edit-authorization section.
  - Add drafting heuristics after vision content guidance and before README front-matter guidance.
  - Replace advisory traceability wording with the required causal-link gate and output reporting.
  - Create the baseline change-local artifact pack for this non-trivial implementation and keep generated-output closeout updates for M3.
- Validation commands:
  - `python scripts/validate-skills.py skills/vision/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md`
  - `git diff --check -- specs/vision-skill.test.md scripts/test-skill-validator.py skills/vision/SKILL.md docs/plans/2026-04-30-vision-skill-quality-refinement.md docs/changes/2026-04-30-vision-skill-quality-refinement`
- Expected observable result: the canonical skill is clearer, test assertions prove the new contract shape, and no root `vision.md` or README front-matter content is changed by this milestone.
- Commit message: `M1: refine canonical vision skill guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Consolidating repeated guidance could accidentally weaken overwrite protection or README boundaries.
  - Drafting heuristics could read like new required `vision.md` sections instead of authoring checks.
- Rollback/recovery:
  - Revert `skills/vision/SKILL.md`, `scripts/test-skill-validator.py`, and the test-spec update together, then rerun skill validation.

### M2. Refresh generated skill and adapter output

- Goal: Propagate the canonical `vision` skill refinement to generated runtime and adapter surfaces through existing generators only.
- Requirements: `R43`-`R45`, `AC6`-`AC7`.
- Files/components likely touched:
  - `.codex/skills/vision/SKILL.md`
  - `dist/adapters/codex/.agents/skills/vision/SKILL.md`
  - `dist/adapters/claude/.claude/skills/vision/SKILL.md`
  - `dist/adapters/opencode/.opencode/skills/vision/SKILL.md`
  - generated adapter manifest or entrypoint files only if the generator updates them
  - this plan
- Dependencies:
  - M1 complete
- Tests to add/update:
  - no new generator behavior expected; update generator tests only if the generated inventory changes beyond `vision` skill content
- Implementation steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Inspect generated output for expected `vision` skill changes and no unrelated generated-output drift.
  - Update this plan progress and validation notes.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/select-validation.py --mode explicit --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md`
  - `git diff --check -- .codex/skills/vision/SKILL.md dist/adapters docs/plans/2026-04-30-vision-skill-quality-refinement.md`
- Expected observable result: generated Codex and public adapter skill copies match the canonical `vision` skill with no hand edits.
- Commit message: `M2: refresh generated vision skill refinement`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Generator output may include broader adapter text churn if templates or manifests derive from changed skill metadata.
- Rollback/recovery:
  - Revert generated output and rerun generator check commands; if canonical skill changes are reverted, regenerate again from the reverted source.

### M3. Change-local closeout and targeted validation

- Goal: Finalize the change-local artifact pack, synchronize lifecycle state, and prove the refinement is ready for code-review.
- Requirements: all requirements in this plan and `AC13`-`AC19`.
- Files/components likely touched:
  - `docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `docs/plans/2026-04-30-vision-skill-quality-refinement.md`
  - `docs/plan.md`
  - changed files from M1 and M2
- Dependencies:
  - M1 and M2 complete
  - matching test spec active
- Tests to add/update:
  - as defined by the revised matching test spec
- Implementation steps:
  - Update `docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml` with generated-output artifacts and final validation evidence.
  - Update this plan's progress, validation notes, and decision log as needed.
  - Keep `docs/plan.md` synchronized with this plan body.
  - Keep M1 `explain-change.md` as implementation rationale; the `explain-change` stage owns final post-verify explanation.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `git diff --check -- .`
- Expected observable result: lifecycle artifacts, proof map, canonical skill, focused tests, generated output, and change-local metadata are coherent and ready for first-pass `code-review`.
- Commit message: `M3: close vision skill refinement`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Lifecycle validation can expose drift between the approved spec, test spec, plan, and change metadata.
- Rollback/recovery:
  - Revert M3 lifecycle metadata first if earlier milestones need to reopen, then rerun lifecycle validation on the remaining touched artifacts.

## Risks and recovery

- Risk: The skill becomes more prescriptive than the spec intended.
  Recovery: keep heuristics as questions or checks, and reject wording that creates new `vision.md` sections or competitor-name requirements.
- Risk: The mode table loses detail that was previously present in prose.
  Recovery: treat R5-R20 and R69-R74 as regression constraints while converting to the table.
- Risk: Generated output drifts from canonical skill sources.
  Recovery: rerun `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1`, then rerun drift checks.
- Risk: Current root `vision.md` or README front-matter gets pulled into the refinement.
  Recovery: keep those files out of milestone write scopes unless a later explicit request changes scope.

## Dependencies

- Plan-review approval is required before updating the test spec and implementing.
- The revised test spec must be active before implementation starts.
- Existing generators must remain the only path for `.codex/skills/` and `dist/adapters/` output.
- No external services, new dependencies, or architecture package are required.

## Progress

- 2026-04-30: plan created from the accepted proposal and approved spec.
- 2026-04-30: plan-review approved with no material findings.
- 2026-04-30: matching test spec updated as the active proof map for this refinement.
- 2026-04-30: M1 focused assertions added to `scripts/test-skill-validator.py`; they failed before the canonical skill revision as expected.
- 2026-04-30: M1 canonical `skills/vision/SKILL.md` revision completed; focused skill-validator assertions pass.
- 2026-04-30: M1 baseline change-local artifact pack created early for durable implementation traceability.
- 2026-04-30: M1 targeted validation passed; generated skill and adapter drift checks are intentionally deferred to M2.
- 2026-04-30: M2 generated Codex and public adapter vision skill output refreshed through `scripts/build-skills.py` and `scripts/build-adapters.py --version 0.1.1`.
- 2026-04-30: M2 targeted generator, adapter, selector, and explicit CI validation passed.
- 2026-04-30: M3 lifecycle handoff text updated in the accepted proposal, approved spec, active test spec, active plan, and change-local evidence.
- 2026-04-30: M3 final targeted validation passed; implementation is ready for first-pass `code-review`.
- 2026-04-30: Code review found CR1-F1, a missing explicit revise-mode ask-or-confirm gate for `substantive` versus `editorial` classification.
- 2026-04-30: CR1-F1 accepted and fixed in the canonical `vision` skill, focused skill-validator assertions, generated Codex skill output, and generated public adapter output.
- 2026-04-30: Review log and review-resolution artifacts added for CR1-F1 and closed after targeted validation.
- 2026-04-30: `code-review-r2` returned `clean-with-notes` with no blocking or required-change findings after the CR1-F1 fix.
- 2026-04-30: `verify` initially found stale tracked lifecycle state because the clean code-review rerun had not been recorded durably; review and readiness artifacts were synchronized before rerunning validation.
- 2026-04-30: `verify` passed with verdict `ready`; branch-ready is satisfied and the next workflow stage is `explain-change`.
- 2026-05-01: A follow-up verify pass found root `vision.md` blocked PR-mode CI as `unclassified-path`; selector coverage and regression tests were added for root `vision.md`.
- 2026-05-01: `code-review-r3` reviewed the post-`code-review-r2` diff, including root `vision.md`, README front-matter, lifecycle sync, and selector coverage, and returned `clean-with-notes` with no material findings.

## Decision log

- 2026-04-30: Architecture is not required because the refinement changes guidance, tests, generated output, and lifecycle artifacts without introducing a new runtime or design boundary.
- 2026-04-30: Repository broad smoke is not required by this plan; targeted structural, generator, adapter, selector, and lifecycle checks cover the touched surfaces.
- 2026-04-30: M1 creates the baseline change-local pack before M3 because implementation-stage changes are non-trivial; M3 remains responsible for generated-output and final closeout updates.
- 2026-04-30: Claude and opencode generated skill copies intentionally omit `argument-hint`; Codex runtime and Codex adapter copies match the canonical skill byte-for-byte.
- 2026-04-30: `docs/plan.md` remains unchanged in M3 because the initiative stays in Active until downstream code-review, verify, explain-change, PR, and final Done closeout.
- 2026-04-30: CR1-F1 is handled as review-resolution rather than changing the approved spec because R18 and T2 already required the ask-or-confirm gate.
- 2026-04-30: `code-review-r2` is recorded as a tracked clean review artifact because branch-ready cannot rely on a chat-only review result. `docs/plan.md` remains Active after verify because explain-change, PR handoff, and final Done closeout are still downstream.
- 2026-05-01: Root `vision.md` selector coverage is treated as part of `R79`-`R80` because the repository now has a tracked root vision artifact, and PR-mode CI must route it instead of blocking as unclassified.

## Surprises and discoveries

- none yet

## Validation notes

- 2026-04-30: test-spec authoring validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md`
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-04-30-vision-skill-quality-refinement.md docs/proposals/2026-04-30-vision-skill-quality-refinement.md specs/vision-skill.md specs/vision-skill.test.md README.md vision.md`
- 2026-04-30: M1 test-first proof:
  - `python scripts/test-skill-validator.py` failed before revising `skills/vision/SKILL.md` because the new workflow-fit placement, drafting-heuristic, edit-authorization, mode-table, and causal-link assertions were not yet satisfied.
  - `python scripts/test-skill-validator.py` passed after revising `skills/vision/SKILL.md`.
- 2026-04-30: M1 targeted validation passed:
  - `python scripts/validate-skills.py skills/vision/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.test.md`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-readme.py README.md --vision-markers`
  - `git diff --check -- specs/vision-skill.test.md scripts/test-skill-validator.py skills/vision/SKILL.md docs/plans/2026-04-30-vision-skill-quality-refinement.md docs/changes/2026-04-30-vision-skill-quality-refinement`
- 2026-04-30: selector inspection passed with generated-output checks deferred to M2:
  - `python scripts/select-validation.py --mode explicit --path specs/vision-skill.test.md --path scripts/test-skill-validator.py --path skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md`
- 2026-04-30: M2 pre-generation drift proof failed as expected:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
- 2026-04-30: M2 generated output refresh completed:
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
- 2026-04-30: M2 targeted validation passed:
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/select-validation.py --mode explicit --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md`
  - `bash scripts/ci.sh --mode explicit --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md`
- 2026-04-30: M2 full selected CI over generated output plus updated plan and change-local evidence passed:
  - `bash scripts/ci.sh --mode explicit --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md`
- 2026-04-30: M3 final targeted validation passed:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md`
  - `git diff --check -- .`
- 2026-04-30: CR1-F1 regression proof and generated-output validation passed:
  - `python scripts/test-skill-validator.py` failed before the canonical skill fix for the new ask-or-confirm assertion.
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-04-30-vision-skill-quality-refinement`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-30-vision-skill-quality-refinement`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md`
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `readme.vision_markers`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md`
  - `bash scripts/ci.sh --mode broad-smoke`
  - `git diff --check -- .`
- 2026-04-30: post-code-review lifecycle sync validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-30-vision-skill-quality-refinement`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md`
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r2.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r2.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md`
  - `git diff --check -- docs/changes/2026-04-30-vision-skill-quality-refinement docs/plans/2026-04-30-vision-skill-quality-refinement.md`
- 2026-05-01: root `vision.md` selector regression proof passed:
  - `python scripts/test-select-validation.py ValidationSelectionTests.test_root_vision_path_selects_marker_validation_without_unclassified_block ValidationSelectionTests.test_pr_mode_routes_root_vision_without_unclassified_block` failed before the selector fix because root `vision.md` was unclassified.
  - `python scripts/test-select-validation.py ValidationSelectionTests.test_root_vision_path_selects_marker_validation_without_unclassified_block ValidationSelectionTests.test_pr_mode_routes_root_vision_without_unclassified_block`
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path .codex/skills/vision/SKILL.md --path README.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r2.md --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path scripts/test-skill-validator.py --path scripts/test-select-validation.py --path scripts/validation_selection.py --path skills/vision/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path vision.md`
  - `bash scripts/ci.sh --mode explicit --path .codex/skills/vision/SKILL.md --path README.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r2.md --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path scripts/test-skill-validator.py --path scripts/test-select-validation.py --path scripts/validation_selection.py --path skills/vision/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path vision.md`
- 2026-05-01: `code-review-r3` focused proof passed:
  - `python scripts/test-select-validation.py ValidationSelectionTests.test_root_vision_path_selects_marker_validation_without_unclassified_block ValidationSelectionTests.test_pr_mode_routes_root_vision_without_unclassified_block`
  - `python scripts/select-validation.py --mode explicit --path vision.md --path README.md --path scripts/validation_selection.py --path scripts/test-select-validation.py` selected `readme.validate`, `readme.vision_markers`, and `selector.regression`
  - `python scripts/validate-readme.py README.md --vision-markers`
  - `git diff --check fd7111d..2d83ac1 --`
- 2026-05-01: `code-review-r3` lifecycle and review-artifact validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-30-vision-skill-quality-refinement`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md`
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r3.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md` selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `readme.vision_markers`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r3.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md`

## Outcome and retrospective

- Implementation milestones M1-M3 are complete, CR1-F1 review-resolution is closed, `code-review-r2` and `code-review-r3` are clean, and the root `vision.md` selector blocker found by verify is fixed with regression coverage. Outcome remains open until verify rerun, explain-change, PR handoff, and final closeout.

## Readiness

- Root `vision.md` selector blocker is fixed and `code-review-r3` is clean. The initiative is ready for `verify` rerun; `explain-change`, `pr-body-ready`, and `pr-open-ready` remain downstream.

## Risks and follow-ups

- Follow-up only if implementation reveals broader drift in proposal, proposal-review, governance, or README ownership guidance.
