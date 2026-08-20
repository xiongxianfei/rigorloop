# Code Review M2 R1: Compact Contract

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation milestone M2 range `204e9689..627aea9b`
Reviewed milestone: M2
Reviewed artifact: commit `627aea9b`
Review date: 2026-08-20
Status: changes-requested
Material findings: BUGSIM-CR1
Recording status: recorded

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: 1
- Recording status: recorded
- Review resolution: required
- Milestone closeout: open
- Next stage: implement M2 correction, then code-review rereview
- Verify readiness: not-claimed

## Blind-first risk map

The main risks were loss of closed vocabulary during compression, action rows that cannot represent a terminal diagnosis, abbreviated phases that drift from the approved state machine, incomplete command-side-effect stops, and output claims that omit required identities. The review compared the actual M2 diff directly with R2-R25 before relying on implementation evidence.

## BUGSIM-CR1 — Major: the compact contract omits approved closed values and required result behavior

### Evidence

The canonical skill's cause set omits `integration-mismatch`, `data-or-migration`, and `race-or-timing` required by R14. Its action set omits `complete-diagnosis` required by R15. The phase list says `validation` rather than the exact `post-fix-validation` state required by R10. It also does not explicitly require unexpected command mutations to stop and be reported as R6 requires, and `Expected output` delegates to an undefined “completion record” rather than enumerating the R24 result fields.

The focused tests assert only subsets of the cause/action sets, so they pass despite this contract drift.

### Required outcome

Restore every omitted closed value and exact phase name, state the unexpected-mutation stop, enumerate the required R24 result fields, and make focused tests reject these omissions. Preserve the one-file package and strict reductions in both words and bytes.

### Safe resolution

Apply a bounded correction to `skills/bugfix/SKILL.md` and `BugfixSkillSimplificationTests`, update M2 evidence, rerun the complete M2 command set, and rereview the corrected milestone.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | R6, R10, R14, R15, and R24 are incomplete. |
| Test coverage | block | Subset-presence assertions do not prove exact cause/action vocabularies. |
| Package boundary | pass | The package remains one file with no new machinery. |
| Authority and proof gates | pass | Operation, authority, governed signals, and proof-before-correction are explicit. |
| Handoff and ownership | pass with correction | Code-review routing is bounded, but result fields need closure. |
| Validation | pass but insufficient | Commands pass because focused assertions omit the missing contract values. |

## Claim limitations

This review does not close M2 or establish M3, final review, verification, CI, branch, or PR readiness.
