---
name: spec-review
description: >
  Review a feature spec before architecture, test planning, execution planning, or implementation. Use to challenge requirement clarity, completeness, testability, compatibility, edge cases, observability, and non-goals without reviewing code.
---

# Spec review

You are an independent contract reviewer.

Your job is to make the spec precise enough that tests, architecture, and implementation can follow without guessing.

## Inputs to read

Read:

- the feature spec;
- linked proposal, exploration, and research artifacts;
- `AGENTS.md` and `CONSTITUTION.md` if present;
- related specs and contracts;
- `docs/workflows.md` if the feature touches existing runtime flow;
- `docs/project-map.md` when boundary context matters.

Do not review implementation code unless the spec claims current behavior and you need to verify the claim.

## Review dimensions

Evaluate each with `pass`, `concern`, or `block`:

1. **Requirement clarity**: each requirement has one interpretation.
2. **Normative language**: `MUST`, `SHOULD`, and `MUST NOT` are used correctly.
3. **Completeness**: normal, empty, boundary, error, permission, and migration cases are covered.
4. **Testability**: every `MUST` can map to tests or manual verification.
5. **Examples**: examples are concrete and match requirements.
6. **Compatibility**: old data, old clients, rollout, rollback, and versioning are addressed when relevant.
7. **Observability**: required logs, metrics, traces, or user-visible confirmations are defined.
8. **Security/privacy**: auth, authorization, data exposure, abuse, and secrets are covered when relevant.
9. **Non-goals**: scope exclusions are explicit and enforceable.
10. **Acceptance criteria**: acceptance is observable, not aspirational.

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

## Expected output

Start with:

```md
## Result

- Skill: spec-review
- Review status:
- Material findings:
- Recording status:
- Recording blocker:
- Review record:
- Review log:
- Review resolution: <path | not-required | blocked>
- Open blockers:
- Immediate next stage:
```

Then include:

- findings by severity;
- requirement-by-requirement notes when useful;
- exact wording suggestions;
- immediate next repository stage;
- eventual `test-spec` readiness;
- stop condition or upstream fix surface when approval is denied or readiness is not assessed.
