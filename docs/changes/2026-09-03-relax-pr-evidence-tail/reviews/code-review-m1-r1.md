# Code Review M1 R1: Proportional PR evidence suffix

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: commit 6d2be4e2
Reviewed artifact: M1 implementation commit 6d2be4e2
Reviewed milestone: M1
Review date: 2026-09-03
Status: changes-requested
Review status: changes-requested
Material findings: PRTAIL-M1-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-03-relax-pr-evidence-tail/reviews/code-review-m1-r1.md`, `docs/changes/2026-09-03-relax-pr-evidence-tail/review-log.md`, and `docs/changes/2026-09-03-relax-pr-evidence-tail/review-resolution.md`
- Open blockers: PRTAIL-M1-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: PRTAIL-M1-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-03-relax-pr-evidence-tail/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-09-03-relax-pr-evidence-tail/review-log.md`
- Review resolution: `docs/changes/2026-09-03-relax-pr-evidence-tail/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2
- Required review-resolution: yes
- Finding IDs: PRTAIL-M1-CR1
- Verify readiness: not-claimed

## Review inputs

- Actual diff: commit `6d2be4e2` against its first parent, bounded to the M1 skill, reference, test, and evidence files.
- Approved Design package: `design-review-r1`, with the exact architecture and focused specification current and authoritative.
- Approved Delivery package: `delivery-review-r2`, with M1 allocated to the proportional canonical contract and preservation of unaffected prior PR requirements.
- Current milestone: M1 is `review-requested`; M2 remains planned.
- Direct proof: 364 skill-validator tests, canonical skill validation, temporary generated-skill validation, focused boundary validation, package-size measurement, and whitespace validation all pass.

## Actual-diff summary

M1 correctly replaces the direct-child topology proxy with a closed cumulative suffix classification, constrains evidence-only acceptance to current attributable evidence, preserves the narrower Verify-result pair, and adds negative contract tests. The same edit also compresses text outside the superseded tail clauses.

## Finding PRTAIL-M1-CR1

Finding ID: PRTAIL-M1-CR1
Severity: major
Location: `skills/pr/SKILL.md:30`, `skills/pr/SKILL.md:61`, `skills/pr/SKILL.md:83`, `skills/pr/SKILL.md:87`, and `skills/pr/SKILL.md:106`
Evidence: The focused specification supersedes only the one-commit/direct-child clauses and requires every other retry, body, result, authority, and claim requirement to remain current. M1 removed the explicit malformed/stale/conflicting/duplicated/unsafe/escaped governed-signal partition, reduced R37 from retry state reconciliation to duplicate avoidance, removed R4's statement that procedure owns body applicability and adequacy, collapsed R40's exact `pr-body-ready`/`pr-open-ready` and post-read-back URL outputs into generic “readiness” and “URL,” and weakened “current owning evidence” to “owning evidence.” Passing literal tests do not prove those retained semantic properties.
Required outcome: Restore the unaffected governed-signal, retry-reconciliation, body-policy ownership, exact result-field, and current-owning-evidence clauses while retaining the proportional suffix rule and existing package-size contract.
Safe resolution path: Accept this finding, route M1 to Implementation, add exact preservation assertions before correction, restore the affected clauses with only semantically neutral compaction elsewhere, rerun every M1 command and package-size check, update M1 evidence, and return the same milestone for Code Review R2.
needs-decision rationale: none; the approved focused specification and prior PR contract already determine the required outcome.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | The proportional suffix satisfies the focused delta, but PRTAIL-M1-CR1 violates its explicit unchanged-contract boundary and AC-PRTAIL-009. |
| Test coverage | concern | Tail classifications and negatives are covered; retained R4, R6, R37, R40, and current-evidence wording lack exact preservation assertions. |
| Edge cases | concern | Retry after concurrent remote or PR change is no longer explicitly required to reconcile rather than replay. |
| Error handling | concern | Invalid governed-signal categories are no longer enumerated at their routing decision. |
| Architecture boundaries | pass | PR remains read-only, Verify owns branch readiness, and the registered Verify result remains exact. |
| Compatibility | concern | Unaffected public PR semantics were compressed despite being outside the approved supersession. |
| Security/privacy | pass | Secret checks, exact identities, and no-force behavior remain explicit. |
| Derived artifact currency | pass | Temporary generation validates canonical M1; tracked adapter candidate parity remains allocated to M2. |
| Unrelated changes | concern | The semantic compression is outside the approved tail-rule scope. |
| Validation evidence | concern | All selected commands pass, but current assertions allow the retained-contract regressions. |

## No automatic downstream handoff

M1 remains open. PRTAIL-M1-CR1 must be dispositioned, corrected, and independently rereviewed before M2 begins. No owner decision is required.
