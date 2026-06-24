---
name: implement
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Implement one approved milestone or isolated implementation request with tests or proof first, then hand it to code-review with validation evidence and plan state updated. Use when requirements, scope, and validation commands are clear enough to code. Use bugfix for defect reproduction/fix loops, code-review to review implementation, verify for final readiness, and pr for PR handoff.
argument-hint: [plan path, milestone ID, feature name, or implementation request]
---

# Test-driven implementation

You are implementing the smallest scope-complete change for the approved slice with tests first.

Do not expand scope. Do not silently alter the spec. Do not declare success without verification evidence.

For planned initiatives, `implement` owns keeping the active plan body current during execution. Update the plan body's progress, decisions, discoveries, and validation notes as work advances instead of leaving those details to later stages.

## Workflow role

- role_name: implement
- stage: execution
- upstream: approved spec, active plan, accepted review-resolution finding, bugfix request, or isolated implementation request with clear scope
- downstream: code-review
- summary: Implement the smallest scope-complete slice with tests or proof first, record validation, update plan state, and hand the milestone to code-review.
- must_not_claim: review passed, clean review, branch readiness, PR readiness, final verification, final closeout readiness, or derived artifact currency without owning proof.

## Quick operating guide

Use this skill to: implement one approved milestone with tests or proof first, then hand it to review.

Read first:

- the active plan `Current Handoff Summary`;
- the current milestone section and its validation notes;
- the governing spec, test spec, plan tasks, and relevant code/tests;
- the specific needed section first; use broader-section or full-file reading only when bounded evidence is insufficient.

Produce:

- test/proof updates, implementation changes, validation evidence, plan updates, and a review-requested milestone handoff.

Stop when:

- milestone state, requirements, scope, or validation evidence is missing, contradictory, or failing.

Do not claim:

- review passed, branch-ready, PR-ready, final-closeout readiness, or derived artifact currency without owning evidence.

Next stage:

- `code-review` for the implemented milestone, unless a stop condition applies.

## Purpose

Implement one approved milestone as the smallest scope-complete, test-driven slice and prepare it for `code-review` without claiming downstream review or verification outcomes.

## Project-local evidence

Public skills operate in customer-project mode by default.

Use project-local artifacts when present and relevant, including `AGENTS.md`, `CONSTITUTION.md`, the active plan, approved specs, test specs, architecture records, ADRs, review-resolution evidence, `docs/workflows.md`, source files, tests, neighboring files, and CI or validation commands.

Do not require RigorLoop repository-internal specs, docs, reports, follow-up files, or governance files in customer projects. Use portable defaults where safe, and block on ambiguity when no safe local guidance or default exists.

## When to use

Use this skill after the relevant spec, architecture, plan, plan-review, and test-spec are ready, or when the user explicitly requests isolated implementation output with clear scope and validation evidence.

This skill is for implementation, tests, proof, and handoff. Use `bugfix` for defect repair, `code-review` for review, `verify` for final readiness, and `pr` for pull request handoff.

## When not to use

Do not use this skill to invent requirements, bypass missing specs, resolve review findings without a recorded finding loop, claim review or branch readiness, or continue into the next milestone before the current milestone is handed to review.

## Inputs to read

Read before editing:

- `AGENTS.md`
- `CONSTITUTION.md` if present
- concrete execution plan
- feature spec
- test spec
- architecture doc and ADRs when relevant
- code and tests listed in the milestone
- existing patterns in neighboring files
- CI or validation commands relevant to the milestone

## Evidence access

Use the smallest sufficient evidence set for the milestone.

Default evidence:

- active plan `Current Handoff Summary`
- current milestone section
- approved spec
- test spec
- code and tests named by the milestone
- validation commands for the milestone

Conditional evidence:

- architecture or ADR when the milestone touches architecture boundaries
- review-resolution when implementing accepted review findings
- `docs/workflows.md` when stage routing or artifact placement is ambiguous
- `CONSTITUTION.md` when governance, source-of-truth, or safety constraints matter
- neighboring files when needed to follow existing patterns

Bounded discovery is not evidence expansion. Record a compact reason only when reading substantive evidence outside the default and triggered conditional set.

Use bounded evidence first, but do not under-read. Expand beyond the milestone when bounded evidence is missing, stale, contradictory, or insufficient to implement the approved slice. Full-file reads remain allowed when the whole file is the target, relevant sections cannot be isolated safely, bounded evidence is contradictory or incomplete, or whole-file context can change the implementation decision.

## Outputs

Produce tests or proof surfaces first where feasible, implementation changes, updated plan progress and validation notes, and a milestone handoff commit that sets the milestone to `review-requested`.

## Handoff

- Normal next stage: `code-review` for the implemented milestone.
- Conditional next stages: stop for a spec, architecture, owner-decision, or validation blocker; return to the same milestone when accepted review findings require fixes; continue to the next milestone only after clean review closes the current milestone.
- For full stage order and downstream-blocking semantics, route through the `workflow` skill.

## Claims this skill must not make

Do not claim:

- review passed, clean review, review-clean status, or no review fixes required;
- branch-ready, PR-ready, `pr-body-ready`, or `pr-open-ready`;
- ready-for-final-closeout or `Ready for final closeout` while any in-scope implementation milestone is open, unreviewed, unresolved, or not closed;
- derived artifacts are current unless validation evidence proves it.

## Progress, readiness, closeout, and Done

- Progress means work that has happened so far.
- Readiness means the next stage that can happen.
- Closeout means the current artifact or stage satisfied its checklist.
- Done means final lifecycle state after required gates are complete.
- Readiness is not Done. Implementation readiness for `code-review` is not review closeout, branch readiness, or PR readiness.

## Docs-changes baseline pack

For ordinary non-trivial work, implementation scope includes the baseline change-local pack:

- `docs/changes/<change-id>/change.yaml`
- durable Markdown reasoning, defaulting to `docs/changes/<change-id>/explain-change.md` for new work unless an approved equivalent reasoning surface already applies

Rules:

- Treat creating or updating that baseline pack as part of the milestone, not as optional follow-up.
- Do not treat PR text alone as the durable reasoning surface for ordinary non-trivial work.
- Do not broaden the docs-changes requirement into isolated manual skill invocations that are not claiming complete workflow delivery.
- Keep standalone `review-resolution.md` and `verify-report.md` conditional; add them only when their governing workflow triggers apply.

## Validation layering

Use selector-selected targeted proof before optional broad smoke when the changed paths are known.

- Inspect selected checks with the project's validation selector when one exists.
- Execute selected checks with the project's validation command.
- Record stable selected check IDs, such as `skills.validate`, `review_artifacts.validate`, or `selector.regression`, in the active plan or change metadata when they explain the proof scope.
- Run the project's broad validation command only when an authoritative trigger requires broad smoke, such as `broad_smoke_required: true`, main/release mode, review-resolution, test-spec, or release metadata.

## First-pass completeness

Before editing:

- identify the same-slice completeness set for the approved slice:
  - in-scope requirements
  - required authored surfaces
  - required aligned surfaces
  - required edge cases
  - the targeted validation set
- target a `first-pass acceptable result`, not merely a plausible first edit.
- treat the `smallest scope-complete change` as the target, not the smallest diff.
- a `first-pass acceptable result` means:
  - every in-scope requirement for the slice is addressed
  - every required authored surface in scope is updated, or explicitly marked `unaffected with rationale`
  - every required aligned surface in scope is updated, or explicitly marked `unaffected with rationale`
  - no known in-scope defect remains
  - the required targeted validation set passes
  - no required same-slice fix is deferred to later review or later cleanup
  - the change does not rely on later cleanup to become contract-complete
- if a required authored or aligned surface remains unchanged, record `unaffected with rationale` in a contributor-visible authoritative surface such as the active plan or required change-local artifacts.
- required edge cases come from approved spec and test-spec items, named regression cases from the motivating incident, changed branch conditions or touched failure paths, existing governing tests or fixtures, and required aligned workflow or skill wording distinctions for the slice.
- a later finding that should have been caught by the same-slice completeness set, required edge cases, or targeted validation is a `preventable first-pass miss`.
- if missing inputs, contradictory instructions, or unresolved scope ambiguity prevent a scope-complete first pass, stop and report the blocker instead of handing off to `code-review`.

## Implementation loop

For each milestone:

1. Confirm milestone scope, requirements covered, and the same-slice completeness set.
2. Identify the tests, proof surfaces, and required edge cases from the test spec and active plan.
3. Write or update the tests first.
4. Run the narrowest relevant test command.
5. Confirm new tests fail for the expected reason when feasible.
6. Implement the minimum production code needed to pass.
7. Run the narrow tests again.
8. Refactor only within milestone scope.
9. Run milestone targeted validation commands before any optional broad smoke.
10. Update the active plan body’s progress, decisions, surprises, aligned-surface audit, and validation notes.
11. When implementation work for the milestone is complete, create an implementation handoff commit using the subject format `M<n>: <implemented milestone outcome>` and include milestone validation in the commit body or referenced evidence.
12. Stop before the next milestone unless the user asked to continue.

Stopping before the next milestone does not cancel a required downstream workflow handoff. In a workflow-managed standard workflow, once the requested milestone is complete and no stop condition applies, hand off to `code-review` instead of waiting for redundant user confirmation.

## Handoff inspection budget

When checking milestone readiness or handoff state, start with the active plan's `Current Handoff Summary`.

Use this order:

1. active plan `Current Handoff Summary`
2. current milestone section
3. validation notes for that milestone
4. review-resolution evidence only when findings exist
5. compact change metadata only for status or artifact pointers

For milestone readiness, do not run broad repository searches to infer milestone state.

Avoid searching all documentation, specifications, skills, derived output, historical reviews, or broad `rg` output before checking active plan state.

If the active plan does not identify the current milestone or next stage, stop and report the missing state instead of searching broadly.

## Milestone-aware handoff

For milestone-based plans, `implement` works on one in-scope implementation milestone at a time.

