# Guide System Source-of-Truth Alignment Test Spec

## Status

active

Approval: approved by maintainer on 2026-06-18 for implementation.

## Related spec and plan

- Spec: [Guide System Source-of-Truth Alignment](guide-system-source-of-truth-alignment.md), approved.
- Plan: [Guide System Source-of-Truth Alignment Plan](../docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md), active.
- Proposal: [RigorLoop Guide System Optimization and Source-of-Truth Alignment](../docs/proposals/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment.md), accepted.
- Spec reviews: [spec-review-r1](../docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/spec-review-r1.md), [spec-review-r2](../docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/spec-review-r2.md).
- Plan review: [plan-review-r1](../docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/plan-review-r1.md).
- Architecture/ADRs: not applicable. Spec review and plan review record that this preserves existing guide, skill-wording, validation ownership, and proof boundaries.

## Testing strategy

This change is verified with repository-owned static validation, validator fixture tests, selected CI, and manual proof artifacts.

- Unit tests cover parser helpers, guide-check diagnostics, selector registration, and fixture-level rejection cases.
- Integration tests run the guide-system validator or artifact-lifecycle guide-system mode against real guide surfaces and representative fixtures.
- End-to-end checks are limited to selected explicit-path CI because no runtime application flow changes.
- Smoke checks run the selected CI wrapper over touched guides, validator scripts, canonical skills, test specs, plan surfaces, and change-local evidence.
- Manual checks cover behavior-preservation proof, cold-read proof, and semantic no-duplication judgments that should not become broad natural-language scoring.
- Contract checks prove README, workflow guide, project map, plan index, learn-session authority, stage-skill portability, validation ownership, and workflow-map ownership boundaries.
- Migration checks prove historical artifacts are not moved in this slice and baseline drift is recorded rather than silently migrated.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | GST-001, GST-002 | contract | Guide classes and ownership matrix classify all major surfaces. |
| R2 | GST-001 | contract | README remains a landing guide. |
| R3 | GST-001 | integration | README guide index is present. |
| R4 | GST-001 | integration | README links to primary guides when present. |
| R5 | GST-001 | manual, contract | README does not duplicate full contracts. |
| R6 | GST-011 | manual | Vision preservation proof. |
| R7 | GST-011 | manual | Constitution preservation proof. |
| R8 | GST-002 | integration | Workflow guide identifies itself as workflow guide and artifact-location map. |
| R9 | GST-002 | integration | Workflow guide includes guide ownership or source-rank guidance. |
| R10 | GST-002 | integration | Workflow guide includes guide ownership matrix or equivalent. |
| R11 | GST-002, GST-012 | integration, manual | Ownership matrix answers common guide-routing questions. |
| R12 | GST-002, GST-006 | integration | Workflow guide distinguishes guide ownership from stage-skill content ownership. |
| R13 | GST-002, GST-008 | contract | Workflow-map spec remains exact registry owner. |
| R14 | GST-002, GST-008 | integration | Machine-checkable registry and Markdown projections are validated when drift validation is in scope. |
| R15 | GST-002, GST-008 | contract | No second canonical registry is introduced. |
| R16 | GST-003 | contract | Project map remains repository orientation. |
| R17 | GST-003 | integration | Project map does not own stage order, placement, or current milestone state. |
| R18 | GST-003 | manual | Project map content remains orientation-focused when current. |
| R19 | GST-004 | integration | Plan index remains bounded live-work index. |
| R20 | GST-004 | integration | Plan index does not contain long-form plan material. |
| R21 | GST-004 | contract | Plan-body placement aligns with workflow-map contract. |
| R22 | GST-004 | integration | No competing canonical plan locations. |
| R23 | GST-004 | integration | Current workflow-map contract uses `docs/plans/YYYY-MM-DD-slug.md`. |
| R24 | GST-004 | integration | `docs/plan.md` remains index only. |
| R25 | GST-005 | integration | Learn sessions are not live routing authority. |
| R26 | GST-005 | integration, manual | Learn-derived routing rules must be promoted to live surfaces before reliance. |
| R27 | GST-006 | manual, integration | Stage skills remain self-contained enough for skill-only adopters. |
| R28 | GST-006 | integration | Stage skills retain portable defaults. |
| R29 | GST-006 | integration | Stage skills use project-local guidance, portable defaults, and block-on-ambiguity behavior. |
| R30 | GST-006 | manual | First-slice skill edits are limited to direct contradictions. |
| R31 | GST-006 | manual | No broad style or symmetry rewrite of lifecycle skills. |
| R32 | GST-007 | integration | Cross-guide validation lives in a guide validator or artifact-lifecycle guide mode. |
| R33 | GST-007 | integration | `validate-skills.py` remains skill-file scoped. |
| R34 | GST-007 | integration | Non-skill guide checks do not move into `validate-skills.py`. |
| R35 | GST-001, GST-007 | integration | README required guide links are checked. |
| R36 | GST-002, GST-007 | integration | Workflow guide ownership and artifact-location sections are checked. |
| R37 | GST-002, GST-007 | integration | Workflow guide ownership/content ownership distinction is checked. |
| R38 | GST-003, GST-007 | integration | Project-map stage-order ownership rejection is checked. |
| R39 | GST-004, GST-007 | integration | Plan-index bounded shape is checked. |
| R40 | GST-005, GST-007 | integration | Learn-only live authority is checked. |
| R41 | GST-006, GST-007 | integration | Directly affected stage-skill placement contradictions are checked. |
| R42 | GST-002, GST-008 | integration | Workflow-map registry/table validation remains canonical. |
| R43 | GST-009 | integration | Generated adapter packaging proof runs when canonical skill changes require it. |
| R44 | GST-010 | migration, manual | Baseline drift is recorded, not automatically migrated. |
| R45 | GST-010 | migration, manual | Historical migration requires separate approval. |
| R46 | GST-010 | contract | Lifecycle stage order is preserved. |
| R47 | GST-010 | contract | Artifact schemas are preserved. |
| R48 | GST-008, GST-010 | integration | Validation command semantics and selected-check behavior are preserved except through approved validator contracts. |
| R49 | GST-009, GST-010 | integration | Generated public adapter output is not hand-edited. |
| R50 | GST-011 | manual | Behavior-preservation proof is required. |
| R51 | GST-012 | manual | Cold-read proof is required. |
| R52 | GST-013 | integration, manual | Stale touched, referenced, generated, or authoritative guide artifacts block later validation when contradictory. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | GST-001, GST-012 | README points users to `docs/workflows.md` without duplicating the full contract. |
| E2 | GST-002, GST-012 | Workflow ownership matrix identifies `docs/plan.md` as live work index. |
| E3 | GST-003 | Project map remains orientation, not policy. |
| E4 | GST-004 | Plan index remains bounded and links to canonical plan bodies. |
| E5 | GST-005 | Learn-derived routing rules are promoted before reliance. |
| E6 | GST-006 | Customer projects without `docs/workflows.md` use portable defaults and block on ambiguity. |
| E7 | GST-007, GST-013 | Stale or missing guide links fail validation. |
| E8 | GST-010 | Historical placement drift is not automatically migrated. |

