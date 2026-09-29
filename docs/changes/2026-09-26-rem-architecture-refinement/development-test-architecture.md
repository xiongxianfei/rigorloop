# Development View: test architecture

The user authorized refining REM and the generated Development View to include the test system. This bounded change records static test organization and dependencies; it does not execute CI, qualify the product, alter test execution, or complete broader software-dependency reconstruction. Skills are excluded by instruction.

## Design and execution plan

1. Extend REM's Development View and realization guidance to include test groups, assessed responsibilities, observation boundaries, fixtures, execution dependencies and required artifacts. Retain the distinction between implementation, assessment mechanisms and observed evidence.
2. Reconstruct bounded CLI, Records, Installation and Packaging test groups from retained owning contracts and current sources. Store attributed groups under each assessed Module's software realization, separately from implementation units. Shared execution tooling retains its Validation contract owner; absent REM allocation is a visible gap, not an invented Module responsibility.
3. Extend the self-contained software schema and shared semantic validation. Require meaningful group names, existing contained repository paths, source attribution, coverage contracts, execution ownership, observation boundaries and limits. Do not mirror a test-method inventory or create new first-class engineering entities.
4. Generate a readable Development test perspective with clickable subject and source navigation, grouped dependency diagrams and progressive detail. Existing five views and source qualifications remain available. No authored Markdown view or compatibility presentation is added.
5. Validate schema and semantic failure handling, source-derived projection, determinism, stale-output checks and actual desktop/mobile browser navigation. Independently review the final bounded change and record evidence.

## Verification allocation and recovery

Use the existing architecture schema, model/projection and browser test entrypoints directly. Add focused negative coverage for malformed groups and unresolved sources/references, and browser checks for the distinction between tested responsibility and implementation ownership. Run only affected checks; do not run CI or the mapped product suites. Test discovery and source inspection describe available mechanisms, not sufficient coverage or passing execution.

Before editing, preserve working bytes in the session-local snapshot identified by `/tmp/rem-development-tests-snapshot`; compare the finished change against that snapshot so prior manual-refactor work and historical evidence remain intact. Changes remain uncommitted unless separately requested. No removals are planned.

## Result and evidence

REM now explicitly includes test organization in the Development concern and distinguishes assessed responsibility, implementation ownership, shared execution ownership, Verification and Evidence. The application profile adds attributed `observed.test_groups` to the existing self-contained software schema. Nine bounded groups cover command admission/reading, diagnostics, recording interactions, stored-record invariants, publication/recovery, verified acquisition, replacement, archive production and packed-consumer composition.

The model preserves the groups as subordinate observations with exact source pointers, without adding logical relationships or changing allocations. Shape, attribution, names, duplicate references and local-file resolution are validated before rendering. Empty optional fixture/selection/artifact lists remain supported. Artifact prerequisites are descriptions rather than assertions of existing files or successful production. The shared execution owner remains the retained Validation contract; its unresolved REM allocation is visible instead of being assigned to MOD-007.

Source inspection corrected two initial mapping descriptions before final generation: v3 adoption cases exercise public mutation/recovery and belong with that boundary; adapter archive installation smoke uses a source-copied CLI candidate and must remain distinct from emitted npm tarball consumption. No mapped product test suite was executed to make these static observations.

| Command or inspection | Actual result |
| --- | --- |
| `python3 tests/engineering/validation/architecture_schema_tests.py` | 48 tests passed in 4.453 seconds. Three new cases cover closed test-group shapes, required references and meaningful text; existing schema protection remains. |
| `python3 tests/engineering/validation/architecture_view_tests.py` | 36 tests passed in 110.654 seconds. Four new cases cover subject/source fidelity without logical allocation, invalid structures, unsafe/missing dependencies, and qualified optional prerequisites. |
| `REM_D2=/tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 python3 tests/engineering/validation/architecture_browser_tests.py` | 17 tests passed in 32.360 seconds. Three new cases cover separate assessment/execution ownership, no inferred tests when observations are absent, and missing-source rejection before compilation or output writes. |
| `python3 tests/engineering/validation/architecture_schema_tests.py ArchitectureSchemaTests.test_current_realization_facets_conform_and_observations_have_registered_sources` | Passed after the two source-description corrections; final facets retain valid shapes and registered attribution. |
| `python3 scripts/render-rem-product-inventory.py` and `--check` | Generation changed zero inventory bytes; the check also passed against the corrected model. |
| `python3 scripts/render-rem-architecture-browser.py --d2 /tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2` and `--check` | Browser regenerated and the read-only freshness comparison passed for all 55 diagrams. |
| Exact-artifact Chromium inspection | 462 assertions passed for all nine groups and four owner scopes, source/role/artifact/limit details, shared support deduplication, accessible group labels, keyboard/history navigation, preserved routes, and desktop/mobile diagram Fit and scrolling. No JavaScript errors or network requests occurred. |
| Python compilation, `node --check scripts/resources/rem-architecture-browser/viewer.js`, `git diff --check` | Passed. |
| Local navigation checks | All eight test coverage/execution contract targets and their declared fragments resolve; all 322 local link targets in the six edited guidance files resolve. |

The generated browser provides `#development/testing` and four `#development/testing-MOD-*` reading scopes, with five additional diagrams. Test names and assessed responsibilities lead the presentation; detailed paths remain in expandable source sections. The overview derives a shared execution-support index by dependency role and exact path, retaining references to every using group. The two Development perspectives remain implementation mapping and test architecture within the existing five-view structure.

Initial independent review found the design and verification allocation coherent. Fresh independent whole-change review found no actionable issue in the corrected source observations, schema, semantic validator, diagrams, browser navigation/details or negative tests. It verified all nine embedded groups and diagram pointers against canonical facets and all 53 distinct referenced revision/file pairs against their attributed source revisions. Final independent supporting-record readback confirmed the command/probe results, artifact identities, preservation claims and limitations without corrections.

Final source digest: `2cf8f01cf8087e0b226dbd431d6452970b13954a16b84408d91173987708417e`. Final standalone HTML SHA-256: `bd1798aa5eeaedf805d5848aace6a25c449c2272d2ca6c0123a5773e73c62ddf`. The final UI-only polish was checked by the exact-artifact Chromium probe after generation. Probe and results are `/tmp/rem-development-testing-ui-check.cjs` and `/tmp/rem-development-testing-ui-result.json`; screenshots under `/tmp/rem-development-testing-*.png` were visually inspected.

Snapshot comparison confirms that existing software facts, sources, proposals and deferrals are preserved; only the new test groups and their attribution are added. All 50 previously generated SVG diagrams remain byte-identical. The 320 inspected protected logical/requirement/system records, unrelated schemas, AGENTS.md and prior change records remain unchanged. The pre-change working snapshot is `/tmp/rem-development-tests-before-wfjrb8gs`; no files were removed and no branch commit was created.

The 101 focused tests and browser observations support this schema/model/presentation refinement. They do not qualify the mapped product suites, establish complete test-system coverage, resolve the shared runner's REM allocation, or establish requirement satisfaction. Broader software-dependency reconstruction and test Process/Physical details remain outside this bounded pass. No skills, CI, product build, installation, release, external publication or operational-record mutation was performed.
