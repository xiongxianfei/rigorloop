# ADR-20260729: Stage-Owned Change-Local Lifecycle State

## Owning change record

`docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml`

## Context

RigorLoop currently distributes mutable lifecycle meaning across governed
artifacts, plan handoff sections, plan indexes, review evidence, workflow
automation state, and derived projections.
Some downstream stages also update upstream status or progress fields.
That makes reviewed files unstable and creates competing current-state owners.

ADR-20260721 consolidated three automation profiles into one target-driven
mechanism, but retained active-plan live-state ownership, parent
authorizations, effective capabilities, a typed policy projection, and
receipt-heavy automation state.
Those layers are unnecessary for the selected portable published-skill model.

The approved feature specification requires:

- stable governed artifacts;
- peer authoring and review stages;
- transition-scoped lifecycle writes;
- workflow-owned routing;
- one repository-local target without another public authorization layer;
- conservative replay after upstream revision; and
- prospective migration without hashes or writer attribution.

## Decision

For a change declaring
`lifecycle_contract: stage-owned-change-local-v1`, use
`docs/changes/<change-id>/change.yaml` as the sole mutable lifecycle-state
surface.

Partition that state into:

- `artifact_states`, keyed by stable artifact ID, for proposal, spec,
  architecture, ADR, plan, and test-spec lifecycle settlement;
- `workflow_state`, for current stage, next stage, blocker, planned work,
  review occurrence, and final-closeout readiness; and
- one structured automation target for the selected repository-local stopping
  point.

Assign write authority by transition:

- an authoring peer writes its governed artifact, authoring evidence, and only
  its matching transitions into `authoring` and `review-required`;
- a review peer writes durable review evidence and only the matching
  settlement transition;
- `plan` initializes missing planned-work state once from a new primary plan;
- `workflow` writes routing and every later planned-work transition only;
- implementation and later stages write only their code or stage-owned
  evidence; and
- every stage treats another stage's artifact and state entry as read-only.

One `$workflow auto: <target>` invocation is sufficient consent for the
repository-local prerequisite stages through that target.
Before each invocation, workflow validates current prerequisites, the exact
artifact or milestone identity, and the invoked stage's fixed write boundary.
The design has no parent-authorization, effective-capability,
activation-selector, risk-profile, or selector-ledger layer.

Review evidence precedes settlement.
An interrupted identical settlement is idempotently reconcilable by the
matching review peer.
Workflow pauses on incomplete or contradictory settlement and never creates a
review verdict.

When a downstream stage discovers an upstream defect, it records the problem
in its own evidence and routes back to the owner.
The owner revision and fresh peer review precede conservative downstream
replay.

Validation checks closed values, legal transitions, evidence consistency,
routing consistency, open blockers, prospective migration, and generated
adapter parity.
It does not use governed-document hashes, protected-path interception, or
claims about which process physically wrote a file.

The mechanism remains repository-local and stops before PR creation, push,
publication, release, deployment, merge, credentials, destructive Git, or
other external mutation.

## Supersession

When accepted, this ADR supersedes the state-placement, plan-owned live-state,
parent-authorization, effective-capability, and typed-policy decisions in:

- `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md`.

It retains that ADR's decisions for:

- one writable target-driven mechanism;
- structured target and occurrence binding;
- formal review independence;
- evidence-first interrupted-work recovery;
- dual-read and single-write migration;
- cancellation evidence preservation; and
- the human-controlled PR and external-action boundary.

The three earlier profile ADRs already superseded by ADR-20260721 remain
historical.

## Alternatives Considered

### Keep plan-owned live state and synchronize projections

Rejected because synchronization preserves multiple mutable surfaces and
continues to require downstream plan updates.

### Keep the two-level authorization and capability model

Rejected because the fixed published-skill write boundary plus current
prerequisite validation provides the required repository-local safety with
less public and implementation complexity.

### Put approval status back into governed artifacts

Rejected because review would need to edit its target or workflow would need
to manufacture settlement, making the reviewed file unstable.

### Add hashes or protected-path interception

Rejected because the first version needs portable stage guidance and semantic
state validation, not deterministic process attribution.

### Add selective downstream reuse after revision

Rejected for the first version because conservative replay is simpler and
does not require a dependency-analysis subsystem.

## Consequences

- Governed artifacts and plans become stable downstream inputs.
- `change.yaml` becomes a shared state surface with narrowly partitioned
  transition ownership.
- Review skills can settle their gate during independent invocation without
  editing the reviewed artifact or advancing routing.
- Workflow can continue automatically after settlement without another public
  authorization parameter.
- Published skills become the primary ownership contract; scripts validate
  structured consistency and generated parity.
- Existing plan projections, profile state, capabilities, selectors, and
  artifact-local statuses remain compatibility inputs only after migration.
- Conservative replay may repeat unaffected downstream work.
- Guidance and review can detect unauthorized upstream changes, but the design
  intentionally does not prove actor attribution.
- No service, database, background scheduler, new dependency, or deployment
  target is introduced.

## Follow-up

- Run `architecture-review` on this ADR, the affected canonical arc42
  sections, and the workflow component and container diagrams.
- After approval, settle this ADR through the owning change record and record
  ADR-20260721 supersession without rewriting its historical rationale.
- Create an execution plan that sequences schema, published-skill, workflow,
  validation, migration, fixture, and generated-adapter changes.
- Create a boundary-first test specification covering every governing
  requirement, boundary, selected interaction, illegal transition, unknown
  value, retry, and migration case.
