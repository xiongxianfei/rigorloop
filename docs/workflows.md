# Workflows

This file is the short operational summary for working in this repository. The normative workflow contract lives in `specs/rigorloop-workflow.md`.

## Skill Contract

- The normative skill-contract source is `specs/skill-contract.md`.
- The workflow-routing source is `specs/rigorloop-workflow.md`.
- Skills are operational guides, not substitute specs.
- Shipped skill text is the user-facing interface. Keep repository-maintainer details such as canonical source paths, generated mirrors, adapter paths, selector path constraints, drift-check mechanics, and shared-block implementation details in contributor surfaces rather than in published skills.
- Skill-contract summaries in this file and `AGENTS.md` do not override approved specs.
- Shared skill policy blocks live under `templates/shared/<block-name>.md`.
- Public shared blocks are copied into consuming skills and checked for drift; maintainer-only blocks such as generated-output handling are not copied into published skills.
- Edit canonical skill source under `skills/<skill>/SKILL.md`; regenerate `.codex/skills/` and `dist/adapters/` instead of hand-editing generated output.
- Evidence reading starts from summaries, stable IDs, headings, targeted sections, check IDs, file paths, counts, and line citations before broad reads.
- Add a skill only when it owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.
- Do not create a new skill for one-off helper behavior, tiny formatting rules, or checklists that belong inside an existing skill.

## Standard Workflow

RigorLoop recommends one standard workflow for complete AI-assisted delivery.

Users may manually invoke an individual skill for focused output. Manual skill invocation is isolated by default and does not mean the full workflow is complete.

Workflow completion claims require evidence from the relevant standard workflow stages.

## Project Vision

- `VISION.md` is the canonical project-vision artifact for project identity, target users, commitments, refusals, and proposal-fit reference.
- The `vision` skill is upstream of the per-change workflow, not a normal lifecycle stage.
- Proposals created or substantively revised after this spec is adopted include `Vision fit`.
- README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `VISION.md`.
- README front-matter is not the source of truth when it conflicts with `VISION.md`.

## Workflow Categories

- Standing artifacts: `VISION.md` and `CONSTITUTION.md`.
  - `VISION.md` absence blocks the first substantive proposal unless the proposal bootstraps project vision.
  - `CONSTITUTION.md` absence blocks governance adoption, workflow-governance changes, and source-of-truth changes unless the proposal bootstraps the constitution.
- Living references: `docs/project-map.md`.
  - Do not rely on the map when it is absent, known-stale, contradicted, or missing the relied-on area. Refresh it or record a no-map rationale before reliance.
  - Calendar freshness thresholds, markers, and the full project-map revision workflow are deferred.
- Workflow infrastructure: `specs/rigorloop-workflow.md`, this summary, affected root guidance, affected stage skills, and generated skill or adapter output when canonical skills change.
  - Workflow-governance changes update affected surfaces, mark them unaffected with rationale, or defer them with owner and follow-up in a tracked or review-visible surface.
- On-demand support: `explore` and `research`.
  - Use them when ambiguity, option expansion, architecture uncertainty, external facts, platform behavior, standards, laws, pricing, or other current evidence affects the decision.
- Per-change chain:
  - `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`
  - For milestone-based plans, the `implement -> code-review -> review-resolution when triggered` segment repeats for each in-scope implementation milestone. Final closeout follows only after all in-scope implementation milestones are closed and required review-resolution is closed.
  - `review-resolution` runs only when material review findings, non-final dispositions, or review outcomes require explicit closeout.
  - `ci-maintenance` is conditional support when hosted workflow automation or related CI infrastructure for a material risk is missing, stale, or wrong.
- Periodic artifacts: `learn`.
  - Run it on cadence, after incident response, contributor observation, repeated findings, blocker or major workflow-process findings, failed release or adapter smoke, accepted postmortem actions, or explicit maintainer request.
  - When a learn session reaches Frame, record it under `docs/learn/sessions/YYYY-MM-DD-<slug>.md`; durable topic guidance uses `docs/learn/topics/<topic>.md` only when confirmed durable lessons justify it.
  - Pre-session scheduled follow-up, deferral, or no-learn rationale can close a trigger only when `learn` does not actually run as a session. Triggered `learn` blocks downstream only when a higher-priority artifact makes it blocking.

## Stage Obligations

The workflow spec owns the full stage-obligation table. The stable obligation values are:

| Obligation | Meaning |
| --- | --- |
| `mandatory` | Required whenever the row's trigger applies. |
| `conditional` | Required only when the trigger applies or the artifact or action is cited as a dependency. |
| `on-demand` | Created or run only when explicitly invoked or when the work depends on it. |
| `periodic` | Run on cadence, incident response, contributor observation, repeated finding, failed smoke, accepted postmortem action, or maintainer request. |

Notes:

