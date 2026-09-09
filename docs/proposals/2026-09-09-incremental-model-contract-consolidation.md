# Replace System's Spec Dependencies through Bounded Model Transfers

## Challenge

[System's responsibility inventory](../design/system/system.md#responsibility-inventory) still routes several current responsibilities through feature specs, ADRs and the mixed system architecture. These sources combine enduring rules, adopted amendments, completed rollout conditions and historical decisions. Readers must reconcile them to determine the current contract, while a model-directory inventory alone cannot establish which obligations have actually moved.

The completed Skill initiative demonstrates a bounded transfer with precise retained rules, consumer reconciliation and readable history. Its [successful Verify](../changes/2026-09-08-skill-model-proposal-family-pilot/verify-report.json) also exposes a current navigation gap: System still describes common Skill ownership prospectively. Meanwhile, the [retained Skill Contract](../../specs/skill-contract.md) legitimately contains specialist plan and boundary-method obligations. Correcting that row must distinguish completed common ownership from the remaining specialist authority.

Removing spec links without transferring their surviving meaning would hide dependencies. Moving every source into models in one initiative would make ownership, compatibility and proof difficult to review.

## Goals

Make System an accurate entry point to current responsibility owners. Replace its normative dependence on legacy specs incrementally, with one accessible current definition for each transferred obligation and its existing applicability.

Preserve useful requirements, decisions, failure behavior, compatibility and historical evidence. Demonstrate coherent adoption through actual consumers, rather than treating document creation or fewer spec links as success.

Establish a bounded next consolidation and explicit receiving ownership for the remainder. Keep model boundaries based on coherent responsibilities rather than individual skills, filenames or adoption batches.

## Scope and non-goals

This proposal selects an incremental direction and a first substantive candidate. It does not commission implementation of every candidate model together.

| Initial goal | Initial goal treatment | Scope budget treatment | Destination and boundary |
| --- | --- | --- | --- |
| Make System reflect completed common Skill adoption | in scope | same-slice dependency | Reconcile current owner wording against adopted evidence; preserve separately owned specialist clauses. Do not repeat the proposal-family pilot. |
| Replace legacy normative dependencies one responsibility at a time | in scope | core to this proposal | Apply existing Design displacement and coordinated-adoption conventions; no new migration framework. |
| Establish Validation Execution ownership | in scope | first-slice candidate | Receive FU-012's remaining validation responsibility; preserve current execution, gate and proof contracts. Design must bound exact sources and consumers. |
| Consolidate Distribution | deferred follow-up | separate proposal | Receive the distribution portion of FU-013; package generation and invocation transformation require their own bounded decision. |
| Consolidate Installation | deferred follow-up | separate proposal | Receive the installation portion of FU-013; trust, managed state and recovery remain with their existing owners until adoption. |
| Consolidate Release | deferred follow-up | separate proposal | Receive the release portion of FU-013; publication authority and release evidence remain separately governed. |
| Resolve specialist Skill remainder and other unmigrated responsibilities | deferred follow-up | separate proposal | FU-014 and the relevant capability owners inventory actual surviving obligations before selecting existing or new model destinations. No generic remainder model is selected. |
| Improve the remaining 17 skills | deferred follow-up | separate proposal | FU-015–018 remain distinct adoption work; common ownership transfer does not certify or rewrite those skills. |

Necessary consumer, validation and navigation corrections belong to the selected transfer. A shared dependency that cannot be reconciled within its boundary returns to Design or a separately approved scope decision; it does not silently recruit another consolidation initiative.

Excluded are a repository-wide rewrite, one model per skill, a fixed final directory catalogue, a second universal contract manual, new record schemas or migration services, new workflow gates, blanket test deletion, whole-directory removal, changes to specialist judgment policy, publication, release execution and real customer installation. Operational manifests, templates and resources are not archival prose merely because a nearby specification is retired.

## Governing principle

> Replace a legacy authority only when its surviving contract has one precise model owner and its consumers have coherently adopted that owner.

## Proposed direction

### Organize ownership before organizing files

Use the existing [Design convention](../design/design/design.md): one living normative Design per coherent responsibility, with System describing composition and referencing local owners. Skills apply these contracts through their specialist methods and selected resources. A skill family is an adoption batch, not automatically a model.

Validation Execution should own how applicable checks are selected and executed, how product gates compose their required evidence, and how execution outcomes and failures are reported. Skill retains content and resource invariants; Test retains test-quality criteria; Review and Closeout retains assessment authority, applicability and closeout consequences; Workflow retains coordination. Record Format and CLI retain representation and recording mechanics. Existing installer and release owners retain their execution and authorization boundaries.

### Begin with a bounded validation transfer

Receive the remaining validation work identified by [FU-012](../follow-ups.md), inspecting the currently applicable portions of the [published-skill-first contract](../../specs/published-skill-first-repository-simplification.md), retained validation architecture and their amendments. Design must select the smallest complete responsibility boundary and identify directly affected consumers. This proposal does not declare every clause in those documents current or safe to retire.

Include System's bounded common Skill ownership reconciliation. Its successful adoption is existing evidence, not a new validation-model deliverable. Retained plan-asset and boundary-method clauses must continue to have explicit current owners; moving them into Skill merely to remove the final spec link is not selected.

The first slice may finish when its reviewed validation responsibility and necessary composition corrections are coherently adopted. Distribution, Installation, Release and remaining skill improvement need not complete first. If inspection reveals an inseparable dependency that materially changes this boundary, return for a scope decision instead of expanding silently.

### Transfer complete meaning and preserve applicability

For each selected source boundary, reconcile the actual surviving requirement, its population, trigger and required outcome, relevant decisions, exceptions, later supersessions and representative acceptance intent. Place the surviving normative meaning in the owning model with enough precision for authors and validator maintainers to apply it without reconstructing archived prose.

Use the existing model displacement map to identify destinations, explicit supersession, justified retention and historical-only content. Include unnumbered obligations and important rationale as well as numbered requirements. Preserve historical IDs and judgments on their original subjects; do not reactivate superseded rollout gates or silently tighten non-adopting populations.

A model must explain behavior and its technical realization to the extent needed for assessment. It must not become a pasted collection of old specifications, nor substitute a general promise to preserve behavior for the only precise rule definition.

### Adopt through the real consumers

A transfer includes the relevant skills, validators, scripts, templates, generated candidates, metadata and current navigation that actually consume the selected contract. Design identifies the interactions; Delivery allocates exact edits and concrete proof under existing contracts. Necessary compatibility corrections preserve useful protective assertions and approved failure boundaries.

Independent assessment must judge contract completeness, coherent ownership and producer/consumer behavior. Mechanical checks establish their bounded structural and execution facts. Existing independent milestone assessments, fresh final whole-change Code Review and distinct successful Verify remain required before replacement authority is relied upon. A new file, a saved record or an isolated package pass is insufficient.

### Retire authority while retaining useful history

After coherent adoption, System points to the model as the current owner. Superseded source definitions cease to be independently maintained. Useful originals remain directly readable with provenance and necessary related navigation; mixed sources retain an explicit current remainder until its own transfer.

Source-path retention may preserve historical dependencies without preserving competing normative authority. Operational inputs remain at their existing paths unless their actual consumers and identity-sensitive projections are coherently relocated. No source is deleted merely because its filename matches a selected model.

### Continue through separately bounded decisions

Distribution, then Installation, then Release is a useful candidate order because package production, package application and publication have distinct contracts and dependencies. It is a direction for evaluating subsequent slices, not a fixed implementation schedule or a requirement to finish all models together. Existing owners remain usable dependencies during each transfer.

The repository maintainer remains accountable for the remainder. Route assigns receiving proposal and Design owners through the existing FU-012–014 records as each bounded initiative is selected. Those records should name any still-unmigrated obligations and next decision; mutable progress does not belong in System or a new adoption registry. Capability adoption remains in FU-015–018.

## Feasibility

**Assessment: feasible as successive bounded contract transfers; the exact validation slice still requires Design inspection.**

The repository already has living-model conventions, a System responsibility inventory, durable follow-up ownership and a completed Skill consolidation with original-byte preservation and independent assessment. These establish a practical approach without requiring a new storage format, packaging mechanism or lifecycle stage.

The inspected material identifies current owner boundaries and likely source families. It does not establish a complete validation dependency graph, prove that every legacy clause survives unchanged, or identify individual files safe to delete. Legacy validation entrypoints and historical proof requirements need explicit applicability assessment; copying their old wording would not establish current policy.

The minimum next Design package is the selected Validation Execution responsibility, scoped System composition corrections and any exact amendments needed to keep affected existing owners and consumers coherent. Missing ownership or an indivisible cross-owner dependency must be resolved before dependent adoption. No performance gain, token saving, file-count reduction or repository-wide conformance result is claimed.

## Impact and major trade-offs

Incremental transfer leaves temporary coexistence between models and retained specs. Explicit clause ownership and adoption boundaries make that coexistence reviewable; a universal conversion deadline would create pressure to retire incomplete contracts.

Preserving readable originals can increase file count while reducing competing authority. The benefit is a usable current contract and trustworthy history, not fewer files. Consumer reconciliation can exceed the size of the model edit, so each slice needs a clear boundary and evidence-backed dependency dispositions.

This direction preserves currently governing behavior by default. Any desired change to validation policy, release permissions, installation semantics or specialist methods requires an explicit decision by its owning stage rather than being bundled into consolidation.

## Decision requested

Approve replacing System's remaining normative spec dependencies through independently bounded, responsibility-owned model transfers, using existing Design, Delivery, review and Verify contracts.

Select Validation Execution as the first substantive consolidation candidate, with the necessary reconciliation of completed common Skill ownership in System. Preserve explicit specialist remainders and existing policy, execution and publication boundaries.

Keep Distribution, Installation, Release, other unmigrated responsibilities and remaining skill adoption in separately approved work with named receiving ownership. Permit the first slice to close independently once its exact transfer and consumers are coherently adopted.

Approval permits scoped Design work. It does not approve exact model requirements, source moves or deletions, test retirement, implementation, publication, customer adoption or the creation of every candidate model at once.
