# Code Review: M4 R11 Stage-Evidence Integrity Binding

## Review metadata

Review ID: code-review-m4-r11
Stage: code-review
Round: M4 R11
Reviewer: separate replacement blind-review agent
Target: M4 correction commit `79d3f40e`
Reviewed artifact: commit `79d3f40e`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR18
Immediate next stage: review-resolution M4

Automated review: yes
Review gate outcome: stop
Native review status: changes-requested
Independence level: L2
Reviewer context ID: m4-r11-reblind-review-agent
Context separation mechanism: A replacement fresh reviewer received an exact bounded neutral packet after the first attempted reviewer reported accidental later-evidence exposure. The replacement reviewer inspected only the production/test diff and exact governing sections, recorded the blind-first risk map, and received validation summaries, prior review evidence, and the prior finding only after the risk-map phase was accepted.
Risk tier: elevated
Risk-tier triggers: Durable review identity and outcome, stage-owned evidence, completed-receipt integrity, recovery, correction routing, and fail-closed validation changed or became jointly binding.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R047, BRF-R068 through BRF-R077, BRF-R100, BRF-R101, and BRF-R102; T10 through T12 proof.
Initial packet inventory: scripts/workflow_automation_state.py@79d3f40e#sha256:965fceb786e1d73d6ef27e81423950f25674b0c744fe5383a5ec2715824db8a4; scripts/validate_workflow_automation.py@79d3f40e#sha256:c0281e17f77d9c41d1b990f003d085ad74725814ffe4251887cf091cbef3b82e; scripts/test-workflow-automation-state.py@79d3f40e#sha256:307c482a48f7dba7fa0b1430d939534cb70d942f4db8d88deffdf145d62d8d37; scripts/test-validate-workflow-automation.py@79d3f40e#sha256:f642a5eb930c847fb812a30132b34f6f474d9033edc70b81ccba93be03372aeb; specs/single-bounded-review-fix-workflow-automation.md@79d3f40e#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@79d3f40e#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@79d3f40e#sha256:5cff1feb6ea1d9ab54d6d0998d85a564563a7260fa1b9a95e2f422d43ff23c32
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:03f38744a5cb68280a542eb41f63c6c063a697e54363a05f2b44ab348e015146
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/workflow_automation_state.py`; `scripts/validate_workflow_automation.py`; their state and validator tests; M4 review evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, reviewer-authored property decomposition, production diff, tests, validation evidence, prior findings

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR17` failed remediation leaves residual `BRF-M4-CR18`, which blocks M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR18`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r11.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r11`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR18`
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `79d3f40e` against parent `08510eb4`, with the implementation/test diff and exact governing clauses inspected before later evidence.
- Tracked governing branch state: commit `79d3f40e`; R11 review evidence was added only after the verdict.
- Governing requirements: BRF-R047, BRF-R068 through BRF-R077, BRF-R100, BRF-R101, and BRF-R102.
- Test contract: T10 through T12 and the M4 CMD15-CMD20 proof boundary.
- Architecture: stage-owning skills own formal review judgments and stage-native completion evidence; the state adapter owns persisted automation state and evidence-first reconciliation.
- Prior review and resolution: `code-review-m4-r10.md` and the BRF-M4-CR17 disposition, released only after the risk map.

## Blind-first risk map

Affected behavior: Completed proposal-review finalization now persists a separate review-evidence snapshot; durable validation reconstructs route and latest-result state from that snapshot and cross-checks proposal input, canonical evidence, observed identity, and one output.

Highest-impact failure modes: A coordinated evidence, route, and latest-result rewrite becomes self-authenticating; parent-format completed receipts become unreadable; outputs are over- or under-bound; projection completeness remains mutable; or completed recovery re-parses stage evidence but ignores a contradiction with persisted review facts.

Changed boundaries: Verifier proof to durable receipt facts; receipt snapshot to routing projection; canonical evidence to output identity; completed receipt to recovery; and review occurrence to correction authority.

Evidence expected: Coordinated fact-rewrite probes; parser-backed proof-to-envelope comparison; all four outcomes; malformed evidence; output and canonical contradictions; recovery and cancellation parity; and unknown-value precedence.

Areas requiring direct inspection: `_project_completed_proposal_review`; `resolve_recorded_proposal_review_receipt`; `verify_transition_completion`; completed recovery; transition key fields; terminal receipt immutability; projection and latest-result validation; and state-store round trips.

Areas intentionally out of scope: M5, M6, public activation, compatibility aliases, generated adapters, external actions, final verification, and PR readiness.

Risk classes considered: Durable-state integrity, stage-evidence ownership, authorization binding, recovery, closed vocabularies, compatibility, partial output, and test adequacy were applicable. Secrets, privacy, network, deployment, UI, and material performance risks were not applicable.

Falsifiable review questions: Can evidence, route, and latest review ID or outcome be changed together? Does a canonical review-record identity cryptographically bind those facts and get rechecked on resume? Can all record/output/canonical identities be coherently rewritten? Does completed recovery compare parser-derived facts with the persisted envelope? Can a terminal receipt be rewritten outside the state adapter without semantic detection?

## Diff summary

Commit `79d3f40e` adds a mandatory `proposal_review_evidence` envelope. Normal and cancellation finalization populate it from parser-backed `VerifiedCompletion`; the structural validator projects the route from this envelope, checks its exact field set and closed outcome, and binds review output identity to canonical and observed identities.

The tests prove route-only review-ID and known-outcome rewrites fail, require the new envelope, reject unknown evidence outcomes, reject a one-sided output mismatch, and confirm normal and cancellation paths persist the snapshot. They do not change the envelope in concert with its route and latest result, and recovery does not compare re-parsed stage facts with the persisted envelope.

## Prior-finding reconciliation

| Prior finding | R11 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR17` | failed-remediation | The fix moves authority from the route into a second mutable receipt copy. Coordinated envelope, route, and latest-result rewrites validate with zero errors. Parser-backed completed recovery observes the original review ID and outcome but returns `continue` without comparing them to the forged envelope. |

