# Workflow Skill Artifact-Location Map Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: `2026-06-17-workflow-skill-artifact-location-map`
- Current owner: agent
- Current stage: implement
- Next stage: code-review
- Blockers: none

## Purpose / big picture

Implement the approved workflow skill artifact-location map contract. The change makes `docs/workflows.md` a deterministic project-local artifact-location map with a machine-checkable registry, keeps detailed plan bodies under `docs/plans/`, preserves stage-skill content ownership, and adds validation so workflow-map, skill-default, and generated-adapter placement drift is caught.

## Source artifacts

- Proposal: [Workflow Skill Artifact-Location Map](../proposals/2026-06-17-workflow-skill-artifact-location-map.md)
- Spec: [Workflow Skill Artifact-Location Map](../../specs/workflow-skill-artifact-location-map.md)
- Architecture: not required; the approved spec states this is a workflow-governance and validation change, not a runtime architecture change.
- Test spec: [Workflow Skill Artifact-Location Map Test Spec](../../specs/workflow-skill-artifact-location-map.test.md)
- Spec review: [spec-review-r2](../changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md)
- Change metadata: [change.yaml](../changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml)

## Context and orientation

The implementation touches workflow-governance surfaces, canonical skill text, and validation. The governing plan-path decision is settled: `docs/plan.md` is the lifecycle index, detailed plan bodies live under `docs/plans/YYYY-MM-DD-slug.md`, and `docs/changes/<change-id>/` is the change-local evidence pack.

Relevant surfaces:

