<!-- Template: test-spec-review-result-skeleton-v1 -->
<!-- Skill: test-spec-review -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/test-spec-review/SKILL.md -->

# Progressive Boundary-First Skill Guidance Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex test-spec-review skill
Target: specs/progressive-boundary-first-skill-guidance.test.md
Status: changes-requested
Review status: changes-requested
Material findings: PBS-TSR1
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: PBS-TSR1
- Recording status: recorded
- Recording blocker: none
- Review record:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/test-spec-review-r1.md`
- Review log:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/review-log.md`
- Review resolution:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/review-resolution.md#test-spec-review-r1`
- Open blockers: PBS-TSR1
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: M2 proof timing and command coverage do not match the approved plan.

## Review inputs

- Test spec:
  `specs/progressive-boundary-first-skill-guidance.test.md`
- Test-spec authoring evidence:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/test-spec-authoring.md`
- Approved feature specification:
  `specs/progressive-boundary-first-skill-guidance.md`
- Approved specification review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/spec-review-r1.md`
- Approved canonical architecture:
  `docs/architecture/system/architecture.md`
- Accepted resource ADR:
  `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`
- Approved architecture review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/architecture-review-r2.md`
- Approved execution plan:
  `docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Approved plan review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/plan-review-r2.md`
- Boundary-first proof-review method:
  `skills/test-spec-review/references/boundary-first-method-v1.md`

## Findings

## Finding PBS-TSR1

Finding ID: PBS-TSR1
Severity: major
Location: Test-spec boundary proof row `PRF-020`, M2 milestone proof row, and T4/T13 compatibility coverage.
Evidence: The approved plan assigns `BND-COMPAT-001` and `INT-004` to M2 and requires M2 fixtures to distinguish pending, active-candidate, grandfathered non-substantive, and substantive revisions. It also requires `python scripts/project-boundary-first-reference.py --check` during M2. The test spec assigns `PRF-020` only to M4 evidence, keeps the grandfathered revision cases in M4-only T13, and omits CMD2 from the M2 milestone row.
Required outcome: M2 must directly prove the complete published-guidance state matrix and run every approved M2 validation command before M2 code review, while M4 retains the separate package and activation-state composition proof.
Safe resolution path: Revise T4 or split a focused M2 compatibility-guidance case, map it to `BND-COMPAT-001` and `INT-004` with M2 evidence, add CMD2 to the M2 milestone row, and leave T3/T13/M4 responsible for candidate, package, and rollback composition. Re-run test-spec authoring validation and require test-spec-review R2.
needs-decision rationale: none

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Governing-contract alignment | concern | Feature behavior is preserved, but M2 proof timing does not fully match the approved plan. |
| Requirement coverage | pass | All 38 requirements map to stable tests. |
| Example coverage | pass | E1 through E6 map to representative automated cases. |
| Negative and boundary coverage | pass | Invalid values, unsafe paths, stale IDs, mixed sets, interruption, fallback, and rollback are covered. |
| Proof-level adequacy | pass | Unit, integration, end-to-end, smoke, contract, and migration levels match the risks. |
| Milestone mapping | block | M2 omits required compatibility-guidance proof and CMD2. |
| Command validity | concern | All commands exist and have owners, but CMD2 is absent from its plan-required M2 gate. |
| Fixture and data design | pass | Fixtures are isolated, deterministic, repository-local, and temporary where derived. |
| Manual-proof boundary | pass | No manual proof is needed; semantic judgment remains in formal review. |
| Observability | pass | T10 defines stable, bounded, first-divergence diagnostics. |
| Determinism and isolation | pass | Network, registry, user-install, time, and shared-state dependencies are excluded. |
| Scope and non-goals | pass | No activation, publication, hard budget, runtime service, or Cartesian inventory is added. |
| Execution economics | pass | Focused milestone checks precede package and broad-smoke proof. |
| Traceability | concern | Stable IDs are consistent, but `PRF-020` hides the earlier M2 proof obligation. |
| Implementation handoff | block | M2 could close without proving guidance it changes, so M1 implementation cannot begin under the approved preimplementation gate. |

## Recommendation

Request the narrow test-spec revision described by PBS-TSR1, then run
`test-spec-review` R2.

No automatic downstream handoff occurs.
The finding was recorded before any review-driven fix.
