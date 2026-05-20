# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2. Spec-Review Skill Readability
Reviewed artifact: commit `3e8ae53` (`M2: improve spec-review skill readability`)
Review date: 2026-05-20
Status: changes-requested
Recording status: recorded

## Scope

Reviewed the M2 implementation slice for `skills/spec-review/SKILL.md`
against the approved spec, active test spec, active plan, proof artifacts, and
validation evidence.

## Review inputs

- Diff: `git show --unified=80 -- skills/spec-review/SKILL.md docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md docs/changes/2026-05-20-spec-family-readability-pass/change.yaml docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md`
- Baseline skill text: `git show HEAD^:skills/spec-review/SKILL.md`
- Plan: `docs/plans/2026-05-20-spec-family-readability-pass.md`
- Spec: `specs/spec-family-readability-pass.md`
- Test spec: `specs/spec-family-readability-pass.test.md`
- Preservation evidence: `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md`
- Parity evidence: `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
- Validation evidence: `docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`

## Diff summary

- `skills/spec-review/SKILL.md` replaces the prose review-dimension sentence
  with a table and a `<review dimension verdict>` placeholder.
- `skills/spec-review/SKILL.md` adds a `Closed enums` section with the
  review-dimension verdict values `pass`, `concern`, and `block`.
- M2 preservation and behavior-parity evidence were added.
- The active plan and plan index moved M2 to `review-requested`.

## Findings

### SFRP-M2-CR1 - Major: review-focus cells introduce unproven guidance beyond the baseline prose

Finding ID: SFRP-M2-CR1
Severity: major
Location: `skills/spec-review/SKILL.md`, `## Review dimensions`, lines 52-63

Evidence:
The baseline M2 source listed the review dimensions and verdict values in one
sentence:

```text
Evaluate each with `pass`, `concern`, or `block`: requirement clarity,
normative language, completeness, testability, examples, compatibility,
observability, security/privacy, non-goals, and acceptance criteria.
```

It then preserved one separate coverage sentence for normal, empty, boundary,
error, permission, migration, rollout, rollback, old-client, old-data behavior,
and observable acceptance.

The M2 edit adds new review-focus text for each dimension, including examples
not present in the baseline text, such as:

```text
Whether logs, metrics, traces, audit events, or user-visible status are
specified when relevant.
```

and:

```text
Whether auth, authorization, secrets, data exposure, abuse cases, or privacy
behavior are covered when relevant.
```

Problem:
The approved spec requires M2 to be presentation-only. `SFRP-R2` requires every
existing rule and output obligation to be preserved, and `SFRP-R8` requires the
review-dimension guidance table to preserve the same dimensions and verdict
guidance. The active test spec's `T6` requires comparing every dimension and
guidance point against its source. The new focus cells may be reasonable review
guidance, but they are not a source-preserving tabulation of the existing M2
text. They can be read as new or more specific review obligations.

Required outcome:
Revise M2 so the `spec-review` table preserves only the existing dimension
names and verdict guidance, or route an explicit spec/owner change if the
project wants to add richer review-focus definitions as behavior.

Safe resolution path:
Keep the `Closed enums` block for `Review dimension verdict`, but make the
review-dimension table a pure presentation rewrite. For example:

- table the 10 baseline dimension names in the same order;
- use a `Verdict` column containing `<review dimension verdict>`, or use a
  similarly non-expanding authority surface;
- keep the existing coverage sentence verbatim after the table;
- remove review-focus examples that are not present in the baseline text; and
- update the preservation and parity evidence to match the narrower table.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `SFRP-R2` and `SFRP-R8` require preservation; the new review-focus cells add unproven guidance beyond the baseline dimension list. |
| Test coverage | block | `T6` requires comparing every dimension and guidance point against its source; the preservation matrix asserts preservation but the added focus examples are not source-mapped. |
| Edge cases | concern | `EC4` says awkward table rewording that could change meaning must preserve source wording or defer the row; M2 chose richer wording without a recorded exception. |
| Error handling | pass | No runtime error-handling behavior is changed. |
| Architecture boundaries | pass | No architecture or ADR surface is changed. |
| Compatibility | concern | Published `spec-review` skill behavior may become stricter or more specific for observability and security/privacy review dimensions. |
| Security/privacy | concern | The diff adds security/privacy-specific review examples not present in baseline; no secrets or unsafe data are introduced. |
| Derived artifact currency | pass | Selected CI included `skills.drift` and `adapters.drift`; full generated-output validation remains assigned to M3. |
| Unrelated changes | pass | The touched files are in the M2 implementation, proof, validation, and plan surfaces. |
| Validation evidence | pass | M2 validation commands are recorded in `change.yaml`, including direct skill validation, lifecycle validation, diff check, and selected CI. |

## Required review-resolution

Yes. `SFRP-M2-CR1` must be resolved before M2 can close or M3 can begin.

## Handoff

- Reviewed milestone: M2. Spec-Review Skill Readability
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Recommended next stage: review-resolution / implement M2 fix
- Final closeout readiness: not ready
