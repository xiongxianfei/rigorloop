---
name: verify
description: >
  Run or reason through the final quality gate after implementation. Use to verify artifact-code-test coherence, requirement coverage, validation commands, CI readiness, drift, and release safety before explanation or PR.
argument-hint: [feature name, branch, plan path, spec path, or verification scope]
---

# Verification gate

You are proving that the implementation, tests, and durable artifacts agree.

Verification is broader than running CI. It checks completeness, correctness, coherence, and evidence.

## Inputs to read

Read:

- feature spec;
- test spec;
- architecture doc and ADRs;
- concrete plan and validation notes;
- actual diff;
- test output and CI status when available;
- code-review findings;
- `AGENTS.md` and `CONSTITUTION.md`;
- CI workflow definitions relevant to the change.

## Verification dimensions

Evaluate each with `pass`, `concern`, or `block`:

1. **Spec coverage**: every implemented behavior maps to a requirement or approved non-contract change.
2. **Requirement satisfaction**: every `MUST` has evidence.
3. **Test coverage**: every required test exists or has a documented manual verification.
4. **Test validity**: tests can fail for the right reason and assert meaningful behavior.
5. **Architecture coherence**: implementation matches design and ADRs.
6. **Plan completion**: milestones are complete or intentionally deferred, and planned initiatives do not have stale lifecycle state between `docs/plan.md` and the plan body.
7. **Validation evidence**: commands, outputs, and CI results are recorded.
8. **Drift detection**: specs/plans/architecture reflect what was actually built.
9. **Risk closure**: rollout, rollback, migration, observability, and security risks are addressed.
10. **Release readiness**: branch state, generated files, migrations, docs, and CI are ready for PR.

## Verification process

1. Build a traceability table:

```text
Requirement → Test IDs → Files changed → Evidence → Status
```

2. Check the actual diff for unplanned behavior.
3. Compare tests against the test spec.
4. For planned initiatives, compare `docs/plan.md` against the plan body and treat stale lifecycle state as a blocker. At minimum, block on completed, blocked, or superseded work still listed under `## Active`; conflicting index-versus-body state; or a plan body marked done, blocked, or superseded while still presenting itself as active or in progress.
5. Run or list required validation commands.
6. Inspect CI workflow scope if CI is expected.
7. Identify artifact drift and propose fixes.
8. Produce a final readiness verdict.

## Commands and evidence

When commands are run, record:

- command;
- working directory;
- pass/fail;
- important output;
- timestamp when relevant.

If commands cannot be run, state why and what evidence is missing.

When planned-initiative lifecycle state matters, record which `docs/plan.md` section and which plan-body lifecycle surfaces were reviewed.

## Rules

- Do not claim CI passed unless CI actually passed.
- Do not claim tests were run unless they were run.
- Do not treat unrun tests as evidence.
- Do not ignore implementation that exceeds the spec.
- Do not treat a planned initiative as PR-ready when lifecycle state is stale.
- Do not accept deferring a known `Done` transition until after merge unless merged state is the deciding event for completion.
- Do not move to PR if blockers remain.
- Do not update artifacts silently; call out drift.

## Expected output

- verification verdict: ready, concerns, or blocked;
- traceability table;
- validation commands and results;
- CI status or CI gap;
- artifact drift findings;
- remaining risks;
- readiness statement for `explain-change` and `pr`.
