# Code Review: Milestone Deadlock Correction R1

Review ID: code-review-deadlock-r1
Stage: code-review
Round: r1
Reviewer: Codex isolated independent code-review context
Target: uncommitted governed-lifecycle milestone completion correction
Reviewed milestone: none
Reviewed artifact: `packages/rigorloop/dist/lib/lifecycle-contract.js`; `packages/rigorloop/dist/lib/lifecycle-operations.js`; `packages/rigorloop/dist/lib/lifecycle-read.js`; `packages/rigorloop/test/lifecycle-milestone.test.js`; `specs/governed-lifecycle-cli.md`; `specs/governed-lifecycle-cli.test.md`
Review date: 2026-08-26
Status: blocked
Review status: blocked
Material findings: RLCLI-DEADLOCK-CR1, RLCLI-DEADLOCK-CR2
Open findings: RLCLI-DEADLOCK-CR1, RLCLI-DEADLOCK-CR2
Recording status: recorded
Automated review: yes
Native review status: blocked
Review gate outcome: blocked
Independence level: L1
Author context ID: root-deadlock-correction
Reviewer context ID: deadlock-boundary-review
Context separation mechanism: separate context-isolated reviewer with no inherited conversation
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: public request schema; workflow routing authority; lifecycle replay; cross-change state projection
Risk-tier classifier: elevated because the correction changes public lifecycle input and authority, replay semantics, and cross-change routing projections
Initial packet inventory: packages/rigorloop/dist/lib/lifecycle-contract.js@working-tree#sha256:486c2c8c7f0a8b3cf56624d6a2673a4a3100593ced6b5f627e8442c38fe96abf; packages/rigorloop/dist/lib/lifecycle-operations.js@working-tree#sha256:14c22893daa1007313dab337afc53a47e481d75b5287656cb0f8c1a7ee4f22e3; packages/rigorloop/dist/lib/lifecycle-read.js@working-tree#sha256:7b906c9abfaaa94768db15825dd9e61f294a082f2be0b6f5f9ae9061c4d0f9be; packages/rigorloop/test/lifecycle-milestone.test.js@working-tree#sha256:caa7cedddac1bbac8cfb76a05f3bc6200adb6af7307005a90550a82a3d8ce6bc; specs/governed-lifecycle-cli.md@working-tree#sha256:050e01cd5d487e555b242748fec243dea7e09f030609e41c328ebc73ffa3d168; specs/governed-lifecycle-cli.test.md@working-tree#sha256:ad7e936dcca33e008e5dd8bc1daee22c9e3cd91ef0431f815e2f1b236f85a1fb
Initial packet hash: sha256:5b35544195e93264308ff896ea975e4a4b00d0b7a8829e8620b27b760f0068c4
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Risk classes considered: authority-boundary contradiction; stale evidence replay; cross-projection inconsistency; governing-artifact drift
Falsifiable review questions: Does milestone completion keep every authoritative routing projection coherent under one approved owner? Does an exact replay reject when only the canonical review log or a non-proof packet constituent changes?
Governing artifacts: `CONSTITUTION.md`; `specs/governed-lifecycle-cli.md`; `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`; `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`; `specs/governed-lifecycle-cli.test.md`
Formal criteria: code-review-v1; boundary-first-v1; requirement-fidelity-gate-v1
Affected behavior: review-evidence consumption, milestone completion, idempotent replay, current-milestone advancement, and next-stage projection
Highest-impact failure modes: CLI crosses workflow authority; lifecycle projections disagree; unreviewed request schema becomes public; automation cannot resume
Changed boundaries: BND-STATE-002; BND-AUTH-002; BND-TEMPORAL-001
Evidence expected: T09 and T10 plus current spec, test-spec, workflow projection, and review-log identities
Areas requiring direct inspection: lifecycle contract and operations modules; milestone tests; governed CLI spec and test spec; owning change record; live observability change projections
Areas intentionally out of scope: M3 observability implementation review; final verification; PR readiness

## Result

- Skill: code-review
- Status: blocked
- Artifacts changed: this review, `review-log.md`, and `review-resolution.md`
- Open blockers: RLCLI-DEADLOCK-CR1, RLCLI-DEADLOCK-CR2
- Next stage: blocked
- Review status: blocked
- Material findings: RLCLI-DEADLOCK-CR1, RLCLI-DEADLOCK-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-deadlock-r1.md`
- Review log: `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Review resolution: `docs/changes/2026-08-24-governed-lifecycle-cli/review-resolution.md`
- Reviewed milestone: none; isolated post-close correction
- Milestone closeout: blocked
- Remaining implementation milestones: none in the owning change; the correction requires an authorized reopened scope
- Required review-resolution: yes
- Finding IDs: RLCLI-DEADLOCK-CR1, RLCLI-DEADLOCK-CR2
- Verify readiness: not-claimed