- `explore` and `research` are on-demand support, not default prerequisites.
- `learn` is periodic or explicitly invoked, not a default final per-change stage. It uses tracked session records after Frame and review-visible no-record closeout only before a session runs.
- `ci-maintenance` means creating or updating hosted CI workflow files, validation automation, or platform configuration. It does not mean running validation, designing tests, specifying validation commands, or waiting for existing CI checks.
- After `spec-review`, the immediate next stage is still `architecture` when needed, otherwise `plan`. Any mention of eventual `test-spec` readiness is downstream readiness, not a stage skip.
- `plan-review` remains the normal immediate handoff into `test-spec`. If implementation readiness is mentioned there, it is downstream readiness rather than the handoff itself.
- In standard workflow execution, stage-owned language stays split: `implement` reports implementation completion or readiness for `code-review`; `code-review` owns review findings; `verify` owns `branch-ready`; `pr` owns `pr-body-ready` and `pr-open-ready`.
- Before `implement` hands off to `code-review`, the slice should satisfy a first-pass acceptable result: address in-scope requirements, required authored and aligned surfaces, required edge cases, and targeted validation for the smallest scope-complete change.
- If a required surface stays unchanged, record `unaffected with rationale` in an authoritative surface such as the active plan or required change-local artifacts. If missing or contradictory inputs prevent that standard, stop with a blocker instead of handing off an incomplete slice.
- Later review comments may still happen. A preventable first-pass miss is a finding that should have been caught by the slice's completeness set, required edge cases, or targeted validation before `code-review`.
- `code-review` may inspect staged or unstaged diffs, but cited governing artifacts only support a clean branch-scoped conclusion when they are confirmed in tracked governing branch state.
- Missing tracked governing authority blocks `clean-with-notes` but does not suppress independently supported findings, and named edge cases need direct proof for clean review or `branch-ready`.
- A material review finding is incomplete unless it has evidence, a required outcome, and a safe resolution path or `needs-decision` rationale.

## Architecture Packages

- When architecture is required, the architecture stage produces or updates the architecture package defined by `specs/architecture-package-method.md` before planning continues.
- Use `templates/architecture.md` and `templates/adr.md` as scaffolds. Real architecture and ADR records live under `docs/architecture/` and `docs/adr/`.

## Efficient Evidence Collection

- Use bounded extraction as the default first pass for large files, repeated scans, generated output, and validation logs.
- Start with inventories, headings, stable IDs, path lists, counts, or matching line numbers before reading broad file content.
- After locating relevant lines, read exact ranges first; broaden to neighboring sections or a full-file read only when needed.
- Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations before raw excerpts or pasted logs.
- Use summary-first, failure-focused, and diff-focused normal output by default. Expand only when needed with `--verbose` or an equivalent documented escape hatch.
- Normal output budgets:
  - routine command output target: 40 lines
  - routine command output warning threshold: 80 lines
  - single excerpt target: 12 lines
  - single excerpt warning threshold: 20 lines
  - multi-file summary default: one summary line per file, with details only for changed, failing, or explicitly requested files
- Do not print every parsed field, every unchanged file, large excerpts, repeated path lists, or routine command output by default.
- Output budgets guide readability and token use; they must not change validation semantics, selected check coverage, or command exit behavior.
- When normal output omits detail, it must say how to request the omitted detail.
- A full-file read is required when the file itself is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on understanding the whole source-of-truth artifact.

## Change-Local Artifacts

