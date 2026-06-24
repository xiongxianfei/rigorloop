# Proposal-Gated Authoring Autoprogression Through Plan Review

## Status

accepted

## Problem

In many full-feature cycles, the highest-value human judgment happens at the proposal boundary:

```text
Is the problem real?
Is the intended outcome clear?
Is the chosen direction worthwhile?
Are scope and tradeoffs acceptable?
```

Once that direction is settled, later authoring gates often follow a deterministic route:

```text
spec
-> spec-review
-> architecture when required
-> architecture-review when required
-> plan
-> plan-review
```

Today, RigorLoop still requires a user or agent to trigger several of those transitions explicitly even when the proposal has been accepted, proposal-review is clean, no owner decision remains, the next stage is already determined by the workflow contract, and the user has already asked the workflow to continue.

The current contract intentionally stops short of this behavior. `proposal` may hand off to `proposal-review`, but `proposal-review -> spec` is outside the existing v1 autoprogression boundary. Direct review invocations also remain isolated by default.

Existing workflow autoprogression already demonstrates the underlying model: workflow-managed flows may advance automatically through known authoring-to-review pairs and through the bounded implementation-to-PR chain, while isolated review requests, fast-lane work, bugfix work, and on-demand stages remain explicit.

The remaining opportunity is to let a user explicitly authorize:

```text
After the proposal gate passes,
continue automatically up to and including plan-review,
stopping on any ambiguity, finding, or owner decision.
```

A bare global `auto=true` flag would be too broad. It could accidentally bypass required architecture, treat a non-clean review as permission to continue, trigger stages during an isolated review, start implementation automatically, hide unresolved owner decisions, make the author and reviewer effectively the same unexamined pass, or continue after workflow state becomes ambiguous.

The feature should therefore be a bounded, opt-in autoprogression profile, not unrestricted autopilot.

## Goals

- Let users opt into automatic continuation after the proposal gate is clean.
- Keep the proposal as the main human decision checkpoint.
- Automatically run `spec`, `spec-review`, conditional `architecture`, conditional `architecture-review`, `plan`, and `plan-review`.
- Stop after a clean `plan-review`.
- Report `test-spec` as the next stage without starting it in the first slice.
- Keep every authoring and review stage distinct and independently recorded.
- Preserve formal review independence even when stages run consecutively.
- Stop immediately on `changes-requested`, `blocked`, `inconclusive`, material findings, `needs-decision`, missing evidence, ambiguous architecture need, conflicting workflow state, user pause, or user cancellation.
- Make autoprogression change-local and explicitly user-authorized.
- Keep direct review-only requests isolated.
- Preserve the current workflow stage order.
- Make interrupted or resumed workflows idempotent and resistant to duplicate stage execution.
- Produce a reviewable audit trail showing which stages ran automatically and why progression stopped or completed.

## Non-goals

- Do not automatically approve a proposal.
- Do not remove proposal-review.
- Do not automatically revise a proposal after proposal-review findings.
- Do not automatically fix spec-review, architecture-review, or plan-review findings in the first slice.
- Do not automatically run `test-spec`, implementation, code review, verification, or PR from this profile.
- Do not introduce background or asynchronous execution.
- Do not continue after the user asks to pause.
- Do not apply this profile to isolated stage invocations.
- Do not apply it to fast-lane or bugfix flows in the first slice.
- Do not auto-run `explore`, `research`, `learn`, or other on-demand stages.
- Do not infer approval from the absence of user response.
- Do not weaken formal review recording.
- Do not allow the authoring stage to self-certify its matching review in the same undifferentiated reasoning pass.
- Do not create a repository-wide default that silently affects every change.
- Do not make `change.yaml` the owner of live next-stage state.
- Do not begin implementation merely because plan-review passed.
- Do not add future autoprogression profiles through this first-slice change; each additional profile needs its own proposal and spec amendment.
- Do not include `test-spec` in a future profile until measured adoption evidence shows `authoring-through-plan-review` is safe across multiple activations, contributors, and change types.
- Do not auto-resume after manual fixes; explicit user resume remains required after a pause.

## Vision fit

fits the current vision

RigorLoop exists to make AI-assisted work traceable, resumable, and reviewable rather than forcing users to manually route every already-determined transition.

This proposal removes redundant prompts while preserving the gates that carry real judgment.

