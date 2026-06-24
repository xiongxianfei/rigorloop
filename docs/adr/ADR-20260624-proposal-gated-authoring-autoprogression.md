# ADR-20260624-proposal-gated-authoring-autoprogression: Proposal-Gated Authoring Autoprogression

## Status

accepted

## Context

RigorLoop already supports bounded automatic continuation for known workflow-managed handoffs, but it intentionally kept `proposal-review -> spec` outside the default v1 boundary. Users still had to manually trigger several already-determined authoring and review stages after a proposal had been accepted and proposal-review was clean.

The accepted proposal and approved spec amendments define a narrower goal: let a user explicitly authorize automatic continuation after the proposal gate through clean `plan-review`, while preserving proposal judgment, review independence, formal recording, direct-review isolation, idempotent resumption, and a hard stop before `test-spec` or implementation.

This is a durable architecture decision because it changes workflow orchestration, adds change-local policy persistence, defines profile-state ownership boundaries, and creates a recorded architecture-assessment routing point between `spec-review` and planning.

## Decision

Add a closed, separately armed workflow profile:

```text
authoring-through-plan-review
```

The user-facing authorization `auto-through: plan-review` maps to the internal policy value `autoprogression.profile: authoring-through-plan-review`. Unknown profile values fail closed. Future profiles, including `authoring-through-test-spec` or implementation profiles, require separate proposal and spec amendments.

Activation requires:

```text
armed && gate-ready && durable authorization persisted
```

Gate readiness is artifact and review state only: accepted proposal, approved recorded proposal-review, no material proposal-review findings, no open proposal blockers, settled proposal scope and non-goals, non-blocking open questions, satisfied standing gates, and unambiguous change ID and artifact placement. User authorization is separate intent and cannot substitute for gate evidence.

Profile authorization is persisted change-locally before any profile-driven transition. The canonical surface is `docs/changes/<change-id>/change.yaml`. The fallback `docs/changes/<change-id>/workflow-policy.yaml` is allowed only when the change-metadata contract rejects policy data, and the fallback decision is recorded in the activation audit trail. Missing, malformed, partially written, or failed persistence pauses before `spec` with `authorization-not-persisted`. Session-only pre-pack arming must be reasserted after the change pack exists.

The profile may run only:

```text
spec
spec-review
architecture assessment
architecture
architecture-review
plan
plan-review
```

Architecture assessment is a recorded workflow-managed micro-stage after approved `spec-review`. It records exactly one of `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`; ambiguity pauses. `architecture-required` routes to `architecture` and `architecture-review`; `architecture-not-required` routes to `plan`.

Review stages stay distinct formal invocations over tracked artifacts, governing sources, formal criteria, and relevant recorded findings. They do not edit the reviewed artifact during review and do not rely on hidden authoring reasoning. If fresh execution context is unavailable, the review context is reset to those inputs.

Clean `plan-review` completes the profile and reports `test-spec` next without invoking it. The profile cannot start `test-spec`, implementation, code-review, explain-change, verify, PR, release, deploy, merge, destructive Git actions, or automatic review-fix loops.

Profile policy metadata records authorization only. It does not own current stage, next stage, review status, branch readiness, PR readiness, active-plan live state, or review-resolution closeout. Those remain owned by existing workflow-state and review surfaces.

## Alternatives considered

### Keep explicit triggering for every post-proposal stage

Rejected because it leaves the user as a manual router for deterministic transitions after the proposal gate has already supplied the main human judgment.

### Add a bare `auto=true` flag

Rejected because the scope is ambiguous and could be interpreted as permission to skip architecture, advance after non-clean reviews, auto-fix findings, start implementation, or apply to isolated review invocations.

### Widen existing autoprogression defaults

Rejected because direct review-only requests and default workflow behavior must remain stable. The new behavior needs explicit change-local authorization and a named profile boundary.

### Use session-only authorization

Rejected because the audit trail would not prove why a resumed workflow advanced. Durable change-local authorization is an activation precondition.

### Make `change.yaml` the live workflow-state owner

Rejected because workflow live-state ownership already belongs to existing workflow artifacts, especially active plans for planned initiatives. Profile policy metadata is authorization evidence, not current-stage authority.

### Continue through `test-spec` or implementation

Rejected for this profile because those stages cross into different risk surfaces. Future profiles require separate proposal, spec amendment, and measured evidence from this profile's safe adoption.

## Consequences

- Workflow-managed authoring can reduce redundant prompts after a clean proposal gate without changing behavior when the profile is `off`.
- Implementations must validate proposal gate evidence, durable authorization persistence, profile state, review evidence, architecture assessment, transition budget, and stop conditions before each profile-driven transition.
- Direct review invocations, manual skill invocations, bugfix flows, fast-lane behavior, review-fix loops, `test-spec`, implementation, verification, and PR behavior remain outside this profile.
- Change metadata or the fallback policy file becomes part of the reviewable audit trail for activation and cancellation.
- Canonical skills and generated guidance need alignment so authoring and review stages preserve distinct stage records even when run consecutively.
- No new service, database, background worker, deployment target, or external publication boundary is introduced.

## Follow-up

- Architecture-review this ADR and the canonical architecture package update.
- Plan implementation of the profile, durable authorization persistence, recorded architecture assessment, stop conditions, audit trail, and fixture-backed transition tests.
- Update canonical skills and generated adapters after implementation changes skill guidance.
- Use measured adoption evidence before proposing any future `authoring-through-test-spec` or implementation profile.
