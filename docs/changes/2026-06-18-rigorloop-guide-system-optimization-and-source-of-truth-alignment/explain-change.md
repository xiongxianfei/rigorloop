# Explain Change

Change ID: `2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`
Explain date: 2026-06-18

## Summary

This change turns RigorLoop's guide surfaces into a source-ranked guide system. It keeps README as first-contact orientation, keeps `docs/workflows.md` as the project-local workflow and artifact-location guide, keeps `docs/project-map.md` as repository orientation, keeps `docs/plan.md` as the bounded plan index, and adds deterministic guide drift validation.

The implementation is split into three reviewed milestones:

- M1 aligned human-facing guide surfaces.
- M2 added cross-guide validation and selector routing.
- M3 recorded behavior-preservation proof, cold-read proof, and lifecycle evidence.

## Problem

RigorLoop had many useful guide-like surfaces, but contributors still had to infer answers to basic questions:

- where to start;
- which guide is authoritative;
- where artifacts go;
- which skill owns artifact content;
- which file shows active work;
- whether learn sessions are live routing authority.

That ambiguity could route artifacts to the wrong path or make guide prose drift from specs, schemas, skills, and the workflow-map contract.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Treat guides as a system, keep README as a landing guide, keep `docs/workflows.md` as workflow/artifact map, preserve stage-skill portable defaults, and add drift validation. |
| Proposal review | Required plan-location boundary, explicit relationship to workflow artifact-location map work, and split validation ownership. |
| Final open-question decisions | Do not add `docs/guides.md` in the first slice; use fenced YAML plus Markdown projections when drift validation is in scope; edit stage skills only for direct contradictions; split skill validation from cross-guide validation; do not migrate historical inconsistencies. |
| Spec | Requirements R1-R52 define guide ownership, source-rank, plan-location boundaries, validation ownership, baseline drift, generated-output boundaries, behavior-preservation proof, and cold-read proof. |
| Architecture | No architecture artifact was required; spec review and plan review recorded that this preserves existing guide, skill-wording, validation-ownership, and proof boundaries. |
| Plan | M1 guide surfaces, M2 cross-guide validation, M3 proof/closeout. |
| Review finding | `GUIDE-CR1` required the guide validator to stop owning a partial duplicate workflow-map registry contract. |

## Requirement Mapping

