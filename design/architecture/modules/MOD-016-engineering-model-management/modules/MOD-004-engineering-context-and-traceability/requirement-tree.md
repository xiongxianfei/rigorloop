# Unified system Requirements view

This architecture refines [MOD-004 Views and traceability](README.md) for one system-level expandable requirement tree containing linked Feature, Function and Module references.
It is an isolated architecture design; it does not claim implementation or design-review approval.
The existing requirement and relationship records remain authoritative.

## Basis and responsibility

The design uses IR-002's traceability need, SR-008's authored relationships and inverse views, SR-009's bounded traversal, and the existing browser reading basis SR-085/086.
FUNC-007 presents definitions and qualifications; FUNC-009 navigates relationships; FUNC-080/081 compose views and the portable reader.
These Functions retain MOD-004 as their accountable owner.
The existing browser AR-046/047 remain applicable; this refinement introduces no new allocation boundary or AR.
These references supply the design basis, not a new assertion of requirement acceptance or satisfaction.

MOD-001 retains input capture and content authority; MOD-003 retains profile interpretation and validity through the existing IF-001/002 cooperation.
Requirements is an optional supplementary architecture view owned by MOD-004, alongside the five standard 4+1 perspectives.
It adds no new Module, Interface or service, and does not redefine the standard five views.
The [relationship ownership table](../../../../../support/README.md#relationship-ownership) governs edge meaning.

## Reader composition

Add **Requirements** to the architecture-view tab row at the RigorLoop system root, after Scenarios.
Enable this optional view for RigorLoop only in the current design scope; it is unavailable at every Module scope.
The Architecture scope tree continues to select RigorLoop or a Module; Requirements has no separate top-level navigation destination.
It opens one workspace whose primary surface is the complete system requirement tree, with an optional detail panel alongside it.
All IRs belong beneath one presentation root labeled with the selected system name and “Requirements”.
That root is not an authored requirement and has no REM identity.
Features, Functions and accountable Modules are expandable reference occurrences inside this same tree; selecting them never opens a separate catalogue or changes the workspace.
The tree uses the available width when details are closed and remains visible when the panel is open on a wide screen.
The architecture tabs remain visible, with RigorLoop selected in the scope tree and Requirements marked as the active view.
Module pages retain Summary and the five standard perspectives without a Requirements tab.

### Optional view selection

Use an explicit presentation selection, not the presence of requirements or a project-name match, to enable the view.
The matched browser-data contract carries an optional boolean `system_requirement_view`; absent or false means disabled, and true enables the system-root tab and routes.
RigorLoop's selected presentation supplies true; other projects remain disabled in this scope.
This is presentation metadata, not a canonical requirement field, Module allocation, public CLI option or extension to the standard five-view vocabulary.
Keep the existing five-view data collection and registered diagram kinds unchanged; the supplementary renderer consumes the existing records and relationships.
Malformed flag values reject assembly under the existing matched-data validation boundary.
When disabled, omit the tab and show an explicit unavailable result for its routes with a link to System Summary.
When enabled with an empty valid requirement collection, keep the tab and display “No requirements in this snapshot”.
Invalid required model content remains an error, not a reason to silently disable the view.

### UI wireframe

```text
Architecture scope: RigorLoop · System
Summary | Logical | Process | Development | Physical | Scenarios | [Requirements]

[Search requirements and references by ID or title]
[Expand all] [Collapse all] [Expand to SR level]

ONE SYSTEM TREE                                        DETAILS       [Close]
v RigorLoop · Requirements                             FUNC-A · Generate report
  v IR-A · Export reliable reports                     Type: Function reference
    v Features (1)                                     Via: SR-A / confirms
      v ↗ FEAT-A · Export reports [confirms]             Behavior, inputs, outputs
        v Realizing Functions (1)                       Features realized
          > ↗ FUNC-A · Generate report [realized by]     Related requirements
    v SR-A · Export every selected record               Accountable Module
      v Functions (1)                                   Sources and qualification
        > ↗ FUNC-A · Generate report [confirms] ← selected
      > Constrained Features (1)
      v Allocated requirements (1)
        v AR-A · Produce a complete report or fail
          v Accountable Module (1)
            > ↗ MOD-A · Report production [allocated to]
          v Constrained Functions (1)
            > ↗ FUNC-A · Generate report [constrains]
    > SR-B · Another system obligation
  > IR-B · Another stakeholder need

v expanded   > collapsed   ↗ linked reference, not requirement containment
```

The RigorLoop shell illustrates placement; the report-related names and letter-suffixed IDs are synthetic presentation examples, not repository entities or newly authored obligations.
The repeated FUNC-A rows refer to one Function through three different declared paths.
The side panel identifies both its entity identity and the occurrence's relationship path.
The generated view uses actual captured identities, names, relationships and qualifications.

### Hierarchy and reference branches

Canonical requirement containment remains IR → SR → AR.
An IR has SR children; SR-derived ARs appear under an “Allocated requirements” presentation group.
ARs have no requirement children, but can expand to show accountable Module and Function reference groups.
Group rows organize presentation; they are not new engineering entities or authored containment edges.
Requirement rows and reference rows have distinct type labels, reference indicators and relationship labels, with readable titles and IDs.
Expanding a group shows all its declared references.
Group counts identify distinct direct targets, not coverage or inferred descendant obligations.

| Tree row | Expandable branches in the same tree | Relationship authority |
| --- | --- | --- |
| System root | All admitted IRs | Presentation root only |
| IR | Confirmed Features; SR children | IR `confirms` and SR containment |
| SR | Confirmed/constrained Functions; constrained Features; allocated requirements | SR `confirms` / `constrains` and AR containment |
| AR | One accountable Module; constrained Functions | AR `allocated_to` / `constrains` |
| Feature reference | Short capability summary; realizing Functions | Feature definition and `realized_by` |
| Function reference | Short behavior summary | Shared Function definition; full relationships in the detail panel |
| Module reference | Short responsibility summary | Shared Module definition; full relationships in the detail panel |

Under an SR's Functions group, a target confirmed and constrained by the same SR appears once with both labels.
Across different groups or requirements, the same target may appear several times as separate reference occurrences while retaining one entity definition.
Each AR has exactly one accountable Module; cooperating Modules must not appear as additional allocation owners.
Scenarios remain separate entities and appear in requirement details through their existing relationships.

Applicable empty groups read “None declared” with no disclosure button; this does not imply completed analysis or zero required behavior.
Unsupported group kinds are absent, rather than fabricated for every requirement type.
An empty admitted requirement collection shows the system root with “No requirements in this snapshot”.
Feature-to-Function references expand beneath the Feature with “Realized by” labeling; they must not become direct IR-to-Function confirmations.
Reverse references, Function allocations and further Module relationships are links in the detail panel, not recursively expanded tree branches.
This finite expansion grammar prevents a shared graph or inverse edge from producing an infinite tree.

### Expansion and selection

Opening the view initially expands the system root and leaves the IRs collapsed, unless a selected deep link requires ancestors to be revealed.
Each requirement, group and reference disclosure is independent; a reference's disclosure shows its summary and permitted branches, while its name selects the full definition in the same detail panel.
Collapsing a branch hides its descendants without erasing their saved expansion states.
“Expand all” opens every branch admitted by the finite grammar; “Collapse all” closes every branch below the visible system root and resets their saved expansion states.
“Expand to SR level” opens the system and IRs, shows SR rows, and closes SRs and all relationship groups.
These actions never change the selected definition; if they hide its occurrence, the panel offers “Reveal in tree”.
With a search active, Expand all and Collapse all operate on the filtered projection; clearing search restores the pre-search expansion state.
Expand to SR level clears search and applies its named whole-system preset.
Closing the detail panel restores tree width and focus to the selected row without clearing selection or expansion.

## AR implementation and verification indicators

Keep three distinct claims: definition lifecycle, implementation progress and verified satisfaction.
The canonical AR `status` remains the definition lifecycle; this profile currently admits only `draft`.
Display it as “Definition: Draft” in the AR detail panel, never as implementation progress.
The tree shows two explicitly named text badges on every AR row, also repeated in its detail panel.
Badges must remain understandable without color and must not appear on a referenced Module or Function as if that reference owned the AR's result.

| Indicator | State | Meaning at the assessed scope and revision |
| --- | --- | --- |
| Implementation | Unknown | No applicable implementation assessment is included in this snapshot |
| Implementation | Not started | The accountable owner explicitly reports that the scoped work has not begun |
| Implementation | Partial | Some of the AR's complete obligation is reported implemented; remaining scope is named |
| Implementation | Implemented | The accountable owner reports the complete AR scope implemented, with coverage and implementation references |
| Verification | Not assessed | No applicable conclusive assessment of the complete AR is included; partial or inconclusive evidence remains visible in details |
| Verification | Passed | An applicable verification assessment supports every acceptance criterion and the AR's complete scope |
| Verification | Failed | Applicable verification identifies an unmet obligation; its affected criteria and failure evidence remain visible |
| Verification | Needs reassessment | A retained assessment's required basis has changed, is stale, conflicts, or cannot establish current applicability |

For example, the display grammar is `AR-xxx · Title [Implementation: Partial] [Verification: Not assessed]`; this is an illustrative state, not an assessment of a real AR.
An implementation claim may coexist with failed verification; passing one test or finishing one Change does not establish a complete AR result.
Unknown must not be relabeled Not started, and a partial result must not be promoted to Implemented or Passed.
Requirement IDs and exact AR definition identities bind the claim; acceptance-criterion positions alone are insufficient when the definition changes.

### Assessment authority and presentation data

Implementation accounts belong to the accountable Module's delivery work; verification judgments belong to the responsible verifier under [Assessment](../../../MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md).
Operational records retain those accounts and their evidence through the supported CLI; canonical AR definitions do not store mutable progress or test results.
The browser is a read-only projection and does not provide a checkbox that marks an AR implemented or passed.
Its reader never scans project-local record stores, fetches live evidence, or infers progress from code existence, Function allocation, a rendered graph, or a completed Change.

The assessment projection must explicitly select supported operational records before generating a shareable snapshot, with selected content and disclosure scope stated by the caller.
For each claim, preserve the AR ID and exact definition identity, assessed scope and criterion coverage, actual reporting actor and time, implementation subject identities, source Change/assessment references, evidence, limitations and remaining gaps.
The generation boundary must establish the selected account's applicability against the captured model and implementation basis; the offline reader cannot compare against a live checkout.
Implementation and verification retain separate authorities and support, even when displayed beside one another.
Unknown state values, wrong requirement kinds, invalid references and contradictory duplicate current accounts must be rejected or explicitly diagnosed before a positive indicator can be displayed.
Selection by newest timestamp alone does not resolve conflicting assessments.

When an AR or material implementation basis changes, preserve the old account as historical detail and withhold current positive claims until reassessed.
If implementation applicability is lost, show Unknown with the previous account's explanation; if a verification account loses applicability, show Needs reassessment with its previous outcome and cause.
An unrelated edit or operational recording update alone does not invalidate an assessment; applicability follows the owning assessment rules.
The detail panel must distinguish absent assessment data from explicitly pending work, and expose actual covered/uncovered criteria, implementation references, verifier evidence, assessed revision and limitations when those data are available.

An SR may summarize known AR implementation counts, with the total and unknown/unassessed counts shown separately.
This is a progress summary only: even all known ARs implemented or verified does not establish allocation completeness or replace verification of the SR's integrated system obligation.
Zero ARs does not establish allocation completeness or 100 percent completion.

The [version 2 delivery format](requirement-delivery-format.md) extends these principles to direct IR/SR accounts and defines exact compatibility and normalized reading. The repository renderer accepts versions 1 and 2; the following section retains the supported external version 1 contract. Both use one internal delivery representation beside the separate Design projection.

### Current repository design-browser scope

The repository renderer accepts an explicitly selected, sanitized JSON assessment export through `--assessments PATH`. The caller selects and reads the retained operational attachment through the supported CLI, checks its disclosure scope, then supplies those bytes. The renderer does not discover records, choose the latest account, or authenticate the reporting actor. The generated disclosure is a reading projection; original judgments remain operational records.

The selection is frozen in the generated `assessment-snapshot.data` JSON companion and embedded in `index.html` for offline reading. Subsequent generation and `--check` reuse that named selection, never a private store. An absent companion means no assessment. `--clear-assessments` explicitly replaces it with an empty selection; replacement and clearing remain subject to normal regeneration checks. This makes the browser reproducible when copied with its generated companion and canonical sources. The companion is generated disclosure data, not a place to author assessments.

The version 1 envelope contains `format_version` and `assessments`. Each selected AR account contains its `requirement`, `definition` (repository-relative path, SHA-256 identity and original UTF-8 JSON `content`), `scope`, `record` (Change and Evidence IDs), separate `implementation` and `verification` claims, and `criteria`. Each claim contains `state`, `actor`, `reported_at` (UTC), `summary`, `limitations` and `subjects` (path and SHA-256 identity). Each criterion contains its one-based `number`, separate implementation and verification states, `evidence` and `gaps` arrays. The content bytes must match the definition identity and decode to the selected AR. Criterion coverage is validated against that captured definition, including when the current definition has added, removed or reordered criteria. The exact AR definition identity binds criterion numbering to the original text. Evidence entries are concise disclosed observations, not automatically executed links or inferred approval.

Closed vocabularies use lowercase hyphenated spellings of the states above. Unknown fields, unknown states, duplicate JSON keys, duplicate AR selections, wrong requirement kinds, unsafe paths, missing claim attribution, malformed identities and incomplete or duplicate criterion coverage reject before output writes. Subject paths must stay within the repository, exclude operational storage and generated browser artifacts, and resolve without escape through symlinks. Complete implementation and verification claims require every criterion respectively implemented or passed, no remaining criterion gaps, no claim limitations and nonempty material subjects. Partial implementation requires named gaps or limitations; Failed verification requires an identified failed criterion; Not assessed must not hide a criterion explicitly assessed Failed. Claims are supplied judgments, not decisions computed from test totals.

At assembly, compare both the AR definition and each claim's selected material subject identities with the checkout. A moved definition is compared through the same AR ID at its current canonical path, retaining the original path as provenance and requiring reassessment. A missing or changed basis preserves the supplied claim as historical detail and replaces its current indicator with Unknown for implementation or Needs reassessment for verification. Each claim has its own applicability and explanation. A changed definition invalidates both claims, and its criterion positions are labeled historical rather than attached to the changed current text. Generation never silently refreshes old identities. Unrelated source changes do not invalidate a claim; the accountable assessor must select a sufficient material basis.

The detail panel displays the assessed scope, actors and time, source record IDs, exact identities, historical outcomes when stale, and each criterion's evidence and remaining gaps. The original version 1 pilot selects AR-046 only. Version 2 supports explicitly supplied IR/SR/AR accounts and conflicts under the linked format contract. Any unselected requirement retains Unknown / Not assessed with an absence explanation; definition lifecycle remains independent. This repository reading refinement does not add a storage schema, mutable status-editing command, automatic reassessment engine or customer generator support.

## Components and data contract

The repository design renderer explicitly selects `system_requirement_view=true`; the reusable projection defaults to false and rejects non-boolean selections. The HTML reader presents the real embedded records without changing canonical obligations. Refresh the generated browser after design changes. This design-reading support does not establish customer generator or package delivery.

| Component | Contract and responsibility | State authority |
| --- | --- | --- |
| Existing model interpreter | Read canonical records, validate typed references and derive requirement parent edges from containment | Authoritative input remains the selected source records |
| Existing browser projection and assembly | Include explicit system-view enablement, entity records, typed relationships, provenance and source identity in the matched offline artifact | Derived snapshot only |
| Existing architecture scope/view navigation | Expose Requirements only when enabled at system scope; route explicit Module-scope changes to Module Summary | Local navigation state; no new Module responsibility |
| Requirement navigation index | Build requirement roots, children, typed reference groups, bounded display occurrences and incoming-reference lookup from embedded data | Ephemeral derived reader indexes |
| Requirement tree and detail renderer | Present the system root, unified hierarchy/reference branches, selected definitions and relationship paths | Local occurrence selection, independent expansion, filter and focus state only |

Reuse the existing embedded `records` and `relationships` representation.
A requirement parent edge has the child's ID as `source`, `parent` as `relation`, and its parent's ID as `target`.
Its source locator identifies containment.
This differs from Module `contained_by` edges; do not reuse the Module-only parent index as a requirement index.
Typed cross-links retain `source`, `relation`, `target`, `path` and `field` attribution.
The reader may derive lookup indexes and virtual group rows, but neither authored JSON nor generated data needs another independently maintained parent/child or inverse-reference collection.
An occurrence key combines the owning requirement's containment path with the ordered presentation-group and target-ID steps; it does not replace the target's entity ID.
Retain the typed edges as attribution on those steps, so an SR confirming and constraining the same Function still has one stable row in its Functions group.
Expansion keys use artifact identity plus occurrence key, so opening FUNC-A under one SR does not expand every appearance of that Function.
Store each entity definition once and dereference it when rendering an occurrence or its detail panel.

Require unique IDs, resolved correctly typed references, one IR parent per SR and one SR parent per AR before assembly.
The presentation root contains all admitted IR records, not arbitrary records lacking a parent.
Use stable ID order for roots and siblings; changing a title must not reorder or reparent a requirement.
Profile-valid omission of optional links remains distinguishable from an invalid reference.
An invalid containment edge or unresolved target rejects preparation under the existing contract, preserving the prior output.
If an opened artifact is malformed, show a bounded “Requirement navigation unavailable” diagnostic rather than rendering an apparently complete partial tree.

## Navigation and reading state

Use `#requirements` for the tree and `#requirements/<requirement-id>` for a selected requirement.
Use `#requirements/<requirement-id>/related/<entity-id>` to inspect a linked entity while keeping the selected requirement and tree visible.
All these routes retain RigorLoop system scope and the active Requirements tab; the requirement ID is a selection within that scope, not another architecture scope.
Do not admit Module-scoped Requirements routes such as `#requirements/MOD-004`; show an explicit unsupported-scope result with navigation to system Requirements or that Module's Summary.
These routes are also unavailable when the explicit optional-view flag is disabled.

Switching between system architecture tabs retains system scope and saves the Requirements tree's selection, expansion, search, panel and scroll state.
Selecting a Module in the Architecture scope tree while Requirements is active opens that Module's Summary and hides the Requirements tab.
This is an explicit scope-transition rule, not a missing-view fallback or an inferred Module requirement slice.
Selecting the RigorLoop root from that Module returns to System Summary; selecting its Requirements tab restores the saved system tree state.
Back to a system Requirements history entry likewise restores its state.
Selecting a Module reference inside the requirement tree only changes the detail panel and keeps system scope.
An explicitly labeled “Open Module architecture” action in that panel changes scope and opens Module Summary.

An encoded `at` fragment parameter selects the occurrence path when a target is reachable through several branches; validate every step against captured edges and the finite expansion grammar.
Without `at`, choose the first matching occurrence in stable display order and reveal its path.
The related route admits direct Feature/Function/Module references and Feature-to-Function paths declared for that owning requirement; an unrelated identity receives an unavailable-link result.
Reverse requirement links select their target requirement's canonical tree route within the workspace.
Other detail-panel relationship links replace only panel content, retain the origin occurrence and show the traversed edge; they never auto-graft another graph branch into the tree.
Such further detail selections remain in local browser history; the tree-addressable fragments above describe only admitted occurrences.
Store search in an encoded `q` fragment parameter, so browser Back restores the filtered context.
Keep independent occurrence expansion, panel visibility, scroll and focus in local history state, scoped to the current artifact; a fresh deep link reconstructs all ancestors and reference groups needed to reveal its selected row.
No database, network API or model write is involved.

The existing `#entity/<id>` routes keep their meaning.
When the optional system view is enabled, requirement entity pages gain an “Open in requirement tree” link and Feature, Function and Module pages gain derived incoming requirement links into it.
When disabled, ordinary entity details and relationship navigation remain available without advertising tree routes.
Following an incoming requirement link opens its canonical tree route and expands its ancestors.
From a Feature detail, “Realized by” links open Function details; from a Function detail, list the Features it realizes and confirming/constraining requirements separately.
Reverse views are computed from the original edges and retain their original direction and attribution.
Browser Back returns to the previous selection and local reading state.

Search matches requirement and displayed Feature/Function/Module IDs and titles case-insensitively.
It shows all matching occurrences and their requirement, group and reference ancestors, temporarily expanding the paths needed to reveal them.
Only paths admitted by the finite tree grammar participate; an otherwise unlinked entity remains discoverable through existing global search.
Ancestors shown for context are distinguished from matches; filtering never changes the underlying parent or relationship data.
Clearing search restores the prior expansion state and selected node.
A selected node hidden by a filter remains identified in the detail pane with a “Reveal in tree” action that clears the filter and expands its ancestors.
Do not silently replace the selection with the first match.
For no matches, show an explicit empty result; for an unknown deep-linked ID, identify the unavailable requirement or reference in this snapshot.

Use nested semantic lists with separate disclosure buttons and ordinary links, not an ARIA tree containing competing interactive chip controls.
Tab reaches controls and links; Enter activates links and Enter/Space toggles disclosures.
Selection, expansion and focus remain distinguishable without color alone.
On narrow screens, retain the architecture scope menu and horizontally scrollable tab row; open details as a dismissible sheet in the same workspace, preserving the tree's selection, expansion, scroll and return focus.
Essential statements, acceptance criteria and relationship targets remain readable from a copied offline artifact even if optional repository source links cannot resolve.

## Realization views and decision

The owning [Requirements view design diagrams](README.md#requirements-view-design-diagrams) define the registered Logical structure, unified tree wireframe and Process interaction diagrams.
Read their generated projections in the browser: [Unified Requirements tree wireframe](../../../../views/browser/index.html#logical/MOD-004/proposed/topology/unified-requirement-tree), [Requirements view structure](../../../../views/browser/index.html#logical/MOD-004/proposed/topology/requirement-view-structure) and [Requirements reader interaction](../../../../views/browser/index.html#process/MOD-004/proposed/sequence/requirement-reader-interaction).
The directly readable [system Requirements tree](../../../../views/browser/index.html#requirements) projects the current canonical model in the repository design browser. The three MOD-004 topics explain its design; they are supplementary to that tree.
Their Module-owned placement explains implementation responsibility; it does not make the proposed Requirements view available at Module scope.

Logical: MOD-004 composes one optionally enabled, system-rooted requirement tree with bounded typed reference branches using the existing model-reading boundaries.
The technical components above are subordinate implementation responsibilities, not new REM entities.

Process: generation captures and interprets the selected model, validates hierarchy and references, embeds the existing records and edges, then assembles and publishes the artifact through the existing browser pipeline.
On open, the reader derives navigation indexes once; disclosure reveals the selected occurrence's permitted children or summary, and selection renders one shared definition in the existing workspace.
Expanding a Feature to a Function adds an explicitly labeled reference occurrence, never a new model edge.

Development: the repository realization extends `scripts/resources/rem-architecture-browser/viewer.js`, `viewer.css` and `index.html` for system-only view admission, navigation, layout and state.
Reuse `scripts/lib/rem_architecture_model.py` interpretation and existing browser projection rather than introducing another filesystem parser.
Projection adds the explicit optional-view flag from the selected RigorLoop presentation; reuse the existing record and relationship payload without duplicating it.
The reader's scope/view navigation admits Requirements only at enabled system scope, while ordinary architecture perspective handling and registered diagram vocabulary retain their five-view meaning.
The proposed customer engine retains the matching template/data contract owned in the Module README; this view does not change its Node/Rust/D2 technology decision.

Physical: the generated HTML and embedded resources execute in the reader's browser with no server or SQLite access.
UI state is disposable and must not outlive its artifact identity as engineering truth.

Scenario: for the existing offline-reading situation SCN-084, select Requirements at the RigorLoop system root, expand an IR's Feature and realizing Functions, then expand an SR's Functions and an AR's accountable Module.
Select each reference into the same panel, collapse a branch without collapsing another occurrence of its shared Function, and use a reverse requirement link to reveal its owning branch.
At each step the copied snapshot supplies the identity, relation direction and relevant definition without retrieving source files.
SCN-008 supplies the relationship-traversal situation; this walkthrough refines presentation and does not add internal steps to the governed black-box Scenario.
Select a Module scope and observe its Summary with no Requirements tab, then return to RigorLoop and select Requirements to recover the saved tree state.

Choose an HTML hierarchy with ordinary relationship links instead of a graph canvas: containment stays readable, shared targets retain their identities, and keyboard/offline reading uses the existing platform.
A canvas, separate relationship datastore and precomputed all-path closure add no necessary capability for this scope.
Revisit rendering scale only when measurements show the nested-list reader inadequate; initially render children on expansion and index direct edges once.

## Verification intent

These are intended observations for later implementation and review, not executed evidence.

| Situation | Observable result and failure detected |
| --- | --- |
| RigorLoop presentation enables the optional view | Requirements appears after Scenarios only at the system root; selecting it retains system scope and the architecture tab row |
| Disabled or absent flag; enabled but empty model | Disabled view exposes neither a tab nor valid Requirements routes; enabled empty view remains available with an honest empty state |
| Invalid enablement type or invalid required model | Assembly rejects the candidate rather than coercing the flag or silently hiding required invalid content |
| Module scope selection and unsupported Module-scoped URL | Explicit scope selection opens Module Summary; the unsupported URL reports unavailability rather than rendering a Module requirement slice |
| Module reference selection, explicit architecture action and return | Reference selection stays in the system detail panel; the labeled architecture action changes scope; returning to system Requirements restores its tree state |
| IR with two SRs, one with ARs, and a second IR | One system root contains every requirement under its exact parent; virtual groups and reference rows remain distinguishable from canonical containment |
| Two SRs confirm one Function; one also constrains it | One target definition is shared; the dual-relation group row shows both labels, separate occurrences expand independently and incoming links reveal both SRs |
| IR confirms a Feature whose Function lacks a direct IR link | The Feature expands to its realizing Function inside the same tree with the path visible; no invented direct confirmation |
| AR with no assessment projection | AR row and details show Implementation: Unknown and Verification: Not assessed; definition lifecycle remains separately labeled, and no code/test/Change-completion inference is made |
| Selected complete, partial, failed, stale or conflicting assessment accounts | Scope, criterion coverage, revision, actual authority and limitations remain visible; partial or stale support never produces a current positive complete-AR badge |
| Selected export followed by ordinary generation/check and explicit clearing | Named frozen selection is reproducible without private records; clearing restores absence; invalid input preserves prior output before compiler invocation |
| Unknown state/version/field, duplicate account/criterion/key, unsafe or symlink-escaping subject path | Strict rejection exposes the owning diagnostic, with no source or output mutation; no inferred positive result |
| Changed material subjects or changed AR criterion count/order; unrelated edit | Claims downgrade independently where their selected basis changed; original criterion text and outcomes remain historical; unrelated edits preserve applicability |
| AR with an allocated Module and cooperating architecture | Its tree branch shows exactly the accountable Module; selection displays responsibility in the same panel without claiming multiple owners |
| Expand/collapse controls and a hidden selected occurrence | Local collapse preserves descendant state; global presets apply their declared scope; selection survives and Reveal in tree restores its path |
| Inverse references form a graph cycle | Expand all terminates at the finite reference grammar and never duplicates a target definition or recurses through reverse links |
| Empty links, absent optional analysis detail and an unallocated Function | Honest scoped absence is shown without satisfaction or ownership inference |
| Missing parent, duplicate identity or wrong target type | Generation rejects the candidate and prior output remains readable |
| Shared Function/Module search, occurrence deep link, linked detail and Back | Matching occurrences and their paths are visible in the same workspace; independent expansion, selection, filter, panel state, scroll and focus remain coherent; missing IDs and no matches are explicit |
| Copied artifact with source checkout and network unavailable | Tree, definitions, direct/inverse links and Feature-to-Function traversal remain usable |
| Keyboard-only and narrow viewport | Disclosures, relationship links, details and return navigation remain reachable and understandable |

Reuse existing model-validation and offline browser walkthrough coverage, with a small independently specified fixture for shared links and parentage.
Expected relationships come from the fixture contract, not from the renderer's own derived indexes.
The integrated design-review subject is this refinement together with the affected existing browser reading contract; implementation remains a separate authorized scope.
