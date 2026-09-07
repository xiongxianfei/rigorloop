# Workflow Model Design

Model validation contract: explicit-recording-v1

## Drafting basis and authority

This is an initial, unapproved model Design draft under the user's explicit exception permitting `docs/design/workflow.md` and `docs/design/cli.md` before formal registration. The exception combines behavioral requirements, architecture and decision rationale in each model file; it does not activate a lifecycle contract, supersede existing documents or authorize implementation. No owning change record has been established for these drafts.

Direction: [Explicit Workflow Recording and Model-Centered Design](../proposals/2026-09-05-explicit-recording-and-model-centered-design.md). Related model: [CLI](cli.md). Current [Constitution](../../CONSTITUTION.md) and [workflow specification](../../specs/rigorloop-workflow.md) remain operative until an approved adoption changes them. The architectural and specification authoring methods are combined here rather than producing mandatory sidecars. This is not yet a complete replacement for all existing workflow contracts.

## Introduction and Goals

The Workflow model defines how responsible humans and agents turn a direction into reviewed design, delivery work and verified outcomes. It owns the meaning of recorded status, responsibilities, review applicability, correction and readiness. Its purpose is durable, inspectable reasoning and resumable work without making a command-line transition engine the decision owner.

The initial model inventory for this change has two members: Workflow and CLI. Workflow owns the engineering process and the model-document convention; CLI owns the safe storage interface. Neither is defined by a feature, class or AI model. Other system models can be identified later without forcing unrelated contracts into either file.

## Architecture Constraints

Current state must remain understandable without Git history, PR access, a network service or a previous chat. Reviewers must remain independent of the work they approve. Saving a decision does not prove it correct. Existing approvals and findings cannot acquire new meaning through a document rename.

This draft deliberately changes the proposed ownership of lifecycle decisions and design documentation. It does not remove final Code Review, change release permissions or authorize automatic progression. Those concerns retain their existing owners.

## Context and Scope

| Actor or model | Owns | Does not own |
| --- | --- | --- |
| Human decision owner | Product direction, scope exceptions, external/destructive authority | Implicit approval through silence |
| Authoring agent | Its model content and explicit correction impact declaration | Approval of its own content |
| Review agent | Judgment, findings, exact reviewed subjects and their settlement | Editing the content it approves |
| Route agent | Selecting work, coordination, recorded current activity and correction responsibility | Manufacturing review or Verify results |
| Implementation agent | Approved implementation and execution evidence | Changing the approved design through code |
| Verify agent | Final coherence assessment and success-only completion evidence | Approving its own correction |
| CLI model | Mechanically validated persistence and observations | Any of the decisions above |

The CLI interface is a dependency, not a superior workflow authority. Local filesystem permissions and runtime controls remain the execution boundary; an actor label in a record is attribution, not authentication.

## Solution Strategy

Use explicit decisions supported by evidence. Responsible actors read the current records and exact subject identities, decide their updates, and submit the related records together through the CLI. The workflow remains governed by skills and independent assessment, but storage accepts a structurally sound correction regardless of the currently recorded stage.

Avoid duplicated readiness fields where one explicit decision suffices. A stored decision and an observation about its supporting evidence are separate: a recorded approval may remain visible while a diagnostic reports that its subject has changed. Consumers must not mistake the visible historical judgment for current permission to proceed.

## Requirements

The following requirements describe the proposed model, not already-active rules. IDs are model-scoped and remain stable when later features revise this document.

