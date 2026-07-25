# Code Review M5 R1

Review ID: code-review-m5-r1
Stage: code-review
Round: M5 R1
Reviewer: fresh blind-first reviewer agent
Target: M5 implementation commit `27aa4eb0`
Reviewed artifact: M5 implementation commit `27aa4eb0`
Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-24
Recording status: recorded
Material findings: BRF-M5-CR1, BRF-M5-CR2, BRF-M5-CR3, BRF-M5-CR4, BRF-M5-CR5
Immediate next stage: review-resolution M5

Automated review: yes
Review gate outcome: stop
Native review status: changes-requested
Independence level: L2
Reviewer context ID: m5-r1-fresh-blind-review-agent
Context separation mechanism: The first candidate reviewer self-disqualified after accidentally seeing plan validation notes and produced no risk map or verdict. A fresh reviewer then received only the exact implementation diff and bounded governing clauses. Validation results, direct probes, prior findings, author summaries, and desired outcomes were withheld until its blind-first risk map was recorded.
Risk tier: elevated
Risk-tier triggers: Autonomous implementation correction, milestone-closing formal review, durable transition completion, final verification authority, and the hard external-action boundary changed.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; approved workflow architecture and ADR; M5 milestone scope.
Formal criteria: Code-review checklist; BRF-R060 through BRF-R067; BRF-R073 through BRF-R090; BRF-R099 through BRF-R100; T13, T15, T17, and T18.
Initial packet inventory: scripts/workflow_automation.py@27aa4eb0#sha256:35b227e047ebf107348bce707df5a380aeb5d08e8557e63856ba3b86edea7438; scripts/workflow_automation_state.py@27aa4eb0#sha256:cab1b4e73fa4d42fad14e877f7398cdc50a5320c506ad9c783842bf0ea984ea9; scripts/test-workflow-automation.py@27aa4eb0#sha256:5a0211aaa696f77015a83e0a232f54fd19be33b4433626d93523777fde71e9be; scripts/test-workflow-automation-state.py@27aa4eb0#sha256:99529409f5bed67d94e15635ca001455326e2013fa7084014a1bdc6983c57a60; specs/single-bounded-review-fix-workflow-automation.md@27aa4eb0#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@27aa4eb0#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@27aa4eb0#sha256:4acc92450f17cf380235657a3e3b3293c7a71568982eea92611dd99acd84df3f; docs/architecture/system/architecture.md@27aa4eb0#sha256:3ad5871a99f96f86e7beed58137a6eab7fdf235a0a36dd5c25f3ea6899e9dca8; docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md@27aa4eb0#sha256:72f84faada32301b58221e008f7bd90d198bc002e51ffa868e5210b1299bd538
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:b1a05ebe31cb158936ccef703b0de1b236d31d7d33ecddd530a1b3462040c75c
Manifest owner: workflow reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/workflow_automation.py`; `scripts/workflow_automation_state.py`; `scripts/test-workflow-automation.py`; `scripts/test-workflow-automation-state.py`
Requirement-fidelity matched path triggers: docs/changes/**/reviews/
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, reviewer-authored property decomposition, production diff, tests, validation evidence
Requirement-fidelity outcome: failed
Requirement-compression result: The implementation compresses correction into an uncalled pure evaluator, validation into first colon-delimited fields, resolution into review-log open IDs, final review into one scope label, explanation into two labels, and verification authority into nonempty strings plus caller booleans.

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Recording status: recorded
- Open blockers: `BRF-M5-CR1` through `BRF-M5-CR5`
- Next stage: review-resolution M5
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5 resolution and rereview, M6
- Verify readiness: not claimed
- PR readiness: not claimed
- Automatic correction: prohibited because every finding has `auto_fix_class: none`

## Blind-first risk map

The reviewer identified correction authorization, stage-owned evidence, milestone ordering, formal-review currentness, recovery, verification authority, external-action containment, and non-public reachability as the changed trust boundaries before seeing validation results.

Highest-impact falsifiable questions included whether implementation correction had an executable receipt-backed caller; whether caller booleans could manufacture final-review, explanation, or verification readiness; whether duplicate or contradictory evidence failed closed; whether milestone review required the latest contained formal occurrence and real review resolution; and whether success was proven to stop before external action.

Affected behavior: Reviewer-owned implementation correction, ordered milestone implementation and review, stage-native completion, final holistic review, explanation, verification, and final canonical position.
Highest-impact failure modes: Unexecutable correction; manufactured verification authority; contradictory evidence accepted as passed; stale or external review evidence; false resolution closure; external-action boundary represented only by assertion.
Changed boundaries: Formal review to correction authority; plan and validation evidence to milestone closure; review and explanation evidence to verification; verification result to the stop before PR.
Evidence expected: Repository-backed correction transactions, authoritative artifact parsers, latest contained reviews, real closed resolution, identity-checked verification basis, external-action traps, and recovery contrasts.
Areas requiring direct inspection: `evaluate_implementation_correction`; `coordinate_non_public_implementation_stage`; `_evidence_fields`; `_milestone_state`; `_canonical_review_occurrence`; `_verify_implementation_stage_completion`; M5 transaction fixtures.
Areas intentionally out of scope: M6 public cutover, legacy-writer removal, adapter generation, PR creation, release, deployment, publication, merge, and other external actions.
Risk classes considered: Authorization integrity; autonomous mutation; reviewer independence; durable-state consistency; milestone ordering; recovery; validation authenticity; formal-review currentness; verification safety; filesystem containment; external side effects.
Falsifiable review questions: Can correction execute through a capability-bound receipt; can caller booleans reach verify; can contradictory fields or duplicate milestones pass; can a symlink or stale review approve closure; can the log replace resolution; can verify cross the external boundary?

## Findings

### BRF-M5-CR1 — Implementation correction is not integrated into an executable workflow path

Finding ID: BRF-M5-CR1
Severity: major
Location: `scripts/workflow_automation.py:308-406`, `scripts/workflow_automation.py:516-522`, `scripts/workflow_automation.py:1441-1547`, and `scripts/workflow_automation_state.py:497-523`
Evidence: `evaluate_implementation_correction` has no production caller. The code-review router exposes a `changes-requested` correction branch, but the stage-native code-review verifier accepts only `approved` and `clean-with-notes`, so a real transaction cannot finalize the review result needed to enter that branch. The coordinator never parses reviewer findings or resolution evidence, executes a reviewed correction recipe, or binds convergence to a prepared receipt. The green T13 test calls the pure helper directly.
Required outcome: A recorded `changes-requested` milestone review may enter correction only through a current implementation-correction capability whose reviewer-owned classification, exact recipe, finding set, budget, path scope, and validation are repository-backed. The correction must use the prepared-receipt path, prove strict convergence, and require fresh independent rereview.
Safe resolution path: Add a dedicated integrated implementation-correction coordinator using canonical review and resolution parsers, a closed executable operation, capability-bound receipt evidence, post-mutation diff and validation proof, stale-review invalidation, and end-to-end T13 contrasts.
needs-decision rationale: none; the approved contract already selects the authority and convergence boundaries.
auto_fix_class: none

### BRF-M5-CR2 — Verification readiness trusts caller assertions instead of tracked closeout evidence

Finding ID: BRF-M5-CR2
Severity: major
Location: `scripts/workflow_automation.py:441-444`, `scripts/workflow_automation.py:1448-1451`, `scripts/workflow_automation.py:1529-1538`, `scripts/workflow_automation_state.py:545-598`, and `scripts/test-workflow-automation.py:3352-3450`
Evidence: The transaction wrapper accepts `verification_authorized`, `final_review_clean`, and `explanation_current` from the caller and forwards them when current-stage proof lacks those facts. Verification-basis validation requires only nonempty strings. The positive transaction uses opaque fake identities and all three booleans without creating final-review or explanation artifacts. Label-only final-review and explanation artifacts, and contradictory verify results, were accepted by direct probes. The test checks a returned `external_action_performed=False` value but does not install T18's external-action trap.
Required outcome: Verification authorization, final-review cleanliness, explanation currentness, branch and command inputs, and verify success must derive exclusively from current canonical artifacts and finalized receipts. Final holistic review must prove its complete scope, and an external-action trap must prove the stop before PR.
Safe resolution path: Remove caller-boolean fallbacks, resolve and rehash every verification-basis artifact, use stage-owned final-review and explanation contracts, and add missing/stale/tampered basis plus real external-action-trap tests.
needs-decision rationale: none; BRF-R085 through BRF-R090 already define the boundary.
auto_fix_class: none

### BRF-M5-CR3 — Stage-native parsers accept contradictory validation and duplicate milestone evidence

Finding ID: BRF-M5-CR3
Severity: major
Location: `scripts/workflow_automation_state.py:396-424`, `scripts/workflow_automation_state.py:476-495`, and `scripts/workflow_automation_state.py:532-598`
Evidence: `_evidence_fields` keeps the first value for duplicate labels, and `_milestone_state` keeps the first matching milestone heading. Direct probes accepted `Result: passed` followed by `Result: failed`, contradictory verify result fields, and a plan containing duplicate M2 headings with different states. The M5 tests contain no equivalent contradictory artifacts.
Required outcome: Every M5 stage artifact must use an authoritative shape-aware parser that rejects duplicate required fields, conflicting values, unknown closed values, invalid structure, duplicate milestones, and handoff/body contradictions before consistency evaluation.
Safe resolution path: Reuse canonical artifact and active-plan parsers. Where a new evidence format is necessary, define a closed exact-one-field contract, bind validation to implementation and command identities, and add direct unknown, duplicate, contradiction, recovery, and ordering regressions.
needs-decision rationale: none; fail-closed evidence handling is already required.
auto_fix_class: none

### BRF-M5-CR4 — Review completion accepts external symlink evidence and stale review occurrences

Finding ID: BRF-M5-CR4
Severity: major
Location: `scripts/workflow_automation_state.py:427-458`, `scripts/workflow_automation_state.py:497-523`, and `scripts/workflow_automation_state.py:545-565`
Evidence: `_canonical_review_occurrence` checks lexical placement but does not reject a symlinked review log or resolve it for containment. A direct probe accepted an in-repository log symlink to an external file. The helper matches only the requested ID and does not require the latest applicable occurrence; a direct probe accepted R1 approved after the canonical log recorded R2 inconclusive. Both milestone and final review use this helper.
Required outcome: Review evidence must be a non-symlink canonical repository/change-root file, and completion must use the latest applicable review for the bound artifact identity, milestone or final occurrence, and review type.
Safe resolution path: Reuse the repository-safe resolver, compare all applicable occurrences in canonical source order, and add external-symlink, path-escape, later blocking outcome, duplicate-ID, and identity-drift tests for milestone and final review.
needs-decision rationale: none; current canonical formal review is already the required authority.
auto_fix_class: none

### BRF-M5-CR5 — Milestone code review substitutes the review log for review resolution

Finding ID: BRF-M5-CR5
Severity: major
Location: `scripts/workflow_automation_state.py:497-523` and `scripts/test-workflow-automation.py:3208-3239`
Evidence: The verifier names an input `review-resolution` but requires its path to equal `review-log.md`, then infers `review_resolution_closed: true` from no open IDs in the current entry. The positive test deliberately supplies the log under the resolution key. A direct probe passed with no `review-resolution.md`; a real closed resolution artifact would fail the path-equality check.
Required outcome: Distinguish clean reviews that need no resolution from material reviews that require canonical closed `review-resolution.md`, final dispositions, actions, rationale, validation, and no open log findings.
Safe resolution path: Reuse `parse_formal_review_resolution` and the formal closeout predicate; project truthful `not-required` versus `closed` gate evidence; add clean/no-resolution, open, closed, needs-decision, stale, and older-open-finding regressions.
needs-decision rationale: none; the review-resolution contract already owns this distinction.
auto_fix_class: none

## Requirement fidelity

| Contract | Result |
| --- | --- |
| BRF-R060 through BRF-R065 / T13 | Blocked because reviewer-owned correction is only a disconnected helper. |
| BRF-R067 | Partial: failure pauses, but the tracked verification gate is bypassable. |
| BRF-R073 through BRF-R077 / T15 | Blocked because contradictory, ambiguous, stale, and external evidence is accepted. |
| BRF-R078 | Blocked because caller booleans and permissive local parsers replace stage-owned authority. |
| BRF-R081 through BRF-R084 / T17 | Blocked by ambiguous plan state, stale review, and false resolution closure. |
| BRF-R085 through BRF-R090 / T18 | Blocked by caller-manufactured closeout evidence and the missing external-action trap. |
| BRF-R099 through BRF-R100 | Blocked because recorded results can derive from non-current or contradictory evidence. |

## Checklist coverage

| Check | Result |
| --- | --- |
| Spec alignment | block |
| Test coverage | block |
| Edge cases | block |
| Error handling | block |
| Architecture boundaries | block |
| Compatibility and isolation | concern; literal context checks pass, actual dispatch proof remains deferred to M6 |
| Security and trust boundaries | block |
| Derived artifact currency | pass |
| Unrelated changes | pass |
| Validation evidence | block for adequacy |

## Validation and direct proof

- Independently ran `python scripts/test-workflow-automation.py`: 52 tests passed.
- Independently ran `python scripts/test-workflow-automation-state.py`: 57 tests passed.
- The fresh reviewer also ran the 64 automation-validator, 15 policy, 104 review-artifact, and 156 lifecycle suites; all passed.
- Python compilation and `git diff --check 3311da6b..27aa4eb0` passed.
- Direct probes reproduced contradictory result acceptance, duplicate milestone acceptance, label-only final review and explanation acceptance, external review-log symlink acceptance, stale approved-review acceptance, and review-log-as-resolution acceptance.
- Passing suites are credible for their fixtures but insufficient because positive fixtures encode several defects and omit the reproduced trust-boundary contrasts.

## Downstream routing

M5 is `resolution-needed`. M6 must not start. Every finding is reviewer-classified `auto_fix_class: none`, so no automatic correction is authorized. After explicit review resolution and implementation, rerun independent M5 code review; any clean elevated-risk outcome requires the configured second-review gate.
