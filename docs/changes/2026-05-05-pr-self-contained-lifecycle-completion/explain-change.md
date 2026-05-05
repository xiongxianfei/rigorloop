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

## M2 Diff Rationale

| Surface | M2 disposition | Rationale |
| --- | --- | --- |
| `scripts/artifact_lifecycle_validation.py` | updated | Adds plan index/body lifecycle agreement checks, terminal plan readiness checks, and non-blocking tracked merge-dependent lifecycle-language warnings. |
| `scripts/test-artifact-lifecycle-validator.py` | updated | Adds failing-first coverage for completed plans under Active, duplicate Active/Done index entries, index-only plan changes, index/body disagreement, terminal stale readiness, true downstream active plans, and warning behavior. |
| `tests/fixtures/artifact-lifecycle/**` | updated | Adds focused fixture repositories for the new lifecycle validator cases. |
| `scripts/test-review-artifact-validator.py` | updated | Adds direct closeout-mode proof that `Closeout status: open` remains blocking even after material findings are resolved. |
| `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/reviews/**` | added | Records the M2 code-review finding, accepted resolution, and clean re-review. |

## M2 Validation

- `python scripts/test-artifact-lifecycle-validator.py` failed before implementation with the expected new M2 failures.
- A follow-up M2 self-check added and first observed a failing duplicate Active/Done index fixture before tightening the parser.
- M2 code-review added and first observed a failing index-only `docs/plan.md` fixture before expanding plan-index-only scope to linked plan bodies.
- `python scripts/test-artifact-lifecycle-validator.py` passed after implementation.
- `python scripts/test-review-artifact-validator.py` passed.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-05-pr-self-contained-lifecycle-completion` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-05-pr-self-contained-lifecycle-completion` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths <proposal/spec/test-spec/plan-index/plan>` passed with expected non-blocking lifecycle-language warnings.
- `bash scripts/ci.sh --mode explicit <M2 surface>` passed selected checks `review_artifacts.regression`, `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed.
- `git diff --check -- <M2 edited surface>` produced no whitespace diagnostics.
- `bash scripts/ci.sh --mode broad-smoke` passed after M2 review-resolution and clean re-review.

## Current Readiness

M1 is implemented, code-reviewed with no required changes, and verified. M2 is implemented, CR-M2-R1-F1 is accepted and resolved, and M2 re-review is clean. The next implementation milestone is M3, which aligns skills and generated outputs.
