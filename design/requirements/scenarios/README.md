# Scenarios

A Scenario is a first-class governed Requirement Analysis entity describing one concrete stakeholder-visible situation.
The [REM Scenario model](../../../rem/models/scenarios.md) owns its meaning, identity, lifecycle, and relationships; the [Scenario Analysis method](../../../rem/methods/scenario-analysis.md) owns the engineering procedure.
Its interaction describes stakeholder actions and observable system responses. Internal Functions, Modules, Interfaces, and implementation mechanisms belong to later design.

## Scenarios by owning IR

Each of these 35 Scenarios has been reviewed and confirmed as current requirement-analysis knowledge for its declared scope.
Each has exactly one owning IR and one primary Feature. The table is derived navigation; JSON records own the links and content.
These situations are analyst-derived from the requirements and selected profile decisions, not observed research or executed verification cases.
The [source register](../sources.md#src-complete-analysis) records their derivation, and the [requirements review](../README.md#review-outcome) states the assessment scope.

| Scenario | Situation | Owning IR | Primary Feature | Informs SRs |
| --- | --- | --- | --- | --- |
| [SCN-001](SCN-001-retrieve-a-saved-definition-in-a-later-session.json) | Retrieve a saved definition in a later session | IR-001 | FEAT-001 | SR-001, SR-002, SR-004 |
| [SCN-002](SCN-002-evolve-an-entity-while-retaining-its-identity.json) | Evolve an entity while retaining its identity | IR-001 | FEAT-002 | SR-002, SR-003 |
| [SCN-003](SCN-003-understand-the-current-definition-and-applicable-decision-rationale.json) | Understand the current definition and applicable decision rationale | IR-001 | FEAT-001 | SR-004, SR-005 |
| [SCN-004](SCN-004-recognize-unavailable-or-incomplete-engineering-knowledge.json) | Recognize unavailable or incomplete engineering knowledge | IR-001 | FEAT-001 | SR-001, SR-004, SR-005 |
| [SCN-005](SCN-005-save-an-engineering-definition-for-later-sessions.json) | Save an engineering definition for later sessions | IR-001 | FEAT-002 | SR-001, SR-002 |
| [SCN-006](SCN-006-record-decision-rationale-for-a-current-engineering-definition.json) | Record decision rationale for a current engineering definition | IR-001 | FEAT-002 | SR-005 |
| [SCN-007](SCN-007-apply-a-relationship-change-and-inspect-both-endpoint-views.json) | Apply a relationship change and inspect both endpoint views | IR-002 | FEAT-003 | SR-008, SR-009, SR-013 |
| [SCN-008](SCN-008-follow-responsibility-paths-within-a-selected-model-state.json) | Follow responsibility paths within a selected model state | IR-002 | FEAT-003 | SR-002, SR-008, SR-009 |
| [SCN-009](SCN-009-review-converging-requirement-and-function-responsibilities.json) | Review converging requirement and function responsibilities | IR-002 | FEAT-003 | SR-010, SR-014 |
| [SCN-010](SCN-010-investigate-possible-impact-of-a-proposed-engineering-change.json) | Investigate possible impact of a proposed engineering change | IR-002 | FEAT-003 | SR-009, SR-011 |
| [SCN-011](SCN-011-read-a-retained-model-under-its-original-governing-rules.json) | Read a retained model under its original governing rules | IR-005 | FEAT-004 | SR-012 |
| [SCN-012](SCN-012-locate-model-violations-before-relying-on-an-authored-state.json) | Locate model violations before relying on an authored state | IR-005 | FEAT-004 | SR-012, SR-013, SR-014 |
| [SCN-013](SCN-013-distinguish-structural-conformance-from-engineering-adequacy.json) | Distinguish structural conformance from engineering adequacy | IR-005 | FEAT-004 | SR-014 |
| [SCN-014](SCN-014-prepare-a-profile-migration-while-preserving-historical-meaning.json) | Prepare a profile migration while preserving historical meaning | IR-005 | FEAT-005 | SR-012, SR-013, SR-015 |
| [SCN-019](SCN-019-establish-an-identifiable-baseline-for-later-engineering-reliance.json) | Establish an identifiable baseline for later engineering reliance | IR-003 | FEAT-006 | SR-020 |
| [SCN-020](SCN-020-understand-what-changed-between-two-retained-engineering-states.json) | Understand what changed between two retained engineering states | IR-003 | FEAT-006 | SR-020, SR-021 |
| [SCN-021](SCN-021-recover-an-earlier-baseline-with-its-original-engineering-meaning.json) | Recover an earlier baseline with its original engineering meaning | IR-003 | FEAT-006 | SR-020, SR-022, SR-007 |
| [SCN-022](SCN-022-explain-an-adopted-change-from-its-recorded-transition.json) | Explain an adopted change from its recorded transition | IR-003 | FEAT-007 | SR-023, SR-004 |
| [SCN-023](SCN-023-resume-interrupted-work-from-recorded-change-context.json) | Resume interrupted work from recorded change context | IR-003 | FEAT-007 | SR-006, SR-007 |
| [SCN-024](SCN-024-determine-whether-a-proposed-action-is-already-authorized.json) | Determine whether a proposed action is already authorized | IR-003 | FEAT-007 | SR-007 |
| [SCN-025](SCN-025-retire-completed-material-while-preserving-current-reliance-and-history.json) | Retire completed material while preserving current reliance and history | IR-003 | FEAT-007 | SR-024, SR-007, SR-020 |
| [SCN-026](SCN-026-define-how-a-requirement-criterion-will-be-verified.json) | Define how a requirement criterion will be verified | IR-004 | FEAT-008 | SR-025 |
| [SCN-027](SCN-027-record-what-actually-happened-during-a-verification-assessment.json) | Record what actually happened during a verification assessment | IR-004 | FEAT-008 | SR-026 |
| [SCN-028](SCN-028-judge-a-claim-against-applicable-observations-and-uncovered-criteria.json) | Judge a claim against applicable observations and uncovered criteria | IR-004 | FEAT-009 | SR-027, SR-028, SR-007 |
| [SCN-029](SCN-029-reassess-earlier-claim-support-after-a-subject-or-criterion-changes.json) | Reassess earlier claim support after a subject or criterion changes | IR-004 | FEAT-009 | SR-027, SR-028, SR-029 |
| [SCN-031](SCN-031-derive-clear-requirements-and-system-definitions-with-canonical-guidance.json) | Derive clear requirements and system definitions with canonical guidance | IR-006 | FEAT-010 | SR-032, SR-033 |
| [SCN-032](SCN-032-correct-and-retire-engineering-definitions-using-their-governing-rules.json) | Correct and retire engineering definitions using their governing rules | IR-006 | FEAT-010 | SR-033, SR-003, SR-024, SR-007 |
| [SCN-033](SCN-033-select-authoring-guidance-after-a-profile-change.json) | Select authoring guidance after a profile change | IR-006 | FEAT-010 | SR-032, SR-033 |
| [SCN-034](SCN-034-assess-authoring-guidance-with-prepared-engineering-tasks.json) | Assess authoring guidance with prepared engineering tasks | IR-006 | FEAT-010 | SR-034, SR-026, SR-027, SR-028 |
| [SCN-035](SCN-035-distinguish-a-reusable-lesson-from-a-local-correction.json) | Distinguish a reusable lesson from a local correction | IR-007 | FEAT-011 | SR-035, SR-026, SR-027 |
| [SCN-036](SCN-036-prepare-a-lesson-based-improvement-for-controlled-adoption.json) | Prepare a lesson-based improvement for controlled adoption | IR-007 | FEAT-011 | SR-037, SR-023, SR-007 |
| [SCN-037](SCN-037-assess-an-improvement-during-the-next-comparable-activity.json) | Assess an improvement during the next comparable activity | IR-007 | FEAT-011 | SR-038, SR-026, SR-027, SR-028 |
| [SCN-038](SCN-038-reassess-a-lesson-after-recurrence-or-a-material-context-change.json) | Reassess a lesson after recurrence or a material context change | IR-007 | FEAT-011 | SR-036, SR-038, SR-029 |
| [SCN-039](SCN-039-consult-applicable-lessons-before-comparable-engineering-work.json) | Consult applicable lessons before comparable engineering work | IR-007 | FEAT-011 | SR-036, SR-007 |
| [SCN-040](SCN-040-define-architectural-responsibilities-with-canonical-guidance.json) | Define architectural responsibilities with canonical guidance | IR-006 | FEAT-010 | SR-032, SR-033 |

## Representation

Store one `<SCN-ID>-<title-slug>.json` per Scenario under the [entity naming convention](../../support/README.md#entity-naming-and-filenames).
Apply the [REM Scenario naming criteria](../../../rem/models/scenarios.md) to describe the stakeholder goal and distinguishing situation clearly.
JSON owns `id` and `title`; derive the readable filename from both, while relationships continue to reference the stable ID alone.
For example, `SCN-001` and `Retrieve a saved definition in a later session` produce `SCN-001-retrieve-a-saved-definition-in-a-later-session.json`.
Refining the title updates its filename; it preserves identity when the represented situation has the same engineering meaning.
The [Scenario schema](../../support/schemas/scenario.schema.json) requires `actor`, `goal`, `context`, `trigger`, `preconditions`, `interaction`, `expected_outcome`, `alternatives`, and `failures`.
Each ordered interaction entry has `actor` and `action`; an action may describe an observable system response.
Alternatives and failures use `condition` and `outcome`. Alternatives still achieve the goal; failures prevent or limit it and describe the observable result or handling.
For SCN-004, an honest report of unavailable information achieves the diagnostic goal. Missing or misleading reporting fails that goal.
Empty preconditions, alternatives, or failures mean none are recorded, not that their absence has been proved.
Sources retain the analysis basis. Apply the [single consequential question rule](../../../rem/methods/requirement-analysis.md#keep-one-consequential-open-question) to unresolved Scenario analysis.
Omit `open_questions` when none remains. When present, the array contains exactly one nonblank question whose answer matters to the Scenario's meaning, scope, or outcomes.
Ask that question before any follow-up; do not combine unrelated decisions into one entry or hide uncertainty merely to satisfy the count.

Exactly one IR authors a `confirms` reference to each Scenario. This is the authoritative ownership relationship; there is no duplicate `ir_id` field or additional requirement parent.
The ownership reference does not itself set the Scenario's lifecycle state.
The Scenario authors `exercises` for its one primary Feature and `informs` for its SRs; derive inverse views.
The `exercises` array has at most one entry. During drafting it may be empty; a `confirmed` Scenario requires exactly one entry, and this profile retains that primary Feature when it becomes `obsolete`.
The `informs` array may be empty while system obligations are being derived, including after Scenario confirmation.
SRs continue to belong to exactly one IR regardless of how many Scenarios inform them.

The lifecycle is `draft → confirmed → obsolete`. Confirmation accepts the stakeholder situation as current analysis knowledge; it does not approve Requirements, implementation, or satisfaction.
Schema validation checks the allowed states and content shape. Engineering review must establish clear meaning, appropriate outcomes, and valid state transitions.

## SR reconciliation

Each confirmed Scenario's material outcomes were reconciled against its linked SR obligations and acceptance criteria. Cross-IR links reuse shared retention, identity, validation, change-authority, and evidence obligations without adding another requirement parent.
The [requirements index](../README.md) locates the complete SR set; the [source register](../sources.md#src-complete-analysis) records the selected boundaries.

The original IR-001 situations retain their stakeholder meanings: SCN-001 and SCN-003 concern inspection, SCN-002 revision, SCN-004 recognition of gaps, SCN-005 saving, and SCN-006 recording rationale.
Assessment Scenarios treat correctly reported negative, mixed, or unestablished underlying results as valid assessment outcomes when that matches their stated goal. Missing basis or misleading reporting can still prevent that goal.

Before declaring an IR's Requirement Analysis complete, every confirmed Scenario must be covered by the resulting SR set or an explicit conclusion that it introduces no additional obligation.
The optional `coverage_note` can record that conclusion when needed; it is analysis, not verification evidence. An empty `informs` list or absence of an open question alone cannot establish coverage.
Candidate obligations proceed through SR analysis. SR-owned `confirms` and `constrains` relationships establish the required behavior and restrictions; a Scenario does not directly define a Function.
Architecture allocation and verification evidence remain later engineering work.