| ID | Required behavior |
| --- | --- |
| WF-SR-01 | Responsible actors MUST explicitly decide stage, status, ownership, review applicability and readiness. Neither saving another record nor a read operation may supply those decisions automatically. |
| WF-SR-02 | A change record MUST identify its contract, proposal, affected model documents, current activity, responsible owner and unresolved blockers. Each referenced review or proof MUST identify its exact subjects. Mutable progress belongs in change records, not model Design documents or plan bodies. |
| WF-SR-03 | A formal reviewer MUST record a judgment against the exact reviewed subjects and its basis before approval is relied on. An author MUST NOT approve its own contribution. CLI persistence success or a caller-supplied reviewer label is not independent-review evidence. |
| WF-SR-04 | Before relying on changed work, its author MUST identify affected approvals and evidence, explicitly mark applicability changes, and record outstanding correction work. Route MUST assess cross-model impacts and select the next responsible owner without requiring that owner to appear in a previously derived pending set. Uncertain impact remains an explicit blocker. |
| WF-SR-05 | Any responsible stage, including Verify, MUST be able to record a newly discovered defect with stable finding identity, affected subjects, evidence, required outcome and correction owner. Failed Verify MUST NOT create a success report. Route records the correction destination; the finding does not need to originate in a prior review stage. |
| WF-SR-06 | A correction MUST retain unresolved findings and supporting judgments until their responsible reviewers record disposition. Returning work for rereview is not approval. Completed work may be explicitly reopened; a former completion or current stage MUST NOT prevent recording that decision. |
| WF-SR-07 | Each model MUST have one authoritative living Design file combining requirements, structure, decisions, boundaries, compatibility and acceptance. Features update affected models; cross-model contracts have one named owner and references from consumers. Mandatory separate specifications, architecture files and ADRs for the same model are removed only upon approved adoption. |
| WF-SR-08 | Requirement and decision references MUST survive normal document revisions. A changed or retired obligation retains its identity and rationale or an explicit replacement mapping. Design Review MUST assess the exact affected model revisions and relevant relationships; approval of one change does not approve another change's concurrent edits. |
| WF-SR-09 | A downstream actor MUST check the current decision basis before reliance. Missing, changed or contradictory required evidence blocks progression and is recorded explicitly; it does not prevent safely recording the blocker or correction. Only successful Verify may record lifecycle completion with exact evidence supporting the required design and delivery obligations. |
| WF-SR-10 | Historical contracts MUST remain explicitly identified and must not be silently reinterpreted. Adoption MUST preserve findings, decisions and proof provenance, identify replacement ownership and provide a supported recovery or rollback boundary. This draft performs no adoption. |

## Building Block View

Workflow has three conceptual parts, not three services or mandatory files: stage skills supply decisions; change-local records preserve those decisions and evidence; model Design documents supply the durable engineering contract. Delivery plans allocate model requirement IDs to work and proof. Independent reviews and Verify assess the resulting chain.

| Artifact responsibility | Proposed owner and placement |
| --- | --- |
| Model engineering truth | One `docs/design/<model>.md` per model |
| Change intent | Existing proposal surface |
| Mutable work state and explicit decisions | Change-local `change.yaml` |
| Current judgment and open findings | Stable change-local review record for the applicable target |
| New non-review-stage blocker, including Verify failure | Structured blocker entries in the change record, with evidence references; no fabricated review |
| Current proof and freshness subjects | Conditional change-local `evidence.yaml` |
| Resolved rationale that still constrains work | Conditional `material-decisions.md` |
| Stable delivery allocation | Existing plan surface |
| Successful final explanation | Success-only `verify-report.md` |

These placements preserve distinct responsibilities under the proposed `explicit-recording-v1` contract defined below; they do not claim compatibility with existing compact schemas. A blocker originating in Verify remains owned there for closure even when a subsequent review supplies supporting judgment. Review findings remain reviewer-owned.

### Explicit record schema

WF-SR-02/03/05/08 own this schema. Every object is closed: only listed fields are admitted, all fields are required unless marked optional, and duplicate keys or IDs are invalid. Empty arrays represent no entries; there are no inferred defaults. IDs use lowercase letters, digits and hyphens, start with a letter or digit, and contain 1–80 characters. Change IDs follow the same grammar. Paths are repository-relative and subject to CLI containment rules. A digest is `sha256:` followed by 64 lowercase hexadecimal digits.

