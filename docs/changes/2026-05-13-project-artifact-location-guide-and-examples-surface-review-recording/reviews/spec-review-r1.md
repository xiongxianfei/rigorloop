# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/project-artifact-location-guide-and-examples-surface.md
Reviewed artifact: specs/project-artifact-location-guide-and-examples-surface.md
Review date: 2026-05-13
Status: changes-requested
Recording status: recorded

## Review inputs

- Spec: `specs/project-artifact-location-guide-and-examples-surface.md`
- Proposal: `docs/proposals/2026-05-13-project-artifact-location-guide-and-examples-surface.md`
- Governing instructions: `AGENTS.md`, `CONSTITUTION.md`
- Related specs: `specs/formal-review-recording.md`, `specs/skill-contract.md`, `specs/rigorloop-workflow.md`
- Workflow summary: `docs/workflows.md`

## Findings

### SR-001: Shared skill lookup wording can bypass specs and schemas

Finding ID: SR-001
Severity: major
Location: `specs/project-artifact-location-guide-and-examples-surface.md`, requirements `R2` and `R5a`.

Evidence: `R2` defines placement conflict rank with approved project specs or schemas before `docs/workflows.md`. `R5a` then requires shared public-skill lookup wording that goes from active plan/change metadata/reviewed artifact path directly to the `docs/workflows.md` artifact-location table, then the skill default path. That required wording omits the spec/schema source from `R2`.

Required outcome: The spec must make the stage-skill lookup rule consistent with the global source-rank rule, or explicitly state that the short shared wording is subordinate to approved specs and schemas and cannot bypass them.

Safe resolution: Update `R5a` to include approved project specs or schemas before the workflow guide, or add a directly adjacent requirement saying the shared lookup wording is a concise stage-skill form that still obeys `R2` and `R2a` when a governing spec or schema constrains placement.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | Most requirements are clear, but `R2` and `R5a` create conflicting lookup behavior. |
| Normative language | pass | Normative language is generally testable and scoped. |
| Completeness | pass | Normal, boundary, retained-fixture, examples, migration, and rollback behavior are covered. |
| Testability | concern | Tests can prove each rule, but `R5a` cannot be tested consistently against `R2` until the conflict is resolved. |
| Examples | pass | Examples are concrete and align with the intended contract. |
| Compatibility | pass | Existing paths, customized projects, retained fixtures, and rollback are addressed. |
| Observability | pass | Artifact changes and validation surfaces are observable. |
| Security/privacy | pass | Secrets and public-skill internal-detail exposure are addressed. |
| Non-goals | pass | Scope exclusions are explicit and enforceable. |
| Acceptance criteria | pass | Acceptance criteria are observable. |

## Recommended next stage

Verdict: changes-requested.

Immediate next repository stage: spec revision and spec-review rerun.

Eventual `test-spec` readiness: conditionally-ready after SR-001 is resolved in the spec.

Downstream implementation readiness: not ready until spec-review passes.
