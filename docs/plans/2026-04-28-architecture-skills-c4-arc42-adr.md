# Architecture Skills C4 arc42 ADR Execution Plan

- Status: active
- Owner: maintainers
- Start date: 2026-04-28
- Last updated: 2026-04-28
- Related issue or PR: none yet
- Supersedes: none
- broad_smoke_required: true
- broad_smoke_reason: Planned initiative touches workflow and governance guidance, lifecycle validation, canonical skills, generated skill mirrors, public adapter packages, templates, and architecture artifacts.

## Purpose / big picture

Implement the approved C4, arc42, and ADR architecture package method in small, reviewable slices. The implementation must introduce one canonical architecture package, keep change-local deltas historical after merge-back, add architecture and ADR templates under `templates/`, align governance and workflow guidance, update architecture skills, refresh generated outputs through existing generators, and add only the narrow lifecycle-validator compatibility required by the approved spec.

This plan intentionally keeps enforcement review-based for the first implementation. It does not add package-shape, C4-file, or ADR-presence validation automation.

## Source artifacts

- Proposal: `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Spec: `specs/architecture-package-method.md`
- Architecture delta: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`
- Architecture diagrams: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/context.mmd` and `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/container.mmd`
- ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Architecture review: approved on 2026-04-28 after lifecycle/status consistency corrections.
- Test spec: `specs/architecture-package-method.test.md`
- Change metadata: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
- Project map: none exists. Orientation comes from existing docs, specs, skills, scripts, schemas, generated outputs, and architecture artifacts.

## Context and orientation

- `specs/architecture-package-method.md` is the normative contract for this change. `specs/rigorloop-workflow.md` should receive only a short stage-level pointer.
- Existing architecture guidance in `skills/architecture/SKILL.md` and `skills/architecture-review/SKILL.md` still describes the older repository-specific architecture shape. They must move to the C4 plus official 12-section arc42 plus ADR method.
- Existing architecture documents under `docs/architecture/` predate the new canonical package lifecycle. They remain legacy or historical until a follow-on migration artifact inventories and classifies them.
- The canonical architecture package must be created under `docs/architecture/system/` with `architecture.md`, `diagrams/context.mmd`, and `diagrams/container.mmd`.
- `templates/` does not currently exist as a canonical authored surface. Adding `templates/architecture.md` and `templates/adr.md` is a canonical-source boundary update that must be reflected in `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md`.
- Canonical skills live under `skills/`; generated Codex runtime skills under `.codex/skills/` and public adapter packages under `dist/adapters/` must be refreshed through existing generation commands, not hand-edited.
- `scripts/validate-artifact-lifecycle.py` currently uses the older architecture required-section contract for every Markdown file under `docs/architecture/`. The implementation must add only the narrow compatibility needed for `docs/architecture/system/architecture.md`.
- `scripts/validation_selection.py` already classifies `templates/`, governance files, workflow guidance, lifecycle artifacts, canonical skills, generated skills, and generated adapters. Change-local architecture Markdown and `.mmd` diagrams are intentionally manual-routed today.

## Non-goals

- Requiring architecture artifacts for trivial or leaf changes with no architecture impact.
- Rewriting every legacy architecture document during this first implementation.
- Treating change-local architecture deltas as permanent current architecture sources.
- Creating a new canonical architecture document for every feature.
- Making 4+1, full UML, or code-level diagrams the default.
- Adding required structural architecture validators for arc42 sections, required C4 diagram files, ADR presence, or package shape.
- Changing validation semantics, selected check coverage, command output, or command exit behavior beyond the narrow lifecycle-validator compatibility required by R71 and R72.
- Adding a new external diagramming, templating, or validation dependency.
- Hand-editing generated `.codex/skills/` or `dist/adapters/` output.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R20` | Canonical `architecture.md` using all 12 arc42 sections, lifecycle metadata, concise `Not applicable` handling, and section update rules |
| `R21`-`R29` | C4 context/container Mermaid source diagrams and diagram-as-code boundaries |
| `R30`-`R43` | Change-local delta usage, merge-back behavior, architecture-aware feature completion, and leaf-change exclusion |
| `R44`-`R48` | ADR trigger, structure, lifecycle vocabulary, and append-only decision history |
| `R49`-`R55` | `templates/` scaffolds and governance/workflow source-boundary updates |
| `R56`-`R58` | Canonical architecture skill updates and generated output refresh through existing generators |
| `R59`-`R66` | First positive example, prospective adoption, and legacy architecture normalization follow-up |
| `R67`-`R72` | Review-based first implementation and narrow lifecycle-validator compatibility only |
| `R73`-`R75` | Security/privacy and contributor-facing readability expectations |
| `AC1`-`AC13` | Acceptance proof through linked artifacts, template paths, diagrams, merge-back, ADR, legacy follow-up, deferred automation, lifecycle-validator compatibility, and validation commands |

