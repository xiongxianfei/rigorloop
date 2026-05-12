# Review Recording Guardrail and Downstream Status Settlement Review Resolution

## Scope

This record resolves material findings from formal lifecycle reviews for the review recording guardrail and downstream status settlement change.

Closeout status: open

## Resolution Entries

### spec-review-r1

Review closeout: spec-review-r1

#### SR-001

Finding ID: SR-001
Disposition: accepted
Owner: implementer
Owning stage: spec
Chosen action: Add a normative change-ID selection rule to `specs/formal-review-recording.md`, including deterministic selection order, generated fallback format, collision behavior, and blocked-recording behavior. Update `specs/formal-review-recording.test.md` to cover each selection path.
Rationale: Formal review skills must not infer or invent change roots inconsistently when recording is required. The spec must define the rule so implementation and tests have one source of truth.
Validation target: Rerun spec-review after the spec and test-spec updates.
Validation evidence: Spec and test-spec updates are drafted in `specs/formal-review-recording.md` and `specs/formal-review-recording.test.md`; spec-review rerun pending.
