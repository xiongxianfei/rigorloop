# Sources for the initial requirement drafts

This register records the basis of ten draft IRs, their decomposition, and the connected system and architecture model. Earlier sections preserve successive drafting decisions, including the [seven-IR analysis](#src-complete-analysis), [first architecture pilot](#src-architecture-pilot), and [published-product extension](#src-published-products). The current CLI allocation is recorded under [SRC-CLI-ALLOCATION](#src-cli-allocation).
The current Module containment and exposure refinement is recorded under [SRC-MODULE-HIERARCHY](#src-module-hierarchy).
Each JSON `sources` entry names a source below and locates the relevant passage or existing requirement.
The accompanying `basis` explains how that material informed the draft.

SRC-VISION, SRC-CONSTITUTION, SRC-SYSTEM, and SRC-DESIGN were read at commit `9b4fbc05b1c95e486bc0c24a35db6edf68e18a48`.
The links below navigate to working-tree files; the commit and repository-relative path identify the drafting basis.
These source references do not rename, replace, or migrate obligations from the existing approved contracts.

## SRC-MODULE-HIERARCHY

Source: the user's proposed four-parent Module decomposition and nested `modules/` representation, followed by authorization to apply the refined REM architecture rules. The living [Module hierarchy and encapsulation model](../../rem/models/architecture-boundaries.md#module-hierarchy-and-encapsulation) defines responsibility containment, single accountable allocation, and continuous provider-side Interface exposure.

The four draft parents compose the existing responsibilities: MOD-016 contains MOD-001–004; MOD-017 contains MOD-005–009; MOD-018 contains MOD-010–012; MOD-019 contains MOD-013–015. Their definitions explain broader integration responsibility and exclusions without taking ownership of child-held state or duplicating direct allocations. The distinction between MOD-008's semantic model-authoring guidance and MOD-012's published invocation procedures remains explicit.

IF-004 is exposed through MOD-018 to preserve its existing public user/agent command boundary, supported by its logical contract and attributed local-process realization. MOD-010 remains its provider. IF-006 is exposed through MOD-019 because its provider MOD-014 and consumer MOD-010 are in different parent trees. Consumer-side MOD-018 does not acquire an exposure declaration. Other declared collaborations remain internal to their respective parent trees; missing governance/specialist cooperation remains deferred.

Filesystem containment authors parentage once. The Interface `exposed_through` field authors visibility once; provider and consumer declarations remain on their actual Modules. The hierarchy migration record (historical operational reference; original assessment unavailable in the current tree) identifies the inspected scope and later check results. This refinement does not approve requirements, expand AR coverage, change stored operational formats, or establish product behavior.

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

Source: [System design](../architecture/composition.md), path `design/architecture/composition.md` at the repository revision above.

SYS-SR-03 provides related intent for an inspectable engineering traceability chain.
SYS-SR-06 distinguishes current truth, work state, judgments, proof, and historical sources.
Those existing obligations have additional scope that remains with their current owner.

## SRC-DESIGN

Source: [Design authoring contract](../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/design-authoring.md), path `design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/design-authoring.md` at the repository revision above.

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
The [clear-definition rule](../../rem/models/operational-support.md#clear-engineering-definitions) and [System Design model](../../rem/models/system-design.md) own reusable semantics; the [asset naming convention](../support/README.md#entity-naming-and-filenames) owns their repository representation.

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

## SRC-CLI-ALLOCATION

Source: the user's instruction to proceed with the next architecture pass after committing the reviewed published-product draft.
Repository revision `9055b3c0` retains that 247-entity starting subject and the refined REM methods used here.
The pass derives allocated obligations from IR-008's SR-040 through SR-047, walks through SCN-041 through SCN-049, and reconciles MOD-010/MOD-011 with IF-003/IF-004.
SR-040 through SR-047 retain the 44 criterion-level contribution arguments in their own attributed `sources` entries. Each entry identifies the unchanged parent criterion position, its allocated contributors, and the reasoning for their cooperation. These are allocation-analysis conclusions, not additional obligations, containment edges, or satisfaction evidence.
The [acceptance-contribution view](../architecture/views/browser/index.html#contributions) derives its rows from those entries; the [cooperation view](../architecture/views/browser/index.html#cooperation) summarizes the existing Module, Interface, and AR contracts. One-based criterion positions are navigation within the analyzed definitions, not stable identities; changes to the criteria require explicit reconciliation of their analysis.
The retained review record (historical operational reference; original assessment unavailable in the current tree) preserves earlier review subjects and actual validation results separately from the current model.

Each AR has one containment parent SR and one accountable Module. Requirements remain draft, and acceptance criteria describe intended observations rather than executed verification evidence.
The current CLI and Record Format contracts below continue to own exact public names, versions, stored shapes, bounds, and safety guarantees. This architectural derivation does not implement, adopt, weaken, or retire them, and does not expand supported operating-system or external-editor guarantees.
The source-qualified product inventory remains the earlier coverage baseline; current allocation results do not retarget its review subject.

## SRC-CLI-REALIZATION

Source: the user's instruction to proceed after rereading refined REM Architecture Design, which includes material physical/software realization beneath Modules and Interfaces.
The [architecture method](../../rem/methods/realization-design.md#design-the-physicalsoftware-realization) and [realization model](../../rem/models/architecture-realization.md#architecture-realization-views) govern this pass. The user's in-progress REM refinements are retained unchanged.
The [application profile](../support/README.md#subordinate-realization-views) defines the optional representation. Canonical owner-contained facets record the bounded mapping and its limits; the [runtime view](../architecture/views/browser/index.html#process) summarizes the selected physical arrangement.

MOD-010/MOD-011 and IF-003/IF-004 distinguish attributed source observations from draft choices and deferred qualification. No new requirement, logical allocation, Module, Interface, or public format is introduced.
Proposed choices retain the shared CLI runtime, filesystem record protocol, and existing command-family boundaries for the declared needs, with alternatives, consequences, and revisit conditions. Those choices are engineering analysis, not observations of conformance or approval of a release.
The original inline-realization pass performed author self-review and focused structural validation; its retained result does not extend the earlier independent logical review to the then-new realization information. Later review subjects retain their own scope in the supporting review record.

## SRC-CLI-SOURCE

Source: selected repository implementation files at commit `9055b3c037b2034dd2ad82c79370ee993e138e0d`, inspected for the CLI realization pass.
The observed views' repository-relative `software_units` and `bindings` paths locate the source artifacts; their `role` and source `locator` text identify relevant symbols. At inspection, the mapped files matched that commit byte-for-byte.

The inspected boundary includes [package metadata](../../packages/rigorloop/package.json), the [executable](../../packages/rigorloop/dist/bin/rigorloop.js), primary/advanced command adapters, discovery and diagnostics, the record engine (historical source `39be9c81583d1c2c9242e900e6e02e393c31e6d7:packages/rigorloop/dist/lib/record-store.js`), [filesystem operations](../../packages/rigorloop/dist/lib/record-store-files.js), candidate construction (historical source `39be9c81583d1c2c9242e900e6e02e393c31e6d7:packages/rigorloop/dist/lib/recording-construction.js`), and format/result/observation helpers named in the views.
The current [CLI](../architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md) and [Record Format](../architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md) remain behavior authorities. Where source and intended behavior differ, source inspection does not amend those obligations.

This is a bounded source inspection, not a complete dependency inventory, executed runtime test, installed-artifact observation, or public-registry observation. It establishes no minimum runtime version or expanded platform support. The package manifest omits an `engines` declaration; qualification must use the retained support contracts and actual candidate evidence.
The [recorded help discrepancy](published-products.md#observed-realization-discrepancy) remains unresolved implementation work.

## SRC-ARCHITECTURE-DIRECTORIES

Source: the user's proposed owner-directory architecture layout and instruction to refine it.
The [application profile](../support/README.md#subordinate-realization-views) records the selected representation: stable-ID/title directories, logical `module.json` or `interface.json`, optional owned realization facets, and derived aggregate views.
REM retains tool-independent ownership and materiality principles; this filesystem and JSON representation belongs to RigorLoop's draft authoring profile.

The retained directory-migration result (historical operational reference; original assessment unavailable in the current tree) records preservation of all 21 logical architecture identities, their definitions and typed relationships, and every observation, proposed choice, source attribution, and deferral from the four inline realization views.
Containment supplies facet ownership without new entity identities or duplicated owner references. The [views](../architecture/views/README.md) summarize authoritative definitions and facet content.
Current production formats, runtime behavior, requirement parentage, prior review subjects, and source revision attribution remain unchanged. Migration checks and review apply to the new representation; they do not establish runtime satisfaction or broaden an earlier approval.

## SRC-PARENT-INTERFACE-OWNERSHIP

Source: the user's clarification that parent contract ownership must be distinguished from child implementation responsibility, followed by the instruction to refine the model.
The ownership refinement record (historical operational reference; original assessment unavailable in the current tree) records the bounded contract review, migration, and checks.

MOD-018 Engineering operations now provides IF-004 as its public command contract; MOD-019 Product delivery provides IF-006 as its installation contract. MOD-010 and MOD-014 retain their existing behavioral responsibilities, state, and Function/AR allocations. MOD-011 retains record cooperation. Consumers, Interface operation guarantees, identities, and realization observations are preserved. No child consumption or duplicate provider is introduced to stand for implementation.

This decision supersedes the provider/exposure choice in SRC-MODULE-HIERARCHY for IF-004/IF-006. Earlier source entries and supporting records retain their original design meaning. `exposed_through` remains available for genuinely child-owned contracts crossing ancestor boundaries; directly parent-owned contracts do not expose themselves. Existing allocations and explicit Module explanations support this bounded contribution account, without asserting a general machine-readable Interface-to-child realization relationship. Source bindings and draft architecture do not establish runtime conformance or implementation adoption.

## SRC-BOUNDARY-CONTRACTS

Source: the user's authorization to analyze parent-boundary contracts from existing Scenarios, beginning with SCN-019 and applying the same method to guidance and release cooperation.
The bounded contract record (historical operational reference; original assessment unavailable in the current tree) identifies the scope, remaining gaps, review, and direct checks.

SCN-019/SR-020 motivates IF-007, provided by MOD-016 and consumed by MOD-005: state-consistent content and original interpretation inspection. Existing FUNC-004/FUNC-012 and IF-001/IF-002 contribute the content/interpretation behavior; FUNC-020 retains the complete Baseline responsibility. Inspection does not confirm retention, authorize establishment, or acquire separately owned material automatically.

SCN-053's adopted-REM authoring alternative and SR-032/033/053/056 motivate IF-008, provided by MOD-017 and consumed by MOD-012. MOD-008/FUNC-032/033 supply guidance selection and explanation; MOD-012/FUNC-053 retains specialist composition. Broader specialist procedures, authority decisions, usefulness assessment, and runtime integration retain their own scope.

SCN-066 with SR-007, SR-025–029, and SR-069/070 motivates separate IF-009 action-authority and IF-010 evidence-applicability contracts, provided by MOD-017 and consumed by MOD-015. MOD-006/FUNC-026 supplies authority assessment; MOD-007/FUNC-029/030 supplies evidence analysis with existing definition/observation/judgment context. MOD-015 retains release qualification, sealing, publication, and actual outcome responsibility. Authority and evidence cannot substitute for each other. Release-specific source clauses keep their original source-qualified meaning under SRC-PUBLISHED-RELEASE.

The current contract definitions and Module relationships refine earlier blanket collaboration deferrals. Existing Interface guarantees, requirement parentage, Scenario content, Function/AR allocations, and realization observations remain unchanged. Per-Scenario view selection is a bounded explanatory scope; it does not assert an execution sequence or complete end-to-end coverage. No new public executable API, storage technology, approval, or satisfaction claim is established.

## SRC-PUBLIC-ENTRIES

- Origin: the user's request to make public commands and skills discoverable in the Logical view and subsequent instruction to refine the canonical mappings and generated navigation.
- Analysis record: Public entry discovery (historical operational reference; original assessment unavailable in the current tree).
- Inspected source population: supported CLI command declarations and the retained CLI/Installation contracts; canonical `skills/*/SKILL.md` filenames and the retained Skill hierarchy. Skill contents are neither read nor invoked for this refinement.
- Observation scope: public entry existence and purpose in the inspected repository sources. This does not qualify an installed package, public registry release, or runtime outcome. Inspection on 2026-09-28 used source contracts and product sources unchanged from `1b96ed18f3be08c0d3701b5cce25954af5c1c913`; skill observation covers filenames only. Proposed REM correspondence uses the separately identified working design subject in the supporting record.
- Proposed correspondence: role-qualified references from public entries to existing REM Functions. Features and accountable Modules are derived from current relationships; detailed specialist obligations and unmapped scope remain explicit.
- Representation: IF-004's interaction facet owns the command catalog; MOD-012's software facet owns the skill catalog. The Logical view and published skill inventory derive from those sources. Earlier source observations and review subjects retain their original applicability.

## SRC-PUBLISHED-CLI

Sources: [CLI](../architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md) and [Record Format](../architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md) at `5cf0c7b6`.
Source-qualified locators identify the path and `CLI-SR-*` or `RF-SR-*` obligation; these namespaces retain their original identities.
The contracts govern the published command boundary and current operational records, including version dispatch, bounded observations, exact candidate construction, write safety, recovery, and diagnostics.
They do not imply that the current CLI reads or writes the new REM JSON records.

## SRC-PUBLISHED-SKILLS

Source: [Skill](../architecture/modules/MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/capability-contract.md) at `5cf0c7b6`, including its named specialist owners and applicability limits.
Source-qualified `SKL-SR-*` locators retain the identity of each common product obligation.
The analysis reads these contracts and inventories canonical capability paths; no `SKILL.md` instructions are invoked.
The common capability contract and current specialist Designs retain detailed behavior authority. New REM authoring proposals do not automatically extend the outputs supported by installed skills.

## SRC-PUBLISHED-PACKAGING

Source: [Packaging](../architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md) at `5cf0c7b6`.
Its source-qualified `DIST-SR-*` obligations cover canonical inventory, faithful transformations, generation isolation, compatible artifacts and integrity metadata, and the packed CLI boundary.
An authored package expectation is not evidence that generation or qualification ran.

## SRC-PUBLISHED-INSTALLATION

Source: [Installation](../architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/installation.md) at `5cf0c7b6`.
Its source-qualified `DIST-SR-*` obligations cover trusted acquisition, supported targets, destination scope, replacement authority, integrity, partial-failure behavior, and private diagnostics.
An installed package does not adopt a project's workflow state or grant engineering authority.

## SRC-PUBLISHED-RELEASE

Source: [Release](../architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/release.md) at `5cf0c7b6`.
Its source-qualified `REL-SR-*` obligations cover compatibility/version decisions, exact candidate qualification, publication authority, external observations, recovery, and durable reporting.
Source-declared transitions and historical examples retain their original applicability. This design analysis neither executes a release nor changes publication permission.

## SRC-PRODUCT-REALIZATION

Source: the user's authorization to establish a coherent initial five-view set, including skill/CLI production and installation. Static inspection on 2026-09-28 used the following tracked sources, unchanged from `33f56fe84ff730d7bd48900cef32170fd0682412`:

- [Adapter build entrypoint](../../scripts/build-adapters.py) and [shared adapter production](../../scripts/lib/packaging/adapter_distribution.py): explicit-output archive production, supported descriptors, selected transformations/resources, archive layouts, and hashes.
- [Candidate composition](../../scripts/lib/release/release_candidate.py): isolated prepared checkout, archive validation before metadata composition, package metadata overlay, and `npm pack` invocation. Release retains candidate qualification, sealing, and publication responsibilities in this shared source file.
- [Package manifest](../../packages/rigorloop/package.json): package allowlist, existing JavaScript runtime, executable mapping, and dependencies. There is no command-code compilation or generation script in this manifest.
- [CLI installation helpers](../../packages/rigorloop/dist/bin/rigorloop.js), [target descriptors](../../packages/rigorloop/dist/lib/adapters.js), [destination installation](../../packages/rigorloop/dist/lib/installer-replacement.js), and [official URL checks](../../packages/rigorloop/dist/lib/official-archive-url.js): selected invocation, trusted acquisition, in-process execution, exact destination units, and retained-original placement.

MOD-013 owns the subordinate production mappings; MOD-014 owns installation software, runtime, and deployment observations; IF-006 records its process binding. The source-to-output paths in MOD-013's software facet describe inspected production code. Output paths are candidate-relative templates, not observed files. Canonical skill directory and template names come from generator declarations and filesystem inventory; no `SKILL.md` content was read or invoked.

[Packaging](../architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md), [Installation](../architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/installation.md), and [Release](../architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/release.md) retain behavioral authority. Source observations do not adopt REM generation, transfer Interface ownership, or change Function/AR allocations. Earlier provenance entries retain their original meaning and scope.

One bounded source/contract discrepancy remains explicit: Packaging DIST-SR-22 requires rejection when neither `--check` nor `--output-dir` is selected, while the inspected `build-adapters.py` still defaults to `sync_adapter_output`. The mapped production route uses explicit isolated output; this task does not change or execute the discrepant path. The installer also visibly relies on descriptor-relative `/proc/self/fd` operations and same-filesystem placement; static inspection supplies no broader platform qualification.

No archive or npm package was built, validated, installed, or published in this pass. Archive contents, reproducibility, instruction semantics, runtime compatibility, destination safety, and release readiness need applicable executable and independent evidence; none follows from an authored architecture facet.

## SRC-RECORD-PROCESS

Source: the user's authorized Process-view refinement for record publication and recovery. Static inspection on 2026-09-28 used the following tracked source and contract files, each verified unchanged from `33f56fe84ff730d7bd48900cef32170fd0682412`:

- Record store (historical source `39be9c81583d1c2c9242e900e6e02e393c31e6d7:packages/rigorloop/dist/lib/record-store.js`): `snapshot`, `candidate`, `acquire`, `loadJournal`, `known`, `publish`, `prepareResult`, `record`, `recover`, `executeRecordStore`, and `executeTargetedStore` establish the observed successful order, terminal preview/no-change alternatives, exact recovery selection, and reader/writer coordination.
- [Filesystem boundary](../../packages/rigorloop/dist/lib/record-store-files.js): guarded byte access, identity checks, exclusive lock creation, replacement, and directory cleanup supply the inspected storage mechanisms; their presence is not durability or platform proof.
- Primary receipt preparation (historical source `39be9c81583d1c2c9242e900e6e02e393c31e6d7:packages/rigorloop/dist/lib/recording-result.js`), targeted mutation adapter (historical source `39be9c81583d1c2c9242e900e6e02e393c31e6d7:packages/rigorloop/dist/lib/recording-mutation-cli.js`), and advanced command adapter (historical source `39be9c81583d1c2c9242e900e6e02e393c31e6d7:packages/rigorloop/dist/lib/record-store-cli.js`) establish callback ownership, bounded preparation before publication, explicit selectors, and result/error mapping.
- [CLI](../architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md#command-interface) and [Records](../architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md#requirements) retain behavior authority, including storage-only claims, preview/no-op distinctions, receipt preparation, current v3 preservation, observed-check concurrency limits, and exact before/candidate recovery.

IF-003's interaction facet records publication and recovery sequences. MOD-011's runtime facet records the private journal lifecycle and its coordination constraints. Their ordered steps and guarded transitions come from the inspected implementation and retained contracts, not from SCN-046/SCN-047 participation or inferred workflow order. Main publication describes targeted changed writes and identifies advanced-path differences. Recovery main steps describe `complete`; the verified `restore` branch is terminal.

Only `prepared` and `committed` are stored journal phases. Journal absence alone does not establish reader availability or cleanup success. Preview performs no private transaction writes; actual execution can change private lock/epoch data before a later rejection or unchanged result. Unknown target bytes, untrusted recovery evidence, interrupted cleanup, and lost responses remain qualified outcomes rather than inferred success or rollback.

No product command, save, recovery, fault injection, or platform verification was executed. Logical records, allocations, Interface ownership, Scenario definitions, and earlier source entries retain their original meaning. These source observations do not establish requirement satisfaction, universal crash safety, exclusion of external editors between observed checks, or permission to perform the documented operations.

## SRC-PHYSICAL-REALIZATION

Source: the user's authorized Physical-view refinement for consumer deployment, storage boundaries, and producer placement. Static inspection on 2026-09-28 used the following tracked files, each verified byte-for-byte unchanged from `33f56fe84ff730d7bd48900cef32170fd0682412`:

- [Package manifest](../../packages/rigorloop/package.json) and [CLI entrypoint](../../packages/rigorloop/dist/bin/rigorloop.js): executable/package mapping, package-relative trusted metadata, `archiveWorkForInit`, initial source selection, in-memory acquisition, and the executable wrapper's conditional diagnostic admission.
- Record store (historical source `39be9c81583d1c2c9242e900e6e02e393c31e6d7:packages/rigorloop/dist/lib/record-store.js`) and [filesystem boundary](../../packages/rigorloop/dist/lib/record-store-files.js): explicitly selected project/change scope, authoritative registered paths, and private lock/epoch/journal addressing. Existing Process observations retain publication and recovery behavior.
- [Installation replacement](../../packages/rigorloop/dist/lib/installer-replacement.js) and [official archive URL validation](../../packages/rigorloop/dist/lib/official-archive-url.js): working-directory-relative selected destinations, private retention outside discovery roots, same-device checks before detachment, and the declared official initial HTTPS address. The alternative explicit local ZIP still depends on trusted bundled metadata.
- [Diagnostic configuration](../../packages/rigorloop/dist/lib/log-config.js) and [diagnostic sink](../../packages/rigorloop/dist/lib/log-sink.js): independent user-state defaults or explicit absolute directory, retained file names, rotation, guarded append, and explicit lookup. An override is not assumed to remain outside the selected project.
- [Candidate preparation](../../scripts/lib/release/release_candidate.py) and [adapter distribution](../../scripts/lib/packaging/adapter_distribution.py): reviewed source commit, temporary prepared checkout, selected candidate output, and explicit generation containment checks. Source, workspace, and output are production roles, not inferred hosts or deployment transfers.
- [CLI](../architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md), [Installation](../architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/installation.md), and [Packaging](../architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md) retain behavioral authority and qualify the inspected implementation observations.

MOD-010 owns the one consumer package/execution binding, its per-participant storage accesses, and diagnostic placement. MOD-011 owns the separation of authoritative records and private coordination. MOD-013 owns source/workspace/output placement. MOD-014 owns the conditional installation/retention constraints. IF-006 owns the qualified official/local acquisition alternatives, while MOD-019 remains its logical provider and MOD-014 its installer participant. Existing placements and the single CLI process are referenced by exact owner and local name; no duplicate allocation, process, or shared-host assertion is introduced.

The record root, installation working directory, and diagnostic root remain independent selectors. A local acquisition source is not automatically linked to this repository's candidate outputs. No consumer host, running process, remote release, package installation, network path, archive bytes, or storage safety was observed by executing the product. No `SKILL.md` contents were read or invoked. These source facts neither qualify platform compatibility nor establish requirement satisfaction, deployment availability, agent-host execution, or successful delivery. All earlier provenance entries and source/contract discrepancies retain their original scope.

## SRC-LOCAL-OPERATIONAL-RECORDS

Source: the user's request to separate the current engineering definition from local operational history, the [local operational record-store proposal](../../docs/proposals/2026-09-29-local-operational-record-store.md), and the subsequent instruction to treat the proposal as RR input and proceed with IR analysis.

The proposal organizes the incoming request; it is not itself a REM IR or approval of one. Analysis selects refinement of IR-003 and IR-008, with reuse of IR-001, IR-002 and IR-004. No distinct new stakeholder need justifies another IR. SQLite remains a proposed physical realization, not the IR statement or a new logical Module.

IR-003 extends the previous available-intact-Baseline recovery scope to creating and restoring operational backups, including retained evidence and project association. It preserves the meaning of earlier Baseline obligations. Restoration still requires a usable retained copy and makes no promise to recover destroyed copies, post-backup work or unsaved content. IR-008 extends command analysis to that operational scope and multiple local agents while preserving explicit actor decisions and retained product-contract authority.

This source qualifies the earlier SRC-QUESTION-RESOLUTION and SRC-COMPLETE-ANALYSIS conclusions for these two IRs: their original analyzed subjects and narrower scope remain historical evidence. Current IR refinement does not retroactively extend their coverage or assessments. Existing Scenario confirmations, SRs, ARs, Functions and architecture facets retain their existing scope; none is evidence that the new backup or storage direction is already analyzed, implemented or verified.

Downstream reconciliation is required: IR-003 owns backup/restore/transfer Scenarios and any new system obligations alongside SR-006 and SR-020–024; IR-008 owns command-facing Scenarios and reconciliation of SR-040–047 and their allocations. IR-001's SR-004/005 continues to own model understanding and applicable rationale, and IR-004 owns assessment applicability. Requirement Analysis must select or add Scenarios and derive assessable SRs before Functional Analysis and Architecture Allocation change their respective records. Detailed persistence and migration behavior remains governed by the retained CLI/Records contracts until explicitly reconciled. The need-level extension is draft and does not activate storage migration or retire `docs/changes/`.

## SRC-CLI-ALLOCATION-BEFORE-LOCAL-STORE

Source: the original SRC-CLI-ALLOCATION contribution arguments for SR-042 through SR-045, recoverable with their original criterion text and AR subjects at commit `c166632db33574996ea94acedd2ed4ec364d89fd` in their same `design/requirements/IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/` paths. This source identifier qualifies those arguments as historical basis after the local-store requirement refinement; their locator and argument text are preserved unchanged. They are no longer current acceptance-coverage claims for changed criteria. The existing ARs and Interfaces remain draft descriptions of the retained v3 contract and need Architecture Allocation reconciliation before implementing the new SRs.

## SRC-LOCAL-OPERATIONAL-ANALYSIS

Source: the user's instruction to proceed with Scenario and SR refinement from the [RR proposal](../../docs/proposals/2026-09-29-local-operational-record-store.md) and the preceding IR-003/IR-008 refinement under SRC-LOCAL-OPERATIONAL-RECORDS. REM Scenario Analysis, Requirement Analysis and Functional Analysis govern this pass; the proposal is input, not an IR or an approval artifact for these records.

The analysis adds SCN-070–074 and SR-074–078. IR-003 owns coherent backup creation (SR-074), faithful restoration (SR-075), safe transfer (SR-076), and preservation during migration (SR-077); IR-008 owns selected cross-Change history inspection (SR-078). Existing SR-004/005 and SR-027/028 retain current-model rationale and assurance responsibility. SR-020–022 and SCN-019–021 retain engineering Baseline scope; operational backup is not another name for Baseline recovery.

FEAT-021 supplies a distinct preservation/restoration capability. FEAT-007 is reused for controlled migration and FEAT-012 for history inspection. FUNC-074 creates backups; FUNC-075 serves both restoration and transfer, avoiding one Function per SR. FUNC-076 handles supported migration and FUNC-077 history selection. These four new Functions are deliberately unallocated; no Module, Interface or AR is invented in this system-analysis pass. Existing recording Functions are reconciled with the revised draft SRs, while observed v3 runtime and physical facets retain their original scope and do not establish replacement-store realization.

SCN-022/023/025/041/042 retain identity but their revised definitions are draft pending reassessment. Their previous confirmed subjects and sources remain recoverable in Git history and are not approval of the new scope. SCN-046 remains the coherent-publication situation; SCN-047 remains the explicit interrupted-update recovery situation. Their unchanged confirmations cover those existing situations only. SR-045 now distinguishes deterministic recovery of an already determined storage outcome from an actor-selected completion/restoration decision. It does not imply that the existing v3 command automatically recovers, or that SQLite activation has been approved. Storage-engine realization and failure details belong to the next architectural reconciliation.

All new Scenarios, SRs, the Feature and Functions are draft. Shared command requirements are referenced by IR-003 Scenarios without changing their single IR parent. No scenario confirmation, requirement approval, runtime migration or evidence applicability is inferred from structural validation. The earlier pending Scenario/SR work recorded under SRC-LOCAL-OPERATIONAL-RECORDS is addressed by this draft package; independent semantic review and architectural reconciliation remain outstanding.

## SRC-REQUIREMENT-FIRST-WORKFLOW

Source: the user's requirement-first workflow specification, subsequent instruction to refactor the whole system before detailed work, explicit selection of one mandatory whole-change Code Review gate with optional interim advice, and authorization to author the system-wide requirement package. The [workflow refactor analysis](workflow-refactor.md) records request interpretation, existing-IR disposition, affected subjects and the coordinated replacement map.

IR-009 remains the owning need; no new IR is required. The draft adds SR-079–083 and SCN-075–082, refines specialist guidance/coordination/recording criteria in SR-053–055 and shared assessment criteria in SR-027–029, and clarifies FEAT-016/017 scope. IR-003 and IR-008 retain authority, provenance and supported recording ownership. The explicit one-gate selection supersedes the earlier pasted milestone-review clause for this proposed requirement basis.

New SRs constrain existing capabilities without claiming completed Function or AR design. New Scenarios remain draft. Existing Functions, ARs, realization facets and historical confirmations retain their previous scope; they do not establish coverage or implementation of the new workflow. Requirement Review, downstream design and coordinated product adoption remain outstanding. Current skill and CLI contracts are not changed or activated by this analysis, and the separate SQLite direction is not a prerequisite assumed implemented.

## SRC-WORKFLOW-REQUIREMENT-REVIEW

Source: the user's authorization for document-based Requirement Review under the [Constitution exception](../../CONSTITUTION.md#workflow-and-review). The recorded assessment was performed by the same author, not an independent reviewer. It established the scoped requirement-analysis basis and confirmed SCN-075–082; this does not establish Function/AR completeness, implementation, workflow activation or SQLite migration.

Applicable outcomes are incorporated in the current model: Requirement Review permits unfinished Function/AR design, SCN-081 permits assessment of a claimed but absent/inapplicable approval, and SR-083 limits active-work disposition to the selected adoption scope. Their owning definitions and the REM method explain those rules without needing the review dossier. Prior source conclusions retain their original scope.

The exact assessment, findings, subject identities and executed-check results are local operational records, not part of the Requirements model. Preserved assessment content identity: SHA-256 `36b30a7d8076e435cea60bde6745bc9bcb21847a927d64753723fdc1bb73e56e`. This provenance summary identifies the historical basis; it is neither a replacement review record nor fresh approval of later revisions. A fresh clone can interpret current definitions without that local evidence; renewed review reliance requires the actual applicable assessment.

## SRC-WORKFLOW-DESIGN

Source: the user's instruction to proceed to System and Architecture Design after the author assessment identified in [the source provenance](#src-workflow-requirement-review). The [architecture composition](../architecture/README.md#requirement-first-workflow-composition) locates current owners: parent composition contracts, Module realization facets, SR-owned allocation arguments and parent-owned test designs for SR-079–083. This source identity remains stable after ownership reconciliation; it does not identify a separate workflow submodel.

This design refines reusable guidance, handoff, context and assurance Functions; adds FUNC-078 for bounded workflow adoption under MOD-006; and adds IF-011 as MOD-017's work-context/adoption contract consumed by MOD-012. MOD-012 also consumes the existing distinct authority and evidence contracts. AR-029–042 allocate the five new SRs across their accountable existing Modules. No Module, requirement statement or acceptance criterion is introduced or changed by this design pass.

The SR confirmation links and FEAT-017 realization link are design additions. The earlier requirement-review hashes retain their original meaning; new design relationships do not silently expand that review into design approval. Existing current-skill/software facets remain implementation observations; new skill names, successor operational contracts and SQLite support are not claimed implemented. SRC-WORKFLOW-CONTRACTS below identifies the subsequent subordinate contract refinement without rewriting this earlier design pass's authority.

## SRC-WORKFLOW-CONTRACTS

Source: the user's instruction to proceed with successor recording and installation contracts after ownership reconciliation. Current detail belongs to [MOD-011 records](../architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md), [MOD-010 commands](../architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/README.md), [MOD-013 packaging](../architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/README.md) and [MOD-014 installation](../architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/README.md).

The boundary analysis reuses IR-010 and FEAT-019 and refines existing SR-065/SCN-063 for separately authorized bounded obsolete-unit retirement. Ordinary force still selects only candidate replacement; path safety, complete preflight, original retention, unrelated-work protection and truthful partial effects remain. FUNC-064 and IF-006 reconcile this narrow extension with SR-083/AR-042. No new IR, Feature, Scenario, Function, Module or Interface is required. The prior SR-079–083 requirement assessment is not rewritten to cover this additional subject; its meaning and hashes remain unchanged.

This proposed design separates v4 semantic records and v2 public operations from their future machine schemas, adapter implementation and runtime adoption. It retains versioned historical tooling only for explicitly authorized historical recovery/import, never as an active automatic fallback. The scoped project exception permits an explicitly identified author assessment; it does not confer independent review, implementation completion or SQLite qualification.

The same boundary check refines existing IR-008 children SR-042–044: applicability is explicit at the contract's reliance boundary, assessment corrections preserve immutable prior accounts, and drift discovered after commit reports that committed outcome instead of promising rollback. FUNC-044–046 carry the corresponding logical behavior. Original v3 narrow-update and recovery rules remain authoritative for their original implementation/version. The refinement adds no new IR/SR identity and does not alter the earlier accepted SR-079–083 subjects.

The affected existing allocations AR-016, AR-018, AR-019 and AR-021 are reconciled with these shared requirement refinements. Their identities and owners are retained; v3-specific representation guarantees remain version-scoped, while v4 typed reference integrity, immutable assessment correction and commit truth are explicit. AR-029–042 remain unchanged.


## SRC-CUSTOMER-BROWSER-REQUIREMENTS

The user requested a designed, repository-distributed architecture browser for customer REM projects and authorized concrete Requirement Analysis and Review. The selected basis is local generation and portable read-only offline views; RigorLoop's own generated site is a separate reference artifact. IR-001/005 are reused unchanged, IR-002 retains its traceability need with explicit customer-view scope, and IR-010 extends its existing distribution need. SR-060 is refined; SR-084–088 and SCN-083–087 supply the missing customer outcomes. FEAT-022 is a durable generation/sharing capability, not a diagram type or delivery work item; FEAT-018 gains browser qualification scope. No new IR, Module, Interface, Function or AR is created.

The [customer browser analysis](published-products.md#customer-architecture-browser-analysis) records the dispositions and preserves the current rationale. The scoped author assessment is retained separately as an operational record (SHA-256 `a9537ee85723f844b3fbfba636900e4daf5132c10cdc99de193156396a0245b6`), not as another requirement definition. The five new Scenarios are confirmed requirement-analysis knowledge under the document-based review exception; this does not assert independent approval, product behavior or public availability. Older source judgments retain their original content scope. New requirements intentionally constrain their Feature while detailed Function coverage remains downstream System Design work.


## SRC-CUSTOMER-BROWSER-DESIGN

The user authorized Function reuse/gap analysis and integrated System/Architecture Design for the customer browser requirements. Existing definition retrieval, interpretation, navigation, command admission and release behaviors are reused within their meaning. FUNC-079–083 add coherent capture, qualified projection, portable artifact assembly, safe derived-output publication/recovery and actual browser-candidate qualification. They allocate to existing MOD-001/004/013. IF-012 is MOD-016's composed browser boundary for MOD-010; IF-001/004/005 are explicitly refined without repurposing the Baseline IF-007 or skill installer IF-006.

AR-043–051 derive from SR-084–088 and allocate one accountable owner each. SR statements and acceptance criteria are unchanged; Function links and allocation sources add design relationships without expanding the earlier requirement assessment. Proposed Node/renderer package, immutable input and versioned output choices belong to [MOD-004](../architecture/modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md); command and production details remain with MOD-010/013. These are target designs, not installed commands, customer platform qualification or observed runtime. Assessment evidence remains local operational history.

## SRC-PROPORTIONATE-REVIEW

Source: the user's clarification that local review should be proportionate, including whether approval can remain usable after subsequent file edits. The selected interpretation permits justified harmless edits to retain applicability and requires independent reassessment for material corrections; unknown impact remains unresolved. A changed file identity alone does not decide review validity.

Reuse IR-004 and IR-009. Clarify existing SR-029, SR-082 and AR-036 and extend SCN-080 with harmless-change continuation and misleading impact labels; preserve their identities and the single whole-change gate. The Scenario refinement is author-assessed requirement-analysis knowledge under the Constitution's document-based exception. Earlier assessment sources retain their original scope; no independent approval, implemented runtime behavior or workflow adoption is inferred.

[Governance](../architecture/modules/MOD-017-engineering-governance/README.md#changes-after-approval) owns the impact rule. The successor CLI/Records contracts preserve original judgments and explicit current applicability while withdrawing universal source-copy retention as a review prerequisite. Evidence required to justify a finding, comparison or preservation obligation still needs adequate retention.

## SRC-CURRENT-HANDOFF

Source: the user's explicit decision to maintain a current structured handoff rather than record all activity. Goal/scope/authority, governing basis, progress, open issues, relevant evidence, review standing and next action must support another participant without the originating conversation. Replace comparable working summaries, record at meaningful handoffs, retain supporting detail selectively, and preserve compact historical completion without continuous repository applicability tracking. Later regressions become linked new work.

Refine IR-003/008 and existing SR-006/023/024/027–029/042/043/082/083; reuse the remaining stakeholder needs. Reconcile their existing Scenarios, Functions, AR-017–019/036/040 and affected Interfaces without new model identities. Earlier source judgments and allocation arguments retain their original scope; SRC-CLI-ALLOCATION-BEFORE-CURRENT-HANDOFF identifies superseded criterion mappings, not proof of the revised behavior. This is authorized design authorship and author assessment under the Constitution exception, not independent approval or runtime adoption.

[Workflow analysis](workflow-refactor.md#current-handoff-refinement) records disposition. [Governance](../architecture/modules/MOD-017-engineering-governance/README.md) owns meaning; [Operations](../architecture/modules/MOD-018-engineering-operations/README.md) owns composition; its CLI and Records children own inputs, representation and recovery. Current v1/v3 implementations and historical import obligations remain version-scoped.

## SRC-SQLITE-ADOPTION

Source: current requirement-first SQLite adoption working-tree implementation, inspected on 2026-10-04. Named source paths in each realization facet identify the current binding; no source inspection asserts passing execution, installation, migration or publication. Earlier file-journal and Proposal-first observations retain their original scope at recoverable commit `39be9c81`; they are not current runtime descriptions. Requirement and Scenario refinements preserve the existing stakeholder needs while reconciling transaction recovery and explicit maintenance with the accepted Module design.

## SRC-SCOPED-TRAVERSAL-DESIGN

Source: the user’s instruction to continue concrete Design after the requirement evaluation exposed SR-009’s traversal and allocation gap.
Derive the bounded SCN-008 cooperation from unchanged SR-009 and FUNC-009: MOD-004 owns general traversal and its allocated obligation; MOD-016 supplies a consumer-focused read contract to MOD-010 using existing definition and interpretation owners.
This source records architecture rationale and proposed semantics only; review judgments and execution evidence remain operational records.

## SRC-RELATIONSHIP-AUTHORING-DESIGN

Design derivation from SR-008 and FUNC-008: single authoritative relationship facts, state-bound candidate admission and retention, and derived endpoint views. AR-057–059 allocate distinct editing, validation and storage obligations. Existing identity, interpretation and traversal allocations remain with their owners. This source records proposed architecture and rationale, not implementation or satisfaction.

## SRC-ALLOCATION-IMPACT-DESIGN

Architecture derivation from SR-010/011, FUNC-010/011 and SCN-009/010. MOD-004 owns attributable rule-based allocation assessment and witnessed potential-impact composition through AR-060/061; existing content, interpretation and traversal responsibilities are reused. This records target Design and rationale, not execution, implementation or requirement satisfaction.

## SRC-ASSURANCE-CONTENT-DESIGN

Architecture derivation from IR-004, SR-025–029, FUNC-027–031 and SCN-026–029 under the user's instruction to complete the Design assessment. AR-062–066 allocate distinct assurance-content obligations to MOD-007. MOD-017 supplies IF-014 preparation to MOD-012, with explicit participant-mediated recording through existing Operations. Assessor-assisted realization preserves separate method, observation, applicability, judgment, authority and actual retention meanings. This records proposed Design and rationale, not installed guidance, executed verification or satisfaction.

## SRC-CONFORMANCE-MIGRATION-DESIGN

Architecture derivation from IR-005, SR-012–015 and SCN-011–014 under the user's instruction to complete this Design pass. Existing AR-010 retains original-profile interpretation; AR-067–069 assign complete conformance diagnostics, separate mechanical/review presentation and source-preserving migration preparation to MOD-003. IF-001 captures attributable raw inputs before pure IF-002 checking and transformation. Candidate preparation leaves adoption and operational-record migration separate. This records proposed Design and rationale, not runtime availability, implementation, executed verification or satisfaction.

## SRC-BASELINE-STATE-DESIGN

Architecture derivation for SR-020–024 and SCN-019–022/025: [baseline state control](../architecture/modules/MOD-017-engineering-governance/state-control.md), immutable custody, original-meaning comparison/recovery and accountable transition/retirement. This source records proposed architecture rationale, not implementation or satisfaction.

## SRC-RESUMPTION-AUTHORITY-DESIGN

Architecture derivation from unchanged SR-006/007, FUNC-025/026 and SCN-023/024: [Change control](../architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/README.md) owns current handoff interpretation and applicable action authority through AR-077/078 and existing IF-011/009. This records proposed architecture rationale; retained review judgments and execution evidence remain operational records.

## SRC-OPERATIONAL-MAINTENANCE-DESIGN

Architecture refinement from unchanged SR-074–077, AR-052–055, FUNC-074–076 and SCN-070–073. [Work record storage](../architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md#database-schema-backup-and-migration) owns finite coherent backup, explicit same-project transfer and preserved-source migration; [the system composition](../architecture/README.md#controlled-work-and-recoverability) connects these outcomes to IR-003 resumption, authority, Baselines and selective retention. This records Design rationale; review judgments, exact assessed identities and execution evidence remain operational records.

## SRC-CURRENT-KNOWLEDGE-DESIGN

Architecture refinement from unchanged IR-001, SR-001–005, AR-001–009 and SCN-001–006. The owning Definition storage, Definition editing and Views and traceability contracts define exact retained content, complete identity scope, supported same-entity revisions and separately applicable current rationale through existing IF-001/002. This records Design rationale; independent judgments and actual execution evidence remain operational records.

## SRC-AUTHORING-GUIDANCE-DESIGN

User-authorized Design assessment of IR-006 and SR-032–034, with existing FEAT-010, FUNC-032–034 and SCN-031–034/040. Derive only the missing MOD-008 source-selection, bounded-correction and prepared-task obligations, preserving canonical method ownership and existing assurance/recording boundaries. This source records proposed Design rationale, not participant results, installed implementation or satisfaction.

## SRC-LESSON-IMPROVEMENT-DESIGN

User-authorized Design assessment of IR-007 and SR-035–038 with existing FEAT-011, FUNC-035–038 and SCN-035–039. Derive missing MOD-009 obligations and IF-017 preparation while preserving existing Learn confirmation/custody, controlled adoption, assurance and retention owners. This is proposed Design rationale, not an executed learning session or evidence of effectiveness.

## SRC-SUBJECT-HISTORY-DESIGN

User-authorized SR-078 Design extends existing command/storage responsibility through FUNC-077, AR-086/087 and proposed IF-003/004 history operations. Explicit recorded identity, retained-scope completeness and state-bound continuation preserve historical meaning. Current runtime contracts, selective retention and separate adoption remain intact; no whole-IR-008 coverage or implementation conclusion follows.

## SRC-ADOPTION-DEPENDENCY-REFINEMENT

User-approved refinement of IR-009, SR-083 and SCN-082 on 2026-10-06: adoption requires compatible recording for selected work; historical import is unnecessary when there are no earlier dependencies, while necessary unavailable migration blocks affected adoption. This narrows the earlier unconditional migration-independent promise to reconcile the [Constitution successor policy](../../CONSTITUTION.md#workflow-and-review). Preserve actual authority, work and historical judgments; authoring, review and portable invocation do not activate a workflow. Supporting allocation and design follow this refined obligation; review judgments and execution evidence remain operational records.
