# PR-Self-Contained Lifecycle Completion Change Explanation

## Summary

This change implements the approved PR-self-contained lifecycle completion workflow amendment. M1 aligns the governing and operational guidance so repo-local lifecycle state changes are recorded in the PR that performs the transition before review opens, while true downstream events keep a plan active until the event occurs.

The implementation is intentionally staged. M1 updates authoritative and operational prose plus the baseline change-local evidence. M2 adds validator behavior, M3 updates canonical skill guidance and generated outputs, and M4 closes final evidence and lifecycle state.

## Source Artifacts

- Proposal: `docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Spec: `specs/rigorloop-workflow.md`, especially `R6dc`, `R8h`-`R8hc`, `R8jb`, and `R8kh`-`R8kj`
- Test spec: `specs/rigorloop-workflow.test.md`, especially `T29`-`T32`
- Plan: `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`

## M1 Diff Rationale

| Surface | M1 disposition | Rationale |
| --- | --- | --- |
| `CONSTITUTION.md` | updated | Adds the required governance wording from `R6dc`: synchronization happens in the PR that performs the lifecycle transition before review opens, and merge is not a trigger for further lifecycle changes. |
| `docs/workflows.md` | updated | Replaces routine merge-dependent plan closeout guidance with PR-contained closeout, true downstream event handling, broader lifecycle inconsistency, and tracked merge-dependent language warning guidance. |
| `AGENTS.md` | updated | Keeps concise agent-facing verification guidance aligned with the governing rule without duplicating the full workflow contract. |
| `docs/learn/topics/plan-lifecycle-closeout.md` | updated | Converts the durable lesson away from merge-dependent closeout and toward PR-contained lifecycle synchronization plus true downstream event handling. |
| `docs/plans/0000-00-00-example-plan.md` | unaffected with rationale | Existing wording already says to update the plan body and `docs/plan.md` in the same change when the lifecycle decision is known; it does not preserve the removed merge-dependent exception. |
| `README.md` | unaffected with rationale | Current README points to workflow docs and does not carry the stale merge-dependent plan-closeout rule. |
| Canonical stage skills and generated outputs | deferred to M3 | The active plan owns canonical skill updates and generated `.codex/skills/` plus `dist/adapters/` refresh in M3 so generated-output drift is handled in one coherent slice. |

## SR-1 Resolution

Spec-review SR-1 asked where merge-dependent language classification is recorded. The active test spec resolves this for the first slice: a warning is treated as addressed only when a contributor-visible tracked or review-visible surface classifies the wording as a true downstream completion event or stale lifecycle wording requiring correction. Automatic warning suppression after classification is not required in the first implementation slice.

## M1 Validation

M1 validation is recorded in `change.yaml` and the active plan.

- `rg -n 'Only merge-dependent ...' CONSTITUTION.md AGENTS.md docs/workflows.md docs/learn/topics/plan-lifecycle-closeout.md docs/plans/0000-00-00-example-plan.md README.md` produced no matches after M1 edits.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed.
- `python scripts/select-validation.py --mode explicit <M1 surface>` passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, and `selector.regression`.
- `bash scripts/ci.sh --mode explicit <M1 surface>` passed with the same selected check IDs.
- `git diff --check -- <M1 edited surface>` produced no whitespace diagnostics.

The first stale-wording scan intentionally failed before M1 edits because stale merge-dependent closeout wording still existed in workflow docs and canonical skills. Skill wording remains deferred to M3 with tracked rationale.

## Current Readiness

M1 is implemented, code-reviewed with no required changes, and verified. The next implementation milestone is M2, which adds lifecycle validator coverage.
