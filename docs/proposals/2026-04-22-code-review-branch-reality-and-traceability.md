# Code Review Branch Reality And Traceability

## Status

- accepted

## Problem

A real project review exposed a remaining gap in the repository's review workflow.

The earlier fix for code-review independence improved first-pass review posture, but it did not fully prevent an implementer-side sanity check from being described too much like a real review result. In the incident that surfaced this proposal:

- an implementation-stage statement said there were no required M1 fixes;
- later manual code-review found one major issue and one minor issue;
- the earlier statement had treated local worktree artifact presence as if it proved branch reality; and
- it inferred test-spec coverage from code shape instead of citing direct proof for the named edge case.

The problem is no longer just "review is not independent enough." The deeper problem is that workflow skills still allow overconfident review-like claims when:

- the speaker is not actually in `code-review`;
- governing artifacts exist locally but are not actually tracked on the branch; or
- requirement and test-spec traceability is inferred instead of demonstrated.

That combination weakens trust in both `code-review` and `verify`, especially for milestone-based work where "milestone-ready" and "branch-ready" are easy to blur.

## Goals

- Prevent `implement` or other non-review stages from making review conclusions they do not own.
- Make branch-scoped review and readiness claims depend on tracked branch reality, not local file presence.
- Make clean review claims cite direct requirement and test-spec evidence for named edge cases instead of relying on inference.
- Preserve the existing workflow order and the earlier independent-review work instead of replacing it.
- Reduce false clean results without forcing universal human review or heavy new automation in the first slice.

## Non-goals

- Reverting workflow autoprogression.
- Requiring a human reviewer for every change.
- Replacing `code-review` with `verify`, tests, or validators alone.
- Building a full review-orchestration subsystem in this slice.
- Solving every possible review-quality problem across every skill in one pass.
- Forcing full automation of semantic test-traceability before the wording contract is stable.

## Context

- The repository already accepted and implemented `code-review` independence under autoprogression.
- That earlier slice improved first-pass review grounding, but it targeted review posture and output shape more than branch-reality checks and stage-owned language.
- Current workflow guidance already distinguishes active tracked artifacts from chat-only state, but the real incident showed that local/untracked artifact presence can still leak into review reasoning.
- The incident also showed a second gap: when a test spec explicitly names an edge case, a reviewer can still over-credit code behavior instead of asking for a direct test or explicit traceability evidence.
- The user feedback is not hypothetical. A manual follow-up review found problems after an earlier agent statement had already implied there were no required milestone fixes.

Related current surfaces:

- `skills/implement/SKILL.md`
- `skills/code-review/SKILL.md`
- `skills/verify/SKILL.md`
- `skills/workflow/SKILL.md`
- `docs/workflows.md`
- `specs/rigorloop-workflow.md`
- `specs/code-review-independence-under-autoprogression.md`

## Options considered

### Option 1: Add a stronger reminder to "be independent" and otherwise keep the current contract

- Advantages:
  - minimal cost
  - no workflow changes
- Disadvantages:
  - repeats the earlier fix without addressing the concrete failure modes
  - still allows worktree presence to masquerade as branch reality
  - still allows non-review stages to sound like they completed review

### Option 2: Move all branch-readiness responsibility into `verify` and leave `code-review` narrow

- Advantages:
  - clearer ownership split on paper
  - keeps `code-review` focused on code and tests
- Disadvantages:
  - leaves review results vulnerable to unsupported clean claims before `verify`
  - does not solve the problem of `implement` making review-like statements
  - pushes too much trust into a later gate

### Option 3: Tighten stage-owned language plus branch-reality and traceability checks across `implement`, `code-review`, and `verify`

- Advantages:
  - addresses the actual incident directly
  - keeps the earlier independent-review work and makes it more operational
  - preserves workflow order while reducing overconfident clean claims
  - lets `implement`, `code-review`, and `verify` each own a narrower, clearer kind of claim
- Disadvantages:
  - adds more explicit wording rules and review discipline
  - may require a follow-up validator later if wording alone drifts

### Option 4: Add immediate validator enforcement for review wording, tracked artifacts, and semantic traceability

- Advantages:
  - strongest enforcement path
  - easiest to audit once fully built
