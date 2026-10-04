# Workflow

Owner: [MOD-006 Change control](module.json). This is supporting contract detail, not a separate REM entity. Source-qualified clause IDs retain their existing meaning.

Model validation contract: model-document-v1

The current workflow is owned by [Change control (MOD-006)](README.md). Its requirement basis is [the requirement-first analysis](../../../../../requirements/workflow-refactor.md). This entry connects repository contributors to that model and the corresponding published skills; it does not define a second lifecycle.

## Progression and ownership

```text
Request / proposal / issue / incident (RR input)
  → requirement-analysis → requirement-review
  → system-design ↔ architecture-design → integrated design-review
  → plan → delivery-review → implement
  → whole-change code-review → final verify → authorized PR
```

Requirement Analysis decides reuse, refinement or creation of IR/SR and supporting Feature/Scenario definitions. Requirement Review is the first mandatory approval and assesses the proposed requirement basis, including justified reuse. It does not require completed Functions or AR allocations. System Design defines logical behavior; Architecture Design assigns Module accountability, Interfaces, realization and ARs. One integrated Design Review assesses their composition.

Route coordinates authorized work from the current handoff. It cannot supply a specialist's judgment, expand user authority or settle an upstream defect by assigning a downstream task. Wrong needs or obligations return to requirement-analysis; logical behavior to system-design; allocation, Interfaces and ARs to architecture-design; delivery sequencing and proof allocation to plan; code defects to implement or bugfix.

## Milestones and reviews

Milestones organize implementation and relevant checks. Once a milestone's required work and checks are complete, otherwise authorized dependent implementation may proceed without a milestone review record, reviewer assignment or clean-review status. Required failures, unresolved material decisions, dependencies and authority limits still block affected work.

There is one mandatory independent whole-change Code Review gate after implementation. Optional interim advisory reviews supply useful findings but no lifecycle approval. Corrections and proportionate independent reassessment occur within the same gate. A one-milestone Change has one whole-change gate. Distinct final Verify assesses whether current evidence and completed work justify the completion claim.

## Current handoff and authority

Use `rigorloop change context --root PATH --change ID --format json` to resume selected active work. Context assembles current intent/authority, governing basis, progress, unresolved issues, evidence, review standing and next action. It reports facts and gaps, not engineering approval. Maintain these facts at consequential transitions and handoffs; do not record every edit or test attempt.

[Records](../../../MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md) owns the operational representation; [CLI](../../../MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md) owns requests and results. Skills know the supported interface and never SQL or private storage paths. Git-held engineering definitions remain understandable without a local database. Completion is a compact historical acceptance account and does not continuously track the current repository.

An isolated specialist invocation remains isolated unless broader work is authorized. Existing authorization through PR permits continuation through eligible work, review, Verify and submission. It does not authorize merge, release or destructive remote operations.

## Optional discovery

Explore and Research are optional support, selected by the decision owner. Explore expands an unclear problem or solution space; Research resolves bounded factual uncertainty among known options. Use both only when each has a distinct material question, and neither when ordinary inspection suffices. Explicit standalone invocation produces the owning discovery artifact; incidental investigation can remain within the decision owner's work. Neither activity grants downstream authority or substitutes for requirement/design ownership.

## Adoption and compatibility

The successor pairs requirement-first-v1 skills with targeted-recording-v2 / rigorloop-records-v4. Installation and a prepared Adoption do not activate workflow policy. Active work requires an explicit compatible disposition, including unresolved dependencies and current authority. Earlier executables retain their own declared contracts; the successor has no residue-selected fallback or v3 writer.

Legacy Proposal and milestone approvals retain their original scope. Explicit import preserves selected originals and maps only qualified current facts. It does not promote old judgments or bulk-delete `docs/changes/`. The adoption plan's private prior executable records bootstrap progress until the successor qualifies.

## Historical provenance

The replaced Proposal-first workflow and filesystem lifecycle procedures are recoverable at commit `39be9c81`, path `docs/design/skill/workflow.md`. Current behavior follows the linked requirement and Module owners above; those old procedures do not remain active alongside them.

## Requirements

These stable local references reconcile the prior document contract with the current REM and Module owners linked above. They do not retain the superseded workflow or filesystem interface.

