<!-- Generated from rem/methods/requirement-analysis.md; source SHA-256 6973551e7d8b2d709a8a99c4d819af049a3bdc0e25ea06e5c64cc0c78e5468e1. Edit the owning REM source. -->

# Requirement Analysis method

Use this method to reconcile an incoming Raw Requirement (RR) with current requirement knowledge, establish or refine clear IRs and verifiable SRs, and formulate ARs only when architecture is understood enough to make allocation meaningful.
The [requirement model](rem-models-requirements.md) owns hierarchy and relationship rules.
The method is independent of any skill, command, file format, review stage, or workflow host.
Apply all seven [5W2H](rem-methods-5w2h.md) questions at each durable requirement level, recording an answer, explicit unknown, or justified non-applicability for each.

## Analyze the RR against current needs

Start from the actual incoming source: a request, proposal, issue, incident, observation, or equivalent RR. Preserve its wording or attributable source well enough that later reasoning can be traced without treating the RR itself as an approved requirement.

Before creating an IR, inspect the applicable current IRs, SRs, governed Scenarios, Features, and known constraints. Separate the underlying need from a suggested solution, implementation preference, or proposed architecture. Determine whether each material part of the RR is already covered, refines an existing need or obligation, establishes a distinct durable need, contains several independent needs, or remains unresolved/conflicting on the available basis.

Do not create a new IR or SR merely because a new RR exists. Reuse an existing requirement when its meaning and scope already cover the need; refine it while preserving identity when the same requirement evolves; create a new IR only for a distinct durable need. Record a no-change, unresolved, or conflict disposition when that is the truthful result.

## Establish or refine the initial requirement

Apply [5W2H](rem-methods-5w2h.md) to every IR created or materially refined by the analysis.
Use existing project intent and stakeholder evidence as inputs, while distinguishing needs from current implementation choices.
Record material unknowns and avoid manufacturing thresholds, stakeholders, or approval.

The IR statement expresses who needs what outcome and why it matters, with relevant scope and conditions.
The analysis supports that statement; What explains the problem and desired outcome, while the other questions establish its basis and context.
Keep provisional assumptions distinct from established constraints, and assess unresolved issues from any part of the analysis using the open-question rule below.

After the initial 5W2H analysis is coherent enough to reason about stakeholder use, apply [Scenario Analysis](rem-methods-scenario-analysis.md).
The IR confirms the stakeholder-visible Feature and first-class governed Scenarios used to analyze that capability.
Scenario identity, lifecycle, and black-box rules are owned by the [Scenario model](rem-models-scenarios.md).
Scenario Analysis may expose candidate logical behavior, but Functions are confirmed through SR and [Functional Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/functional-analysis.md), not by the Scenario alone.
Before IR analysis is considered complete, the IR MUST confirm at least one durable Feature, and each confirmed Feature introduced or materially extended by that IR MUST be exercised by at least one confirmed Scenario owned by the IR.

## Keep one consequential open question

Each IR and SR may retain at most one open question; retain none when the available sources and analysis settle the need or obligation.
A valuable question identifies a specific unresolved decision or missing evidence that materially affects the requirement's meaning, scope, derivation, or acceptance.
Make clear what answer or evidence would resolve it. Do not manufacture a question solely to populate a field or ask for detail that does not affect an engineering decision.

Resolve what can be established from the available sources before selecting the question that matters most.
If several independent issues remain, continue the analysis and resolve them before treating the record as sufficiently defined; decompose a mixed need or obligation only when its engineering meaning justifies separate requirements.
Do not concatenate independent questions into one entry or conceal unresolved issues to meet the limit.
The supporting analysis must remain candid about uncertainty, and dependent decisions remain provisional until their basis is settled.

This limit applies to IRs and SRs. The representation may keep an empty or single-item list; its schema can check cardinality and nonblank content, while engineering review judges the question's value.

## Name the initial requirement

An IR name must identify a concrete need or desired outcome and the subject it concerns.
Prefer a short outcome phrase that a reader can understand without opening the full record.
An action and its object often make that meaning clear; a precise noun phrase is acceptable when equally clear.
Add a distinguishing condition or context when the outcome and subject alone could be confused with another need.
For example, "Preserve engineering knowledge across sessions" names the outcome, subject, and relevant context.

