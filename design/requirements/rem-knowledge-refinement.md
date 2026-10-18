# REM knowledge refinement and requirements-analysis pilot

## Request and scope

The user asked how to refine REM from the latest Knowledge Practice System and authorized the proposed next step: draft a coverage outline and requirements-analysis pilot acceptance criteria.
The [research note](../../docs/research/2026-10-18-rem-refinement-from-current-kps.md) supplies the comparison; the [coverage outline](../../rem/docs/body-of-knowledge-outline.md) proposes subject understanding, intended capabilities and explicit gaps.
This document supplies supporting requirement analysis and assessable pilot outcomes.
It proposes bounded reuse of existing requirements; it is not a new requirement hierarchy or an implementation approval.

Owning Change: `2026-10-18-rem-knowledge-refinement`; read its current handoff through `rigorloop change context`.
Review standing, findings, actual execution evidence and progression belong to that operational record.

The immediate deliverables are a draft whole-REM subject outline, a detailed requirements-analysis slice, source/ownership reconciliation and the pilot criteria below.
The later pilot would refine the relevant explanations together and assess their use.
This slice does not implement that pilot, change current REM semantics, select a new method edition, claim KPS compatibility, or publish externally.

## Need and context

An engineer, reviewer or agent needs to use REM explanations to make a bounded engineering decision without reconstructing the originating conversation.
The initial task is to reconcile a request with existing requirement knowledge, explain the resulting obligation and identify how it could be assessed.
The broader subject outline keeps adjacent capabilities and missing coverage visible while the pilot explores this one task.

| Analysis dimension | Interpretation for this bounded request |
| --- | --- |
| What | Define what REM needs to explain and what successful requirements-analysis guidance should enable a reader to produce. |
| Why | File inventories and well-formed examples alone do not show whether readers can reason about an unfamiliar request. |
| Who | Engineers new to REM, experienced reviewers and engineering agents; the maintainer selects scope, and independent review assesses the proposed requirement basis. |
| When | Before a broad knowledge rewrite or a claim that current guidance achieves the intended capability. |
| Where | Canonical REM knowledge, with RigorLoop-specific acceptance and operational assessment kept in their owning project surfaces. |
| How | Define source-informed coverage, prepare contrasting tasks and compare produced semantic outcomes with explicit criteria. |
| How much | One detailed requirements slice within a whole-REM outline; no invented speed target, learning-effect threshold or participant sample size. |

No new durable IR/SR is proposed by this analysis; this table records the request interpretation rather than replacing the existing requirements' 5W2H analyses.
Selection of the later pilot's actual participants and guidance revision belongs to its assessment allocation before execution.

## Existing requirement disposition

The requirement JSON records below retain their current draft status.
Proposing reuse for this slice does not approve them globally or claim their full satisfaction.

| Existing owner | Proposed disposition and bounded acceptance relevance |
| --- | --- |
| [IR-006 — guide people and agents](IR-006-guide-people-and-agents-in-authoring-engineering-models/ir.json) | Reuse: understandable authoring guidance is the existing need; a newer editorial source does not establish a different need. |
| [SR-032 — applicable canonical guidance](IR-006-guide-people-and-agents-in-authoring-engineering-models/SR-032-select-applicable-canonical-authoring-guidance/sr.json) | Reuse: the outline locates relevant owners and declares gaps; the pilot distinguishes current REM rules, examples and consulted KPS guidance. |
| [SR-033 — bounded authoring and correction](IR-006-guide-people-and-agents-in-authoring-engineering-models/SR-033-guide-bounded-engineering-authoring-and-correction/sr.json) | Reuse: assess seven-question analysis, parentage, black-box Scenarios and supported versus unresolved actions. The pilot does not cover all architecture, rename or retirement cases in this broader SR. |
| [SR-034 — semantic authoring outcomes](IR-006-guide-people-and-agents-in-authoring-engineering-models/SR-034-assess-guidance-using-semantic-authoring-outcomes/sr.json) | Reuse: prepare inputs and expected outcomes; preserve incorrect results, ambiguity and extra help; separate participant groups and unperformed tasks. This pilot samples requirements analysis, not the SR's complete task population. |
| [IR-009 — portable guided work](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/ir.json), [SR-056 — meaning across reading paths](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-056-preserve-guidance-meaning-and-evidence-quality-across-reading-paths/sr.json) | Reuse: local summaries preserve current owner meaning and source limits. Future packaged changes need equivalent guidance, without requiring repository internals for the reader task. |
| [SR-079 — reconcile incoming requests](IR-009-carry-out-portable-guided-engineering-work-across-the-project-lifecycle/SR-079-reconcile-incoming-requests-with-existing-requirement-owners/sr.json) | Reuse: compare each material RR part with existing needs and obligations, and explain reuse, refinement, creation or unresolved disposition. |

