# Explicit Recording and Model-Centered Design — Advisory Review

## Recording basis

This isolated advisory record accompanies the user's request to fix the finding and rereview. It reconstructs the independent first-pass result from the preceding review before correction. It uses the previously proposed review location, not a registered lifecycle path. The user-authorized two-model drafting exception and exclusion of OS-specific investigation apply. No formal package, upstream review identity, registration or settlement is claimed.

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: `workflow` → [Workflow](../design/workflow.md); `cli` → [CLI](../design/cli.md).
- Upstream review ID: None; isolated advisory proposal approval only.
- Review ID and round: No formal review ID or round assigned; independent first pass reconstructed before correction.
- Material findings: MODEL-DR-001.
- Correction targets: `cli`, Design authoring.
- Recording status: recorded.
- Settlement status: not-applicable.
- Open blockers: Inspect cannot represent the promised snapshot in its closed result schema.
- Immediate next stage: Authorized Design correction, then independent advisory rereview.
- Claim limitations: No adoption, implementation approval, formal package settlement or automatic downstream handoff.

## Finding MODEL-DR-001

- Finding ID: MODEL-DR-001
- Severity: major
- Location: CLI model, Result schema and exit behavior, versus CLI-SR-01, the inspect invocation and Read and check.
- Evidence: The pre-correction inspect contract promises recorded values and a registered snapshot, but the exact result fields contain no content or snapshot member. The files array permits only path and identity. Recorded activity, owners, judgments, blockers, evidence and bodies cannot be returned through that closed schema; diagnostic summaries are not a substitute.
- Required outcome: Represent the coherent recorded snapshot explicitly, including missing registered files, without mixing it with observations or enlarging ordinary save results unnecessarily.
- Safe resolution path: Add the smallest inspection-content representation with explicit presence rules and reuse the Workflow model's record definitions.
- needs-decision rationale: None; ordinary CLI Design authoring decision.
- Finding scope: artifact-local.
- Affected artifact IDs: `cli` (descriptive advisory model ID, not a registered artifact identity).
- Owning stages: Design authoring.

## Independent first-pass basis

Reviewer: the independent `review_compact_fix` agent, not the model-document author. The reviewer read both complete drafts and the proposal and found no further material semantic transition cycle. Workflow owns decision meaning; CLI owns storage. Separate specification/ADR files and OS-specific investigation were not required. Boundary-format mapping and adoption reconciliation remained disclosed pre-implementation obligations, not extra findings manufactured from draft incompleteness.

## Correction and rereview

At initial recording, correction and rereview had not occurred. The first-pass result and finding above are preserved as the original assessment.

### Independent rereview result

- Skill: design-review
- Review status: approved within this isolated advisory draft-review scope.
- Package members: `workflow` → [Workflow](../design/workflow.md); `cli` → [CLI](../design/cli.md).
- Upstream review ID: None; isolated advisory proposal approval only.
- Review ID and round: No formal review ID or round assigned; independent correction rereview.
- Material findings: None open; MODEL-DR-001 resolved.
- Correction targets: None for this finding.
- Recording status: recorded.
- Settlement status: not-applicable.
- Open blockers: None in the reviewed correction; the drafts retain their disclosed pre-implementation reconciliation obligations.
- Immediate next stage: Isolated stop; no automatic downstream handoff.
- Claim limitations: No registration, formal package approval, implementation permission, adoption or activation is established. Boundary-format mapping, adoption reconciliation and later proof remain required before implementation readiness.

### MODEL-DR-001 disposition and evidence

Disposition: accepted and resolved by the Design correction, independently rereviewed by `review_compact_fix`, which authored neither model document.

The CLI result now explicitly includes `snapshot`. Successful inspection returns exact UTF-8 record content in `snapshot.records`, bound to the same coherent file set and identities as `files`. Missing registered supporting records have null content and identity with an observation; an absent root has an empty snapshot. An unreadable, malformed or unsafe manifest rejects without a snapshot. Other operations and non-inspected outcomes use null, so ordinary saves do not echo record bodies and interrupted inspection does not expose partial content. The content reuses the Workflow model's record definitions rather than introducing a second semantic schema.

This satisfies the first-pass required outcome and CLI-SR-01/05/11. The reviewer reread both complete current model drafts and the preserved first-pass record. Workflow still owns explicit decisions and downstream reliance; CLI owns coherent storage and observations. No further material cross-model contradiction or semantic transition cycle was identified in this advisory scope. The correction adds no lifecycle engine, mandatory sidecar Design file or OS investigation.

