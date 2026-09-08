# Unified Design Authoring and Bounded Model Consolidation

## Challenge

RigorLoop is moving toward one living Design per model, but its authoring skills still expose two overlapping responsibilities. The `spec` and `architecture` skills already instruct authors to maintain assigned living models, while their ordinary roles and handoffs continue to describe separate specification, architecture, and ADR work. A rename alone would preserve that inconsistency.[^1]

The existing system architecture also combines current model references with extensive historical material and separate architecture-package/ADR ownership. Readers must distinguish current engineering obligations from superseded descriptions before making a change.[^2]

Model-centered authoring must address more than local document structure. The project needs a clear account of how models cooperate, who owns shared contracts, which system-wide properties their composition must preserve, and what evidence can assess important design claims. Consolidating every existing document at once would make delivering the new skill depend on a repository-wide migration.

## Goals

Deliver one `design` authoring skill that combines behavioral requirements, technical realization, important decisions, and verification intent in the owning living Designs. Keep independent `design-review` and existing downstream responsibilities.

Make system-and-component relationships understandable without duplicating their contracts. Let technical feasibility inform the selected behavior while preserving approved product direction. Establish meaningful representative acceptance scenarios from which concrete tests can be derived.

Complete a first bounded migration that demonstrates the authoring and composition method, retires its superseded current authorities, and leaves the remaining consolidation explicitly owned by later changes. The destination is one current Design set; repository-wide completion is not this initiative's acceptance condition.

## Scope and non-goals

The initial intent and scope budget are preserved as follows:

| Requested outcome | Initial goal treatment | Scope budget treatment | Boundary |
| --- | --- | --- | --- |
| Unified `design` authoring skill | in scope | core to this proposal | Replace separate normal spec/architecture authoring with one coherent contract, resources, and handoff. |
| Models as the center of engineering design | in scope | core to this proposal | Maintain behavior, structure, rationale, boundaries, and acceptance under one owner per coherent responsibility. Governance, approved direction, and mutable work state retain their existing owners. |
| Many models cooperating within one system | in scope | core to this proposal | Define system composition, shared-contract ownership, affected-model coordination, and a usable system-level view for the migrated slice. |
| How to assess Design and test its realization | in scope | core to this proposal | Distinguish design assessment and feasibility evidence from implementation verification; retain representative scenarios, not an exhaustive test whitelist. |
| Coordinated governance, review, routing, planning, validation, and package consumers | in scope | same-slice dependency | Reconcile affected consumers and governing amendments with the unified authoring path; preserve their separate responsibilities. |
| First document migration | in scope | separate implementation slice | Reconcile the design-authoring/model-composition responsibility and its directly affected sources and consumers within this initiative. |
| Complete removal of remaining specifications, architecture documents, and ADR authorities | deferred follow-up | deferable follow-up | Later bounded changes consolidate remaining responsibilities and retire their superseded sources. |
| Release/publication and customer-project adoption | out of scope | out of scope | Retain separately authorized execution and adoption boundaries. |

The proposed first migration boundary is the **design-authoring and model-composition responsibility**: the relevant architecture-package method, Workflow's model-document convention, system-level ownership/composition sections, and directly related method decisions. Design must identify the exact selected sections, decisions, model subjects, and consumers before Delivery allocates their edits. This does not include rewriting the entire system architecture or every feature specification.

Remaining consolidation is owned by the repository maintainer as direction owner, with Route responsible for assigning later bounded changes to the affected Design owners through the existing follow-up ownership surface. Design must name retained responsibilities and their current owners; Delivery must make the follow-up assignments durable before this initiative closes. This proposal does not authorize execution of those later changes or make the project map their work tracker.

Out of scope are a new lifecycle gate, a standalone test-spec stage, a per-test ledger, automatic documentation migration, a new model-management service, changes to runtime record formats, or unrelated product behavior. Unchanged legacy documents and historical review records are not blanket deletion targets.

## Governing principle

> Give each engineering obligation and shared interaction one current Design owner, and make the basis for assessing it explicit.

## Proposed direction

### One authoring skill, one reconciled engineering contract

Replace the separate normal authoring responsibilities with `design`. It creates or revises the smallest justified set of living model documents, combining required behavior, technical constraints, structural choices, important decision rationale, and acceptance intent. Features update their affected models rather than creating another feature-specific spec/architecture pair. Use the established model-centered `docs/design` layout and model-owned supporting examples.

Behavior and technical realization are reconciled together. A feasibility constraint may require revising the proposed behavior, but the author must return a material product-direction change to its owner rather than silently weaken an approved goal for implementation convenience.

