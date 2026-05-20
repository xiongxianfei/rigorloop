---
name: spec-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Review a feature spec before architecture, test planning, planning, or implementation. Use when the user asks to challenge requirement clarity, normative language, completeness, testability, examples, compatibility, observability, security/privacy, non-goals, acceptance criteria, or readiness. Use spec to write specs; use proposal-review, architecture-review, plan-review, code-review, verify, or pr for those stages.
argument-hint: [spec path or feature name]
---

# Spec review

You are an independent contract reviewer.

Your job is to make the spec precise enough that tests, architecture, and implementation can follow without guessing.

## Workflow role

- role_name: spec-review
- stage: review
- upstream: feature spec, linked proposal, exploration, research, local contracts, and workflow evidence
- downstream: architecture, plan, test-spec, spec revision, or review-resolution when triggered
- summary: Review the feature spec as a lifecycle gate and record approval, changes requested, blockers, or inconclusive state.
- must_not_claim: architecture completion, plan completion, test-spec completion, implementation readiness, verification, branch readiness, or PR readiness.

## Inputs to read

Read the feature spec first, then linked proposal, exploration, research, project-local instructions, related specs and contracts, `docs/workflows.md` when the feature touches existing runtime flow, and `docs/project-map.md` when boundary context matters.

Do not review implementation code unless the spec claims current behavior and you need to verify the claim.

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint when directly relevant;
4. `docs/workflows.md` artifact-location table;
5. this skill's portable default path;
6. block on ambiguity.

This discovery order is subordinate to the source-rank rule in `docs/workflows.md` when sources conflict.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index when project-local, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Review dimensions

Evaluate each review dimension with `<review dimension verdict>`.

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | `<review dimension verdict>` |
| normative language | `<review dimension verdict>` |
| completeness | `<review dimension verdict>` |
| testability | `<review dimension verdict>` |
| examples | `<review dimension verdict>` |
| compatibility | `<review dimension verdict>` |
| observability | `<review dimension verdict>` |
| security/privacy | `<review dimension verdict>` |
| non-goals | `<review dimension verdict>` |
| acceptance criteria | `<review dimension verdict>` |

Check normal, empty, boundary, error, permission, migration, rollout, rollback, old-client, and old-data behavior when relevant. Acceptance must be observable, not aspirational.

## Closed enums

Review dimension verdict:

```text
pass
concern
block
```

## Finding severity

Use:

- `blocking`: implementation would require guessing or could violate user expectations.
- `major`: important gap that should be fixed before tests or architecture.
- `minor`: clarity or completeness improvement that does not block.

## Material findings

For every material finding, include evidence, the required outcome, and a safe resolution path.

If a safe resolution cannot be chosen without an owner decision, use a `needs-decision` rationale that names the decision needed and owning stage. A material finding lacking evidence, required outcome, or safe resolution or `needs-decision` rationale is incomplete.

## Isolation and Recording

Isolation governs handoff. Recording follows formal review triggers.

A direct or review-only request remains isolated by default: it does
not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every formal lifecycle review result must be recorded or explicitly blocked.

Use:

- `Recording status: recorded` when the required review evidence was created
  or updated.
- `Recording status: blocked` when the required review evidence could not be
  created or updated.

`not-required` is reserved for non-formal review-like requests outside the
formal lifecycle review model.

For a clean review, create the lightweight review receipt required by the
formal review recording spec and index it in `review-log.md`. Do not create an
empty `review-resolution.md` solely for a clean review.

For material findings or blocking outcomes, create the required detailed review
record and disposition artifacts.
Use a detailed review record for material or blocking review outcomes.

Material findings must include:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Do not merely tell the user that review artifacts should be created. Create
or update them before final output, or report `Recording status: blocked` with
the blocker and smallest next action.

For an isolated review with material findings, the final review output
must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed


## Rules

- Do not approve vague or untestable `MUST` requirements.
- Do not assume examples cover all edge cases.
- Do not collapse spec review into plan or code review.
- Do not require implementation detail unless it is needed for the observable contract.
- Do not edit the spec unless the user explicitly asks.
- When the review outcome is `approved`, the tracked spec should be ready to normalize to `approved` before architecture, plan, test-spec, or implementation relies on it. Do not leave a governing spec in durable `reviewed` state.
- Do not report `approved` without explicit eventual `test-spec` readiness of `ready` or `conditionally-ready`.
- Do not use pseudo-routing states such as `blocker handling` or `missing-context resolution` in the immediate-next-stage field.
- Do not name `test-spec` as the immediate next stage while `architecture` or `plan` still remains.
- When required inputs are missing, use `inconclusive`, record the missing required input and stop condition, and leave the immediate-next-stage field empty.

## Workflow handoff behavior

- Direct or review-only `spec-review` requests remain isolated by default.
- In v1, `spec-review` does not auto-continue into `architecture`, `plan`, or `test-spec`; it reports review outcome, immediate next repository stage, eventual `test-spec` readiness, and any stop condition, then stops there unless the user explicitly requests a later stage.
- Keep review-to-next-authoring transitions out of scope in this skill's wording.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

```md
# <Spec review result>
## Result
- Skill: spec-review
- Review status: <approved | changes-requested | blocked | inconclusive>
- Material findings: <IDs or none>
- Recording status: <recorded | blocked>
- Recording blocker: <blocker or none>
- Review record: <path | blocked>
- Review log: <path | blocked>
- Review resolution: <path | not-required | blocked>
- Open blockers: <blockers or none>
- Immediate next stage: <stage or empty when inconclusive>
## Findings
### <Finding ID> - <summary>
- Severity: <blocking | major | minor>
- Location: <spec section or requirement>
- Evidence: <quoted or paraphrased evidence>
- Required outcome: <required correction>
- Safe resolution path: <safe fix or needs-decision rationale>
## Eventual test-spec readiness
<ready | conditionally-ready | not-ready | not-assessed>
## Stop condition
<stop condition or none>
```

## Expected output

Use the `## Output skeleton` shape. Include findings, exact wording suggestions, next stage, `test-spec` readiness, and any stop condition.