- Disadvantages:
  - too large for the first corrective slice
  - semantic traceability is not stable enough yet for reliable automation
  - risks solving a process problem with premature tooling

## Recommended direction

Choose Option 3.

The repository should add a focused follow-up contract for review grounding that covers three best-practice layers together:

1. Stage-owned language
   - `implement` should report implementation completion, milestone validation, and readiness for `code-review`.
   - `implement` should not say things like "post-implementation review found no required fixes" or otherwise imply that review already happened.
   - `code-review` owns review findings. `verify` owns branch-readiness confirmation. `pr` owns PR-opening readiness.

2. Branch reality over local presence
   - The tracked-branch requirement applies to cited governing artifacts, branch-readiness claims, PR-readiness claims, and claims that an artifact is part of the reviewed branch authority.
   - It does not require every code change under review to already be committed.
   - `code-review` may review actual changed files, staged changes, uncommitted diffs, or a PR diff depending on the review context.
   - If `code-review` cites proposal, spec, test spec, architecture, ADR, or plan artifacts as governing evidence, the reviewer should confirm those inputs are actually present in the reviewed branch state.
   - Local-only governing artifacts may be used as informal background, but they must not support a clean branch-scoped review conclusion.
   - When required governing inputs are not tracked in the reviewed branch state, `code-review` should return `inconclusive` rather than a clean result.
   - `verify` should block branch-readiness or PR-readiness when required authoritative artifacts are missing from tracked branch state.

3. Explicit requirement and test-spec traceability
   - When a test spec names a specific edge case or failure path, a clean review should cite direct proof for that path or explicitly call out the gap.
   - Code-shape inference alone is too weak for a clean result when the test spec asked for a direct simulation or direct coverage of a named path.
   - Review outputs should make it visible which requirement or test-spec item was checked and what evidence supported the conclusion.

The practical best practices are:

- Separate "implementation sanity check" from "review result" in both wording and status.
- Review from `git` reality, not filesystem reality.
- Require direct evidence for named edge cases before calling them covered.
- Distinguish `milestone-ready` from `branch-ready` and do not let either one imply `review-clean`.
- Use wording-first contract changes now, then add automation only after the pattern is stable.

## Expected behavior changes

- `implement` outputs become narrower and stop making review-like conclusions.
- `code-review` becomes stricter about confirming that cited governing artifacts are actually on the reviewed branch.
- `code-review` returns `inconclusive` when a branch-scoped review depends on required governing artifacts that are only local or untracked.
- `code-review` clean results become stricter about direct evidence for named test-spec edge cases.
- `verify` becomes the explicit owner of branch-readiness language and blocks branch-ready or PR-ready claims when required authoritative artifacts are missing from tracked branch state.
- A change can still be implementation-complete or milestone-ready while remaining review-blocked or branch-not-ready.
- The workflow preserves the current stage order and earlier independent-review boundary, but the vocabulary and proof expectations become harder to overstate.

## Architecture impact

This is still a workflow-contract and skill-guidance change, not a runtime architecture change.

Likely touched surfaces:

- a focused follow-up spec for branch-reality and traceability review grounding
- `specs/rigorloop-workflow.md` as the enduring normative home for the repo-wide workflow invariant
- matching test spec
- `skills/implement/SKILL.md`
- `skills/code-review/SKILL.md`
- `skills/verify/SKILL.md`
- `skills/workflow/SKILL.md`
- `docs/workflows.md`
- regenerated `.codex/skills/`

No new storage, service boundary, or standalone orchestration subsystem should be necessary for the first slice.

The focused follow-up spec is the change vehicle. `specs/rigorloop-workflow.md` is the enduring authoritative workflow rule and should not remain optional for this slice.

## Testing and verification strategy

- Write a focused spec for:
  - stage-owned review language;
  - tracked-branch artifact reality for cited governing inputs; and
  - explicit review traceability for named test-spec edge cases.
- Add a matching test spec that covers:
  - `implement` not claiming review completion;
  - `code-review` allowing review of actual changed files while requiring cited governing artifacts to be confirmed in reviewed branch state;
  - `code-review` returning `inconclusive` when required governing inputs are only local or untracked;
  - clean reviews failing or downgrading when named test-spec coverage is only inferred;
  - `verify` blocking branch-ready or PR-ready claims when required authoritative artifacts are missing from tracked branch state;
  - preserved compatibility with the earlier code-review independence slice.
