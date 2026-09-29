# Bounded 4+1 architecture projection

This supporting record covers the user-authorized manual REM refactor. It is not a workflow approval, runtime verification, or baseline closeout. Existing review records retain their original subjects.

## Scope and sequence

Apply the [REM Architecture Views method](../../../rem/methods/architecture-views.md) to the current working model. Produce a whole-model Logical overview and bounded CLI Process, Development, Physical, and Scenario views. SCN-046 (coherent publication) and SCN-047 (explicit interrupted-update recovery) are the selected +1 examples.

1. Preserve the current working material and identify the canonical projection inputs and omissions.
2. Add a repository-local deterministic renderer for the five views, retaining the existing CLI acceptance-contribution arguments. Read canonical JSON and derive inverse relationships and requirement containment; keep the derived index ephemeral.
3. Reconcile view navigation and the application profile. Keep existing supporting perspectives and historical review subjects intact.
4. Check regeneration, drift detection, invalid-reference rejection, provenance, and preservation of canonical inputs. Independently review the generated perspectives against the owning records, correct findings, and record the actual result here.

## Projection contract and verification allocation

`python3 scripts/render-rem-architecture-views.py` writes only `logical.md`, `process.md`, `development.md`, `physical.md`, and `scenarios.md` under `design/architecture/views/`. `--root PATH` selects an explicit repository root; the default is the script's repository. `--check` compares expected output without writing and fails on drift. Load and resolve inputs before any output write. This is authoring support for the bounded draft profile, not a published CLI capability or a general architecture interpreter.

Projection uses stable IDs, typed declared relationships, containment-derived requirement parentage, and linked owner/facet fields. Output order and source identity are deterministic; input identity includes working-file contents instead of relying only on a Git revision. Preserve observed/proposed/deferred distinctions. Keep subordinate facets subordinate. Views and their renderer do not define architecture facts.

The Logical view includes all Modules and declared Interface participation, with Function/AR ownership and state authority available as detail. Its existing `cli-acceptance-contributions` anchor and all 44 SR-owned contribution arguments must survive. The other views cover the two CLI Modules and two Interfaces with populated realization. The Scenario view follows `informs` to SRs, SR-confirmed Functions and contained ARs to accountable Modules; this is a participation slice, not proof that every related Function executes in the Scenario. No internal sequence is inferred solely from graph reachability. Existing black-box Scenario records remain unchanged.

Direct checks cover repeatable generation, read-only drift detection, changed canonical input reflected in output, and rejection of missing or wrong-type references before writes. Compare canonical JSON and schemas with the saved pre-work snapshot. Inspect local links, generated diagram structure, and whitespace. Independent review covers cross-view meaning, source qualification, missing topology, recovery outcomes, and the absence of invented execution order. No CI or product runtime tests are required for this scoped authoring task.

## Preservation and recovery

Pre-work copies and path/content hashes of `design/` and `rem/` were captured before edits. The 331-file manifest has SHA-256 `d3cd35405b9aba3cf1914450a79a779646cffe80c5d881ee0c6b18951977f3d2`. The temporary copy supports this working-session preservation check; it is not a durable engineering baseline. Restore only files changed by this task; do not reset unrelated working changes. New generated pages and the renderer can be removed independently if the projection is withdrawn. Existing canonical entities, schemas, Scenarios, and historical reviews retain their meaning and bytes unless a separately justified correction is recorded.

## Result

Implemented the bounded renderer and all five projections. The Logical view covers 15 Modules, six Interfaces, Function/AR allocations, and all 44 SR-owned contribution arguments. Process and Physical use readable attributed observation tables; Development shows shared source units; the two Scenario views retain stakeholder outcomes, exercised Feature provenance, exact participation paths, and source-owned Interface guarantees. Internal execution order is not inferred from relationship reachability.

The view index, architecture/model navigation, application profile, and REM method now explain source-state identity, regeneration, declared scope, and the limits of participation graphs. Link checking also corrected two existing Scenario Analysis anchors in REM's knowledge-reconstruction navigation. Existing supporting views and historical review records remain in place.

Executed directly:

```bash
python3 scripts/render-rem-architecture-views.py
python3 scripts/render-rem-architecture-views.py --check
python3 tests/engineering/validation/architecture_view_tests.py
```

Generation and final drift checking passed. The seven focused tests passed in the final run (15.402 seconds), covering repeatability, exactly five output targets, canonical and unrelated-file preservation, read-only missing/edited-output detection, changed names/allocations, missing/wrong-type references, unsupported vocabulary, supported obsolete Scenarios and deliberate allocation gaps, and shared software responsibilities. The contribution check preserves every one of the 44 canonical basis arguments.

Independent semantic and implementation review found no remaining material issue in the final renderer and five outputs. Review retained pure preview versus fresh guarded execution, fitting receipts before publication, exact verified recovery, foreign-state protection, committed-outcome preservation, and external-editor limitations. Corrections during review added supported obsolete/unallocated handling and Feature provenance, and replaced prose-heavy metadata diagrams with clearer tables. The assessed renderer SHA-256 is `1bc48290f2bf60103a97091cf01c805a0ea7ce55d7da1abcc2db9cde573c4cef`.

The final canonical input identity is `08df459bb762beba985a397451cf6289c9c3e0b3008e91a835308dc71c8f467e`, covering 265 entity records and 14 realization facets. A separate preservation comparison found all 294 canonical JSON/schema files byte-identical to the pre-work snapshot. Local Markdown checking passed 2,608 paths/anchors across 42 pages; four Mermaid blocks passed node/edge structural checks and all detail tags balanced. This is structural diagram inspection, not an executed visual-rendering check.

The combined seven-file renderer/test/output subject has SHA-256 `9df1815f00965cda31693dd6d07ac337b18dd19109df98ea4092c6f4c8365b0b`. Its input is the sorted repository-relative paths for the renderer, direct test file, and five generated pages, each followed by NUL, the file's SHA-256, and newline. This identifies the checked projection artifacts; it does not retarget earlier model reviews.

No CI, skill invocation, application runtime verification, or public-tool integration was performed. The generated Process/Development/Physical scope remains the bounded CLI example; remaining realization, structured runtime/deployment topology, platform qualification, and product conformance retain their owning deferrals. No requirement, allocation, Scenario lifecycle, or architectural decision was changed by generation.