| Requirement range | Implemented by |
| --- | --- |
| R1-R5 | README guide index and landing-guide preservation. |
| R6-R15 | Workflow guide ownership/source-rank wording and workflow-map registry boundary preservation. |
| R16-R24 | Project-map boundary wording and plan-index/plan-body separation. |
| R25-R31 | Learn-session non-authority wording and stage-skill no-bulk-edit boundary. |
| R32-R42 | `scripts/validate-guide-system.py`, selector routing, guide-system regression tests, and `GUIDE-CR1` delegation to `validate_workflow_artifact_map_contract`. |
| R43-R49 | Behavior-preservation proof, no generated adapter edits, no schema/stage-order changes, and no historical migration. |
| R50-R52 | `behavior-preservation.md`, `guide-cold-read.md`, registered proof evidence, and selected guide validation. |

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `README.md` | Added `Where to go next` guide index. | Make README a landing guide that routes readers without duplicating workflow contracts. | R2-R5, GST-001 | `validate-guide-system.py`, selected CI `readme.validate`, `readme.vision_markers`, `guide_system.validate` |
| `docs/workflows.md` | Added guide ownership/source-rank wording, learn-session non-authority, and clearer stage-skill/content boundary. | Make this file the project-local workflow and artifact-location guide while preserving workflow-map registry ownership. | R8-R15, R25-R29, GST-002, GST-005 | `validate-guide-system.py`, workflow-map validator composition, selected CI |
| `docs/project-map.md` | Clarified that project-map does not own workflow stage order, exact lifecycle artifact placement, or current milestone state. | Keep project-map as repository orientation, not hidden workflow policy. | R16-R18, GST-003 | `validate-guide-system.py` project-map checks |
| `docs/plan.md` | Updated active index entry and kept it bounded. | Keep live work state in a compact index while detailed plan state remains in `docs/plans/`. | R19-R24, GST-004 | `validate-guide-system.py`, artifact lifecycle validation |
| `docs/proposals/...md` | Recorded the accepted proposal and proposal-review revisions. | Preserve decision history and source-of-truth alignment before spec. | Proposal stage, proposal-review findings | Proposal-review record and lifecycle validation |
| `specs/guide-system-source-of-truth-alignment.md` | Added approved contract requirements for guide ownership, validation ownership, baseline drift, and proof. | Make the guide-system behavior reviewable and testable. | R1-R52 | Spec-review R1/R2 |
| `specs/guide-system-source-of-truth-alignment.test.md` | Added GST-001 through GST-013. | Map each requirement and edge case to concrete tests or manual proof. | Test-spec stage | Approved test spec and selected CI |
| `scripts/validate-guide-system.py` | Added dedicated cross-guide validation. | Detect guide/source-of-truth drift without expanding `validate-skills.py`. | R32-R42, GST-007, GST-008 | `python scripts/test-guide-system-validator.py`, `python scripts/validate-guide-system.py` |
| `scripts/test-guide-system-validator.py` | Added fixture tests for README links, workflow guide sections, project-map scope, plan-index boundary, learn-session authority, stage-skill plan defaults, duplicate registry placement, and workflow-map delegation. | Prove deterministic guide checks and `GUIDE-CR1` regression coverage. | GST-001-GST-008 | 10 passing tests after `GUIDE-CR1` resolution |
| `scripts/validation_selection.py` | Routed guide surfaces to guide-system validation and registered `guide-cold-read.md` as deterministic change-local evidence. | Ensure changed guide/proof paths get selected validation and do not create evidence-registration debt. | R48, R52, GST-007, GST-013 | `python scripts/test-select-validation.py`, selected CI |
| `scripts/test-select-validation.py` | Added selector expectations for guide validation and `guide-cold-read.md` evidence routing. | Prove selected validation includes the right owners for changed guide and proof paths. | GST-007, GST-013 | 99 passing selector tests |
| `behavior-preservation.md` | Added preservation matrix. | Prove README, `VISION.md`, `CONSTITUTION.md`, workflows, project-map, plan index, stage skills, learn sessions, generated adapters, baseline drift, migration, schema, validation, and security boundaries are preserved. | R43-R50, GST-009-GST-011 | Manual proof plus lifecycle/metadata validation |
| `guide-cold-read.md` | Added cold-read Q&A from current guide surfaces. | Prove a new contributor can answer guide-routing questions without chat history or learn-session archaeology. | R11, R50-R51, GST-012 | Manual proof plus registered evidence validation |
| `review-log.md`, `review-resolution.md`, `reviews/*` | Recorded proposal/spec/plan/code reviews and resolved `GUIDE-CR1`. | Preserve formal review evidence and material finding closeout. | Review rules, `GUIDE-CR1` | `validate-review-artifacts.py --mode closeout` |
| `change.yaml` | Recorded artifacts, requirements, tests, validation ledger, and changed files. | Keep compact change metadata and validation evidence. | Change metadata contract | `validate-change-metadata.py` |
| `docs/plans/...md` | Recorded plan state, milestones, validation notes, and handoffs. | Keep the active plan as current workflow state owner. | Plan milestone contract | artifact lifecycle validation |

## Tests Added Or Changed