## Findings

## Finding BRF-M4-CR18

Finding ID: BRF-M4-CR18
Severity: major
Location: `scripts/validate_workflow_automation.py:276-365`; `scripts/workflow_automation_state.py:600-655`; coverage gap in `scripts/test-validate-workflow-automation.py:724-955`
Evidence: `resolve_recorded_proposal_review_receipt` uses `receipt.proposal_review_evidence` as the source for review ID and outcome, then checks other mutable receipt/result fields against that same source. The prepared transition key does not cover terminal review facts, so it cannot independently authenticate this copy. The parser independently recovers review ID and outcome during `verify_transition_completion`, but completed recovery compares only outputs and canonical identities and discards the semantic contradiction. Direct probes changed evidence, route, and latest review ID together and returned zero errors; changed evidence, route, latest outcome, and clean gate together and returned zero errors; and coherently changed review-record, output, canonical, observed, route, evidence, and latest identities and returned zero errors. A real parser-backed recovery probe retained the true `proposal-review-r1/approved` facts while the receipt stated `proposal-review-forged/changes-requested`, yet returned `continue completed-evidence-current`.
Required outcome: Every completed proposal-review receipt must validate review ID, outcome, reviewed proposal identity, and review-record identity against independently re-read or independently integrity-bound stage-native evidence. Completed recovery must pause on any mismatch between parser-derived `VerifiedCompletion` facts and the persisted envelope, route, or latest projection. Coordinated receipt/result rewrites must not become self-authenticating.
Safe resolution path: Define one canonical projection from `VerifiedCompletion` to the proposal-review evidence envelope and reuse it during finalization and completed recovery. After `verify_transition_completion` re-reads the formal review and review log, compare the projected envelope exactly with persisted `proposal_review_evidence`, then validate route and latest result from that independently derived projection. Ensure every status or resume path that claims semantic validity uses repository-root-backed parsing. Add regressions that jointly mutate envelope, route, and latest result for review ID and every alternative known outcome, plus a recovery regression that requires pause when parser facts contradict the persisted envelope. Retain the coherent output/canonical identity probe.
needs-decision rationale: none; the approved stage-owned evidence and recovery contracts already select independent evidence. The remediation stops one comparison short.
auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R047 records exact review ID and one closed outcome | block | Both can be coordinately rewritten in evidence, route, and latest result while validation passes. |
| BRF-R068 deterministic prepared key | pass | The prepared key still covers immutable pre-stage operation inputs; terminal proof needs a separate independent comparison. |
| BRF-R069 completed receipt records output and canonical synchronization | pass structurally | Required fields and exact singleton output are enforced. |
| BRF-R073 inspects stage-owned evidence before resume | block semantically | Recovery re-parses the evidence but ignores its review-ID and outcome contradiction with persisted state. |
| BRF-R074 reconciles valid evidence without rerun | block | Forged completed state is treated as current rather than paused for reconciliation. |
| BRF-R076 canonical or output mismatch pauses | block for complete review integrity | Coordinated semantic and identity rewrites remain accepted. |
| BRF-R077 partial or unknown evidence fails closed | pass for the changed surface | Missing envelope and unknown evidence outcome reject. |
| BRF-R100 status and resume rely on tracked identities and receipts | block | Persisted semantic facts are trusted as self-consistent copies instead of being checked against tracked artifact bytes during recovery. |
| BRF-R101 unknown values fail before consistency | pass | Unknown evidence outcome is rejected by vocabulary validation first. |
| BRF-R102 unknown-value regression exists | pass | The new unknown-evidence-outcome test covers the closed field. |
| T10 proposal-review occurrence, gate, and routing | block | Ordinary matrices pass; coordinated durable rewrite and recovery contradiction are not covered. |
| T11 correction is bounded | concern | Correction selection derives from the mutable outcome envelope, although the selected capability basis is checked. |
| T12 review isolation | not applicable | No review invocation or reviewed-artifact edit boundary changed. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R047, BRF-R073, BRF-R074, BRF-R076, and BRF-R100 remain incomplete. |
| Test coverage | block | No coordinated envelope rewrite or parser-proof-versus-envelope recovery regression exists. |
| Edge cases | block | Coordinated ID, outcome, and identity rewrites pass. |
| Error handling | block | Completed recovery continues after observing a semantic contradiction. |
| Architecture boundaries | concern | The stage parser is invoked, but its independently owned facts are discarded at the completed-recovery decision boundary. |
| Compatibility | concern | The mandatory new field rejects parent-format completed receipts; the non-public M4 harness limits current exposure, but no explicit compatibility proof is present. |
| Security/privacy | concern | No secret or privacy issue exists; durable review and authorization history remains rewriteable. |
| Derived artifact currency | pass | No generated artifact changed. |
| Unrelated changes | pass | The implementation is scoped to the attempted fix, its tests, and required lifecycle evidence. |
| Validation evidence | block for sufficiency | Focused and broad suites omit the falsifying coordinated cases. |