Review commands: `cat docs/reviews/explicit-recording-and-model-centered-design.md`, `cat docs/design/workflow.md`, `cat docs/design/cli.md`, and bounded `sed` reads of the corrected result section and remaining Workflow sections. `git diff --check -- docs/reviews/explicit-recording-and-model-centered-design.md docs/design/workflow.md docs/design/cli.md` checks whitespace only. No executable behavior, model schema implementation or formal lifecycle validation is claimed.

## Selector-error clarification — independent Design rereview

- Skill: design-review
- Review status: approved (isolated advisory scope)
- Package members: `workflow` → `docs/design/workflow.md`; `cli` → `docs/design/cli.md` (descriptive model IDs, not formal registrations)
- Upstream review ID: None; existing independent advisory proposal judgment remains the basis
- Review ID and round: No formal identity assigned; subsequent independent correction rereview
- Material findings: None open; ER-M2-001 Design clarification resolved
- Correction targets: None at Design; implementing the clarified schema/parser remains M2 work
- Recording status: recorded, advisory-durable
- Settlement status: not-applicable
- Open blockers: None for this bounded Design correction; adoption and previously disclosed reconciliation obligations remain
- Immediate next stage: Return judgment to the coordinating agent; no automatic lifecycle handoff or settlement
- Claim limitations: No implementation correctness, schema parity, M2 closeout, ordinary activation, Verify or branch readiness claimed. M2 execution authority comes from the user's separate explicit request, not this review.

The independent reviewer reread both complete model documents, the prior advisory Design record and the ER-M2-001 preflight. The reviewer authored neither model. The CLI Result schema now explicitly permits null only for unavailable selectors in an empty, rejected invalid-input result with exit 2. Recognized operation and exactly one valid change selector are retained independently. Repeated change selectors cannot select an arbitrary identity. Non-rejected outcomes still require valid selectors; request and persisted-record identities are not widened. This removes the need to fabricate a change or command identity and directly resolves the preflight contradiction.

Argument failures have one safe result envelope rather than a second command schema. Format-error fallback, retention of a single valid JSON selector, no repository/stdin access during argument rejection, and suppression of raw rejected selector values make the error path sufficiently definite for implementation and direct testing. These rules preserve the CLI-SR-02/11 input/error boundary without changing storage outcomes or Workflow decision ownership. The unchanged Workflow schema therefore remains coherent with the narrow result-only exception.

All six Design-review contract questions were reconsidered: architecture supports the clarified failure outcome; technical and authority constraints remain explicit; the proposal's simplicity and faithful-recording goals are preserved; data/trust/recovery ownership is unchanged; embedded decisions remain consistent; and the identified contradiction is resolved. The eight existing boundary dimensions remain applicable as previously allocated. This correction directly refines input-domain and error-output composition, preserves identity/authority and privacy constraints, and introduces no new lifecycle, concurrency, recovery or historical migration behavior. One file per model, no OS investigation, independent review and deferred ordinary adoption remain intact. No additional material issue was identified.

Commands used: `cat` and bounded `sed` reads of the complete members and prior records, plus the design-review skill and required references/assets. No code tests were represented as Design proof; schema and public CLI selector tests belong to the upcoming M2 implementation review.

## External-edit boundary — current independent Design rereview

- Skill: design-review
- Review status: approved (isolated advisory scope)
- Package members: `workflow` → `docs/design/workflow.md`; `cli` → `docs/design/cli.md` (descriptive model IDs)
- Upstream review ID: None; existing independent advisory proposal judgment remains the basis, with the user's explicit concurrency-scope refinement
- Review ID and round: No formal identity assigned; independent bounded rereview
- Material findings: None at Design; ER-M2-005's requested Design decision is resolved
- Correction targets: None at Design; affected implementation assessment remains Code Review-owned
- Recording status: recorded, advisory-durable
- Settlement status: not-applicable
- Open blockers: None for this Design decision; implementation review and ordinary-adoption obligations remain
- Immediate next stage: Affected M2 Code Review under separate user authority; no automatic lifecycle handoff
- Claim limitations: No implementation approval, code-finding closeout, formal registration, ordinary activation, M3 permission, Verify or branch readiness

