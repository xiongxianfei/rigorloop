# Architecture views

Open [the architecture browser](browser/index.html#home) directly in a browser. It includes all five REM views, diagrams, details and source links; no server or network is required.

| View | Reading focus |
| --- | --- |
| [Logical](browser/index.html#overview) | Module responsibilities, Interfaces, allocations, technical component structure, Commands and Skills |
| [Process](browser/index.html#process) | Execution boundaries, publication/recovery interactions, coordination and lifecycle |
| [Development](browser/index.html#development) | Software organization, Interface bindings, product construction and test architecture |
| [Physical](browser/index.html#physical) | Consumer deployment, storage and isolation, production placement |
| [Scenarios](browser/index.html#scenarios) | Stakeholder outcomes, selected obligations and applicable details across the other views |

Logical navigation also provides [CLI cooperation](browser/index.html#cooperation), nine contract walkthroughs, and the 22 [CLI acceptance contributions](browser/index.html#contributions). These explain recorded responsibilities and obligations; they do not establish executed behavior or requirement satisfaction. Names lead the diagrams; exact identities, source paths and qualifications remain available in detail. Use zoom, scrolling and Fit for larger diagrams.

Public capabilities presents the designed [Skills](browser/index.html#skills) and [Commands](browser/index.html#commands) as searchable entries with purposes, responsible Modules and governing design contracts. Existing procedure files and dispatch observations remain in the owning Development realization under **Observed public sources**. Catalogue inclusion does not require implementation or installation.

Development includes [Test architecture](browser/index.html#development/testing): bounded CLI, Records, Installation and Packaging groups, their assessed Modules, observation boundaries, fixtures and execution dependencies. Shared execution tooling links to its retained Validation contract; its REM allocation remains unresolved. These source observations describe test organization, not passing results or complete coverage.

The [publication](browser/index.html#scenario/SCN-046) and [recovery](browser/index.html#scenario/SCN-047) Scenario walkthroughs explain each expected, alternative and failure outcome through selected criteria, exact accountable Modules, Interface contracts and relevant Process, Development and Physical details. Their test links provide context rather than asserted outcome coverage. The other selected Scenarios retain their full outcomes and broad traceability, with detailed outcome selections shown as not yet developed. Canonical Scenario records remain unchanged.

## Generate and check

Edit the owning engineering records and explicitly registered source diagrams, then run from the repository root:

```bash
python3 scripts/render-rem-product-inventory.py
python3 scripts/render-rem-architecture-browser.py --d2 /path/to/d2
python3 scripts/render-rem-product-inventory.py --check
python3 scripts/render-rem-architecture-browser.py --d2 /path/to/d2 --check
```

Generation uses D2 0.9.0 with ELK for derived projections and Dagre for authored diagrams. Supply `--d2` or `REM_D2`, or put D2 on PATH. No Mermaid or browser runtime is needed to generate diagrams. Missing required tools fail generation; no implicit downloader runs in the generator. Reading needs only a browser. `--root PATH` selects a repository snapshot. Checks compare expected bytes without writing. Reload the browser after regeneration.

Offline reader tests use the locked Puppeteer package in `tests/engineering/validation/browser-toolchain/` and Chrome 149.0.7827.55. Install test dependencies with `npm ci --ignore-scripts` in an isolated copy; set `REM_PUPPETEER` to its `node_modules/puppeteer` directory and `REM_CHROMIUM` to the browser executable. These dependencies are used by tests only.

`browser/` contains replaceable generated HTML, D2/SVG diagrams and a hash manifest. The shared model/projection lives in `scripts/lib/rem_architecture_model.py`; browser templates and interaction code live in `scripts/resources/rem-architecture-browser/`. The separate inventory generator owns only the marked block in `design/requirements/published-products.md`. Do not hand-edit generated output.

The [REM method](../../../rem/methods/architecture-views.md) defines the concerns; the [application profile](../../support/README.md#four-plus-one-view-projection) defines their repository interpretation. Canonical records own facts and source qualifications. This directory maintains one browser presentation and this reading guide.

The [consolidation record](../../../docs/changes/2026-09-26-rem-architecture-refinement/browser-view-consolidation.md) records validation and the recovery revision for retired Markdown views and their earlier evidence links. Historical subjects retain their original meaning; current generation does not depend on retired files.

## Workflow design projections

The [architecture composition](../README.md#requirement-first-workflow-composition) locates current design owners. Review acceptance does not turn a generated view into another model or remove applicable design facts; later revisions update owners and regenerate these views.

Maintain the current design directly in those owning sources and regenerate the browser when it changes. Diagram labels distinguish Design from Observed implementation facts; they are not a proposal/approval lifecycle. Design decisions can be corrected in place without creating another direction document.

- Logical derives parent/child responsibility, Function and AR allocation, and IF-008–011 cooperation from entity records.
- Process currently displays MOD-012's proposed runtime choice separately from observed CLI execution. The [Process projection refinement](../../support/README.md#process-projection-refinement) retains a deferred structured-renderer option. Architecture Design can refine topology and qualified activity/interaction explanations in the owning sources without a delivery-plan prerequisite. Detailed gate semantics remain with Governance; no target process execution is asserted.
- [Change control Process](browser/index.html#process/MOD-006) shows the resume-and-coordinate sequence. Its Parent composition links the [whole-change review and Verify sequence](browser/index.html#process/MOD-017/proposed/sequence/whole-change-review-and-correction), and its separate correction sequence, owned by Change and quality control. Milestone progress, review attempts and Verify remain distinct; implementation observations remain separately attributable.
- Development displays proposed replacement entrypoints and packaging choices from MOD-012/013 software facets alongside the unchanged observed catalog.
- Physical displays MOD-018's proposed local placement and MOD-014's installation choice; it does not claim deployed SQLite support or atomic project migration.
- Scenario entity details expose SCN-075–082 and their requirement links. Selected generated walkthroughs remain the existing five Scenarios; the new internal walkthrough and proof intent belong to the [Operations](../modules/MOD-018-engineering-operations/test-design.md) and [Governance](../modules/MOD-017-engineering-governance/test-design.md) test designs. Their absence from the selected walkthrough panel is an explicit projection limit, not missing stakeholder requirements or executed proof.

Proposed facet decisions carry rationale, alternatives, consequences and revisit conditions. Projection does not implement, adopt or approve them. Delivery sequencing and assessment results remain outside generated design views.

## Proposed customer distribution

The [customer browser composition](../README.md#customer-architecture-browser-composition) distinguishes reusable customer generation/reading capability from RigorLoop’s own generated reference documentation. The [requirement analysis](../../requirements/published-products.md#customer-architecture-browser-analysis) proposes the supporting requirement refinements. This browser remains the current repository implementation; no customer package, command or publication is established by these drafts.

The [first-project adoption](../modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#rigorloop-as-the-first-supported-project) makes this repository the primary user of the same packaged generator supplied to customers. Build and qualify that candidate, invoke its public boundary with this project's immutable source selection, and retain `design/architecture/views/browser/` as the explicitly chosen reading output. Until the replacement is implemented and qualified, the current Python generation instructions above remain accurate. The target wrapper will delegate to the packaged tool; no separate repository browser engine or generic template framework is required.


## Customer browser design views

[The composition](../README.md#customer-architecture-browser-composition) maps customer Scenarios and cross-parent responsibilities. [MOD-004's owning design](../modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md) contains the Logical cooperation, proposed Process topology/sequence, publication lifecycle, Development resources and Physical placement. Generated views project allocations and proposed facets. Source-owned D2 topics are explicitly registered by the owning Module and compiled into the same browser; readers execute no diagram source code and arbitrary Markdown is not scraped for diagrams.

The selected customer walkthroughs SCN-083–087 are explained in the composition. The current browser's five existing selected Scenario profiles remain unchanged; record details and source links are available without claiming new generated outcome coverage. A generated view is a reading surface, not a separate approval record or implemented customer product.

## Scope and view navigation

[System Summary](browser/index.html#home) provides system orientation. Select the RigorLoop root or a Module in the vertical architecture tree, then use the horizontal Summary and five view links. Tree selection preserves the active view; view selection preserves scope. [Logical](browser/index.html#overview) retains its published fragment. Use sequence diagrams for ordered exchanges between responsible participants, flowcharts for decisions, and state diagrams for established transitions. Keep each interaction focused on one path, use plain-language messages, and explain material exceptions beside it. Process details combine projected and registered diagrams under Runtime topology, Interactions, and State and coordination; empty conditional groups are omitted. Public capabilities are shown for command/skill catalogues and explicit web bindings supplied by the selected model. Cooperation and acceptance contributions remain reachable from relevant Module and requirement context, with their existing fragments preserved.

[MOD-004 Process](browser/index.html#process/MOD-004) displays the registered generation topology, generation sequence and publication/recovery state diagram inline, with “On this page” controls for moving among them. [Change control Process](browser/index.html#process/MOD-006) shows Resume and coordinate work. Its Parent composition links the MOD-017 sequences [Review and verify the completed change](browser/index.html#process/MOD-017/proposed/sequence/whole-change-review-and-correction) and [Correct and reassess](browser/index.html#process/MOD-017/proposed/sequence/correct-and-reassess). Existing flowchart fragments still open the corresponding current sequence.

[The owning reading contract](../modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#integrated-browser-reading) defines registration, qualifications and source identity. A missing Module view remains an explicit scoped gap; related stakeholder Scenario links are requirement-derived context, not inferred execution or satisfaction.

Module Process pages also link registered topics from their immediate parent under Parent composition, when available. The link retains the parent's owner and opens the same diagram; containment supplies reading context without asserting the child's participation. A child's missing Process realization stays visible even when parent context exists.

[Skills and commands Process](browser/index.html#process/MOD-018) presents the target **Record a handoff update** and **Discover a saved update after a lost response** sequences. [Work record storage Process](browser/index.html#process/MOD-011) presents **Inspect after an interrupted update** and **SQLite transaction outcomes**, with parent links to those recording sequences. [Work record storage Physical](browser/index.html#physical/MOD-011) presents **Target operational storage placement** for the direct SQLite v4 backend. These five D2 diagrams are authored once in the owning Module READMEs and registered into this browser. The existing observed Publication/Recovery flows and v3 physical placement remain available with their original qualification; they do not describe adoption of the target or simultaneous authoritative stores.

## Architecture browser capability

The Public capabilities navigation includes [Architecture browser](browser/index.html#capability/architecture-browser), alongside Commands and Skills. Its page explains current reading behavior, access, limitations and engineering basis, then links to the existing architecture views. “Technical design” opens [MOD-004 Logical](browser/index.html#logical/MOD-004), where Browser technical structure follows the responsibility overview. “Development design” opens [MOD-004 Development](browser/index.html#development/MOD-004), where the inline [Browser software organization](browser/index.html#development/MOD-004/proposed/topology/browser-software-organization) explains the target source-unit and package-resource dependencies. The owning source distinguishes that target from the current Python implementation; package production remains separately owned by MOD-013. The owning MOD-004 README supplies its descriptions through `browser-capability.toml`; the projection preserves source identities and offline text. The broader customer generator and distribution remain proposed. Missing bindings produce no web entry, and an entry does not add another architecture view.

## Inline diagram reading

Module realization pages adapt to their available content. [MOD-009 Development](browser/index.html#development/MOD-009) shows the scoped absence of recorded detail. [MOD-006 Process](browser/index.html#process/MOD-006) displays its one Resume and coordinate work graph directly. [MOD-004 Development](browser/index.html#development/MOD-004) displays software organization, file/package containment and build/artifact graphs with section navigation. [MOD-004 Process](browser/index.html#process/MOD-004) presents three concern-ordered graphs with section navigation. Each graph retains its qualification, independent Zoom/Fit controls and expanded link. Section jumps preserve the current route; expanded pages return to the same Module and view. Sources are collapsed below the graphs, and parent-owned diagrams remain attributed links. The system overview retains its composition and scoped navigation.

The Logical page presents responsibilities and technical components/contracts. The Development page leads with source/package organization and its rationale. [MOD-004 Development](browser/index.html#development/MOD-004) keeps the software-organization, file/package and build/artifact diagrams visible and places the existing Python and web-resource mapping in collapsed **Implementation references** below the design content. Expand it to read source links and current limitations. The table comes from the owning Module README; it is not separately authored in the browser. Design remains independent of whether implementation mappings exist.

[MOD-004 Development](browser/index.html#development/MOD-004) also presents **Build and resources** after the Development diagrams. This source-owned design table explains the engine, profiles, offline resources and renderer, and links to the package-production contract. Product packaging and runtime customer snapshot generation retain their distinct owners and view concerns. Implementation references stay collapsed below the design.

The [software graph](browser/index.html#development/MOD-004/proposed/topology/browser-software-organization) explains the Rust crate’s internal source units, CLI adapter source, reusable template sources and data-contract resources. The [file and package graph](browser/index.html#development/MOD-004/proposed/topology/browser-file-organization) identifies intended authored sources, bundled resources and generated package/website outputs; the owning design supplies its text tree. The [build and artifacts graph](browser/index.html#development/MOD-004/proposed/topology/browser-build-packaging) distinguishes MOD-013’s reusable CLI candidate from MOD-004’s project website assembly. The website contains platform and project data, which may be embedded together in offline HTML. Execution order and recovery remain in Process.

The [Generation sequence](browser/index.html#process/MOD-004/proposed/sequence/generation-sequence) shows how those components cooperate over time: interpret the model, project browser data, render diagrams, check data/template compatibility, assemble the website and publish. A separate later reading phase loads the embedded template and data without contacting the generator. Development explains structure and the data contract; Process explains ordering and failure handoffs; Physical explains where the generator, artifacts and reader run.

The [reusable template reading design](../modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#reusable-template-reading-design) maps the page shell, navigation/search, view presentation, diagram controls and source disclosure to their internal browser-data inputs. RigorLoop's real pages are the primary reading example; a small independent model such as Harbor Library supplements them to expose accidental project assumptions. A universal presentation schema and a comprehensive second project are deferred.

The [technology decision](../modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#technology-decision) selects the existing Node CLI as a thin adapter, one Rust browser engine, bundled D2 and the plain HTML/CSS/JavaScript reader. MOD-004 Logical shows their component/contract structure and technology annotations; Development shows source/build relationships; Process shows their execution boundaries and recovery outcomes. This is the target design. The Python commands above remain the working repository generator until the packaged replacement is qualified.

The [browser technical model](../modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#technical-model-browser-components-and-contracts) owns component responsibilities, Module mappings, data/artifact authority and linked contracts. [MOD-004 Logical](browser/index.html#logical/MOD-004) shows its [Technical structure](browser/index.html#logical/MOD-004/proposed/topology/browser-technical-structure) inline after the collaboration overview, with section jumps and the existing zoom/expanded controls. Modules without a registered technical topic retain their existing overview. The Development diagrams and their published links remain source/build perspectives of that same design; no extra view tab or authored model copy is introduced.

[Work record storage Logical](browser/index.html#logical/MOD-011) adds **Current record relationships**; [Development](browser/index.html#development/MOD-011) adds **SQLite software organization**. Its Process page also presents **Create a coherent backup** and **Restore an authorized snapshot**. These source-owned D2 views explain the schema, selected binding and explicit maintenance separately from ordinary Change transactions. They describe target behavior, not implemented SQLite support.

The [Review recording sequence](browser/index.html#process/MOD-018/proposed/sequence/record-review-assessment) is under Skills and commands → Process. Its owning [request/result walkthrough](../modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/README.md#review-recording-walkthrough) explains the public CLI and typed storage boundary with one complete example; it does not introduce another page or operational record.
