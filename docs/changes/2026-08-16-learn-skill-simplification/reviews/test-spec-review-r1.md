# Test-Spec Review R1: Learn Skill Simplification

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/learn-skill-simplification.test.md`

Reviewed artifact: commit `8b844688`
Review date: 2026-08-17
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: LRNSIM-TSR1, LRNSIM-TSR2
Immediate next stage: review-resolution
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: LRNSIM-TSR1, LRNSIM-TSR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-16-learn-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-16-learn-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-learn-skill-simplification/review-resolution.md`
- Open blockers: M1 proof timing is internally inconsistent, and R37 compact-result behavior lacks direct proof
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: bounded automation target reached at the first formal test-spec-review result; implementation remains blocked pending disposition, test-spec revision, and rereview

## Findings

## Finding LRNSIM-TSR1

Finding ID: LRNSIM-TSR1
Severity: major
Location: `Milestone proof map` M1 row, PRF-006, T2-T3, T7-T10, T14, and CMD1/CMD3
Evidence: M1 claims T2-T3, T7-T12, and T14 are required with CMD1, but T2-T10 and T14 each name CMD3, which is a planned M2 test class and cannot run while M1 intentionally leaves the canonical package unchanged. PRF-006 also assigns the complete recovery boundary, including R46, to required milestone M2 even though the approved plan requires architecture-trigger proof to close in M1 before M2 begins. The proof map therefore cannot establish its stated M1 gate with the commands available at that milestone.
Required outcome: Separate M1 inventory, scenario-contract, baseline, and architecture-trigger proof from M2 package-behavior proof; ensure every M1-required test uses an M1-available command; and bind R46's direct obligation to M1 before canonical mutation.
Safe resolution path: Add or split a focused M1 case using CMD1 for ledger closure, scenario serialization, exact caller inventory, baseline identity, and R46 no-trigger or stop behavior; remove M2-only cases from the M1 row; split PRF-006 when necessary so recovery behavior remains M2 while architecture escalation is explicitly M1; update acceptance and milestone mappings consistently.
needs-decision rationale: none

## Finding LRNSIM-TSR2

Finding ID: LRNSIM-TSR2
Severity: major
Location: Requirement coverage row `R36-R40, R47`, PRF-004, T9-T11, and absence of a compact-result test
Evidence: R37 requires the compact result to distinguish operation, session identity and path, trigger and scope, confirmation, session recording, topic effects, route IDs and settlements, owner-result identities, blockers, next owner or handoff, and claim limitations. The coverage row points to T9-T11, but those cases prove legacy ownership, historical compatibility, and ledgers; none constructs or asserts the complete result for `run-learn-session`, `record-learn-route-result`, blocked input, or idempotent replay. PRF-004 cites broad composition cases without a direct result-shape assertion.
Required outcome: Add direct deterministic proof for the complete R37 result across the two successful operations and representative blocked or idempotent outcomes, including omission or sentinel behavior for inapplicable fields and narrow claim limitations.
Safe resolution path: Add one focused compact-result test, map R37 and the relevant acceptance and composition rows to it, assign an executable M2 command, and keep result layout structural rather than adding a new asset unless repeated drift independently justifies one.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| governing-contract alignment | pass | The proof map consumes the approved spec, no-architecture assessment, active plan, and clean upstream reviews without redefining behavior. |
| requirement coverage | concern | All requirement ranges are listed, but R37 lacks a direct asserting case. |
| acceptance-criterion coverage | pass with revision | AC1 claims full mapping and must include the new R37 case and corrected M1 gate. |
| example and edge coverage | pass | E1-E12 and EC1-EC11 have explicit mappings and outcomes. |
| boundary and interaction coverage | concern | All boundaries and interactions are present, but PRF-006 assigns R46 to the wrong required milestone. |
| negative and failure coverage | pass | Unknown values, collisions, partial state, stale identity, wrong completion kind, missing resources, and architecture triggers are represented. |
| proof-level adequacy | pass | Contract and integration levels suit the content and package claims. |
| milestone mapping | block | M1 depends on multiple M2-only CMD3 cases and cannot close with its stated command set. |
| command validity | pass with revision | Command paths are coherent, but planned class availability does not match M1 case ownership. |
| fixture and data design | pass | Filesystem, session, route, cross-spec, ledger, and package fixtures are deterministic and bounded. |
| manual-proof boundary | pass | No manual proof is required, and ordinary review is not recast as acceptance. |
| determinism and isolation | pass | Network, target-agent, external mutation, transcript grading, and migration are excluded. |
| implementation handoff | block | Implementation would need to invent M1/M2 proof separation and the R37 assertions. |

## Boundary assessment

Every approved boundary and selected interaction has a structural proof row, and boundary validation passes. Semantic proof timing is not yet adequate for BND-RECOVERY-001/R46, and BND-COMPOSE-001 lacks direct proof of the required compact result surface.

## No additional findings rationale

Stable route IDs, completion-kind mismatches, contributor versus destination authority, historical compatibility, both-profile measurement, package parity, and architecture fallback otherwise have proportionate positive and negative coverage. The two findings are proof-map defects and do not require a spec, architecture, or plan change.

## Claim limitations

This review does not claim tests were implemented or run, implementation is authorized, validation passed, or the branch is ready for verification or PR review.
