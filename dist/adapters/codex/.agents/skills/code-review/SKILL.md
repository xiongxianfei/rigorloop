---
name: code-review
description: >
  Perform an independent implementation review against the spec, architecture, plan, test spec, actual diff, and validation evidence. Use after implementation or before PR readiness decisions.
argument-hint: [branch, diff, plan path, spec path, or feature name]
---

# Independent implementation review

You are reviewing in independent-review mode with fresh eyes.

Your job is to determine whether the implementation satisfies the approved contract safely, not whether it merely looks plausible.

## Quick operating guide

Use this skill to: independently review an implementation slice against governing artifacts, actual diff, tests, and validation evidence.

Read first:

- the actual diff or changed files;
- the active plan `Current Handoff Summary` when a plan exists;
- the governing spec, test spec, plan milestone, and validation notes;
- the specific needed section first; use broader-section or full-file reading only when bounded evidence is insufficient.

Produce:

- a first-pass review status, material findings or no-finding rationale, checklist coverage, and milestone-aware handoff.

Stop when:

- the diff, governing artifacts, milestone state, or validation evidence cannot support a credible review.

Do not claim:

- branch-ready, PR-ready, verification passed, CI passed, or implementation fixes unless separately owned.

Next stage:

- review-resolution for findings, next implementation milestone after a clean non-final review, or final closeout after a clean final review.

## Purpose

Review the actual implementation slice against approved artifacts, tests, diff, and validation evidence, then produce a first-pass review status and milestone-aware handoff.

## When to use

Use this skill after `implement` hands off a milestone, before PR readiness decisions, or when a user explicitly asks for an implementation review against the governing artifacts.

## When not to use

Do not use this skill to fix findings before recording them, claim branch or PR readiness, substitute passing tests for review, or review from memory without inspecting the actual review surface.

## Inputs to read

Read:

- actual diff or changed files;
- governing spec, test spec, plan milestone, architecture, and ADRs when relevant;
- plan validation notes, tests, CI results, and selector-selected targeted proof with stable check IDs when in scope;
- invocation context, explicit stop instructions, repository governance, and related code/tests when needed.

Prefer a fresh session, separate reviewer, or separate agent when available. If not, intentionally reset assumptions before reading the diff.

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

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Outputs

Produce a first-pass review record with status, inputs, diff summary, findings or no-finding rationale, checklist coverage, and a milestone-aware next-stage decision.

## Handoff

- Normal next stage: follow the active plan and milestone state after the first-pass review.
- Conditional next stages: `review-resolution` for material or required-change findings; `implement <next milestone>` after a clean non-final milestone; final closeout after a clean final milestone; stop on `blocked` or `inconclusive`.
- A clean non-final milestone closes only that milestone and hands off to `implement <next milestone>`.
- A clean final milestone reaches final closeout, not direct `verify`; final closeout runs `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`.
- Do not hand off to final closeout while implementation milestones remain open or required review-resolution remains unresolved.
- For full stage order and downstream-blocking semantics, route through the `workflow` skill.

## Claims this skill must not make

Do not claim:

- branch-ready, PR-ready, `pr-body-ready`, or `pr-open-ready`;
- CI passed, verification passed, or tests passed unless cited as evidence from the owning validation surface;
- implementation fixes were made unless this review also owns a recorded resolution flow;
- derived artifacts are current unless validation evidence proves it.

## Progress, readiness, closeout, and Done

- Progress means work that has happened so far.
- Readiness means the next stage that can happen.
- Closeout means the current artifact or stage satisfied its checklist.
- Done means final lifecycle state after required gates are complete.
- Readiness is not Done. A clean non-final milestone review closes that milestone, not the whole plan.

## Independent-review mode

- Ground the review in the actual diff or changed files, approved upstream artifacts, checklist coverage, and available validation evidence.
- Do not treat remembered implementation intent, chat memory, or passing tests alone as sufficient review grounding.
- If you cannot inspect the actual diff, relevant tests, or authoritative upstream artifacts, do not return `clean-with-notes`. Use `changes-requested` or `blocked` when the review surface independently supports a finding; otherwise use `inconclusive`.

## Review surface and tracked governing branch state

