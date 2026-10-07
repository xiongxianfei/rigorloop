<!-- Generated from rem/practices/engineer-a-change.md; source SHA-256 c43c02846abf258f826989381db272731460dd2f77955eccc810930e00a00a3d. Edit the owning REM source. -->

---
id: "rem:practice:change"
type: "practice"
basis_kind: "REM-authored synthesis; current REM rules apply; sources qualified below"
---

# Engineer a bounded change

## Key takeaway

Carry one real outcome from request through design and assessment, while keeping assumptions, authority and evidence explicit.

## Summary

This is REM’s main operating Practice. It combines request reconciliation, requirements reasoning, behavior, architecture, assessment and change review. Each stage contains enough information to perform the local work without opening another file. The stages are revisitable decision contexts, not a mandatory waterfall, project schema or approval lifecycle.

## Goal, inputs and use boundary
Use this Practice for a new capability, defect correction or material engineering change. Begin with an incoming request or observation, relevant current definitions, known implementation information and the people able to clarify or authorize consequential choices. No supplied project data is assumed correct merely because it uses REM names.

Local vocabulary: **RR** means Raw Requirement, an input; **IR** means Initial Requirement, a durable need; **SR** means System Requirement, an obligation on the system; **AR** means Allocated Requirement, a narrower architectural obligation. A **Feature** is a capability, a **Function** logical behavior, a **Module** responsibility and an **Interface** an interaction agreement. These meanings are methodological vocabulary, not mandatory machine record types.

## Stage map and entry routes
| Stage | Output useful to the next decision |
|---|---|
| 1. Bound the change | Goal, authority, current reference and significant unknowns |
| 2. Reconcile need and input | Need, constraints, suggestions and origin trail |
| 3. Make outcomes assessable | Scenarios and candidate obligations with rationale |
| 4. Explain behavior | Logical contributions and appropriate coverage |
| 5. Allocate and compose | Responsibilities, agreements and integration argument |
| 6. Compare realization | Bounded technical choice and concern-specific views |
| 7. Assess at the available maturity | Plans or actual scoped evidence and judgments |
| 8. Decide, update and learn | Authorized action, current reference and next review |

An implementation defect can start with observation and Stage 7, then return to the requirement or design ambiguity it reveals. A changed operational assumption can start with Stages 1 and 8. Do not manufacture missing earlier approvals to follow the route.

## Stage 1 — Bound the change
### Stage summary
**Goal:** establish the outcome and permitted work. **Why:** a coherent technical response can still solve the wrong problem or exceed authority. **Do:** describe the change, boundary and relevant current reference. **Observe:** missing stakeholders, unavailable implementation evidence and irreversible commitments. **Success:** a bounded next decision. **Next:** reconcile the input, or first resolve authority/scope blockers.

### Procedure and understanding
Write what prompted the work and what would be different if it succeeded. Identify affected users, system/environment boundaries and existing obligations. Name the actual source of constraints and decision authority; leave them unknown if not established. Separate an observation from a diagnosis. “A reader received mixed content” is different from “the database is wrong.”

List material unknowns and prioritize the one that can most change the next action. Keep all material Change-level unknowns visible. For each IR and SR, retain at most one consequential open question: resolve the others through analysis before treating the requirement as sufficiently defined, or separate mixed obligations only when their meaning justifies it. Never hide or concatenate independent issues to meet the limit; dependent choices stay provisional. Scale effort to consequence: a reversible wording clarification needs less design analysis than a change to a safety or recovery guarantee.

### Check and fallback
If no one can explain the intended outcome, stop solution selection and clarify. If actual source code or contracts are unavailable, state that limit and keep conclusions at the proposal level.

## Stage 2 — Reconcile the need and the input
### Stage summary
**Goal:** distinguish intent from means. **Why:** a request can mix legitimate constraints with replaceable suggestions. **Do:** retain the wording, separate meanings and compare existing obligations. **Observe:** duplicates and conflicts. **Success:** a justified interpretation. **Next:** scenarios and obligations, or clarification/no change.