Common types are `Subject = {path, identity}` and `Actor = {id, role}`. `identity` is a digest of exact file bytes; `role` is one of `human`, `proposal`, `design`, `plan`, `review`, `route`, `implement`, `verify`, `support`. A reference to a record entry is `{path, id}`; it identifies the entry, not a claim about freshness. Narrative fields are nonempty strings. IDs are unique within their containing array. Referenced subject files may have changed or disappeared; those are observations, unlike a dangling reference to an entry inside the candidate record set.

| Record | Exact structured fields |
| --- | --- |
| `change.yaml` | `schema_version: 1`, `contract: explicit-recording-v1`, `change_id`, `proposal: Subject`, `models: [{id, subject: Subject}]`, `activity: {stage, status, owner: Actor, reason}`, `plan: Subject or null`, `work: [{id, status, owner: Actor, requirement_refs: [string]}]`, `records: [{path, kind}]`, `applicability: [{path, value, actor: Actor, reason}]`, `blockers: [Blocker]` |
| `reviews/<review-id>.md` metadata | `schema_version: 1`, `change_id`, `id`, `target`, `reviewer: Actor`, `contributors: [Actor]`, `independence_basis`, `subjects: [Subject]`, `judgment`, `findings: [Blocker]` |
| `evidence.yaml` | `schema_version: 1`, `change_id`, `checks: [{id, actor: Actor, subjects: [Subject], result, procedure, summary}]` |
| `material-decisions.md` metadata | `schema_version: 1`, `change_id`, `decisions: [{id, actor: Actor, subjects: [Subject], rationale, source_refs: [EntryRef]}]` |
| `verify-report.md` metadata | `schema_version: 1`, `change_id`, `verifier: Actor`, `subjects: [Subject]`, `evidence_refs: [EntryRef]`, `review_refs: [EntryRef]`, `outcome: success` |

`Blocker` has exactly `{id, reporter: Actor, owner: Actor, subjects: [Subject], evidence, required_outcome, state, resolution}`. `state` is `open`, `resolved` or `deferred`; `resolution` is null for open work or `{actor: Actor, rationale, evidence_refs: [EntryRef]}` otherwise. The CLI checks this representation, not whether the resolution is justified. An empty evidence-reference array is valid for a reasoned disposition but does not prove the disposition adequate. Review-record blockers are findings; change-record blockers allow any stage to record a defect without inventing a review.

`stage` is `proposal`, `proposal-review`, `design`, `design-review`, `plan`, `delivery-review`, `implement`, `code-review`, `verify` or `support`. `status` is `pending`, `in-progress`, `blocked`, `ready`, `completed` or `cancelled`. These are labels, not a transition graph: any well-formed old/new label pair is recordable. `target` is `proposal`, `design`, `delivery` or `code`; `judgment` is `approved`, `changes-requested`, `blocked` or `inconclusive`. Evidence `result` is `passed`, `failed` or `inconclusive`. Applicability `value` is `current`, `stale` or `not-applicable`. Record `kind` is `review`, `evidence`, `decisions` or `verify`.

The `records` array declares every supporting authoritative record for this change; `change.yaml` is implicit. Each declared record must exist in the candidate set and have the matching kind and change identity. Each supporting record has exactly one explicit applicability entry in `change.yaml`. Extra physical files are not discovered as authority. A new supporting record and its registry/applicability entries are submitted together. These are referential checks, not review prerequisites.

The CLI model owns bytes and encoding. Markdown record bodies carry nonempty human-readable reasoning, while their structured metadata owns IDs and enumerated judgments. Body text cannot override metadata. Subject and evidence arrays may be empty while recording incomplete work; Workflow actors must not use incomplete records to justify approval or completion. A Verify report's metadata admits only success, but the CLI does not establish that its assertion is true.

### Responsibility-specific updates

The unified `design` responsibility combines architecture and specification authorship; it is not a new permission principal. Existing architecture/spec skills can supply portions during adoption, but one reconciled model document is the reviewed subject. Proposal, plan, implementation and Verify remain distinct responsibilities; review targets retain independent reviewers.

