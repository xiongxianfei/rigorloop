# Architecture views

Open [the architecture browser](browser/index.html) directly in a browser. It includes all five REM views, diagrams, details and source links; no server or network is required.

| View | Reading focus |
| --- | --- |
| [Logical](browser/index.html#overview) | Module responsibilities, hierarchy, Interfaces, allocations, Commands and Skills |
| [Process](browser/index.html#process) | Execution boundaries, publication/recovery interactions, coordination and lifecycle |
| [Development](browser/index.html#development) | Software organization, Interface bindings, product construction and test architecture |
| [Physical](browser/index.html#physical) | Consumer deployment, storage and isolation, production placement |
| [Scenarios](browser/index.html#scenarios) | Stakeholder outcomes, selected obligations and applicable details across the other views |

Logical navigation also provides [CLI cooperation](browser/index.html#cooperation), nine contract walkthroughs, and the 44 [CLI acceptance contributions](browser/index.html#contributions). These explain recorded responsibilities and obligations; they do not establish executed behavior or requirement satisfaction. Names lead the diagrams; exact identities, source paths and qualifications remain available in detail. Use zoom, scrolling and Fit for larger diagrams.

Development includes [Test architecture](browser/index.html#development/testing): bounded CLI, Records, Installation and Packaging groups, their assessed Modules, observation boundaries, fixtures and execution dependencies. Shared execution tooling links to its retained Validation contract; its REM allocation remains unresolved. These source observations describe test organization, not passing results or complete coverage.

The [publication](browser/index.html#scenario/SCN-046) and [recovery](browser/index.html#scenario/SCN-047) Scenario walkthroughs explain each expected, alternative and failure outcome through selected criteria, exact accountable Modules, Interface contracts and relevant Process, Development and Physical details. Their test links provide context rather than asserted outcome coverage. The other selected Scenarios retain their full outcomes and broad traceability, with detailed outcome selections shown as not yet developed. Canonical Scenario records remain unchanged.

## Generate and check

Edit the owning engineering JSON records, then run from the repository root:

```bash
python3 scripts/render-rem-product-inventory.py
python3 scripts/render-rem-architecture-browser.py --d2 /path/to/d2
python3 scripts/render-rem-product-inventory.py --check
python3 scripts/render-rem-architecture-browser.py --d2 /path/to/d2 --check
```

Generation uses D2 0.9.0 with ELK; supply `--d2` or place that version on PATH. Reading the browser needs no compiler. `--root PATH` selects a repository snapshot. Checks compare expected bytes without writing. Reload the browser after regeneration.

`browser/` contains replaceable generated HTML, D2/SVG diagrams and a hash manifest. The shared model/projection lives in `scripts/lib/rem_architecture_model.py`; browser templates and interaction code live in `scripts/resources/rem-architecture-browser/`. The separate inventory generator owns only the marked block in `design/requirements/published-products.md`. Do not hand-edit generated output.

The [REM method](../../../rem/methods/architecture-views.md) defines the concerns; the [application profile](../../support/README.md#four-plus-one-view-projection) defines their repository interpretation. Canonical records own facts and source qualifications. This directory maintains one browser presentation and this reading guide.

The [consolidation record](../../../docs/changes/2026-09-26-rem-architecture-refinement/browser-view-consolidation.md) records validation and the recovery revision for retired Markdown views and their earlier evidence links. Historical subjects retain their original meaning; current generation does not depend on retired files.