- Manual skill invocations may omit `docs/changes/<change-id>/` when they are not used to claim complete workflow delivery.
- For non-trivial work, the baseline change-local pack is `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning.
- For new non-trivial work, the default durable reasoning artifact is `docs/changes/<change-id>/explain-change.md`.
- PR text remains the reviewer-facing summary surface; it does not replace required durable reasoning for non-trivial work.
- Standalone `review-resolution.md` and `verify-report.md` remain conditional and are added only when their governing workflow triggers apply.
- Detailed formal review files under `docs/changes/<change-id>/reviews/` are stage-neutral across proposal, spec, architecture, plan, and code review.
- Review recording has one material-finding rule: Material review findings are always recorded. All material findings require detailed change-local review files.
- Direct or review-only requests remain isolated by default. Isolation stops handoff, not recording.
- If a detailed file is required before a change-local root exists, create the smallest initial review-record root first. Material findings require `change.yaml`, `review-log.md`, `review-resolution.md`, and `reviews/<stage>-r<n>.md`; no-material triggers require `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md` without an empty `review-resolution.md`.
- Clean required reviews with no material findings may settle in the reviewed artifact when no detailed-record trigger applies.
- When material findings exist for a non-trivial change, use `docs/changes/<change-id>/review-resolution.md` and approved dispositions: `accepted`, `rejected`, `deferred`, `partially-accepted`, and `needs-decision`.
- `needs-decision` is not final. It keeps `review-resolution.md` at `Closeout status: open` and blocks `explain-change`, `verify`, and `pr` until an authorized owner resolves or explicitly defers it.
- `Closeout status: closed` means every material finding has a final disposition, `review-log.md` lists no open findings, and the required action, rationale, follow-up, and validation evidence records for that disposition exist.
- Keep PR and explain-change review summaries concise: summarize counts by disposition and link `review-resolution.md` instead of duplicating detailed review records.
- Approved legacy top-level artifacts under `docs/explain/` remain valid durable reasoning surfaces until they are migrated or retired.
- `docs/changes/0001-skill-validator/` is a rich example of a fully formed pack, not the universal minimum for every non-trivial change.

## Autoprogression

- Distinguish `workflow-managed` completion flows from isolated stage requests.
- In v1, workflow-managed autoprogression applies only to:
  - `proposal -> proposal-review`
  - `spec -> spec-review`
  - `architecture -> architecture-review` when that review stage is the next mandatory or triggered downstream step
  - standard workflow execution from `implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`
- In workflow-managed standard workflow runs, `code-review` first emits a first-pass review record grounded in the actual diff, upstream artifacts, checklist coverage, and validation evidence before any review-driven fixes begin.
- In workflow-managed standard workflow milestone-based plans, first-pass `clean-with-notes` on a non-final implementation milestone closes the reviewed milestone and continues to the next in-scope implementation milestone.
- In workflow-managed standard workflow milestone-based plans, first-pass `clean-with-notes` on the final implementation milestone reaches final closeout only when no in-scope implementation milestone remains open or unresolved.
- In workflow-managed standard workflow runs, first-pass `changes-requested` continues to `review-resolution`, and first-pass `blocked` or `inconclusive` stops.
- If the active plan does not clearly identify the reviewed milestone or remaining in-scope implementation milestones, stop for a plan update or inconclusive review instead of inferring final-closeout readiness.
- Clean reviews require checklist coverage plus no-finding rationale. Positive notes are optional and only useful when they add specific evidence-backed context.
- Direct `pr` remains in scope and opens the PR when readiness passes.
- Direct `proposal-review`, `spec-review`, `architecture-review`, `code-review`, `verify`, and `explain-change` stay isolated by default unless the user asks to carry the change through completion.
- Manual skill invocations and bugfix skill invocations stay isolated or explicit-step in v1.
- On-demand and periodic actions such as `explore`, `research`, and `learn` do not auto-run by default.
- Stop automatic continuation when the user explicitly pauses, validation fails, a review or design issue needs a real decision, permissions or tooling block the next step, or the next action would be stronger than PR creation such as merge, release, deploy, or destructive Git operations.
- Autoprogression does not replace lifecycle bookkeeping. After `code-review`, `verify`, or other review gates change the real initiative state, update the active plan, any affected active test spec, and `docs/plan.md` before claiming downstream readiness.
- Repo-local lifecycle synchronization happens inside the PR that performs the lifecycle transition, before that PR opens for review. Merge integrates pre-validated state; it is not a routine trigger for further lifecycle closeout.

## Planned Milestone Work

- Use a concrete plan under `docs/plans/` for multi-file, risky, ambiguous, migration-heavy, or milestone-based work.
- `docs/plan.md` is the lifecycle index for planned initiatives; concrete plan bodies live under `docs/plans/`.
- Each implementation milestone has one `Milestone state`: `planned`, `implementing`, `review-requested`, `resolution-needed`, or `closed`.
- Use `review-requested` after implementation and targeted validation are complete and the milestone is handed to `code-review`.
- Use `resolution-needed` when review findings require review-resolution, fixes, owner decision, or re-review.
- Track the current milestone, current milestone state, last reviewed milestone, review status, remaining in-scope implementation milestones, next stage, final closeout readiness, and the reason in the active plan or review handoff.
- Use `lifecycle-closeout` for a milestone or section that tracks only downstream gates such as `ci-maintenance`, `explain-change`, `verify`, PR handoff, release, deploy, or final plan closeout.
- During execution, `implement` keeps the active plan body's progress, decisions, discoveries, and validation notes current.
- When a planned initiative changes lifecycle state, final lifecycle closeout updates both `docs/plan.md` and the plan body.
- If a PR completes a planned initiative, move it to `Done` in both `docs/plan.md` and the plan body before opening the PR for review.
- If completion depends on a true downstream event such as release, deploy, package publication, external migration, or an observed hosted result, keep the plan `Active` and name the downstream event or follow-up condition.
- Do not use merge itself as a routine downstream completion event.
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
- Broader repo-local lifecycle inconsistency blocks `branch-ready` when the inconsistent artifact is touched, referenced, generated, or authoritative for the changed area.
- Tracked wording such as "after merge", "post-merge", or "once this lands" should be treated as a reviewer-attention warning unless it is corrected, classified as a true downstream event, or made blocking by a lifecycle inconsistency.

## Source Of Truth

- Edit canonical workflow content in:
  - `docs/`
  - `specs/`
  - `skills/`
  - `schemas/`
  - `scripts/`
  - `templates/`
- Do not hand-edit generated Codex compatibility output in:
  - `.codex/skills/`
- Do not hand-edit generated public adapter packages in:
  - `dist/adapters/`
- For public adapter packages, `skills/` is the canonical authored skill source, `dist/adapters/` is generated installable output for Codex, Claude Code, and opencode, and `.codex/skills/` is a separate generated local Codex mirror.
- Use `docs/plans/0000-00-00-example-plan.md` for plan structure. Do not reintroduce a second plan-template path.

## Validation

Use selector-selected targeted proof as the first validation layer for non-trivial work when the changed paths are known:

- Inspect selection without running checks: `python scripts/select-validation.py --mode explicit --path <path>...`
- Execute targeted proof through the wrapper: `bash scripts/ci.sh --mode explicit --path <path>...`
- Examples of stable selected-check IDs are `skills.validate`, `review_artifacts.validate`, and `artifact_lifecycle.validate`.

`scripts/ci.sh` is the execution wrapper for selected checks. It does not imply broad smoke for every PR.

Use broad smoke only when an authoritative trigger requires it, such as selector mode `main`, selector mode `release`, an explicit `--broad-smoke` request, active plan field `broad_smoke_required: true`, test-spec requirement, review-resolution requirement, or release metadata. The selected check ID for repository broad smoke is `broad_smoke.repo`, and the direct command is:

```bash
bash scripts/ci.sh --mode broad-smoke
```

Run these structural checks before PR:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/validate-release.py --version v0.1.1`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <repo-path> [...]`

Use `bash scripts/ci.sh` with an explicit mode to run checks through the repository-owned CI wrapper and report the commands you actually ran. Hosted PR CI uses `--mode pr --base <sha> --head <sha>`, main CI uses `--mode main --base <sha> --head <sha>`, and release automation uses release-specific validation. No-argument `bash scripts/ci.sh` remains legacy broad smoke, not the normal first proof step.

Selected-check execution supports bounded local parallelism. Use `--jobs <N>` to cap concurrent reviewed parallel-safe checks; when omitted, the wrapper uses available CPU count minus one with a floor of one. Use `--jobs 1` for explicit sequential execution when debugging races or reducing local resource pressure. Use `--timeout <seconds>` to override the 60-second per-check timeout, `--fail-fast` to stop launching queued checks after an observed failure while preserving already-started check results, and `--verbose` to include successful check output in stable order.

Ordinary contributors do not need all supported tools installed locally for non-smoke validation. Repository-owned checks validate generated package structure, drift, manifests, release metadata, and security without invoking Codex, Claude Code, or opencode.

Reserve `python scripts/validate-artifact-lifecycle.py --mode local` for clean worktrees only. When unrelated drafts, untracked files, or other local-only changes are present, use `--mode explicit-paths`, the diff-derived CI modes, or `bash scripts/ci.sh` instead of treating `local` mode as milestone proof.

When a change updates canonical `skills/`, keep generated `.codex/skills/` output on the `build-skills.py --check` proof path. Do not treat generated `.codex/skills/*` files as authored lifecycle-managed inputs for explicit-path artifact validation.

## CI And Release

- `.github/workflows/ci.yml` should remain a thin wrapper around repo-owned validation commands. It may set up required tooling and pass explicit diff inputs, but validation logic belongs in `scripts/ci.sh`.
- The hosted CI workflow stays matrix-free in this first bounded-parallelism slice. Future hosted fan-out, if approved later, should consume stable check IDs from repository-owned scripts instead of duplicating selector path classification or hardcoded selected-check lists in workflow YAML.
- `scripts/release-verify.sh` is the repository-owned release gate for `v0.1.0-rc.1`, `v0.1.0`, and `v0.1.1`. It accepts a tag argument or `GITHUB_REF_NAME`, checks generated adapters and release metadata, and consumes tracked release notes from `docs/releases/<tag>/release-notes.md`.
- RC releases may be published before full manual smoke only when non-smoke gates pass and no smoke row records `fail`. Stable releases require passing Codex, Claude Code, and opencode smoke rows.

## Documentation Ownership

- `README.md`: public project overview
- `docs/workflows.md`: operational workflow summary
- `docs/plan.md`: index of active, blocked, done, and superseded plans
- `docs/plans/*.md`: concrete execution plans
- `specs/*.md`: normative behavior contract
- `specs/*.test.md`: contract-to-test mapping
- `templates/*.md`: canonical scaffolds for workflow artifacts
