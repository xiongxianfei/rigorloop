# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/downstream-status-settlement-before-reliance.md
Status: changes-requested

## Review inputs

- Spec: `specs/downstream-status-settlement-before-reliance.md`
- Proposal: `docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md`
- Workflow summary: `docs/workflows.md`

## Findings

### SR-001: Blocked settlement output requires a `New status` even when no target exists

Finding ID: SR-001
Severity: major
Location: `specs/downstream-status-settlement-before-reliance.md`, requirements `R17`, `R22`, `R24`, and settlement output shape.

Evidence: `R17` requires blocked settlement when the artifact type, lifecycle field, or next status is not listed. `R22` and the output shape still require every settlement block to include `new status`. In missing-mapping or ambiguous-ADR cases, the blocker is precisely that no deterministic new status can be selected.

Required outcome: The spec must define what `New status` contains for blocked settlement, including blocked cases where a target status is unknown or not applicable.

Safe resolution: Clarify the settlement output contract so blocked settlement can report the intended target status when known, or `not-applicable`/equivalent when no deterministic target exists. Keep `Settlement blocker` as the required explanation for why settlement could not proceed.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | The settlement-output requirements are ambiguous for blocked unmapped cases. |
| Normative language | pass | Requirements use normative language consistently. |
| Completeness | concern | Normal, blocked, no-edit, unknown-vocabulary, and later-slice boundaries are covered, but blocked output shape is incomplete. |
| Testability | concern | Tests cannot assert `New status` for blocked unknown mappings until the field's blocked value is defined. |
| Examples | pass | Examples match the first-slice behavior. |
| Compatibility | pass | Historical artifacts are not bulk-migrated and formal review recording is unchanged. |
| Observability | concern | Settlement output is observable, but one required field is underdefined for blockers. |
| Security/privacy | pass | No new sensitive data or authorization behavior is introduced. |
| Non-goals | pass | Later skills, review-side sync, and lifecycle-validator enforcement are excluded. |
| Acceptance criteria | concern | AC6 requires blocked output, but the blocked output field semantics need clarification. |

## Recommended next stage

Verdict: changes-requested.

Immediate next repository stage: spec revision and spec-review rerun.

Eventual `test-spec` readiness: conditionally-ready after SR-001 is resolved in the spec.

Downstream implementation readiness: not ready until spec-review passes.
