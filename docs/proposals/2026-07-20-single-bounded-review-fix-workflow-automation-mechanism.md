# Single Bounded Review-Fix Workflow Automation Mechanism

## Status

accepted

## Problem

RigorLoop currently implements workflow automation through three separately evolved mechanisms:

- `authoring-through-plan-review` for proposal-gated authoring;
- `bounded-review-fix` for proposal-side target-driven authoring and review correction;
- `implementation-through-verify` for test-spec settlement, implementation, code review, explanation, and verification.

These mechanisms preserve important safety boundaries, but they represent automation state, authorization, resumption, stopping, and reporting differently.
The differences make the workflow harder to explain, validate, extend, and resume than the underlying lifecycle requires.

Adding another automated boundary currently encourages another profile, another state shape, and another set of routing rules.
That increases the risk of contradictory state ownership, inconsistent failure behavior, duplicate transition logic, and drift between public skills, specifications, validators, and examples.

The problem is therefore not primarily command naming.
It is that `bounded-review-fix` is currently limited to the proposal-side path instead of serving as the one automation mechanism that moves toward a declared lifecycle target, applies stage-specific policy, and requires new authorization when the risk class changes.

## Goals

- Establish `bounded-review-fix` as the only target-driven workflow automation mechanism for all supported lifecycle automation.
- Retire `authoring-through-plan-review` and `implementation-through-verify` as mechanisms for new automation runs.
- Represent requested target, authorization, pause, cancellation, evaluation evidence, and completion consistently.
- Preserve the active plan as the canonical owner of current milestone and next-stage state.
- Separate the desired target from the authority currently granted to reach it.
- Preserve distinct authorization boundaries for artifact authoring, implementation, verification, and external actions.
- Preserve formal review independence, requirement-fidelity gates, review recording, and bounded correction behavior.
- Include `proposal-review` as a first-class public target without requiring a proposal to be approved before it can be reviewed.
- Preserve stage-specific authority over what counts as a safe correction.
- Make interruption and resumption idempotent across the full supported lifecycle.
- Fail closed on unknown stages, statuses, authorization classes, capability kinds, outcomes, or contradictory state.
- Support existing public command forms through adapters during migration.
- Preserve historical workflow metadata without rewriting completed change records.
- Reduce future automation additions to `bounded-review-fix` stage-policy and transition-registry changes rather than new end-to-end profile state machines.

## Non-goals

- Do not authorize implementation merely because authoring automation was authorized.
- Do not create one blanket proposal-to-verify permission.
- Do not make change metadata the owner of live milestone, next-stage, review, branch-readiness, or PR-readiness state.
- Do not weaken proposal, spec, architecture, plan, test-spec, code-review, explain-change, or verify gates.
- Do not make review skills edit the artifacts they are reviewing in the same undifferentiated pass.
- Do not change reviewer-owned implementation correction classification or driver-owned proposal-side correction classification without a separate contract decision.
- Do not automatically repair verification failures.
- Do not automatically open a PR, push, publish, release, deploy, merge, or perform destructive Git operations.
- Do not add background execution, a hosted workflow service, or an external scheduler.
- Do not make automation a repository-wide default.
- Do not require a public command rename in the first slice.
- Do not invalidate historical `authoring-through-plan-review`, `bounded-review-fix`, or `implementation-through-verify` evidence.
- Do not preserve the retired profiles as alternative writable automation mechanisms after migration.
- Do not expand bugfix or isolated manual skill invocations into workflow-managed automation by default.

## Vision fit

fits the current vision

RigorLoop is intended to make AI-assisted work traceable, resumable, and reviewable in Git.
A single evidence-driven automation mechanism improves resumption and auditability while keeping human authorization attached to meaningful risk boundaries.

The proposal would conflict with the vision if unification made automation less inspectable, collapsed human judgment into blanket consent, obscured which stage owned a decision, or required a hosted control plane.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Standardize workflow automation | in scope | Goals, Recommended direction |
| Standardize the mechanism rather than only the command name | in scope | Problem, Recommended direction |
| Support automation through implementation, code review, and verify | in scope | Expected behavior changes |
| Preserve safe implementation authorization | in scope | Parent authorizations, effective capabilities, and checkpoints |
| Avoid separate automation state machines for each lifecycle boundary | in scope | Single transition engine |
| Make `bounded-review-fix` the only automation mechanism | in scope | Recommended direction |
| Remove public `auto-through` naming immediately | out of scope | Non-goals, Rollout and rollback |
| Preserve existing safety and review behavior | in scope | Stage-policy preservation, Testing and verification strategy |
| Keep PR and stronger external actions human-controlled | in scope | Non-goals, External-action boundary |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Expand `bounded-review-fix` into the single target-driven automation engine | core to this proposal | This is the mechanism being standardized. |
| Single durable `bounded-review-fix` authorization and run evidence | core to this proposal | Resume and audit behavior need one representation. |
| Risk-scoped parent authorizations and effective capabilities | core to this proposal | Mechanism unification must not collapse human checkpoints. |
| Stage transition and policy registry | core to this proposal | The engine needs a consistent way to select stage behavior. |
| Active-plan state ownership preservation | same-slice dependency | A new automation record cannot become competing workflow truth. |
| Review independence and correction policy preservation | same-slice dependency | Existing automated review safety is part of compatibility. |
| Legacy profile read compatibility | same-slice dependency | Active and historical change records must remain interpretable. |
| New-record single-write migration | core to this proposal | Two writable mechanisms would recreate drift. |
| Workflow specs, architecture, ADR, skills, schemas, and validators | same-slice dependency | The mechanism is cross-component and contract-visible. |
| Generated adapter verification | same-slice dependency | Public skill behavior must remain aligned with canonical sources. |
| Immediate removal of public `auto-through` commands | deferable follow-up | Command spelling is separable from mechanism ownership. |
| `implement` and `code-review` target semantics | same-slice dependency | A single stage-target mechanism needs unambiguous milestone-local stopping behavior. |
| Non-circular `proposal-review` authorization | same-slice dependency | The first review needs identity-bound review authority before a clean proposal gate exists. |
| Automatic PR or external-action execution | out of scope | These actions retain separate human authority. |
| Hosted or asynchronous automation runtime | out of scope | RigorLoop remains repository-local and interaction-driven. |

## Context

The accepted workflow contracts deliberately introduced automation in bounded slices.
That sequencing produced strong safety properties:

- proposal-gated authoring cannot imply implementation authority;
- proposal-side review-fix automation stops no later than `test-spec-review`;
- implementation automation is separately authorized and phase-gated;
- every implementation milestone receives independent code review;
- correction loops are bounded and fail closed;
- verification requires fresh evidence and does not auto-repair failures;
- PR and stronger external actions remain outside automation.

