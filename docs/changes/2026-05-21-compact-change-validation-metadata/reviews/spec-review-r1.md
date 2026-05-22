# Spec Review R1 - Compact Change Validation Metadata

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/compact-change-validation-metadata.md
Reviewed artifact: specs/compact-change-validation-metadata.md
Review date: 2026-05-21
Status: changes-requested
Recording status: recorded

## Review inputs

- Spec: `specs/compact-change-validation-metadata.md`
- Accepted proposal: `docs/proposals/2026-05-21-compact-change-validation-metadata.md`
- Proposal review approval: `docs/changes/2026-05-21-compact-change-validation-metadata/reviews/proposal-review-r1.md`
- Change metadata: `docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: CVM-SR1, CVM-SR2, CVM-SR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-21-compact-change-validation-metadata/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md`
- Review resolution: `docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md`
- Open blockers: CVM-SR1, CVM-SR2, CVM-SR3
- Immediate next stage: spec revision

## Findings

### CVM-SR1 - Literal brace escaping is required but not specified

Finding ID: CVM-SR1
Severity: major
Location: `specs/compact-change-validation-metadata.md` R13, AC20
Evidence: R13 says, "The compact path-variable contract MUST define an escape for literal braces before implementation is complete." AC20 says path-variable interpolation defines an escape for literal braces. The spec does not define the actual escape syntax. Test-spec and implementation cannot know whether literal braces are represented as `{{`, `\{`, percent encoding, or something else.
Required outcome: The spec must define one literal-brace escape syntax and the validator behavior for escaped braces before test-spec or implementation relies on it.
Safe resolution path: Add a requirement such as: "A literal `{` or `}` in a compact path template is represented as `{{` or `}}`; validators resolve doubled braces to literal braces before variable interpolation and reject unmatched literal braces." Update examples, edge cases, and acceptance criteria to match the chosen syntax.

### CVM-SR2 - First-exists stage contract lacks the required stage mapping

Finding ID: CVM-SR2
Severity: major
Location: `specs/compact-change-validation-metadata.md` R22-R24, EC10-EC12
Evidence: R22 requires filesystem checks once each artifact class's first-exists lifecycle stage has been reached, and R23 says existence requirements are derived from lifecycle stage and artifact first-exists stage. The spec never defines the artifact-class-to-first-exists-stage table, how the current lifecycle stage is represented in compact metadata, or the ordering used to decide whether a stage has been reached.
Required outcome: The spec must define enough stage semantics for validators and tests to decide when each resolved path must exist.
Safe resolution path: Add a table mapping artifact variables/classes such as `proposal`, `spec`, `test_spec`, `plan`, `review_log`, `review_resolution`, `reviews/*`, and optional transcript files to first-exists stages. Also define where the current lifecycle stage comes from, how stage ordering is compared, and how unknown artifact classes or unknown stages fail.

### CVM-SR3 - `stages_validated` consistency references undefined summary rules

Finding ID: CVM-SR3
Severity: major
Location: `specs/compact-change-validation-metadata.md` R48, AC9, EC7
Evidence: R48 says "`validation_summary.stages_validated` MUST match the stages represented by validation events according to the compact summary rules." The spec does not define those compact summary rules. It is unclear whether `stages_validated` includes only `pass` events, all completed events, skipped events with owner decisions, blocked events, or `not-run` planned stages.
Required outcome: The spec must define exactly how `validation_summary.stages_validated` is derived from `validation_events`.
Safe resolution path: Add a derivation rule such as: "`stages_validated` is the ordered list of event `stage` values whose `result` is `pass`; events with `fail`, `blocked`, `skipped`, or `not-run` are excluded from `stages_validated` and represented through `all_passed: false` and `open_validation_blockers` or skipped/not-run details." If a different rule is desired, state it explicitly and update summary examples and acceptance criteria.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Most requirements are clear, but brace escaping, first-exists stages, and summary-stage derivation are underspecified. |
| normative language | concern | R13 and R48 use normative language while deferring the actual rule. |
| completeness | concern | Core compatibility, bundle, event, count, transcript, and migration behavior is covered; three validator-critical derivation rules are missing. |
| testability | concern | Tests cannot be deterministic for brace escaping, existence-by-stage, or `stages_validated` consistency until the spec defines those rules. |
| examples | concern | Examples cover the main happy path but do not show literal brace escaping, first-exists stage behavior, or summary-stage derivation for non-pass events. |
| compatibility | pass | Legacy compatibility, within-file hybrid rejection, migration boundaries, and rollback are explicit. |
| observability | pass | The spec requires stable validator errors and visible summary, stage, count, blocker, and transcript-reference evidence. |
| security/privacy | pass | The spec rejects secrets, credentials, machine-local paths, hostnames, proxy credentials, and outside-repo transcript references. |
| non-goals | pass | Bulk migration, transcript internals, CLI scaffolding, review-record semantics, and validation selection changes are out of scope. |
| acceptance criteria | concern | Acceptance criteria need concrete coverage for the missing brace escape, first-exists mapping, and `stages_validated` derivation rules. |

## Eventual test-spec readiness

not-ready

## Stop condition

Resolve CVM-SR1, CVM-SR2, and CVM-SR3 in the spec, then rerun spec-review before architecture, plan, test-spec, or implementation relies on the spec.

## Recommendation

Request spec revision. Do not start architecture, planning, test-spec, or implementation until literal-brace escaping, first-exists stage mapping, and `stages_validated` derivation are specified as testable contracts.
