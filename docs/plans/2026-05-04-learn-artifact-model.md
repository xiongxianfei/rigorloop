# Learn Artifact Model Implementation Plan

## Status

- active

- Owner: maintainers
- Start date: 2026-05-04
- Last updated: 2026-05-04
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: refactored
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow governance, skill guidance, validation selection, generated skill mirrors, and generated public adapter output. Focused selector-selected checks, skill validation, lifecycle validation, generated-output drift checks, adapter validation, and explicit-path CI are the required proof unless plan-review, test-spec, code-review, review-resolution, or verify elevates broad smoke.

## Purpose / Big Picture

Implement the approved learn artifact model so `learn` sessions have one canonical session-record surface, optional curated topic guidance, contributor-confirmed classifications, action routing into authoritative artifacts, and bounded evidence collection.

This is workflow-governance and documentation-infrastructure work. It changes contributor-visible artifact routing and validation selection, not product runtime behavior, storage, deployment, hosted services, or release packaging.

## Source Artifacts

- Proposal: [Optimize Learn Skill](../proposals/2026-05-03-optimize-learn-skill.md), accepted.
- Spec: [Learn Artifact Model](../../specs/learn-artifact-model.md), approved after spec-review on 2026-05-04.
- Spec-review outcome: approved with no material findings after the classification model, deterministic session-record creation, no-record boundary, and periodic window fields were added.
- Architecture: not required. The approved work is a workflow-governance, documentation, skill, selector, and generated-output change without a runtime architecture boundary.
- Test spec: [Learn Artifact Model test spec](../../specs/learn-artifact-model.test.md), active.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on repository-map claims for architecture, data flow, or module boundaries. Orientation comes from the approved proposal, approved spec, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, the existing workflow spec/test spec, the learn skill, validation selector code, and bounded file inventories. If implementation later relies on broader repository-shape claims, refresh `docs/project-map.md` or record a narrower no-map rationale before relying on those claims.

## Context and Orientation

- `specs/learn-artifact-model.md` is the approved contract for final learn surfaces and behavior.
- `specs/rigorloop-workflow.md` still contains the temporary `learn` closeout rule in `R7be` and old follow-on/non-goal text that names the deferred final model. Implementation must retire or replace that temporary wording without changing `learn` into a default per-change stage.
- `specs/rigorloop-workflow.test.md` has active proof surface `T23` for the old temporary learn closeout. It must be updated so proof maps to the final model.
- `skills/learn/SKILL.md` still routes general retrospectives to `docs/retrospectives/YYYY-MM-DD-slug.md` and uses temporary follow-up/no-learn surfaces before the learn refactor. It must become the primary operator guidance for the four-phase learn process.
- `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` currently state that `learn` is periodic or explicitly invoked and record no-learn or follow-up closeout. They must stay aligned with the approved final model where their guidance is affected.
- `README.md` mentions periodic learning but does not define learn artifact surfaces. Initial disposition: unaffected unless implementation finds wording that conflicts with the final model.
- `docs/learn/` does not exist. The first implementation may add a lightweight `docs/learn/README.md` index but must not add templates, empty topic files, or a prebuilt taxonomy.
- `scripts/validation_selection.py` currently has no `docs/learn/**` category. The selector must recognize `docs/learn/sessions/**` and `docs/learn/topics/**` as known learn artifact paths without incorrectly sending them through lifecycle validation.
- Canonical skill source is under `skills/`. Generated `.codex/skills/` and `dist/adapters/` output must be refreshed through repository generators only.

## Non-Goals

