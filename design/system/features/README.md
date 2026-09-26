# Features

A Feature is a durable product-visible or stakeholder-visible capability.
It explains the value the system provides and can evolve under multiple Requirements and Changes.

The collection uses one `<FEAT-ID>-<title-slug>.json` file per Feature under the [asset naming convention](../../support/README.md#entity-naming-and-filenames).
Names and capability descriptions belong in the entity content, independently of its stable identity.
The current analysis defines these eleven capabilities. Functions may be shared across them; Feature boundaries keep inspection, authoring, guidance, assessment, and controlled adoption distinguishable.

| Feature | Capability | Realizing Functions |
| --- | --- | --- |
| [FEAT-001](FEAT-001-inspect-engineering-definitions-and-their-rationale.json) | Inspect engineering definitions and their rationale | FUNC-003, FUNC-004, FUNC-007 |
| [FEAT-002](FEAT-002-author-and-revise-engineering-definitions.json) | Author and revise engineering definitions | FUNC-001, FUNC-002, FUNC-003, FUNC-005, FUNC-006 |
| [FEAT-003](FEAT-003-trace-engineering-relationships-and-change-impact.json) | Trace engineering relationships and change impact | FUNC-003, FUNC-008, FUNC-009, FUNC-010, FUNC-011 |
| [FEAT-004](FEAT-004-assess-engineering-model-conformance.json) | Assess engineering model conformance | FUNC-002, FUNC-012, FUNC-013 |
| [FEAT-005](FEAT-005-migrate-engineering-models-between-declared-profiles.json) | Migrate engineering models between declared profiles | FUNC-002, FUNC-012, FUNC-013, FUNC-014 |
| [FEAT-006](FEAT-006-inspect-compare-and-recover-retained-engineering-baselines.json) | Inspect, compare, and recover retained engineering baselines | FUNC-020, FUNC-021, FUNC-022 |
| [FEAT-007](FEAT-007-control-and-resume-engineering-changes.json) | Control and resume engineering changes | FUNC-023, FUNC-024, FUNC-025, FUNC-026 |
| [FEAT-008](FEAT-008-define-verification-and-record-observed-evidence.json) | Define verification and record observed evidence | FUNC-027, FUNC-028 |
| [FEAT-009](FEAT-009-assess-evidence-supporting-engineering-claims.json) | Assess evidence supporting engineering claims | FUNC-029, FUNC-030, FUNC-031 |
| [FEAT-010](FEAT-010-guide-engineering-model-authors.json) | Guide engineering model authors | FUNC-032, FUNC-033, FUNC-034, FUNC-028, FUNC-029, FUNC-031 |
| [FEAT-011](FEAT-011-apply-and-assess-engineering-lessons.json) | Apply and assess engineering lessons | FUNC-035, FUNC-036, FUNC-037, FUNC-038, FUNC-023, FUNC-026, FUNC-028, FUNC-029, FUNC-031 |

The save/revise capability remains bounded to engineering definitions. Guidance, model conformance, change control, and assurance have their own Features and reuse shared behavior where appropriate.

Describe the capability's purpose, scope, and externally meaningful outcomes.
Use a name that identifies the stakeholder capability and its subject; an action phrase such as "Inspect engineering definitions and their rationale" makes that meaning visible in repository navigation.
Use `description` to explain who can achieve what useful outcome, and `scope` to define the capability's boundaries.
Review these fields against the [REM System Design clarity criteria](../../../rem/models/system-design.md); names and scope must distinguish neighboring Features without promising capabilities outside the current definition.
Reference the [Functions](../functions/README.md) that realize it through `realized_by` relationships authored here (REM `realizedBy`).
Keep shared Functions in their own collection and derive the reverse Feature membership view.

[Requirements](../../requirements/README.md) own the obligations constraining the capability.
A Feature description does not replace those obligations or claim that they have been verified.
IR-owned `confirms` links establish the Feature's analysis basis; Scenario-owned `exercises` links describe its use.
Do not author inverse IR, SR, or Scenario lists in the Feature.

The [Feature schema](../../support/schemas/feature.schema.json) requires identity, type, title, draft status, description, explicit included and excluded scope, Function references, and sources.
Feature records do not include `open_questions`.
An early draft may have an empty `realized_by` list while SR analysis develops Functions. All current Features have explicit realization links.
5W2H remains mandatory for requirements; a Feature uses the capability description and scope instead of duplicating requirement analysis.