The independent reviewer read both complete current model documents, the proposal, prior advisory Design judgments and ER-M2-005 evidence. The reviewer authored neither model. The user explicitly chose the narrower external-edit guarantee; this is an intentional scope decision, not a claim that another hash check fixed the demonstrated race.

CLI-SR-04 now distinguishes exclusion of competing CLI writers from identity checks on external edits. CLI-SR-06 applies the observed-check boundary to recovery. Save safety and recovery boundary plainly tells users not to edit record files manually or through other tools during record/recover, states that exact-target edits after the final check may be overwritten, and applies that limitation to save, completion and restoration. The related runtime, boundary, quality and risk prose agrees. Observed conflicts and third states still stop; ancestor containment, supported-reader coherence, recovery evidence and committed-success protections are retained. The narrow timing exclusion does not waive CLI-SR-09's path protections.

The unchanged Workflow model remains coherent: actors own explicit decisions and must reassess current evidence before reliance, while the CLI owns storage and its stated external boundary. One file per model, independent review, historical contract isolation and final Code Review remain intact. The proposal's recording direction is preserved under the user's express refinement; no new transition engine, dependency, OS investigation or mandatory Design sidecar is introduced.

All six Design contract questions were considered together. The revised guarantee is technically bounded, operational assumptions are explicit, actor/CLI trust and recovery ownership remain consistent, embedded decisions agree, and the specific contradiction behind ER-M2-005 is resolved. The existing eight boundary dimensions remain allocated; this correction narrows temporal/external identity protection without removing input, state, authority, composition, recovery or compatibility obligations. No further material cross-model issue was identified in this advisory rereview.

ER-M2-005 is resolved only as a Design-owner decision here. Its original Code Review evidence remains unchanged and must receive an explicit affected implementation assessment; this review does not convert the observed overwrite into implementation approval or settle that code finding.

Commands used: `cat` reads of the complete members, proposal, prior review and required skill resources, and a bounded `tail` read of ER-M2-005 context. No hashes, executable behavior tests or lifecycle operations were used for this Design judgment.

## Model-validation mapping — current independent Design rereview

- Skill: design-review
- Review status: approved (isolated advisory scope)
- Package members: `workflow` → `docs/design/workflow.md`; `cli` → `docs/design/cli.md` (descriptive model IDs)
- Upstream review ID: None; existing independent advisory proposal judgment and explicit two-model exception remain the basis
- Review ID and round: No formal identity assigned; independent M3 dependency rereview
- Material findings: None
- Correction targets: None at Design for this mapping
- Recording status: recorded, advisory-durable
- Settlement status: not-applicable
- Open blockers: The named M3 Design-mapping dependency is resolved; implementation and adoption proof remain separate
- Immediate next stage: Return judgment to the coordinator; M3 implementation requires its existing separate user authority and subsequent Code Review
- Claim limitations: No validator correctness, guidance implementation, M3 completion, formal registration, ordinary activation, Verify or whole-branch readiness

The independent reviewer read both complete current model documents, the proposal/advisory review basis and the M3 preflight. The reviewer authored neither model. Workflow's Model validation and proof mapping now owns the previously missing document contract; CLI links to that owner and declares the same explicit marker without duplicating the rule.

The mapping is sufficiently definite for implementation: only explicitly selected, contained regular model files qualify; symlinks and missing/unknown markers reject without historical fallback. Required headings, table columns, stable requirement-ID grammar, all eight exact scenario labels, duplicate/missing rows, local requirement references and reasoned non-applicability have defined treatment. Model path plus requirement ID or dimension label provides a reference without another identifier series. Both current members retain their existing requirements and eight applicable rows.

Traceability responsibilities remain coherent. Model requirements and requirement-linked combined hazards own behavior; examples cannot introduce it. Plans allocate affected requirements, rows and hazards to checks and expected evidence, while execution evidence records results and exact subjects. Validators assess representation/reference integrity, not semantic coverage, independence or approval. This resolves the M3 preflight gap without turning `record-store` into a document or workflow eligibility engine.

All six Design contract questions were considered as one package judgment. The selected representation supports the stated behavior, safe inputs and historical compatibility; responsibility and proof ownership are explicit; embedded decisions and proposal simplicity goals remain aligned; the prior mapping ambiguity is resolved. The eight existing reasoning dimensions and material composed hazards remain present despite the deliberate replacement of the older four-table serialization. That replacement is explicit and model-scoped, not claimed historical-format conformance. One file per model, no OS investigation, the approved external-edit limit and withheld ordinary activation remain unchanged.

