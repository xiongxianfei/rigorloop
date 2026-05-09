---
name: verify
description: >
  Run final verification after durable change rationale exists and before PR handoff. Use to verify artifact-code-test coherence,
  requirement coverage, validation commands, CI readiness, drift, release safety, and scoped direct validation checks.
---

# Verification gate

You are proving that the implementation, tests, and durable artifacts agree.

Verification is broader than running CI. It checks completeness, correctness, coherence, and evidence.

`verify` owns `branch-ready`. The `pr` stage owns `pr-body-ready` and `pr-open-ready`.

## Purpose

Run final verification after durable change rationale exists and before PR handoff.

`verify` validates the final change pack: implementation, tests, derived artifacts, lifecycle artifacts, validation evidence, risk closeout, and any required `explain-change` artifact all agree and are current.

`verify` owns validation evidence and branch-ready proof. It does not create the durable explanation and does not prepare the PR body.

Final verification is scoped evidence and must not own the active plan's current next stage. Use the active plan `Current Handoff Summary` to assess current planned-initiative state.

## When to use

Use this skill after all in-scope implementation milestones are closed, code-review/review-resolution obligations are complete, `ci-maintenance` is complete when triggered, and `explain-change` exists and is current. Use it directly only when a user explicitly asks for an isolated verification gate.

## When not to use

Do not use this skill to replace code-review, prepare PR body readiness, open a PR, close unresolved review findings, or claim hosted CI status that was not observed.

## Inputs to read

Read:

- feature spec;
- test spec;
- architecture doc and ADRs;
- touched or authoritative lifecycle-managed artifacts relevant to the change;
- concrete plan and validation notes;
- actual diff;
- test output and CI status when available;
- code-review findings;
- review-resolution.md when material review findings exist;
- selector output or wrapper output for targeted proof when changed paths were validated through selected checks;
- verify-report.md when required manual proof exists for a normal change;
- release metadata when release smoke or release manual proof is in scope;
- `AGENTS.md` and `CONSTITUTION.md`;
- CI workflow definitions relevant to the change.

## Outputs

Produce a verification verdict, traceability and drift assessment, validation evidence summary, blocker list if any, and the next valid handoff toward `pr` or stop.

## Handoff

- Normal next stage: `pr` when branch readiness passes.
- Conditional next stages: route back to `ci-maintenance` or `explain-change` when a required pre-verify automation or rationale artifact is missing or stale; stop when blockers remain.
- For full stage order and downstream-blocking semantics, route through the `workflow` skill.

## Direct verify

A user may invoke `verify` directly for an isolated validation check.

A direct `verify` result is isolated by default. It may report validation evidence for the requested scope, but it does not imply that the full workflow has completed, that `explain-change` exists, or that PR handoff is ready unless those artifacts are present and explicitly verified.

## Workflow-managed final verify

In workflow-managed final closeout, `verify` runs after:

- implementation milestones are closed;
- required review-resolution is closed;
- `ci-maintenance` is complete when triggered;
- durable rationale exists after `explain-change` and is current.

Then `verify` hands off to `pr` when branch-ready evidence is complete.

## Claims this skill must not make

Do not claim:

- PR-ready, PR body ready, `pr-body-ready`, or `pr-open-ready`;
- review passed unless code-review evidence is cited;
- CI passed unless hosted CI was actually observed or the statement is explicitly local validation only;
- derived artifacts are current unless validation evidence proves it.

## Progress, readiness, closeout, and Done

- Progress means work that has happened so far.
- Readiness means the next stage that can happen.
- Closeout means the current artifact or stage satisfied its checklist.
- Done means final lifecycle state after required gates are complete.
- Readiness is not Done. `branch-ready` is not PR body readiness or final lifecycle Done.

## Verification dimensions

Evaluate each with `pass`, `concern`, or `block`:

1. **Spec coverage**: every implemented behavior maps to a requirement or approved non-contract change.
2. **Requirement satisfaction**: every `MUST` has evidence.
3. **Test coverage**: every required test exists or has a documented manual verification.
4. **Test validity**: tests can fail for the right reason and assert meaningful behavior.
5. **Architecture coherence**: implementation matches design and ADRs.
6. **Artifact lifecycle state**: touched, referenced, generated, and authoritative lifecycle-managed artifacts do not advertise stale or contradictory status, readiness, closeout, or replacement state.
7. **Plan completion**: milestones are complete or intentionally deferred, and planned initiatives do not have stale lifecycle state between `docs/plan.md` and the plan body.
8. **Validation evidence**: commands, outputs, and CI results are recorded.
9. **Drift detection**: specs/plans/architecture reflect what was actually built.
10. **Risk closure**: rollout, rollback, migration, observability, and security risks are addressed.
11. **Release readiness**: branch state, generated files, migrations, docs, and CI are ready for PR.

## Verification process

1. Build a traceability table:

```text
Requirement → Test IDs → Files changed → Evidence → Status
```

