# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1. Baseline and Validator Foundation
Reviewed artifact: commit `4ebe5c4` (`M1: add proposal-family asset validator foundation`)
Review date: 2026-05-20
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: PFA-M1-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md
- Review resolution: docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md
- Reviewed milestone: M1. Baseline and Validator Foundation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: PFA-M1-CR1
- Verify readiness: not-claimed

## Scope

Reviewed the M1 implementation against the actual commit diff, the approved proposal-family asset spec and test spec, the active plan milestone, baseline evidence, validator changes, fixture tests, and recorded validation evidence.

## Review inputs

- Diff/review surface: commit `4ebe5c4`
- Tracked governing branch state: commit `4ebe5c4` on `proposal/proposal-family-assets-progressive-disclosure`
- Governing artifacts:
  - `specs/proposal-family-assets-progressive-disclosure.md`
  - `specs/proposal-family-assets-progressive-disclosure.test.md`
  - `docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md`
  - `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md`
- Validation evidence:
  - `python scripts/test-skill-validator.py` - pass, 150 tests
  - `python scripts/validate-skills.py` - pass, 23 skill files
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass before this review record
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` - pass, 3 artifact files
  - `git diff --check --` - pass

## Diff summary

- Added the proposal-family accepted artifact set and review-class structural-label/forbidden-label constants to `scripts/skill_validation.py`.
- Added proposal-family asset validation for approved asset paths, non-asset packaged resources, resource-map `COPY` entries, metadata, statuses, placeholders, filler text, root dependencies, and proposal-review policy-shaped content.
- Extended generated asset presence mapping to include proposal-family skills.
- Added fixture tests for valid proposal-family asset layouts, invalid asset inventories, bad resource-map entries, metadata/status/placeholder failures, proposal-review forbidden labels/prose, generated-output missing asset naming, and baseline-summary presence.
- Created the pinned baseline and change metadata, and updated the active plan to hand off M1 for code review.

## Findings

### PFA-M1-CR1 - Major: proposal-review asset validation does not reject non-allowlisted structural labels

Finding ID: PFA-M1-CR1
Severity: major
Location: `scripts/skill_validation.py:212`, `scripts/skill_validation.py:700`
Evidence: The implementation defines `PROPOSAL_REVIEW_ASSET_ALLOWED_FIELD_LABELS` at `scripts/skill_validation.py:212`, but `_proposal_review_asset_policy_lines` only uses the allowlist to skip allowed labels. A field label that is not in the allowlist is appended to `review_policy_lines` at `scripts/skill_validation.py:716`, and `_validate_proposal_family_asset_file` only turns that into an error if `PROPOSAL_REVIEW_ASSET_FORBIDDEN_POLICY_PATTERN` matches at `scripts/skill_validation.py:778`. That means a non-allowlisted label such as `Architecture impact: <guidance>` or `Testability notes: <notes>` can pass if it does not contain one of the currently forbidden phrases.
Required outcome: `proposal-review` asset validation must fail for field labels that match the structural label shape but are not in `PROPOSAL_REVIEW_ASSET_ALLOWED_FIELD_LABELS`, independent of the forbidden-policy regex.
Safe resolution path: Add a validator error for non-allowlisted `proposal-review` field labels, add a failing fixture such as `- Architecture impact: <guidance>` or `- Testability notes: <notes>`, keep the existing allowed-label fixtures passing, rerun `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, change metadata/review artifact validation, lifecycle validation, and `git diff --check --`.

Governing requirement: `PFA-R25` requires an explicit structural-label allowlist, `PFA-R26` says the allowlist includes only fields needed by `review-result-skeleton.md` and `material-finding.md`, and `PFA-R51` requires deterministic proposal-review structural-label allowlist checks. The test spec also requires invalid proposal-family asset fixtures for review-judgment assets.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `PFA-R25` through `PFA-R27` require an explicit structural-label allowlist; the validator does not reject all non-allowlisted labels. |
| Test coverage | concern | The tests cover required forbidden labels and positive allowed labels, but do not cover a non-allowlisted neutral-looking label. |
| Edge cases | concern | `proposal-review` assets with policy-shaped labels not named in the forbidden regex can slip through. |
| Error handling | pass | Existing metadata, placeholder, root dependency, resource-map, and generated-output helper errors are stable and specific. |
| Architecture boundaries | pass | M1 does not change architecture, adapter roots, lockfiles, CLI behavior, or generated output. |
| Compatibility | pass | The diff is additive validator/test coverage and does not alter public skill behavior in M1. |
| Security/privacy | pass | No secrets, credentials, external services, unsafe logging, or auth/security runtime behavior are introduced. |
| Derived artifact currency | pass | M1 does not edit generated output; generated mirror and adapter proof remain assigned to M4. |
| Unrelated changes | pass | The implementation is scoped to lifecycle artifacts, baseline evidence, validator logic, and validator tests for this initiative. |
| Validation evidence | concern | The recorded commands pass, but the missing non-allowlisted-label test leaves a requirement gap in the proof surface. |

## No-finding rationale

Not applicable; material finding `PFA-M1-CR1` requires resolution before M1 can close.

## Residual risks

After fixing `PFA-M1-CR1`, M2 and M3 still need code review to ensure the real extracted assets satisfy the validator boundary and keep rules in `SKILL.md`.

## Handoff

- Reviewed milestone: M1. Baseline and Validator Foundation
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Recommended next stage: review-resolution for `PFA-M1-CR1`, then return M1 to implementation and rerun code-review.
- Final closeout readiness: not ready; M1 has an open finding and M2-M4 remain open.
