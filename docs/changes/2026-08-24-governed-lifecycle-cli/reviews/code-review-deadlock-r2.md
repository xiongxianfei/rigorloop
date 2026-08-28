# Code Review: Stale Correction Route Deadlock R2

Review ID: code-review-deadlock-r2
Stage: code-review
Round: r2
Reviewer: Codex same-context fresh-assumption direct reviewer
Target: stale pre-authored upstream correction routing bugfix
Reviewed milestone: none
Reviewed artifact: `packages/rigorloop/dist/lib/lifecycle-read.js@working-tree#sha256:eb5176cccd6551c7e997bd47aafac41f8543ecf9a1e241a1100c13cfda1347f4`; `packages/rigorloop/dist/lib/lifecycle-operations.js@working-tree#sha256:5ecf078d702ac7818fb52807e02be2e8ce1f661cdd135379b4a7ee4dc56e91f7`; `packages/rigorloop/test/lifecycle-correction-route.test.js@working-tree#sha256:1b114499e6bd3111eb0ba36378ba6a67e520beaa355efc00a0f5f0d889183533`
Review date: 2026-08-27
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none
Open findings: none
Recording status: recorded
Automated review: no
Native review status: clean-with-notes
Risk tier: elevated
Risk-tier triggers: lifecycle mutation permission; stale artifact identity; workflow routing authority
Governing artifacts: `CONSTITUTION.md`; `specs/governed-lifecycle-cli.md`; `docs/workflows.md`; `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`
Formal criteria: code-review-v1; boundary-first-v1; direct-correction-review-v1
Affected boundaries: BND-STATE-001; BND-AUTH-001; BND-AUTH-002; BND-COMPOSE-002; BND-TEMPORAL-001; INT-001
Areas intentionally out of scope: resolution of RLCLI-DEADLOCK-CR1 and RLCLI-DEADLOCK-CR2; broader observability implementation; lifecycle routing mutation; final verification; PR readiness

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-deadlock-r2.md`; `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Open blockers: RLCLI-DEADLOCK-CR1 and RLCLI-DEADLOCK-CR2 remain open outside this bugfix slice
- Next stage: blocked pending workflow-owned correction routing and resolution of the existing findings
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-deadlock-r2.md`
- Review log: `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Review resolution: not-required for this no-finding review; the existing resolution remains open for CR1 and CR2
- Reviewed milestone: none; isolated lifecycle correction
- Milestone closeout: not-applicable
- Remaining implementation milestones: none in the owning governed-lifecycle CLI change
- Required review-resolution: no for this review; yes remains required for CR1 and CR2
- Finding IDs: none
- Verify readiness: not-claimed

## Actual-diff assessment

The correction changes permission interpretation only when all stale identities belong to settled upstream authoring artifacts, an unresolved material finding exists, and the workflow owns an eligible backward route. Context now reports `RL_WORKFLOW_ROUTE_REQUIRED` and withholds direct `record-artifact-revision` until workflow routing occurs. The route operation accepts stale destination bytes only when at least one supplied finding is actually open, snapshots the registered prior artifact identity, and leaves semantic registration to the destination authoring stage.

The direct mutation bypass was challenged with an empty finding set. It rejects with `RL_CORRECTION_ROUTE_INVALID` and preserves `change.yaml` bytes. Unknown findings, wrong destinations, stale lifecycle revisions, lateral routes, and conflicting active routes retain their prior fail-closed behavior.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R10, R11a, R17, R18, R19, and R28 preserve context, guarded registration, stale-evidence correction, concurrency, narrow mutation, and CLI use. |
| Test coverage | pass | The focused regression covers discovery, context routing, empty-finding rejection, exact prior identity, and successful registration; adjacent route/read tests cover negative paths. |
| Edge cases | pass | Current versus stale destination, empty and unknown findings, stale request revision, conflicting route, and non-destination revision are exercised. |
| Error handling | pass | Invalid routes reject before lifecycle mutation with stable correction-route errors. |
| Architecture boundaries | pass | Workflow selects and records the route; the authoring stage registers its artifact; the CLI validates both operations. |
| Compatibility | pass | Current-identity correction routing remains unchanged, while stale identity without an open finding remains unadvertised and rejected. |
| Security/privacy | pass | No new diagnostic payload or path exposure is introduced; exact path and hash validation remain in place. |
| Derived artifact currency | concern | The owning spec and test-spec registrations remain stale by design and require the now-available correction workflow; this review does not settle them. |
| Unrelated changes | pass | The reviewed slice is limited to correction permission, route identity binding, and its regression proof. |
| Validation evidence | pass | Focused 13/13 passed during review; author-reported full package 252/252 was consistent but was not rerun as an independent broad-smoke claim. |

## Direct-proof gaps and residual risk

No material proof gap was found for the reviewed defect. Finding-to-artifact semantic selection remains workflow-owned because the durable finding ledger does not encode a mechanically authoritative artifact target; the route still requires workflow authority, explicit destination evidence, current lifecycle revision, and currently open finding IDs. This is unchanged trust allocation rather than a new CLI semantic decision.

## Handoff

This direct review is isolated and makes no independent-review, branch-readiness, verification, or PR-readiness claim. There is no automatic downstream handoff. Workflow may now create the guarded correction route, after which the spec owner can register the already-authored revision; CR1 and CR2 still require their recorded resolution path.
