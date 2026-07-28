# Boundary-First Test Spec Review R8

Review ID: test-spec-review-r8
Stage: test-spec-review
Round: 8
Reviewer: independent Codex test-spec reviewer
Target: `specs/boundary-first-proof-model.test.md`
Reviewed artifact: commit 9a172d19
Review date: 2026-07-28
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: PBF-TSR8-1
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Finding

### PBF-TSR8-1

Finding ID: PBF-TSR8-1
Severity: major
Location: Input artifact identities
Evidence: The test spec still cites the R3 plan and plan-review identities,
while its corrected proof population relies on the approved R6 plan.
Required outcome: Identify the exact approved R6 plan and plan-review inputs.
Safe resolution path: Replace the two stale identity rows and repeat
test-spec review.
needs-decision rationale: none

## Prior-finding reconciliation

PBF-TSR7-1 is substantively resolved. Every adapter-included governed pair is
covered across all three target trees, while CMD9 owns applicability.
