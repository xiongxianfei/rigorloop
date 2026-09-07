# Explicit Workflow Recording and Model-Centered Design

## Challenge

RigorLoop's compact CLI currently combines safe persistence with workflow-state derivation and a closed set of permitted transitions. Correction work has exposed circular dependencies: revised artifacts conflict with retained review identities, authoring owners cannot always reach the required correction state, and completed work cannot always be reopened through a permitted path. Extending the transition engine to address each case increases protocol complexity and can make the tool itself prevent responsible agents from recording necessary corrections.

Design information is also fragmented across feature specifications, architecture documents and ADRs. A single model's requirements, behavior, structure and decisions must be reconciled across several files, sometimes repeated for successive features. This adds document coordination without necessarily adding an independent engineering decision.

The user requests a different division of responsibility: agents decide workflow status and record it explicitly through a simpler CLI, while each coherent model has one authoritative Design file. The intent is not to remove engineering rigor, but to keep workflow judgment with responsible people and agents and reduce competing sources of design truth.

## Goals

- Make the CLI a dependable tool for inspecting, validating and recording explicit updates, not an automatic workflow-state engine.
- Keep stage selection, ownership, correction, review judgment and readiness decisions with their responsible agents and human decision owners.
- Retain safe persistence, explicit identities, conflict detection and recoverability without using a closed transition graph to dictate workflow decisions.
- Maintain one authoritative Design file per model, combining its requirements, architecture, behavior, important decisions, boundaries and acceptance criteria.
- Let features update the models they affect rather than create a new mandatory Design package for every feature.
- Preserve independent review, current evidence, traceability and resumability without requiring Git, PR access or chat history.

## Scope and non-goals

Here, a model means a coherent part of the system with its own concepts, responsibilities, rules and boundaries. It does not mean an AI model, a single class, a database table, a feature or a change request. Workflow and CLI are illustrative model boundaries, not a final inventory selected by this proposal.

### Initial intent treatment

| Goal or concern | Treatment | Destination |
| --- | --- | --- |
| CLI records status rather than changing it automatically | in scope | Explicit recording responsibility boundary |
| Avoid workflow deadlocks caused by CLI transition rules | in scope | Agent-owned transitions and correction decisions |
| One Design file per model, not per feature | in scope | Model-centered documentation and ownership |
| Preserve useful requirements, architecture and decisions | in scope | Unified model Design content rather than mandatory sidecar documents |
| Preserve independent review and trustworthy evidence | in scope | Workflow skills, review and Verify obligations |
| Keep the earlier goal of removing mandatory final Code Review visible | deferred follow-up | The existing closeout-simplification proposal retains that separate decision; this proposal neither activates nor revokes it |
| Implement the earlier correction-engine extension as a prerequisite | rejected option | It assumes the automatic-transition direction this proposal replaces; necessary compatibility work must be justified under the new direction |
| Automatically convert existing records or delete older Design documents | out of scope | Adoption and historical disposition require explicit downstream decisions |

### Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Separate workflow decisions from CLI recording | core to this proposal | Directly addresses the user-requested simplification |
| One authoritative Design file per model | core to this proposal | Removes the mandatory split of one model across document types |
| Mechanical validation, conflict protection and recoverable writes | same-slice dependency | Simpler orchestration must not compromise stored data |
| Agent responsibility, independent review and explicit correction updates | same-slice dependency | Removing engine-owned transitions leaves obligations that need named owners |
| Exact commands, update formats, model inventory and Design-file conventions | first-slice candidate | These are downstream Design decisions |
| Governance, skills, schemas, validators, templates and documentation alignment | separate implementation slice | The new ownership and artifact contracts must become coherent across supported surfaces |
| Compatibility and disposition of existing records and model documentation | same-slice dependency | Current evidence cannot be silently reinterpreted or lost |
| Broader final-review removal and public command consolidation | separate proposal | Existing closeout/CLI-simplification direction must be reconciled, not silently bundled into this decision |

This proposal extends and challenges directions in [Remove Mandatory Final Code Review and Simplify the CLI](2026-09-04-remove-final-code-review-and-simplify-cli.md) and [Restore Reviewable Compact Corrections](2026-09-05-compact-correction-lifecycle-amendment.md). It proposes replacing their assumption that additional engine-owned lifecycle transitions are the solution to correction failures. It does not settle, supersede, migrate or close either initiative merely by being authored. Their review findings remain evidence of problems that the eventual replacement must address, not approvals to carry their proposed mechanisms forward.

Proposals, delivery plans, review records, evidence and mutable workflow status remain distinct concerns. One Design file per model does not mean one file for the entire repository, all project activity or all review evidence. General project management, hosted state, automatic publication, arbitrary unvalidated file writing, elimination of review and weakening of execution permissions are non-goals.

## Governing principle

Keep each decision with its responsible actor, each model's design in one place, and the tool responsible for recording faithfully and safely.

## Proposed direction

### Explicit decisions, dependable recording

Agents working under the workflow skills and human direction should explicitly choose and submit the intended workflow updates. The appropriate author, reviewer, route agent or Verify agent owns decisions about current stage, status, correction ownership, review applicability and readiness. The CLI records those decisions; it does not choose the next stage, automatically settle a review, move ownership, reopen work or derive a new lifecycle status from another edit.