## Milestones

### M1. Add canonical arc42 lifecycle compatibility

- Goal: Let the artifact lifecycle validator accept the new canonical `docs/architecture/system/architecture.md` arc42 package shape without weakening validation for legacy architecture files or adding package-shape enforcement.
- Requirements: `R7`-`R12`, `R67`-`R72`, `AC3`, `AC11`, `AC12`.
- Files/components likely touched:
  - `scripts/artifact_lifecycle_contracts.py`
  - `scripts/artifact_lifecycle_validation.py` if path-specific compatibility is cleaner there
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/artifact-lifecycle/`
  - this plan and `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
- Dependencies: approved spec and architecture-review approval. This milestone must finish before creating `docs/architecture/system/architecture.md`.
- Tests to add/update:
  - canonical system architecture fixture with 12 official arc42 sections passes;
  - legacy architecture fixture still requires the older architecture contract unless explicitly outside scope;
  - missing status, invalid lifecycle status, placeholders, stale readiness, and terminal closeout behavior remain unchanged;
  - compatibility does not require C4 diagram files, ADR presence, or package-shape validation.
- Implementation steps:
  - Add a narrow contract branch for `docs/architecture/system/architecture.md`.
  - Keep existing architecture contract behavior for other `docs/architecture/*.md` files.
  - Add focused fixtures that prove only the canonical arc42 path gets the new section contract.
  - Do not change selector categories, selected checks, command output, or command exit behavior.
- Validation commands:
  - Pass-gate commands:
    - `python scripts/test-artifact-lifecycle-validator.py`
    - `python scripts/test-select-validation.py`
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.md --path docs/adr/ADR-20260428-architecture-package-method.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
    - `bash scripts/ci.sh --mode explicit --path scripts/artifact_lifecycle_contracts.py --path scripts/artifact_lifecycle_validation.py --path scripts/test-artifact-lifecycle-validator.py`
    - `git diff --check -- scripts tests/fixtures/artifact-lifecycle docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/plan.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
- Expected observable result: the repository can add `docs/architecture/system/architecture.md` in M3 without the lifecycle validator rejecting the official arc42 section model.
- Commit message: `M1: add canonical architecture lifecycle compatibility`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: path-specific compatibility could accidentally exempt legacy architecture docs or become hidden enforcement automation.
- Rollback/recovery: revert the compatibility branch and fixtures; do not create the canonical package until the validator contract is safe.

### M2. Add templates, governance boundary, and workflow pointer

- Goal: Add the architecture and ADR scaffolds under `templates/`, update governance/source-boundary guidance, and add only a short workflow/spec routing pointer to the focused method spec.
- Requirements: `R2`, `R3`, `R49`-`R55`, `R70`, `R75`, `AC2`, `AC8`.
- Files/components likely touched:
  - `templates/architecture.md`
  - `templates/adr.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - this plan and change metadata
- Dependencies: M1 may run independently, but governance and workflow wording must follow the approved spec and avoid duplicating the focused package contract.
- Tests to add/update:
  - no new validator behavior unless existing tests require fixture updates for `templates/` classification or lifecycle references.
  - review proof that templates include the required arc42 and ADR scaffolding without pretending to be live artifacts.
