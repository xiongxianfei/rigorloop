# Requirement model

The [concepts](../concepts/README.md) distinguish the initial need, system obligation, and allocated obligation.
The [requirement-analysis method](../methods/requirement-analysis.md) develops those three levels.

```text
IR
├── SR
│   ├── AR
│   └── AR
└── SR
    └── AR
```

## Containment

- Each SR MUST have exactly one IR parent.
- Each AR MUST have exactly one SR parent.
- Requirement parentage MUST be acyclic.
- An IR or SR may be developed before its children are known; an SR need not have ARs immediately.

These parent relationships are exclusive: an SR cannot belong to several IRs, and an AR cannot belong to several SRs.
An IR may have multiple SR children, and an SR may have multiple AR children.
Source references and other relationships do not establish additional parents.

IR-to-SR decomposition converts an initial need into system-level obligations.
SR-to-AR derivation allocates lower-level obligations to architectural responsibility.
An AR is a durable requirement, not a record that an allocation event occurred.

## Cross-domain relationships

| Source | Relationship | Target | Meaning |
| --- | --- | --- | --- |
| SR | constrains | Feature or Function | The obligation limits or shapes capability or behavior |
| AR | constrains | Function | An allocated obligation constrains logical behavior |
| AR | allocatedTo | Module | Architecture is responsible for satisfying the allocated obligation |
| Requirement | verifiedBy | Verification | An assessment determines whether the obligation is satisfied |

Cross-domain references may be many-to-many without changing the single-parent requirement hierarchy.
References for related concerns do not create additional containment or derivation parents.
Do not duplicate one obligation merely to place it under several parents.

Every active AR SHOULD identify the architectural responsibility for satisfying it.
Exact allocation cardinalities remain an [open refinement](../README.md#open-refinements).
An SR SHOULD avoid prescribing implementation unless that implementation is itself a required constraint.

## Identity and content

Every requirement has a stable identity, a clear name, and analysis that accounts for all seven 5W2H questions at its level.
An IR states the initial need.
An SR or AR states the obligation and the conditions needed to assess satisfaction.
Analysis, rationale, and provenance support the requirement without becoming substitutes for its statement.
The statement is the authoritative need or obligation; What explains its problem and desired outcome as part of the supporting analysis.
The selected representation records all seven answers without duplicating semantic facts and distinguishes assumptions, constraints, and unresolved questions.

| Property | Meaning | Effect of change |
| --- | --- | --- |
| Identity | Stable designation of the engineering entity | Preserved while the same requirement evolves |
| Display name | Human-readable expression of the need or obligation | May be refined without changing identity |
| Physical location | Position in the selected storage representation | May change without changing identity; can also carry containment meaning |

Names and physical labels must not be treated as independent identities.
A readable location can include an identity and a name, with one authoritative source for each and consistent derived labels.
The [Operational Support model](operational-support.md#naming-and-location) owns representation and rename rules.

Parentage is authored once.
If a representation uses physical containment as its authoritative parent relation, it derives the parent view from that containment.
Another representation may author an explicit parent reference instead.

Renaming a containing directory while keeping the same parent identity preserves requirement parentage.
Moving an SR to a different IR, or an AR to a different SR, changes its parentage when location represents containment.
That move requires reconsidering the derivation and affected obligations; it is not merely a readability edit.
Requirement identities do not encode their current parent and are not renumbered solely because a parent changes.

Identity persists across evolution of the same requirement; revision and evidence applicability remain distinct concerns.
Requirement satisfaction, approval, and implementation status must not be inferred from the presence of the requirement file.
