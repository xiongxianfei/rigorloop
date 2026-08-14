# Test-Spec Review R1: Project-Map Skill Simplification

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/project-map.test.md`
Reviewed artifact: commit `15aeff1e`
Review date: 2026-08-14
Status: changes-requested
Review status: changes-requested
Material findings: PMAPTSR-PR1
Recording status: recorded
Immediate next stage: review-resolution
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: PMAPTSR-PR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-14-project-map-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-14-project-map-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-14-project-map-skill-simplification/review-resolution.md`
- Open blockers: PMAPTSR-PR1
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: bounded automation target reached at the first formal test-spec-review result; implementation remains blocked pending disposition, test-spec revision, and rereview

## Findings

## Finding PMAPTSR-PR1

Finding ID: PMAPTSR-PR1
Severity: major
Location: `specs/project-map.test.md:372` and `specs/project-map.test.md:377`; hybrid proof mappings that rely on MP0 or MP1
Evidence: MP0 and MP1 provide stable identifiers, procedures, and evidence paths, but neither records an automation rationale, execution environment, explicit pass condition, explicit failure condition, or owning stage. The proof map and milestone map cite these procedures as required hybrid evidence, so an implementer cannot execute or evaluate them from the authored test specification alone.
Required outcome: Give every cited manual procedure an explicit automation rationale, environment, exact steps, evidence artifact, pass condition, failure condition, and owning stage, while preserving its requirement and milestone mappings.
Safe resolution path: Revise MP0 and MP1 without weakening their semantic-preservation claims, or convert an affected proof row to fully automated proof when a deterministic command genuinely owns the claim; then rerun boundary validation and independent test-spec review.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| governing-contract alignment | pass | The proof map consumes the approved specification, reviewed architecture, and active plan without redefining behavior. |
| requirement coverage | pass | The normative requirements and approved examples have mapped proof. |
| boundary and interaction coverage | pass | Applicable boundaries and selected interactions have direct proof obligations, and repository boundary validation passes. |
| operation and assembly coverage | pass | Target-state selection, bounded coordination preflight, PMA0, and PMA1 have positive and negative scenarios. |
| transaction coverage | pass | Root prerequisites, area-first writing, root-registration commit, exact retry, conflict, ambiguity, and stale-root behavior are covered. |
| audit and freshness coverage | pass | Audit remains read-only, correction requires a new refresh, and dirty or stale evidence remains visible. |
| compatibility and package coverage | pass | Read-old/write-new result behavior and canonical, generated, archived, and installed parity are mapped. |
| automated command design | pass | The deterministic commands have named scope, evidence, failure behavior, and milestone ownership. |
| manual proof design | block | MP0 and MP1 omit the execution and verdict fields required for executable manual evidence. |
| milestone mapping | pass | Preservation, package mutation, parity proof, and lifecycle closeout are separated into reviewable milestones. |
| determinism and isolation | pass | Acceptance excludes network services, publication, target-agent execution, prompt journeys, and transcript grading. |
| implementation handoff | block | Required hybrid proof cannot be executed or evaluated deterministically from the current manual procedure records. |

## No-finding areas

- The feature and proof records pass deterministic boundary validation.
- Operation, scope, target state, preflight, assembly, authority, and missing-resource outcomes are covered.
- The area transaction has explicit success, interruption, recovery, conflict, and idempotency scenarios.
- The skeleton remains the sole structural owner and does not acquire policy authority.
- Package proof covers canonical, generated, archived, and clean-installed targets.
- No acceptance command executes or grades Codex, Claude Code, opencode, or another target-agent runtime.

## Claim limitations

This review records one proof-map defect and blocks implementation handoff. It does not claim implemented tests, completed milestones, validation success, verification, branch readiness, or PR readiness.
