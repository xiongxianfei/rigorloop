# RigorLoop Engineering Method

RigorLoop Engineering Method (REM) is a tool-independent, model-based engineering methodology.
Requirements express what must be satisfied; System Design describes capabilities and behavior; Architecture Design assigns responsibility.
Operational Support defines how the engineering model is represented, governed, validated, and maintained.

Implementation realizes the design, verification produces evidence, and controlled Changes evolve identifiable Baselines.

## Status and use

This directory is the living home of the proposed method, reorganized from the user's initial 43-section REM proposal.
Refine the relevant document here as methodological decisions become clearer.
The method describes reusable engineering practice; its application to RigorLoop is being drafted separately under `design/`.

The selected authoring rules apply all seven 5W2H questions to every IR, SR, and AR, give IRs clear names, and limit each IR and SR to at most one consequential open question.
Those rules are recorded in [Requirement Analysis](methods/requirement-analysis.md).
[Principle 16](principles/README.md) extends the clarity commitment across engineering definitions; the [System Design model](models/system-design.md#clear-names-and-boundaries) defines its application to Features and Functions.
RigorLoop's separate application draft selects readable IR and SR directory names and structured seven-part analysis with self-contained schemas as representation conventions.
The rest of the methodology remains proposed; these documents do not silently replace existing approved repository contracts.

[Knowledge Reconstruction](knowledge-reconstruction.md) explains how these authoritative Concept, Principle, Model, and Method documents combine to build REM and why each knowledge owner exists.
It is an integration guide, not another knowledge category.

## Contents and ownership

| Package | Owns | Reader's question |
| --- | --- | --- |
| [Concepts](concepts/README.md) | Definitions and distinctions | What does each term mean? |
| [Principles](principles/README.md) | Governing engineering commitments | What must the method preserve? |
| [Models](models/README.md) | Entity structures, relationships, and invariants | How does engineering information fit together? |
| [Methods](methods/README.md) | Repeatable analysis and design procedures | How do we produce and refine the information? |

A concept defines an IR; the requirement model defines its relationship to SRs; the analysis method explains how to develop it.
Reference that owner when another document needs the rule instead of creating an independently maintained definition.

## Selected methods

| Activity | Current method | Application |
| --- | --- | --- |
| Analyze requirements | [5W2H](methods/5w2h.md) | Account for every question at each IR, SR, and AR level |
| Analyze stakeholder scenarios | [Scenario Analysis](methods/scenario-analysis.md) | Confirm the durable Feature and governed black-box Scenarios; expose candidate obligations |
| Derive system obligations | [Requirement Analysis](methods/requirement-analysis.md#derive-system-requirements) | Create verifiable SRs under one IR and hand behavior questions to Functional Analysis |
| Confirm logical behavior | [Functional Analysis](methods/functional-analysis.md) | Confirm durable Functions from SRs and reconcile Feature realization |
| Allocate logical architecture | [Architecture Allocation](methods/architecture-allocation.md) | Allocate one primary Module per Function and exactly one Module per AR; identify logical Interfaces |
| Complete architecture design | [Architecture Design](methods/architecture-design.md) | Produce semantic Module/Interface architecture outputs, state/data ownership, and material subordinate physical/software realization without prescribing storage |
| Generate architecture views | [4+1 Architecture Views](methods/architecture-views.md) | Generate classic Logical, Process, Development, Physical, and Scenario projections from authoritative REM knowledge |
| Evolve and assess the model | [Engineering cycle](methods/README.md#engineering-cycle) | Iterate between need, design, realization, evidence, and baseline decisions |

The current core now has explicit procedures from Initial Requirement through logical allocation, physical/software architecture realization, and generated 4+1 architecture views.
Verification and the broader universal engineering concerns remain later refinements.

## Method boundaries

REM does not mandate JSON, directory layouts, Git, Rust, a web application, a CLI, or a CI service.
A project selects a representation and tools through Operational Support while preserving REM's engineering semantics.
RigorLoop provides a reference implementation; its current technology choices do not become universal method requirements.

## Open refinements

- REM conformance levels and which invariants are mandatory for partial adoption still need a dedicated definition.
- The universal method defines semantic relationships; each project still needs representation/tool choices through Operational Support and its chosen implementation.
- Verification has conceptual and model coverage but does not yet have a dedicated universal REM method.

These open items do not weaken the tightened Requirements → Scenario/Feature → Function → Architecture semantics.
