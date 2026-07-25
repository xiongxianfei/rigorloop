# Test Spec Review R2

Review ID: test-spec-review-r2
Stage: test-spec-review
Round: 2
Reviewer: Codex test-spec-review
Target: specs/single-bounded-review-fix-workflow-automation.test.md
Reviewed artifact: specs/single-bounded-review-fix-workflow-automation.test.md
Review date: 2026-07-21
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: BRF-TSR4
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: BRF-TSR4
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/test-spec-review-r2.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md
- Open blockers: milestone-local activation is ambiguous for proof cases that span multiple milestones
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: revise and rereview the active test spec before M1 implementation

## Review inputs

| Artifact | SHA-256 |
| --- | --- |
| `specs/single-bounded-review-fix-workflow-automation.test.md` | `4064f10802f5ac2d0c6cda70e70075b543e06f7ea92a0bc7f66f397465d48459` |
| `specs/single-bounded-review-fix-workflow-automation.md` | `59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070` |
| `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md` | `520c339beafd76bf146fc16708ce47aed31e44b110363a6437c3b19e37ee83f8` |
| `docs/architecture/system/architecture.md` | `3ad5871a99f96f86e7beed58137a6eab7fdf235a0a36dd5c25f3ea6899e9dca8` |
| `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md` | `72f84faada32301b58221e008f7bd90d198bc002e51ffa868e5210b1299bd538` |
| `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/test-spec-review-r1.md` | `fa990ce8a1f8753da173766e58f206bd92cfb712f6e47e6970a0a014b9e2fde4` |

The feature spec is approved, architecture and ADR are settled, plan-review R2 is approved, and the revised test spec has a stable identifiable revision.
The proof map is reviewable; the remaining finding is local to milestone activation in the test specification.

## Prior finding closure

| Finding | R2 result | Evidence |
| --- | --- | --- |
| `BRF-TSR1` | resolved | MP1-MP3 now record automation rationale, owner, owning stage, environment, exact steps, evidence, pass/fail conditions, and required gates; T22 owns the former untracked output checks. |
| `BRF-TSR2` | resolved | CMD30 is a directly executable, pipe-free, manifest-derived temporary-output command; CMD18 names M4 as its first required milestone and records later reuse. |
| `BRF-TSR3` | resolved | The deterministic fixture contract fixes clock, IDs, environment, locale, timezone, randomness, filesystem, teardown, process state, and order proof. |

## Findings

### BRF-TSR4

Finding ID: BRF-TSR4
Severity: major
Location: `specs/single-bounded-review-fix-workflow-automation.test.md:151-160` and `specs/single-bounded-review-fix-workflow-automation.test.md:566-577`
Evidence: The milestone table requires T29 at M2 using CMD4-CMD9, while T29 declares CMD6, CMD7, CMD8, and the M6-owned CMD25 and describes both state-level and full-engine fixtures, status evidence, and external-action trap assertions. Its only activation statement is `Required by milestone: M2 and M6`, so it does not define which assertions constitute M2 completion and which remain planned until M6. The same unspecialized pattern appears in other cases required by multiple milestones, where a case-level command list includes commands first owned by a later milestone. The milestone command rows imply a split, but the test cases do not make that split executable or traceable.
Required outcome: Every test case required by more than one milestone must state the exact assertions and command IDs activated at each milestone, and no earlier milestone may appear to depend on a later-owned command or unavailable component. State-level determinism required at M2 must be independently passable before the full engine exists; full-engine order-independence remains an M6 gate.
Safe resolution path: Audit all multi-milestone cases and add an explicit per-milestone activation map linking each milestone to its currently executable assertions and commands. Prefer splitting T29 into a stable M2 state/receipt/migration determinism case using CMD6-CMD8 and a separate M6 full-engine order-independence case using CMD25, then update requirement coverage, the milestone proof map, fixture order proof, test counts, and command mappings. Rerun test-spec-review after the proof IDs and activation boundaries are internally consistent.
needs-decision rationale: none

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The proof map operationalizes the approved contract and does not reopen product or architecture decisions. |
| Requirement coverage | pass | All 139 requirements and acceptance families remain mapped. |
| Example coverage | pass | E1-E12 map to stable test IDs. |
| Negative and boundary coverage | pass | Failure, stale-state, unknown-value, authorization, migration, cancellation, rollback, and external-action boundaries are covered. |
| Proof-level adequacy | pass | Automated, contract, integration, end-to-end, smoke, and bounded manual levels match the risks. |
| Milestone mapping | block | Multi-milestone cases do not define milestone-local assertion and command activation; T29 crosses the M2/M6 component boundary. |
| Command validity | concern | Individual commands are well classified, but case-level command applicability can conflict with the command's first required milestone. |
| Fixture and data design | pass | Deterministic, isolated, temporary, stage-native fixtures are specified. |
| Manual-proof boundary | pass | MP1-MP3 are complete, owned, evidenced, and limited to inspection that automation cannot fully establish. |
| Observability | pass | Failure meaning and durable evidence are explicit. |
| Determinism and isolation | pass | All relevant nondeterministic inputs and repeat/order proof are controlled. |
| Scope and non-goals | pass | The test spec adds no unapproved mechanism, external action, alias removal, or hosted-execution scope. |
| Execution economics | pass | Focused milestone checks precede final cutover and broad smoke. |
| Traceability | concern | Requirement-to-test traceability is complete, but test-to-milestone command traceability is not exhaustive for progressive cases. |
| Implementation handoff | block | M2 implementation would have to infer the subset of T29 that is required before later engine components exist. |

## Recommendation

Revise only the active test specification and its lifecycle references.
No feature-spec, architecture, ADR, or plan redesign is required.
After milestone-local activation is explicit, rerun `test-spec-review` before M1 implementation.

This direct formal review is isolated and does not automatically revise the test spec or start implementation.