- The review surface may be changed files, a staged diff, an unstaged diff, a PR diff, a commit range, an explicit patch, or another local review target.
- Tracked governing branch state supports branch-scoped conclusions about cleanliness, authority, or readiness.
- Reviewed implementation changes need not all be committed, but governing artifacts cited for a clean branch-scoped conclusion must be present in tracked governing branch state.
- Local-only governing artifacts may inform background understanding, but not a clean branch-scoped conclusion.

## Mixed-evidence handling

- Missing tracked governing authority blocks `clean-with-notes`.
- Missing tracked governing authority does not suppress independently supported `changes-requested` or `blocked` findings.
- Use `inconclusive` only when missing evidence prevents both a supported finding and a clean conclusion.

## Direct proof for named edge cases

- Clean review conclusions for named edge cases must cite direct proof from a targeted test, targeted validation output, or an explicit manual verification note when manual verification is allowed.
- Code-shape inference alone is insufficient direct proof for a named edge case.
- If a named edge-case proof gap is actionable within approved scope, report it as a finding; if evidence is too limited to assess, use `inconclusive`.
- For validation-routing changes, targeted proof names selected checks or executed checks; broad smoke is separate and required only when an authoritative trigger applies.

## First-pass checklist coverage

Evaluate each check with `pass`, `concern`, or `block`, and cite concrete evidence from the diff, tests, or governing artifacts:

1. **Spec alignment**: behavior matches approved scope and non-goals.
2. **Test coverage**: tests prove changed behavior and regressions.
3. **Edge cases**: named edge cases and failure paths are covered.
4. **Error handling**: invalid states, partial failures, permissions, and fallbacks are safe.
5. **Architecture boundaries**: design and ADR boundaries are respected.
6. **Compatibility**: workflow expectations, contributor contracts, and migrations remain valid.
7. **Security/privacy**: no secret leakage, unsafe logging, auth bypass, or policy regression.
8. **Derived artifact currency**: canonical and derived artifacts stay synchronized when generation is involved.
9. **Unrelated changes**: the reviewed diff does not quietly include unrelated edits.
10. **Validation evidence**: named commands and results are relevant and credible.

For sensitive change classes, explicitly cite the relevant governing requirements, risks, or checklist items instead of relying on a generic clean summary.

## First-pass statuses

Use exactly one first-pass review status:

- `clean-with-notes`: the review passes and no unresolved accepted fix is required before the next stage.
- `changes-requested`: one or more fixable findings exist within current approved scope and with sufficient evidence to act.
- `blocked`: the review cannot safely auto-enter `review-resolution` under current approved scope without a new decision.
- `inconclusive`: the reviewer cannot inspect enough evidence to produce a credible clean or actionable result.

Issues that are clearly fixable within current approved scope and with sufficient evidence to act use `changes-requested`, not `blocked`.

## Severity

Use:

- `blocker`: unsafe to merge or violates a `MUST`.
- `major`: should be fixed before PR approval.
- `minor`: improvement that does not block.
- `nit`: optional style/readability suggestion.
- `positive`: good pattern worth keeping.

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

- Produce a first-pass review record before any review-driven fix is applied or any `review-resolution` work begins.
- The first-pass review record must include: review status, review inputs, diff summary, findings, checklist coverage, no-finding rationale when no findings exist, and recommended next stage.
- Surfacing findings first means the findings are visible before fixes begin. It does not create a new user decision gate unless a stop condition applies.
- A clean first-pass review with no material findings does not create a standalone `review-resolution.md` requirement by itself.
- Do not confuse passing tests with compliance.
- Do not review from memory; use the actual diff.
- Do not request broad rewrites when a targeted fix is enough.
- Do not claim a credible clean result when required evidence or tracked governing authority is missing; use `inconclusive` instead unless the review surface independently supports a finding.
- Do not require positive notes in a clean review. Include them only when they provide specific, evidence-backed information useful to future maintainers.
- Do not emit generic praise such as `looks good` without checklist coverage and no-finding rationale. That is an invalid clean review.
- Do not expose secrets, credentials, or sensitive runtime values from the diff or validation outputs.

## Workflow handoff behavior

