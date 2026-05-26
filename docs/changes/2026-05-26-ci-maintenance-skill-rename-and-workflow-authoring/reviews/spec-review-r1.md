# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Target: specs/ci-maintenance-skill.md
Reviewed artifact: specs/ci-maintenance-skill.md
Review date: 2026-05-26
Reviewer: Codex spec-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: CIM-SR1, CIM-SR2, CIM-SR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/spec-review-r1.md
- Review log: docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-log.md
- Review resolution: docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-resolution.md
- Open blockers: CIM-SR1, CIM-SR2, CIM-SR3
- Immediate next stage: spec revision

## Findings

## Finding CIM-SR1

Finding ID: CIM-SR1
Severity: major
Location: specs/ci-maintenance-skill.md, `CIM-R1` through `CIM-R4`; `specs/skill-contract.md`, `R29g`
Evidence: The spec requires the renamed skill name and front matter `name: ci-maintenance`, but it does not require the normalized published-skill frontmatter metadata required by the skill contract. `specs/skill-contract.md` requires a normalized published skill to include frontmatter `version` and `schema-version` fields.
Required outcome: Add requirements and acceptance criteria requiring the renamed `ci-maintenance` skill front matter to include `version` and `schema-version`, with the current reviewed schema version when applicable.
Safe resolution path: Add a requirement such as `CIM-R3a. The ci-maintenance skill front matter MUST include version and schema-version fields required by the published-skill contract.` Add acceptance criteria and validation coverage proving `skills/ci-maintenance/SKILL.md` includes those fields.
needs-decision rationale: none

## Finding CIM-SR2

Finding ID: CIM-SR2
Severity: major
Location: specs/ci-maintenance-skill.md, `Next artifacts`
Evidence: The spec lists `test-spec` before `plan` and `plan-review` in `Next artifacts`. `docs/workflows.md` defines the per-change chain as `spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec`, and states that after `spec-review`, the immediate next stage is `architecture` when needed, otherwise `plan`; `plan-review` remains the normal immediate handoff into `test-spec`.
Required outcome: Align `Next artifacts` with the repository workflow sequence. Because this change touches public skill identity, resources, generated adapters, validators, and workflow guidance, the spec should route from `spec-review` to architecture assessment or `plan`, then `plan-review`, then `test-spec`.
Safe resolution path: Replace the `Next artifacts` list with `spec-review`, `architecture` and `architecture-review` if required, `plan`, `plan-review`, `test-spec`, `implementation`, `code-review`, `review-resolution when triggered`, `explain-change`, `verify`, and `pr`. If architecture is intentionally not required, record a rationale instead of silently skipping it.
needs-decision rationale: none

## Finding CIM-SR3

Finding ID: CIM-SR3
Severity: major
Location: specs/ci-maintenance-skill.md, `CIM-R37`
Evidence: `CIM-R37` says workflows default to `permissions: contents: read` unless a known workflow need requires a "narrower job-specific elevation." That phrase is internally contradictory: an elevation is broader or additional permission, while "narrower" implies reducing permission.
Required outcome: Clarify the permissions contract so the default is least privilege and any additional or broader job-specific permission is justified by a known workflow need.
Safe resolution path: Replace the final clause with wording such as: `unless a known workflow need requires additional or broader job-specific permissions, and that elevation is justified in the workflow rationale.` Keep the default `permissions: contents: read` behavior.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
|---|---|---|
| requirement clarity | concern | Most requirements are precise, but CIM-SR3 leaves a contradictory permissions clause. |
| normative language | concern | MUST clauses are mostly testable; CIM-SR1 shows one required metadata obligation missing from the normative set. |
| completeness | concern | The spec covers the proposal well, but omits normalized frontmatter metadata and has stale downstream sequencing. |
| testability | concern | Rename, resources, risk map, and command-boundary checks are testable; frontmatter metadata coverage needs to be added. |
| examples | pass | Examples cover hard rename, missing commands, portability, unmapped surfaces, and workflow review. |
| compatibility | concern | Hard rename is clear, but downstream sequencing should match the workflow contract before relying on the spec. |
| observability | pass | Validation and adapter evidence are named clearly. |
| security/privacy | concern | Security posture is strong overall, but CIM-SR3 needs unambiguous permissions-elevation wording. |
| non-goals | pass | Non-goals preserve repository CI behavior and exclude deployment, release, and alias support. |
| acceptance criteria | concern | Acceptance criteria need frontmatter metadata coverage and should align with the corrected sequencing. |

## Eventual test-spec readiness

not-ready

The spec has enough structure for a focused test spec after revision, but test-spec authoring should wait until the metadata requirement, downstream sequence, and permissions wording are corrected.

## Stop condition

Material findings CIM-SR1, CIM-SR2, and CIM-SR3 require spec revision before approval.

## Recommended spec edits

- Add explicit `version` and `schema-version` frontmatter requirements and acceptance criteria for `ci-maintenance`.
- Update `Next artifacts` to follow `spec-review -> architecture when needed -> plan -> plan-review -> test-spec`.
- Rewrite `CIM-R37` so broader job-specific permissions are allowed only when justified by a known workflow need.

## No-finding statement

Not applicable. This review recorded material findings.
