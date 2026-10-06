<!-- Generated from rem/methods/views/logical.md; source SHA-256 975825a5208f7386ae47c1b45e69220662ca67533c0050ac3caf6c83b47313ce. Edit the owning REM source. -->

# Logical View

## Logical View

The Logical View answers:

> What architectural responsibilities and technical components exist, what contracts connect them, and how do the components realize the accountable responsibilities?

Prefer these semantic inputs:

- Feature and Function context where it helps explain capability and behavior;
- Function-to-Module primary/supporting allocation;
- AR-to-Module allocation;
- Module definitions, responsibilities, exclusions, dependencies, and significant state/data ownership;
- logical Interfaces and their providers/consumers.
- the owned technical model's component responsibilities, contracts, state/artifact authority, realization mappings and relevant technology annotations.

The Logical View SHOULD begin with the highest useful in-scope Module level so a reader can understand the major responsibility boundaries before seeing lower-level detail. Show parent Modules and the significant Interfaces visible at that level first; reveal child Modules and internal Interfaces when the reader drills into a parent. Functions, ARs, Features, and state/data ownership SHOULD be progressively disclosed only after the relevant Module context is understood.

A parent Module boundary SHOULD hide descendant-internal Interfaces by default. A descendant-provided Interface that is explicitly exposed through that parent MAY appear at the parent level while retaining the descendant provider as its authoritative owner.

Label directly parent-provided contracts as provided by that parent. Keep contract ownership distinct from child behavior and exposed child-owned contracts. Views MUST NOT infer Interface implementation by every child from containment alone.

Begin with responsibilities and contracts. Technical structure MAY then expose selected components and technology choices that explain their realization. Runtime process boundaries, deployment targets and source paths retain their Process, Physical and Development concerns; do not infer them from a component box.

A simplified Module-to-Module edge MAY be rendered for readability when it is derived from an Interface, provided the underlying Interface remains discoverable and the simplification does not change the contract meaning.

Show recorded collaboration limits beside the overview to distinguish undeveloped contracts from architectural independence. An isolated Module or a missing edge does not establish that no collaboration is needed. Summarize known gaps from their authoritative owners; do not invent Interface edges to complete the picture. Allocation and Interface counts describe modeled content and MUST NOT be presented as proof of completeness or satisfaction.

### Logical reading perspectives

A Logical presentation MAY separate or combine the following reading perspectives to answer its readers' questions while preserving the responsibility overview and progressive disclosure.
They are optional presentations of the Logical concern, not additional architecture-view kinds, owning models, mandatory pages, or mandatory diagrams.

| Reading perspective | Reader's question | Selected information |
| --- | --- | --- |
| Architecture overview | What are the major responsibilities? | Highest useful Module boundaries and significant visible Interfaces |
| Technical structure | Which components and contracts realize those responsibilities? | Owned technical model: component boundaries, meaningful dependencies, data/artifact authority, technology annotations and explicit Module/Interface mappings |
| Public capabilities | What can a participant use? | Public entry names, purposes, contracts, and attributed Function correspondence |
| Module structure | How is this responsibility divided? | Selected Module, immediate children, responsibilities, exclusions, and state/data ownership |
| Collaboration | How do these responsibilities interact? | Named Interfaces, exact providers/consumers, and declared boundary exposure |
| Interface contract | What does this interaction promise? | Operations, inputs, outputs, guarantees, failures, and compatibility |
| Behavior and requirement allocation | What behavior and obligations belong here? | Feature/Function context, accountable Modules, and direct versus descendant AR allocations |

Readers SHOULD be able to move between an entry, its relevant behavior, its accountable responsibilities, and its contracts using the recorded relationships.
These navigation paths do not imply an execution sequence or transfer responsibility to the entry's catalog owner.
Select and combine perspectives for the intended concern rather than requiring a fixed number of screens or one complete diagram.

A production responsibility and its logical artifact contract may appear here when modeled.
The technical model may show a generator as a component with an input/output contract. Its source units, build transformations and package dependencies belong in Development; runtime execution and physical placement retain their respective view concerns. Classify the relationship by the question it answers, rather than assigning every diagram containing a software component or technology name to Development.
Missing production mappings must be resolved with their authoritative owners before a view can present them as established facts.

### Public-entry navigation

When readers need to discover available public capabilities, provide a compact entry index alongside the logical responsibility overview. Expand command, procedure, or other entry groups beneath their owning boundary; expose purpose, logical correspondence, accountable responsibilities, and the detailed contract before incidental implementation detail. Keep the initial Module/Interface diagram focused on architecture.

Related public capabilities MAY share a presentation grouping or reading level.
Grouping MUST NOT establish Module containment, Interface ownership, dependency, or execution order.
A visual layer is not an architectural layer unless the authoritative model separately establishes the relevant responsibility and relationships.
An implementation chooses its actual capability categories; REM does not require any particular public product form.

Apply the [public-entry realization model](rem-models-architecture-realization.md#public-entry-discoverability): observe existing names and source contracts, analyze role-qualified Function correspondence, then derive Feature and Module context from their existing relationships. Distinguish observed availability in inspected source from proposed correspondence and runtime qualification. An entry may involve responsibilities outside its catalog's containing Module; preserve those exact allocations.

Generate every inventory of the same entries from the authoritative owner record or link to that inventory. Mark missing correspondence explicitly. Common invocation behavior alone does not establish complete specialist coverage. Detailed syntax and procedures remain with their source contracts; readers should reach them through attributable links.

Validate entry identity within its owner, supported mapping roles, compatible references, source navigation, and agreement between inventories. A mapping change must refresh affected views without changing Function ownership or creating Scenario participation. Review semantic contributions against the actual contract; successful reference validation is not an adequacy judgment.
