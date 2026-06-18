# Explain Change: Workflow Skill Artifact-Location Map

## Status

- Change ID: `2026-06-17-workflow-skill-artifact-location-map`
- Evidence state: active
- Scope: rationale for the implemented workflow artifact-location map change after M3 code-review.
- Current handoff: `verify` is the next owning stage; this explanation does not claim final verification, branch readiness, or PR readiness.

## Summary

This change makes workflow-managed artifact placement deterministic. It turns `docs/workflows.md` into the project-local artifact-location map, keeps artifact content ownership with the stage skills, preserves detailed plan bodies under `docs/plans/YYYY-MM-DD-slug.md`, and adds validation so drift between the workflow map, workflow skill defaults, affected stage skills, and packaged adapter output is caught.

The implementation keeps the repository-standard split:

- `docs/plan.md` is the bounded lifecycle index.
- `docs/plans/YYYY-MM-DD-slug.md` contains concrete plan bodies.
- `docs/changes/<change-id>/` contains formal lifecycle evidence such as reviews, review resolution, explain-change, verification evidence, and PR handoff evidence.

## Problem

Maintainers were still asking where common workflow artifacts belong. Two placement questions exposed the issue:

- plan placement was easy to confuse between `docs/plan.md`, `docs/plan/`, `docs/plans/`, and change-local paths;
- proposal/spec review placement needed a deterministic change-local answer under `docs/changes/<change-id>/reviews/`.

The old workflow guide and workflow skill were directionally correct but not deterministic enough to prevent drift between project-local guidance, skill defaults, stage-skill wording, learn-session conclusions, and generated adapter behavior.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Use dual-layer placement: `docs/workflows.md` is the project-local map; stage skills keep portable defaults and artifact-content ownership. |
| Owner correction | Preserve this repository's best practice: detailed workflow-managed plan bodies stay under `docs/plans/YYYY-MM-DD-slug.md`. |
| Spec requirements | R1-R15 require workflow-map generation, a canonical YAML registry, synchronized Markdown projections, and required artifact entries. |
| Spec requirements | R16-R20 preserve `docs/plan.md` as the index and `docs/plans/YYYY-MM-DD-slug.md` as the plan-body path. |
| Spec requirements | R21-R25 align workflow defaults and only directly contradictory stage-skill placement text. |
| Spec requirements | R26-R47 define source rank, formal review placement, learn-session non-authority, and validation/drift behavior. |
| Spec requirements | R48-R53 require adapter proof, cold-read proof, lifecycle/schema preservation, generated-output boundaries, and customer-project portability. |
| Architecture | No architecture artifact was required; the approved plan classifies the change as workflow governance, skill text, and validation behavior rather than runtime architecture. |
| Plan milestones | M1 updated the map and skill contract, M2 added validators and regressions, and M3 recorded adapter proof, cold-read proof, behavior preservation, and explanation evidence. |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `docs/workflows.md` | Added the canonical `artifact_locations` YAML registry, Markdown projection tables, review-placement table, plan surfaces, customization notes, and unknown-artifact blocker language. | Provide a deterministic project-local artifact-location map that humans can read and validators can check. | R6-R15, R16-R20, R35-R39, R47. | M1 tests and M2 registry/table validation. |
| `skills/workflow/SKILL.md` | Updated workflow-map ownership, source-rank fallback, unknown-artifact blocking, formal change-pack evidence boundaries, and default paths. | Make the workflow skill create/refresh the map while preserving stage-skill content ownership and portable defaults. | R1-R5, R21, R26-R34, R53. | `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`. |
| `skills/plan/SKILL.md` | Added the project-local workflow-map lookup wording without changing the plan-body path contract. | Align directly affected stage-skill placement behavior without bulk style edits. | R22-R25. | M2 stage-skill contradiction checks. |
| `scripts/skill_validation.py` | Added workflow artifact-map parsing and drift checks for required registry entries, placement fields, registry/table agreement, plan path drift, review path drift, unknown artifact inputs, workflow default drift, and affected stage-skill contradictions. | Make placement drift fail deterministically instead of relying on prose review. | R42-R47, AC11-AC16, AC19-AC20. | M2 skill-validator regressions. |
| `scripts/test-skill-validator.py` | Added M1 and M2 regression coverage, including the WFO-CR1 regression requiring `architecture_record` and `adr`. | Prove the validator catches the named drift and missing-entry cases. | Test spec T3-T13, T15; WFO-CR1. | `python scripts/test-skill-validator.py` passed with 200 tests after M2/WFO-CR1. |
| `docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md` | Recorded the accepted direction, the owner-corrected plan-location decision, map representation, stage-skill edit policy, and acceptance criteria. | Preserve the decision record for why the implementation uses `docs/plans/` and dual-layer placement. | Proposal-review R1/R2. | Proposal-review records and review-resolution entries. |
| `specs/workflow-skill-artifact-location-map.md` | Added the approved contract requirements, examples, edge cases, compatibility constraints, and acceptance criteria. | Make the workflow-map behavior testable and authoritative before implementation. | Spec-review R1/R2. | Spec-review records and lifecycle validation. |
| `specs/workflow-skill-artifact-location-map.test.md` | Mapped requirements to targeted tests, selected CI, manual cold-read proof, and adapter proof. | Ensure every MUST has concrete proof before implementation and final review. | Test-spec approval. | Owner-approved test spec and M3 proof. |
| `docs/plans/2026-06-18-workflow-skill-artifact-location-map.md` and `docs/plan.md` | Added the living execution plan, kept the plan index link relative/clickable, and tracked M1-M3 state through final closeout handoff. | Keep active lifecycle state in the plan surfaces this repository uses. | Plan-review R1 and AGENTS plan policy. | Lifecycle and selected CI validation. |
| `docs/changes/2026-06-17-workflow-skill-artifact-location-map/*` | Added compact change metadata, review records, review log, review resolution, behavior-preservation proof, and this explanation. | Provide change-local traceability for formal reviews, findings, validation, cold-read proof, and final rationale. | Workflow contract and M3. | Review artifact validation and change metadata validation. |
| `specs/skill-contract.md` and `specs/skill-contract.test.md` | Included the new workflow-map contract surfaces in the skill-contract trace where needed. | Keep skill contract references synchronized with the workflow-map optimization. | Existing skill-contract governance. | Selected lifecycle and skill validation. |

