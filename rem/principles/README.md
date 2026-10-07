# REM principles

These are the twenty-two governing principles of the proposed [RigorLoop Engineering Method](../README.md).
A principle explains a deeper engineering relationship and why it matters, then connects that explanation to a commitment REM preserves.
Each document separates **Relationship and why**, **REM commitment**, and **Application** so readers can distinguish the reasoning, the selected rule, and its owning Model or Method.
These explanations give the rationale for REM's choices; they do not claim that every chosen structure is a universal engineering law or that the method's effectiveness has been empirically established.
[Concepts](../concepts/README.md) define the terms; [models](../models/README.md) own relationship constraints; [methods](../methods/README.md) explain their application.

| Principle | Commitment |
| --- | --- |
| 1 | [Separate requirements from system assets](01-separate-requirements-from-system-assets.md) |
| 2 | [Keep the durable requirement hierarchy IR → SR → AR](02-keep-the-durable-requirement-hierarchy-ir--sr--ar.md) |
| 3 | [Model durable capabilities and behavior as Features and Functions](03-model-durable-capabilities-and-behavior-as-features-and-functions.md) |
| 4 | [Model durable architectural structure as hierarchical Modules and Interfaces](04-model-durable-architectural-structure-as-hierarchical-modules-and-interfaces.md) |
| 5 | [Allocate System Requirements through Allocated Requirements](05-allocate-system-requirements-through-allocated-requirements.md) |
| 6 | [Allocate Functions independently to architectural responsibility](06-allocate-functions-independently-to-architectural-responsibility.md) |
| 7 | [Keep requirement allocation and functional allocation mutually consistent](07-keep-requirement-allocation-and-functional-allocation-mutually-consistent.md) |
| 8 | [Use trees for true containment and typed graphs across domains](08-use-trees-for-true-containment-and-typed-graphs-across-domains.md) |
| 9 | [Store each semantic fact once and derive inverse views](09-store-each-semantic-fact-once-and-derive-inverse-views.md) |
| 10 | [Keep stable identity independent of naming and physical location](10-keep-stable-identity-independent-of-naming-and-physical-location.md) |
| 11 | [Let Changes evolve Baselines without replacing current definitions](11-let-changes-evolve-baselines-without-replacing-current-definitions.md) |
| 12 | [Preserve historical engineering meaning](12-preserve-historical-engineering-meaning.md) |
| 13 | [Support engineering claims with applicable evidence](13-support-engineering-claims-with-applicable-evidence.md) |
| 14 | [Govern the engineering model through a metamodel](14-govern-the-engineering-model-through-a-metamodel.md) |
| 15 | [Keep configuration-management technology replaceable while preserving engineering semantics](15-keep-configuration-management-technology-replaceable-while-preserving-engineering-semantics.md) |
| 16 | [Make engineering definitions clear and distinguishable](16-make-engineering-definitions-clear-and-distinguishable.md) |
| 17 | [Keep Scenarios governed, black-box, and stakeholder-observable](17-keep-scenarios-governed-black-box-and-stakeholder-observable.md) |
| 18 | [Preserve responsibility ownership through technical realization](18-preserve-responsibility-ownership-through-technical-realization.md) |
| 19 | [Generate architecture views from one authoritative semantic model](19-generate-architecture-views-from-one-authoritative-semantic-model.md) |
| 20 | [Preserve encapsulation through Module hierarchy](20-preserve-encapsulation-through-module-hierarchy.md) |
| 21 | [Make public capabilities traceable to architectural responsibility](21-make-public-capabilities-traceable-to-architectural-responsibility.md) |
| 22 | [Reconcile incoming requests before creating requirements](22-reconcile-incoming-requests-before-creating-requirements.md) |

## Applying the principles

[Requirement analysis](../methods/requirement-analysis.md) applies Principle 22 by reconciling each RR with current requirement knowledge before reusing, refining, or creating IRs and SRs; it also owns the selected 5W2H method and clear IR naming guidance.
[Scenario Analysis](../methods/scenario-analysis.md) develops first-class stakeholder-visible Scenarios, confirms the durable Feature needed by the IR, and identifies candidate behavior for later confirmation through SR analysis.
The [Scenario model](../models/scenarios.md) applies Principle 17 to Scenario identity, lifecycle, cardinality, and black-box boundaries.
[Functional Analysis](../methods/functional-analysis.md) confirms Functions from SR obligations without mirroring the requirement tree.
[Architecture Allocation](../methods/architecture-allocation.md) applies Principles 4, 8, and 20 by establishing coherent Module containment, assigning one accountable primary Module per Function and exactly one Module per AR at the lowest coherent boundary, and making boundary-crossing Interface exposure explicit.
[Architecture Design](../methods/architecture-design.md) applies Principles 18 and 20 by preserving logical Module/Interface hierarchy and encapsulation while defining material physical/software realization as subordinate architecture information.
[4+1 Architecture Views](../methods/architecture-views.md) applies Principles 19 and 20 by generating Logical, Process, Development, Physical, and Scenario projections from the authoritative architecture and Scenario knowledge, beginning from the highest useful Module level and revealing contained responsibilities progressively.
The [public-entry realization model](../models/architecture-realization.md#public-entry-discoverability) and [Logical view navigation](../methods/views/logical.md#public-entry-navigation) apply Principle 21 without introducing a second capability hierarchy or transferring specialist behavior to a shared invocation owner.
The [System Design model](../models/system-design.md#clear-names-and-boundaries) applies Principle 16 to Feature and Function names and definitions.
Prefer an action and its subject, adding a condition when it distinguishes the intended meaning; semantic clarity matters more than a rigid grammatical pattern.
An entity's stable identity remains independent of its wording.
[Operational Support](../models/operational-support.md#naming-and-location) owns representation conventions such as deriving readable filenames from identities and titles; Principle 16 does not impose a filesystem layout.