- Implementation steps:
  - Add `templates/architecture.md` with lifecycle metadata plus the 12 official arc42 headings.
  - Add `templates/adr.md` with title, status, context, decision, alternatives considered, consequences, and follow-up.
  - Update `CONSTITUTION.md` and `AGENTS.md` to include `templates/` as canonical authored workflow content.
  - Update `docs/workflows.md` with concise contributor guidance and a pointer to `specs/architecture-package-method.md`.
  - Update `specs/rigorloop-workflow.md` with only the stage-level routing/output rule and pointer to the focused spec.
- Validation commands:
  - Pass-gate commands:
    - `python scripts/select-validation.py --mode explicit --path templates/architecture.md --path templates/adr.md --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`
    - `bash scripts/ci.sh --mode explicit --path templates/architecture.md --path templates/adr.md --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/architecture-package-method.md --path specs/rigorloop-workflow.md`
    - `git diff --check -- templates CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
- Expected observable result: contributors see `templates/` as authored workflow content, workflow routing points to the focused method spec, and templates are clearly scaffolds rather than live architecture or ADR records.
- Commit message: `M2: add architecture templates and workflow guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: workflow spec could become a second normative home, or templates could drift from the approved spec.
- Rollback/recovery: revert templates and guidance updates together so `templates/` is not left half-declared as a canonical source boundary.

### M3. Create canonical architecture package and merge back durable content

- Goal: Create the canonical architecture package and diagrams, using the architecture-method change itself as the first positive example and merging durable content out of the change-local delta.
- Requirements: `R1`, `R4`-`R43`, `R59`-`R64`, `R66`, `R73`-`R75`, `AC1`-`AC7`, `AC9`-`AC11`.
- Files/components likely touched:
  - `docs/architecture/system/architecture.md`
  - `docs/architecture/system/diagrams/context.mmd`
  - `docs/architecture/system/diagrams/container.mmd`
  - `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`
  - `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/`
  - this plan and change metadata
- Dependencies: M1 must be complete. M2 templates should exist before authoring the canonical package.
- Tests to add/update:
  - lifecycle validation for the canonical package path;
  - manual architecture-package review against all 12 arc42 headings, required context/container diagrams, ADR link, merge-back statement, and `Not applicable` rationale where used.
- Implementation steps:
  - Create `docs/architecture/system/architecture.md` from the new template.
  - Add `docs/architecture/system/diagrams/context.mmd` and `docs/architecture/system/diagrams/container.mmd` as Mermaid source-text C4 views.
  - Merge durable architecture-method content from the change-local delta into the canonical package.
  - Make section 9 of the canonical package summarize and link `docs/adr/ADR-20260428-architecture-package-method.md`.
  - Keep the change-local delta as historical evidence and ensure it does not claim to be canonical downstream guidance.
  - Preserve legacy `docs/architecture/` documents until the follow-on normalization artifact classifies them.
- Validation commands:
  - Pass-gate commands:
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260428-architecture-package-method.md --path specs/architecture-package-method.md`
    - `bash scripts/ci.sh --mode explicit --path docs/architecture/system/architecture.md`
    - `git diff --check -- docs/architecture/system docs/changes/2026-04-28-architecture-skills-c4-arc42-adr docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
  - Selector inspection / manual-routing proof:
    - `python scripts/select-validation.py --mode explicit --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd`
    - Expected selector result: blocked with `docs/architecture/system/architecture.md` lifecycle-routed and `.mmd` diagram paths requiring manual routing. The manual route is architecture/code-review diff inspection because first-slice C4-file enforcement is intentionally not automated.
- Expected observable result: `docs/architecture/system/` becomes the canonical current architecture package, and the change-local delta remains historical evidence only.
- Commit message: `M3: add canonical architecture package`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state reviewed; `docs/plan.md` remains active because the initiative is not complete
  - [x] progress updated
  - [x] decision log updated
  - [x] validation notes updated
  - [x] milestone committed
- Risks: canonical package could duplicate too much change-local detail or leave the merge-back boundary ambiguous.
- Rollback/recovery: remove the canonical package files and restore the change-local delta as the only reviewed architecture evidence until a corrected package is ready.

### M4. Update architecture skills and refresh generated outputs