It is falsified if a non-clean review automatically advances, architecture is skipped when required, implementation begins without a separate authorization profile, review evidence is missing, direct review requests stop being isolated, user silence is interpreted as approval, a resumed workflow repeats completed stages, automation makes it harder to understand why a stage ran, or proposal quality receives less human attention because the profile is enabled.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Add a flag for automatic downstream stages | in scope | Recommended direction |
| Activate automation after the proposal is clear | in scope | Proposal gate |
| Automatically run `spec` | in scope | Autoprogression chain |
| Automatically run `spec-review` | in scope | Autoprogression chain |
| Automatically run `plan` | in scope | Autoprogression chain |
| Automatically run `plan-review` | in scope | Autoprogression chain |
| Preserve human proposal judgment | in scope | Proposal gate, Non-goals |
| Avoid unnecessary manual stage triggering | in scope | Problem, Expected behavior changes |
| Automatically implement after planning | out of scope | Non-goals |
| Automatically repair review findings | deferred follow-up | Deferred follow-up directions |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Opt-in autoprogression profile | core to this proposal | The user needs a bounded activation mechanism. |
| Proposal-clear gate | core to this proposal | Automation should not start from vague judgment. |
| Spec and spec-review chaining | core to this proposal | Primary requested behavior. |
| Conditional architecture chaining | same-slice dependency | The workflow should not skip architecture when triggered. |
| Plan and plan-review chaining | core to this proposal | Primary requested behavior. |
| Independent review execution | same-slice dependency | Automatic chaining should not become self-approval. |
| Change-local policy recording | core to this proposal | Enables audit and safe resumption. |
| Stop and pause semantics | core to this proposal | Prevents runaway execution. |
| Workflow-state validation | same-slice dependency | Prevents duplicate or contradictory transitions. |
| Test-spec autoprogression | separate implementation slice | The requested first boundary is plan-review. |
| Automatic review-fix loops | separate proposal | Higher risk; findings may need owner judgment. |
| Implementation-to-PR changes | out of scope | Existing bounded autoprogression already governs that chain. |
| Project-wide persistent default | deferable follow-up | Change-local opt-in is safer first. |

## Context

The existing workflow already distinguishes:

```text
workflow-managed
isolated
direct-pr
```

and allows bounded autoprogression only where the next stage is already safely known. Current v1 behavior includes authoring-to-matching-review transitions and the implementation-to-PR chain, but keeps direct review requests isolated and excludes `proposal-review -> spec`.

The current routing contract also says that an approved `spec-review` goes to:

```text
architecture, when architecture remains required
otherwise plan
```

and that `plan-review` normally hands off to `test-spec`.

This proposal extends those existing rules rather than creating a second workflow model.

### Terminology

- `Proposal gate`: the artifact and review state at which proposal direction is sufficiently settled to permit automatic downstream authoring.
- `Gate-ready proposal`: a proposal whose artifacts and review evidence satisfy the proposal gate, independent of whether the user has authorized automation.
- `Armed profile`: the user has requested automation, but it cannot begin until the proposal is gate-ready.
- `Active profile`: the proposal is gate-ready, the profile is armed, and the orchestrator is allowed to continue through the bounded stage set.
- `Paused profile`: automation encountered a stop condition and will not continue without explicit user resumption.
- `Completed profile`: the profile reached a clean `plan-review` and stopped as designed.

### Proposal gate

Do not use the phrase "proposal is clear" as an unstructured subjective condition.

The proposal gate passes only when all of these are true:

- proposal artifact exists;
- proposal status is accepted;
- latest formal proposal-review status is approved;
- proposal-review recording status is recorded;
- proposal-review has no material findings;
- proposal-review has no open blockers;
- proposal scope and non-goals are settled enough for spec;
- proposal open questions do not block specification;
- required vision and constitution gates are satisfied;
- change ID and artifact placement are unambiguous.

User authorization is intentionally not part of the proposal gate. Activation requires both:

```text
profile is armed
and
proposal gate passes
```

The proposal-review result should explicitly route to:

```text
Immediate next stage: spec
```

An `approved` result alone is insufficient if the artifact remains in a transitional status or formal recording is incomplete.

## Options considered

### Option 1: Keep explicit triggering for every stage

Keep requiring users or agents to invoke each downstream stage manually after proposal-review.

