# Scenario-derived parent-boundary contracts

The user authorized the proposed Scenario → collaboration → Interface → child-responsibility analysis. This slice starts with SCN-019 and applies the same method to SCN-053 and SCN-066. It defines the selected cross-parent interactions and preserves their ordinary, incomplete, and failure distinctions. It does not claim complete architecture coverage, implementation, approval, or satisfied requirements.

## Scope and sequence

1. Inspect the Scenarios, applicable SRs/Functions, parent/child responsibilities, and existing Interfaces. Compare reuse, refinement, and a new cohesive contract before allocating a new identity.
2. Refine REM's consumer-driven Interface analysis method without requiring one Interface per Module or child.
3. Define IF-007 Engineering state content and interpretation under MOD-016 for MOD-005; IF-008 Applicable engineering authoring guidance under MOD-017 for MOD-012; IF-009 Applicable governed-action authority and IF-010 Claim evidence applicability and coverage under MOD-017 for MOD-015. Author each provider and consumer once on its Module. Preserve existing Interface identities, operations, and participation.
4. Explain contributing child responsibilities through current Function allocations and explicit Module prose. Preserve requirement parentage, Scenario black-box content, and all Function/AR allocations. Attribute the bounded derivation in Interface/Module sources and the source register.
5. Generate Logical and Scenario participation views from actual relationships. Extend the selected Scenario views to SCN-019, SCN-053, and SCN-066 with their relevant selected contracts. Keep per-Scenario contract selection explicit so adding a Governance Interface cannot make it appear applicable to every descendant Scenario. Contract owners outside the allocated Modules are context, not inferred executing participants.
6. Reconcile current indexes and counts, run focused schema/model/projection checks, compare preservation against the snapshot, and independently review the complete authored contracts and generated result. No skills, CI, runtime migration, release, or commit is requested.

## Contract boundaries and retained gaps

IF-007 supplies content and interpretation for an explicitly selected state and membership. It composes existing definition access and interpretation rather than exposing IF-001/IF-002 wholesale. It reports actual acquisition completeness, conflicts, historical rules, and external-reference limits. Reading coherent material does not establish durable Baseline retention: MOD-005 retains Baseline identity, membership, applicable authority, retention confirmation, and resulting claims. Detailed retention/change-authorization cooperation remains explicit later work; no new snapshot transaction or storage mechanism is invented.

IF-008 covers the adopted model-authoring branch of specialist guidance: selection and explanation of applicable canonical guidance. MOD-008 retains the semantic guidance contribution; MOD-012 retains published invocation, specialist execution/handoff, and output responsibilities. This contract does not turn all published skills into an implementation of one generic authoring procedure.

IF-009 supplies applicable authority information and disposition without creating approval or executing the requested governed action. IF-010 assesses evidence applicability, criterion coverage, contradictions, and the supported scoped judgment without executing verification or qualifying/releasing a product. These are separate contracts because valid authority cannot replace evidence and favorable evidence cannot grant authority. MOD-015 retains exact candidate identity, release qualification, sealing, publication, and actual outcome reporting. Existing IF-005 artifact supply and IF-006 installation contracts retain their scope.

## Verification allocation

Independent semantic review will assess each new contract against the selected Scenario, SR outcomes, child contributions, and existing contracts. Structural checks cover schema shape, unique identity/provider/operation names, typed provider/consumer/source references, naming, and preserved allocation. Projection regressions cover the expanded Scenario set, per-Scenario contract scope, exact provider context, no invented execution/ownership, and continued independent descendant-exposure support. Preserve original selected Scenario outcomes and all 44 CLI contribution arguments.

Direct schema/model and view suites, renderer generation/read-only checking, local links/anchors, graph-source checks, whitespace checks, and snapshot comparison provide bounded evidence. Canonical contract prose and source context remain subject to engineering judgment; tests do not prove semantic adequacy or runtime satisfaction.

## Result

Completed this bounded design slice on 2026-09-28. Four draft Interfaces add explicit consumer-facing contracts without changing the existing six Interfaces:

