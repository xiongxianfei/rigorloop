# Skill Readability and Self-Containment Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M3. Cold-read, behavior parity, token comparison, and rollout handoff
Reviewed artifact: commit `4df4d42` (`M3: record skill readability pilot evidence`)
Review date: 2026-05-18
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Status: complete
- Review status: changes-requested
- Material findings: SRSC-M3-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-18-skill-readability-self-containment/reviews/code-review-m3-r1.md
- Review log: docs/changes/2026-05-18-skill-readability-self-containment/review-log.md
- Review resolution: docs/changes/2026-05-18-skill-readability-self-containment/review-resolution.md
- Artifacts changed: review record, review log, review resolution, plan body, change metadata
- Open blockers: SRSC-M3-CR1
- Next stage: review-resolution for SRSC-M3-CR1, then implement M3 fix and rerun code-review
- Reviewed milestone: M3. Cold-read, behavior parity, token comparison, and rollout handoff
- Review status: changes-requested
- Milestone closeout: M3 resolution-needed
- Remaining implementation milestones: M3
- Required review-resolution: yes
- Finding IDs: SRSC-M3-CR1
- Verify readiness: not ready; M3 has an open material finding

## Review Inputs

- Diff/review surface: commit `4df4d42`, `git show --stat --oneline HEAD`, `git show --name-only --format=fuller HEAD`, focused reads of the M3 evidence reports, token report, active plan, and pilot skill files.
- Tracked governing branch state: approved spec, active test spec, active plan, change metadata, M3 evidence reports, and reviewed implementation commit are tracked on branch `proposal/2026-05-18-skill-readability-self-containment`.
- Governing artifacts:
  - `specs/skill-readability-contract.md`
  - `specs/skill-readability-contract.test.md`
  - `docs/plans/2026-05-18-skill-readability-self-containment.md`
  - `docs/changes/2026-05-18-skill-readability-self-containment/cold-read-report.md`
  - `docs/changes/2026-05-18-skill-readability-self-containment/behavior-parity-report.md`
  - `docs/reports/token-cost/skills/2026-05-18-skill-readability-self-containment.md`
- Validation evidence rerun during review:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-18-skill-readability-self-containment.md --path docs/plan.md --path specs/skill-readability-contract.md --path specs/skill-readability-contract.test.md --path docs/changes/2026-05-18-skill-readability-self-containment/change.yaml --path docs/changes/2026-05-18-skill-readability-self-containment/review-log.md --path docs/changes/2026-05-18-skill-readability-self-containment/review-resolution.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-18-skill-readability-self-containment`
  - `git diff --check --`

## Diff Summary

M3 records cold-read evidence against installed Codex adapter output, behavior-parity evidence against the baseline pilot skills, after-change token comparison for `proposal` and `proposal-review`, and plan/change metadata handoff state for M3 code-review. It also reduces the pilot skill wording enough to keep both pilot skills within the approved +5% token tolerance.

## Findings

### SRSC-M3-CR1 - Major - Closed enum values are still restated after authoritative enum blocks

Finding ID: SRSC-M3-CR1
Severity: major
Location: `skills/proposal/SKILL.md:150`, `skills/proposal/SKILL.md:160`, `skills/proposal/SKILL.md:195`, `skills/proposal/SKILL.md:217`, `skills/proposal-review/SKILL.md:136`, `skills/proposal-review/SKILL.md:146`

Evidence: The approved spec requires "Every closed enum used by a rewritten skill MUST appear in a fenced block or table exactly once in that skill" and "A rewritten skill MUST NOT restate the same closed enum values in multiple prose locations" (`R16`, `R17`). The current pilot skills still restate enum values after their authoritative fenced blocks:

- `proposal` defines `Closed enum: initial goal treatment` at line 150, then repeats the same five values as a bullet list at lines 160-166.
- `proposal` defines `Closed enum: scope budget treatment` at line 195, then repeats the same seven values as the "Allowed treatments" list at lines 217-225.
- `proposal-review` defines `Closed enum: initial goal treatment` at line 136, then repeats the same five values as a bullet list at lines 146-152.

The validator passes, but this is a direct manual contract miss for the duplicate-enum edge that M3 is supposed to leave ready for rollout.

Required outcome: Each affected closed enum value set must appear exactly once per skill. Subsequent instructions should reference the authoritative enum by name or use placeholder wording such as `<one initial goal treatment value>` without restating every value.

Safe resolution path: In `skills/proposal/SKILL.md`, replace the repeated initial-goal bullet list with a sentence that references the `initial goal treatment` enum, and remove or rewrite the repeated `Allowed treatments` list so it points to the `scope budget treatment` enum instead of listing values again. In `skills/proposal-review/SKILL.md`, replace the repeated initial-goal bullet list with a sentence that references the `initial goal treatment` enum. Rerun `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/measure-skill-tokens.py`, lifecycle/change metadata validation, and M3 code-review.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | M3 evidence covers R41-R53 and token thresholds, but the current pilot skill text violates R16/R17 by repeating closed enum values after authoritative blocks. |
| Test coverage | concern | `python scripts/test-skill-validator.py` passed 97 tests, but the static check does not catch the duplicated canonical values in the pilot skills. Manual review caught SRSC-M3-CR1. |
| Edge cases | block | The named edge case "Closed enum appears in output skeleton" is fine, but the broader R16/R17 duplicate-enum contract is not satisfied for initial goal and scope budget enums. |
| Error handling | pass | No runtime error handling changes are introduced; unresolved cold-read references and token hard-cap breaches are recorded as stop conditions. |
| Architecture boundaries | pass | No build-time partials, include mechanism, adapter package format, manifest format, release archive contract, or generated-output hand-editing change appears in the diff. |
| Compatibility | pass | Front matter remains the already-validated `version: "1.0.0"` and `schema-version: skill-readability-v1`; adapter output validation evidence remains unchanged. |
| Security/privacy | pass | M3 evidence uses synthetic/public-safe text and temporary adapter output paths; no secrets or private runtime values are introduced. |
| Derived artifact currency | pass | M3 records temporary adapter build/validation and cold-read installed output paths; no generated adapter body is tracked or hand-edited. |
| Unrelated changes | pass | The M3 commit is limited to pilot skill token reductions, M3 evidence, plan/index state, token report, and change metadata. |
| Validation evidence | concern | Rerun commands passed, including validator, skill validation, token measurement, lifecycle, metadata, review-artifact validation, and diff check; the material issue is a manual contract gap not covered by current automation. |

## No-Finding Rationale

Not applicable. SRSC-M3-CR1 requires a fix before M3 can close.

## Residual Risks

- The duplicate-enum validator does not yet catch this exact pilot-skill pattern. The immediate requirement is to fix the pilot text; extending automation can be considered during follow-on rollout if the team wants stronger guardrails.

## Recommended Next Stage

Enter `review-resolution` for SRSC-M3-CR1, keep M3 in `resolution-needed`, apply the targeted enum-reference fix, then return M3 to `code-review`.