Those properties should remain.
What should change is the duplication of orchestration and persistence concepts across separate profiles.

The active plan `Current Handoff Summary` already owns the live workflow position for planned initiatives.
Change-local automation metadata should continue to provide authorization, evaluation, pause, cancellation, and audit evidence without becoming a second next-stage owner.

The current architecture, workflow specs, and ADRs explicitly describe separate profiles.
This proposal therefore changes durable workflow architecture and requires approved spec amendments, architecture review, and an ADR that supersedes the profile-specific mechanism decisions without erasing their historical rationale.

## Options Considered

### O0: Keep the existing mechanisms

Continue maintaining the three existing profiles independently.

Benefits:

- No compatibility migration.
- Existing behavior and proof remain unchanged.

Costs and risks:

- New automation boundaries continue to encourage new profiles.
- State, resume, status, cancellation, and validation behavior can drift.
- Contributors must understand several mechanisms before extending one lifecycle.

This option is reasonable if no further automation is expected.
It is not recommended because the current direction explicitly seeks broader, consistent automation.

### O1: Add a shared command dispatcher over existing mechanisms

Normalize public commands and dispatch each target to an existing profile.

Benefits:

- Small implementation scope.
- Low immediate migration risk.
- Public behavior can look consistent.

Costs and risks:

- The underlying state machines remain duplicated.
- Status, resume, authorization, and stop behavior remain profile-specific.
- The main mechanism problem is hidden rather than solved.

This option is useful as a temporary compatibility layer but not as the target architecture.

### O2: Make `bounded-review-fix` the single target-driven engine

Evolve `bounded-review-fix` into the one automation run model and transition evaluator.
Keep stage-specific safety behavior in policy modules selected by the next lifecycle transition.

Benefits:

- One model for target, authorization, pause, cancellation, resume, and audit evidence.
- Existing safety boundaries can remain distinct.
- Future stages extend a registry and policy set rather than adding an end-to-end profile.
- Historical command forms can remain adapters.
- Validation can use one closed vocabulary and transition matrix.

Costs and risks:

- Requires coordinated spec, architecture, schema, validator, skill, and fixture changes.
- Migration must prove behavioral equivalence for three existing mechanisms.
- Poor state ownership design could compete with the active plan.

Recommended.

### O3: Build a fully declarative workflow graph immediately

Represent all stages, prerequisites, transitions, review gates, correction policies, and permissions in a data-defined graph interpreted by a generic engine.

Benefits:

- Strong long-term extensibility.
- Potential for complete transition-matrix generation and visualization.

Costs and risks:

- High initial design and validation burden.
- Stage semantics are not uniform enough to make all behavior safely declarative today.
- A large abstraction could conceal important review and ownership rules.

This is a possible later evolution after O2 proves the stable common fields.

### O4: Use one continuous proposal-to-verify authorization

Let one early invocation authorize every automatic transition through verification.

Benefits:

- Lowest interaction count.
- Simple apparent user model.

Costs and risks:

- Implementation can be authorized before its plan, commands, affected paths, and tests are known.
- Human checkpoints become ceremonial rather than authoritative.
- A single stale authorization has excessive scope.

Rejected.

## Recommended Direction

Adopt O2: make `bounded-review-fix` the only workflow automation mechanism, backed by stage-policy modules, risk-scoped parent authorizations, and stage-bound effective capabilities.

`authoring-through-plan-review` and `implementation-through-verify` should stop being mechanisms that can own newly authorized runs.
Their safety rules should move into `bounded-review-fix` stage policies, and their historical records should remain readable through compatibility projection.

### Single bounded-review-fix run

Each change should have at most one active `bounded-review-fix` run.
The run records:

- a structured target containing a closed stage, occurrence identity, and completion predicate;
- automation status;
- change identity;
- bounded parent authorizations and identity-bound effective capabilities;
- cancellation and pause evidence;
- the identities of workflow artifacts used by the latest transition evaluation;
- write-ahead transition receipts sufficient for audit, reconciliation, and idempotent resume.

An illustrative shape is:

```yaml
workflow:
  automation:
    mechanism: bounded-review-fix
    version: 2
    run_id: bounded-review-fix-run-001
    status: active
    change_id: 2026-07-20-example
    target:
      stage: verify
      occurrence:
        kind: final
      completion:
        verification: passed
    parent_authorizations:
      authorization-authoring-001:
        authorization_id: authorization-authoring-001
        authorization_class: authoring
        status: active
        policy_version: 1
        change_id: 2026-07-20-example
        authorized_by: user
        authorized_at: "2026-07-20T00:00:00Z"
        maximum_scope:
          target:
            stage: test-spec-review
            occurrence:
              kind: singleton
          capability_kinds: [proposal-review, proposal-correction, post-proposal-authoring]
          affected_path_roots: [docs/proposals/, specs/, docs/architecture/, docs/changes/2026-07-20-example/]
          mutation_categories: [change-local-review-evidence, proposal-content, downstream-authoring-artifacts]
          correction_budget:
            max_cycles_per_review: 2
            max_findings_per_cycle: 5
            max_changed_files_per_cycle: 3
        revocation:
          revoked: false
          revoked_by: null
          revoked_at: null
        invalidation:
          on_change_identity_mismatch: pause
          on_policy_change: pause
          on_scope_expansion: pause
    effective_capabilities:
      capability-proposal-review-001:
        capability_id: capability-proposal-review-001
        capability_kind: proposal-review
        parent_authorization_id: authorization-authoring-001
        status: active
        policy_version: 1
        change_id: 2026-07-20-example
        derived_at: "2026-07-20T00:01:00Z"
        stage:
          name: proposal-review
          occurrence:
            kind: singleton
        basis:
          proposal_identity: sha256:example-proposal
        scope:
          mutation_categories: [change-local-review-evidence]
        invalidation:
          on_parent_revocation: invalidate
          on_proposal_identity_change: invalidate
          on_policy_change: pause
          on_scope_expansion: pause
    external_actions: prohibited
    in_flight_transition: none
    last_evaluation:
      evidence: docs/changes/2026-07-20-example/change.yaml
    stop_before: pr
```

The later spec and architecture should define the exact schema.
The example establishes ownership and separation, not final field names.

The neutral persisted namespace separates the canonical automation record from its mechanism identifier.
It does not create a second mechanism: `workflow.automation.mechanism` has the single writable value `bounded-review-fix` in this proposal.
Legacy `workflow.autoprogression` records remain compatibility inputs only.

### Target and authority are independent

The structured `target` describes the requested stopping boundary.
It does not imply that the engine currently has authority to cross every intervening boundary.

