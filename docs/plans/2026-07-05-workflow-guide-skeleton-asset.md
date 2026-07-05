# Workflow Guide Skeleton Asset Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Change ID: 2026-07-05-workflow-guide-skeleton-asset
- Start date: 2026-07-05
- Last updated: 2026-07-05
- Related issue or PR: none yet
- Supersedes: none

## Goal

Add a packaged structural workflow-guide skeleton asset for `docs/workflows.md`, map it from the workflow skill, and validate canonical-source, generated-skill, and adapter packaging behavior without changing workflow order or artifact schemas.

## Why now

The workflow skill already owns creation and refresh behavior for project-local workflow guides, but it lacks a copy-and-fill skeleton.
That leaves agents to recreate a substantial structured guide from memory and increases drift risk between `docs/workflows.md`, the workflow skill, stage skills, validators, and generated packaging.

## Scope

### In scope

- Add `skills/workflow/assets/workflows-skeleton.md`.
- Add a `COPY assets/workflows-skeleton.md` resource-map entry to `skills/workflow/SKILL.md`.
- Keep the skeleton structural and aligned with `specs/workflow-skill-artifact-location-map.md`.
- Add validation for skeleton existence, resource-map mapping, required skeleton sections, workflow-map registry/table alignment, and generated packaging when the workflow skill is packaged.
- Update generated mirrors or adapter packaging through repository-owned scripts only when required by canonical source changes.
- Record behavior-preservation and change rationale before verify.

### Out of scope

- Do not change lifecycle stage order.
- Do not change proposal, spec, plan, review, verify, PR, or learn artifact content schemas.
- Do not migrate or regenerate existing `docs/workflows.md`.
- Do not bulk-edit stage skills for wording style.
- Do not hand-edit generated adapter output.
- Do not add a CLI scaffold for workflow guide creation.

## Constraints

- The workflow-map spec is the normative contract for guide registry and placement behavior.
- `docs/workflows.md` owns project-local artifact placement; the skeleton provides structure for new or fully refreshed guides.
- Stage skills keep artifact content ownership and portable defaults.
- Generated output must be deterministic and reproducible from canonical sources.
- Unknown artifact types continue to block rather than infer paths.

## Current Handoff Summary

- Current milestone: M3. Generated output proof and lifecycle closeout
- Current milestone state: closed
- Latest review evidence: code-review-m3-r1
- Last reviewed milestone: M3
- Review status: approved; stage=code-review; round=r1
- Remaining in-scope implementation milestones: none
- Next stage: verify
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: verify-pending, pr-handoff-pending — all implementation milestones, code reviews, review-resolution, and explain-change are complete; verify and PR handoff remain open.

## Milestones

### M1. Canonical skeleton asset and workflow skill mapping

- Milestone state: closed
- Deliverable: `skills/workflow/assets/workflows-skeleton.md` and `skills/workflow/SKILL.md` resource-map guidance.
- Requirements: R54-R61, AC21-AC25, AC27, AC30, AC31.
- Files: `skills/workflow/assets/workflows-skeleton.md`, `skills/workflow/SKILL.md`, focused directly contradictory stage-skill text only if found.
- Tests: skeleton existence, resource-map mapping, required metadata comments, required structural sections, and no hidden lifecycle policy.
- Validation:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py -k workflow`
  - `git diff --check -- skills/workflow/SKILL.md skills/workflow/assets/workflows-skeleton.md`
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M1
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] current milestone projection updated before starting M2
- Milestone commit message: `M1: add workflow guide skeleton asset`
- Rollback: remove the resource-map entry and skeleton asset together.

### M2. Validation coverage and fixtures

- Milestone state: closed
- Deliverable: repository-owned checks proving skeleton/resource-map presence, required section coverage, registry/table alignment, and stage-skill boundary preservation.
- Requirements: R58-R63, AC26-AC31.
- Files: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, related fixtures if needed, and only directly relevant validation docs.
- Tests: missing skeleton, missing resource-map entry, missing required skeleton section, registry/table mismatch, stage-skill full-table duplication when directly checked, and unknown artifact blocking.
- Validation:
  - `python scripts/test-skill-validator.py -k workflow`
  - `python scripts/test-skill-validator.py -k workflow_map`
  - `python scripts/validate-guide-system.py`
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py`
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M2
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] current milestone projection updated before starting M3
- Milestone commit message: `M2: validate workflow guide skeleton packaging`
- Rollback: remove skeleton-specific checks while preserving independently valid workflow-map registry validation.

### M3. Generated output proof and lifecycle closeout