### Procedure and understanding
For each significant statement, write the apparent need, context, proposed solution and assumptions separately. Ask which restrictions are binding and why. Compare the meaning with existing needs and capabilities before creating a new obligation. Record the origin and the reason for retaining, clarifying, changing or declining the request.

For “Use a database so I can retrieve the reviewed release,” retrieval is a need and database is a suggestion unless its authority is established. Questions about which release and what “reviewed” means can matter more than the storage choice. Account for all seven 5W2H questions for every IR, SR and AR: who, what, why, where, when, how and how much. Record a supported answer, an explicit unknown or justified non-applicability for each at that requirement’s level. No separate worksheet or fixed field layout is required; references to authoritative answers avoid duplication.

### Check and fallback
Confirm consequential interpretations with appropriate stakeholders. A well-phrased rewrite is not authorization. If an imposed technology is confirmed, retain that constraint rather than treating all solution language as a defect.

## Stage 3 — Make the outcome concrete and assessable
### Stage summary
**Goal:** connect need to obligations. **Why:** design and assessment require shared meaning. **Do:** describe a normal and relevant alternate Scenario, then candidate requirements. **Observe:** hidden assumptions and invented precision. **Success:** understandable obligations with assessment paths. **Next:** behavior/design or further need clarification.

### Procedure and understanding
Describe actor, context, trigger, boundary-visible interaction and result without internal implementation names. Add significant failure or degraded conditions. Identify a durable capability where it helps, then state the system obligation: subject, conditions, required outcome and any agreed measure. Keep rationale and assumptions alongside the statement.

Use IR for the durable need and SR for the system obligation. Each SR has exactly one parent IR; each later AR has exactly one parent SR, with acyclic parentage. Source and coverage references may be many-to-many without creating additional parents. An SR can concern behavior, performance, Interface, environment or structure. Ask how it would be evaluated by inspection, analysis, demonstration or test. Do not invent numerical thresholds or force every obligation through a new Function. Requirements validation asks whether these are appropriate obligations, not whether a product already meets them.

Each Scenario has exactly one owning IR. A confirmed Scenario exercises exactly one primary Feature confirmed by that IR; before Scenario Analysis is complete it informs at least one SR or has an explicit no-new-obligation conclusion. Before IR analysis is complete, the IR confirms at least one durable Feature and each confirmed Feature has an owned confirmed Scenario exercising it. Keep the Scenario at the stakeholder boundary; internal participation belongs in a derived architecture walkthrough.

### Check and fallback
Look for conflicting terms, missing alternative outcomes, infeasible promises and an assumption treated as a guarantee. If “complete release” or the fault domain is unclear, resolve that before claiming recovery design adequacy.

## Stage 4 — Explain behavior and coverage
### Stage summary
**Goal:** identify the logical contributions. **Why:** capability, obligation and code structure are different. **Do:** describe Functions and appropriate coverage arguments. **Observe:** missing effects and artificial behavior labels. **Success:** meaningful contributions, not merely links. **Next:** responsibility analysis.

### Procedure and understanding
From the Scenario, identify what the system observes, transforms, decides and communicates. For each useful Function, state triggers, inputs, outputs/effects and failure behavior. Reuse existing behavior when its meaning matches. Do not infer execution order from a static dependency path.

Explain how Functions contribute to requirements. For an architectural constraint such as “the core library is independent of an optional adapter,” an inspection of dependencies can be the appropriate route; there need not be a Function called “be independent.” Before System Design for an approved SR is complete, it confirms at least one relevant Function whose behavior the obligation governs. Reuse real governed behavior for a quality or structural constraint, and leave a missing coverage argument explicit. Each completed Feature design is realized by at least one confirmed Function; inspection evidence does not replace these design relationships. Keep stakeholder Scenarios separate from the architecture walkthrough that assigns these behaviors to responsibilities.

### Check and fallback
If a proposed Function has no understandable effect, clarify or remove it. If behavior cannot meet a requirement under current assumptions, revisit the obligation or design rather than adding a decorative trace.

## Stage 5 — Allocate responsibility and analyze interactions
### Stage summary
**Goal:** make the whole outcome someone’s coherent engineering concern. **Why:** good parts can compose badly. **Do:** propose boundaries, narrower obligations and Interface agreements. **Observe:** missing guarantees and circular assumptions. **Success:** an inspectable integration argument. **Next:** technical alternatives or boundary revision.