The proposed outcomes specialize these obligations for an assessment task; they are not new SRs, permanent checklist fields or additional workflow gates.
No Function, Module, Interface or AR is created to mirror the coverage rows.

## Feature and Scenario reconciliation

[FEAT-010 — Guide engineering model authors](../system/features/FEAT-010-guide-engineering-model-authors.json) already covers finding guidance, bounded authoring and semantic assessment.
Reuse [SCN-031 — derive clear requirements](scenarios/SCN-031-derive-clear-requirements-and-system-definitions-with-canonical-guidance.json) for the reader task and its missing-context outcome.
Reuse [SCN-032 — correct definitions](scenarios/SCN-032-correct-and-retire-engineering-definitions-using-their-governing-rules.json) for the refinement/correction variation.
The pilot covers the requirements portion of those Scenarios; it does not assert their complete downstream design outcomes.

[FEAT-015 — portable capabilities](../system/features/FEAT-015-select-and-invoke-portable-engineering-capabilities.json) and [SCN-052 — complete selected guidance](scenarios/SCN-052-obtain-the-complete-guidance-required-by-a-selected-path.json) retain their IR-009 ownership for the later packaged reading path.
They are not reassigned to IR-006 merely because they support the same pilot.
The task cases below are assessment fixtures within these existing stakeholder situations, not newly confirmed governed Scenarios.

## Draft deliverable criteria

1. The coverage outline identifies the reader, target depth, boundaries and source-informed subject structure before mapping current files; its topic rows connect required understanding, an observable capability and a specific gap.
2. Requirements-analysis coverage distinguishes source/request, need, obligation, Feature, Scenario, behavior, allocation and evidence, including material ambiguity and failure outcomes.
3. The proposed pilot has sufficient starting information, expected semantic outcomes and rejection examples to expose a reader guessing a missing instruction or inventing unsupported facts.
4. Existing requirement and Scenario reuse is justified, current rules retain their owners, and source provenance distinguishes fresh inspection from retained earlier inspection.
5. The drafts are navigable from REM, use working local references, preserve generated guidance freshness and identify unperformed assessments honestly.

## Pilot outcome and boundaries

Target task: **reconcile an incoming request and derive justified, assessable system obligations**.
The produced account contains an attributable RR interpretation, comparison with existing requirements, a justified disposition, the necessary IR/SR analysis, stakeholder Feature/Scenario reasoning, acceptance intent and a next action.
The representation is free unless the selected project supplies an applicable schema.
Completing a worksheet, adding entities or matching example wording does not establish success.

The later explanation work should connect [Requirements Concepts](../../rem/concepts/requirements.md), relevant [Principles](../../rem/principles/README.md), the [Requirements](../../rem/models/requirements.md) and [Scenario](../../rem/models/scenarios.md) Models, [5W2H](../../rem/methods/5w2h.md), [Requirement Analysis](../../rem/methods/requirement-analysis.md), [Scenario Analysis](../../rem/methods/scenario-analysis.md), and the requirements stages of [Engineer a change](../../rem/practices/engineer-a-change.md).
The [offline-responsibility example](../../rem/practices/WORKED-EXAMPLE.md) provides a shared illustration; later architecture and assessment sections remain distinguishable from the pilot's requirement output.
These are candidate authoring locations, not a requirement to edit every file or create one document for each topic.

## Prepared task cases

All case facts are constructed assessment inputs, not observations of a real user or accepted product requirements.
`IR-PILOT-*`, `SR-PILOT-*` and related labels below are fixture-local identities; they are not additions to the repository model.
Each case begins from its own supplied baseline; one participant's output is not another case's prerequisite.
Before execution, a reviewer checks the expected decisions against the input and canonical rules rather than deriving the expected answer from the guidance under test.

For A–C, the constructed export is `snapshot-pilot-01`: Function `FUNC-PILOT-01` has primary Module `MOD-PILOT-01` and supporting Module `MOD-PILOT-02`; both Modules exist.
For the missing-mapping variation, remove only the primary-owner relationship; for the invalid-mapping variation, replace its target with absent `MOD-PILOT-99`.
These are separate input copies and establish the expected data boundary independently of any proposed viewer.
The participant is authoring requirements and assessment intent; no implemented viewer or executed product test is supplied.

