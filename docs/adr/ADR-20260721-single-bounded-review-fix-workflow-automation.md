# ADR-20260721: Single Bounded Review-Fix Workflow Automation Mechanism

## Status

accepted

## Context

RigorLoop accumulated three independently writable workflow-automation profiles: `authoring-through-plan-review`, `implementation-through-verify`, and proposal-side `bounded-review-fix`. They preserve useful safety policies, but duplicate command routing, persistence, status, resume, cancellation, transition recovery, and target semantics. Keeping those profiles writable would leave multiple state machines that can disagree about authority and progress.

The approved unified specification makes `bounded-review-fix` the only writable workflow-automation mechanism. The decision must preserve stage-owned artifacts, formal review independence, active-plan workflow-state ownership, risk-class authorization boundaries, bounded correction policies, legacy command compatibility, and the stop before PR or other external actions.

## Decision

Use one repository-local, target-driven workflow-automation engine identified as `bounded-review-fix`. Persist all new automation state beneath the neutral namespace:

```yaml
workflow:
  automation:
    mechanism: bounded-review-fix
    version: 2
```

The physical first-version persistence surface is `docs/changes/<change-id>/change.yaml#workflow.automation`. No separate automation-state or receipt file is introduced.

The approved workflow specifications are the normative owner of stage-policy semantics. `scripts/workflow_automation_policy.py` contains one immutable typed Python projection. Every automatable stage policy contains `stage`, `predecessor_rule`, `owning_skill`, `occurrence_rule`, `required_authorization_class`, `capability_kind`, `permitted_mutation_category`, `applicability_rule`, `prerequisite_rule`, `required_input_identities`, `completion_rule`, `completion_evidence`, `next_stage_calculation`, `retry_policy`, `correction_policy`, and `stop_behavior`. The historically singular `permitted_mutation_category` field stores a non-empty immutable set; actual capability mutation categories must be a subset of both that stage-local set and the parent authorization. Planning and implementation cannot add, omit, or reinterpret those fields. Exhaustive conformance tests reject missing or duplicate policies, incomplete records, unknown values, unsupported stage mappings, and projection drift. The first version has no second hand-authored YAML or JSON policy registry.

Physical ownership is:

- `skills/workflow/SKILL.md`: public command, pause, and workflow handoff semantics;
- `scripts/workflow_automation.py`: command adaptation, target and canonical-position resolution, authorization evaluation, and transition coordination;
- `scripts/workflow_automation_policy.py`: frozen policies and closed enums;
- `scripts/workflow_automation_state.py`: the only writer of `change.yaml#workflow.automation`, including state access and prepared-transition reconciliation;
- `scripts/workflow_code_state.py`: repository-owned target-ref and merge-base anchor resolution, immutable review-target binding, complete anchored code-state derivation, and post-review Git/worktree drift detection;
- `scripts/validate_workflow_automation.py`: policy, run, authorization, capability, target, receipt, migration, and canonical-state consistency validation;
- change-local evidence: ownership of the persisted automation data.

The engine is decomposed into these responsibilities:

- a command and compatibility adapter normalizes `$workflow auto: <stage>`, status, off, and supported legacy aliases;
- a target binder resolves every public stage to a structured stage, occurrence identity, and completion predicate before persistence;
- a canonical-position resolver derives position from authoritative artifacts and reviews before an active plan exists, then reads the active plan's `Current Handoff Summary` after plan creation;
- the immutable typed Python stage-policy registry projects the complete approved stage-policy contract without becoming normative authority;
- an authorization evaluator separates durable bounded parent authorization from concrete effective capability and refuses capabilities whose basis or scope is stale or broader than the parent;
- a transition coordinator asks the state adapter to write a prepared receipt before mutation, invokes one stage-owned operation, reconciles durable completion evidence against the originally bound `effective_capability_id`, synchronizes canonical workflow state, and then finalizes the receipt;
- validators fail closed on unknown closed-vocabulary values, ambiguous targets, stale authority, contradictory canonical evidence, invalid receipts, and multiple in-flight transitions.

