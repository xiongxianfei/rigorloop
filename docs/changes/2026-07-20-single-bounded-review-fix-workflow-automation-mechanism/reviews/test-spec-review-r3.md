# Test Spec Review R3

Review ID: test-spec-review-r3
Stage: test-spec-review
Round: 3
Reviewer: Codex test-spec-review
Target: specs/single-bounded-review-fix-workflow-automation.test.md
Reviewed artifact: specs/single-bounded-review-fix-workflow-automation.test.md
Review date: 2026-07-21
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: None
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: none; existing finding `BRF-TSR4` remains open
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/test-spec-review-r3.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md
- Open blockers: `BRF-TSR4`; T26 is required by M6 but has no M6 case-level or progressive activation contract
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: complete the T26 M4/M6 activation mapping and rereview before M1 implementation

## Review inputs

| Artifact | SHA-256 |
| --- | --- |
| `specs/single-bounded-review-fix-workflow-automation.test.md` | `29d84449cbcac25ca557e84f02cbacfdfac51feb3d91f8abc0b4a73459ec3368` |
| `specs/single-bounded-review-fix-workflow-automation.md` | `59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070` |
| `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md` | `ea0ab22c5cfb05e0d086ce62d8fda39c96f8056e5cc57c53c5562976ae274ec2` |
| `docs/architecture/system/architecture.md` | `3ad5871a99f96f86e7beed58137a6eab7fdf235a0a36dd5c25f3ea6899e9dca8` |
| `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md` | `72f84faada32301b58221e008f7bd90d198bc002e51ffa868e5210b1299bd538` |
| `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/test-spec-review-r2.md` | `4f5cf2a267074870ffa0835587349db5ee9d50df2ea18422c95d6383fbb71663` |

The feature spec is approved, architecture and ADR are settled, plan-review R2 is approved, and the revised test-spec identity is current.
The proof map is reviewable; the remaining defect is local to the test specification.

## Prior finding closure

| Finding | R3 result | Evidence |
| --- | --- | --- |
| `BRF-TSR1` | resolved | MP1-MP3 remain complete and T22 owns the automated public-output assertions. |
| `BRF-TSR2` | resolved | CMD30 remains directly executable as stored and CMD18 retains one first-required gate. |
| `BRF-TSR3` | resolved | The deterministic fixture contract remains complete and is now applied at separate state and composed-engine boundaries. |
| `BRF-TSR4` | not resolved | T29 and T30 correctly separate M2 and M6 proof, and 14 progressive cases are mapped, but T26 is listed as an M6 proof obligation without an M6 activation entry or M6 requirement in the case. |

## Findings

No new material finding is opened.
The existing `BRF-TSR4` record remains the governing finding because its required outcome was exhaustive milestone-local activation.

Rereview evidence:

- The M6 milestone row requires `T25-T28`, which includes T26.
- T26 declares `CMD17` and the M6-owned `CMD25`, but says only `Required by milestone: M4`.
- The progressive activation table has no T26 row defining M4 assertions, M6 assertions, or explicit deferral.
- An implementer must therefore infer whether CMD25 is an M6 proof obligation, a regression-only command, or stale case metadata.

Required outcome remains: every test required at multiple gates must bind exact milestone-local assertions and commands, and later-owned commands must be explicitly deferred at earlier gates.

Safe resolution remains: add T26 to the progressive activation table with M4/CMD17 authoring-route proof and M6/CMD25 composed public-route proof, and change its case-level requirement to `M4 and M6`; alternatively remove T26 from M6 and CMD25 from the case if M6 proof is intentionally delegated to another stable test ID. The former matches the current M6 cutover design.

Owner decision is not required.

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The proof map continues to operationalize the approved spec, architecture, and plan without changing them. |
| Requirement coverage | pass | All 139 requirements and acceptance families remain mapped. |
| Example coverage | pass | E1-E12 remain mapped to stable test IDs. |
| Negative and boundary coverage | pass | Failure, stale-state, authorization, migration, cancellation, rollback, and external-action boundaries remain covered. |
| Proof-level adequacy | pass | T29/T30 now correctly separate state integration proof from composed end-to-end proof. |
| Milestone mapping | block | T26 is required by the M6 row but its case and activation table describe only M4. |
| Command validity | concern | CMD17 and CMD25 are individually classified correctly, but their T26 milestone applicability is incomplete. |
| Fixture and data design | pass | Fixtures remain deterministic, isolated, temporary, and stage-native. |
| Manual-proof boundary | pass | MP1-MP3 remain complete and bounded. |
| Observability | pass | Failure meaning and durable evidence remain explicit. |
| Determinism and isolation | pass | The split T29/T30 contracts control nondeterminism at both executable boundaries. |
| Scope and non-goals | pass | No unapproved behavior or external action was added. |
| Execution economics | pass | Focused milestone proof remains separated from final cutover and broad smoke. |
| Traceability | block | T26 has contradictory case-level and milestone-level ownership and no progressive activation entry. |
| Implementation handoff | block | Implementation would still have to infer T26's M6 obligation. |

## Recommendation

Apply the one-case `BRF-TSR4` completion described above, then rerun `test-spec-review`.
No feature-spec, architecture, ADR, or plan redesign is required.

This direct formal review is isolated and does not automatically revise the test spec or start implementation.
