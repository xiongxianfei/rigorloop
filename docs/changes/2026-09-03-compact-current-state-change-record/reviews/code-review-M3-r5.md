# Code Review M3 R5: Exact operation eligibility

Review ID: code-review-m3-r5
Stage: code-review
Round: r5
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: M3 compact semantic-operation and bounded CLI implementation against Design Review R9 and Delivery Review R6
Reviewed milestone: M3
Review date: 2026-09-04
Status: changes-requested
Review status: changes-requested
Material findings: CCSR-M3-CR6
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Open blockers: CCSR-M3-CR6
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CCSR-M3-CR6
- Recording status: recorded
- Review record: `reviews/code-review-M3-r5.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CCSR-M3-CR6
- Verify readiness: not-claimed

## Finding CCSR-M3-CR6

- Finding ID: CCSR-M3-CR6
- Severity: major
- Location: `packages/rigorloop/dist/lib/compact-eligibility.js:35-49`, `packages/rigorloop/dist/lib/compact-eligibility.js:93-115`, and `packages/rigorloop/dist/lib/compact-eligibility.js:138-140`
- Evidence: The R4 corrections close non-loss, expected-file, stable-registration, final-Verify, and tested target gaps, but the approved fourteen-operation matrix is still only partially encoded. `advance-stage` structurally rejects `implement → code-review` whenever an active milestone exists, although that active milestone selects the Code Review handoff. Conversely, `replace-review` and `settle-review` may target any review while the current stage is any review gate, without proving that target kind and reviewer responsibility are due at that gate. `upsert-decision` becomes structurally eligible at any stage once one decision exists, rather than only review-resolution or the responsible stage, and `invalidate-evidence` does not prove that every selection is a current entry or a directly observed drift source. These are direct untested violations of the Design R9 operation eligibility matrix and can either block a valid workflow or admit an ineligible mutation.
- Required outcome: Derive exact stage, active-work, target-kind, reviewer-responsibility, decision-owner/source, and evidence-invalidation predicates for every operation; admit the normal active-milestone authoring-to-review handoff; reject wrong-gate review replacement/settlement, wrong-stage decision mutation, and invalid evidence selections; and prove the positive and negative partitions with table-driven tests.
- Safe resolution path: Add failing matrix vectors first, centralize target-stage derivation, make structural eligibility conservative when no exact request is supplied, enforce exact request predicates without treating overall progression as permission, and rerun focused plus package validation before a fresh holistic M3 review.
- needs-decision rationale: none; Specification lines 259-280 and TG-09 through TG-13 already define the required behavior.

## Checklist

| Area | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Several approved operation predicates remain absent or contradictory. |
| Test coverage | block | The 20-test focused suite omits wrong-gate review, active-milestone handoff, decision responsibility, and invalidation-source partitions. |
| Non-loss and bounded input | pass | R4 sibling non-loss and exact expected-file findings are corrected with direct tests. |
| Verify coupling | pass | Final review, evidence basis, remaining work, report path, and observed subjects are directly checked. |
| Compatibility and trust boundary | pass | Legacy writes remain denied and no caller permission, Git, PR, network, or log dependency was introduced. |
| Validation evidence | concern | All named commands pass, but they do not prove the missing matrix partitions. |

## Handoff

M3 remains under review. Resolve and route CCSR-M3-CR6 to implementation, correct the exact matrix, and perform Code Review M3 R6. No milestone, Verify, or PR readiness is claimed.
