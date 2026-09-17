# Retire feature-format support and its exclusive maintenance

## Challenge

PR #199 established System-owned test rules and concrete Release, Skill and Authoring coverage. It deliberately preserved compatibility. The remaining problem is that RigorLoop still publishes feature-spec amendment and companion proof-map procedures and validates their formats even though the user has selected living Designs and no longer wants `specs/` support. Maintaining that accepted behavior also retains parsers, resource copies, fixtures and tests.

The preserved `codex/retire-obsolete-compatibility` workspace mixes this unfinished retirement with the now-merged testing work. This proposal extracts the feature-format withdrawal from that work onto merged baseline `5822e0e6`. It neither reuses the old proposal's approvals nor claims to finish every compatibility family.

## Goals

- End feature-spec and companion test-spec/proof-map authoring and structural validation as supported RigorLoop operations, including the previously retained customer format.
- Remove exclusive instructions, resource distribution, format dispatch, fixtures and tests together, while preserving useful current-model protection.
- Make the unsupported-operation boundary clear without modifying customer documents, rewriting historical evidence or weakening current record safety.
- Apply the merged test rules and affected model coverage to decide what proof survives; do not retain a test merely because it existed.

## Scope and non-goals

| Initial intent | Treatment | Destination |
| --- | --- | --- |
| Stop supporting `specs/` and its feature/proof workflow | in scope | This proposal and the affected Authoring, Validation, Workflow and CLI contracts. |
| Remove redundant or obsolete executable tests and fixtures boldly | in scope | Delete exclusive retired-format protection; preserve distinct current-model observations under System's rules. |
| Preserve test intent beyond the plan | in scope | Update affected model coverage with the behavior change, using the merged rules and catalogs. |
| Remove the five retired Skill archive mappings and obsolete examples-prefix handling | deferred follow-up | Original compatibility-retirement initiative; separate change-range support decision. |
| Adopt detailed test catalogs across all models | deferred follow-up | Model owners on substantive revision; PR #199 already delivered the selected Release/Skill/Authoring application. |

The compatibility assessment below is a bounded disposition for this change, not a permanent registry or authorization to remove every historical-looking branch.

| Behavior family and observed source | Classification and disposition | Scope budget treatment |
| --- | --- | --- |
| Feature amendments and companion proof-map methods in `skills/design`, `skills/design-review`, `skills/delivery-review`, shared boundary resources and their consumers | Currently supported requirement selected for retirement. Remove exclusive methods and reconcile all invocation/load paths and packaged inventories. | core to this proposal |
| Feature/proof validators and `specs/` selection in `scripts/lib/validation/boundary_first_validation.py`, document admission and `validation_selection.py` | Currently supported requirement selected for retirement. Remove accepted-format dispatch and exclusive structural rules; retain bounded unsupported-input handling and current model validation. | core to this proposal |
| `spec` artifact location in `packages/rigorloop/dist/lib/workflow-context.js` and matching skill defaults | Current compatibility surface selected for retirement with the workflow it advertises; preserve other factual discovery and location behavior. | same-slice dependency |
| Format-specific boundary structural/path/handoff tests and feature/proof fixtures | Exclusive retired-behavior proof: delete after separating any shared current-model, path containment, rejection or no-write observation. | same-slice dependency |
| Feature/ADR/architecture source interpretation and historical requirements | Supported source-reading responsibility: retain traceability and project authority; source input does not authorize retired output or automatic conversion. | same-slice dependency |
| Compact boundary scan, model validation, test catalogs, current records, installation and package integrity | Supported current requirements: retain meaningful independent observations and shared helpers used by them. | same-slice dependency |
| Five Skill archive deletion mappings, `docs/examples/` routing, flat-model and relocation aliases, old tooling-path routing | Existing change-range compatibility retained in this slice. Original retirement initiative owns later support-window decisions and consumer proof. | deferable follow-up |
| Rejection of retired record formats and commands; archived record classification | Supported safety and preservation requirements, not old-format operation. Retain. | out of scope |
| Synthetic package names, versions and historical-looking data | Representative fixture values, not compatibility promises. No removal based solely on their spelling or age. | out of scope |

