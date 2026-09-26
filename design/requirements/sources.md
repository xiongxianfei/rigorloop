# Sources for the initial requirement drafts

This register records the basis of ten draft IRs, their decomposition, and the connected system and architecture model. Earlier sections preserve successive drafting decisions, including the [seven-IR analysis](#src-complete-analysis) and [first architecture pilot](#src-architecture-pilot). The current extension is recorded under [SRC-PUBLISHED-PRODUCTS](#src-published-products).
Each JSON `sources` entry names a source below and locates the relevant passage or existing requirement.
The accompanying `basis` explains how that material informed the draft.

SRC-VISION, SRC-CONSTITUTION, SRC-SYSTEM, and SRC-DESIGN were read at commit `9b4fbc05b1c95e486bc0c24a35db6edf68e18a48`.
The links below navigate to working-tree files; the commit and repository-relative path identify the drafting basis.
These source references do not rename, replace, or migrate obligations from the existing approved contracts.

## SRC-REM

Source: the user's proposed **RigorLoop Engineering Method (REM)** supplied in the refactor discussion.
Its stated status is **Proposed normative methodology**.
The user authorized drafting requirements from this direction; that authorization does not mark the resulting records approved.

Section numbers in JSON source locators refer to that supplied proposal.
The selected extracts below preserve relevant source wording locally; they are not a copy of the complete method.

Section 3 separates requirements, durable assets, and Change history.
Sections 5 and 13 describe durable engineering knowledge and evolving Features and Functions.
Sections 8, 17, 28, 29, and 34 describe requirement parentage, converging allocations, and cross-domain relationships.
Sections 20–22 describe metamodel governance, validation, lifecycle, and authoring rules; Section 33 describes the iterative engineering cycle.

Sections 23–25 define controlled Changes, identifiable Baselines, and configuration management.
Sections 26–27 distinguish Verification, Evidence, and Judgment.
Sections 30–32, 35, and 42 supply the following relevant principles:

> REM requires one authoritative representation of each semantic fact.

> Current assets MUST remain understandable without replaying the entire history.

> Historical engineering records MUST preserve their original meaning.

> Every governed engineering entity MUST have a stable identity independent of its display name.

> Typed references MUST resolve to compatible types.

> Engineering claims require applicable evidence.

The proposal is tool-independent and does not prescribe Git, JSON, Rust, a filesystem layout, or a CI system.

## SRC-REM-REFINEMENT

Source: the user's subsequent instruction to establish `rem/` and clarify the method and principles used for authoring.

> For requirements, we need to use 5W2H method and IR's name should be clear.

The living method is now recorded in [rem/](../../rem/README.md).
[Requirement Analysis](../../rem/methods/requirement-analysis.md) applies this instruction through required 5W2H analysis and clear IR names.
[5W2H](../../rem/methods/5w2h.md) explains the questions, uncertainty handling, and distinction between analysis and record fields.

These are current working documents authored after the repository revision above.
The refinement strengthens the original proposal's preferred analysis technique for the current authoring work.
It does not rewrite the original SRC-REM wording or approve the resulting requirement drafts.

## Repository naming refinement

The user subsequently authorized applying the discussed naming design to REM knowledge and the requirement directories.
[Directory naming](README.md#directory-naming) records the selected repository convention.
The method distinguishes stable identity, readable names, physical location, and requirement parentage.

This refinement changed the locations of the draft IR and SR records and reconciled current navigation.
Their identities, titles, need statements, source entries, and analysis content were preserved.
It did not rewrite the original proposal, change requirement approval, or transfer obligations from the existing contracts.

## Inline analysis and schema refinement

The user subsequently clarified that 5W2H applies to IRs, SRs, and ARs, with exactly one IR parent per SR and one SR parent per AR.
The representation selected at that stage used `statement` for What and an inline `analysis` object for the remaining six answers.
It recorded unknowns explicitly and did not require a separate analysis document for each requirement.

The user authorized two self-contained schemas and explicitly rejected separate common and 5W2H schema files for these small record types.
The initial records retained their identities, titles, statements, source entries, acceptance criteria where present, and analysis meaning while consolidating that analysis into JSON.
This refinement did not alter the original SRC-REM extracts, approve the drafts, or migrate existing approved contracts.
The structured-analysis refinement below records the subsequent representation decision.

## SRC-REQUIREMENT-EXPANSION

Source: the user's instruction to create the additional needs proposed during the requirement-coverage discussion and then recount the open questions.
The proposal identified three additional IRs and suggested IR-003 as the likely parent of two related needs.
Drafting SR-006 and SR-007 beneath IR-003 interprets the instruction to create all proposed needs; their exact decomposition and placement remain draft engineering judgments.
The following locators preserve the proposal's scope and its treatment in the current drafts:

| Locator | Proposed need and treatment |
| --- | --- |
| IR-005: Keep engineering models valid and consistently interpreted | Explicit model rules and understandable validation results, separate from proof of requirement satisfaction |
| IR-006: Guide people and agents in authoring engineering models | Clear guidance for creating and refining engineering information without guessing required content or duplicating authoritative facts |
| IR-007: Improve engineering practice from recorded lessons | Turn failures and review findings into improvements that influence future work |
| IR-003 expansion: Resume interrupted work | Retain current work context, ownership, outstanding items, and next actions; elaborated as SR-006 |
| IR-003 expansion: Preserve human decision authority | Respect project decision boundaries during controlled change; elaborated as SR-007 |

The analysis and open questions are drafting interpretations grounded in the cited sources and this direction.
The authorization creates drafts for review; it does not establish completeness, approve implementation, or replace existing contracts.
IR-003 retains its identity, title, statement, and previous source entries; its supporting analysis now makes these two concerns explicit.

## Structured 5W2H refinement

The user subsequently selected explicit structured objects for all seven 5W2H questions, using `snake_case` field names.
The current profile adds `analysis.what` for problem and desired-outcome context while preserving `statement` as the authoritative need or obligation.
It identifies each record's `type` and distinguishes provisional `assumptions`, additional imposed `constraints`, and `open_questions` at the record root.
Open questions may concern any analysis dimension; they are no longer nested under How much.
Optional analysis fields capture relevant detail without requiring placeholders for inapplicable information.

The existing requirement identities, titles, statements, source entries, acceptance criteria, scope boundaries, and open questions are preserved in the revised representation.
[Record content and schemas](README.md#record-content-and-schemas) describes the current field rules.
The two schemas remain self-contained, the records remain drafts, and this refinement does not migrate existing approved contracts or introduce runtime validation.

## SRC-QUESTION-RESOLUTION

Source: the user's instruction to solve the recorded open questions and the resulting engineering decisions below.
The requirement ID headings are the source locators.

This section preserves the twenty question entries present when the user instructed: “Please solve the open questions.”
It records engineering decisions made under that delegated instruction, not a claim that the user individually supplied every answer.
The current answers live in the linked requirement JSON fields; this section preserves their original questions, decision locations, and rationale.

### Scope and authority

The answers select an initial RigorLoop authoring profile for the durable product requirements.
They apply to one governed project's selected model state and its controlled evolution, rather than only to the editing session that produced these drafts.
Profile expansion is a later controlled change; excluded capacity, latency, and storage-disaster guarantees are not pending promises within this profile.
The policy for model scope and capacity is owned by IR-001; IR-002 and SR-001 reference it.
Retention, recovery, and historical interpretation have distinct answers and must not be conflated with current retrieval.

Existing preservation, authority, and evidence principles come from the [Constitution](../../CONSTITUTION.md) and [Vision](../../VISION.md).
The selected profile boundaries, authoring scenarios, and assessment policies are new draft engineering decisions within that direction.
Requirements remain `draft`. Question resolution is not requirement approval, implementation, capacity certification, observed usability, recovery evidence, or satisfaction.
No performance measurements, recovery trials, authoring studies, or effectiveness observations are claimed by this section.
The schema and content checks for this change establish structural validity and preservation of the prior requirements, not those product outcomes.

### IR-001

Current answers: [IR-001 — Preserve engineering knowledge across sessions](IR-001-preserve-engineering-knowledge-across-sessions/ir.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| What retention duration is required? Resolve this before introducing obligations that depend on it. | `analysis.when.conditions`; IR-003 retention policy | Current engineering reliance determines retention, so an arbitrary expiry could remove still-needed information. Historical retention has a separate owner. |
| What model size must be supported? Resolve this before introducing obligations that depend on it. | `analysis.how_much.scale` | A single-model correctness boundary answers the initial authoring need without claiming unmeasured capacity. Completeness and resource failures remain observable. |
| What access-time targets are needed? Resolve this before introducing obligations that depend on them. | `analysis.how.approach` and `analysis.how_much.scope` | The selected profile commits to correct retrieval and explicit failure reporting, not an elapsed-time service level. No benchmark result is asserted. |

### IR-002

Current answers: [IR-002 — Trace engineering obligations and responsibilities](IR-002-trace-engineering-obligations-and-responsibilities/ir.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| What model size must be supported? | `analysis.how_much.scale`, referring to IR-001 | The same model participates in retrieval and traceability; separately chosen size targets would describe inconsistent supported populations. |
| What traversal limits are appropriate? | `analysis.how.approach` and `analysis.how_much.scope` | Declared traversal scope, cycle handling, and explicit incomplete results preserve useful traceability without promising unbounded execution. |
| What response-time targets are needed? | `analysis.how_much.scope` | Response-time guarantees are outside the selected profile; navigation still has assessable correctness and completeness outcomes. |

### IR-003

Current answers: [IR-003 — Control engineering changes and recover prior states](IR-003-control-engineering-changes-and-recover-prior-states/ir.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| What retention periods apply? | `analysis.when.conditions` and `analysis.how_much.scope` | Existing preservation rules retain current reliance and recoverable history. Lifecycle-based disposition is the selected policy, rather than age-based expiry. |
| What recovery-time objectives are required? | `analysis.how.approach` and `analysis.how_much.scope` | Recovery from an available retained baseline is a coherent supported scenario. A disaster-recovery service and elapsed-time commitment are separate capabilities excluded from this profile. |
| What data-loss bounds are acceptable? | `analysis.how_much.limits` and `assumptions` | A complete recovery must match the selected baseline exactly. This provides an assessable bound without pretending that a retained baseline contains later unsaved work or survives destruction of its storage. |

### IR-004

Current answers: [IR-004 — Assess engineering claims using applicable evidence](IR-004-assess-engineering-claims-using-applicable-evidence/ir.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| What evidence is sufficient for each claimed outcome under its acceptance conditions? | `analysis.how.approach` and `analysis.how_much.scope` | Sufficiency depends on covered acceptance criteria and applicability to the assessed subject. Counting tests alone cannot establish the claimed outcome. |

### IR-005

Current answers: [IR-005 — Keep engineering models valid and consistently interpreted](IR-005-keep-engineering-models-valid-and-consistently-interpreted/ir.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| Which model validity rules must be checked automatically, and which require engineering review? | `analysis.how.approach` | Mechanically decidable invariants and engineering adequacy need different assessment methods. Intended coverage is distinguished from the two schemas already implemented. |
| What compatibility and interpretation scope must be supported when the metamodel changes, including models authored under earlier rules? | `analysis.how_much.scope` | Binding each baseline to its own rules preserves interpretation without forcing the current authoring implementation to accept every earlier format. |

### IR-006

Current answers: [IR-006 — Guide people and agents in authoring engineering models](IR-006-guide-people-and-agents-in-authoring-engineering-models/ir.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| Which authoring activities and participant experience levels must the initial guidance support? | `analysis.who.affected_users`, `analysis.how_much.scope`, and `assumptions` | Explicit activity and audience boundaries allow guidance to be assessed. Staged format support does not silently become a promise that all entity schemas already exist. |
| What distinct guidance needs do people and engineering agents have for those activities? | `analysis.how.approach` | People and agents need common semantics, while explanatory navigation and deterministic processing need different presentation support. |
| What representative authoring tasks and observations should be used to assess whether the guidance is understandable and useful? | `analysis.how.approach` | Representative tasks and observable results make guidance assessable. Defining those tasks is distinct from observing successful use. |

### IR-007

Current answers: [IR-007 — Improve engineering practice from recorded lessons](IR-007-improve-engineering-practice-from-recorded-lessons/ir.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| Which classes of failures and review findings require a retained lesson rather than only a local correction? | `analysis.when.conditions` | Reusable or high-consequence mechanisms justify retained lessons; requiring one for every local correction would not establish broader learning. |
| What outcomes and observation period are sufficient to assess whether an adopted lesson improved subsequent work? | `analysis.how.approach` and `analysis.how_much.scope` | Comparable opportunities, specified outcomes, and recorded observations provide a relevant assessment window. No opportunity means unassessed effectiveness, not success or a newly missing policy decision. |

### SR-001

Current answers: [SR-001 — Retain engineering definitions across sessions](IR-001-preserve-engineering-knowledge-across-sessions/SR-001-retain-engineering-definitions-across-sessions/sr.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| What retention duration and supported model size follow from IR-001? The current obligation applies while saved information remains in the governed scope. | `analysis.when.conditions`, `analysis.how_much`, and added `acceptance_criteria`, referring to IR-001 and IR-003 | The child follows the parent scope and retention policy. Its additional criteria make retention and incomplete retrieval observable without authoring competing numerical limits. |

### SR-006

Current answers: [SR-006 — Resume changes from recorded work context](IR-003-control-engineering-changes-and-recover-prior-states/SR-006-resume-changes-from-recorded-work-context/sr.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| Which additional activity-specific context must be recorded beyond the common resumption set? | `analysis.how.approach`, `analysis.how_much.scope`, and added `acceptance_criteria` | Authoring, implementation, verification, and review have different resumption needs. Authoritative references prevent duplicate facts, and planned work remains distinct from observations. |

### SR-007

Current answers: [SR-007 — Preserve human authority over governed decisions](IR-003-control-engineering-changes-and-recover-prior-states/SR-007-preserve-human-authority-over-governed-decisions/sr.json).

| Original question | Resolution location | Rationale |
| --- | --- | --- |
| Which decision types must remain reserved for human decision, and what delegation scopes may project policy permit? | `analysis.how.approach`, `analysis.how_much.scope`, `constraints`, and added `acceptance_criteria` | Existing authority rules supply the decision boundary. Bounded standing delegation preserves continuity while scope changes or revocation invalidate only the affected authority. |

### Completion of this question set

Each of the twenty original entries has a concrete policy, scope, or assessment-method answer at the location above.
The entries can therefore leave the current `open_questions` lists without losing their basis.
Future discoveries remain valid reasons to add new questions or revise the profile; this decision does not establish that the requirement inventory or SR decomposition is complete.

## SRC-VISION

Source: [VISION.md](../../VISION.md), path `VISION.md` at the repository revision above.

The Pitch and Resumable across sessions and agents sections motivate durable knowledge beyond conversations.
The traceability and human-understanding principles motivate IR-002 and IR-004.
What it commits to distinguishes understandable current reliance from recoverable retired history.
Durable lessons supplies IR-007's learning intent; resumption and human decision authority inform SR-006 and SR-007.

## SRC-CONSTITUTION

Source: [CONSTITUTION.md](../../CONSTITUTION.md), path `CONSTITUTION.md` at the repository revision above.

Repository cleanup and historical retention supplies the existing preservation boundary relevant to IR-003.
Current obligations must retain an owner; retained historical meaning must remain recoverable.
These drafts do not amend that policy or introduce a new approval process.

## SRC-SYSTEM

Source: [System design](../../docs/design/system.md), path `docs/design/system.md` at the repository revision above.

SYS-SR-03 provides related intent for an inspectable engineering traceability chain.
SYS-SR-06 distinguishes current truth, work state, judgments, proof, and historical sources.
Those existing obligations have additional scope that remains with their current owner.

## SRC-DESIGN

Source: [Design authoring contract](../../docs/design/skill/authoring/design.md), path `docs/design/skill/authoring/design.md` at the repository revision above.

DES-SR-06 provides related intent for retained decision context, alternatives, consequences, and identity.
DES-SR-11 distinguishes stable references from changed assessment subjects.
DES-SR-21 provides related intent for retaining what current readers need without replaying history.
These are source contracts being read for context; no skill has been invoked and their full obligations have not been transferred.

## SRC-IR-001-SCENARIO-ANALYSIS

Source: the user's instruction to proceed with the first connected IR-001 example under the renewed [Scenario Analysis method](../../rem/methods/scenario-analysis.md), [Requirement Analysis method](../../rem/methods/requirement-analysis.md), and [System Design model](../../rem/models/system-design.md).
These refinements extend the original REM source above; they do not rewrite the original proposal or the earlier requirement-question resolutions.
The analysis starts from the existing [IR-001](IR-001-preserve-engineering-knowledge-across-sessions/ir.json) and its five draft SRs, preserving their identities and requirement parentage.

The authorized work proceeds through concrete situations, capability boundaries, reconciliation of existing SRs, and logical Function definitions, with minimal schemas and local structural checks supporting the records.
The scenarios and capability boundaries are analyst-derived drafts under that mandate, not quotations supplied individually by the user, observed research findings, or demonstrated product behavior.
No new SR identity was needed for this bounded example. The other IRs and SR-006 / SR-007 retain their previous content.

### Requirement refinement basis

| Locator | Analysis and refinement |
| --- | --- |
| IR-001 | Scenario Analysis makes the retained-knowledge need concrete and establishes the initial capabilities. Its existing need, retention policy, capacity boundary, and other domain boundaries remain applicable. |
| SR-001 | Make the parent's already selected retrieval-state and failure/completeness rules explicit in the statement and observable criteria, while preserving the earlier criteria. |
| SR-002 | Make no-match and ambiguous identity lookup observable; a name or location cannot substitute for unambiguous designation. |
| SR-003 | Preserve identity through the supported same-entity changes. Clarify that moving requirements between parents is a semantic derivation change, not merely a location edit. |
| SR-004 | Preserve direct current-state understanding and identify missing required current context separately from optional historical explanation. |
| SR-005 | Preserve recorded reasoning while making missing reasoning and unresolved applicability visible for the selected definition. Access does not certify the decision. |

### Scenario derivation basis

| Locator | Situation selected from the existing need |
| --- | --- |
| SCN-001 | A saved definition must survive the originating session and remain retrievable by another participant in an identifiable state. |
| SCN-002 | Ordinary evolution of an existing entity must preserve its identity without disguising an identity conflict or semantic parent change. |
| SCN-003 | Current understanding depends on access to both the definition and the decision reasoning still relied on after Changes. |
| SCN-004 | A reader needs accurate information about unavailable, unsupported, partial, or failed retrieval, with separate treatment of definition content and rationale. |

### System-design basis

| Locator | Capability or behavior decision |
| --- | --- |
| FEAT-001 | Originally named Engineering Knowledge Explorer, this capability groups inspection of retained definitions and applicable reasoning; it does not promise a particular UI, full-text search, or historical reconstruction. |
| FEAT-002 | Originally named Engineering Model Authoring, this capability groups the complementary save and revision behavior. This first scope is limited to IR-001 and does not claim the complete authoring-guidance capability needed by IR-006. |
| FUNC-001 | Retention is a logical behavior distinct from later retrieval, making the saved-content boundary explicit. |
| FUNC-002 | Identity checking must cover the declared model scope before a model-wide uniqueness conclusion. |
| FUNC-003 | Both capabilities need unambiguous identity resolution; they share this definition. |
| FUNC-004 | Definition retrieval reports content, selected state, and completeness without reconstructing current meaning from Changes. |
| FUNC-005 | Revision preserves an entity's identity while distinguishing its changing state and unsupported semantic changes. |
| FUNC-006 | Recorded reasoning and its applicable association require retention independently of presentation. |
| FUNC-007 | Presenting current context includes access to associated reasoning and must distinguish definition completeness from reasoning availability. |

The JSON records own current relationships and behavior; these tables preserve the drafting rationale rather than serving as a second relationship registry.
At that first System Design slice, every Function explicitly deferred Module allocation. Modules, Interfaces, ARs, runtime realization, and verification evidence were outside its scope.
At that drafting stage, an empty `open_questions` list recorded that no additional question remained for the bounded draft; it did not establish complete RigorLoop coverage, approval, or satisfaction.
The [current authoring profile](README.md#record-content-and-schemas) now omits the field when no question remains and permits exactly one consequential question when present.

## SRC-ASSET-CLARITY-REFINEMENT

Source: the user's direction that Feature and Function clarity is a REM principle, followed by selection of descriptive names and `<ID>-<full-title-in-kebab-case>.json` filenames.
The [clarity principle](../../rem/principles/README.md) and [System Design model](../../rem/models/system-design.md) own reusable semantics; the [asset naming convention](../support/README.md#entity-naming-and-filenames) owns their repository representation.

Locators `FEAT-001`, `FEAT-002`, and `FUNC-001` through `FUNC-007` identify the existing draft assets refined under this instruction.
Their names and descriptions identify the engineering subject and distinguish stakeholder capabilities from logical behavior.
The explanations distinguish identity resolution from content retrieval, changing a definition from retaining supplied content, and retaining recorded reasoning from presenting its applicable context.
IDs, typed relationships, scope boundaries, behavior, and lifecycle status are preserved; the two original Feature names above remain identifiable as the initial drafting context.
This refinement establishes no new requirement, Module allocation, implementation, approval, or verification evidence.

## SRC-SCENARIO-MODEL-REFINEMENT

Source: the user's refined [Scenario model](../../rem/models/scenarios.md) and [Scenario Analysis method](../../rem/methods/scenario-analysis.md), followed by the instruction to apply the refinement to IR-001.
Scenarios are now first-class governed Requirement Analysis entities with one owning IR, a stakeholder goal, black-box interactions and outcomes, and the lifecycle `draft → confirmed → obsolete`.
A confirmed Scenario has exactly one primary Feature. Scenario-to-SR references remain many-to-many without changing requirement parentage.

The existing Scenario records were reconciled against IR-001 and SR-001 through SR-005. The situations remain analyst-derived drafts, not observed research or executed product behavior.
The original source entries and record-level source references above preserve their drafting meaning; this entry records the subsequent refinement.

| Locator | Refinement basis |
| --- | --- |
| IR-001 | Preserve the existing need and 5W2H analysis. Its `confirms` references identify it as the single owner of all six Scenarios; ownership does not itself confirm their lifecycle state. |
| SCN-001 | Preserve the later-session retrieval goal and identity. Move the former author-save setup to externally meaningful preconditions; represent the independent authoring goal as SCN-005. |
| SCN-002 | Preserve the same-entity revision goal and identity, including identity conflicts and the boundary between physical relocation and semantic requirement reparenting. |
| SCN-003 | Preserve the reviewer-understanding goal and identity. Move prior rationale recording to preconditions; represent the independent recording goal as SCN-006. |
| SCN-004 | Preserve recognition of unavailable or incomplete knowledge. Honest diagnostic outcomes succeed at that goal; absent, incomplete, or misleading diagnostic reporting limits or fails it. |
| SCN-005 | Assign a new identity to the distinct author-save goal previously embedded in SCN-001. Existing retention and identity obligations already cover this situation. |
| SCN-006 | Assign a new identity to the distinct author-record-rationale goal previously embedded in SCN-003. The existing recorded-rationale obligation already covers this situation. |

The primary Features follow those goals: inspection or authoring. The Scenario JSON records own the actual Feature and SR links; this table records the reasoning for preserving or introducing their identities.
Review found the material obligations of these six situations represented in the existing five SRs, including explicit incomplete and failed outcomes, so no additional SR was derived for this refinement.
At that Scenario refinement, the seven Function and two Feature definitions, all existing SR definitions, and the other IRs retained their content. Architecture allocation remained deferred.
At that refinement, all six Scenarios remained `draft`; the representation change did not itself confirm their lifecycle state or establish complete IR analysis, requirement approval, implementation, or verification evidence.

## SRC-COMPLETE-ANALYSIS

Source: the user's instruction to finish all IR/SR/Feature/Function analysis, following the agreed connected analysis of Features, Scenarios, system obligations, and logical behavior under the refined REM.
The [Requirement Analysis completion criteria](../../rem/methods/requirement-analysis.md#reconcile-and-review) define this pass; the [Scenario Analysis method](../../rem/methods/scenario-analysis.md) supplies the stakeholder situations and outcome review.

The scope is the seven existing IRs and the initial authoring-profile decisions already recorded under [SRC-QUESTION-RESOLUTION](#src-question-resolution).
Locators under this source are the stable IDs of the authored or reconciled records. Their individual `basis` entries identify the parent need, existing obligation, or capability boundary that justifies the content.
The records are analyst-derived definitions, not quotations of independently supplied stakeholder research or observations of running product behavior.
Original source references and existing requirement identities remain intact. Current repository contracts under `docs/` keep their authority; this pass does not claim that all existing product obligations have been migrated.

### Derivation boundaries

| Need | Analysis boundary |
| --- | --- |
| IR-001 | Retain and understand current definitions, identity, and applicable recorded rationale; reuse its existing five SRs and seven Functions. |
| IR-002 | Author relationship facts once, navigate their declared scope, compare allocated responsibilities, and identify possible impact with traceable paths. |
| IR-003 | Identify, compare, recover, and evolve retained states; preserve historical meaning, resumption context, and applicable decision authority. Existing SR-006 and SR-007 keep their identities. |
| IR-004 | Distinguish verification definitions, observations, applicability, criterion coverage, contradictions, and bounded judgments, including after change. |
| IR-005 | Interpret the selected metamodel, diagnose rule violations, separate structural conformance from semantic adequacy, and prepare explicit profile migrations. |
| IR-006 | Select and apply canonical guidance for supported human and agent activities, and assess its usefulness against observable semantic task outcomes. |
| IR-007 | Select reusable lessons, expose their applicability during future work, prepare accountable improvements, and assess their observed effect at comparable opportunities. |

Retention, relationship interpretation, authority, and evidence assessment are shared through their existing owners rather than copied as new obligations under every consuming IR.
Sources, metamodel rules, and existing scope decisions support the selected boundaries; no universal performance target, automatic authorization, or numerical evidence threshold is invented.
Requirements and System Design assets retain `draft` status under their current schemas. Completion of this analysis is distinct from their approval, architecture allocation, implementation, or satisfaction.
Independent semantic reviews covered all seven IRs and their connected definitions. After correction and closure of the reported coverage, interpretation, and outcome-classification findings, the 35 Scenarios were accepted as `confirmed` current analysis knowledge under the Scenario lifecycle.
The first IR-001 definitions preserve their engineering meanings; FUNC-004 now explicitly uses the profile declared by the selected state, and SR-012 constrains that interpretation. SR-001 and SR-005 now reference the derived IR-003 recovery and provenance responsibilities in present tense.
The [requirements index](README.md) records the scoped review outcome and the direct checks actually performed for the authored model.

## SRC-ARCHITECTURE-PILOT

Source: the user's instruction to proceed with the proposed responsibility-based architecture method, a responsibility map across the 33 Functions, and an IR-001 architecture example with supporting schemas.
The [Architecture Design method](../../rem/methods/architecture-design.md) describes the reusable procedure; the [architecture index](../architecture/README.md) records its application, bounded walkthrough, review, and remaining scope.

The starting definition model is retained at repository revision `5cf0c7b6`: seven IRs, 32 SRs, 11 Features, 33 Functions, and 35 confirmed Scenarios.
This source records analyst-derived target architecture. It does not describe observed runtime Modules, transfer existing contract authority, or claim approval, implementation, or requirement satisfaction.
Locators are the stable IDs of the affected entities; each record explains its derivation or allocation basis.

The map proposes nine Module responsibilities across all existing Functions. Function definitions retain their identities, behavior, inputs, outputs, failure conditions, and prior provenance; their draft allocation replaces the previous explicit deferral.
The detailed pilot covers SR-001 through SR-005 using nine ARs, and the shared declared-profile interpretation responsibility using AR-010 beneath SR-012 in its original IR-005 tree.
Sharing this responsibility does not create a second parent SR or move SR-012 into IR-001.
The two Interfaces describe storage access and model interpretation/identity checking. Module-owned participation and Function/AR-owned allocations are authoritative; navigation tables derive their inverse views.

### Architecture choices and limits

- Group content custody and state-scoped access separately from preparing revisions, interpreting rules, and presenting engineering context. This prevents an authoring edit, a structural finding, and an explanatory view from becoming competing sources of current truth.
- Assign one accountable Module per Function and per AR in this draft profile. Collaborating responsibilities use explicit Interfaces; an SR may derive several independently allocated ARs.
- Supply raw state/profile material to interpretation so interpreted retrieval does not depend recursively on itself. Bind identity findings and writes to the same candidate and selected basis, and keep all related reads attributable to a consistent selected state.
- Preserve incomplete, unsupported, unavailable, ambiguous, stale, and failed outcomes where their meaning affects reliance. Neither structural interpretation nor successful retention confers approval or evidence applicability.
- Reuse full-title filenames and containment-based requirement parentage. AR analysis uses the existing seven-part 5W2H convention, with an optional single consequential question; Module and Interface content uses architecture-specific fields.

Interfaces and ARs for the remaining IRs are deferred in the Module definitions, including baseline establishment, change authority, assurance, guidance, and learning interactions.
The pilot assumes an identifiable selected state and an already applicable authority context. It defines how requests/results preserve those limits but does not implement the deferred authority or baseline services.
No storage technology, language, transport, deployment layout, performance target, or runtime adoption is selected.

## SRC-PUBLISHED-PRODUCTS

Source: the user's instruction to analyze the published CLI and skills coverage and proceed with the proposed reconciliation of requirements, system capabilities, and architectural responsibilities.
The [published-product coverage analysis](published-products.md) defines the inspected population, source-qualified obligation dispositions, remaining scope, and bounded review results.
It follows the current Requirement Analysis, Scenario Analysis, Functional Analysis, and Architecture Allocation methods in `rem/`.

The sources below are existing repository contracts at `5cf0c7b6`, inspected for their obligations and declared adoption boundaries. The task does not invoke a skill, inspect public registries, execute publication or installation, or assert the version currently available to customers.
New requirements, system assets, and architecture records are analyst-derived drafts. The 27 new Scenarios were confirmed after independent review and author reconciliation; that accepts analysis knowledge, not product behavior or requirement satisfaction. A correspondence to a source requirement preserves a traceable basis but does not migrate its complete contract, approve a replacement, or retire its current owner.
The original seven IRs cover engineering-model responsibilities; the extension adds distinct user needs for explicit command operations, portable guided engineering activities, and trustworthy compatible tooling distribution.
Existing authority, evidence, authoring, and learning responsibilities are reused where their meaning matches. Detailed source guarantees remain applicable until an explicit adoption reconciles them.
Two prior records receive bounded reconciliation: IR-006 reflects current schema availability, and SR-014 confirms the existing Functions governed by its constraint obligation under refined Functional Analysis. Their original need, obligation, acceptance criteria, and earlier source entries remain intact.

## SRC-PUBLISHED-CLI

Sources: [CLI](../../docs/design/cli/cli.md) and [Record Format](../../docs/design/cli/records.md) at `5cf0c7b6`.
Source-qualified locators identify the path and `CLI-SR-*` or `RF-SR-*` obligation; these namespaces retain their original identities.
The contracts govern the published command boundary and current operational records, including version dispatch, bounded observations, exact candidate construction, write safety, recovery, and diagnostics.
They do not imply that the current CLI reads or writes the new REM JSON records.

## SRC-PUBLISHED-SKILLS

Source: [Skill](../../docs/design/skill/skill.md) at `5cf0c7b6`, including its named specialist owners and applicability limits.
Source-qualified `SKL-SR-*` locators retain the identity of each common product obligation.
The analysis reads these contracts and inventories canonical capability paths; no `SKILL.md` instructions are invoked.
The common capability contract and current specialist Designs retain detailed behavior authority. New REM authoring proposals do not automatically extend the outputs supported by installed skills.

## SRC-PUBLISHED-PACKAGING

Source: [Packaging](../../docs/design/engineering/packaging.md) at `5cf0c7b6`.
Its source-qualified `DIST-SR-*` obligations cover canonical inventory, faithful transformations, generation isolation, compatible artifacts and integrity metadata, and the packed CLI boundary.
An authored package expectation is not evidence that generation or qualification ran.

## SRC-PUBLISHED-INSTALLATION

Source: [Installation](../../docs/design/cli/installation.md) at `5cf0c7b6`.
Its source-qualified `DIST-SR-*` obligations cover trusted acquisition, supported targets, destination scope, replacement authority, integrity, partial-failure behavior, and private diagnostics.
An installed package does not adopt a project's workflow state or grant engineering authority.

## SRC-PUBLISHED-RELEASE

Source: [Release](../../docs/design/engineering/release/release.md) at `5cf0c7b6`.
Its source-qualified `REL-SR-*` obligations cover compatibility/version decisions, exact candidate qualification, publication authority, external observations, recovery, and durable reporting.
Source-declared transitions and historical examples retain their original applicability. This design analysis neither executes a release nor changes publication permission.
