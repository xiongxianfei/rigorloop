---
id: "rem:practice:existing"
type: "practice"
basis_kind: "REM-authored synthesis; current REM rules apply; sources qualified below"
---

# Review an existing system

## Key takeaway

Reconstruct what the system demonstrably does before treating its current structure as intended, approved or correct.

## Summary

Use this Practice when documentation is incomplete, current behavior is disputed or a change requires a reliable starting account. It separates observed implementation, documented intent, inferred rationale and proposed improvements. Existing names and code paths are evidence to inspect, not automatic architectural truth.

## Goal and prerequisites
Produce a bounded account useful for a stated decision. Obtain permitted access to relevant documentation, implementation, operational observations and responsible people. Do not run disruptive tests without authorization. An absent document may mean missing evidence rather than absence of a requirement.

Local terms: a requirement is an obligation; a Function is logical behavior; a Module is responsibility; a realization is its technical implementation; a claim is what you believe the system does. A baseline/reference identifies the version and context under review.

## Stage map
1. Bound the review and identify available evidence.
2. Recover needs, obligations and actual behavior.
3. Reconstruct responsibilities and interactions.
4. Compare claims with applicable evidence.
5. Decide what to retain, investigate or change.

## Stage 1 — Bound the review
### Stage summary
**Goal:** know what is being reviewed. **Why:** evidence from several versions can create a fictional system. **Do:** identify scope, version, decision and access limits. **Observe:** missing authority and conflicting sources. **Success:** a bounded review plan. **Next:** collect claim-relevant evidence.

Describe the real question, such as whether current publication supports the newly proposed fault condition. List the documents, builds, configurations and people available. Identify which statements are approved, historical or merely descriptive. Keep access limitations visible. If source code is unavailable, do not assert an implementation design from the README alone.

**Fallback:** narrow the claim to what can be inspected or request appropriate access; do not complete gaps from a familiar architectural pattern.

## Stage 2 — Recover intent and observed behavior
### Stage summary
**Goal:** distinguish what was wanted from what exists. **Why:** implementation can embody an obsolete decision. **Do:** trace requests and obligations, then observe relevant use. **Observe:** inferred intent and untested behavior. **Success:** separate accounts with gaps. **Next:** reconstruct collaboration.

Preserve actual wording and origins of obligations. Ask which user outcome explains each important behavior. Where the history is missing, label your explanation as inferred. Describe a normal and meaningful failure Scenario at the system boundary. Compare it with documented requirements and available observations; a code path's existence does not establish its executed result.

For a REM model, inspect each SR’s single IR parent, each AR’s single SR parent and acyclic parentage. Check all seven 5W2H questions and the per-IR/SR consequential-question limit without concealing unresolved issues. A Scenario has one owning IR; a confirmed Scenario has one primary Feature confirmed by that IR and informs SRs or records a no-new-obligation conclusion. Check IR/Feature/Scenario coverage before calling the analysis complete. Missing links are gaps to investigate, not permission to invent traceability or retrospectively confirm a Scenario.

**Fallback:** if current behavior and intent disagree, record the conflict. Do not silently rewrite the obligation to match what the product happens to do.

## Stage 3 — Reconstruct responsibility and interaction
### Stage summary
**Goal:** explain how contributions fit together. **Why:** folders, processes and responsibility need not coincide. **Do:** identify logical actions, agreements and realization mappings. **Observe:** hidden assumptions and missing integration guarantees. **Success:** a checkable walkthrough. **Next:** evidence review.

Describe Functions by inputs, effects and failure behavior. Propose responsibility boundaries only as a hypothesis when authority is unknown. Inspect caller/provider assumptions about success, partial completion, version, retry and visibility. Distinguish a parent's own agreement from exposing a child's agreement. Walk the Scenario through the collaboration, explicitly marking unconfirmed steps.

Before calling System Design complete, inspect each approved SR’s relevant Function coverage and each Feature’s realization by confirmed Functions. Before calling allocation complete, check one accountable primary Module per active Function, optional supporting Modules, and one allocated Module per active AR. Inspect Module containment for at most one parent and no cycles, and Interfaces for one provider and explicit exposure through every crossed provider-side ancestor. Distinguish provider accountability from implementation contributions, and keep material realization under the responsible Module or Interface.

Compare these rules with observed relationships; label absent or conflicting facts instead of manufacturing compliant owners. Tailor Logical, Process, Development, Physical and Scenario presentations with explicit coverage and reasons for omission or combination, retaining material concerns and project-required views.

**Fallback:** when a diagram is more certain than its sources, weaken its labels. A dependency line is not proof of runtime order.

## Stage 4 — Compare the claims with evidence
### Stage summary
**Goal:** establish warranted conclusions. **Why:** plans and old tests may not apply to the current claim. **Do:** match claim, context, configuration and actual observation. **Observe:** unsupported scope expansion. **Success:** supported, contradicted and unresolved meanings are distinguishable. **Next:** prioritize action.

Separate model conformance from requirements validity, specified product conformance and intended-use success. Read the actual assessment scope rather than relying on “tests pass.” Identify relevant test/analysis configurations and anomalies. Check integration behavior where parts alone are insufficient. Assess whether the reviewed requirement itself is appropriate to intended use. An evidence gap is not proof of failure; a passing local test is not proof of the whole outcome.

**Fallback:** plan a discriminating assessment or narrow the claim. Preserve contradictory results for investigation.

## Stage 5 — Decide and update
### Stage summary
**Goal:** create an actionable current account. **Why:** reconstruction only helps if it changes the next decision. **Do:** separate factual corrections from proposed design changes. **Observe:** unapproved assumptions masquerading as decisions. **Success:** a bounded recommendation and next action. **Next:** an authorized change or another review.

Prioritize discrepancies by consequence. Correct descriptive mistakes where the evidence is clear, but obtain appropriate approval for obligations and design changes. Preserve old evidence and its scope. Record the current reference, assumptions requiring confirmation, required assessments and who can decide. Promote a reusable lesson into REM only with adequate reasoning and scope.

## Troubleshooting
If reviewers disagree, first compare configuration and claim meaning. If the system is inaccessible, publish an evidence-limited review rather than a complete reconstruction. If every discrepancy is called a defect, separate documentation error, changed need, unapproved implementation and failed obligation.

## Current review summary
Fill from actual work: reviewed scope/version; established intent; observed behavior; inferred architecture; unresolved gaps; applicable evidence; proposed changes; actual decision and next action. Nothing here asserts an inspected user implementation.

## Basis and deeper knowledge

This Practice is an authored synthesis of origin tracing, architecture reasoning and scoped assessment. [Gotel/Finkelstein](../references/gotel-finkelstein-1994-requirements-traceability-problem.md#located-contribution), NASA [requirements management](../references/nasa-2016-systems-engineering-handbook.md#requirements-management), [verification](../references/nasa-2016-systems-engineering-handbook.md#product-verification) and [validation](../references/nasa-2016-systems-engineering-handbook.md#product-validation), and [Kruchten](../references/kruchten-1995-architectural-blueprints.md#located-contributions) support those particular concerns. Deeper procedures: [Requirement Analysis](../methods/requirement-analysis.md), [Architecture Views](../methods/architecture-views.md), [Verification](../methods/plan-and-assess-verification.md) and [Intended-use validation](../methods/validate-stakeholder-outcomes.md). Current [Models](../models/README.md) own relationship rules and evolution, and the [supporting knowledge guide](understand-rem/README.md) explains their cooperation. This is not an audit certification or a substitute for domain-specific assurance.