- Goal: Align canonical architecture authoring and review skills with the new method, then regenerate `.codex/skills/` and public adapter packages through existing commands.
- Requirements: `R56`-`R58`, `R73`-`R75`, `AC4`, `AC5`, `AC7`, `AC11`.
- Files/components likely touched:
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `.codex/skills/architecture/SKILL.md`
  - `.codex/skills/architecture-review/SKILL.md`
  - generated files under `dist/adapters/`
  - this plan and change metadata
- Dependencies: M2 and M3 should establish the final method paths and artifact shape. Generated output must be produced from canonical sources only.
- Tests to add/update:
  - skill validation for updated canonical skills;
  - generated skill drift proof;
  - adapter drift and adapter validation proof after public adapter output is refreshed.
- Implementation steps:
  - Update `skills/architecture/SKILL.md` to default to the canonical package, change-local deltas, official arc42 sections, C4 context/container diagrams, ADR triggers, merge-back, and full-file-read guidance.
  - Update `skills/architecture-review/SKILL.md` to review C4 sufficiency, all 12 arc42 sections, Runtime View and Deployment View conditions, merge-back, legacy status, and ADR completeness.
  - Run `python scripts/build-skills.py` to refresh `.codex/skills/`.
  - Run `python scripts/build-adapters.py --version 0.1.1` to refresh public adapter packages.
- Validation commands:
  - Pass-gate commands:
    - `python scripts/validate-skills.py`
    - `python scripts/test-skill-validator.py`
    - `python scripts/build-skills.py --check`
    - `python scripts/test-adapter-distribution.py`
    - `python scripts/build-adapters.py --version 0.1.1 --check`
    - `python scripts/validate-adapters.py --version 0.1.1`
    - `python scripts/test-select-validation.py`
    - `bash scripts/ci.sh --mode explicit --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/manifest.yaml`
    - `git diff --check -- skills/architecture/SKILL.md skills/architecture-review/SKILL.md .codex/skills dist/adapters docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
- Expected observable result: architecture skills teach and review the approved C4, arc42, canonical-package, change-local-delta, and ADR method, and generated outputs match canonical skills.
- Commit message: `M4: align architecture skills with package method`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state reviewed; `docs/plan.md` remains active because the initiative is not complete
  - [x] progress updated
  - [x] decision log updated
  - [x] validation notes updated
  - [x] milestone committed
- Risks: generated adapters could drift if only `.codex/skills/` is refreshed, or skill wording could imply heavy docs for leaf changes.
- Rollback/recovery: revert canonical skill edits and rerun both generators so derived outputs return to the previous state.

### M5. Add legacy normalization follow-up and final closeout evidence

- Goal: Record the required follow-on legacy normalization artifact, update lifecycle evidence, and run final validation before code review and verification.
- Requirements: `R37`-`R39`, `R61`, `R65`, `R66`, `AC10`, `AC13`.
- Files/components likely touched:
  - `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
  - `docs/plan.md`
  - this plan
  - `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
  - `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/explain-change.md` if implementation reaches explain-change in this branch
- Dependencies: M1-M4 complete and test spec active before implementation starts.
- Tests to add/update:
  - change metadata validation includes plan and final changed-file list;
  - lifecycle validation includes proposal, spec, ADR, canonical architecture, active plan, and `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`;
  - manual inventory proof compares `find docs/architecture -type f | sort` output with the follow-on artifact inventory;
  - review proof confirms every inventoried architecture document has a classification, rationale, canonical replacement or merge-back target where applicable, and remaining follow-up work;
  - broad smoke runs before final PR readiness because the initiative crosses validation, governance, docs, skills, generated outputs, and adapters.
- Implementation steps:
  - Create and populate `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` as the follow-on legacy architecture lifecycle normalization artifact required by the approved spec.
  - Inventory every current document under `docs/architecture/`.
  - Classify each inventoried document as `current canonical content`, `superseded`, `archived/historical snapshot`, or another explicitly documented historical status.
  - Record rationale for each classification.
  - Record canonical replacement or merge-back target for each classification where applicable.
  - Identify follow-up work needed to complete lifecycle normalization.
  - Update `docs/plan.md` and this plan together when lifecycle state changes.
  - Keep the change metadata artifacts, requirements, tests, validation notes, changed files, and review status current.
  - Record any manual-routing selector proof for `.mmd` diagrams and change-local architecture files.
  - Prepare for `code-review`, `verify`, `explain-change`, and `pr` only after all plan milestones and the active test spec are satisfied.
- Validation commands:
  - Pass-gate commands:
    - `python scripts/validate-change-metadata.py docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
    - `python scripts/test-change-metadata-validator.py`
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.md --path docs/adr/ADR-20260428-architecture-package-method.md --path docs/architecture/system/architecture.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
    - `bash scripts/ci.sh --mode broad-smoke`
    - `git diff --check -- .`
  - Manual inventory proof:
    - `find docs/architecture -type f | sort`
    - Expected result: every path in the command output appears in `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` with classification, rationale, target where applicable, and remaining follow-up work.
