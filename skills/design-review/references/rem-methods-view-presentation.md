<!-- Generated from rem/methods/view-presentation.md; source SHA-256 4a704d15df57af7692c2152c4bbd9b2cea3bc577b4742a3ed0651303a7fcb1ca. Edit the owning REM source. -->

# Knowledge, projection, and presentation

## Knowledge, projection, and presentation

Keep three responsibilities distinct:

| Layer | Responsibility | Change owner |
| --- | --- | --- |
| Authoritative engineering knowledge | Defines requirements, behavior, architectural responsibility, contracts, and material realization information | The applicable REM engineering entity or subordinate information owner |
| Semantic projection | Selects scope, traverses typed relationships, derives inverse relationships, aggregates or collapses detail, and retains exact source ownership and provenance | The projection rules for the selected view |
| Rendered presentation | Arranges labels and diagrams and provides navigation, search, filtering, or other interaction appropriate to the reader | The presentation rules and resources |

```text
Authoritative engineering knowledge
        ↓ semantic projection
Derived view content
        ↓ presentation
Rendered view
```

These layers do not require separate files, services, or new first-class engineering entities.
The derived Architecture View Graph may support several projections, and a projection may support several presentations.
Material Module/Interface realization information belongs to the authoritative knowledge layer even when called a realization view.

Presentation choices MUST preserve the selected engineering meaning.
A change to which relationships are included or how ownership is aggregated changes the projection rules, even when implemented in a rendering tool.
Visual arrangement MUST NOT create Module containment, Interface ownership, allocation, or an execution sequence absent from the authoritative information.

### Authored explanations and generated presentations

