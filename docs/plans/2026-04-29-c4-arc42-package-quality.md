# C4 arc42 Package Quality Refinement Execution Plan

- Status: active
- Owner: maintainers
- Start date: 2026-04-29
- Last updated: 2026-04-29
- Related issue or PR: none yet
- Supersedes: none
- broad_smoke_required: true
- broad_smoke_reason: Planned initiative touches architecture templates, canonical architecture skills, generated Codex skill mirrors, generated public adapter packages, lifecycle-managed artifacts, and the canonical architecture package.

## Purpose / big picture

Implement the approved package-quality refinement for RigorLoop's C4, arc42, and ADR architecture method without changing the accepted method itself. The implementation keeps one canonical architecture package, improves template scaffolding, tightens architecture and architecture-review skills, refreshes generated skill and adapter output through existing generators, and keeps the first refinement review-based rather than adding new package-shape enforcement automation.

The architecture-stage work already refined and passed review for the canonical package and diagrams. This plan treats that approved architecture update as the baseline and sequences the remaining template, skill, generated-output, and closeout work into reviewable slices.

## Source artifacts

- Proposal: `docs/proposals/2026-04-29-c4-arc42-package-quality.md`
- Focused spec: `specs/architecture-package-method.md`
- Canonical architecture package: `docs/architecture/system/architecture.md`
- Change-local architecture delta: `docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md`
- ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Change metadata: `docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
- Matching test spec: `specs/architecture-package-method.test.md`, active proof map for R76-R118 and AC14-AC20 after the 2026-04-29 package-quality update.

## Context and orientation

- `docs/architecture/system/architecture.md` is the long-lived canonical architecture source; `docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md` is change-local evidence.
- Default package diagrams live under `docs/architecture/system/diagrams/` as `.mmd` source files and are referenced by relative links from `architecture.md`.
- `templates/architecture.md` teaches the full 12-section arc42 structure; `templates/diagram-styles.mmd` will become the shared C4 Mermaid styling source.
- `skills/architecture/SKILL.md` and `skills/architecture-review/SKILL.md` are canonical skill sources. Generated `.codex/skills/` and `dist/adapters/` output must be refreshed through existing generators only.
- Existing validation scripts select lifecycle, change metadata, skill, adapter, and broad-smoke checks. They must not become package-shape, required C4-file, required arc42-section, or ADR-presence enforcement in this slice.
- `docs/project-map.md` does not exist; orientation comes from the source artifacts and current repository layout.

## Non-goals

- Reopening the C4 plus official arc42 plus ADR method decision.
- Adding a component diagram before the refined container view and Building Block View prove deeper detail is needed.
- Adding required architecture package validators for arc42 section presence, C4 diagram files, ADR presence, package shape, or C4 visual sufficiency.
- Adding new external diagramming or validation dependencies.
- Hand-editing `.codex/skills/` or `dist/adapters/`.
- Adding a full worked architecture example inside `skills/architecture/SKILL.md`.
- Requiring architecture-review findings to classify every issue by C4 level.

## Requirements covered

- R76-R86: diagram source location, one authored source file, relative links, generated image boundary, and change-local diagram lifecycle.
- R87-R95: C4 semantics for Mermaid diagrams, shared styling, role classes, technology labels, intent-labeled relationships, and component-diagram discipline.
- R96-R104: hierarchical Building Block View, link-focused Architecture Decisions, quality-scenario guidance, and Deployment View boundary guidance.
- R105-R107: template additions for diagram styles, separate diagram source, relative links, hierarchy, deployment, and ADR summaries.
- R108-R111: concise architecture skill content, required output shape, minimal C4 snippets, ADR triggers, and external location for full worked examples.
- R112-R118: architecture-review finding format, severity vocabulary, location requirement, no mandatory C4-level classification, and material-finding contract preservation.
- AC14-AC20: accepted criteria for diagram source policy, C4 semantics, templates, component discipline, concise skill content, architecture-review findings, and generated output refresh.

## Milestones

### M1. Template and diagram-style scaffolding

- Goal: Add the shared Mermaid C4 role style source and update the architecture template so authors start from separate diagram source files, relative links, hierarchical building blocks, concise deployment guidance, link-focused ADR summaries, and a commented quality-scenario scaffold.
- Requirements: R76-R83, R87-R91, R96-R107, AC14-AC17.
- Files/components likely touched: `templates/architecture.md`, `templates/diagram-styles.mmd`, `docs/plans/2026-04-29-c4-arc42-package-quality.md`, `docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`.
- Dependencies: approved spec and architecture-review-approved canonical package.
- Tests to add/update: no new structural validator; use targeted template inspection plus existing selector, lifecycle, and CI wrapper checks.
- Implementation steps:
  - Add `templates/diagram-styles.mmd` with shared person, system, external, and container class definitions.
  - Update `templates/architecture.md` to reference package diagrams with relative links, keep diagram source separate, and specify `.mmd` for default Mermaid diagrams.
  - Add a commented section 10 quality-scenario scaffold and concise prompts for Building Block View, Deployment View, and Architecture Decisions.
  - Update plan progress and change metadata.
- Validation commands:
  - `rg -n "diagram-styles|diagrams/context\\.mmd|diagrams/container\\.mmd|Quality scenarios|Building Block View|Architecture Decisions|Deployment View" templates/architecture.md templates/diagram-styles.mmd`
  - `python scripts/select-validation.py --mode explicit --path templates/architecture.md --path templates/diagram-styles.mmd --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path templates/architecture.md --path templates/diagram-styles.mmd --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
  - `git diff --check -- templates docs/plans/2026-04-29-c4-arc42-package-quality.md docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
- Expected observable result: authors have canonical template and style scaffolding for reviewable C4 Mermaid source without new enforcement automation.
- Commit message: `M1: add architecture diagram template scaffolding`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: template language can become a hidden validator by sounding more rigid than the spec.
- Rollback/recovery: revert only template changes and keep spec/architecture guidance as the source of truth until wording is corrected.

### M2. Architecture authoring skill update

- Goal: Keep `skills/architecture/SKILL.md` concise while teaching the required output shape, minimal C4 context/container snippets, ADR triggers, use/skip guidance, diagram-source policy, and full-file-read guidance.
- Requirements: R76-R95, R98-R111, AC14-AC18.
- Files/components likely touched: `skills/architecture/SKILL.md`, possibly `scripts/test-skill-validator.py`, plan and change metadata.
- Dependencies: M1 template wording should be stable enough for the skill to point authors to templates rather than duplicate structure.
- Tests to add/update: update skill validation regression only if existing checks do not cover required skill shape or scan-efficiency wording.
- Implementation steps:
  - Add a short output shape pointing to change-local deltas or the canonical package, context/container diagrams, and ADRs.
  - Add one minimal C4 context snippet and one minimal C4 container snippet without a full worked example.
  - Add an ADR trigger list and when-to-use/when-not-to-use guidance.
  - Preserve summary/ID-based evidence guidance and explicit full-file-read guidance.
  - Update plan progress and change metadata.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/select-validation.py --mode explicit --path skills/architecture/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/architecture/SKILL.md --path dist/adapters/claude/.claude/skills/architecture/SKILL.md --path dist/adapters/codex/.agents/skills/architecture/SKILL.md --path dist/adapters/opencode/.opencode/skills/architecture/SKILL.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path skills/architecture/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/architecture/SKILL.md --path dist/adapters/claude/.claude/skills/architecture/SKILL.md --path dist/adapters/codex/.agents/skills/architecture/SKILL.md --path dist/adapters/opencode/.opencode/skills/architecture/SKILL.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md`
  - `git diff --check -- skills/architecture/SKILL.md scripts/test-skill-validator.py .codex/skills/architecture/SKILL.md dist/adapters/claude/.claude/skills/architecture/SKILL.md dist/adapters/codex/.agents/skills/architecture/SKILL.md dist/adapters/opencode/.opencode/skills/architecture/SKILL.md docs/plans/2026-04-29-c4-arc42-package-quality.md docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml docs/plan.md`
