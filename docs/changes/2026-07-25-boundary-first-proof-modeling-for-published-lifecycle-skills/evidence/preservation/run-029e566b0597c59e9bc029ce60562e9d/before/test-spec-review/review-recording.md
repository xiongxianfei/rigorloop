---
name: test-spec-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Independently review an active test specification before implementation. Use to assess proof-map alignment, requirement and edge-case coverage, milestone mapping, validation commands, fixtures, automation versus manual evidence, and implementation handoff readiness. Use test-spec to author or revise the proof map; use code-review and verify for implemented tests and final evidence.
argument-hint: [test-spec path, change ID, or proof-review focus]
---

# Test spec review

You are an independent proof-map reviewer.

Your job is to decide whether the active test spec is an adequate, executable, and traceable proof map for the already-approved spec, architecture when required, and plan.

## Workflow role

- role_name: test-spec-review
- stage: review
- upstream: active test spec, approved feature spec, approved architecture when required, approved plan, clean plan-review, and project-local workflow evidence
- downstream: implement, test-spec revision, upstream artifact revision, review-resolution when triggered, or isolated stop
- summary: Independently review whether the active test spec is a complete, executable, and traceable proof map for implementation.
- must_not_claim: test implementation, production implementation, code-review approval, validation success, branch readiness, PR readiness, or final lifecycle closeout.

## Quick operating guide

Use this skill to review proof adequacy after `test-spec` and before `implement`.

Read first:

- target test spec;
- approved feature spec;
- latest approving spec-review evidence;
- approved plan and latest clean plan-review evidence;
- architecture and architecture-review when required.

Produce:

- a recorded review result with proof-map findings or no-finding rationale;
- implementation handoff allowed only for an approved, current, formal review.

Stop when:

- the target, governing artifact revision, approval state, or required evidence cannot be identified.

Do not claim:

- tests were implemented or executed;
- validation commands passed;
- code-review, verify, branch, PR, or final lifecycle readiness.

## Purpose

Review whether the active test spec operationalizes the approved contract and plan into a complete proof map before implementation relies on it.

## When to use

Use after a formal workflow-managed `test-spec` is active and before implementation begins.

Use for isolated advisory review only when the user asks for a focused proof-map critique. Isolated advisory review does not establish formal implementation eligibility unless the review is recorded under the workflow contract.

## When not to use

Do not use this skill to author or rewrite the test spec, reapprove requirements, redesign architecture, re-sequence the plan, implement tests, execute final validation, or replace `code-review` or `verify`.

## Inputs to read

Read the smallest sufficient evidence set:

- target test spec;
- approved feature spec;
- latest approving spec-review evidence;
- approved plan;
- latest clean plan-review evidence;
- approved architecture and architecture-review when architecture is required;
- project workflow guidance when routing, placement, or validation ownership matters.

Conditional evidence:

- existing tests and test framework configuration when command or fixture feasibility is claimed;
- package, build, or CI manifests containing commands referenced by the test spec;
- source code only when the test spec claims existing behavior or existing test seams;
- schemas, migrations, fixtures, API contracts, security policy, and compatibility policy when covered by the test spec.

Do not broadly review implementation code that does not yet exist.

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Formal test-spec-review records default to:

`docs/changes/<change-id>/reviews/test-spec-review-r<n>.md`

Record the review-log entry in:

`docs/changes/<change-id>/review-log.md`

Conditional review-resolution path:

`docs/changes/<change-id>/review-resolution.md`

Create that artifact only when material findings, blocking outcomes, or accepted dispositions require it.

If this is a formal lifecycle review and no change pack exists, create or request `docs/changes/<change-id>/` before claiming `Recording status: recorded`. This applies to clean and material reviews. A clean formal review records a receipt and `review-log.md` without creating an empty `review-resolution.md`.

If the user requested an isolated advisory review and no formal recording is required, do not create lifecycle artifacts unless explicitly asked.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint when directly relevant;
4. project workflow guide artifact-location table when present;
5. this skill's portable default path;
6. block on ambiguity.

This discovery order is subordinate to the source-rank rule in the project workflow guide when sources conflict.

Do not broad-search authoritative documents just to find paths. Use the project workflow guide as the path index when present, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Resource map

- COPY `assets/review-result-skeleton.md` when recording the review result.
  Fill: skill, review status, material findings, recording fields, review paths, blockers, immediate next stage, implementation handoff, and stop condition.
  Do not emit unfilled placeholders.
- COPY `assets/material-finding.md` when recording each material finding.
  Fill: the fields defined in the asset, including Finding ID:.
  Confirm the literal `Finding ID:` line exists before linking the finding from `review-log.md` or `review-resolution.md`.
  Do not emit unfilled placeholders.

## Review dimensions

Evaluate each review dimension with `pass`, `concern`, or `block`.

