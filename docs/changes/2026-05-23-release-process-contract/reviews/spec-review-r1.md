# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/release-process-contract.md
Status: changes-requested

## Review inputs

- Spec: `specs/release-process-contract.md`
- Related proposal: `docs/proposals/2026-05-23-release-process-contract.md`
- Proposal-review approval: `docs/changes/2026-05-23-release-process-contract/reviews/proposal-review-r2.md`
- Related release specs: `specs/rigorloop-npm-publication.md`, `specs/publish-next-release-with-single-authored-skill-source.md`, `specs/stop-tracking-generated-public-adapter-skill-bodies.md`
- Related evidence-routing spec: `specs/change-record-catalog-registration-and-bounded-read-model.md`
- Governance: `CONSTITUTION.md`, `docs/workflows.md`

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: `REL-SR1`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-release-process-contract/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-23-release-process-contract/review-log.md`
- Review resolution: `docs/changes/2026-05-23-release-process-contract/review-resolution.md`
- Open blockers: `REL-SR1`
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: revise the spec and rerun spec-review before architecture, plan, test-spec, or implementation relies on it.
- No automatic downstream handoff: this review is isolated and does not start architecture, plan, test-spec, or implementation work.

## Findings

### REL-SR1 - Emergency deferrals conflict with the unconditional full release gate

Finding ID: REL-SR1
Severity: major
Location: `specs/release-process-contract.md` lines 107, 213-215, and 336
Evidence: REL-R14 says "A release MUST pass the full release gate before publish." REL-R63 says emergency release evidence records "which gates were deferred" and who approved deferral. AC-REL-005 says the full gate is required "except for recorded emergency deferrals." The requirements therefore contain both an unconditional full-gate requirement and an emergency deferred-gate path, so implementers cannot tell whether an emergency release may publish with approved deferred gates.
Required outcome: Make the emergency exception explicit in the normative requirements so the hard gate remains the default and emergency deferral is the only recorded exception.
Safe resolution path: Revise REL-R14 or add an adjacent requirement such as: "A release MUST pass the full release gate before publish unless it is an emergency release with recorded owner-approved gate deferrals under REL-R63. Non-deferred gates, release evidence creation, secret suppression, and post-publish registry verification remain mandatory." Ensure AC-REL-005 and the emergency edge case cite the same exception.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | The release process boundary, evidence, npm, verification, and recovery requirements are clear; the emergency gate exception is contradictory. |
| normative language | concern | Most `MUST` requirements are testable, but REL-R14 conflicts with REL-R63 and AC-REL-005. |
| completeness | pass | The spec covers process boundary, versioning, gate, evidence, npm path, registry verification, failure states, compatibility, observability, and security. |
| testability | concern | Tests cannot assert both unconditional full-gate pass and emergency deferred-gate publish behavior without a clarified exception. |
| examples | pass | Examples cover routine publish, release-process change, generated-output drift, manual fallback, bad package content, and plan-index boundary. |
| compatibility | pass | The spec preserves historical releases, release-specific specs, and non-release package behavior. |
| observability | pass | Release evidence reconstruction requirements are explicit. |
| security/privacy | pass | Secret, token, OTP, private environment, and machine-local path exclusions are explicit. |
| non-goals | pass | Package behavior, CLI behavior, adapter layout, staged publishing, release CLI, and historical backfill are excluded. |
| acceptance criteria | concern | AC-REL-005 contains the right exception, but the requirement body must match it. |

## Eventual test-spec readiness

not-ready

The spec is close, but test-spec should not proceed until `REL-SR1` is resolved and spec-review reruns.

## Stop condition

Revise the spec to settle the full-gate versus emergency-deferral rule. Rerun spec-review before architecture, plan, test-spec, or implementation relies on the spec.