- `docs/workflows.md`: project-local workflow guide and artifact-location map to restructure with a YAML registry plus human-readable projections.
- `skills/workflow/SKILL.md`: canonical workflow skill source that must create or refresh the workflow guide, define source rank, block unknown artifacts, and preserve stage-skill content ownership.
- `skills/plan/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`: first-slice stage skills to inspect and edit only for direct contradictions.
- `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, and related validation scripts: likely homes for drift, registry, and adapter checks.
- `docs/changes/2026-06-17-workflow-skill-artifact-location-map/`: change-local review, resolution, metadata, and implementation evidence.

## Non-goals

- Do not change lifecycle stage order.
- Do not redefine proposal, spec, plan, review, verify, PR, or learn content schemas.
- Do not migrate existing `docs/plans/*.md` files.
- Do not introduce a new CLI scaffold for change-pack creation.
- Do not remove stage-skill portable defaults.
- Do not hand-edit generated public adapter output.
- Do not bulk-edit lifecycle skills for style-only consistency.

## Requirements covered

- R1-R5: M1 updates workflow-skill ownership, map-refresh, and stage-skill boundary text.
- R6-R15: M1 adds the workflow-map registry and Markdown projection contract to `docs/workflows.md`.
- R16-R20: M1 preserves `docs/plan.md` as index and `docs/plans/YYYY-MM-DD-slug.md` as detailed plan-body path.
- R21-R25: M1 updates workflow defaults and directly contradictory stage-skill placement text only.
- R26-R34: M1 encodes source rank, explicit-path limits, fallback behavior, and formal recording boundaries.
- R35-R39: M1 keeps formal review records under `docs/changes/<change-id>/reviews/` and review-log/resolution placement.
- R40-R41: M1 prevents learn sessions from becoming live placement authority.
- R42-R47: M2 adds drift, unknown-artifact, registry/table, and review-path validation.
- R48: M3 proves generated adapters include the updated workflow skill when packaged.
- R49: M3 records cold-read proof for proposal-review placement, workflow-managed plan placement, and `docs/plan.md` purpose.
- R50-R53: All milestones preserve lifecycle order, artifact schemas, generated-output boundaries, and customer-project portability.

## Current Handoff Summary

- Current milestone: M2. Workflow-map validation and drift checks
- Current milestone state: review-requested
- Last reviewed milestone: M1
- Review status: WFO-CR1 resolved; M2 returned to code-review
- Remaining in-scope implementation milestones: M2 pending code-review, M3
- Next stage: code-review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M2 re-review, M3 implementation and code-review, explain-change, verify, and PR handoff remain.

## Milestones

### M1. Workflow map and skill contract update

- Milestone state: closed
- Goal: Update `docs/workflows.md` and directly affected skill text so the project-local artifact-location map, portable defaults, source rank, and formal evidence placement match the approved spec.
- Requirements: R1-R41, R50-R53
- Files/components likely touched:
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `.agents/skills/` only through repository-owned generation if required by normal local mirror workflows
- Dependencies:
  - Approved spec and this plan.
  - Test spec should define exact static checks before implementation starts.
- Tests to add/update:
  - Skill text validation fixtures for workflow-map ownership, stage-skill ownership boundary, source rank, plan path, review path, and learn-session non-authority.
  - Static tests that reject stale `docs/changes/<change-id>/plan.md` as the canonical plan-body path.
- Implementation steps:
  - Add or refresh `docs/workflows.md` sections for source rank, lifecycle graph, stage obligations, artifact registry, artifact-location map, review placement, plan surfaces, customization, and migration notes.
  - Add a canonical fenced YAML `artifact_locations` registry and synchronized Markdown projections.
  - Update `skills/workflow/SKILL.md` to own creating/refreshing `docs/workflows.md`, preserve stage-skill content ownership, block unknown artifacts, and record map-update reasons.
  - Inspect `plan`, `proposal-review`, and `spec-review` skills and edit only direct contradictions.
  - Keep `docs/plans/YYYY-MM-DD-slug.md` as the canonical detailed plan-body path and `docs/changes/<change-id>/reviews/` as formal review-record placement.
- Validation commands:
  - `python scripts/test-skill-validator.py -k workflow`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md`
  - `git diff --check -- docs/workflows.md skills/workflow/SKILL.md skills/plan/SKILL.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md`
- Expected observable result: A maintainer can cold-read `docs/workflows.md` and the workflow skill and answer where proposals, specs, plans, reviews, verification, PR handoff, and learn records go without prior chat context.
- Commit message: `M1: update workflow map and placement guidance`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log unchanged; no new sequencing decision
  - validation notes updated
  - milestone commit created in this handoff
- Risks:
  - The workflow skill becomes too large or starts owning artifact content.
  - The workflow map and stage skills drift during the same edit.
- Rollback/recovery:
  - Revert `docs/workflows.md` and skill text together, then rerun skill validation and lifecycle validation.

### M2. Workflow-map validation and drift checks

- Milestone state: review-requested
- Goal: Add deterministic validation for registry shape, registry/table agreement, stale plan-path drift, review path drift, unknown artifact blocking, and affected skill defaults.
- Requirements: R6-R15, R42-R47, AC3-AC6, AC11-AC16, AC19-AC20
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py` if needed as an entry point
  - Optional focused workflow-map validator or fixtures if existing skill validation becomes too broad
  - `docs/workflows.md`
- Dependencies:
  - M1 registry and skill text shape.
  - Test spec must define exact fixtures and failure modes.
- Tests to add/update:
  - Parser/fixture tests for a valid YAML registry and synchronized Markdown table.
  - Failure fixtures for missing owner/trigger, duplicate placement representation, stale `docs/changes/<change-id>/plan.md`, formal review records outside `docs/changes/<change-id>/reviews/`, and unknown artifact types.
  - Tests that directly affected stage skills do not contradict the workflow map.
- Implementation steps:
  - Choose whether to extend existing skill validation or create a small workflow-map validator.
  - Parse the fenced YAML registry structurally rather than by prose.
  - Compare registry entries to the Markdown artifact-location tables.
  - Add drift checks against workflow skill defaults and first-slice affected stage skills.
  - Ensure validators report unresolved unknown artifact types instead of deriving paths.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md`
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py docs/workflows.md docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md`
- Expected observable result: Validation fails deterministically when workflow map, workflow skill defaults, or directly affected stage-skill placement text drift.
- Commit message: `M2: validate workflow artifact map drift`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Validators overfit prose instead of stable structure.
  - New checks duplicate artifact lifecycle validation responsibilities.
- Rollback/recovery:
  - Disable only the new workflow-map checks or fixtures, preserve unrelated validation, and record the blocker for follow-up.

### M3. Adapter proof, cold-read evidence, and lifecycle closeout

- Milestone state: planned
- Goal: Prove packaged workflow skill output is current when relevant, record cold-read placement proof, and synchronize lifecycle evidence before final review and verification.
- Requirements: R48-R53, AC16-AC20
- Files/components likely touched:
  - Generated or packaged adapter proof through repository-owned scripts only
  - `docs/changes/2026-06-17-workflow-skill-artifact-location-map/behavior-preservation.md`
  - `docs/changes/2026-06-17-workflow-skill-artifact-location-map/explain-change.md`
  - `docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `docs/plans/2026-06-18-workflow-skill-artifact-location-map.md`
  - `docs/plan.md`
- Dependencies:
  - M1 and M2 closed after code-review.
- Tests to add/update:
  - Adapter generation/check commands when canonical workflow skill changes affect packaged output.
  - Cold-read proof that answers the three required questions without relying on chat history.
- Implementation steps:
  - Run adapter generation/check commands required by selected validation for changed canonical skills.
  - Record behavior-preservation proof covering lifecycle order, stage ownership, plan index, plan body, review records, customer projects, and generated adapters.
  - Record cold-read proof for proposal-review record placement, workflow-managed plan placement, and `docs/plan.md` purpose.
  - Update change metadata, plan progress, validation notes, and final handoff state.
  - Prepare explain-change before final verify.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path specs/workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
- Expected observable result: The branch has current canonical skill, workflow-map, validation, adapter proof, cold-read proof, and lifecycle evidence ready for final code-review, explain-change, verify, and PR handoff.
- Commit message: `M3: prove workflow map packaging and closeout`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Adapter tooling may not be available locally or selected validation may require a narrower command.
  - Cold-read proof could duplicate spec text instead of proving actual skill/map behavior.
- Rollback/recovery:
  - Record adapter proof as blocked only if tooling is unavailable and selected validation allows it; otherwise fix generation drift before final handoff.

## Validation plan

- `python scripts/test-skill-validator.py`: primary regression suite for skill text and placement validation.
- `python scripts/validate-skills.py`: canonical skill structure and contract validation.
- `python scripts/test-build-skills.py`: generated local mirror regression when canonical skills change.
- `python scripts/build-skills.py --check`: generated skill mirror drift check.
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`: public adapter archive smoke when canonical public skills change.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map`: review artifact integrity.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`: change metadata integrity.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: lifecycle language and artifact-scope validation for touched artifacts.
- `bash scripts/ci.sh --mode explicit --path ...`: selected repository-owned validation for touched surfaces before final handoff.

## Risks and recovery

- Risk: `docs/workflows.md` becomes a second copy of stage-skill schemas.
  - Recovery: Keep the workflow map limited to placement, owner, and required trigger; move content-schema rules back to owning stage skills or specs.
- Risk: The registry and Markdown table drift.
  - Recovery: Treat registry as validator source of truth and make registry/table mismatch fail.
- Risk: Plan placement confusion reappears.
  - Recovery: Keep `docs/plans/YYYY-MM-DD-slug.md` as the only canonical detailed plan-body path and add stale-path validation for `docs/changes/<change-id>/plan.md`.
- Risk: Customer projects without `docs/workflows.md` lose portable defaults.
  - Recovery: Keep stage-skill portable defaults and source-rank fallback.
- Risk: Generated adapter proof is missed after canonical workflow skill changes.
  - Recovery: Run selected adapter drift/generation validation and record any tooling blocker before claiming readiness.

## Dependencies

- Spec approval from spec-review R2.
- Plan-review approval before test-spec and implementation.
- Test-spec must translate every `MUST` into concrete checks before implementation.
- Repository-owned validation scripts must remain the source for CI and adapter proof.

## Progress

- 2026-06-18: Created execution plan after spec-review R2 approved the revised spec.
- 2026-06-18: Created active test spec after plan-review R1 approved the execution plan.
- 2026-06-18: Recorded owner approval of the active test spec for implementation reliance.
- 2026-06-18: Implemented M1. Added focused tests first for workflow-map registry and workflow-skill default paths. Updated `docs/workflows.md` with canonical YAML registry, Markdown projections, review placement, plan surfaces, customization, and migration notes. Updated `skills/workflow/SKILL.md` to define map ownership, tracked-guide behavior, source-rank fallback, formal change-pack evidence boundaries, unknown-artifact blocking, map-update reason recording, and current default paths.
- 2026-06-18: Inspected `skills/plan/SKILL.md`, `skills/proposal-review/SKILL.md`, and `skills/spec-review/SKILL.md`; no M1 edit was needed because their plan and review placement text already matched the approved map.
- 2026-06-18: Recorded code-review M1 R1 as clean-with-notes with no material findings. Closed M1 and handed off to M2 implementation.
- 2026-06-18: Started M2 implementation for workflow-map structural validation and drift checks.
- 2026-06-18: Implemented M2. Added structural workflow artifact-map validation to `scripts/skill_validation.py` and fixture-backed tests in `scripts/test-skill-validator.py` for registry parsing, missing fields, duplicate registry keys, ambiguous placement representations, table/registry mismatch, stale change-pack plan paths, review records outside the change pack, workflow-skill default drift, affected stage-skill contradictions, and unknown artifact types. Wired the validator into canonical workflow skill validation.
- 2026-06-18: Recorded code-review M2 R1 as changes-requested with WFO-CR1 open. M2 needs review-resolution before re-review.
- 2026-06-18: Resolved WFO-CR1 by requiring `architecture_record` and `adr` in workflow artifact-map required-entry validation and adding targeted regression coverage for both missing-entry cases. Returned M2 to code-review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-18 | Use three implementation milestones: map/skill contract, validation, adapter and closeout proof. | The work separates user-facing workflow/skill text from validator implementation and final packaging evidence. | One large milestone combining docs, skills, validation, and adapter proof. |
| 2026-06-18 | Treat architecture as not required for this plan. | The approved spec frames the change as workflow-governance, skill text, and validation behavior without runtime architecture changes. | Add an architecture stage for a non-runtime documentation and validation slice. |

## Surprises and discoveries

- The validation selector required generated-skill and adapter archive proof for M1 because canonical `skills/workflow/SKILL.md` changed; selected CI passed those checks.

## Validation notes

- 2026-06-18: Plan authoring validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-skill-artifact-location-map.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md`
  - `git diff --check -- specs/workflow-skill-artifact-location-map.md docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path specs/workflow-skill-artifact-location-map.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md`
- 2026-06-18: Test spec authoring validation passed after replacing stale readiness wording with active-proof-surface wording:
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.test.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/plan-review-r1.md --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md`
  - `git diff --check -- specs/workflow-skill-artifact-location-map.test.md specs/workflow-skill-artifact-location-map.md docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path specs/workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.test.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/plan-review-r1.md`
- 2026-06-18: M1 implementation validation passed:
  - `python scripts/test-skill-validator.py -k workflow_map_m1`
  - `python scripts/test-skill-validator.py -k project_artifact_location_m1`
  - `python scripts/test-skill-validator.py -k workflow`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md`
  - `git diff --check -- docs/workflows.md skills/workflow/SKILL.md skills/plan/SKILL.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path specs/workflow-skill-artifact-location-map.test.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path specs/workflow-skill-artifact-location-map.test.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
- 2026-06-18: Code-review M1 R1 recording validation passed after adding required clean-receipt fields:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-17-workflow-skill-artifact-location-map`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/code-review-m1-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md`
  - `git diff --check -- docs/changes/2026-06-17-workflow-skill-artifact-location-map docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/code-review-m1-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md`
- 2026-06-18: M2 implementation validation passed:
  - `python scripts/test-skill-validator.py -k workflow_map_m2` first failed before validator helper implementation, then passed after implementation.
  - `python scripts/test-skill-validator.py -k workflow`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md`
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py docs/workflows.md docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md`
  - `git diff --name-status -- docs/plans`
  - `python scripts/select-validation.py --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py docs/workflows.md docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
- 2026-06-18: Code-review M2 R1 recording validation passed after fixing review-resolution needs-decision fields and open-review metadata shape:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-17-workflow-skill-artifact-location-map`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/code-review-m2-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md`
  - `git diff --check -- docs/changes/2026-06-17-workflow-skill-artifact-location-map docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/code-review-m2-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md`
- 2026-06-18: WFO-CR1 resolution validation passed:
  - `python scripts/test-skill-validator.py -k workflow_map_m2`
  - `python scripts/test-skill-validator.py -k workflow`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.test.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py`
  - `git diff --check --`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path specs/workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.test.md`

## Outcome and retrospective

- Pending completion.

## Readiness

- See `Current Handoff Summary`.
- Ready for `code-review` of M2 after WFO-CR1 resolution; not ready for M3, final closeout, verify, or PR.
