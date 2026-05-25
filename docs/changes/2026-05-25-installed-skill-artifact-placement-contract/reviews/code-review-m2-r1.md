# Code Review M2 R1: Installed-Skill Artifact Placement Contract

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M2. Canonical Skill and Workflow Map Wording
Reviewed artifact: implementation commit `d4b7ef8`
Review date: 2026-05-25
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m2-r1.md`, `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md`, `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md`, `docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md`, `docs/plan.md`, `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SAP-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md`
- Review resolution: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md`
- Reviewed milestone: M2. Canonical Skill and Workflow Map Wording
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: SAP-M2-CR1
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: implementation commit `d4b7ef8` on branch `proposal/installed-skill-artifact-placement-contract-pr`.
- Tracked governing branch state: approved spec, active test spec, active plan, M1 closed review evidence, M2 implementation commit, review log, and change metadata are tracked.
- Governing artifacts:
  - `specs/installed-skill-artifact-placement-contract.md`
  - `specs/installed-skill-artifact-placement-contract.test.md`
  - `docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md`
  - `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`
- Validation evidence:
  - `python scripts/test-skill-validator.py` passed with 172 tests after M2.
  - `python scripts/validate-skills.py` passed with 23 skill files after M2.
  - `python scripts/build-skills.py --check` passed after M2.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml` passed after M2 metadata update.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md --path specs/installed-skill-artifact-placement-contract.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml` passed during review with 3 artifact files.
  - `git diff --check -- ...` passed after M2.

## Diff summary

M2 updates canonical public skill wording for `proposal-review`, `spec-review`, and `plan`; synchronizes `docs/workflows.md` with the portable placement contract and partial workflow-guide fallback rule; adds canonical-surface assertions to `scripts/test-skill-validator.py`; and wires first-slice placement checks into canonical `validate-skills.py` coverage through `scripts/skill_validation.py`. It also updates active lifecycle state and validation metadata for the M2 handoff.

## Findings

### SAP-M2-CR1 - Plan readiness footer still points to implement M2 after M2 handoff

Finding ID: SAP-M2-CR1
Severity: major
Location: `docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md:306`
Evidence: The active plan's `Current Handoff Summary` says the current milestone is M2, the milestone state is `review-requested`, and the next stage is `code-review M2` at lines 61-68. The plan index also says M2 implementation is complete and `code-review M2` is next. But the same plan's `## Readiness` footer still says `Ready for implement M2`; after M2 is committed and handed to review, that readiness line is stale and contradicts the live handoff state.
Required outcome: Synchronize the plan readiness footer with the active handoff state so it no longer says `implement M2` after M2 has already been implemented and reviewed.
Safe resolution path: Update the plan readiness footer to point to the active next stage for this finding loop, then rerun lifecycle validation for the plan, plan index, change metadata, review log, review-resolution, and this review record. Keep the active plan's `Current Handoff Summary`, `docs/plan.md`, review log, and change metadata aligned.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | `proposal-review` states `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`; `spec-review` states `docs/changes/<change-id>/reviews/spec-review-r<n>.md`; both state review-log, conditional review-resolution, create-or-request change-pack behavior, clean review handling, isolated advisory behavior, and per-artifact workflow-guide fallback. |
| Test coverage | pass | `scripts/test-skill-validator.py` adds canonical checks for first-slice review skills and `plan`; implementation evidence shows 172 tests passed. |
| Edge cases | pass | The edited skill wording covers partial workflow-guide fallback, clean formal review without empty resolution, missing change pack fallback, isolated advisory review, and plan-surface disambiguation. |
| Error handling | pass | The validator returns deterministic errors for missing paths, missing stage-owned wording, missing change-pack behavior, missing plan surfaces, and workflow-map drift. Unknown review skills return without first-slice placement errors. |
| Architecture boundaries | pass | No new runtime components, persistence, APIs, schemas, CLI scaffolding, generated shared partials, or adapter output edits are introduced. |
| Compatibility | concern | Public skill and workflow-map compatibility is preserved, but lifecycle handoff compatibility has a stale plan readiness line captured in `SAP-M2-CR1`. |
| Security/privacy | pass | The wording uses portable project-relative paths and does not require secrets, credentials, host-specific paths, generated adapter internals, or maintainer-only implementation mechanics. |
| Derived artifact currency | pass | `python scripts/build-skills.py --check` validates generated local skill mirrors from canonical source; adapter archive proof remains correctly scoped to M3. |
| Unrelated changes | pass | The diff is limited to first-slice skill/workflow wording, skill validation/tests, and required lifecycle evidence. |
| Validation evidence | concern | The recorded M2 validation commands are relevant and passed, but they did not catch the stale plan readiness footer described in `SAP-M2-CR1`. |

## No-finding rationale

Not applicable. One material finding requires resolution before M2 can close.

## Residual risks

- M3 still owns generated adapter output proof and cold-read evidence; this review does not claim installed adapter readiness.
- The M2 validator wiring intentionally enforces plan-surface checks only for canonical `plan` in this slice; broader plan-family rollout remains outside M2 unless later approved.

## Handoff

This review is recorded. M2 moves to `resolution-needed`. Next stage is `review-resolution` for `SAP-M2-CR1`, then an M2 fix and rerun `code-review`.