| Interface | Sole provider | Exact consumer | Established contract scope |
| --- | --- | --- | --- |
| IF-007 | MOD-016 | MOD-005 | Selected-state content and original interpretation for SCN-019 inspection |
| IF-008 | MOD-017 | MOD-012 | Applicable adopted-REM authoring guidance for SCN-053 |
| IF-009 | MOD-017 | MOD-015 | Applicable governed-action authority for SCN-066 |
| IF-010 | MOD-017 | MOD-015 | Claim evidence applicability and coverage for SCN-066 |

Twelve Module records now declare the exact provider/consumer relationships, explain child contributions, or narrow their remaining design limits. REM documents consumer-driven Scenario analysis, cohesive contract scope, independent authority/evidence concerns, and bounded per-Scenario view selection. The current model contains 273 entities, including 19 Modules and ten Interfaces, with 14 realization facets and 15 schemas. Function and AR ownership remains unchanged.

The Logical overview now shows six parent-boundary Interfaces. Scenario views select IF-007 for SCN-019, IF-003/IF-004 for SCN-046 and SCN-047, IF-008 for SCN-053, and IF-005/IF-009/IF-010 for SCN-066. Exact consumer/provider relationships and ancestor-owned contract context remain distinct from Function participation. Original Scenario outcomes and all 44 CLI contribution arguments are preserved. Process, Development, and Physical views differ from the preceding snapshot only in source identity.

Direct checks actually run:

```text
python3 tests/engineering/validation/architecture_schema_tests.py       26 passed
python3 tests/engineering/validation/system_design_schema_tests.py     18 passed
python3 tests/engineering/validation/architecture_view_tests.py         17 passed
python3 scripts/render-rem-architecture-views.py                       generated five views
python3 scripts/render-rem-architecture-views.py --check               passed
git diff --check                                                      passed
```

Additional direct inspection checked 42 current design/REM/supporting Markdown files, 3,463 local links and 377 Markdown anchors; 11 Mermaid graph sources with 150 edges; and 68 balanced disclosures with unique HTML identities. These checks passed. Scoped whitespace and final-newline checks passed for all 39 changed/new files. These are source checks; browser rendering was not exercised.

Snapshot comparison covered 351 files. Exactly twelve existing JSON records changed, all Modules, and four Interface records were added. Requirement, Feature, Scenario, Function and AR content; the original six Interfaces; all realization facets and schemas; existing Module identity, state ownership and scope; previous responsibility/source entries; prior supporting review records; and the user's two architecture archives remain preserved. Current documentation and indexes agree with the canonical records.

Independent whole-subject review assessed the new contracts against Scenario/SR outcomes, existing Release clauses, child responsibilities, preservation, REM rules, renderer, regression assertions, generated views, and final current documentation. One documentation wording finding was corrected: the view index now describes SR `confirms` references to Functions rather than implying confirmed Function lifecycle status. The reviewer confirmed closure; no findings remain for this bounded subject.

Generated source identity:

```text
043cb645a5577f9555dc436ec626055a2f3368bb4c7edc228aca80829eb4ad10
```

Whole working-subject identity:

```text
d0954b18ef60415544a690a665208ced12339d03cca04bf8f6c20bb025191711
```

The whole subject is the 347 files selected by all `design/**/*.json`, `design/**/*.md`, and `rem/**/*.md`, plus the renderer and three test files in the command list above. Its SHA-256 input is the sorted repository-relative POSIX path, NUL, the lowercase hexadecimal SHA-256 of that file's working bytes, and newline for each file. This supporting record and the archives are excluded. The generated source identity uses only the entity and realization inputs defined by the renderer.

Inspection does not establish durable Baseline retention. Retention confirmation, wider specialist/release collaborations, remaining AR derivation, physical realization, and runtime satisfaction remain explicitly outside this result. No skills, CI, runtime migration, release, or commit was performed. This record provides scoped design and validation evidence; it does not replace workflow approval or requirement-satisfaction evidence.
