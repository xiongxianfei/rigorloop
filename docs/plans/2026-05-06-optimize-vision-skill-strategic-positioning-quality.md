# Optimize Vision Skill Strategic Positioning Quality Execution Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-06
- Last updated: 2026-05-07
- Related issue or PR: none yet
- Supersedes: none
- broad_smoke_required: false
- broad_smoke_reason: This change updates workflow-governance artifacts, skill guidance, repository validation, tests, generated skill output, adapter output, and vision rationale artifacts. It does not add runtime data flow, storage, network boundaries, deployment behavior, release packaging, schemas, or external integrations that require repository broad smoke by default.

## Purpose / Big Picture

Implement the accepted strategic-positioning refinement for the `vision` skill. The work should make the skill identify the true project category before drafting or materially repositioning `VISION.md`, preserve the rationale in `docs/vision/strategic-positioning.md` when required, and prevent a lower-level compatibility surface such as Git, CI, repository layout, or package format from becoming the headline when a higher-level methodology or workflow category is present.

The work also retires active lowercase `vision.md` migration behavior from user-facing guidance and repository validation. Historical records may continue to mention lowercase `vision.md`; active skill behavior and repo-owned validation should treat root `VISION.md` as the only supported project-vision artifact.

## Source Artifacts

- Proposal: [Optimize Vision Skill Strategic Positioning Quality](../proposals/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md), accepted on 2026-05-06.
- Spec: [Vision Skill](../../specs/vision-skill.md), approved after `spec-review-r3` on 2026-05-06.
- Architecture: not required. The accepted proposal and approved spec change authored guidance, tests, selectors, validation, generated outputs, and durable rationale artifacts without adding or changing a runtime boundary, data store, network integration, deployment boundary, external dependency, or architecture package.
- Test spec: [Vision Skill Test Spec](../../specs/vision-skill.test.md) is active for the strategic-positioning contract and retired lowercase `vision.md` behavior.
- Project map: none present. Orientation comes from `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `VISION.md`, `README.md`, `specs/vision-skill.md`, `specs/vision-skill.test.md`, `skills/vision/SKILL.md`, `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, selector and skill-validator tests, generated-output scripts, and the change-local review records.
- Review records: [review log](../changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-log.md), [review resolution](../changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-resolution.md), and detailed review records under `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/reviews/`.

## Context and Orientation

- Canonical authored skills live under `skills/`. Generated Codex runtime mirrors under `.codex/skills/` and public adapter packages under `dist/adapters/` must be refreshed through generators, not hand-edited.
- `skills/vision/SKILL.md` still has migration-era behavior for legacy root `vision.md` and a 500-word cap. The approved spec replaces that with a 750-word normal cap, a hard 900-word maximum, strategic-positioning guidance, and retired lowercase path behavior.
- `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` still mention migration-recognized legacy root `vision.md`. The approved spec requires active proposal and proposal-review guidance to use root `VISION.md` and not preserve lowercase no-vision exceptions.
- `scripts/validation_selection.py` currently classifies both `vision.md` and `VISION.md` as root vision paths and carries a both-file conflict check. The approved spec requires selector routing and repo-owned validation not to classify root `vision.md` as a supported root vision surface, migration input, conflict participant, or no-vision exception.
- `specs/vision-skill.test.md` is active for the consolidated vision skill contract and now covers `E9`-`E13`, `R73`-`R86`, the 750/900-word policy, `docs/vision/strategic-positioning.md`, lowercase path retirement, selector negative proof for root `vision.md`, generated-output drift, and change-local rationale for the current material repositioning.
- `scripts/test-skill-validator.py` contains focused assertions for the old migration model. Those assertions must be replaced or extended before canonical skill changes are made.
- The current branch includes a material project-vision repositioning in `VISION.md`, README front-matter, and `CONSTITUTION.md`. Because the approved spec requires durable rationale for material repositioning, this plan includes creating `docs/vision/strategic-positioning.md` and summarizing the positioning delta in the change-local explanation before PR handoff.