Pros:

- Simplest and safest.
- No workflow-policy changes.

Cons:

- Users remain manual routers for deterministic transitions.
- Repeated confirmation adds friction without adding judgment.

### Option 2: Add a bare `auto=true` flag

Add one boolean that tells the workflow to keep going after a stage completes.

Pros:

- Simple interface.
- Easy to understand initially.

Cons:

- Scope is ambiguous.
- Difficult to extend safely.
- Could be interpreted as permission to implement or auto-fix.
- Harder to validate.

Rejected.

### Option 3: Add a bounded authoring autoprogression profile

Introduce a closed profile:

```text
authoring-through-plan-review
```

Pros:

- Explicit stopping boundary.
- Preserves proposal as the human checkpoint.
- Includes required conditional architecture.
- Keeps reviews formal and independent.
- Extensible without changing boolean meaning.
- Safe default remains off.

Cons:

- Requires coordinated workflow and skill-contract changes.
- Needs machine-readable state and broad fixture coverage.

Recommended.

### Option 4: Full autopilot from proposal through PR

Continue automatically through test design, implementation, review, verification, and PR.

Pros:

- Maximum reduction in user prompts.

Cons:

- Combines decision, authoring, review, implementation, verification, and publication authority.
- Increases risk substantially.
- Conflicts with the requested proposal-centered human checkpoint.

Rejected.

## Recommended direction

Introduce a closed autoprogression profile:

```text
off
authoring-through-plan-review
```

Do not use a bare boolean internally.

Use this user-facing flag:

```text
auto-through: plan-review
```

Store it internally as:

```text
autoprogression.profile: authoring-through-plan-review
```

The user-facing key indexes profiles by stopping boundary, which matches how users describe the feature. The internal name indexes by scope, which matches how the workflow state machine reasons about it. The closed profile gives the flag a defined scope and allows future profiles without changing the meaning of `true`. Adding future profiles should require a separate proposal and spec amendment rather than silently expanding this profile.

### Activation contract

The first slice should be change-local.

Persist authorization in `docs/changes/<change-id>/change.yaml`:

```yaml
workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
```

This field records automation policy only.

It does not own current stage, next stage, review status, branch readiness, or PR readiness. Those remain owned by existing workflow artifacts.

The user may enable the profile at workflow start, after reviewing the proposal, after a clean proposal-review, or when resuming an existing workflow before spec begins.

Arming before the change pack exists records non-durable intent only. The user should re-assert authorization once the change-local surface exists so the workflow can persist it in `change.yaml`. If the downstream spec determines `change.yaml` cannot carry workflow-policy data, use `docs/changes/<change-id>/workflow-policy.yaml` as the fallback rather than creating a new top-level surface.

Activation uses `armed && gate-ready`, not a subjective "proposal is clear" check. An unarmed but otherwise gate-ready proposal should be reported as gate-ready with the profile still `off`, not as a failed proposal gate.

A repository-wide "always auto after proposal" setting is out of the first slice. This prevents an adopter from being surprised by automatic stage execution merely because a repository was configured by another contributor.

### Autoprogression chain

When the profile is active, use:

```text
accepted proposal
-> approved proposal-review
-> spec
-> spec-review
-> architecture assessment
-> architecture
-> architecture-review
    when architecture is required
-> plan
-> plan-review
-> stop
```

After clean plan-review:

```text
Next stage: test-spec
Autoprogression profile: completed
```

Do not start `test-spec` in this profile.

### Stage behavior

The `spec` stage uses the accepted proposal, proposal-review result, relevant vision and governance, current project map when relevant, and existing contracts affected by the direction. It records the spec and reports readiness for `spec-review`.

The `spec-review` stage runs as a separate review stage and inspects the tracked spec, not the authoring stage's hidden reasoning. An `approved` result continues to architecture assessment. `changes-requested`, `blocked`, or `inconclusive` pauses the profile. The first slice does not revise the spec automatically.

After approved spec-review, the workflow runs an architecture assessment as a recorded workflow-managed micro-stage. The assessment should inspect the approved spec, proposal-review result, spec-review result, existing architecture and ADR records when relevant, and the architecture trigger list below. It records one of three outcomes:

- `architecture-required`;
- `architecture-not-required`;
- `architecture-ambiguous`.

