# Repository tooling organization

## Purpose / big picture

Make repository tooling ownership visible by separating stable commands, internal implementation and authored resources, preserving existing behavior and protective tests.

## Current Handoff Summary

- Owning change record: none selected; scoped portable work authorized by the user on `refactor/validation-organization`.
- Evidence: the existing [refinement record](../changes/2026-09-14-design-suitability-review/contract-refinement.md) and its independent reviews. No historical lifecycle state is advanced.

## Source artifacts

- Proposal: no separate artifact; the user selected and authorized this bounded maintenance direction.
- Design: [Engineering ENG-SR-16](../design/engineering/engineering.md#repository-tooling-organization), [System](../design/system.md), [Validation](../design/engineering/validation.md), [Packaging](../design/engineering/packaging.md), [Release](../design/engineering/release/release.md), exact subjects in [Design Review](../changes/2026-09-14-design-suitability-review/reviews/tooling-organization-design-review.md).
- Prior-contract test spec: none additionally selected; existing owner requirements and test protections apply.

## Context and orientation

The scripts root mixes supported commands, internal Python/Node modules and three authored resource files. Python tests add scripts to their import path; subprocess bootstrap strings import internal modules, synthetic selector workspaces copy specific modules, and release fixtures copy the scripts tree. Release currently hashes top-level Python/shell code; relocation must extend this guard to nested maintained inputs. The branch already contains uncommitted changes, including completed test relocation; preserve that baseline.

### Concrete move map

Every source starts directly under scripts unless shown otherwise. Keep filenames. New Python packages have explicit initializers and qualified imports from the scripts root.

| Sources | Destination | Disposition |
| --- | --- | --- |
| boundary_first_reference.py, boundary_first_validation.py, model_layout.py, project_yaml.py, record_store_classification.py, skill_validation.py, validation_execution.py, validation_selection.py | scripts/lib/validation/ | Internal implementation; update imports and actual workers. Retain uncertain project_yaml helper without deleting its behavior. |
| validation_node_adapter.mjs, record_snapshot_git.mjs | scripts/lib/validation/ | Internal Node helpers; update launcher/import resolution. |
| adapter_distribution.py, npm_package_validation.py | scripts/lib/packaging/ | Packaging implementation; retain executable build/validate commands. |
| release_candidate.py, release_coordination.py, release_execution.py, release_provider.py, release_transaction.py, release_evidence.py | scripts/lib/release/ | Release implementation; retain a thin scripts/release_evidence.py command for its existing public invocation. |
| scripts/adapter_templates/claude/CLAUDE.md, scripts/adapter_templates/codex/AGENTS.md | scripts/resources/adapter-templates/ | Preserve authored bytes and reader semantics. |
| scripts/boundary-first-resources.yaml | scripts/resources/boundary-first/boundary-first-resources.yaml | Preserve closed manifest bytes and canonical source ownership. |

Entrypoints include ci.sh, select-validation.py, validate-* commands, build-* commands, record classification, release dispatch/preparation/closeout and boundary projection. They retain their paths and supported arguments. Existing large command implementations need no unrelated extraction. No blanket alias imports, duplicated implementation, new runner or dependency is selected.

## Non-goals

No test deletion, package layout change, public skill edit, runtime product change, release publication, universal CLI, new submodel, broad source cleanup or unrelated plan settlement. Current historical evidence retains its original paths and meaning. No commit or external handoff is selected.

## Requirements covered

| Requirement or obligation | Allocation |
| --- | --- |
| ENG-SR-16; System layout | M1 and TG-1: commands/imports/resources follow their owners without behavior loss. |
| TEST-SR-04/05/08/10/12/15–17; VAL-SR-01/03/04/05/17/21/22/27/28 | M1 and TG-1: complete discovery, exact selection, reruns, isolation and failure handling remain protected. |
| DIST-SR-03/04/05/06/18/23/24 | M1 and TG-2: unchanged authored inputs, real archive/package/installed consumer behavior. |
| REL-SR-09 and Release loaded/source integrity obligations | M1 and TG-2: stable commands, coherent prepared source and detection of changed nested implementation/resources. |

Engineering Composition/path, Compatibility/migration and External/environment scenarios apply directly. Other applicable owner scenarios retain existing failure, concurrency, cleanup and authority proof; no new external permission or lifecycle transition is introduced.

## Milestones

### M1. Move internal tooling and resources with every active consumer

- Milestone kind: implementation.
- Engineering purpose: one coherent migration of the mutually dependent import graph, resource readers, copied source fixtures and identity boundary; do not expose an intermediate tree where moved production code escapes the loaded/source guard.
- Requirements: all rows above.
- Architecture responsibility: Engineering placement and the existing Validation, Packaging and Release responsibilities.
- Dependencies: exact Design Review and independent Delivery Review of this plan.
- Implementation scope: the concrete move map, Python package initializers, imports and mock targets, worker bootstrap/module resolution, Node helper imports, root/resource resolution, exact changed-path routing, recursive source identity, direct and copied-repository consumers, current contributor/navigation references.
- Files/components likely touched: scripts, existing tests, directly affected package test callers if found, CONTRIBUTING and current project-map tooling detail. Do not edit generated adapters or published skills.
- Required verification: TG-1 — capture normal-loader case IDs, establish old/new path-routing regression and nested identity counterexamples before implementation, then demonstrate direct and isolated workers, command compatibility and complete discovery. TG-2 — real resource generation, package validation and prepared-candidate integration.
- Evidence expectations: retain baseline-relative move/consumer map, exact changed subjects, unchanged resource bytes, original/current case IDs, actual commands/results and resolved findings in the existing refinement record.
- Implementation steps: capture recoverable source/index baseline; add meaningful routing/identity proof; move code/resources; reconcile qualified imports, roots, subprocess strings and owned temporary copies; expand maintained-source identity; inspect every current caller; execute targeted proof; update current navigation; complete required combined scope.
- Validation commands: `python tests/engineering/validation/test-select-validation.py`; `python tests/engineering/validation/test-validation-execution.py`; `python tests/engineering/packaging/test-adapter-distribution.py`; `python tests/engineering/packaging/test-npm-package-publication.py`; `python tests/engineering/release/test-release-transaction.py`; `bash scripts/ci.sh --mode local --broad-smoke --jobs 4`; `git diff --check`. A complete selected execution may supply required suite proof without redundant direct repetition. Start with focused methods before full selection.
- Expected observable result: all baseline cases remain discoverable and execute; old/new changed paths select equivalent checks; actual stable commands resolve qualified modules and resources; changed nested production input changes source identity and triggers existing candidate mismatch rejection; bytecode alone does not change maintained-source identity.
- Completion criteria: every mapped source/resource has one current owner and working consumers, command paths remain supported, existing assertions remain meaningful, no silently unclassified input or skipped case appears, and required integration proof completes.
- Required evidence: TG-1/TG-2 and final selection/discovery/consumer results with applicability limits.
- Review handoff: independent complete M1 Code Review, including CI-maintenance impact on command selection and subprocess execution.
- Risks: synthetic source copies, mock targets, same-directory readers and recursive source identities can hide omissions or unexpected environment dependence.
- Rollback/recovery: restore the entire captured tooling/test/caller slice coherently from the pre-migration working-tree snapshot and its index backup, preserving prior changes. Do not reset the branch, suppress failures or weaken timeouts.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: M1 and all required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered migration and its interactions; milestone review informs but does not substitute.
- Evidence: exact final subjects, independent basis and explicit concern dispositions.
- Successor: separate scoped Verify. No whole-branch or governed completion is inferred.

## Change-level verification

### TG-2. Real command-to-candidate compatibility

- Covers: ENG-SR-16, DIST-SR-03/04/18/23/24, REL-SR-09 and M1's shared import/resource/source-integrity boundaries.
- Demonstrate: package commands find the same maintained resources; real archives and installed npm consumers preserve content and behavior; candidate preparation consumes coherent relocated source and rejects changed nested code/resources without publication.
- Evidence expectations: actual existing adapter/package suites and real candidate integration, plus focused identity regression covering nested files, runtime bytecode exclusion and existing mismatch guard. Preserve loaded-script identity before/after checks; no cached success substitutes.
- Non-applicability: hosted CI, public release, installed agent semantic certification and unrelated branch changes are outside this local migration.

## Validation plan

Use normal-loader discovery before/after all 14 entrypoints; collection is inventory, not passing execution. Preserve stable case IDs and enumerate only intentional additions. Verify unchanged resource bytes and active reader paths. Inspect selector results for actual new paths and old deletions; unknown tooling paths must still fail closed. Run meaningful focused proof, then required local/broad execution. Reuse unaffected actual passes only with explicit subject/environment applicability; any relevant correction receives fresh proof. Check updated current documentation structure/prose and diff whitespace.

## Risks and recovery

The migration touches a shared implementation graph rather than independent public interfaces, so splitting it into arbitrary directory milestones could produce a misleading partial source identity. Keep changes reviewable through the exact move map, baseline-relative diff and targeted proof. Missing imports/resources, altered case population or changed production semantics blocks completion; correct or restore the coherent slice rather than introducing compatibility re-export files.

## Dependencies

Design Review precedes plan reliance; Delivery Review precedes implementation. Independent milestone review precedes fresh whole-change review and distinct scoped Verify. Earlier test-migration reviews retain their historical subjects; this work requires its own assessment.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-14 | One integrated source/resource migration with stable commands | Shared imports, candidate copies and loaded-source identity must remain coherent. | Arbitrary directory milestones that temporarily omit moved code from integrity checks. |
| 2026-09-14 | Explicit packages and a single retained dual-use command wrapper | Ownership becomes visible without breaking supported command callers. | Wildcard legacy aliases and a new universal CLI. |

## Readiness

This document is stable execution intent. Actual assessments, corrections and validation belong in the referenced evidence; this plan does not grant approval or lifecycle state.
