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

- Current milestone: M1. Canonical skeleton asset and workflow skill mapping
- Current milestone state: review-requested
- Latest review evidence: test-spec-review-r1
- Last reviewed milestone: none
- Review status: review-requested; stage=code-review; round=r1
- Remaining in-scope implementation milestones: M1, M2, M3
- Next stage: code-review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — code-review, explain-change, verify, and PR handoff remain open.

## Milestones

### M1. Canonical skeleton asset and workflow skill mapping

- Milestone state: review-requested
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
  - [ ] code-review completed
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] current milestone projection updated before starting M2
- Milestone commit message: `M1: add workflow guide skeleton asset`
- Rollback: remove the resource-map entry and skeleton asset together.

### M2. Validation coverage and fixtures

- Milestone state: planned
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
  - [ ] targeted validation passed
  - [ ] hand off to code-review for M2
- Review closeout:
  - [ ] code-review completed
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] current milestone projection updated before starting M3
- Milestone commit message: `M2: validate workflow guide skeleton packaging`
- Rollback: remove skeleton-specific checks while preserving independently valid workflow-map registry validation.

### M3. Generated output proof and lifecycle closeout

- Milestone state: planned
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
  - [ ] targeted validation passed
  - [ ] hand off to code-review for M3
- Review closeout:
  - [ ] code-review completed
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] final closeout gates can begin only after all implementation milestones are closed
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

## Decision log

- 2026-07-05: Use `skills/workflow/assets/workflows-skeleton.md` as the asset path -> mirrors target artifact `docs/workflows.md`.
- 2026-07-05: Amend existing workflow-map spec -> it already owns guide registry and placement behavior.
- 2026-07-05: Split implementation into asset, validation, and packaging-proof milestones -> keeps diffs reviewable and preserves generated-output boundaries.
- 2026-07-05: Use `docs/plans/YYYY-MM-DD-<slug>.md` for the skeleton change-plan path -> the approved workflow-map spec's plan-body contract outranks the older proposal draft path.

## Surprises and discoveries

- The proposal draft skeleton used `docs/changes/<change-id>/plan.md` for `change_plan`, but the approved workflow-map spec requires `docs/plans/YYYY-MM-DD-slug.md`. M1 follows the approved spec.

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

## Outcome and retrospective

Pending. Keep this section historical until implementation, review, verification, and PR handoff complete.

## Readiness

- See `Current Handoff Summary`.
- Readiness is not Done; downstream gates remain open.

## Risks and follow-ups

- Risk: skeleton becomes hidden policy. Mitigation: keep lifecycle policy in specs, workflow guide, and concise skill instructions.
- Risk: validator duplicates workflow-map registry ownership. Mitigation: compose or extend workflow-map validation instead of cloning a divergent contract.
- Risk: generated packaging proof is skipped. Mitigation: keep M3 focused on repository-owned generated-skill and adapter proof.
