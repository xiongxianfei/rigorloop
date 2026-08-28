# Code Review: Milestone Completion and Replay Correction R3

Review ID: code-review-deadlock-r3
Stage: code-review
Round: r3
Reviewer: Codex same-context fresh-assumption direct reviewer
Reviewer context ID: root-deadlock-correction-r3-review
Author context ID: root-deadlock-correction-r3-implementation
Independence level: L0
Context separation mechanism: same-context fresh-assumption reset followed by artifact-first diff, contract, failure-path, and direct-proof inspection
Author context excluded: false
Target: correction of `RLCLI-DEADLOCK-CR1` and `RLCLI-DEADLOCK-CR2`
Reviewed milestone: none
Reviewed artifact: isolated post-close governed lifecycle CLI correction
Review date: 2026-08-27
Status: inconclusive
Review status: inconclusive
Review gate outcome: inconclusive
Material findings: none
Open findings: none
Recording status: recorded
Automated review: no
Native review status: inconclusive
Risk tier: elevated
Risk-tier triggers: workflow routing authority; milestone settlement; current-revision replay; durable evidence identity; legacy-state compatibility
Risk-tier classifier: affected-path-and-contract-surface-v1
Initial packet inventory: packages/rigorloop/dist/lib/lifecycle-operations.js@working-tree#sha256:e8cc606851121e7025c7f43d412ab52d99bcf2d370e4656f83a8b7bdcc4ec37a; packages/rigorloop/test/lifecycle-milestone.test.js@working-tree#sha256:cbd9ab0e6d5b5287aef2d3608e20a365de832b56180b2e92fb8ca89fd54b5232; specs/governed-lifecycle-cli.md@working-tree#sha256:06e8856209816c1692cc3baab4a41b3936b8118f6be4c668de7a80665f0c1b82; specs/governed-lifecycle-cli.test.md@working-tree#sha256:84e93b72a2416d8ede18c83916b6a9e93f90798602e02ecd482f8c4e9bcae0ba; docs/architecture/system/architecture.md@working-tree#sha256:78e708c76b5f787e4f54e55d16d7abc827dd16f90ea578b4dec11f06cf93ff67; docs/changes/2026-08-24-governed-lifecycle-cli/evidence/deadlock-completion-replay-correction-r1.md@working-tree#sha256:e925557f0d8367b00daa46f72024230ca9c407344fb835124b9632680b87904f
Initial packet hash: sha256:192af5cf09d0cee0ffce0fa16cb0eb821c4eac0683b8e9436691b0ea5a8d6b28
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: false
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Governing artifacts: `CONSTITUTION.md`; `specs/governed-lifecycle-cli.md`; `specs/governed-lifecycle-cli.test.md`; `docs/architecture/system/architecture.md`; `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`
Formal criteria: code-review-v1; boundary-first-v1; requirement-fidelity-gate-v1
Affected behavior: milestone completion settlement, workflow-selected successor start, routing projection synchronization, current-revision evidence replay, and legacy registration upgrade
Highest-impact failure modes: completion silently routes; authoritative projections disagree; stale evidence is accepted as idempotent; legacy replay mutates routing; rejection partially persists
Changed boundaries: BND-STATE-002; BND-AUTH-002; BND-TEMPORAL-001; INT-005
Evidence expected: approved R16/R22/R31 and T09; no-routing completion diff; synchronized start diff; exact, omitted, and independently drifted replay outcomes; unchanged rejection bytes; deterministic legacy upgrade
Areas requiring direct inspection: `lifecycle-operations.js`; milestone tests; approved spec, test spec, architecture, and ADR; prior CR1/CR2 evidence; implementation result
Areas intentionally out of scope: unrelated observability implementation; final branch verification; PR readiness
Risk classes considered: authority boundary; state projection; retry and stale evidence; packet identity; compatibility; atomic rejection; privacy; scope expansion
Falsifiable review questions: Does completion leave every routing projection unchanged? Does start synchronize every present active projection or reject contradiction? Can omission or isolated receipt, canonical-log, proof, or non-proof packet drift return `already-recorded`? Can legacy replay repair routing implicitly?
Review target identity: sha256:192af5cf09d0cee0ffce0fa16cb0eb821c4eac0683b8e9436691b0ea5a8d6b28
Governing artifacts inspected: approved governed CLI spec r5, test spec r5, canonical architecture r5, ADR-20260824, prior deadlock review and resolution, implementation and focused tests
Adversarial hypotheses tested: completion still routes; active automation can disagree; review path can be omitted; unrelated log append invalidates the occurrence; receipt, occurrence, proof, or packet-only drift is accepted; old closed milestone replay mutates routing
Direct proofs performed: C05 13/13; lifecycle operation suite 71/71; package suite 253/253; byte-unchanged rejection assertions; legacy upgrade and exact replay assertions
Validation evidence challenged: focused proof was expanded to lifecycle siblings and the full package; cross-milestone validation was deliberately rerun after resolution rather than treating its transient pre-resolution mismatch as implementation success
Unreviewed surfaces: unrelated observability implementation and its milestone evidence; hosted CI; final branch ancestry and release packaging
Confidence: high for the reviewed correction; final verify remains separately owned
No-finding rationale: Every outcome-changing authority, state, replay, drift, and compatibility branch named by CR1/CR2 and INT-005 has matching implementation logic and direct proof, with no contradictory behavior found in adjacent lifecycle or package tests.

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-deadlock-r3.md`; `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Open blockers: an independent L1 clean review is required before this elevated correction may advance
- Next stage: independent code-review
- Review status: inconclusive
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-deadlock-r3.md`
- Review log: `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Review resolution: `docs/changes/2026-08-24-governed-lifecycle-cli/review-resolution.md`
- Reviewed milestone: none; isolated post-close correction
- Milestone closeout: not-applicable
- Remaining implementation milestones: none in the owning governed-lifecycle CLI change
- Required review-resolution: yes, after independent clean agreement
- Finding IDs: none
- Verify readiness: not-claimed

