# Spec Review R2: Workflow-Routed Upstream Corrections

Review ID: spec-review-r2
Stage: spec-review
Round: r2
Reviewer: Codex independent spec-review context
Target: `specs/workflow-routed-upstream-corrections.md`
Reviewed artifact: `sha256:66f22be6e1d6cfe51cb9bf77913a165cbb63d87729529b54138519246e142dc8`
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: WRUC-SR4
- Open blockers: two split boundary dimensions overclaim complete requirement ownership
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: same-stage rereview required after truthful boundary consolidation

## Recording

- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/reviews/spec-review-r2.md`
- Review log: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/review-log.md`
- Review resolution: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/review-resolution.md`

## Governed settlement

- Settlement mode: governed-spec-entry
- Settlement status: revision-required after CLI recording and settlement
- Governed change identity: `2026-08-25-workflow-routed-upstream-corrections`

## Boundary review

- Boundary applicability: `boundary-first-v1` applicable but semantically incomplete
- Boundary resources: `boundary-first-method-v1.md`, `boundary-first-feature-authoring-v1.md`
- Boundary blocker: state and authority boundary rows claim full-dimension requirements while each describes only one partial family

## Automated review

- Automation mode: workflow-managed-automated
- Automation evidence: current workflow routing and exact CLI context for `spec-review-r2`
- Automation result: bounded boundary-record correction eligible; rereview required

## Findings

## Finding WRUC-SR4

Finding ID: WRUC-SR4
Severity: material
Location: boundary applicability, BND-STATE-001, BND-STATE-002, BND-AUTH-001, BND-AUTH-002, INT-002, and E4
Evidence: Structural normalization gives both state boundaries the complete state requirement set and both authority boundaries the complete authority requirement set, but each row still describes only correction routing or only registration withdrawal. A reader cannot derive every claimed requirement's partitions, invariants, and outcomes from either definition.
Required outcome: Make every boundary definition truthfully cover its complete declared requirement set without duplicate partial ownership.
Safe resolution path: Consolidate state behavior into one `BND-STATE-001`, consolidate authority behavior into one `BND-AUTH-001`, and update interaction and example references without changing normative requirements.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | pass |
| normative language | pass |
| completeness | concern |
| testability | block |
| examples | concern |
| compatibility | pass |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | concern |

## Boundary assessment

The R1 corrections are complete. The remaining issue is limited to truthful boundary ownership: mechanically duplicated requirement sets must not imply that two partial rows independently define outcomes they do not describe.

## Recommendation

Consolidate the two affected boundary dimensions, preserve all requirements and examples, then perform spec-review r3.

## Claim limitations

This review does not approve the specification or any downstream artifact, implementation, validation, verification, branch, CI, or PR state.
