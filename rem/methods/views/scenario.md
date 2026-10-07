# Scenario View (+1)

## Scenario View (+1)

The Scenario View answers:

> How does the architecture participate in satisfying one governed stakeholder Scenario end-to-end?

The Scenario View MUST be anchored by an existing governed Scenario.
The authoritative Scenario remains black-box and stakeholder-observable; do not add internal Modules, Interfaces, or call sequences to the Scenario definition itself.

Generate an architecture participation slice by traversing relevant relationships such as:

```text
Scenario
    ↓ informs
SR
    ├── confirms → Function ──> Module
    └── derives  → AR ─────────> Module
                                │
                                ├── contained by → parent Module(s)
                                ↕
                             Interface
                       (internal or exposed)
                                ↓
                       relevant realization
```

The Scenario View MAY overlay relevant Logical, Process, Development, or Physical details when they help explain how the scenario is satisfied.

### Outcome walkthroughs

Organize a Scenario walkthrough around its expected outcome and its material alternative and failure outcomes. Begin with the stakeholder situation and full observable outcome, then explain the relevant obligations, accountable responsibilities, collaboration contracts and realization. Keep broad traceability available as supporting detail. An outcome with incomplete architectural explanation must remain visible.

An outcome walkthrough SHOULD make these questions answerable:

- Which existing SR or AR criteria are relevant to this outcome, and what is their analysis basis?
- Which Modules hold the selected allocations, and which Modules provide the applicable Interface contracts?
- Which recorded Process interactions or lifecycle details help explain the outcome and its failure boundaries?
- Which Development software mappings and Physical placements apply within the selected scope?
- Which test organization is relevant context, what outcome-specific coverage has actually been established, and what applicable evidence exists?
- Which connections or explanations remain unselected, incomplete or unresolved?

Operational Support MAY define a bounded reading profile selecting canonical outcomes, criteria and realization references. The profile supplies explanatory scope; it does not create requirements, allocations, execution order or assurance claims. Resolve substantive outcome text, criteria, responsibilities and realization details from their authoritative sources. Short display labels may aid navigation but must retain access to the complete canonical meaning and source attribution. Validate selected references and their scope before generating the view.

Scenario records remain stakeholder-facing. Do not embed internal architecture in them to support presentation. New guarantees, responsibilities or interactions discovered during walkthrough analysis belong with the appropriate requirement or architecture owner before the view relies on them.

Test groups selected through a responsibility or a source contract are contextual test organization. Establish an outcome-specific coverage argument before presenting them as verifying that outcome; actual execution evidence and its applicability require their separate assessment. Missing evidence in a bounded projection means none is linked there, not that no evidence exists elsewhere. Similarly, an unselected realization detail is a reading gap, not proof that the architecture lacks it.

### Participation and consistency

Reachability establishes relevant participation, not execution order. An SR or Feature may cover behavior beyond one Scenario, so a reachable Function is not automatically a step in that Scenario. Generate internal sequencing, concurrency, and placement only from sufficient authoritative architecture information. Prose-only realization may support an attributed explanation while leaving a more detailed diagram deferred.

When an allocated child participates beneath a parent-owned contract, a Scenario projection MAY show the declared ancestor contract as boundary context. Preserve the exact provider and source relationship, and keep that context separate from allocated behavior. An ancestor's `provides` relationship alone does not establish that its Interface executes in the Scenario or that every descendant realizes it.

Select Interface context for each Scenario from its declared analysis scope and actual relationships. A participating consumer's selected Interface may reveal a provider outside its ancestry; show that exact contract owner as context without inventing an executing participant. A shared ancestor or a contract selected for another Scenario is insufficient to make it applicable here. Expose relevant recorded design limits so a bounded contract contribution cannot appear to complete the entire Scenario.

Use the Scenario View to validate the other four views:

- Does every required Function have accountable architecture?
- Do the AR obligations have responsible Modules?
- Are required Module collaborations represented by Interfaces?
- Can runtime/software/deployment realization support the required outcomes?
- Are failure, incomplete, or alternative Scenario outcomes left without architectural responsibility?

Investigate a broken or unexplained path against the authoritative sources.
A missing architectural obligation, responsibility, or contract is an architecture-analysis finding; a relationship omitted or misrepresented by the projection is a projection finding.
Apply [correction ownership](../view-presentation.md#correction-ownership) and regenerate the affected view after reconciliation.
