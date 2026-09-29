# Visible Interface names in the Logical browser

The user found that diagram labels displayed only Interface identifiers, leaving the contract meaning unclear. The previous browser used full titles only in tooltips and collapsed collaboration lists. This correction makes names visible in the ordinary reading path and preserves identifiers for traceability.

## Scope and proof

Apply the REM [Architecture Views method](../../../rem/methods/architecture-views.md#correction-ownership) as a presentation correction. Preserve canonical JSON, exact Interface ownership, Module containment, allocations, and the existing semantic projection. Change generated diagram labels/layout and browser presentation resources; regenerate their outputs. Keep earlier review records unchanged.

1. Require canonical Interface titles and stable identifiers to be visible in generated diagrams without hovering, clicking, or expanding a disclosure. Adapt layout to accommodate meaningful labels.
2. Place a visible, linked Interface list next to the diagram's reading context, with exact provider and selected consumer attribution. Preserve the same scope as the depicted collaborations.
3. Extend the existing real-generation check to inspect visible SVG text, excluding tooltip-only titles. Exercise the actual browser on the overview and Module pages, including narrow displays, Interface navigation, and diagram controls. Review for label collisions and ownership clarity.
4. Run focused checks and independently inspect the result. No skills, CI, canonical-model edits, REM changes, or commit are part of this correction.

## Result

The browser now shows each Interface's full canonical title and stable identifier on its connection. Wrapped labels, white label backgrounds, adjusted diagram spacing, and wider selected leaf Modules where multiple collaborations meet keep the names separate. Each diagram also has an always-expanded, linked Interface list with exact providers and the consumers shown in that diagram. Accessible link names use canonical titles rather than concatenated SVG text fragments.

The existing real-generation test was extended to inspect visible SVG text, excluding tooltips. Before the correction it failed on `module-MOD-002.svg`: IF-001's visible text contained only `IF-001`, omitting `Engineering definition access`.

Focused checks on the corrected output:

- `REM_D2=/tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 python3 tests/engineering/validation/architecture_browser_tests.py`: all six tests passed. This includes real compilation and visible canonical names in all 20 generated diagrams.
- `python3 scripts/render-rem-architecture-browser.py --d2 /tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 --check`: browser and all 20 diagrams current. D2 version: 0.9.0.
- The generated browser was exercised from its local HTML file in Chromium 151.0.7922.34 using Playwright 1.63.0. Across the overview and 19 Module routes, all 43 connection labels contained their full canonical names and all 37 scoped Interface-list entries were expanded. After fonts loaded, text-bound checks found no Interface-to-Interface or Interface-to-Module label collisions.
- Mouse and keyboard navigation reached the named Interface contracts. Zoom and Fit controls worked. Desktop and 390-pixel mobile checks found no page overflow; mobile Interface-list navigation worked. Overview, operations, and mobile screenshots were inspected. No browser errors or HTTP requests were observed.
- `node --check scripts/resources/rem-architecture-browser/viewer.js` and `git diff --check` passed.

Independent review found no blocking semantic or navigation findings. Final review of the selected-leaf layout correction and this evidence record was also clean.

The semantic projection is unchanged, including source digest `cd1103ca2bc52ed35fdae20f6f9643e15ba1e7dbe4507a1045be6ba62907ad9f`. The embedded model matches the pre-correction snapshot exactly. Canonical JSON, REM, and earlier supporting records retain their prior contents. This evidence covers the inspected browser and current generated diagrams; it does not establish readability for arbitrary future models or every browser. No CI, skills, or commit were run for this correction.
