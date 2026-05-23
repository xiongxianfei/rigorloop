# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/validation-idempotency-and-cache-hit-safety.md
Status: changes-requested

## Review inputs

- Spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Related proposal: `docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md`
- Proposal-review approval: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/proposal-review-r2.md`
- Related contracts: `specs/compact-change-validation-metadata.md`, `specs/test-layering-and-change-scoped-validation.md`, `specs/plan-index-lifecycle-ownership.md`
- Governance: `CONSTITUTION.md`, `docs/workflows.md`

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: `VIC-SR1`, `VIC-SR2`, `VIC-SR3`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md`
- Open blockers: `VIC-SR1`, `VIC-SR2`, `VIC-SR3`
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: revise the spec and rerun spec-review before test-spec, planning, or implementation relies on it.
- No automatic downstream handoff: this review is isolated and does not start architecture, plan, test-spec, or implementation work.

## Findings

### VIC-SR1 - Command and path normalization are underspecified

Finding ID: VIC-SR1
Severity: major
Location: `Requirements` R6-R7 and R13-R15; `Edge cases` EC19-EC20
Evidence: R6 and R7 require the same normalized validator command and command hash. R14 requires the ordered explicit `--path` list after normalization. EC19 says the normalized command and ordered path list determine whether the same paths in a different order are the same command, while EC20 says duplicate explicit paths require deterministic normalization before cache eligibility is allowed. The spec does not define whether path order is preserved or canonicalized, how duplicates participate in the hash, or what "normalized" means for argv and paths.
Required outcome: Define a deterministic command/path normalization contract that tests can implement without guessing.
Safe resolution path: Add requirements that define normalized argv and explicit path handling. For example: preserve user-supplied argv order after repository-relative path normalization; define whether duplicate paths remain distinct entries or are rejected; define whether two commands with the same paths in different orders are distinct cache keys; and require command-hash fixtures for order and duplicate cases.

### VIC-SR2 - Closeout evidence fields are not anchored to the change metadata contract

Finding ID: VIC-SR2
Severity: major
Location: Examples E6-E7; R50-R59; `Error and boundary behavior` EC14-EC15; `Compatibility and migration`
Evidence: The spec introduces `actual-run-pass`, `actual-run-fail`, `blocked`, and `cache-hit-inner-loop`, and examples use `validation_events[].evidence_kind` and `evidence_ref`. R57 says `validate-change-metadata.py` must reject `change.yaml` evidence references that promote cache hits into closeout passes. The spec does not define whether these fields live only in compact `schema_version: 2` `validation_events`, whether legacy `validation` entries may use them, or the exact shape validators must accept or reject.
Required outcome: Define the `change.yaml` data contract for first-slice closeout and cache-hit evidence references.
Safe resolution path: Add a compatibility section or requirements that name the supported metadata shape. For example: first-slice formal cache/closeout evidence references are supported only in compact `schema_version: 2` `validation_events` with explicit fields `stage`, `lifecycle_stage`, `result`, `evidence_kind`, and optional `evidence_ref`; legacy metadata remains valid but cannot claim cache-hit closeout evidence. Then define how `result: pass` interacts with each evidence kind.

### VIC-SR3 - Measurement evidence location and shape are deferred to test-spec

Finding ID: VIC-SR3
Severity: major
Location: R75; `Observability`; `Performance expectations`; `Open questions`
Evidence: R75 requires measurement after implementation, and observability/performance sections require cache-hit count, cache-miss count, eligible command count, estimated time saved, and remaining validation cost. The Open questions section says the test spec should choose where measurement evidence is recorded. Test specs should operationalize requirements, not choose the durable evidence surface for a workflow gate.
Required outcome: Define where Workstream A measurement evidence lives and the minimum fields it records.
Safe resolution path: Add a measurement evidence contract before spec-review approval. For example: `docs/changes/<change-id>/validation-cache-measurement.md` or `.yaml` records total eligible commands, cache-hit count, cache-miss count, estimated time saved, validators still rerun, remaining validation cost, and Workstream B recommendation state. Keep exact fixture names and command invocations for the test spec.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Core cache-hit conditions are clear, but normalization and metadata anchoring need sharper contracts. |
| normative language | pass | The spec uses testable `MUST` language for most safety-critical behavior. |
| completeness | concern | Measurement location and change metadata shape are incomplete for downstream reliance. |
| testability | concern | Most requirements are testable, but command normalization and closeout evidence shape would force test authors to infer behavior. |
| examples | pass | Examples cover pass reuse, invalidation, failed prior result, evidence review, closeout failure, valid closeout, local cache, and Workstream B gating. |
| compatibility | concern | Legacy metadata compatibility is stated, but the new cache/closeout fields are not mapped to compact versus legacy metadata. |
| observability | concern | Cache-hit observability is strong; measurement evidence lacks a durable location. |
| security/privacy | pass | Tracked evidence exclusions for secrets, hostnames, usernames, env dumps, and absolute paths are explicit. |
| non-goals | pass | Workstream B, remote/shared cache, broader validator caching, and closeout cache-skip are excluded. |
| acceptance criteria | concern | Acceptance criteria are mostly aligned but need coverage for normalization, metadata shape, and measurement evidence location. |

## Eventual test-spec readiness

not-ready

The spec is close, but test-spec should not proceed until `VIC-SR1`, `VIC-SR2`, and `VIC-SR3` are resolved.

## Stop condition

Revise the spec to settle command/path normalization, closeout evidence metadata shape, and measurement evidence location. Rerun spec-review before architecture, plan, test-spec, or implementation relies on the spec.
