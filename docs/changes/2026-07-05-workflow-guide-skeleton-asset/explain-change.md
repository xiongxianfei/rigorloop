# Explain Change

## Status

- Change ID: 2026-07-05-workflow-guide-skeleton-asset
- Stage: explain-change
- Evidence status: before final verify
- Last updated: 2026-07-05

## Summary

This change gives the workflow skill a packaged structural skeleton for creating or fully refreshing `docs/workflows.md`.
It also amends the workflow-map spec and test spec, adds validator coverage, proves generated skill and adapter packaging behavior, and records the lifecycle evidence for the proposal through final implementation review.

The change exists because the workflow skill already owned guide creation behavior, but the skill package did not include the copy-and-fill structure agents need to create a consistent project-local workflow guide.

## Problem

The accepted proposal identified a source-of-truth gap:

- `skills/workflow/SKILL.md` said the workflow skill creates or refreshes `docs/workflows.md`.
- The workflow-map contract expected that guide to contain source rank, registry, routing, placement, customization, migration, and validation guidance.
- The workflow skill did not ship a skeleton asset for that structured guide.

Without a skeleton, agents could recreate the guide from memory, omit required sections, duplicate long placement guidance in stage skills, or drift from the registry contract.

## Decision Trail

| Decision source | Decision | Impact |
| --- | --- | --- |
| Proposal | Add `skills/workflow/assets/workflows-skeleton.md` and map it from `skills/workflow/SKILL.md`. | The workflow skill now ships the structure it already needs for guide creation. |
| Proposal | Use `assets/workflows-skeleton.md` because it mirrors `docs/workflows.md`. | The asset name follows the target artifact name. |
| Proposal | Include both YAML registry and Markdown table. | YAML supports validator-oriented checks; Markdown supports human review. |
| Proposal | Do not migrate existing `docs/workflows.md`. | Existing project guides remain untouched; skeleton use is forward-looking. |
| Spec R58-R63 | Keep the skeleton structural, mapped, validated, and packaged when workflow is packaged. | Implementation focused on structure, validator coverage, and generated-output proof. |
| Test spec T21 | Prove generated skill mirrors and adapter packages include the mapped skeleton asset when packaging applies. | M3 added direct generated skill and adapter archive assertions. |
| Architecture assessment | `architecture-not-required`. | No runtime architecture or ADR was introduced. |
| Plan M1 | Add canonical asset and workflow skill map. | Created the skeleton and `COPY` resource-map entry. |
| Plan M2 | Add validation coverage and fixtures. | Added deterministic validator and negative tests. |
| Plan M3 | Prove generated output and behavior preservation. | Added packaging assertions and behavior-preservation evidence. |

## Diff Rationale By Area