- Use document and skill review to keep `implement`, `code-review`, `verify`, `workflow`, and the short workflow summary aligned.
- Treat the first follow-up slice as contract, skill-wording, test-spec coverage, and manual or document review only.
- Defer validator-backed enforcement for forbidden implement-stage review language to a later follow-up once the wording pattern is stable enough to automate safely.

## Rollout and rollback

Rollout:

- settle this proposal;
- write a focused follow-up spec and test spec;
- update the directly affected workflow and skill surfaces;
- prove the contract through focused test-spec coverage plus manual or document review of the touched surfaces;
- regenerate `.codex/skills/`;
- validate the touched artifact set with repo-owned checks.

Rollback:

- revert the wording and workflow-contract changes if they prove too strict or unclear;
- keep the earlier code-review-independence work unless the repository later decides that work itself needs revision.

## Risks and mitigations

- Risk: the new wording becomes verbose but still does not change behavior.
  - Mitigation: tie the follow-up spec to the exact incident failure modes: stage-owned language, tracked artifact reality, and named test-spec evidence.
- Risk: reviewers still infer coverage from code when a test spec wanted a direct test.
  - Mitigation: require explicit traceability language for named edge cases and treat unsupported clean claims as findings or incompleteness.
- Risk: the slice broadens into a general rewrite of all readiness language.
  - Mitigation: start with `implement`, `code-review`, `verify`, and `workflow` only.
- Risk: automation is added too early and becomes brittle.
  - Mitigation: keep v1 wording-first and defer validators until the contract is stable.
- Risk: users confuse milestone completion with branch readiness less, but still assume either one implies merge readiness.
  - Mitigation: make the stages own different claims explicitly and keep those claims visible in outputs.

## Open questions

- None.

## Decision log

- 2026-04-22: Rejected a reminder-only fix. Reason: the earlier discussion already proved that generic independence language was not enough.
- 2026-04-22: Rejected moving all responsibility into `verify`. Reason: that would leave unsupported clean review claims uncorrected too late in the flow.
- 2026-04-22: Chose stage-owned language plus branch-reality and traceability checks as the recommended direction. Reason: it directly addresses the real incident without redesigning the workflow.
- 2026-04-22: Rejected immediate full automation as the first step. Reason: the wording contract is not stable enough yet for reliable semantic enforcement.
- 2026-04-22: Settled the first follow-up slice as contract, skill wording, test-spec coverage, and manual or document review. Reason: that is the smallest corrective slice that addresses the real incident without betting on premature automation.
- 2026-04-22: Deferred validator-backed enforcement for forbidden implement-stage review language to a later follow-up. Reason: validator enforcement should wait until the wording pattern is stable.
- 2026-04-22: Settled the negative outcome split between `code-review` and `verify`. Reason: `code-review` should return `inconclusive` when required governing inputs are not tracked, while `verify` should block branch-ready or PR-ready claims when required authoritative artifacts are missing from tracked branch state.
- 2026-04-22: Settled the scope of the tracked-branch requirement. Reason: it applies to cited governing artifacts and branch-scoped readiness or authority claims, not as a blanket rule that every reviewed code change must already be committed.
- 2026-04-22: Settled `specs/rigorloop-workflow.md` as a required touched surface and enduring normative home. Reason: this is a repo-wide workflow invariant, while the focused follow-up spec is only the change vehicle.

## Next artifacts

- focused spec for branch-reality and traceability review grounding
- matching test spec
- plan if no separate architecture artifact becomes necessary
- architecture only if the follow-up broadens beyond workflow and skill guidance

## Follow-on artifacts

- `specs/code-review-branch-reality-and-traceability.md`
- `specs/code-review-branch-reality-and-traceability.test.md`
- `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`

## Readiness

- This proposal is accepted.
- The focused follow-up spec now exists and is approved.
- The focused active test spec now exists.
- The active execution plan now exists.
- No further `proposal-review` action is pending.
- No separate architecture artifact is expected for this slice.
- The next stage is `implement`.
- No open proposal-stage questions remain.
