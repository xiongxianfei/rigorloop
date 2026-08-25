# Spec Review R1: Governed Lifecycle CLI

Review ID: spec-review-r1
Stage: spec-review
Round: r1
Reviewer: Codex independent spec-review context
Target: `specs/governed-lifecycle-cli.md`
Reviewed artifact: `sha256:0138b7709fc9ff994135782ebdda6ed0f3c50d07d2ab8f2562ba309ec940e10c`
Review date: 2026-08-24
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: RLCLI-SR1, RLCLI-SR2, RLCLI-SR3
- Open blockers: evidence invalidation, post-replacement failure recovery, and idempotent retry outcomes are not fully specified
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: same-stage rereview required after the three bounded contract corrections

## Recording

- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Review resolution: `docs/changes/2026-08-24-governed-lifecycle-cli/review-resolution.md`

## Governed settlement

- Settlement mode: governed-spec-entry
- Settlement status: revision-required
- Governed change identity: `2026-08-24-governed-lifecycle-cli`

## Boundary review

- Boundary applicability: `boundary-first-v1` applicable
- Boundary resources: `boundary-first-method-v1.md`, `boundary-first-feature-authoring-v1.md`
- Boundary blocker: three requirement-owned outcomes are incomplete or internally ambiguous

## Automated review

- Automation mode: workflow-managed-automated
- Automation evidence: `review-invocation-spec-review-r1.yaml`
- Automation result: bounded contract correction eligible; independent rereview required before promotion

## Findings

## Finding RLCLI-SR1

Finding ID: RLCLI-SR1
Severity: major
Location: R17, BND-STATE-001, BND-AUTH-001, and INT-001
Evidence: R17 requires invalidation according to a matrix “defined by this spec and its architecture,” but the specification contains no matrix identifying which governed input changes invalidate which reviews, validation evidence, settlements, or milestone evidence. Architecture cannot safely choose a normative user-visible invalidation policy that the feature contract leaves open.
Required outcome: Define the first-release invalidation matrix in the specification, including the subject change, affected evidence classes, resulting evidence state, settlement effect, and required corrective operation.
Safe resolution path: Add a closed invalidation table grounded in R17 and reference it from the relevant identity, state, and interaction boundaries without broadening the command surface.
needs-decision rationale: none

## Finding RLCLI-SR2

Finding ID: RLCLI-SR2
Severity: major
Location: R20-R21, `RL_POST_VALIDATION_FAILED`, INT-002, and EC7
Evidence: R20 durably replaces `change.yaml` before post-validation, while EC7 allows either preserving or restoring the last valid snapshot. Those are observably different outcomes, and the contract does not state what a process interruption after replacement but before validation leaves for the next invocation.
Required outcome: Specify one deterministic committed-state and recovery outcome for post-replacement validation failure and interruption, including what status and repair action the next invocation observes.
Safe resolution path: Define replacement as a pending recoverable state backed by an adjacent prior snapshot until post-validation succeeds, require automatic rollback where safe, and define a closed repair condition for interrupted reconciliation.
needs-decision rationale: none

## Finding RLCLI-SR3

Finding ID: RLCLI-SR3
Severity: major
Location: R18, R22, BND-TEMPORAL-001, EC5, and EC6
Evidence: R18 requires every stale expected lifecycle revision to fail before mutation, while R22 says an “identical completed operation against its resulting revision” succeeds idempotently. An identical request cannot both retain its original expected revision and target the resulting revision, so clients and proof authors cannot derive the required retry result.
Required outcome: Define idempotent replay independently from stale-request rejection and state exactly whether an original stale envelope fails or an equivalent operation submitted against the current revision reports already recorded.
Safe resolution path: Preserve R18’s fail-closed stale rule; define an equivalent operation against the current revision as `already-recorded` when the requested durable facts are identical, and keep the original old-revision envelope stale.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | concern |
| completeness | block |
| testability | block |
| examples | concern |
| compatibility | pass |
| observability | concern |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | concern |

## Boundary assessment

All eight core dimensions are classified and structurally valid. The selected interactions identify the right hazards, but `INT-001` and `INT-002` do not yet own complete normative outcomes because the invalidation and recovery policies remain open. The retry partition is internally ambiguous between stale rejection and already-recorded success.

## Recommendation

Apply the three bounded corrections and perform a fresh independent spec review. Architecture assessment, planning, and test-spec authoring remain blocked until approval.

## Claim limitations

This review does not approve the specification, settle architecture, authorize planning, establish test-spec readiness, or claim implementation, verification, branch, CI, or PR readiness.