- Do not make `learn` mandatory for every change.
- Do not make `learn` the lifecycle bookkeeping owner for `docs/plan.md`, plan bodies, review-resolution closeout, verification readiness, PR readiness, or CI status.
- Do not create session templates, topic templates, empty topic files, or a fixed topic taxonomy.
- Do not build an issue tracker, project-management system, background indexer, or automated lesson triage service.
- Do not migrate historical notes into `docs/learn/` unless a later approved migration plan requires it.
- Do not treat topic files as authoritative policy, specs, ADRs, architecture docs, workflow contracts, or skill contracts.
- Do not capture durable lessons from isolated single events without reusable evidence or systemic-gap evidence.
- Do not bypass downstream review for derivative ADRs, proposals, specs, architecture docs, workflow changes, or skill behavior changes.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`, `R26`-`R30` | Preserve periodic or explicit `learn` triggers, evidence standards, single-event handling, maintainer-request handling, and empty-session validity in `specs/rigorloop-workflow.md`, `docs/workflows.md`, root guidance, and `skills/learn/SKILL.md`. |
| `R2`-`R9` | Define session-record creation, canonical paths, optional `docs/learn/README.md`, no empty taxonomy, and required session-record fields in the learn skill, workflow spec, and lightweight learn index. |
| `R10`-`R18` | Implement four-phase process guidance, evidence-bound observations, already-captured lesson checks, one primary classification, secondary routes, contributor confirmation, and no-routing-without-confirmation in `skills/learn/SKILL.md` and skill-validator proof. |
| `R19`-`R25a` | Implement routing rules for `observation`, `durable-lesson`, `artifact-update`, `decision`, `direction`, `process-follow-up`, `no-durable-lesson`, and pre-session no-record closeout in skill and workflow guidance. |
| `R31`-`R35` | Document topic-file authority, non-override rules, authoritative artifact updates, topic curation, and traceability for removal or absorption in `docs/learn/README.md`, the learn skill, and workflow guidance. |
| `R36`-`R43` | Implement bounded evidence collection and trigger-specific evidence guidance in `skills/learn/SKILL.md`, with tests for stable required wording. |
| `R44` | Add selector recognition and regression coverage for `docs/learn/sessions/**`, `docs/learn/topics/**`, and optional `docs/learn/README.md`. |
| `R45` | Keep affected workflow-governance surfaces aligned or record unaffected rationale in this plan, the test spec, or implementation artifacts. |
| `R46` | Update `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md` so the temporary learn-recording rule no longer acts as the final model. |
| `R47` | Refresh generated `.codex/skills/` and public adapter output through `build-skills.py` and `build-adapters.py`. |

## Milestones

### M1. Workflow Contract And Governance Alignment

- Goal: Replace temporary learn-model wording in authoritative workflow surfaces with the approved final session/topic/action routing model while preserving the nonblocking periodic role of `learn`.
- Requirements: `R1`-`R9`, `R19`-`R35`, `R45`, `R46`.
- Files/components likely touched: `specs/rigorloop-workflow.md`, `specs/rigorloop-workflow.test.md`, `docs/workflows.md`, `AGENTS.md`, `CONSTITUTION.md`, possibly `README.md` only if affected wording is found, `docs/changes/2026-05-04-learn-artifact-model/change.yaml`, `docs/changes/2026-05-04-learn-artifact-model/explain-change.md`, this plan.
- Dependencies: approved `specs/learn-artifact-model.md`; accepted `docs/proposals/2026-05-03-optimize-learn-skill.md`; plan-review accepted; active `specs/learn-artifact-model.test.md`.
- Tests to add/update: update `specs/rigorloop-workflow.test.md`; map requirements in `specs/learn-artifact-model.test.md`.
- Implementation steps:
  - Replace deferred/temporary learn-model wording in `specs/rigorloop-workflow.md` with references to the approved final model and canonical `docs/learn/` surfaces.
  - Update `specs/rigorloop-workflow.test.md` so `T23` and related non-goal/readiness language verify the final model instead of temporary surfaces.
  - Align `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` where they discuss triggered learn closeout, no-learn rationale, and durable lessons.
  - Review `README.md`; update it only if it conflicts with the final model, otherwise record it as unaffected in the plan or explain-change.
  - Create the change-local artifact pack and keep plan progress current.
- Validation commands:
  - `rg -n "docs/learn|docs/learnings|docs/retrospectives|temporary learn|final learn|no-learn|scheduled follow-up|periodic" specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/workflows.md AGENTS.md CONSTITUTION.md README.md`
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/plan.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/plan.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md README.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md specs/learn-artifact-model.md specs/learn-artifact-model.test.md docs/plans/2026-05-04-learn-artifact-model.md docs/plan.md docs/changes/2026-05-04-learn-artifact-model`
- Expected observable result: contributors can read the workflow contract and summaries and find the final learn artifact model instead of the old temporary-surface rule.
- Commit message: `M1: align workflow contract with learn artifact model`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: broad workflow edits can accidentally change stage order or make `learn` look mandatory for every change.
- Rollback/recovery: revert only the workflow/governance wording and return to the approved spec for corrected wording before touching skill or selector behavior.

### M2. Learn Path Selector Recognition

- Goal: Classify `docs/learn/sessions/**`, `docs/learn/topics/**`, and `docs/learn/README.md` as known learn artifact paths with lightweight selector behavior and regression coverage before any `docs/learn/**` artifact is created or selector-validated.
- Requirements: `R44`.
- Files/components likely touched: `scripts/validation_selection.py`, `scripts/test-select-validation.py`, change-local artifacts, this plan.
- Dependencies: M1 defines final workflow contract.
- Tests to add/update: selector regression tests that assert learn paths are classified, produce no unclassified paths, and do not route session/topic files through lifecycle validation.
- Implementation steps:
  - Add a learn-artifact category for `docs/learn/README.md`, `docs/learn/sessions/**`, and `docs/learn/topics/**`.
  - Add selector tests for session records, topic files, and the optional README index.
  - Ensure selector output remains `ok` and does not produce manual-routing blockers for recognized learn paths.
  - Keep validation lightweight; do not add templates or structural content validators for session/topic files.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path docs/learn/README.md --path docs/learn/sessions/2026-05-04-example.md --path docs/learn/topics/verification.md`
  - `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
- Expected observable result: the validation selector recognizes the new learn artifact namespace without treating raw session records or curated topic files as lifecycle-managed specs.
- Commit message: `M2: classify learn artifact paths`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: sending `docs/learn/**` through the wrong validator could make valid learn sessions fail because they are not lifecycle-managed artifacts.
- Rollback/recovery: revert selector category changes and keep `docs/learn/**` path recognition deferred until a safer lightweight category is defined.

### M3. Learn Skill, Learn Index, And Generated Output

- Goal: Make `skills/learn/SKILL.md` guide the approved Frame, Observe, Classify, Route process, add the lightweight learn namespace index, and refresh generated skill/adapter output.
- Requirements: `R2`-`R43`, `R47`.
- Files/components likely touched: `skills/learn/SKILL.md`, `docs/learn/README.md`, `scripts/test-skill-validator.py`, `.codex/skills/learn/SKILL.md`, `dist/adapters/claude/.claude/skills/learn/SKILL.md`, `dist/adapters/codex/.agents/skills/learn/SKILL.md`, `dist/adapters/opencode/.opencode/skills/learn/SKILL.md`, change-local artifacts, this plan.
- Dependencies: M1 wording is stable enough that the skill can point to the approved workflow surfaces without duplicating unrelated lifecycle rules; M2 selector recognition is complete so `docs/learn/README.md` can be created and selector-validated without an unclassified-path blocker.
- Tests to add/update: extend `scripts/test-skill-validator.py` for stable learn terms such as `docs/learn/sessions`, `docs/learn/topics`, `Frame`, `Observe`, `Classify`, `Route`, `primary classification`, `secondary routes`, `no-durable-lesson`, and bounded evidence language.
- Implementation steps:
  - Rewrite `skills/learn/SKILL.md` around the four ordered phases and trigger-specific bounded evidence guidance.
  - Replace `docs/retrospectives/**` and temporary follow-up/no-learn guidance with `docs/learn/sessions/**`, `docs/learn/topics/**`, action-owning artifacts, and pre-session no-record closeout.
  - Add `docs/learn/README.md` as an index explaining `sessions/` and `topics/` without adding templates or empty topic files.
  - Update skill-validator regression expectations for the new stable learn guidance.
  - Run generators for `.codex/skills/` and `dist/adapters/`.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/select-validation.py --mode explicit --path skills/learn/SKILL.md --path docs/learn/README.md --path scripts/test-skill-validator.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `bash scripts/ci.sh --mode explicit --path skills/learn/SKILL.md --path docs/learn/README.md --path scripts/test-skill-validator.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `git diff --check -- skills/learn/SKILL.md docs/learn/README.md scripts/test-skill-validator.py .codex/skills/learn/SKILL.md dist/adapters/claude/.claude/skills/learn/SKILL.md dist/adapters/codex/.agents/skills/learn/SKILL.md dist/adapters/opencode/.opencode/skills/learn/SKILL.md docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
- Expected observable result: invoking `learn` gives contributors process guidance and canonical paths that match the approved spec, and generated outputs match canonical skill source.
- Commit message: `M3: implement learn skill artifact routing`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: the skill may become a template disguised as guidance, or generated outputs may drift if generators are not run.
- Rollback/recovery: revert canonical skill/index changes, rerun generators, and keep workflow contract in M1 as the source of truth while correcting skill wording.

### M4. Final Validation And Lifecycle Closeout

- Goal: Prove the full implementation surface is coherent, update lifecycle state, and prepare the change for review handoff.
- Requirements: `R1`-`R47`.
- Files/components likely touched: `docs/plan.md`, this plan, `docs/changes/2026-05-04-learn-artifact-model/change.yaml`, `docs/changes/2026-05-04-learn-artifact-model/explain-change.md`, possibly review/verify artifacts if triggered.
- Dependencies: M1-M3 complete; generated output is in sync; no material review findings remain open.
- Tests to add/update: no new feature behavior tests beyond M1-M3; final proof reruns selected checks and drift checks across the whole changed surface.
- Implementation steps:
  - Run selector-selected CI for all touched paths.
  - Run structural skill, selector, lifecycle, generated skill, adapter drift, and adapter validation checks explicitly.
  - Update plan progress, validation notes, surprises, and outcome; update `docs/plan.md` when lifecycle state changes.
  - Update explain-change with final rationale and validation evidence.
  - Stop for `code-review` and downstream gates; do not skip review-resolution if material findings appear.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-03-optimize-learn-skill.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/learn/README.md --path docs/proposals/2026-05-03-optimize-learn-skill.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path skills/learn/SKILL.md --path scripts/test-skill-validator.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `git diff --check --`
- Expected observable result: all touched authoritative and generated surfaces agree on the final learn artifact model and validation evidence is ready for `code-review`.
- Commit message: `M4: close learn artifact model implementation`
- Milestone closeout:
  - [ ] validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks: final validation may reveal stale lifecycle-managed artifacts that were referenced by the plan or explain-change.
- Rollback/recovery: fix stale touched/referenced artifacts before verify; if the implementation must be abandoned, mark this plan blocked or superseded and restore temporary learn guidance consistently.

## Validation Plan

- Use selector-selected targeted proof first for each milestone.
- Use `specs/learn-artifact-model.test.md` as the requirement-to-test proof map once it is authored and active.
- Run repository-owned skill, selector, lifecycle, generated-output drift, adapter validation, and explicit-path CI commands named in the milestone that touches each surface.
- Use broad smoke only if `plan-review`, `test-spec`, `code-review`, `review-resolution`, or `verify` adds a higher-priority trigger.
- Do not claim hosted CI status unless a hosted run is observed.

## Risks And Recovery

- Risk: learn guidance becomes too heavy for small explicit invocations.
  - Recovery: keep `docs/learn/README.md` an index only, avoid templates, and keep bounded evidence rules in the skill.
- Risk: topic files become quasi-policy.
  - Recovery: route behavior changes to authoritative artifacts and treat topic files as curated guidance with source links.
- Risk: selector validation is too strict for raw session records.
  - Recovery: keep the first selector slice lightweight and avoid lifecycle validation for `docs/learn/sessions/**`.
- Risk: generated output drift appears after skill changes.
  - Recovery: rerun `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1`, then rerun drift checks.
- Risk: affected governance surfaces drift.
  - Recovery: update the affected surface or record unaffected/deferred rationale in a contributor-visible artifact before downstream handoff.

## Dependencies

- `specs/learn-artifact-model.md` is approved.
- `docs/proposals/2026-05-03-optimize-learn-skill.md` is accepted.
- `plan-review` must accept this plan before implementation.
- `specs/learn-artifact-model.test.md` must be authored and active before implementation.
- Learn path selector recognition must complete before any `docs/learn/**` artifact is created or selector-validated.
- Generated outputs depend on `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1`.
- Adapter validation uses version `0.1.1`.
- No external service, network dependency, new package dependency, or issue tracker is required.

## Progress

- [x] 2026-05-04: Plan created and `docs/plan.md` index updated.
- [x] 2026-05-04: Plan-review sequencing finding resolved by moving selector recognition before learn index creation.
- [x] 2026-05-04: Plan-review approved with no material findings after selector sequencing was fixed.
- [x] 2026-05-04: Test spec authored and marked active.
- [x] 2026-05-04: M1 complete.
- [x] 2026-05-04: M1 `code-review` round 1 finding `CR-M1-F1` accepted and resolved.
- [x] 2026-05-04: M1 `code-review` round 2 completed with `clean-with-notes`.
- [x] 2026-05-04: M1 verified as a milestone slice; full initiative branch-ready is deferred until M2-M4 complete.
- [x] 2026-05-04: M2 selector tests written first; representative learn paths failed as unclassified before implementation.
- [x] 2026-05-04: M2 implementation complete; `docs/learn/README.md`, `docs/learn/sessions/**`, and `docs/learn/topics/**` now classify as lightweight `learn-artifact` paths.
- [x] M2 complete.
- [x] 2026-05-04: M2 `code-review` round 1 finding `CR-M2-F1` accepted and resolved before round 2.
- [x] 2026-05-04: M2 `code-review` round 2 completed with `clean-with-notes`.
- [x] 2026-05-04: M2 verified as a milestone slice; full initiative branch-ready is deferred until M3-M4 complete.
- [x] 2026-05-04: M3 skill-validator regression was written before implementation; it failed as expected because `docs/learn/README.md` did not exist and the canonical learn guidance was still old.
- [x] 2026-05-04: M3 implementation complete; `skills/learn/SKILL.md` now guides Frame, Observe, Classify, and Route; `docs/learn/README.md` is the lightweight namespace index; generated skill and public adapter outputs were refreshed.
- [x] 2026-05-04: M3 selector-selected CI passed for canonical skill, learn index, regression test, generated Codex skill output, generated public adapter output, plan, and change metadata.
- [x] M3 complete.
- [x] 2026-05-04: M3 `code-review` round 1 completed with `clean-with-notes`.
- [x] 2026-05-04: M3 verified as a milestone slice; full initiative branch-ready is deferred until M4 completes final validation and lifecycle closeout.
- [x] 2026-05-04: M3 `code-review` round 2 finding `CR-M3-R2-F1` accepted and resolved; the learn skill now covers maintainer-driven rule adoption without accumulated evidence.
- [x] 2026-05-04: M3 `code-review` round 3 completed with `clean-with-notes`.
- [ ] M4 complete.

## Decision Log

- 2026-05-04: No separate architecture artifact is required because the approved spec changes repository workflow, docs, skill guidance, selector routing, and generated output rather than runtime architecture, data flow, persistence, deployment, or integration boundaries.
- 2026-05-04: `docs/learn/README.md` is planned as a lightweight namespace index, not a template, because the spec allows an index but forbids first-slice session/topic templates and empty topic taxonomy.
- 2026-05-04: Selector recognition for `docs/learn/**` should be a lightweight category rather than lifecycle validation because session records and topic files are not lifecycle-managed specs, plans, ADRs, or architecture artifacts.
- 2026-05-04: Selector recognition must precede the learn skill/index milestone because current validation selection blocks unclassified `docs/learn/**` paths.
- 2026-05-04: M1 keeps detailed learn-session procedure in `specs/learn-artifact-model.md` and `specs/learn-artifact-model.test.md`; `specs/rigorloop-workflow.md` owns only workflow-level routing, nonblocking behavior, and source-of-truth boundaries.
- 2026-05-04: M2 classifies learn paths as `learn-artifact` and selects no validator for those paths. This keeps validation lightweight until session/topic shapes are proven by usage or a later validator contract.
- 2026-05-04: M3 names public adapter output and install-location alternatives alongside `.codex/skills/` in the learn skill's generated-output boundary so repository generators keep `learn` portable across Codex, Claude, and opencode adapters.

## Surprises And Discoveries

- `docs/project-map.md` is absent; this plan records a no-map rationale and does not rely on it.
- `README.md` mentions periodic learning as a lifecycle category but does not define learn artifact surfaces; M1 leaves it unchanged and records it as unaffected in `docs/changes/2026-05-04-learn-artifact-model/change.yaml`.
- M1 code-review found that two affected surfaces omitted incident response and contributor observation from the learn trigger list even though the workflow contract and learn artifact spec included them. The targeted fix restored those trigger classes in `docs/workflows.md` and `specs/rigorloop-workflow.test.md`.
- M2 does not create `docs/learn/README.md` or any session/topic file; selector recognition now makes those paths safe for M3 to create and selector-validate.
- M3 adapter generation initially treated `learn` as non-portable when the skill mentioned `.codex/skills/` without public adapter alternatives. Naming `dist/adapters/`, `.agents/skills`, `.claude/skills`, and `.opencode/skills` in the generated-output boundary restored generated adapter coverage.
- M3 follow-up code-review found that the learn skill omitted the `R29` maintainer-driven rule-adoption edge case. The targeted fix added that guidance to the canonical skill, protected it in skill-validator coverage, and regenerated skill and adapter outputs.

## Validation Notes

- 2026-05-04: Plan creation validation passed.
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/proposals/2026-05-03-optimize-learn-skill.md --path specs/learn-artifact-model.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/proposals/2026-05-03-optimize-learn-skill.md --path specs/learn-artifact-model.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/proposals/2026-05-03-optimize-learn-skill.md --path specs/learn-artifact-model.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-04-learn-artifact-model.md docs/proposals/2026-05-03-optimize-learn-skill.md specs/learn-artifact-model.md`
- 2026-05-04: Test spec authoring validation passed.
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/proposals/2026-05-03-optimize-learn-skill.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/proposals/2026-05-03-optimize-learn-skill.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/proposals/2026-05-03-optimize-learn-skill.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-04-learn-artifact-model.md docs/proposals/2026-05-03-optimize-learn-skill.md specs/learn-artifact-model.md specs/learn-artifact-model.test.md`
- 2026-05-04: M1 validation passed.
  - `rg -n 'temporary learn|future learn refactor|final learn artifact model is deferred|docs/learnings|docs/retrospectives|Until a focused \`learn\` refactor|scheduled \`learn\` follow-ups and explicit no-learn rationales|temporary recording surfaces|Future focused \`learn\` refactor' specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/workflows.md AGENTS.md CONSTITUTION.md README.md`
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/plan.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/plan.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md README.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md specs/learn-artifact-model.md specs/learn-artifact-model.test.md docs/plans/2026-05-04-learn-artifact-model.md docs/plan.md docs/changes/2026-05-04-learn-artifact-model`
- 2026-05-04: M1 review-resolution validation passed after resolving `CR-M1-F1`.
  - `rg -n 'temporary learn|future learn refactor|final learn artifact model is deferred|docs/learnings|docs/retrospectives|Until a focused \`learn\` refactor|scheduled \`learn\` follow-ups and explicit no-learn rationales|temporary recording surfaces|Future focused \`learn\` refactor' specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/workflows.md AGENTS.md CONSTITUTION.md README.md`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path specs/rigorloop-workflow.test.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r1.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r1.md --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md`
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path specs/rigorloop-workflow.test.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r1.md`
  - `git diff --check -- docs/workflows.md specs/rigorloop-workflow.test.md docs/changes/2026-05-04-learn-artifact-model`
- 2026-05-04: M1 code-review round 2 validation passed.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path specs/rigorloop-workflow.test.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r1.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r2.md`
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path specs/rigorloop-workflow.test.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r1.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r2.md`
  - `git diff --check -- docs/workflows.md specs/rigorloop-workflow.test.md docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
- 2026-05-04: M1 verification passed for the committed M1 slice.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
  - `rg -n 'temporary learn|future learn refactor|final learn artifact model is deferred|docs/learnings|docs/retrospectives|Until a focused \`learn\` refactor|scheduled \`learn\` follow-ups and explicit no-learn rationales|temporary recording surfaces|Future focused \`learn\` refactor' specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/workflows.md AGENTS.md CONSTITUTION.md README.md`
  - `git diff --check HEAD~2..HEAD -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md specs/learn-artifact-model.md specs/learn-artifact-model.test.md docs/proposals/2026-05-03-optimize-learn-skill.md docs/plan.md docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path docs/proposals/2026-05-03-optimize-learn-skill.md --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r1.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r2.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path docs/proposals/2026-05-03-optimize-learn-skill.md --path docs/plan.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r1.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m1-r2.md`
- 2026-05-04: M2 pre-implementation selector regression failed as expected.
  - `python scripts/test-select-validation.py`
- 2026-05-04: M2 selector implementation validation passed.
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path docs/learn/README.md --path docs/learn/sessions/2026-05-04-example.md --path docs/learn/topics/verification.md`
  - `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
- 2026-05-04: M2 review-resolution validation initially failed because the first review record omitted the required `Finding ID:` field for `CR-M2-F1`; the review record was corrected and validation passed.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
- 2026-05-04: M2 review-resolution validation passed after fixing the stale plan outcome and review record format.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m2-r1.md`
  - `git diff --check -- docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
- 2026-05-04: M2 code-review round 2 validation passed.
  - `python scripts/select-validation.py --mode explicit --path docs/learn/README.md --path docs/learn/sessions/2026-05-04-example.md --path docs/learn/topics/verification.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m2-r2.md`
  - `git diff --check -- docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
- 2026-05-04: M2 verification passed for the committed M2 slice.
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path docs/learn/README.md --path docs/learn/sessions/2026-05-04-example.md --path docs/learn/topics/verification.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
  - `git diff --check HEAD~3..HEAD -- scripts/validation_selection.py scripts/test-select-validation.py docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m2-r1.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m2-r2.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/plans/2026-05-04-learn-artifact-model.md`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m2-r1.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m2-r2.md`
- 2026-05-04: M3 pre-implementation skill-validator regression failed as expected.
  - `python scripts/test-skill-validator.py`
- 2026-05-04: M3 implementation validation passed.
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/select-validation.py --mode explicit --path skills/learn/SKILL.md --path docs/learn/README.md --path scripts/test-skill-validator.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `bash scripts/ci.sh --mode explicit --path skills/learn/SKILL.md --path docs/learn/README.md --path scripts/test-skill-validator.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
  - `git diff --check -- skills/learn/SKILL.md docs/learn/README.md scripts/test-skill-validator.py .codex/skills/learn/SKILL.md dist/adapters/claude/.claude/skills/learn/SKILL.md dist/adapters/codex/.agents/skills/learn/SKILL.md dist/adapters/opencode/.opencode/skills/learn/SKILL.md docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
- 2026-05-04: M3 code-review round 1 validation passed.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m3-r1.md`
  - `git diff --check -- docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
- 2026-05-04: M3 verification passed for the committed M3 slice.
  - `rg -n "learn artifact|2026-05-04-learn-artifact-model|Active|Done|Blocked|Superseded" docs/plan.md`
  - `python scripts/select-validation.py --mode explicit --path skills/learn/SKILL.md --path docs/learn/README.md --path scripts/test-skill-validator.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m3-r1.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
  - `git diff --check HEAD~2..HEAD -- skills/learn/SKILL.md docs/learn/README.md scripts/test-skill-validator.py .codex/skills/learn/SKILL.md dist/adapters/claude/.claude/skills/learn/SKILL.md dist/adapters/codex/.agents/skills/learn/SKILL.md dist/adapters/opencode/.opencode/skills/learn/SKILL.md docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model`
  - `bash scripts/ci.sh --mode explicit --path skills/learn/SKILL.md --path docs/learn/README.md --path scripts/test-skill-validator.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m3-r1.md`
- 2026-05-04: M3 review-resolution validation passed after resolving `CR-M3-R2-F1`.
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/select-validation.py --mode explicit --path skills/learn/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m3-r2.md`
  - `bash scripts/ci.sh --mode explicit --path skills/learn/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m3-r2.md --path docs/changes/2026-05-04-learn-artifact-model/review-log.md --path docs/changes/2026-05-04-learn-artifact-model/review-resolution.md`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-04-learn-artifact-model`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model`
  - `git diff --check -- skills/learn/SKILL.md scripts/test-skill-validator.py .codex/skills/learn/SKILL.md dist/adapters/claude/.claude/skills/learn/SKILL.md dist/adapters/codex/.agents/skills/learn/SKILL.md dist/adapters/opencode/.opencode/skills/learn/SKILL.md docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m3-r2.md docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m3-r3.md docs/changes/2026-05-04-learn-artifact-model/review-log.md docs/changes/2026-05-04-learn-artifact-model/review-resolution.md`

## Outcome And Retrospective

- Active. M1-M3 are verified; latest M3 review is `clean-with-notes`; M4 is not started.

## Readiness

M3 is verified as a milestone slice. The full initiative is not branch-ready because M4 final validation and lifecycle closeout remain incomplete.

Stop before M4 unless the user explicitly starts the next milestone. Implementation must keep this plan's progress, decisions, discoveries, and validation notes current as later milestones proceed.
