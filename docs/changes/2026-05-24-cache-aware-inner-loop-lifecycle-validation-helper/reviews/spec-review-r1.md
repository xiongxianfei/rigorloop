# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/validation-idempotency-and-cache-hit-safety.md
Status: changes-requested

## Review inputs

- Spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Related proposal: `docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
- Proposal-review approval: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/proposal-review-r1.md`
- Existing test spec context: `specs/validation-idempotency-and-cache-hit-safety.test.md`
- Workflow guidance: `docs/workflows.md`
- Governance: `CONSTITUTION.md`

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: `VIC-IH-SR1`, `VIC-IH-SR2`, `VIC-IH-SR3`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md`
- Review resolution: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md`
- Open blockers: `VIC-IH-SR1`, `VIC-IH-SR2`, `VIC-IH-SR3`
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: revise the spec and rerun spec-review before architecture, plan, test-spec, or implementation relies on the helper amendment.
- No automatic downstream handoff: this review is isolated and does not start architecture, plan, test-spec, or implementation work.

## Findings

### VIC-IH-SR1 - Helper command normalization does not define what prior pass can be reused

Finding ID: VIC-IH-SR1
Severity: major
Location: `Requirements` R1, R6-R8, R131-R134; `Command and explicit-path normalization`; `Cache-aware inner-loop helper mode`; Examples E10-E11.
Evidence: R6-R8 require the same normalized command, command hash, and input-surface hash. R131-R134 add `explicit-paths-inner-loop` and say it evaluates the same explicit-path lifecycle command-family cache identity as `explicit-paths`. The normalization section says the helper uses the same command-family cache identity, but it does not define whether the helper's normalized command hash uses the literal `--mode explicit-paths-inner-loop` argv or a canonical direct `--mode explicit-paths` argv. If it uses the literal helper mode, it cannot reuse prior direct `explicit-paths` actual-run passes; if it canonicalizes to direct `explicit-paths`, the spec does not say how evidence records the displayed helper command versus the normalized cache command.
Required outcome: Define the cache identity normalization relationship between `explicit-paths-inner-loop` and direct `explicit-paths` so implementers know which previous passing event the helper may reuse.
Safe resolution path: Revise the spec to state whether the helper's cache identity normalizes the helper mode to the canonical direct `explicit-paths` command, or whether it keys on the literal helper mode. If it normalizes to direct `explicit-paths`, define the exact canonical argv used for command hash, prior passing event matching, and evidence recording. If it keys on the helper mode, update the adoption rationale and examples so they do not imply reuse of prior direct actual-run passes.
needs-decision rationale: none

### VIC-IH-SR2 - Non-goal conflicts with helper eligibility

Finding ID: VIC-IH-SR2
Severity: major
Location: `Requirements` R1-R3; `Non-goals`.
Evidence: R1 allows cache eligibility for the explicit-path lifecycle command family including `--mode explicit-paths-inner-loop`, and R3 excludes modes other than `explicit-paths` and `explicit-paths-inner-loop`. The Non-goals section still says, "Do not cache validators other than `validate-artifact-lifecycle.py --mode explicit-paths` in the first slice." A downstream reader can reasonably read that as excluding the new helper mode.
Required outcome: Remove the normative conflict between the updated helper eligibility requirements and the unchanged non-goal excluding validators other than direct `explicit-paths`.
Safe resolution path: Revise the non-goal to exclude validators outside the explicit-path lifecycle command family while naming `explicit-paths-inner-loop` as the only allowed helper mode, or otherwise make the non-goal use the same eligibility language as R1 and R3.
needs-decision rationale: none

### VIC-IH-SR3 - Measurement schema omits helper fields from the normative field list

Finding ID: VIC-IH-SR3
Severity: major
Location: R121, R129, R157, `Workstream A measurement evidence`, AC45.
Evidence: R157 says the measurement surface must distinguish helper invocations, cache hits, cache misses, actual-run fallbacks, and closeout actual runs. The YAML example and AC45 include `helper_invocations`, `actual_run_fallbacks`, and `closeout_actual_runs`. But R121's MUST include summary field list still names only the original fields: `eligible_commands`, `cache_hits`, `cache_misses`, `cache_disabled`, `actual_runs`, `estimated_seconds_saved`, `remaining_validation_seconds`, and `cache_hit_rate`. R129's impossible-count rule also checks only the original `cache_hits + cache_misses + cache_disabled` relationship.
Required outcome: Make the measurement schema internally consistent for helper-specific fields and count relationships.
Safe resolution path: Update R121 and related measurement requirements so the required summary field list includes `helper_invocations`, `actual_run_fallbacks`, and `closeout_actual_runs`, or explicitly place those fields elsewhere. Add count consistency rules for helper fields, such as `actual_run_fallbacks <= helper_invocations`, helper cache hits plus fallbacks not exceeding helper invocations, and closeout actual runs remaining separate from helper cache hits.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Most helper behavior is clear, but the cache identity normalization for helper mode versus direct mode is underspecified. |
| normative language | concern | The new `MUST` requirements are generally testable, but the non-goal conflicts with R1/R3 and the measurement field requirements conflict with the example/AC. |
| completeness | concern | The helper contract covers safe evidence writes, CI exclusion, closeout boundary, and selector routes, but prior-pass matching and measurement consistency need revision. |
| testability | concern | Tests cannot know whether a prior direct `explicit-paths` actual run should satisfy a helper cache hit until command normalization is specified. |
| examples | concern | E10 implies the helper can use existing explicit-path cache identity, but the normalized command contract does not say how. |
| compatibility | pass | Existing direct `explicit-paths`, closeout, verify, PR-readiness, and CI behavior are preserved in concept. |
| observability | concern | Helper output and formal evidence visibility are covered; measurement observability needs a consistent schema. |
| security/privacy | pass | Safe evidence path, repository-relative evidence, local-cache, and published-skill privacy boundaries are explicit. |
| non-goals | concern | One non-goal still excludes everything other than direct `explicit-paths`, conflicting with the helper amendment. |
| acceptance criteria | concern | AC33-AC45 are useful, but AC35 and AC45 depend on the unresolved cache normalization and measurement-schema details. |

## Eventual test-spec readiness

not-ready

The test spec should not be amended until `VIC-IH-SR1`, `VIC-IH-SR2`, and `VIC-IH-SR3` are resolved and spec-review reruns.

## Stop condition

Revise the spec to settle helper command normalization, eligibility/non-goal consistency, and measurement field/count consistency. Rerun spec-review before architecture, plan, test-spec, or implementation relies on the helper amendment.