| Area | Files | Why changed | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- |
| Workflow skeleton asset | `skills/workflow/assets/workflows-skeleton.md` | Provides a copy-and-fill structure for new or fully refreshed project-local workflow guides. | Proposal; spec R58-R59 | `test_workflow_guide_skeleton_m1_contains_required_structure`; `validate-skills.py` |
| Workflow skill map | `skills/workflow/SKILL.md` | Adds a `Resource map` entry that tells agents to copy the skeleton and not emit unfilled placeholders. | Proposal; spec R60 | `test_workflow_guide_skeleton_m1_asset_and_resource_map_exist` |
| Spec contract | `specs/workflow-skill-artifact-location-map.md` | Adds skeleton asset, structural boundary, validation, packaging, and non-migration requirements. | Accepted proposal | Spec-review R1; test-spec mapping |
| Test spec | `specs/workflow-skill-artifact-location-map.test.md` | Maps skeleton requirements to concrete validator, packaging, edge-case, and non-migration proof cases. | Spec R58-R63 | Test-spec-review R1 |
| Skeleton validator | `scripts/skill_validation.py` | Validates metadata comments, required sections, registry coverage, table consistency, source-rank terms, structural boundary, and stage-skill table boundary. | Spec R58-R62 | `python scripts/test-skill-validator.py -k workflow_guide_skeleton` |
| Guide-system composition | `scripts/validate-guide-system.py` | Runs the skeleton validator from the guide-system validation path while preserving workflow-map ownership of registry/table consistency. | Spec R62; validator layering decision | `python scripts/validate-guide-system.py` |
| Validator tests | `scripts/test-skill-validator.py` | Adds positive and negative coverage for missing sections, missing required registry entries, registry/table drift, source-rank terms, and full policy table regression. | Test spec T19-T20 | `python scripts/test-skill-validator.py -k workflow` |
| Generated skill proof | `scripts/test-build-skills.py` | Asserts generated local skill mirror output includes `workflow/assets/workflows-skeleton.md`. | Spec R63; test spec T21 | `python scripts/test-build-skills.py` |
| Adapter packaging proof | `scripts/test-adapter-distribution.py` | Asserts every adapter archive that actually packages `workflow` also packages the skeleton asset with canonical text. | Spec R63; test spec T21 | targeted adapter archive tests |
| Selector routing repair | `scripts/validation_selection.py`; `scripts/test-select-validation.py`; `scripts/test-guide-system-validator.py` | Registers deterministic architecture-assessment and PR handoff evidence so PR-mode CI does not block on manual routing, and updates the guide-system fixture to include the canonical workflow skeleton. | CI failure from PR #122; selector registration contract | `python scripts/test-select-validation.py -k lifecycle_closeout_evidence_files_route_without_manual_debt`; `python scripts/test-guide-system-validator.py`; `bash scripts/ci.sh --mode pr ...` |
| Lifecycle evidence | `docs/changes/2026-07-05-workflow-guide-skeleton-asset/` | Records proposal, reviews, behavior preservation, review resolution, and change metadata. | Repository workflow contract | review artifact and lifecycle validators |
| Planning state | `docs/plans/2026-07-05-workflow-guide-skeleton-asset.md`; `docs/plan.md` | Tracks milestone progression from planning through code-review and now explain-change handoff. | Active plan policy | lifecycle explicit-path validation |
| Learn evidence | `docs/learn/sessions/2026-07-05-workflow-guide-skeleton.md` | Captures the related lesson that motivated the skeleton/source-of-truth alignment. | User request to commit related learn file | tracked in change metadata |

## Tests Added Or Changed

| Test or check | What it proves | Why this level is appropriate |
| --- | --- | --- |
| `test_workflow_guide_skeleton_m1_asset_and_resource_map_exist` | The asset exists and `skills/workflow/SKILL.md` maps it with `COPY`. | Unit-level structural check catches missing packaged-source wiring. |
| `test_workflow_guide_skeleton_m1_contains_required_structure` | The skeleton has required metadata, sections, registry, table, and source-rank terms. | Unit-level text validation is enough for a structural Markdown asset. |
| `test_workflow_guide_skeleton_m1_stays_structural` | The skeleton avoids hidden lifecycle policy, including the full stage-obligations policy table. | Regression coverage protects the source-of-truth boundary from review-found drift. |
| `test_workflow_guide_skeleton_m2_composes_workflow_map_validation` | The skeleton validator composes workflow-map registry/table checks and rejects missing sections, missing entries, and table drift. | Integration-style validator test proves layering without duplicating a second registry contract. |
| `test_output_dir_generates_complete_skill_mirror` | Generated local skill mirror output includes `workflow/assets/workflows-skeleton.md`. | Smoke-level generated-output proof matches T21 and avoids tracked generated output edits. |
| `test_adapter_archives_include_workflow_skeleton_when_workflow_is_packaged` | Adapter archives include the skeleton whenever they package `workflow`. | Smoke-level archive proof covers the packaging failure mode from R63/EC11b. |
| `test_lifecycle_closeout_evidence_files_route_without_manual_debt` | `architecture-assessment.md` and change-local `pr.md` route through lifecycle validation instead of selector manual-routing blockers. | Regression coverage matches the hosted CI failure mode. |
| `test_valid_fixture_passes` in `scripts/test-guide-system-validator.py` | The guide-system valid fixture includes the workflow skeleton expected by the new skeleton validator. | Regression coverage keeps guide-system tests aligned with the new validator contract. |

## Validation Evidence Available Before Final Verify

Validation has been run at each milestone and review gate.
Key evidence recorded in the plan and change metadata includes:

| Command | Result |
| --- | --- |
| `python scripts/test-skill-validator.py -k workflow_guide_skeleton_m1` | pass |
| `python scripts/test-skill-validator.py -k workflow_guide_skeleton` | pass |
| `python scripts/test-skill-validator.py -k workflow` | pass |
| `python scripts/test-skill-validator.py -k workflow_map` | pass |
| `python scripts/validate-guide-system.py` | pass |
| `python scripts/test-build-skills.py` | pass |
| `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives AdapterDistributionTests.test_adapter_archives_include_workflow_skeleton_when_workflow_is_packaged` | pass |
| `python scripts/validate-skills.py` | pass |
| `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-05-workflow-guide-skeleton-asset` | pass |
| `python scripts/validate-change-metadata.py docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml` | pass |
| `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` | pass |
| `python scripts/validate-documentation-prose.py ...` | pass |
| `git diff --check ...` | pass |
| `python scripts/test-select-validation.py -k lifecycle_closeout_evidence_files_route_without_manual_debt` | pass |
| `python scripts/test-guide-system-validator.py` | pass |
| `bash scripts/ci.sh --mode pr --base f72b64930153e4ea4df41f5a098f6f9467944115 --head 09401e6f96c13faf7fef3f701bcfa52d7a7e3ae0` | pass |

No hosted CI result is claimed by this explanation.
Final `verify` still owns branch-readiness and final validation conclusions.

## Review Resolution Summary

Review resolution is recorded in `docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md`.

| Review stage | Outcome |
| --- | --- |
| proposal-review-r1 | no material findings |
| spec-review-r1 | no material findings |
| plan-review-r1 | no material findings |
| test-spec-review-r1 | no material findings |
| code-review-m1-r1 | 3 material findings recorded |
| code-review-m1-r2 | no material findings |
| code-review-m2-r1 | no material findings |
| code-review-m3-r1 | no material findings |

M1 review findings were resolved or dispositioned:

- `WGS-M1-CR1`: accepted and fixed by aligning source-rank text and tests.
- `WGS-M1-CR2`: deferred by owner direction; `<slug>` remains for this pass and future normalization is tracked as a later concern.
- `WGS-M1-CR3`: accepted and fixed by replacing the populated stage-obligations policy table with a placeholder-oriented scaffold.

`review-resolution.md` has `Closeout status: closed`; the review log records no open findings.

## Alternatives Rejected

| Alternative | Reason rejected |
| --- | --- |
| Keep workflow without a skeleton | Leaves agents recreating a structured guide from memory and gives validators no packaged template to check. |
| Inline the full guide structure in `SKILL.md` | Makes the skill noisy and increases drift between structure and policy. |
| Put hidden lifecycle policy in the skeleton | Creates a second policy owner and violates the structural-only requirement. |
| Force workflow into every adapter archive | R63 requires the skeleton when an adapter packages `workflow`; current portability rules exclude `workflow` from Claude/opencode because of Codex-specific `$skill` syntax. |
| Regenerate or migrate existing `docs/workflows.md` | The proposal and spec explicitly preserve existing guides and require only forward use for new or fully refreshed guides. |
| Add a CLI scaffold | Explicitly out of scope for this proposal. |

## Scope Control

The change preserves the non-goals:

- no workflow order change;
- no artifact content schema change;
- no stage-skill broad rewrite;
- no historical `docs/workflows.md` migration;
- no generated public adapter hand edits;
- no CLI scaffold.

The workflow skill remains responsible for guide creation and refresh behavior.
Stage skills continue to own their artifact content and portable defaults.
The workflow-map validator remains the owner of registry/table consistency.

## Risks And Follow-Ups

| Risk or follow-up | Status |
| --- | --- |
| `<slug>` placeholder normalization | Deferred by owner direction from M1 review; future validator/spec alignment may address it. |
| Claude/opencode workflow packaging | Not applicable in this change while `workflow` remains excluded by existing portability rules. |
| Existing workflow guides | Not migrated by this change; future explicit migration work would need its own task. |
| Final branch readiness | Not claimed here; route to `verify` after this explanation. |

## Readiness

Explain-change is complete for this change.
The active plan should now hand off to `verify`.