| Too vague or prematurely technical | Clearer need-oriented name |
| --- | --- |
| Durability | Preserve engineering knowledge across sessions |
| Traceability | Trace engineering obligations and responsibilities |
| Change management | Control engineering changes and recover prior states |
| Verification | Assess engineering claims using applicable evidence |
| Use Git | Recover retained engineering baselines |

These are naming examples, not additional requirements.
Do not substitute a named Feature, Module, tool, delivery task, or implementation solution for the stakeholder need.
A genuine mandated technology constraint can appear when its source and necessity are established.

Review the name using three questions:

1. Can the reader identify the subject and intended outcome?
2. Does the name distinguish this need from neighboring IRs?
3. Does it match the statement without promising broader scope or prescribing an unsupported solution?

Renaming an IR preserves its stable identity.
Refining a title does not silently change the obligation, approve the IR, or renew verification evidence.
Recheck the title against its statement and 5W2H analysis whenever either changes.

Names in the engineering model remain distinct from physical storage labels.
[Operational Support](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/operational-support.md#naming-and-location) defines how a project represents names and updates locations.
The analysis method does not prescribe a directory structure or require an extra abbreviation of the title.

## Derive system requirements

Translate each reconciled IR and its supported Scenarios into independently assessable system obligations.
State the required outcome and the relevant conditions, then describe observable acceptance criteria.
Apply 5W2H to each SR's system obligation, using the parent IR as context and answering at the system level.
Resolve or explicitly retain gaps in actors, scope, timing, quality, and quantities.

Derive each SR under exactly one parent IR.
References to related concerns do not establish another parent.
Separate behavior from rationale and distinguish a required constraint from an implementation possibility.
Use implementation-independent language unless the implementation itself is required.

An acceptance criterion describes what an assessment should observe.
It does not claim that verification has occurred or that the requirement is satisfied.
Give each SR a name that identifies its specific obligation; a clear outcome phrase or precise noun phrase is appropriate.

After accepting the requirement basis, use [Functional Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/functional-analysis.md) to identify the logical behavior required to satisfy each approved SR and confirm its corresponding Functions in System Design.
Requirement approval does not require those Functions or architectural allocations to be complete. Record remaining design obligations explicitly.
Before System Design for an approved SR is considered complete, it must confirm at least one relevant Function under the [System Design model](rem-models-system-design.md#function-relationships).
Reuse an existing Function when it already represents the required behavior.
Do not create a Function merely to mirror the requirement tree; SR-to-Function relationships may be many-to-many.

The SR remains the normative obligation.
Functional Analysis owns the behavior boundary, Feature-to-Function reconciliation, and Function quality criteria.
Requirement Analysis must not allocate Modules while deriving the SR.

## Formulate allocated requirements with architectural context

AR formulation is not a prerequisite for System Design. Develop or refine ARs only after architectural responsibilities are understood sufficiently to make the lower-level obligation and its accountable boundary meaningful. In the normal REM engineering cycle, [Architecture Allocation](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/architecture-allocation.md) provides that context and invokes these requirement-quality rules while deriving and allocating ARs.

For each AR, state the lower-level obligation, retain exactly one parent SR, and allocate the AR to exactly one accountable Module. Apply 5W2H to that allocated obligation, including its responsible parties, operating conditions, boundaries, and limits. Check it against the Functions, state, policies, Interfaces, and encapsulation boundary assigned to that responsibility.

If one lower-level obligation would require several accountable Modules, decompose it into separate ARs under the same parent SR. Do not create an AR merely to fill a tree level or invent a Module to finish a worksheet. Reconcile AR allocation with Function allocation through [Architecture Allocation](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/architecture-allocation.md). An allocation change can expose a missing or incorrect SR and require requirement refinement; preserve the historical meaning of previous states. Give each AR a name that makes its allocated obligation understandable within the architectural context.

## Reconcile and review

Read the name, statement, analysis, acceptance criteria, and source basis together.
Resolve disagreement between them or leave the unsettled point explicit in the draft.
When using existing contracts, preserve their identities and distinguish related source material from an actual obligation transfer.

The output is a requirement draft with explicit analysis and assessment intent.
Approval, implementation, and satisfaction remain separate decisions and observations.
