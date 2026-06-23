# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-06-23-evidence-bound-incremental-project-map.md
Reviewed artifact: docs/plans/2026-06-23-evidence-bound-incremental-project-map.md
Review date: 2026-06-23
Recording status: recorded
Status: changes-requested

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: PMAP-PLAN1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r1.md`
- Review log: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md`
- Review resolution: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md#plan-review-r1`
- Open blockers: PMAP-PLAN1-F1
- Immediate next stage: plan revision

## Findings

Finding ID: PMAP-PLAN1-F1
Finding: M1 cannot close cleanly before M2 because it expects canonical validator failures that only M2 resolves.
Location: `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md` M1, M2, and Current Handoff Summary
Severity: major
Evidence: M1 is the current planned milestone and is supposed to add validation coverage before changing the skill body. Its expected observable result says validator tests fail before the skill and skeleton are updated, then pass once M2 satisfies the contract. The same M1 closeout requires validation passed, and M1 validation includes `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, and selected validation over `skills/project-map/SKILL.md`. M2 is the milestone that actually updates `skills/project-map/SKILL.md` and adds `skills/project-map/assets/project-map-skeleton.md`.
Required outcome: The plan must make each milestone independently closeable. No milestone may require intentionally failing tests or canonical-skill validation failures to remain unresolved until a later milestone while also requiring validation passed for that milestone.
Safe resolution path: Revise the milestone sequence so M1 either adds only reusable validator/fixture harness changes that pass against current canonical sources, or combines the red canonical `project-map` expectations with the M2 skill/skeleton update in one milestone. Another safe option is to make M1 a documented test-design/test-spec preparation milestone with no failing repository tests committed, then make M2 own the first passing canonical validator change. Update Current Handoff Summary, M1/M2 dependencies, validation commands, and expected observable results so the first implementation handoff is closeable without relying on M2.
needs-decision rationale: none

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Self-contained context | pass | The plan names source artifacts, current skill state, validator anchors, generated-output anchors, and the existing unmigrated project map. |
| Source alignment | pass | Requirements map to the approved `specs/project-map.md`, and non-goals preserve no automatic map migration or generated-output hand-editing. |
| Milestone size | concern | The four-slice shape is reasonable, but M1 and M2 currently split red canonical validation from the implementation that makes it pass. |
| Sequencing | block | PMAP-PLAN1-F1 makes the current first implementation milestone uncloseable as written. |
| Scope discipline | pass | The plan excludes runtime tracing, graph generation, broad artifact validation, and existing map migration. |
| Validation quality | concern | Validation commands are concrete, but M1's validation expectations conflict with its own pre-M2 position. |
| TDD readiness | block | The plan supports test-first intent, but the red/green boundary is not represented in a closeable milestone sequence. |
| Risk coverage | pass | The plan identifies validator overfit, skill length, area-map fragmentation, adapter proof, and unmigrated map risks with recovery paths. |
| Architecture alignment | pass | The plan respects the approved architecture and treats Project maps as current-state living references, not architecture design. |
| Operational readiness | pass | Generated output and adapter proof are temporary-output based and avoid hand-editing generated adapter bodies. |
| Plan maintainability | concern | A small plan revision should be enough, but leaving M1 as written would create misleading progress and validation state. |

## Missing Milestones Or Dependencies

No additional milestone is required. The existing M1/M2 boundary needs revision so the first implementation milestone can close with passing validation before handoff to code-review.

## Suggested Edits

- Change M1 expected observable result so it does not require committed failing canonical validation that only M2 can fix.
- Move canonical `project-map` opt-in/resource-map/skeleton asset assertions that necessarily fail against current `skills/project-map/` into M2, or merge M1 and M2.
- Keep any M1-only tests limited to reusable validator helper behavior or negative fixtures that pass as tests because the expected diagnostic is asserted.
- Update the Current Handoff Summary if the first current milestone changes.

## Readiness

The plan is not ready for `test-spec` until PMAP-PLAN1-F1 is resolved and plan-review is rerun.

This review is isolated. It does not automatically continue into plan revision.