Keep `design-review` independent. Update its subject selection and correction handoffs to assess the exact affected model set and relevant relationships, rather than requiring a fixed architecture/specification/ADR tuple. Proposal, Delivery planning, implementation, Code Review, and Verify retain their distinct roles.

The normal public authoring path becomes `design` at coordinated adoption. Design must specify the withdrawal or compatibility treatment of the old invocation names; they must not remain independent competing authoring contracts. Removing an entry point does not itself retire the documents it previously authored.

### System composition without duplicate component contracts

Establish a system-level Design view that explains external boundaries, the model inventory, responsibility relationships, significant dependencies, end-to-end behavior, and system-wide quality and failure obligations. Its purpose is to explain the assembled system, not to copy every component's requirements. In this slice, identify the selected responsibilities and refer to the declared owners of unmigrated areas without claiming those areas have been consolidated.

Each component model owns its local contract. Each shared contract has one named owner, with references from its consumers. A system-level model owns genuinely system-wide composition obligations; it is not a higher-priority document that can silently override component rules or existing governance. A submodel is a coherent responsibility, not automatically one old file, feature, team, or implementation class.

Use the existing structural and runtime-view methods where useful. Preserve their reasoning value while reconciling their packaging with the living-model convention; do not create another architecture copy simply to retain the old file layout.[^3]

When an interface or shared assumption changes, the author identifies affected consumers and required reconciliation. Review covers the changed models and relevant interactions; neither every change nor every reader must load the whole repository. Existing CLI assistance remains mechanical—selection, identities, records, and structural checks—not a semantic dependency or readiness engine.

### Design must explain how its claims can be assessed

Every adopted model should make its important requirements, invariants, representative conditions, and observable expected outcomes clear. Address applicable failure, compatibility, authority, recovery, and cross-model conditions, including side effects that must not occur.

Distinguish two questions:

**Is the proposed Design coherent and credible?** Use independent assessment, scenario walkthroughs, counterexamples, and targeted feasibility evidence where a material claim needs it. Expose assumptions and unresolved decisions; structural validation alone is not approval.

**Does the implementation satisfy that Design?** Define the intended outcomes and observation boundaries in Design. Delivery allocates concrete checks, commands, milestone evidence, and integrated verification; implementation supplies fixtures and assertions. Actual results remain in existing evidence records rather than becoming mutable status inside the Design.

Representative scenarios are not an exhaustive catalogue of permitted tests. Additional concrete cases may derive from justified obligations and hazards. A test's absence from the scenarios does not authorize removal. Apply the existing Test criteria and Review and Closeout policy instead of creating another owner of test adequacy or evidence applicability.[^4]

System composition must include representative integrated outcomes where local model checks alone cannot establish the required property. This does not make formal proof, a prototype, or a complete test implementation mandatory for every Design.

### Migrate authority, not merely filenames

For the first bounded slice, map each displaced requirement and material decision to its destination, explicit supersession, or justified retention outside the slice. Resolve contradictions before relying on the new contract; copying conflicting clauses into one file is not consolidation.

Preserve stable references or explicit replacement mappings. Carry forward the decision context, meaningful alternatives, consequences, and still-applicable constraints needed to understand the current Design. Do not copy every procedural review round or rewrite historical approvals to claim they assessed the consolidated document. These preservation obligations build on the existing living-model convention.[^5]

After the selected replacement is adopted, current navigation and consumer instructions point to its Design owner. Remove fully superseded sources from the current authoritative set; mixed documents retain clearly identified, unmigrated responsibilities. Historical access must remain distinguishable from current authority. Exact archival or file-removal mechanics belong to Design and authorized Delivery, not automatic authoring.

New work uses the unified authoring method. During coexistence, `design` may consume and make explicitly scoped revisions to an unmigrated source under its declared contract; it must not silently migrate it or force repository-wide conversion to complete a small change. A migrated obligation must never acquire two current owners.

### Deliver a usable first slice and explicit follow-up

Align the skill's instructions, conditional references, assets, routing and review consumers, planning handoff, validators, and supported generated packages as one coherent capability. Published guidance must work without RigorLoop's internal Design checkout and must load only the methods relevant to the invocation.

The first migration must demonstrate more than a reformatted document: the selected model responsibilities and system relationship are reconciled, their important expected outcomes are reviewable, and downstream planning can derive local and integrated proof without reconstructing separate spec and architecture authorities.

This initiative is complete when the unified authoring path and its required consumers work together, the named first slice has independently reviewed replacement ownership and verification intent, its superseded current sources have the approved disposition, and remaining consolidation has named follow-up ownership. It must not claim that all old documentation has been migrated.