No automatic migration, deletion or rewriting of customer documents; no removal of stored-record schemas or historical change directories; no withdrawal of other installation or release promises. No new test framework, mandatory case-per-function inventory, compatibility registry or case CLI. The preserved workspace and earlier judgments retain their original subjects. The five-path and examples-prefix retirement is intentionally deferred because supporting older Git ranges is a distinct decision from accepting feature documents.

## Governing principle

Support current outcomes explicitly, and remove retired behavior together with its exclusive maintenance while preserving current safety and evidence.

## Proposed direction

Make living Designs with model-owned coverage and Delivery allocation the supported engineering authoring path. Withdraw RigorLoop feature-spec amendment and companion proof-format operations in repository and customer use. Reconcile published guidance, review/delivery consumers, structural validation, factual artifact-location defaults and package resources as one coherent support change.

Existing documents remain readable source material. A request requiring retired output must receive a clear unsupported-operation explanation and leave project files unchanged. An authorized scoped adoption may transfer applicable requirements and decision meaning to a living Design; installation, a validator pass or this repository's policy alone supplies no customer adoption authority. Current generic record subject inspection remains available and is not a feature-format validator.

Remove format-exclusive parsing, vocabulary, dispatch, resource declarations and copied methods rather than retaining dormant alternate implementations. Do not remove shared parsing or boundary reasoning simply because its current filename mentions the older method. Reconcile changed assumptions in System, Skill/Authoring and Validation and in the existing Skill and Authoring catalogs. Preserve stable current requirement and scenario identities where their responsibility survives; disposition genuinely retired obligations explicitly.

Use System's test-maintenance rules to distinguish deleted support from consolidated current proof. Remove exclusive positive, negative and adoption-handoff cases for the retired formats. Retain a proportionate public-boundary observation of unsupported input, with useful diagnostics and preservation, plus current model/catalog, containment and resource-integrity protection. Design owns the precise accepted population and failure behavior; Delivery owns the exact deletion list, test allocation and recovery steps. No numerical deletion target or unchanged test count is promised.

## Feasibility

Assessment: feasible with existing owners and mechanisms; no new subsystem or dependency is needed. At merged baseline `5822e0e6`, `validate_feature_record`, `validate_proof_map` and `validate_changed_spec` expose the accepted format, while the same validation module also contains the surviving model checker. `test-boundary-first-validation.py` already groups feature structure, paths, adoption handoff, models, commands and catalog admission separately. This separation supports targeted deletion, but does not justify removing the whole module or aggregate.

The boundary-resource manifest declares compact-core, feature-authoring and proof as separate resources. The compact method survives; format-exclusive entries and copies can be reconciled through the existing generator and package checks. The CLI's factual `spec` location is another visible consumer, so guidance-only removal would be incomplete. Existing merged coverage and native test discovery provide a basis for testing the reduced contract without introducing another catalog platform.

No blocker to Design is known. The main constraints are shared helpers, transitive packaged methods, accepted-format assumptions in current contracts and preservation of current rejection/containment behavior. Each is an explicit Design/Delivery reconciliation obligation before removal. The inventory is evidence for this bounded withdrawal, not a claim that all repository compatibility has been exhaustively assessed.

## Impact and major trade-offs

This intentionally ends a previously supported customer workflow. Release communication must describe that support change and the living-Design alternative without implying automatic conversion; release publication and version selection remain separately owned. Previously released artifacts and recorded judgments keep their original meaning.

The reduction trades feature-format operation for a smaller supported surface. Source interpretation, project authority and meaningful current failure detection remain necessary. Recovery restores a coherent matching contract, guidance, resources and validator from the retained baseline; it must not reinterpret or rewrite customer files or historical evidence.

## Decision requested

Approve this bounded feature-format withdrawal for independent Proposal Review, then affected Design reconciliation/review and reviewed Delivery allocation. Treat PR #199's testing rules as the baseline, preserve the original retirement workspace, and defer historical path/window retirement and unrelated compatibility withdrawals to their owning initiative. This proposal does not itself approve implementation or claim completion of the broader retirement program.
