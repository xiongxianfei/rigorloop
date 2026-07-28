# Boundary-First Architecture Review R3

Review ID: architecture-review-r3
Stage: architecture-review
Round: 3
Reviewer: Independent architecture reviewer
Target: docs/architecture/system/architecture.md
Companion ADR: docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md
Status: changes-requested
Material findings: PBF-AR3
Immediate next stage: architecture revision
Plan readiness: not-ready

## Result

The two-state manifest, source-control baseline, existing adapter metadata,
read-only rollback, operator-owned external action, ADR supersession, and
complexity discipline pass review.

## Finding PBF-AR3

Finding ID: PBF-AR3
Severity: material
Location: docs/architecture/system/architecture.md, Risks and Technical Debt
Evidence: Three risk controls retain activation-time hashes, pre-activation
opt-in, and YAML mechanical-projection assumptions that the approved spec and
superseding ADR removed.
Required outcome: use the immutable full parent revision plus sorted eligible
paths, active-only opt-in, and validator-checked reviewed two-state manifest
without projection or writer semantics.
Safe resolution path: mechanically revise the three stale risk-table rows.
needs-decision rationale: none

## Review Dimensions

| Review dimension | Verdict |
| --- | --- |
| spec alignment | block |
| package shape | pass |
| boundary clarity | pass |
| data ownership | pass |
| interface safety | pass |
| runtime and failure handling | pass |
| deployment and execution boundaries | pass |
| security/privacy | pass |
| quality and operations | concern |
| testing feasibility | pass |
| complexity discipline | pass |
| ADR quality | pass |
| plan readiness | block |

## Recommendation

Revise the three stale risk controls and repeat architecture review.
