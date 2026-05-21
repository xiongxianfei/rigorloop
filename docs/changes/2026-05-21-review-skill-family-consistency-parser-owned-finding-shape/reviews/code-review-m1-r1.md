# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: 365ba35c9c47970c722b3a60613dc126502567f6
Reviewed artifact: docs/plans/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md M1
Review date: 2026-05-21
Status: changes-requested
Recording status: recorded

## Scope

Reviewed M1 implementation commit `365ba35c9c47970c722b3a60613dc126502567f6` against the approved spec, active test spec, active execution plan, and recorded validation evidence.

## Review inputs

- Diff/review surface: `365ba35c9c47970c722b3a60613dc126502567f6`
- Governing spec: `specs/review-skill-family-consistency-parser-owned-finding-shape.md`
- Test spec: `specs/review-skill-family-consistency-parser-owned-finding-shape.test.md`
- Plan milestone: `docs/plans/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md` M1
- Validation evidence: M1 commands recorded in `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/change.yaml`
- Changed tests inspected: `scripts/test-skill-validator.py`, `scripts/test-review-artifact-validator.py`
- Changed validator inspected: `scripts/skill_validation.py`

## Result

- Review status: changes-requested
- Reviewed milestone: M1. Validator foundation and contract sufficiency assessment
- Material findings: RSF-M1-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/review-log.md`
- Review resolution: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/review-resolution.md`
- Open blockers: RSF-M1-CR1
- Immediate next stage: review-resolution M1
- Final closeout readiness: not-ready
- Stop condition: none; the finding is fixable within approved M1 scope

## Diff summary

M1 adds review-family asset validation checks in `scripts/skill_validation.py`, focused skill-validator coverage in `scripts/test-skill-validator.py`, review-artifact parser-owned identity fixture coverage in `scripts/test-review-artifact-validator.py`, skill-contract sufficiency evidence, and lifecycle state updates for the M1 implementation handoff.

## Material findings

### RSF-M1-CR1

Finding ID: RSF-M1-CR1
Severity: major
Location: `scripts/test-review-artifact-validator.py:726`
Evidence: `test_non_enum_severity_is_not_structure_validated` calls `replace_field(root / "reviews" / "code-review-r1.md", "Severity", "not-a-current-enum")` and then asserts the fixture passes. The referenced `valid-open-resolution` review fixture has no `Severity:` line in `reviews/code-review-r1.md`, and `replace_field` only rewrites an existing matching field. The test is therefore a no-op before validation and would still pass if the structure validator later started rejecting non-enum `Severity:` values. This does not prove the approved RSF-R20/RSF-R21 boundary or test-spec T4 step 5.
Required outcome: Make the non-enum severity proof construct an actual material-finding record containing `Severity: not-a-current-enum`, then assert structure validation still passes. The test must fail if structure validation begins rejecting non-enum severity values in this slice.
Safe resolution path: Update the fixture setup in `test_non_enum_severity_is_not_structure_validated` to insert or construct a `Severity: not-a-current-enum` field in a detailed material-finding record before calling `self.assertPasses(root)`. Rerun `python scripts/test-review-artifact-validator.py`, the M1 focused validation suite, review-artifact validation, lifecycle/metadata validation, and `git diff --check --`; then update the active plan and change metadata with the corrected evidence.

## Checklist coverage

| Checklist item | Verdict | Evidence |
|---|---|---|
| Spec alignment | concern | M1 preserves the no-severity-enum-validation intent in implementation shape, but the direct proof for that boundary is ineffective. |
| Test coverage | block | `test_non_enum_severity_is_not_structure_validated` does not actually exercise a non-enum `Severity:` field. |
| Edge cases | concern | Parser-owned `Finding ID:` identity defects are covered, but the named non-goal edge case for severity-enum validation lacks direct proof. |
| Error handling | pass | The changed skill validator raises deterministic `SkillValidationError` failures for malformed review-family assets and resource maps. |
| Architecture boundaries | pass | M1 stays within validators/tests/lifecycle evidence and does not introduce runtime architecture or adapter install-root changes. |
| Compatibility | pass | No review-skill behavior or parser contract is changed in M1. |
| Security/privacy | pass | The diff does not introduce secrets, external services, auth behavior, or sensitive logging. |
| Derived artifact currency | pass | M1 does not touch generated adapter output; generated-output proof is reserved for M5. |
| Unrelated changes | pass | The diff is scoped to lifecycle artifacts plus M1 validator/test changes. |
| Validation evidence | concern | The recorded M1 validation commands passed, but one named proof is vacuous and must be corrected before M1 can close. |

## Recommendation

Request M1 review-resolution for RSF-M1-CR1. Do not start M2 until the non-enum severity proof is corrected and M1 is returned for code-review.
