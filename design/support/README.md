# Operational Support

This directory defines RigorLoop's representation and validation of its engineering model.
The reusable [REM Operational Support model](../../rem/models/operational-support.md) describes the responsibilities independently of storage format or tooling.

The [initial authoring profile decisions](../requirements/sources.md#src-question-resolution) locate the selected requirements for model scope, retention, recovery, evidence, metamodel compatibility, authoring guidance, handoffs, authority, and learning.
They define intended behavior and assessment boundaries; the schemas below implement record-shape checks only.

## Record schemas

The current draft authoring profile uses eight self-contained JSON Schema Draft 2020-12 documents:

| Record | Schema | Meaning |
| --- | --- | --- |
| `ir.json` | [ir.schema.json](schemas/ir.schema.json) | Initial need with 5W2H analysis and attributed sources |
| `sr.json` | [sr.schema.json](schemas/sr.schema.json) | System obligation with 5W2H analysis, acceptance criteria, and attributed sources |
| `AR-*.json` | [ar.schema.json](schemas/ar.schema.json) | Lower-level obligation with 5W2H analysis, acceptance criteria, and one accountable Module |
| `SCN-*.json` | [scenario.schema.json](schemas/scenario.schema.json) | Governed stakeholder situation, observable interaction and outcomes, and links to its primary Feature and SRs |
| `FEAT-*.json` | [feature.schema.json](schemas/feature.schema.json) | Durable capability, scope, and realizing Functions |
| `FUNC-*.json` | [function.schema.json](schemas/function.schema.json) | Logical behavior, inputs, outputs, failures, and allocation disposition |
| `MOD-*.json` | [module.schema.json](schemas/module.schema.json) | Architectural responsibility, state ownership, boundaries, and Interface references |
| `IF-*.json` | [interface.schema.json](schemas/interface.schema.json) | Operations, outcomes, consistency, and compatibility at an interaction boundary |

Each schema contains its own field rules; requirement schemas contain their inline analysis definitions.
There is no shared schema or separate 5W2H schema.
The [requirement authoring guide](../requirements/README.md#record-content-and-schemas) explains the fields and directory conventions.

The IR, SR, and AR schemas require nonblank text and all seven 5W2H objects under `analysis`, including `what`.
The requirement `statement` remains authoritative; `analysis.what` explains its problem and desired outcome without copying it.
Stakeholder, condition, context, and source lists must be nonempty.
SRs and ARs additionally require nonempty acceptance criteria.
The required root lists `assumptions` and `constraints` may be empty.
For IR, SR, AR, and Scenario, `open_questions` is optional and contains exactly one nonblank entry when present. Omit it when no consequential question remains; empty lists are rejected.
The [question-selection rule](../../rem/methods/requirement-analysis.md#keep-one-consequential-open-question) defines how to select and ask one valuable question at a time; schema validation enforces the count, while engineering review assesses its value and whether independent questions have been bundled.
Optional fields may be omitted, optional 5W2H lists may be empty, and no field accepts `null`.
Unknown fields and unsupported vocabulary are rejected: each schema fixes its record `type`, and `5W2H` is the selected requirement-analysis method.
IR, SR, AR, Feature, Function, Module, and Interface schemas currently permit only `draft` status. Scenario status may be `draft`, `confirmed`, or `obsolete` under the [Scenario lifecycle](../../rem/models/scenarios.md#lifecycle).
An empty list does not establish completeness, approval, or satisfaction; the authoring guide explains each field's meaning.

The schemas describe the contents of one record.
A validator must explicitly select the schema by the declared collection and filename above; placing the schemas here does not automatically validate files.
Cross-file and engineering review must still check:

- Unique identities across the governed model and their agreement with directory names.
- Exactly one IR parent for each SR and exactly one SR parent for each AR.
- Exactly one owning IR for each Scenario, recorded by an incoming IR `confirms` reference.
- Resolvable, correctly typed relationships and attributable sources.
- Clear names, sound derivation, meaningful analysis, and assessable obligations.
- Valid lifecycle transitions, including sufficient downstream obligation analysis before Scenario confirmation.
- Applicable evidence before a satisfaction claim.

Lifecycle transitions beyond the selected Scenario profile and runtime validation integration remain to be defined as the model develops.

## Scenario and system-design records

[Scenarios](../requirements/scenarios/README.md) live in `design/requirements/scenarios/<SCN-ID>-<title-slug>.json` as governed Requirement Analysis entities, outside the requirement containment tree.
Each records its actor, goal, context, trigger, preconditions, observable interaction, expected outcome, alternatives, failures, and typed relationships.
Each `interaction` entry has `actor` and `action`, with observable system responses represented as actions by the system. It must remain meaningful independently of internal solution design.
`exercises` records at most one primary Feature; it may be empty in a draft. Confirmed Scenarios require exactly one primary Feature, which must also be confirmed by their owning IR, and this profile retains that reference when they become obsolete.
The schema permits an empty `informs` array, but does not authorize lifecycle confirmation. Refined Scenario Analysis requires sufficient downstream SR analysis or an explicit conclusion before confirmation; a Scenario introducing no additional obligation may record that conclusion in `coverage_note`.
That completion rule and the validity of lifecycle transitions require engineering review; accepting the state vocabulary in JSON does not perform those reviews.

[Features](../system/features/README.md) live in `design/system/features/<FEAT-ID>-<title-slug>.json` and describe durable capability through `description` and `scope.includes` / `scope.excludes`.
Their required `realized_by` list may be empty until SR analysis establishes Functions.
[Functions](../system/functions/README.md) live in `design/system/functions/<FUNC-ID>-<title-slug>.json` and define inputs, preconditions, outputs, behavior, and failure behavior.
Each Function has exactly one of `allocated_to` (one accountable Module) or `unallocated_reason` (explicit reason and limits for deferred allocation).
All 63 current Functions have draft `allocated_to` references to 15 proposed Modules. The [Architecture Design](../architecture/README.md) distinguishes this responsibility map from the bounded Interface and AR coverage developed so far.

Every new record begins with a stable ID, type, title, draft status, and nonempty attributed `sources` using the [source register](../requirements/sources.md).
Scenarios may record one consequential `open_questions` entry under the same rule as IRs and SRs. Feature and Function records have no `open_questions` field; their closed schemas reject it.
Scenario alternatives and failures, and Function failures, use closed `{ "condition": "...", "outcome": "..." }` objects.
Scenario alternatives achieve the stated goal through a different path; failures prevent or limit that goal. Honest retrieval diagnostics can therefore be successful alternatives when recognizing gaps is the goal.
Preconditions, alternatives/failure lists, and scope exclusions may be empty when none are recorded; required interactions, inputs, outputs, behavior, and Feature inclusions are nonempty.
Text is nonblank, objects reject undeclared fields, and `null` is unsupported throughout.
5W2H is not mechanically copied into Scenarios or system assets.

## Architecture and allocated-requirement records

[Modules](../architecture/modules/README.md) live in `design/architecture/modules/<MOD-ID>-<title-slug>.json`.
Each records its `description`, nonempty `responsibilities`, `owned_state`, and `scope.includes` / `scope.excludes`.
The required `provides` and `consumes` lists reference Interfaces through unique stable IDs; they may be empty.
`owned_state` may be empty for a Module that owns no enduring state. Nonempty `design_limits` records the scope of the proposed design and any deferred contract detail.
Do not interpret an empty Interface list as evidence that all dependencies have been analyzed; inspect the Module's stated limits.

[Interfaces](../architecture/interfaces/README.md) live in `design/architecture/interfaces/<IF-ID>-<title-slug>.json`.
Each has a description, nonempty `operations`, `consistency_rules`, and `compatibility_rules`.
An operation records a lowercase snake_case `name`, `purpose`, nonempty `inputs`, `outputs`, and `behavior`, plus `preconditions` and `failure_behavior` lists that may be empty.
Failure entries use closed `{ "condition": "...", "outcome": "..." }` objects.
Operation names must be unique within the Interface; the focused check below enforces that rule beyond JSON Schema.
Provider and consumer views are derived from Module references, never repeated in Interface fields. Each of the six current Interfaces has one provider and at least one consumer. Refined REM requires exactly one provider and allows zero or more consumers; the stronger current consumer-count check is a property of this authored model, beyond the individual-record JSON Schema.

An AR lives directly inside its owning SR directory as `<AR-ID>-<title-slug>.json`.
Its `statement`, inline 5W2H `analysis`, `acceptance_criteria`, `assumptions`, `constraints`, and `sources` use the requirement profile described above, with exactly one scalar `allocated_to` Module reference.
Optional `constrains` links identify Functions shaped by the obligation. ARs do not have `confirms`, a copied parent ID, or an unallocated disposition.
Containment supplies exactly one parent SR, and the stable AR identity does not encode that parent.
An AR may record one consequential open question under the requirement rule. Modules and Interfaces, like Features and Functions, reject `open_questions`.

The current target architecture contains 15 draft Modules, six draft Interfaces, and ten draft ARs: nine under IR-001 and one under IR-005's SR-012 for the shared interpretation responsibility.
Detailed AR coverage is bounded to that first example. Four Interfaces connect the subsequent published-product responsibilities, while further interactions and ARs remain explicit `design_limits`.
These records propose an architecture. They do not describe an observed implementation or establish complete architectural coverage of all ten IRs.

## Entity naming and filenames

Apply REM's [clarity principle](../../rem/principles/README.md), [Scenario criteria](../../rem/models/scenarios.md), and [System Design criteria](../../rem/models/system-design.md) to the name and definition before deriving a physical label.
Names communicate engineering meaning; identities preserve continuity.
The title must identify the engineering purpose and subject, distinguish the entity from its neighbors, and agree with its current scope.
Scenario titles describe a stakeholder goal and situation; Feature titles describe a stakeholder capability; Function titles describe a logical action. Prefer action plus subject and add conditions when they distinguish the meaning.
Module titles identify a cohesive architectural responsibility; Interface titles identify the interaction contract; AR titles identify the allocated obligation.

For Scenario, Feature, Function, Module, Interface, and AR records, use `<ID>-<title-slug>.json`.
The JSON `id` owns stable identity and `title` owns the readable name. Derive the suffix using the same [full-title normalization](../requirements/README.md#directory-naming) as IR and SR directory names.
Preserve all title words; do not maintain a separate `slug` or abbreviate the suffix independently.

For example:

```text
requirements/scenarios/SCN-001-retrieve-a-saved-definition-in-a-later-session.json
system/features/FEAT-001-inspect-engineering-definitions-and-their-rationale.json
system/functions/FUNC-001-retain-engineering-definition.json
architecture/modules/MOD-001-engineering-model-storage.json
architecture/interfaces/IF-001-engineering-definition-access.json
```

A title change requires a matching filename change and reconciliation of current path-based links and consumers.
Keep the entity ID and ID-based relationships unchanged when the same entity is renamed.
Check the destination before renaming; a collision or unsupported filename must be resolved without overwriting another record, truncating the title silently, or generating a replacement ID.
Historical paths retain the meaning of their original states.

IRs and SRs use title-derived directories containing `ir.json` or `sr.json`. AR files use the full-title filename convention directly within their single parent SR directory, without an additional AR directory.
It is a repository representation choice. REM's clarity principle also applies to implementations that do not use files.
JSON Schema checks required text and shape; checking filename agreement requires reading the file path, and judging clarity requires engineering review.

## Relationship ownership

JSON names use `snake_case`. REM `realizedBy` is represented by `realized_by`. The existing Function field `allocated_to` represents the accountable `primaryModule` relationship in the refined REM; the same field on an AR represents `allocatedTo`. This task preserves that selected serialized spelling rather than renaming existing records. Supporting Module cooperation is described through the scoped Interface contracts; this profile has not added a separately authored per-Function supporting-Module field.

| Authored record | JSON field | Compatible targets |
| --- | --- | --- |
| IR | `confirms` | Feature or Scenario |
| Scenario | `exercises` | One primary Feature; may be empty in a draft |
| Scenario | `informs` | SR |
| SR | `confirms` | Function |
| SR | `constrains` | Feature or Function |
| Feature | `realized_by` | Function |
| Function | `allocated_to` | Module, when allocated |
| AR | `allocated_to` | Exactly one Module |
| AR | `constrains` | Function |
| Module | `provides` | Interface |
| Module | `consumes` | Interface |

All fields except `allocated_to` are arrays of unique stable IDs; schema checks enforce their target prefixes.
The IR and SR relationship fields and AR `constrains` are optional so partial drafts remain valid; the other array fields are required.
Scenario `exercises` has at most one entry, with exactly one required for confirmed and obsolete records.
An empty `informs` in a draft requires SR reconciliation or an explicit no-additional-obligation conclusion before confirmation. An empty `realized_by` leaves logical realization to later SR analysis.
The current analysis records system-design connections across all ten IRs. Functions carry proposed primary Module allocations. Detailed AR coverage remains bounded to IR-001 and its shared SR-012 dependency; Interface coverage includes that pilot and the four published-product contracts, with further interactions explicitly deferred.
Actual target existence, type, and compatibility require cross-file checks; a correctly spelled ID alone is insufficient.

Author each relation at its source in this table and derive reverse views. Do not add inverse lists or parent IDs to the target.
Requirement parentage still comes solely from directory containment. Scenario ownership is a separate relationship: exactly one IR must reference each Scenario through `confirms`.
Scenarios may inform multiple SRs, and an SR may be informed by multiple Scenarios, without changing requirement parentage.
Textual requirement `constraints` remain distinct from typed `constrains` links.
For Features and Functions, `confirms` records an analysis conclusion. For a Scenario, the IR reference records ownership while its own `status` records lifecycle confirmation separately.
These references grant no approval, execution authority, or satisfaction claim.

## Compatibility and adoption

This extends the unpublished draft profile: existing IR/SR records remain valid without the new optional relationships, and their identities and containment stay unchanged.
Consumers of the extended profile must use the updated schemas; earlier closed schemas correctly reject the new fields.
The question-field refinement permitted the field on IR, SR, and Scenario only when exactly one consequential question was recorded; the architecture extension applies the same rule to ARs. Earlier profiles required IR/SR/Scenario question lists and allowed multiple Scenario questions; consumers must adopt the new optional-field and cardinality rules.
The fourteen IR/SR records and six Scenarios present at that refinement had empty question lists; those fields were removed without discarding any question. A future migration containing several unresolved questions must resolve or reconcile them explicitly rather than truncate the list. Features and Functions continue to reject the field.
The asset naming refinement moved the two Feature and seven Function drafts from ID-only filenames to the title-derived convention. Their IDs, relationship targets, scope, and draft status remained unchanged; collection links were reconciled. Consumers discover these files by collection and read `id` from JSON, rather than treating the full filename stem as identity.
The governed Scenario refinement replaced `flow` with structured `interaction`, added `goal` and `failures`, removed `candidate_behavior`, restricted each Scenario to one primary Feature, and defined the three lifecycle states.
SCN-001 through SCN-004 retain their identities and main stakeholder meanings. Their embedded save and record-rationale goals receive new SCN-005 and SCN-006 identities, all owned by IR-001. The [source register](../requirements/sources.md#src-scenario-model-refinement) records that analysis and its existing SR coverage.
Earlier Scenario JSON must be reconciled with these rules; it will not validate unchanged. That refinement preserved the six Scenario drafts and the existing SR, Feature, and Function meanings.
The Scenario naming refinement moved those six records from ID-only filenames to `<SCN-ID>-<title-slug>.json`, preserving their JSON content, including identity, title, references, scope, sources, and draft status.
Current links use the new paths. Consumers discover Scenarios through `SCN-*.json` and read the JSON `id`; an ID-only filename or the complete filename stem must not be assumed to be the identity.
Current product contracts and runtime validators under `docs/` are unaffected. These authoring schemas do not adopt a new production format or claim that the CLI implements REM.
Current requirements and assets retain draft status. The subsequent seven-IR analysis completed the connected definitions and confirmed 35 Scenarios after semantic review and correction; the format migrations themselves did not confer that status.

The first architecture extension added three self-contained schemas and Module, Interface, and AR records without changing existing Function behavior, requirement parentage, or stable identities.
Each of the then-existing 33 Function records replaced its deferred allocation reason with one draft Module reference and appended the architectural basis in `sources`.
The existing Function schema already supports this representation. Consumers that enumerate entity kinds or validate cross-file references must include the new collections and relationships before relying on the extended model.

The [published-product extension](../requirements/published-products.md) adds three IRs, 29 SRs, nine Features, 30 Functions, 27 confirmed Scenarios, six Modules, and four Interfaces using those same eight schemas. It reconciles IR-006's current schema-availability statement and adds SR-014's confirmation of the two existing Functions it already governs under refined Functional Analysis. Earlier requirement meanings, acceptance criteria, and Function behavior remain unchanged. It does not alter stored CLI record formats, installed guidance, package formats, or release behavior.
The responsibility map is a proposed target; detailed contracts for the remaining obligations and implementation mappings remain later work.

## Focused local check

From the repository root, run:

```bash
python3 tests/engineering/validation/requirement_schema_tests.py
python3 tests/engineering/validation/system_design_schema_tests.py
python3 tests/engineering/validation/architecture_schema_tests.py
```

This check requires Python 3 and a `jsonschema` installation supporting Draft 2020-12.
These direct checks validate the schemas and current records, and exercise malformed and unsupported records using independent fixtures.
Requirement checks cover IR/SR 5W2H and optional typed references; requirement and Scenario/system checks cover omission or exactly one nonblank question for IR/SR/Scenario and reject empty or multiple entries.
Scenario/system checks also cover interaction and outcome content, lifecycle vocabulary, primary-Feature cardinality, staged empty links, target prefixes, duplicate references, explicit allocation disposition, and rejection of open questions on Features and Functions.
The Scenario/system suite also checks unique identities, title-derived names, SR and AR containment, exactly one IR owner per Scenario, and compatible existing targets across the current requirement, system-design, and architecture collections.
It checks that the completed analysis has IR-to-SR/Feature/Scenario connections, SR design effects, Scenario coverage references, Function realization and requirement basis, and registered source identifiers. These are properties of this authored analysis; early drafts remain permitted by the schemas.
Architecture checks cover the three new record shapes, AR 5W2H and acceptance criteria, one accountable Module, optional typed constraints and one-question cardinality, required Interface operation content, and closed vocabulary and object fields.
Independent malformed fixtures exercise rejection of duplicate links, wrong target types, copied parent and inverse fields, unsupported names, blank content, and multiple owners. Current-record checks require one provider and at least one consumer for each authored Interface and unique operation names within it.
Those checks expose missing or incompatible connections, not whether linked behavior actually satisfies an obligation. No suite establishes semantic coverage, the adequacy of a source basis, valid lifecycle transitions, or intended product behavior; Interface failure and consistency behavior still require implementation and applicable evidence.
CI integration is not part of this initial profile.

Schema conformance establishes structural validity only.
IR/SR/AR/Feature/Function/Module/Interface records remain drafts; confirmed Scenarios express accepted analysis knowledge. The existing repository contracts retain their authority during migration.
