# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: working tree diff for M2. Canonical Project-Map Skill, Skeleton, and Enforcement
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m2-r1.md`, `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md`, `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md`, `docs/plan.md`, `docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
- Open blockers: none
- Next stage: implement M3
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M2. Canonical Project-Map Skill, Skeleton, and Enforcement
- Milestone closeout: closed
- Remaining implementation milestones: M3, M4
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review inputs

- Review surface: working tree diff for M2 canonical skill, skeleton asset, canonical enforcement, validator tests, behavior-preservation evidence, and lifecycle state updates.
- Tracked governing branch state: approved spec `specs/project-map.md`, active test spec `specs/project-map.test.md`, approved active plan `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md`, and current M2 validation evidence in the active plan and change metadata.
- Governing artifacts: M2 milestone in the active plan; `specs/project-map.md` R1-R77 and R83; `specs/project-map.test.md` T4-T11, T16, T18, and T21.
- Validation evidence: `python scripts/test-skill-validator.py -k project_map`, `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py skills/project-map/SKILL.md`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, artifact lifecycle validation, change metadata validation, selected CI, and whitespace validation recorded in the active plan and change metadata.
- Implementation files reviewed: `skills/project-map/SKILL.md`, `skills/project-map/assets/project-map-skeleton.md`, `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, and `docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md`.

## Diff summary

M2 normalizes the canonical `project-map` skill with `version`, `schema-version`, workflow role, operating modes, placement rules, freshness metadata, evidence classes, material-claim examples, source ranking, command/runtime evidence boundaries, root/area map rules, diagram rules, downstream reliance, follow-up boundaries, stop conditions, and result output shape.

The new `assets/project-map-skeleton.md` packages a copy-and-fill Markdown skeleton containing metadata fields, the required map sections, area-map registration table, and evidence-trail shape. Policy remains in `SKILL.md`.

The validator now opts canonical `project-map` into structural contract checks after the canonical skill and skeleton exist. Tests cover the valid canonical skill plus corrupted copies for missing workflow role, missing skeleton asset, and hidden skeleton policy.

The behavior-preservation evidence records M2 coverage for orientation-only role, current-state focus, eleven-section structure, path citations, observation/inference split, narrow-area support, risk routing, handoff, and customer-project mode.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `skills/project-map/SKILL.md` covers current-state orientation and must-not-claim boundaries at lines 16-27, modes at lines 76-85, freshness at lines 108-137, evidence classes/source rank at lines 139-168, commands/runtime evidence at lines 170-181, root/area maps at lines 183-196, diagrams at lines 219-225, and downstream reliance at lines 227-243. |
| Test coverage | pass | `scripts/test-skill-validator.py` validates the canonical skill and corrupted copies for missing workflow role, missing skeleton asset, and skeleton policy leakage at lines 3737-3811. |
| Edge cases | pass | Named M2 edge cases for unsupported `orientation` stage, skeleton policy leakage, missing mapped resource, and configured/executed command boundaries are covered by the stage decision in the plan, validator tests, and skill text lines 170-181. |
| Error handling | pass | `validate_project_map_contract_fixture` accumulates diagnostics for missing sections/fields and stops skeleton-content validation after a missing asset diagnostic at `scripts/skill_validation.py` lines 1908-2010. |
| Architecture boundaries | pass | M2 touches canonical skill text, skeleton asset, validator, tests, and behavior evidence only. It does not change architecture docs, runtime code, generated adapter bodies, or existing project maps. |
| Compatibility | pass | Existing customer-project wording is preserved at `skills/project-map/SKILL.md` lines 68-74. Existing project maps are not migrated, and the next produced-output proof remains assigned to M3. |
| Security/privacy | pass | The diff adds static Markdown guidance and local validation checks only; command guidance requires go-ahead for mutating, network, build, or test execution at `skills/project-map/SKILL.md` lines 177-179. |
| Derived artifact currency | pass | `python scripts/build-skills.py --check` passed, and selected CI included `skills.drift` and `adapters.drift`; M4 still owns full generated adapter inclusion proof. |
| Unrelated changes | pass | The reviewed M2 diff is scoped to canonical `project-map`, its skeleton, project-map validation/tests, behavior-preservation evidence, and M2 lifecycle state. Earlier proposal/spec/architecture/plan artifacts are outside this behavior review surface. |
| Validation evidence | pass | The active plan records M2 validation at `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md` lines 369-370, including selected CI checks `skills.validate`, `skills.regression`, `skills.generation_regression`, `skills.drift`, `adapters.drift`, lifecycle, metadata, and guide-system validation. |

## No-finding rationale

The implementation satisfies M2's canonical-plus-enforcement boundary: the canonical skill and skeleton were updated together, then canonical enforcement was enabled. The validator catches the stable structural failures named by the test spec without becoming a full produced-map artifact validator.

The skeleton asset owns only reusable output structure and short fill instructions. Evidence ranking, inference policy, refresh triggers, future-design prohibitions, handoff rules, and claim boundaries remain in `SKILL.md`, matching the approved skeleton boundary.

## Residual risks

M3 still needs representative produced-output proof and cold-read proof. M4 still needs generated adapter inclusion proof. This review does not claim final verification, branch readiness, PR readiness, or final lifecycle closeout.

## Handoff

Reviewed milestone: M2. Canonical Project-Map Skill, Skeleton, and Enforcement
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Remaining implementation milestones: M3, M4
Next stage: implement M3
Final closeout readiness: not ready; M3-M4, explain-change, verify, and PR handoff have not completed.

Do not claim branch readiness, PR readiness, verification, final lifecycle closeout, or full generated adapter inclusion from this review.
