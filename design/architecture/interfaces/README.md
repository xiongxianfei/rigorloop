# Interfaces

An Interface defines an explicit interaction contract between architectural responsibilities.
Apply the [REM Interface criteria](../../../rem/models/architecture-design.md#interfaces) to purpose, inputs, outputs, preconditions, failure outcomes, consistency, and compatibility.

The collection uses `<IF-ID>-<full-title-slug>.json` under the [entity naming convention](../../support/README.md#entity-naming-and-filenames).
The six draft contracts cover the [IR-001 architecture walkthrough](../README.md#scenario-walkthrough) and the proposed [published-product responsibilities](../../requirements/published-products.md). They describe logical interactions and artifact contracts rather than asserting new public runtime APIs or implementation.

<!-- interface-index:start -->

| Interface | Contract | Provider | Consumers |
| --- | --- | --- | --- |
| [IF-001](IF-001-engineering-definition-access.json) | Engineering definition access | [MOD-001](../modules/MOD-001-engineering-model-storage.json) | [MOD-002](../modules/MOD-002-engineering-model-authoring.json), [MOD-004](../modules/MOD-004-engineering-context-and-traceability.json) |
| [IF-002](IF-002-engineering-model-interpretation-and-identity-checks.json) | Engineering model interpretation and identity checks | [MOD-003](../modules/MOD-003-engineering-model-conformance.json) | [MOD-001](../modules/MOD-001-engineering-model-storage.json), [MOD-002](../modules/MOD-002-engineering-model-authoring.json) |
| [IF-003](IF-003-operational-record-access-and-publication.json) | Operational record access and publication | [MOD-011](../modules/MOD-011-operational-record-persistence.json) | [MOD-010](../modules/MOD-010-engineering-command-interface.json) |
| [IF-004](IF-004-scoped-public-command-execution.json) | Scoped public command execution | [MOD-010](../modules/MOD-010-engineering-command-interface.json) | [MOD-012](../modules/MOD-012-published-engineering-capability-guidance.json) |
| [IF-005](IF-005-verifiable-product-candidate-artifacts.json) | Verifiable product candidate artifacts | [MOD-013](../modules/MOD-013-product-package-production.json) | [MOD-014](../modules/MOD-014-verified-skill-installation.json), [MOD-015](../modules/MOD-015-product-release-coordination.json) |
| [IF-006](IF-006-verified-skill-installation-execution.json) | Verified skill installation execution | [MOD-014](../modules/MOD-014-verified-skill-installation.json) | [MOD-010](../modules/MOD-010-engineering-command-interface.json) |

<!-- interface-index:end -->

Participation is derived from Module-owned `provides` and `consumes` references. Do not repeat provider or consumer lists in Interface JSON.
Each current Interface has one accountable provider and at least one modeled consumer. Refined REM requires exactly one provider and permits zero or more consumers; the current consumer count is a property of these authored contracts.
An empty set of contracts elsewhere means recorded interactions are deferred, not that the Module needs no cooperation.

The self-contained [Interface schema](../../support/schemas/interface.schema.json) requires identity, title, draft status, description, named operations, consistency rules, compatibility rules, and sources.
Each operation has a unique `snake_case` name within the Interface and explains its purpose, inputs, preconditions, outputs, behavior, and condition/outcome failures.
Operation names identify contract behavior rather than stable first-class engineering entities.
No transport, wire encoding, database, programming language, or deployment decision is implied.

IF-001 preserves state and completeness across content access, including rationale availability and applicability.
IF-002 interprets supplied content and checks supplied candidate scope without recursively fetching its own interpretation basis.
Their consistency rules connect identity checking to the state actually retained and prevent mixing different selected states into an apparently complete account.
The written outcomes require later implementation verification; schema conformance alone cannot establish them.
