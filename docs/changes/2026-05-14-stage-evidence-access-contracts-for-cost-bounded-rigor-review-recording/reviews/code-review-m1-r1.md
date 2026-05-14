# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Target: commit 1ef3725
Reviewed artifact: M1 proposal-side stage evidence access implementation
Review date: 2026-05-14
Reviewer: Codex code-review
Recording status: recorded
Status: changes-requested

## Review status

changes-requested

## Review inputs

- Diff/review surface: commit `1ef3725` (`M1: add proposal-side stage evidence access guidance`).
- Tracked governing branch state: accepted proposal, approved spec, active test spec, active plan, review records, change metadata, and implementation commit are tracked.
- Governing artifacts:
  - `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md`
  - `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md`
  - `docs/plans/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md`
- Validation evidence:
  - `python scripts/test-skill-validator.py` passed after the test-first failure and guidance implementation.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md` passed and did not select M2 skill paths.
  - `python scripts/build-skills.py --check`, `python scripts/test-build-skills.py`, and the selected adapter archive smoke passed.
  - lifecycle, review-artifact, change-metadata, selector-regression, static token measurement, and `git diff --check --` validation passed.

## Diff summary

The implementation adds a shared `Stage Evidence Access` model to `docs/workflows.md`, adds concise evidence-access sections to `proposal` and `proposal-review`, leaves `spec` unchanged with rationale in the active plan, and adds concept-level static checks in `scripts/test-skill-validator.py`.

The commit also adds the proposal, spec, test spec, active plan, plan index update, change metadata, and prior lifecycle review records for the initiative.

## Findings

### SEA-M1-CR1-1 - Committed plan index includes an unrelated M5 lifecycle transition without its synchronized plan body

Finding ID: SEA-M1-CR1-1
Severity: major

Location: `docs/plan.md`

Evidence: The M1 commit changes `docs/plan.md` by moving `2026-05-14 Cost-bounded rigor M5 progressive-loading follow-through` from `Active` to `Done`, but the matching M5 plan-body closeout is not part of the committed review surface. In the committed branch state, `docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md` still has `Status: active`, `Next stage: hosted CI / PR review`, and `Final closeout readiness: pr-open`, while `docs/plan.md` now says the same plan is completed and merged.

Required outcome: The M1 implementation commit must not include an unrelated M5 lifecycle transition unless the synchronized M5 plan-body closeout is also intentionally in scope. For this M1 review, remove the unrelated M5 index transition from the committed M1 diff and keep only the stage evidence access plan-index change.

Safe resolution path: Restore the M5 `docs/plan.md` entry to its pre-M1 location/state in the committed diff, leave the unrelated dirty M5 plan-body work outside this milestone, rerun lifecycle and diff validation, and rerun code-review.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | concern | The evidence-access guidance itself satisfies M1 scope, but the plan-index M5 transition is outside R1-R34. |
| Test coverage | pass | Static concept checks cover shared model, proposal-side local guidance, bounded discovery, expansion reason behavior, and M1/M2 validation separation. |
| Edge cases | pass | `spec` is unchanged with rationale; M2 `implement`, `code-review`, and `plan` skills are not edited. |
| Error handling | pass | No runtime behavior changed; guidance preserves expansion on missing, stale, contradictory, or insufficient bounded evidence. |
| Architecture boundaries | pass | No architecture, runtime, adapter packaging, release, or generated-output source model change is introduced by the evidence-access implementation. |
| Compatibility | concern | The unrelated M5 plan-index transition creates branch-state lifecycle drift against the committed M5 plan body. |
| Security/privacy | pass | Guidance favors targeted evidence and avoids broad dumps. |
| Derived artifact currency | pass | Generated local mirror checks and adapter archive smoke passed. |
| Unrelated changes | block | `docs/plan.md` includes an unrelated M5 lifecycle transition without the matching committed plan body. |
| Validation evidence | pass | Named selected checks and lifecycle validations were run, but they did not include the committed M5 plan body and therefore did not catch the unrelated drift. |

## No-finding rationale

Not applicable; one material finding requires a targeted fix before a clean M1 review.

## Residual risks

The unrelated dirty M5 plan-body closeout remains in the local worktree outside this M1 review surface and must not be silently committed as part of M1.

## Milestone-aware handoff

- Reviewed milestone: M1. Proposal-side stage evidence access guidance.
- Review status: changes-requested.
- Milestone state after review: resolution-needed.
- Required review-resolution: required for `SEA-M1-CR1-1`.
- Remaining implementation milestones: M1.
- Next stage: review-resolution / implement fix for M1.
- Final closeout readiness: not ready; M1 has an open code-review finding.
