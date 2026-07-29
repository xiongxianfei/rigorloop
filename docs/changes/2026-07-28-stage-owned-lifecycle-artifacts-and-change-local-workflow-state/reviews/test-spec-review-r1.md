# Test Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex test-spec-review skill
Target: specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.test.md
Status: changes-requested
Review status: changes-requested
Original review source: User-requested `$test-spec-review` on 2026-07-29.
Material findings: SLA-TSR1, SLA-TSR2, SLA-TSR3
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: SLA-TSR1, SLA-TSR2, SLA-TSR3
- Recording status: recorded
- Recording blocker: none
- Review record:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/test-spec-review-r1.md`
- Review log:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md`
- Review resolution:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#test-spec-review-r1`
- Open blockers: SLA-TSR1, SLA-TSR2, SLA-TSR3
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: proof-map revision and fresh test-spec-review required

## Review inputs

- Test spec:
  `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.test.md`
- Approved feature spec:
  `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Approved spec review:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r6.md`
- Approved plan:
  `docs/plans/2026-07-29-stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Approved plan review:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/plan-review-r2.md`
- Approved architecture:
  `docs/architecture/system/architecture.md`
- Approved architecture review:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/architecture-review-r2.md`
- ADR:
  `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md`
- Boundary-first review method:
  `skills/test-spec-review/references/boundary-first-method-v1.md`
- Compatibility projections:
  the 32 matching test specs named by SLA-R074c

All registered command entrypoint files exist.
Only no-side-effect help inspection was performed for the boundary validator
and CI wrapper.
No proof command, fixture suite, network action, secret access, or final
validation was executed during review.

## Findings

## Finding SLA-TSR1

Finding ID: SLA-TSR1
Severity: major
Location: Validation commands, Milestone proof map, PRF-009, T5-T8,
  T13, T19, T20, and T22; primary test spec lines 83, 174-198, 254-317,
  358-369, 436-486
Evidence: CMD4 and CMD6 are first required in M3, CMD11 in M5, and CMD12
  at final verify. M1 nevertheless claims T5, T6, and T19, whose command
  lists include CMD4/CMD6; PRF-009 claims INT-001 closes in M1 using
  CMD4/CMD6. M2 claims T7, T8, T11, T12, T13, T19, and T20 even though
  several are test-case-owned by M3, M5, M6, or M7 and require later
  commands. T13 lists CMD12 while also being required in M6 without an
  explicit deferred-command split. T22 says it is required by M3 and M6 but
  appears in neither milestone row. The map therefore cannot establish which
  portion is executable and mandatory at each code-review gate.
Required outcome: Every milestone must depend only on proof available at
  that milestone, and every test's staged activation must be explicit.
  INT-001 must have direct M1 proof using M1-owned commands, while later state
  integration remains visibly deferred to M3.
Safe resolution path: Split cross-milestone cases into early
  published-skill contract assertions and later state/composed assertions, or
  add a progressive activation table that names each earlier assertion,
  available command, later assertion, and deferral. Remove later-only tests
  from M1/M2 rows, add T22 to M3/M6, and distinguish T13's M6 containment
  proof from CMD12 final-verify proof.
needs-decision rationale: none

## Finding SLA-TSR2

Finding ID: SLA-TSR2
Severity: major
Location: Manual QA checklist MP1 and MP2; primary test spec lines 555-582;
  hybrid proof rows PRF-003, PRF-004, PRF-008, and PRF-014
Evidence: MP1 and MP2 name owners, general steps, pass/fail conditions, and
  evidence, but neither records the required automation rationale, required
  environment, owning stage, or exact required gate. MP1 also combines
  M1/M2/M5 without saying which changed surfaces trigger it at each gate.
  Because four boundary obligations cite these procedures as hybrid proof,
  the missing fields leave authority, composition, environment, and recovery
  proof non-executable.
Required outcome: Every manual procedure must have a stable, complete,
  independently executable contract with an automation rationale, owner,
  owning stage, required environment, exact steps, evidence artifact, pass
  condition, failure condition, and required gate.
Safe resolution path: Rewrite MP1 and MP2 with the complete closed manual
  proof shape. Bind MP1 separately to each applicable M1/M2/M5 review surface
  and bind MP2 to M5 preactivation, M6 cutover, and final verify recheck.
  Keep the procedures limited to semantic and call-path judgments that
  deterministic checks cannot prove.
needs-decision rationale: none

## Finding SLA-TSR3

Finding ID: SLA-TSR3
Severity: major
Location: T14, Migration or compatibility tests, and all 32
  `Stage-owned lifecycle proof alignment` notices; primary test spec lines
  371-382 and 513-521; dependent notices at lines 7-17 of each revised test
  spec
Evidence: T14 requires classification of each matching proof map's replaced
  rows and retained behavior. The 32 revisions contain identical generic text
  that points to the matching feature spec and T14, but none identifies its
  exact replaced subject, affected coverage/test IDs, or disposition of
  retained rows. A reviewer or implementer must redo the semantic audit to
  know whether a legacy row is historical, retained, or prohibited for a
  governed change. This does not make AC-SLA-035 independently traceable or
  prove the preimplementation gate is closed.
Required outcome: Each dependent proof map must have an exact, reviewable
  disposition for its replaced proof subject while preserving unrelated
  proof.
Safe resolution path: Add one central compatibility projection matrix to
  the primary test spec keyed by all 32 dependent test-spec paths. For each
  row, record the matching source spec, exact replaced subject, affected
  test/coverage IDs or an explicit whole-subject rule, retained proof
  disposition, and replacement test IDs. Update each short notice to cite its
  stable matrix row. This preserves small dependent-file diffs while making
  T14 and test-spec-review executable.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The proof map preserves published-skill ownership, change-local state, conservative replay, minimal validation, atomic cutover, and excluded mechanisms. |
| Requirement coverage | pass | All 122 requirements and 35 acceptance criteria resolve through stable grouped mappings and concrete tests. |
| Example coverage | pass | E1-E13 map to stable test cases with behavior owned by the approved spec. |
| Negative and boundary coverage | pass | Invalid, stale, unknown, conflicting, migration, rollback, cancellation, verification, and external-action cases are represented. |
| Proof-level adequacy | block | Four hybrid boundary obligations rely on incomplete MP1/MP2 contracts. |
| Milestone mapping | block | M1/M2 claim later-owned commands and tests, and T22 is absent from its required milestones. |
| Command validity | concern | Entrypoints resolve and command metadata is complete, but cross-milestone activation and CMD12 deferral are ambiguous. |
| Fixture and data design | pass | Fixtures are local, deterministic, representative, history-preserving, and use fail-on-call external doubles. |
| Manual-proof boundary | block | MP1/MP2 omit mandatory procedure fields and exact gate bindings. |
| Observability | pass | Test cases name failure meaning and planned evidence; diagnostics are required to identify invalid fields and safe owners. |
| Determinism and isolation | pass | Network, credentials, external mutation, shared generated output, and history rewriting are excluded. |
| Scope and non-goals | pass | No hashes, selectors, protected paths, new validator family, selective reuse, or external action is introduced. |
| Execution economics | pass | Focused existing checks precede two broad-smoke boundaries and one final PR-mode gate. |
| Traceability | block | The 32 compatibility projections do not identify which legacy proof rows are replaced versus retained. |
| Implementation handoff | block | M1 cannot begin until timing, manual proof, and compatibility dispositions are revised and re-reviewed. |

## Boundary-first assessment

All eight boundary IDs and seven interaction IDs are present with direct
covered rows.
Negative partitions and composed public paths are represented.
Structural completeness is not sufficient for approval because PRF-003,
PRF-004, PRF-008, and PRF-014 depend on incomplete manual procedures, and
PRF-009 is timed before its listed commands become mandatory.

## Recommendation

Changes requested.

Revise the test spec and the 32 lightweight projection notices as described by
SLA-TSR1 through SLA-TSR3, record dispositions, and rerun test-spec-review.

This direct review is isolated.
It does not edit the test specifications, authorize implementation, execute
proof commands, or advance workflow routing.
