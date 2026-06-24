# Learn Session: Verify Repetition Cost

## Status

Recorded: 2026-06-24

Session state: recorded

## Frame

Trigger:

The maintainer explicitly invoked `learn` after the implementation-autoprogression change required repeated `verify` passes and asked why the verify stage cost so many times.

Trigger type:

Explicit maintainer request / contributor observation after repeated verification and commit-amend cycles.

Scope:

- Why this change's final verify repeated.
- Which repetitions were required by the workflow contract.
- Which repetitions were avoidable process or evidence-shape churn.
- Candidate follow-ups for future final-verify cost reduction.

Evidence in scope:

- `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/verify-report.md`
- `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/change.yaml`
- `docs/plans/2026-06-24-implementation-autoprogression-through-verify.md`
- `docs/plan.md`
- Recent reflog entries for `Add implementation autoprogression profile`, including initial commit and later amends.
- Final clean-worktree verification evidence for commit `64d0d21a`.
- Prior learn topic `docs/learn/topics/plan-lifecycle-closeout.md`
- Prior learn topic `docs/learn/topics/workflow-stage-order.md`
- Prior session `docs/learn/sessions/2026-05-08-verify-explain-change-order.md`
- Prior session `docs/learn/sessions/2026-05-24-adoption-surface-cache-nonuse.md`

Explicit exclusions:

- No workflow, validator, skill, or topic guidance update is made by this session.
- No claim is made about hosted CI; hosted CI was not observed.
- No new PR readiness or plan completion state is created by `learn`.
- No retrospective rewrites are made to the implementation-autoprogression verify report beyond what was already committed before this session.

Prior learnings reviewed:

- `docs/learn/topics/plan-lifecycle-closeout.md`
- `docs/learn/topics/workflow-stage-order.md`
- `docs/learn/sessions/2026-05-08-verify-explain-change-order.md`
- `docs/learn/sessions/2026-05-24-adoption-surface-cache-nonuse.md`

Session record path:

`docs/learn/sessions/2026-06-24-verify-repetition-cost.md`

## Observe

### O1 - The first expensive verify found a real branch-readiness blocker

Evidence:

- The earlier verify report recorded `Result: blocked`, `Branch readiness: not ready`, and a blocker for an intentionally invalid metadata fixture whose path and `change_id` tripped unrelated lifecycle ownership checks before the intended forbidden-field proof could be isolated.
- The report also recorded a second blocker: required new governing and change-local artifacts were untracked.
- The verification-fix slice then moved the invalid fixture under the change ID path and reran code-review M5 R2.

Observation:

This part of the cost was mostly legitimate. Final verify is required to catch lifecycle and branch-state blockers that are invisible to narrower unit tests. Once the fixture path changed, the workflow correctly required review evidence and fresh verification because the branch-ready surface had changed.

### O2 - Broad validation was rerun before the tracked-state blocker was resolved

Evidence:

- Before commit, final validation repeatedly ran broad checks such as `test-artifact-lifecycle-validator.py`, `test-skill-validator.py`, adapter archive validation, and `test-adapter-distribution.py`.
- At that time, the required new governing and change-local artifacts were still untracked, so branch readiness could not pass regardless of the expensive validation result.
- After the artifacts were committed, a clean-worktree lifecycle check validated zero local artifact files and the branch-state blocker disappeared.

Observation:

Some cost was avoidable. The verify sequence proved expensive local checks while a cheaper precondition, "all authoritative artifacts that branch readiness depends on are tracked," was still false. A staged or committed-state preflight before broad smoke would have prevented at least one expensive pass from ending in a known branch-readiness block.

### O3 - The verify report became stale when the commit changed repository state

Evidence:

- The report was updated from blocked to passed only after the required artifacts were committed.
- That commit changed the facts reported by verify: the branch-state blocker no longer existed, `docs/plan.md` and the plan body could route to `pr`, and `change.yaml` needed a final pass event.
- This required artifact edits and an amend even after the first successful commit.

Observation:

The cost came from verifying a pre-commit worktree and then using commit creation to resolve a verify blocker. When commit/stage state itself is part of the verification claim, final verify should either run after the commit exists or use an evidence pattern that explicitly anticipates a post-commit refresh.

### O4 - Self-referential commit hashes caused extra amend churn

Evidence:

- The reflog shows one initial commit and three amend states for the same message:

```text
3e6c8739 commit: Add implementation autoprogression profile
ff6f11d8 commit (amend): Add implementation autoprogression profile
c811628a commit (amend): Add implementation autoprogression profile
64d0d21a commit (amend): Add implementation autoprogression profile
```

- The verify report and change metadata briefly embedded earlier amended hashes such as `3e6c8739` and `ff6f11d8`.
- Amending the commit changed the hash again, making the embedded hash stale.
- The final committed report uses stable wording: current `HEAD` and clean worktree, not a literal self-referential commit hash.

Observation:

This was avoidable. A commit cannot reliably record its own final hash inside the files it contains when the commit is still being amended. For tracked evidence inside the same commit, use stable references such as current `HEAD`, branch state, clean worktree, or an external post-commit note, not the commit's literal hash.

## Root Cause

The verify stage cost so many times for two different reasons:

1. Required cost: final verify correctly found a real lifecycle fixture blocker and later enforced that branch readiness depended on required authoritative artifacts being tracked.
2. Avoidable cost: the sequence ran expensive broad validation before the cheap tracked-state precondition was resolved, then tried to record mutable commit hashes inside the commit being amended.

The repeated loop was not caused by failing tests. The validation suites were mostly passing. The churn came from evidence-state changes around verify: untracked authoritative artifacts, stale verify-report status after commit, and self-invalidating commit-hash references.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | session record only | maintainer question plus verify report evidence | The original blocker was real and already fixed; this explains legitimate cost rather than creating new guidance. |
| O2 | process-follow-up | pending confirmation | candidate verify preflight or workflow/verify skill guidance | not confirmed | A cheap tracked-state preflight before broad smoke would reduce repeated cost, but changing verify sequencing belongs in an owning artifact. |
| O3 | process-follow-up | pending confirmation | candidate workflow/verify guidance for post-commit evidence refresh | not confirmed | The pattern is reusable, but it would change final-verify process expectations. |
| O4 | durable-lesson candidate | pending confirmation | candidate topic entry or verify-report guidance: avoid self-referential hashes in same-commit evidence | not confirmed | The pattern is clear and reusable, but contributor confirmation is required before routing to a topic or authoritative artifact. |

Contributor confirmation status:

The maintainer confirmed the trigger by asking why verify cost so many times. No confirmation was given to update topic guidance, workflow guidance, validators, or skills from this session.

## Route

- Session record created.
- No topic update made because final durable classification and routing require contributor confirmation.
- No workflow, verify skill, validator, plan template, or artifact contract update made from this learn session.

## Candidate Follow-Ups

Pending contributor confirmation:

1. Add a verify preflight checklist or validator helper that checks branch-state preconditions before broad smoke:

```text
git status --short
required authoritative artifacts tracked
plan index and plan body agree
review closeout clean
explain-change exists and is current
```

2. Update verify guidance to prefer stable same-commit evidence wording:

```text
use: current HEAD, clean worktree, tracked branch state
avoid: literal final commit hash inside a file that will be amended into that same commit
```

3. Consider a two-step final verify shape for large changes:

```text
preflight verify: cheap branch-state and artifact-state gates
broad verify: expensive tests and adapter/release checks only after preflight passes
```

## Validation

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-06-24-verify-repetition-cost.md`: passed; no lifecycle-managed artifact files were selected.
- `git diff --check -- docs/learn/sessions/2026-06-24-verify-repetition-cost.md`: passed.
- `python scripts/select-validation.py --mode explicit --path docs/learn/sessions/2026-06-24-verify-repetition-cost.md`: passed; selected `guide_system.validate`.
- `python scripts/validate-guide-system.py`: passed.