- Expected observable result: architecture authors get compact process guidance and are directed to templates for structure instead of a long skill body.
- Commit message: `M2: tighten architecture authoring skill`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: the skill may become too verbose or duplicate the full template.
- Rollback/recovery: trim examples back to the required snippets and leave detailed structure in `templates/architecture.md`.

### M3. Architecture-review skill update

- Goal: Update `skills/architecture-review/SKILL.md` to review C4 sufficiency, all 12 arc42 sections, diagram-source policy, component-diagram discipline, quality scenarios, ADR link focus, deployment boundary quality, merge-back, and simple finding format while preserving the material-finding contract.
- Requirements: R87-R104, R112-R118, AC15-AC19.
- Files/components likely touched: `skills/architecture-review/SKILL.md`, `scripts/test-skill-validator.py`, generated `.codex/skills/architecture-review/SKILL.md`, generated public adapter architecture-review skill copies, plan and change metadata.
- Dependencies: M2 authoring language should be stable enough for review guidance to align with it.
- Tests to add/update: update skill validation regression only if existing checks do not cover required architecture-review shape or material-finding wording.
- Implementation steps:
  - Add checks for embedded or duplicated diagrams, generic non-C4 flowcharts, wrong C4 level, missing role classes, missing technology labels where relevant, and unlabeled relationships.
  - Add checks for flat Building Block Views, duplicated ADR rationale, weak quality-scenario content, and Deployment View source-layout repetition.
  - Define the simple finding shape: finding, location, severity, recommendation.
  - State that material findings must also include evidence, required outcome, and a safe resolution path or `needs-decision` rationale.
  - Update plan progress and change metadata.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
  - `python scripts/select-validation.py --mode explicit --path skills/architecture-review/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/claude/.claude/skills/architecture-review/SKILL.md --path dist/adapters/codex/.agents/skills/architecture-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path skills/architecture-review/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/claude/.claude/skills/architecture-review/SKILL.md --path dist/adapters/codex/.agents/skills/architecture-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md`
  - `git diff --check -- skills/architecture-review/SKILL.md scripts/test-skill-validator.py .codex/skills/architecture-review/SKILL.md dist/adapters/claude/.claude/skills/architecture-review/SKILL.md dist/adapters/codex/.agents/skills/architecture-review/SKILL.md dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md docs/plans/2026-04-29-c4-arc42-package-quality.md docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml docs/plan.md`