- Expected observable result: all required method surfaces exist, generated output is synchronized, legacy migration follow-up is populated with an inventory and classification for every current `docs/architecture/` document, and final validation evidence is ready for code-review and verify.
- Commit message: `M5: close architecture method rollout evidence`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks: closeout could claim legacy architecture normalization is complete when only the follow-on artifact exists.
- Rollback/recovery: revert closeout artifact and plan-index updates; keep legacy architecture documents explicitly unnormalized until the follow-on migration runs.

## Validation plan

This plan uses two validation command types:

- Pass-gate commands are expected to succeed as written and are required for milestone completion.
- Selector inspection / manual-routing proofs are used to prove selector behavior for unsupported or intentionally unclassified paths. A blocked selector result is expected and does not fail the milestone when this plan records the manual route that will be used instead.

Validation starts with the smallest milestone-specific commands, then expands only when the milestone crosses domains. Final validation includes broad smoke because the completed initiative changes lifecycle validation, workflow/governance guidance, canonical skills, generated skill output, generated adapter output, templates, and architecture artifacts.

The first implementation must not use newly added package-shape automation as proof. Review, lifecycle validation, skill validation, generated-output drift checks, adapter validation, change metadata validation, and broad smoke are the proof surfaces for this slice.

## Risks and recovery

- Risk: lifecycle compatibility becomes broader than R71/R72 allow.
  Recovery: revert the validator compatibility branch, keep fixtures failing until the path-specific contract is corrected, and do not add the canonical package.
- Risk: templates, skills, and canonical package wording diverge.
  Recovery: treat the approved spec as source of truth, update all three surfaces in the same milestone, and rerun skill/generated-output checks.
- Risk: change-local delta remains a competing source of truth.
  Recovery: update the canonical package with durable content, mark the delta historical, and record that downstream work relies on `docs/architecture/system/`.
- Risk: legacy architecture documents are implied to be normalized too early.
  Recovery: keep guidance explicit that legacy docs remain unnormalized until the follow-on migration artifact is executed.
- Risk: generated outputs are hand-edited or only partially refreshed.
  Recovery: rerun `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1`, then rerun drift checks.

## Dependencies

- `plan-review` must approve this plan before `test-spec`.
- `test-spec` must be active before implementation.
- M1 must complete before M3 because the canonical package would otherwise fail the current lifecycle validator.
- M2 should complete before M3 so the canonical package can follow the final template and source-boundary guidance.
- M4 depends on M2 and M3 for stable paths and method wording.
- M5 depends on M1-M4 and records closeout only after generated outputs and lifecycle artifacts are synchronized.
- No new external dependencies are allowed by the approved spec.

## Progress

- 2026-04-28: plan drafted after accepted proposal, approved spec, approved architecture delta, and accepted ADR.
- 2026-04-28: plan-stage validation passed for change metadata, lifecycle scope, selector inspection, and whitespace checks.
- 2026-04-28: M5 revised after plan-review to require populated legacy architecture inventory, classifications, rationale, targets, and follow-up work.
- 2026-04-28: test spec created and activated after plan-review approval.
- 2026-04-28: M1 tests were added first. The initial `python scripts/test-artifact-lifecycle-validator.py` run failed as expected because `docs/architecture/system/architecture.md` still required legacy architecture sections.
- 2026-04-28: M1 implemented exact-path lifecycle compatibility for `docs/architecture/system/architecture.md`, kept legacy architecture Markdown on the older contract, and proved the canonical branch does not enforce package shape, C4 diagram files, or ADR presence.
- 2026-04-28: M2 added `templates/architecture.md` and `templates/adr.md`, declared `templates/` as canonical authored workflow content in governance/workflow guidance, and added only a stage-level architecture package pointer to `specs/rigorloop-workflow.md`.
- 2026-04-28: M3 created `docs/architecture/system/architecture.md` plus context and container Mermaid diagrams, merged durable architecture-method content from the change-local delta, and marked the delta as historical evidence after merge-back.
- 2026-04-28: M4 updated the architecture and architecture-review skills for the C4, arc42, canonical-package, change-local-delta, merge-back, ADR, legacy-status, and full-file-read rules, then refreshed `.codex/skills/` and public adapter skill output through the existing generators.