The old validator's rejection of model paths is expected pre-implementation evidence, not proof that this mapping is implemented or an additional Design defect. M3 must implement and independently prove the selected recognition, rejection and reference behavior, and guidance must preserve the structural-versus-semantic distinction. No additional material Design gap was identified in this bounded review.

Commands used: `cat`, `sed` and `tail` for complete model and bounded proposal/review/preflight reads and the required Design-review skill resources. No hashes, code tests, model edits or lifecycle operations were used for this judgment.

## Grandfathered-authority handoff — independent Design rereview

- Skill: design-review
- Review status: approved (isolated advisory scope)
- Package members: `workflow` → `docs/design/workflow.md`; `cli` → `docs/design/cli.md` (descriptive model IDs)
- Upstream review ID: None; existing independent advisory proposal judgment and explicit user exception remain the basis
- Review ID and round: No formal identity assigned; bounded M4 dependency rereview
- Material findings: None at Design; ER-M4-002's requested Design decision is resolved
- Correction targets: None in this two-model package; affected validation and governing-surface reconciliation remain implementation work
- Recording status: recorded, advisory-durable
- Settlement status: not-applicable
- Open blockers: No remaining Design ambiguity for this handoff; implementation, affected Code Review and adoption proof remain separate
- Immediate next stage: Return judgment to coordinator; no automatic lifecycle handoff
- Claim limitations: No validator correctness, code-finding closeout, complete M4, formal registration, public activation, Verify or branch readiness

The independent reviewer read both complete current model files, the proposal, prior advisory Design/Delivery basis, ER-M4-002 context and the exact shared-authority amendments. The reviewer authored neither model nor those amendments. This review applies only in `/home/xiongxianfei/data/20260419-rigorloop.worktrees/explicit-recording-m4-IYKgvb`; it neither edits nor changes the original worktree's recorded result.

Workflow now distinguishes structural success from pending semantic assessment. For changed unmarked grandfathered specs, `review_required` names the paths and Design Review owner; `review-required` with exit zero does not claim approval. Structural errors still fail with nonzero exit, even in a mixed result. Non-grandfathered missing/unknown markers and malformed boundary content remain errors. Independent assessment belongs in the existing review record, and missing, uncertain or stale classification blocks reliance and Verify. The validator does not authenticate that assessment or become an eligibility engine. This resolves ER-M4-002's owner/handoff ambiguity without adding a receipt, configuration layer, state transition or model file.

### Independent classification of the reported amendments

The classifications below cover only the actual additions relative to isolated baseline `d6770adfbbd835363d3b428acbd5a27a9485171b`, not hypothetical activation changes or the entire historical documents.

| Exact subject and amendment | Classification | Basis and preservation |
| --- | --- | --- |
| `specs/rigorloop-workflow.md`, added `Prospective explicit recording` heading and its two paragraphs | New-profile-only | The additions explicitly limit model ownership, explicit decisions and unified Design to authorized `explicit-recording-v1` work; ordinary activation is disabled. They retain final whole-change review, exact subjects, proof and historical procedures without conversion. No historical remainder is edited. Assessed against WF-SR-01–10 and CLI's contract separation; not mislabeled a non-substantive wording change. |
| `specs/skill-contract.md`, added opening paragraph under `Goal and context` | New-profile-only | Replacement artifact/transition shapes apply only to the prospective isolated profile. Skill naming, self-containment, resource integrity, independence, evidence and claim boundaries remain; adoption and adapter agreement are separate prerequisites. The historical remainder is unchanged. Assessed against WF-SR-07/08/10 and the model-owned validation mapping. |

These are this reviewer's affirmative classifications, not inferred author approval. They preserve grandfathering of the unchanged historical remainder while reviewing the new-profile obligations against their owning model. Later amendments, activation edits or changed subjects require fresh assessment; this record cannot be replayed as approval of those changes.

All six Design contract questions were assessed together: the architecture supports the reporting/decision split; compatibility, authority and failure constraints are explicit; proposal simplicity and independent-review goals are preserved; CLI storage and Workflow meaning remain separate; embedded decisions agree without extra ADRs; and the named handoff is defined enough for bounded implementation. The existing eight boundary dimensions remain represented. This correction particularly addresses input classification, authority, mixed success/failure, stale review and historical compatibility without changing storage, concurrency, recovery or external-edit guarantees.

