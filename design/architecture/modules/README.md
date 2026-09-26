# Modules

A Module is a durable architectural responsibility with a meaningful boundary.
The [REM definition criteria](../../../rem/models/architecture-design.md#modules) explain purpose, responsibility, state authority, and exclusions; the [architecture method](../../../rem/methods/architecture-design.md) develops those boundaries.

The collection uses `<MOD-ID>-<full-title-slug>.json` under the [entity naming convention](../../support/README.md#entity-naming-and-filenames).
All 15 records describe proposed target architecture with `draft` status. They establish no observed code boundary, implementation, approval, or requirement satisfaction.

<!-- module-index:start -->

| Module | Responsibility | Provides | Consumes |
| --- | --- | --- | --- |
| [MOD-001](MOD-001-engineering-model-storage.json) | Engineering model storage | [IF-001](../interfaces/IF-001-engineering-definition-access.json) | [IF-002](../interfaces/IF-002-engineering-model-interpretation-and-identity-checks.json) |
| [MOD-002](MOD-002-engineering-model-authoring.json) | Engineering model authoring | — | [IF-001](../interfaces/IF-001-engineering-definition-access.json), [IF-002](../interfaces/IF-002-engineering-model-interpretation-and-identity-checks.json) |
| [MOD-003](MOD-003-engineering-model-conformance.json) | Engineering model conformance | [IF-002](../interfaces/IF-002-engineering-model-interpretation-and-identity-checks.json) | — |
| [MOD-004](MOD-004-engineering-context-and-traceability.json) | Engineering context and traceability | — | [IF-001](../interfaces/IF-001-engineering-definition-access.json) |
| [MOD-005](MOD-005-engineering-baseline-management.json) | Engineering baseline management | — | — |
| [MOD-006](MOD-006-engineering-change-control.json) | Engineering change control | — | — |
| [MOD-007](MOD-007-engineering-verification-and-assurance.json) | Engineering verification and assurance | — | — |
| [MOD-008](MOD-008-engineering-authoring-guidance.json) | Engineering authoring guidance | — | — |
| [MOD-009](MOD-009-engineering-learning.json) | Engineering learning | — | — |
| [MOD-010](MOD-010-engineering-command-interface.json) | Engineering command interface | [IF-004](../interfaces/IF-004-scoped-public-command-execution.json) | [IF-003](../interfaces/IF-003-operational-record-access-and-publication.json), [IF-006](../interfaces/IF-006-verified-skill-installation-execution.json) |
| [MOD-011](MOD-011-operational-record-persistence.json) | Operational record persistence | [IF-003](../interfaces/IF-003-operational-record-access-and-publication.json) | — |
| [MOD-012](MOD-012-published-engineering-capability-guidance.json) | Published engineering capability guidance | — | [IF-004](../interfaces/IF-004-scoped-public-command-execution.json) |
| [MOD-013](MOD-013-product-package-production.json) | Product package production | [IF-005](../interfaces/IF-005-verifiable-product-candidate-artifacts.json) | — |
| [MOD-014](MOD-014-verified-skill-installation.json) | Verified skill installation | [IF-006](../interfaces/IF-006-verified-skill-installation-execution.json) | [IF-005](../interfaces/IF-005-verifiable-product-candidate-artifacts.json) |
| [MOD-015](MOD-015-product-release-coordination.json) | Product release coordination | — | [IF-005](../interfaces/IF-005-verifiable-product-candidate-artifacts.json) |

<!-- module-index:end -->

The [responsibility map](../README.md#responsibility-map) derives assigned Functions; the [requirement convergence view](../README.md#requirement-and-function-convergence) derives assigned ARs.
Do not add inverse Function or AR lists to Module JSON.
Modules author `provides` and `consumes` references; the Interface owns its actual contract.

The self-contained [Module schema](../../support/schemas/module.schema.json) requires identity, title, draft status, description, responsibilities, owned state, included/excluded scope, Interface participation, design limits, and attributed sources.
`owned_state` may be empty for a stateless responsibility. Where stored content and authority over meaning have different owners, explain the distinction rather than claiming unrestricted ownership in both places.
Empty Interface lists do not establish independence: each Module's `design_limits` identifies deferred interactions and pilot coverage.
Module and Interface schemas do not include `open_questions`; material uncertainty belongs explicitly in the relevant design definition and prevents unsupported coverage claims.

Architecture need not map one-to-one to packages, source directories, processes, or deployment units. No realization mapping is asserted in this first draft.
