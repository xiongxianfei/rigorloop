---
name: verify
description: >
  Run or reason through the final quality gate after implementation. Use to verify artifact-code-test coherence, requirement coverage, validation commands, CI readiness, drift, and release safety before explanation or PR.
argument-hint: [feature name, branch, plan path, spec path, or verification scope]
---

# Verification gate

You are proving that the implementation, tests, and durable artifacts agree.

Verification is broader than running CI. It checks completeness, correctness, coherence, and evidence.

`verify` owns `branch-ready`. The `pr` stage owns `pr-body-ready` and `pr-open-ready`.

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
- `AGENTS.md` and `CONSTITUTION.md`;
- CI workflow definitions relevant to the change.

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
4. Build the related artifact set from changed files, `docs/changes/<change-id>/change.yaml`, explain-change artifacts, the active plan, generated outputs, governing specs, governing architecture docs or ADRs, governing test specs, and draft PR text only when that draft PR body already exists.
4a. When `branch-ready` depends on cited governing artifacts, confirm those authoritative artifacts are present in tracked governing branch state rather than only in the local worktree.
5. For ordinary non-trivial work, confirm the required baseline change-local pack exists: `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning, defaulting to `docs/changes/<change-id>/explain-change.md` unless an approved equivalent surface applies.
6. Treat a missing required baseline change-local pack as a blocker, not acceptable silence.
7. When material review findings exist, run `python scripts/validate-review-artifacts.py --mode closeout docs/changes/<change-id>` and inspect `review-resolution.md`.
8. Block on `Closeout status: open`, any `needs-decision` disposition, missing final action, missing rationale, missing follow-up record, or missing `Validation evidence` required for an accepted fix.
9. For lifecycle-managed artifacts, treat stale or inconsistent touched, referenced, generated, or authoritative artifacts as blockers. Report unrelated stale baseline artifacts as warnings instead of blocking the change.
10. For planned initiatives, compare `docs/plan.md` against the plan body and treat stale lifecycle state as a blocker. At minimum, block on completed, blocked, or superseded work still listed under `## Active`; conflicting index-versus-body state; or a plan body marked done, blocked, or superseded while still presenting itself as active or in progress.
11. Run or list required validation commands.
12. Inspect CI workflow scope if CI is expected.
13. Identify artifact drift and propose fixes.
14. Produce a final readiness verdict.

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
- Do not treat material review findings as closed unless `review-resolution.md` is at `Closeout status: closed` and closeout validation passes.
- Do not continue past `needs-decision`; it is not a final disposition.
- Do not accept deferring a known `Done` transition until after merge unless merged state is the deciding event for completion.
- Do not move to PR if blockers remain.
- Do not update artifacts silently; call out drift.

## Workflow handoff behavior

- In a workflow-managed full-feature flow, successful `verify` hands off to the next required or default downstream stage for the lane.
- In that full-feature lane, the downstream stage is `ci` when the governing workflow contract elevates it; otherwise it is `explain-change`.
- Direct `verify` requests remain isolated by default unless the user explicitly asks to continue through completion.
- When `verify` stops because of blockers or pause conditions, name the blocked next stage and the reason continuation stopped.

## Expected output

- verification verdict: ready, concerns, or blocked;
- traceability table;
- validation commands and results;
- CI status or CI gap;
- artifact drift findings;
- remaining risks;
- readiness statement for `branch-ready`, `ci`, `explain-change`, isolated stop, or blocker state.
