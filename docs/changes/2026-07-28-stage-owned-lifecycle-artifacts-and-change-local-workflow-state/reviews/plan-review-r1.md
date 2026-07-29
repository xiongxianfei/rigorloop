# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review skill
Target: docs/plans/2026-07-29-stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md
Status: changes-requested
Original review source: User-requested `$plan-review` on 2026-07-29.
Material findings: SLA-PL1, SLA-PL2
Immediate next stage: plan revision
Automatic downstream handoff: none

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: SLA-PL1, SLA-PL2
- Recording status: recorded
- Recording blocker: none
- Review record:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/plan-review-r1.md`
- Review log:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md`
- Review resolution:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#plan-review-r1`
- Open blockers: SLA-PL1, SLA-PL2
- Immediate next stage: plan revision

## Review inputs

- Plan:
  `docs/plans/2026-07-29-stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Accepted proposal:
  `docs/proposals/2026-07-28-approved-specification-baselines-and-controlled-amendment-workflow.md`
- Approved specification:
  `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Approved spec review:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r6.md`
- Canonical architecture: `docs/architecture/system/architecture.md`
- Proposed ADR:
  `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md`
- Approved architecture review:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/architecture-review-r2.md`
- Boundary-first review method:
  `skills/plan-review/references/boundary-first-method-v1.md`
- Compatibility audit:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/compatibility-audit.md`

The matching test specification does not exist yet.
The plan correctly makes reviewed test-spec proof a precondition of M1.

## Findings

### SLA-PL1 - M4 grants implementation write scope over upstream artifacts

Finding ID: SLA-PL1
Severity: major
Location: M4 `Files/components likely touched`, `Implementation steps`, and
`Dependencies`; plan lines 335-372
Evidence: M4 lists `docs/plan.md`, all 32 approved reciprocal-notice
specifications, and dependent `specs/*.test.md` files as implementation
surfaces. Those are plan-, spec-, and test-spec-owned governed artifacts.
The same milestone later says stale proof maps must be updated through
`test-spec`, not implementation, and its dependency says those revisions must
already be reviewed before implementation relies on them. Allowing M4 to
touch these files contradicts SLA-R014 through SLA-R020, SLA-R027,
SLA-R042 through SLA-R047, SLA-R072 through SLA-R074e, BND-AUTH-001,
BND-COMPAT-001, INT-005, and the plan's own fixed-write-boundary purpose.
Required outcome: Every implementation milestone must treat plans,
specifications, architecture records, ADRs, and test specs as read-only.
Required stale proof-map revisions must be completed by `test-spec` and
`test-spec-review` before M1 begins.
Safe resolution path: Remove `docs/plan.md`, reciprocal-notice specs, and
dependent test specs from M4's writable file list. Add them as explicit
read-only compatibility inputs. Move stale proof-map identification,
revision, and approval into one preimplementation test-spec gate. Keep M4
limited to migration code, validators, query behavior, fixtures, and semantic
audits that read those upstream sources without modifying them.
needs-decision rationale: none

### SLA-PL2 - The activation milestone has no executable atomic cutover boundary

Finding ID: SLA-PL2
Severity: major
Location: Boundary ownership for BND-ENV-001 and INT-006; M5; Validation plan;
plan lines 129, 135, 389-456, and 515-520
Evidence: M5 combines generated package construction, canonical/generated
parity, the complete boundary-first end-to-end suite, behavior-preservation
evidence, and prospective marker activation in one implementation and rollback
unit. It says to enable marker creation but does not name the canonical source
that changes new and resumed workflow behavior from dormant support to active
marker writes. Earlier milestones already modify the workflow engine and
published workflow skill, so the plan does not prove which boundary keeps the
new writer unreachable before M5. M5 also lists
`python scripts/validate-adapters.py` without the required `--version`
argument; direct `--help` inspection confirms the bare command exits as invalid
usage. These gaps prevent BND-ENV-001 and INT-006 from closing independently
with executable proof and safe rollback.
Required outcome: Define one explicit atomic activation surface and a runnable
preactivation-to-cutover proof sequence. Generated parity and complete
preactivation proof must pass before the source that begins marker creation is
changed, and activation rollback must disable new marker creation without
restoring retired writers.
Safe resolution path: Split current M5 into a preactivation integration and
generated-parity milestone and a small atomic cutover milestone, then renumber
lifecycle closeout. Keep the public writer disabled through the preactivation
milestone; name the exact workflow/state initializer or canonical public
surface changed by cutover; run versioned temporary adapter generation and
`validate-adapters.py --root <temporary-output> --version <version>`; execute
the full boundary and broad-smoke gates before cutover; then run focused
post-cutover marker, status, cancellation, verify-stop, and external-action
containment proof. If one implementation milestone is retained, it must still
define separate preactivation and cutover commits, exact activation owner,
executable versioned commands, and rollback between them.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| Self-contained context | pass | The plan names governing artifacts, current components, state owners, non-goals, requirements, risks, commands, and downstream gates. |
| Source alignment | block | M4's writable scope contradicts the approved prohibition on downstream modification of plan, spec, and test-spec artifacts. |
| Milestone size | block | M5 combines generated packaging, complete integration proof, evidence authoring, and production activation in one rollback unit. |
| Sequencing | block | Stale test-spec revision is simultaneously a pre-M1 gate and an M4 implementation surface; activation has no named dormant-to-active source transition. |
| Scope discipline | block | M4 permits writes outside implementation ownership even though the overall non-goals and architecture correctly prohibit them. |
| Validation quality | block | The adapter validation command is not executable as written, and no focused post-cutover command proves the activation transition. |
| TDD readiness | concern | Each boundary has a named proof milestone, but BND-ENV-001 and INT-006 cannot close independently until cutover proof is split and executable. |
| Risk coverage | concern | Migration and partial rollout risks are identified, but the mechanism that keeps public marker creation disabled before cutover is not. |
| Architecture alignment | block | Component ownership is otherwise aligned; upstream artifact writes and an unnamed activation owner violate the stage-owned component boundary. |
| Operational readiness | block | The final implementation milestone cannot be closed reliably with the current command and cutover definition. |
| Plan maintainability | pass | Stable plan intent, requirements, boundary IDs, dependencies, rollback notes, and change-local state pointers are easy to navigate. |

## Missing milestones or dependencies

- A preimplementation test-spec migration gate that owns all stale dependent
  proof-map revisions before M1.
- A preactivation integration/parity milestone that leaves public marker
  creation disabled.
- An atomic cutover milestone naming the exact marker-creation owner,
  executable versioned adapter commands, focused post-cutover proof, and
  rollback boundary.

## Exact suggested edits

1. Make M4's approved specs, plan index, and dependent test specs read-only
   inputs; keep its writable scope in migration code, validators, and fixtures.
2. State that `test-spec` and `test-spec-review` complete the stale-proof audit
   and every required proof-map revision before M1.
3. Split M5 into preactivation generated parity/integration proof and atomic
   activation, then move lifecycle closeout to the next milestone number.
4. Name the exact source changed by atomic activation and the invariant that
   keeps marker creation disabled beforehand.
5. Replace the bare adapter validator command with versioned temporary-output
   generation and validation, and add focused post-cutover commands.
6. Update requirement, boundary, interaction, dependency, validation, decision
   log, and remaining-gate mappings to the revised milestone numbers.

## Recommendation

Changes requested.

Revise the plan, record dispositions for SLA-PL1 and SLA-PL2, validate the
revised plan, and rerun plan-review before test-spec authoring.

This direct review is isolated.
It does not edit the plan, start test-spec, authorize implementation, or
advance workflow routing.
