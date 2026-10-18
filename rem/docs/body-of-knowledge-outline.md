# REM body of knowledge outline

## Key takeaway

Use the engineering question to identify what must be understood and what the reader should be able to do, then locate the explanations and remaining gaps.

## Summary

This draft proposes the subject coverage for applying REM to bounded software-intensive engineering work.
It develops requirements analysis in detail and identifies the intended depth of neighboring subjects.
The grouping is REM-authored synthesis, informed by the sources below; it is not a complete systems-engineering syllabus or an assertion that the current explanations achieve every outcome.
Current rules remain with their [Concept, Principle, Model and Method owners](../README.md#contents-and-ownership).
The [operating Practices](../practices/README.md) supply activity sequences, and [Understand REM](../practices/understand-rem/README.md) explains how those owners cooperate.

## Reader, scope and depth

The intended readers are engineers, reviewers and engineering agents who can describe a software-intensive system and inspect a small set of existing project definitions.
Readers new to REM need local explanations of its vocabulary; familiarity with the originating conversation, RigorLoop CLI or a particular representation is not assumed.
The target capability is to explain and prepare a bounded change from need through design and assessment while preserving attributable decisions and uncertainty.
Awareness of downstream work does not imply competence to perform every specialist task.

The selected scope includes normal, alternative and failure outcomes; relevant quality and interface constraints; current versus historical knowledge; and limits on engineering claims.
Specialized safety certification, regulatory compliance, detailed hardware design, comprehensive project management and product-specific programming instruction are outside this outline.
A project may require those subjects; their omission here cannot waive its obligations.
REM partial-adoption conformance levels remain undefined in the [current overview](../README.md#open-refinements).

## Source structure and adaptation

| Basis | Inspected contribution and selection | Boundary |
| --- | --- | --- |
| [NASA Systems Engineering Handbook, Revision 2](../references/nasa-2016-systems-engineering-handbook.md#subject-coverage-and-stakeholder-expectations) | Chapter 4 separates stakeholder expectations, technical requirements, logical decomposition and design solutions; chapters 5 and 6 identify realization and crosscutting management subjects. Selected requirements passages inform the detailed slice. | This outline reorganizes those concerns for REM readers. NASA terminology, lifecycle, approval arrangements and the complete chapter population are not adopted. The selected chapters are one source family. |
| [REM source map](../SOURCES.md) | Existing scoped contributions from Zave/Jackson, Gotel/Finkelstein, Parnas, Kruchten, ATAM and PROV support assumptions, traceability, decomposition, views, trade-offs and provenance. | Those records retain their stated inspection limits; linking them here is not a new full-text assessment or a claim that they prescribe REM. |
| [KPS Core 11.0.0 at the inspected revision](../references/kps-11-knowledge-practice-system.md) | Guidance on capability-oriented subject coverage, meaningful overlap, locally usable explanations and separate coverage/usability/source-fidelity review. | Editorial guidance consulted for this proposal; REM's declared KPS basis and authoring compatibility remain as stated in [metadata](../metadata.md). |

The eight areas below separate need, obligation, behavior, responsibility, realization, assurance, evolution and supporting knowledge management because readers need to reason about their different claims.
They do not form eight lifecycle gates or replace the five knowledge-role folders.
Requirements can constrain later design; design can reveal a missing obligation; assessment can return a correction to either owner.
Evolution preserves what those decisions meant, and Operational Support makes the information usable throughout.

## Overall outline

| Subject area | Topics and connection to the rest of REM |
| --- | --- |
| [Stakeholder needs and context](#stakeholder-needs-and-context) | Incoming requests, affected parties, desired outcomes, constraints and environmental assumptions establish the context for obligations. |
| [Requirements and scenarios](#requirements-and-scenarios) | Reconciliation, need/obligation distinctions, Features, black-box Scenarios, derivation, quality criteria and uncertainty establish what needs to be satisfied. |
| [Logical behavior](#logical-behavior) | Functions, behavioral boundaries, Feature realization and failure behavior explain how system behavior addresses obligations. |
| [Architecture and interfaces](#architecture-and-interfaces) | Responsibility, allocation, containment, interaction contracts, quality trade-offs and views connect behavior to accountable boundaries. |
| [Realization and integration](#realization-and-integration) | Technical mechanisms, deployment, integration and transition connect the architecture to an actual system and its operating context. |
| [Verification and intended-use validation](#verification-and-intended-use-validation) | Criteria, observations, assumptions and scoped judgments distinguish specified conformance from stakeholder success. |
| [Evolution and provenance](#evolution-and-provenance) | Identity, change impact, baselines, retirement and source history keep current decisions and earlier evidence interpretable. |
| [Operational support and improvement](#operational-support-and-improvement) | Representation, guidance selection, uncertainty in decisions and learning from use support the other areas. |

## Reading coverage descriptions

Coverage describes the local explanation available for the stated task, not a learner result or review approval.
**Partial** means a named explanation contributes but a specific account or worked application is still missing.
**Source only** means a publication contribution is recorded but the corresponding local teaching content has not been identified.
**Missing** means neither has been identified for the stated depth.
**Covered at stated depth** requires a content assessment against that depth; no row below claims that assessment has been completed.
Outside the detailed requirements slice, the gaps are provisional development questions requiring focused inspection before authoring.

## Stakeholder needs and context

The [NASA stakeholder-expectations contribution](../references/nasa-2016-systems-engineering-handbook.md#subject-coverage-and-stakeholder-expectations) motivates identifying affected parties, outcomes, assumptions and constraints.
REM's RR-to-IR reconciliation is its own application of these concerns.

| Topic | Understand | Be able to do | Existing explanations and gaps |
| --- | --- | --- | --- |
| Incoming need and solution suggestion | A request is evidence about a need; its preferred technology is not automatically a binding constraint. | Separate source wording, desired outcome, suggested solution and actual restriction in one request. | **Partial:** [RR concept](../concepts/requirement-input.md), [Requirement Analysis](../methods/requirement-analysis.md#analyze-the-rr-against-current-needs). Add a contrasting example in which the suggested mechanism is optional and another in which an attributable constraint makes it mandatory. |
| Stakeholders and decision authority | The requester, affected users, maintainers and decision owner can have different interests. | Identify whose answer is needed to settle an ambiguous outcome and explain why the analyst cannot invent it. | **Partial:** [5W2H](../methods/5w2h.md), [Engineer a change](../practices/engineer-a-change.md#stage-1--bound-the-change). Develop a local case that exposes an omitted affected party and a decision requiring their input. |
| Boundary and environmental assumptions | A system obligation and an assumption about its environment have different control and evidence needs. | Explain a condition under which correct specified behavior would still fail the intended outcome. | **Partial:** [Domain-assumption Principle](../principles/satisfaction-depends-on-domain-assumptions.md), [Requirements Model](../models/requirements.md). Connect the distinction to the pilot's offline snapshot and its potentially outdated ownership information. |

## Requirements and scenarios

This is the detailed pilot slice: reconcile an RR with existing knowledge and derive assessable system obligations.
[NASA requirements definition](../references/nasa-2016-systems-engineering-handbook.md#requirements-definition) informs rationale and quality, while [requirements management](../references/nasa-2016-systems-engineering-handbook.md#requirements-management) informs traceability and controlled change.
The exact IR/SR/AR hierarchy, Scenario ownership, seven-question analysis and open-question limit are REM selections.

| Topic | Understand | Be able to do | Existing explanations and gaps |
| --- | --- | --- | --- |
| Reuse, refinement and creation | Identity follows the continuing need or obligation; a new request need not create a new requirement. | Compare the request with supplied existing meanings and justify reuse, identity-preserving refinement, distinct creation or unresolved disposition. | **Partial:** [Reconciliation method](../methods/requirement-analysis.md#analyze-the-rr-against-current-needs). The [worked example](../practices/WORKED-EXAMPLE.md#reconcile-the-request) assumes a missing capability and creates one; add contrasts for covered and changed needs. |
| Need, system obligation and allocated obligation | IR describes a need, SR an obligation on the system, and AR a lower obligation allocated with architectural context. Parentage is distinct from related-source references. | Explain why a candidate belongs at one level and why deriving an SR does not require inventing a Module or AR. | **Partial:** [Requirements Concepts](../concepts/requirements.md), [Requirements Model](../models/requirements.md#containment). Add a connected example deriving the system obligation before allocation is known. |
| Requirement analysis and uncertainty | The statement carries the obligation; 5W2H explains its context. Unknown, assumption and justified non-applicability differ. | Address all seven questions for an IR and SR without fabricating a threshold; keep independent unresolved issues visible and dependent work provisional. | **Partial:** [5W2H](../methods/5w2h.md), [open-question rule](../methods/requirement-analysis.md#keep-one-consequential-open-question). Add a case where analysis must continue rather than hiding several issues in one question; the external basis of the named technique needs targeted source work. |
| Features and black-box Scenarios | A Feature is a durable capability; a Scenario describes one stakeholder situation exercising it. Neither is an internal call sequence. | Reuse or define a Feature, describe normal and material failure outcomes, and explain one owning IR and one primary Feature per confirmed Scenario. | **Partial:** [Scenario Model](../models/scenarios.md), [Scenario Analysis](../methods/scenario-analysis.md), [System Design](../models/system-design.md#feature-definition). Add a counterexample that exposes implementation detail incorrectly placed in a Scenario. |
| Derivation and traceability | A Scenario informs SR analysis; an SR has one IR parent. A trace does not by itself explain why the obligation is needed. | Explain how each proposed SR contributes to the need, identify the relevant Scenario outcome, and justify when no additional obligation is needed. | **Partial:** [Requirement relationships](../models/requirements.md#cross-domain-relationships), [Requirement Analysis](../methods/requirement-analysis.md#derive-system-requirements). Develop the reasoning between the pilot's request, Scenario, obligation and acceptance criterion rather than presenting only a completed relationship table. |
| Functional and quality obligations | Required behavior, operating conditions, quality constraints and interface-related outcomes can all affect satisfaction. | Identify the behavior and quality concern in a request; formulate an assessable obligation or identify the missing evidence that prevents it. | **Partial:** [Requirement quality](../models/requirements.md#requirement-quality), [5W2H](../methods/5w2h.md#questions). Add a contrast between a supported offline condition and an unsupported request to work “quickly.” |
| Acceptance and claim boundaries | Acceptance criteria specify observations; defining a criterion is different from producing evidence. | State preconditions, action, expected observation and a relevant failure observation, while explaining what remains unproved. | **Partial:** [Verification method](../methods/plan-and-assess-verification.md), [worked assessment plans](../practices/WORKED-EXAMPLE.md#assessment-plans). Trace proposed observations back to the derived SR and contrast them with intended-use evidence. |
| Requirement handoff and correction | Requirement validity, design completeness and demonstrated satisfaction are different claims. | Hand off a coherent draft or an explicit unresolved decision; identify later behavior, allocation and assessment work without claiming it is complete. | **Partial:** [Requirement Analysis](../methods/requirement-analysis.md#reconcile-and-review), [Requirement quality](../models/requirements.md#requirement-quality). Add a complete pilot exit showing what is ready for review and what is deliberately unperformed. |

## Logical behavior

The [logical-decomposition source contribution](../references/nasa-2016-systems-engineering-handbook.md#logical-decomposition) motivates analysis of behavior and derived obligations; REM owns Feature/Function relationships.

| Topic | Understand | Be able to do | Existing explanations and gaps |
| --- | --- | --- | --- |
| Capability, behavior and coverage | A stakeholder capability may require several Functions; SR-to-Function relationships need not mirror the requirement tree. | Explain the contribution of candidate Functions and recognize an uncovered SR or unnecessary duplicate. | **Partial:** [System Design Model](../models/system-design.md), [Functional Analysis](../methods/functional-analysis.md). Assess local coverage with a case containing shared behavior and more than one SR. |
| Inputs, outputs and failure behavior | A Function boundary includes conditions and outcomes relevant to its obligations. | Explain normal and failed behavior without assigning implementation responsibility prematurely. | **Partial:** [Function definition](../models/system-design.md#function-definition), [System Design reconstruction](../practices/understand-rem/system-design.md). Investigate whether a new reader can interpret a changed input or failure condition from the local account. |

## Architecture and interfaces

The [Parnas](../references/parnas-1972-criteria-for-decomposing-systems.md), [Kruchten](../references/kruchten-1995-architectural-blueprints.md), [interface-management](../references/nasa-2016-systems-engineering-handbook.md#interface-management) and [ATAM](../references/kazman-2000-atam-method-for-architecture-evaluation.md) contributions motivate distinct concerns; they do not uniquely determine REM's architecture rules.

| Topic | Understand | Be able to do | Existing explanations and gaps |
| --- | --- | --- | --- |
| Responsibility and allocation | Primary accountability, supporting participation, requirement allocation and Module containment are different relationships. | Justify one coherent accountable boundary and recognize when decomposition must change. | **Partial:** [Boundaries](../models/architecture-boundaries.md), [Allocation](../models/architecture-allocation.md). Add a worked case with a supporting Module and explain the ownership conclusion. |
| Interfaces and state | Agreement depends on interaction semantics and ownership, including failure conditions and exposure through containing boundaries. | Trace an interaction across responsibilities and identify an incompatible assumption or unspecified state owner. | **Partial:** [Architecture Design](../models/architecture-design.md), [Architecture Design method](../methods/architecture-design.md). Investigate normal/failure interaction coverage before selecting an additional example. |
| Trade-offs and explanatory views | Different concerns require different comparisons and presentations of the same authoritative information. | Compare alternatives under a stated concern and justify a selected view or an omission with coverage elsewhere. | **Partial:** [Architecture decisions](../practices/make-an-architecture-decision.md), [Architecture Views](../methods/architecture-views.md). Deepen contextual method selection and an unfamiliar trade-off case. |

## Realization and integration

The [NASA subject structure](../references/nasa-2016-systems-engineering-handbook.md#subject-coverage-and-stakeholder-expectations) includes implementation, integration and transition.
REM's current local material emphasizes realization under architectural responsibility.

| Topic | Understand | Be able to do | Existing explanations and gaps |
| --- | --- | --- | --- |
| Technical realization | A component, process or deployment choice realizes responsibilities without automatically changing their owners. | Connect a mechanism to the relevant Module/Interface and explain a material assumption or deferred choice. | **Partial:** [Realization Model](../models/architecture-realization.md), [Realization Design](../methods/realization-design.md). Investigate coverage of migration and operating constraints beyond the small offline example. |
| Integration and transition | Independently acceptable components may not produce the intended combined outcome; transition adds an operating context. | Identify an interaction-level observation and a readiness question before use in a different environment. | **Partial:** [Integration Principle](../principles/component-results-do-not-establish-system-results.md), [Engineer a change](../practices/engineer-a-change.md). Transition is **source only** at the selected NASA chapter-outline level; a local treatment and detailed source inspection remain needed if operational transition is developed further. |

## Verification and intended-use validation

Existing [verification](../references/nasa-2016-systems-engineering-handbook.md#product-verification) and [validation](../references/nasa-2016-systems-engineering-handbook.md#product-validation) source notes distinguish two assessment questions.

| Topic | Understand | Be able to do | Existing explanations and gaps |
| --- | --- | --- | --- |
| Specified conformance and evidence | Criteria, subject state, observation and judgment are distinct; old or narrow evidence may not support the current claim. | Choose a relevant observation and explain the limit of an unrun plan, stale result or component-only check. | **Partial:** [Verification](../methods/plan-and-assess-verification.md), [Evidence Principle](../principles/evidence-applies-to-a-claim-and-context.md). Assess interpretation of an adverse or inconclusive result beyond the authored illustration. |
| Intended-use outcomes | A technically conforming system can still fail the stakeholder's task under actual conditions. | Define a bounded participant task and report outcome, confusion and help required without claiming general effectiveness. | **Partial:** [Intended-use validation](../methods/validate-stakeholder-outcomes.md), [assessment Practice](../practices/verify-and-validate-a-bounded-slice.md). Actual participant evidence is absent; editorial walkthroughs can assess guidance but cannot substitute for it. |

## Evolution and provenance

[Requirements management](../references/nasa-2016-systems-engineering-handbook.md#requirements-management), [configuration management](../references/nasa-2016-systems-engineering-handbook.md#configuration-management) and [PROV](../references/w3c-2013-prov-overview.md) contribute different parts of change and attribution reasoning.

| Topic | Understand | Be able to do | Existing explanations and gaps |
| --- | --- | --- | --- |
| Identity, change and retirement | Refining a definition, moving its representation and changing its parent have different meanings; retirement needs surviving obligations addressed. | Explain affected relationships and preserve the meaning of an earlier baseline through a proposed change. | **Partial:** [Evolution Concepts](../concepts/evolution.md), [Requirements identity](../models/requirements.md#identity-and-content), [Evolution reconstruction](../practices/understand-rem/evolution.md). Inspect a case where several consumers depend on the changed meaning. |
| Provenance and applicability | Knowing where a claim came from does not establish that it is true or applicable now. | Separate source observations, later interpretations and current reliance on evidence. | **Partial:** [History Principle](../principles/later-interpretation-does-not-rewrite-earlier-observation.md), [Assurance Concepts](../concepts/assurance.md). Assess a disputed-source or changed-assumption case. |

## Operational support and improvement

This area connects REM's representation choices with the [KPS editorial guidance](../references/kps-11-knowledge-practice-system.md) and existing scoped [decision-analysis contribution](../references/nasa-2016-systems-engineering-handbook.md#decision-analysis).

| Topic | Understand | Be able to do | Existing explanations and gaps |
| --- | --- | --- | --- |
| Representation and guidance | A view or local summary can repeat relevant meaning while retaining one authoritative owner. | Find the applicable source and distinguish a stale or incomplete presentation from a rule change. | **Partial:** [Operational Support](../models/operational-support.md), [View Presentation](../methods/view-presentation.md). Investigate useful local overlap and explicit source/version selection for each reading path. |
| Decision uncertainty and risk | An assumption can affect the consequence of a choice; more information helps only when relevant to that decision. | Identify a consequential uncertainty, a discriminating observation and a reversible next step when commitment is premature. | **Partial:** [Architecture decision Practice](../practices/make-an-architecture-decision.md). General technical-risk management is **source only** at the NASA chapter-outline level, not a locally taught comprehensive process. |
| Improve guidance from use | A documentation correction, an editorial usability result and evidence of engineering effectiveness support different claims. | Locate the responsible knowledge owner, propose a bounded correction and state what observation would support retaining it. | **Partial:** [Improve REM](../practices/improve-rem-through-actual-use.md). Obtain and retain actual reader difficulties before generalizing benefits. |

## Maintaining this outline

Revise the topic and required depth when inspected sources or intended reader tasks reveal a gap; then reconcile the linked explanations.
Keep each row's remaining gap beside its current material so navigation cannot imply complete coverage.
Preserve helpful overlap with the reconstruction guide while maintaining one subject coverage outline.
Task order stays in Practices, delivery priorities stay with the responsible project, and actual assessment results remain separate from these intended capabilities.
This draft uses selected KPS editorial guidance and ordinary Markdown tables; it does not claim full adoption of KPS's outline illustration or validator profile.