- Expected observable result: architecture-review records severity and location without mandatory C4-level classification, while material findings still meet the repository-wide finding contract.
- Commit message: `M3: tighten architecture review skill`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: review guidance could weaken material finding completeness by overemphasizing the simple finding format.
- Rollback/recovery: restore explicit material-finding contract wording and rerun review-artifact and skill validation.

### M4. Generated output refresh

- Goal: Refresh generated Codex runtime skills and public adapter packages from canonical skill sources through existing generators only.
- Requirements: R58, R108-R118, AC18-AC20.
- Files/components likely touched: `.codex/skills/architecture/SKILL.md`, `.codex/skills/architecture-review/SKILL.md`, `dist/adapters/`, plan and change metadata.
- Dependencies: M2 and M3 canonical skill edits must be complete.
- Tests to add/update: no direct edits to generated output tests unless generator behavior changes unexpectedly.
- Implementation steps:
  - Run `python scripts/build-skills.py` after canonical skill edits.
  - Run `python scripts/build-adapters.py --version 0.1.1` after generated Codex skills are refreshed.
  - Verify generated output drift and adapter package validity.
  - Update plan progress and change metadata.
- Validation commands:
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/manifest.yaml --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/manifest.yaml --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
  - `git diff --check -- skills/architecture/SKILL.md skills/architecture-review/SKILL.md .codex/skills dist/adapters docs/plans/2026-04-29-c4-arc42-package-quality.md docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
- Expected observable result: generated `.codex/skills/` and `dist/adapters/` outputs match canonical skills and adapter validations pass.
- Commit message: `M4: refresh generated architecture skill outputs`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: generated outputs may partially refresh or include unrelated generated churn.
- Rollback/recovery: revert generated outputs, rerun both generators from clean canonical skill sources, and re-run drift checks before continuing.

### M5. Lifecycle closeout and final validation

- Goal: Synchronize lifecycle-managed artifacts, change metadata, plan progress, validation evidence, and final readiness after all implementation milestones pass.
- Requirements: all R76-R118 and AC14-AC20 touched by the plan.
- Files/components likely touched: `docs/plan.md`, this plan file, `docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`, possibly `specs/architecture-package-method.test.md`, `docs/proposals/2026-04-29-c4-arc42-package-quality.md`, `specs/architecture-package-method.md`, and generated outputs from prior milestones.
- Dependencies: M1-M4 complete and an active matching test spec. M5 prepares implementation closeout and readiness for `code-review`; `code-review` and `verify` remain downstream gates before `explain-change` and PR readiness.
- Tests to add/update: final test-spec coverage and closeout evidence must match the changed surfaces; no new enforcement automation unless a later approved artifact adds it.
- Implementation steps:
  - Update plan progress, decision log, surprises, validation notes, outcome, and readiness.
  - Update `docs/plan.md` from Active to Done only during PR closeout, not during implementation.
  - Keep proposal, spec, architecture, and test spec readiness aligned with actual workflow handoff.
  - Run final lifecycle, change metadata, skill, adapter, selector, and broad-smoke validation.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-29-c4-arc42-package-quality.md --path specs/architecture-package-method.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-04-29-c4-arc42-package-quality.md --path specs/architecture-package-method.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md --path templates/architecture.md --path templates/diagram-styles.mmd --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/manifest.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-04-29-c4-arc42-package-quality.md --path specs/architecture-package-method.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md --path templates/architecture.md --path templates/diagram-styles.mmd --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/manifest.yaml`
  - `bash scripts/ci.sh --mode broad-smoke`
  - `git diff --check -- .`
