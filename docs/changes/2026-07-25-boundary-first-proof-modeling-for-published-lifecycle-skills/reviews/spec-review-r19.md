# Boundary-First Proof Modeling Spec Review R19

Review ID: spec-review-r19
Stage: spec-review
Round: 19
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: implementation-discovered skill-inventory amendment
Reviewed artifact: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR19-1, BFP-SR19-2
Immediate next stage: spec revision
Spec readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: focused inventory amendment and current runtime protocol schema
Manifest owner: workflow orchestrator

## Findings

### BFP-SR19-1 - Accepted skill-row classification is not deterministic

Finding ID: BFP-SR19-1
Severity: major

The amendment introduced closed logical roles without fixing the exact
`skills/list` request, accepted row predicates, scope values, empty-error
requirement, uniqueness rules, or collision-free normalization.

Required outcome: Define the exact request and mutually exclusive predicates
for manifested and runtime-system rows, then add valid-enum wrong-scope,
duplicate name/path, non-empty-error, wrong-CWD, stale-cache, and normalization
collision contrasts.

### BFP-SR19-2 - Complete inventory conflicts with optional system rows

Finding ID: BFP-SR19-2
Severity: major

The amendment made runtime-system rows optional while also requiring omission
to fail, without defining an authoritative roster or discovery algorithm.

Required outcome: Bind an exact system roster to an independent,
identity-bound source or make omission apply only to manifested skills.
