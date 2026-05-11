# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Contributor spec-review
Target: specs/release-token-friendliness-benchmark-for-skills.md
Status: changes-requested

## Review inputs

- Spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Proposal: `docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`
- Related specs: `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md`, `specs/skill-token-cost-optimization.md`, `specs/multi-agent-adapters-first-public-release.md`

## Findings

### RTF-SR1 - Analyzer summary schema conflicts with sanitized raw-JSONL omission

Finding ID: RTF-SR1
Severity: major
Evidence: R14c says that when `raw_jsonl_tracked` is false, `evidence.jsonl` must be empty and the release can rely on analyzer or sanitized summary evidence. R15b then says each analyzer summary must include `run.id` and `run.jsonl`. The spec does not say whether `run.jsonl` may be empty, may point to untracked local raw JSONL, or must be sanitized when raw data is omitted.
Required outcome: Make analyzer summary identity compatible with the raw-or-sanitized evidence contract without requiring private or untracked raw JSONL paths in durable release evidence.
Safe resolution: Update R15 and related examples so analyzer summaries include explicit run source metadata such as `run.id`, `run.raw_jsonl_tracked`, `run.jsonl`, `run.sanitized_source` or `run.sanitized_summary`, and `run.raw_omission_reason`; require `run.jsonl` only when raw JSONL is tracked.

### RTF-SR2 - Non-final blocked/not-run dynamic metadata is required but not shaped

Finding ID: RTF-SR2
Severity: major
Evidence: R6b allows early adoption and RC preparation to use `dynamic_runtime.status: blocked` or `not-run` only when metadata records a reason, owner, environment, follow-up, and whether release may proceed. The required fields in R2d do not include these fields, and no later requirement defines their exact paths or enum values.
Required outcome: Define a testable metadata shape for non-final `blocked` and `not-run` dynamic benchmark states.
Safe resolution: Add a `dynamic_runtime.incomplete` or similarly named metadata block with required fields for `reason`, `owner`, `environment`, `follow_up`, and `release_may_proceed`; require it when non-final `dynamic_runtime.status` is `blocked` or `not-run`.

### RTF-SR3 - First-baseline comparison metadata is ambiguous

Finding ID: RTF-SR3
Severity: major
Evidence: R21a says that if no prior report exists, the first report must declare itself the baseline. R21b says comparison metadata must identify the previous release, previous report path, comparability, and deltas. For the first report, no previous release, previous report, or numeric deltas exist.
Required outcome: Define the exact comparison metadata contract for the first release baseline.
Safe resolution: Add a baseline case that permits empty or `null` previous-release fields, requires `baseline: true` or equivalent, and defines deltas as empty, `null`, or `not-applicable` when no prior report exists. Require numeric deltas only when `comparison.comparable: true` and a previous report exists.

## Checklist coverage

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | Most requirements are precise, but RTF-SR1 and RTF-SR3 leave contradictory interpretations. |
| Normative language | pass | `MUST`, `SHOULD`, `MAY`, and `MUST NOT` are generally used correctly. |
| Completeness | concern | RTF-SR2 leaves a required non-final metadata state underspecified. |
| Testability | changes-requested | RTF-SR1, RTF-SR2, and RTF-SR3 would force validator or test authors to guess. |
| Examples | concern | Examples cover the main flows but do not show analyzer summary behavior when raw JSONL is omitted or first-baseline comparison shape. |
| Compatibility | pass | Existing baseline reports, adapter validation, raw evidence retention, and future report generators are addressed. |
| Observability | pass | Runner output, validator diagnostics, environment fields, and top cost drivers are covered. |
| Security/privacy | concern | RTF-SR1 could accidentally preserve private raw JSONL paths in analyzer summaries. |
| Non-goals | pass | Scope exclusions are explicit and enforceable. |
| Acceptance criteria | concern | Acceptance is observable, but it inherits the three metadata ambiguities above. |

## Review outcome

Outcome: changes-requested

Immediate next repository stage: spec revision

Eventual test-spec readiness: not-ready

Stop condition: Resolve RTF-SR1, RTF-SR2, and RTF-SR3 before approving the spec or using it for architecture, execution planning, test-spec authoring, or implementation.

This direct spec-review request is isolated and does not automatically hand off to downstream stages.
