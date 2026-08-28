# Code Review: Milestone Completion and Replay Correction R4

Review ID: code-review-deadlock-r4
Stage: code-review
Round: r4
Reviewer: Codex independent L1 subagent reviewer with supervising direct-probe confirmation
Reviewer context ID: root-deadlock-boundary-review-l1-r4
Author context ID: root-deadlock-correction-r3-implementation
Independence level: L1
Context separation mechanism: fork-none independent reviewer context with a neutral six-file manifest; supervising review independently reproduced every recorded finding in temporary repositories
Author context excluded: false
Target: correction of `RLCLI-DEADLOCK-CR1` and `RLCLI-DEADLOCK-CR2`
Reviewed milestone: none
Reviewed artifact: isolated post-close governed lifecycle CLI correction
Review date: 2026-08-27
Status: changes-requested
Review status: changes-requested
Review gate outcome: stop
Recording status: recorded
Material findings: RLCLI-DEADLOCK-CR3
Open findings: none
Automated review: yes
Native review status: changes-requested
Risk tier: elevated
Risk-tier triggers: workflow routing authority; milestone legal transitions; remaining-work projection; current-revision replay; durable review identity; legacy-state compatibility
Risk-tier classifier: affected-path-and-contract-surface-v1
Initial packet inventory: packages/rigorloop/dist/lib/lifecycle-operations.js@working-tree#sha256:e8cc606851121e7025c7f43d412ab52d99bcf2d370e4656f83a8b7bdcc4ec37a; packages/rigorloop/test/lifecycle-milestone.test.js@working-tree#sha256:cbd9ab0e6d5b5287aef2d3608e20a365de832b56180b2e92fb8ca89fd54b5232; specs/governed-lifecycle-cli.md@working-tree#sha256:06e8856209816c1692cc3baab4a41b3936b8118f6be4c668de7a80665f0c1b82; specs/governed-lifecycle-cli.test.md@working-tree#sha256:84e93b72a2416d8ede18c83916b6a9e93f90798602e02ecd482f8c4e9bcae0ba; docs/architecture/system/architecture.md@working-tree#sha256:78e708c76b5f787e4f54e55d16d7abc827dd16f90ea578b4dec11f06cf93ff67; docs/changes/2026-08-24-governed-lifecycle-cli/evidence/deadlock-completion-replay-correction-r1.md@working-tree#sha256:e925557f0d8367b00daa46f72024230ca9c407344fb835124b9632680b87904f
Initial packet hash: sha256:192af5cf09d0cee0ffce0fa16cb0eb821c4eac0683b8e9436691b0ea5a8d6b28
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Governing artifacts: `CONSTITUTION.md`; `specs/governed-lifecycle-cli.md`; `specs/governed-lifecycle-cli.test.md`; `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`; `docs/architecture/system/architecture.md`; `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`
Formal criteria: code-review-v1; boundary-first-v1; requirement-fidelity-gate-v1
Requirement fidelity applicability: applicable
Affected behavior: milestone completion settlement, workflow-selected successor start, remaining-work projection validation, supplied and pre-projected review replay, canonical review-log occurrence binding, active automation synchronization, and legacy registration upgrade
Highest-impact failure modes: stale review evidence is accepted as idempotent; one review ID binds multiple canonical occurrences; an illegal milestone transition commits; contradictory remaining-work state is advanced; workflow and automation projections diverge
Changed boundaries: BND-STATE-002; BND-AUTH-001; BND-AUTH-002; BND-TEMPORAL-001; INT-005; SLA-R037h; SLA-R037j
Evidence expected: approved R16/R17/R22/R31 and T09; no-routing completion diff; synchronized start diff; exact and drifted replay outcomes for every review mode; unique canonical-log binding; legal transition and remaining-projection rejection; unchanged rejection bytes
Areas requiring direct inspection: `lifecycle-operations.js`; milestone tests; approved spec, test spec, architecture, ADR, and the stage-owned milestone-transition contract
Areas intentionally out of scope: unrelated observability implementation; final branch verification; PR readiness; hosted CI
Risk classes considered: authority boundary; state projection; legal transition; retry and stale evidence; canonical occurrence identity; compatibility; atomic rejection; privacy; scope expansion
Falsifiable review questions: Does completion leave routing unchanged? Does start reject every inconsistent milestone or routing projection? Can supplied or pre-projected review drift return `already-recorded`? Can duplicate canonical rows bind one review ID ambiguously? Can completion skip `review-requested`? Can legacy upgrade change routing?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-deadlock-r4.md`; `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`; `docs/changes/2026-08-24-governed-lifecycle-cli/review-resolution.md`
- Open blockers: `RLCLI-DEADLOCK-CR2`; `RLCLI-DEADLOCK-CR3`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `RLCLI-DEADLOCK-CR3`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-deadlock-r4.md`
- Review log: `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Review resolution: `docs/changes/2026-08-24-governed-lifecycle-cli/review-resolution.md`
- Reviewed milestone: none; isolated post-close correction
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none in the owning governed-lifecycle CLI change
- Required review-resolution: yes
- Finding IDs: `RLCLI-DEADLOCK-CR3`
- Verify readiness: not-claimed

## Prior finding RLCLI-DEADLOCK-CR2 reconciliation

- Severity: major
- Location: `packages/rigorloop/dist/lib/lifecycle-operations.js:240-251,342-355,650-660,679-686`; `packages/rigorloop/test/lifecycle-milestone.test.js:118-127,187-203,219-258`
- Evidence: The supplied-review path now persists and revalidates receipt, canonical occurrence, and packet identities, but the sibling pre-projected path still reduces authority to `review_round`, `review_stage`, and `review_status`. A temporary-repository probe completed from a valid pre-projected review, changed only the referenced review bytes, refreshed the lifecycle revision, and received exit `0` with `already-recorded`. Separately, `requireLogEntry` selects the first matching table row without proving uniqueness; a probe with two identical canonical rows for one review ID completed and mutated the milestone successfully. Focused T09 exercises drift only for the supplied-review path and exercises contradictory field values, not duplicate occurrences.
- Required outcome: Both supplied and pre-projected completion modes must persist and reconstruct all evidence that authorized review settlement, and one review ID must resolve to exactly one canonical log occurrence. Any referenced review drift, missing identity, or duplicate occurrence must fail before mutation; exact replay and an unrelated non-occurrence log append must remain idempotent.
- Safe resolution path: Extend the normalized completion record or replace the projected shortcut with exact registered-review reconstruction; make `requireLogEntry` reject zero or multiple canonical occurrences; add public-CLI regressions for projected-review drift and duplicate identical prose/table occurrences, then rerun C05 and rereview the frozen replacement packet.
- needs-decision rationale: none; this is an in-scope implementation and proof correction under approved R16, R17, R22, T09, BND-AUTH-001, and BND-TEMPORAL-001.

## Finding RLCLI-DEADLOCK-CR3

Finding ID: RLCLI-DEADLOCK-CR3
- Severity: major
- Location: `packages/rigorloop/dist/lib/lifecycle-operations.js:613-637,640-693`; `packages/rigorloop/test/lifecycle-milestone.test.js:109-168`; `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md:524-540`
- Evidence: `start-milestone` validates the selected milestone and predecessors but never verifies that `remaining_implementation_milestones` equals all non-closed implementation milestones. A temporary-repository probe with `current_milestone: M2`, both M2/M3 planned, and `remaining_implementation_milestones: [M3]` had no pre-status errors; start exited `0`, mutated M2 to implementing, and retained the contradictory projection. `complete-milestone` also explicitly permits source state `implementing`; a second probe supplied an exact clean review and observed exit `0` with a direct `implementing -> closed` mutation, although SLA-R037h makes `implementing -> review-requested -> closed` the only legal sequence. Focused tests do not cover either invalid pre-state.
- Required outcome: Start and completion must fail closed on inconsistent current/remaining milestone projections and must enforce the exact legal source transition. Rejected operations must leave lifecycle bytes unchanged.
- Safe resolution path: Add one shared milestone-prestate validator for current milestone, ordered remaining implementation IDs, and allowed source state; require `review-requested` before closure or revise the higher-priority milestone contract through its owner if atomic closure from `implementing` is intended; add public-CLI negative regressions and rerun C05 before rereview.
- needs-decision rationale: none for enforcing the current contract; if direct `implementing -> closed` is intended, the stage-owned lifecycle spec owner must first approve that normative change.

## Prior-finding reconciliation

| Finding ID | Classification | Evidence |
| --- | --- | --- |
| `RLCLI-DEADLOCK-CR1` | resolved | Completion leaves routing unchanged; a separate workflow-selected start synchronizes `workflow_state` and active automation, and contradictory active automation rejects unchanged. |
| `RLCLI-DEADLOCK-CR2` | failed-remediation | The supplied-review path is repaired, but pre-projected evidence drift and ambiguous duplicate canonical occurrences still authorize success. |
| `RLCLI-DEADLOCK-CR3` | new-finding | Independent adversarial probes found unenforced milestone source-state and remaining-projection invariants. |

## Requirement-fidelity matrix

| Property | Required surfaces | Result | Evidence |
| --- | --- | --- | --- |
| Completion does not select continuation | spec, architecture, implementation, T09 | pass | R16/R31, architecture two-step protocol, lines 687-693, and focused completion assertions agree. |
| Workflow-selected start synchronizes present routing projections | architecture, implementation, T09 | pass | Lines 618-637 and active/contradictory automation tests agree. |
| Every authorizing replay constituent is current | implementation, T09 | block | Supplied mode passes; pre-projected mode omits its review evidence identity and accepts drift. |
| Canonical review occurrence is exact | implementation, T09 | block | Field contradictions reject, but duplicate matching occurrences are not rejected or tested. |
| Milestone state and remaining projection are legal | stage-owned contract, implementation, T09 | block | Start accepts inconsistent remaining work; completion accepts the absent `implementing -> closed` transition. |
| Legacy completion cannot route | implementation, T09 | pass | Matching legacy evidence upgrades only registration and older mismatches reject. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | R16/R31 routing separation is aligned; legal transition and remaining-projection enforcement are incomplete. |
| Test coverage | concern | C05 is green but omits pre-projected drift, duplicate occurrences, inconsistent remaining work, and direct implementing closure. |
| Edge cases | concern | Supplied-review drift and active automation are covered; sibling projected and ambiguous-log paths are not. |
| Error handling | concern | Covered rejection paths preserve bytes, but the four probed invalid states succeed. |
| Architecture boundaries | pass | Workflow selects continuation and completion does not route. |
| Compatibility | concern | Legacy upgrade is bounded, but pre-projected compatibility is status-bound rather than evidence-bound. |
| Security/privacy | pass | No new secret, network, external-action, or absolute-path exposure was found. |
| Derived artifact currency | pass | The six-file packet and registered spec, test-spec, and architecture identities match current bytes. |
| Unrelated changes | pass | Review and findings are confined to the frozen deadlock packet. |
| Validation evidence | concern | C05 and the lifecycle suite pass, but direct adversarial probes falsify untested contract properties. |

## Validation

- Packet inventory: all six identities matched; aggregate `sha256:192af5cf09d0cee0ffce0fa16cb0eb821c4eac0683b8e9436691b0ea5a8d6b28` matched the recorded serialization.
- `node --test packages/rigorloop/test/lifecycle-milestone.test.js packages/rigorloop/test/lifecycle-migration-repair.test.js`: passed, 13/13.
- `node --test packages/rigorloop/test/lifecycle-*.test.js`: passed, 71/71.
- `git diff --check -- <six frozen packet paths>`: passed.
- Direct projected-review drift probe: failed contract; replay returned exit `0`, `already-recorded` after review-byte drift.
- Direct duplicate-log-occurrence probe: failed contract; completion returned exit `0` and closed the milestone with two identical canonical rows.
- Direct inconsistent-remaining-work probe: failed contract; start returned exit `0` and mutated the milestone.
- Direct illegal-source-state probe: failed contract; completion returned exit `0` and changed `implementing` directly to `closed`.

## Direct-proof gaps and residual risk

The focused suite proves the repaired direct-receipt and routing paths but not their sibling pre-projected and invalid-prestate paths. Until CR2 and CR3 are resolved and rereviewed, lifecycle replay can overclaim idempotence and workflow can persist a state transition forbidden by the governing lifecycle model.

## Handoff

This workflow-managed L1 review stops with `changes-requested`. `RLCLI-DEADLOCK-CR1` is resolved. `RLCLI-DEADLOCK-CR2` remains open as failed remediation, and `RLCLI-DEADLOCK-CR3` is new. Review-resolution and a fresh independent rereview are required before final verification; this record does not claim branch or PR readiness.
