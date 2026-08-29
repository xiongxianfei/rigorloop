# Code Review CLI Fix R1: Milestone Handoff and Direct Review Settlement

Review ID: code-review-cli-fix-r1
Stage: code-review
Round: r1
Reviewer: Codex independent review context `/root/cli_fix_review`
Review date: 2026-08-29
Target: commit `f354dd1aa20394f7ee197d0ce3dd905dc292cb3f`, CLI-fix paths only
Reviewed milestone: none
Reviewed artifact: CLI fix commit `f354dd1aa20394f7ee197d0ce3dd905dc292cb3f`
Recording status: recorded
Status: blocked
Review status: blocked
Material findings: CRG-CLI-CR1, CRG-CLI-CR2

## Result

- Skill: code-review
- Status: blocked
- Artifacts changed: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-cli-fix-r1.md`, `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`, and `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Open blockers: CRG-CLI-CR1 and CRG-CLI-CR2
- Next stage: review-resolution
- Review status: blocked
- Material findings: CRG-CLI-CR1, CRG-CLI-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-cli-fix-r1.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Reviewed milestone: none
- Milestone closeout: not-applicable
- Remaining implementation milestones: M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: CRG-CLI-CR1, CRG-CLI-CR2
- Verify readiness: not-claimed

## Review inputs

- Commit range: `d8b3d84a8d55b4ac20699f36d856cefe3e067b7b..f354dd1aa20394f7ee197d0ce3dd905dc292cb3f`
- Reviewed implementation: `packages/rigorloop/dist/lib/lifecycle-operations.js`
- Reviewed tests: `packages/rigorloop/test/lifecycle-milestone.test.js`, `packages/rigorloop/test/lifecycle-read.test.js`, and `packages/rigorloop/test/lifecycle-contract.test.js`
- Governing authority: `specs/rigorloop-workflow.md` R7x through R7xa and `specs/governed-lifecycle-cli.md` E6, E7, R3, R16, R22, Inputs and outputs, and State and invariants
- Review mode: direct independent review requested as a stop gate before M2; automation-only review fields were not applied

## Actual-diff summary

The fix adds a first phase to `complete-milestone`: an `implementing` milestone with passing evidence moves to `review-requested`, and workflow routing moves from `implement` to `code-review`. It also classifies a milestone review as automated only when any automation gate or packet field is present; a direct clean review can therefore settle a milestone without a packet inventory. Automated receipts retain their packet validation and replay behavior.

The commit also records M1 closure and starts M2. Those lifecycle-record changes are outside this CLI-fix judgment and were not treated as evidence that the new CLI behavior is correct.

## Findings

### Finding CRG-CLI-CR1

Finding ID: CRG-CLI-CR1

Severity: major

Location: `packages/rigorloop/dist/lib/lifecycle-operations.js:331-361`; `packages/rigorloop/test/lifecycle-milestone.test.js:160-169`

Evidence: The new `automated` branch skips all implementation-packet identity checks when `Review gate outcome`, `Initial packet inventory`, and `Initial packet hash` are absent. The new direct-review test proves settlement with a receipt that contains no target commit, reviewed revision, implementation path, or packet identity. The CLI verifies only milestone ID, outcome, recording status, log consistency, and the separate milestone-proof file. An otherwise canonical receipt from an earlier or unrelated implementation revision can therefore close the current milestone. This contradicts `specs/governed-lifecycle-cli.md` R16 and E7, which require the completion fingerprint and replay to bind the exact current reviewed packet.

Required outcome: Direct milestone reviews must be bound to the exact implementation revision they reviewed, and replay must revalidate that identity. The direct path need not inherit automation-only gate metadata or per-document hashes, but it cannot accept an identity-free receipt.

Safe resolution path: Add one concise direct-review identity, preferably the reviewed commit ID plus a clean-current-HEAD check or another approved aggregate implementation identity, include it in the normalized completion fingerprint, add stale and unrelated-target regression tests, and revise the governing CLI spec if this intentionally replaces the existing packet-inventory rule. Preserve the current full packet validation for formally automated reviews.

needs-decision rationale: The governing CLI specification currently requires complete packet identity. The specification owner must approve a simpler exact commit or aggregate identity before implementation substitutes it.

### Finding CRG-CLI-CR2

Finding ID: CRG-CLI-CR2

Severity: major

Location: `packages/rigorloop/dist/lib/lifecycle-operations.js:790-805`; `specs/governed-lifecycle-cli.md:56-64,90,125`

Evidence: `complete-milestone` now succeeds from `implementing`, returns `review-requested`, and changes `workflow_state.current_stage` plus the active automation projection to `code-review`. The approved CLI contract defines `complete-milestone` as the post-review close operation, states that it closes only a reviewed milestone, and says completion does not perform routing. R3 also enumerates the first-release commands without a separate implementation-handoff operation. The workflow spec requires the `review-requested` transition, but the CLI spec does not authorize this overloaded public operation or its routing mutation. The passing tests exercise the new behavior while leaving the governing feature spec unchanged.

Required outcome: The public CLI contract and implementation must agree on one fail-closed operation for implementation-to-review handoff, including its name, allowed source state, proof requirements, routing mutation, replay semantics, and separation from reviewed milestone closure.

Safe resolution path: Revise `specs/governed-lifecycle-cli.md` to authorize a clearly defined two-phase `complete-milestone` operation and add current-revision replay plus contradictory-state tests, or introduce a dedicated closed-vocabulary handoff operation and keep `complete-milestone` post-review-only. Then rerun the lifecycle contract, read, milestone, and transaction suites.

needs-decision rationale: Choosing an overloaded two-phase operation versus a distinct handoff operation changes the approved public CLI contract and belongs to the CLI specification owner.

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CRG-CLI-CR1 contradicts exact reviewed-packet identity in R16/E7; CRG-CLI-CR2 changes the documented semantics and routing authority of `complete-milestone`. |
| Test coverage | concern | The happy paths pass, but no test rejects a direct receipt that reviewed a different commit or proves current-revision idempotency of the new handoff phase. |
| Edge cases | block | A stale or unrelated direct review can authorize current milestone closure. |
| Error handling | concern | Contradictory routing is rejected, but the new handoff behavior has no explicit contract or replay test. |
| Architecture boundaries | concern | Workflow-owned routing is mechanically applied, but the approved CLI boundary has not authorized that mutation through `complete-milestone`. |
| Compatibility | block | Existing approved command semantics are changed without the corresponding governing-spec revision. |
| Security/privacy | pass | No secret, credential, personal-data, network, or permission surface changes. |
| Derived artifact currency | pass | No generated or packaged surface is part of this bounded CLI fix. |
| Unrelated changes | concern | The commit also mutates change-local M1/M2 state and records review evidence; those paths are excluded from this judgment. |
| Validation evidence | pass with limitation | All 53 targeted lifecycle tests pass, but the new success test directly demonstrates the missing direct-review implementation identity. |

## Direct proof

```text
node --test packages/rigorloop/test/lifecycle-milestone.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-contract.test.js
=> 53 passed, 0 failed
```

`complete milestone accepts a canonical direct clean review without automation gate fields` passes with a review fixture that declares no target commit, artifact revision, implementation path, or packet identity. That is direct proof of CRG-CLI-CR1, not evidence that the settlement is safe.

## Handoff

This direct review is isolated and is a stop gate for M2. There is no automatic downstream handoff. CRG-CLI-CR1 and CRG-CLI-CR2 require disposition and correction, followed by an independent rereview of the changed CLI paths. `change.yaml` was not changed by this review.
