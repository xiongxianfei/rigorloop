# Workflows

This file is the short operational summary for working in this repository. The normative workflow contract lives in `specs/rigorloop-workflow.md`.

## Choose A Lane

- Use the fast lane for trivial or low-risk work only.
  - Reference path: `spec -> implement -> verify -> pr`
  - Allowed categories: typos, formatting-only changes, small documentation clarifications, comment-only changes, small test-fixture corrections, small non-behavioral renames, and minor generated-artifact refreshes that do not change generator behavior.
  - Do not use fast lane for: behavior changes, workflow-stage changes, skill-triggering changes, architecture changes, security-sensitive behavior, CI behavior changes, release packaging, schemas, generated-output logic, or changes that are hard to roll back safely.
  - Fast-lane evidence: record a spec with intent, expected change, out of scope, and validation in the PR body, issue comment, commit message, or a linked change note.
- Use the full lifecycle for non-trivial work.
  - Required for behavior changes, workflow-stage changes, CI behavior changes, schema changes, architecture changes, and generated-output logic.

## Full Lifecycle

`constitution / project-map when needed -> explore -> research when needed -> proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review when needed -> plan -> plan-review -> test-spec -> implement -> code-review -> verify -> ci when GitHub workflow automation for a material risk is missing or stale -> explain-change -> pr`

Notes:

- `ci` means creating or updating GitHub workflows or related automation for a material risk. It does not mean waiting for routine CI to run.
- Not every stage is required for every change; stage classification and enforcement rules are defined in `specs/rigorloop-workflow.md`.
- After `spec-review`, the immediate next stage is still `architecture` when needed, otherwise `plan`. Any mention of eventual `test-spec` readiness is downstream readiness, not a stage skip.
- `plan-review` remains the normal immediate handoff into `test-spec`. If implementation readiness is mentioned there, it is downstream readiness rather than the handoff itself.
- In the execution lane, stage-owned language stays split: `implement` reports implementation completion or readiness for `code-review`; `code-review` owns review findings; `verify` owns `branch-ready`; `pr` owns `pr-body-ready` and `pr-open-ready`.
- `code-review` may inspect staged or unstaged diffs, but cited governing artifacts only support a clean branch-scoped conclusion when they are confirmed in tracked governing branch state.
- Missing tracked governing authority blocks `clean-with-notes` but does not suppress independently supported findings, and named edge cases need direct proof for clean review or `branch-ready`.
- `learn` is advice-only. Treat it as an explicit follow-up when a durable lesson actually emerged or another approved rule elevates it.

## Change-Local Artifacts

