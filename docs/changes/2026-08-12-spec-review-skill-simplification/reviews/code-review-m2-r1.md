# Spec-Review Skill Simplification Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation commit `8ebe9ba5`
Reviewed milestone: M2
Review date: 2026-08-12
Status: changes-requested
Review status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: SRSS-CR-M2-R1-001
- Recording status: recorded
- Open blockers: governed-reference load and recording order are circular for automated review
- Immediate next stage: review-resolution
- Automatic downstream handoff: bounded correction and rereview only
- Verify readiness: not-claimed

## Finding SRSS-CR-M2-R1-001

- Finding ID: SRSS-CR-M2-R1-001
- Severity: major
- Location: `skills/spec-review/SKILL.md` Resource map and `references/governed-spec-review-settlement.md` load condition
- Evidence: The reference owns workflow-managed context reset, manifest evidence, and automation pause procedure, but both the map and reference required universal recording to succeed before the reference loaded. Automated review needs those procedures before review judgment and recording. R14 and R23 require loading after `governed-spec-entry` authority; R25 requires only settlement to wait for recording.
- Required outcome: Load the governed reference after exact governed authority is established, while keeping matching-entry settlement gated on successful universal recording.
- Safe resolution path: Change the map and reference preamble to the R14/R23 condition, add an explicit settlement precondition, update the coupled contract wording and focused assertion, then rerun CMD2-CMD5 and context-reset review.
- Auto-fix class: declared-safe
- Declared-safe boundary: the named load-condition and settlement-precondition wording, coupled contract sentence, and focused test only
- Required validation: CMD2, CMD3, CMD4, CMD5

## Handoff

M2 remains review-requested. The bounded correction may run because the finding has a deterministic spec-derived recipe and no owner decision.