| Responsible actor | Allowed semantic edit under the workflow |
| --- | --- |
| Author | Its engineering content and recorded subject references; its work item; new blocker; marking affected applicability stale with rationale |
| Reviewer | Its review, finding dispositions and declaration of current review applicability after exact assessment |
| Route | Activity, work allocation, record registration, correction owner and justified applicability restrictions; never a fabricated judgment |
| Evidence producer | Its evidence checks and their applicability declaration |
| Verify | Its blockers/dispositions, final report and explicit completion decision after checking all obligations |

Whole-file replacement does not transfer ownership of neighboring fields. An actor preserves other actors' entries verbatim unless an authorized decision specifically changes them. Anyone responsible for affected work may conservatively mark evidence stale, but cannot restore another actor's approval merely because hashes match. Different actor decisions may be recorded in successive transactions; no single transaction requires every responsible agent to be simultaneously available. Semantic ownership is enforced by skills, review and runtime authority, not by trusting request labels.

For independence, the reviewer records the actual contributor identities and a concrete basis: a separately conducted review by an agent or human who did not author the reviewed contribution. Changing a role label or starting another turn of the same author is insufficient. The receiving actor inspects the review output and available execution provenance; if provenance cannot establish separation, it records a blocker or requests an independent human review. This contract introduces neither authentication tokens nor a new attestation service.

### Adoption and historical compatibility

WF-SR-10 selects new changes only for the first version. No in-place migration, contract-field rewrite or bulk document deletion is supported. Existing changes continue through their exact historical handlers; defects in those handlers remain separately owned. Neither earlier proposal is automatically closed or superseded.

Coherent adoption requires approved governing amendments, the matching model documents, recording schemas and CLI, stage guidance, validators, templates and supported adapter output to agree. The adopting delivery package must enumerate these surfaces and evidence of their agreement. A new root is created only by an explicitly requested `explicit-recording-v1` record operation after that adoption; there is no background conversion or silently changed default for historical roots. Drafting these files does not satisfy adoption.

Consolidation is incremental by model. Before a model document becomes authoritative for new work, its adoption decision must identify each displaced normative section, its replacement requirement/decision IDs and any deliberately retained external model contract. Earlier specs, architecture documents and ADRs remain readable under their historical contracts. New approvals cover the consolidated content; old approvals are not retargeted to it. Mixed historical/new references identify which contract owns each obligation, and conflicting authority blocks reliance until resolved.

Rollback before any new-contract writes restores the prior distribution and guidance without changing records. After new-contract records exist, reverting to an old writer is not a rollback strategy: retain a compatible reader, stop new writes and fix forward, or obtain a separately approved conversion. Persisted new records are never deleted to make an old client work. Copying obligations from an old change into a new one requires explicit owner disposition under the old contract and preserved source references; it is not offered as a way around unresolved findings.

### Replacement inventory for adoption

This inventory implements WF-SR-07/10 at the level of governing rules and affected surfaces. It is a proposed scope map, not a supersession receipt, migration script or implementation file count. `Replace for new contract` means the identified rule ceases to govern `explicit-recording-v1` only after coherent adoption; historical contracts retain it. `Amend shared guidance` means contract selection must be explicit rather than globally replacing old behavior. All unlisted unrelated behavior remains outside the proposed replacement.

