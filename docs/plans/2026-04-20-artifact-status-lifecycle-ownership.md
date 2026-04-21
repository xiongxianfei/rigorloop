# Artifact status lifecycle ownership plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-20
- Last updated: 2026-04-21
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved artifact-status lifecycle ownership change so top-level workflow artifacts remain trustworthy after review, adoption, supersession, archival, or abandonment.

This initiative is the artifact-wide follow-through to the earlier plan-lifecycle fix. The repository already corrected stale state for execution plans, but proposals, specs, test specs, architecture docs, and ADRs can still drift into misleading states such as `draft`, `reviewed`, `complete`, or `proposed` long after the repository depends on them as settled guidance.

The implementation needs to land as one coherent sequence:

- add a small repo-owned lifecycle validator with deterministic scope modes and fixture coverage;
- update workflow docs, skills, templates, and approved example surfaces so the contract is discoverable without chat history;
- wire the validator into `verify` and CI through the existing script-first pattern; and
- normalize relied-on stale artifact state without rewriting unrelated historical artifacts in bulk.

## Source artifacts

- Proposal: `docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md`
- Spec: `specs/artifact-status-lifecycle-ownership.md`
- Spec-review findings carried into this plan:
  - `reviewed` is a transitional review event, not a durable relied-on state;
  - settlement and closeout are distinct, so `accepted`, `approved`, and `active` remain settled current states rather than closeout states;
  - ADR durable transitions are maintainer, architecture-owner, design-authority, or explicitly delegated actions;
  - first-release executable validation must stay minimal and objective;
  - identifier enforcement applies only to artifact classes whose contracts already define identifiers.
- Architecture: `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md`
- Architecture-review findings carried into this plan:
  - verify scope must be deterministic by explicit mode: `local`, `pr-ci`, `push-main-ci`, and `explicit-paths`;
  - executable enforcement must read from one stable contract registry;
  - examples remain non-normative alignment or fixture surfaces rather than runtime rule sources.
