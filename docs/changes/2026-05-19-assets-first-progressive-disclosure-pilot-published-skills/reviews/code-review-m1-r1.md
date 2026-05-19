# Code Review M1 R1: Assets-First Progressive Disclosure Pilot

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit e70545d6c3e75cd33d8b0d5437f9ca88d0363a85
Status: changes-requested
Reviewed artifact: M1. Asset Contract Validation And Test Spec Support
Review date: 2026-05-19
Recording status: recorded

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: APD-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-log.md
- Review resolution: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-resolution.md
- Open blockers: APD-CR1
- Immediate next stage: review-resolution for M1

## Review inputs

- Diff/review surface: commit `e70545d6c3e75cd33d8b0d5437f9ca88d0363a85` (`M1: validate plan asset contract`).
- Tracked governing branch state: proposal, spec amendment, test-spec amendment, active plan, change metadata, and M1 commit are tracked in the reviewed commit.
- Governing artifacts: `specs/skill-contract.md` R37-R45, `specs/skill-contract.test.md` T33-T34, and `docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md` M1.
- Validation evidence: M1 commit message and active plan validation notes record `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, change-metadata validation, artifact lifecycle validation, `git diff --check`, and selected CI as passing after implementation.

## Diff summary

M1 adds scoped validation helpers in `scripts/skill_validation.py` for the `plan` asset pilot, including exact approved asset inventory, metadata, normative status, structural fingerprints, visible placeholders, forbidden repository-root required dependencies, literal `COPY` entries, fields-to-fill wording, no-unfilled-placeholder guidance, and `plan-skeleton.md` section-set parity. It adds positive and negative fixture coverage under `tests/fixtures/skills/published-design/` and new assertions in `scripts/test-skill-validator.py`. It also records the approved proposal/spec/test-spec/plan/change-local lifecycle packet and moves M1 to `review-requested`.

## Findings

### APD-CR1 - Missing direct fixture proof for plan asset resource-map omissions

Finding ID: APD-CR1
Severity: major
Location: `scripts/test-skill-validator.py`, plan asset tests; `tests/fixtures/skills/published-design/`.
Evidence: T34 requires validator fixtures to fail for a "missing resource-map entry" for the assets-first plan pilot, and the M1 plan repeats that failing fixtures should cover "missing resource-map entries." The added plan-asset tests cover valid assets, exact asset count, missing metadata, non-normative status, non-`COPY`, missing fields, missing placeholder, forbidden root dependency, fingerprint mismatch, and section-set mismatch, but there is no plan-asset fixture/test where all four assets exist and one `Resource map` entry is omitted.
Required outcome: M1 must include direct plan-asset regression proof for an omitted asset resource-map entry, not only nearby generic packaged-resource coverage.
Safe resolution path: Add a fixture such as `tests/fixtures/skills/published-design/plan-assets-missing-resource-map-entry/` with the approved four asset files but an omitted `Resource map` entry for one asset. Add a matching `scripts/test-skill-validator.py` assertion that fails with `Resource map must name packaged resource 'assets/<asset>.md'` or an equivalent plan-asset-specific error. Rerun the M1 validation commands and update the active plan/change metadata evidence.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | The implementation aligns with R37-R39 and R42-R43 for most deterministic checks, but APD-CR1 leaves one T34/M1 named proof case uncovered. |
| Test coverage | block | `scripts/test-skill-validator.py` lacks a plan-asset missing resource-map-entry fixture/test required by T34 and the M1 plan. |
| Edge cases | block | EC30 includes resource-map omissions; the direct plan-asset proof is absent. |
| Error handling | pass | Invalid metadata, status, `COPY`, fields, placeholders, root dependencies, fingerprints, and section sets have negative fixtures. |
| Architecture boundaries | pass | The change is scoped to static validator/test fixtures and does not alter adapter roots, lockfiles, CLI behavior, or real `skills/plan` assets in M1. |
| Compatibility | pass | `_validate_plan_asset_pilot` only activates for `name: plan` with an `assets/` directory, so flat canonical `skills/plan/SKILL.md` remains valid before M2. |
| Security/privacy | pass | Added checks reject required repository-root dependencies in assets; no secret-bearing surfaces were introduced in reviewed code or fixtures. |
| Derived artifact currency | pass | M1 does not generate or hand-edit public adapter outputs; generated-asset proof is deferred to M3 by plan. |
| Unrelated changes | pass | The reviewed commit contains the lifecycle packet for this initiative and the M1 validator/test slice; no unrelated skill bodies were modified. |
| Validation evidence | concern | Reported commands are relevant and credible, but the missing fixture means the validation set is incomplete for T34. |

## No-finding rationale

Not applicable. APD-CR1 requires a targeted fix before M1 can close.

## Residual risks

After APD-CR1 is fixed, re-review should confirm the new omission fixture exercises the plan asset path specifically and does not rely only on the pre-existing generic `references/detail.md` resource-map test.

## Milestone handoff

- Reviewed milestone: M1. Asset Contract Validation And Test Spec Support
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for APD-CR1
- Remaining implementation milestones: M1, M2, M3
- Next stage: review-resolution for M1
- Final closeout readiness: not ready; M1 has an open code-review finding and M2/M3 remain unimplemented.
