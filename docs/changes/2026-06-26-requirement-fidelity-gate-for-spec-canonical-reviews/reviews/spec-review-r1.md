# Spec Review R1

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SR1-F1, SR1-F2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/spec-review-r1.md
- Review log: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md
- Review resolution: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md
- Open blockers: SR1-F1, SR1-F2
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: resolve SR1-F1 and SR1-F2, then rerun spec-review before architecture, plan, test-spec, or implementation relies on this spec.

## Review Metadata

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/requirement-fidelity-gate.md
Status: changes-requested

## Findings

### SR1-F1 - Manual review applicability is undefined

Finding ID: SR1-F1

Severity: major

Location: `specs/requirement-fidelity-gate.md`, requirement `R1` and `Examples first`.

Evidence: `R1` requires "Formal automated reviews and high-risk manual reviews" to apply the requirement-fidelity gate, but the spec does not define `high-risk manual review`, provide a closed trigger set for manual review applicability, or say who records that determination. The examples define deterministic automated applicability and a workflow-managed automated code-review case, but no example covers a manual review being classified as high-risk or not high-risk.

Required outcome: The spec must make manual-review applicability testable. It must either define a closed high-risk manual review trigger model, with recording and override behavior, or remove the `high-risk manual reviews` obligation from first-slice normative scope and route manual adoption through an explicit opt-in/follow-on.

Safe resolution path: Add a glossary definition and requirements for manual-review applicability, such as a closed trigger enum, required manifest fields, and an example showing a manual review classified as applicable. Alternatively, revise `R1` to cover formal automated reviews in the first slice and state that manual reviews may opt in but are not required until a later accepted spec defines manual applicability.

needs-decision rationale: none

### SR1-F2 - Calibration sampling obligations are not measurable

Finding ID: SR1-F2

Severity: major

Location: `specs/requirement-fidelity-gate.md`, requirements `R17`, `R44`, `R45`, and acceptance criteria `AC-RFG-014` and `AC-RFG-015`.

Evidence: `R17` says reviewer-authored decomposition reviews must be "eligible for higher calibration sampling" without defining the baseline, higher rate, owner, or evidence. `R45` says `not-applicable` receipts must be sampled "periodically" without defining cadence, minimum rate, owner, or evidence. `R44` requires a rotating corpus but does not define what makes a corpus iteration or rotation sufficient. The acceptance criteria repeat these obligations but cannot be tested without inventing policy.

Required outcome: The spec must make calibration and sampling requirements measurable or explicitly defer their exact policy outside the first slice. Tests and validators need enough contract to determine whether the sampling and rotation obligations are satisfied.

Safe resolution path: Add a bounded first-slice sampling contract, for example minimum sample rates, review-family ownership, evidence fields, and rotation cadence, or downgrade these statements to non-normative rollout guidance with a follow-on artifact that will define sampling policy before enforcement. Update acceptance criteria to match the chosen scope.

needs-decision rationale: none

## Dimension Results

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | `SR1-F1` leaves manual review applicability undefined; `SR1-F2` leaves sampling obligations underspecified. |
| normative language | concern | Most requirements are stable and testable, but `high-risk`, `higher`, and `periodically` are normative terms without measurable definitions. |
| completeness | concern | The spec covers automated applicability, decomposition, receipts, validator matrices, and compression findings, but does not complete manual applicability or sampling policy. |
| testability | concern | Tests cannot determine high-risk manual review classification or compliance with higher/periodic sampling without guessing. |
| examples | concern | Examples cover automated applicability and not-applicable receipts, but no manual high-risk classification or sampling/rotation example exists. |
| compatibility | pass | Existing independent gates, historical reviews, stage order, rollback, and adapter refresh boundaries are preserved. |
| observability | concern | Review evidence fields are strong, but sampling evidence lacks required owner/rate/cadence fields. |
| security/privacy | pass | The spec forbids secrets, private network access, and side-effecting external systems. |
| non-goals | pass | Historical migration, broad full-spec reads, automatic repair, finding quotas, and workflow stage-order changes are excluded. |
| acceptance criteria | concern | AC-RFG-014 and AC-RFG-015 require sampling and rotating corpus behavior that is not yet measurable. |

## Readiness

The spec is not ready for architecture, plan, test-spec, or implementation until `SR1-F1` and `SR1-F2` are resolved and same-stage spec-review reruns.
