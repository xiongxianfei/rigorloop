# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Target: docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md
Reviewed artifact: docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md
Review date: 2026-05-25
Reviewer: Codex plan-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: SRTR-PR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/reviews/plan-review-r1.md
- Review log: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/review-log.md
- Review resolution: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/review-resolution.md
- Open blockers: SRTR-PR1
- Immediate next stage: plan revision

## Findings

## Finding SRTR-PR1

Finding ID: SRTR-PR1
Severity: major
Location: docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md, M1 Validator and Fixture Coverage
Evidence: M1 says its goal is to add validator and fixture coverage "before changing canonical skill wording" (line 85), then instructs the implementer to "Record expected failing checks before the canonical skill/result skeleton is updated, then pass after M2" (line 108). The same M1 milestone requires `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, and milestone closeout with "validation passed", "milestone committed", and "code-review requested for M1" before M2 begins (lines 109-121). That makes M1 non-closable as a standalone milestone: either the new checks fail until M2 changes the canonical skill and skeleton, or M1 must dilute the checks so they do not enforce the approved contract.
Required outcome: Revise the plan so every implementation milestone has a coherent, passable validation boundary. The plan must not require an M1 code-review handoff while M1 intentionally leaves contract checks failing against unchanged canonical skill assets.
Safe resolution path: Choose one sequencing model and make it explicit. Either combine validator coverage and canonical skill/skeleton changes into one first implementation milestone that can pass before code-review, or make M1 a non-implementation preparatory/test-design step with no standalone code-review closeout and move the first pass/fail validator enforcement into the milestone that updates `skills/spec-review/SKILL.md` and `assets/review-result-skeleton.md`. A third safe option is to keep M1 separate but scope it only to fixture/parser scaffolding that passes against controlled fixtures, with canonical-skill enforcement enabled in M2.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
|---|---|---|
| self-contained context | pass | The plan identifies the accepted proposal, approved amended spec, change metadata, review evidence, canonical skill source, result skeleton asset, material-finding asset, and generated-output boundaries. |
| source alignment | pass | The plan traces R1-R8 and acceptance criteria to planned work, preserves the `test-spec` immediate-route ban for `spec-review`, and recognizes the matching test spec is stale. |
| milestone size | concern | M1 and M2 are individually understandable, but SRTR-PR1 shows their boundary is not reviewable as written because M1 depends on M2 to pass. |
| sequencing | block | M1 is sequenced before canonical skill/result-skeleton edits while also requiring passing validation and code-review for checks expected to fail until M2. |
| scope discipline | pass | The plan keeps adjacent skills, workflow order, adapter output, material-finding asset shape, review status values, and finding severity values scoped. |
| validation quality | concern | The validation set is strong, but the M1 validation timing is internally inconsistent. |
| TDD readiness | concern | The plan correctly wants contract tests first, but it needs a milestone boundary that can represent expected failure without claiming a clean implementation slice. |
| risk coverage | pass | The plan names overfitting, stale test-spec, readiness weakening, material-finding drift, generated-output drift, and broad-refactor pressure. |
| architecture alignment | pass | No separate architecture artifact is needed for this localized skill, asset, validator, and generated-output change. |
| operational readiness | pass | Adapter-version uncertainty and local tooling limits are called out with recovery paths. |
| plan maintainability | concern | The current handoff summary is good, but M1/M2 closeout semantics need revision before implementation can proceed cleanly. |

## Missing milestones or dependencies

No additional artifact class is missing. The plan already blocks implementation on the matching test-spec amendment. The required fix is milestone-boundary and sequencing clarity, not a new architecture or workflow artifact.

## Suggested plan edits

- Revise M1/M2 so the first implementation milestone that requests code-review can pass all named validation commands.
- If keeping TDD-first evidence, record expected failures as part of a combined milestone or as pre-implementation test-spec/design evidence, not as a standalone implementation milestone with clean closeout.
- Keep the test-spec amendment dependency before implementation.
- Preserve the existing M3 generated-output proof milestone.

## No-finding statement

Not applicable. This review recorded a material finding.
