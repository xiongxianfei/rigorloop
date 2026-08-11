# Spec Review R1: Workflow Skill Simplification

Review ID: spec-review-r1
Stage: spec-review
Round: r1
Reviewer: Codex independent contract reviewer
Target: specs/workflow-skill-simplification.md
Reviewed artifact: `specs/workflow-skill-simplification.md`
Status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: WFSIM-SR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-11-workflow-skill-simplification/reviews/spec-review-r1.md
- Review log: docs/changes/2026-08-11-workflow-skill-simplification/review-log.md
- Review resolution: docs/changes/2026-08-11-workflow-skill-simplification/review-resolution.md
- Open blockers: stateless automation commands have no valid assembly in the claimed closed lattice
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: revise and rereview the invocation assembly contract before architecture assessment

## Findings

### Finding WFSIM-SR1

Finding ID: WFSIM-SR1
Severity: major
Location: R4-R5, R18-R19, BND-INPUT-001, AC1
Evidence: R19 supports `auto: status` and `auto: off` when no selected change or active run and requires the automation reference only. In that case `automation_command_context` is true while governed, armed, and guide-authoring contexts are false. R5 names six valid assemblies, but `WPB-automation-bootstrap` is limited by R7 to a new target command that creates governed identity. The stateless status/off combination therefore has neither a valid assembly nor an explicit stop despite being required to succeed.
Required outcome: Add one valid stateless automation-command assembly, update the closed assembly count and boundary record, and distinguish it from target bootstrap and durable armed automation.
Safe resolution path: Define `WPS-stateless-automation-command` for `status` or `off` with no selected change and no active run; load `SKILL.md` plus the automation reference; return `no-active-run`; create no state. Update R5, R19, BND-INPUT-001, E1 or a new example, AC1, measurements, and static fixture coverage. Preserve `WPB` for new target commands only.
needs-decision rationale: none; the accepted proposal already requires the stateless success behavior, so this revision only closes its omitted assembly identity.

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Individual requirements are precise, but the valid-profile count contradicts R19. |
| normative language | pass | Normative obligations consistently use testable `MUST` and `MUST NOT` forms. |
| completeness | block | One supported predicate combination is absent from the closed assembly lattice. |
| testability | concern | R19 is testable, but AC1 would classify its input as outside the six valid assemblies. |
| examples | concern | No example owns the stateless status/off success path. |
| compatibility | pass | Existing command spelling, state meaning, and no-migration boundary are preserved. |
| observability | pass | Diagnostics, evidence, and package measurements are explicit. |
| security/privacy | pass | Acceptance remains repository-local and excludes runtime credentials and transcripts. |
| non-goals | pass | Runtime, schema, workflow-order, and permanent-validator expansion remain excluded. |
| acceptance criteria | block | AC1 cannot be satisfied together with R19 until the assembly set is closed. |

## Recommended wording

- Add `WPS-stateless-automation-command` as the seventh valid assembly.
- Keep `WPS` state-free and limited to `status` or `off` when no selected change and no active run.
- Keep `WPB` transient and limited to a new target command requiring governed identity establishment.
- Extend measurement and fixture obligations to `WPS`.

## Recommendation

Revise the spec through the bounded correction path, then perform `spec-review-r2`. Architecture assessment remains blocked until the rereview is approved.