For example, a run may target `verify` while holding only authoring authority.
It can progress through approved authoring stages and then pause at the implementation boundary.
The user can authorize implementation after the plan, test spec, validation commands, working-tree baseline, and affected scope are concrete.

The expanded `bounded-review-fix` mechanism should recognize these risk-scoped authorization classes:

| Authorization class | Maximum authority |
| --- | --- |
| `authoring` | Identity-bound proposal review, eligible proposal-side corrections, and post-proposal authoring through test-spec review. |
| `implementation` | Ordered milestones, tests, production changes, milestone code reviews, and eligible review-driven corrections. |
| `verification` | Final explanation and fresh verification after implementation closeout. |

Authorization should be change-local, explicit, durable, and narrow enough that the authorized scope is already knowable.
An earlier parent authorization or effective capability never implies a later risk-class authorization.

Within one risk class, a user may provide a bounded parent authorization that declares the maximum target, stage family, artifact roots, mutation categories, and correction budget.
The parent authorization is durable user consent, not executable mutation authority.
The engine materializes an effective capability only after that capability's concrete stage-appropriate basis exists, and the capability may never exceed the parent authorization.
This derivation cannot cross from authoring into implementation, verification, or external actions.

External actions are not an authorization class in the first mechanism version.
The automation record stores the closed value `external_actions: prohibited`; a future proposal is required before external actions can become grantable.

### Two-level authorization contract

The mechanism distinguishes bounded parent authorization from effective capability.

A bounded parent authorization records explicit user consent and the maximum scope available within one risk class.
It is not executable mutation authority.

An effective capability authorizes one concrete stage operation.
It is derived from one active parent authorization and binds to a complete stage-appropriate basis.

The common invariant is:

```text
effective capability
=
valid parent authorization identity
+
complete stage-appropriate basis
+
scope no broader than the parent authorization
```

Review identities are required only when the applicable stage policy can legitimately require an existing review.

Every bounded parent authorization records:

- authorization ID and class;
- policy version;
- change ID;
- authorizer and authorization time;
- maximum structured target;
- allowed capability kinds;
- maximum path and mutation scope;
- correction budget where applicable;
- status and revocation state;
- invalidation behavior.

Every effective capability records:

- capability ID and kind;
- parent authorization ID;
- policy version and change ID;
- stage and occurrence;
- stage-appropriate basis identities;
- actual bounded mutation scope;
- derivation time and status;
- invalidation behavior.

Only effective capabilities authorize stage execution or mutation.

An illustrative implementation capability is:

```yaml
capability-implementation-M2-001:
  capability_id: capability-implementation-M2-001
  capability_kind: implementation
  parent_authorization_id: authorization-implementation-001
  status: active
  policy_version: 1
  change_id: 2026-07-20-example
  derived_at: "2026-07-20T00:01:00Z"
  stage:
    name: implement
    occurrence:
      kind: milestone
      milestone_id: M2
  basis:
    plan:
      path: docs/plans/2026-07-20-example.md
      identity: sha256:example-plan
    plan_review_id: plan-review-r2
    test_spec:
      path: specs/example.test.md
      identity: sha256:example-test-spec
    test_spec_review_id: test-spec-review-r1
  scope:
    milestones: [M1, M2]
    mutation_categories: [tests, production-code, change-local-evidence]
    affected_path_roots: [scripts/, tests/]
    validation_commands_identity: sha256:example-command-set
  invalidation:
    on_basis_change: pause
    on_review_staleness: pause
    on_scope_expansion: pause
    on_policy_change: pause
```

The exact identity algorithm belongs in the spec.
The binding principle is settled here: a material basis, review, milestone, path, mutation-category, command, proof-obligation, canonical-state, or incompatible policy change pauses or invalidates the effective capability before further mutation.

Capability-specific minimum bases are:

| Capability | Minimum stage-appropriate basis | Review identity required? |
| --- | --- | --- |
| `proposal-review` | Change identity, exact reviewable proposal identity, standing artifact gates, structured target, review policy, and review-evidence roots. | No. |
| `proposal-correction` | Exact reviewed proposal identity, review record, accepted finding set, classifier policy, proposal roots, and correction budget. | Yes. |
| `post-proposal-authoring` | Exact proposal identity, approved applicable proposal review, closed required review resolution, allowed stage range, structured target, artifact roots, and correction budget. | Yes. |
| `implementation@M<n>` | Approved plan and plan review, active test spec and approved test-spec review, milestone set, affected paths, mutation categories, and validation-command set. | Yes. |
| `verification` | Closed implementation milestones, clean final holistic code review, valid promotion evidence, current explanation inputs, and concrete branch-state verification inputs. | Yes. |

A capability may be derived only when:

- its parent authorization exists, is active, and has not been revoked;
- its capability kind and stage occurrence are inside the parent's maximum scope and target;
- its actual path roots, mutation categories, and correction budget are subsets of the parent maximums;
- its risk class matches the parent authorization class;
- its stage-appropriate basis is complete and current;
- its policy version is compatible;
- no conflicting active capability or transition exists.

Parent revocation, cancellation, supersession, change-identity mismatch, scope narrowing, or incompatible policy change pauses or invalidates all derived capabilities.
A basis, review, finding-set, occurrence, command, canonical-state, or required-scope change pauses or invalidates the affected capability.
Material scope expansion creates a new capability and, when it exceeds the parent envelope, requires a new parent authorization.

### Proposal-review bootstrap without circular authority

`proposal-review` is a first-class public target and is the only authoring capability that does not require a clean proposal gate.
Its effective capability binds to an exact reviewable proposal identity and permits only the invocation of the stage-owning review skill plus durable change-local review evidence.
It never permits proposal-content mutation, downstream authoring, implementation, verification, or external actions.

An illustrative effective capability is:

```yaml
capability-proposal-review-001:
  capability_id: capability-proposal-review-001
  capability_kind: proposal-review
  parent_authorization_id: authorization-authoring-001
  status: active
  policy_version: 1
  change_id: 2026-07-20-example
  derived_at: "2026-07-20T00:01:00Z"
  stage:
    name: proposal-review
    occurrence:
      kind: singleton
  basis:
    proposal:
      path: docs/proposals/2026-07-20-example.md
      identity: sha256:example-proposal
    standing_gates_identity: sha256:example-standing-gates
    review_policy_identity: sha256:example-proposal-review-policy
  scope:
    mutation_categories: [change-local-review-evidence]
    affected_path_roots: [docs/changes/2026-07-20-example/]
  prohibited_mutation_categories:
    - proposal-content
    - downstream-artifacts
    - implementation
    - verification
    - external-actions
```

