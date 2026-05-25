# Code Review M1 R2: Installed-Skill Artifact Placement Contract

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M1. Placement Contract Validation Scaffolding
Reviewed artifact: resolution commit `d2e665d`
Review date: 2026-05-25
Recording status: recorded
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m1-r2.md`, `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md`, `docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md`, `docs/plan.md`, `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`
- Open blockers: none
- Next stage: implement M2
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/code-review-m1-r2.md`
- Review log: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md`
- Review resolution: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md`
- Reviewed milestone: M1. Placement Contract Validation Scaffolding
- Milestone closeout: closed
- Remaining implementation milestones: M2, M3
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: resolution commit `d2e665d` and focused diff `5a544bd..HEAD` for `scripts/skill_validation.py` and `scripts/test-skill-validator.py`.
- Tracked governing branch state: approved spec, active test spec, active plan, M1 implementation commit `f0320d5`, first-pass review `code-review-m1-r1`, closed `review-resolution.md`, and resolution commit `d2e665d` are tracked on branch `proposal/installed-skill-artifact-placement-contract`.
- Governing artifacts:
  - `specs/installed-skill-artifact-placement-contract.md`
  - `specs/installed-skill-artifact-placement-contract.test.md`
  - `docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md`
  - `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md`
- Validation evidence:
  - `python scripts/test-skill-validator.py` passed with 170 tests.
  - `python scripts/validate-skills.py` passed with 23 skill files.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml` passed.

## Diff summary

The resolution adds first-slice record-type expectations for `proposal-review` and `spec-review` to the placement helper, checks those expectations only against the extracted `Artifact placement` block, and keeps canonical skill enforcement deferred until M2. The tests now build explicit compliant fixtures for both review skills and add negative coverage for wrong-stage record wording, missing stage-owned record wording, and non-placement prose that should not satisfy the placement block.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | The helper now covers R2/T2 stage-owned record type in addition to M1's existing R26-R28 placement checks, without changing public skill wording or generated output before M2/M3. |
| Test coverage | pass | `test_installed_skill_artifact_placement_contract_helper_rejects_wrong_record_type`, `...rejects_missing_record_type`, and `...rejects_wrong_record_type_in_artifact_placement_only` directly prove `SAP-M1-CR1`; `python scripts/test-skill-validator.py` passed. |
| Edge cases | pass | The exact regression, `spec-review` path with `proposal-review records` prose, is rejected; the reverse proposal/spec case is also covered. |
| Error handling | pass | The helper returns deterministic error strings and keeps unknown skill names outside this first-slice check. |
| Architecture boundaries | pass | The change stays in validator/test scaffolding and does not add runtime components, persistence, generated-output logic, or public skill wording. |
| Compatibility | pass | `python scripts/validate-skills.py` still passes because canonical enforcement remains intentionally deferred until M2. |
| Security/privacy | pass | The diff adds static path/prose checks only and introduces no secrets, host paths, credentials, or policy-sensitive data. |
| Derived artifact currency | pass | No generated skills or adapters are changed in M1; M3 remains responsible for generated-output proof. |
| Unrelated changes | pass | The resolution diff is limited to the accepted helper/test fix plus lifecycle state updates for the review-resolution loop. |
| Validation evidence | pass | Skill tests, skill validation, review artifact structure/closeout, change metadata validation, lifecycle validation, and diff checks are recorded in the active plan/change metadata. |

## No-finding rationale

The original finding is resolved: the helper now rejects wrong stage-owned record types in the placement block and the tests include the exact failing shape from `SAP-M1-CR1`. Existing M1 checks for path, review log, conditional review-resolution, change-pack behavior, isolated advisory carve-out, workflow drift, and plan surfaces remain intact, and canonical public skill enforcement remains deferred to M2 as planned.

## Residual risks

- M1 proves helper behavior only. M2 still needs to wire the first-slice public skill wording and workflow-map synchronization into canonical validation after the skill text is updated.

## Handoff

M1 is clean and closed. Next stage is `implement M2`. This review does not claim branch readiness, PR readiness, generated adapter readiness, or final verification.
