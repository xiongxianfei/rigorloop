# Spec Review R1: Workflow-Routed Upstream Corrections

Review ID: spec-review-r1
Stage: spec-review
Round: r1
Reviewer: Codex independent spec-review context
Target: `specs/workflow-routed-upstream-corrections.md`
Reviewed artifact: `sha256:3c22f1de9f619be6bf9050889e75a257916a7b99238973bf032dcf44e33a48aa`
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: WRUC-SR1, WRUC-SR2, WRUC-SR3
- Open blockers: active-route blocker projection, exact return evidence, and withdrawal receipt revision identity are ambiguous
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: same-stage rereview required after the three bounded contract corrections

## Recording

- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/review-log.md`
- Review resolution: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/review-resolution.md`

## Governed settlement

- Settlement mode: governed-spec-entry
- Settlement status: revision-required after CLI recording and settlement
- Governed change identity: `2026-08-25-workflow-routed-upstream-corrections`

## Boundary review

- Boundary applicability: `boundary-first-v1` applicable
- Boundary resources: `boundary-first-method-v1.md`, `boundary-first-feature-authoring-v1.md`
- Boundary blocker: three requirement-owned state, identity, and temporal outcomes are incomplete

## Automated review

- Automation mode: workflow-managed-automated
- Automation evidence: current workflow routing and exact CLI context for `spec-review-r1`
- Automation result: bounded spec correction eligible; independent rereview required before architecture

## Findings

## Finding WRUC-SR1

Finding ID: WRUC-SR1
Severity: material
Location: R9-R11, R16, BND-STATE-001, and INT-001
Evidence: The source blocker must be preserved for exact restoration, but the contract does not state whether that blocker remains in active workflow routing during correction. Existing lifecycle permission logic treats a workflow blocker as fatal, so an implementation can preserve it in place and still reject the exact destination revision that R11 requires.
Required outcome: Define the active-route workflow projection, including where the suspended blocker lives, what current blocker is exposed, and how only the destination operation bypasses the suspended source condition.
Safe resolution path: Move the source blocker into the immutable source snapshot, expose route-active coordination as the current state without a fatal source blocker, and restore the original blocker byte-for-byte on return.
needs-decision rationale: none

## Finding WRUC-SR2

Finding ID: WRUC-SR2
Severity: material
Location: R14-R15, inputs and outputs, BND-AUTH-001, and BND-ENV-001
Evidence: Return requires a contained evidence path but the evidence contents are not bound to the route, revised artifact, approving review occurrence, or expected revision. The phrase `same-stage review` is also ambiguous because authoring and review authorities have different stage names.
Required outcome: Define exact return-evidence fields and identify the approving review by artifact ID, revised SHA-256, review ID, review round, review stage authority, outcome, and durable evidence identity.
Safe resolution path: Add a closed return-evidence contract and replace `same-stage review` with the exact matching review authority derived from the destination artifact kind.
needs-decision rationale: none

## Finding WRUC-SR3

Finding ID: WRUC-SR3
Severity: material
Location: R25, successful withdrawal output, BND-TEMPORAL-001, and BND-COMPAT-001
Evidence: The receipt must contain an `operation lifecycle revision`, but the contract does not distinguish the request's prior revision from the resulting revision. Persisting the resulting hash inside the bytes used to calculate that hash is circular and cannot have a deterministic ordinary SHA-256 construction.
Required outcome: Bind the receipt to the expected prior lifecycle revision and define the resulting revision only in the operation result, not as self-referential stored receipt content.
Safe resolution path: Rename the durable field `prior_lifecycle_revision`; retain `resulting_lifecycle_revision` solely in the common CLI result envelope.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | concern |
| completeness | block |
| testability | block |
| examples | pass |
| compatibility | concern |
| observability | concern |
| security/privacy | concern |
| non-goals | pass |
| acceptance criteria | concern |

## Boundary assessment

All eight core dimensions are classified and structurally present. `BND-STATE-001` does not yet define the active route's blocker projection, `BND-AUTH-001` does not bind return authority to an exact review occurrence, and `BND-TEMPORAL-001` admits a potentially self-referential receipt identity. Those are normative gaps rather than downstream architecture choices.

## Recommendation

Apply the three bounded corrections and perform a fresh independent spec review. Architecture assessment, planning, and test-spec authoring remain blocked until approval.

## Claim limitations

This review does not approve the specification, settle architecture, authorize planning, establish test-spec readiness, or claim implementation, verification, branch, CI, or PR readiness.
