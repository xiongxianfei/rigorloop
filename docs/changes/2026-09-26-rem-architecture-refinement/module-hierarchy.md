# Hierarchical Module architecture migration

This record covers the user-authorized manual application of the refined REM Module hierarchy and encapsulation rules. It is a bounded design-model and authoring-tool migration, not product implementation, workflow approval, or runtime verification. Earlier reviews keep their original subjects and conclusions.

## Scope and sequence

1. Preserve the current working model and review the refined containment/exposure contract.
2. Define MOD-016 Engineering model management, MOD-017 Engineering governance, MOD-018 Engineering operations, and MOD-019 Product delivery as genuine broader responsibilities. Move MOD-001–004, MOD-005–009, MOD-010–012, and MOD-013–015 respectively into their parent's `modules/` collection, preserving child identities, definitions, allocations, and realization content.
3. Adopt filesystem-derived Module parentage and Interface-owned `exposed_through` references in Operational Support. Expose IF-004 through MOD-018 for its established public caller boundary and IF-006 through MOD-019 for its consumer MOD-010; retain the original providers.
4. Update recursive discovery, structural/semantic checks, and the derived 4+1 Architecture View Graph. Generate the Logical view from the highest useful Module level, with expandable children and source-qualified descendant allocation summaries.
5. Reconcile current navigation, inspect representative Scenarios and ownership, run focused checks, and independently review the migrated model and tooling. Record actual findings/results here. No CI, skills, release, or commit is requested.

## Representation and validation contract

Modules use `architecture/modules/<owner>/module.json`, recursively followed only through `<owner>/modules/<child>/module.json`. Each owner may contain its existing `realization/`. Physical containment is the sole authored parent fact; `parent_module` and duplicate `children` lists are not introduced. Top-level Modules form a forest beneath the system boundary. Every nested collection must have a valid enclosing Module, identities remain globally unique, and unsupported JSON placement is rejected instead of skipped. No universal depth limit is added. Interfaces remain in the existing shared collection.

An Interface may have a nonempty unique `exposed_through` array of Module IDs, omitted when no exposure is declared. Each target must be a strict ancestor of its one provider. Every provider-side ancestor between the provider and an exposed boundary must also expose the Interface. For each declared consumer outside a provider ancestor's subtree, that ancestor must appear in the exposure set. Consumer ancestry does not itself require exposure. Deliberate exposure for an external actor is allowed without inventing a Module consumer. Parent exposure never adds a provider or changes the Interface identity.

Keep Function and AR `allocated_to` unchanged unless an independently justified responsibility change requires correction. A parent can own a genuinely broader obligation, but descendant display does not author another allocation. Derived totals use unique IDs and distinguish direct versus descendant ownership. Realization facets remain owned by their original Module; shared processes, packages, and files do not change logical containment.

The renderer remains a bounded repository authoring command, with deterministic UTF-8 output, exact-byte read-only `--check`, and no writes until all input/reference/exposure checks pass. Its derived graph represents containment, exposure, exact allocations, and source provenance. A collapsed view retains exact provider/consumer attribution for boundary Interfaces and hides descendant-internal collaboration by default. Drilling into a parent reveals children, internal and exposed Interfaces, and allocation/state details. Scenario ancestry is context, not another executing participant. Missing architecture stays explicit.

## Verification allocation and preservation

Independent positive/negative fixtures cover recursive layout, malformed/orphan/duplicate owners, exposure shape and typed references, non-ancestor targets, skipped intermediate exposure, and valid sibling versus cross-tree collaboration. Renderer tests exercise parent overview/drill-down, direct/descendant allocation separation, exact Interface attribution, supported deeper nesting, deterministic regeneration, and rejection without output mutation. Existing source-preservation, single-owner, Scenario, and schema checks remain applicable.

Run the focused requirement, system-design, architecture-schema, and architecture-view suites directly, plus renderer `--check`, local path/anchor inspection, scoped whitespace checks, and a canonical preservation comparison. These checks do not execute the product or prove requirements satisfied. Existing IR-001 walkthrough conclusions and SCN-046/047 publication/recovery obligations must survive the new containment without being retargeted as a new historical approval.

Pre-work copies and hashes were captured for 344 relevant working files; manifest SHA-256: `e067d29d2db9916564395787d82ec743a7d2943c8ec1ce358577ead7cea71c0f`. This temporary snapshot supports selective recovery and comparison during this session. Preserve unrelated changes and the user's existing archive files. Source records, names, direct allocations, and facet bytes should remain unchanged except four added parents and IF-004/IF-006 exposure plus attributed derivation. Update current links to moved owners; retain historical review bytes and their original meaning.

