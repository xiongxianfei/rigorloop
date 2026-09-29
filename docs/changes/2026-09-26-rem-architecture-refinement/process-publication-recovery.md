# Process View: record publication and recovery

The user selected the next Process View refinement: explain record publication and interruption recovery for SCN-046 and SCN-047. This work expands the existing runtime overview with selected interactions and coordination/lifecycle presentations from owner-contained realization facts.

## Contract and sequence

1. Inspect the retained CLI publication, bounded-receipt, exclusion and recovery contracts and their current implementation. Preserve prior source observations and distinguish this inspection from executed verification.
2. Record the minimum typed runtime interaction and transaction-lifecycle facts in the accountable architecture facets. Keep local participants, steps and states subordinate to those owners. Scenario selection supplies analysis context; it cannot establish runtime order. Preserve logical allocations, Interface providers and requirement/Scenario definitions.
3. Generate meaningful, linked publication/recovery interactions and coordination diagrams alongside the runtime overview. Preserve preview, no-change, prepublication rejection, interruption, committed-state recovery restrictions and safe-stop outcomes. Keep detailed behavior and its limitations readable in both browser and text projections.
4. Check the new closed structures and reference semantics before generation, generated diagrams and safe output handling, and actual browser navigation and readability. Independently review the complete bounded change and compare against the pre-task snapshot.

## Verification allocation

Schema checks protect shape and vocabulary boundaries. Projection checks reject unresolved participants, incompatible Module/Interface references, malformed step/state transitions and unsupported structures before output writes. Positive projection assertions preserve conditional paths and source qualification. Real D2 compilation and browser checks cover selected diagrams, links, keyboard navigation and readable desktop/mobile presentation. Snapshot comparison protects unrelated manual-refactor work, REM knowledge, canonical logical facts and previous supporting evidence.

No skills, CI, product record mutations, build/install/release/publication, or commit are included. Runtime source inspection and rendered-view tests do not establish requirement satisfaction or filesystem durability.

## Result and evidence

