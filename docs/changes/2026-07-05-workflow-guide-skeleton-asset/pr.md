# PR Handoff

## Status

- Change ID: 2026-07-05-workflow-guide-skeleton-asset
- Stage: pr
- PR status: opened
- PR URL: https://github.com/xiongxianfei/rigorloop/pull/122
- Last updated: 2026-07-05

## Title

feat: add workflow guide skeleton asset

## Body

### Summary

- Add a packaged `skills/workflow/assets/workflows-skeleton.md` for new or fully refreshed project-local `docs/workflows.md` guides.
- Map the skeleton from `skills/workflow/SKILL.md` with a `COPY` resource-map entry.
- Add workflow-guide skeleton validation, generated skill mirror proof, and adapter archive proof for packaged workflow assets.
- Record proposal, review, behavior-preservation, explain-change, and verify evidence for the workflow-managed change.

### Why

- The workflow skill already owns creating or refreshing `docs/workflows.md`, but it did not ship a stable copy-and-fill structure.
- Without the skeleton, agents could recreate workflow guides inconsistently, omit required registry/table sections, or drift from the workflow-map contract.
- The accepted direction keeps normative policy in specs and concise skill instructions while using the asset for structure.

### Spec / plan / architecture

- Proposal: `docs/proposals/2026-07-05-workflow-guide-skeleton-asset.md`
- Spec: `specs/workflow-skill-artifact-location-map.md`
- Test spec: `specs/workflow-skill-artifact-location-map.test.md`
- Architecture / ADRs: `docs/changes/2026-07-05-workflow-guide-skeleton-asset/architecture-assessment.md` records `architecture-not-required`
- Plan: `docs/plans/2026-07-05-workflow-guide-skeleton-asset.md`
- Explain change: `docs/changes/2026-07-05-workflow-guide-skeleton-asset/explain-change.md`
- Verify report: `docs/changes/2026-07-05-workflow-guide-skeleton-asset/verify-report.md`

### What changed

- Added the workflow guide skeleton asset with source rank, lifecycle graph scaffold, stage-obligation scaffold, YAML registry, Markdown artifact table, review placement, plan surfaces, customization, migration, and validation notes.
- Added a workflow skill resource-map entry that points agents to copy the skeleton for new or fully rewritten project-local workflow guides.
- Amended the workflow-map spec and test spec with skeleton structure, validation, packaging, and non-migration requirements.
- Added validator coverage that checks skeleton metadata, sections, structural boundaries, registry/table consistency, and stage-skill table-duplication boundaries.
- Added generated-output proof for local skill mirrors and adapter archives when `workflow` is packaged.
- Preserved existing `docs/workflows.md`; this change does not migrate historical workflow guides.

### Tests and verification

- [x] `python scripts/test-skill-validator.py -k workflow_guide_skeleton` — 4 tests OK
- [x] `python scripts/test-skill-validator.py -k workflow` — 41 tests OK
- [x] `python scripts/validate-guide-system.py` — guide system validation passed
- [x] `python scripts/test-build-skills.py` — 7 tests OK
- [x] `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives AdapterDistributionTests.test_adapter_archives_include_workflow_skeleton_when_workflow_is_packaged` — 2 tests OK
- [x] `python scripts/validate-skills.py` — validated 24 skill files
- [x] `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-05-workflow-guide-skeleton-asset` — reviews=8, findings=3, log_entries=8, resolution_entries=3
- [x] `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` — valid change metadata
- [x] `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` — validated 3 artifact files
- [x] `python scripts/validate-documentation-prose.py ...` — errors=0 warnings=0
- [x] `git diff --check $(git merge-base HEAD main)..HEAD` — no whitespace errors
- [x] `python scripts/build-adapters.py --version v0.1.3 --output-dir "$tmp_adapters"` plus archive inspection — workflow skeleton present when workflow packaged: `codex`
- [x] `python scripts/test-select-validation.py -k lifecycle_closeout_evidence_files_route_without_manual_debt` — 1 test passed
- [x] `python scripts/test-guide-system-validator.py` — 10 tests OK
- [x] `bash scripts/ci.sh --mode pr --base f72b64930153e4ea4df41f5a098f6f9467944115 --head 09401e6f96c13faf7fef3f701bcfa52d7a7e3ae0` — selected CI checks passed locally
- [ ] CI — failed before selector-routing repair; hosted rerun pending after the repair is pushed

### Requirement coverage

- R58 → T20 → `skills/workflow/assets/workflows-skeleton.md`, skeleton validator tests, guide-system validation
- R59 → T19/T20 → structural skeleton assertions and no full stage-obligations policy-table regression
- R60 → T20 → workflow skill `Resource map` assertion and no full skeleton inline
- R61 → T19/T20 → no stage-skill rewrite; validator coverage preserves stage-skill boundary
- R62 → T20 → skeleton validator and workflow-map composition checks
- R63 → T21 → generated skill mirror test and adapter archive packaging test
- AC30 → T19 → `docs/workflows.md` remains unchanged

### Review resolution summary

- Accepted: 2
- Rejected: 0
- Deferred: 1
- Partially accepted: 0
- Needs decision: 0
- Review-resolution: `docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md`

### Risks and rollback

- Risk: skeleton becomes hidden policy. Mitigation: structural tests reject full lifecycle policy table content.
- Risk: registry validation splits ownership. Mitigation: skeleton validation composes the workflow-map validator rather than creating a second registry contract.
- Risk: generated packaging omits the skeleton. Mitigation: generated skill and adapter archive checks prove inclusion when `workflow` is packaged.
- Rollback: remove the skeleton asset, workflow skill resource-map entry, skeleton-specific validation/tests, and generated-output proof checks together.

### Reviewer notes

- The adapter packaging assertion is intentionally conditional: it checks archives that actually package `workflow`. Current portability rules package `workflow` for Codex and exclude it from Claude/opencode because of existing Codex-specific `$skill` invocation syntax.
- Existing `docs/workflows.md` is intentionally untouched.
- `<slug>` placeholder normalization was deferred by owner direction from M1 review and is not part of this scope.
- PR #122 hosted CI initially failed because `architecture-assessment.md` and `pr.md` lacked deterministic change-local evidence routing. The repair registers those evidence classes and updates the guide-system validator fixture.

### Follow-ups

- Consider a future placeholder-literal normalization task if the approved workflow-map contract moves away from `<slug>`.
- Hosted CI should be reviewed after the PR opens.
