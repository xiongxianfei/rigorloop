# Test-Spec-Review Skill Simplification Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context

Target: `specs/test-spec-review-skill-simplification.test.md`

Reviewed artifact: `specs/test-spec-review-skill-simplification.test.md` at commit `953ea71b`

Review date: 2026-08-11
Status: changes-requested
Review status: changes-requested
Material findings: TSRSIM-TSR1, TSRSIM-TSR2
Recording status: recorded
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: TSRSIM-TSR1, TSRSIM-TSR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-11-test-spec-review-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-11-test-spec-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-11-test-spec-review-skill-simplification/review-resolution.md`
- Open blockers: TSRSIM-TSR1, TSRSIM-TSR2
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: implementation remains blocked pending test-spec correction and rereview

## Finding TSRSIM-TSR1

Finding ID: TSRSIM-TSR1
Severity: major
Location: `Milestone proof map` M1 row and test case T8
Evidence: The M1 row requires `T6-T9`, which includes T8. T8 computes before-and-after package and assembly measurements, declares `Required by milestone: M3`, and depends on the post-refactor package. The approved plan assigns only the baseline measurement to M1 and the completed comparison to M3. Requiring T8 before M1 code review therefore creates an impossible or misleading gate.
Required outcome: Make M1 require only proof executable from the unchanged baseline package, while keeping completed before-and-after assembly measurement in M3.
Safe resolution path: Change the M1 test set to `T6, T7, T9, T14`; retain `T8` in the M3 row; and confirm the M1 evidence still includes the baseline measurement named by the plan.
needs-decision rationale: none

## Finding TSRSIM-TSR2

Finding ID: TSRSIM-TSR2
Severity: major
Location: R13 coverage, PRF-005, and test case T16
Evidence: R13 requires shared recording procedure to cover retry and conflict handling. PRF-005 cites T16 as temporal proof, but T16's fixture and steps cover record shapes, blocked recording, ordering, and settlement without an interrupted identical retry or conflicting review-ID reuse case. The proof map therefore asserts temporal coverage that its named test does not exercise.
Required outcome: Add direct deterministic proof for idempotent interrupted recording or settlement retry and for conflict-stop behavior.
Safe resolution path: Extend T16 fixtures and steps with an identical incomplete settlement retry that reconciles without duplicating records, plus conflicting review-ID reuse that stops without mutation; make the expected and failure outcomes explicit while retaining CMD3 and CMD10 as the existing proof owners.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The proof map operationalizes the approved spec and plan without changing behavior. |
| Requirement coverage | concern | All R1-R39 are mapped, but R13 retry and conflict procedure lacks direct test steps. |
| Example coverage | pass | E1-E9 map to stable tests. |
| Negative and boundary coverage | concern | Resource, authority, status, and package failures are strong; recording retry and conflict are omitted. |
| Proof-level adequacy | concern | PRF-005 claims temporal proof broader than T16 currently establishes. |
| Milestone mapping | block | T8 is required by both M1 and M3 despite depending on post-refactor evidence and declaring M3 ownership. |
| Command validity | pass | Named commands exist, ownership is explicit, zero-test behavior is defined, and target runtimes are excluded. |
| Fixture and data design | concern | Add interrupted retry and conflicting-ID fixtures to the otherwise deterministic recording set. |
| Manual-proof boundary | pass | MP0 and MP1 are exact, justified, owned, and evidenced. |
| Observability | pass | Tests and commands identify IDs, evidence artifacts, recording paths, and failure meanings. |
| Determinism and isolation | pass | Proof excludes network, publication, credentials, and target-agent execution. |
| Scope and non-goals | pass | No runtime journey, tokenizer gate, or new permanent validator is introduced. |
| Execution economics | pass | Focused M1 and M2 proof is separated from broader M3 package proof. |
| Traceability | concern | ID coverage is complete, but one milestone mapping and one temporal claim are inconsistent with their direct proof. |
| Implementation handoff | block | M1 gating and recording retry behavior would require implementation-time interpretation. |

## No-finding areas

- All 39 requirements, 9 examples, 13 edge cases, 8 boundary IDs, and 7 selected interaction IDs have explicit proof-map rows.
- CMD1 matches the approved plan, defines all six semantic dispositions including `asset-owned`, and rejects unknown closed values before consistency checks.
- CMD7 uses the trusted immutable `v0.3.6` fixture, checked subprocesses, and an automatically cleaned temporary directory.
- Static scenarios, package validation, and manual semantic review explicitly exclude Codex, Claude Code, opencode, or another target-agent runtime.
