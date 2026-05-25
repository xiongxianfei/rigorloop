# Code Review M1 R1: Installed-Skill Artifact Placement Contract

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1. Placement Contract Validation Scaffolding
Reviewed artifact: implementation commit `f0320d5`
Review date: 2026-05-25
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m1-r1.md`, `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md`, `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md`, `docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md`, `docs/plan.md`, `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SAP-M1-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md`
- Review resolution: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md`
- Reviewed milestone: M1. Placement Contract Validation Scaffolding
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: SAP-M1-CR1
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `f0320d5` on branch `proposal/installed-skill-artifact-placement-contract`.
- Tracked governing branch state: approved proposal, approved spec, active test spec, active plan, change metadata, review log, and M1 implementation commit are tracked.
- Governing artifacts:
  - `specs/installed-skill-artifact-placement-contract.md`
  - `specs/installed-skill-artifact-placement-contract.test.md`
  - `docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md`
  - `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`
- Validation evidence:
  - `python scripts/test-skill-validator.py` passed with 167 tests after M1 helper implementation.
  - `python scripts/validate-skills.py` passed with 23 skill files.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed.
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md docs/plan.md docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed.

## Diff summary

M1 adds fixture-backed placement contract helpers to `scripts/skill_validation.py` and matching tests in `scripts/test-skill-validator.py`. The helpers check first-slice proposal/spec review placement paths, review-log placement, conditional review-resolution placement, create-or-request change-pack wording before recorded status, isolated advisory carve-out wording, workflow-map drift, and plan-surface path distinctions. The commit also records the proposal, spec, test spec, active plan, and change-local review evidence for this workflow-managed change.

## Findings

### SAP-M1-CR1 - Compliant spec-review fixture does not prove the stage-owned record type

Finding ID: SAP-M1-CR1
Severity: major
Location: `scripts/test-skill-validator.py`, lines 4561-4587; `scripts/skill_validation.py`, lines 502-525.
Evidence: The passing fixture builds `spec_review` by replacing only `proposal-review-r<n>.md` with `spec-review-r<n>.md`. The surrounding prose therefore still says `Formal proposal-review records go under:` for the `spec-review` subtest, and `validate_installed_skill_artifact_placement_contract` accepts it because it checks the path, review log, conditional resolution, change-pack behavior, and isolated advisory wording, but not the stage-owned record type. This misses the approved requirement that each placement block state the artifact or record type owned by the skill.
Required outcome: The M1 validator helper and tests must reject a `spec-review` placement block that names the wrong stage-owned record type, while still accepting compliant `proposal-review` and `spec-review` fixture text.
Safe resolution path: Update the helper to require stage-owned record wording for first-slice review skills, for example `proposal-review record`/`proposal-review records` for `proposal-review` and `spec-review record`/`spec-review records` for `spec-review`. Split or correct the compliant fixtures so the `spec-review` fixture says `Formal spec-review records go under:`. Add a negative assertion for wrong stage-owned wording, rerun `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, lifecycle validation for the touched artifacts, and `git diff --check -- ...`.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | concern | M1 correctly targets R26-R28 helper validation, but `SAP-M1-CR1` leaves R2/T2 stage-owned record-type proof incomplete. |
| Test coverage | concern | Tests cover missing path, missing change-pack behavior, workflow drift, and plan surfaces, but the passing spec-review fixture itself carries the wrong stage-owned prose. |
| Edge cases | concern | The named cold-read/stage-owned edge is not fully protected because a skill-only reader could see the wrong review stage name while validation still passes. |
| Error handling | pass | Helper failures return deterministic error strings; no runtime exception or unsafe fallback path is introduced. |
| Architecture boundaries | pass | No architecture, persistence, API, deployment, or generated adapter boundary is changed in M1. |
| Compatibility | pass | M1 deliberately keeps the new helpers fixture-backed and does not wire canonical enforcement before M2 public skill wording changes. |
| Security/privacy | pass | The diff adds repository-relative path checks only and does not expose secrets, credentials, or private host paths. |
| Derived artifact currency | pass | Generated skill/adapters are not changed in M1; M3 owns generated-output proof. |
| Unrelated changes | pass | The implementation diff is limited to validator/test scaffolding plus the required lifecycle artifacts for the approved change. |
| Validation evidence | concern | Recorded validation commands are relevant and passed, but they did not catch the stage-owned record-type hole described in `SAP-M1-CR1`. |

## No-finding rationale

Not applicable. One material finding requires resolution before M1 can close.

## Residual risks

- Keep the resolution narrow. M1 should add deterministic stage-owned wording coverage without wiring canonical enforcement until M2 updates the public skill text.

## Handoff

This review is recorded. M1 moves to `resolution-needed`. Next stage is `review-resolution` for `SAP-M1-CR1`, then an M1 fix and rerun `code-review`.