## Actual-diff assessment

The revised spec and architecture resolve the former ownership contradiction: workflow selects continuation, `complete-milestone` reports eligibility without routing, and a separate workflow-authorized `start-milestone` applies the deterministic route atomically. The implementation follows that boundary. Completion changes milestone settlement and cursor state only; start changes the selected milestone and synchronizes both workflow-state routing fields plus an active automation projection. A contradictory active projection rejects before persistence.

Direct review consumption now creates a canonical versioned completion record whose fingerprint includes the milestone proof, receipt, exact review-log occurrence, complete packet inventory, normalized review facts, milestone identity, and authority. The replay path reconstructs those facts from current repository bytes. Omitted evidence and each independently drifted constituent fail with `RL_STALE_EVIDENCE`; an unrelated log append and an identity-equal request remain idempotent. The legacy path upgrades only matching evidence registration and cannot perform the removed implicit routing repair.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R16, R22, R31, AC11, AC12, E6, E7, and INT-005 agree on separate completion/start authority and evidence-complete replay. |
| Test coverage | pass | T09 directly covers no-routing completion, successor start, absent/active/contradictory automation, omission, receipt/log/proof/non-proof drift, unrelated append, exact replay, and legacy upgrade. |
| Edge cases | pass | Wrong milestone, non-clean review, open findings, stale packet, missing prose facts, canonical table contradictions, final implementation transition, and older replay all fail or remain bounded as required. |
| Error handling | pass | Evidence drift normalizes to `RL_STALE_EVIDENCE`; routing contradictions reject with `RL_OPERATION_NOT_PERMITTED`; rejected candidates retain byte-identical lifecycle state. |
| Architecture boundaries | pass | Completion does not select or apply continuation; start applies only the workflow-requested current milestone and synchronizes present authoritative projections. |
| Compatibility | pass | Existing fingerprinted registrations replay exactly; matching legacy registrations upgrade once without routing; conflicting legacy facts fail unchanged. |
| Security/privacy | pass | No new secret-bearing output, network boundary, arbitrary setter, or machine-local path projection is introduced. |
| Derived artifact currency | pass | The corrected spec, test spec, and canonical architecture have current clean review receipts at their recorded identities. |
| Unrelated changes | pass | Review was limited to the two recorded deadlock findings and the prior narrow correction-route prerequisite. |
| Validation evidence | pass | Focused C05 passed 13/13, lifecycle operations passed 71/71, package tests passed 253/253, and diff checking passed. The temporary pre-resolution C09 mismatch is explicitly recorded and must be rerun after finding closeout. |

## Direct-proof gaps and residual risk

No material gap remains for the reviewed findings. Workflow authorization is a structural repository claim rather than authenticated actor identity, as already documented by the threat model. A malicious maintainer with unrestricted repository authority remains outside the CLI integrity boundary. Final branch verification and broader observability closeout remain separate gates.

## Handoff

This L0 assessment is inconclusive for gate advancement because the elevated correction requires independent review. A fresh L1 review must inspect the exact packet before `RLCLI-DEADLOCK-CR1` and `RLCLI-DEADLOCK-CR2` are closed. It does not claim final verification or PR readiness.
