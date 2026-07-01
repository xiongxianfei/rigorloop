# ADR-20260630: Bounded Review-Fix Autoprogression

## Status

accepted

## Context

RigorLoop already has separately armed autoprogression profiles for proposal-gated authoring and implementation-through-verify. Proposal-side review-fix loops still require repetitive manual routing even when findings are deterministic, safe, and already recorded with clear resolution paths.

The approved review-fix autoprogression spec defines a simple chat command, `$workflow auto: <target-stage>`, and deliberately excludes dry-run mode, separate apply-mode state, implementation, code-review, verify, PR, release, publication, network, and external-state operations.

## Decision

Add a separately armed workflow-managed profile named `bounded-review-fix`.

Persist its authorization and profile-local cursor under:

```yaml
workflow:
  autoprogression:
    review_fix:
      status: armed
      profile: bounded-review-fix
      target_stage: spec-review
      armed_by: user
      armed_at: "2026-06-30T00:00:00Z"
      current_stage: proposal-review
      current_review: none
      stop_reason: none
      last_updated_evidence: docs/changes/<change-id>/change.yaml
```

The closed `target_stage` enum is:

- `proposal-review`
- `spec`
- `spec-review`
- `architecture`
- `architecture-review`
- `plan`
- `plan-review`
- `test-spec`
- `test-spec-review`

The workflow driver owns orchestration and auto-safe classification. Existing authoring and review skills keep their artifact and gate responsibilities. Direct review invocations remain isolated and do not create, activate, resume, or advance review-fix state.

Activation requires durable authorization plus a clean current-stage gate. Proposal-start activation additionally requires an accepted proposal, approved recorded proposal-review, no open findings, and unambiguous change and artifact placement.

The driver may apply only deterministic auto-safe fixes after review evidence is recorded. It records disposition in `review-resolution.md`, reruns the same review after every auto-fix cycle, and continues only after the current review is clean and the requested target boundary allows it.

The loop is bounded at two auto-fix/rereview cycles per review gate, five material findings per cycle, three files changed per cycle, ten files changed per chat invocation, and no transition past the armed target stage.

After approved recorded `spec-review`, the driver records exactly one architecture assessment:

- `architecture-required`: route through `architecture` and `architecture-review`;
- `architecture-not-required`: skip those conditional stages and continue only to the next applicable in-bound target;
- `architecture-ambiguous`: stop for owner decision.

If the requested target is a skipped conditional architecture stage, the profile stops with `target-not-applicable` instead of claiming the target was reached.

Cancellation, off, completed, target-reached, paused, and contradictory-state transitions update `workflow.autoprogression.review_fix` deterministically in `change.yaml` or in the approved fallback policy surface when change metadata cannot carry policy data.

## Alternatives Considered

- Keep the loop fully manual. This preserves safety but keeps high-friction repeated routing for deterministic review fixes.
- Make review skills self-edit or auto-continue by default. This would collapse gate and editor roles and violate direct-review isolation.
- Reuse `authoring-through-plan-review`. That profile explicitly excludes automatic review-fix loops and stops before `test-spec`.
- Add dry-run and apply-mode state. The accepted owner direction rejected this extra state for the first design.
- Add a global continue-until-done mode. That would cross implementation, verification, PR, release, and external-effect boundaries.

## Consequences

- Workflow guidance, validators, review-resolution handling, and generated adapter guidance need updates for the new closed profile and state shape.
- Validators must fail closed for unknown profile, status, target-stage, auto-fix class, review status, disposition, architecture assessment, and stop-reason values.
- Review-fix automation remains review-gated and observable because every auto-fix follows recorded review evidence, durable disposition, changed-file reporting, and same-review rerun.
- No new deployed service, background worker, CLI deployment boundary, database, or external scheduler is introduced.
- Existing `authoring-through-plan-review` and `implementation-through-verify` semantics remain unchanged.

## Follow-up

- Run `architecture-review` on this architecture update and ADR.
- Create the execution plan, plan review, test spec, and test-spec review before implementation.
