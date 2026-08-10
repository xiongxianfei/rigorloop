# Published-Skill-First Repository Simplification Test-Spec Review R2

Review ID: test-spec-review-r2
Stage: test-spec-review
Round: 2
Reviewer: Codex independent test-spec-review context
Target: `specs/published-skill-first-repository-simplification.test.md`
Reviewed artifact: `specs/published-skill-first-repository-simplification.test.md`
Review date: 2026-08-10
Status: changes-requested
Review status: changes-requested
Recording status: recorded
Material findings: PSR-TSR2-001
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: workflow-managed bounded correction

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: PSR-TSR2-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/test-spec-review-r2.md`
- Review log: `docs/changes/2026-08-10-published-skill-first-repository-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-10-published-skill-first-repository-simplification/review-resolution.md#test-spec-review-r2`
- Open blockers: PSR-TSR2-001
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: one stale lifecycle-command evidence reference requires test-spec revision

## Findings

## Finding PSR-TSR2-001

Finding ID: PSR-TSR2-001
Severity: major
Location: `specs/published-skill-first-repository-simplification.test.md`, CMD18
Evidence: CMD18 is required by the preimplementation milestone row but validates `evidence/test-spec-authoring.md`. The active test-spec entry identifies `evidence/test-spec-revision-r2.md` as its authoring evidence. Running CMD18 as written would validate historical initial authoring evidence rather than the current reviewed revision.
Required outcome: The preimplementation lifecycle command must validate the active R2 test-spec authoring evidence.
Safe resolution path: Replace only CMD18's evidence operand with `docs/changes/2026-08-10-published-skill-first-repository-simplification/evidence/test-spec-revision-r2.md`, update revision evidence, and rerun formal test-spec review.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | Current spec-review R2 is linked and behavior remains aligned. |
| Requirement, example, and edge coverage | pass | All approved IDs retain direct proof. |
| Negative and boundary coverage | pass | Every boundary and interaction has direct negative or composed proof. |
| Proof-level adequacy | pass | MP1 is now an exact, justified, review-owned manual procedure. |
| Milestone mapping | concern | Preimplementation CMD18 points to stale authoring evidence. |
| Command validity | block | CMD18 does not validate the active revision evidence. |
| Fixture, observability, determinism, and scope | pass | Proof remains local, actionable, deterministic, non-publishing, and excludes target runtimes. |
| Traceability | pass | PSR-TSR1-001 and PSR-TSR1-002 are resolved. |
| Implementation handoff | block | Current authoring evidence would not be validated by the required command. |

## Handoff

PSR-TSR1-001 and PSR-TSR1-002 are resolved.
Implementation remains blocked only on PSR-TSR2-001 and the required R3 review.