- Milestone state: closed
- Deliverable: generated-skill and adapter packaging proof plus behavior-preservation and explanation evidence.
- Requirements: R62-R63, AC28-AC30.
- Files: generated-skill proof outputs only when repository-owned scripts update tracked generated support surfaces; `dist/adapters/README.md` or `dist/adapters/manifest.yaml` only if canonical packaging metadata changes; change-local evidence.
- Tests: generated skill output includes mapped assets; adapter archive packaging includes the skeleton when workflow is packaged; generated public adapter output is not hand-edited.
- Validation:
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.test.md --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path docs/plan.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml`
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M3
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] final closeout gates can begin only after all implementation milestones are closed
- Milestone commit message: `M3: prove workflow skeleton package output`
- Rollback: revert generated proof updates by regenerating from canonical sources or removing skeleton-specific generated-output checks.

## Progress

- 2026-07-05: Proposal accepted and clean proposal-review recorded.
- 2026-07-05: Workflow-map spec amended and clean spec-review recorded.
- 2026-07-05: Architecture assessment recorded `architecture-not-required`.
- 2026-07-05: Plan created for plan-review.
- 2026-07-05: Plan-review R1 approved the plan with no material findings.
- 2026-07-05: Test spec amended with skeleton asset proof cases and routed to test-spec-review.
- 2026-07-05: Test-spec-review R1 approved the proof map with no material findings.
- 2026-07-05: M1 added workflow guide skeleton tests, `skills/workflow/assets/workflows-skeleton.md`, and the workflow skill resource-map entry.
- 2026-07-05: M1 left existing `docs/workflows.md` and stage-skill placement text unchanged. Rationale: M1 only packages the structural skeleton and workflow skill map; no directly contradictory stage-skill placement text or existing guide migration is in scope for this milestone.
- 2026-07-05: M1 implementation reached review-requested after targeted validation passed.
- 2026-07-05: Code-review M1 R1 requested changes for WGS-M1-CR1, WGS-M1-CR2, and WGS-M1-CR3.
- 2026-07-05: M1 fixed WGS-M1-CR1 by revising skeleton source-rank text and adding required-term assertions.
- 2026-07-05: M1 fixed WGS-M1-CR3 by replacing the populated stage-obligations policy table with a compact scaffold and adding regression assertions against the full policy table.
- 2026-07-05: M1 deferred WGS-M1-CR2 by owner direction; `<slug>` remains in the skeleton for this pass and path-literal normalization is a later validator/spec alignment task.
- 2026-07-05: M1 returned to review-requested for code-review R2 after targeted validation passed.
- 2026-07-05: Code-review M1 R2 recorded clean-with-notes, closed M1, and handed off to implement M2.
- 2026-07-05: M2 added a workflow-guide skeleton validator that composes the existing workflow-map registry/table contract, wired it into guide-system validation, added missing-section, missing-registry-entry, and table-drift regression tests, and aligned the skeleton registry/table projection with canonical workflow-map labels.
- 2026-07-05: M2 reached review-requested after targeted validation passed.
- 2026-07-05: Code-review M2 R1 recorded clean-with-notes, closed M2, and handed off to implement M3.
- 2026-07-05: M3 added explicit generated skill mirror and adapter archive regression assertions for the workflow skeleton asset.
- 2026-07-05: M3 confirmed adapter archive proof is conditional: `workflow` is currently packaged for Codex and excluded from Claude/opencode by existing Codex-specific invocation portability rules.
- 2026-07-05: M3 recorded behavior-preservation evidence and reached review-requested after targeted validation passed.
- 2026-07-05: Code-review M3 R1 completed clean-with-notes, closed all implementation milestones, and handed off to explain-change.
- 2026-07-05: Explain-change recorded durable change rationale and handed off to verify.

## Decision log

- 2026-07-05: Use `skills/workflow/assets/workflows-skeleton.md` as the asset path -> mirrors target artifact `docs/workflows.md`.
- 2026-07-05: Amend existing workflow-map spec -> it already owns guide registry and placement behavior.
- 2026-07-05: Split implementation into asset, validation, and packaging-proof milestones -> keeps diffs reviewable and preserves generated-output boundaries.
- 2026-07-05: Use `docs/plans/YYYY-MM-DD-<slug>.md` for the skeleton change-plan path -> the approved workflow-map spec's plan-body contract outranks the older proposal draft path.
- 2026-07-05: Defer changing `<slug>` placeholders in the skeleton -> owner clarified that this placeholder is intentionally used for now and needs a later alignment task.
- 2026-07-05: Compose skeleton registry/table validation through the workflow-map validator -> avoids a second guide-system-owned registry contract while allowing the explicitly deferred `<slug>` placeholder spelling to remain in the skeleton.
- 2026-07-05: Treat non-Codex workflow adapter archives as not applicable for skeleton inclusion while the workflow skill is excluded from those adapters -> R63 and AC29 require skeleton packaging when the workflow skill is packaged, not forced inclusion of a non-portable skill.

## Surprises and discoveries

- The proposal draft skeleton used `docs/changes/<change-id>/plan.md` for `change_plan`, but the approved workflow-map spec requires `docs/plans/YYYY-MM-DD-slug.md`. M1 follows the approved spec.
- The initial broad adapter archive proof expected the workflow skeleton in every adapter archive. Inspecting adapter decisions showed the current contract is conditional: only Codex packages `workflow`; Claude and opencode exclude it because the skill contains Codex-specific `$skill` invocation syntax.

## Validation notes

- Pre-plan checks:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-05-workflow-guide-skeleton-asset`
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-05-workflow-guide-skeleton-asset.md --path specs/workflow-skill-artifact-location-map.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-log.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/proposal-review-r1.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/spec-review-r1.md`
  - `python scripts/validate-documentation-prose.py --path specs/workflow-skill-artifact-location-map.md`
- M1 implementation validation:
  - `python scripts/test-skill-validator.py -k workflow_guide_skeleton_m1` passed.
  - `python scripts/test-skill-validator.py -k workflow` passed.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/validate-skills.py skills/workflow/SKILL.md` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.test.md --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path docs/plan.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `git diff --check -- skills/workflow/SKILL.md skills/workflow/assets/workflows-skeleton.md scripts/test-skill-validator.py` passed.
