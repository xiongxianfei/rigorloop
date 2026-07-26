# Boundary-First Proof Modeling Plan Review R7

Review ID: plan-review-r7
Stage: plan-review
Round: 7
Reviewer: Codex plan-review skill with context-separated independent reviewer
Target: corrected M2 plan projection
Reviewed artifact: docs/plans/2026-07-25-boundary-first-proof-modeling.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-PL7-1
Immediate next stage: plan revision
Implementation readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact R7 plan candidate; accepted runtime ADR; plan-review R6 findings and resolutions
Manifest owner: workflow orchestrator

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: BFP-PL7-1
- Immediate next stage: plan revision

## Findings

### BFP-PL7-1 - Feature and protocol-item classification vocabularies are merged

Finding ID: BFP-PL7-1
Severity: major

Evidence:

- The plan applies the protocol-item categories to both feature rows and
  protocol items, losing the accepted ADR's distinct pre-turn semantics.

Required outcome:

Preserve separate closed exactly-once classifications for feature rows and
protocol items.

Safe resolution:

Classify feature rows as permitted built-in tool, permitted non-tool runtime
behavior, or must-be-disabled tool-bearing behavior. Classify protocol items
as permitted side effect, non-side-effect protocol traffic, or prohibited
capability event. Test each mapping independently.

## Prior-Finding Reconciliation

BFP-PL6-1 and BFP-PL6-3 are resolved. BFP-PL6-2 is otherwise resolved; exact
tools and negative mapping contrasts remain present.
