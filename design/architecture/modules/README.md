# Modules

A Module is a durable architectural responsibility with a meaningful boundary.
The [REM definition criteria](../../../rem/models/architecture-design.md#modules) explain purpose, responsibility, state authority, and exclusions; the [architecture method](../../../rem/methods/architecture-design.md) develops those boundaries.

The collection uses `<MOD-ID>-<full-title-slug>/module.json` under the [entity naming convention](../../support/README.md#entity-naming-and-filenames). Child owners use the same convention under their parent's `modules/` directory. This nesting alone defines parentage: do not add `parent_module` fields or authored child lists. An owner can have both `modules/` and `realization/` directories.
All 19 records describe proposed target architecture with `draft` status: four parents and 15 children. MOD-010 and MOD-011 additionally distinguish source-backed implementation observations from proposed realization choices; neither establishes approval or requirement satisfaction.

Parents own genuine broader responsibilities; children refine them. The index follows containment order and derives its Parent column from paths. Interface exposure is derived from Interface-owned `exposed_through` references, independently of a Module's directly authored `provides` and `consumes` relationships.
`provides` identifies the Module accountable for an Interface contract. MOD-018 owns IF-004 while MOD-010 and MOD-011 retain their allocated behavior; MOD-019 owns IF-006 while MOD-014 retains installation behavior. Child realization does not add a provider or a consumer. No current Interface declares descendant exposure.
MOD-016 owns IF-007 for selected-state content and interpretation. MOD-017 owns IF-008 for adopted model-authoring guidance and IF-009/IF-010 for authority and evidence support. Their consumers are MOD-005, MOD-012, and MOD-015 respectively. The [bounded cooperation analysis](../views/browser/index.html#scenarios) distinguishes contract accountability from each child's unchanged behavior and outstanding work.

<!-- module-index:start -->

| Module | Responsibility | Parent | Directly provides | Directly consumes | Exposes descendant Interface |
| --- | --- | --- | --- | --- | --- |
| [MOD-016](MOD-016-engineering-model-management/module.json) | Engineering model management | — | [IF-007](../interfaces/IF-007-engineering-state-content-and-interpretation/interface.json) | — | — |
| [MOD-001](MOD-016-engineering-model-management/modules/MOD-001-engineering-model-storage/module.json) | Engineering model storage | [MOD-016](MOD-016-engineering-model-management/module.json) | [IF-001](../interfaces/IF-001-engineering-definition-access/interface.json) | [IF-002](../interfaces/IF-002-engineering-model-interpretation-and-identity-checks/interface.json) | — |
| [MOD-002](MOD-016-engineering-model-management/modules/MOD-002-engineering-model-authoring/module.json) | Engineering model authoring | [MOD-016](MOD-016-engineering-model-management/module.json) | — | [IF-001](../interfaces/IF-001-engineering-definition-access/interface.json), [IF-002](../interfaces/IF-002-engineering-model-interpretation-and-identity-checks/interface.json) | — |
| [MOD-003](MOD-016-engineering-model-management/modules/MOD-003-engineering-model-conformance/module.json) | Engineering model conformance | [MOD-016](MOD-016-engineering-model-management/module.json) | [IF-002](../interfaces/IF-002-engineering-model-interpretation-and-identity-checks/interface.json) | — | — |
| [MOD-004](MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/module.json) | Engineering context and traceability | [MOD-016](MOD-016-engineering-model-management/module.json) | — | [IF-001](../interfaces/IF-001-engineering-definition-access/interface.json) | — |
| [MOD-017](MOD-017-engineering-governance/module.json) | Engineering governance | — | [IF-008](../interfaces/IF-008-applicable-engineering-authoring-guidance/interface.json), [IF-009](../interfaces/IF-009-applicable-governed-action-authority/interface.json), [IF-010](../interfaces/IF-010-claim-evidence-applicability-and-coverage/interface.json) | — | — |
| [MOD-005](MOD-017-engineering-governance/modules/MOD-005-engineering-baseline-management/module.json) | Engineering baseline management | [MOD-017](MOD-017-engineering-governance/module.json) | — | [IF-007](../interfaces/IF-007-engineering-state-content-and-interpretation/interface.json) | — |
| [MOD-006](MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/module.json) | Engineering change control | [MOD-017](MOD-017-engineering-governance/module.json) | — | — | — |
| [MOD-007](MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/module.json) | Engineering verification and assurance | [MOD-017](MOD-017-engineering-governance/module.json) | — | — | — |
| [MOD-008](MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/module.json) | Engineering authoring guidance | [MOD-017](MOD-017-engineering-governance/module.json) | — | — | — |
| [MOD-009](MOD-017-engineering-governance/modules/MOD-009-engineering-learning/module.json) | Engineering learning | [MOD-017](MOD-017-engineering-governance/module.json) | — | — | — |
| [MOD-018](MOD-018-engineering-operations/module.json) | Engineering operations | — | [IF-004](../interfaces/IF-004-scoped-public-command-execution/interface.json) | — | — |
| [MOD-010](MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/module.json) | Engineering command interface | [MOD-018](MOD-018-engineering-operations/module.json) | — | [IF-003](../interfaces/IF-003-operational-record-access-and-publication/interface.json), [IF-006](../interfaces/IF-006-verified-skill-installation-execution/interface.json) | — |
| [MOD-011](MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/module.json) | Operational record persistence | [MOD-018](MOD-018-engineering-operations/module.json) | [IF-003](../interfaces/IF-003-operational-record-access-and-publication/interface.json) | — | — |
| [MOD-012](MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/module.json) | Published engineering capability guidance | [MOD-018](MOD-018-engineering-operations/module.json) | — | [IF-004](../interfaces/IF-004-scoped-public-command-execution/interface.json), [IF-008](../interfaces/IF-008-applicable-engineering-authoring-guidance/interface.json) | — |
| [MOD-019](MOD-019-product-delivery/module.json) | Product delivery | — | [IF-006](../interfaces/IF-006-verified-skill-installation-execution/interface.json) | — | — |
| [MOD-013](MOD-019-product-delivery/modules/MOD-013-product-package-production/module.json) | Product package production | [MOD-019](MOD-019-product-delivery/module.json) | [IF-005](../interfaces/IF-005-verifiable-product-candidate-artifacts/interface.json) | — | — |
| [MOD-014](MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/module.json) | Verified skill installation | [MOD-019](MOD-019-product-delivery/module.json) | — | [IF-005](../interfaces/IF-005-verifiable-product-candidate-artifacts/interface.json) | — |
| [MOD-015](MOD-019-product-delivery/modules/MOD-015-product-release-coordination/module.json) | Product release coordination | [MOD-019](MOD-019-product-delivery/module.json) | — | [IF-005](../interfaces/IF-005-verifiable-product-candidate-artifacts/interface.json), [IF-009](../interfaces/IF-009-applicable-governed-action-authority/interface.json), [IF-010](../interfaces/IF-010-claim-evidence-applicability-and-coverage/interface.json) | — |

<!-- module-index:end -->

The [responsibility map](../README.md#responsibility-map) derives assigned Functions; the [requirement convergence view](../README.md#requirement-and-function-convergence) derives assigned ARs. The [Logical view](../views/browser/index.html#overview) distinguishes direct assignments from unique descendant summaries.
Functions and ARs allocate to their lowest coherent accountable Module. Parents may own genuine broader obligations, but display rollups do not duplicate ownership. Do not add inverse Function or AR lists to Module JSON.
Modules author `provides` and `consumes` references; the Interface record defines the contract. The provider is accountable for that contract, while Function and AR allocations identify the Modules accountable for the contributing behavior and obligations.

The self-contained [Module schema](../../support/schemas/module.schema.json) requires identity, title, draft status, description, responsibilities, owned state, included/excluded scope, Interface participation, design limits, and attributed sources.
`owned_state` may be empty for a stateless responsibility. Where stored content and authority over meaning have different owners, explain the distinction rather than claiming unrestricted ownership in both places.
Empty Interface lists do not establish independence: each Module's `design_limits` identifies deferred interactions and pilot coverage.
Module and Interface schemas do not include `open_questions`; material uncertainty belongs explicitly in the relevant design definition and prevents unsupported coverage claims.

Architecture need not map one-to-one to packages, source directories, processes, or deployment units. Optional sibling `realization/*.json` files follow the [realization profile](../../support/README.md#subordinate-realization-views). They record material source mappings, runtime, persistence, packaging, technologies, choices, and deferrals without adding first-class entity types.
The [runtime view](../views/browser/index.html#process) summarizes the current bounded example from MOD-010 and MOD-011.
