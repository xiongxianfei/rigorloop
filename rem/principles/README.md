# REM principles

These are the eighteen governing principles of the proposed [RigorLoop Engineering Method](../README.md).
[Concepts](../concepts/README.md) define the terms; [models](../models/README.md) own relationship constraints; [methods](../methods/README.md) explain their application.

1. **Separate requirements from system assets.**
   Requirements express what must become or remain true; assets describe capabilities, behavior, and architecture.
2. **Keep the durable requirement hierarchy IR → SR → AR.**
   Initial needs, system obligations, and allocated obligations have distinct meanings and containment levels.
3. **Model durable capabilities and behavior as Features and Functions.**
   IR analysis confirms stakeholder-visible Features, SR analysis confirms logical Functions, and these assets evolve across requirements and Changes. Scenarios provide usage context but do not replace the durable Feature.
4. **Model durable architectural structure as Modules and Interfaces.**
   Modules express responsibility; Interfaces express interaction contracts.
5. **Allocate System Requirements through Allocated Requirements.**
   An AR remains a requirement while assigning a lower-level obligation to architecture.
6. **Allocate Functions independently to architectural responsibility.**
   Logical behavior and requirement obligations approach architecture from different directions.
7. **Keep requirement allocation and functional allocation mutually consistent.**
   Architectural responsibility must reconcile the behavior performed with the obligations it must satisfy.
8. **Use trees for true containment and typed graphs across domains.**
   Do not force the entire engineering system into one hierarchy.
9. **Store each semantic fact once and derive inverse views.**
   Multiple views should not require independently maintained copies of the same relationship.
10. **Keep stable identity independent of naming and physical location.**
    Renaming or moving an entity does not itself create a new identity.
11. **Let Changes evolve Baselines without replacing current definitions.**
    Current assets remain understandable without replaying the complete Change history.
12. **Preserve historical engineering meaning.**
    Later allocations, names, and decisions must not rewrite what an earlier state meant.
13. **Support engineering claims with applicable evidence.**
    Distinguish the intended assessment, the observations actually obtained, and the judgment they support.
14. **Govern the engineering model through a metamodel.**
    Operational Support defines valid structures, relationships, lifecycle, and maintenance rules.
15. **Keep configuration-management technology replaceable while preserving engineering semantics.**
    A tool-independent method requires controlled, recoverable engineering history without prescribing a particular technology.
16. **Make engineering definitions clear and distinguishable.**
    Each definition has a meaningful name and a precise purpose and scope that readers can understand using current authoritative information. Its name identifies the engineering purpose and subject, distinguishes neighboring definitions, and agrees with the definition's actual scope.
17. **Keep Scenarios governed, black-box, and stakeholder-observable.**
   Scenarios preserve concrete stakeholder situations with stable identity and lifecycle while avoiding internal Functions, Modules, Interfaces, or implementation sequences; they inform SR analysis rather than replacing system design.
18. **Separate logical architecture from physical/software realization.**
   Modules and Interfaces remain the durable first-class architecture assets. Material software structures, runtime/process boundaries, persistence mechanisms, deployment choices, interaction mechanisms, and technology selections are governed as subordinate realization information owned by those assets. Architecture views are derived from authoritative semantic outputs and must not become a second source of truth.
   Separating realization facets in storage preserves their owner and logical meaning; it does not by itself create new identities or independent lifecycles.

## Applying the principles

[Requirement analysis](../methods/requirement-analysis.md) owns the selected 5W2H method and clear IR naming guidance.
[Scenario Analysis](../methods/scenario-analysis.md) develops first-class stakeholder-visible Scenarios, confirms the durable Feature needed by the IR, and identifies candidate behavior for later confirmation through SR analysis.
The [Scenario model](../models/scenarios.md) applies Principle 17 to Scenario identity, lifecycle, cardinality, and black-box boundaries.
[Functional Analysis](../methods/functional-analysis.md) confirms Functions from SR obligations without mirroring the requirement tree.
[Architecture Allocation](../methods/architecture-allocation.md) assigns one accountable primary Module per Function and exactly one Module per AR.
[Architecture Design](../methods/architecture-design.md) applies Principle 18 by preserving logical Module/Interface meaning while defining the material physical/software realization as subordinate architecture views.
The [System Design model](../models/system-design.md#clear-names-and-boundaries) applies Principle 16 to Feature and Function names and definitions.
Prefer an action and its subject, adding a condition when it distinguishes the intended meaning; semantic clarity matters more than a rigid grammatical pattern.
An entity's stable identity remains independent of its wording.
[Operational Support](../models/operational-support.md#naming-and-location) owns representation conventions such as deriving readable filenames from identities and titles; Principle 16 does not impose a filesystem layout.