Review and correction remain separate capabilities.
When proposal review requests changes, the review capability ends after recording its evidence.
An eligible correction uses a separate `proposal-correction` capability bound to the reviewed proposal identity, accepted finding set, deterministic safety classification, and remaining correction budget.
Any proposal-content change invalidates the prior review capability and review result for gate purposes; rereview binds a new `proposal-review` capability to the new proposal identity.

A clean review may satisfy the basis for a `post-proposal` authoring capability, but it does not create unrestricted authority.
The engine may derive that capability without another interaction only when the user's existing bounded parent authoring authorization already includes the later target, stage family, artifact roots, and mutation categories.
The derived capability records both the parent authorization identity and the clean proposal-review identity.
If either scope is missing, stale, ambiguous, or exceeded, the run pauses for authorization.

This is not a future-contingent effective capability: no post-proposal mutation capability exists before its proposal and review basis are concrete.
It is also not implicit risk escalation because derivation remains inside the already authorized authoring class.
Implementation and verification still require their own explicit durable parent authorizations and cannot be derived from parent authoring authority.

Implementation and verification always use separate durable parent authorizations and effective capabilities.
One user interaction may authorize both only when the complete prerequisites and basis identities for both effective capabilities already exist and validate independently at that moment.
The engine never records a future-contingent verification capability before implementation closeout, final-review evidence, promotion evidence, and verification inputs are concrete.

### Expanded target boundary

`bounded-review-fix` should own the supported automatic lifecycle path through `verify`:

```text
proposal-review
-> spec
-> spec-review
-> architecture and architecture-review when required
-> plan
-> plan-review
-> test-spec
-> test-spec-review
-> ordered implement and code-review loops
-> explain-change
-> verify
-> stop before pr
```

The public target-stage vocabulary is closed to:

```text
proposal-review
spec
spec-review
architecture
architecture-review
plan
plan-review
test-spec
test-spec-review
implement
code-review
verify
```

The following trigger or support stages may run internally but are not public targets in this proposal:

```text
proposal
architecture-assessment
review-resolution
ci-maintenance
explain-change
final-holistic-code-review
```

Public command aliases resolve to a structured target before authorization is persisted.
The target contains a stage, occurrence identity, binding time, and completion predicate.

For a milestone-local target:

```yaml
target:
  stage: code-review
  occurrence:
    kind: milestone
    milestone_id: M2
  bound_at: "2026-07-20T00:00:00Z"
  completion:
    review_status: approved
    review_resolution: closed
    milestone_state: closed
```

Singleton targets use `occurrence.kind: singleton`.
Final verification uses `occurrence.kind: final`.

### Proposal-review outcome semantics

A proposal-review occurrence is recorded when a formal review record is durably written against the exact bound proposal identity and contains one closed review outcome:

- `approved`;
- `changes-requested`;
- `blocked`;
- `inconclusive`.

Recording the review occurrence and satisfying the clean proposal gate are separate facts.
Only `approved` satisfies the clean proposal gate.

An illustrative review-result receipt is:

```yaml
review_result:
  occurrence_recorded: true
  review_id: proposal-review-r3
  reviewed_artifact_identity: sha256:example-proposal
  outcome: inconclusive
  clean_gate: not-satisfied
  routing_action: pause
  pause_reason: proposal-review-inconclusive
```

`clean_gate` is closed to `satisfied` and `not-satisfied`.
`routing_action` is closed to `continue`, `correction-loop`, `stop-at-target`, `pause`, and `fail-closed`.

| Outcome | Occurrence recorded | Clean gate | Exact `proposal-review` target | Later target |
| --- | --- | --- | --- | --- |
| `approved` | yes | satisfied | Stop successfully at the target. | Continue with a valid post-proposal capability; otherwise pause for authorization. |
| `changes-requested` | yes | not satisfied | Stop at the requested review target with findings. | Enter correction and rereview only with a valid correction capability and remaining budget; otherwise pause. |
| `blocked` | yes | not satisfied | Pause with the recorded blocker. | Pause without downstream continuation. |
| `inconclusive` | yes | not satisfied | Pause for missing or insufficient evidence. | Pause without downstream continuation. |
| unknown value | no valid occurrence | invalid | Fail closed. | Fail closed. |

When the explicit target is `proposal-review`, reaching the review occurrence reports the exact outcome and clean-gate state; it never reinterprets stage occurrence as proposal approval.
For `changes-requested`, proposal correction applies only accepted bounded fixes under a valid correction capability and remaining budget.
Correction changes the proposal identity, makes the prior review stale for gate purposes, and requires a new proposal-review capability and rereview.
Budget exhaustion, a new finding, or an owner-decision finding pauses.
`blocked` and `inconclusive` never enter an automatic correction loop and never continue downstream.
An inconclusive review is not rerun without a material input or evidence change.
An unknown review outcome fails closed and does not count as a valid recorded occurrence.

`implement@M<n>` completes only when the named milestone implementation exists, milestone-required validation passes, and the plan records that milestone as `review-requested`; it implies no code-review approval.

`code-review@M<n>` completes only when the named milestone-local code review is approved, required review-resolution is closed, and the plan records that milestone as closed or advanced according to plan policy.
The target remains bound to that milestone after interruption and never silently rebinds to a later milestone.

`verify` completes only after all implementation milestones close, final holistic code-review requirements pass, `explain-change` is current, and fresh verification succeeds.
It performs no PR or external action.

When architecture is not required, a later target records a `not-applicable` architecture transition and continues.
An explicit `architecture` or `architecture-review` target ends with `target-not-applicable` when architecture is not required.
Ambiguous architecture applicability pauses.

Reaching any target never skips its prerequisites, reviews, resolution, or state synchronization.

### Single transition engine

Every automatic transition should follow the same control flow:

```text
read canonical workflow state
-> identify the next valid stage toward the target
-> select the stage policy
-> verify prerequisites and artifact identities
-> verify the required parent authorization and effective capability
-> compute a stable transition key
-> persist a prepared transition receipt
-> invoke the stage-owning skill
-> inspect stage-owned completion evidence
-> synchronize canonical state
-> finalize the transition receipt
-> stop, pause, or continue
```

The engine should not replace specialized stage skills.
It coordinates them and validates their handoffs.

The prepared receipt is written before mutation because stage execution may update several Markdown and YAML artifacts that cannot be committed atomically.
An illustrative receipt is:

```yaml
transition_id: transition-0007
transition_key: sha256:example-transition-key
policy_version: 1
run_id: bounded-review-fix-run-001
change_id: 2026-07-20-example
from_position: test-spec-review
to_stage: implement
target:
  stage: code-review
  occurrence:
    kind: milestone
    milestone_id: M2
capability_id: capability-implementation-M2-001
input_identities:
  plan: sha256:example-plan
  test_spec: sha256:example-test-spec
  test_spec_review: review:test-spec-review-r1
expected_postcondition:
  milestone: M2
  milestone_state: review-requested
status: prepared
outputs: []
canonical_sync:
  status: pending
```

Receipt statuses are closed to `prepared`, `completed`, `failed`, `paused`, and `cancelled`.
Every stage policy declares exactly one retry policy: `idempotent-retry`, `reconcile-only`, or `manual-recovery`.
At most one transition may be in flight for one change.

Resume behavior is deterministic:

| Observed state | Required action |
| --- | --- |
| `prepared` with no completion evidence | Retry only for `idempotent-retry`; otherwise pause. |
| `prepared` with valid completion evidence | Reconcile outputs and canonical state without rerunning the stage. |
| `completed` with matching canonical state | Continue. |
| `completed` with different canonical state | Pause for explicit reconciliation. |
| More than one in-flight transition | Fail closed. |
| Unknown status or policy version | Fail closed. |
| Output identity changed after completion | Pause for explicit reconciliation. |

Partially written output never counts as stage completion merely because a path exists.
Resume checks stage-owned completion evidence before any retry.

### Stage-policy registry

The mechanism should use a closed registry of automatable stages.
Each stage policy describes:

- predecessor and applicability rules;
- required parent authorization class and capability kind;
- owning skill;
- permitted mutation category;
- required input identities;
- required completion and review evidence;
- next-stage calculation;
- correction-loop policy when applicable;
- stop and pause outcomes.

The first registry is an immutable typed Python registry using closed enums and frozen policy records.
Workflow specifications remain normative; the Python registry is their executable projection and receives exhaustive consistency tests.
A second hand-authored YAML or JSON stage registry is not introduced in the first mechanism version.
A generated declarative representation may be reconsidered after the common fields stabilize through real migration evidence.

### Stage-policy preservation

Expanding `bounded-review-fix` should preserve, rather than average, existing stage policies.

Proposal-side review-fix policy can retain driver-owned deterministic safety classification.
Implementation code-review policy can retain reviewer-owned `auto_fix_class` and the current mechanical or declared-safe correction contract.
Automated review can retain the independent adversarial and requirement-fidelity gates.

The engine standardizes how those policies are invoked, recorded, resumed, and stopped.
It does not claim that every stage has identical correction authority.

### Canonical state ownership

The automation mechanism does not own an independent workflow cursor.
Canonical workflow position has two deterministic epochs.

Before an active plan exists, position is derived through the closed stage-transition registry from:

- authoritative artifact existence and settlement state;
- the identity, status, and freshness of the latest applicable formal review;
- open review-resolution findings and closeout state;
- architecture applicability and the recorded architecture assessment;
- artifact identities and contradictions among governing sources.

The derivation produces a position for the current evaluation but does not persist `current_stage` or `next_stage` as automation-owned truth.
Multiple plausible positions, stale review evidence, or contradictory artifacts pause the run.

The canonical ownership handoff occurs when the plan artifact is created, passes required structural validation, has an active lifecycle state, and contains a valid `Current Handoff Summary`.
The transition receipt records the observed pre-plan identities and the validated plan identity at that handoff.

After that boundary, the active plan `Current Handoff Summary` is authoritative for:

- current milestone;
- milestone state;
- last reviewed milestone;
- review status;
- remaining implementation milestones;
- next stage;
- final-closeout readiness.

Automation metadata records only the identities it observed and receipts for transitions it prepared or attempted.
A mismatch between those identities and the canonical pre-plan derivation or active-plan state pauses before another transition.

### External-action boundary

The expanded `bounded-review-fix` engine stops before `pr` by default.
PR opening and stronger external actions remain explicit stage invocations with their existing authority and readiness checks.
Adding an automatic external-action authorization would require a separate proposal and spec amendment.

## Expected Behavior Changes

- Existing workflow automation entry points can route through the single `bounded-review-fix` transition engine.
- Status, pause, cancellation, target completion, and resume reporting become consistent across authoring and implementation work.
- A target beyond the current authorization boundary produces a precise authorization-required pause rather than selecting another profile.
- `proposal-review` can run against an exact proposal identity before a clean proposal gate exists, while mutating only change-local review evidence.
- A proposal review never edits the proposal it reviews; corrections and rereview use separate identity-bound capabilities.
- Continuation beyond proposal review requires a clean gate and a concrete post-proposal authoring capability derived within, and never beyond, the user's bounded authoring authorization.
- Authoring authorization does not permit implementation.
- Implementation authorization does not permit verification until its promotion and closeout evidence are satisfied.
- Verification authorization does not permit PR or external actions.
- Completed stages and clean reviews are not repeated merely because automation resumes.
- A stale artifact identity or contradictory canonical state pauses before mutation.
- Unknown target stages, authorization classes, capability kinds, statuses, outcomes, or stage-policy values fail closed.
- Existing public command forms can remain available as adapters during migration.
- Historical profile records remain readable and retain their original meaning.
- New automation capabilities extend the `bounded-review-fix` run and transition model instead of defining another end-to-end profile.
- New authorizations no longer create `authoring-through-plan-review` or `implementation-through-verify` records.

## Architecture Impact

This proposal changes a durable cross-component workflow architecture decision.
Architecture assessment should record `architecture-required`.

Expected affected boundaries include:

| Surface | Expected impact |
| --- | --- |
| Workflow orchestration | Expand `bounded-review-fix` and replace profile-specific transition evaluators with its target-driven evaluator. |
| Workflow state synchronization | Derive pre-plan position, hand ownership to the validated active plan, and check canonical state before and after every automated transition. |
| Change metadata | Add neutral `workflow.automation` state with `mechanism: bounded-review-fix` while retaining legacy `workflow.autoprogression` reads. |
| Stage-policy registry | Centralize closed stage routing, authorization class, evidence, and stop behavior. |
| Review gates | Preserve independence, fidelity, recording, correction, and rereview policies behind stage adapters. |
| Workflow specifications | Replace profile-specific mechanism requirements with single-`bounded-review-fix` requirements and compatibility mappings. |
| Architecture package and ADRs | Supersede the separate profile mechanism while preserving their safety decisions. |
| Canonical skills | Align workflow and affected stage skills with single-mechanism handoff semantics. |
| Validators and fixtures | Validate closed vocabularies, transitions, parent authorizations, effective capabilities, migration, and equivalence. |
| Public adapters | Verify generated release archives contain aligned canonical guidance. |

