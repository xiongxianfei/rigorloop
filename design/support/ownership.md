# Engineering definition ownership

The repository-held REM model is the entry point for current engineering meaning. Requirements live in `design/requirements/`, Features and Functions in `design/system/`, and Modules, Interfaces and their realization in `design/architecture/`. Reusable engineering methods live in `rem/`. User and contributor instructions live in `docs/`; they reference their governing definitions rather than becoming parallel design owners.

## Detailed contracts

A Module or Interface may retain supporting Markdown contracts, examples, decisions and test-design catalogs alongside its entity record. These are subordinate detail of that responsibility, not additional REM entities or independent submodels. The architecture index owns system-wide composition. Shared repository development and validation rules live under `design/support/`; the validation executor is not the product's engineering-model conformance Module.

| Responsibility | Current owner and supporting detail |
| --- | --- |
| System-wide cooperation and integrated acceptance | Architecture composition; existing SYS-SR and TEST-SR clause identities |
| Command admission, rendering, exit classes and diagnostics | MOD-010 Command handling; command contract |
| Stored records, version interpretation and persistence | MOD-011 Work record storage; record contract and current SQLite realization |
| Lifecycle, planning and external handoff authority | MOD-006 Change control; workflow, planning and delivery handoff |
| Independent judgment, applicability and final Verify | MOD-007 Review and verification; assessment contract |
| Requirement/design authoring, discovery and project foundations | MOD-008 Authoring guidance; activity-specific contracts consuming canonical REM methods |
| Reusable lessons and improvement | MOD-009 Lessons and improvement; learning contract |
| Published invocation and resource integrity | MOD-012 Skill procedures; capability contract and its coverage |
| Artifact construction and generated resources | MOD-013 Package production; packaging contract |
| Verified acquisition and destination effects | MOD-014 Skill installation; installation contract |
| Candidate qualification, publication and recovery | MOD-015 Release coordination; release contract and coverage |
| Repository development, check admission/execution and shared test policy | Repository support documents and shared test-design rules; policy accountability remains system-wide composition |

Retained source-qualified clauses such as CLI-SR, WF-SR, DIST-SR and TEST-SR preserve their existing meaning. They are detailed contract references, not newly introduced REM System Requirements. Existing IR/SR records retain their stable identities and refer to the responsible current clause where applicable. New or changed stakeholder obligations still require requirement analysis; moving a clause does not approve it, promote an entity's status or expand supported behavior.

The explicit validation registry identifies supporting contract documents and selected coverage packages. Its contract keys do not define Module boundaries or a competing architecture hierarchy. The portable `model-document-v1` profile remains available to customer projects with their own layout; repository-owned contracts use exact registered locations. Structural conformance does not establish semantic adequacy or approval.

## Sources, views and evidence

Entity records own relationships; supporting contracts own detailed rules; realization facets own selected technology and explanation. Views are generated projections of these sources. Changing a source location must reconcile reference resolvers, generators, link consumers, schemas, published resources and actual validation selection together. Do not author a second copy of the same rule in a browser view or skill package.

Selected synthetic protocol examples belong under `tests/fixtures/cli-contract-examples/`. They retain their declared historical version and original synthetic assessed-subject identities; relocating them does not adopt that protocol or relabel its judgments. Their navigation identifies the current owner and scope. Executable tests and current examples must resolve through their declared location. Historical payload paths are data, not instructions to load retired design sources.

Reviews, mutable handoffs, execution results and migration dispositions are operational records accessed through the CLI. Current design remains readable without them. Historical approval identities retain their original subjects; current provenance to retired material names its recoverable commit and original path. Git retains retired narratives once their surviving responsibilities and current dependencies have been reconciled.

## Evolution and removal

Before removing a source, account for both numbered and unnumbered obligations, rationale, representation and failure rules, useful examples and protective proof. Transfer surviving meaning to its accountable owner, consolidate duplication, or record a justified retirement. Unmapped supported behavior or an unresolved current consumer blocks the affected removal. A file-count map alone is insufficient.

Reconcile relative links from their original resolved targets, not merely by changing directory strings. Preserve byte-sensitive historical fixtures and original judgments. Update active provenance to current owners only when it still denotes the same obligation. Historical source-qualified provenance remains historical. Existing regression and negative protection survives unless its responsible owner establishes redundancy or retirement; the migration does not require a permanent test for the existence of its disposition report.
