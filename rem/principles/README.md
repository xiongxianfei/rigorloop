# REM principles

These are the twenty-two governing principles of the proposed [RigorLoop Engineering Method](../README.md).
[Concepts](../concepts/README.md) define the terms; [models](../models/README.md) own relationship constraints; [methods](../methods/README.md) explain their application.

1. **Separate requirements from system assets.**

    Requirements express what must become or remain true; assets describe capabilities, behavior, and architecture.

2. **Keep the durable requirement hierarchy IR → SR → AR.**

    Initial needs, system obligations, and allocated obligations have distinct meanings and containment levels.

3. **Model durable capabilities and behavior as Features and Functions.**

    IR analysis confirms stakeholder-visible Features, SR analysis confirms logical Functions, and these assets evolve across requirements and Changes. Scenarios provide usage context but do not replace the durable Feature.

4. **Model durable architectural structure as hierarchical Modules and Interfaces.**

    Modules express responsibility and may contain Modules that refine broader responsibility; Interfaces express interaction contracts.

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
    Present engineering meaning first. Stable identities support traceability; readers should not need to interpret identifiers to understand a responsibility or contract.

17. **Keep Scenarios governed, black-box, and stakeholder-observable.**

    Scenarios preserve concrete stakeholder situations with stable identity and lifecycle while avoiding internal Functions, Modules, Interfaces, or implementation sequences; they inform SR analysis rather than replacing system design.

18. **Preserve responsibility ownership through technical realization.**

    Modules and Interfaces remain the durable first-class architecture assets. Material software structures, runtime/process boundaries, persistence mechanisms, deployment choices, interaction mechanisms, and technology selections are governed as subordinate realization information owned by those assets.
    The technical model makes component responsibilities, contracts and realization mappings explicit. Its technical structure may be presented within the Logical View; that presentation does not turn components into Modules or transfer accountability. Development explains source/package/build organization, Process explains execution, and Physical explains placement using the same owned design.

19. **Generate architecture views from one authoritative semantic model.**

    Use complementary architecture views to address distinct concerns. REM adopts the five 4+1 concerns through its [documented adaptation](../methods/architecture-views.md#adoption-and-adaptation-in-rem): Logical, Process, Development, Physical, and Scenario. Derive them from authoritative engineering knowledge and choose presentations that make their concerns understandable. Views may select, collapse, or emphasize information for comprehension, but they must preserve semantic meaning, ownership, and provenance and must not become a second source of truth.
    Keep authoritative knowledge, semantic projection, and rendered presentation distinct. Knowledge may include structured facts and authored explanations under their declared owners; rendering an owning explanation does not create another source of architecture truth. Identify the source state and derivation rules so views remain traceable and regenerable.
    Present one useful responsibility level at a time with navigable detail. Assess both semantic fidelity and the intended reading tasks in the rendered view; a complete generated inventory alone does not establish comprehension.
    For the Process View, select model kinds by runtime concern rather than visual preference: use runtime topology as the primary whole-system projection when runtime concerns are material, and use interaction, lifecycle, control-flow, timing, or formal-concurrency models only when authoritative runtime information supports those concerns. At a focused Module or operation scope, select the explanation that answers the concern without requiring an additional topology diagram. Never infer execution order from Logical Module/Interface reachability.
    Visible labels may shorten canonical names when their meaning remains faithful and unambiguous in context. Keep full names and stable identities accessible through detail or reference without requiring their repetition throughout a diagram. Presentation labels do not create new identities or change authoritative definitions or relationships.

20. **Preserve encapsulation through Module hierarchy.**

    Parent Modules are real architectural responsibility boundaries. Child Modules refine their parent responsibility; allocations target the lowest coherent accountable Module; descendant allocations roll up for comprehension without duplicating ownership; and a child-provided Interface remains internal to its containing boundary unless explicitly exposed through each parent boundary it crosses.
    Assign Interface ownership to the Module accountable for the contract and assign its realizing behavior separately. A parent may own a contract realized through child responsibilities; implementation location alone does not determine its provider.

21. **Make public capabilities traceable to architectural responsibility.**

    A reader should be able to trace a public entry's name and purpose to its logical behavior, accountable responsibilities, and realization. Record the mapping once and derive navigable views. A public command, procedure, or other entry does not automatically require its own Feature, Module, or Interface. Distinguish observed entry existence from proposed behavioral correspondence, preserve incomplete mappings, and never infer ownership or satisfaction from catalog placement.

22. **Reconcile incoming requests before creating requirements.**

    Treat a request, proposal, issue, incident, observation, or other RR as analysis input rather than an approved requirement. Compare it with current IRs, SRs, Scenarios, Features, and known constraints before creating new durable definitions. Reuse or refine existing requirements when their meaning fits, create new requirements only when a distinct durable need or obligation is justified, and retain explicit provenance, conflict, uncertainty, or no-change dispositions.

## Applying the principles

[Requirement analysis](../methods/requirement-analysis.md) applies Principle 22 by reconciling each RR with current requirement knowledge before reusing, refining, or creating IRs and SRs; it also owns the selected 5W2H method and clear IR naming guidance.
[Scenario Analysis](../methods/scenario-analysis.md) develops first-class stakeholder-visible Scenarios, confirms the durable Feature needed by the IR, and identifies candidate behavior for later confirmation through SR analysis.
The [Scenario model](../models/scenarios.md) applies Principle 17 to Scenario identity, lifecycle, cardinality, and black-box boundaries.
[Functional Analysis](../methods/functional-analysis.md) confirms Functions from SR obligations without mirroring the requirement tree.
[Architecture Allocation](../methods/architecture-allocation.md) applies Principles 4, 8, and 20 by establishing coherent Module containment, assigning one accountable primary Module per Function and exactly one Module per AR at the lowest coherent boundary, and making boundary-crossing Interface exposure explicit.
[Architecture Design](../methods/architecture-design.md) applies Principles 18 and 20 by preserving logical Module/Interface hierarchy and encapsulation while defining material physical/software realization as subordinate architecture information.
[4+1 Architecture Views](../methods/architecture-views.md) applies Principles 19 and 20 by generating Logical, Process, Development, Physical, and Scenario projections from the authoritative architecture and Scenario knowledge, beginning from the highest useful Module level and revealing contained responsibilities progressively.
The [public-entry realization model](../models/architecture-design.md#public-entry-discoverability) and [Logical view navigation](../methods/architecture-views.md#public-entry-navigation) apply Principle 21 without introducing a second capability hierarchy or transferring specialist behavior to a shared invocation owner.
The [System Design model](../models/system-design.md#clear-names-and-boundaries) applies Principle 16 to Feature and Function names and definitions.
Prefer an action and its subject, adding a condition when it distinguishes the intended meaning; semantic clarity matters more than a rigid grammatical pattern.
An entity's stable identity remains independent of its wording.
[Operational Support](../models/operational-support.md#naming-and-location) owns representation conventions such as deriving readable filenames from identities and titles; Principle 16 does not impose a filesystem layout.