- Fast-lane work may omit `docs/changes/<change-id>/` only when the approved fast-lane policy allows omission.
- For non-trivial work, the baseline change-local pack is `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning.
- For new non-trivial work, the default durable reasoning artifact is `docs/changes/<change-id>/explain-change.md`.
- PR text remains the reviewer-facing summary surface; it does not replace required durable reasoning for non-trivial work.
- Standalone `review-resolution.md` and `verify-report.md` remain conditional and are added only when their governing workflow triggers apply.
- Approved legacy top-level artifacts under `docs/explain/` remain valid durable reasoning surfaces until they are migrated or retired.
- `docs/changes/0001-skill-validator/` is a rich example of a fully formed pack, not the universal minimum for every non-trivial change.

## Autoprogression

- Distinguish `workflow-managed` completion flows from isolated stage requests.
- In v1, workflow-managed autoprogression applies only to:
  - `proposal -> proposal-review`
  - `spec -> spec-review`
  - `architecture -> architecture-review` when that review stage is the next required or default downstream step
  - full-feature execution from `implement -> code-review -> verify -> ci when triggered -> explain-change -> pr`
- In workflow-managed full-feature runs, `code-review` first emits a first-pass review record grounded in the actual diff, upstream artifacts, checklist coverage, and validation evidence before any review-driven fixes begin.
- In workflow-managed full-feature runs, first-pass `clean-with-notes` continues to `verify`, first-pass `changes-requested` continues to `review-resolution`, and first-pass `blocked` or `inconclusive` stops.
- Clean reviews require checklist coverage plus no-finding rationale. Positive notes are optional and only useful when they add specific evidence-backed context.
- Direct `pr` remains in scope and opens the PR when readiness passes.
- Direct `proposal-review`, `spec-review`, `architecture-review`, `code-review`, `verify`, and `explain-change` stay isolated by default unless the user asks to carry the change through completion.
- Fast-lane and bugfix execution stay on the repository's existing explicit-step behavior in v1.
- `learn` remains advice-only and does not auto-run by default.
- Stop automatic continuation when the user explicitly pauses, validation fails, a review or design issue needs a real decision, permissions or tooling block the next step, or the next action would be stronger than PR creation such as merge, release, deploy, or destructive Git operations.
- Autoprogression does not replace lifecycle bookkeeping. After `code-review`, `verify`, or other review gates change the real initiative state, update the active plan, any affected active test spec, and `docs/plan.md` before claiming downstream readiness.

## Planned Milestone Work

- Use a concrete plan under `docs/plans/` for multi-file, risky, ambiguous, migration-heavy, or milestone-based work.
- `docs/plan.md` is the lifecycle index for planned initiatives; concrete plan bodies live under `docs/plans/`.
- During execution, `implement` keeps the active plan body's progress, decisions, discoveries, and validation notes current.
- When a planned initiative changes lifecycle state, final lifecycle closeout updates both `docs/plan.md` and the plan body.
- If a planned initiative's outcome is already known before PR creation, move it to `Done` in both `docs/plan.md` and the plan body before opening the PR. Only merge-dependent `Done` transitions should wait for immediate post-merge cleanup.
- `verify` blocks PR readiness when stale lifecycle state remains between the plan index and the plan body.
- Execution plans follow `docs/plans/0000-00-00-example-plan.md`.
- Each completed planned milestone ends with a coherent commit using:
  - `M<n>: <completed milestone outcome>`
- A pull request may contain one or more completed milestone commits when that is the clearest review boundary.
- Before opening or repairing a PR, compare the head branch against the current base branch. If the branch already backed a merged PR or drags already-merged history into the diff, create a fresh branch from the current base and cherry-pick or restack only the intended commits before final validation and PR creation.

## Artifact Lifecycle

Lifecycle-managed top-level artifacts keep their own tracked status. Do not treat PR state, branch state, or chat-only review outcomes as a replacement for artifact-local lifecycle state.

| Artifact | Settlement states | Closeout or terminal states |
| --- | --- | --- |
| Proposal | `accepted` | `rejected`, `abandoned`, `superseded`, `archived` |
| Spec | `approved` | `abandoned`, `superseded`, `archived` |
| Architecture | `approved` | `abandoned`, `superseded`, `archived` |
| Test spec | `active` | `abandoned`, `superseded`, `archived` |
| ADR | `accepted`, `active` | `deprecated`, `superseded`, `archived`, `abandoned` |

Notes:

- `reviewed` is transitional review output, not a durable relied-on state for proposals, top-level specs, test specs, or architecture docs.
- `accepted`, `approved`, and `active` are settlement states. `done`, `deprecated`, `rejected`, `abandoned`, `superseded`, and `archived` are closeout or terminal states.
- Keep `Next artifacts` as planning history while an artifact is active. Use `Follow-on artifacts` or `Closeout` for actual downstream artifacts or final disposition. If a `Follow-on artifacts` section appears before real follow-ons exist, it must say `None yet`.
- `superseded` artifacts must identify their replacement with `superseded_by` or equivalent labeled text. `archived` artifacts do not require a replacement pointer.
- `verify` blocks on stale lifecycle-managed artifacts that are touched, referenced, generated, or authoritative for the changed area, and it warns on unrelated stale baseline artifacts.
- Draft PR-body references participate in `verify` only when draft PR text already exists. Before that, `verify` uses `docs/changes/<change-id>/change.yaml`, explain-change artifacts, the active plan, and other touched or referenced authoritative artifacts.

## Source Of Truth

- Edit canonical workflow content in:
  - `docs/`
  - `specs/`
  - `skills/`
  - `schemas/`
  - `scripts/`
- Do not hand-edit generated Codex compatibility output in:
  - `.codex/skills/`
- Use `docs/plans/0000-00-00-example-plan.md` for plan structure. Do not reintroduce a second plan-template path.

## Validation

Run these first-release structural checks before PR:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <repo-path> [...]`

Use `bash scripts/ci.sh` to run the same checks through the repository-owned CI wrapper and report the commands you actually ran. In hosted CI, the wrapper receives explicit SHA inputs for `pr-ci` or `push-main-ci`; outside CI, it falls back to deterministic explicit-path validation over tracked changes or the latest commit diff.

Reserve `python scripts/validate-artifact-lifecycle.py --mode local` for clean worktrees only. When unrelated drafts, untracked files, or other local-only changes are present, use `--mode explicit-paths`, the diff-derived CI modes, or `bash scripts/ci.sh` instead of treating `local` mode as milestone proof.

When a change updates canonical `skills/`, keep generated `.codex/skills/` output on the `build-skills.py --check` proof path. Do not treat generated `.codex/skills/*` files as authored lifecycle-managed inputs for explicit-path artifact validation.

## CI And Release

- `.github/workflows/ci.yml` should remain a thin wrapper around repo-owned validation commands. It may set up required tooling and pass explicit diff inputs, but validation logic belongs in `scripts/ci.sh`.
- Current release automation remains conservative and tag-driven. Do not treat `scripts/release-verify.sh` as a mature release gate until repository-specific checks replace the template behavior.

## Documentation Ownership

- `README.md`: public project overview
- `docs/workflows.md`: operational workflow summary
- `docs/plan.md`: index of active, blocked, done, and superseded plans
- `docs/plans/*.md`: concrete execution plans
- `specs/*.md`: normative behavior contract
- `specs/*.test.md`: contract-to-test mapping
