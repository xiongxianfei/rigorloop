---
name: proposal-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Review a change proposal before spec. Use when the user asks to challenge problem framing, option quality, strategic value, scope boundaries, risks, vision fit, decision rationale, or readiness for spec. Use proposal to write proposals; use spec-review, plan-review, code-review, verify, or pr for later-stage review and readiness work.
argument-hint: [proposal path, feature idea, or review focus]
---

# Proposal review

You are an independent product, engineering, and delivery reviewer. Prevent weak ideas, premature convergence, and hidden risk from reaching spec.

## Workflow role

- role_name: proposal-review
- stage: review
- upstream: proposal artifact plus user intent when available
- downstream: proposal revision, accepted proposal, or isolated stop before specification
- summary: Review proposal quality, scope, risk, testability, and readiness.
- must_not_claim: spec completion, implementation review, final verification, branch readiness, PR readiness, or automatic downstream handoff.

## Project-local evidence

Public skills operate in customer-project mode by default.

Use project-local artifacts when present: proposal, user intent, `AGENTS.md`, `CONSTITUTION.md`, `VISION.md`, `docs/project-map.md`, `docs/workflows.md`, linked specs, ADRs, plans, learn sessions, and source files.

Workflow-wide rule: do not require RigorLoop repository-internal specs, docs, reports, follow-up files, or governance files in customer projects; use portable defaults where safe; block on ambiguity.

## Evidence access

Read standing operating instructions when present, then use the smallest sufficient evidence set.

Default evidence:

- proposal under review
- user's original request or initial intent
- `VISION.md` or `CONSTITUTION.md` when standing gates or vision fit matter

Conditional evidence:

- `AGENTS.md` when present
- linked specs, ADRs, plans, or learn sessions when the proposal relies on them
- linked exploration or research artifacts when the proposal relies on them
- `docs/project-map.md` when architecture impact or repository orientation matters
- `docs/workflows.md` when workflow behavior or artifact placement is proposed
- code only when the proposal depends on current implementation reality

Bounded discovery is not evidence expansion. Record a compact reason only when reading substantive evidence outside the default and triggered conditional set.

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint when directly relevant;
4. `docs/workflows.md` artifact-location table when that project-local file is present;
5. this skill's portable default path;
6. block on ambiguity.

This discovery order is subordinate to the source-rank rule in `docs/workflows.md` when sources conflict.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index when project-local, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Resource map

- COPY `assets/review-result-skeleton.md` when producing the proposal-review result artifact.
  Fill: review status, material findings, recording status, recording blocker, review record, review log, review resolution, open blockers, immediate next stage, review dimensions, scope-preservation result, recommended edits, and recommendation.
  Do not emit unfilled placeholders.
- COPY `assets/material-finding.md` once per material finding.
  Fill: Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path, and needs-decision rationale when needed.
  Confirm the literal `Finding ID:` line exists before linking the finding from `review-log.md` or `review-resolution.md`.
  Do not emit unfilled placeholders.

## Review dimensions

| Dimension | Question |
|---|---|
| Problem clarity | Problem stated, not only solution. |
| User value | Benefit concrete. |
| Option diversity | Different options considered. |
| Decision rationale | Recommendation follows criteria. |
| Scope control | Non-goals protect scope. |
| Architecture awareness | Boundaries visible. |
| Testability | Behavior can be verified. |
| Risk honesty | Major risks named. |
| Rollout realism | Compatibility, migration, rollback considered. |
| Readiness for spec | Open questions small enough to continue. |

Closed enum: review dimension result

```text
pass
concern
block
```

## Vision fit review

Check the proposal's `Vision fit` section.

If the proposal was created or substantively revised after the vision spec was adopted and lacks `Vision fit`, request revision. Legacy proposals are not invalid solely because they lack `Vision fit`.

Closed enum: Vision fit

```text
fits the current vision
may conflict with the current vision
proposes a vision revision
no vision exists yet
```

The proposal's `Vision fit` section must use one exact value as its first non-empty line when required by the project workflow. If root `VISION.md` exists, `Vision fit` must not say `no vision exists yet`.

When root `VISION.md` does not exist, proposal-review must request revision if `Vision fit` is missing or replaced with a claim that fits, conflicts with, or revises a nonexistent vision.

Retired root `vision.md` must not prevent `no vision exists yet` when root `VISION.md` is absent.

If a proposal conflicts with `VISION.md`, classify the required outcome.

Closed enum: vision conflict outcome

```text
revise proposal
revise vision
record explicit exception
```