| ID | Existing source and exact rule area | Treatment and destination | Preservation or adoption obligation |
| --- | --- | --- | --- |
| WF-MAP-01 | [Constitution](../../CONSTITUTION.md), Source of truth order, Architecture rules and Review rules: separate specification/architecture authority and authorship; Design Review's architecture/specification/ADR package | Amend shared guidance: WF-SR-07/08 and WF-DEC-02 establish one model document and one exact affected-model review basis. | Retain independent approval, traceability, source precedence, plan ownership and pre-implementation review. Do not demote governance itself into a model file. |
| WF-MAP-02 | [Workflow specification](../../specs/rigorloop-workflow.md), opening compact-current-state clauses and historical lifecycle chains: architecture then spec and compact semantic-operation progression | Replace for new contract: WF-SR-01/04/07/09 and Responsibility-specific updates. | Preserve old chains under their discriminators. Support skills, delivery review, code review and Verify remain obligations; this proposal does not remove final Code Review. |
| WF-MAP-03 | [Compact record contract](../../specs/compact-current-state-change-record.md), SR-02/03: artifact package and coordinator with derived permitted operations | Replace for new contract: WF-SR-02/07 and Explicit record schema. | Preserve distinct proposal, plan, review and proof surfaces. The new `activity`, `work`, registry and applicability entries are explicit actor decisions, not a renamed derived coordinator. |
| WF-MAP-04 | Compact record contract, SR-07–13 and SR-47: stable reviews, judgment/disposition vocabularies, material decisions and invalidation | Replace for new contract: WF-SR-03–06/08 and the review/blocker/decision schema. | Preserve finding identity, unresolved obligations and rationale. Do not translate old vocabulary or retarget reviewed hashes in place. New non-review blockers must not fabricate reviewer evidence. |
| WF-MAP-05 | Compact record contract, SR-14–18: proof freshness, success-only Verify and invalidating later edits | Split ownership: WF-SR-04/05/09 owns explicit applicability, downstream reliance and completion; CLI-SR-04/07 owns identity checks and observations. | Preserve failed evidence and prevent stale completion claims from authorizing work. Saving a contradictory assertion is possible under the new contract; treating it as valid is not. |
| WF-MAP-06 | Compact record contract, SR-32/34–36/48: responsibility, compatibility, coherent activation, rollback and exact-change bootstrap | Replace for new contract: WF-SR-01/03/10 and Adoption and historical compatibility. | Retain external execution authority and historical handlers. Do not generalize or reuse the compact implementing change's special bootstrap for these drafts. |
| WF-MAP-07 | [System architecture](../architecture/system/architecture.md), Crosscutting Concepts → Source of truth, Lowest sufficient architecture surface and Lifecycle status | Amend shared guidance: this model owns unified design truth and explicit workflow decisions for new work. | Keep unrelated system architecture, prior ADR rationale and historical ownership readable. No whole-file replacement of the system architecture is proposed. |
| WF-MAP-08 | [Architecture skill](../../skills/architecture/SKILL.md), [spec skill](../../skills/spec/SKILL.md), [Design Review skill](../../skills/design-review/SKILL.md): separate authoring output and exact package inputs | Amend shared guidance: unified `design` responsibility and review of affected model files under WF-SR-07/08. | Preserve engineering coverage and reviewer independence. Adapter invocation names need not be removed to combine the authored output; any public skill retirement needs an explicit compatibility decision. |
| WF-MAP-09 | [Route skill](../../skills/route/SKILL.md) and [Verify skill](../../skills/verify/SKILL.md): permitted-operation context, routing, correction and final completion | Amend shared guidance: WF-SR-01/04/05/06/09 supplies decision ownership; consume CLI storage observations without delegated eligibility judgment. | Keep author/reviewer write boundaries, isolated invocation limits and external permissions. No new automatic progression is introduced. |
| WF-MAP-10 | [AGENTS.md](../../AGENTS.md), Artifact lifecycle defaults, Planning and workflow, Required reading before implementation | Amend shared guidance to select model-file authority and explicit recording only for the new contract. | Preserve canonical source paths, user changes, historical continuation, small diffs and validation obligations. |

The CLI model owns the companion storage/schema/runtime inventory; these rows do not duplicate its normative interface. Prior [closeout simplification](../proposals/2026-09-04-remove-final-code-review-and-simplify-cli.md) and [correction lifecycle](../proposals/2026-09-05-compact-correction-lifecycle-amendment.md) initiatives, their design artifacts and findings are retained as separately owned work. This inventory neither establishes their current lifecycle state nor closes their obligations.

### Adoption support surfaces and completion check

