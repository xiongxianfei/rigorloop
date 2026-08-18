# Code Review M2 R1: Explain-Change Skill Simplification

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation milestone M2 range `f9b5f8e1..9c5ba56b`
Reviewed milestone: M2
Reviewed artifact: commit `9c5ba56b`
Review date: 2026-08-18
Status: changes-requested
Material findings: EXCSIM-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, its invocation manifest, `review-log.md`, and `review-resolution.md`
- Open blockers: EXCSIM-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: EXCSIM-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-18-explain-change-skill-simplification/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-18-explain-change-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-18-explain-change-skill-simplification/review-resolution.md#code-review-m2-r1`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: EXCSIM-CR1
- Verify readiness: not-claimed

## Blind-first risk map

The highest-impact risks were loss of universal safeguards, incomplete action or resource combinations, unsafe replacement, an over-broad post-review evidence tail, stale reviewed-subject reuse, policy in the skeleton, and a profile that did not actually shrink. Direct inspection covered the package, coupled workflow and Git-state changes, focused and broad tests, generated-skill checks, and exact profile measurements.

## Material finding

Finding ID: EXCSIM-CR1
Severity: major
Location: `scripts/workflow_automation.py:486`
Evidence: `resolve_verification_readiness` supplies every verification-basis artifact path as `lifecycle_evidence_paths`. The new Git provider correctly permits only one direct-child commit, but that commit may still change the plan, final review, promotion, branch state, commands, or other-stage evidence because all are allowlisted. R26-R27 permit only the exact explanation artifact in the post-review commit and explicitly forbid change-record or other-stage evidence mutation.
Required outcome: Bind the post-review path allowance to only the exact explanation artifact and prove that verification constructs no broader exemption.
Safe resolution path: Change only the verification-readiness resolver and its focused test so the Git code-state anchor receives `explanation_inputs_identity` as the sole lifecycle evidence path; rerun workflow, Git-state, focused, broad skill, and build validation; rereview M2.
needs-decision rationale: none; the approved spec already fixes the allowed tail.
auto_fix_class: declared-safe
declared-safe recipe: replace the broad artifact-set comprehension with the exact explanation path and add a captured-call regression assertion.
forbidden paths: published skill package, governing artifacts, lifecycle schema, code-state provider contract, unrelated workflow stages.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | R26-R27 are compressed by an over-broad allowed-path set. |
| Test coverage | concern | One- versus multi-commit ancestry is proved, but the caller's exact path allowance is not. |
| Edge cases | block | A one-commit tail that mutates other-stage evidence is incorrectly accepted. |
| Error handling | pass | Invalid identities, missing fields, broader ancestry, and stale reviewed subjects fail closed. |
| Architecture boundaries | pass | No new persistence or owner is needed for the bounded correction. |
| Compatibility | pass | Published package and universal literals pass existing validators. |
| Security/privacy | pass | No external or sensitive-data behavior changed. |
| Derived artifact currency | pass for M2 | Build and check-mode package validation pass. |
| Unrelated changes | pass | The reviewed range stays within the approved package and directly coupled workflow surfaces. |
| Validation evidence | concern | All selected commands pass because no test captures the allowed-path argument. |

## Claim limitations

M2 remains open until EXCSIM-CR1 is corrected and rereviewed. No final verification or readiness claim is made.