One required adoption reconciliation remains explicit: `specs/boundary-first-proof-model.md` currently says historical feature validation remains unchanged. That sentence and the named inherited review-owner clauses must agree with the approved reporting-only handoff before the changed validator is relied on. Workflow's Adoption support surfaces/completion check already owns that exact governing diff and prohibits deferred required dependencies. This review does not declare the source amended, override it silently or approve a blanket historical exemption. Existing feature-format/activation requirements and semantic review stay mandatory; only the reporting/owner handoff changes as selected here.

The design is sufficient for the bounded M4 implementation under separate user authority. ER-M4-002 remains Code Review-owned for implementation disposition: tests must establish review-only exit behavior, mixed-error failure and retained fail-closed cases, followed by affected independent review. No implementation result follows from this Design approval.

Commands used: complete `cat` reads of both members and required Design-review resources, and bounded `sed`, `tail`, `rg` and `git diff HEAD` reads of proposal, authority, prior evidence and shared-spec amendments. No content hashes, lifecycle operations or implementation tests were used as Design judgment.

## M4 adoption wording — independent classification refresh

- Skill: design-review
- Review status: approved (isolated advisory scope)
- Package members: `workflow` → `docs/design/workflow.md`; `cli` → `docs/design/cli.md`
- Upstream review ID: None; existing advisory proposal judgment, unchanged reviewed models and explicit user M4 authority
- Review ID and round: No formal identity assigned; bounded adoption-reconciliation assessment
- Material findings: None at Design in these shared-spec amendments
- Correction targets: None for the assessed wording
- Recording status: recorded, advisory-durable
- Settlement status: not-applicable
- Open blockers: Independent M4 Code Review and remaining adoption evidence remain separate; this is not their approval
- Immediate next stage: Isolated return of classification to coordinator
- Claim limitations: No implementation correctness, release, formal registration, complete M4 or final verification

The same independent reviewer, who authored neither model nor shared-spec amendments, reassessed the current adoption wording against the complete, unchanged two-model Design package and its approved handoff. The earlier classification covered only prospective/disabled wording and is not reused as approval of this changed text. This result applies only to the isolated worktree's current candidate.

| Exact current amendment | Independent classification and reasoning |
| --- | --- |
| `specs/rigorloop-workflow.md`, `Explicit recording` heading and two opening paragraphs | New-profile-only adoption reconciliation. The first paragraph now selects explicitly requested new roots, names the matching recorder distribution and `record-store inspect` context, and explicitly preserves historical procedures without conversion. The second retains the full independent review/Verify sequence and actor-owned decisions. These implement WF-SR-01/03/07/09/10 and CLI-SR-01/10; they do not edit or approve a changed historical remainder. |
| `specs/skill-contract.md`, first paragraph of `Goal and context` | New-profile-only adoption reconciliation. The current paragraph applies model shapes only to explicitly selected new changes in an adopting project, retains naming, self-containment, resource integrity, independence, evidence and claim boundaries, and requires matching CLI/templates/adapters. Distribution availability expressly grants neither adoption nor review authority. The historical remainder is unchanged. This agrees with WF-SR-07/08/10. |

Both classifications are affirmative reviewer judgments against these exact sections, not inferred approvals or a declaration that the candidate is fully implemented. They are substantive for the new profile, not disguised formatting changes. Historical handlers and their obligations remain governed by the retained remainder. Further activation or shared-authority edits invalidate reliance on this bounded assessment until reassessed.

All six Design criteria remain satisfied for this reconciliation: selected behavior has an explicit recorder/actor architecture, real authority and compatibility limits remain, the accepted direction is preserved, storage and semantic trust boundaries remain separate, embedded decisions agree, and no additional Design choice is required by these amendments. The eight existing model boundary dimensions and their proof obligations remain unchanged. One file per model, no OS investigation, no in-place migration, and the separate final whole-change review are preserved.

Read evidence: current shared-spec diffs and scoped governance/profile amendments, the complete previously read unchanged model members, accepted proposal and prior independent Design/Delivery records. No hashes or code-test result is used to infer Design approval. ER-M4-004's separate public-command integration defect remains Code Review-owned; this classification does not resolve it.
