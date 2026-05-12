# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/formal-review-recording.md
Status: changes-requested

## Review inputs

- Spec: `specs/formal-review-recording.md`
- Proposal: `docs/proposals/2026-05-12-record-every-formal-review.md`
- Governing instructions: `AGENTS.md`, `CONSTITUTION.md`
- Related spec: `specs/formal-review-recording.md`

## Findings

### SR-001: Isolated clean review receipts lack a root-shape contract

Finding ID: SR-001
Severity: major
Location: `specs/formal-review-recording.md`, requirements `R4`, `R5`, and `R31`; missing root-shape rule for isolated or review-only clean formal review receipts.

Evidence: `R5` requires isolated or review-only no-material formal reviews to create a clean review receipt or report blocked recording. `R31` requires selecting a change ID and creating required artifacts under `docs/changes/<change-id>/`. But `R4` only defines the initial review-record root when a workflow-managed formal review triggers a review file before a change-local root exists. The draft does not state whether an isolated clean receipt using a generated change ID needs `change.yaml`, only `review-log.md`, or another minimal root shape.

Required outcome: The spec must define the minimal change-local root for isolated or review-only clean formal review receipts when no existing change root exists.

Safe resolution path: Add a requirement that no-material clean receipt roots, including isolated/review-only clean reviews, include at least `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md`, while still not creating `review-resolution.md` solely for the clean review. Alternatively, define a different explicit root shape and update examples, edge cases, and acceptance criteria to match it.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | The clean receipt rule is clear, but the root shape for isolated clean receipts is not. |
| Normative language | pass | The new requirements use testable normative language. |
| Completeness | concern | Normal clean review behavior is covered; isolated clean review root creation is incomplete. |
| Testability | concern | Tests cannot reliably assert the generated root shape for isolated clean reviews without the missing rule. |
| Examples | concern | Examples cover clean receipts and artifact status, but not isolated clean receipt root creation. |
| Compatibility | pass | Prospective rollout and historical clean settlements are addressed. |
| Observability | pass | Review-log indexing and recording output are observable. |
| Security/privacy | pass | Existing review artifact privacy rules remain applicable. |
| Non-goals | pass | Scope exclusions remain enforceable. |
| Acceptance criteria | concern | Acceptance covers clean receipts generally but not the isolated generated-root case. |

## Recommended next stage

Verdict: changes-requested.

Immediate next repository stage: spec revision and spec-review rerun.

Eventual `test-spec` readiness: conditionally-ready after SR-001 is resolved.

Downstream implementation readiness: not ready until spec-review passes.