Architecture is required when the change introduces or materially alters subsystem boundaries, data flow, trust boundaries, public interfaces, persistence, deployment, generated-output architecture, release or compatibility architecture, or a durable design tradeoff requiring an ADR. Architecture is ambiguous when the assessor cannot justify either `architecture-required` or `architecture-not-required` from tracked artifacts without owner judgment, missing system context, or a disputed boundary classification. Ambiguity pauses the profile rather than guessing.

When architecture is required, the workflow runs:

```text
architecture
-> architecture-review
```

No separate user confirmation is required between a recorded `architecture-required` assessment and the `architecture` stage. The assessment is the routing decision. A clean architecture-review continues to plan. Any material finding, non-approval result, or owner decision pauses the profile. The architecture stage should not introduce a new ADR automatically when it exposes an owner decision.

The `plan` stage uses only approved upstream artifacts and should not reopen product direction or silently reinterpret unresolved review findings.

The `plan-review` stage runs as a separate formal review stage. An `approved` result marks the profile completed and reports `test-spec` next. `changes-requested`, `blocked`, or `inconclusive` pauses the profile. It does not start `test-spec`.

### Review independence

Automatic progression should not mean automatic self-approval.

Each review stage should:

- run as a distinct skill invocation;
- read the tracked artifact as its review target;
- avoid relying on author-stage hidden reasoning;
- use the formal review criteria for that stage;
- record its result before any downstream action;
- avoid editing the reviewed artifact during the review;
- stop on findings rather than quietly repairing them.

Where the agent platform supports fresh or independent review context, use it. Where it does not, the stage should still reset context to reviewed artifact, governing sources, formal review criteria, and recorded prior findings when relevant rather than continuing the authoring narrative.

For this proposal, a `material finding` means a formal review finding classified as material under the repository's review-recording contract because it can affect scope, correctness, compatibility, security, workflow state, artifact validity, or an owner decision. The review stage owns that classification and records it before downstream routing.

### Stop conditions

The profile pauses immediately when any of these occurs:

- user requests pause or cancellation;
- proposal gate is incomplete;
- required artifact is missing;
- artifact placement is ambiguous;
- review recording fails;
- review status is `changes-requested`;
- review status is `blocked`;
- review status is `inconclusive`;
- material finding exists;
- `needs-decision` remains open;
- proposal direction should change;
- spec conflicts with accepted proposal;
- architecture need is ambiguous;
- architecture requires owner selection;
- plan would rely on unresolved upstream ambiguity;
- workflow state is contradictory;
- stage was already partially executed without reliable completion evidence;
- maximum transition count is reached.

The result should state:

- last completed stage;
- stage that stopped;
- reason;
- required next action;
- whether the profile remains armed or is paused.

Contradictory workflow state means the current state surfaces cannot all be true at once. Examples include a plan claiming downstream readiness while the referenced review remains non-approved, a profile marked completed while `plan-review` evidence is missing, multiple live next-stage owners naming different next stages for the same change, an artifact status that conflicts with the latest formal review result, or a change-local policy value that the workflow spec does not recognize.

### No automatic repair loop in the first slice

When a review requests changes, the profile pauses.

It does not automatically run spec revision, architecture revision, plan revision, review-resolution, or rereview.

This boundary is deliberate. Review findings can contain product, architecture, risk, compatibility, or owner decisions that should not be reduced to an automatic edit loop.

### Idempotence and resumption

Automatic chaining should be safe to resume.

Before invoking a stage, the orchestrator should inspect current workflow state, artifact existence, artifact status, latest formal review result, open review findings, recording completion, and autoprogression profile.

Rules:

- Do not recreate a completed artifact merely because the workflow resumed.
- Do not rerun a clean review unless rereview is required.
- Do not skip an incomplete or conflicting artifact.
- Do not infer completion from file existence alone.
- If stage completion is ambiguous, pause.
- A paused profile requires explicit user resume.
- Manual fixes do not auto-resume the profile. Resume requires explicit user authorization because fixes may change the spec, plan, proposal direction, or rereview scope.
- A completed profile does not restart automatically.
- User cancellation changes the profile to `off`.

No background processing is implied. Autoprogression means consecutive stage execution within an active workflow-managed interaction without redundant confirmation prompts.

### Transition budget

Use a bounded transition budget to prevent runaway execution.

