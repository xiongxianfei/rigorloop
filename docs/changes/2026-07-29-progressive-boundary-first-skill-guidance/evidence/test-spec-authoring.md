# Progressive Boundary-First Skill Guidance Test-Spec Authoring

Evidence ID: progressive-boundary-first-test-spec-authoring
Artifact ID: test-spec
Stage: test-spec
Artifact: `specs/progressive-boundary-first-skill-guidance.test.md`
Owning change record:
`docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`
Completion status: complete
Resulting review-request path:
`docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/test-spec-review-r2.md`

## Inputs

- Approved feature specification:
  `specs/progressive-boundary-first-skill-guidance.md`
- Approved specification review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/spec-review-r1.md`
- Approved canonical architecture:
  `docs/architecture/system/architecture.md`
- Accepted resource-composition ADR:
  `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`
- Approved architecture review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/architecture-review-r2.md`
- Approved execution plan:
  `docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Approved plan review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/plan-review-r2.md`
- Boundary-first proof method:
  `skills/test-spec/references/boundary-first-method-v1.md`

## Authoring result

The revised test spec maps all 38 feature requirements, 16 acceptance
criteria, six examples, 17 edge cases, 16 approved boundaries, and five
selected interactions to 16 stable automated test cases and 23 staged proof
obligations.

Proof is grouped by distinct observable outcome and material hazard rather
than by every possible combination.
The four implementation milestones retain separate proof, evidence, review,
and rollback boundaries.
The repository-live activation state remains `pending`; active behavior is
tested only through isolated candidate fixtures.

The validation ledger assigns stable command IDs to every named command,
records current ownership and first required milestone, defines failure and
zero-test behavior, and keeps package proof local, temporary, and
non-publishing.
No manual proof or uncovered gap remains.

## Test-spec-review R1 resolution

`PBS-TSR1` is addressed without changing the feature contract, architecture,
plan, test-case count, or implementation scope.

- T4 now proves the pending, active, grandfathered non-substantive, and
  grandfathered substantive guidance matrix during M2.
- `BND-COMPAT-001` and `INT-004` each have an M2 guidance obligation and a
  separate M4 state-composition obligation.
- CMD2 is now required by the M2 milestone proof row, matching the approved
  plan.
- T3 and T13 remain responsible for M4 activation, package, compatibility,
  and rollback composition.

## Authoring checks

- The test spec uses the normative test-spec and repeated-row assets.
- Every boundary and interaction ID is copied from the approved feature spec.
- Every implementation milestone maps test IDs, command IDs, evidence, and a
  code-review gate.
- Existing scripts and adapter version `v0.1.5` were inspected for command
  feasibility; validation commands were not executed during authoring.
