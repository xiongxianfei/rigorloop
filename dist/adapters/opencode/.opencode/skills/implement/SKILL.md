---
name: implement
description: >
  Implement a reviewed milestone using strict test-driven development. Use after spec, architecture, plan, and test-spec are ready, or in the fast lane after an explicit spec and test checklist exist.
---

# Test-driven implementation

You are implementing the smallest scope-complete change for the approved slice with tests first.

Do not expand scope. Do not silently alter the spec. Do not declare success without verification evidence.

For planned initiatives, `implement` owns keeping the active plan body current during execution. Update the plan body's progress, decisions, discoveries, and validation notes as work advances instead of leaving those details to later stages.

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

## Docs-changes baseline pack

For ordinary non-trivial work, implementation scope includes the baseline change-local pack:

- `docs/changes/<change-id>/change.yaml`
- durable Markdown reasoning, defaulting to `docs/changes/<change-id>/explain-change.md` for new work unless an approved equivalent reasoning surface already applies

Rules:

- Treat creating or updating that baseline pack as part of the milestone, not as optional follow-up.
- Do not treat PR text alone as the durable reasoning surface for ordinary non-trivial work.
- Do not broaden the docs-changes requirement into approved fast-lane work.
- Keep standalone `review-resolution.md` and `verify-report.md` conditional; add them only when their governing workflow triggers apply.

## Validation layering

Use selector-selected targeted proof before optional broad smoke when the changed paths are known.

- Inspect selected checks with `python scripts/select-validation.py --mode explicit --path <path>...`.
- Execute selected checks with `bash scripts/ci.sh --mode explicit --path <path>...`.
- Record stable selected check IDs, such as `skills.validate`, `review_artifacts.validate`, or `selector.regression`, in the active plan or change metadata when they explain the proof scope.
- Run `bash scripts/ci.sh --mode broad-smoke` only when an authoritative trigger requires broad smoke, such as `broad_smoke_required: true`, main/release mode, review-resolution, test-spec, or release metadata.

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
11. When the milestone is complete, create a milestone closeout commit using the subject format `M<n>: <completed milestone outcome>` and include milestone validation in the commit body or referenced evidence.
12. Stop before the next milestone unless the user asked to continue.

Stopping before the next milestone does not cancel a required downstream workflow handoff. In a workflow-managed full-feature flow, once the requested milestone is complete and no stop condition applies, hand off to `code-review` instead of waiting for redundant user confirmation.

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
- In the full-feature lane, successful `implement` completion hands off to `code-review` unless a stop condition applies.
- Implementation-stage closeout may report milestone completion, validation, blockers, readiness for `code-review`, or the next milestone.
- Do not use `implement` to claim review findings, review-clean status, or `branch-ready`. If review has not happened yet, say the change is ready for `code-review`, not that no required fixes were found.
- If milestone validation fails or the implementation reveals a blocker that needs a real user decision, stop before `code-review` and report the blocker explicitly.
- Ordinary later review comments may still happen. A `preventable first-pass miss` is only a finding that should have been caught by the same-slice completeness set, required edge cases, or targeted validation before handoff.
- This v1 autoprogression rule does not expand fast-lane or bugfix execution behavior through the `implement` skill.

## Plan update requirements

Update the concrete plan with:

- milestone progress;
- decisions made during implementation;
- surprises and discoveries;
- validation commands run;
- validation results;
- known follow-ups or deferred work.
- for planned initiatives, keep `docs/plan.md` as lifecycle bookkeeping rather than a milestone journal;
- if lifecycle state changes during implementation, update both `docs/plan.md` and the plan body, or record why only a merge-dependent `Done` transition remains pending.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- milestone implemented;
- tests added or updated first;
- validation commands and results;
- files changed;
- plan updates made;
- blockers or spec gaps;
- readiness statement for `code-review`, blocker/pause state, or next milestone, without implying review findings or `branch-ready`.