## Non-Goals

- Do not turn `VISION.md` into a proposal, spec, architecture document, roadmap, task tracker, feature list, requirements list, or project-management system.
- Do not make `docs/vision/strategic-positioning.md` independently authoritative over `VISION.md`.
- Do not make `vision` a normal per-change lifecycle stage or add a separate `vision-review` skill.
- Do not require external research for ordinary vision drafting.
- Do not add a prompt-output quality harness in this slice.
- Do not force every project into the RigorLoop methodology pattern.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not rewrite historical proposals, specs, plans, reviews, change-local artifacts, or PR records solely to replace old lowercase `vision.md` text.
- Do not change runtime behavior, release packaging, schemas, deployment behavior, or adapter runtime execution.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R8`, `AC1`, `AC8`-`AC10` | active governance, workflow, README, proposal, proposal-review, vision skill, selector, validation, and test guidance aligned on root `VISION.md`; historical lowercase references preserved only as archival text |
| `R9`-`R19`, `AC2` | canonical `skills/vision/SKILL.md`, focused skill-validator assertions, and generated skill/adapter output for state-based interface and required reporting |
| `R20`-`R31`, `AC3`-`AC4` | `skills/vision/SKILL.md` establishment, update, sync, overwrite, substantive/editorial, change-local causal-link, and retired root `vision.md` boundaries |
| `R32`-`R39`, `R73`-`R86`, `AC10`-`AC16` | strategic-positioning pass, anti-anchor rule, methodology-as-product guidance, 750/900-word policy, optional methodology section, final quality gates, `docs/vision/strategic-positioning.md`, and focused static assertions |
| `R40`-`R48`, `AC3`, `AC5` | README marker contract and front-matter derivation preserved in skill guidance, README validation, and README front-matter diff review |
| `R49`-`R62`, `AC6`-`AC7` | `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, and skill-validator assertions for `Vision fit` behavior against `VISION.md` without lowercase migration exceptions |
| `R63`-`R67`, `AC8`-`AC9` | workflow boundary, generated-output ownership, selector routing for `VISION.md`, and removal of supported root `vision.md` routing or conflict behavior |
| `R68`-`R72` | publication safety, research boundaries, researched-fact reporting, and bounded evidence collection in canonical skill guidance |

## Immediate Test-Spec Handoff

`plan-review` approved this plan on 2026-05-06 with no material findings. The focused `test-spec` stage is complete, and `specs/vision-skill.test.md` is the active proof map for implementation.

The active test spec maps every new or changed `MUST` requirement and `AC11`-`AC16` to concrete proof surfaces. It covers strategic-positioning static assertions, methodology and substrate fixtures, the 750/900-word policy, `docs/vision/strategic-positioning.md` creation/update/no-update behavior, retired lowercase `vision.md` behavior, selector routing changes, generated-output drift checks, and change-local rationale for substantive repositioning.

Implementation may now start at M1. Within implementation milestones, add or update the relevant assertions before changing the corresponding behavior, and close each milestone only after the paired implementation makes the milestone validation pass.

## Milestones

### M1. Update Proof Map, Static Assertions, and Selector Behavior

- Goal: Make the proof surfaces enforce the approved strategic-positioning contract and retired lowercase path behavior.
- Requirements: `R7`-`R8`, `R32`-`R39`, `R63`-`R67`, `R73`-`R86`, `AC8`-`AC16`.
- Files/components likely touched:
  - `specs/vision-skill.test.md`
  - `scripts/test-skill-validator.py`
  - `scripts/test-select-validation.py`
  - `scripts/validation_selection.py`
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - this plan
- Dependencies:
  - `plan-review` approval
  - active revised `specs/vision-skill.test.md`
