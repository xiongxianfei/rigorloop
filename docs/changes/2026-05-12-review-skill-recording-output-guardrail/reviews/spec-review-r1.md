# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/formal-review-recording.md
Status: changes-requested

## Review inputs

- Spec: `specs/formal-review-recording.md`
- Accepted proposal: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
- Learn session: `docs/learn/sessions/2026-05-12-review-approval-status-sync.md`
- Governing instructions: `CONSTITUTION.md`, `AGENTS.md`
- Workflow guidance: `docs/workflows.md`

## Findings

### SR1: Status sync is optional where the proposal requires it

Finding ID: SR1
Severity: major
Location: `specs/formal-review-recording.md`, `R30`
Evidence: The accepted proposal says clean or approving formal review results should synchronize the reviewed artifact to its next artifact-specific lifecycle status when the status surface is clear, or report `Status sync: blocked`. The draft spec defines `Status sync: updated` and `Status sync: blocked`, but `R30` says review skills `MAY update` the reviewed artifact's lifecycle/status/readiness/closeout surface. That makes the core status-sync behavior optional even when the status target is clear and edits are allowed.
Required outcome: The spec must require status sync for clean or approving formal review results when the target is clear and edits are allowed, while preserving blocker behavior when edits are forbidden, the status owner is ambiguous, repository state is unavailable, or the artifact lacks an editable status surface.
Safe resolution: Change `R30` from optional permission to a required behavior, for example: "For clean or approving formal review results, review skills MUST update the reviewed artifact's owned lifecycle/status/readiness/closeout surface when the target is clear and edits are allowed; otherwise they MUST report `Status sync: blocked`."

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | Most new requirements are clear, but `R30` weakens the main status-sync requirement. |
| Normative language | concern | `MAY update` should be `MUST update` or `MUST report blocked` for clean/approving outcomes. |
| Completeness | pass | Normal, no-edit, ambiguous target, material finding, and no-material detailed record cases are covered. |
| Testability | concern | Tests cannot assert required status sync while the spec says the update is optional. |
| Examples | pass | Examples E11-E16 align with the intended behavior. |
| Compatibility | pass | Historical artifacts and vocabulary preservation are addressed. |
| Observability | pass | Recording and status sync fields are observable. |
| Security/privacy | pass | Secret handling remains covered. |
| Non-goals | pass | No downstream auto-continuation and no source-code status edits are excluded. |
| Acceptance criteria | concern | Acceptance criteria require clean approvals to update status, but `R30` does not. |

## Recommended next stage

Review outcome: changes-requested.

Immediate next repository stage: spec revision.

Eventual `test-spec` readiness: conditionally-ready after `SR1` is resolved and spec-review reruns clean.

Stop condition: Do not proceed to test-spec, plan, or implementation until `R30` is corrected and this spec-review finding is closed.
