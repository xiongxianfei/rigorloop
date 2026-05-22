# Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M4. Preservation evidence and lifecycle closeout in working tree
Status: changes-requested

## Review inputs

- Review surface: M4 working-tree diff for final identity evidence, `behavior-preservation.md`, `script-output-layer-audit.md`, `change.yaml`, the active plan, and plan index.
- Governing artifacts: `CONSTITUTION.md` planned-initiative state ownership rules; `specs/script-output-optimization.md` R49 through R50, R62 through R65, and AC21, AC27 through AC30, AC35 through AC36; `specs/script-output-optimization.test.md` TSRO-015 through TSRO-027; M4 in `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`.
- Validation evidence: M4 validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`, including final hash comparison, replayed producer selected-test extraction, ordinary output-contract validation, broad-smoke default and verbose runs, selected-CI regression, lifecycle validation, metadata validation, review-artifact validation, and patch hygiene.
- Related lifecycle artifacts inspected: `docs/plan.md`, `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-log.md`, and `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-resolution.md`.

## Diff summary

M4 adds final broad-smoke child-command identity evidence and final producer selected-test identity evidence. The broad-smoke command list hash remains `8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f`, and the producer selected-test hash remains `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`.

The audit and behavior-preservation evidence record the final identity proofs, selected-CI regression proof, ordinary-validation coverage proof, and out-of-scope surface proof. The plan index and change metadata record M4 validation evidence.

## Findings

### BSO-M4-CR1: M4 milestone state is internally stale after implementation handoff

Finding ID: BSO-M4-CR1
Severity: major
Location: `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md:65`, `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md:276`, `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md:296`

Evidence: Before this review was recorded, the active plan's Current Handoff Summary said:

```text
Current milestone state: review-requested
```

But the M4 milestone body still said:

```text
Milestone state: planned
```

M4 explicitly includes lifecycle state synchronization as an implementation responsibility:

```text
Synchronize `docs/plan.md`, this plan, and `change.yaml` before final closeout gates.
```

The constitution also requires the active plan's Current Handoff Summary to own current live state and requires state-changing handoffs to perform a state-sync check across affected owners. With the M4 body still marked `planned`, the plan is internally contradictory at the exact milestone whose closeout purpose is preservation evidence and lifecycle synchronization.

Required outcome: The active plan must have a consistent M4 state across its Current Handoff Summary and M4 milestone body before M4 can close or downstream final closeout can begin.

Safe resolution path: Update the M4 milestone body to the current lifecycle state used by the handoff. Because this review records a material finding, the immediate state should be `resolution-needed`; after the fix is implemented and re-reviewed cleanly, move M4 to `closed` and synchronize `docs/plan.md`, the active plan, and `change.yaml`. Rerun metadata, artifact lifecycle, review-artifact, and patch-hygiene validation.

## Checklist coverage

- Spec alignment: pass. Final broad-smoke and producer identity hashes match baseline evidence, and M4 records ordinary-validation, selected-CI, and out-of-scope surface proof.
- Test coverage: pass. Recorded M4 validation includes ordinary `python scripts/test-select-validation.py`, direct producer modes, broad-smoke default and verbose runs, and selected explicit CI.
- Edge cases: pass. M4 preserves quiet compatibility proof, verbose proof, selected-CI regression proof, and no generated/artifact scope expansion.
- Error handling: pass. M4 does not change runtime failure handling; prior failure-output behavior remains covered by M2 and M3 tests.
- Architecture boundaries: pass. M4 updates evidence and lifecycle artifacts only; no new architecture surface or shared helper is introduced.
- Compatibility: concern. The plan's M4 lifecycle state is inconsistent between the handoff summary and the milestone body.
- Security/privacy: pass. M4 evidence does not add secrets, credentials, or unsafe environment dumps.
- Derived artifact currency: pass. M4 records no generated skill, adapter, public package, JSON, validation selection, or validation coverage changes.
- Unrelated changes: pass. The M4 diff is scoped to final evidence and lifecycle state handoff.
- Validation evidence: concern. The runtime validation evidence is credible, but lifecycle state synchronization is not yet complete enough to close M4.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M4. Preservation evidence and lifecycle closeout
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `BSO-M4-CR1`
Remaining implementation milestones: M4 resolution and re-review
Verify readiness: not-claimed
