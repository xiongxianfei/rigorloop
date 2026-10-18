# Engineering Validation Model Design

Model validation contract: model-document-v1

## Introduction and Goals

Run a small essential regression suite through ordinary native test runners. The maintainer explicitly selected reduced automated coverage on 2026-10-18. This replaces the custom selector, scheduler, per-case adapters and report-envelope infrastructure. Product behavior, final independent review and distinct Verify remain governed by their existing owners.

## Context and Scope

[System](../architecture/composition.md) owns test quality; this model owns repository commands and execution scope. [Development](development.md#validation) owns contributor practice. Packaging, Installation and Release own their actual artifact and publication checks. Tests cannot grant publication authority.

## Architecture Constraints

The supported routine command is `bash scripts/ci.sh`, without arguments. It executes the same four groups locally, on pull requests and on main. Native runners own discovery, failure output and process exit status. There is no path classification, worker scheduler, report destination, result cache, broad-smoke mode or implicit release-candidate preparation. Removed contributor options fail with a usage error instead of silently narrowing checks.

## Requirements

| ID | Required behavior |
| --- | --- |
| VAL-SR-01 | The direct runner MUST execute the declared essential groups with isolated mutable fixtures and propagate a failed command. |
| VAL-SR-12 | Evidence MUST state actual commands, results, scope and limitations. A selected suite pass MUST NOT claim complete product coverage or hosted CI success. Native runner output is sufficient; custom timing/report schemas are retired. |
| VAL-SR-13 | Removal MUST reconcile actual imports, callers, fixtures, model coverage and generated consumers. The authorized reduction and residual risks MUST remain explicit. |
| VAL-SR-14 | Retained direct test entrypoints MUST discover and execute their declared population without optional hidden cases. Public command/store/archive claims require observations at those real boundaries. |
| VAL-SR-15 | Release qualification MUST retain actual candidate integrity and public observations under Release ownership; routine CI MUST NOT publish or substitute source tests for candidate checks. |
| VAL-SR-16 | Current consumers MUST agree on the smaller suite; historical judgments and customer contracts retain their original meaning. |
| VAL-SR-17 | Tests MUST own temporary state and cleanup, preserve user files, and avoid leaking credentials or private environment data. |
| VAL-SR-18 | Performance claims MUST identify measured scope and environment; fewer cases or lines alone are not a measured speedup. |
| VAL-SR-38 | Complete-suite claims MUST describe only the selected essential suite. Unimplemented model scenarios remain explicit gaps, not inferred coverage. |

The earlier execution/adoption obligations VAL-SR-02–11, 19–37 are retired as mandatory repository mechanisms by the selected minimal-suite policy. This includes exhaustive path admission, canonical check catalogs, worker budgets, per-case isolation adapters, timing JSON and automated complete-model coverage admission. Their original definitions remain in Git at `d7761c8c9c34f0f3a4bb3a74504190e0ceafed53:design/support/validation.md`. Independent product requirements and historical outcomes are not retired by this disposition.

## Solution Strategy

Reuse assertions for high-consequence outcomes, consolidate setup only where useful, and remove test-only infrastructure. Keep model and generation commands available for changes that need them; ordinary CI does not run every validator. No automatic replacement of semantic review with phrase checks is selected.

## Architecture Overview

`ci.sh` invokes native Node tests for workflow, storage/recovery and installation safety, then Python tests for packed installation/archive integrity and skill resources. GitHub CI installs the existing Node dependency and invokes that same command. Release invokes its actual qualification commands and a small release-boundary group. Tests use real temporary stores and archives; no repository-global test result store is introduced.

## Runtime View

Run from the repository root, reject arguments, execute declared groups in order, stop on nonzero exit, and preserve ordinary command output. No hidden path-based selection or success-on-empty discovery is permitted. A missing file is an error. An interrupted command is incomplete evidence.

### Test sources, groups and fixtures

The [system test design](test-design/system-test-design.md) owns scenarios and expected observations; this document owns current executable mappings and coverage gaps. This table locates execution sources.

| Group | Current sources |
| --- | --- |
| Workflow | `packages/rigorloop/test/operational-review.test.js` |
| Storage/recovery | `packages/rigorloop/test/operational-{store,update,maintenance}.test.js` |
| Installation | `packages/rigorloop/test/installer-replacement.test.js`; `tests/engineering/packaging/test-npm-package-publication.py`; `tests/engineering/packaging/test-adapter-distribution.py` |
| Skill integrity | `tests/skill/test-skill-validator.py` |
| Release boundary | `tests/engineering/release/test-release-transaction.py`; existing release validators |

Keep support local and small. Tests may contain an ordered recovery scenario; native runner execution does not require a custom scheduler or a receipt per case. Runtime generators, release scripts and record examples are product inputs and are not deleted merely because they live under scripts or fixtures.

### Proof quality, maintenance and evidence

The selected reduction intentionally removes automatic coverage of exhaustive malformed-input combinations, detailed CLI rendering, legacy import permutations, model/schema validators, documentation wording, browser interaction and rare concurrency/interruption interleavings. These are reduced-assurance areas, not unsupported product features. Changes affecting them must allocate explicit focused tests or concrete manual/review evidence; the essential suite cannot establish their correctness. Preserve high-consequence state, authority and destructive-write assertions in the retained groups. The [system test design](test-design/system-test-design.md) owns stable scenario intent; current missing proof is recorded here.

## Current coverage allocation

This implementation mapping changes when tests, discovery or coverage change. It refers to the stable scenarios in the [system test design](test-design/system-test-design.md); it does not prescribe additional scenarios or record run results.

### Current essential scenarios

| Design outcome | Current execution allocation and limits |
| --- | --- |
| Valid completion — [Workflow][workflow], [Assessment][assessment] | [Workflow tests][workflow-tests]: six cases exercising actual CLI records and transitions. |
| Durable, atomic changes — [CLI][cli], [Records][records] | [Store tests][store-tests] and [update tests][update-tests]. |
| Protected storage — [Records][records] | [Store tests][store-tests]. |
| Recoverable state — [Records][records] | [Maintenance tests][maintenance-tests]. Store/update/maintenance together contain eleven cases. |
| Safe installation — [Installation][installation] | [Installer tests][installer-tests]: three cases with actual filesystem effects. |
| Complete usable artifacts — [Packaging][packaging], [Installation][installation] | [Archive test][archive-tests] and [package tests][package-tests]: three Python cases, including clean installation and a packed-CLI workflow check. |
| Usable skill resources — [Skill procedures][skill] | [Skill tests][skill-tests]: two cases. Archive inventory above supplies the additional packaged-resource observation. |

### Current release scenarios

| Design outcome | Current execution allocation and limits |
| --- | --- |
| Exact publication authority — [Release][release], especially REL-SR-08/12/23 | [Tag identity tests][release-identity] and authority cases in [release execution tests][release-execution]. |
| Honest publication and retry — [Release][release], especially REL-SR-10/14/24 | Executor cases in [release execution tests][release-execution]. Eight cases in total through the [release entrypoint][release-tests]. |

### Current system coverage

| Design outcome | Current execution allocation and limits |
| --- | --- |
| Resumable authorized work — SCN-023/075–081; SR-006/007/027–029/079–082 | Workflow assertions above cover selected record transitions. Actor interpretation, broader handoff variations and semantic harmlessness need an actual-subject walkthrough. |
| Coherent adoption — SCN-082; SR-023/024/055/083 | Proposed integrated activation/migration proof. Retained installation/store checks supply only their listed boundaries. |
| Payload and historical-account preservation — SCN-023/045–047; SR-006/023/024/043–047 | Backup/restore assertions observe selected records and payloads. Full retention/cleanup races, compaction and completion-retry variants remain gaps. |
| Bounded transactional interfaces — SR-040–047/074–077 | Store/update tests cover selected rejection, stale-update and COMMIT-fault cases. Capacity limits, cross-Change cycles, before/after comparison races and complete selector discovery need focused proof when affected. |
| Maintenance and acquired-runtime coherence — SR-043–047/074–077 | Existing maintenance and installed-package cases are partial proof. Rare lease/payload races, legacy import preservation and the full platform qualification matrix remain unproved by routine CI. |
| Explicit obsolete-skill replacement — SCN-063 and [Installation][installation] | Generic conflict, unsafe-path and partial-install assertions remain. The full versioned replacement-profile and actual agent-discovery observations require their own qualified candidate proof. |
| Customer browser and projection — SR-084–088; AR-043–051 | Current structural checks and freshness establish only their explicit boundaries. Full customer/offline/publication, semantic topology and reader-configuration proof remain gaps. |
| Requirement-tree reading — [reading contract][requirement-tree] | Intended reading/assessment observations; the essential suite does not implement this browser coverage. Use independent fixture relationships and actual rendered/offline inspection for affected work. |
| Model custody and authoring — SR-001–005 and MOD-002 | Proposed model-engine behavior and semantic readability require actual boundary proof; operational-store tests do not qualify model custody. |
| Conformance and migration — SR-012–015 | Schema checks cover only declared structures. Actual decoding, graph checks, transformation and consumer compatibility need affected proof. |
| Baselines, transitions and retirement — SR-020–024 | Proposed model custody/recovery and actor interpretation remain separate from retained operational maintenance assertions. |
| Traversal, allocation and potential impact — SR-009–011 | Future composed acquisition, interpretation and analysis proof. Browser/schema counts establish neither complete analysis nor semantic allocation adequacy. |
| Assurance content and methodology — SR-025–029; REM guidance | Workflow and packaging tests cover selected boundaries only. Exact criterion interpretation, semantic preservation and stakeholder effectiveness require accountable actual-subject assessment. |
| Learning and improvement — SR-035–038; IR-007 | Semantic learning/adoption/effectiveness observations remain unautomated. A lesson or adopted version alone cannot establish the direct stakeholder outcome. |
| Selected-subject history — SR-078 | Proposed query/migration/read-only platform qualification; current store tests do not establish this extension's availability. |
| Requirement delivery and evaluation — SR/AR/IR assessment contracts | Former browser/runtime/UI tests are retired. Current structure and freshness checks do not establish these semantic, recovery or accessibility outcomes. |

### Current coverage gaps

The essential suite is intentionally small. For changes affecting the areas below, allocate focused executable proof or a concrete review/operational observation. Missing automation remains a gap; no routine change must rebuild the former catalog before proceeding.

| Area | Significant outcomes not established by the retained suite |
| --- | --- |
| Input, compatibility and presentation | Exhaustive malformed-input permutations, detailed CLI diagnostics/rendering, legacy import/migration variants, all closed-vocabulary boundaries and private-data suppression. Use the affected public boundary and preserved-state/privacy observations when changing these contracts. |
| Skill structure and resources | Every metadata/description boundary, readability vocabulary, resource verb/directory rule, escaped/unlisted paths, shared-resource projection drift and unknown-consumer precedence. Current validation and one missing-resource fault do not prove every negative rule or semantic portability. |
| Specialist operations | All Bugfix write/proof-authority variants; CI assembly selection, concurrent replacement, partial write/retry and bounded PR repair; late invocation/recording triggers. Assess actual authority, original failing-proof identity, preserved newer state and hosted observations for the affected operation. |
| Models and views | The integrated browser/projection/requirement-tree observations above remain unqualified by the essential suite. Structural checks and generated freshness establish only their stated boundaries. |
| Release preparation and qualification | All profile/version-intent partitions, source/tooling identity faults, seal/receipt variants, cheap preflight/discovery failures, remote-tag uncertainty, generated-marker/literal ownership, check-mode no-write behavior, idempotence and interrupted preparation. Qualification must still use the actual candidate and preserve human content and earlier evidence. |
| Publication and reporting | All concurrent attempts, unknown/uncertain remote states and bounded polling, partial assets, public identity conflicts or drift during smoke, authority revocation between writes, lost reporting, neighbor preservation and diagnostic-timing tolerance. Preserve observed public facts; a failed or incomplete report must not prompt duplicate immutable publication. |
| Exceptional release or incident | Routine eligibility needs its existing engineering basis. Exceptional authentication/deferral needs explicit bounded authority. Recovery from bad public contents preserves failed history and uses the authorized correction path. These are actual-event assessments, not synthetic permission or extra routine review gates. |

These gaps retain the reduced-assurance decision from the minimal-suite change. Centralizing documentation removes no retained executable assertion and does not retire supported product behavior or weaken final review/Verify.

### Execution cost reporting

Use native test output and optional external wall-clock timing for a scoped observation. No worker-duration JSON, report reservation, cache, performance threshold or benchmark ledger is required. The old environment variables are no longer report interfaces.

### Model-owned test-design admission

The single [system test design](test-design/system-test-design.md) describes intended conditions and observations independently of implementation. Optional structural validation checks declared Markdown and local references without importing test suites or admitting retired JSON catalogs. Requirement-to-assertion adequacy remains an independent semantic assessment; structural success does not establish coverage.

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | VAL-SR-01 | Arguments to the direct runner reject before tests; valid invocation runs all essential groups. |
| State/lifecycle | VAL-SR-12 | Failed or interrupted execution cannot establish a passing complete-suite claim. |
| Identity/authority | VAL-SR-15 | Routine checks grant no publication authority; release still checks actual candidate identity. |
| Composition/path | VAL-SR-13, VAL-SR-14 | Every retained source is reached by its native entrypoint; deleted helpers have no current executable consumers. |
| Temporal/retry | VAL-SR-01, VAL-SR-17 | A repeated invocation owns fresh fixtures; no stale cache result replaces execution. |
| Failure/recovery | VAL-SR-14, VAL-SR-17 | Negative and recovery scenarios observe preserved state and user files. |
| Compatibility/migration | VAL-SR-16 | Removed contributor options reject; product records and historical judgments retain their meaning. |
| External/environment | VAL-SR-15, VAL-SR-18 | Tests use qualified local tools and controlled public-service fixtures; public observations remain release-owned. |

## Deployment View

Local and ordinary CI execution require Python and the package-supported Node version, with package dependencies installed. Routine CI does not install Chromium, Puppeteer, D2 or jsonschema. Changes to browser/model generators use their existing declared tools on demand. Release retains its own tool and authority boundaries.

## Crosscutting Concepts

Use [shared test-design rules](test-design/rules.md) for assertion quality, explicit limitations and meaningful negative cases. User-authorized reduction of regression breadth is distinct from an equivalence-preserving refactor. Review must judge the selected essential protection and disclosed residual risk rather than infer preserved coverage from a green run.

## Architecture Decisions

Keep the existing command name and required release entrypoints, replace their implementation directly, remove unused internal execution layers and reconcile all current consumers. Do not retain mode aliases or a dormant legacy suite. Git history is the recovery source.

## Quality Requirements

Failures remain visible; tests must detect the intended defect, preserve unrelated files and leave no private fixture state in the repository. Whole-change review and distinct Verify remain required.

## Risks and Technical Debt

Less automatic coverage makes changes outside the essential path more dependent on deliberate scoped proof. No empirical reliability or productivity improvement is claimed. Release public-service behavior still requires the actual observations specified by Release.

## Historical provenance

The prior validation contract and removed tests are recoverable at `d7761c8c9c34f0f3a4bb3a74504190e0ceafed53`. The [minimal-suite plan](../../docs/plans/2026-10-18-minimal-tests.md) records the selected scope; results and judgments belong to its Change.

[workflow]: ../architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md
[assessment]: ../architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md
[cli]: ../architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md
[records]: ../architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md
[installation]: ../architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/installation.md
[packaging]: ../architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md
[skill]: ../architecture/modules/MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/capability-contract.md
[release]: ../architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/release.md
[workflow-tests]: ../../packages/rigorloop/test/operational-review.test.js
[store-tests]: ../../packages/rigorloop/test/operational-store.test.js
[update-tests]: ../../packages/rigorloop/test/operational-update.test.js
[maintenance-tests]: ../../packages/rigorloop/test/operational-maintenance.test.js
[installer-tests]: ../../packages/rigorloop/test/installer-replacement.test.js
[archive-tests]: ../../tests/engineering/packaging/adapter_archive_tests.py
[package-tests]: ../../tests/engineering/packaging/test-npm-package-publication.py
[skill-tests]: ../../tests/skill/test-skill-validator.py
[release-identity]: ../../tests/engineering/release/release_identity_tests.py
[release-execution]: ../../tests/engineering/release/release_execution_tests.py
[release-tests]: ../../tests/engineering/release/test-release-transaction.py
[requirement-tree]: ../architecture/modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/requirement-tree.md
