# Coherent initial 4+1 browser

The user authorized a shared, navigable initial 4+1 set covering skills, commands, and product delivery. Existing canonical definitions and source qualifications remain authoritative; the views explain selected architecture and its remaining limits.

## Contract and sequence

1. Use the existing governed Scenarios for baseline inspection, command publication/recovery, specialist guidance, and release. Preserve their black-box definitions, existing participation rules, and exact contract ownership.
2. Inspect current packaging and installation contracts and implementation without invoking skills. Record material source, transformation, output, and placement observations under the accountable production/installation Modules, with attributed revision and unresolved design limits. No build, release, or installation is performed.
3. Derive all five view projections from the same identified model. Reuse facet discovery and Scenario traversal for Markdown and browser generation; preserve observed/proposed/deferred distinctions and exact ownership. Projection must include new material facets without claiming unmodeled runtime sequences or placements.
4. Provide browser navigation for Logical, Process, Development, Physical, and Scenarios, with readable summaries, owner/source links, cross-view navigation, and explicit coverage limits. Retain existing names-first Logical diagrams, command/skill entry routes, identity lookup, and keyboard navigation.
5. Extend focused checks for new projection/navigation contracts and inspect the actual browser at desktop and mobile sizes. Run relevant schema, projection, browser-generation, drift, documentation, and source-preservation checks; independently review the final result. No skills, CI, publication, installation, or commit are requested.

## Result

Completed on 2026-09-28 as a bounded initial projection, without changing entity allocations, contract ownership, or canonical Scenario definitions.

The [offline browser](../../../design/architecture/views/browser/index.html) now provides Logical, Process, Development, Physical, and Scenario navigation. Owner pages and public command/skill entries link to applicable realization views. Observed facts, proposed choices, deferred decisions, and source attribution remain distinguishable. The [view guide](../../../design/architecture/views/README.md) documents regeneration.

`Model.architecture_views()` supplies the same discovered facet selections and Scenario slices to the Markdown renderer and embedded browser model. The model contains 273 entities and 21 realization facets: Process selects six runtime/interaction facets, Development selects nine software/representation/technology facets, and Physical selects six deployment/persistence facets. The five Scenario selections remain SCN-019, SCN-046, SCN-047, SCN-053, and SCN-066. Behavioral allocation, selected contract-provider context, and ancestry remain distinct.

Six new facets record bounded observations: MOD-013 software/deployment; MOD-014 software/runtime/deployment; and IF-006 interaction. MOD-013's software facet records skill archive production and CLI candidate composition as source inputs, transformation implementation, and candidate output layouts. The additive `observed.production_paths` software-schema field describes these subordinate observations without adding entities or build evidence. Candidate output templates are displayed as text, while inspected source paths are navigable. MOD-019 remains IF-006's sole provider; MOD-014 retains the installation behavior.

All generated views identify canonical source digest `508f099d79bac63b9c6837fda6fae271e62c41267706a2bd778a53030c60387d`. This identifies the working model bytes, not a committed repository Baseline or implementation qualification. Source observations retain the inspected revision `33f56fe84ff730d7bd48900cef32170fd0682412` under `SRC-PRODUCT-REALIZATION` in the [source register](../../../design/requirements/sources.md#src-product-realization).

## Validation and review

The focused checks actually run were:

| Check | Result |
| --- | --- |
| `python3 tests/engineering/validation/architecture_schema_tests.py` | 38 tests passed, including attributed production mapping and current facet conformance |
| `python3 tests/engineering/validation/architecture_view_tests.py` | 25 tests passed, including shared selections, new facet discovery, production paths, and Scenario scope; final targeted Scenario scope check also passed |
| `REM_D2=/tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 python3 tests/engineering/validation/architecture_browser_tests.py` | All seven tests passed with D2 0.9.0, including composed generation, labels, escaping, and drift behavior |
| `node --check scripts/resources/rem-architecture-browser/viewer.js` | Passed |
| Both renderer generation commands in the view guide | Succeeded |
| Both renderer `--check` commands, using the pinned D2 compiler for the browser | Passed without writes |
| `git diff --check` and scoped new-file whitespace checks | Passed |

An initial browser-suite invocation without `REM_D2` passed five tests and skipped two compiler-dependent cases. The subsequent explicit-compiler invocation above ran all seven; the skipped run is not the composed-generation evidence.

Actual Chromium checks used temporary Playwright tooling against the generated local HTML at 1440 × 1100 and 390 × 844. They exercised 359 entity, public-entry, view, and owner routes; five Scenario walkthroughs; both production paths; cross-view keyboard navigation and browser back navigation; source links; and candidate-output presentation. The final run checked 361 distinct source paths and 5,986 rendered links, with no page/console errors, external HTTP requests, or horizontal page overflow. Separate Logical regression checks covered all 20 diagrams, 43 visible Interface labels, and 37 expanded collaboration entries, with no label overlaps. Existing identity lookup, focus/hover behavior, zoom/Fit, and mouse/keyboard contract navigation passed. Desktop and mobile screenshots were inspected for readability.

Independent review found one accessibility issue: cross-view links lost the destination view in their accessible names. The correction retains Process/Development/Physical in both accessible names and identity tooltips; scoped navigation marks the current section while exact pages retain their page marker. Final browser assertions verified this correction. Independent source, model, projection, and presentation review then reported no remaining findings in this bounded change.

## Preservation and remaining limits

A 407-file pre-task snapshot comparison found no missing files or unexpected protected changes. All 18 REM documents, 11 earlier supporting records, and 244 requirement/system JSON files remain byte-for-byte unchanged. Existing entity edits are limited to MOD-013/MOD-014 design limits and appended source attribution. Their earlier provenance remains intact; the existing source register is preserved as a prefix. The only existing schema changed is the software realization schema. Twelve inspected production/installation source and contract files still match the attributed repository revision. Local documentation checks covered 3,048 paths, 580 anchors, 29 browser routes, and 19 skill-path existence checks with no errors; skill contents were not read.

The records retain two material implementation qualifications. The default `build-adapters.py` branch still calls `sync_adapter_output` without `--check` or `--output-dir`, contrary to Packaging DIST-SR-22; only the explicit-output production path is mapped here, and implementation correction remains separate. Installer `/proc/self/fd` and same-filesystem assumptions still require applicable platform proof. Existing CLI JavaScript is packaged with candidate metadata; no command-code generation from REM is claimed.

Complete specialist cooperation, unrecorded runtime/deployment details, executable outcome coverage, and build/install/release qualification remain with their owners. No skills, CI, product builds, installations, publication, or commits were performed for this task.