No new service, database, scheduler, hosted agent, dependency, or deployment boundary is expected.

## Testing and Verification Strategy

The later test specification should combine structural, fixture-driven, integration, and behavior-preservation proof.

| Check ID | What is proved |
| --- | --- |
| `UWA-001` | At most one `bounded-review-fix` automation run is active for a change. |
| `UWA-002` | Unknown target stages fail closed before transition evaluation. |
| `UWA-003` | Unknown statuses, authorization classes, and capability kinds fail closed. |
| `UWA-004` | Target stage does not imply authorization for intervening risk classes. |
| `UWA-005` | Authoring can progress toward a later target and pauses before implementation without an implementation parent authorization and effective capability. |
| `UWA-006` | Implementation activates only from clean, synchronized planning and test-spec evidence. |
| `UWA-007` | Verification activates only after required implementation closeout, final holistic review, and promotion evidence. |
| `UWA-008` | External actions remain prohibited to automatic parent authorizations and effective capabilities. |
| `UWA-009` | Pre-plan position derives from authoritative artifacts and reviews, then ownership hands to the validated active plan. |
| `UWA-010` | Resume does not recreate completed artifacts or rerun clean reviews without a rereview trigger. |
| `UWA-011` | Proposal-side correction authority remains driver-owned and bounded. |
| `UWA-012` | Implementation correction authority remains reviewer-owned and bounded. |
| `UWA-013` | Automated code review retains independence and requirement-fidelity gates. |
| `UWA-014` | New findings, non-shrinking correction sets, owner decisions, or budget exhaustion pause. |
| `UWA-015` | Verification failure pauses without automatic repair. |
| `UWA-016` | A prepared transition receipt exists before mutation and supports evidence-first reconciliation after interruption. |
| `UWA-017` | Historical authoring-profile records project to equivalent `bounded-review-fix` decisions. |
| `UWA-018` | Historical review-fix records project to equivalent expanded-format decisions. |
| `UWA-019` | Historical implementation-profile phases project to equivalent authorizations, capabilities, and stops. |
| `UWA-020` | New automation writes use only the expanded `bounded-review-fix` format. |
| `UWA-021` | Legacy and expanded `bounded-review-fix` evaluation produce equivalent routing for shared fixtures. |
| `UWA-022` | Existing public command adapters select the same `bounded-review-fix` run semantics. |
| `UWA-023` | Direct review and manual skills remain isolated by default. |
| `UWA-024` | Generated skill and adapter guidance remains deterministic and aligned. |
| `UWA-025` | Every new closed-vocabulary constant has an `unknown_value` or `not_in_vocabulary` regression. |
| `UWA-026` | New authorizations cannot write `authoring-through-plan-review` or `implementation-through-verify` profile state. |
| `UWA-027` | `implement` and `code-review` targets stop at the current approved milestone occurrence without confusing milestone-local review with final holistic review. |
| `UWA-028` | `proposal-review` authorizes review and durable review evidence against an exact proposal identity without requiring a prior clean proposal gate. |
| `UWA-029` | A proposal-review capability cannot mutate proposal content or create downstream artifacts. |
| `UWA-030` | Proposal correction invalidates the prior review for gate purposes and rereview binds to the new proposal identity. |
| `UWA-031` | A post-proposal authoring capability materializes only after clean review evidence exists and remains within its bounded parent authoring authorization. |
| `UWA-032` | Parent authoring authority cannot derive implementation, verification, or external-action capabilities. |
| `UWA-033` | A parent authorization alone cannot execute a stage or mutate an artifact. |
| `UWA-034` | A proposal-review capability with an exact proposal basis and no prior review identity is valid; one missing the proposal identity fails. |
| `UWA-035` | Proposal-correction and post-proposal capabilities fail when their required review identities are missing or stale. |
| `UWA-036` | A capability missing its parent, exceeding the parent target, expanding path or mutation scope, or crossing risk class fails closed. |
| `UWA-037` | Parent revocation or invalidation propagates to every active derived capability. |
| `UWA-038` | A changed capability basis pauses or invalidates that capability instead of mutating it into new scope. |
| `UWA-039` | All four closed proposal-review outcomes have deterministic exact-target and later-target routing. |
| `UWA-040` | A proposal identity change preserves historical review occurrence but makes its gate evidence stale and requires rereview. |
| `UWA-041` | An inconclusive review with no material evidence change remains paused and does not spin. |

Decision acceptance criteria are:

| ID | Criterion |
| --- | --- |
| `AC-BRF-031` | Pre-plan workflow position derives from authoritative artifacts, current formal reviews, review-resolution state, architecture applicability, and the closed transition registry. |
| `AC-BRF-032` | A validated active plan takes canonical ownership through a receipt-recorded handoff, and automation metadata never owns an independent `next_stage`. |
| `AC-BRF-033` | Every bounded parent authorization binds stable identity, authorization class, policy version, change ID, authorizer, maximum structured target, maximum scope, revocation state, and invalidation behavior. |
| `AC-BRF-034` | Material basis, review, milestone, path, mutation-category, command, proof-obligation, canonical-state, or incompatible policy change pauses or invalidates its effective capability. |
| `AC-BRF-035` | Every mutation transition persists a prepared receipt with deterministic identity, expected postcondition, and retry policy before stage invocation. |
| `AC-BRF-036` | Interrupted transitions inspect stage-owned completion evidence and reconcile before any retry; multiple in-flight transitions fail closed. |
| `AC-BRF-037` | Repeated-stage targets bind to a milestone ID and cannot silently rebind after resume. |
| `AC-BRF-038` | Milestone-local code review remains distinct from final holistic code review and final verification completion. |
| `AC-BRF-039` | Active legacy migration is one-way on first mutating resume; terminal history remains readable indefinitely and mixed writable state fails closed. |
| `AC-BRF-040` | Implementation and verification use separate parent authorizations and effective capabilities, and verification capability is never recorded before its concrete basis exists. |
| `AC-BRF-041` | `proposal-review` is a public singleton target with an identity-bound effective review capability that does not require a clean proposal gate. |
| `AC-BRF-042` | Proposal-review authority permits only review invocation and change-local review-evidence mutation, never proposal-content mutation. |
| `AC-BRF-043` | Proposal correction and rereview use separate capabilities, and a changed proposal identity makes prior review evidence stale for gate purposes. |
| `AC-BRF-044` | Post-proposal authoring authority materializes only from a concrete clean review basis and cannot exceed its bounded parent authoring authorization. |
| `AC-BRF-045` | Effective capability derivation cannot cross authoring, implementation, verification, or external-action risk classes. |
| `AC-BRF-046` | Every effective capability binds one parent authorization identity, one capability kind, one stage occurrence, one complete stage-appropriate basis, bounded actual scope, and invalidation behavior. |
| `AC-BRF-047` | Review identities are mandatory only when required by the applicable stage-policy basis. |
| `AC-BRF-048` | An effective capability cannot exceed its parent target, path roots, mutation categories, correction budget, or risk class. |
| `AC-BRF-049` | Revoking or invalidating a parent authorization pauses or invalidates all capabilities derived from it. |
| `AC-BRF-050` | A capability missing its parent authorization or using a stale parent identity fails closed. |
| `AC-BRF-051` | Review-occurrence recording and clean-gate satisfaction are represented separately. |
| `AC-BRF-052` | `approved` records the occurrence and satisfies the clean proposal gate. |
| `AC-BRF-053` | `changes-requested` records the occurrence but does not satisfy the gate. |
| `AC-BRF-054` | `changes-requested` enters correction only with a valid correction capability and remaining budget. |
| `AC-BRF-055` | `blocked` records the occurrence, does not satisfy the gate, and pauses. |
| `AC-BRF-056` | `inconclusive` records the occurrence, does not satisfy the gate, and pauses. |
| `AC-BRF-057` | Unknown review outcomes fail closed and do not count as a valid occurrence. |
| `AC-BRF-058` | A later target cannot continue unless the latest review of the current proposal identity is `approved`. |

