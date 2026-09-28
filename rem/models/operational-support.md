# Operational Support model

Operational Support governs the engineering design system itself.
It defines how Requirement Analysis, System Design, and Architecture Design are represented, interpreted, validated, and maintained.
Application production operations are a separate concern unless they are part of the system being modeled.

## Metamodel and project representation

The metamodel defines valid engineering-model structures.
It SHOULD specify entity types, fields, relationship types, cardinalities, identity rules, and naming rules.
It SHOULD also specify validation, lifecycle, authoring, retirement, migration, baseline, and change rules.

REM supplies common semantics; a project implementation selects their concrete representation.
For example, an implementation may use JSON records, filesystem containment, and a version-control repository.
Those choices do not change what a Requirement, Function, Module, Module-containment relationship, or Interface exposure means. An implementation may impose practical representation limits, such as a supported maximum Module nesting depth, provided it presents that limit as implementation/Operational Support policy rather than universal REM semantics.

## Naming and location

Each project representation defines how stable identity, display name, and physical location are recorded and related.
Keep one authoritative source for identity and name, and derive any repeated storage labels from those sources.
Readable labels help people navigate the model without making the labels themselves entity identities.
[Principle 16](../principles/README.md) governs the clarity of the engineering name and definition; the project representation governs how that name appears in storage.

A filesystem representation may combine a stable identity and a normalized readable title in a directory or filename, such as an ID followed by a title slug.
Such a representation defines title normalization, label consistency, and collision handling.
Another implementation may expose the same identity and name through a database or another storage interface.
REM does not require directories or a particular filename pattern.

An explicit rename preserves entity identity, reconciles current references, and checks whether containment changes.
When physical containment expresses parentage, a move between different parent entities is a model change.
Keep current navigation coherent while preserving historical references against their original states.
Do not retarget previous assessments to new subjects merely because identities or names match.

An implementation should explain how unsupported names or locations are handled rather than silently truncating titles or replacing identities.
Changing a storage convention also requires reconciliation of the tools and consumers that rely on it.

## Validation and maintenance

Structural checks assess representation, containment, identity, and reference integrity.
Engineering assessment determines whether obligations, behavior, allocation, and proof are coherent and adequate.
A structurally valid model can still contain incomplete reasoning or unsupported claims.

Maintain the metamodel through controlled changes with explicit compatibility and migration decisions.
Preserve historical meaning when entity representations or relationship conventions change.
A baseline's interpretation must remain attributable to the metamodel and conventions applicable to it.

## Generated-view maintenance

For each maintained family of generated views, Operational Support MUST define a generation and refresh contract.
The contract identifies:

- the intended readers, concerns, and selected engineering scope;
- the authoritative inputs and their actual source state, including working changes when present;
- the applicable metamodel interpretation and semantic projection rules, with enough identity to recover the versions used;
- the presentation rules, templates, and relevant tool configuration needed to reproduce the claimed result;
- the generated outputs, their relationship to their inputs, and the owner of their maintenance;
- the regeneration, freshness-checking, publication, and failure-handling procedures.

These are semantic responsibilities; the project selects their representation.
The contract MAY reference existing configuration and controlled artifacts rather than duplicate their contents or require a separate metadata file.
It does not prescribe a storage format, diagram language, compiler, browser, or command.

Given the same source state, interpretation, scope, and projection rules, generated engineering meaning SHOULD be reproducible.
A project that requires identical output bytes or layout MUST additionally identify and control the rendering dependencies and configuration relevant to that claim.
A presentation replacement MUST preserve the selected engineering meaning and its provenance.

Freshness checking MUST distinguish outputs that match their declared inputs and generation rules from outputs requiring regeneration.
Currentness relative to a selected historical state MUST remain distinguishable from currentness relative to the latest working model.
A previous assessment remains attached to the source state and generated subject it actually inspected.
Regeneration alone does not transfer that assessment to changed output.

The publication procedure MUST prevent a failed generation or a mixture of outputs from different generation states from being presented as one successfully refreshed view set.
It MAY retain the last successful set with its original identity and an explicit indication that the requested refresh failed or remains pending.
The project defines the recovery mechanism and which checks are required before refreshed output can be relied on.

The [Architecture Views method](../methods/architecture-views.md#generation-and-assessment-cycle) owns the procedure for producing and assessing architecture presentations.
Its [correction ownership](../methods/architecture-views.md#correction-ownership) distinguishes model, projection, presentation, and maintenance findings.

## Method and application boundary

REM methods define reusable analysis procedures such as 5W2H.
Operational Support records how a project applies and represents their outputs.
Using a method does not by itself prescribe a directory, mandatory JSON keys, command, agent, or service.