For `authoring-through-plan-review`, the maximum normal sequence is:

```text
spec
spec-review
architecture
architecture-review
plan
plan-review
```

The normal transition budget is six stage invocations per activation: `spec`, `spec-review`, optional `architecture`, optional `architecture-review`, `plan`, and `plan-review`. When architecture is not required, the unused architecture slots still count as skipped slots rather than permission to run other stages.

The orchestrator should run each stage at most once per activation unless an explicit rereview event exists. If a rereview event is explicitly authorized after a pause, the resumed budget is:

```text
remaining uncompleted stages
+ explicitly authorized rereview stages
```

Unexpected cycles or any attempt to spend the budget on `test-spec`, implementation, or review-fix loops pauses the profile.

## Expected behavior changes

### Flag off

Behavior remains unchanged:

```text
proposal-review approved
-> report spec as next stage
-> stop
```

### Flag on, architecture not required

```text
proposal-review approved
-> spec
-> spec-review approved
-> plan
-> plan-review approved
-> stop with test-spec next
```

### Flag on, architecture required

```text
proposal-review approved
-> spec
-> spec-review approved
-> architecture
-> architecture-review approved
-> plan
-> plan-review approved
-> stop with test-spec next
```

### Review requests changes

```text
spec-review changes-requested
-> record finding
-> pause
-> do not revise automatically
```

### Direct review request

```text
user directly invokes spec-review
-> isolated review
-> no autoprogression, even if the repository has an armed profile
```

unless the user explicitly invokes the workflow-managed resume path.

## Architecture impact

| Surface | Impact |
| --- | --- |
| Workflow-stage autoprogression spec | Extend review-to-next-authoring boundary. |
| RigorLoop workflow spec | Define profile, gate, sequence, and stops. |
| Workflow skill | Read and enforce the opt-in profile. |
| Proposal-review | Expose deterministic proposal-gate result. |
| Spec and spec-review | Support workflow-managed consecutive execution. |
| Architecture and architecture-review | Support conditional profile participation. |
| Plan and plan-review | Support profile completion boundary. |
| Change metadata | May record change-local automation policy. |
| Review recording | Preserve formal receipts and findings. |
| Artifact lifecycle validation | Validate profile/state consistency. |
| Generated skill/adapters | Rebuild when canonical skills change. |
| Runtime services | No new service, persistence engine, or background worker. |

Architecture assessment is recommended because the implementation may add a machine-readable workflow policy field and change orchestration behavior across several stages, even though it does not introduce a deployed service.

Generated skill/adapters refers to this repository's public adapter distribution surfaces that are rebuilt from canonical skill sources. If canonical skill guidance changes, generated adapter guidance should be regenerated or validated so public command surfaces stay aligned.

## Testing and verification strategy

| Check ID | What is verified |
| --- | --- |
| `APGA-001` | Default profile is `off`. |
| `APGA-002` | An unknown profile fails closed. |
| `APGA-003` | An armed profile does not start before the proposal gate passes. |
| `APGA-004` | Proposal status must be accepted. |
| `APGA-005` | Proposal-review must be approved and recorded. |
| `APGA-006` | Material proposal-review findings block activation. |
| `APGA-007` | Material proposal-review findings paired with `inconclusive` block activation. |
| `APGA-008` | Armed profile plus clean proposal gate starts spec automatically. |
| `APGA-009` | Spec completion starts spec-review automatically. |
| `APGA-010` | Clean spec-review with no architecture need starts plan. |
| `APGA-011` | Architecture-required flow runs architecture and architecture-review. |
| `APGA-012` | Ambiguous architecture need pauses. |
| `APGA-013` | `changes-requested` pauses without auto-editing. |
| `APGA-014` | `blocked` pauses. |
| `APGA-015` | `inconclusive` pauses. |
| `APGA-016` | `needs-decision` pauses. |
| `APGA-017` | Clean plan-review completes the profile. |
| `APGA-018` | Test-spec is reported but not invoked. |
| `APGA-019` | Direct review invocation remains isolated. |
| `APGA-020` | Fast-lane and bugfix flows remain explicit-step. |
| `APGA-021` | User pause takes effect before the next stage. |
| `APGA-022` | Resume does not duplicate completed stages. |
| `APGA-023` | File existence alone does not prove stage completion. |
| `APGA-024` | Every automatically run review is recorded. |
| `APGA-025` | Review runs independently from authoring context. |
| `APGA-026` | The profile cannot start implementation. |
| `APGA-027` | The transition budget prevents loops. |
| `APGA-028` | Invalid or contradictory workflow state pauses safely. |
| `APGA-029` | User cancellation disables the profile only after cancellation is durably recorded. |
| `APGA-030` | Generated adapters contain aligned stage guidance. |
| `APGA-031` | Activation pauses with reason `authorization-not-persisted` when no durable authorization record exists. |
| `APGA-032` | Activation pauses when the durable authorization record is malformed or missing required fields. |
| `APGA-033` | Activation pauses when the authorization persistence write fails. |
| `APGA-034` | Pre-pack arming does not permit activation; re-assertion after change-pack creation is required. |
| `APGA-035` | Cancellation must be durably recorded; an in-memory cancel that fails to persist keeps the prior durable profile state and pauses. |
| `APGA-036` | The `workflow-policy.yaml` fallback is used only when the change-metadata contract rejects policy data, and the fallback decision appears in the audit trail. |
| `APGA-037` | Existing v1 autoprogression behavior is preserved when the new profile is off. |

