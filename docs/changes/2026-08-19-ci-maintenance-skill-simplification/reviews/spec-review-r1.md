# Spec Review R1: CI-Maintenance Skill Simplification

Review ID: spec-review-r1
Stage: spec-review
Round: r1
Reviewer: Codex independent spec-review context
Target: `specs/ci-maintenance-skill-simplification.md`
Reviewed artifact: `sha256:63282d54f25fa10dcb3b56eaad0071b0ba8779ff9681e947187f4e2e1b2e57e8`
Review date: 2026-08-19
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: CIMSIM-SR1
- Open blockers: the focused amendment does not identify the existing approved clauses that its new skeleton, privilege, and review contracts replace
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: same-stage rereview required after the compatibility relationship is explicit

## Recording

- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/review-resolution.md`

## Governed settlement

- Settlement mode: governed-spec-entry
- Settlement status: revision-required
- Governed change identity: `2026-08-19-ci-maintenance-skill-simplification`

## Boundary review

- Boundary applicability: `boundary-first-v1` applicable
- Boundary resources: `boundary-first-method-v1.md`, `boundary-first-feature-authoring-v1.md`
- Boundary blocker: compatibility ownership does not settle overlapping approved requirements

## Automated review

- Automation mode: workflow-managed-automated
- Automation evidence: `review-invocation-spec-review-r1.yaml`
- Automation result: bounded compatibility correction eligible; rereview required before promotion

## Findings

## Finding CIMSIM-SR1

Finding ID: CIMSIM-SR1
Severity: major
Location: contract context, R21-R25, R43-R45, and Compatibility and migration
Evidence: `specs/ci-maintenance-skill.md` remains approved and requires the skeleton to include PR and boundary structures and cache/action/command placeholders (`CIM-R25`, `CIM-R59`), treats privileged deployment and release authoring as outside the first slice (`CIM-R45`), and requires every workflow review to include changed-surface coverage (`CIM-R53`). The new focused spec deliberately narrows the skeleton, permits approved-design privileged realization, and allows narrow review without the risk map, but does not state which approved clauses it amends.
Required outcome: Add an explicit focused-amendment relationship and closed legacy-clause disposition table so implementation and validation use one authoritative rule for every overlap while preserving unaffected clauses.
Safe resolution path: Append one requirement governing amendment precedence; add a compatibility table mapping each superseded or narrowed legacy clause to its replacement requirements; include the new requirement in the compatibility boundary; then rereview without changing the selected package or scope.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | pass |
| normative language | pass |
| completeness | block |
| testability | pass with revision |
| examples | pass |
| compatibility | block |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | pass with revision |

## Boundary assessment

All eight dimensions are applicable and their partitions, invariants, outcomes, and interactions are otherwise complete. `BND-COMPAT-001` correctly requires explicit consumer ownership, but the specification does not apply that invariant to the already approved CI-maintenance feature contract.

## Recommendation

Apply the bounded compatibility correction and perform a fresh independent spec review. Architecture assessment, planning, and test-spec authoring remain blocked until approval.

## Claim limitations

This review does not approve the specification, settle architecture, authorize planning, establish test-spec readiness, or claim implementation, verification, branch, hosted-CI, or PR readiness.
