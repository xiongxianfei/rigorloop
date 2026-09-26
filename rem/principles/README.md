# REM principles

These are the fifteen governing principles of the proposed [RigorLoop Engineering Method](../README.md).
[Concepts](../concepts/README.md) define the terms; [models](../models/README.md) own relationship constraints; [methods](../methods/README.md) explain their application.

1. **Separate requirements from system assets.**
   Requirements express what must become or remain true; assets describe capabilities, behavior, and architecture.
2. **Keep the durable requirement hierarchy IR → SR → AR.**
   Initial needs, system obligations, and allocated obligations have distinct meanings and containment levels.
3. **Model durable capabilities and behavior as Features and Functions.**
   These assets evolve across requirements and Changes.
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

## Applying the principles

[Requirement analysis](../methods/requirement-analysis.md) owns the selected 5W2H method and clear IR naming guidance.
An IR's display name should communicate its need while its stable identity remains independent of that wording.
These application rules refine how authors work; they do not add another canonical principle or replace the models' explicit requirement levels.