The CLI should still validate the structure and internal references of submitted records, reject stale writes and unsafe paths, protect against unintended overwrites, and persist related explicit updates atomically with recovery. Computing storage identities or revision tokens is mechanical bookkeeping, not permission to infer workflow outcomes. Reads may expose recorded state and diagnostic observations without silently mutating it.

Validation must not recreate the removed workflow engine under another name. Checks of data shape, reference integrity and transaction safety remain distinct from deciding whether an agent ought to advance the workflow. Workflow obligations and semantic consistency are assessed by the responsible skills, independent review and Verify. A successful save means the explicit records were saved safely, not that their substantive judgment or the whole change was approved.

When an artifact changes, the responsible agent must explicitly record any required review invalidation, evidence update and correction ownership. The tool must not silently supply those decisions or conceal omitted work. Design must make the boundary between rejecting an internally inconsistent update and reporting a workflow concern understandable, without requiring an engine-defined transition sequence. Explicit recording is not permission for an author to fabricate an independent review or for a caller metadata field to authenticate its own authority.

### One authoritative Design file per model

Each model should have one living Design document containing its normative requirements and behavior together with the structure, ownership, decisions, trade-offs, failure and recovery boundaries, compatibility and acceptance criteria needed to understand that model. There should be no mandatory separate specification, architecture document or ADR for the same model. Diagrams can be embedded; supporting assets must not become competing owners of normative design.

A feature may affect one model or several. It updates the corresponding model documents instead of automatically creating another feature-specific Design file. Conversely, multiple features may evolve the same model. Model boundaries should follow coherent responsibility, not incidental file layout or the size of the latest change.

Cross-model relationships should use explicit references and identify which model owns each contract. A shared concern belongs with a clearly identified model or a deliberately defined shared model; it should not require duplicating the same decision across documents. Important decision rationale stays with the owning model. Historical ADRs and older documents remain evidence until an explicit consolidation and disposition process establishes their replacement.

Independent Design Review should assess the exact affected model documents and their relevant cross-model relationships as one change's design basis. Unified authoring does not allow self-approval. Stable requirement and boundary references must remain traceable into delivery work, implementation and evidence. Mutable lifecycle status stays in workflow records rather than becoming another field to synchronize inside model Design documents.

## Feasibility

Assessment: feasible, with material governance and compatibility work before adoption. RigorLoop already has repository-local records, stage skills, independent review responsibilities and a separation between pure evaluation and transactional persistence. The proposed direction changes which actor supplies lifecycle decisions; it does not require a hosted service, new authentication principal or a different source of truth outside the repository. Existing requirements, architecture explanations and decision rationale can be consolidated by model without discarding their engineering content.

The current Constitution requires separate architecture/specification authorship and review of that package, while the compact contract assigns state derivation and closed eligibility to the evaluator. Those rules conflict with the proposed direction and must be amended coherently rather than bypassed through an implementation shortcut. Supporting skills, validators, templates and integrations also depend on the existing shapes.

The earlier proposals and their correction difficulties supply the problem evidence; they do not prove this alternative implemented or verified. No project-map inference is needed for this direction decision. The main constraints are retaining independent judgment after removing transition enforcement, keeping explicit updates coherent, preserving model-document traceability, and providing a supported adoption path for existing work. Exact model boundaries, update semantics, compatibility contracts, migration rules and proof allocation belong to Design and Delivery. No known conceptual constraint requires either automatic CLI-owned transitions or multiple mandatory Design files for the same model.

## Impact and major trade-offs

Moving lifecycle decisions out of the CLI intentionally reduces automatic enforcement of workflow ordering. It can remove engine-induced correction deadlocks, but does not guarantee that agents will make correct or complete decisions. Clear ownership, explicit records, independent review and evidence checks become more important. The proposal does not disguise that responsibility transfer as a command rename.

One file per model reduces duplicate definitions but can increase shared-document contention or produce an oversized document if model boundaries are poor. Design must balance cohesive ownership against unnecessary model splitting. Fewer documents must not mean fewer requirements, missing decision rationale or weaker review coverage.

This direction requires changes to governing principles about artifact separation and CLI-derived state, while retaining the project's commitments to reviewability, traceability, safe persistence and verified outcomes. Existing records and historical approvals cannot automatically acquire new meaning. Supported adoption, rollback and the eventual disposition of the earlier correction-engine proposals must be explicit. Drafting or approving this proposal alone grants no authority to rewrite them.

## Decision requested

Approve the direction to:

1. make the CLI a mechanically validating, conflict-safe, recoverable recorder of explicit workflow updates rather than an automatic lifecycle-transition engine;
2. place stage, status, correction, applicability and readiness decisions with their responsible agents and human owners while retaining independent review and Verify;
3. use one authoritative Design file per coherent model, combining requirements, architecture and important decisions instead of requiring separate specification, architecture and ADR files for that model;
4. have features update the affected model designs, with explicit cross-model ownership and traceability;
5. preserve separate workflow records, proposals, delivery plans, reviews and evidence where their responsibilities remain distinct;
6. reconcile governing contracts, skills, validation and compatibility before adopting the new direction; and
7. replace further expansion of the correction-state engine as the proposed solution, while preserving the earlier proposals and findings until their explicit disposition.

Approval establishes this responsibility and documentation direction only. It does not approve exact commands, schemas, model names or file paths, skill restructuring, migration, historical supersession, removal of final Code Review, implementation, activation or release readiness.