### Procedure and understanding
Group responsibilities around coherent obligations and likely change. Give each active Function exactly one accountable primary Module before allocation is complete, with zero or more supporting Modules. Allocate each active AR to exactly one Module and retain exactly one parent SR. If a lower-level obligation spans several accountable Modules, split it into separate ARs under the same SR. Derive ARs where lower-level responsibility is needed, not to fill a tree; explain how they combine toward the SR.

Function and AR allocation are separate relationships that must agree about behavior, state, policy and obligations. Choose the lowest Module that coherently owns the complete responsibility; a parent’s roll-up visibility does not add another owner. A Module has at most one parent, with acyclic containment; each level must express responsibility rather than a folder or arbitrary depth rule.

For each consequential interaction, describe accepted input, effect, success meaning, failure behavior and assumptions about order, version or availability. Each Interface has exactly one provider Module and zero or more consumers. Distinguish a parent-owned agreement implemented internally from a child-owned agreement deliberately exposed to callers. A child-provided Interface crossing containment boundaries must be explicitly exposed through every intervening provider-side parent boundary; exposure preserves its identity and provider. Implementation participation does not transfer contract accountability. Walk one normal and one relevant failure Scenario through the proposed collaboration.

In the release example, Builder can establish content validity and Store can preserve accepted content, while Reader selects and reports a release. Their individual guarantees still leave a question about publication visibility and selection consistency. That gap belongs in the integration argument, not behind ownership labels.

### Check and fallback
A promise that every participant assumes another provides is a gap. Revise the boundary, agreement or system obligation. Escalate real safety/security concerns to appropriate expertise instead of guessing a contract.

## Stage 6 — Select a bounded realization and explain the views
### Stage summary
**Goal:** choose an implementable approach at justified confidence. **Why:** several designs can satisfy the same need with different trade-offs. **Do:** compare mechanisms under relevant quality scenarios. **Observe:** untested benefits, hidden costs and incompatible constraints. **Success:** a scoped choice and next evidence. **Next:** assessment planning/execution or another experiment.

### Procedure and understanding
Separate fixed constraints from preferences. Compare feasible alternatives at similar detail, including keeping the current approach when viable. For each, describe mechanism, assumptions, expected quality effects, cost and uncertainty. Name the next test or analysis that could change the choice.

Logical responsibility is not physical placement. A library, service or database name is insufficient: explain data, ordering, failure and reader behavior needed for the claim. Keep material realization information under its Module or Interface owner; technologies and components do not acquire first-class REM identity merely by being named. Select presentations using the Logical, Process, Development, Physical and Scenario concern vocabulary. Record why a view is omitted or combined and where its material concerns are covered; retain project-required views. Derive presentations from the authoritative semantic facts, with source state and projection meaning explicit. Label what is proposed versus observed and define relationship meaning; a diagram cannot establish atomicity or performance by itself.

### Check and fallback
If the decisive mechanism is unknown, record a provisional option and an investigation, not a settled result. If a threshold or preference lacks authority, obtain it rather than constructing a spurious weighted score.

## Stage 7 — Plan and perform appropriate assessment
### Stage summary
**Goal:** determine what is actually warranted. **Why:** plan, evidence, verification and intended-use validation differ. **Do:** state claims and conditions, then plan or execute only at the available maturity. **Observe:** anomalies and scope mismatches. **Success:** a defensible scoped conclusion. **Next:** revise, collect more evidence or seek a decision.

### Procedure and understanding
First check model conformance separately from whether the obligations are appropriate, the product satisfies them or intended use succeeds. Valid parentage and complete links alone establish none of those outcomes. For product verification, identify the obligation and relevant configuration. Describe the procedure, expected observations and coverage, then execute only with actual capability and authorization. Record what happened, including departures and anomalies. Do not replace missing observations with expected results.

For intended-use validation, ask whether relevant stakeholders can achieve the outcome in the operational context. A unit check on stored bytes does not establish that a reviewer can identify the reviewed release. Plan representative use, simulation, analysis or demonstration and record its limits. Keep requirements validation—the quality and necessity of the obligations—distinct from both product questions.