- Expected observable result: lifecycle state, generated output, validation evidence, and plan index state are synchronized and ready for `code-review`; `explain-change` and PR readiness depend on later `verify`.
- Commit message: `M5: close c4 arc42 package quality refinement`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: closeout can claim readiness before generated output, test spec, or lifecycle artifacts are synchronized.
- Rollback/recovery: move readiness back to the last completed gate, keep the plan Active, and rerun missing validation before PR handoff.

## Validation plan

This plan uses pass-gate commands only for milestone completion unless a milestone explicitly records selector inspection behavior. Selector-selected broad smoke is expected because the plan declares `broad_smoke_required: true`; final closeout also runs `bash scripts/ci.sh --mode broad-smoke` directly.

Validation starts with the smallest milestone-specific checks, then expands to skill, adapter, lifecycle, change metadata, selector, and broad-smoke checks as the change touches generated outputs and lifecycle-managed artifacts. The first implementation remains review-based for architecture package shape and C4 sufficiency; validation commands prove routing, lifecycle, metadata, skill structure, generated-output drift, adapter packaging, and repository smoke health.

## Risks and recovery

- Risk: diagrams or templates drift into generic flowchart guidance again. Recovery: compare against R87-R93 and the reviewed canonical diagrams, then correct template/skill wording before generation.
- Risk: skill content becomes too long. Recovery: move full examples to references or templates and keep only the required output shape, snippets, triggers, and use/skip guidance in the skill.
- Risk: architecture-review finding format weakens repository-wide material finding evidence. Recovery: restore explicit material-finding contract language and rerun review-artifact and skill checks.
- Risk: generated output is edited directly. Recovery: revert generated surfaces, edit canonical skills, rerun generators, and rerun drift checks.
- Risk: new validators accidentally enforce package shape. Recovery: remove validator changes and rely on architecture-review evidence for this slice.

## Dependencies

- `plan-review` must approve this plan before test-spec updates.
- `test-spec` must update or confirm coverage for R76-R118 and AC14-AC20 before implementation.
- M1 should complete before M2 and M3 so skills can point to stable template and style scaffolding.
- M4 depends on M2 and M3 because generated output must reflect canonical skill changes.
- M5 depends on M1-M4 and an active matching test spec. It prepares implementation closeout and readiness for `code-review`; `code-review` and `verify` remain downstream gates before `explain-change` and PR readiness.
- No new external dependencies are allowed by the approved spec.

## Progress

