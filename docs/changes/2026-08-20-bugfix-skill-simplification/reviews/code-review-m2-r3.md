# Code Review M2 R3: Truthful Complete Contract

Review ID: code-review-m2-r3
Stage: code-review
Round: r3
Reviewer: Codex independent code-review context
Target: corrected implementation milestone M2 range `204e9689..bda11b3b`
Reviewed milestone: M2
Reviewed artifact: commit `bda11b3b`
Review date: 2026-08-20
Status: changes-requested
Material findings: BUGSIM-CR3
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, invocation manifest, and review log
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BUGSIM-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-20-bugfix-skill-simplification/reviews/code-review-m2-r3.md`
- Review log: `docs/changes/2026-08-20-bugfix-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-20-bugfix-skill-simplification/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: BUGSIM-CR3
- Verify readiness: not-claimed

## Blind-first risk map

The highest risks were a nominally complete table with unclassified edge states, an ordering conflict between blocker and owner-routing rows, an absent-defect request entering the fix path, and tests that proved only text presence rather than the promised deterministic cross-product. Direct inspection covered R2, R7, R12, R15-R17, T2, T5, T8, T11, the complete canonical skill, and the focused test implementation.

## Finding BUGSIM-CR3

- Finding ID: BUGSIM-CR3
- Severity: major
- Location: `skills/bugfix/SKILL.md` operation and current-action rules; `scripts/test-skill-validator.py` focused proof tests
- Evidence: R2 requires an invocation without one concrete defect to return `blocked`, but the skill never states that result. The first current-action row routes a generic “conflicting axis” to `stop-blocked` before the later R17-required `contract basis: conflicting` owner route, so the two rows can match the same state. The proof table admits only a complete deterministic alternative for infeasible testing but does not state how an incomplete claimed alternative is classified. Finally, `test_evidence_vocabularies_and_proof_table_are_complete` checks substrings only; it does not execute the T8 feasibility/proof cross-product or prove exactly one action per admitted combination.
- Required outcome: Make absent-defect handling explicit, distinguish cross-axis inconsistency from the recognized `contract basis: conflicting` value, classify incomplete alternative evidence before table evaluation, and add deterministic tests that prove the proof-action cross-product is exhaustive and pairwise non-overlapping.
- Safe resolution path: Add the smallest exact clauses to `SKILL.md`, replace the substring-only proof-table assertion with a parser-backed or equivalent deterministic table evaluator, run the M2 command ledger, and return the same milestone for code-review-m2-r4.
- needs-decision rationale: none; R2, R7, R12, R16, R17, T2, T5, T8, and T11 already establish the required outcome.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | R2 and R17 have ambiguous or missing edge behavior. |
| Test coverage | block | T8 promises cross-product proof, but the focused test checks only literal rows. |
| Edge cases | block | Incomplete alternative evidence and absent defect are not explicitly classified. |
| Error handling | concern | Generic conflict precedence can shadow the required contract-owner route. |
| Architecture boundaries | pass | The package remains one file with no new state owner or runtime. |
| Compatibility | pass with M3 reconciliation pending | No resource or lifecycle surface was added; final legacy reconciliation remains M3 work. |
| Security/privacy | pass | Command, write, external-effect, and lifecycle claim limits remain fail-closed. |
| Derived artifact currency | not yet due | Package-chain proof belongs to M3. |
| Unrelated changes | pass | The implementation correction is scoped to the bugfix contract and tests. |
| Validation evidence | concern | Commands pass, but the selected focused assertion does not directly prove T8. |

## Requirement-fidelity receipt

R7, R12, and R21 are now fully represented inline, and R26 correctly treats counts as diagnostic. R2 is missing its explicit absent-defect terminal behavior, while R16-R17 and T8 are not yet projected deterministically across the skill and focused tests. Requirement fidelity therefore fails only for BUGSIM-CR3.

## Prior-finding reconciliation

`BUGSIM-CR1` remains resolved. `BUGSIM-CR2` remains resolved: all formerly omitted vocabularies and tables are now inline and the 1,047-word, 8,926-byte package is reported truthfully. `BUGSIM-CR3` is a new finding discovered in the blind-first pass.

## Claim limitations

M2 remains open. This review does not establish M3 completion, final holistic review, explanation, verification, hosted CI, branch readiness, or PR readiness.
