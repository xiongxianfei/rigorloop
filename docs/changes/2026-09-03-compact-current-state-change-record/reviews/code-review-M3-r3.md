# Code Review M3 R3: Derived-state and freshness boundary

Review ID: code-review-m3-r3
Stage: code-review
Round: r3
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: M3 compact semantic-operation implementation against the approved Design R6 package
Reviewed milestone: M3
Review date: 2026-09-04
Status: changes-requested
Review status: changes-requested
Material findings: CCSR-M3-CR2
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-M3-r3.md`, `review-log.md`, and `review-resolution.md`
- Open blockers: CCSR-M3-CR2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CCSR-M3-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `reviews/code-review-M3-r3.md`
- Review log: `review-log.md`
- Review resolution: `review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CCSR-M3-CR2
- Verify readiness: not-claimed

## Finding CCSR-M3-CR2

- Finding ID: CCSR-M3-CR2
- Severity: major
- Location: `specs/compact-current-state-change-record.md` SR-03, SR-14, SR-15, SR-22, SR-25, SR-26, SR-34 and the approved M3 evaluator/request design
- Evidence: M3 could validate a caller-constructed candidate set, but the approved contract did not define how dependency IDs resolve, how code or implementation subject drift is observed without Git, or the exact lifecycle-derived operation matrix. `permitted_operations` was writable coordinator state, and `migrate-change` required one evaluator to validate incompatible source and candidate contracts. The implementation therefore could not construct a unique legal result or prove freshness without inventing normative behavior.
- Required outcome: Make callers supply semantic intent and stage-owned content only; make the evaluator derive `change.yaml`, references, readiness, operation eligibility, and lifecycle revision; define typed dependencies and bounded direct subject identity checks; remove durable permitted-operation authority; and apply compact v1 prospectively without an in-place legacy migration operation.
- Safe resolution path: Accept the finding, route the material direction revision to Proposal, obtain fresh Proposal Review, revise and register the exact Specification, Architecture, and ADR package, obtain fresh Design Review, revise and approve Delivery allocation, then realign and rereview M1 through M3 implementation before continuation.
- needs-decision rationale: none; the user selected the minimal derived-state and prospective-adoption direction explicitly.

## Checklist

| Area | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | The approved schema admits caller-constructed derived state and leaves dependency resolution incomplete. |
| Test coverage | concern | Existing M1/M2 tests prove the old candidate-file contract, not evaluator construction or direct subject drift. |
| Edge cases | block | Direct code-subject drift and cross-contract source/candidate validation lack owned outcomes. |
| Error handling | concern | The old evaluator cannot distinguish unresolved dependency identity from legitimate unchanged state. |
| Architecture boundaries | block | Semantic authorship and mechanical state derivation are not separated sufficiently. |
| Compatibility | block | In-place migration adds an unnecessary mixed-contract writer to prospective adoption. |
| Security/privacy | pass | No caller identity, Git, PR, network, or hosted permission dependency is required. |
| Derived artifact currency | block | Schema and implementation must follow the refined Design package after approval. |
| Unrelated changes | pass | The correction remains scoped to compact-state derivation and freshness. |
| Validation evidence | concern | Existing passing tests remain useful for transaction mechanics but cannot approve the revised semantic contract. |

## Handoff

M3 remains implementing. CCSR-M3-CR2 routes to Proposal and Design; no milestone, branch, Verify, or PR readiness is claimed.