### Behavior-preservation proof

Create:

```text
docs/changes/<change-id>/behavior-preservation.md
```

Required matrix:

| Surface | Baseline | New proof | Result |
| --- | --- | --- | --- |
| Proposal-to-proposal-review | Existing workflow-managed autoprogression | unchanged | preserved |
| Direct proposal-review | isolated | still isolated | preserved |
| Proposal-review-to-spec | explicit user action | profile-controlled automatic transition | intentionally extended |
| Spec-to-spec-review | already bounded automatic pair | unchanged | preserved |
| Architecture-to-review | already bounded automatic pair | unchanged | preserved |
| Spec-review routing | architecture or plan | unchanged | preserved |
| Plan-review routing | test-spec | still next stage; not auto-run | preserved |
| Review findings | stop/manual resolution | unchanged in first slice | preserved |
| Fast lane | explicit-step | unchanged | preserved |
| Bugfix lane | explicit-step | unchanged | preserved |
| Implementation chain | existing bounded behavior | unchanged | preserved |
| Review recording | formal evidence required | unchanged | preserved |
| Profile authorization persistence | optional/advisory | mandatory durable record; pause on absence or failure | intentionally tightened |

## Rollout and rollback

### Rollout

1. Approve the proposal.
2. Amend `specs/workflow-stage-autoprogression.md`.
3. Amend `specs/rigorloop-workflow.md`.
4. Review both spec amendments.
5. Add or update matching test specs.
6. Assess whether architecture or change-metadata schema work is required.
7. Write and review the implementation plan.
8. Add the profile in audit-only mode.
9. Run fixture-backed simulated stage chains.
10. Enable profile execution for explicit change-local opt-ins.
11. Update affected canonical skills.
12. Rebuild and validate generated skills/adapters.
13. Run several dogfood cycles with the profile off and on.
14. Evaluate the success metrics.

### Rollback

- Set the profile to `off`.
- Restore explicit `proposal-review -> spec` triggering.
- Preserve artifacts and formal review records already created.
- Do not delete automatically produced specs, plans, or reviews merely because automation is disabled.
- Keep stop-condition and audit evidence.
- Revert workflow guidance and generated outputs together.
- Do not retain an unrecognized profile value in active change records.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Proposal receives less human attention | Require explicit authorization and a clean proposal gate. |
| Automation skips architecture | Include mandatory architecture assessment and fail closed. |
| Same agent rubber-stamps its own artifact | Separate author and review invocations with tracked-artifact input. |
| Review findings are auto-fixed incorrectly | No automatic repair loop in the first slice. |
| User loses control | Support pause and cancellation before every transition. |
| Resumption duplicates stages | Use recorded stage/review state and idempotence checks. |
| Flag meaning expands silently | Use a closed profile instead of a boolean. |
| Profile starts in isolated review | Restrict it to workflow-managed context. |
| Automated sequence runs too long | Use a bounded transition budget and stop after plan-review. |
| Metadata becomes live-state owner | Record policy only; existing owner continues to control next stage. |
| Agents claim implementation readiness | Stop before test-spec and implementation. |
| Review recording is skipped for speed | Make recorded review evidence a continuation precondition. |

