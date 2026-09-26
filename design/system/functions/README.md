# Functions

A Function represents logical system behavior, independently of its physical implementation wherever practical.
It may contribute to several [Features](../features/README.md).

The collection uses one `<FUNC-ID>-<title-slug>.json` file per Function under the [asset naming convention](../../support/README.md#entity-naming-and-filenames).
Names and behavior descriptions belong in the entity content, independently of its stable identity.
The current analysis defines 33 Functions. The confirming and constraining SR views below are derived from requirement references; they are not separately authored Function fields.

| Function | Logical behavior | Confirming SRs | Constraining SRs |
| --- | --- | --- | --- |
| [FUNC-001](FUNC-001-retain-engineering-definition.json) | Retain engineering definition | SR-001 | — |
| [FUNC-002](FUNC-002-check-entity-identity-presence-and-uniqueness.json) | Check entity identity presence and uniqueness | SR-002, SR-013 | SR-015 |
| [FUNC-003](FUNC-003-resolve-engineering-entity-by-stable-id.json) | Resolve engineering entity by stable ID | SR-002, SR-008, SR-009 | — |
| [FUNC-004](FUNC-004-retrieve-engineering-definition-from-selected-model-state.json) | Retrieve engineering definition from selected model state | SR-001, SR-004 | SR-012 |
| [FUNC-005](FUNC-005-revise-engineering-entity-while-preserving-identity.json) | Revise engineering entity while preserving identity | SR-003 | — |
| [FUNC-006](FUNC-006-retain-applicable-decision-rationale.json) | Retain applicable decision rationale | SR-005 | — |
| [FUNC-007](FUNC-007-present-current-engineering-definition-and-applicable-rationale.json) | Present current engineering definition and applicable rationale | SR-004, SR-005 | — |
| [FUNC-008](FUNC-008-author-typed-engineering-relationships.json) | Author typed engineering relationships | SR-008 | SR-013 |
| [FUNC-009](FUNC-009-traverse-selected-engineering-relationships.json) | Traverse selected engineering relationships | SR-009 | SR-008, SR-010, SR-011 |
| [FUNC-010](FUNC-010-assess-declared-architectural-allocation-consistency.json) | Assess declared architectural allocation consistency | SR-010 | SR-014 |
| [FUNC-011](FUNC-011-report-possible-change-impact.json) | Report possible change impact | SR-011 | — |
| [FUNC-012](FUNC-012-interpret-a-model-with-its-declared-metamodel.json) | Interpret a model with its declared metamodel | SR-012 | SR-013, SR-015 |
| [FUNC-013](FUNC-013-diagnose-model-conformance-against-declared-rules.json) | Diagnose model conformance against declared rules | SR-013 | SR-014, SR-015 |
| [FUNC-014](FUNC-014-prepare-a-model-migration-candidate.json) | Prepare a model migration candidate | SR-015 | — |
| [FUNC-020](FUNC-020-establish-and-inspect-retained-engineering-baselines.json) | Establish and inspect retained engineering baselines | SR-020 | — |
| [FUNC-021](FUNC-021-compare-selected-retained-engineering-states.json) | Compare selected retained engineering states | SR-021 | — |
| [FUNC-022](FUNC-022-recover-the-recorded-content-of-a-retained-baseline.json) | Recover the recorded content of a retained baseline | SR-022 | SR-007 |
| [FUNC-023](FUNC-023-record-controlled-change-transitions-and-provenance.json) | Record controlled change transitions and provenance | SR-023 | SR-007 |
| [FUNC-024](FUNC-024-assess-and-apply-retirement-of-current-view-material.json) | Assess and apply retirement of current-view material | SR-024 | SR-007 |
| [FUNC-025](FUNC-025-retain-and-retrieve-activity-specific-change-context.json) | Retain and retrieve activity-specific change context | SR-006 | SR-007 |
| [FUNC-026](FUNC-026-determine-applicable-authority-before-governed-actions.json) | Determine applicable authority before governed actions | SR-007 | — |
| [FUNC-027](FUNC-027-retain-criterion-based-verification-definitions.json) | Retain criterion-based verification definitions | SR-025 | — |
| [FUNC-028](FUNC-028-retain-actual-verification-observations-and-provenance.json) | Retain actual verification observations and provenance | SR-026 | — |
| [FUNC-029](FUNC-029-assess-evidence-applicability-to-a-declared-claim.json) | Assess evidence applicability to a declared claim | SR-027, SR-029 | — |
| [FUNC-030](FUNC-030-expose-claim-criterion-coverage-and-contradictory-evidence.json) | Expose claim criterion coverage and contradictory evidence | SR-028, SR-029 | — |
| [FUNC-031](FUNC-031-record-scoped-engineering-judgments-and-their-basis.json) | Record scoped engineering judgments and their basis | SR-028, SR-029 | SR-007 |
| [FUNC-032](FUNC-032-select-canonical-guidance-for-an-authoring-activity.json) | Select canonical guidance for an authoring activity | SR-032 | — |
| [FUNC-033](FUNC-033-explain-engineering-authoring-and-correction-steps.json) | Explain engineering authoring and correction steps | SR-033 | — |
| [FUNC-034](FUNC-034-assess-authoring-guidance-against-prepared-task-outcomes.json) | Assess authoring guidance against prepared task outcomes | SR-034 | — |
| [FUNC-035](FUNC-035-characterize-a-reusable-lesson-from-an-engineering-finding.json) | Characterize a reusable lesson from an engineering finding | SR-035 | — |
| [FUNC-036](FUNC-036-select-lessons-applicable-to-planned-engineering-work.json) | Select lessons applicable to planned engineering work | SR-036 | — |
| [FUNC-037](FUNC-037-formulate-an-accountable-engineering-improvement-proposal.json) | Formulate an accountable engineering improvement proposal | SR-037 | — |
| [FUNC-038](FUNC-038-assess-observed-effects-of-an-adopted-engineering-improvement.json) | Assess observed effects of an adopted engineering improvement | SR-038 | — |

Describe inputs, outputs, relevant state, and failure behavior.
Prefer an action and its engineering subject, adding a distinguishing condition where it matters: "Retrieve engineering definition from selected model state" identifies both the returned content and its state boundary.
Apply the [REM System Design clarity criteria](../../../rem/models/system-design.md) to distinguish neighboring responsibilities. For example, resolution identifies an entity; retrieval obtains its content; revision changes a definition; retention preserves supplied content.
Make "current" relative to the selected model state and identify the authoring profile behind "supported" behavior.
Author an `allocated_to` reference to the accountable [Module](../../architecture/modules/README.md) (REM `allocatedTo`).
If architecture deliberately leaves a Function unallocated, record `unallocated_reason` with that decision and its limits instead.
The draft profile accepts exactly one of those fields, and at most one accountable Module per Function. This does not settle wider REM allocation cardinalities.
All current Functions deliberately defer allocation; no Module or AR coverage is claimed.

Feature membership is derived from Feature-owned `realized_by` references.
Trace applicable constraints from [Requirements](../../requirements/README.md).
SR-owned `confirms` references establish the logical behavior through requirement analysis; a Scenario's candidate behavior is not its authoritative Function definition.

The [Function schema](../../support/schemas/function.schema.json) requires identity, type, title, draft status, description, inputs, preconditions, outputs, behavior, failure behavior, an allocation disposition, and sources.
Function records do not include `open_questions`.

Implementation references identify where the behavior is realized.
The logical behavior remains understandable without reproducing implementation internals.