| Test/proof | What it proves | Why this level is appropriate |
| --- | --- | --- |
| `scripts/test-guide-system-validator.py` | Guide validation catches missing README guide links, missing workflow guide sections, project-map policy ownership, plan-index bloat, learn-only live authority, stage-skill path contradiction, duplicate artifact registry placement, and workflow-map-owned registry/table mismatch. | Unit/fixture tests are the right level for deterministic static validation. |
| `scripts/test-select-validation.py` | Changed guide surfaces select `guide_system.validate`; guide validator changes select regressions; `guide-cold-read.md` is registered change evidence rather than manual routing debt. | Selector routing is a deterministic path-classification behavior. |
| `behavior-preservation.md` | Required preservation matrix for guide surfaces, generated-output boundaries, migration boundaries, lifecycle order, schemas, validation semantics, and security/privacy posture. | Manual proof is appropriate for semantic no-duplication and no-migration claims. |
| `guide-cold-read.md` | Required cold-read Q&A from current guide surfaces only. | Manual proof is appropriate for contributor navigation and no chat-history reliance. |

## Validation Evidence Before Final Verify

Validation evidence is recorded in `change.yaml` and the active plan. Key commands run include:

- `python scripts/test-guide-system-validator.py`
- `python scripts/validate-guide-system.py`
- `python scripts/test-select-validation.py`
- `python scripts/test-skill-validator.py -k workflow`
- `python scripts/test-skill-validator.py`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `bash scripts/ci.sh --mode explicit ...`
- `git diff --check -- ...`

Hosted CI has not been claimed here. Final verification has not run yet.

## Review Resolution Summary

Material findings: 1 total.

| Finding | Disposition | Status | Summary |
| --- | --- | --- | --- |
| `GUIDE-CR1` | accepted | resolved | Refactored guide-system validation so `GUIDE-008` composes `skill_validation.validate_workflow_artifact_map_contract` instead of duplicating workflow-map registry/table semantics. |

Review-resolution closeout is closed in `review-resolution.md`, and `review-log.md` lists no open findings. M1, M2, and M3 code reviews are clean after the `GUIDE-CR1` rerun.

## Alternatives Rejected

| Alternative | Why rejected |
| --- | --- |
| Add `docs/guides.md` in the first slice. | It would add another guide surface before ownership stabilized. README plus `docs/workflows.md` is enough for first-slice routing. |
| Make README the workflow manual. | That would duplicate contracts and make README another source of truth. |
| Put cross-guide checks in `validate-skills.py`. | That would over-expand the skill validator beyond skill-file checks. |
| Let guide-system validation own workflow-map registry semantics. | Rejected by `GUIDE-CR1`; exact registry/table consistency remains owned by workflow-map validation. |
| Migrate historical artifacts. | Historical migration is out of scope and requires a separate approved proposal or plan. |
| Run adapter packaging checks for this slice. | No canonical `skills/` files or generated adapter output changed, so adapter packaging proof was not triggered. |

## Scope Control

Preserved non-goals:

- no lifecycle stage-order change;
- no artifact schema change;
- no canonical plan-body path change away from `docs/plans/YYYY-MM-DD-slug.md`;
- no broad lifecycle skill style rewrite;
- no historical artifact migration;
- no `docs/guides.md` in the first slice;
- no generated adapter hand edits;
- no PR, branch, hosted CI, release, or final verify readiness claim.

## Risks And Follow-Ups

| Risk | Current mitigation |
| --- | --- |
| Guide prose can still drift over time. | `validate-guide-system.py`, selector routing, workflow-map validator composition, and registered evidence classes catch the targeted drift cases. |
| Future guide evidence paths could create manual-routing debt. | Selector now registers `guide-cold-read.md`; unknown deterministic evidence remains blocking until registered or explicitly deferred. |
| The project map can become stale because it is a living reference. | `docs/project-map.md` states refresh/bypass conditions; guide validation checks its scope boundary. |
| Final workflow completion is not done yet. | Active plan now hands off to `verify`; PR handoff remains downstream. |

## Current Handoff

The active plan records M1, M2, and M3 as closed after clean code review. This explain-change artifact is now updated for final verification. Next stage: `verify`.