## Decision log

- 2026-04-28: split lifecycle-validator compatibility into M1 before canonical package creation because the approved architecture requires adding validator compatibility before `docs/architecture/system/architecture.md`.
- 2026-04-28: kept architecture-package enforcement automation out of scope for every milestone; review and existing validators are the first-slice proof path.
- 2026-04-28: planned broad smoke for final validation because the initiative crosses governance, workflow docs, scripts, skills, generated outputs, adapter packages, and architecture artifacts.
- 2026-04-28: made M5 create a populated legacy normalization plan rather than a placeholder because R65 requires inventory and classification before the repository can claim legacy architecture normalization is complete.
- 2026-04-28: implemented M1 as lifecycle-only compatibility by adding a canonical architecture contract with no required sections. This satisfies R71 while preserving R72's no required arc42 section, C4 diagram, ADR-presence, or package-shape enforcement boundary.
- 2026-04-28: implemented M2 without adding validator behavior or dependencies. Template content is reviewed manually under T2/T7/T8, while selector, lifecycle, and CI wrapper checks prove routing and touched lifecycle artifacts.
- 2026-04-28: implemented M3 as a documentation and diagram merge-back slice only. The canonical package is now the current architecture baseline, while `.mmd` diagram completeness remains manual-routed review evidence under the approved first-slice boundary.
- 2026-04-28: implemented M4 by editing only canonical skill sources first, then refreshing generated `.codex/skills/` and `dist/adapters/` output through `scripts/build-skills.py` and `scripts/build-adapters.py --version 0.1.1`.

## Surprises and discoveries

- `docs/project-map.md` does not exist; orientation is based on the existing repository layout and source artifacts.
- `scripts/validation_selection.py` already classifies `templates/`, governance, workflow, canonical skills, generated skills, generated adapters, and lifecycle artifacts.
- Change-local architecture files and `.mmd` diagrams are not deterministic selector pass-gate paths today; they remain manual-routed review evidence.
- M1 fixture files under `tests/fixtures/artifact-lifecycle/` are unclassified by the v1 selector when passed directly. The selected proof for M1 is `artifact_lifecycle.regression` from the touched lifecycle validator scripts, plus direct regression-test execution and diff checks.
- `scripts/artifact_lifecycle_validation.py` was unaffected in M1 because exact-path compatibility could be expressed in the contract registry without changing validation flow, command output, selected coverage, or exit behavior.
- M2 did not require changes under `scripts/` or generated output because `templates/` is already classified by the selector and the first implementation remains review-based for template content.
- M3 selector inspection blocked the canonical `.mmd` diagram paths as expected. The manual route is architecture/code-review diff inspection because the first implementation intentionally does not add required C4-file enforcement.
- M4 did not require new validation automation. Existing skill validation already enforces summary and stable-ID first reasoning plus full-file-read guidance for scan-sensitive skills.
- M4 adapter generation refreshed adapter-embedded architecture skills only; `dist/adapters/manifest.yaml` remained content-identical after regeneration.

## Validation notes

