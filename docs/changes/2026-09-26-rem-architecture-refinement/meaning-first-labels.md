# Meaning first in architecture labels

The user requested less prominent internal numbering after reviewing the named Interface diagrams. Names should explain responsibilities and contracts; stable identifiers should remain available for traceability without occupying every box and connection.

## Contract and sequence

Apply the REM Architecture Views presentation boundary. Preserve canonical JSON, semantic projection, ownership, references, and earlier records. Refine the existing REM clarity/view guidance rather than adding another entity or identity convention.

1. Display Module names and meaningful Interface names in diagrams. Shorten the two existing titles beginning with `Applicable` through exact presentation substitutions, keeping other titles intact. Disambiguate any resulting collisions instead of silently conflating contracts.
2. Use names for overview navigation, cards, and Interface lists. Keep canonical titles and IDs in entity details, search, hover, and keyboard-focus information. Continue routing by stable identity. Presentation labels do not rename canonical entities.
3. Adapt the existing SVG-generation assertion to check visible meaning, secondary identity, and unchanged links. Regenerate the browser; exercise desktop/mobile reading, hover/focus, search by both name and ID, and contract navigation. Inspect rendered labels for collisions.
4. Run focused browser tests, generator currentness, JavaScript syntax, and changed-prose checks. Independently review the final delta and preserve the previous model/evidence snapshot. No skills, CI, or commit are requested.

## Result

REM Principles 16 and 19 and the Architecture Views readability method now place engineering meaning first and keep stable identity accessible as supporting information. The browser uses names in diagrams, navigation, cards, and Interface lists. The two agreed shorter labels remain mapped to canonical titles; conflicting abbreviations restore the full title, and identical canonical titles retain secondary IDs to distinguish their links. Entity pages and search results retain identifiers. Hover and keyboard-focus tooltips expose full canonical names and IDs, with Escape dismissal. The renderer supplies Interface SVG title metadata because D2 0.9.0 omits connection tooltips.

Focused proof:

- `REM_D2=/tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 python3 tests/engineering/validation/architecture_browser_tests.py`: all seven tests passed in 14.877 seconds. Actual generated SVG checks cover meaningful labels, identity metadata, preserved links, changed canonical titles, abbreviation collisions, and duplicate canonical titles alongside the existing escaping and drift protections.
- `python3 scripts/render-rem-architecture-browser.py --d2 /tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2 --check`: browser and all 20 diagrams current.
- Actual local HTML inspection used Chromium 151.0.7922.34 through Playwright 1.63.0. Across 20 diagram routes, all 43 Interface connection labels retained meaningful names and all 37 expanded Interface-list entries retained their full canonical names and owner context. No routine IDs appeared in the overview's visible diagram, cards, list, or navigation. After font loading, text-bound checks found zero Interface-to-Interface or Interface-to-Module label collisions.
- Mouse and keyboard contract navigation, canonical-name/short-name/ID searches, zoom/Fit, mobile lists, and hover/focus identity information passed. A review found that a lingering mouse hover could override a newly focused link's tooltip. The correction makes the latest pointer/focus trigger authoritative; the final browser probe verifies the tooltip and accessibility description move to the newly focused link. Focus-triggered scrolling also preserves the tooltip, and Escape dismisses it.
- Desktop and 390-pixel mobile screenshots were inspected. No page overflow, browser errors, or HTTP requests were observed. `node --check scripts/resources/rem-architecture-browser/viewer.js`, changed-prose validation, and `git diff --check` passed.

Independent review confirmed the tooltip correction on the regenerated browser and found no remaining blocking findings in the presentation or REM changes.

The 312 snapshotted canonical JSON and earlier supporting-record files are unchanged. The embedded engineering model is identical to the prior browser's model; its source digest remains `cd1103ca2bc52ed35fdae20f6f9643e15ba1e7dbe4507a1045be6ba62907ad9f`. Earlier evidence retains its original subject. These observations cover the current generated model in the inspected Chromium environment, not every future model or browser. No skills, CI, or commit were run.
