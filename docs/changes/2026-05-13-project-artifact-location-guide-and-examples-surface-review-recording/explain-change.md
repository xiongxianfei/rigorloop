# Explain Change: Project Artifact Location Guide and Examples Surface

## Summary

This change makes artifact placement explicit without putting long path rules into every public skill.

The implementation adds a project-local artifact-location map to `docs/workflows.md`, teaches `workflow` when to create or refresh that guide, gives public stage skills a concise lookup rule, keeps `docs/examples/**` as non-lifecycle example content, records why `docs/changes/0001-skill-validator/` remains as a retained fixture, adds regression coverage for those invariants, and refreshes generated public adapter output.

## Problem

Public RigorLoop skills were being simplified so they no longer carried repeated path tables, review-root algorithms, generated-output details, or example path lists. That left a practical placement question: where should proposals, specs, plans, reviews, examples, change metadata, reports, and generated outputs go?

The accepted proposal chose `docs/workflows.md` as the user-facing project-local artifact map, while preserving specs and schemas as the authority for exact artifact shapes. The approved spec then made the distinction testable through requirements `R1`-`R12b`.

## Decision Trail

The proposal selected Option 3: use `docs/workflows.md` as the project artifact map. The alternative of keeping long path rules inside every skill was rejected because it duplicates rules and causes drift. The alternative of putting all placement rules in specs only was rejected because specs are not the most usable day-to-day path index for downstream projects.

Spec review raised `SR-001`: the source-rank rule and skill lookup wording could be read as inconsistent. The accepted resolution distinguished precedence from discovery order. `R2` is precedence when sources conflict; `R5a` is the token-efficient lookup path. Skills should use the workflow guide as the path index and consult governing specs or schemas when they are already known, directly relevant, cited, or needed for exact shape.

Plan review raised `PR-001`: the milestone closeout language needed each milestone to hand off to `code-review`, with M4 as generated-output implementation plus its own review. The accepted plan split implementation into:

| Milestone | Purpose | Review |
|---|---|---|
| M1 | Workflow artifact map and retained fixture rationale | `code-review-r1` |
| M2 | Stage skill lookup wording and static proof | `code-review-r2` |
| M3 | Examples routing and lifecycle validation | `code-review-r3` |
| M4 | Generated adapter refresh and final implementation review | `code-review-r4` |

No architecture package was created because the approved plan records this as workflow guidance, skill text, examples routing, validation, and generated-output work with no runtime architecture or data-flow change.

## Diff Rationale By Area

| Area | Files | Change | Reason | Source / Evidence |
|---|---|---|---|---|
| Proposal, spec, and test spec | `docs/proposals/2026-05-13-project-artifact-location-guide-and-examples-surface.md`, `specs/project-artifact-location-guide-and-examples-surface.md`, `specs/project-artifact-location-guide-and-examples-surface.test.md` | Added the accepted proposal, approved behavior contract, and active test spec. | The change needed a durable contract before altering public workflow and skill behavior. | Proposal goals; spec `R1`-`R12b`; test cases `T1`-`T14`; reviews `proposal-review-r1`, `spec-review-r1`, `spec-review-r2`. |
| Workflow guide | `docs/workflows.md` | Added the artifact-location map, source-rank guidance, schema disclaimer, conditional review-resolution/verify-report rows, and examples/retained-fixture guidance. | Users and agents need one project-local place to find default artifact locations without mistaking the table for schema authority. | Spec `R1`-`R4c`, `R6`, `R7`, `R9`, `R12b`; M1 plan. |
| Workflow skill | `skills/workflow/SKILL.md` | Added workflow-guide creation/refresh triggers and clarified that workflow owns the guide, not every artifact's content. | `workflow` must keep the guide current when placement changes, while routing users to stage skills for artifact content. | Spec `R3`-`R3b`; test `T3`; M1 validation. |
| Public stage skills | `skills/{proposal,spec,architecture,plan,test-spec,proposal-review,spec-review,architecture-review,plan-review,code-review,explain-change,verify,pr}/SKILL.md` | Added the shared concise artifact-placement lookup block to affected public skills. | Skills need token-efficient placement behavior without copying the full artifact-location table or broad-searching every authority. | Spec `R2c`-`R2g`, `R5`-`R5g`, `R10b`; test `T2`, `T4`; M2 validation. |
| Retained fixture marker | `docs/changes/0001-skill-validator/README.md` | Added rationale that the path is a retained validator fixture and historical proof pack, not an active change root or universal template, with `docs/examples/changes/skill-validator/` as the preferred future move target. | The fixture remains in an active-looking location because references and validators still depend on it. | Spec `R7`-`R8a`; test `T8`; M1/M3 validation. |
| Validation tests | `scripts/test-skill-validator.py`, `scripts/test-select-validation.py`, `scripts/test-artifact-lifecycle-validator.py`, `scripts/test-review-artifact-validator.py` | Added static and validator coverage for artifact-map wording, shared skill lookup wording, examples routing, lifecycle behavior, formal-review examples, and retained-fixture rationale. | The contract needs repository-owned checks so examples do not become active lifecycle state and public skills do not regress into duplicated path rules or broad scans. | Spec `R11`-`R11d`; tests `T1`-`T8`, `T10`, `T14`; M1-M3 validation. |
| Generated adapters | `dist/adapters/claude/**`, `dist/adapters/codex/**`, `dist/adapters/opencode/**` | Regenerated tracked public adapter output for 14 changed skills across three adapters. | Canonical skill source changed in M1 and M2, so tracked generated adapter packages had to be refreshed. | Spec `R10`-`R10b`; test `T9`; M4 validation. |
| Lifecycle evidence | `docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md`, `docs/plan.md`, `docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/**` | Recorded the active plan, change metadata, review log, review-resolution entries, proposal/spec/plan/code review records, milestone progress, validation notes, and handoffs. | The repository workflow requires durable traceability for non-trivial planned work and per-milestone code review handoffs. | `AGENTS.md`; plan `T14`; reviews `code-review-r1` through `code-review-r4`. |

