---
id: "rem:practice:decision"
type: "practice"
basis_kind: "REM-authored synthesis; current REM rules apply; sources qualified below"
---

# Make an architecture decision

## Key takeaway

A useful decision record exposes the conditions under which the selected mechanism is preferable—and what would change the choice.

## Summary

This Practice turns a consequential architecture question into a bounded comparison and an explicit decision. It integrates stakeholder concerns, alternatives, mechanism reasoning, targeted evidence and actual authority. It is a practical REM synthesis, not the complete ATAM process or an automatic optimization procedure.

## Goal and local understanding
A quality concern is an outcome such as recoverability, performance or modifiability under conditions. A sensitivity is a design property that materially affects an outcome. A trade-off couples benefits and costs across concerns. A Module is responsibility; a component, process or storage system is a candidate realization.

Inputs are the decision to make, relevant obligations, constraints, existing design and available evidence. Determine who can decide. Avoid irreversible implementation work when the key requirement or authority is still unresolved.

## Stage map
1. Define the decision and consequences.
2. Make the comparison concrete.
3. Explain competing mechanisms.
4. Obtain the discriminating evidence.
5. Decide and state review triggers.

## Stage 1 — Define the decision
### Stage summary
**Goal:** distinguish need, constraint and choice. **Why:** “choose technology X” can hide the actual problem. **Do:** state the outcome and binding restrictions. **Observe:** unsupported preferences. **Success:** a bounded decision question. **Next:** scenarios.

Write what the system must accomplish and what freedom remains. Confirm which implementation constraints are mandatory and where their authority comes from. Describe the consequences of a wrong or delayed choice. Retaining the existing design is an option when it satisfies the need; novelty is not a criterion by itself.

**Fallback:** return to request reconciliation if stakeholders disagree about the outcome.

## Stage 2 — Make the comparison concrete
### Stage summary
**Goal:** define meaningful decision criteria. **Why:** abstract quality labels admit incompatible interpretations. **Do:** write representative stimulus, environment, response and measure where justified. **Observe:** fabricated numbers and missing concerns. **Success:** comparable scenarios. **Next:** alternatives.

For recovery, identify the fault and what remains observable afterward. For performance, specify workload and measurement conditions. For modifiability, name a plausible change and affected consumers. Separate actual measures from proposed targets needing agreement. Include the operational people affected, not just implementation convenience.

**Fallback:** keep an uncertain measure open and compare qualitatively at the supported level; do not create an arbitrary precision score.

## Stage 3 — Explain alternatives
### Stage summary
**Goal:** compare how designs produce outcomes. **Why:** a technology name does not specify its guarantees. **Do:** describe responsibilities, interactions, realization and assumptions for each feasible option. **Observe:** uneven detail and hidden cost. **Success:** credible competing arguments. **Next:** evidence.

Compare alternatives under current REM rules. Preserve single SR/IR and AR/SR parentage and the governed Scenario’s owning IR and primary Feature; the architecture walkthrough adds internal participation without rewriting that stakeholder Scenario. Complete System Design links each approved SR to relevant Functions. Complete allocation gives every active Function one primary accountable Module and every active AR one allocated Module, with supporting contributions distinct from ownership. Module containment is acyclic with at most one parent; each Interface has one provider and explicit exposure through each crossed provider-side ancestor. If an alternative needs a rule change, surface it as a separate proposal for the governing owner.

Use a short table of mechanisms, expected benefits, costs, risks and assumptions. Trace one normal and one failure Scenario through each. Inspect how boundary choices expose or hide likely changes. Include migration and operating cost when consequential. Identify what would fail first under an important changed assumption.

For release publication, “prepare then expose” may reduce partial-visibility reasoning, but the switch and reader behavior still need suitable semantics. Extra stored versions can create retention and cleanup work. These are conditional arguments, not measured outcomes.

Keep technical components, state authority and material mechanisms under the responsible Module or Interface; realization choices do not silently transfer accountability. Select Logical, Process, Development, Physical and Scenario presentations by the comparison question. Explain omitted or combined views and where their material concerns are covered; keep project-required views and derive presentations from the same authoritative facts.

**Fallback:** eliminate an option only for a stated infeasibility or constraint; do not caricature alternatives to justify a favored choice.

## Stage 4 — Obtain discriminating evidence
### Stage summary
**Goal:** reduce uncertainty that can change the choice. **Why:** more information about a non-critical detail may not help. **Do:** select an analysis, prototype, inspection or test. **Observe:** actual results and scope. **Success:** a narrower uncertainty or explicit remaining gap. **Next:** decision or targeted rework.

Write the competing predictions before the activity. Identify configuration and risk boundaries. If only planning is possible, retain expected results as expectations. If execution occurs, preserve observations and anomalies. Compare the actual task with the intended scenario. Stop research when it is sufficient for the bounded decision, not when every possible question is answered.

**Fallback:** if a major assumption remains unresolved, make a reversible provisional recommendation or postpone commitment under actual authority.

## Stage 5 — Decide and define reopening triggers
### Stage summary
**Goal:** make the reasoning maintainable. **Why:** a rational choice can become unsuitable when conditions change. **Do:** record choice, authority, alternatives, evidence and residual uncertainty. **Observe:** claims stronger than support. **Success:** a decision others can inspect. **Next:** implementation/assessment or additional inquiry.

State why this option is appropriate now. Record what is not established, including testing not performed. Identify affected requirements, Interface agreements and downstream assessments. Name triggers such as changed fault scope, workload, provider guarantee or a failed prediction. A decision to accept risk does not convert that risk into evidence of satisfaction.

## Review and current summary
Record actual question, constraints, chosen/provisional option, evidence inspected, authority, residual risks and next check. No example outcome is preapproved. If a future reviewer cannot identify what evidence would change the decision, the record may be a justification narrative rather than an analysis.

## Basis and deeper knowledge

The inspected [ATAM abstract](../references/kazman-2000-atam-method-for-architecture-evaluation.md#located-contributions) supports analysis of tradeoffs among quality concerns; it is not evidence for a complete ATAM procedure or a scoring scheme. [Parnas](../references/parnas-1972-criteria-for-decomposing-systems.md#located-contribution) supports examining change consequences when choosing boundaries. The local sensitivity questions, comparison procedure and five-stage integration above are REM-authored synthesis. See [Realization Design](../methods/realization-design.md), [Technical model and realization](../models/architecture-realization.md), [Architecture Allocation](../methods/architecture-allocation.md), [Module hierarchy and Interface exposure](../models/architecture-boundaries.md), [Architecture Views](../methods/architecture-views.md) and the separate [worked example — inspect responsibility offline](WORKED-EXAMPLE.md) for more depth.
