# Code Review: M4 R15 Source Chronology and Canonical Snapshot Rereview

## Review metadata

Review ID: code-review-m4-r15
Stage: code-review
Round: M4 R15
Reviewer: fresh blind-first reviewer agent with independent elevated-risk second review
Target: M4 correction commit `7568f910`
Reviewed artifact: commit `7568f910`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: clean-with-notes
Review status: clean-with-notes
Review date: 2026-07-24
Recording status: recorded
Material findings: None
Immediate next stage: implement M5

Automated review: yes
Review gate outcome: advance
Native review status: clean-with-notes
Independence level: L2
Reviewer context ID: m4-r15-blind-review-agent
Context separation mechanism: A fresh agent received only the exact six-file target, bounded governing clauses, architecture and ADR boundaries, and neutral M4 scope. It recorded a blind-first risk map before validation summaries, evidence menus, implementation notes, prior findings, or desired outcome were released. A second fresh reviewer independently challenged the resulting clean verdict.
Risk tier: elevated
Risk-tier triggers: Canonical review chronology, durable automation-state reads, query snapshot selection, and evidence-first recovery changed.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; approved workflow architecture and ADR; M4 milestone scope.
Formal criteria: Code-review checklist; BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, BRF-R099 through BRF-R102; T10, T15, and T22.
Initial packet inventory: scripts/review_artifact_validation.py@7568f910#sha256:47135ac99d44f4175568ef9b353fcefb52508bf0b54054ee46cf1ab9a8e92b72; scripts/workflow_automation_state.py@7568f910#sha256:57fe7981acd3f3db23002abb48eff0a537da5f18ec544fb7211a8d68ad0942dd; scripts/query-change-record.py@7568f910#sha256:1dab3db8c56e1ffb1f8a3d82b7ea1a5513cab604997b11b5e05dd79405cf4604; scripts/test-review-artifact-validator.py@7568f910#sha256:aea2a80dcc26c4159a1b7cf4b84ca63b7d5968348e96e4cc99fda84d831f4603; scripts/test-workflow-automation-state.py@7568f910#sha256:b69b9d54386828f81d01c4e2678245513706b668c8c4c388cb863fec3278660f; scripts/test-query-change-record.py@7568f910#sha256:bbac1ccd343d3f0bbdb1bc87dd542e5c1a6df70ee21f2f0f40c40489e736a695
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:8fda9f7c3793701a4bb6a3989a698d9deedbba1456814def97aab2db4dead289
Manifest owner: workflow reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Affected behavior: Accepted formal review-log representations now share canonical physical chronology, proposal-review aggregate semantics bind that chronology, and bounded queries validate and project one state-adapter snapshot.
Highest-impact failure modes: Record-format grouping could select an older occurrence; a stale preliminary parse could hide valid or invalid unified state; query-only compatibility could weaken unified or write paths; recovery could rerun or continue from contradictory evidence.
Changed boundaries: Review parser to durable review semantics; change-record query to state adapter; automation-specific error classification; query-only legacy tolerance.
Evidence expected: Both mixed-format source orders, later-occurrence and rewind proof, same-snapshot valid and invalid query contrasts, strict unified/write identity checks, byte preservation, and no-reinvoke recovery.
Areas requiring direct inspection: `_parse_review_log`; `_verify_transition_completion`; `validate_workflow_automation_semantics`; `WorkflowAutomationStateStore.read`; `load_change_metadata`; focused parser, state, query, and recovery tests.
Areas intentionally out of scope: M5 and M6 integration, public command cutover, final holistic review, verification, PR readiness, and external actions.
Risk classes considered: canonical chronology, durable state integrity, read-only snapshot consistency, recovery/idempotency, compatibility, error taxonomy, closed-vocabulary handling, path integrity, and scope containment.
Falsifiable review questions: Do both accepted formats retain physical order; can latest state rewind; can a stale first parse bypass unified state; does legacy tolerance reach unified or mutation paths; do invalid states mutate files or reinvoke stages?