| Surface | Required adoption action | Owner |
| --- | --- | --- |
| [Skill contract](../../specs/skill-contract.md), canonical skill references/assets and [skill validator](../../scripts/skill_validation.py) | Reconcile contract-sensitive artifact placement and claim boundaries; retain source ownership and published-skill quality requirements. Resource changes must be traced from the modified canonical skills, not installed copies. | Workflow Design, then Delivery allocation |
| [Boundary method](../../specs/references/boundary-first-method-v1.md), [feature authoring format](../../specs/references/boundary-first-feature-authoring-v1.md), [boundary validator](../../scripts/validate-boundary-first.py) | Implement the Model validation and proof mapping below for explicitly marked model files; preserve existing feature-format validation for historical documents. | Workflow owns the mapping; Delivery implements and proves recognition before adoption |
| [Adapter builder](../../scripts/build-adapters.py), [adapter validator](../../scripts/validate-adapters.py), [adapter support manifest](../../dist/adapters/manifest.yaml) | Regenerate and validate supported public outputs from canonical sources when the changed guidance is adopted. Do not hand-edit generated packages. | Delivery allocation |
| Model adoption decisions and affected plan/verification references | Enumerate displaced requirement IDs and retained outside-model references for each actual consolidated model revision; validate links and exact reviewed identities. | Model author and independent Design Review |

The inventory identifies the principal replacement sites, but is not evidence that every transitive skill resource or normative clause has been reconciled. Before adoption, each row must have an exact reviewed diff or an explicit unaffected/deferred disposition, with no required dependency left deferred. Delivery must expand affected source resources into a concrete file list; it must not treat a directory-level inventory row as proof of completion. Existing change records and review evidence are not bulk-edit targets. No governing surface named above is changed by this drafting step.

## Runtime View

### Normal work

Route selects an authorized activity and records it explicitly. The author updates the affected model document, identifies impact and submits its recording changes. An independent reviewer assesses the exact content and records the judgment and applicability decision. Route separately records the next activity only when its basis is adequate. One actor does not impersonate another to bundle their decisions into a single save.

### Revising previously reviewed content

An edit can temporarily leave the recorded review subject behind the actual file. The CLI reports the mismatch without changing the review. The author records the revised artifact identity, affected applicability and correction work; the retained review continues to identify the bytes actually reviewed. Route can choose the needed author directly, including a previously completed owner. Independent rereview supplies a new judgment before downstream reliance.

### A defect found at Verify

Verify records a blocker and failed evidence, not a success report. Route records a correction owner and activity even when the previous stage was terminal or no author was pending. The author fixes the owning model or implementation; affected reviewers independently reassess their subjects. Verify closes its blocker only after checking the correction and supporting evidence, then reruns the required final assessment.

### Concurrent edits or interrupted recording

An actor that loses a revision conflict rereads current records and reassesses its decisions; it must not replay an outdated approval against different content. Storage recovery is owned by the CLI model. Workflow consumers do not rely on a mixed or recovery-required snapshot and do not interpret mechanical recovery as a new decision.

## Deployment View

Workflow remains repository-local guidance and artifacts consumed by supported agent integrations. There is no new daemon, hosted coordinator or authenticated workflow service. Skill generation and public adapter packaging remain unchanged during drafting. Adoption later requires coherent guidance across the supported integrations; an old skill must not silently write the new contract.

## Crosscutting Concepts

### Model documentation and traceability

This file owns the one-file-per-model convention. `cli.md` consumes it rather than restating that contract. Model documents contain stable intent, including meaningful decisions and rejected alternatives. Change records identify affected model paths and exact content identities; requirement references combine model identity and stable local ID. A shared contract belongs to one existing model or a deliberately justified shared model, never duplicate normative prose.

Two features changing the same model use the same document. They must reconcile overlapping requirements before either treats a review as applicable to the combined content. Splitting or renaming a model requires an explicit responsibility and reference mapping, not just a size threshold.

### Model validation and proof mapping

WF-SR-07/08/09 own this mapping for `explicit-recording-v1`. A model file uses the existing `Requirements` table and `Boundary scan and acceptance scenarios` table; it does not need a separate feature spec, test spec or four-table boundary record. This is a model-specific replacement of that document format, not a claim of historical `boundary-first-v1` serialization conformance. The boundary reasoning and independent assessment obligations remain.

