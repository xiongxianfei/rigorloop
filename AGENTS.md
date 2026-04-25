# AGENTS.md

This repository uses Codex to help maintain a public open source project.

Optimize for correctness, explicitness, small reviewable diffs, and alignment with the documented contract over speculative improvements.

Detailed governance lives in `CONSTITUTION.md`. `AGENTS.md` stays concise and points to the governing artifacts.

## Instruction precedence

When instructions conflict, follow this order:

1. Direct user request
2. `CONSTITUTION.md`
3. Approved feature spec in `specs/`
4. Approved architecture or ADR docs when relevant
5. Active execution plan file in `docs/plans/`
6. Matching test spec in `specs/`
7. `docs/workflows.md`
8. This file

Do not silently blend conflicting higher-priority instructions. Call out the conflict, explain the impact, and follow the highest-priority source that already implies the answer.

## Repository defaults

- Prefer the smallest change that fully satisfies the request.
- Do not add unrelated refactors while implementing a scoped task.
- Preserve user changes unless explicitly asked to revert them.
- When behavior changes, update the relevant spec, test spec, docs, or examples in the same change when this repository uses them.
- Reuse existing scripts and workflows before inventing new commands or processes.
- Edit canonical workflow content in `docs/`, `specs/`, `skills/`, `schemas/`, and `scripts/`.
- Do not hand-edit generated Codex compatibility output in `.codex/skills/`.
- Do not hand-edit generated public adapter package output in `dist/adapters/`.
- Public adapter packages for Codex, Claude Code, and opencode are generated under `dist/adapters/`; `.codex/skills/` remains a separate generated local Codex runtime mirror.
- For non-trivial work, the baseline change-local artifact pack is `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning. Standalone `review-resolution.md` and `verify-report.md` remain conditional under the workflow contract.
- When material review findings exist, record complete findings with evidence, required outcome, and safe resolution or `needs-decision` rationale. Use `review-resolution.md` dispositions `accepted`, `rejected`, `deferred`, `partially-accepted`, or `needs-decision`; `needs-decision` keeps `Closeout status: open`, while `Closeout status: closed` requires final dispositions and validation evidence.
- Keep `AGENTS.md` practical. Move workflow detail to `docs/workflows.md` and feature-specific detail to `specs/`.

## Planning and workflow

Use a plan first for work that is multi-file, risky, ambiguous, architecture-affecting, migration-heavy, or large enough that it should be split into reviewable milestones.

For the lifecycle contract, follow `specs/rigorloop-workflow.md`.

Use `docs/workflows.md` for the short operational summary.

Once proposal, spec, and architecture are already settled, execution usually proceeds through:

`plan -> plan-review -> test-spec -> implement -> code-review -> verify -> ci when needed -> explain-change -> pr`

In workflow-managed completion flows, continue automatically into the next required or default downstream stage when the approved autoprogression contract says to do so. Do not wait for redundant user confirmation to enter a known review or PR gate. Review-only or explicitly isolated stage requests stay isolated, direct `pr` still opens the PR when readiness passes, and fast-lane and bugfix execution remain explicit-step unless a higher-priority artifact broadens them.

Add `plan-review` before spec work when the task is risky, cross-cutting, or hard to sequence cleanly.

Use `bugfix` for bugs, `ci` for GitHub Actions or automation changes when workflow automation for a material risk is missing or stale, and `pr` only when the branch is already ready for review.

## Plan file policy

- `docs/roadmap.md` stores future ideas and unapproved work.
- `docs/plan.md` is the lifecycle index of active, blocked, done, and superseded execution plans. It is not the body of a plan.
- Concrete plan files under `docs/plans/` are the plan bodies that carry initiative detail.
- Every approved initiative gets its own living plan file under `docs/plans/YYYY-MM-DD-slug.md`.
- Never overwrite an older plan when starting a new initiative.
- If a new plan replaces an older one, keep the older file and mark it as superseded.
- Execution plans should follow `docs/plans/0000-00-00-example-plan.md`.

## Required reading before implementation

Before implementing behavior-changing work, follow the source-of-truth order from `CONSTITUTION.md`. In practice, read in this order when the files exist:

1. `CONSTITUTION.md`
2. the relevant feature spec in `specs/<feature>.md`
3. approved architecture or ADR docs when they are relevant to the change
4. `docs/plan.md`, then the active plan file in `docs/plans/`
5. the matching test spec in `specs/<feature>.test.md`
6. `docs/workflows.md` when the task touches an existing flow or release process
7. the files you expect to modify

If the work changes externally observable behavior and no relevant spec exists, create or request the missing spec before coding the contract into the implementation.

## Spec and test conventions

- `specs/<feature>.md` defines the contract: requirements, examples, edge cases, non-goals, compatibility expectations, and acceptance criteria.
- `specs/<feature>.test.md` maps requirements and edge cases to concrete tests.
- Every `MUST` in a spec should map to at least one test.
- The test spec does not override the feature spec; it operationalizes it.

## Artifact lifecycle defaults

- Proposal, spec, test-spec, architecture, and ADR status lives inside the artifact, not in PR state or chat-only review outcomes.
- For proposals, top-level specs, test specs, architecture docs, and ADRs, `reviewed` is transitional only where it exists in older artifacts. Durable current states are `accepted`, `approved`, and `active`. Terminal or historical states include `deprecated`, `rejected`, `abandoned`, `superseded`, and `archived`.
- Keep `Next artifacts` as planning history while an artifact is active. Use `Follow-on artifacts` or `Closeout` for actual downstream artifacts or final disposition. If a `Follow-on artifacts` section appears before real follow-ons exist, it must say `None yet`.
- `superseded` artifacts must identify their replacement with `superseded_by` or equivalent labeled text.
- `verify` blocks on stale touched, referenced, generated, or authoritative lifecycle-managed artifacts and warns on unrelated stale baseline debt.

## Implementation rules

- Keep diffs scoped.
- Write or update tests first when feasible.
- Run the smallest relevant verification scope first, then expand only as needed.
- If validation fails, stop and fix the failure before moving to the next milestone.
- During execution, `implement` owns ongoing plan-body updates. Keep the active plan's progress, decisions, discoveries, and validation notes current as work proceeds.
- If a spec gap blocks safe implementation, state it explicitly instead of silently guessing.

## Verification expectations

- Until the repository-wide validation scripts are fully implemented, use the exact validation commands named in the active plan and matching test spec.
- When repo-owned validation scripts exist, run those named commands before PR instead of inventing substitute checks.
- For adapter package work, ordinary contributors do not need all supported tools installed locally; non-smoke validation is repository-owned through adapter generation, adapter validation, release metadata validation, and `scripts/release-verify.sh`.
- Release automation must use tracked release notes under `docs/releases/<tag>/release-notes.md`; do not rely on generated release notes for adapter compatibility claims.
- For planned initiatives, final lifecycle closeout updates both `docs/plan.md` and the plan body when lifecycle state changes, and `verify` treats stale lifecycle state between them as blocking PR readiness.
- Do not report success without naming the commands actually run.

## Change management

- Do not rewrite plan, spec, or workflow files unless the task requires it.
- Remove or challenge stale instructions when they no longer match reality.
- If a request conflicts with the current spec, ask whether the spec should change or the implementation should intentionally diverge only when the higher-priority sources do not already imply the answer.

## Definition of done

A task is not done unless all of the following are true:

- the implementation matches the current contract
- relevant verification was run, or any inability to run it is stated clearly
- named edge cases and failure paths are handled or explicitly deferred
- the user-visible scope does not silently exceed what was agreed
- the active plan reflects what actually happened when a plan was used
- meaningful assumptions and open questions are called out in the final response