## Validation and direct proof

- Independently reran 64 workflow-automation validator tests; they passed.
- Independently reran 51 state/recovery tests; they passed.
- The replacement reviewer independently reran 7 proposal-review engine tests and 15 policy tests; they passed.
- Four coordinated tamper probes returned zero validator errors.
- Parser-backed completed recovery returned `continue completed-evidence-current` while its proof retained the true review ID and outcome and the persisted envelope contained forged values.
- `git diff --check 08510eb4 79d3f40e` passed.
- The released CMD15-CMD20 and 11-check broad-smoke evidence was challenged but not independently rerun because the focused counterexample already falsified remediation.

## No-finding rationale

Not applicable; this review has one material failed remediation.

## Independent-review sufficiency receipt

- Target identity: commit `79d3f40e` against parent `08510eb4`
- Independence: L2 replacement blind reviewer; risk map recorded before later evidence and prior findings were released
- Governing artifacts inspected: exact BRF-R047, BRF-R068 through BRF-R077, BRF-R100 through BRF-R102, state invariants, T10 through T12, M4 plan section, and later R10 resolution evidence
- Risk classes: durable integrity, stage-evidence ownership, recovery, output/canonical binding, closed vocabulary, compatibility, and test adequacy
- Adversarial hypotheses: coordinated review-ID rewrite; coordinated known-outcome rewrite; coherent record/output/canonical identity rewrite; fully coordinated rewrite; parser-reread contradiction during completed recovery
- Direct proof: four structural-validator counterexamples and one real parser-backed recovery counterexample
- Validation evidence challenged: 64 validator, 51 state, 7 proposal-review engine, and 15 policy tests rerun; larger released suites are non-dispositive after focused falsification
- Unreviewed or uncertain surfaces: M5/M6, public activation, complete parent-format migration behavior, and broad-smoke rerun
- Confidence: high
- No-finding rationale: not applicable

## Residual risks

Rereview must prove independently re-read review facts govern durable validation and completed recovery, all coordinated rewrites pause or fail, and legitimate historical/cancellation paths retain their original semantics. M5 and M6 remain out of scope and blocked.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for residual finding `BRF-M4-CR18`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready
- Reason: implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending; review-state=open; open-count=1; open-findings=BRF-M4-CR18

This direct review remains isolated. It records the finding and does not automatically apply a fix or enter review-resolution.
