# Operational Support model

Operational Support governs the engineering design system itself.
It defines how Requirement Analysis, System Design, and Architecture Design are represented, interpreted, validated, and maintained.
Application production operations are a separate concern unless they are part of the system being modeled.

## Metamodel and project representation

The metamodel defines valid engineering-model structures.
It SHOULD specify entity types, fields, relationship types, cardinalities, identity rules, and naming rules.
It SHOULD also specify validation, lifecycle, authoring, retirement, migration, baseline, and change rules.

REM supplies common semantics; an implementation profile selects their concrete representation.
For example, a profile may use JSON records, filesystem containment, and a version-control repository.
Those choices do not change what a Requirement, Function, or Module means.

## Naming and location

Each project representation defines how stable identity, display name, and physical location are recorded and related.
Keep one authoritative source for identity and name, and derive any repeated storage labels from those sources.
Readable labels help people navigate the model without making the labels themselves entity identities.
[Principle 16](../principles/README.md) governs the clarity of the engineering name and definition; the representation profile governs how that name appears in storage.

A filesystem representation may combine a stable identity and a normalized readable title in a directory or filename, such as an ID followed by a title slug.
Such a representation defines title normalization, label consistency, and collision handling.
Another implementation may expose the same identity and name through a database or another storage interface.
REM does not require directories or a particular filename pattern.

An explicit rename preserves entity identity, reconciles current references, and checks whether containment changes.
When physical containment expresses parentage, a move between different parent entities is a model change.
Keep current navigation coherent while preserving historical references against their original states.
Do not retarget previous assessments to new subjects merely because identities or names match.

A profile should explain how unsupported names or locations are handled rather than silently truncating titles or replacing identities.
Changing a storage convention also requires reconciliation of the tools and consumers that rely on it.

## Validation and maintenance

Structural checks assess representation, containment, identity, and reference integrity.
Engineering assessment determines whether obligations, behavior, allocation, and proof are coherent and adequate.
A structurally valid model can still contain incomplete reasoning or unsupported claims.

Maintain the metamodel through controlled changes with explicit compatibility and migration decisions.
Preserve historical meaning when entity representations or relationship conventions change.
A baseline's interpretation must remain attributable to the metamodel and conventions applicable to it.

Analysis walkthroughs may support engineering work without becoming additional authoritative design assets.
Before retiring such material, place any unique current conclusion or derivation with its owning requirement or design definition, and derive explanatory views from those owners.
Retain review and validation records with their assessed scope and historical meaning; do not mix them into current definitions or retarget an earlier review when its supporting document is reorganized.

## Method and application boundary

REM methods define reusable analysis procedures such as 5W2H.
Operational Support records how a project applies and represents their outputs.
Using a method does not by itself prescribe a directory, mandatory JSON keys, command, agent, or service.
