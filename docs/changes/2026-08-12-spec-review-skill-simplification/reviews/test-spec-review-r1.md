# Spec-Review Skill Simplification Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/spec-review-skill-simplification.test.md`
Reviewed artifact: commit `65e99325`
Review date: 2026-08-12
Status: changes-requested
Review status: changes-requested
Material findings: SRSS-TSR1
Recording status: recorded
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: SRSS-TSR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-12-spec-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-spec-review-skill-simplification/review-resolution.md`
- Open blockers: SRSS-TSR1
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: implementation remains blocked pending test-spec correction and rereview

## Finding SRSS-TSR1

Finding ID: SRSS-TSR1
Severity: major
Location: `specs/spec-review-skill-simplification.test.md`, Milestone proof map M1 row
Evidence: The M1 row requires `T6-T9`, which includes T8. T8 measures final before-and-after profile and package results, declares `Required by milestone: M3`, and requires the post-refactor package. The approved plan assigns only baseline measurement to M1 and the completed comparison to M3.
Required outcome: Make M1 require only proof executable from the unchanged baseline package while retaining completed profile comparison in M3.
Safe resolution path: Change the M1 test set to `T6, T7, T9, T14`, retain `T8` in M3, and keep the M1 baseline evidence artifact.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The proof map operationalizes the approved spec and plan without changing behavior. |
| Requirement coverage | pass | All R1-R45 have mapped proof. |
| Example coverage | pass | E1-E8 map to stable tests. |
| Negative and boundary coverage | pass | Invalid, stale, missing-resource, retry, mixed-package, and rollback cases are represented. |
| Proof-level adequacy | pass | Automated, hybrid, end-to-end, and manual proof boundaries match the claims. |
| Milestone mapping | block | T8 cannot complete at M1 because it requires the final package. |
| Command validity | pass | Commands are exact, owned, side-effect bounded, and zero-test behavior is explicit. |
| Fixture and data design | pass | Static records and temporary package roots are deterministic. |
| Manual-proof boundary | pass | MP0 and MP1 have exact procedures, owners, evidence, and failure conditions. |
| Observability | pass | Cases and commands identify IDs, artifacts, and failure meaning. |
| Determinism and isolation | pass | Proof excludes network, publication, credentials, and target-agent execution. |
| Scope and non-goals | pass | No runtime journey, tokenizer gate, or new permanent validator is introduced. |
| Execution economics | pass | Focused M1/M2 proof remains separate from broader M3 package proof. |
| Traceability | concern | One milestone range contradicts T8's explicit M3 ownership. |
| Implementation handoff | block | M1 acceptance would otherwise require unavailable post-refactor evidence. |

## No-finding areas

- The boundary feature and proof records pass the repository boundary validator.
- CMD1 is the exact approved standard-library ledger and scenario proof and rejects unknown closed values before consistency checks.
- CMD7 is an exact, recoverable, local temporary adapter proof for all supported targets.
- T13 names CMD6 for incomplete and mixed package fixtures, CMD7 for the valid selected package, and CMD9 for lifecycle metadata.
- No acceptance step executes Codex, Claude Code, opencode, or another target-agent runtime.
