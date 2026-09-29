# Parent Interface contract ownership

The user requested refinement of the distinction between an Interface's accountable provider and the child responsibilities that realize its behavior. This bounded design migration assigns the existing public contracts to their accountable parent Modules. It preserves Interface identity, operation guarantees, consumers, Function/AR allocations, and realization observations. Earlier work records retain their original subjects.

## Contract and sequence

1. Preserve the working model and review contract accountability against the parent and Interface definitions.
2. Clarify REM: `provides` identifies the single Module accountable for the Interface contract. A parent may provide a contract realized through child behavior. Child-provided exposure remains valid when the child actually owns the contract. Implementation location alone does not decide provider ownership.
3. Make MOD-018 the sole provider of IF-004 and MOD-019 the sole provider of IF-006. Remove these entries from MOD-010/MOD-014 and remove the now-inapplicable `exposed_through` fields. Preserve MOD-012's IF-004 consumption and MOD-010's IF-006 consumption. Keep IF-001/002/003/005 ownership and all Function/AR allocations unchanged.
4. Reconcile parent/child responsibility explanations and provenance. MOD-010 continues command admission, dispatch, presentation, and receipt behavior; MOD-011 retains record publication/recovery; MOD-014 retains installation behavior. Existing allocations, definitions, and realization facets explain these contributions without a new duplicate provider, fake child consumption, or invented machine-readable realization relation.
5. Update current navigation and derived views, preserve the established hierarchical disclosure, and keep Scenario parent-contract context distinct from executing behavior. A participant's ancestor-owned Interface may appear as structural contract context from actual `provides` relationships; ancestry alone must not assert that the contract executes in a Scenario. Consumers and provider identities remain exact.
6. Run focused structural/projection checks and independently review the actual model, renderer, tests, and generated pages. Record actual results here. No skills, CI, runtime migration, release, or commit is requested.

## Verification and compatibility

JSON shapes remain unchanged. The provider is authored only through Module `provides`; inverse Interface/provider indexes are derived. Current records gain attributed ownership-refinement sources, while prior source entries retain their historical design meaning. No Interface operation, failure, consistency, or compatibility guarantee changes. No wrapper Interface, new engineering entity, Function/AR owner, or new runtime capability is introduced.

Focused schema/model checks cover single-provider referential integrity and unchanged allocation. Projection checks must demonstrate parent-owned contracts at the top level, preserved child allocations, contextual ancestor contracts without invented executing participants, and accurate counts. Preserve independent descendant-exposure fixtures after the current examples become parent-owned: valid deeper exposure and invalid/missing/skipped boundaries remain supported behavior. A fixture may explicitly select child ownership to test that distinct case rather than assuming it from the current model.

Verify canonical changes against the pre-work snapshot, current Markdown links/anchors, generated-source graph structure, and deterministic read-only rendering. Preserve all historical supporting records and user archives. Review the existing realization prose before claiming that source bindings require edits; unchanged implementation observations must not be rewritten to suggest a different historical implementation.

## Result

MOD-018 now directly provides IF-004, and MOD-019 directly provides IF-006. MOD-010 and MOD-014 retain their behavioral responsibilities, Function/AR allocations, and state authority. Parent and child definitions explain the contribution boundaries explicitly; MOD-011 retains record publication/recovery. IF-004/IF-006 omit `exposed_through`, and no new provider or artificial child consumption was added. The other four Interfaces retain their providers. REM now states the accountable-contract distinction in its model, principle, architecture methods, and view guidance.

The Logical view shows the two parent `provides` relationships and zero current descendant exposures. Hierarchical disclosure and exact allocation summaries remain intact. SCN-046/SCN-047 retain IF-004 and its actual provider in a separate, attributed ancestor-contract context table. The parent receives no invented behavior allocation or execution-graph role. This contextual projection is restricted to the view's declared Interface scope; ancestry does not imply every ancestor contract is applicable or executed.

The following commands ran successfully:

```bash
python3 tests/engineering/validation/architecture_schema_tests.py
python3 tests/engineering/validation/system_design_schema_tests.py
python3 tests/engineering/validation/architecture_view_tests.py
python3 tests/engineering/validation/architecture_view_tests.py ArchitectureViewProjectionTests.test_deeper_hierarchy_and_direct_parent_allocation_are_supported
python3 scripts/render-rem-architecture-views.py
python3 scripts/render-rem-architecture-views.py --check
git diff --check
```

The three suites passed 26, 18, and 16 tests respectively: 60 tests. The targeted rerun passed after strengthening the existing deeper-hierarchy assertion to distinguish child exposure from parent provision. Fixtures explicitly select child-owned contracts to preserve valid and invalid exposure coverage. New projection checks cover exact parent providers, unchanged child allocations/counts, selected ancestor-contract context, and exclusion of an unselected ancestor Interface. These checks do not infer semantic adequacy from counts.

Regeneration refreshed all five source identities. Process, Development, and Physical contents differ only in that digest line; Logical and Scenario projections reflect the scoped ownership refinement. The read-only check confirmed all five outputs are current. Current navigation inspection resolved 3,083 local links, including 337 anchors, across 42 current REM/design Markdown files and this record. The nine architecture-view Mermaid graphs have unique declared nodes and resolving edge endpoints. Changed-file whitespace and final-newline checks passed, including untracked files.

Snapshot comparison confirmed exactly six changed canonical JSON records. IF-004/IF-006 change only by removing exposure and appending the new source attribution; their identities, operation guarantees, consistency/compatibility rules, consumers, and earlier provenance are preserved. All 63 Function records, 28 AR records, 14 realization facets, and 15 schemas remain byte-identical. Earlier supporting records and user archives remain unchanged. The source register explicitly identifies which previous provider/exposure decision is superseded without rewriting its historical basis.

Independent contract review supported genuine parent accountability before migration. Final read-only review assessed the actual six records, five REM refinements, source basis, current indexes/guidance, renderer, test assertions, and generated pages. It found no remaining findings within this ownership scope and independently confirmed preservation, exact providers, selected contract context, and unchanged realization content.

Reviewed identities:

```text
Canonical view source: aa9e469e2b1a62f52019caee9b1e14cbc99a6441514c1751fc2240f2bb11ba07
Renderer: ca18a6da430c9460773b08702533c9d099fe31bf80614b3b023148a0a2eb3cf9
Projection tests: 1a36bafa8e10ca5e18609e5d3d9a4907f842f13ebed1b3e6a59eb4088f202521
Logical view: ef95834ac79ec67c9a9097723a442a374fcab11c492471527c31cfcdb03e7c04
Scenario view: 5b26dde394f140f211cde1a65861df6e4130a8f88aa2e0013dbf28cb12fb0fe8
```

The canonical source still contains 269 entities and 14 realization facets. Working subject identity: `0038b63920b0adbcd3ad29c8c5130ee6cad9bc7776c71256142618e66e438dba`. It covers 318 files: all 298 `design/**/*.json`; the five generated pages; the renderer and projection test; `rem/models/architecture-design.md`, `rem/principles/README.md`, and REM's architecture-design/allocation/views methods; the Architecture/Module/Interface/view READMEs; `design/architecture/views/dependencies.md`; `design/support/README.md`; and `design/requirements/published-products.md` plus `sources.md`. Compute SHA-256 over each sorted repository-relative path, NUL, lowercase hexadecimal file SHA-256, and newline. This record is excluded; earlier subjects are not retargeted.

Browser rendering and runtime conformance were not assessed. Missing cross-parent collaboration contracts, further AR derivation, and IF-006 implementation mapping remain explicit architecture work. No skills, CI, runtime migration, release, or commit ran for this refinement.