Automation state records observed evidence identities and receipts. It does not own an independent `current_stage` or `next_stage`. Stage-owning skills continue to own artifacts and formal review results. Review-finding classification remains stage-specific: proposal-side deterministic correction is driver-owned, implementation correction eligibility is reviewer-owned, and verification failure never authorizes automatic repair.

Every prepared receipt records `effective_capability_id`. The effective capability is the executable authority and links to its non-executable parent authorization through `parent_authorization_id`. A receipt does not bind directly to a parent authorization, resume does not silently replace the recorded capability, and an invalidated capability pauses reconciliation.

Verification currentness uses an independently owned canonical code-state
anchor resolver and provider. The resolver discovers the repository-owned
default target ref, derives its merge base with the exact commit named by the
canonical final-review record, and binds change, review, target, and governed
evidence identities into an immutable anchor. The Git provider derives the
complete anchored change set, including added, modified, deleted, and renamed
paths, and rejects target-ref drift, unapproved post-review commits, dirty
tracked paths, and untracked paths. Branch-state evidence must project the
anchor and provider's exact revisions, path set, and identity; it cannot select
its own hashing domain. Test-only provider injection is rejected for Git
repositories. Post-review exclusions come only from exact basis-validated
change-local or plan lifecycle-evidence paths; code paths cannot be exempted.

The engine permits a destination target beyond current authority, but target selection never implies blanket consent. Authoring, implementation, and verification use distinct parent authorizations and effective capabilities. Verification authority cannot be persisted contingently before its complete basis exists. PR creation, push, publication, deployment, merge, destructive Git operations, and other external actions are prohibited.

Migration is dual-read and single-write. Legacy records remain readable; supported legacy commands normalize into structured unified targets. The first mutating resume of active legacy state creates unified state plus a migration receipt and makes the legacy record read-only. New writes never update a retired profile. Ordinary lifecycle continuation that has no persisted automation run remains governed by the workflow specifications and is not a second automation mechanism.

## Supersession

This ADR supersedes:

- `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`;
- `docs/adr/ADR-20260624-implementation-through-verify-autoprogression.md`;
- `docs/adr/ADR-20260630-bounded-review-fix-autoprogression.md`.

Their safety constraints remain historical rationale and are preserved where the unified specification rebinds them to stage policies, authorization classes, capabilities, or run state.

Architecture-review R3 approved this ADR. Its acceptance and the three predecessor ADRs' supersession metadata were normalized together before execution planning relied on the decision.

## Alternatives Considered

### Keep three writable profiles

Rejected because shared dispatch would not remove competing persistence, recovery, cancellation, and authorization state machines.

### Add a dispatcher without consolidating state

Rejected because a common command surface would hide rather than resolve state and policy drift.

### Model the first version as a fully declarative workflow graph

Rejected because several stage rules require executable predicates, and a second hand-authored data registry would risk drifting from the normative specifications. A typed immutable Python registry is the initial executable projection.

### Treat a target as blanket authority

Rejected because reaching later stages crosses distinct authoring, implementation, verification, and external-action risk boundaries.

## Consequences

- Status, resume, cancellation, target binding, authorization, receipt recovery, and migration have one writable implementation path.
- The component is more capable than any retired profile and therefore requires closed stage policies, exhaustive validators, and evidence-first recovery tests.
- The design adds four named Python modules but creates one state-write boundary and avoids a second policy or persistence format.
- The active plan remains the live workflow-state owner after plan creation; automation metadata cannot become a competing cursor.
- Legacy aliases remain supported during the migration window but write only unified state.
- Existing stage skills, review gates, review-finding ownership, and lifecycle continuation remain independently testable.
- No new service, database, background worker, hosted actor, deployment target, or external-action authority is introduced.

## Follow-up

- Run `architecture-review` on this ADR, the canonical architecture update, and both workflow-automation diagrams.
- After approval, change this ADR to `accepted` and change all three predecessor ADRs to `superseded` with `superseded_by` links in the same lifecycle update.
- Create an execution plan and test specification covering target binding, state vocabularies, capability derivation, interrupted-transition recovery, migration, cancellation, and stage-policy conformance.
- Update canonical skills, schemas, validators, and generated adapter guidance only through the reviewed implementation plan.