Validation should begin with focused schema, state-sync, and routing fixtures, then expand through skill validation, generated-output checks, adapter validation, artifact lifecycle validation, review-artifact validation, and the repository-owned CI wrapper selected by the later plan.

## Rollout and Rollback

Use a dual-read, single-write migration.

During adoption:

- terminal historical legacy records remain readable indefinitely and side-effect free;
- active legacy records present at cutover are eligible for one-way migration on their first explicitly authorized mutating resume;
- the first mutating resume creates the expanded run, records a migration receipt, and makes the source legacy record read-only for that change;
- new automation authorizations write only the expanded `bounded-review-fix` format;
- existing public commands act as adapters to the `bounded-review-fix` engine;
- equivalence fixtures compare legacy routing with `bounded-review-fix` routing;
- mixed writable legacy and expanded state fails closed;
- completed historical records retain their original artifact meaning.

Active legacy-resume support ends only after a repository audit proves that no active legacy records remain to migrate.
Reading a legacy record never mutates it; projection becomes durable only on an explicitly authorized mutating resume.

An illustrative migration receipt is:

```yaml
migration:
  source_mechanism: implementation-through-verify
  source_record_identity: sha256:example-legacy-record
  projected_at: "2026-07-20T00:00:00Z"
  bounded_review_fix_run_id: bounded-review-fix-run-001
  projection_result: equivalent
```

The current `implementation-through-verify` phases should map to parent authorizations, effective capabilities, and evidence during compatibility reads:

| Legacy phase | `bounded-review-fix` interpretation |
| --- | --- |
| `A` | Audit evaluation only; no executable capability. |
| `B` | Implementation authorization and capability within the current ordered-milestone and review boundary. |
| `C` | Verification authorization and capability only when existing promotion evidence is valid. |

The current authoring profile maps to a bounded authoring parent authorization, stage-appropriate capabilities, and its original target boundary.
Existing review-fix records project through a versioned compatibility read while retaining their original proposal-side authority until the first mutating resume writes the new record.

Do not maintain two independent writable engines after expanded `bounded-review-fix` writes begin.
Legacy execution should be limited to projecting existing records into the common evaluator.

Rollback should disable creation and automatic continuation of expanded `bounded-review-fix` runs, leave their durable evidence intact, and return affected changes to explicit manual stage invocation.
Rollback should not manufacture retired profile records from expanded runs or delete formal reviews, resolutions, validation evidence, or completed artifacts.

Public command removal or renaming can occur later under a separately declared compatibility policy after the mechanism migration is stable.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| The expanded `bounded-review-fix` engine becomes blanket autopilot | Separate target, bounded parent authorization, and effective capability; prohibit implicit risk escalation. |
| Automation metadata competes with active-plan state | Store observed identities and receipts, not authoritative live next-stage state; pause on mismatch. |
| Stage-specific safety is lost in abstraction | Keep explicit stage-policy modules and behavior-preservation fixtures. |
| Migration changes historical meaning | Use dual-read projection without rewriting historical records. |
| Two writable mechanisms drift | Switch new authorizations to single-write `bounded-review-fix` state and keep legacy support read-only. |
| Unknown values fall through | Use closed vocabularies and explicit unknown-value regression tests. |
| Resume repeats work | Require stage completion evidence, input identities, and idempotent transition receipts. |
| Early authorization reaches unknown implementation scope | Require separate implementation authorization and effective capability only after planning and test-spec gates are concrete. |
| Review independence weakens | Preserve neutral review packets, phase receipts, risk-tier gates, and requirement-fidelity checks. |
| Proposal review requires its own approval and becomes circular | Bind a review-only effective capability to the exact proposal identity, then require a separate clean-gate-based capability for post-proposal authoring. |
| Parent authorization becomes disguised blanket authority | Treat it only as a maximum envelope; materialize identity-bound effective capabilities after concrete bases exist and prohibit derivation across risk classes. |
| Correction policy becomes overly generic | Keep proposal-side and implementation-side classification authority distinct. |
| Phase migration weakens rollout controls | Map legacy phases exactly and require equivalent promotion evidence before verification capability. |
| A recorded review is mistaken for approval | Store occurrence recording and clean-gate satisfaction separately and allow only `approved` to satisfy the gate. |
| Inconclusive review spins without new evidence | Pause with a stable reason and require material evidence change before reevaluation. |
| Public behavior changes unexpectedly | Keep command forms as adapters during mechanism rollout and document any later deprecation separately. |
| Rollback corrupts lifecycle evidence | Pause automation and fall back to explicit stages without deleting or reverse-converting evidence. |

## Open-question resolutions

### Stage-policy registry

The first stage-policy registry is an immutable typed Python registry.
Workflow specifications remain normative, and the registry is their exhaustively tested executable projection.
A second hand-authored data registry is not introduced in the first mechanism version.

### Legacy active resume

Migration uses a state-based compatibility window.
Terminal legacy records remain readable indefinitely.
Active legacy records migrate once on their first explicitly authorized mutating resume, after which the legacy state is read-only for that change.
New authorizations use only the expanded `bounded-review-fix` format, and active-resume compatibility ends only after an audit finds no active legacy records.

### Implementation and verification authorization

Implementation and verification always use separate durable parent authorizations and effective capabilities.
One interaction may authorize both only when the concrete prerequisites and basis identities for both effective capabilities already exist and validate independently.
Future-contingent verification capability is not recorded.

