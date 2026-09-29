# Physical View: deployment, storage and production placement

The user authorized refinement of the Physical View around consumer deployment, storage and isolation, and production placement. The existing graph is a qualified placement inventory; this work makes the physical relationships and distinct contexts understandable without inventing hosts, deployment outcomes or connections from directory names.

## Contract and sequence

1. Inspect the retained CLI, Installation, Packaging and relevant realization contracts and source. Reuse the existing package, runtime and placement facts; preserve their earlier provenance. Record fresh source inspection separately from actual deployment or product execution evidence.
2. Add minimal typed, owner-contained physical facts and references where needed. Distinguish package artifacts, execution environments, filesystem locations, persistent data and external acquisition sources. Preserve logical ownership, allocation and Module containment. Explicitly qualify unmodeled agent hosting, distribution availability and platform guarantees.
3. Generate a meaningful Physical overview with consumer deployment, storage/isolation and producer placement presentations. Keep exact paths and constraints in readable drilldown. Preserve existing owner routes and all other architecture views; render only relationships supported by canonical facts, with exact source pointers.
4. Check the closed authoring shapes, scoped references and projection semantics before writes; compile the diagrams; inspect browser navigation/readability on desktop and mobile; independently review the complete bounded change and compare against its pre-task snapshot.

## Verification allocation

Schema cases protect required context and reference shapes and reject unknown vocabulary. Projection cases protect physical reference resolution, context separation, ownership versus placement, missing facts, and rejection before output writes. Generator cases exercise meaningful names, explicit connections, source pointers, standalone navigation and deterministic safe generation. Actual browser checks cover complete canonical detail, graph/readability controls, existing navigation and added perspectives. Snapshot comparison protects unrelated manual-refactor work, REM knowledge, canonical logical entities and previous evidence.

No skills, CI, product record mutations, build/install/release/publication, or commit are included. Changes describe and present architecture; they do not qualify product artifacts or alter runtime behavior.

## Result and evidence

Completed on 2026-09-28 against inspected implementation commit `33f56fe84ff730d7bd48900cef32170fd0682412` and the existing uncommitted architecture model. Six existing realization facets now record one package/execution binding with five participant-specific storage accesses, two alternative archive sources, three producer placement roles, and four location constraints. The nine named placements retain their owner-scoped identity. References resolve exact placement or execution names; matching directory labels do not create connections or identify hosts.

The [browser](../../../design/architecture/views/browser/index.html#physical) has a compact Physical overview and three focused presentations: [Consumer deployment](../../../design/architecture/views/browser/index.html#physical/consumer), [Storage and isolation](../../../design/architecture/views/browser/index.html#physical/storage), and [Production placement](../../../design/architecture/views/browser/index.html#physical/production). Source details retain every access purpose and condition, acquisition qualification, isolation rule, source pointer, and unprojected fact. Existing owner routes remain available; IF-006 displays the Consumer diagram as explicitly labeled context. Exact paths remain in drilldown. The [Markdown projection](../../../design/architecture/views/physical.md) contains the same canonical facts.

Generated identity:

- Source digest: `18f886c6124d4381e2a20441f8c7d1911d3849db9f4bb66e14f20ae92858df58` over 273 engineering entities and 21 realization facets. The 779 logical relationships are unchanged.
- Standalone browser SHA-256: `b93cd8826d01826056c59254b2c4048ac92b6e8ffb51e401dfc9584f4cfd9d06`.
- 50 compiled diagrams; the Physical overview is refined and three Physical topic diagrams are added. The existing Process and Physical owner diagrams remain byte-identical when projected from the same current model.

Focused validation actually run:

| Command or inspection | Result |
| --- | --- |
| `python3 tests/engineering/validation/architecture_schema_tests.py` | 45 tests passed, including closed shapes, source requirements and unknown vocabulary. |
| `python3 tests/engineering/validation/architecture_view_tests.py` | 34 tests passed, including exact context/reference resolution, qualification retention and rejection before writes. |
| `REM_D2=/tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 python3 tests/engineering/validation/architecture_browser_tests.py` | 12 tests passed with D2 0.9.0, including explicit access actors, alternative inputs, placement roles and absence of inferred connections. |
| `python3 scripts/render-rem-architecture-views.py --check` | All five architecture views, Logical text reference and skill inventory current. |
| `python3 scripts/render-rem-architecture-browser.py --check --d2 /tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2` | Browser and all 50 diagrams current. |
| Python compilation, `node --check scripts/resources/rem-architecture-browser/viewer.js`, and whitespace checks | Passed. |
| Actual Chromium Physical inspection on the final standalone HTML | 443 assertions passed across nine Physical routes and three Process regression topics, at 1440-pixel desktop and 390-pixel mobile widths. Complete details, typed links, source paths, keyboard/pointer navigation, history, Fit/readable zoom and visible initial graph labels checked. No JavaScript/console errors, network requests or page overflow. |
| Separate unprojected-detail browser fixture | Additional placement and binding entries retained, including every access purpose, condition and binding constraint. |
| Actual Chromium five-view navigation inspection | 361 routes, five scenario walkthroughs, two production paths, 361 distinct source paths and 6,690 page links checked. No errors, network requests or page overflow. |
| Diagram compilation and screenshot inspection | All four Physical overview/topic diagrams compiled; desktop/mobile screenshots inspected. Text bounding-box checks found no overlapping graph labels. |

The first full projection run exposed an outdated test fixture that deleted the optional runtime while retaining newly authored references to it. The fixture now removes those references before deleting their target, preserving the intended optional-discovery test and strict referential integrity. The complete rerun passed. Browser inspection also found the missing IF-006 owner diagram context; the final artifact includes the contextual diagram and passed the rerun.

Temporary browser probes and their outputs were `/tmp/rem-physical-topic-ui-check.cjs`, `/tmp/rem-physical-topic-ui-result.json`, `/tmp/rigorloop-five-view-check.cjs`, and `/tmp/rigorloop-five-view-result.json`. These paths are session-local inspection aids; the commands, scope, identities and outcomes above are the durable evidence record.

Independent read-only review found no actionable issue in the source claims, schema/profile, validation, graph semantics, detail preservation, tests or final IF-006 context change. Review checked all 101 generated manifest members and all 29 Physical diagram source pointers. The final record received a separate readback.

Preservation was checked against the 472-file pre-task snapshot at `/tmp/rigorloop-physical-refinement-y7j0d67p`: no baseline file was removed; all 308 protected REM files, requirement JSON, system files, logical Module/Interface records and earlier change records were byte-identical. All prior values in the six edited facets were retained; the source registry change is append-only. No unrelated manual-refactor work was reverted.

These results validate the architecture records and their presentation. They do not establish deployed hosts, current release availability, installed product behavior, a connection from candidate output to a consumer archive, or general filesystem/platform safety. Skills and CI were not run; no product build, installation, release, publication, operational-record mutation or commit was performed.