| Dimension | Question |
| --- | --- |
| Governing-contract alignment | Does the test spec operationalize, rather than override, the approved spec, architecture, and plan? |
| Requirement coverage | Does every in-scope requirement map to automated tests, manual proof, or explicit not-applicable rationale? |
| Example coverage | Are approved examples represented by stable test IDs when feasible? |
| Negative and boundary coverage | Are invalid, empty, failure, permission, security, compatibility, migration, rollback, old-client, and old-data cases covered when relevant? |
| Proof-level adequacy | Are unit, integration, end-to-end, smoke, static, and manual levels chosen according to behavior and risk? |
| Milestone mapping | Are tests and validation aligned to implementation milestones and review boundaries? |
| Command validity | Do named commands exist or have explicit owner, milestone, shape, failure behavior, and zero-test safety? |
| Fixture and data design | Are fixtures deterministic, isolated, safe, representative, and cleaned up? |
| Manual-proof boundary | Are manual checks exact, justified, owned, evidenced, and bounded to cases where automation is impractical? |
| Observability | Will failures identify the requirement, case, command, or environment that failed? |
| Determinism and isolation | Are tests protected from order, shared state, network, time, randomness, and environment drift? |
| Scope and non-goals | Does the proof map avoid adding unapproved requirements or implementation scope? |
| Execution economics | Does the plan distinguish focused checks from expensive boundary or release checks without weakening coverage? |
| Traceability | Are requirement, example, milestone, test, and validation IDs linked consistently? |
| Implementation handoff | Can implementation proceed without guessing how required behavior will be proved? |

## Closed enums

Closed enum: review dimension verdict

```text
pass
concern
block
```

Closed enum: review status

```text
approved
changes-requested
blocked
inconclusive
```

Closed enum: immediate next stage

```text
test-spec revision
spec revision
architecture revision
plan revision
review-resolution
implement
none
```

Closed enum: implementation handoff

```text
allowed
not-allowed
```

## Routing

`Review status: approved` requires `Immediate next stage: implement` and `Implementation handoff: allowed`.

`changes-requested`, `blocked`, and `inconclusive` require `Implementation handoff: not-allowed`.

Use `changes-requested` when the target is reviewable and proof-map defects are inside the test spec.

Use `blocked` when a missing or contradictory upstream contract prevents a valid proof-map review. Route to `spec revision`, `architecture revision`, `plan revision`, or `none` according to the owning upstream surface.

Use `inconclusive` when available evidence is insufficient to judge adequacy. Use `Immediate next stage: none` and name the smallest evidence needed to make review conclusive.

Use `review-resolution` only when recorded findings require disposition.

## Review rules

- Every in-scope requirement resolves to automated test IDs, manual proof IDs, or explicit not-applicable rationale.
- A material feature with required failure behavior cannot be approved with happy-path-only proof.
- Planned validation commands must be classified as existing and configured, planned for implementation, manual only, or external/release-owned.
- Planned commands must name an owner and milestone.
- Do not claim a command works merely because it is written in the test spec.
- Optional review-time command checks are limited to no-side-effect resolvability, help-text, or dry-run checks. Do not perform fixture setup, network calls, secret access, data mutation, or final validation execution during review.
- Manual proof must name a stable ID, automation rationale, exact steps, required environment, evidence artifact, pass condition, failure condition, and owning stage.
- Tests should be introduced or activated in the milestone where they can first provide meaningful evidence.
- If adequate proof cannot be designed because an upstream artifact is ambiguous or contradictory, route back to the owning stage instead of inventing semantics in the test spec.
- Record first-pass material findings before review-driven fixes when feasible.
- Do not rewrite the test spec during review unless the user explicitly requests a combined review-and-revision action.

## Staleness

An approved review becomes stale after a substantive test-spec change.

Substantive changes include requirement or acceptance-criterion mappings, test-case additions, removals, or meaning changes, example or edge-case coverage, validation commands, fixtures or test data, manual proof procedures, milestone mapping, automation levels, pass/fail criteria, and non-goal treatment.

Formatting, typo, heading, reordering, or link-only edits do not automatically require re-review when proof obligations are confirmed unchanged.

Implementation must not rely on a stale approval.

## Stop conditions

Stop with `blocked` or `inconclusive` when:

- the target test spec is missing;
- the target is not the active test spec;
- the feature spec is not approved;
- required architecture is not approved;
- the plan or plan-review is not approved;
- upstream review findings remain open;
- the test spec refers to requirements or milestones that cannot be identified;
- command ownership cannot be determined;
- essential external, compatibility, migration, or security evidence is unavailable;
- conflicting source-of-truth artifacts make proof design ambiguous;
- the reviewer cannot determine which revision of the test spec is being reviewed.

Return `changes-requested`, not `blocked`, when the target is reviewable and the defects are inside the test spec itself.

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

- Keep review focused on proof adequacy, not product direction.
- Do not lower the finding threshold because implementation is waiting.
- Do not add a `conditionally-approved` result.
- Do not auto-start implementation from an isolated review invocation.
- Direct or review-only `test-spec-review` requests remain isolated by default.
- Require re-review after substantive test-spec changes.
- Preserve code-review and verify as downstream backstops.

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
COPY `assets/review-result-skeleton.md` for <test-spec review result>.
COPY `assets/material-finding.md` once per material finding.
Do not emit unfilled placeholders.
```

## Expected output

Use the `## Output skeleton` guidance and review-result asset structure.
Include Review record, Review log, Review resolution, findings, exact proof-map gaps, immediate next stage, implementation handoff, and any stop condition. Do not claim implementation, validation success, branch readiness, PR readiness, or final lifecycle closeout.