Authoritative engineering knowledge may include structured definitions and relationships, prose, and authored interaction or lifecycle explanations. The [Architecture Design model](rem-models-architecture-design.md#authored-architecture-explanations) owns their semantic authority. Authoring a sequence in an owning design is a way to define or explain an interaction; rendering that sequence in a 4+1 view is a presentation of the same source.

```text
Owning architecture knowledge
├── Structured definitions and relationships
└── Authored interaction and lifecycle explanations
                    │
                    ▼
       Selected, attributable view content
                    │
                    ▼
        Rendered 4+1 presentations
```

Do not require a tool to invent an interaction from a dependency graph, or require every authored exchange to become a new entity or duplicate structured record. Select the authoritative explanation, retain its owner and source state, and render or reference it in the relevant view. When a presentation combines authored explanations and derived relationships, distinguish what each source establishes; a shared page does not establish an unrecorded relationship between them.

A diagram source can contain engineering semantics as well as layout instructions. A change to participants, ordering, conditions, guarantees, or outcomes belongs to the engineering owner. A change only to spacing, visual arrangement, or faithful labels belongs to presentation. Correct the source that owns the changed meaning, reconcile affected contracts, and regenerate; do not maintain a separately edited browser version of the interaction.

## Progressive disclosure

Human-facing views SHOULD begin with the smallest useful architectural picture and reveal detail on demand.
For hierarchical architecture, the Logical View SHOULD normally start with top-level or otherwise highest-useful parent Modules and their visible cross-boundary Interfaces. Expanding a parent reveals its child Modules and internal/exposed Interfaces; expanding a child then reveals Functions, ARs, state/data ownership, and realization.

Do not flatten the entire Module hierarchy into one first-frame graph merely because every relationship can be rendered.

The readable navigation SHOULD follow the same containment as the diagrams. Child details belong within their parent's expansion or a linked child view, rather than appearing as peer entries beside every ancestor. Navigation should first lead to readable architectural context while retaining separately accessible canonical sources.

Separate responsibility and collaboration explanations from optional full allocation and provenance inventories. An empty allocation or state section MUST describe only what the selected owner and its actual descendants establish; a leaf Module must not imply that missing obligations are allocated beneath it.

Agent-facing views SHOULD expose deterministic typed nodes, typed relationships, and provenance sufficient for traversal such as neighborhood, upstream-why, downstream-how, and Scenario participation queries.

Human and agent views SHOULD derive from the same semantic projection rules even when their presentation formats differ.

### Rendered readability and navigation

Choose a presentation tool for the intended reading environment. A browser view MAY use generated interactive diagrams and linked detail pages; a document MAY use small linked diagrams. The tool remains replaceable. Generated graph/layout source MUST derive from authoritative knowledge; when the selected input is an authored architecture explanation, render that owning source without creating a second independently maintained account of its semantics.

Show one useful responsibility level at a time. Keep public-entry catalogs, complete allocation inventories, and provenance outside the initial diagram. A reader SHOULD be able to select a Module or Interface, understand its responsibility or contract, follow its children or collaborators, and return to the previous context. Diagram simplification MUST retain discoverable exact relationship owners and recorded scope limits.

Lead visible labels with meaningful names. A diagram SHOULD explain Module responsibilities and Interface contracts without requiring readers to interpret stable identifiers. Identifiers need not appear beside every label.

A presentation MAY shorten a canonical name when the resulting label remains faithful and unambiguous within the selected view. Preserve the words needed to distinguish neighboring responsibilities and contracts; if shortening creates ambiguity, restore meaningful context. An identifier alone does not resolve unclear engineering meaning. A presentation label MUST retain its mapping to the canonical entity and MUST NOT redefine its identity, scope, ownership, or relationships.

Keep the full canonical name and stable identity available in linked details or an equivalent reference. Interactive views SHOULD also expose them on hover and keyboard focus, with detail navigation usable without hovering. When search is available, it SHOULD accept canonical names and stable identifiers as well as any shortened visible labels. Static views SHOULD provide attributable references that allow the same identity lookup without interactive controls.

Assess readability in the rendered presentation. Inspect label meaning and ambiguity, size, edge distinction, navigation, and representative narrow and wide displays. Verify that readers can understand visible names and reach full names, stable identities, and exact contract owners. Structural validity, successful generation, and complete reference links do not by themselves establish human comprehension. Retain a detailed text reference where useful, but do not require readers to traverse that inventory to understand the architectural overview.

Choose representative tasks for the declared audience and concern.
For example, a reader of a Logical view should be able to locate an accountable Module, distinguish its children from surrounding context, understand an Interface's purpose and exact provider/consumers, follow an allocation, and reach the authoritative source.
For a static document, linked sections or references may support these tasks; interactive controls are a presentation choice.
Agent-facing projections should be assessed through the declared typed traversal and provenance tasks.

Record the assessed source state, projection and presentation identity, rendered artifact or reproducible subject, reading environment, tasks exercised, observations, and unresolved limitations.
An automated navigation check establishes the behavior it exercised; the assessment must also judge whether the selected content and presentation explain the intended architectural concern.
Evidence for one artifact or reading environment does not establish usability for uninspected outputs or environments.

## Correction ownership

Investigate whether the finding originates in engineering knowledge, derivation, presentation, or maintenance before changing its owner.

| Finding | Responsible correction |
| --- | --- |
| Missing or contradictory obligation, responsibility, contract, allocation, or realization decision | Reconcile the authoritative engineering information, then regenerate dependent views |
| Incorrect selection, traversal, aggregation, source attribution, or collapsed ownership | Correct the semantic projection rules and regenerate the affected outputs |
| Overlapping labels, ambiguous visual notation, unreadable scale, or confusing navigation | Correct presentation rules or resources while preserving the engineering meaning |
| Stale, mixed, or incomplete generated output presented as current | Correct generation, freshness checking, publication, or recovery under Operational Support |

A finding may involve more than one owner.
Reconcile each affected responsibility and reassess the corrected subject.
Editing generated output alone does not provide a durable correction; make the change in its authoritative input, projection rule, presentation resource, or maintenance procedure.
