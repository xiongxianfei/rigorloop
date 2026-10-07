# RigorLoop Engineering Method

RigorLoop Engineering Method (REM) is a tool-independent, model-based engineering methodology.
Requirements express what must be satisfied; System Design describes capabilities and behavior; Architecture Design assigns responsibility through hierarchical Modules, encapsulated Interfaces, and material realization.
Operational Support defines how the engineering model is represented, governed, validated, and maintained.

Requirement Analysis begins from Raw Requirement (RR) input such as a request, proposal, issue, incident, or observation. RR is reconciled against current engineering knowledge and does not become a durable IR merely because it was submitted.

Implementation realizes the design, verification produces evidence, and controlled Changes evolve identifiable Baselines.

## Start from the work

Choose among the five [operating Practices](practices/README.md) for change engineering, existing-system review, assessment, architecture decisions or improving REM. Their local stages apply current rules and link deeper canonical guidance.

Use [Engineer a change](practices/engineer-a-change.md) for an end-to-end application and its [worked example](practices/WORKED-EXAMPLE.md) for a bounded design with unexecuted assessment plans.
Use [verification](methods/plan-and-assess-verification.md) for specified conformance and [intended-use validation](methods/validate-stakeholder-outcomes.md) for stakeholder outcomes.
Select architecture presentations through [explicit view tailoring](methods/architecture-views.md#view-selection-and-tailoring).
[Source references](SOURCES.md) identify external support and distinguish it from REM's selected rules.

## Status and use

[Method metadata](metadata.md) declares REM’s own version and the exact KPS version it is based on. Maintained REM documents inherit that declaration; stable document identities and source publication/inspection provenance remain distinct. The based-on relationship does not assert assessed KPS conformance or publish a software release.

This directory holds the current knowledge for the declared REM edition.
Refine the relevant document here as methodological decisions become clearer.
The method describes reusable engineering practice; its application to RigorLoop is being drafted separately under `design/`.

The selected authoring rules apply all seven 5W2H questions to every IR, SR, and AR, give IRs clear names, and limit each IR and SR to at most one consequential open question.
Those rules are recorded in [Requirement Analysis](methods/requirement-analysis.md).
[Operational Support](models/operational-support.md#clear-engineering-definitions) owns the clarity commitment across engineering definitions; the [System Design model](models/system-design.md#clear-names-and-boundaries) defines its application to Features and Functions.
RigorLoop's separate application draft selects readable IR and SR directory names and structured seven-part analysis with self-contained schemas as representation conventions.
These methodology documents do not silently replace existing approved repository contracts.

[Knowledge Reconstruction](practices/understand-rem/README.md) explains how these authoritative Concept, Principle, Model, Method, and Practice documents combine to build REM and why each knowledge owner exists.
It is an integration guide, not another knowledge category.

## Contents and ownership

| Package | Owns | Reader's question |
| --- | --- | --- |
| [Concepts](concepts/README.md) | Definitions and distinctions | What does each term mean? |
| [Principles](principles/README.md) | Explanatory relationships, rationale and limits | What deeper explanatory relationship matters, and why? |
| [Models](models/README.md) | Entity structures, relationships, and invariants | How does engineering information fit together? |
| [Methods](methods/README.md) | Repeatable analysis and design procedures | How do we produce and refine the information? |
| [Practices](practices/README.md) | Goal-oriented application and worked examples | How do these methods fit together in real work? |

A concept defines an IR; the requirement model defines its relationship to SRs; the analysis method explains how to develop it.
Reference that owner when another document needs the rule instead of creating an independently maintained definition.

## Selected methods

| Activity | Current method | Application |
| --- | --- | --- |
| Analyze requirements | [5W2H](methods/5w2h.md) | Account for every question at each IR, SR, and AR level |
| Analyze stakeholder scenarios | [Scenario Analysis](methods/scenario-analysis.md) | Confirm the durable Feature and governed black-box Scenarios; expose candidate obligations |
| Reconcile incoming needs and derive system obligations | [Requirement Analysis](methods/requirement-analysis.md) | Treat request/proposal material as RR input, reuse/refine/create IRs as justified, derive/refine verifiable SRs, and hand behavior questions to Functional Analysis |
| Confirm logical behavior | [Functional Analysis](methods/functional-analysis.md) | Confirm durable Functions from SRs and reconcile Feature realization |
| Allocate logical architecture | [Architecture Allocation](methods/architecture-allocation.md) | Establish/refine Module hierarchy, allocate one primary Module per Function, derive/refine justified ARs with architecture context and allocate each to exactly one Module, and identify/expose logical Interfaces |
| Complete architecture design | [Architecture Design](methods/architecture-design.md) | Produce hierarchical Module/Interface architecture outputs, encapsulation boundaries, state/data ownership, and material subordinate physical/software realization without prescribing storage |
| Generate architecture views | [4+1 Architecture Views](methods/architecture-views.md) | Apply REM's adaptation of Logical, Process, Development, Physical, and Scenario views, assess semantic fidelity and reading tasks, and maintain identifiable, regenerable presentations |
| Evolve and assess the model | [Engineer a change](practices/engineer-a-change.md#stage-map-and-entry-routes) | Iterate between need, design, realization, evidence, and baseline decisions |

The current core now has explicit procedures from RR reconciliation through durable Requirements, logical System Design, hierarchical Architecture Design, physical/software realization, and generated 4+1 architecture views.
Dedicated verification and intended-use validation methods make assessment planning, observations and scoped conclusions explicit. Concrete workflow-stage names, review cadence, implementation milestone policy, and RigorLoop skill boundaries remain reference-implementation concerns rather than REM methodology semantics.

Architecture guidance distinguishes [authored explanations and generated presentations](methods/view-presentation.md#authored-explanations-and-generated-presentations), selects [readable behavioral explanations](methods/views/process.md#readable-behavioral-explanations) by question and scope, clarifies [Module naming and identity](models/architecture-boundaries.md#module-names-and-identity), and separates [current engineering knowledge from operational records](models/operational-support.md#engineering-knowledge-and-operational-records). These rules do not select a renderer, storage technology, browser layout, or review cadence.

For architecture-view rationale, start with the [original 4+1 approach](methods/architecture-views.md#origin-and-reference), then read [REM's adoption and adaptation](methods/architecture-views.md#adoption-and-adaptation-in-rem). The optional [Logical reading perspectives](methods/views/logical.md#logical-reading-perspectives) guide comprehension within the Logical View; they do not add standard views or prescribe repository pages.

## Method boundaries

REM does not mandate JSON, directory layouts, Git, Rust, a web application, a CLI, or a CI service.
A project selects a representation and tools through Operational Support while preserving REM's engineering semantics. REM defines hierarchical Module containment and encapsulation but does not prescribe a universal hierarchy-depth limit; an implementation such as RigorLoop may impose a practical supported depth as implementation policy.
RigorLoop provides a reference implementation; its current technology choices do not become universal method requirements.

## Open refinements

- REM conformance levels and which invariants are mandatory for partial adoption still need a dedicated definition.
- The universal method defines semantic relationships; each project still needs representation/tool choices through Operational Support and its chosen implementation.
- Method effectiveness for particular users and projects requires scoped observed assessment; illustrative examples do not establish that outcome.

These open items do not weaken the tightened Requirements → Scenario/Feature → Function → Architecture semantics.