Model validation accepts an explicitly selected, repository-contained regular file at `docs/design/<model>.md`, where the filename stem follows the model ID grammar. Symlinked paths are rejected. Each file declares exactly once `Model validation contract: explicit-recording-v1`. Missing or unknown contract markers reject; they never fall back to feature validation. Historical `specs/` documents retain their feature-format and activation rules, with the semantic-review handoff clarified below. Validating a model draft does not activate it or require a registered change record.

The `Requirements` table has columns `ID` and `Required behavior`, with unique stable IDs and nonempty requirement text. Requirement IDs begin with a letter and contain only letters, digits and hyphens; existing WF-SR and CLI-SR IDs stay unchanged. The scenario table has exactly `Dimension`, `Requirement basis` and `Distinct outcome to demonstrate`. It contains each of the eight dimension labels shown below exactly once. An applicable row lists unique IDs declared in that model's Requirements table, separated by comma and space, plus a nonempty outcome. A non-applicable row uses `-` as its requirement basis and an outcome beginning `Not applicable:` followed by a reason. Unknown labels, duplicate or missing rows, malformed tables and undeclared requirement references reject. Each required table and its heading occurs once.

References use the model path plus its existing requirement ID, or the model path plus the exact dimension label for a scenario row; review and evidence subjects also retain exact file identities. Consumers link to the owning model rather than duplicate its rule. Material combined hazards remain concise requirement-linked prose alongside the scenario table; examples illustrate those requirements, never add behavior. No new boundary or proof ID series is required.

Delivery plans map every affected requirement, scenario row and material combined hazard to a verification group, concrete checks and expected evidence. Execution evidence records actual results and exact subjects. Validators check structure and reference resolution, not coverage adequacy, reviewer independence, approval or completion; independent Design and Delivery reviews assess those meanings. This is document tooling, not another responsibility for `record-store`.

For changed grandfathered specs without a boundary marker, structural validation MUST report a separate `review_required` observation naming each path and Design Review as owner. With no structural errors, the result is `review-required` with exit zero: structural checks passed, semantic approval is not established. Structural errors still produce failure and nonzero exit, including when review observations are also present. A missing or unknown marker on a non-grandfathered spec, or malformed existing boundary content, is never converted to a review observation.

Before downstream reliance, independent Design Review MUST classify each reported amendment against its exact reviewed subjects in the existing review record. A non-substantive historical amendment retains grandfathering; a substantive historical behavior change requires the existing feature-format adoption. A new-profile-only amendment is assessed against its owning model and must explicitly preserve the historical remainder. Missing, uncertain or stale classification blocks progression and Verify, even when structural CI passes. The validator neither infers nor authenticates this decision; no extra classification file, receipt or CLI state transition is introduced. This clarifies the handoff in PBF-R049b/PBF-R055a/PBF-R056 and replaces the retired `spec-review` owner with Design Review, without changing historical behavior or waiving semantic review.

### Boundary scan and acceptance scenarios

These rows are the Workflow model's boundary allocations under Model validation and proof mapping above. All eight dimensions apply. They define the review and verification scope, not a claim that validation or adoption has occurred.

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | WF-SR-02, WF-SR-05 | A blocker identifies an actionable owner and evidence; incomplete evidence cannot support readiness. |
| State/lifecycle | WF-SR-04, WF-SR-06 | Reopen completed work explicitly without a pending-owner or previous-stage prerequisite. |
| Identity/authority | WF-SR-03, WF-SR-08 | Reject reliance on self-approval or approval of another revision. |
| Composition/path | WF-SR-07, WF-SR-09 | A change spanning both models includes both exact revisions and their owned relationship. |
| Temporal/retry | WF-SR-08, WF-SR-09 | Concurrent model edits require fresh applicability assessment, not approval replay. |
| Failure/recovery | WF-SR-05, WF-SR-09 | A new Verify defect is durably recordable before correction, without a success report. |
| Compatibility/migration | WF-SR-10 | An old approval is preserved but not silently converted to a new-contract approval. |
| External/environment | WF-SR-02, WF-SR-09 | Another agent can resume from current local records without Git, PRs or chat. |