### Case A — Reuse a covered need

**Given:** A maintainer must identify responsibility during offline review. Fixture IR-PILOT-01 expresses that need; SR-PILOT-01 requires displaying a known Function's recorded primary Module and snapshot identity from a valid local export without network requests. A Feature and black-box Scenario already cover that interaction. The requester confirms that “owner” means the recorded primary Module, snapshot-relative information is sufficient and any presentation meeting the outcome is acceptable; a new screen is not mandatory.

**Incoming request:** “Add an offline ownership screen; I need to see who owns this Function and which export I am reading.”

**Expected outcome:** Reuse the existing IR, SR, Feature and Scenario without manufacturing new identities. Explain that a new screen is a suggested realization and that the request is already covered under the supplied conditions. The next action investigates the implementation or presentation gap; the existence of the SR does not prove it is implemented.

**Detectable wrong result:** Create a second IR for the screen, infer that the requirement is satisfied, or substitute a supporting Module for the primary owner.

### Case B — Refine an existing obligation

**Given:** The same offline need and valid-mapping SR exist. The current baseline does not specify the user-visible outcome of a missing owner mapping. The requester confirms that this variation serves the same offline capability and that the viewer must disclose absence without inferring an owner. No new performance target is supplied.

**Incoming request:** “If this export has no owner for the selected Function, tell me that the mapping is unavailable instead of guessing.”

**Expected outcome:** Explain the previously uncovered failure outcome and propose an identity-preserving refinement to the existing SR and affected Scenario. The acceptance intent distinguishes valid mapping from missing mapping and retains snapshot identity and offline conditions. A separately named SR is acceptable only if the participant justifies a distinct obligation boundary; an arbitrary ID quota is not the criterion.

**Detectable wrong result:** Create a new stakeholder need merely for an error message, hide the missing outcome in implementation notes, or introduce a guessed performance threshold.

### Case C — Establish a genuinely missing need

**Given:** A bounded fictional project has identifiable Functions and primary Modules but no requirement or Feature for offline responsibility inspection. The maintainer needs the recorded owner of one known Function during a disconnected review, accepts a supplied snapshot as the information boundary, requires explicit missing/invalid-mapping reporting and has supplied no response-time threshold. Local read-only inspection is permitted; implementation and approval authority remain separate.

**Incoming request:** “During an offline review, I need to find who owns this behavior.”

**Expected outcome:** Justify a new need after checking the supplied baseline; draft an IR, a durable Feature, black-box Scenario outcomes and system obligations under the IR. Account for all seven analysis questions at the IR and SR levels using the given facts, explicit unknowns or justified non-applicability. Explain why the acceptance observations address the need and why Function design, Module allocation and actual evidence can remain unperformed.

**Acceptance observation example:** With an identified export, known Function and independently known mapping, the proposed assessment observes the recorded owner and source state while checking absence of network requests; missing or invalid mappings produce an explicit unavailable/invalid result. This is planned proof, not a test execution or prescribed UI.

**Detectable wrong result:** Copy the RR as an approved IR, treat the Feature as a screen implementation, insert an internal lookup sequence into the Scenario, or invent an AR solely to complete the tree.

### Case D — Preserve ambiguity in an unfamiliar domain

**Given:** A fictional maintenance-planning system already retains an approved inspection schedule for a selected asset. Existing obligations identify the asset and schedule revision. The proposed use is disconnected field work. The requester supplies no permitted age of cached information, source availability guarantee or speed criterion; a suggestion to use AI has no separate authority.

**Incoming request:** “Show the latest approved inspection schedule instantly while I am offline; use AI to fill anything missing.”

**Expected outcome:** Compare the existing capability with the new operating conditions, distinguish a cached approved revision from a guaranteed latest revision, identify the unsupported completion proposal and preserve the independent freshness, missing-data and performance issues. Explain which decision or evidence would settle each issue and leave dependent obligations provisional. A coherent cache-relative alternative may be proposed explicitly for decision, not silently substituted for “latest.”

**Detectable wrong result:** Promise currentness without a source guarantee, fabricate an inspection schedule, invent a numeric latency target, or concatenate unresolved decisions into one nominal question to satisfy REM's open-question limit.

This case is held out from the worked explanation in the later pilot. A reader must transfer the reasoning rather than reproduce the offline-ownership example.
It does not ask participants to supply domain-specific maintenance rules or assert safety compliance.