Clean-review sufficiency receipt: yes
Review target identity: commit `7568f910`
Governing artifacts inspected: approved spec clauses BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, and BRF-R099 through BRF-R102; T10, T15, and T22; bounded architecture and ADR passages; exact six-file diff.
Adversarial hypotheses tested: format grouping overrides chronology; older result rewinds latest review; duplicate occurrence proceeds; stale first parse hides unified automation; legacy tolerance weakens strict paths; diagnostics collapse; reads mutate bytes; compact expansion replaces the snapshot; recovery reruns or proceeds on unsafe evidence.
Direct proofs performed: both mixed-format parser orders; later-occurrence and rewind state tests; same-snapshot and no-automation-first query tests; focused recovery policy and drift tests; adapted legacy/unified/write-boundary, diagnostic, byte-preservation, compact-expansion, and duplicate-review probes.
Validation evidence challenged: Aggregate counts were compared with changed branches and named negative cases. The primary reviewer reran 104 parser, 57 state, and 22 query tests from the exact target tree; the second reviewer reran 13 focused tests and the scoped diff check.
Unreviewed surfaces: M5/M6 integration, public aliases, final public result composition, final holistic review, verification, and PR handoff.
Confidence: high
No-finding rationale: The two prior defects are corrected at their shared parser/state and query/state boundaries, direct negative proof covers the changed branches, and neither independent reviewer found contradictory in-scope evidence.

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/review_artifact_validation.py`; `scripts/workflow_automation_state.py`; `scripts/query-change-record.py`; their three focused test modules.
Requirement-fidelity matched path triggers: scripts/*validator*; docs/changes/**/reviews/
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence > prior findings
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: none found
Requirement-fidelity no-finding rationale: Chronology is projected consistently from parser through completion proof and aggregate semantics; query validation and projection share one state-store snapshot; legacy tolerance is explicitly bounded; recovery and read-only properties have direct negative evidence.

## Phase receipts

| Phase | Status | Evidence |
| --- | --- | --- |
| neutral-initial-packet | recorded | Exact six-file target, bounded governing clauses, architecture and ADR passages, and neutral M4 scope only. |
| risk-map-recorded | recorded | The primary reviewer recorded affected behavior, failure modes, boundaries, evidence expectations, risk classes, and falsifiable questions before later evidence. |
| evidence-menu-released | recorded | Targeted parser/state/query results and bounded adversarial probes were released only after the risk map. |
| evidence-results-released | recorded | The reviewer reran focused suites and independently challenged chronology, snapshot, compatibility, diagnostics, byte preservation, and recovery. |
| prior-findings-released | recorded | `BRF-M4-CR22`, `BRF-M4-CR23`, their claimed fixes, and reported broader validation were released after the evidence challenge. |
| verdict-recorded | recorded | Both prior findings were resolved; the primary verdict was clean-with-notes. |
| elevated-second-review | recorded | A second fresh reviewer returned `agree-clean`; no `BRF-M4-CR24` was issued. |

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review-resolution summary, active plan, plan index, and change metadata
- Open blockers: none for M4
- Next stage: implement M5
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r15.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: not-required for new findings; prior R14 resolution remains closed
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: closed
- Remaining implementation milestones: M5, M6
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `7568f910` against parent `97999fc6`.
- Tracked governing branch state: approved specification, architecture, ADR, active test specification, and active plan are tracked.
- Primary review evidence: neutral blind-first risk map, staged evidence challenge, requirement-property comparison, and prior-finding reconciliation.
- Elevated second review: `agree-clean` after independent six-file inspection and 13 focused tests.

## Diff summary

The correction source-sorts the combined detailed and clean-table review-log projection, records canonical occurrence line in proposal-review completion proof, and uses that line for aggregate latest and duplicate checks.

The query helper now obtains its projected document from one unconditional state-store read. Invalid unified state uses an automation-specific exception, while query-only legacy tolerance remains ineffective for unified state and is not used by mutation paths.

Tests cover both record-format orders, mixed-format latest/rewind semantics, and stale parser views that omit valid or invalid tracked unified automation.

## Prior-finding reconciliation

| Prior finding | R15 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR22` | resolved | The parser source-sorts both accepted formats, durable proof stores the canonical line, aggregate semantics uses physical occurrence order, both source orders pass, and older-result rewind fails. |
| `BRF-M4-CR23` | resolved | Query loading unconditionally projects the state-store document; valid and invalid no-automation-first contrasts pass; legacy tolerance cannot bypass unified or strict write checks. |

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The M4-owned BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, and BRF-R099 through BRF-R102 properties remain satisfied. |
| Test coverage | pass | Both mixed formats, latest rewind, same-snapshot loading, invalid unified state, compatibility, and focused recovery branches have direct proof. |
| Edge cases | pass | Duplicate review evidence, change-ID mismatch, malformed shape, unsafe path, compact expansion, identity drift, and no-evidence retry were challenged. |
| Error handling | pass | Unified contract failures remain distinct from unsupported shape and every challenged query path preserves file bytes. |
| Architecture boundaries | pass | Stage-owned review evidence remains authoritative and the state adapter owns canonical automation reads and writes. |
| Compatibility | pass | Non-unified legacy/compact reads retain compatibility while unified and mutation paths stay strict. |
| Security/privacy | pass | No secret, network, external-action, or authorization-widening surface changed. |
| Derived artifact currency | pass | No generated or derived public artifact changed. |
| Unrelated changes | pass | The six-file correction is limited to chronology, snapshot loading, error classification, and regressions. |
| Validation evidence | pass | Directly affected suites and focused negative probes passed; broader released evidence was challenged rather than accepted by count alone. |

## Requirement-property coverage

| Requirement family | Result | Evidence |
| --- | --- | --- |
| BRF-R006, BRF-R099, BRF-R100 | pass for M4-owned status/query surfaces | One validating snapshot supplies the read-only projection and tracked identities. |
| BRF-R047, BRF-R066 | pass | Canonical source chronology preserves history and prevents older-review rewind. |
| BRF-R073 through BRF-R077 | pass for affected recovery surface | Valid completion does not reinvoke; missing/partial/drift evidence follows policy or pauses/fails closed. |
| BRF-R101, BRF-R102 | pass | No new vocabulary was added and existing unknown-value regressions remain passing. |
| T10, T15, T22 | pass for changed M4 surfaces | Mixed chronology, evidence-first recovery, and same-snapshot read-only status have direct proof. |

## No-finding rationale

The blind-first review identified the same two dominant defect classes later released from R14: cross-format chronology corruption and stale preliminary-parser snapshot bypass. The correction repairs each issue at both affected boundaries rather than masking it in tests. Independent focused proof covers the relevant positive and negative paths, and the elevated second reviewer agreed with the clean result.

## Residual risks

- M5 and M6 integration, public command/alias composition, final public result composition, final holistic review, verification, and PR readiness remain unreviewed.
- Synthetic duplicate numeric source positions are not naturally constructible in the line-oriented parser; realizable duplicate review IDs and receipt-to-occurrence duplication fail closed.
- The bounded rereview did not isolate every unchanged T10/T15 branch, but full affected suites passed and focused proof covers every changed boundary.
- The existing lifecycle merge-language warning remains visible as non-blocking baseline evidence.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no; all 78 material findings are resolved
- Remaining in-scope implementation milestones: M5, M6
- Next stage: implement M5
- Final closeout readiness: not ready; two implementation milestones, final holistic review, explanation, verification, and PR handoff remain

This direct review is isolated and does not start M5 automatically.