- When implementation work begins, transition the current milestone from `planned` to `implementing`.
- After implementation and targeted validation complete, record targeted validation evidence, decisions, surprises, and follow-ups in the active plan.
- When no stop condition applies, set the current milestone to `review-requested` and hand off to `code-review` for that milestone.
- Perform a state-sync check before claiming readiness for `code-review`.
- Run the project artifact-lifecycle state-sync check before claiming readiness for `code-review`.
- Update the active plan `Current Handoff Summary` when the milestone moves to `review-requested`.
- Implementation completion is handoff evidence, not milestone closeout. `implementation-complete` may appear as an evidence description, but it is not a milestone state.
- The milestone becomes `closed` only after clean code-review and any required review-resolution are complete.
- If accepted review findings return to implementation, keep fixes attached to the same milestone. After fixes and targeted validation evidence are complete, return that same milestone to `review-requested` before rerun review.

`implement` must not set plan readiness to `Ready for final closeout` while any in-scope implementation milestone remains unreviewed, unresolved, or open. `Ready for final closeout` is valid only after all in-scope implementation milestones are closed or explicitly deferred by plan revision, final milestone code-review has completed, and required review-resolution is closed.

## TDD rules

- Tests first for new behavior.
- Regression test first for bugs.
- Minimal implementation to make tests pass.
- Refactor after green, not before.
- Delete or rewrite tests that pass for the wrong reason.
- Do not write broad mocks that bypass the behavior under test.

## Scope rules

- Implement only approved requirements and milestone tasks.
- Prefer the `smallest scope-complete change` over the smallest diff.
- Do not add unrelated refactors.
- Do not change public behavior not covered by the spec.
- Do not defer a required same-slice fix to later review, later milestone, or later cleanup.
- If code reveals a spec or architecture gap, stop and update the artifact or document the blocker.
- If validation fails, fix or report before moving on.
- Do not mark a milestone complete without the milestone commit.
- Do not assume every completed milestone needs its own PR; multiple completed milestones may continue in the same PR when that is the clearest review unit.

## Workflow handoff

- Do not hand off to `code-review` until the slice meets the `first-pass acceptable result` bar.
- In a workflow-managed standard workflow, successful `implement` completion hands off to `code-review` unless a stop condition applies.
- Implementation-stage closeout may report milestone completion, validation, blockers, readiness for `code-review`, or the next milestone.
- Do not use `implement` to claim review findings, review-clean status, or `branch-ready`. If review has not happened yet, say the change is ready for `code-review`, not that no required fixes were found.
- If milestone validation fails or the implementation reveals a blocker that needs a real user decision, stop before `code-review` and report the blocker explicitly.
- Ordinary later review comments may still happen. A `preventable first-pass miss` is only a finding that should have been caught by the same-slice completeness set, required edge cases, or targeted validation before handoff.
- This v1 autoprogression rule does not expand manual skill invocation or bugfix execution behavior through the `implement` skill.

## Plan update requirements

Update the concrete plan with:

- milestone progress;
- decisions made during implementation;
- surprises and discoveries;
- validation commands run;
- validation results;
- known follow-ups or deferred work.
- for planned initiatives, keep `docs/plan.md` as lifecycle bookkeeping rather than a milestone journal;
- if lifecycle state changes during implementation, update both `docs/plan.md` and the plan body before the PR opens for review;
- if completion depends on a true downstream completion event, keep the plan `Active`, name that event, and do not treat merge itself as the event.

## Stop conditions

Stop before handoff when:

- required source artifacts are missing, contradictory, or not approved enough for the workflow state;
- tests or targeted validation fail and the failure is not fixed;
- a spec, architecture, owner-decision, security, permission, or scope blocker appears;
- the slice cannot meet the first-pass acceptable result;
- the current milestone cannot be updated to `review-requested` with validation evidence and a milestone commit.

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

Fill placeholders such as `<paths or none>` with concrete milestone evidence.

```md
## Result

- Skill: implement
- Status: implemented | blocked
- Artifacts changed: <paths or none>
- Open blockers: <blockers or none>
- Next stage: code-review | blocked
- Milestone: <milestone ID or isolated request>
- Milestone state: review-requested | blocked
- Tests or proof updated first:
- Validation:
- Plan updates:

## Implementation summary
<scope-complete change, same-slice coverage, and important decisions>

## Validation evidence
<commands and pass/fail results>

## Handoff
<review-requested milestone state, commit, or blocker>
```

## Expected output

Use the `## Output skeleton` shape.

Start with:

```md
## Result

- Skill: implement
- Status: <implemented | blocked>
- Artifacts changed: <paths or none>
- Open blockers: <blockers or none>
- Next stage: <code-review | blocked>
- Validation: <commands and results>
- Milestone state: <review-requested | blocked>
```

Then include the milestone implemented, tests or proof added first, validation results, plan updates, blockers or spec gaps, and readiness for `code-review` or a clear blocked state. Do not imply review findings, final verification, final closeout readiness, or `branch-ready`.
