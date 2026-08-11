# Test-Spec-Review Skill Simplification Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: M1 commit `27942a64`
Reviewed artifact: commit `27942a64`
Reviewed milestone: M1
Review date: 2026-08-11
Status: changes-requested
Review status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: review record, invocation manifest, review log, and review resolution
- Open blockers: TSRSIM-CR-M1-R1-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: TSRSIM-CR-M1-R1-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-11-test-spec-review-skill-simplification/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-11-test-spec-review-skill-simplification/review-log.md`
- Review resolution: required before fixing
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: TSRSIM-CR-M1-R1-001
- Verify readiness: not-claimed

## Review boundary and risk map

The blind-first review inspected `9b0cd7d4..27942a64` before using CMD1 results. Highest-impact risks were omitted universal rules, semantic/literal conflation, open closed vocabularies, incomplete scenarios, and premature package movement. Direct inspection covered the complete 359-line baseline skill, all ledger rows, all scenarios and negative fixtures, exact validator consumers, hashes, and the actual diff. M2 package behavior and M3 distribution parity were intentionally out of scope.

## Finding TSRSIM-CR-M1-R1-001

Finding ID: TSRSIM-CR-M1-R1-001
Severity: major
Location: `docs/changes/2026-08-11-test-spec-review-skill-simplification/test-spec-review-rule-disposition.yaml`; baseline `skills/test-spec-review/SKILL.md:162-182`
Evidence: The baseline owns a behaviorally significant `Generated Markdown readability` contract governing semantic source lines, stable IDs, tables, proof-bearing commands, diagrams, and manual-proof boundaries. None of the 18 semantic rows owns or disposes that section, while R25 requires every behaviorally significant current rule to have exactly one disposition. CMD1 validates row shape but cannot detect a missing baseline rule.
Required outcome: Add one stable semantic row for generated Markdown readability with its baseline source, applicable assemblies, retained-inline destination, governing requirements, and direct preservation proof; update the M1 evidence count and audit statement.
Safe resolution path: Add `TSR-RULE-READABILITY-001` to the rule ledger, retain the rule inline for all four assemblies, update the count from 18 to 19, rerun exact CMD1 and lifecycle validation, and rereview the correction. Do not change the canonical skill package.
needs-decision rationale: none
Auto fix class: mechanical. Allowed paths are the M1 semantic ledger and M1 preservation evidence; authority is R25 and the exact baseline section; validation is CMD1, metadata validation, unchanged-package check, and rereview.

## Requirement-fidelity receipt

| Area | Result | Evidence |
| --- | --- | --- |
| R25 complete semantic disposition | fail | One baseline behavior section has no ledger owner. |
| R26-R28 closed values and literals | pass | Unknown fixtures fail first; literal inventory is separate. |
| R29-R30 measurements | pass | Canonical LF-normalized resources and assemblies are reported separately. |
| M1 ordering | pass | No canonical skill or validator file changed. |

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | R25 completeness is not satisfied. |
| Test coverage | concern | CMD1 proves present rows but cannot detect the omitted baseline rule. |
| Edge cases and recovery | pass | Sixteen required scenarios and two unknown-value negatives are present. |
| Error handling | pass | Unknown closed values are rejected before dependent checks. |
| Architecture boundaries | pass | M1 changes only change-local evidence. |
| Compatibility | pass | Exact consumers are separated from semantic ownership. |
| Security/privacy | pass | Repository-local reads only; no runtime, network, or credentials. |
| Derived artifact currency | pass | Canonical and generated packages are untouched. |
| Unrelated changes | pass | Diff is confined to the approved M1 evidence surface. |
| Validation evidence | concern | Named commands pass, but the semantic audit missed one section. |

## Handoff

M1 remains open and requires review-resolution plus the bounded mechanical correction. No downstream milestone or final readiness is authorized.