- Tests to add/update:
  - requirement and acceptance-criteria coverage for `R73`-`R86` and `AC11`-`AC16`
  - static assertions for strategic-positioning pass fields, anti-anchor guidance, methodology-as-product guidance, pitch quality, word-budget policy, optional-section guard, final quality gates, and output reporting
  - fixture-style assertions for RigorLoop methodology, ordinary implementation substrate, and true substrate project categories
  - selector tests proving root `VISION.md` remains supported and root `vision.md` is no longer a supported root vision surface, migration input, root-vision conflict participant, or no-vision exception
- Implementation steps:
  - Update `specs/vision-skill.test.md` as the active proof map after plan-review.
  - Add or update focused skill-validator assertions before changing canonical skill text.
  - Update selector tests before changing selector behavior.
  - Revise `scripts/validation_selection.py` to remove active root `vision.md` support and conflict/no-vision behavior while preserving historical artifact tolerance outside active validation behavior.
  - Confirm targeted tests fail for the old contract before paired implementation where practical, then pass after the selector and assertion updates.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path VISION.md`
  - `python scripts/select-validation.py --mode explicit --path vision.md`
  - `python scripts/select-validation.py --mode explicit --path specs/vision-skill.test.md --path scripts/test-skill-validator.py --path scripts/test-select-validation.py --path scripts/validation_selection.py`
  - `bash scripts/ci.sh --mode explicit --path specs/vision-skill.test.md --path scripts/test-skill-validator.py --path scripts/test-select-validation.py --path scripts/validation_selection.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - `git diff --check -- specs/vision-skill.test.md scripts/test-skill-validator.py scripts/test-select-validation.py scripts/validation_selection.py docs/plans/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality`
- Expected observable result: tests and selector output enforce the new strategic-positioning and lowercase-retirement contract without relying on prompt-output evaluation.
- Commit message: `M1: prove strategic vision skill contract`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Static assertions can become brittle if they overfit exact prose instead of durable contract phrases.
  - Removing lowercase routing can accidentally make historical lowercase references look invalid rather than merely archival.
- Rollback/recovery:
  - Revert test and selector changes together, then rerun selector and skill-validator tests to restore the previous validation contract.

### M2. Update Canonical Skill Guidance and Vision Rationale Artifacts

- Goal: Implement the approved authored guidance and durable rationale behavior in canonical project files.
- Requirements: `R1`-`R62`, `R68`-`R86`, `AC1`-`AC16`.
- Files/components likely touched:
  - `skills/vision/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `CONSTITUTION.md`
  - `VISION.md`
  - `README.md`
  - `docs/vision/strategic-positioning.md`
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md`
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - this plan
- Dependencies:
  - M1 proof updates complete
  - active revised test spec
- Tests to add/update:
  - no additional test families expected beyond M1; update assertions only if canonical guidance reveals a gap in the proof map
- Implementation steps:
  - Update `skills/vision/SKILL.md` with the strategic-positioning pass, required fields, durable rationale path, authority rule, anti-anchor guidance, methodology-as-product guidance, 750/900-word policy, optional methodology section rule, final quality gates, and final-output reporting.
  - Remove active migration handling for root `vision.md` from `skills/vision/SKILL.md`; requests to read, edit, merge, delete, or migrate that path should stop with a canonical-path explanation unless the owner gives a separate non-vision-file instruction.
  - Update `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` so `Vision fit` behavior is anchored to root `VISION.md` and no longer preserves migration-recognized lowercase `vision.md` exceptions.
  - Preserve README marker safety, existing-vision overwrite protection, substantive/editorial confirmation, change-local causal-link gating, security boundaries, and research boundaries.
  - Create `docs/vision/strategic-positioning.md` for the current material RigorLoop vision repositioning, with compact sections for category, primary user, primary pain, primary promise, core mechanism, alternatives, tradeoff, compatibility surfaces, refusals, falsifiability, and authority wording.
  - Record the positioning delta and link to `docs/vision/strategic-positioning.md` in `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md`.
  - Confirm `CONSTITUTION.md`, `VISION.md`, and README front-matter remain aligned with the accepted higher-level project category and do not become feature lists or requirements docs.
