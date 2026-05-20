# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1. Spec Skill Readability
Reviewed artifact: commit `97730d4` (`M1: improve spec skill readability`)
Review date: 2026-05-20
Status: changes-requested
Recording status: recorded

## Scope

Reviewed the M1 implementation slice for `skills/spec/SKILL.md` against the
approved spec, active test spec, active plan, proof artifacts, and validation
evidence.

## Review inputs

- Diff: `git show --unified=80 -- skills/spec/SKILL.md scripts/test-skill-validator.py docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
- Plan: `docs/plans/2026-05-20-spec-family-readability-pass.md`
- Spec: `specs/spec-family-readability-pass.md`
- Test spec: `specs/spec-family-readability-pass.test.md`
- Preservation evidence: `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md`
- Parity evidence: `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
- Validation evidence: `docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`

## Diff summary

- `skills/spec/SKILL.md` tabulates required-section guidance.
- `skills/spec/SKILL.md` adds a `Closed enums` section for spec status and settlement result.
- The upstream settlement output skeleton and spec output skeleton reference enum placeholders instead of restating the full enum values.
- `scripts/test-skill-validator.py` updates the downstream status-settlement regression expectation from the exact inline settlement-result value list to only the `Settlement result:` field label.
- M1 preservation and parity evidence were added, and the plan state moved M1 to `review-requested`.

## Findings

### SFRP-M1-CR1 - Major: validation fixture weakens settlement-result coverage for unaffected skills

Finding ID: SFRP-M1-CR1
Severity: major
Location: `scripts/test-skill-validator.py`, `test_downstream_status_settlement_first_slice_skill_guidance`

Evidence:
The M1 diff changes the shared `common_required_terms` expectation from:

```text
Settlement result: updated | blocked | not-needed
```

to:

```text
Settlement result:
```

That shared list is applied to every skill in
`DOWNSTREAM_STATUS_SETTLEMENT_FIRST_SLICE_SKILLS`, not only `spec`.

Problem:
M1 is allowed to remove the duplicate inline settlement-result value list from
`skills/spec/SKILL.md` because `spec` now owns those values in an authoritative
`Closed enums` block. The same proof does not apply to the unaffected
`architecture` and `plan` skills. The updated fixture no longer verifies that
those unaffected skills still expose the settlement-result values, so the
regression test lost coverage outside the M1 skill surface.

Required outcome:
Keep the new `spec` enum-authority shape valid while preserving exact
settlement-result value coverage for unaffected first-slice skills.

Safe resolution path:
Adjust the regression fixture so:

- common expectations require the settlement-result field label;
- `spec`-specific expectations require `<settlement result>` and the
  authoritative settlement values in its `Closed enums` block;
- `architecture` and `plan` continue to require the existing inline value list,
  unless those skills are changed under their own approved milestone.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | `skills/spec/SKILL.md` changes align with `SFRP-R7`, `SFRP-R10` through `SFRP-R14`, and `SFRP-R19` through `SFRP-R23`; finding `SFRP-M1-CR1` concerns the validation fixture scope. |
| Test coverage | block | `scripts/test-skill-validator.py` was weakened for unaffected first-slice skills. |
| Edge cases | concern | `EC1` is covered for `spec`, but the validation fixture no longer protects duplicate/enum coverage for unaffected skills. |
| Error handling | pass | No runtime error-handling behavior is changed. |
| Architecture boundaries | pass | No architecture or ADR surface is touched. |
| Compatibility | concern | The skill text remains compatible; the validator coverage regression needs fixing before milestone closeout. |
| Security/privacy | pass | No secrets, credentials, external services, or private data flows are introduced. |
| Derived artifact currency | pass | M1 selected CI ran `skills.drift` and `adapters.drift`; full generated-output validation remains assigned to M3. |
| Unrelated changes | concern | The fixture change affects `architecture` and `plan` validation coverage beyond the `spec` skill. |
| Validation evidence | pass | M1 validation commands are recorded in `change.yaml`; selected CI passed after the fixture change, but the finding explains why that pass is insufficient. |

## Required review-resolution

Yes. `SFRP-M1-CR1` must be resolved before M1 can close or M2 can begin.

## Handoff

- Reviewed milestone: M1. Spec Skill Readability
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Recommended next stage: review-resolution / implement M1 fix
- Final closeout readiness: not ready