## Tests Added Or Changed

| Test surface | What it proves | Why this level is appropriate |
| --- | --- | --- |
| `test_workflow_map_m1_*` fixtures in `scripts/test-skill-validator.py` | The workflow guide and workflow skill expose the expected registry/default path contract, including `docs/plans/YYYY-MM-DD-slug.md`. | Static skill/docs validation is enough for user-facing placement text. |
| `test_workflow_map_m2_*` fixtures in `scripts/test-skill-validator.py` | Registry shape, missing fields, duplicate keys, ambiguous placement, table/path drift, stale change-pack plan paths, review-path drift, unknown artifact inputs, and stage-skill contradictions fail deterministically. | The behavior is parser/validator behavior, so unit-style regression fixtures are the direct proof. |
| `test_workflow_map_m2_validator_requires_architecture_registry_entries` | Removing `architecture_record` or `adr` from the registry fails with the missing artifact key named. | This directly covers the code-review finding WFO-CR1. |
| Manual cold-read proof in `behavior-preservation.md` | A maintainer can answer where proposal-review records go, where detailed workflow plans go, and what `docs/plan.md` is for without chat history. | The test spec allows manual proof because this is human-facing documentation behavior. |
| Adapter proof commands | Generated public adapter packaging is current when the packaged workflow skill changes. | Repository-owned generation/check commands are the authoritative proof for generated-output boundaries. |

## Validation Evidence Before Final Verify

Available validation evidence is recorded in `change.yaml` and the active plan. Key completed checks include:

- `python scripts/test-skill-validator.py -k workflow_map_m1`
- `python scripts/test-skill-validator.py -k workflow_map_m2`
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-build-skills.py`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `bash scripts/ci.sh --mode explicit ...`
- `git diff --check --`

Two useful failures were corrected and kept in the validation ledger:

- the initial M3 metadata shape used unsupported custom artifact keys for behavior-preservation and cold-read proof, so the proof was kept as registered change evidence and `explain_change` remained the only new metadata artifact key;
- a separate `cold-read-proof.md` path triggered selector evidence-registration debt, so the cold-read proof was consolidated into `behavior-preservation.md`, the location named by the test spec.

## Review Resolution Summary

`review-resolution.md` is closed. It records:

- proposal-review R1: 3 material findings, all accepted and resolved;
- spec-review R1: 3 material findings, all accepted and resolved;
- code-review M2 R1: 1 material finding, accepted and resolved;
- proposal-review R2, spec-review R2, plan-review R1, code-review M1 R1, code-review M2 R2, and code-review M3 R1: no material findings.

See `docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md` for dispositions. `review-log.md` lists no open findings.

## Alternatives Rejected

| Alternative | Why rejected |
| --- | --- |
| Keep workflow guidance narrative-only. | It would not make artifact placement deterministic or validator-checkable. |
| Make `docs/workflows.md` the only placement source. | It would break skill-only adopters and remove portable defaults. |
| Put all placement rules only in stage skills. | It would make project-local customization and cross-skill drift validation difficult. |
| Move detailed workflow plans into `docs/changes/<change-id>/plan.md`. | The owner corrected the direction and required this repository's best practice: concrete plan bodies under `docs/plans/YYYY-MM-DD-slug.md`. |
| Migrate historical `docs/plans/*.md` files. | Migration was a non-goal; this change defines and validates forward behavior. |
| Hand-edit generated public adapter output. | Generated-output boundaries require repository-owned build/check scripts instead. |

## Scope Control

The change intentionally does not:

- change lifecycle stage order;
- redefine proposal, spec, plan, review, verify, PR, or learn schemas;
- move historical plan files;
- introduce a new CLI scaffold;
- remove stage-skill portable defaults;
- make learn sessions live routing authority;
- claim final verification, branch readiness, PR-body readiness, or PR-open readiness.

## Risks And Follow-Ups

- Final verify still needs to rerun the owning readiness checks after this explanation update.
- The current implementation validates stable registry and table structure; future artifact classes should be added through the same registry/table/test path.
- Adapter archives were proven through repository-owned scripts, but release publication still belongs to the PR/release workflow.

## Readiness Statement

All implementation milestones are closed, review-resolution is closed, and this explanation is current after code-review M3 R1. The next owning stage is `verify`; final verification, branch readiness, and PR readiness are not claimed here.