## Tests Added Or Changed

`scripts/test-skill-validator.py` now covers the static contract for the workflow guide, workflow skill refresh triggers, retained fixture rationale, and shared public-skill lookup wording. It proves `T1`-`T4`, `T8`, and the static portions of `T10`/`T14`.

`scripts/test-select-validation.py` now covers representative `docs/examples/**` paths so selector routing treats them as example content, not active lifecycle paths. It proves `T5`.

`scripts/test-artifact-lifecycle-validator.py` now covers formal-review example paths under `docs/examples/**` and retained fixture rationale, proving examples do not become active plan, change, or review state. It supports `T6`, `T8`, and `T14`.

`scripts/test-review-artifact-validator.py` now proves formal review examples under `docs/examples/formal-review-recording/**` do not trigger active review closeout. It proves `T7`.

No new adapter tests were needed in M4. Existing adapter generation, validation, and distribution tests were the right level for `T9` because the milestone only refreshed derived adapter output after canonical skill edits.

## Validation Evidence Available Before Final Verify

The active plan and `change.yaml` record the full milestone validation history. Key evidence:

- M1 proof-first failure: `python scripts/test-skill-validator.py` failed before the artifact map, workflow triggers, and retained fixture marker existed.
- M1 passed: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, explicit lifecycle validation, change metadata validation, and `git diff --check`.
- M2 proof-first failure: `python scripts/test-skill-validator.py` failed before shared artifact lookup wording existed.
- M2 passed: skill validator, skill validation, lifecycle validation, review-artifact closeout, change metadata validation, and `git diff --check`.
- M3 passed: selector, lifecycle, review-artifact, change-metadata, and skill-validator tests; explicit selector and lifecycle validation for example paths; `git diff --check`.
- M4 proof-first adapter drift: `python scripts/build-adapters.py --version 0.1.1 --check` and `python scripts/validate-adapters.py --version 0.1.1` failed with 42 stale generated adapter files.
- M4 passed after regeneration: `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/test-adapter-distribution.py`, skill/selector/lifecycle/review/change-metadata test suites, review-artifact closeout, change metadata validation, explicit lifecycle validation, and `git diff --check`.

Hosted CI has not been claimed. Final `verify` still owns final validation and readiness checks.

## Review Resolution Summary

`review-resolution.md` is closed.

Material findings:

| Finding | Source review | Disposition | Summary |
|---|---|---|---|
| `SR-001` | `spec-review-r1` | accepted | Clarified source-rank precedence versus token-efficient lookup/read order. |
| `PR-001` | `plan-review-r1` | accepted | Required M1-M4 to each hand off to `code-review`, with M4 as generated-output implementation plus its own review. |

No material findings were raised in `proposal-review-r1`, `spec-review-r2`, `plan-review-r2`, or `code-review-r1` through `code-review-r4`.

## Alternatives Rejected

Keeping detailed path rules inside every skill was rejected because it duplicates long guidance, expands public skill text, and creates drift when project artifact locations change.

Putting all placement rules only in specs was rejected because specs remain the authority for exact shapes but are not the best project-local path index for day-to-day use.

Moving `docs/changes/0001-skill-validator/` immediately was rejected for this slice because existing validators, specs, docs, and historical references still cite the active-looking path. The safer outcome was to retain it with visible rationale and a future preferred move target.

Hand-editing generated adapter output was rejected. M4 used `python scripts/build-adapters.py --version 0.1.1` so `dist/adapters/**` remains derived from canonical `skills/**`.

Broad smoke validation by default was rejected by the test spec. The plan used milestone-specific and targeted validation unless an authority triggered more.

## Scope Control

The change did not alter the standard workflow order, formal review recording schema, review-resolution dispositions, or generated adapter packaging behavior.

`docs/workflows.md` now provides default locations and owning skills, but it does not override `CONSTITUTION.md`, approved specs, schemas, active plan state, matching test specs, or explicit safe user paths.

The public skills gained concise lookup wording, not full path tables, long review-root algorithms, or repository-maintainer-only validator internals.

Examples stayed under `docs/examples/**`; the retained `docs/changes/0001-skill-validator/` path was marked as a fixture rather than generalized into a required change-root template.

## Risks And Follow-Ups

The artifact-location map can still become stale if future changes alter paths without refreshing `docs/workflows.md`. The workflow skill now names refresh triggers, and validation can catch stable wording regressions.

The shared lookup wording is repeated across affected public skills. Static validation protects the current wording, but a future shared-block source could reduce drift if the repository introduces one.

`docs/changes/0001-skill-validator/` remains an active-looking path. It has durable rationale now, but a future cleanup can move it to `docs/examples/changes/skill-validator/` once all references and validators can be updated safely.

Final `verify` and PR handoff are still incomplete. The active plan state is ready for `verify` only after this explanation is recorded and validated; it is not PR-ready.