## Open questions

None.

### Closed question log

| Question | Answer | Where recorded |
| --- | --- | --- |
| What should the user-facing flag be called? | Use `auto-through: plan-review` for users and `autoprogression.profile: authoring-through-plan-review` internally. | Recommended direction |
| What exact field owns change-local authorization? | Persist policy in `docs/changes/<change-id>/change.yaml`; fall back to `docs/changes/<change-id>/workflow-policy.yaml` only if the downstream spec rejects `change.yaml` for policy data. | Activation contract |
| Can the profile be armed before proposal-review? | Yes, but pre-change-pack arming is non-durable and should be re-asserted once the change-local surface exists. | Activation contract |
| Should architecture always auto-run when triggered? | Yes, after recorded `architecture-required`; pause if architecture surfaces an owner decision or material finding. | Stage behavior |
| Should a paused profile resume automatically after fixes? | No. Explicit user resume is durable policy, not only a first-slice limit. | Non-goals; Idempotence and resumption |
| Should test-spec be included later? | Only through a separate `authoring-through-test-spec` proposal after measured safety evidence. | Non-goals; Deferred follow-up directions |

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-24 | Preserve proposal as the human decision checkpoint. | Product direction carries the highest-value manual judgment. | Full automatic lifecycle from an initial request. |
| 2026-06-24 | Use a bounded profile rather than `auto=true`. | Scope and stopping behavior should remain explicit. | Unrestricted boolean flag. |
| 2026-06-24 | Stop after plan-review. | Matches the requested first slice and preserves a checkpoint before test design and implementation. | Continue automatically into implementation. |
| 2026-06-24 | Include conditional architecture. | The standard workflow should not skip triggered architecture. | Hard-code spec-review directly to plan. |
| 2026-06-24 | Pause on all non-clean reviews. | Automatic repair can conceal owner decisions. | Automatic review-fix loops. |
| 2026-06-24 | Keep direct reviews isolated. | A review-only request is not authorization for end-to-end continuation. | Treat any clean review as workflow continuation. |
| 2026-06-24 | Require explicit resume after a pause. | Prevents surprising continuation after manual corrections. | Resume automatically after file changes. |

## Deferred follow-up directions

- Proposal for `authoring-through-test-spec`.
- Proposal for bounded automatic review-resolution and rereview.
- Proposal for a repository-level default after change-local adoption proves safe.
- Proposal for autoprogression telemetry or summary metrics if local evidence is insufficient.
- Proposal for fast-lane or bugfix automation only if their explicit-step model later becomes a measured bottleneck.

Each follow-up profile should require its own proposal and spec amendment. The first slice should not define a generic profile-registration mechanism.

The `authoring-through-test-spec` follow-up should not start until adoption evidence shows this profile completed without unexpected stops across a measured sample, such as at least five change-local activations, at least two distinct contributors, and at least three change types, with audit trails available for review. The downstream proposal may revise the exact thresholds, but it should keep the trigger measurable.

## Next artifacts

- `proposal-review`
- `specs/workflow-stage-autoprogression.md` amendment
- `specs/rigorloop-workflow.md` amendment
- `spec-review`
- recorded architecture assessment
- architecture and architecture-review, if required
- test-spec amendment
- plan
- plan-review

Later implementation, code-review, explain-change, verify, and PR artifacts remain normal lifecycle stages for implementing the approved change. They are not runtime stages that this autoprogression profile may start.

## Follow-on artifacts

- `proposal-review`: approved in [proposal-review-r1](../changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/proposal-review-r1.md)
- `spec`: draft amendments in [Workflow Stage Autoprogression](../../specs/workflow-stage-autoprogression.md) and [RigorLoop Workflow](../../specs/rigorloop-workflow.md)

## Readiness

- This proposal is accepted.
- Spec work is now tracked in `specs/workflow-stage-autoprogression.md` and `specs/rigorloop-workflow.md`.
- No further `proposal-review` action is pending.

## Core invariant

```text
Human approval settles the proposal direction.

After that gate, an explicitly enabled workflow may advance through deterministic
authoring and review stages without redundant prompts.

Every stage remains real.
Every review remains independent and recorded.
Any ambiguity or non-clean result stops the chain.
The first profile ends at plan-review and never starts implementation.
```
