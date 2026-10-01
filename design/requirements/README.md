# Requirement Analysis

Requirements express what must become or remain true.
REM separates the initial need, the system obligation, and its allocation to architectural responsibility.
The [REM requirement model](../../rem/models/requirements.md) owns the general semantics.
Apply the [requirement-analysis method](../../rem/methods/requirement-analysis.md) when authoring these records.

| Type | Meaning | Containment |
| --- | --- | --- |
| Initial Requirement (IR) | Durable stakeholder, business, product, regulatory, operational, or engineering need | Root requirement |
| System Requirement (SR) | Verifiable obligation imposed on the system as a whole | Exactly one IR parent |
| Allocated Requirement (AR) | Lower-level obligation derived from an SR and allocated to architecture | Exactly one SR parent |

## Analysis coverage

The current draft contains 10 IRs, 76 SRs, 22 Features, 73 Functions, and 80 Scenarios.
The original seven-IR engineering-model analysis is extended by [published-product coverage](published-products.md): explicit CLI operations, portable guided engineering activities, and trustworthy compatible tool distribution.
IRs, SRs, Features, and Functions retain `draft` status; 70 Scenarios are confirmed, including eight assessed workflow and five customer-browser Scenarios; five revised and five local-history Scenarios remain draft.
These are bounded definition and coverage conclusions, not requirement approval, implemented behavior, or a complete migration of existing product contracts.
Current [Requirement Analysis](../../rem/methods/requirement-analysis.md), [Scenario Analysis](../../rem/methods/scenario-analysis.md), and [Functional Analysis](../../rem/methods/functional-analysis.md) define the method; the source register distinguishes each derivation pass.

| IR | Need | SRs | Scenarios | Features |
| --- | --- | ---: | ---: | ---: |
| [IR-001](IR-001-preserve-engineering-knowledge-across-sessions/ir.json) | Preserve engineering knowledge across sessions | 5 | 6 | 2 |
| [IR-002](IR-002-trace-engineering-obligations-and-responsibilities/ir.json) | Trace engineering obligations and responsibilities | 8 | 8 | 2 |
| [IR-003](IR-003-control-engineering-changes-and-recover-prior-states/ir.json) | Control engineering changes and recover prior states | 11 | 11 | 3 |
| [IR-004](IR-004-assess-engineering-claims-using-applicable-evidence/ir.json) | Assess engineering claims using applicable evidence | 5 | 4 | 2 |
| [IR-005](IR-005-keep-engineering-models-valid-and-consistently-interpreted/ir.json) | Keep engineering models valid and consistently interpreted | 4 | 4 | 2 |
| [IR-006](IR-006-guide-people-and-agents-in-authoring-engineering-models/ir.json) | Guide people and agents in authoring engineering models | 3 | 5 | 1 |
| [IR-007](IR-007-improve-engineering-practice-from-recorded-lessons/ir.json) | Improve engineering practice from recorded lessons | 4 | 5 | 1 |
| [IR-008](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/ir.json) | Operate on recorded engineering work through reliable explicit commands | 9 | 10 | 3 |
| [IR-009](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/ir.json) | Carry out portable guided engineering work across the project lifecycle | 12 | 16 | 3 |
| [IR-010](IR-010-obtain-trustworthy-compatible-rigorloop-tools/ir.json) | Obtain trustworthy compatible RigorLoop tools | 15 | 11 | 3 |

Counts and navigation are derived from the JSON records; those records own identities, containment, and relationships.
Every requirement records all seven 5W2H answers, and SRs define observable acceptance criteria and attributable scope.
The [Scenario index](scenarios/README.md), [Features](../system/features/README.md), and [Functions](../system/functions/README.md) expose the connected model.

## Local operational-history refinement