- 2026-04-29: architecture-review approved the canonical package update and change-local architecture delta with no findings.
- 2026-04-29: normalized `docs/architecture/system/architecture.md` and `docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md` to `approved` for planning handoff.
- 2026-04-29: drafted this execution plan and registered it in `docs/plan.md`.
- 2026-04-29: plan-stage validation passed for selector routing, change metadata, lifecycle state, whitespace, and selected CI checks including broad smoke.
- 2026-04-29: revised M5 after plan-review finding PR-F1 to keep `code-review` and `verify` as downstream gates rather than implementation milestone prerequisites.
- 2026-04-29: plan-review approved the revised plan; test-spec updated `specs/architecture-package-method.test.md` for R76-R118 and AC14-AC20.
- 2026-04-29: implemented M1 template and diagram-style scaffolding in `templates/architecture.md` and `templates/diagram-styles.mmd`; M2-M5 remain pending.
- 2026-04-29: code-review M1 R1 found stale readiness handoff wording (CR1-F1); the finding was accepted and closed by updating readiness to point to M2 after M1 code-review.
- 2026-04-29: implemented M2 architecture authoring skill update in `skills/architecture/SKILL.md`, added skill-validator regression coverage, and refreshed generated Codex skill plus public adapter output through existing generators because selector-selected drift checks require generated output to stay in sync.
- 2026-04-29: code-review M2 R1 passed with no material findings; recorded the clean review under `docs/changes/2026-04-29-c4-arc42-package-quality/reviews/code-review-m2-r1.md`.
- 2026-04-29: implemented M3 architecture-review skill update in `skills/architecture-review/SKILL.md`, added regression coverage for the simple finding format and material-finding contract preservation, and refreshed generated Codex skill plus public adapter output through existing generators because selector-selected drift checks require generated output to stay in sync.
- 2026-04-29: code-review M3 R1 passed with no material findings; recorded the clean review under `docs/changes/2026-04-29-c4-arc42-package-quality/reviews/code-review-m3-r1.md`.
- 2026-04-29: implemented M4 generated-output sync by rerunning the existing skill and adapter generators after M2 and M3; no generated file diff was produced because earlier milestone validation had already refreshed the required generated output.

## Decision log

- 2026-04-29: treat the reviewed canonical architecture package refinement as the approved baseline; implementation milestones start with templates and skills rather than redoing architecture-stage content.
- 2026-04-29: keep generated output refresh in its own milestone so canonical skill edits can be reviewed before generated mirrors and adapter packages change.
- 2026-04-29: require broad smoke at final validation because the initiative crosses skills, generated output, templates, lifecycle artifacts, and architecture docs.
- 2026-04-29: keep M1 review-based by adding template scaffolding only; no package-shape, C4-file, ADR-presence, or arc42-section enforcement automation was added.
- 2026-04-29: M2 refreshed generated `.codex/skills/architecture/SKILL.md` and adapter architecture skill copies through generators even though generated refresh has a later dedicated milestone, because the selector-selected M2 checks include `skills.drift` and `adapters.drift`. M4 remains necessary as the final generated-output sync check after M3.
- 2026-04-29: M3 refreshed generated `.codex/skills/architecture-review/SKILL.md` and adapter architecture-review skill copies through generators even though generated refresh has a later dedicated milestone, because the selector-selected M3 checks include `skills.drift` and `adapters.drift`. M4 remains necessary as the final generated-output sync check after M3 review.
- 2026-04-29: M4 is an idempotent generated-output sync milestone for this run because M2 and M3 already refreshed generated skill and adapter output when selector-selected drift checks required it.

## Surprises and discoveries

- 2026-04-29: M1 selector routing includes `selector.regression` for changed `templates/` paths in addition to lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M2 canonical skill edits immediately made generated skill and adapter drift checks fail; required M2 validation could not pass without generator refresh.
- 2026-04-29: M3 canonical architecture-review skill edits immediately made generated skill and adapter drift checks fail; required M3 validation could not pass without generator refresh.
- 2026-04-29: M4 generator reruns produced no file diff; generated output was already synchronized by the earlier selector-required M2 and M3 refreshes.

## Validation notes

