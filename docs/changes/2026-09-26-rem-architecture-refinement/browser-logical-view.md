# Clickable browser Logical view

The user identified the generated Logical page as unreadable and selected a browser with clickable navigation. The 2,788-line, 366,008-byte page mixed architectural context with 114 disclosures and full reference inventories. Earlier structural validation did not establish rendered usability. This slice provides a focused reading surface while retaining the detailed reference and canonical engineering meaning.

## Contract and sequence

1. Preserve the current working sources, prior supporting records, and user archives. No skills, CI, product runtime changes, or commit are authorized for this slice.
2. Generate one overview of the four parent Modules, one focused diagram per Module, and separate command and skill catalogs. A Module route exposes its immediate children and relevant declared collaborations. Exact providers, consumers, allocations, source qualifications, and recorded limits remain discoverable.
3. Keep canonical JSON authoritative. Generate browser navigation and D2 diagram sources from the existing validated projection model; D2 0.9.0 with ELK performs layout. The generated HTML embeds its data, CSS, JavaScript, and SVGs and works offline without installing a viewer or running a server.
4. Make logical.md a small navigation page and retain the full projection as logical-reference.md. Preserve existing Module, public-catalog, and CLI-contribution anchors. Refine REM's presentation method and the local application profile without prescribing D2 as a REM requirement.
5. Validate projection semantics and failure-before-write behavior with focused tests, then inspect and exercise the actual rendered browser. Independently review the finished subject and compare the initial snapshot. Do not infer architectural completeness or requirement satisfaction from a working viewer.

## Verification allocation

Focused model checks protect the four-parent overview and five recorded cross-parent Interface contributions; parent-owned contracts remain on parent boundaries, and child Function/AR allocations remain exact. Public catalog views preserve 40 command names, 19 skill names, proposed contribution roles, and incomplete specialist mappings. Unknown mapping vocabulary continues to fail in the shared model before consistency resolution.

Generator checks protect offline embedding and escaping, deterministic output, read-only drift detection, source changes reaching projections, invalid-model rejection before writes, and compiler failure before publication. Diagram source and SVG are generated artifacts; authored UI assets are maintained in scripts/resources/rem-architecture-browser/.

Rendered checks cover overview legibility, Module and Interface diagram links, child and parent navigation, browser history, catalog filtering and entry detail, source links, missing routes, mobile overflow, and console/page errors. Rendered inspection complements structural assertions. Snapshot comparison protects canonical JSON, schemas, all earlier supporting records, and archives.

## Result

The [offline browser](../../../design/architecture/views/browser/index.html) is generated with twenty linked SVG diagrams: one four-parent overview and nineteen Module scopes. Interface pages preserve all ten exact contracts. Separate searchable catalogs cover forty commands and nineteen skills, with entry detail linking proposed Function contributions, exact accountable Modules, Features, contracts, and mapping limits. Entity pages also expose the remaining requirement and system records. Canonical JSON remains the authority.

The first right-oriented diagrams compressed text excessively; actual SVG inspection also found long edge-label collisions. The final diagrams use downward layout, readable node labels, compact Interface IDs with full-title tooltips, and extra parent-boundary padding. IF-009 and IF-010 retain distinct edges. The overview fits four responsibilities without tiny labels on the inspected desktop. Larger Module diagrams preserve readable scale with scrolling, zoom, and an explicit Fit control. Accessible text lists provide the same collaborations. The browser shows draft/selected-scope qualification and the source-owned design limits.

The prior 2,788-line Logical page is now a 68-line navigation document. The complete projection is retained in [logical-reference.md](../../../design/architecture/views/logical-reference.md), with only its title and introductory navigation changed. Existing Module, catalog, and CLI-contribution anchors remain valid. The other four views and the generated skill inventory are byte-identical to the initial snapshot. REM Principle 19 and the Architecture Views method now require assessment of rendered readability, and the application profile documents this replaceable browser presentation.

Direct checks actually run:

```text
python3 tests/engineering/validation/architecture_view_tests.py
  23 existing cases passed; the new landing case passed after correcting
  an overbroad test assertion. All 24 distinct cases passed.
REM_D2=/path/to/d2 python3 tests/engineering/validation/architecture_browser_tests.py
  6 passed, including real D2 generation and reproducible read-only checks.
python3 tests/engineering/validation/architecture_schema_tests.py \
  ArchitectureSchemaTests.test_current_architecture_and_allocated_requirement_records_conform
  1 passed against the current records and generated-output layout.
python3 scripts/render-rem-architecture-views.py --check
  Passed: five views, Logical reference, and marked skill inventory current.
python3 scripts/render-rem-architecture-browser.py --d2 /path/to/d2 --check
  Passed: browser, twenty D2/SVG diagram pairs, and manifest current.
node --check scripts/resources/rem-architecture-browser/viewer.js
git diff --check
  Passed.
```

The D2 executable used was `/tmp/rigorloop-browser-tools-slmxtuts/d2-v0.9.0/bin/d2`. Its official Linux AMD64 release archive was verified against SHA-256 `5669ddc46b99e942cc96078f4a4e36d5e62103348f4c05179ede27802fdd87a9` before extraction. D2 remains a separate authoring prerequisite and is not downloaded by the renderer. The generated page embeds all its runtime resources; reading it requires no additional dependency.

Actual browser checks used temporary Playwright 1.63.0 with the existing Chromium 151.0.7922.34 executable. All 332 entity/public-entry routes rendered, and all 465 inspected local source-link occurrences resolved. Checks exercised mouse and keyboard diagram links, exact Interface providers/consumers, parent/child navigation, browser back/forward, command and skill filtering, empty results, public-entry accountability, global search, malformed/missing routes, and source navigation. Desktop 1440×1100 and mobile 390×844 checks found no page-wide horizontal overflow, JavaScript/console errors, or HTTP(S) requests. Final layout inspection additionally covered all four parent diagrams, zoom/Fit controls, the IF-004 diagram link, and mobile overview/catalog screenshots. Route assertions waited for hash navigation to render.

Source navigation checks passed across 43 current design/REM/supporting Markdown files: 4,346 local links and 686 Markdown anchors. The eleven retained Mermaid graphs and 139 text-reference disclosures remain structurally valid. All 59 scoped changed/new files passed final-newline and applicable authored-text whitespace checks. Comparison with 358 initial snapshots confirms that all 303 existing design JSON files (273 entities, fifteen facets, fifteen schemas), every earlier supporting record, and both user archives remain byte-identical. No new canonical JSON was introduced.

The generated model source identity remains:

```text
cd1103ca2bc52ed35fdae20f6f9643e15ba1e7dbe4507a1045be6ba62907ad9f
```

The final working subject identity is:

```text
781c504d6f23376bf39367cf4f89b77bdaaac3a638a0ce8b933fddbb793df6b2
```

That identity covers 397 files: all `design/**/*.json`, `design/**/*.md`, and `rem/**/*.md`; every generated file under `design/architecture/views/browser/`; the three authored UI assets; both architecture-view renderers; the browser projection helper; and the four architecture/system schema and projection test files. The SHA-256 input is the sorted repository-relative POSIX path, NUL, lowercase hexadecimal SHA-256 of its working bytes, and newline per file. Supporting records and archives are excluded.

Independent review found no blocking semantic or navigation defects, confirmed unchanged canonical inputs and historical records, and separately exercised 91 browser routes and 225 source-link occurrences. Its small overview-count wording finding was corrected. Final independent readback is complete and clean for the 397-file subject above. The reviewer independently recomputed its identity, ran both renderer checks and all six browser tests, inspected the final overview and Governance screenshots, and confirmed the recorded evidence and limitations. No blocking findings remain.

This evidence establishes bounded presentation, navigation, and generation behavior in the inspected Chromium environment. It does not establish cross-browser qualification, architecture completeness, implementation conformance, requirement satisfaction, or workflow approval. No SKILL.md was read, skill invoked, CI run, product dependency changed, or commit created.