| ID | Required behavior |
| --- | --- |
| WF-SR-01 | Responsible actors MUST explicitly decide activity, status, ownership and authorized continuation. Workflow MUST consume review applicability and closeout conclusions under RC-SR-04/05/13 rather than infer them from saves or reads. |
| WF-SR-02 | A Change MUST identify its contract, RR, current accepted requirement/design basis, activity, authority, owner, open issues, selected evidence and next action. Mutable progress belongs to current operational records, not engineering definitions or plan bodies. |
| WF-SR-03 | Workflow MUST obtain the required independent judgment through Review and Closeout RC-SR-01–04 before relying on approval. This stable ID now references that policy owner; it does not redefine reviewer independence or judgment. |
| WF-SR-04 | Route MUST assess cross-model correction impacts and select the responsible owner without requiring that owner to appear in a previously derived pending set. Authors and receiving actors MUST apply RC-SR-05–07/10 to changed-subject impact, applicability and reassessment; uncertain impact is handled under that policy. |
| WF-SR-05 | Workflow MUST provide an owned recording and correction path for defects discovered by any responsible stage, including Verify, under RC-SR-08/10/14. Record Format and CLI retain representation and mechanical recording ownership. |
| WF-SR-06 | Completion MUST remain a historical acceptance statement. Later regressions become linked new work; an error in the original account receives an explicit completion note. Open active-work obligations retain owned correction and disposition paths. |
| WF-SR-07 | Workflow MUST preserve the distinct Requirement Analysis, System Design and Architecture Design owners under DES-SR-01. Reuse without modification is a valid requirement disposition. |
| WF-SR-08 | Workflow MUST preserve Design DES-SR-06/11/13 reference and decision continuity when coordinating revisions. Exact affected-model review and concurrent-change applicability MUST follow RC-SR-01/02/05/06/10; retaining a reference MUST NOT retarget an old approval. |
| WF-SR-09 | Workflow MUST condition continuation and completion coordination on the applicable assessments and closeout obligations owned by RC-SR-05/11–15. Missing readiness MUST NOT prevent recording owned blockers or corrections under RC-SR-14. Workflow coordinates Delivery allocation under Design DES-SR-10/16 and the Model validation and proof mapping reference below. |
| WF-SR-10 | Retirement MUST preserve required original bytes and approval meaning. Explicit qualified import supplies current facts only through per-record disposition; historical approval MUST NOT become successor approval. |
| WF-SR-11 | Skills MUST use task-oriented CLI reads and mutations with actor-supplied meaning and opaque current revisions. The CLI owns mechanical validation, relationships, serialization and persistence; skills MUST NOT execute SQL or reconstruct runtime files. |
| WF-SR-12 | Assessment applicability MUST identify accountable attribution, actual scope and retained support. Updating evidence or preparing a candidate MUST NOT silently renew another actor’s judgment. |
| WF-SR-13 | Workflow MUST keep the recorded correction owner distinct from the disposition owner defined by RC-SR-08–10/14. Review findings and change-level blockers use the selected Record Format targets; route coordinates their correction without manufacturing another actor’s disposition. |
| WF-SR-14 | Workflow actors MUST select and expand useful context for their decisions and apply RC-SR-04/05/18 before reliance. Diagnostic detail remains a CLI observation, not a storage prerequisite or a source of activity-selection authority. |
| WF-SR-15 | The complete successful Verify assessment and final explanation, and the shared material-decisions narrative, MUST be available through normal targeted reads with recorded applicability and identities. Retrieving a deliverable MUST NOT require advanced inspection of unrelated records or imply renewed verification. |
| WF-SR-16 | Workflow MUST preserve the final assessment dependency defined by RC-SR-11/12 in delivery and closeout coordination, including when later corrections affect a previously reviewed result. The plan and specialist assessments supply the basis; route MUST NOT fabricate a final-review judgment or treat a milestone result as a whole-change result. |
| WF-SR-17 | For work using the adopted TEST-SR criteria, Workflow MUST route missing intended behavior to Design, missing proof allocation to planning, and defective concrete tests to the responsible implementation or correction activity. Planning and specialist assessments MUST consume the shared criteria in System TEST-SR-01–13 without assigning that model judgment, applicability or closeout authority. |
| WF-SR-18 | The successor MUST reconcile requirement-first skills, v2 transport, v4 SQLite storage, examples and packages together. Earlier data requires explicit qualified import; installation MUST NOT activate governance or supply approval. |
| WF-SR-19 | Follow-ups MUST live with an action-owning artifact or explicit accepted cross-change register under Follow-up placement below. Orientation, a learning classification, historical plan text or a recorded route MUST NOT imply execution commitment or downstream completion. |


### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | WF-SR-01 | Unknown contracts, malformed references or unsupported scope stop the affected operation without inferred defaults. |
| State/lifecycle | WF-SR-01 | Progress, accepted basis, review judgment, final Verify and historical completion remain distinct; saved state alone advances none. |
| Identity/authority | WF-SR-01 | The actual responsible actor, declared scope and current support govern reliance; an identifier or role label does not establish authority. |
| Composition/path | WF-SR-01 | Changed producer and consumer contracts are reconciled together, including packaged conditional resources and referenced engineering definitions. |
| Temporal/retry | WF-SR-01 | A changed basis requires rereading and proportionate reassessment; an old submission does not acquire current authority on retry. |
| Failure/recovery | WF-SR-01 | Interrupted work exposes its actual outcome and an owned next step without erasing unresolved issues or inventing success. |
| Compatibility/migration | WF-SR-01 | Retired procedures remain historical; successor behavior requires explicit applicable adoption/import and cannot relabel old approval. |
| External/environment | WF-SR-01 | Local engineering results remain separate from installed, published or hosted outcomes; required observations must actually be made. |

## Test design

Inspect the current responsibilities and boundary scenarios against the owning REM model and Module contract. Structural checks establish format only; independent review judges semantic coverage. Runtime record behavior is exercised by the package’s operational store, update, reliance, review and maintenance tests; skill guidance is assessed in actual generated archives with the resource validator and independent scenario inspection. Required combined and negative proof is allocated in the adoption plan.