## Result

The migration now contains 269 first-class entities: 19 Modules (four parents and 15 children), six Interfaces, and the unchanged requirement/system/Scenario populations. All 63 Functions and 28 ARs retain their exact accountable Modules. The four parents introduce broader compositional responsibilities, with no duplicate allocations, state ownership, or new realization claims. IF-004 exposes through MOD-018 and IF-006 through MOD-019; their providers remain MOD-010 and MOD-014.

Recursive discovery and exposure checks now cover the nested representation. The Logical overview starts with MOD-016–019 and IF-004/006; parent expansion reveals child collaboration. Descendant summaries contain unique IDs with their exact accountable owners: MOD-016 has 14 Functions / 10 ARs, MOD-017 19 / 0, MOD-018 16 / 18, and MOD-019 14 / 0. These are derived summaries, not parent allocations. Scenario ancestry remains context; all 44 CLI acceptance-contribution arguments and the selected publication/recovery outcomes retain their source meaning.

The following commands ran successfully:

```bash
python3 tests/engineering/validation/requirement_schema_tests.py
python3 tests/engineering/validation/system_design_schema_tests.py
python3 tests/engineering/validation/architecture_schema_tests.py
python3 tests/engineering/validation/architecture_view_tests.py
python3 scripts/render-rem-architecture-views.py
python3 scripts/render-rem-architecture-views.py --check
git diff --check
```

The four suites passed 13, 18, 26, and 11 tests respectively: 68 tests. Coverage includes owner layout and identity, nested hierarchy, typed and continuous exposure, cross-boundary consumers, unchanged direct ownership, deeper nesting, derived summaries, deterministic output, and rejection without output mutation. The renderer's read-only check confirmed all five generated pages match their current canonical inputs. A direct local scan checked 3,113 links, including 138 Markdown anchors, across the 42 current REM/design Markdown files and this record. All targets resolved. The eight generated Mermaid graph blocks have distinct declared node identifiers and resolved edge endpoints; expandable-detail tags are balanced. This checks diagram source structure, not visual browser rendering. Whitespace and final-newline inspection also passed across the complete subject, including untracked files.

An independent preservation audit verified the pre-work snapshot and all 25 moved paths. Of 294 preexisting design JSON files, 291 remain byte-identical at their retained or moved paths. Only the Interface schema and IF-004/IF-006 changed; removing their declared exposure and one appended `SRC-MODULE-HIERARCHY` attribution per Interface reproduces each original object. Only MOD-016–019 add entity identities. All 14 realization facets, 63 Function allocations, 28 AR allocations, two earlier supporting records, 18 REM files, and both user archives remain unchanged. Current navigation follows the moved owners; historical review subjects and conclusions were preserved.

Independent read-only review found no actionable issue in the scoped contract, four parent definitions, canonical migration, Interface exposure, renderer, focused test assertions, or generated views. It independently reproduced the model source identity and descendant counts, checked exact provider/consumer attribution, and confirmed that CLI contribution arguments and Interface guarantees survive the projection. Documentation review found one incomplete relationship-ownership table: it omitted `exposed_through` and its optionality. The table now identifies strict provider ancestors, continuous exposure, and omission when no exposure is declared. Independent rereview closed the finding with no remaining issues in the reviewed scope. This establishes bounded model/projection consistency, not runtime conformance or requirement satisfaction.

Canonical view source identity: `1020bbbc4f13e88cc9f7ff97023187b3a96f7790e254ed17442363ee33deac88`, covering 269 entity records and 14 realization facets.

Working subject identity: `ab8602c4e95cf10ccb8f1556069919a4dafaa9d98efac5d8fe9cb6d9f0d58b21`. It covers 344 files: all 298 `design/**/*.json`, 23 `design/**/*.md`, 18 `rem/**/*.md`, the renderer, and the four test files named above. Compute SHA-256 over each sorted repository-relative path, NUL, the lowercase hexadecimal SHA-256 of that file's bytes, and newline. This record and the preserved archives are excluded. The identity records the current uncommitted subject without replacing earlier review identities.

The broader architecture remains draft. Deferred cross-group Interfaces, remaining AR derivation (including IR-009/IR-010), and realization outside the bounded CLI example still need their own design and evidence. No skills, CI, product-runtime checks, release, or commit ran for this refinement.
