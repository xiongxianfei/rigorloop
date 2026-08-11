# M2 Skill Refactor Evidence

Milestone: M2
Date: 2026-08-10
Status: implementation-complete; review pending

## Implemented package boundary

- `SKILL.md` retains direct and isolated review authority, evidence selection,
  checklist, statuses, severity, material-finding requirements, recording,
  direct proof and rereview, stops, claim limits, milestone routing, the compact
  boundary bridge, resource triggers, and asset-owned output instructions.
- `references/workflow-managed-automated-review.md` owns only the armed
  automation phases: neutral packet, blind-first risk map, evidence challenge,
  requirement fidelity, correction classification, bounded correction,
  receipts, promotion, pause, and failure procedure.
- The automation reference is mapped once with the exact trigger “only when the
  invocation is a formally armed workflow-managed automated review or
  correction loop.”
- The result and material-finding assets remain the sole full copy-and-fill
  structures. No target-agent runtime, prompt, transcript, selector, scheduler,
  or permanent size gate was added.

## Focused proof

| Command | Result |
| --- | --- |
| `python scripts/validate-skills.py skills/code-review/SKILL.md` | pass; one canonical skill validated |
| `python scripts/test-skill-validator.py` | pass; 290 tests, 16 governed skips |
| `python scripts/build-skills.py --check` | pass; temporary generated skill tree validated |
| `git diff --check` | pass |

The focused regression suite now reads automation-only requirements from the
mapped reference, checks the exact load trigger, rejects universal policy in
that reference, confirms universal headings remain inline, and confirms output
structure remains asset-owned. The legacy review-family validator allowlist was
narrowly extended for this one approved code-review reference; unrelated
review-family packaged resources remain rejected.

## Interim measurements

| Metric | Before | After M2 | Change |
| --- | ---: | ---: | ---: |
| `SKILL.md` lines | 518 | 355 | -31.5% |
| `SKILL.md` words | 4514 | 2647 | -41.4% |
| `SKILL.md` estimated tokens | 8160 | 4813 | -41.0% |
| Conditional-reference words | 0 | 886 | +886 |
| Conditional-reference estimated tokens | 0 | 1749 | +1749 |
| Total package words | 5569 | 4588 | -17.6% |
| Total package estimated tokens | 10116 | 8519 | -15.8% |
| Mapped resources | 3 | 4 | +1 |

The non-normative 35–45 percent common-path target is met by words and estimated
tokens. Package totals also fall because duplicated automation and full inline
output structure were removed rather than merely relocated. M3 owns the final
repeatable measurement and generated/installed parity evidence.

## Handoff

M2 is ready for independent code review. This evidence does not claim package
parity across adapters, final semantic preservation, or verify readiness.