### Check and fallback
When no implementation exists, retain product-execution checks as plans and identify design risks. A performed inspection or analysis can support a scoped design conclusion when its subject, premises, method and limits are available; it does not establish an unobserved product outcome. If a result applies to a narrower fault domain or older configuration, restrict the conclusion. A waiver or risk acceptance is not satisfaction.

## Stage 8 — Decide, update the reference and learn
### Stage summary
**Goal:** preserve a usable current account without rewriting history. **Why:** later changes affect meaning and evidence applicability. **Do:** document the authorized action, affected knowledge and next review. **Observe:** stale views and unresolved acceptance. **Success:** current scope and remaining questions are explicit. **Next:** operate, assess or return to the affected stage.

### Procedure and understanding
Present the current claim, evidence, assumptions, gaps and residual risks to the actual authority. Record what is decided and what is not. Update requirements, design descriptions and views affected by the meaning change. Preserve historical observations and identify the current baseline/reference in the project's existing mechanism. Author each semantic fact once and derive inverse references and views; physical stores may differ without becoming competing semantic authorities. Current definitions must be understandable without replaying change history, and later interpretations must not rewrite earlier observations.

Record one learning item at the right level: a mistaken assumption, missing distinction, weak Model, ineffective Method or bad orchestration. Do not create a universal Principle from one outcome. When a source or upstream explanation changes, revisit local summaries as well as links.

### Check and fallback
A release note is not evidence of product quality. If a change extends the claim, examine earlier evidence applicability. If authority is absent, retain the proposal rather than manufacturing acceptance.

## Cross-stage troubleshooting
| Symptom | First check | Next action |
|---|---|---|
| Requirements are multiplying | Duplicate meaning, solution preferences, missing source trail | Reconcile before decomposing further |
| Every diagram looks complete but the outcome is unclear | Trace contribution versus satisfaction; actual stakeholder Scenario | Walk a normal and failure interaction |
| Parts pass but integration fails | Caller/provider assumptions, ordering, failure contracts | Revisit Stage 5 and revise the assessment |
| A decision cannot be closed | Missing evidence versus missing authority or preference | Identify the actual blocker, not more generic analysis |
| Old results are reused after a change | Claim meaning and configuration applicability | Limit the conclusion and plan new evidence |

## Current Practice summary — complete only from actual work
Record: current goal and reference; established facts; candidate decisions; unresolved assumptions; actual evidence and its scope; authorized action; next review. No project execution, approval or result is prefilled in this publication. A compact record is enough when it answers those questions.

## Basis, limits and deeper knowledge

NASA [requirements definition](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S01.md), [requirements management](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S03.md), [verification](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S04.md), [validation](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S05.md), [integration](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S16.md) and [Interface management](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S17.md) support the corresponding engineering concerns. [Zave/Jackson](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S12.md) informs conditional satisfaction; [Parnas](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S10.md) informs boundary reasoning; [Gotel/Finkelstein](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S13.md) informs origin traceability; [Kruchten](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S11.md) informs views; the inspected [ATAM abstract](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S14.md) supports examining quality tradeoffs. Exact REM rules and the orchestration above are REM-authored, not source-prescribed or empirically validated.

The [worked example — inspect responsibility offline](rem-practices-WORKED-EXAMPLE.md) applies current rules through a bounded design and unexecuted assessment plans. The release-publication passages above are separate illustrative fragments, not a completed product design. Deeper procedures: [Requirement Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/requirement-analysis.md), [5W2H](rem-methods-5w2h.md), [Scenario Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/scenario-analysis.md), [Functional Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/functional-analysis.md), [Architecture Allocation](rem-methods-architecture-allocation.md), [Architecture Design](rem-methods-architecture-design.md), [Realization Design](rem-methods-realization-design.md), [Architecture Views](rem-methods-architecture-views.md), [Verification](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/plan-and-assess-verification.md) and [Intended-use validation](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/validate-stakeholder-outcomes.md). [Evolution](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/README.md#evolution) governs current and historical meaning; [Operational Support](rem-models-operational-support.md) governs representation. These links supply depth; the operating route is above.
