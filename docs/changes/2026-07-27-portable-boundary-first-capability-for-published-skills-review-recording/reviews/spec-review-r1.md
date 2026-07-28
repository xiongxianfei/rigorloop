# Boundary-First Proof Model Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Independent contract review
Target: specs/boundary-first-proof-model.md
Companion scope: specs/rigorloop-workflow.md; specs/skill-contract.md
Status: changes-requested
Material findings: PBF-SR1, PBF-SR2, PBF-SR3
Architecture assessment: required
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: PBF-SR1, PBF-SR2, PBF-SR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/spec-review-r1.md
- Review log: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md
- Review resolution: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md#spec-review-r1
- Open blockers: PBF-SR1, PBF-SR2, PBF-SR3
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: record grammar and activation enforcement require revision before architecture reliance

## Findings

## Finding PBF-SR1

Finding ID: PBF-SR1
Severity: major
Location: specs/boundary-first-proof-model.md, PBF-R014 through PBF-R040 and Edge cases
Evidence: The draft permits feature-specific dimension extensions without defining their serialization, defines dimension-specific boundary prefixes without an explicit dimension-to-prefix mapping, omits a closed empty-cell and multi-ID serialization rule, and allows cross-feature imports in EC8 without defining an import contract.
Required outcome: Make the v1 record grammar closed enough for deterministic parsing without inventing extension, delimiter, sentinel, prefix, or import semantics.
Safe resolution path: Prohibit dimension extensions and cross-feature boundary imports in v1; add an explicit core-dimension-to-prefix column; require ASCII `-` for absent values and comma-space separation for multiple IDs; constrain contract-owned IDs while leaving project-owned test, command, regression, gap, and manual-procedure IDs to the project-local stable-ID grammar.
needs-decision rationale: none

## Finding PBF-SR2

Finding ID: PBF-SR2
Severity: major
Location: specs/boundary-first-proof-model.md, activation header and PBF-R003 through PBF-R007, PBF-R052 through PBF-R058
Evidence: The draft names an activation state but does not define the durable activation baseline that distinguishes grandfathered historical feature specs from new or substantively revised specs, nor who owns substantive-revision classification when structural validation cannot infer semantics.
Required outcome: Define deterministic activation evidence and separate structural enforcement from semantic revision classification.
Safe resolution path: Require an activation record containing state, contract version, activation time, activation baseline identity, and grandfathered feature-spec inventory identity; let architecture select the concrete path and format; require structural validation for new specs and marker shape, and require spec-review to classify whether edits to grandfathered specs are substantive.
needs-decision rationale: none

## Finding PBF-SR3

Finding ID: PBF-SR3
Severity: major
Location: specs/boundary-first-proof-model.md, PBF-R033 through PBF-R040
Evidence: The proof-map table includes `Uncovered gap` on every proof row but does not define when the row is a proof versus a gap, which fields must be `-`, or whether a gap can count toward the requirement that every boundary and interaction has proof.
Required outcome: Prevent an uncovered-gap row from being mistaken for coverage or implementation readiness.
Safe resolution path: Define proof rows as either `covered` or `gap`, add a closed `Coverage state` column, require complete proof fields for `covered`, require a gap ID and `-` proof fields for `gap`, and state that any gap blocks test-spec-review approval and implementation.
needs-decision rationale: none

## Review Dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | concern |
| normative language | pass |
| completeness | block |
| testability | block |
| examples | pass |
| compatibility | concern |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | concern |

## Recommendation

Preserve the three-owner contract split and revise the boundary grammar,
activation evidence, and proof-gap semantics.
After recording resolution and revising the specs, perform spec-review R2.