- 2026-04-29: `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-04-29-c4-arc42-package-quality.md --path specs/architecture-package-method.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` returned `status: ok` and selected artifact lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: `python scripts/validate-change-metadata.py docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml` passed.
- 2026-04-29: `python scripts/test-change-metadata-validator.py` passed.
- 2026-04-29: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-29-c4-arc42-package-quality.md --path specs/architecture-package-method.md --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` passed.
- 2026-04-29: `git diff --check -- docs/proposals/2026-04-29-c4-arc42-package-quality.md specs/architecture-package-method.md docs/architecture/system docs/changes/2026-04-29-c4-arc42-package-quality docs/plans/2026-04-29-c4-arc42-package-quality.md docs/plan.md` passed.
- 2026-04-29: `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-04-29-c4-arc42-package-quality.md --path specs/architecture-package-method.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` passed selected lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: test-spec update `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-04-29-c4-arc42-package-quality.md --path specs/architecture-package-method.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` returned `status: ok` and selected artifact lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: test-spec update `python scripts/validate-change-metadata.py docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml` passed.
- 2026-04-29: test-spec update `python scripts/test-change-metadata-validator.py` passed.
- 2026-04-29: test-spec update `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-29-c4-arc42-package-quality.md --path specs/architecture-package-method.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` passed.
- 2026-04-29: test-spec update `git diff --check -- docs/proposals/2026-04-29-c4-arc42-package-quality.md specs/architecture-package-method.md specs/architecture-package-method.test.md docs/architecture/system docs/changes/2026-04-29-c4-arc42-package-quality docs/plans/2026-04-29-c4-arc42-package-quality.md docs/plan.md` passed.
- 2026-04-29: test-spec update `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-04-29-c4-arc42-package-quality.md --path specs/architecture-package-method.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` passed selected lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M1 pre-edit inspection `rg -n "diagram-styles|diagrams/context\\.mmd|diagrams/container\\.mmd|Quality scenarios|Building Block View|Architecture Decisions|Deployment View" templates/architecture.md templates/diagram-styles.mmd` failed as expected because `templates/diagram-styles.mmd` did not exist.
- 2026-04-29: M1 `rg -n "diagram-styles|diagrams/context\\.mmd|diagrams/container\\.mmd|Quality scenarios|Building Block View|Architecture Decisions|Deployment View" templates/architecture.md templates/diagram-styles.mmd` passed after template scaffolding was added.
- 2026-04-29: M1 `python scripts/select-validation.py --mode explicit --path templates/architecture.md --path templates/diagram-styles.mmd --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml` returned `status: ok` and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- 2026-04-29: M1 `git diff --check -- templates docs/plans/2026-04-29-c4-arc42-package-quality.md docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml` passed.
- 2026-04-29: M1 `bash scripts/ci.sh --mode explicit --path templates/architecture.md --path templates/diagram-styles.mmd --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml` passed selected lifecycle, change metadata, selector regression, and broad-smoke checks.
- 2026-04-29: M1 code-review `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-04-29-c4-arc42-package-quality` passed.
- 2026-04-29: M1 code-review `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-29-c4-arc42-package-quality` passed.
- 2026-04-29: M1 code-review `python scripts/select-validation.py --mode explicit --path templates/architecture.md --path templates/diagram-styles.mmd --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/reviews/code-review-m1-r1.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-log.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-resolution.md --path docs/plan.md` returned `status: ok` and selected review artifact, lifecycle, change metadata, selector regression, and broad-smoke checks.
- 2026-04-29: M1 code-review `git diff --check -- docs/changes/2026-04-29-c4-arc42-package-quality docs/plans/2026-04-29-c4-arc42-package-quality.md docs/plan.md` passed.
- 2026-04-29: M1 code-review `bash scripts/ci.sh --mode explicit --path templates/architecture.md --path templates/diagram-styles.mmd --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/changes/2026-04-29-c4-arc42-package-quality/reviews/code-review-m1-r1.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-log.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-resolution.md --path docs/plan.md` passed selected review artifact, lifecycle, change metadata, selector regression, and broad-smoke checks.
- 2026-04-29: M2 pre-implementation `python scripts/test-skill-validator.py` failed as expected after adding the architecture-skill regression because `skills/architecture/SKILL.md` did not yet include the required output-shape, C4 container snippet, ADR trigger heading, use/skip heading, and reference-example boundary.
- 2026-04-29: M2 `python scripts/validate-skills.py` passed.
- 2026-04-29: M2 `python scripts/test-skill-validator.py` passed after updating `skills/architecture/SKILL.md`.
- 2026-04-29: M2 pre-generation `python scripts/build-skills.py --check` failed as expected because `.codex/skills/architecture/SKILL.md` was stale after the canonical skill edit.
- 2026-04-29: M2 pre-generation `python scripts/build-adapters.py --version 0.1.1 --check` failed as expected with three stale architecture adapter skill files after the canonical skill edit.
- 2026-04-29: M2 `python scripts/build-skills.py` refreshed generated Codex skill output.
- 2026-04-29: M2 `python scripts/build-adapters.py --version 0.1.1` refreshed public adapter output.
- 2026-04-29: M2 `python scripts/build-skills.py --check` passed.
- 2026-04-29: M2 `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- 2026-04-29: M2 `python scripts/validate-adapters.py --version 0.1.1` passed.
- 2026-04-29: M2 final `python scripts/select-validation.py --mode explicit --path skills/architecture/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/architecture/SKILL.md --path dist/adapters/claude/.claude/skills/architecture/SKILL.md --path dist/adapters/codex/.agents/skills/architecture/SKILL.md --path dist/adapters/opencode/.opencode/skills/architecture/SKILL.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md` returned `status: ok` and selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `broad_smoke.repo`.
- 2026-04-29: M2 final `git diff --check -- skills/architecture/SKILL.md scripts/test-skill-validator.py .codex/skills/architecture/SKILL.md dist/adapters/claude/.claude/skills/architecture/SKILL.md dist/adapters/codex/.agents/skills/architecture/SKILL.md dist/adapters/opencode/.opencode/skills/architecture/SKILL.md docs/plans/2026-04-29-c4-arc42-package-quality.md docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml docs/plan.md` passed.
- 2026-04-29: M2 final `bash scripts/ci.sh --mode explicit --path skills/architecture/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/architecture/SKILL.md --path dist/adapters/claude/.claude/skills/architecture/SKILL.md --path dist/adapters/codex/.agents/skills/architecture/SKILL.md --path dist/adapters/opencode/.opencode/skills/architecture/SKILL.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md` passed selected skill, generated skill drift, adapter regression/drift/validation, lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M2 code-review closeout `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-04-29-c4-arc42-package-quality` passed.
- 2026-04-29: M2 code-review closeout `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-29-c4-arc42-package-quality` passed.
- 2026-04-29: M2 code-review closeout `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-29-c4-arc42-package-quality/reviews/code-review-m2-r1.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-log.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-resolution.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` returned `status: ok` and selected review artifact, lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M2 code-review closeout `git diff --check -- docs/changes/2026-04-29-c4-arc42-package-quality docs/plans/2026-04-29-c4-arc42-package-quality.md docs/plan.md` passed.
- 2026-04-29: M2 code-review closeout `bash scripts/ci.sh --mode explicit --path docs/changes/2026-04-29-c4-arc42-package-quality/reviews/code-review-m2-r1.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-log.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-resolution.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` passed selected review artifact, lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M3 pre-implementation `python scripts/test-skill-validator.py` failed as expected after adding the architecture-review regression because `skills/architecture-review/SKILL.md` did not yet include the required package-quality finding triggers, simple finding format, severity vocabulary, and material-finding contract preservation wording.
- 2026-04-29: M3 `python scripts/validate-skills.py` passed.
- 2026-04-29: M3 `python scripts/test-skill-validator.py` passed after updating `skills/architecture-review/SKILL.md`.
- 2026-04-29: M3 selector inspection `python scripts/select-validation.py --mode explicit --path skills/architecture-review/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml` returned `status: ok` and selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, artifact lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M3 pre-generation `python scripts/build-skills.py --check` failed as expected because `.codex/skills/architecture-review/SKILL.md` was stale after the canonical skill edit.
- 2026-04-29: M3 pre-generation `python scripts/build-adapters.py --version 0.1.1 --check` failed as expected with three stale architecture-review adapter skill files after the canonical skill edit.
- 2026-04-29: M3 `python scripts/build-skills.py` refreshed generated Codex skill output.
- 2026-04-29: M3 `python scripts/build-adapters.py --version 0.1.1` refreshed public adapter output.
- 2026-04-29: M3 `python scripts/build-skills.py --check` passed.
- 2026-04-29: M3 `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- 2026-04-29: M3 `python scripts/validate-adapters.py --version 0.1.1` passed.
- 2026-04-29: M3 `python scripts/test-adapter-distribution.py` passed.
- 2026-04-29: M3 `python scripts/test-review-artifact-validator.py` passed.
- 2026-04-29: M3 `python scripts/test-change-metadata-validator.py` passed.
- 2026-04-29: M3 `python scripts/validate-change-metadata.py docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml` passed.
- 2026-04-29: M3 `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml` passed.
- 2026-04-29: M3 final `python scripts/select-validation.py --mode explicit --path skills/architecture-review/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/claude/.claude/skills/architecture-review/SKILL.md --path dist/adapters/codex/.agents/skills/architecture-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md` returned `status: ok` and selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, artifact lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M3 final `git diff --check -- skills/architecture-review/SKILL.md scripts/test-skill-validator.py .codex/skills/architecture-review/SKILL.md dist/adapters/claude/.claude/skills/architecture-review/SKILL.md dist/adapters/codex/.agents/skills/architecture-review/SKILL.md dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md docs/plans/2026-04-29-c4-arc42-package-quality.md docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml docs/plan.md` passed.
- 2026-04-29: M3 final `bash scripts/ci.sh --mode explicit --path skills/architecture-review/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/claude/.claude/skills/architecture-review/SKILL.md --path dist/adapters/codex/.agents/skills/architecture-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md` passed selected skill, generated skill drift, adapter regression/drift/validation, lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M3 code-review closeout `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-04-29-c4-arc42-package-quality` passed.
- 2026-04-29: M3 code-review closeout `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-29-c4-arc42-package-quality` passed.
- 2026-04-29: M3 code-review closeout `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-29-c4-arc42-package-quality/reviews/code-review-m3-r1.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-log.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-resolution.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` returned `status: ok` and selected review artifact, lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M3 code-review closeout `git diff --check -- docs/changes/2026-04-29-c4-arc42-package-quality docs/plans/2026-04-29-c4-arc42-package-quality.md docs/plan.md` passed.
- 2026-04-29: M3 code-review closeout `bash scripts/ci.sh --mode explicit --path docs/changes/2026-04-29-c4-arc42-package-quality/reviews/code-review-m3-r1.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-log.md --path docs/changes/2026-04-29-c4-arc42-package-quality/review-resolution.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/plan.md` passed selected review artifact, lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M4 `python scripts/build-skills.py` passed and produced no generated file diff.
- 2026-04-29: M4 `python scripts/build-adapters.py --version 0.1.1` passed and produced no generated file diff.
- 2026-04-29: M4 `python scripts/build-skills.py --check` passed.
- 2026-04-29: M4 `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- 2026-04-29: M4 `python scripts/validate-adapters.py --version 0.1.1` passed.
- 2026-04-29: M4 `python scripts/test-adapter-distribution.py` passed.
- 2026-04-29: M4 `python scripts/test-select-validation.py` passed.
- 2026-04-29: M4 final `python scripts/select-validation.py --mode explicit --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/manifest.yaml --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md` returned `status: ok` and selected skill, generated skill drift, adapter regression/drift/validation, lifecycle, change metadata, and broad-smoke checks.
- 2026-04-29: M4 final `git diff --check -- skills/architecture/SKILL.md skills/architecture-review/SKILL.md .codex/skills dist/adapters docs/plans/2026-04-29-c4-arc42-package-quality.md docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml docs/plan.md` passed.
- 2026-04-29: M4 final `bash scripts/ci.sh --mode explicit --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/manifest.yaml --path docs/plans/2026-04-29-c4-arc42-package-quality.md --path docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml --path docs/plan.md` passed selected skill, generated skill drift, adapter regression/drift/validation, lifecycle, change metadata, and broad-smoke checks.

## Outcome and retrospective

- To be filled after implementation, verification, explain-change, and PR closeout.

## Readiness

- Immediate next repository stage: `code-review` for M4.
- Test spec readiness: active; `specs/architecture-package-method.test.md` covers R76-R118 and AC14-AC20 for this refinement.
- Implementation readiness: M1, M2, and M3 implementation and code-review closeout are complete. M4 implementation is complete and ready for code-review. M5 remains pending.