- In a workflow-managed standard workflow, emit the first-pass review record before any review-driven fix begins.
- In a workflow-managed standard workflow, `clean-with-notes` hands off according to the active plan and milestone state when no stop condition applies.
- In a workflow-managed standard workflow, `changes-requested` enters the `review-resolution` loop, addresses the findings, and reruns `code-review` when no stop condition applies.
- In a workflow-managed standard workflow, `blocked` stops and reports the blocker.
- In a workflow-managed standard workflow, `inconclusive` stops and reports the missing evidence. It does not enter `review-resolution`.
- Stop instead of auto-entering `review-resolution` when the request is review-only, the request is isolated `code-review`, a finding requires a product/spec/architecture/ADR/scope decision, a higher-priority repository policy requires human review, the actual diff/tests/upstream artifacts are unavailable, or the user explicitly asked to stop after review.
- Direct `code-review` requests remain isolated by default unless the user explicitly asks to continue beyond the review result.

## Stop conditions

Stop instead of clean handoff when:

- the actual diff, relevant tests, or authoritative upstream artifacts cannot be inspected;
- required tracked governing authority is missing for a clean branch-scoped conclusion;
- findings require a product, spec, architecture, ADR, ownership, or scope decision;
- review-only or isolated invocation forbids downstream continuation;
- the reviewed milestone or remaining in-scope implementation milestones cannot be determined.

## Milestone-aware review handoff

For a milestone-based plan, identify the reviewed milestone and inspect the active plan before choosing the next stage.

- A clean non-final milestone closes the reviewed milestone and hands off to the next in-scope implementation milestone.
- A clean final milestone closes the reviewed milestone and hands off to `ci-maintenance` when triggered; otherwise it hands off to `explain-change`, only when no in-scope implementation milestone remains open or unresolved and no required review-resolution remains open.
- Findings that require review-resolution, fixes, owner decision, or re-review move the reviewed milestone to `resolution-needed` and keep the workflow on that same milestone.
- Accepted fixes remain attached to the same milestone. When re-review is required, the milestone returns to `review-requested` before rerun `code-review`.
- If the reviewed milestone or remaining in-scope implementation milestones cannot be determined from the active plan and review output, return `inconclusive` or require a plan update instead of handing off to final closeout.

A clean review of one non-final implementation milestone is not proof that the whole plan is ready for final closeout.

## Plan closeout check

For milestone-based plans, the review output must include or require a current handoff summary with:

- reviewed milestone;
- review status;
- milestone state after review;
- required review-resolution, if any;
- remaining in-scope implementation milestones;
- next stage;
- final closeout readiness and the reason.

Update or require update of the active plan `Current Handoff Summary` before downstream handoff.

When review is `clean-with-notes` and no review-resolution is required, update or require update of the reviewed milestone from `review-requested` to `closed`. When findings require review-resolution, update or require update of the reviewed milestone to `resolution-needed`.

## Recommended clean review template

```md
## Review status
clean-with-notes

## Review inputs
- Diff/review surface:
- Tracked governing branch state:
- Governing artifacts:
- Validation evidence:

## Diff summary
<Actual-diff summary.>

## Findings
No blocking or required-change findings.

## Checklist coverage
<Each required checklist item marked pass, concern, or block with evidence.>

## No-finding rationale
<Why the diff, tests, and validation support clean-with-notes.>

## Residual risks
<Remaining limits or None identified.>
```

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

Use this result format.

Start with:

```md
## Result

- Skill: code-review
- Status:
- Review status:
- Material findings:
- Recording status:
- Recording blocker:
- Review record:
- Review log:
- Review resolution: <path | not-required | blocked>
- Artifacts changed:
- Open blockers:
- Next stage:
- Reviewed milestone:
- Review status:
- Milestone closeout:
- Remaining implementation milestones:
- Required review-resolution:
- Finding IDs:
- Verify readiness:
```

Then include:

- first-pass review record with:
  - review status using `clean-with-notes`, `changes-requested`, `blocked`, or `inconclusive`;
  - review inputs;
  - diff summary;
- findings with exact file/path references;
- checklist coverage;
- no-finding rationale when applicable;
- any missing tracked governing artifacts or direct-proof gaps that affected the result;
- optional positive notes only when they add specific evidence-backed value; and
- recommended next stage or stop reason.
