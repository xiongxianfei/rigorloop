# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Contributor spec-review
Target: specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md
Status: changes-requested

## Review inputs

- Spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Proposal: `docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Existing approved contract: `specs/release-token-friendliness-benchmark-for-skills.md`
- Governance: `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`
- Prior proposal review records: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/proposal-review-r1.md`, `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/proposal-review-r2.md`

## Findings

### EDTF-SR1 - Required benchmark waiver role is internally inconsistent

Finding ID: EDTF-SR1
Severity: major
Status: open

Evidence: R8g says final public releases with required benchmark `fail` or `inconclusive` block unless there is a valid `release-owner` waiver. R9a then limits valid waiver approval roles to `release-owner`, `release-manager`, and `repository-maintainer`, and R9b requires an allowed `approved_role`.

Problem: Implementers cannot tell whether `release-manager` and `repository-maintainer` are valid approvers for required result-quality waivers or whether only `release-owner` is valid. This affects token-cost validator behavior and release-gate outcomes.

Required outcome: The spec must use one waiver authority rule for required benchmark result-quality waivers.

Safe resolution: Change R8g to refer to a valid required-benchmark result-quality waiver, then let R9 define the allowed approval roles. If the desired policy is stricter, change R9a to only allow `release-owner` for required benchmark waivers and move the broader role enum to non-required or non-final waivers.

### EDTF-SR2 - Claimed optional benchmark failure semantics are underspecified

Finding ID: EDTF-SR2
Severity: major
Status: open

Evidence: R4a says missing optional extended benchmarks do not block unless the release claims coverage for the optional benchmark or changed-skill policy makes the benchmark required. R8h says optional `fail` or `inconclusive` results warn when they are not required and not claimed as release coverage. The spec does not state what happens when an optional benchmark is claimed as release coverage and then is missing, failed, inconclusive, or not reviewed.

Problem: Release validation and token-cost validation would need to guess whether claimed optional coverage follows required-benchmark gates, blocks only when missing, blocks on result quality, or must be downgraded to a warning.

Required outcome: The spec must define release-gate behavior for optional benchmarks that are explicitly claimed as release coverage.

Safe resolution: Add a requirement that an optional benchmark claimed as release coverage is treated as release-required for evidence and result-quality purposes: missing, invalid, failed, not-reviewed, or unwaived inconclusive claimed optional coverage blocks final release. Alternatively, require the report to remove the claim and record the run as optional warning evidence before validation can pass.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | Waiver authority and claimed optional coverage gates have multiple plausible interpretations. |
| Normative language | concern | `release-owner waiver` conflicts with the allowed-role enum. |
| Completeness | concern | Claimed optional benchmark failure cases are not fully specified. |
| Testability | concern | Tests cannot assert a single expected result for claimed optional failures or non-owner waiver roles. |
| Examples | pass | Examples cover core, carryover, optional warning, changed-skill requirement, generated trace, context transport, and architecture-review behavior. |
| Compatibility | pass | v1/v2 baseline and pre-transition evidence behavior are covered. |
| Observability | pass | Coverage metadata, result-quality metadata, warnings, and required-context visibility are defined. |
| Security/privacy | pass | Local paths, private output, waiver surfaces, and fixture data are bounded. |
| Non-goals | pass | Exclusions are explicit and enforceable. |
| Acceptance criteria | concern | Acceptance criteria do not yet force the two ambiguous release-gate cases to be resolved. |

## Outcome

Review outcome: changes-requested

Immediate next repository stage: spec

Eventual test-spec readiness: not-ready

Stop condition: Resolve EDTF-SR1 and EDTF-SR2 in the spec, then rerun `spec-review`.