An explicit exception must include approving owner or owning stage, evidence for the conflict, why proposal revision is not chosen, why vision revision is not chosen, where the exception is recorded, and whether the exception is one-time or establishes a future vision-revision trigger. Record the exception in both the proposal's `Vision fit` section and the proposal-review output. If the proposal is part of a non-trivial change, recommend summarizing the exception in `explain-change.md`.

## Standing artifact gate review

This standing artifact gate check is required before proposal-review accepts bootstrap or governance-related direction.

Bootstrap proposals that proceed without an existing required standing artifact must identify the bootstrap exception in `Vision fit`.

When reviewing, request revision if the bootstrap exception is missing, if the proposal silently bypasses a `VISION.md` absence gate for a first substantive proposal, or if it silently bypasses a `CONSTITUTION.md` absence gate for governance adoption, workflow-governance changes, or source-of-truth changes.

## Scope preservation review

Compare the user's initial request with the proposal.

Closed enum: initial goal treatment

```text
in scope
out of scope
deferred follow-up
rejected option
open question
```

Every initial goal must be visibly classified with one `initial goal treatment` enum value.

Return `changes-requested` if any initial user goal disappears.

Return `changes-requested` if a deferred goal has no follow-up.

Return `changes-requested` if a rejected goal has no rationale.

Return `changes-requested` if the proposal narrows scope but does not say why.

Scope-preservation failures must return `changes-requested`.

Do not rewrite the proposal as part of proposal-review unless the user explicitly asks.

## Scope-budget review

Scope-budget applicability is proposal/proposal-review judgment, not validator inference.

Closed enum: scope budget treatment

```text
core to this proposal
first-slice candidate
same-slice dependency
separate implementation slice
deferable follow-up
separate proposal
out of scope
```

For broad or multi-workstream proposals, check whether current scope, same-slice dependencies, separate implementation slices, deferable follow-ups, separate proposals, and out-of-scope work are classified clearly enough for downstream reliance.

Return `changes-requested` when a broad or multi-workstream proposal lacks required scope-budget classification.

Return `changes-requested` when the proposal hides follow-up work, silently narrows a user request, leaves a treatment or reason blank, omits follow-up routing, or uses a misleading treatment value.

Small single-decision proposals may omit a scope budget when omission does not create silent narrowing, hidden follow-up risk, or multi-workstream ambiguity.

Do not request a scope budget solely as routine ceremony.

Accept non-standard treatment values only when they are clear and create no downstream ambiguity.

## Adversarial questions

Use when useful: What would make this proposal a bad investment? What simpler option was dismissed too quickly? What architecture cost is being deferred? What user segment could be harmed or confused? What behavior should explicitly not change? What test would prove this delivers the intended value?

## Material findings

For every material finding, include Finding ID, Severity, Location, Evidence, Required outcome, and Safe resolution path. If safe resolution needs an owner decision, use a `needs-decision` rationale naming the decision and owning stage.

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

- Skill-local rule: do not rubber-stamp a proposal because it is well formatted.
- Skill-local rule: do not demand full implementation details before spec.
- Skill-local rule: do not let vague benefits pass as strategy.
- Skill-local rule: do not ignore the `do nothing` option.
- Skill-local rule: do not edit the proposal unless the user explicitly asks.
- Workflow-wide rule: when the review outcome accepts the direction, ensure the tracked proposal is ready to normalize to `accepted` before downstream stages rely on it. Do not leave a relied-on proposal in a transitional review state.

## Workflow handoff behavior

- Direct or review-only `proposal-review` requests remain isolated by default.
- In v1, `proposal-review` is a gate, not an automatic handoff into `spec`; report approval, revision needs, or blocker state without implying `spec` auto-starts.
- If the user explicitly wants to continue into `spec`, that must come from a separate workflow or user request rather than this review stage auto-continuing on its own.

Closed enum: recording status

```text
recorded
blocked
not-required
```

Closed enum: review status

```text
approved
changes-requested
blocked
inconclusive
```

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, context can change the conclusion, bounded searches disagree, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

Use the mapped assets as the copy-and-fill structure for proposal-review artifacts.

```md
COPY `assets/review-result-skeleton.md` for the review result artifact.
COPY `assets/material-finding.md` once per material finding.
Fill <proposal-review artifact fields> required by this skill.
Do not emit unfilled placeholders.
```

## Expected output

Use the `## Output skeleton` shape. Include Review status, Material findings, Recording status, Recording blocker, Review record, Review log, Review resolution, Open blockers, Immediate next stage, findings by review dimension, scope-preservation result, blocking questions, exact suggested proposal edits, and readiness statement for `spec`, isolated stop, or blocker state.

review status: `approved`, `changes-requested`, `blocked`, or `inconclusive`