The material composed hazards are changed subject plus retained approval, completed owner plus new correction, and cross-model concurrent edits plus downstream reliance. WF-SR-03/04/06/08/09 own their outcomes; examples do not introduce new rules.

### Security, observability and usability

Decision provenance is inspectable, not cryptographically authenticated by actor text. Permissions remain with the surrounding runtime and human authority. Records should reference necessary evidence without copying credentials or raw sensitive output. Readers must see recorded decisions, unresolved blockers and observed drift separately. Text-based documents and CLI projections require no graphical UI or color interpretation. No numerical throughput target is introduced for human/agent judgment.

## Architecture Decisions

| ID | Decision and rationale | Alternative and consequence |
| --- | --- | --- |
| WF-DEC-01 | Skills and humans own workflow semantics; CLI records them. This removes stage eligibility as a prerequisite for recording repairs. | Extending the transition engine preserves automatic enforcement but recreates correction dependencies. Explicit decisions increase actor responsibility. |
| WF-DEC-02 | Consolidate normative design by coherent model, with embedded decision rationale. | Feature-specific spec/architecture/ADR packages multiply sources for the same model. Unified documents need disciplined ownership and concurrency handling. |
| WF-DEC-03 | Retain exact reviewed identities when subjects change; explicitly change applicability instead of rewriting what was reviewed. | Retargeting an old approval would misrepresent evidence. Preserved identities require readers to distinguish recorded judgment from usable approval. |
| WF-DEC-04 | Non-review-stage defects use change-local blockers, not synthetic review judgments or failure-shaped Verify reports. | A review-only finding surface makes Verify correction depend on another stage recording its discovery. |

No separate ADR is created under the user-authorized drafting exception. These decisions are proposed, not settled historical replacements.

## Quality Requirements

| Quality | Acceptance condition | Requirement coverage |
| --- | --- | --- |
| Correctability | Both a completed author and a newly failing Verify can record the necessary correction without engine-owned transitions. | WF-SR-01, WF-SR-04, WF-SR-05, WF-SR-06 |
| Trustworthiness | A save, self-approval or stale subject cannot be used as evidence of independent approval. | WF-SR-03, WF-SR-08, WF-SR-09 |
| Resumability | A fresh reader locates current work, owner, findings and exact evidence from repository records alone. | WF-SR-02, WF-SR-09 |
| Design coherence | Every affected requirement has one owning model and a trace into planned work and proof. | WF-SR-07, WF-SR-08 |
| Compatibility | Adoption accounts for every affected historical artifact without erasing unresolved obligations. | WF-SR-10 |

Delivery planning must allocate concrete proof to these requirements and composed hazards; this draft does not claim that proof exists.

## Risks and Technical Debt

Removing automatic ordering checks makes incomplete actor decisions easier to persist. Independent checks reduce that risk but do not guarantee correct agents. A single model file can become contentious or too broad; splitting must follow responsibility, not recreate one file per feature. Existing governance, schemas and validators still encode the older design and cannot validate this draft as an adopted replacement.

The model-validation mapping is now defined above for independent review; validator and guidance support are Delivery work, not implemented by this document. Exact adoption diffs and transitive resource coverage still require implementation and proof before activation. Any newly discovered requirement-level gap returns to Design. Adapter-specific independence evidence remains a Delivery obligation. No missing behavior is inherited implicitly from the current CLI.

## Glossary

Model: coherent system responsibility with owned concepts and rules. Judgment: an actor's substantive assessment. Applicability: whether that judgment may support current work. Observation: a mechanical fact about stored or actual data. Recording: safe persistence, not approval. Adoption: explicit establishment of a new governing contract and its compatibility boundary.

## Next artifacts

Refine these two model designs and their adoption contract before an explicitly authorized independent Design Review. Delivery planning follows approved Design, not this draft.

## Follow-on artifacts

None yet.