## Finding RLCLI-DEADLOCK-CR1

Finding ID: RLCLI-DEADLOCK-CR1
Severity: blocker
Location: `specs/governed-lifecycle-cli.md:76`; `specs/governed-lifecycle-cli.md:91`; `packages/rigorloop/dist/lib/lifecycle-operations.js:577-580,607-610`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml:130-179`
Evidence: Revised R16 requires `complete-milestone` to project the next implementation stage, while unchanged R31 says the first-release CLI MUST NOT perform workflow routing. The implementation writes `workflow_state.current_stage` and `next_stage`, but the live transaction left `workflow.automation.current_stage` at `code-review` while `workflow_state.current_stage` became `implement`; the subsequent `implement` invocation could not establish matching armed authority. The owning governed-CLI change also records approved spec and test-spec identities `e80a5266...` and `b007a655...`, while current bytes are `050e01cd...` and `ad7e936d...`.
Required outcome: The spec owner must choose and approve one authority model: either keep routing workflow-owned and make milestone completion return enough deterministic facts for workflow to perform the continuation, or define a narrow CLI routing operation/exception that atomically updates every authoritative routing projection. The matching test spec must directly prove the selected model, the revised artifacts must receive current reviews, and the implementation must then be rereviewed.
Safe resolution path: Route the contradictory R16/R31 revision to `spec`, then `spec-review`; align T09 and route it through `test-spec-review`; update implementation only after that decision. Preserve the already-proved review-log binding and replay invariants while removing or completing the unauthorized partial routing behavior.
needs-decision rationale: The choice changes the public CLI/workflow authority boundary and cannot be made by code review or implementation. Owner: governed-lifecycle CLI spec owner and workflow contract owner.

## Finding RLCLI-DEADLOCK-CR2

Finding ID: RLCLI-DEADLOCK-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-operations.js:563-583`; `packages/rigorloop/test/lifecycle-milestone.test.js`
Evidence: Initial milestone completion validates the supplied review receipt against the canonical review-log entry and validates every declared packet constituent. After closure, however, the replay path compares only the milestone evidence path/hash, review receipt path/hash, and round before returning `already-recorded` or applying legacy reconciliation. It neither reruns the canonical review-log binding nor revalidates non-proof packet identities. Changing only the review log or a packet constituent other than `evidence_path` can therefore leave the request accepted as an exact replay even though the evidence set that authorized completion is no longer identical. The stale-packet regression mutates a source that is also the milestone evidence path, so it does not exercise either gap.
Required outcome: A closed completion replay must fail closed when the canonical review-log facts or any identity-bearing completion packet constituent differs from the evidence accepted at initial completion.
Safe resolution path: After the CR1 authority decision, either rerun the full completion-evidence validation before returning `already-recorded`, or persist and revalidate the canonical review-log identity and complete packet inventory. Add separate regressions for review-log-only drift and drift of a packet constituent that is not the milestone proof file.
needs-decision rationale: none; this is an accepted implementation defect, but correction must wait until CR1 establishes the authoritative transition contract.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | R16 and R31 prescribe contradictory ownership for the new stage projection. |
| Test coverage | block | Milestone tests do not prove agreement with `workflow.automation`, review-log-only replay drift, or non-proof packet-only replay drift. |
| Edge cases | pass | Table/prose review logs, stale packets, conflicts, older replay, immediate predecessor, and lifecycle-closeout routing are directly covered. |
| Error handling | pass | Invalid evidence and conflicting durable facts reject without mutation in focused proof. |
| Architecture boundaries | block | The CLI performs workflow routing despite the current no-routing boundary. |
| Compatibility | block | `review_evidence_path` and legacy reconciliation are new public behavior under stale governing identities. |
| Security/privacy | pass | Paths remain repository-relative, symlink-refusing, and tied to exact hashes. |
| Derived artifact currency | block | Governed spec and test-spec registrations do not match current bytes. |
| Unrelated changes | concern | The correction was added to the observability branch after the governed-CLI initiative had reached final closeout. |
| Validation evidence | pass with limitation | Focused 9/9 and package 251/251 passed; repository-wide lifecycle validation correctly reports the governed-CLI spec/test-spec stale. |

## Direct-proof gaps

No direct test proves that every authoritative workflow projection remains coherent after milestone completion. Replay tests also do not isolate canonical review-log drift or non-proof packet drift. A clean result cannot rely on the revised R16/T09 until their owning review gates establish current authority.

## Handoff

This direct review is isolated. There is no automatic downstream handoff. Resolve `RLCLI-DEADLOCK-CR1`, then correct `RLCLI-DEADLOCK-CR2` and rereview the exact revised packet. An owner decision is required for CR1.
