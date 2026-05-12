# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/formal-review-recording.md
Status: changes-requested

## Review inputs

- Spec: `specs/formal-review-recording.md`
- Test spec: `specs/formal-review-recording.test.md`
- Proposal: `docs/proposals/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md`
- Governing instructions: `AGENTS.md`, `CONSTITUTION.md`
- Workflow summary: `docs/workflows.md`

## Findings

### SR-001: Change-ID selection rule is required but not defined

Finding ID: SR-001
Severity: major
Location: `specs/formal-review-recording.md`, requirements `R31` and `R32`; missing normative change-ID selection rule for required review-recording artifacts.

Evidence: `R31` says normative change-ID selection rules must live in the spec or a linked formal review recording reference. The draft amendment also uses blocked recording when a change ID cannot be selected, and the proposal requires moving full change-ID selection rules to the formal review recording contract or reference. However, the spec does not define the selection order, deterministic fallback format, ambiguity behavior, or what artifact metadata counts as a valid source.

Required outcome: The spec must define the change-ID selection contract or link to a concrete normative reference that does. Implementers must not need to infer how formal review skills choose `docs/changes/<change-id>/` when recording is required.

Safe resolution: Add a requirement block that chooses the change ID in a deterministic order, such as active change root, reviewed artifact metadata, user-provided change ID, then generated `YYYY-MM-DD-<reviewed-artifact-or-topic>-review-recording`; require `Recording status: blocked` when the result remains ambiguous; and update the test spec to cover that rule.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | Most new requirements are clear, but change-ID selection is left as an ownership requirement rather than a concrete rule. |
| Normative language | pass | The amendment uses testable `MUST` and `SHOULD` language. |
| Completeness | concern | Recording status, Location, examples, and status-sync boundaries are covered; change-ID selection is incomplete. |
| Testability | concern | `T24` can test examples, and `T21`-`T23` can test skill text, but no test can prove an unspecified change-ID algorithm. |
| Examples | pass | New examples are concrete and align with the intended behavior. |
| Compatibility | pass | Historical artifacts and generated output migration boundaries are named. |
| Observability | pass | Recording status and artifact paths make review recording observable. |
| Security/privacy | pass | Secrets and example-data boundaries are covered. |
| Non-goals | pass | Downstream settlement and review-side status sync are excluded from the first slice. |
| Acceptance criteria | concern | Acceptance mentions normative change-ID rules but the actual rule is not yet present. |

## Recommended next stage

Verdict: changes-requested.

Immediate next repository stage: spec revision and spec-review rerun.

Eventual `test-spec` readiness: conditionally-ready after SR-001 is resolved in the spec and test spec.

Downstream implementation readiness: not ready until spec-review passes.