2. Check the actual diff for unplanned behavior.
3. Compare tests against the test spec.
4. Build the related artifact set from changed files, `docs/changes/<change-id>/change.yaml`, explain-change artifacts, the active plan, derived artifacts, governing specs, governing architecture docs or ADRs, governing test specs, and draft PR text only when that draft PR body already exists.
4a. When `branch-ready` depends on cited governing artifacts, confirm those authoritative artifacts are present in tracked governing branch state rather than only in the local worktree.
5. For ordinary non-trivial work, confirm the required baseline change-local pack exists: `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning, defaulting to `docs/changes/<change-id>/explain-change.md` unless an approved equivalent surface applies.
6. Treat a missing required baseline change-local pack as a blocker, not acceptable silence.
7. When material review findings exist, run the project's review-artifact closeout validation when one exists and inspect `review-resolution.md`.
7a. New or revised `review-resolution.md` files should use the scan-first shape: summary, resolution overview table, compact finding details, shared validation evidence when applicable, and closeout checklist while preserving parseable per-finding labels.
8. Block on `Closeout status: open`, any `needs-decision` disposition, stale `review-log.md` open findings, missing final action, missing rationale, missing follow-up record, or missing `Validation evidence` required for an accepted fix.
8a. `Closeout status: closed` requires final dispositions for all material findings and no stale `review-log.md` open findings.
8b. A stage-owned non-approval outcome that blocks downstream progress or requires revision needs a same-stage later review round or explicit reviewer or owner closeout naming the original Review ID; `review-resolution.md` alone is not a silent substitute.
8c. For no-material review events, no-material detailed records need `review-log.md` but not an empty `review-resolution.md`.
9. For lifecycle-managed artifacts, treat stale or inconsistent touched, referenced, generated, or authoritative artifacts as blockers. Report unrelated stale baseline artifacts as warnings instead of blocking the change.
10. For planned initiatives, compare `docs/plan.md` against the plan body and treat stale lifecycle state as a blocker. At minimum, block on completed, blocked, or superseded work still listed under `## Active`; conflicting index-versus-body state; or a plan body marked done, blocked, or superseded while still presenting itself as active or in progress.
10a. Confirm lifecycle transitions performed by this PR are recorded in both surfaces before the PR opens for review. If the plan remains `Active`, it must name a true downstream completion event; merge itself is not that event.
11. Confirm targeted proof ran for the changed surfaces, preferably through the project's validation selector or project validation command, and record stable selected check IDs where useful.
12. For planned initiatives or other authoritative triggers, confirm broad smoke evidence exists through the project's broad validation command or selected broad-smoke check.
13. If the active plan, test spec, review-resolution, or release metadata records `broad_smoke_required: true`, do not mark `branch-ready` without broad smoke evidence or an explicit blocker.
14. Inspect CI workflow scope if CI is expected.
15. Identify artifact drift and propose fixes.
16. Produce a final readiness verdict.

## Commands and evidence

When commands are run, record:

- command;
- working directory;
- pass/fail;
- important output;
- timestamp when relevant.

If commands cannot be run, state why and what evidence is missing.

When planned-initiative lifecycle state matters, record which `docs/plan.md` section and which plan-body lifecycle surfaces were reviewed.

When PR-body references are not yet available, record which pre-PR handoff surfaces supplied authoritative references instead. Final PR text must not add new authoritative artifact references without rerunning `verify`.

For required manual proof on normal changes, inspect `docs/changes/<change-id>/verify-report.md`. Required manual proof records must name the check ID, result, why it is manual, performer, date, evidence, and when applicable reason, owner, and follow-up. A check that is intentionally not automated must say `manual by design`.

For release smoke, inspect release metadata under `docs/releases/<version>/` rather than inventing a normal-change `verify-report.md`. Manual proof result `fail` blocks `verify`; `blocked` or `not-run` also blocks unless the governing stage or release contract explicitly allows that temporary state with rationale, owner, and follow-up.

## Rules

- Do not claim CI passed unless CI actually passed.
- Do not claim tests were run unless they were run.
- Do not treat unrun tests as evidence.
- Do not ignore implementation that exceeds the spec.
- Do not treat `reviewed` as a durable passing state for relied-on proposals, specs, test specs, or architecture docs.
- Do not let touched or authoritative stale artifacts pass as baseline debt.
- Do not treat local-only authoritative artifacts as sufficient support for `branch-ready`.
- Do not treat unresolved named edge-case proof gaps as compatible with `branch-ready`.
- Do not treat a planned initiative as `branch-ready` when lifecycle state is stale.
- Do not treat material review findings as closed unless `review-resolution.md` is at `Closeout status: closed`, `review-log.md` lists no open findings, and closeout validation passes.
- Do not continue past `needs-decision`; it is not a final disposition.
- Do not accept deferring a known `Done` transition to a later merge boundary. A plan may remain `Active` only for a named true downstream completion event, and merge itself is not that event.
- Do not move to PR if blockers remain.
- Do not update artifacts silently; call out drift.

## Workflow handoff behavior

- In a workflow-managed standard workflow, successful `verify` hands off to `pr` unless a stop condition applies.
- Before final `verify`, `ci-maintenance` runs when hosted workflow automation, validation automation, or related platform configuration must be created or changed, then `explain-change` creates the durable rationale.
- Direct `verify` requests remain isolated by default unless the user explicitly asks to continue through completion.
- When `verify` stops because of blockers or pause conditions, name the blocked next stage and the reason continuation stopped.

## Stop conditions

Stop before downstream handoff when:

- implementation milestones, code-review, or review-resolution remain open;
- required validation, derived-artifact currency checks, or selector-selected proof are missing or failing;
- lifecycle state is stale between the plan index and plan body;
- touched or authoritative artifacts advertise stale status or readiness;
- branch-ready cannot be supported by tracked governing branch state.

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

- Skill: verify
- Status:
- Artifacts changed:
- Open blockers:
- Next stage:
- Validation:
- Readiness:
```

Then include:

- verification verdict: ready, concerns, or blocked;
- traceability table;
- validation commands and results;
- CI status or CI gap;
- artifact drift findings;
- remaining risks;
- readiness statement for `branch-ready`, `pr`, isolated stop, or blocker state.
