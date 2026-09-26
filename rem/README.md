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
| Analyze stakeholder scenarios | [Scenario Analysis](methods/scenario-analysis.md) | Name and define the durable Feature, confirm Scenarios, and expose candidate behavior |
| Name an IR | [IR naming](methods/requirement-analysis.md#name-the-initial-requirement) | Name the concrete need or desired outcome and its subject |
| Derive system obligations and behavior | [Requirement Analysis](methods/requirement-analysis.md#derive-system-requirements) | Separate assessable obligations from the initial need and confirm Functions with clear names and behavior boundaries |
| Allocate responsibility | [Architecture model](models/architecture-design.md) | Allocate Functions and ARs independently and assess their consistency |
| Evolve and assess the model | [Engineering cycle](methods/README.md#engineering-cycle) | Iterate between need, design, realization, evidence, and baseline decisions |

Requirement Analysis and Scenario Analysis currently have detailed procedures here.
The cycle and allocation rules establish direction for later method refinement without claiming a complete workflow implementation.

## Method boundaries

REM does not mandate JSON, directory layouts, Git, Rust, a web application, a CLI, or a CI service.
A project selects a representation and tools through Operational Support while preserving REM's engineering semantics.
RigorLoop provides a reference implementation; its current technology choices do not become universal method requirements.

## Open refinements

- The initial proposal defines SRs as verifiable but says they SHOULD be verifiable; the exact obligation strength remains to be settled.
- Its core-invariant section says implementations SHOULD enforce rules that individually use MUST; conformance levels need clarification.
- Function and AR allocation identify accountable responsibility, but exact allocation cardinalities and permitted exceptions need refinement.
- The conceptual SR-to-AR derivation is defined; its canonical serialized relationship name and field representation remain open.

These issues do not weaken the explicit single-parent requirement hierarchy or authorize fabricated approvals or evidence.