- 2026-04-28: `python scripts/validate-change-metadata.py docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: `python scripts/test-change-metadata-validator.py` passed.
- 2026-04-28: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.md --path docs/adr/ADR-20260428-architecture-package-method.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml --path docs/plan.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md` passed.
- 2026-04-28: `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` returned `status: ok` and selected lifecycle, change-metadata, and broad-smoke checks. Broad smoke is recorded as a final implementation gate, not a plan-drafting pass gate.
- 2026-04-28: `git diff --check -- docs/plan.md docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: after the M5 inventory/classification revision, `python scripts/validate-change-metadata.py docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: after the M5 inventory/classification revision, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.md --path docs/adr/ADR-20260428-architecture-package-method.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: after the M5 inventory/classification revision, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml --path docs/plan.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md` passed.
- 2026-04-28: after the M5 inventory/classification revision, `git diff --check -- docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/architecture-package-method.test.md --path specs/architecture-package-method.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml --path docs/adr/ADR-20260428-architecture-package-method.md` passed after test-spec creation.
- 2026-04-28: `python scripts/validate-change-metadata.py docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed after test-spec metadata updates.
- 2026-04-28: `python scripts/select-validation.py --mode explicit --path specs/architecture-package-method.test.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/plan.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` returned `status: ok` and selected lifecycle, change-metadata, and final broad-smoke checks. Broad smoke remains the final implementation gate.
- 2026-04-28: `git diff --check -- specs/architecture-package-method.test.md docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/plan.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml --path docs/plan.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.test.md` passed.
- 2026-04-28: `python scripts/test-change-metadata-validator.py` passed after test-spec metadata updates.
- 2026-04-28: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/architecture-package-method.test.md --path specs/architecture-package-method.md --path docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/adr/ADR-20260428-architecture-package-method.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md` passed.
- 2026-04-28: initial M1 `python scripts/test-artifact-lifecycle-validator.py` run failed as expected in `test_valid_canonical_arc42_architecture_passes` with missing legacy architecture sections.
- 2026-04-28: final M1 `python scripts/test-artifact-lifecycle-validator.py` passed with 37 tests.
- 2026-04-28: M1 `python scripts/select-validation.py --mode explicit --path scripts/artifact_lifecycle_contracts.py --path scripts/artifact_lifecycle_validation.py --path scripts/test-artifact-lifecycle-validator.py` returned `status: ok` and selected `artifact_lifecycle.regression`.
- 2026-04-28: M1 selector inspection including new fixture paths returned `status: blocked` for unclassified fixture files, which is expected because fixture paths are proven through `artifact_lifecycle.regression` rather than direct selector routing.
- 2026-04-28: M1 `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.md --path docs/adr/ADR-20260428-architecture-package-method.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: M1 `bash scripts/ci.sh --mode explicit --path scripts/artifact_lifecycle_contracts.py --path scripts/artifact_lifecycle_validation.py --path scripts/test-artifact-lifecycle-validator.py` passed and executed selected check `artifact_lifecycle.regression`.
- 2026-04-28: M1 `git diff --check -- scripts tests/fixtures/artifact-lifecycle docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/plan.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: M1 `python scripts/validate-change-metadata.py docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed after closeout metadata updates.
- 2026-04-28: M1 `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml --path docs/plan.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.test.md` passed after closeout updates.
- 2026-04-28: M2 manual template heading inspection with `rg -n "^## " templates/architecture.md templates/adr.md` confirmed the architecture template has lifecycle metadata before all 12 official arc42 section headings and the ADR template has the required status, context, decision, alternatives, consequences, and follow-up headings.
- 2026-04-28: M2 `python scripts/select-validation.py --mode explicit --path templates/architecture.md --path templates/adr.md --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md` returned `status: ok` and selected `artifact_lifecycle.validate` plus `selector.regression`.
- 2026-04-28: M2 `bash scripts/ci.sh --mode explicit --path templates/architecture.md --path templates/adr.md --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md` passed.
- 2026-04-28: M2 `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/architecture-package-method.md --path specs/rigorloop-workflow.md` passed.
- 2026-04-28: M2 `git diff --check -- templates CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: M2 closeout `python scripts/validate-change-metadata.py docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: M2 closeout `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml --path docs/plan.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.test.md --path specs/rigorloop-workflow.md` passed.
- 2026-04-28: M2 closeout `python scripts/test-change-metadata-validator.py` passed.
- 2026-04-28: initial M3 `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260428-architecture-package-method.md --path specs/architecture-package-method.md` failed as expected because the canonical package did not exist yet.
- 2026-04-28: M3 manual heading inspection with `rg -n "^## " docs/architecture/system/architecture.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md` confirmed the canonical package preserves lifecycle metadata before all 12 official arc42 section headings and the change-local delta records historical merge-back status.
- 2026-04-28: M3 `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260428-architecture-package-method.md --path specs/architecture-package-method.md` passed.
- 2026-04-28: M3 selector inspection `python scripts/select-validation.py --mode explicit --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd` returned `status: blocked` with `docs/architecture/system/architecture.md` selecting `artifact_lifecycle.validate` and both `.mmd` paths unclassified for manual routing.
- 2026-04-28: M3 supported-path selector `python scripts/select-validation.py --mode explicit --path docs/architecture/system/architecture.md` returned `status: ok` and selected `artifact_lifecycle.validate`.
- 2026-04-28: M3 `bash scripts/ci.sh --mode explicit --path docs/architecture/system/architecture.md` passed.
- 2026-04-28: M3 `git diff --check -- docs/architecture/system docs/changes/2026-04-28-architecture-skills-c4-arc42-adr docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: M3 closeout `python scripts/validate-change-metadata.py docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: M3 closeout `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml --path docs/plan.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260428-architecture-package-method.md` passed.
- 2026-04-28: M3 closeout `python scripts/test-change-metadata-validator.py` passed.
- 2026-04-28: M4 `python scripts/validate-skills.py` passed after canonical skill edits.
- 2026-04-28: initial M4 `python scripts/test-skill-validator.py` failed because the edited architecture skills did not preserve the exact scan-sensitive `summary and stable-ID first`, `check IDs`, `file paths`, `line citations`, and whole-file-read wording; the skill wording was corrected before generation.
- 2026-04-28: M4 `python scripts/test-skill-validator.py` passed after wording correction.
- 2026-04-28: initial M4 `python scripts/build-skills.py --check` failed as expected after canonical skill edits because `.codex/skills/architecture*/SKILL.md` was stale; generated skills were refreshed with `python scripts/build-skills.py`.
- 2026-04-28: M4 `python scripts/build-adapters.py --version 0.1.1` refreshed public adapter package skill output from canonical sources.
- 2026-04-28: M4 `python scripts/build-skills.py --check` passed after generated skill refresh.
- 2026-04-28: M4 `python scripts/test-adapter-distribution.py` passed with 56 tests.
- 2026-04-28: M4 `python scripts/build-adapters.py --version 0.1.1 --check` passed and reported adapter output in sync.
- 2026-04-28: M4 `python scripts/validate-adapters.py --version 0.1.1` passed.
- 2026-04-28: M4 `python scripts/test-select-validation.py` passed with 27 tests.
- 2026-04-28: M4 selector inspection `python scripts/select-validation.py --mode explicit --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/manifest.yaml` returned `status: ok` and selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, and `adapters.validate`.
- 2026-04-28: M4 `bash scripts/ci.sh --mode explicit --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path dist/adapters/manifest.yaml` passed all selected checks.
- 2026-04-28: M4 closeout `python scripts/validate-change-metadata.py docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.
- 2026-04-28: M4 closeout `python scripts/test-change-metadata-validator.py` passed.
- 2026-04-28: M4 closeout `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml --path docs/plan.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260428-architecture-package-method.md` passed.
- 2026-04-28: M4 closeout `python scripts/select-validation.py --mode explicit --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` returned `status: ok` and selected lifecycle, change-metadata, and broad-smoke checks because the active plan requires broad smoke.
- 2026-04-28: M4 closeout `bash scripts/ci.sh --mode broad-smoke` passed.
- 2026-04-28: M4 `git diff --check -- skills/architecture/SKILL.md skills/architecture-review/SKILL.md .codex/skills dist/adapters docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml` passed.

## Outcome and retrospective

- M1, M2, M3, and M4 are complete. M5 has not been started.

## Readiness

- Immediate next repository stage: `code-review` for the completed M4 slice.
- Test spec readiness: complete; `specs/architecture-package-method.test.md` is active.
- Next implementation milestone after M4 review handoff: M5, `Add legacy normalization follow-up and final closeout evidence`.
