# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `4455a6f` M1 canonical skill guidance and static proof
Reviewed milestone: M1
Status: changes-requested
Recording status: recorded

## Scope

This first-pass review covered M1 implementation for downstream status settlement before reliance: canonical `spec`, `architecture`, and `plan` skill guidance plus static validator coverage in `scripts/test-skill-validator.py`.

## Finding

### CR-001: Static proof and skill guidance omit required blocked-settlement and edit-permission semantics

Finding ID: CR-001
Severity: major
Location: `scripts/test-skill-validator.py` lines 1285-1328; `skills/spec/SKILL.md` lines 50-65; `skills/architecture/SKILL.md` lines 49-64; `skills/plan/SKILL.md` lines 65-80

Evidence: The approved test spec requires static proof that workflow-managed downstream execution does not ask whether edits are allowed, that missing status surfaces, unknown artifact types, unknown lifecycle fields, and unmapped next statuses block settlement, that blocked known-target settlement reports the intended target status, and that blocked unknown-target settlement reports `New status: not-applicable`. The new validator assertions only require broad terms such as `review-only`, `no-edit`, `not-applicable`, and `Settlement blocker`, and the skill text only says to block when evidence/status surface is missing or the ADR vocabulary is unknown. It does not explicitly preserve the R8 no-edit-question rule, the full R17/R23b/R23c blocked-target split, or the R24a known-target versus unknown-target blocker distinction across the first-slice skills.

Required outcome: M1 must make the approved settlement output and blocker semantics explicit enough for downstream agents and static validation to enforce the named edge cases in T4-T6.

Safe resolution path: Update the `spec`, `architecture`, and `plan` upstream status settlement sections to state that normal workflow-managed downstream execution does not ask whether edits are allowed; unknown artifact type, lifecycle field, or next status blocks instead of guessing; blocked known-target settlement reports the intended `New status`; blocked unknown-target settlement reports `New status: not-applicable`; and `Settlement blocker` distinguishes known-target evidence/state blockers from unknown-target mapping/vocabulary blockers. Tighten `scripts/test-skill-validator.py` to assert those phrases or equivalent precise contract terms for the first-slice skills.

## Checklist Coverage

- Spec alignment: block. `R8`, `R17`, `R17a`, `R23b`, `R23c`, and `R24a` are not fully represented in skill guidance/static proof.
- Test coverage: block. `T4`, `T5`, and `T6` name edge-case assertions that the added validator does not directly check.
- Edge cases: block. Unknown target, known target blocked by unresolved state, and no-edit-question behavior are under-specified.
- Error handling: concern. The guidance blocks broadly, but does not require the output distinction needed for safe blocked settlement.
- Architecture boundaries: pass. The change stays in canonical skill guidance and static proof; generated output remains M2.
- Compatibility: pass. Later-slice skills and formal review skills were not given operational settlement fields.
- Security/privacy: pass. No sensitive data or runtime values are introduced.
- Derived artifact currency: pass for M1. Generated outputs are intentionally deferred to M2.
- Unrelated changes: pass. Diff matches the active plan/source artifact scope.
- Validation evidence: concern. Commands passed, but the static assertions do not cover all approved named edge cases.

## Review Status

changes-requested

## Recommended Next Stage

review-resolution for `CR-001`, then implement the M1 fix and rerun code-review.