## Feasibility

**Assessment: feasible as a coordinated authoring refactor and bounded consolidation; exact migration membership and consumer changes require Design.**

The current authored skills contain living-model authoring instructions, behavioral requirements, architecture reasoning, scoped v2 recording, and selectively packaged Test guidance. Workflow already specifies unified Design responsibility, one authoritative living Design per model, preserved references, and downstream verification allocation.[^1][^4][^5] The work is primarily reconciliation and integration, not inventing those responsibilities again.

The material constraints are public invocation compatibility, mixed current/historical document ownership, preservation of decision meaning, and coherent installed guidance. These inspected source surfaces support the direction; they do not establish an exhaustive migration inventory, completed implementation, or measured token savings. No direction-level feasibility blocker is identified. Governing amendments and the exact first-slice basis require independent review before adoption; unresolved competing ownership would block reliance on the replacement.

Evidence limits: this proposal uses direct, bounded inspection of the cited canonical sources. The project map describes an older compact-record baseline and is not relied on for current ownership. The installed CLI does not expose `workflow-context`; the repository CLI's discovery command returned `rejected` with incomplete discovery. Consequently no workflow selection, absence of governed work, or readiness is inferred from it. This isolated authoring invocation has no selected change ID or owning-change pointer and uses the proposal skill's portable placement default. A later governed handoff must establish its exact change context.

## Impact and major trade-offs

A unified skill removes a handoff between separate authoring responsibilities but can become too broad if it loads both old manuals in full. Keep the common method compact and specialist depth conditional.

A system-level view improves composition reasoning but can become another oversized competing document. Limit it to system-owned obligations, relationships, and references to component contracts; current component truth remains with its owner.

Incremental migration delivers the capability sooner, but temporarily retains more than one documentation format. Explicit per-responsibility ownership is required during that period. The trade-off is intentional: complete the selected first slice without declaring unrelated consolidation finished or maintaining duplicate current definitions.

Changing public skill names affects callers and packages. Their coordinated transition must be explicit; token, runtime, and document-count improvements are not assumed or used as numerical acceptance targets.

The Constitution's Review rules still require separate architecture/specification authorship and a fixed Design Review package, while the adopted Workflow model describes unified Design responsibility. This proposal requests reconciliation of those governing rules as part of the direction, not immediate override of the Constitution. Design must include the affected governance and consumer amendments in its reviewed adoption basis; current authority remains in force until that adoption.

## Decision requested

Approve delivery of one unified `design` authoring skill, coordinated independent-review and downstream consumers, system/component composition guidance, and the first bounded migration of design-authoring/model-composition responsibilities.

Approve embedding behavioral requirements, technical realization, important decisions, and representative verification intent in each owning living Design. Approve the direction of the governing amendments needed to reconcile separate authorship and fixed-package rules with that responsibility. Approve retiring superseded current authorities within the selected slice after reconciliation, while preserving historical meaning and assigning the remaining consolidation to later changes under the follow-up ownership above.

Approval selects this direction and its bounded completion criterion. It does not approve the final model inventory, exact source deletions, automatic migration, new APIs or record schemas, implementation, review outcomes, publication, or customer adoption. Those remain subject to the applicable Design, Delivery, review, and execution authority. Proposal Review is the next assessment; this artifact does not record its approval.

[^1]: [Specification skill](../../skills/spec/SKILL.md), Explicit recording, Workflow role, and Contract quality; [Architecture skill](../../skills/architecture/SKILL.md), Explicit recording, Workflow role, Scope and routing, and Universal write and handoff boundaries.
[^2]: [System architecture](../architecture/system/architecture.md), opening ownership amendments, Source of truth, Legacy architecture handling, and Architecture Decisions.
[^3]: [Architecture package method specification](../../specs/architecture-package-method.md), Goal and context and Glossary; [Architecture method guidance](../../skills/architecture/references/architecture-package-method.md), arc42 method, C4 and diagrams, and ADRs. Their existing artifact/ADR packaging is a subject of this proposal's reconciliation, not an unchanged requirement imposed on the new skill.
[^4]: [Test quality guidance](../../skills/architecture/references/test-quality.md), Derive the protection, Select meaningful cases, and Check the oracle; [Test model](../design/test/test.md) and [Review and Closeout model](../design/review-closeout/review-closeout.md) retain their declared policy ownership.
[^5]: [Workflow model](../design/workflow/workflow.md), WF-SR-07/08, Responsibility-specific updates, Model documentation and traceability, Model-centered layout and examples, and Model validation and proof mapping. These references identify the inspected repository sources, not independent confirmation of repository-wide consolidation or customer adoption.