- Related architecture and ADR context:
  - `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
  - `docs/adr/ADR-20260419-repository-source-layout.md`
- Test spec: `specs/artifact-status-lifecycle-ownership.test.md`

## Context and orientation

- The repository already uses repo-owned structural validators and a thin CI wrapper:
  - `scripts/validate-skills.py`
  - `scripts/test-skill-validator.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml`
- The new feature should follow the same pattern:
  - repo-owned Python validation logic in `scripts/`
  - fixture-backed tests under `tests/fixtures/`
  - thin hosted CI wiring that delegates to `scripts/ci.sh`
- Canonical workflow guidance currently lives in:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - canonical skills under `skills/`
  - templates under `specs/feature-template.md` and `specs/feature-template.test.md`
- Generated Codex compatibility output under `.codex/skills/` remains derived. Do not hand-edit it. Use `python scripts/build-skills.py` and `python scripts/build-skills.py --check`.
- In-scope authoritative artifact classes for this feature are:
  - proposals under `docs/proposals/`
  - top-level feature specs under `specs/`
  - test specs under `specs/*.test.md`
  - architecture docs under `docs/architecture/`
  - ADRs under `docs/adr/`
- Baseline gaps identified at planning time:
  - no artifact lifecycle validator existed yet;
  - `specs/feature-template.md` and `specs/feature-template.test.md` still teach outdated status models;
  - historical test specs still advertise `Status: complete`, which the approved spec forbids as a durable state;
  - proposal and architecture lifecycle detail currently relies mostly on skills and approved examples rather than dedicated templates;
  - the approved source proposal, spec, and architecture for this feature initially existed in the worktree as untracked local files;
  - there is no `docs/project-map.md`, but the repository architecture doc and ADR provide enough context for this implementation.
- Two unrelated untracked proposal drafts already exist and are out of scope:
  - `docs/proposals/2026-04-20-docs-changes-usage-policy.md`
  - `docs/proposals/2026-04-20-workflow-stage-handoff-clarity.md`

## Non-goals

- Add a second central lifecycle registry that competes with artifact-local status.
- Build a generalized markdown-schema framework for every document type in v0.1.
- Depend on network calls, GitHub API reads, or branch-name heuristics for verify scope.
- Rewrite every historical proposal, spec, architecture doc, ADR, or test spec in one sweep regardless of whether current work relies on it.
- Redefine the already-approved plan lifecycle model beyond keeping workflow summaries and validators consistent with it.
- Pull unrelated untracked proposal drafts into this initiative.

## Pre-implementation prerequisites

- Before `test-spec` or `implement`, add the accepted proposal, approved spec, and approved architecture for this feature to tracked repository state:
  - `docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md`
  - `specs/artifact-status-lifecycle-ownership.md`
  - `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md`
- Do not let downstream stages rely on those source artifacts while they exist only as untracked local files.
- Create `specs/artifact-status-lifecycle-ownership.test.md` before implementation so the validator, migration, and verify/CI behavior have explicit proof mapping.
- Treat `--mode local` as optional proof only when the working tree has no unrelated changes. Milestone-required validation should use `--mode explicit-paths` or explicit CI diff inputs unless local scope is known to be clean.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R3c`, `R14`, `R14a`, `R14b` | `specs/rigorloop-workflow.md`, `docs/workflows.md`, `CONSTITUTION.md`, `AGENTS.md`, canonical skills, templates, approved example artifacts, generated `.codex/skills/` |
| `R4`-`R10e`, `R12` | `scripts/artifact_lifecycle_contracts.py`, `scripts/artifact_lifecycle_validation.py`, `scripts/validate-artifact-lifecycle.py`, fixture cases, touched proposals/specs/test specs/architecture docs/ADR artifacts |
| `R11`-`R13c` | deterministic scope resolver modes, validator CLI, `scripts/ci.sh`, `.github/workflows/ci.yml`, verify guidance, fixture tests |
| `R15`-`R15b` | migration pass over relied-on stale artifacts, warning-only treatment for unrelated baseline debt, source-artifact normalization during adoption |

## Milestones

### M1. Add the artifact lifecycle validator core and fixture coverage

- Goal:
  - Create the small repo-owned validator subsystem described by the architecture so objective lifecycle defects can be checked deterministically outside CI first.
- Requirements:
  - `R2`, `R4`-`R10e`, `R12`, `R13`, `R13a`, `R13aa`, `R13b`, `R13c`
- Files/components likely touched:
  - `scripts/artifact_lifecycle_contracts.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - new fixtures under `tests/fixtures/artifact-lifecycle/`
- Dependencies:
  - approved spec and architecture
  - tracked source artifacts prerequisite must be satisfied before downstream stages cite this milestone as authoritative repo state
- Tests to add/update:
  - fixture cases for:
    - valid artifact records by class
    - invalid status vocabulary
    - missing required sections or metadata
    - empty required sections
    - placeholder text
    - invalid identifier or naming when the class contract requires it
    - test spec `complete` rejection
    - superseded artifacts missing replacement pointers
    - `Follow-on artifacts` sections that are empty instead of `None yet`
    - generated-source boundary violations
    - objective status versus readiness contradictions
    - related-scope expansion from `docs/changes/<change-id>/change.yaml`
    - related-scope expansion from an explain-change artifact
    - related-scope expansion from the active plan
    - optional draft PR-body references when a draft PR body exists
- Implementation steps:
  - define one executable contract registry entry per in-scope artifact class
  - implement parsing for status, readiness, `Next artifacts`, `Follow-on artifacts`, replacement-pointer metadata, and class-specific identifiers
  - implement the explicit mode contract for `explicit-paths`, `local`, `pr-ci`, and `push-main-ci`
  - implement related-scope expansion from `docs/changes/<change-id>/change.yaml`, explain-change artifacts, the active plan, and optional draft PR text when it exists
  - classify blocking versus warning-only findings based on relatedness
  - add focused fixture-driven tests for pass and fail cases
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md --path docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md`
  - optional when the working tree has no unrelated changes: `python scripts/validate-artifact-lifecycle.py --mode local`
  - `git diff --check -- scripts tests/fixtures`
- Expected observable result:
  - the repository can run a deterministic local artifact-lifecycle check that enforces only objective structural rules and emits blocker versus warning findings
- Commit message: `M1: add artifact lifecycle validator core`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - parser rules may become too broad and misclassify real historical artifacts
  - mode handling may silently guess scope if the CLI contract is not kept strict
- Rollback/recovery:
  - revert the new validator module, CLI, and fixtures together
  - keep only rule definitions that are demonstrably correct if the parser needs redesign

### M2. Align workflow docs, skills, templates, and example surfaces

- Goal:
  - Make the lifecycle contract discoverable from human-facing repo artifacts and keep canonical and generated guidance synchronized.
- Requirements:
  - `R1`-`R3c`, `R6`, `R6a`, `R7`-`R10e`, `R14`, `R14a`, `R14b`
- Files/components likely touched:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `specs/feature-template.md`
  - `specs/feature-template.test.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/workflow/SKILL.md`
  - generated `.codex/skills/`
  - approved example artifacts for proposal and architecture guidance where no dedicated template exists yet
- Dependencies:
  - M1 registry semantics should be stable enough that human guidance mirrors the executable contract instead of diverging from it
- Tests to add/update:
  - the future test spec should cover:
    - the workflow-summary matrix columns and row semantics;
    - settlement versus closeout guidance;
    - per-artifact durable status vocabulary;
    - `verify` block versus warning behavior;
    - generated `.codex/skills/` regeneration and drift checks
- Implementation steps:
  - update `specs/rigorloop-workflow.md` with the compact artifact lifecycle summary matrix required by the approved spec
  - update `docs/workflows.md`, `CONSTITUTION.md`, and `AGENTS.md` where workflow or governance wording changes
  - update feature spec and test-spec templates so they teach the new lifecycle and closeout model
  - update canonical skills for proposal, spec, test-spec, architecture, verify, and workflow behavior
  - use approved example artifacts for proposal and architecture classes as illustrative aligned surfaces rather than adding a second enforcement source
  - regenerate `.codex/skills/` from canonical `skills/`
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n "Settlement states|Closeout or terminal states|Follow-on artifacts|superseded_by|archived|active|reviewed|complete" CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/feature-template.md specs/feature-template.test.md skills .codex/skills`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/feature-template.md specs/feature-template.test.md skills .codex/skills`
- Expected observable result:
  - contributors can discover the artifact lifecycle contract from canonical docs, templates, and skills without relying on chat history, and generated skill output remains in sync
- Commit message: `M2: align artifact lifecycle guidance surfaces`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - templates may grow beyond the minimum contract actually required
  - canonical and generated guidance may drift if regeneration is skipped or incomplete
- Rollback/recovery:
  - revert guidance changes as one unit
  - regenerate `.codex/skills/` after rollback and rerun drift validation

### M3. Integrate deterministic lifecycle validation into verify and CI

- Goal:
  - Run the new validator through the repository’s standard validation path and make mode-specific scope handling explicit in local and hosted verification.
- Requirements:
  - `R11`, `R11a`-`R11e`, `R13`, `R13a`, `R13b`, `R13c`
- Files/components likely touched:
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml`
  - any helper wiring needed to pass explicit CI diff inputs
- Dependencies:
  - M1 validator exists
  - M2 human guidance is stable enough that CI and verify commands match the documented contract
- Tests to add/update:
  - fixture or integration coverage for:
    - missing `pr-ci` base/head inputs failing clearly
    - missing `push-main-ci` before/after inputs failing clearly
    - local mode using repo state without network calls
    - explicit-path mode honoring only the passed paths
    - related-scope expansion from `docs/changes/<change-id>/change.yaml`
    - related-scope expansion from an explain-change artifact
    - related-scope expansion from the active plan
    - optional draft PR-body references when a draft PR body exists
- Implementation steps:
  - wire `scripts/ci.sh` to run the lifecycle validator and its fixture suite alongside existing checks
  - keep `.github/workflows/ci.yml` as a thin wrapper and pass explicit SHA inputs for pull-request and push contexts
  - ensure the validator exits non-zero only on blocking findings and reports unrelated stale baseline artifacts as warnings
  - make the verify and CI path exercise the same related-scope inputs: `docs/changes/<change-id>/change.yaml`, explain-change artifacts, the active plan, and optional draft PR text when present
  - confirm the command shape used by CI matches the command shape contributors will run locally
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md --path docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md`
  - `python scripts/validate-artifact-lifecycle.py --mode pr-ci --base "$(git rev-parse HEAD~1)" --head "$(git rev-parse HEAD)"`
  - `python scripts/validate-artifact-lifecycle.py --mode push-main-ci --before "$(git rev-parse HEAD~1)" --after "$(git rev-parse HEAD)"`
  - `bash scripts/ci.sh`
  - `git diff --check -- scripts/ci.sh .github/workflows/ci.yml scripts`
- Expected observable result:
  - local verify and hosted CI use the same repo-owned lifecycle validator path with explicit scope inputs and clear failure behavior
- Commit message: `M3: wire artifact lifecycle validation into CI`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - CI mode wiring may choose the wrong diff range and over-block unrelated changes
  - warning-only baseline findings may be lost if CI output is too terse
- Rollback/recovery:
  - revert the CI wrapper changes and keep the validator available for explicit local runs
  - preserve deterministic CLI mode behavior even if CI wiring needs a second pass

### M4. Normalize relied-on stale artifacts and closeout metadata

- Goal:
  - Migrate the touched and authoritative artifacts the repository currently relies on so the new validator does not block current work for known stale state.
- Requirements:
  - `R2`, `R6a`, `R7`-`R10e`, `R11`-`R12`, `R15`, `R15a`, `R15b`
- Files/components likely touched:
  - `docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md`
  - `specs/artifact-status-lifecycle-ownership.md`
  - `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md`
  - relied-on historical test specs such as:
    - `specs/rigorloop-workflow.test.md`
    - `specs/constitution-governance-surface.test.md`
    - `specs/plan-index-lifecycle-ownership.test.md`
  - any touched authoritative artifact the validator identifies as stale within the feature’s change scope
- Dependencies:
  - M1-M3 should be in place so migration uses the same validator and human contract that future work will use
- Tests to add/update:
  - the future test spec should cover:
    - migration of `complete` test specs to truthful terminal states;
    - truthful readiness wording for settled current artifacts;
    - `superseded_by` enforcement where replacements exist;
    - warning-only treatment for unrelated stale baseline debt
- Implementation steps:
  - run the lifecycle validator over the local repo and classify blocking versus warning findings
  - normalize the feature’s own accepted proposal, approved spec, and approved architecture as tracked relied-on artifacts
  - reclassify relied-on historical test specs from `complete` to truthful lifecycle states such as `archived`
  - add closeout or `Follow-on artifacts` surfaces only where the approved contract actually requires them
  - leave unrelated stale baseline artifacts outside the changed area as warning-only debt unless the current change must rely on them
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md --path specs/artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path specs/rigorloop-workflow.test.md --path specs/constitution-governance-surface.test.md --path specs/plan-index-lifecycle-ownership.test.md`
  - optional when the working tree has no unrelated changes: `python scripts/validate-artifact-lifecycle.py --mode local`
  - `rg -n '^## Status$|^- (draft|under review|accepted|rejected|abandoned|superseded|archived|approved|active|proposed|deprecated|reviewed|complete)$|^## (Next artifacts|Follow-on artifacts|Readiness)$|^superseded_by:' docs/proposals specs docs/architecture docs/adr`
  - `bash scripts/ci.sh`
  - manual review: confirm touched authoritative artifacts are truthful, and confirm any remaining stale artifacts are unrelated baseline warnings rather than blockers
  - `git diff --check -- docs/proposals specs docs/architecture docs/adr`
- Expected observable result:
  - the repository no longer relies on stale state for the authoritative artifacts touched by this initiative, and unrelated stale baseline debt is explicit instead of silently blocking
- Commit message: `M4: migrate artifact lifecycle state`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - migration may rewrite historical intent instead of adding truthful closeout metadata
  - settled current artifacts may be incorrectly treated as historical closeout cases
- Rollback/recovery:
  - revert the migration slice while preserving any clearly truthful source-artifact status normalization
  - keep unrelated baseline artifacts untouched unless later work specifically adopts them

## Validation plan

- Before implementation, create `specs/artifact-status-lifecycle-ownership.test.md` and map every `MUST` plus the important examples and edge cases to named tests or manual proof surfaces.
- Use milestone-scoped validation first:
  - M1: new validator fixture suite plus explicit-path CLI runs, with local CLI proof only when the working tree is clean
  - M2: workflow/template/skill scans plus skill validation and generated-output drift check
  - M3: explicit CLI mode runs and `bash scripts/ci.sh`
  - M4: targeted explicit-path lifecycle validation plus repository scans, manual artifact truthfulness review, and optional local-mode proof only when the working tree is clean
- Treat manual review as a first-class proof surface for this feature:
  - compare human guidance against the approved spec and architecture
  - compare touched artifacts’ status, readiness, and closeout surfaces
  - confirm unrelated stale baseline artifacts are warnings only
- Before `verify` and `pr`, rerun the repo-owned wrapper:
  - `bash scripts/ci.sh`
- Record the exact commands and artifact-truthfulness evidence in this plan’s `Validation notes` during implementation.

## Risks and recovery

- Risk: the validator becomes broader than the approved v0.1 scope and starts enforcing subjective document quality.
  - Recovery: keep rules limited to the objective defect list in the approved spec and move subjective concerns back to review comments.
- Risk: verify/CI scope classification blocks unrelated repo debt.
  - Recovery: keep explicit mode inputs strict and preserve warning-only treatment for unrelated stale baseline artifacts.
- Risk: migration over-corrects settled current guidance into historical closeout wording.
  - Recovery: preserve the settlement-versus-closeout split and require actual terminal disposition before adding terminal closeout surfaces.
- Risk: human guidance and executable rules drift apart.
  - Recovery: treat the registry as the sole executable rule source, regenerate `.codex/skills/`, and use targeted scans in M2 and M3.

## Dependencies

- Internal:
  - `docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md`
  - `specs/artifact-status-lifecycle-ownership.md`
  - `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md`
  - `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
  - `docs/adr/ADR-20260419-repository-source-layout.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - canonical `skills/`
  - generated `.codex/skills/`
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml`
  - existing fixtures under `tests/fixtures/`
- External:
  - none

## Progress

- [x] M1. Add the artifact lifecycle validator core and fixture coverage
- [x] M2. Align workflow docs, skills, templates, and example surfaces
- [x] M3. Integrate deterministic lifecycle validation into verify and CI
- [ ] M4. Normalize relied-on stale artifacts and closeout metadata
- 2026-04-20: plan created.
- 2026-04-20: planning found that the accepted proposal, approved spec, and approved architecture for this feature remain untracked local files and must be tracked before downstream stages rely on them.
- 2026-04-20: planning confirmed that no `docs/project-map.md` exists; the existing repository architecture doc and ADR remain sufficient context.
- 2026-04-20: planning confirmed that historical test specs still use `Status: complete`, so migration cannot stop at docs-and-validator changes.
- 2026-04-20: created `specs/artifact-status-lifecycle-ownership.test.md` and mapped the approved requirements, examples, and migration cases to validator, manual-review, and CI proof surfaces.
- 2026-04-20: moved the accepted proposal, approved spec, and approved architecture for this feature into tracked git state so downstream stages can rely on repository artifacts instead of untracked local files.
- 2026-04-20: started implementation, normalized `specs/artifact-status-lifecycle-ownership.test.md` from `draft` to `active`, and updated this plan from `draft` to `active`.
- 2026-04-20: completed M1 by adding the artifact lifecycle contract registry, validator helper, CLI entrypoint, and fixture-driven validator tests under `scripts/` and `tests/fixtures/artifact-lifecycle/`.
- 2026-04-21: addressed the first M1 code-review pass by narrowing spec classification to lifecycle-managed behavior contracts, fixing duplicate-ID severity classification, applying stale-readiness checks only to settled or terminal artifacts, and adding `Next artifacts` validation plus regression fixtures.
- 2026-04-21: completed M2 by aligning `specs/rigorloop-workflow.md`, root workflow guidance, feature templates, and the canonical/generated proposal/spec/test-spec/architecture/verify/workflow skills with the settled-versus-terminal artifact lifecycle model.
- 2026-04-21: addressed the M2 code-review findings by fixing the ADR guidance surface to include `Archived` and by updating the approved proposal example to use split settlement-versus-terminal columns plus explicit closeout timing.
- 2026-04-21: expanded the ADR lifecycle contract to the shared lowercase status family requested during implementation: `draft`, `proposed`, `accepted`, `active`, `deprecated`, `superseded`, `archived`, and `abandoned`. This required coordinated updates to the approved spec, workflow guidance, validator contract, fixtures, generated skills, and the relied-on repository-layout ADR.
- 2026-04-21: completed M3 by wiring the artifact lifecycle validator into `scripts/ci.sh` and `.github/workflows/ci.yml`, adding diff-mode regression coverage, and tightening plan-surface reference expansion so CI-mode validation stays deterministic without treating future milestone references as current blockers.
- 2026-04-21: addressed the M3 code-review findings by switching `pr-ci` to merge-base-aware diffs, reading diff-derived scope and baseline artifacts from tracked commit snapshots, and expanding active-plan reference extraction across the whole plan with lifecycle-path filtering.

## Decision log

- 2026-04-20: split implementation into four milestones so validator foundation, human guidance alignment, CI integration, and migration remain independently reviewable. Rationale: each slice has a different proof surface and failure mode.
- 2026-04-20: keep executable lifecycle rules in one stable registry rather than scraping templates, skills, or examples at runtime. Rationale: the approved architecture requires one deterministic enforcement source and makes examples non-normative.
- 2026-04-20: require the feature proposal, spec, and architecture to be tracked before `test-spec` or `implement`. Rationale: later stages should cite tracked repository artifacts rather than untracked local files or chat-only review history.
- 2026-04-20: use skills, workflow docs, existing templates, and approved example artifacts as the human guidance surfaces for proposal, spec, test-spec, architecture, and ADR lifecycle behavior. Rationale: the repository does not yet have dedicated canonical templates for every in-scope artifact class, and the approved design does not require adding them all in this change.
- 2026-04-20: keep the new test spec in `draft` until implementation starts using it as the governing proof surface. Rationale: the approved spec reserves `active` for a test spec that implementation or review is already actively using.
- 2026-04-20: normalize the test spec to `active` once M1 began relying on it as the governing proof surface. Rationale: the approved lifecycle contract treats live implementation use as the transition point from `draft` to `active`.
- 2026-04-20: restrict recursive related-scope reference expansion to `docs/changes/`, `docs/explain/`, `docs/plans/`, and optional draft PR-body input. Rationale: explicit-path validation should stay deterministic and must not pull unrelated repository artifacts into scope from arbitrary Markdown files.
- 2026-04-20: ignore referenced paths that are absent during scope expansion instead of failing the whole run. Rationale: pre-PR handoff surfaces may mention artifacts that are not present in a narrow fixture tree, and missing references are not themselves an approved M1 blocker.
- 2026-04-21: classify top-level `specs/*.md` files as lifecycle-managed behavior specs only when their content matches the contract shape instead of using path alone. Rationale: the `specs/` directory may legitimately contain ordinary documentation such as `README.md`.
- 2026-04-21: build the full artifact identifier index before assigning duplicate-ID severity. Rationale: duplicate groups must block whenever any participant is related to the change, not only when the second-seen artifact happens to be related.
- 2026-04-21: restrict stale-readiness checks to settled or terminal artifact states. Rationale: draft and proposed artifacts can legitimately say they are ready for the next review stage.
- 2026-04-21: parse and validate `Next artifacts` when the section exists. Rationale: M1 claims `R9a` and `R9b` coverage, so the validator must enforce at least the objective non-empty-history rule for preserved planning sections.
- 2026-04-21: keep proposal and architecture example artifacts as illustrative aligned surfaces without adding new dedicated templates in M2. Rationale: the approved examples already model the lifecycle contract well enough for human guidance, and the approved architecture forbids treating examples as a second executable rule source.
- 2026-04-21: update lifecycle semantics in human guidance now, but leave standard validator and CI command wiring to M3. Rationale: M2 owns discoverability across docs, templates, and skills, while M3 owns repo-wide `verify` and `scripts/ci.sh` integration.
- 2026-04-21: keep the ADR guidance review-fix aligned to the approved spec instead of broadening the ADR status contract during M2. Rationale: the approved spec and validator currently allow `Proposed`, `Accepted`, `Superseded`, and `Archived` for ADRs, so the M2 fix should close the guidance gap without introducing a wider unreviewed status model.
- 2026-04-21: broaden the ADR status contract when the user explicitly requested the shared lowercase lifecycle format. Rationale: once that higher-priority direction changed, leaving ADRs on the older mixed-case subset would have kept the canonical skill, workflow docs, validator, and relied-on ADR artifact inconsistent with the requested source of truth.
- 2026-04-21: when `scripts/ci.sh` runs outside hosted CI, use `explicit-paths` over the tracked diff first and fall back to `HEAD~1..HEAD` only when there is no tracked diff. Rationale: local wrapper runs must stay deterministic without pulling unrelated untracked drafts into scope through `local` mode.
- 2026-04-21: compute `pr-ci` changed paths from the merge-base-aware PR diff (`base...head`). Rationale: pull-request validation must follow the current change rather than tree differences introduced by unrelated base-branch advances.
- 2026-04-21: in `pr-ci` and `push-main-ci`, read changed-scope surfaces and baseline artifact discovery from the tracked `head` or `after` snapshot instead of the local filesystem. Rationale: local diff-mode proofs must match hosted CI and must not warn on unrelated untracked drafts.
- 2026-04-21: extract lifecycle and artifact path references from the whole active plan, filtered to lifecycle/reference path patterns, instead of only the `Source artifacts` section. Rationale: active plans can govern authoritative artifacts outside the source-artifact summary, so plan-wide references must stay discoverable without scraping unrelated non-lifecycle docs.
- 2026-04-21: treat changed `.codex/` paths as explicit generated-source blockers only in `explicit-paths` mode, not in diff-derived CI modes. Rationale: PR and push validation must tolerate legitimate generated-output refreshes while still rejecting attempts to validate generated output as authored source of truth directly.

## Surprises and discoveries

- No `docs/project-map.md` exists, but the repository architecture doc and ADR already give enough structural context to plan this feature safely.
- The approved source proposal, spec, and architecture for this feature were still untracked at planning time, which would have made later-stage traceability brittle if not corrected before `test-spec`.
- Historical test specs still advertise `complete`, so the migration scope necessarily includes top-level spec artifacts rather than only workflow docs and validators.
- Proposal and architecture lifecycle guidance currently depends more on skills and approved examples than on dedicated templates, so M2 must treat those surfaces carefully.
- Broad recursive Markdown reference expansion initially pulled unrelated repo docs and generated `.codex/` paths into explicit-path validation. Restricting expansion to the approved scope surfaces restored deterministic relatedness.
- Placeholder detection needed to ignore fenced code blocks and inline code so valid prose examples like `` `TODO` `` in specs and proposals do not become false blockers.
- The `specs/` directory can legitimately contain ordinary documentation as well as lifecycle-managed behavior specs, so spec classification needs content-shape checks instead of path-only matching.
- Duplicate-identifier severity cannot be assigned incrementally without missing the case where a changed artifact collides with an unchanged baseline artifact.
- The existing spec and test-spec templates were far slimmer than the approved lifecycle contract, so M2 needed to expand them materially to teach status normalization, closeout, and readiness patterns instead of only adding a few status bullets.
- The approved proposal example still carried the older single-column lifecycle summary after the first M2 pass, so manual example-surface review has to check terminology drift separately from the workflow spec and skills.
- The ADR status request was larger than a skill-only wording tweak: once lowercase shared ADR statuses were adopted, the approved spec, validator fixtures, generated skills, and the real relied-on ADR all needed to move together or the repository would immediately reintroduce lifecycle drift.
- Diff-derived validation must read tracked commit snapshots rather than the live working tree; otherwise local untracked drafts and unstaged edits leak into PR or push validation in ways hosted CI would never see.
- Active plans can reference authoritative artifacts outside `Source artifacts`, so plan-scope extraction needs whole-plan lifecycle-path filtering rather than a `Source artifacts`-only shortcut or naive unrestricted Markdown scraping.
- Diff-derived validation must distinguish between generated outputs as related surfaces and generated outputs as authored-source inputs; otherwise normal regenerated `.codex/skills/` changes become false blockers in CI.

## Validation notes

- Red state before implementation:
  - `python scripts/test-artifact-lifecycle-validator.py` -> failed with `ModuleNotFoundError: No module named 'artifact_lifecycle_validation'`
- Red state before the M1 review-fix pass:
  - `python scripts/test-artifact-lifecycle-validator.py` -> failed (`3` failures covering spec-doc classification, duplicate-ID severity with a related participant, and missing `Next artifacts` validation)
- Green validation after implementation:
  - `python scripts/test-artifact-lifecycle-validator.py` -> passed (`20` tests)
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md` -> passed (`validated 1 artifact files in explicit-paths mode`)
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md --path docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md` -> passed (`validated 3 artifact files in explicit-paths mode`)
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.test.md` -> passed (`validated 1 artifact files in explicit-paths mode`)
  - `git diff --check -- scripts tests/fixtures` -> passed
- Green validation after the M1 review-fix pass:
  - `python scripts/test-artifact-lifecycle-validator.py` -> passed (`24` tests)
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md` -> passed (`validated 1 artifact files in explicit-paths mode`)
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md --path docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md` -> passed (`validated 3 artifact files in explicit-paths mode`)
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.test.md` -> passed (`validated 1 artifact files in explicit-paths mode`)
  - `git diff --check -- scripts tests/fixtures docs/plans/2026-04-20-artifact-status-lifecycle-ownership.md` -> passed
- Green validation after M2 guidance alignment:
  - `python scripts/validate-skills.py` -> passed (`validated 22 skill files under /home/xiongxianfei/data/20260419-rigorloop/skills`)
  - `python scripts/build-skills.py` -> passed (`synced generated skills from /home/xiongxianfei/data/20260419-rigorloop/skills to /home/xiongxianfei/data/20260419-rigorloop/.codex/skills`)
  - `python scripts/build-skills.py --check` -> passed (`generated skills are in sync under /home/xiongxianfei/data/20260419-rigorloop/.codex/skills`)
  - `rg -n "Settlement states|Closeout or terminal states|Follow-on artifacts|superseded_by|archived|active|reviewed|complete" CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/feature-template.md specs/feature-template.test.md skills .codex/skills` -> passed (`human guidance and generated skills contain the expected lifecycle vocabulary and summary headings`)
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/feature-template.md specs/feature-template.test.md skills .codex/skills` -> passed
- Green validation after the M2 code-review fix:
  - `python scripts/validate-skills.py` -> passed (`validated 22 skill files under /home/xiongxianfei/data/20260419-rigorloop/skills`)
  - `python scripts/build-skills.py` -> passed (`synced generated skills from /home/xiongxianfei/data/20260419-rigorloop/skills to /home/xiongxianfei/data/20260419-rigorloop/.codex/skills`)
  - `python scripts/build-skills.py --check` -> passed (`generated skills are in sync under /home/xiongxianfei/data/20260419-rigorloop/.codex/skills`)
  - `rg -n "Settlement states|Closeout / terminal states|Closeout required when|Follow-on artifacts|superseded_by|archived|Accepted | Proposed | Superseded | Archived" docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md skills/architecture/SKILL.md .codex/skills/architecture/SKILL.md` -> passed (`example and ADR guidance surfaces now expose the expected split terminology and ADR status line`)
  - `git diff --check -- docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md skills/architecture/SKILL.md .codex/skills/architecture/SKILL.md docs/plans/2026-04-20-artifact-status-lifecycle-ownership.md` -> passed
- Green validation after the ADR status-model update:
  - `python scripts/test-artifact-lifecycle-validator.py` -> passed (`26` tests)
  - `python scripts/validate-skills.py` -> passed (`validated 22 skill files under /home/xiongxianfei/data/20260419-rigorloop/skills`)
  - `python scripts/build-skills.py` -> passed (`synced generated skills from /home/xiongxianfei/data/20260419-rigorloop/skills to /home/xiongxianfei/data/20260419-rigorloop/.codex/skills`)
  - `python scripts/build-skills.py --check` -> passed (`generated skills are in sync under /home/xiongxianfei/data/20260419-rigorloop/.codex/skills`)
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md --path docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/adr/ADR-20260419-repository-source-layout.md` -> passed (`validated 4 artifact files in explicit-paths mode`)
  - `rg -n "draft \\| proposed \\| accepted \\| active \\| deprecated \\| superseded \\| archived \\| abandoned|accepted, active|deprecated, superseded, archived, abandoned|draft and proposed are active-work states|accepted and active are settlement states|deprecated, superseded, archived, and abandoned are terminal" specs/artifact-status-lifecycle-ownership.md docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md specs/rigorloop-workflow.md docs/workflows.md CONSTITUTION.md AGENTS.md skills/architecture/SKILL.md skills/workflow/SKILL.md .codex/skills/architecture/SKILL.md .codex/skills/workflow/SKILL.md docs/adr/ADR-20260419-repository-source-layout.md scripts/artifact_lifecycle_contracts.py` -> passed (`shared lowercase ADR statuses and settlement-versus-terminal wording appear across the governing contract, guidance, validator, and relied-on ADR artifact`)
  - `git diff --check -- specs/artifact-status-lifecycle-ownership.md docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md specs/rigorloop-workflow.md docs/workflows.md CONSTITUTION.md AGENTS.md skills .codex/skills scripts/artifact_lifecycle_contracts.py scripts/test-artifact-lifecycle-validator.py tests/fixtures/artifact-lifecycle docs/adr/ADR-20260419-repository-source-layout.md` -> passed
- Green validation after M3 CI integration:
  - `python scripts/test-artifact-lifecycle-validator.py` -> passed (`30` tests including `pr-ci`, `push-main-ci`, plan-scope, and generated-output regressions)
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md --path docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md` -> passed (`validated 2 artifact files in explicit-paths mode`)
  - `python scripts/validate-artifact-lifecycle.py --mode pr-ci --base "$(git rev-parse HEAD~1)" --head "$(git rev-parse HEAD)"` -> passed with warnings only (`validated 7 artifact files in pr-ci mode`; warnings were unrelated stale baseline debt, not blockers)
  - `python scripts/validate-artifact-lifecycle.py --mode push-main-ci --before "$(git rev-parse HEAD~1)" --after "$(git rev-parse HEAD)"` -> passed with warnings only (`validated 7 artifact files in push-main-ci mode`; warnings were unrelated stale baseline debt, not blockers)
  - `bash scripts/ci.sh` -> passed (`scripts/ci.sh` now runs skill validation, skill fixtures, generated-skill drift check, artifact lifecycle validator fixtures, and lifecycle validation using deterministic CI or local fallback inputs`)
  - `git diff --check -- scripts/ci.sh .github/workflows/ci.yml scripts docs/workflows.md docs/plans/2026-04-20-artifact-status-lifecycle-ownership.md` -> passed
- Green validation after the M3 code-review fix:
  - `python scripts/test-artifact-lifecycle-validator.py` -> passed (`32` tests including merge-base PR scope, tracked-only diff-mode baseline discovery, and whole-plan artifact-reference expansion)
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/artifact-status-lifecycle-ownership.md --path docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md` -> passed (`validated 2 artifact files in explicit-paths mode`)
  - `bash scripts/ci.sh` -> passed (`local tracked-diff fallback stayed deterministic after the M3 scope corrections`)
  - `git diff --check -- scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py docs/plans/2026-04-20-artifact-status-lifecycle-ownership.md` -> passed
- Supporting lifecycle bookkeeping validation:
  - `git diff --check -- docs/plan.md docs/plans/2026-04-20-artifact-status-lifecycle-ownership.md specs/artifact-status-lifecycle-ownership.test.md` -> passed
- Optional proof not run:
  - `python scripts/validate-artifact-lifecycle.py --mode local` was intentionally skipped because the working tree contains unrelated untracked proposal drafts, so `local` mode would not have been clean milestone proof.

## Outcome and retrospective

- This plan is still active. Do not mark the initiative `Done`, `Blocked`, or `Superseded` until the real lifecycle decision is known.
- When lifecycle state changes, update both `docs/plan.md` and this plan body in the same change.

## Readiness

- This initiative remains active; M1-M3 are complete.
- The tracked-source-artifact prerequisite is satisfied and the test spec is now active at `specs/artifact-status-lifecycle-ownership.test.md`.
- M3 is ready for `code-review`.
- M1-M3 together satisfy the v0.1 first-enforcement stack of docs, validator, fixtures, `verify`, and CI.
- M4 has not started.
