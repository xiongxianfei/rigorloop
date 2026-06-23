# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: working tree diff for M1. Project-Map Validator and Fixture Scaffolding
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m1-r1.md`, `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md`, `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md`, `docs/plan.md`, `docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
- Open blockers: none
- Next stage: implement M2
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M1. Project-Map Validator and Fixture Scaffolding
- Milestone closeout: closed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review inputs

- Review surface: working tree diff for M1 implementation files, controlled fixtures, selector fix, lifecycle state, and change-local fixture evidence.
- Tracked governing branch state: approved spec `specs/project-map.md`, active test spec `specs/project-map.test.md`, approved active plan `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md`, and current M1 validation evidence in the active plan and change metadata.
- Governing artifacts: M1 milestone in the active plan; `specs/project-map.md` R3-R5, R36, R58-R65, R78-R80; `specs/project-map.test.md` T1-T3.
- Validation evidence: `python scripts/test-skill-validator.py -k project_map`, `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/select-validation.py --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills`, `python scripts/test-build-skills.py`, selector regression, selected CI, artifact lifecycle validation, change metadata validation, and whitespace validation recorded in the active plan and change metadata.
- Implementation files reviewed: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, `scripts/validation_selection.py`, `scripts/test-select-validation.py`, `tests/fixtures/skills/project-map-contract/valid/SKILL.md`, `tests/fixtures/skills/project-map-contract/valid/assets/project-map-skeleton.md`, and `docs/changes/2026-06-23-evidence-bound-incremental-project-map/validator-fixtures.md`.

## Diff summary

M1 adds `validate_project_map_contract_fixture` as a controlled fixture helper without wiring it into canonical `validate_skill_file` enforcement. The helper validates structural project-map fixture expectations for normalized metadata, workflow-role fields, operating modes, map metadata, evidence classes, material and incidental claim examples, root/area map registration columns, required output headings, skeleton `COPY` mapping, skeleton section coverage, and skeleton policy leakage.

`scripts/test-skill-validator.py` adds a valid controlled fixture test plus negative temporary-copy tests for missing baseline, missing `audit` mode, non-`COPY` skeleton resource-map entry, and hidden skeleton policy. The fixture lives under `tests/fixtures/skills/project-map-contract/valid/`.

The selector now classifies the directory path `tests/fixtures/skills` as `validator-skills`, matching the active plan's M1 selected-validation command. `docs/changes/.../validator-fixtures.md` records the controlled-fixture evidence and the explicit canonical-enforcement boundary.

Canonical `skills/project-map/SKILL.md`, the canonical `skills/project-map/assets/project-map-skeleton.md`, generated skill output, and adapter output are not changed by M1.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M1 is limited to fixture/helper scaffolding for R3-R5, R36, R58-R65, and R78-R80. The helper docstring states it is controlled-fixture only and M2 owns canonical enforcement, matching the plan boundary. |
| Test coverage | pass | `scripts/test-skill-validator.py` has a passing valid fixture test and negative tests for baseline, mode, resource-map verb, and skeleton policy diagnostics. |
| Edge cases | pass | The named M1 edge cases are fixture-level diagnostics, and each negative case passes by asserting expected diagnostics instead of committing red canonical checks. |
| Error handling | pass | The helper accumulates diagnostics and handles missing sections by setting empty section text before checking required fields. Missing skeleton asset produces a diagnostic and stops skeleton-content checks. |
| Architecture boundaries | pass | M1 changes validation scaffolding only. It does not alter architecture documents, runtime components, canonical project-map behavior, generated output, or adapter packages. |
| Compatibility | pass | Canonical `project-map` enforcement remains disabled until M2, so existing canonical skill validation stays green. The selector directory classification makes the approved M1 command deterministic. |
| Security/privacy | pass | The diff adds repository-relative fixture paths and static validation text only; no secrets, credentials, network access, or runtime execution behavior is introduced. |
| Derived artifact currency | pass | M1 changes no generated skill or adapter output. `python scripts/test-build-skills.py` and selected CI `skills.generation_regression` passed. |
| Unrelated changes | pass | The reviewed M1 diff is scoped to validator helper/tests, controlled fixtures, selector classification, and M1 lifecycle evidence. Earlier proposal/spec/architecture/plan artifacts are outside the M1 code-review behavior surface. |
| Validation evidence | pass | The active plan and change metadata record the required M1 commands, selected CI, lifecycle validation, metadata validation, selector regression, generation regression, and whitespace validation as passing. |

## No-finding rationale

The implementation satisfies the revised M1 boundary from plan-review: it proves the approved project-map contract shape against controlled valid and invalid fixtures while avoiding canonical enforcement against unchanged `skills/project-map/SKILL.md`. Negative fixtures pass by asserting diagnostics, so no intentionally failing canonical state is committed.

The selector change is narrow and justified by the approved M1 validation command: before the fix, concrete fixture files were classifiable but the directory path in the plan was not. The added selector regression covers that exact directory form and selected CI reran the full selector regression.

## Residual risks

The helper uses structural string checks appropriate for M1 fixture scaffolding. M2 still needs to update the canonical skill, add the canonical skeleton asset, and enable canonical enforcement atomically.

## Handoff

Reviewed milestone: M1. Project-Map Validator and Fixture Scaffolding
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Remaining implementation milestones: M2, M3, M4
Next stage: implement M2
Final closeout readiness: not ready; M2-M4, explain-change, verify, and PR handoff have not completed.

Do not claim branch readiness, PR readiness, verification, final lifecycle closeout, or canonical project-map enforcement from this review.
