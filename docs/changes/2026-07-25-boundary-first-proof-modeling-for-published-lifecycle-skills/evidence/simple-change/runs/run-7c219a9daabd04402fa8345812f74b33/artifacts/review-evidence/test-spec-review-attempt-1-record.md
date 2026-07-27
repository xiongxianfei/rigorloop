# Portable text normalizer test specification review

Review ID: test-spec-review-r1
Stage: test-spec-review
Status: changes-requested
Reviewed artifact identity: sha256:ffdf1d5c28ae9c7124c260ad9b01493ef4782d664902dc1d93e448bfa8364045
Material findings: finding.unicode-whitespace, finding.isolated-prerequisite
Recording status: recorded

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: finding.unicode-whitespace, finding.isolated-prerequisite
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/test-spec-review.md
- Review log: review-log/test-spec-review.md
- Review resolution: review-resolution/test-spec-review.md
- Open blockers: finding.unicode-whitespace, finding.isolated-prerequisite
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: revise the test specification and submit the substantive revision for re-review

## Findings

## Finding finding.unicode-whitespace

- Finding ID: finding.unicode-whitespace
- Severity: material
- Location: T1, T2, T6; Fixtures and data
- Evidence: R2 governs Unicode whitespace without narrowing the set, but the fixtures cover only representative or bounded characters. No test directly proves every Unicode whitespace character at leading and trailing boundaries.
- Required outcome: Define automated coverage over the complete Unicode whitespace set for leading, trailing, combined-boundary, and all-whitespace inputs.
- Safe resolution path: Revise T1 and T2, or add stable test cases, using a deterministic authoritative enumeration of Unicode whitespace while preserving R2 semantics.
- needs-decision rationale: none

## Finding finding.isolated-prerequisite

- Finding ID: finding.isolated-prerequisite
- Severity: material
- Location: Uncovered gaps; Next artifacts; Readiness
- Evidence: The test specification says an approved plan, plan review, commands, automation locations, and milestone mapping are required before final test-spec-review handoff. Approved R28y explicitly binds this review to the closed behavior-evidence artifact set and places architecture, plan, and plan-review outside the scenario.
- Required outcome: Remove the asserted plan-dependent review prerequisite and describe the artifact as eligible for this isolated behavior-evidence review while retaining Implementation handoff: not-allowed.
- Safe resolution path: Revise only the workflow-readiness statements; do not invent plan, architecture, commands, milestones, or implementation authority.
- needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| Governing-contract alignment | block |
| Requirement coverage | block |
| Example coverage | pass |
| Negative and boundary coverage | block |
| Proof-level adequacy | concern |
| Milestone mapping | pass |
| Command validity | pass |
| Fixture and data design | block |
| Manual-proof boundary | pass |
| Observability | pass |
| Determinism and isolation | concern |
| Scope and non-goals | pass |
| Execution economics | pass |
| Traceability | pass |
| Implementation handoff | block |

## Boundary-first review

Boundary model version: v1
Boundary model scope: R1-R4

The proof map uses the exact feature-owned boundaries `mode.selection`, `text.trim`, `text.preserve`, and `mode.unknown`, plus `interaction.mode-outcome`. Every applicable boundary and the selected interaction has a unique proof obligation with automated test IDs and no manual procedure. T4 and T5 directly cover preservation and unknown-mode outcomes, and T6 covers the composed public behavior. The proof for `text.trim` is incomplete because representative Unicode whitespace fixtures do not establish R2 across the governed Unicode whitespace set. No boundary or interaction ID was invented or renamed.

This is the isolated behavior-evidence review authorized by approved R28y. Architecture, plan, and plan-review were not required or inferred. No automatic downstream handoff occurs, and this review grants no implementation authority.