- Validation commands:
  - `python scripts/validate-skills.py skills/vision/SKILL.md`
  - `python scripts/validate-skills.py skills/proposal/SKILL.md`
  - `python scripts/validate-skills.py skills/proposal-review/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-readme.py README.md --vision-markers`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path CONSTITUTION.md --path README.md --path VISION.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/vision/strategic-positioning.md --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md --path docs/plans/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path README.md --path VISION.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path docs/vision/strategic-positioning.md --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md`
  - `git diff --check -- CONSTITUTION.md README.md VISION.md specs/vision-skill.md specs/vision-skill.test.md skills/vision/SKILL.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md docs/vision docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality docs/plans/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md`
- Expected observable result: canonical authored guidance implements the approved contract, active lowercase migration behavior is retired, and the current material vision repositioning has durable rationale.
- Commit message: `M2: update strategic vision guidance`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Adding strategic-positioning guidance could turn into a required `VISION.md` worksheet or feature list if the skill prose is too prescriptive.
  - Removing lowercase handling could weaken ordinary file-safety behavior for explicit non-vision requests about root `vision.md`.
  - The positioning rationale could be mistaken for a second source of truth.
- Rollback/recovery:
  - Revert canonical guidance and rationale artifacts together, rerun skill validation and README marker validation, and keep `VISION.md` canonical.

### M3. Refresh Generated Skill and Adapter Output

- Goal: Propagate canonical skill changes to generated runtime and adapter surfaces through repository generators.
- Requirements: `R9`-`R11`, `R63`-`R65`, and generated-output proof for all changed skill guidance.
- Files/components likely touched:
  - `.codex/skills/vision/SKILL.md`
  - `.codex/skills/proposal/SKILL.md`
  - `.codex/skills/proposal-review/SKILL.md`
  - generated public adapter skill copies under `dist/adapters/`
  - generated adapter manifests or command files only if generator output changes them
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - this plan
- Dependencies:
  - M1 through M2 complete
- Tests to add/update:
  - no new generator behavior expected; add generator tests only if the generated inventory changes beyond expected skill content propagation
- Implementation steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Inspect generated diffs for expected `vision`, `proposal`, and `proposal-review` skill changes only.
  - Keep generated outputs derived from canonical `skills/` sources; do not patch generated files manually.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/select-validation.py --mode explicit --path .codex/skills/vision/SKILL.md --path .codex/skills/proposal/SKILL.md --path .codex/skills/proposal-review/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/proposal/SKILL.md --path dist/adapters/codex/.agents/skills/proposal-review/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/proposal/SKILL.md --path dist/adapters/claude/.claude/skills/proposal-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal-review/SKILL.md`
  - `bash scripts/ci.sh --mode explicit --path .codex/skills/vision/SKILL.md --path .codex/skills/proposal/SKILL.md --path .codex/skills/proposal-review/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/proposal/SKILL.md --path dist/adapters/codex/.agents/skills/proposal-review/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/proposal/SKILL.md --path dist/adapters/claude/.claude/skills/proposal-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal-review/SKILL.md`
  - `git diff --check -- .codex/skills dist/adapters docs/plans/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md`
- Expected observable result: generated Codex and public adapter outputs match canonical skill guidance with no hand edits or unrelated generated churn.
- Commit message: `M3: refresh strategic vision generated output`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Generated output may include broader adapter churn if adapter templates or manifests derive from changed skill metadata.
- Rollback/recovery:
  - Revert generated output and rerun generator check commands; if canonical skill changes are reverted, regenerate from the reverted source.

### M4. Final Lifecycle Closeout and Validation Evidence