- M1 review-fix validation:
  - `python scripts/test-skill-validator.py -k workflow_guide_skeleton_m1` passed.
  - `python scripts/test-skill-validator.py -k workflow` passed.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-05-workflow-guide-skeleton-asset` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path docs/plan.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-log.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/code-review-m1-r1.md` passed.
  - `python scripts/validate-documentation-prose.py --path skills/workflow/assets/workflows-skeleton.md` passed.
  - `python scripts/validate-documentation-prose.py --path skills/workflow/assets/workflows-skeleton.md --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md` passed.
  - `git diff --check -- skills/workflow/assets/workflows-skeleton.md scripts/test-skill-validator.py` passed.
  - `git diff --check -- skills/workflow/assets/workflows-skeleton.md scripts/test-skill-validator.py docs/plans/2026-07-05-workflow-guide-skeleton-asset.md docs/plan.md docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-log.md docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md` passed.
- M1 code-review R2 validation:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-05-workflow-guide-skeleton-asset` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path docs/plan.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-log.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/code-review-m1-r2.md` passed.
  - `python scripts/test-skill-validator.py -k workflow_guide_skeleton_m1` passed.
- M2 implementation validation:
  - `python scripts/test-skill-validator.py -k workflow_guide_skeleton` passed.
  - `python scripts/test-skill-validator.py -k workflow` passed.
  - `python scripts/test-skill-validator.py -k workflow_map` passed.
  - `python scripts/validate-guide-system.py` passed.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path docs/plan.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `python scripts/validate-documentation-prose.py --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path skills/workflow/assets/workflows-skeleton.md` passed.
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py scripts/validate-guide-system.py skills/workflow/assets/workflows-skeleton.md docs/plans/2026-07-05-workflow-guide-skeleton-asset.md docs/plan.md docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
- M2 code-review R1 validation:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-05-workflow-guide-skeleton-asset` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path docs/plan.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-log.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/code-review-m2-r1.md` passed.
  - `python scripts/validate-documentation-prose.py --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/code-review-m2-r1.md --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md` passed.
- M3 implementation validation:
  - `python scripts/test-build-skills.py` passed.
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives AdapterDistributionTests.test_adapter_archives_include_workflow_skeleton_when_workflow_is_packaged` passed.
  - `python scripts/build-skills.py --output-dir "$tmp_skills"; test -f "$tmp_skills/workflow/assets/workflows-skeleton.md"` passed using temporary output.
  - `python scripts/build-adapters.py --version v0.1.3 --output-dir "$tmp_adapters"` plus archive inspection passed; `workflow` skeleton was present when `workflow` was packaged: `codex`.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `python scripts/validate-documentation-prose.py --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/behavior-preservation.md --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.test.md --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path docs/plan.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `git diff --check -- scripts/test-build-skills.py scripts/test-adapter-distribution.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/behavior-preservation.md docs/plans/2026-07-05-workflow-guide-skeleton-asset.md docs/plan.md docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
- M3 code-review R1 validation:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-05-workflow-guide-skeleton-asset` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `python scripts/validate-documentation-prose.py --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/code-review-m3-r1.md --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path docs/plan.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-log.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/code-review-m3-r1.md` passed.
  - `git diff --check -- docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/code-review-m3-r1.md docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-log.md docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md docs/plans/2026-07-05-workflow-guide-skeleton-asset.md docs/plan.md docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
- Explain-change validation:
  - `python scripts/validate-documentation-prose.py --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/explain-change.md --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-07-05-workflow-guide-skeleton-asset.md --path docs/plan.md --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml --path docs/changes/2026-07-05-workflow-guide-skeleton-asset/explain-change.md` passed.
  - `git diff --check -- docs/changes/2026-07-05-workflow-guide-skeleton-asset/explain-change.md docs/plans/2026-07-05-workflow-guide-skeleton-asset.md docs/plan.md docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` passed.

## Outcome and retrospective

Pending. Keep this section historical until implementation, review, verification, and PR handoff complete.

## Readiness

- See `Current Handoff Summary`.
- Readiness is not Done; downstream gates remain open.

## Risks and follow-ups

- Risk: skeleton becomes hidden policy. Mitigation: keep lifecycle policy in specs, workflow guide, and concise skill instructions.
- Risk: validator duplicates workflow-map registry ownership. Mitigation: compose or extend workflow-map validation instead of cloning a divergent contract.
- Risk: generated packaging proof is skipped. Mitigation: keep M3 focused on repository-owned generated-skill and adapter proof.
