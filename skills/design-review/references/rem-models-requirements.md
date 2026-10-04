<!-- Generated from rem/models/requirements.md; source SHA-256 91e68cf217ed10cf4c794722bb48718926d3994f3495089f36fbd8a8372c88a8. Edit the owning REM source. -->

# Requirement model

The [concepts](https://github.com/xiongxianfei/rigorloop/blob/main/rem/concepts/README.md#requirement-input) distinguish the incoming Raw Requirement (RR) from the durable Initial Requirement, System Requirement, and Allocated Requirement.
The [Requirement Analysis method](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/requirement-analysis.md) reconciles RR input with the current requirement model and develops the three durable levels.

```text
IR
├── SR
│   ├── AR
│   └── AR
└── SR
    └── AR
```

## Requirement input and reconciliation

An RR is outside the durable requirement hierarchy. It supplies source intent, context, or evidence for analysis but does not become an IR merely because it was submitted or accepted for analysis.

Requirement Analysis MUST inspect applicable current IRs and SRs before creating durable requirements. For each material part of the RR, the analysis SHOULD establish one of these semantic dispositions:

- already covered without requirement change;
- refine an existing IR or SR while preserving its identity when the same need or obligation remains;
- create a new IR when a distinct durable need is justified, then derive or refine its SRs;
- separate several independent needs before creating or changing requirements;
- retain an explicit unresolved or conflicting disposition when the available basis is insufficient.

An RR may affect several durable requirements, and several RRs may contribute provenance to the same requirement. These source relationships do not create additional requirement parents. REM does not require RR to have a stable REM identity; a project MAY preserve an external request/proposal identity and exact source reference through Operational Support.

## Containment

- Each SR MUST have exactly one IR parent.
- Each AR MUST have exactly one SR parent.
- Requirement parentage MUST be acyclic.
- An IR or SR MAY exist before its children are known.
- An SR MAY have zero AR children while architectural allocation is not yet established.

These parent relationships are exclusive: an SR cannot belong to several IRs, and an AR cannot belong to several SRs.
An IR may have multiple SR children, and an SR may have multiple AR children.
Source references and other relationships do not establish additional parents.

IR-to-SR decomposition converts a durable need into system-level obligations.
SR-to-AR derivation creates lower-level obligations assigned to architectural responsibility.
An AR is a durable requirement, not a record that an allocation event occurred.

## Requirement quality

An approved SR MUST be stated so that satisfaction can be assessed through defined verification criteria.
An approved AR MUST likewise be assessable at its allocated architectural scope.
Draft requirements may retain explicit unknowns while analysis is incomplete.

Requirement approval establishes an assessable obligation as a basis for design; it does not require completed Function design or AR allocation.
Missing downstream design MUST remain explicit without being treated, by itself, as a requirement-validity failure.
The [System Design model](rem-models-system-design.md#function-relationships) owns Function coverage required for design completeness; architectural allocation has its own completeness conditions below.
Requirement validity, design completeness, and demonstrated satisfaction are distinct claims.

An SR SHOULD avoid prescribing implementation unless that implementation is itself a required constraint.
An AR may be more architecture-specific because its purpose is to state the obligation assigned to a Module, but it still states what must be satisfied rather than implementation steps.

## Cross-domain relationships

| Source | Relationship | Target | Meaning |
| --- | --- | --- | --- |
| IR | confirms | Feature | Initial Requirement analysis confirms the durable stakeholder-visible capability needed to address the need |
| IR | confirms | Scenario | Initial Requirement analysis confirms a governed stakeholder situation relevant to the need |
| Scenario | exercises | Feature | The Scenario describes one concrete way the stakeholder uses or experiences the Feature |
| Scenario | informs | SR | Scenario Analysis exposes system obligations needed to support the Scenario |
| SR | confirms | Function | System Requirement analysis confirms the logical behavior that carries the system obligation |
| SR | constrains | Feature or Function | The obligation may additionally limit or shape capability or behavior |
| AR | constrains | Function | The allocated obligation may constrain logical behavior owned by the allocated architecture |
| AR | allocatedTo | Module | Exactly one Module is accountable for satisfying the allocated obligation |
| Requirement | verifiedBy | Verification | An assessment determines whether the obligation is satisfied |

Cross-domain references may be many-to-many without changing the single-parent requirement hierarchy.
The [Scenario model](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/scenarios.md) owns Scenario identity, lifecycle, and cardinality.
The [System Design model](rem-models-system-design.md) owns Feature and Function relationships.
The [Architecture Design model](rem-models-architecture-design.md) owns allocation cardinalities.

A confirmed Scenario does not directly confirm a Function.
It informs SR analysis; the `SR confirms Function` relationship records authoritative logical-behavior confirmation.

References for related concerns do not create additional containment or derivation parents.
Do not duplicate one obligation merely to place it under several parents.

## SR-to-AR completeness

An SR MAY remain system-level without ARs while architecture has not yet been allocated.
When lower-level architectural responsibility is required, derive one or more ARs.

Architectural allocation for an SR is complete only when every lower-level obligation required to satisfy that SR is covered by an AR allocated to one accountable Module.
Do not create an AR merely to fill the tree.

If one lower-level obligation spans several Modules, decompose it into separate ARs under the same SR rather than assigning one AR to several Modules.

## Identity and content

Every requirement has a stable identity, a clear name, and analysis that accounts for all seven 5W2H questions at its level.
An IR states the durable need established or refined after RR reconciliation.
An SR or AR states the obligation and the conditions needed to assess satisfaction.
Analysis, rationale, and provenance support the requirement without becoming substitutes for its statement.
The statement is the authoritative need or obligation; What explains its problem and desired outcome as part of the supporting analysis.

| Property | Meaning | Effect of change |
| --- | --- | --- |
| Identity | Stable designation of the engineering entity | Preserved while the same requirement evolves |
| Display name | Human-readable expression of the need or obligation | May be refined without changing identity |
| Physical location | Position in the selected storage representation | May change without changing identity; can also carry containment meaning |

Names and physical labels must not be treated as independent identities.
A readable location can include an identity and a name, with one authoritative source for each and consistent derived labels.
The [Operational Support model](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/operational-support.md#naming-and-location) owns representation and rename rules.

Parentage is authored once.
If a representation uses physical containment as its authoritative parent relation, it derives the parent view from that containment.
Another representation may author an explicit parent reference instead.

Moving an SR to a different IR, or an AR to a different SR, changes semantic parentage and requires reconsidering derivation and affected obligations.
Requirement identities do not encode their current parent and are not renumbered solely because a parent changes.

Requirement satisfaction, approval, implementation, and evidence applicability remain distinct concerns and MUST NOT be inferred from the presence of a requirement definition.