- Goal: Synchronize lifecycle artifacts, prove the full planned change, and prepare for review and PR handoff.
- Requirements: all requirements covered by this plan.
- Files/components likely touched:
  - `docs/plan.md`
  - this plan
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md`
  - final changed authored and generated surfaces from M1 through M3
- Dependencies:
  - M1 through M3 complete
  - code-review, review-resolution when triggered, verify, explain-change, and PR handoff sequencing after implementation
- Tests to add/update:
  - none expected beyond the active test spec and milestone proof surfaces
- Implementation steps:
  - Update this plan's progress, decision log, surprises, validation notes, outcome, and readiness as milestones complete.
  - Update `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml` with final changed files and validation evidence.
  - Keep `docs/plan.md` synchronized with this plan body when lifecycle state changes. If the PR claims this initiative is complete, move both the plan index entry and this plan body to Done before PR review opens.
  - Run final targeted validation over authored, test, selector, generated, review, plan, and change-local artifacts.
  - Leave the plan Active if a true downstream completion event remains; merge itself is not a downstream completion event.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md --path docs/proposals/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/vision/strategic-positioning.md --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-log.md --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-resolution.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-readme.py README.md --vision-markers`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path README.md --path VISION.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path .codex/skills/vision/SKILL.md --path .codex/skills/proposal/SKILL.md --path .codex/skills/proposal-review/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/proposal/SKILL.md --path dist/adapters/codex/.agents/skills/proposal-review/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/proposal/SKILL.md --path dist/adapters/claude/.claude/skills/proposal-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal-review/SKILL.md --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/test-skill-validator.py --path docs/vision/strategic-positioning.md --path docs/plan.md --path docs/plans/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - `git diff --check -- .`
- Expected observable result: lifecycle artifacts are synchronized, review findings are closed, targeted validation passes, and the change is ready for first-pass `code-review` or later PR handoff depending on the workflow point.
- Commit message: `M4: close strategic vision lifecycle`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Lifecycle closeout can become stale if later code-review, verify, or PR readiness discovers missing evidence.
- Rollback/recovery:
  - Reopen this plan and the plan index together if downstream review or verification requires additional work; keep review-resolution open while material findings remain unresolved.

## Validation Plan

Validation proceeds from focused proof to generated-output drift and final lifecycle checks:

- Test-spec proof: `specs/vision-skill.test.md` maps changed requirements, examples, edge cases, and acceptance criteria to concrete tests.
- Skill proof: `python scripts/validate-skills.py` and `python scripts/test-skill-validator.py`.
- Selector proof: `python scripts/test-select-validation.py`, explicit selection for root `VISION.md`, explicit selection for root `vision.md`, and selector-selected CI.
- README proof: `python scripts/validate-readme.py README.md --vision-markers`.
- Generated-output proof: `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/test-adapter-distribution.py`, and `python scripts/validate-adapters.py --version 0.1.1`.
- Review and lifecycle proof: review artifact structure/closeout validation, change metadata validation, artifact lifecycle validation over the touched proposal, spec, test spec, plan, review, rationale, and change-local artifacts.
- Final whitespace proof: `git diff --check -- .` plus targeted trailing-whitespace scan when needed.

Repository broad smoke is not planned by default. If plan-review, test-spec, selector output, review-resolution, verify, release metadata, or another authoritative artifact later requires broad smoke, record the trigger in this plan and run `bash scripts/ci.sh --mode broad-smoke`.

## Risks and Recovery

- Risk: Strategic-positioning guidance becomes a second vision document or a required `VISION.md` worksheet.
  Recovery: keep `docs/vision/strategic-positioning.md` explicitly supporting and non-authoritative; keep the skill guidance framed as pre-drafting checks and rationale output.
- Risk: The skill overfits to RigorLoop and weakens ordinary product or true-substrate cases.
  Recovery: include static assertions or fixture text for methodology, ordinary product with implementation substrate, and true substrate product examples.
- Risk: Retiring lowercase `vision.md` behavior accidentally rewrites historical records or breaks explicit non-vision file requests.
  Recovery: preserve historical-reference non-rewrite rules and keep explicit owner non-vision-file instructions as the path for ordinary file handling.