Completed on 2026-09-28. The [Process browser](../../../design/architecture/views/browser/index.html#process) now offers the runtime overview plus three focused presentations:

- [Record publication](../../../design/architecture/views/browser/index.html#process/interaction/publication): nine ordered main steps, a three-step terminal preview alternative, and an unchanged alternative. Receipt preparation precedes journal creation and authoritative replacement; private lock/epoch effects remain distinct from authoritative mutation.
- [Record recovery](../../../design/architecture/views/browser/index.html#process/interaction/recovery): eight ordered completion steps and a three-step terminal restoration alternative. Recovery verifies exact retained identities, rejects unknown states, and cannot restore a committed journal.
- [Journal coordination](../../../design/architecture/views/browser/index.html#process/lifecycle/coordination): three descriptive states and four guarded transitions. Physical journal absence is distinct from the only stored phases, prepared and committed; lock/read gates and uncertain outcomes remain explicit.

IF-003's interaction facet owns the two source-observed sequences. MOD-011's runtime facet owns the journal lifecycle. The existing interaction/runtime schemas now admit their closed subordinate structures. Local step/state names introduce no independent engineering entity. Participant types and contract boundaries, operation names, declared step participants, local-name uniqueness, and transition endpoints are checked before rendering. A parent-owned Interface may execute through a contributing child without changing its exact provider or inventing an executing parent.

The source inventory adds SRC-RECORD-PROCESS. All seven inspected implementation/contract files were checked unchanged against revision `33f56fe84ff730d7bd48900cef32170fd0682412`. Earlier facet observations and their source entries remain intact. Fresh inspection establishes the new ordered account; regeneration itself does not reinspect implementation or qualify behavior.

The browser now has 47 diagrams, including the three additions. Process pages provide meaningful step/participant names, explicit terminal branches, source details, failures, guarded transitions, and cross-page navigation. Interactions open at a readable scale; narrow screens begin on the first step, with scrolling and Fit available. Additional canonical interactions without selected diagrams remain readable in facet detail. The [generated text](../../../design/architecture/views/process.md) retains the complete steps, alternatives, failures, guards, effects, and provenance.

Canonical source digest: `de0a0bf421ebacc3053cb88ff18d8c9ef5af45524113b7143c414bda84592f1a`. Final browser HTML SHA-256: `8a8a41937674d4a49a64392bae228d6c8403ad4b8af4d7e80c308d0b2bcc8bcf`. These identify the inspected model/presentation, not a product execution result.

## Validation and independent review

| Actual check | Result |
| --- | --- |
| `python3 tests/engineering/validation/architecture_schema_tests.py` | All 42 tests passed, including independent interaction/lifecycle shape tests. The two new tests failed before schema support and passed afterward. |
| `python3 tests/engineering/validation/architecture_view_tests.py` | All 31 tests passed. New cases protect malformed structures, incompatible/undeclared participants, unknown operation/state references, duplicate names/transitions, no-write rejection, and parent-provider versus child-execution semantics. |
| `REM_D2=/tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 python3 tests/engineering/validation/architecture_browser_tests.py` | All ten tests passed with the real compiler. New graph assertions protect receipt-before-publication order, independent terminal branches, exact lifecycle transitions, source pointers, and omission when typed facts are absent. Existing escaping, output preservation, standalone routes, drift, and retirement checks passed for all 47 diagrams. |
| `python3 scripts/render-rem-architecture-views.py --check` | Current; no writes. |
| `python3 scripts/render-rem-architecture-browser.py --d2 /tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 --check` | Browser and all 47 diagrams current; no writes. |
| Python compilation, `node --check scripts/resources/rem-architecture-browser/viewer.js`, scoped authored-file whitespace, and `git diff --check` | Passed. |

Actual Chromium verification of the final HTML passed 208 assertions across seven Process routes and three topics at 1440 × 1000 and 390 × 844. It checked all canonical steps, terminal branches, outcomes, failures, guards, source links, navigation/current-page state, disclosure contents, readable scale/Fit, pointer/focus/Escape, browser Back and keyboard Enter. No JavaScript/console errors, HTTP requests, or horizontal page overflow occurred. Publication, recovery, coordination, and narrow-screen screenshots were inspected. A separate injected valid third-sequence fixture established that ungraphed interactions retain all their readable details without modifying the canonical model.

A complete cross-view browser check also passed 360 existing routes, five Scenario walkthroughs, two production mappings, 361 distinct source paths, and 6,615 links at desktop/mobile sizes, with no errors or HTTP requests. Previous realization diagrams were compared under the same model and remain byte-identical; only the three selected diagrams were added.

Independent review identified and resolved two issues: the participant profile initially required the exact provider while validation allowed contributing descendants, and the browser initially hid additional ungraphed interactions when a field contained graphed entries. The profile/test now preserve logical ownership versus execution; detail rendering replaces only covered array entries. Independent Chromium readback confirmed an additional interaction remains accessible. A separate entrypoint check exposed the new helper import under audited `runpy`; explicit script-path resolution restored that supported invocation, and the no-skill-content audit passed. Final whole-task review and the subsequent narrow-screen centering review reported no remaining findings.

## Preservation and limits

Comparison against the 464-file pre-task snapshot confirms all 304 protected REM documents, canonical logical entities, and earlier supporting records remain byte-for-byte unchanged. No snapshotted file was deleted. The source inventory is append-only, and all prior values in the two extended facets are preserved. The model retains 273 entities, 779 logical relationships, 21 realization facets, the same five Scenario selections, and unchanged Function/AR allocation and Interface ownership.

This work reconstructs and presents bounded publication/recovery source behavior. Installation, package production, release runtime, and broader Process completeness remain outside its scope. Known external-edit timing and platform/durability limits remain explicit; no source diagram demonstrates requirement satisfaction, successful record mutation, or recovery execution. No skills, CI, product record mutation, build, installation, release, publication, or commit were performed. Changes remain in the existing manual-refactor workspace.
