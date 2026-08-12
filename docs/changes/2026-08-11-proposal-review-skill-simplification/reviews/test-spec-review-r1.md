# Proposal-Review Skill Simplification Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/proposal-review-skill-simplification.test.md`
Reviewed artifact: `specs/proposal-review-skill-simplification.test.md` at commit `97d50401`
Review date: 2026-08-11
Status: changes-requested
Review status: changes-requested
Material findings: PRRSIM-TSR1, PRRSIM-TSR2
Recording status: recorded
Lifecycle mode: formal
Handoff mode: workflow-managed
Boundary applicability: `boundary-first-v1` applicable
Recording applicability: required for formal review
Loaded resources: `SKILL.md`, both boundary references, recording-and-settlement reference, and result asset
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Automatic downstream handoff: workflow-managed bounded correction and rereview

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: PRRSIM-TSR1, PRRSIM-TSR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-11-proposal-review-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-11-proposal-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-11-proposal-review-skill-simplification/review-resolution.md`
- Open blockers: PRRSIM-TSR1, PRRSIM-TSR2
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: implementation remains blocked pending test-spec correction and rereview

## Findings

## Finding PRRSIM-TSR1

Finding ID: PRRSIM-TSR1
Severity: major
Location: `Milestone proof map` M1 row and test case T9
Evidence: M1 requires T9 before M1 code review, but T9 combines the baseline scenarios with before-and-after assembly measurement and declares itself required by both M1 and M3. The approved plan assigns only baseline measurement to M1 and the completed comparison to M3, after the package refactor.
Required outcome: Make M1 depend only on proof executable against the unchanged baseline package while retaining complete before-and-after assembly measurement in M3.
Safe resolution path: Split T9 into baseline scenario and measurement proof or narrow T9 to M1-executable scenario and baseline assertions, add a separate M3 measurement case, and update coverage, proof obligations, milestone rows, and command/evidence mappings consistently.
needs-decision rationale: none

## Finding PRRSIM-TSR2

Finding ID: PRRSIM-TSR2
Severity: major
Location: PRF-005, test cases T2 and T4, and BND-TEMPORAL-001 coverage
Evidence: The approved spec assigns bounded retry handling to the recording reference and defines temporal retry, replay, and conflict outcomes, but T2 and T4 assert initial recording and side-effect branches without an interrupted identical write, reconciliation without duplicate evidence, or conflicting review-ID reuse that stops without mutation.
Required outcome: Add direct deterministic proof for idempotent interrupted recording or settlement retry and conflicting review-ID reuse.
Safe resolution path: Extend T4 or add a dedicated case with an identical incomplete settlement retry that reconciles exactly once and a reused review ID for a different target or result that stops without mutation; update PRF-005, edge coverage, milestone mapping, fixtures, and evidence accordingly.
needs-decision rationale: none

## Proof-map assessment

- Requirements: all R1-R37 are mapped, but the two temporal and milestone defects above prevent approval.
- Examples: E1-E8 map to concrete cases without creating behavior.
- Boundaries: all eight applicable boundary IDs have covered proof obligations with exact governing requirement sets.
- Interactions: INT-001 through INT-006 have direct composed proof at contract or integration level.
- Edge cases: EC1-EC10 map to negative or recovery assertions.
- Milestones: M1 freezes inventories and scenarios, M2 proves canonical composition and authority, and M3 proves measurements, semantics, distribution, and rollback before their respective code reviews.
- Commands: CMD1-CMD10 have closed classifications, owners, first-required gates, failure behavior, zero-test behavior, evidence, and safe side-effect boundaries.
- Manual proof: MP0 and MP1 contain rationale, environment, exact steps, evidence, pass and failure conditions, and owner stage.
- Runtime boundary: no command executes or grades Codex, Claude Code, opencode, or another target-agent runtime.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| requirement traceability | pass | Every normative requirement has direct proof and observable assertions. |
| acceptance criteria | pass | The cases collectively prove all sixteen acceptance clusters. |
| negative and failure coverage | pass | Unknown modes, invalid pairs, late triggers, collisions, blocked writes, ambiguity, missing resources, mixed packages, and stale authority are explicit. |
| proof-level adequacy | pass | Static contracts, validator integration, filesystem e2e package proof, and semantic manual review match their claims. |
| boundary and interaction coverage | pass | All approved IDs are consumed unchanged and validated structurally. |
| milestone mapping | block | M1 currently depends on T9's post-refactor measurement portion. |
| command feasibility | pass | Existing commands and relevant flags resolve; planned CMD1 is fully specified before M1. |
| fixtures and determinism | pass | JSON-compatible static fixtures, unknown-first negatives, trusted package version, and managed temporary roots avoid network, time, randomness, and shared-state drift. |
| manual evidence | pass | MP0 and MP1 are exact, bounded, and evidence-producing. |
| compatibility and rollback | pass | Literal migration, raw-byte distribution, mixed-package rejection, and prior complete-package recovery are directly covered. |
| scope and economics | pass | Existing validators are reused, target-runtime execution is excluded, and change-local metrics do not become permanent gates. |
| implementation handoff | block | Implementation remains blocked until corrected proof receives approval. |

## Recommendation

Changes requested.
Correct the M1/M3 measurement split and add direct retry and conflict proof, then rerun `test-spec-review`; implementation handoff remains not allowed.