- Risk: Removing selector support for lowercase `vision.md` leaves path changes unclassified.
  Recovery: update selector tests for the approved retired behavior and use explicit-mode CI over changed selector and skill surfaces.
- Risk: Generated output is edited by hand or drifts from canonical skills.
  Recovery: regenerate through `scripts/build-skills.py` and `scripts/build-adapters.py --version 0.1.1`, then rerun drift checks.
- Risk: The current material vision repositioning lacks durable rationale.
  Recovery: create `docs/vision/strategic-positioning.md` and record the change-local delta in `explain-change.md` during M2.

## Dependencies

- `plan-review` approval is required before test-spec authoring and implementation.
- A revised `specs/vision-skill.test.md` must be active before implementation begins.
- No architecture package or ADR is required unless plan-review discovers a design boundary not visible in the approved proposal/spec.
- Existing generators must remain the only write path for `.codex/skills/` and `dist/adapters/` output.
- Review-resolution is closed after resolving `CR1-F1`; reopen it only if a later formal review produces material findings.

## Progress

- [x] 2026-05-06: proposal accepted after proposal-review scope clarification for lowercase `vision.md` retirement.
- [x] 2026-05-06: spec updated and approved after `spec-review-r3`; `SR1-F1` and `SR2-F1` are closed.
- [x] 2026-05-06: execution plan created and indexed for plan-review.
- [x] 2026-05-06: plan-review approved with no material findings; minor selector expectation note captured in the active test spec.
- [x] 2026-05-06: `specs/vision-skill.test.md` updated as the active strategic-positioning proof map.
- [x] M1 complete: proof map, static assertions, and selector behavior updated.
- [x] M2 complete: canonical skill guidance and vision rationale artifacts updated.
- [x] M3 complete: generated skill and adapter output refreshed.
- [x] M4 complete: lifecycle closeout and final validation evidence synchronized.
- [x] code-review finding `CR1-F1` resolved with static assertion coverage, canonical skill fix, generated-output refresh, and review-resolution closeout evidence.
- [x] code-review rerun clean.

## Decision Log

- 2026-05-06: Architecture package not required. The approved proposal states no runtime data flow, storage, network boundary, or deployment boundary is expected; the implementation stays in authored guidance, validation, tests, and generated outputs.
- 2026-05-06: Split selector/test proof from canonical skill guidance and generated-output refresh. This keeps the highest-risk behavior changes reviewable and preserves the repository's test-first implementation rule.
- 2026-05-06: Include `docs/vision/strategic-positioning.md` in implementation scope for the current RigorLoop vision repositioning. The branch already materially re-centers the project vision, and the approved spec requires durable rationale for material repositioning.
- 2026-05-06: Do not add a prompt-output evaluation harness. The accepted proposal selected static assertions for this slice.
- 2026-05-06: Close M1, M2, and M3 as a coupled implementation group. M1 static assertions target canonical M2 guidance, and M2 canonical skill changes intentionally trigger generated-output drift that only M3 can resolve.

## Surprises and Discoveries

- 2026-05-06: The original M2 validation command used `python scripts/validate-skills.py` with three positional skill targets, but the script accepts at most one optional target. The plan now records one command per target plus the full validation command.
- 2026-05-06: `docs/vision/strategic-positioning.md` was initially unclassified by `scripts/validation_selection.py`, which blocked selected CI for the new durable rationale path. The selector now treats `docs/vision/*.md` as lifecycle-managed Markdown and selects artifact lifecycle validation.
- 2026-05-06: M2 selected CI correctly failed on `skills.drift` and `adapters.drift` before M3, proving the generated Codex and adapter outputs had to be refreshed in the same implementation slice.

## Validation Notes

