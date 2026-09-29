# Graphs for every architecture view

The user identified that only Logical had browser graphs. The earlier five-view browser added navigation and qualified detail pages, but left the other four graphical projections incomplete. This correction supplies graphs for those existing views within the recorded architecture scope.

## Contract and sequence

1. Preserve all existing logical entities, allocations, Interface providers, Scenarios, REM documents, and historical records. Add only the minimum source-attributed structured realization facts needed to project runtime and physical placement without parsing prose or inventing topology.
2. Generate Process execution structure, Development software/production mappings, Physical placement, and Scenario participation graphs from canonical facts and the existing selected Scenario slices. Distinguish execution participation from logical Interface accountability, candidate output from produced artifacts, and Scenario relevance from execution order. Keep local realization handles subordinate to their owners.
3. Render those graphs before detail cards with readable names, contextual links, legends, source attribution, keyboard navigation, and zoom/Fit. Preserve the existing Logical diagrams and all public-entry routes. Use focused graphs where complete inventories would obscure the concern.
4. Validate structural shapes and typed references, semantic projection and source qualification, safe generation/drift behavior, and actual browser rendering at desktop and mobile sizes. Record independent review and preservation evidence. No skills, CI, product execution, publication, or commit are included.

## Verification allocation

Schema checks protect the new closed realization shapes. Model/projection checks reject missing or incompatible references and distinguish runtime participants from contract providers. Browser-generator checks exercise the new graph families, source links, escaping, standalone navigation, and drift/failure handling. Actual browser checks establish that every view has a rendered graph, intended graph links work, and labels/navigation remain usable without network access. Source comparison protects unrelated manual-refactor work and prior records.

## Result

Completed on 2026-09-28. The offline browser now embeds 44 diagrams: the existing 20 Logical diagrams plus four Process, nine Development, five Physical, and six Scenario diagrams. Every view has a landing graph; focused graphs explain selected owners and all five existing Scenario walkthroughs. The [view guide](../../../design/architecture/views/README.md) documents regeneration and navigation.

The canonical model still contains 273 entities, 779 logical relationships, and 21 realization facets. Five existing facets gained source-qualified structure: one shared CLI `execution` under MOD-010 runtime, and seven `placements` across MOD-010 deployment, MOD-011 persistence, MOD-013 deployment, and MOD-014 deployment. Three existing facet schemas gained the corresponding closed shapes. The model validates participating types, entry/provider compatibility, conditional call endpoints, declared consumption, provider ancestry, and accountable placement ownership before rendering.

Process arrows come only from explicitly recorded conditional calls; IF-006 retains MOD-019 as its logical provider while MOD-014 is its recorded execution endpoint. Physical groups derive from named locations and path templates, with no inferred transfer edges or separate-machine claims. Development shows observed software units, Interface bindings, MOD-012's 19 published procedure source paths, and MOD-013's two production mappings. Catalog paths do not infer Function realization; candidate templates link to owning detail pages, not purported output artifacts. Development's shared facet selection now includes interaction facets with concrete bindings so the diagram and text details cover the same source mappings.

Scenario graphs reuse the five existing participation slices. Requirement/behavior sets collapse by exact accountable Module; separately styled contract context retains exact providers and consumers. These are traceability graphs, not ordered runtime diagrams. Names lead the presentation; source pointers, local node meaning, and destination identity remain available through links and accessible labels.

Generated source digest: `3faac0f95e495d9f93a5d240831c44829bafab82fec4dc19538a29715135f65a`. This identifies the working canonical model, not execution or publication evidence. The renderer continues to compile with D2 0.9.0/ELK, embeds all SVGs for offline use, and supports safe retirement and standalone navigation for the additional diagram families.

## Validation and review

| Actual check | Result |
| --- | --- |
| `python3 tests/engineering/validation/architecture_schema_tests.py` | 40 tests passed, including two new closed execution/placement shape tests; the new cases failed before schema support and passed after it |
| `python3 tests/engineering/validation/architecture_view_tests.py` | Final integrated run: all 28 tests passed, including malformed structure/reference rejection before writes, runtime/provider distinction, and placement rendering |
| `REM_D2=/tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 python3 tests/engineering/validation/architecture_browser_tests.py` | All nine tests passed with the real compiler; all 44 diagrams, Scenario aggregation, procedure/source mappings, standalone routes, escaping, drift, obsolete-file handling, and failure preservation covered |
| `python3 scripts/render-rem-architecture-views.py --check` | Current, no writes |
| `python3 scripts/render-rem-architecture-browser.py --d2 /tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 --check` | Browser and all 44 diagrams current, no writes |
| Python compilation, `node --check scripts/resources/rem-architecture-browser/viewer.js`, scoped authored-file whitespace, and `git diff --check` | Passed |

Actual Chromium checks at 1440 × 1100 and 390 × 844 covered all 24 new graph scopes, 216 SVG links, and 437 text-label spans. There were no detected label overlaps, page/console errors, or external HTTP requests. Every new graph initially fits its stage; zoom/Fit and keyboard links work. A separate complete browser pass exercised 360 routes, 361 distinct source paths, and 6,572 rendered links without missing destinations or horizontal page overflow. The existing 20 Logical diagrams separately passed 43 visible Interface-label and 37 collaboration-list checks, identity lookup, pointer/focus navigation, and zoom/Fit. Desktop/mobile screenshots of the new views and focused production/release graphs were inspected.

Review corrected three presentation problems: parallel Process labels initially overlapped; the initial shared zoom policy cropped the new graph scopes; and subordinate graph nodes lost their own accessible meaning when sharing an owner route. Labels now separate cleanly, new graphs initially Fit a larger responsive stage, and each accessible name retains its own node text/role before its destination context. Browser checks assert distinct source-node names and focus tooltips. Scenario caption wording was also corrected to describe the actual traceability details rather than nonexistent relationship tables. Independent final review and a separate narrow Chromium accessibility readback reported no remaining findings in this bounded subject.

## Preservation and limits

Comparison with the 414-file pre-task snapshot preserves all 303 prior REM documents, canonical entities, and supporting records byte-for-byte. Requirement/Scenario/system definitions, Function and AR allocations, Module containment, Interface providers/consumers, and the five Scenario selections remain unchanged. Existing logical graph generation retains its meaning. New execution and placement data inherit the existing source inspection qualifications; skill file contents were not read.

Independent documentation checking found no broken local links, anchors, or browser routes in the changed guides and generated Markdown; skill references were checked for existence only. The completed evidence record's links and whitespace were checked separately after its results were recorded.

Graphical coverage remains bounded by recorded facts. Fitted overviews summarize scope; zoom, scrolling, and focused pages expose small labels and complete detail. Empty or missing topology is not evidence of architectural independence, and no diagram establishes a build, runtime outcome, installed artifact, platform guarantee, or satisfied requirement. Existing production/installation conformance gaps remain recorded with their owners. No skills, CI, product execution, installation, publication, or commit were performed.
