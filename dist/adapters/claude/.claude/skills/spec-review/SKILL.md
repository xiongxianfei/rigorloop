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

Isolation governs handoff. Recording follows the finding. These are
independent.

A direct or review-only review request remains isolated by default: it
does not automatically continue into downstream workflow stages.
Isolation does not suppress recording.

A material finding requires a durable change-local review record under
`docs/changes/<change-id>/reviews/`. This applies regardless of whether
the review was workflow-managed or isolated.

The durable record must be created before review-driven edits begin. If
review-driven edits already began before the durable record exists, the
record is reconstructed and must disclose source, timing, available
evidence, stable Finding IDs, and known fidelity loss.

A tracked artifact is any version-controlled repository file whose
change will be committed or reviewed as part of the work. This includes
lifecycle artifacts, governance files, workflow summaries, skills,
specs, schemas, scripts, generated outputs, README content, and
change-local artifacts. Edits to ephemeral chat output, local scratch
files, or unversioned drafts are not tracked artifact edits.

The recording obligation is also a resolution-step gate. A revision
made in response to a material finding is incomplete until the finding
is durably recorded.

Materiality is governed by `CONSTITUTION.md` and is not redefined here.
A material finding requires evidence, required outcome, and a safe
resolution path or `needs-decision` rationale before it drives fixes.

Operational shortcut: if a finding changes or blocks a tracked artifact
edit, changes scope, changes requirements, changes architecture,
changes sequencing, changes validation, creates follow-up work, or
requires disposition, treat it as material unless the reviewer
explicitly records a non-material rationale.

Reconstructed records are governed by `specs/rigorloop-workflow.md`.

Clean reviews with no material findings remain lightweight and may
settle in the reviewed artifact when no detailed-record trigger
applies.

For an isolated review with material findings, final review output names
the isolated handoff status, material Finding IDs, required durable
review record path or reconstruction requirement, confirms
`review-resolution.md` is required, and states the next allowed action:
`create-change-local-record-before-fixing`,
`reconstruct-record-because-fixes-already-began`, or
`stop-for-owner-decision`. Downstream handoff remains stopped unless
explicitly requested.

## Detailed Review Records

Use these detailed review record triggers for formal lifecycle reviews:

- material findings
- stage-owned non-approval outcomes that block downstream progress or require revision
- reconstructed review evidence
- closeout evidence citation
- explicit reviewer or maintainer request

Examples of stage-owned non-approval outcomes include `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, and equivalent blocking stage-specific outcomes.

When a detailed review file is created, `review-log.md` indexes it. Material findings need stable `Finding ID` values and disposition in `review-resolution.md`.

In this contract, clean reviews can settle artifact-locally when no detailed review record triggers apply. For no-material review events, no-material detailed records need `review-log.md` but not an empty `review-resolution.md`. Likewise, artifact-local settlement must not replace detailed review records when a trigger applies.

Do not add a dedicated `pr-review` stage. It is an unsupported review stage unless a later approved spec extends the stage set. A material maintainer PR comment that needs disposition must first be promoted into a supported formal lifecycle review record with a stable `Finding ID`.

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

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- review outcome: `approved`, `changes-requested`, `blocked`, or `inconclusive`;
- findings by severity;
- requirement-by-requirement notes when useful;
- exact wording suggestions;
- immediate next repository stage;
- eventual `test-spec` readiness;
- stop condition or upstream fix surface when approval is denied or readiness is not assessed.