## Pilot acceptance criteria

The labels identify this pilot's observations and do not add new engineering requirement IDs.

| Criterion | Observable outcome | Existing basis |
| --- | --- | --- |
| P1 — Source and applicability | Identify the selected REM guidance and supplied case facts; distinguish a required constraint from a solution preference and KPS editorial advice. | SR-032, SR-056, SR-079 |
| P2 — Justified disposition | Explain reuse in A, the missing failure outcome and appropriate refinement in B, and justified creation in C; preserve identities where meaning continues. | SR-033, SR-079 |
| P3 — Coherent requirement analysis | In C, explain the need, system obligation and each relevant 5W2H answer without invented stakeholders, scope or quantities. In D, preserve missing information and the consequence for readiness. | SR-033, SR-079 |
| P4 — Stakeholder relationships | Keep Scenarios black-box, distinguish the durable Feature, retain the Scenario's IR/primary-Feature ownership and link outcomes to obligations without inventing internal architecture. | SR-033; SCN-031 |
| P5 — Assessable obligations | State a positive and relevant adverse observation for B/C, with input state, conditions and observable outcome. Explain their relation to the SR and what they cannot establish about intended use. | SR-033, SR-034 |
| P6 — Honest uncertainty and next action | In D, expose the incompatible or unsupported expectations and identify a decision owner or evidence need; do not hide independent questions or claim dependent design is ready. | SR-033, SR-079 |
| P7 — Local usability | For the selected Practice stages, a participant can perform and explain the applicable case decisions with outbound links hidden after receiving the stated prerequisites. Record every additional explanation required. | SR-034, SR-056 |
| P8 — Faithful support and bounded claims | Restore links and locate the current owners. Distinguish external contributions, REM's normative selections, authored examples, proposed assessments and actual observations. | SR-032, SR-034, SR-056 |

A materially wrong disposition, invented fact, hidden uncertainty, changed cardinality or unsupported success claim prevents the affected task from passing, even if a structural validator accepts the output.
Equivalent wording and alternative representations are acceptable when their meaning and relationships satisfy the criteria.
If a task needs essential coaching absent from its stated prerequisites and local guidance, record the gap and revise the relevant explanation; do not erase the initial result after coaching.

## Assessment procedure and evidence boundaries

Before a run, identify the participant group, the exact guidance and fixture revisions, prerequisites, selected case and expected criteria.
For a new author, supply the prerequisite vocabulary actually stated by the candidate guidance; do not assume knowledge of this conversation.
Keep results for new authors, experienced reviewers and agents separate. Testing one group does not establish outcomes for the others.

Assess three questions separately:

1. **Coverage:** compare the detailed outline with the selected engineering source passages and case variations; include material gaps even when a happy-path example works.
2. **Usability:** use the selected Practice stage with links hidden, then inspect the participant's disposition, explanation and next action against P1–P7. Record ambiguity and additional help. An author's paper walkthrough is editorial evidence; identify it as such.
3. **Source fidelity:** restore links and compare the relevant local explanations with canonical REM owners and inspected source passages under P8. A citation, file hash or passing parser cannot establish faithful meaning by itself.

The pilot can establish scoped editorial adequacy or observed task success for actual participants.
It cannot establish general learning effectiveness, a causal improvement over the earlier edition or complete satisfaction of SR-034.
A before/after comparison, if later selected, must identify task familiarity, supplied help and other changed conditions; no improvement percentage is assumed here.
Actual observations and judgments belong in the owning operational records, with failed and unperformed criteria retained explicitly.

## Compatibility and downstream handoff

Preserve the [current REM edition and KPS basis](../../rem/metadata.md), requirement hierarchy, Scenario ownership, 5W2H obligation, open-question rule, Function/AR accountability and evidence boundaries.
The outline is supporting navigation, not a new knowledge type or a source of competing invariants.
The [owning composition](../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/rem-guidance.md) retains responsibility for guidance, and current project recording/review rules govern judgments.

Requirement Review should assess the bounded reuse conclusion, coverage targets, cases and criteria before they become an accepted basis for pilot design.
Subsequent design must resolve local explanation boundaries and affected consumers; delivery must allocate concrete authoring and assessment work.
If canonical projected guidance changes, reconcile its generated resources and assess both repository and selected packaged reading paths.
This draft allocation does not supply a required review judgment, an executed reader trial, or final Verify.