## Edge case coverage

| Edge case | Covered by |
| --- | --- |
| EC1 missing guide surface | GST-001, GST-013 |
| EC2 stale guide link | GST-001, GST-007, GST-013 |
| EC3 guide ownership conflict | GST-002, GST-007, GST-013 |
| EC4 workflow-map conflict | GST-002, GST-004, GST-008 |
| EC5 stage-skill conflict | GST-006, GST-007 |
| EC6 learn-only rule | GST-005, GST-007 |
| EC7 historical artifact drift | GST-010 |
| EC8 validator overreach | GST-008 |

## Test cases

### GST-001. README remains a compact landing guide

- Covers: R1-R5, R35, E1, EC1, EC2
- Level: integration
- Fixture/setup: `README.md`, required guide files, guide-system validator fixtures for valid, missing-link, and duplicate-contract cases.
- Steps:
  - Add or update guide validation that parses README guide links.
  - Assert README links to `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, and stage-skill usage guidance when those surfaces exist.
  - Assert missing optional guide links are not required when the guide surface is absent.
  - Assert README does not contain full workflow stage tables, full artifact schemas, or full stage-skill operating instructions.
  - Run selected CI against README and the guide-system validator.
- Expected result: README gives first-contact navigation without becoming a workflow manual.
- Failure proves: README is either insufficient for orientation or has become a duplicate source of truth.
- Automation location: `scripts/validate-guide-system.py` or `scripts/validate-artifact-lifecycle.py --mode guide-system`; selector coverage in `scripts/test-select-validation.py`.

### GST-002. Workflow guide owns guide routing without replacing the workflow-map contract

- Covers: R1, R8-R15, R36, R37, R42, E2, EC3, EC4
- Level: integration
- Fixture/setup: `docs/workflows.md`, `specs/workflow-skill-artifact-location-map.md`, valid and invalid workflow guide fixtures.
- Steps:
  - Assert `docs/workflows.md` identifies itself as the project-local workflow guide and artifact-location map.
  - Assert it includes guide ownership or source-rank guidance plus a guide ownership matrix or equivalent index.
  - Assert the matrix identifies primary guides for project vision, governance, artifact placement, repository structure, active work, one-change evidence, stage execution, and historical rationale.
  - Assert wording distinguishes guide ownership from stage-skill artifact-content ownership.
  - Assert the fenced YAML artifact registry remains in `docs/workflows.md` and Markdown tables do not contradict it when drift validation is in scope.
  - Assert no second canonical artifact-location registry is introduced outside the workflow guide.
- Expected result: `docs/workflows.md` routes users and maps artifacts while the workflow-map spec still owns exact registry semantics.
- Failure proves: guide routing is ambiguous or the guide-system work created a competing registry contract.
- Automation location: guide-system validator or artifact-lifecycle guide mode plus workflow-map registry/table validation.

### GST-003. Project map remains repository orientation

- Covers: R16-R18, R38, E3, EC3
- Level: integration
- Fixture/setup: `docs/project-map.md`, fixtures with valid orientation mentions and invalid workflow-policy ownership.
- Steps:
  - Assert project-map text may mention workflow surfaces for orientation.
  - Assert it does not define lifecycle stage order, exact lifecycle artifact placement, or current milestone state.
  - Assert it remains focused on directories, components, runtime boundaries, generated artifacts, validation surfaces, external boundaries, or orientation risks when those areas are present.
- Expected result: contributors use project-map to understand repository structure, not workflow policy.
- Failure proves: project-map can become a hidden workflow authority.
- Automation location: guide-system validator fixture tests and selected CI for `docs/project-map.md`.

### GST-004. Plan index and plan body placement remain separated

- Covers: R19-R24, R39, E4, EC4, EC5
- Level: integration
- Fixture/setup: `docs/plan.md`, active plan body under `docs/plans/`, workflow-map contract, fixtures for competing plan locations and plan-index bloat.
- Steps:
  - Assert `docs/plan.md` contains bounded active, blocked, superseded, and recent done index content only.
  - Assert detailed milestones and journals live in `docs/plans/YYYY-MM-DD-slug.md` under the current workflow-map contract.
  - Assert `docs/changes/<change-id>/plan.md` is not introduced as a competing canonical plan body path for this role.
  - Assert plan-index validation rejects long review summaries, complete transcripts, or detailed implementation plan bodies in `docs/plan.md`.
- Expected result: users find current work in `docs/plan.md` and detailed execution in the plan body without competing canonical plan locations.
- Failure proves: plan-location confusion or unbounded plan-index growth returned.
- Automation location: guide-system validator or artifact-lifecycle guide mode; `python scripts/test-artifact-lifecycle-validator.py`.

### GST-005. Learn sessions remain historical rationale

- Covers: R25, R26, R40, E5, EC6
- Level: integration
- Fixture/setup: `docs/learn/sessions/` fixtures with historical rationale, learn-only live rule, and promoted live rule.
- Steps:
  - Assert learn sessions may contain historical observations and routing rationale.
  - Assert downstream live routing reliance fails when the rule exists only in learn-session text.
  - Assert the same rule passes when promoted to `docs/workflows.md`, an approved spec, a schema, or owning stage-skill guidance.
  - Assert README, workflow guide, project map, and plan index do not cite learn sessions as live routing authority.
- Expected result: learn sessions explain history but do not become hidden live rules.
- Failure proves: contributors must do learn-session archaeology to route future work.
- Automation location: guide-system validator fixture tests and selected CI for changed learn or guide surfaces.

### GST-006. Stage skills preserve portable defaults and only direct contradictions are edited

- Covers: R12, R27-R31, R41, E6, EC5
- Level: integration
- Fixture/setup: affected `skills/*/SKILL.md`, especially `skills/workflow/SKILL.md` and any stage skill with directly contradictory placement text.
- Steps:
  - Inspect affected stage skills before editing and record whether each is unchanged, directly contradictory, or updated.
  - Assert stage skills remain self-contained enough to operate in a customer project with no `docs/workflows.md`.
  - Assert stage skills use project-local workflow guidance when present, portable defaults where safe, and block on remaining ambiguity.
  - Assert first-slice edits are limited to direct contradictions with the approved workflow guide, source-rank model, or artifact-location registry.
  - Assert no lifecycle skill receives a style-only or symmetry-only rewrite.
- Expected result: stage skills stay portable and aligned without centralizing all placement knowledge into `docs/workflows.md`.
- Failure proves: skill-only adopters regress or the first slice exceeds its approved scope.
- Automation location: `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, guide-system validator affected-skill checks, and manual diff review.

### GST-007. Cross-guide validation is owned by the correct validator

- Covers: R32-R41, R52, E7, EC2, EC3, EC5, EC6
- Level: integration
- Fixture/setup: new guide-system validator or artifact-lifecycle guide-system mode, `scripts/validation_selection.py`, `scripts/test-select-validation.py`, invalid guide fixtures.
- Steps:
  - Implement cross-guide checks in a dedicated guide-system validator or artifact-lifecycle guide-system mode.
  - Assert `validate-skills.py` remains limited to skill-file checks unless a check directly inspects packaged skill content.
  - Assert README links, workflow guide sections, project-map scope, plan-index boundary, learn-session non-authority, and directly affected stage-skill contradictions fail with stable guide check IDs.
  - Assert selected validation routes touched README, workflow guide, project map, plan index, learn, skill, and validator paths to the appropriate checks.
- Expected result: cross-guide drift is deterministic, selected by CI, and not buried inside the skill validator.
- Failure proves: guide drift can escape validation or the skill validator has been over-expanded.
- Automation location: `python scripts/test-select-validation.py`, guide-system validator regression tests, and selected CI.

### GST-008. Validator behavior stays deterministic and does not duplicate workflow-map semantics

- Covers: R13-R15, R42, R48, EC4, EC8
- Level: unit
- Fixture/setup: parser fixtures for headings, links, fenced YAML, Markdown tables, stable text fixtures, and over-broad prose cases.
- Steps:
  - Assert checks use stable structures such as links, headings, fenced YAML, tables, paths, check IDs, and reviewed fixture text.
  - Assert broad natural-language quality scoring is not used.
  - Assert workflow-map registry/table consistency remains owned by the workflow-map validator or composed validator call.
  - Assert command exit behavior, selected-check behavior, and required validation evidence do not change except through approved validator contracts.
- Expected result: guide-system validation is reliable and maintainable.
- Failure proves: the validator became fragile prose scoring or created a second workflow-map contract.
- Automation location: validator unit tests and `python scripts/test-artifact-lifecycle-validator.py` or dedicated `python scripts/test-guide-system-validator.py`.

### GST-009. Canonical skill changes are packaged without hand-editing generated output

- Covers: R43, R49
- Level: integration
- Fixture/setup: canonical skill files under `skills/`, generated local skill output, public adapter release tooling.
- Steps:
  - If canonical skill files change, run `python scripts/build-skills.py --check`.
  - If generated adapter proof is required, run repository-owned adapter validation such as `python scripts/test-build-skills.py` and `python scripts/test-adapter-distribution.py`.
  - Assert generated public adapter output is derived from canonical source and not hand-edited.
  - Assert `.codex/skills/` remains untracked local runtime state.
- Expected result: changed skill guide content is packaged reproducibly when packaging is in scope.
- Failure proves: published skill text can drift from canonical skill source.
- Automation location: `python scripts/build-skills.py --check`, `python scripts/test-build-skills.py`, `python scripts/test-adapter-distribution.py`.

### GST-010. Compatibility, baseline drift, and migration boundaries are preserved

- Covers: R44-R49, E8, EC7
- Level: manual
- Fixture/setup: implementation diff, active plan, change metadata, behavior-preservation proof, historical artifacts that predate the guide system.
- Steps:
  - Assert existing guide inconsistencies are recorded as baseline drift rather than moved automatically.
  - Assert no historical artifacts or guide families are migrated unless separately approved.
  - Assert lifecycle stage order and artifact content schemas are unchanged.
  - Assert validation command semantics and selected-check behavior are unchanged except for the approved guide-system validation contract.
  - Assert generated public adapter output is not hand-edited.
- Expected result: the first slice defines forward guide ownership without hidden migration or compatibility drift.
- Failure proves: guide cleanup silently changed workflow semantics or historical state.
- Automation location: manual review in behavior-preservation proof plus selected CI.

### GST-011. Behavior-preservation proof covers all required surfaces

- Covers: R6, R7, R44-R50
- Level: manual
- Fixture/setup: `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/behavior-preservation.md`.
- Steps:
  - Record a matrix for README, `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, stage skills, and learn sessions.
  - For each surface, name baseline behavior, new proof, preservation result, and any baseline drift or unaffected rationale.
  - Assert the proof links to implementation evidence and validation commands rather than restating intentions only.
- Expected result: reviewers can see that guide-system alignment strengthened orientation without changing prohibited behavior.
- Failure proves: preservation claims are unsupported or rely on chat history.
- Automation location: manual proof artifact plus `python scripts/validate-change-metadata.py` when the proof path is registered.

### GST-012. Cold-read proof answers common guide-routing questions

- Covers: R11, R50, R51, E1-E4
- Level: manual
- Fixture/setup: `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/guide-cold-read.md`.
- Steps:
  - Ask a reviewer to answer the guide-routing questions using only current guide surfaces.
  - Include questions for where to start, proposal placement, formal review placement, `docs/plan.md` purpose, detailed plan location, repository structure, governance, live routing authority, and historical-rationale-only files.
  - Record answers, source file links, and whether the reviewer needed chat history or learn-session archaeology.
- Expected result: a new contributor can find the right guide for common questions without prior conversation context.
- Failure proves: guide-system optimization did not solve the onboarding and routing problem.
- Automation location: manual proof artifact.

### GST-013. Stale authoritative guide drift blocks later validation

- Covers: R52, EC1, EC2, EC3
- Level: integration
- Fixture/setup: validator fixtures for missing guide links, contradicted ownership claims, and stale authoritative guide surfaces.
- Steps:
  - Assert touched, referenced, generated, or authoritative guide artifacts that contradict the spec or higher-priority source fail guide-system validation, spec-review, code-review, or verify as appropriate.
  - Assert unrelated stale baseline debt may be reported separately without blocking the scoped implementation unless it is touched, referenced, generated, or authoritative for the change.
  - Assert diagnostics name the stale surface and stable guide check ID where practical.
- Expected result: future guide drift is visible and blocking when it affects the current change.
- Failure proves: stale guide artifacts can silently reintroduce routing ambiguity.
- Automation location: guide-system validator fixture tests, selected CI, and later verify evidence.

## Fixtures and data

- Valid and invalid guide-system fixtures under `tests/fixtures/guide-system/` if a dedicated guide validator is added.
- Artifact-lifecycle fixtures under `tests/fixtures/artifact-lifecycle/` if guide-system mode is implemented there.
- Representative README fixtures for missing guide links and contract duplication.
- Representative workflow guide fixtures for missing guide ownership, missing artifact-location section, invalid YAML/table projection, and duplicate registry ownership.
- Representative project-map, plan-index, learn-session, and stage-skill fixtures for boundary violations.
- Real repository guide surfaces are used for integration and selected CI checks after implementation.

## Mocking/stubbing policy

Avoid network, hosted CI, or external service mocks. Use temporary fixture repositories and subprocess calls to repository-owned validators. Do not mock parser behavior that is the subject of the test. Mocking is acceptable only for filesystem isolation around fixture roots.

## Migration or compatibility tests

- GST-010 manually proves no historical artifact migration occurs in the first slice.
- GST-004 proves the plan-body path stays aligned with the approved workflow-map contract.
- GST-008 proves validation semantics and selected-check behavior do not change outside the approved guide-system validator contract.
- GST-009 proves generated outputs remain reproducible from canonical sources when skill packaging is in scope.

## Observability verification

Validation evidence must include:

- guide-system validator or artifact-lifecycle guide-system mode output with stable guide check IDs where practical;
- selected CI output for touched guide, validator, skill, adapter, spec, plan, and change-local paths;
- behavior-preservation proof;
- cold-read proof;
- change metadata validation and review-artifact validation.

## Security/privacy verification

- Assert guide-system validation does not require network access, hosted service state, secrets, credentials, private tokens, usernames, or machine-local private paths.
- Assert stage-skill portability wording does not require customer projects to depend on RigorLoop repository-internal paths unless those paths are explicitly project-local in that customer repository or packaged with the installed skill.

## Performance checks

- Run guide-system checks through selected explicit-path CI for touched guide surfaces.
- Ensure guide validation uses deterministic parsing and fixtures rather than broad natural-language scans.
- Do not require broad smoke solely because README, guide text, proposal, spec, or test-spec artifacts changed unless another authoritative trigger requires it.

## Manual QA checklist

- README remains concise and links out instead of becoming a workflow manual.
- `docs/workflows.md` guide ownership content is scannable as a matrix, table, or equivalent compact structure.
- `docs/project-map.md` orients to the repository and does not own workflow policy.
- `docs/plan.md` remains bounded and links to detailed plan bodies instead of embedding them.
- Learn sessions are not cited as live routing authority.
- Stage-skill edits are limited to direct contradictions and preserve portable defaults.
- Behavior-preservation and cold-read proof rely on current repository artifacts, not chat history.

## What not to test and why

- Do not test every historical guide artifact for migration compliance; historical migration is out of scope.
- Do not snapshot entire guide files; the behavioral contract is about links, headings, ownership boundaries, paths, registry consistency, and proof surfaces.
- Do not use broad prose scoring to decide whether guides are "good"; validator checks must use deterministic structures.
- Do not test external hosted CI or network state; ordinary guide checks are local repository-owned validation.
- Do not require adapter tests when canonical skill content and generated adapter packaging are unaffected.

## Uncovered gaps

None. The implementation may choose either a dedicated guide-system validator or artifact-lifecycle guide-system mode; this test spec covers both acceptable forms.

## Next artifacts

- implement
- code-review
- explain-change
- verify
- pr

## Follow-on artifacts

None yet.

## Readiness

Active proof-planning surface for `implement M1`. This test spec does not claim implementation, code-review, verification, branch, or PR readiness.