The [local operational-history analysis](sources.md#src-local-operational-analysis) treats the proposal as RR input and refines IR-003 and IR-008 without adding an IR. It adds five draft Scenarios (SCN-070–074), five SRs (SR-074–078), FEAT-021 and four unallocated Functions (FUNC-074–077), and reconciles continuing records. Five materially revised Scenarios return to draft pending reassessment; earlier confirmation remains evidence only for their original subjects. SR-042–045 no longer use old allocation arguments as current coverage claims. Existing ARs and realization facets still require architectural reconciliation before adoption.

## System requirements

A shared SR retains exactly one IR parent even when Scenarios owned by other IRs use it.
SR-014 is a constraint on existing assessment behavior; it does not create an artificial Function.

The [requirement-first workflow analysis](workflow-refactor.md) refines IR-009, adds SR-079–083 and SCN-075–082, and reconciles shared guidance and assessment criteria. The [source register](sources.md#src-workflow-requirement-review) identifies the author-assessed requirement basis and SCN-075–082 confirmation under the Constitution exception. The [integrated design](../architecture/README.md#requirement-first-workflow-composition) now supplies Function and AR proposals; detailed boundary design, integrated review and coordinated adoption remain outstanding; no independent review or product activation is claimed.

| SR | Parent | System obligation |
| --- | --- | --- |
| [SR-001](IR-001-preserve-engineering-knowledge-across-sessions/SR-001-retain-engineering-definitions-across-sessions/sr.json) | IR-001 | Retain engineering definitions across sessions |
| [SR-002](IR-001-preserve-engineering-knowledge-across-sessions/SR-002-unambiguous-entity-identity/sr.json) | IR-001 | Unambiguous entity identity |
| [SR-003](IR-001-preserve-engineering-knowledge-across-sessions/SR-003-preserve-identity-through-entity-evolution/sr.json) | IR-001 | Preserve identity through entity evolution |
| [SR-004](IR-001-preserve-engineering-knowledge-across-sessions/SR-004-understand-current-definitions-without-history-replay/sr.json) | IR-001 | Understand current definitions without history replay |
| [SR-005](IR-001-preserve-engineering-knowledge-across-sessions/SR-005-retain-applicable-decision-rationale/sr.json) | IR-001 | Retain applicable decision rationale |
| [SR-006](IR-003-control-engineering-changes-and-recover-prior-states/SR-006-resume-changes-from-recorded-work-context/sr.json) | IR-003 | Resume changes from recorded work context |
| [SR-007](IR-003-control-engineering-changes-and-recover-prior-states/SR-007-preserve-human-authority-over-governed-decisions/sr.json) | IR-003 | Preserve human authority over governed decisions |
| [SR-008](IR-002-trace-engineering-obligations-and-responsibilities/SR-008-author-engineering-relationships-once-and-derive-inverse-views/sr.json) | IR-002 | Author engineering relationships once and derive inverse views |
| [SR-009](IR-002-trace-engineering-obligations-and-responsibilities/SR-009-traverse-selected-engineering-relationships-with-explicit-completeness/sr.json) | IR-002 | Traverse selected engineering relationships with explicit completeness |
| [SR-010](IR-002-trace-engineering-obligations-and-responsibilities/SR-010-expose-gaps-and-conflicts-in-architectural-allocation/sr.json) | IR-002 | Expose gaps and conflicts in architectural allocation |
| [SR-011](IR-002-trace-engineering-obligations-and-responsibilities/SR-011-explain-possible-change-impact-through-engineering-paths/sr.json) | IR-002 | Explain possible change impact through engineering paths |
| [SR-012](IR-005-keep-engineering-models-valid-and-consistently-interpreted/SR-012-interpret-model-states-using-their-identified-metamodel/sr.json) | IR-005 | Interpret model states using their identified metamodel |
| [SR-013](IR-005-keep-engineering-models-valid-and-consistently-interpreted/SR-013-diagnose-violations-of-declared-model-rules/sr.json) | IR-005 | Diagnose violations of declared model rules |
| [SR-014](IR-005-keep-engineering-models-valid-and-consistently-interpreted/SR-014-separate-model-conformance-results-from-engineering-judgments/sr.json) | IR-005 | Separate model conformance results from engineering judgments |
| [SR-015](IR-005-keep-engineering-models-valid-and-consistently-interpreted/SR-015-prepare-explicit-model-migrations-without-rewriting-history/sr.json) | IR-005 | Prepare explicit model migrations without rewriting history |
| [SR-020](IR-003-control-engineering-changes-and-recover-prior-states/SR-020-identify-and-preserve-coherent-engineering-baselines/sr.json) | IR-003 | Identify and preserve coherent engineering baselines |
| [SR-021](IR-003-control-engineering-changes-and-recover-prior-states/SR-021-compare-retained-engineering-states-with-their-original-meaning/sr.json) | IR-003 | Compare retained engineering states with their original meaning |
| [SR-022](IR-003-control-engineering-changes-and-recover-prior-states/SR-022-recover-retained-baselines-without-altering-historical-meaning/sr.json) | IR-003 | Recover retained baselines without altering historical meaning |
| [SR-023](IR-003-control-engineering-changes-and-recover-prior-states/SR-023-record-controlled-transitions-and-their-engineering-provenance/sr.json) | IR-003 | Record controlled transitions and their engineering provenance |
| [SR-024](IR-003-control-engineering-changes-and-recover-prior-states/SR-024-retire-current-view-material-only-after-resolving-surviving-dependencies/sr.json) | IR-003 | Retire current-view material only after resolving surviving dependencies |
| [SR-025](IR-004-assess-engineering-claims-using-applicable-evidence/SR-025-define-verification-against-identifiable-requirement-criteria/sr.json) | IR-004 | Define verification against identifiable requirement criteria |
| [SR-026](IR-004-assess-engineering-claims-using-applicable-evidence/SR-026-retain-actual-verification-observations-and-execution-state/sr.json) | IR-004 | Retain actual verification observations and execution state |
| [SR-027](IR-004-assess-engineering-claims-using-applicable-evidence/SR-027-assess-evidence-applicability-to-the-claimed-engineering-state/sr.json) | IR-004 | Assess evidence applicability to the claimed engineering state |
| [SR-028](IR-004-assess-engineering-claims-using-applicable-evidence/SR-028-record-scoped-engineering-judgments-from-criterion-coverage/sr.json) | IR-004 | Record scoped engineering judgments from criterion coverage |
| [SR-029](IR-004-assess-engineering-claims-using-applicable-evidence/SR-029-reassess-claim-support-after-engineering-changes/sr.json) | IR-004 | Reassess claim support after engineering changes |
| [SR-032](IR-006-guide-people-and-agents-in-authoring-engineering-models/SR-032-select-applicable-canonical-authoring-guidance/sr.json) | IR-006 | Select applicable canonical authoring guidance |
| [SR-033](IR-006-guide-people-and-agents-in-authoring-engineering-models/SR-033-guide-bounded-engineering-authoring-and-correction/sr.json) | IR-006 | Guide bounded engineering authoring and correction |
| [SR-034](IR-006-guide-people-and-agents-in-authoring-engineering-models/SR-034-assess-guidance-using-semantic-authoring-outcomes/sr.json) | IR-006 | Assess guidance using semantic authoring outcomes |
| [SR-035](IR-007-improve-engineering-practice-from-recorded-lessons/SR-035-characterize-reusable-engineering-lessons-from-supported-findings/sr.json) | IR-007 | Characterize reusable engineering lessons from supported findings |
| [SR-036](IR-007-improve-engineering-practice-from-recorded-lessons/SR-036-present-applicable-lessons-when-preparing-engineering-work/sr.json) | IR-007 | Present applicable lessons when preparing engineering work |
| [SR-037](IR-007-improve-engineering-practice-from-recorded-lessons/SR-037-prepare-accountable-improvements-for-controlled-adoption/sr.json) | IR-007 | Prepare accountable improvements for controlled adoption |
| [SR-038](IR-007-improve-engineering-practice-from-recorded-lessons/SR-038-assess-improvement-effects-at-comparable-opportunities/sr.json) | IR-007 | Assess improvement effects at comparable opportunities |
| [SR-040](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/SR-040-preserve-explicit-command-admission-and-independent-interface-contracts/sr.json) | IR-008 | Preserve explicit command admission and independent interface contracts |
| [SR-041](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/SR-041-return-coherent-explicitly-selected-engineering-records-and-subject-identities/sr.json) | IR-008 | Return coherent explicitly selected engineering records and subject identities |
| [SR-042](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/SR-042-enforce-the-current-registered-record-contract-without-inventing-decisions/sr.json) | IR-008 | Enforce the current registered record contract without inventing decisions |
| [SR-043](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/SR-043-construct-lossless-updates-from-explicit-engineering-decisions/sr.json) | IR-008 | Construct lossless updates from explicit engineering decisions |
| [SR-044](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/SR-044-publish-record-updates-with-fresh-basis-and-coherent-durable-outcomes/sr.json) | IR-008 | Publish record updates with fresh basis and coherent durable outcomes |
| [SR-045](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/SR-045-recover-interrupted-record-transactions-without-guessing-or-replaying-decisions/sr.json) | IR-008 | Recover interrupted record transactions without guessing or replaying decisions |
| [SR-046](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/SR-046-return-bounded-faithful-command-outcomes-and-selected-explanations/sr.json) | IR-008 | Return bounded faithful command outcomes and selected explanations |
| [SR-047](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/SR-047-keep-local-command-diagnostics-private-and-semantically-independent/sr.json) | IR-008 | Keep local command diagnostics private and semantically independent |
| [SR-050](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-050-expose-distinct-published-engineering-capabilities/sr.json) | IR-009 | Expose distinct published engineering capabilities |
| [SR-051](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-051-prepare-project-portable-engineering-invocations/sr.json) | IR-009 | Prepare project-portable engineering invocations |
| [SR-052](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-052-select-complete-resources-for-the-invoked-engineering-path/sr.json) | IR-009 | Select complete resources for the invoked engineering path |
| [SR-053](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-053-guide-specialist-engineering-work-with-usable-scoped-outputs/sr.json) | IR-009 | Guide specialist engineering work with usable scoped outputs |
| [SR-054](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-054-coordinate-engineering-handoffs-using-applicable-work-and-assessment-state/sr.json) | IR-009 | Coordinate engineering handoffs using applicable work and assessment state |
| [SR-055](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-055-separate-portable-output-from-governed-recording/sr.json) | IR-009 | Separate portable output from governed recording |
| [SR-056](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-056-preserve-guidance-meaning-and-evidence-quality-across-reading-paths/sr.json) | IR-009 | Preserve guidance meaning and evidence quality across reading paths |
| [SR-060](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-060-produce-faithful-supported-product-candidates/sr.json) | IR-010 | Produce faithful supported product candidates |
| [SR-061](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-061-generate-candidates-deterministically-outside-active-installations/sr.json) | IR-010 | Generate candidates deterministically outside active installations |
| [SR-062](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-062-bind-artifact-metadata-to-actual-candidate-bytes/sr.json) | IR-010 | Bind artifact metadata to actual candidate bytes |
| [SR-063](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-063-qualify-the-actual-executable-cli-package/sr.json) | IR-010 | Qualify the actual executable CLI package |
| [SR-064](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-064-acquire-and-verify-a-supported-installation-candidate/sr.json) | IR-010 | Acquire and verify a supported installation candidate |
| [SR-065](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-065-install-verified-units-within-explicit-safe-replacement-boundaries/sr.json) | IR-010 | Install verified units within explicit safe replacement boundaries |
| [SR-066](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-066-report-installation-plans-and-outcomes-without-exposing-private-data/sr.json) | IR-010 | Report installation plans and outcomes without exposing private data |
| [SR-067](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-067-select-compatible-release-identity-and-supported-execution-scope/sr.json) | IR-010 | Select compatible release identity and supported execution scope |
| [SR-068](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-068-prepare-release-projections-from-one-authoritative-profile/sr.json) | IR-010 | Prepare release projections from one authoritative profile |
| [SR-069](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-069-qualify-the-exact-prepared-release-candidate/sr.json) | IR-010 | Qualify the exact prepared release candidate |
| [SR-070](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-070-publish-only-the-authorized-immutable-candidate/sr.json) | IR-010 | Publish only the authorized immutable candidate |
| [SR-071](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-071-record-observed-public-release-outcomes-and-bounded-closeout/sr.json) | IR-010 | Record observed public release outcomes and bounded closeout |
| [SR-072](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-072-recover-publication-failures-without-overwriting-public-history/sr.json) | IR-010 | Recover publication failures without overwriting public history |
| [SR-073](IR-010-obtain-trustworthy-compatible-rigorloop-tools/SR-073-coordinate-supported-routine-releases-around-one-candidate-approval/sr.json) | IR-010 | Coordinate supported routine releases around one candidate approval |
| [SR-074](IR-003-control-engineering-changes-and-recover-prior-states/SR-074-create-coherent-recoverable-operational-backups/sr.json) | IR-003 | Create coherent recoverable operational backups |
| [SR-075](IR-003-control-engineering-changes-and-recover-prior-states/SR-075-restore-operational-history-without-changing-its-original-meaning/sr.json) | IR-003 | Restore operational history without changing its original meaning |
| [SR-076](IR-003-control-engineering-changes-and-recover-prior-states/SR-076-transfer-retained-operational-work-with-explicit-project-association/sr.json) | IR-003 | Transfer retained operational work with explicit project association |
| [SR-077](IR-003-control-engineering-changes-and-recover-prior-states/SR-077-migrate-operational-records-with-explicit-preservation-and-disposition/sr.json) | IR-003 | Migrate operational records with explicit preservation and disposition |
| [SR-078](IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/SR-078-query-retained-change-history-by-selected-engineering-subject/sr.json) | IR-008 | Query retained change history by selected engineering subject |
| [SR-079](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-079-reconcile-incoming-requests-with-existing-requirement-owners/sr.json) | IR-009 | Reconcile incoming requests with existing requirement owners |
| [SR-080](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-080-establish-the-reviewed-requirement-basis-before-dependent-design/sr.json) | IR-009 | Establish the reviewed requirement basis before dependent design |
| [SR-081](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-081-preserve-distinct-authoring-ownership-and-integrated-design-assessment/sr.json) | IR-009 | Preserve distinct authoring ownership and integrated design assessment |
| [SR-082](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-082-require-one-whole-change-review-gate-after-checked-implementation/sr.json) | IR-009 | Require one whole-change review gate after checked implementation |
| [SR-083](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-083-adopt-replacement-workflow-contracts-without-reinterpreting-history/sr.json) | IR-009 | Adopt replacement workflow contracts without reinterpreting history |

The [architecture model](../architecture/README.md) retains primary Module allocations for 64 Functions; four local-history Functions await allocation. Its 51 ARs comprise ten from the first detailed pilot—nine beneath IR-001 and shared interpretation AR-010 beneath SR-012 in IR-005—and 18 beneath IR-008's SR-040 through SR-047, plus 14 workflow ARs beneath SR-079–083.
The [CLI cooperation view](../architecture/views/browser/index.html#cooperation) summarizes how those product obligations relate to their Scenarios, Functions, Modules, and Interfaces. Allocation for the remaining SRs is deferred; draft allocation does not establish implementation or satisfaction.
The [parent-boundary cooperation view](../architecture/views/browser/index.html#scenarios) adds selected Interface contributions for SCN-019, SCN-053, and SCN-066. These contracts preserve the existing Scenario and requirement definitions and introduce no new ARs or allocation changes. State acquisition, guidance, authority, and evidence support each retain their declared limits; their existence does not establish complete Scenario satisfaction.
The [original question resolutions](sources.md#src-question-resolution) remain the selected scope basis; the decomposition adds assessable obligations and logical behavior without inventing new service targets or authority policy.

## Review outcome

This system-level analysis review describes the subject retained at repository revision `5cf0c7b6`, before architectural allocations were added.
The [architecture review](../architecture/README.md#review-and-validation) describes the later initial allocation work. The [published-product review](published-products.md#review-and-validation) identifies the subsequent extended model, preservation checks, and its limits.

The review covered the seven IR needs, their SR acceptance outcomes, Feature boundaries, Scenario goals and outcomes, and Function inputs, behavior, outputs, and failures.
Independent review groups covered IR-001, IR-002/005, IR-003/004, and IR-006/007, followed by cross-domain reconciliation.
Material findings were resolved before Scenario confirmation: selected-state profile interpretation, interrupted or changed-state relationship edits, and classification of adverse observations versus failure of an assessment itself.
No consequential open question remains recorded for this declared analysis scope. This does not preclude new needs or questions during architecture, implementation, or use.

The following direct checks passed on the reviewed model:

```bash
python3 tests/engineering/validation/requirement_schema_tests.py
python3 tests/engineering/validation/system_design_schema_tests.py
```

The requirement suite passed 13 tests; the system/model suite passed 18 tests, covering shape, identity, names, containment, typed references, ownership, source IDs, and required analysis connections.
Semantic coverage was reviewed separately; graph connectivity and passing schemas do not establish requirement satisfaction.
CI was not run, and the existing repository contracts retain authority over current product behavior.

Review subject digest: `ac16ae4d585d0ef5544ef91cbcdde40897e40dcf61be6c604eb13e654dc09461`. This SHA-256 covers the sorted repository-relative paths and SHA-256 content digests of the 118 entity JSON records under `design/` at `5cf0c7b6`, excluding schemas. It is retained as the identity of that earlier review subject, not relabeled as a digest of the later architecture draft.

## File placement

```text
requirements/
├── scenarios/
│   └── SCN-001-retrieve-a-saved-definition-in-a-later-session.json
└── IR-001-preserve-engineering-knowledge-across-sessions/
    ├── ir.json
    └── SR-001-retain-engineering-definitions-across-sessions/
        ├── sr.json
        └── AR-001-retain-accepted-definitions-beyond-the-authoring-session.json
```

This excerpt shows the selected naming convention using current records.
The index above lists all IRs and SRs; the [architecture convergence view](../architecture/README.md#requirement-and-function-convergence) lists the 28 ARs and their derived parents and allocations.

## Directory naming

This repository stores each IR in `<IR-ID>-<title-slug>/ir.json` and each SR in `<SR-ID>-<title-slug>/sr.json` beneath its owning IR.
The convention applies to these draft collections and implements [REM's naming and location guidance](../../rem/models/operational-support.md#naming-and-location).
It is a repository representation choice, not a universal REM requirement.

| Part | Authoritative source | Rule |
| --- | --- | --- |
| Identity | JSON `id` | Preserve the ID; the directory prefix must match it |
| Display name | JSON `title` | Express the need or obligation clearly |
| Directory suffix | Derived from `title` | Keep a readable, consistently normalized label |
| Requirement filename | Record kind | Use `ir.json` or `sr.json` |

Derive the suffix by lowercasing the full title, replacing each run of characters other than letters or digits with one hyphen, and trimming leading or trailing hyphens.
Preserve word order and retain all words; do not introduce a separately maintained `slug` field or silently abbreviate the title.
For example, `IR-001` and `Preserve engineering knowledge across sessions` produce `IR-001-preserve-engineering-knowledge-across-sessions`.

The suffix must be nonempty, and distinct requirements must retain distinct IDs even when their titles match.
Before a move, check that the target location is available; do not overwrite an existing directory or assign a new ID to bypass a collision.
If a name cannot be represented within the storage system's limits, resolve that representation issue explicitly.

Refine the title and rename its directory together when the normalized suffix changes.
Preserve the requirement's identity, statement, and parentage unless a semantic change is separately intended.
Use stable IDs for engineering relationships, and update current path-based links and consumers during the rename.
Historical references retain the paths and subjects belonging to their recorded revisions.

## Parentage

Directory containment is the selected authoritative parent relationship.
A separately authored parent field would duplicate that fact.

Each SR belongs to exactly one IR directory, and each AR belongs to exactly one SR directory.
An IR may contain several SRs, and an SR may contain several ARs.
Do not place copies of the same requirement under different parents; source references do not create another parent.

Entity identities remain stable independently of their parent, display name, and physical path.
The requirement hierarchy has no cycles.
Renaming an IR directory leaves its SRs under the same IR identity.
Moving an SR into a different IR changes its parentage and requires reviewing its derivation.

Scenarios are governed Requirement Analysis entities in the separate `scenarios/` collection, outside this requirement tree.
Each Scenario has exactly one owning IR, authored through that IR's `confirms` reference; there is no separately authored Scenario parent field.
This ownership reference does not move a Scenario from `draft` to `confirmed`.

## Record content and schemas

JSON is the selected authoring representation for this first draft, not a requirement imposed by REM.
The [IR schema](../support/schemas/ir.schema.json) and [SR schema](../support/schemas/sr.schema.json) define two self-contained JSON Schema Draft 2020-12 documents.
Each contains its own field definitions, including analysis and sources; no shared or separate 5W2H schema is needed.
Field names use `snake_case`.

Both record types require the following root fields:

| Content | Purpose |
| --- | --- |
| `id`, `title` | Stable entity identity and editable display name |
| `type` | `initial-requirement` for an IR or `system-requirement` for an SR |
| `status` | `draft`, the only state currently defined; no approval or satisfaction is implied |
| `statement` | Authoritative initial need for an IR, or system obligation for an SR |
| `analysis` | `method: "5W2H"` and the seven structured answers below |
| `assumptions` | Provisional premises relied on during analysis |
| `constraints` | Additional imposed restrictions on the need or obligation |
| `sources` | Nonempty list of attributed source references |

An SR also requires a nonempty `acceptance_criteria` list describing observable expected outcomes.
The seven analysis objects and their required and optional fields are:

| Object under `analysis` | Required fields | Optional fields |
| --- | --- | --- |
| `what` | `problem`, `desired_outcome` | — |
| `why` | `rationale` | `value` list |
| `who` | Nonempty `stakeholders` list | `affected_users` list |
| `when` | Nonempty `conditions` list | `frequency` |
| `where` | Nonempty `contexts` list | — |
| `how` | `approach` | — |
| `how_much` | `scope` | `scale`, `limits` list |

Text values, including items in text lists, must be nonblank; `null` is not accepted.
The required root lists `assumptions` and `constraints` may be empty, as may the optional 5W2H lists when present.
The root field `open_questions` is optional. When present, it contains exactly one nonblank entry (`minItems: 1`, `maxItems: 1`).
Apply the [REM question-selection rule](../../rem/methods/requirement-analysis.md#keep-one-consequential-open-question): retain a specific question whose answer affects meaning, scope, derivation, or acceptance, and identify what decision or evidence is needed.
Omit `open_questions` when no such question remains; an empty list is rejected. Schema validation cannot judge whether a question is valuable.
Ask the most consequential unresolved question first and resolve it before asking the next. Do not bundle independent questions or hide unresolved issues to satisfy the limit.
Omit irrelevant optional fields. If an optional detail is unknown, omit it and assess whether it raises the consequential open question.
For an unknown required answer, state that it remains unresolved and follow the same question-selection rule without pretending that other unresolved issues are settled.
Each entry in the nonempty `sources` list contains `source`, `locator`, and `basis`.
Attributed allocation analysis may use these existing fields to identify an acceptance-criterion position, its contributing ARs, and the reasoning for their cooperation. The original CLI example recorded 44 arguments; arguments for changed SR-042–045 criteria now use [historical allocation provenance](sources.md#src-cli-allocation-before-local-store), while unchanged criterion contributions remain under SRC-CLI-ALLOCATION. These entries preserve analysis provenance; they do not add obligations, duplicate containment relationships, or establish satisfaction. Criterion positions refer to the unchanged analyzed lists and require reconciliation if those criteria change.
Objects reject undeclared fields, and the schemas reject unsupported record types, lifecycle states, or analysis methods.

`analysis.what` explains the problem and desired outcome without copying the requirement statement.
Keep assumptions distinct from established constraints and unresolved questions.
Record additional imposed restrictions in root `constraints`; there is no `how.constraints` field.
Record quantitative bounds once in `how_much.limits`, without repeating them in root `constraints`.
An empty `constraints` list means no additional restrictions are recorded there; the statement and analysis still establish scope and boundaries.
Do not duplicate analysis in standalone `rationale`, `stakeholders`, `context`, `scope`, or `scope_notes` fields.
Parentage and directory suffixes remain derived from containment and titles; do not add parent IDs, child lists, or a `slug` field.

No separate `analysis.md` is required for these records.
If a later requirement needs substantial supporting analysis, define how to reference that material through Operational Support without maintaining duplicate facts.

The schemas check one record's structure, field values, and types.
They do not establish unique identities across files, correct parentage or directory names, source resolution, sound derivation, or requirement satisfaction.
Those checks require model-wide validation or engineering review.
See [Operational Support](../support/README.md) for the focused schema checks and their scope.

The [source register](sources.md) records the REM extracts and the exact repository revision used for drafting.
References to existing requirement IDs establish context, not equivalence or migration.
The existing obligations keep their original identities and authority until explicitly reconciled.

Acceptance criteria describe intended proof outcomes; they are neither executed checks nor evidence.
Verification definitions, evidence, and requirement satisfaction judgments have not been created here.

## Cross-domain references

An IR may author `confirms` references to Features and Scenarios; an SR may author `confirms` references to Functions and `constrains` references to Features or Functions.
These are arrays of stable IDs with no duplicates. The [Operational Support relationship table](../support/README.md#relationship-ownership) defines all permitted targets and the one authoring owner of each relationship.
The optional fields preserve earlier draft records; omission or an empty list means that no relationship of that kind has yet been recorded, not that analysis is complete.
Textual `constraints` and typed `constrains` relationships have distinct meanings.
For assets, `confirms` records an analysis conclusion within the draft model. For Scenarios it records the owning IR; the Scenario's `status` separately records its lifecycle state.
Neither relationship constitutes human approval, implementation, or verification.

## Analysis and allocation

Apply [5W2H](../../rem/methods/5w2h.md) to every IR, SR, and AR at its own level and record an answer, explicit unknown, or justified non-applicability for each question.
Use [clear IR names](../../rem/methods/requirement-analysis.md#name-the-initial-requirement) that identify the need and its subject.
This repository represents the seven answers through structured objects in `analysis`; REM does not prescribe that storage format.
Use [Scenario Analysis](../../rem/methods/scenario-analysis.md) to establish relevant Scenarios and durable Features from the need.
Derive system-level obligations from the need and supported Scenarios, then establish the logical Functions through SR analysis.

Derive allocated obligations when architectural responsibility is understood.
An AR remains a durable, verifiable requirement throughout later Changes.

An SR may constrain [Features](../system/features/README.md) and [Functions](../system/functions/README.md).
An AR is allocated to a [Module](../architecture/modules/README.md) and may constrain Functions.

Author the requirement's references separately from its parentage.
Derive inverse asset lists from those references.
The current IR, SR, and [AR schema](../support/schemas/ar.schema.json) define the cross-domain references above.

### Allocated requirement records

An AR uses `<AR-ID>-<full-title-slug>.json` directly within the directory containing its sole parent `sr.json`.
Its stable ID is independent of its parent and title; do not encode parentage in the identity or add a duplicate parent field.
The conceptual `SR derives AR` relationship is represented by this authoritative containment, with no separately authored SR child list.

The AR shape retains the requirement fields described above: identity, title, draft status, authoritative statement, structured seven-part 5W2H analysis, acceptance criteria, assumptions, constraints, and sources.
Its `type` is `allocated-requirement`. It requires one scalar `allocated_to` Module ID and may include unique `constrains` Function IDs.
An AR does not use SR's `confirms` field. An optional `open_questions` field contains exactly one consequential nonblank question when needed and is omitted otherwise.
Create an AR when its accountable architectural boundary is known; do not invent a lower-level requirement to fill a tree level.
The [Architecture Design method](../../rem/methods/architecture-design.md#derive-allocated-requirements) guides derivation and checks the composed AR obligations against the parent SR.

Requirements should state observable acceptance criteria and eventually link to applicable verification definitions.
Requirement text alone does not establish satisfaction or supply execution evidence.

## Customer browser proposal

The [customer architecture browser analysis](published-products.md#customer-architecture-browser-analysis) records the scoped JSON refinement, SR-084–088, SCN-083–087 and FEAT-022. The [source register](sources.md#src-customer-browser-requirements) identifies the requirement basis and its explicit downstream design limits; counts above include these records.

## Definition and assessment ownership

IRs, SRs, ARs, Scenarios and their supporting analysis define current engineering meaning. Source-register entries retain concise provenance and the rationale needed to understand that meaning. Review judgments, findings, exact assessed-subject identities and executed-check history belong to operational records under the [Constitution](../../CONSTITUTION.md#documentation-and-governance-maintenance). A document-based review is not a Requirements submodel. Moving its record does not change requirement meaning, Scenario confirmation or the subjects originally assessed.
