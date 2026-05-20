# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M3. `spec-review` assets
Reviewed artifact: commit `be799f9` (`M3: add spec-review assets`)
Review date: 2026-05-20
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: SFA-M3-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/code-review-m3-r1.md
- Review log: docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md
- Review resolution: docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md
- Reviewed milestone: M3. `spec-review` assets
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Finding IDs: SFA-M3-CR1
- Verify readiness: not-claimed

## Scope

Reviewed M3 against the actual implementation diff, approved spec and test
spec, active plan, changed `spec-review` skill/assets, validator changes, and
recorded M3 validation evidence.

## Review inputs

- Diff/review surface: commit `be799f9`
- Tracked governing branch state: commit `be799f9` on `proposal/spec-family-assets-progressive-disclosure`
- Governing artifacts:
  - `specs/spec-family-assets-progressive-disclosure.md`
  - `specs/spec-family-assets-progressive-disclosure.test.md`
  - `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md`
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md`
- Validation evidence:
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `git diff --check -- .`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`

## Diff summary

- Added `skills/spec-review/assets/review-result-skeleton.md` and
  `skills/spec-review/assets/review-finding.md`.
- Added `COPY` resource-map entries to `skills/spec-review/SKILL.md` and
  replaced the inline output skeleton with asset-copy guidance.
- Recorded M3 preservation, behavior-parity, token, and cold-read evidence.
- Adjusted review-class asset validation to allow structural field-label lines
  while still attempting to reject review-policy prose.

## Findings

### SFA-M3-CR1 - Review-class policy validator now allows forbidden policy labels

Finding ID: SFA-M3-CR1
Severity: major
Location: `scripts/skill_validation.py:179`, `scripts/skill_validation.py:599`, `scripts/test-skill-validator.py:831`

Evidence: `SPEC_REVIEW_ASSET_ALLOWED_FIELD_LABEL_PATTERN` accepts any simple field-label line ending in a placeholder, and `_validate_spec_family_asset_file` removes every matching line before applying `SPEC_REVIEW_ASSET_FORBIDDEN_POLICY_PATTERN`. That means a spec-review asset line such as `- Severity policy: <policy>` or `- Recording-status rules: <rules>` would be skipped before the forbidden-policy check, even though `SFA-R24` says spec-review assets must not contain severity policy or recording-status rules. The updated positive fixture proves `Recording status` is accepted, but the negative fixture only checks prose (`This asset MUST define severity policy...`) and does not prove forbidden policy labels still fail.

Required outcome: Keep structural field labels such as `Recording status`, `Review record`, and `Review resolution` valid, but ensure forbidden review-policy labels or rule-like labels containing `severity policy`, `sufficiency`, `safe-resolution decision`, `recording-status rules`, `security`, `privacy`, `observability`, or `review dimension` still fail deterministically.

Safe resolution path: Replace the broad field-label exemption with an explicit allowlist of approved structural labels for `spec-review` assets, or run the forbidden-policy check against the label text before exempting a line. Add a negative fixture/test proving a field-label-shaped forbidden policy line, such as `- Severity policy: <policy>`, still fails with the existing review-policy error.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `SFA-R24` and `SFA-R42` require deterministic review-class boundary checks; the validator currently skips forbidden policy terms when they appear as placeholder field labels. |
| Test coverage | block | The positive fixture covers allowed `Recording status`, but no negative fixture proves forbidden policy field labels still fail. |
| Edge cases | block | The named review-class asset boundary includes severity policy and recording-status rules; those exact label-shaped cases are not protected after the validator relaxation. |
| Error handling | pass | The issue is validator coverage, not runtime error behavior. Existing validator errors remain stable for prose violations. |
| Architecture boundaries | pass | No adapter roots, lockfiles, CLI behavior, or release trust boundaries changed. |
| Compatibility | concern | The intended compatibility of review-class assets is preserved in current assets, but the validator no longer reliably enforces that boundary for future edits. |
| Security/privacy | concern | The same broad exemption could allow `Security: <...>` or `Privacy: <...>` field labels in a spec-review asset despite `SFA-R24`. |
| Derived artifact currency | pass | M3 does not own generated mirror or adapter archive proof; M5 remains responsible for generated-output proof. |
| Unrelated changes | pass | The diff is scoped to M3 assets, validator/test updates, and lifecycle evidence. |
| Validation evidence | concern | Recorded validation passed, but it did not exercise the forbidden-policy-as-field-label regression. |

## No-finding rationale

Not applicable; M3 has one required-change finding.

## Residual risks

M4 and M5 remain open. Generated skill mirror and temporary adapter archive proof
remain planned for M5 and are not claimed by this review.

## Handoff

- Reviewed milestone: M3. `spec-review` assets
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Recommended next stage: review-resolution / implement M3 fix
- Final closeout readiness: not ready; M3, M4, M5, explain-change, verify, and PR handoff remain open.
- Automatic downstream handoff: none from this isolated code-review invocation.
