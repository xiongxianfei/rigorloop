# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/change-record-catalog-registration-and-bounded-read-model.md
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: CRM-SR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r1.md
- Review log: docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md
- Review resolution: docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md
- Open blockers: CRM-SR1
- Immediate next stage: spec revision

## Findings

### CRM-SR1 - Next artifacts route test-spec before plan and plan-review

Finding ID: CRM-SR1
Severity: major
Location: `specs/change-record-catalog-registration-and-bounded-read-model.md:408`
Evidence: The spec's `Next artifacts` section lists `spec-review`, then `test-spec`, then `plan` and `plan-review`. `docs/workflows.md` defines the standard chain as `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement`, and the `spec-review` skill explicitly says not to name `test-spec` as the immediate next stage while architecture or plan still remains.
Required outcome: Revise `Next artifacts` so downstream routing does not place `test-spec` before any required architecture, plan, and plan-review stages.
Safe resolution path: Update the spec's `Next artifacts` to route from `spec-review` to `architecture` or `architecture-review` when required by the architecture gate, otherwise to `plan`, then `plan-review`, then `test-spec`. Preserve Workstream A before Workstream B sequencing inside the later plan or test-spec surfaces rather than using `test-spec` as the immediate post-review artifact.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | pass | Requirement IDs are stable and define observable selector, registry, query-helper, skill-guidance, and compatibility behavior. |
| normative language | pass | `MUST`, `SHOULD`, and `MAY` requirements are testable or intentionally conditional. |
| completeness | concern | The behavioral contract is complete enough, but downstream artifact routing is wrong in `Next artifacts`; see CRM-SR1. |
| testability | pass | Requirements and acceptance criteria map to selector fixtures, registry validation, query-helper probes, legacy/compact metadata cases, and adapter validation. |
| examples | pass | Examples cover registered, unregistered, broad-pattern, actual-changed-path, query, and full-read escalation behavior. |
| compatibility | pass | The spec preserves existing valid change records, existing selector safety, and current lifecycle/readiness semantics. |
| observability | pass | Selector diagnostics, registration debt, query diagnostics, detail pointers, and validation evidence are specified. |
| security/privacy | pass | The query helper and registry contracts reject machine-local paths, secrets, external paths, and command execution from metadata. |
| non-goals | pass | Non-goals protect selector safety, state-owner boundaries, historical migration, workflow semantics, and scaffolding scope. |
| acceptance criteria | pass | Acceptance criteria cover the key registration, query-helper, migration, adapter, and semantic-preservation outcomes. |

## Eventual test-spec readiness

Conditionally-ready after CRM-SR1 is resolved. The requirements are testable, but test-spec should not start until downstream artifact routing is corrected.

## Stop condition

Resolve CRM-SR1 in the spec and rerun spec-review before architecture, planning, test-spec, or implementation relies on this spec.