### Proposal-review authorization

`proposal-review` remains a public target inside `bounded-review-fix`.
It uses an identity-bound effective authoring capability whose basis is the exact reviewable proposal rather than a clean proposal gate.
That capability may invoke and record proposal review but cannot mutate proposal content or continue downstream.
Proposal correction and post-proposal authoring use separate effective capabilities.
A post-proposal capability may be derived without another interaction only from an existing bounded parent authoring authorization and only after its clean proposal and review basis exists; capability derivation never crosses into implementation, verification, or external actions.

### Proposal-review outcome routing

Review occurrence and clean-gate satisfaction are separate recorded facts.
All four closed outcomes are durable evidence.
Only `approved` satisfies the clean proposal gate.
`changes-requested` may enter correction only with a valid correction capability and remaining budget.
`blocked` and `inconclusive` pause without downstream continuation, and unknown outcomes fail closed.

## Open Questions

None.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-20 | Standardize the automation mechanism rather than only public command syntax. | Shared syntax over separate state machines would preserve the main maintenance and consistency problem. | Command-dispatch-only normalization. |
| 2026-07-20 | Make `bounded-review-fix` the only target-driven automation mechanism. | It already owns target-bounded workflow automation and review-fix loops, so expanding it avoids creating a fourth mechanism. | Existing separate mechanisms; a new generically named engine; immediate fully declarative graph. |
| 2026-07-20 | Separate requested target from granted authority. | A user can express an eventual destination without prematurely authorizing unknown implementation scope. | One blanket proposal-to-verify authorization. |
| 2026-07-20 | Preserve the active plan as live workflow-state owner. | The constitution and workflow contract already assign milestone and next-stage truth to the plan. | Automation record as a second live state machine. |
| 2026-07-20 | Preserve stage-specific review and correction authority. | Proposal-side artifacts and production-code findings have different safe-fix contracts. | One generic auto-fix classifier. |
| 2026-07-20 | Use dual-read, single-write migration. | Historical evidence must remain interpretable while new state converges on one mechanism. | Bulk historical rewrite; indefinite dual writes. |
| 2026-07-20 | Keep public command naming outside the first mechanism slice. | Command adapters can preserve compatibility while the underlying engine is replaced. | Immediate command removal as part of the architecture migration. |
| 2026-07-20 | Keep PR and stronger external actions outside automatic authorization. | Those effects require separate human authority and existing stage readiness checks. | Automation through PR or publication. |
| 2026-07-20 | Retire `authoring-through-plan-review` and `implementation-through-verify` for new writes. | A single mechanism requires one writable state model; their safety behavior can survive as stage policies and compatibility projections. | Multiple writable profiles behind a shared dispatcher. |
| 2026-07-20 | Derive canonical position from authoritative evidence before planning and hand ownership to the validated active plan. | The engine needs deterministic pre-plan routing without owning a competing cursor. | Automation-owned `current_stage`; plan ownership before a plan exists. |
| 2026-07-20 | Bind executable capabilities to concrete artifact identities and bounded mutation scope. | Status-only authority can outlive the evidence and scope the user actually approved. | Unbound `authorized` flags. |
| 2026-07-20 | Use write-ahead prepared transition receipts and evidence-first recovery. | Multi-artifact stage writes are not atomic and cannot be recovered safely from post-hoc receipts. | Receipt-only-after-completion; blind retry. |
| 2026-07-20 | Bind repeated targets to milestone occurrences and completion predicates. | A stage string can silently rebind after resume and cannot distinguish milestone-local from final review. | Bare `target_stage` for repeated stages. |
| 2026-07-20 | Persist new state under neutral `workflow.automation` with `mechanism: bounded-review-fix`. | The mechanism remains singular while its namespace accurately covers authoring, implementation, and verification. | Universal state under proposal-side `review_fix`; a second automation mechanism. |
| 2026-07-20 | Use a typed Python stage-policy registry first. | Executable predicates and closed enums need one testable projection while specifications remain normative. | A second hand-authored YAML or JSON registry. |
| 2026-07-20 | Migrate active legacy state once on first mutating resume. | State-based cutover preserves history and avoids indefinite dual-write behavior. | Calendar-only expiry; bulk history rewrite. |
| 2026-07-20 | Keep implementation and verification authorization separate. | Verification capability cannot exist before implementation closeout and final-review evidence are concrete. | Future-contingent verification capability. |
| 2026-07-20 | Include `proposal-review` through a review-only effective authoring capability bound to the exact proposal identity. | Requiring a clean proposal gate before its first review is circular, while letting review mutate the proposal would weaken independence. | Remove `proposal-review` from automation; let the review share an undifferentiated authoring grant. |
| 2026-07-20 | Derive post-proposal authoring capability only within a bounded parent authoring authorization after clean review evidence exists. | This supports uninterrupted authoring automation without persisting an effective grant before its concrete basis or crossing a risk boundary. | Blanket future grant; mandatory redundant confirmation after every clean authoring review. |
| 2026-07-21 | Use distinct bounded parent authorization and effective capability record types. | User consent defines a maximum envelope, while executable authority needs a current stage-specific basis and bounded actual scope. | One ambiguous grant schema; proposal-review-only exception wording. |
| 2026-07-21 | Require stage-appropriate basis identities rather than universal review identities. | Proposal review legitimately precedes its own review identity, while later capabilities still require applicable approved reviews. | Universal reviewed-basis invariant. |
| 2026-07-21 | Separate proposal-review occurrence recording from clean-gate satisfaction. | Formal evidence can exist for every closed review outcome, but only approval permits downstream authoring. | Treating every recorded review as approval; omitting `inconclusive`. |

## Next Artifacts

- `proposal-review`
- Amend `specs/workflow-stage-autoprogression.md`
- Amend `specs/rigorloop-workflow.md`
- Amend `specs/review-fix-autoprogression.md` and `specs/review-finding-resolution-contract.md` where compatibility requires it
- `spec-review`
- Architecture update to `docs/architecture/system/architecture.md`
- ADR establishing `bounded-review-fix` as the only writable automation mechanism and superseding the other profile-specific mechanism decisions while preserving their safety constraints
- `architecture-review`
- Execution plan and `plan-review`
- Matching test specification and `test-spec-review`

## Follow-on Artifacts

- [Single Bounded Review-Fix Workflow Automation spec](../../specs/single-bounded-review-fix-workflow-automation.md)

## Readiness

Proposal-review R4 approved the direction with no material findings, and the proposal lifecycle status is `accepted`.
The accepted direction is ready for specification and the architecture work identified under `Next Artifacts`.
