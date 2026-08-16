# Test-Spec Review R1: Architecture-Review Skill Simplification

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/architecture-review-skill-simplification.test.md`
Reviewed artifact: commit `b560ae0e`
Review date: 2026-08-16
Status: changes-requested
Review status: changes-requested
Material findings: ARRTSR-PR1
Recording status: recorded
Immediate next stage: review-resolution
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: ARRTSR-PR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-16-architecture-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-architecture-review-skill-simplification/review-resolution.md`
- Open blockers: ARRTSR-PR1
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: bounded automation target reached at the first formal test-spec-review result; implementation remains blocked pending disposition, test-spec revision, and rereview

## Findings

## Finding ARRTSR-PR1

Finding ID: ARRTSR-PR1
Severity: major
Location: `specs/architecture-review-skill-simplification.test.md`, T8 and the R28-R36 coverage row
Evidence: R30 requires direct proof that canonical architecture reaches `approved`, each ADR reaches the exact `accepted` or `active` state recorded by current authoring evidence, and a missing or ambiguous intended ADR state blocks the complete settlement. T8 covers a generic approved combined target set but its fixture and expected result do not enumerate either valid ADR state or the missing and ambiguous failure partitions. T9 covers ambiguous targets generally, which does not prove the distinct intended-ADR-state contract.
Required outcome: Add direct deterministic cases for canonical `approved`, ADR `accepted`, ADR `active`, missing intended ADR state, and ambiguous intended ADR state, and assert that either invalid ADR-state case leaves every target unchanged and blocks complete settlement.
Safe resolution path: Extend T8 or add a focused case, update the requirement, proof, acceptance, edge, and milestone mappings as needed, rerun boundary validation, and obtain a fresh independent test-spec review.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| governing-contract alignment | pass | The proof map consumes the approved spec, no-architecture assessment, active plan, and clean upstream reviews without redefining behavior. |
| requirement coverage | concern | All requirement ranges are mapped, but R30 lacks direct proof for its per-kind success states and mandatory invalid-state stop. |
| acceptance-criterion coverage | pass | AC1 through AC12 map to stable cases, commands, and milestones. |
| example and edge coverage | pass with revision | E1 through E12 and EC1 through EC8 map to cases, but R30's missing and ambiguous intended-state partitions need explicit edge treatment. |
| boundary and interaction coverage | pass | All seven boundaries and INT-001 through INT-005 have structurally valid covered obligations, and repository boundary validation passes. |
| negative and failure coverage | block | The intended ADR post-state failure branch is material settlement behavior and is not directly exercised. |
| settlement coverage | block | Generic approval does not prove canonical `approved`, ADR `accepted`, ADR `active`, or complete blocking when ADR intent is unresolved. |
| prepared-retry coverage | pass | Evidence-before-write, manifest contents, interruption, pending-write replay, duplication, concurrency, and changed-state stops are explicit. |
| proof-level adequacy | pass | Contract, integration, and smoke levels match the content, lifecycle, recovery, measurement, and distribution claims. |
| milestone mapping | pass | M1 freezes ownership and evidence capability, M2 changes the package, M3 proves reduction and parity, and M4 owns closeout. |
| command validity | pass | Planned focused classes use the existing test runner, and all existing command paths resolve. |
| fixture and data design | pass with revision | Temporary review evidence and change records are appropriate; T8 needs the complete ADR intended-state partitions. |
| manual-proof boundary | pass | No manual proof is required, and ordinary lifecycle or PR review is not recast as another acceptance procedure. |
| determinism and isolation | pass | Acceptance excludes network services, publication, target-agent execution, transcript grading, and an extra manual gate. |
| implementation handoff | block | Implementation would need to invent the exact R30 fixtures and expected all-target failure behavior. |

## No-finding areas

- Package loading, missing resources, shared-block parity, and semantic/literal ownership have deterministic proof.
- All four surfaces, all four assemblies, all six valid authority combinations, and representative invalid combinations are covered.
- Record-only subjects, governing-basis staleness, evidence-scoped non-approval dispositions, prepared manifests, exact retry, and concurrency have direct cases.
- Canonical-through-installed parity and real formal-profile reduction remain separately visible.
- No acceptance command executes or grades Codex, Claude Code, opencode, or another target-agent runtime.

## Claim limitations

This review records one proof-map defect and blocks implementation handoff. It does not claim implemented tests, completed milestones, validation success, verification, branch readiness, or PR readiness.
