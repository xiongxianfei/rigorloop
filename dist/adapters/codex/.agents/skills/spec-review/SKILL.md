---
name: spec-review
description: >
  Review a feature spec before architecture, test planning, execution planning, or implementation. Use to challenge requirement clarity, completeness, testability, compatibility, edge cases, observability, and non-goals without reviewing code.
argument-hint: [spec path or feature name]
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

When workflow-managed review findings are recorded under `docs/changes/<change-id>/reviews/`, preserve the first-pass review record before fixes and record dispositions in `review-resolution.md`.

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

## Expected output

- review outcome: `approved`, `changes-requested`, `blocked`, or `inconclusive`;
- findings by severity;
- requirement-by-requirement notes when useful;
- exact wording suggestions;
- immediate next repository stage;
- eventual `test-spec` readiness;
- stop condition or upstream fix surface when approval is denied or readiness is not assessed.