- 2026-05-06: Plan creation used the accepted proposal, approved `specs/vision-skill.md`, `spec-review-r3`, existing vision migration plans, current `specs/vision-skill.test.md`, current canonical skills, selector/test inventories, and current change-local review records.
- 2026-05-06: Test-spec update activated the strategic-positioning proof map, including the plan-review note that explicit root `vision.md` selector proof is expected to be negative rather than a passing migration route.
- 2026-05-06: Test-spec validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`, explicit artifact-lifecycle validation over the touched proposal/spec/test-spec/plan/review/change-local paths, `git diff --check`, trailing-whitespace scan, and selected `bash scripts/ci.sh --mode explicit` over the same touched paths. Artifact lifecycle emitted the known reviewer-attention warning for older `docs/plan.md` lifecycle wording in a Done entry.
- 2026-05-06: M1/M2 implementation proof passed with `python scripts/test-skill-validator.py`, `python scripts/test-select-validation.py`, `python scripts/validate-skills.py`, targeted `python scripts/validate-skills.py` for `skills/vision/SKILL.md`, `skills/proposal/SKILL.md`, and `skills/proposal-review/SKILL.md`, `python scripts/validate-readme.py README.md --vision-markers`, explicit selector probes for `VISION.md`, `vision.md`, `docs/vision/strategic-positioning.md`, and selector/test paths, and selected CI over the M1 proof-map and selector surfaces.
- 2026-05-06: The explicit root `vision.md` selector proof exited nonzero with `status: blocked`, `unclassified_paths: ["vision.md"]`, no `readme.vision_markers`, and no `vision-path-conflict`; this is the expected retired lowercase behavior.
- 2026-05-06: M2 selected CI over canonical skill and rationale paths initially failed on `skills.drift` and `adapters.drift`, then passed after M3 refreshed generated output from canonical sources.
- 2026-05-06: M3 generated-output proof passed with `python scripts/build-skills.py`, `python scripts/build-adapters.py --version 0.1.1`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/test-adapter-distribution.py`, `python scripts/validate-adapters.py --version 0.1.1`, generated-path selector inspection, and generated-path selected CI.
- 2026-05-06: M4 lifecycle proof passed with `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality`, `python scripts/validate-change-metadata.py docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`, explicit artifact lifecycle validation over plan/proposal/spec/test-spec/rationale/change-local review paths, `git diff --check -- .`, targeted trailing-whitespace scan, and final selected CI over the full changed-file set. Artifact lifecycle continued to emit the known reviewer-attention warning for older lifecycle wording in a Done entry in `docs/plan.md`.
- 2026-05-06: First-pass code-review recorded `CR1-F1` and returned `changes-requested`. Review artifact structure validation, change metadata validation, artifact lifecycle validation, whitespace checks, and selected CI over the code-review record and lifecycle paths passed with review-resolution open.
- 2026-05-07: `CR1-F1` resolution proof first added a static assertion that failed against the stale skill wording, then updated `skills/vision/SKILL.md` so explicit project-vision establishment creates root `VISION.md` without a retired lowercase-file precondition. `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py skills/vision/SKILL.md`, generator refreshes, generator drift checks, adapter validation, a no-match scan for "neither root vision file exists" across canonical/generated vision skill files, and selected CI over canonical/generated vision skill paths passed after the fix.
- 2026-05-07: Same-stage code-review rerun recorded `code-review-r2` with `clean-with-notes` and no material findings.

## Outcome and Retrospective

- Active. Implementation milestones M1 through M4 are complete. First-pass code-review requested changes for `CR1-F1`, and the finding is resolved with review-resolution closed. Same-stage code-review rerun returned `clean-with-notes`. The plan remains Active for verify, explain-change refresh, PR handoff, and PR-self-contained Done closeout.

## Readiness

- Plan-review approved.
- Test spec active.
- M1 through M4 implementation complete.
- First-pass code-review finding `CR1-F1` resolved and review-resolution closed.
- Code-review rerun clean.
- Next: verify.
