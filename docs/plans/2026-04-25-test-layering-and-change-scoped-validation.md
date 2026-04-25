# Test layering and change-scoped validation implementation plan

- Status: done
- Owner: maintainer + Codex
- Start date: 2026-04-25
- Last updated: 2026-04-25
- Related issue or PR: none
- Supersedes: none
- broad_smoke_required: true
- broad_smoke_reason: Planned initiative touching validation routing, CI wrapper behavior, workflow guidance, and generated adapter-shipped skills.

## Purpose / big picture

Implement the approved layered validation contract so contributors can get fast, change-scoped proof first without weakening final confidence gates. The change adds a JSON validation selector, makes `scripts/ci.sh` consume selector output instead of owning independent path routing, records broad-smoke trigger sources explicitly, and aligns workflow guidance with targeted proof, broad smoke, and structured manual proof.

The plan preserves the repository value of trustworthy automation. It optimizes validation order, not validation coverage.

## Source artifacts

- Proposal: `docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md`
- Spec: `specs/test-layering-and-change-scoped-validation.md`
- Spec review: approved after SR2 updates; no material findings remain open.
- Architecture: `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md`
- Architecture review: `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/reviews/architecture-review-r1.md` and `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/reviews/architecture-review-r2.md`
- Review resolution: `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md`
- Test spec: `specs/test-layering-and-change-scoped-validation.test.md`
- Existing workflow contract: `specs/rigorloop-workflow.md`
- Existing workflow summary: `docs/workflows.md`
- Project map: none exists. Existing repository layout is small enough for this plan to orient from scripts, specs, docs, skills, schemas, and generated adapter sources.

## Context and orientation

- `scripts/ci.sh` currently runs a fixed broad check set and derives review-artifact and lifecycle validation scope internally.
- The approved architecture moves routing into `scripts/select-validation.py` backed by a shared `scripts/validation_selection.py` module.
- Existing validators remain authoritative for proof execution: skills, generated skills, adapters, review artifacts, change metadata, lifecycle artifacts, and release metadata.
- `scripts/validate-artifact-lifecycle.py` already supports explicit paths and Git range modes.
- `scripts/validate-review-artifacts.py` already supports structure and closeout modes for change-local review records.
- `scripts/validate-change-metadata.py` already validates one or more `change.yaml` files.
- The selector must return JSON with stable check IDs, rationale, affected roots, blocking results, and mode-specific status.
- The architecture decision for v1 is conservative: unclassified paths always block with `unclassified-path`; no fallback set is implemented until a later approved change defines it.
- Broad smoke must remain source-attributed through `broad_smoke.required` and `broad_smoke.sources`, not reduced to a bare flag.
- Normal manual proof belongs in `docs/changes/<change-id>/verify-report.md`; release smoke proof belongs in release metadata. `verify` owns manual-proof closeout validation.
- Canonical skills live under `skills/`; generated `.codex/skills/` and public adapter packages must be regenerated if adapter-shipped skill guidance changes.

## Non-goals

- Reducing required proof for non-trivial changes.
- Replacing full CI, release checks, generated-output drift checks, or manual adapter smoke.
- Creating a dependency graph for arbitrary application/runtime code.
- Selecting tests for app/runtime code that this repository does not contain.
- Replacing human review.
- Requiring every documentation expectation to be machine-enforced in the first implementation slice.
- Requiring ordinary contributors to install Claude Code, OpenCode, or Codex for non-smoke validation.
- Implementing conservative fallback behavior before the fallback check set is explicitly defined by a later approved change.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R2c` | Workflow docs, stage skills, active plan broad-smoke source, and final validation behavior |
| `R3`-`R5t` | `scripts/validation_selection.py`, `scripts/select-validation.py`, JSON contract, exit codes, check catalog, and command substitution |
| `R6`-`R13b` | Selector path classification, affected roots, release version inference, validation-script mappings, and selector self-tests |
| `R14`-`R15b` | V1 `unclassified-path` blocking behavior and future fallback non-execution guard |
| `R16`-`R16d` | `scripts/ci.sh` selector consumption and non-recursive `--mode broad-smoke` |
| `R17`-`R20` | Source-attributed broad-smoke trigger model and planned-initiative broad smoke before final handoff |
| `R21`-`R21n` | `verify` guidance for manual-proof storage, required fields, and closeout behavior |
| `R22`-`R26` | Fixture-driven selector tests, stable check-ID assertions, and actionable wrapper failures |

## Milestones

### M1. Selector core, catalog, and path classification

- Goal:
  - Add the standalone selector command and shared selection module with JSON output, stable check IDs, path classification, broad-smoke trigger attribution, and v1 unclassified-path blocking.
- Requirements:
  - `R3`-`R15b`, `R17c`-`R17g`, `R22`-`R26`
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/select-validation.py`
  - `scripts/test-select-validation.py`
  - `tests/fixtures/validation-selection/` if fixture files are useful
  - `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`
  - this plan
- Dependencies:
  - approved spec and architecture
  - no third-party dependencies
  - no hosted CI changes yet
- Tests to add/update:
  - JSON shape contains required top-level fields and selected-check fields
  - status/exit-code mapping for `ok`, `blocked`, `fallback`, and `error`
  - invalid invocation errors for missing mode-specific inputs
  - local and explicit path selection for `skills/**`
  - generated adapter path selection for `dist/adapters/**`
  - review artifact root selection for `review-log.md`, `review-resolution.md`, and `reviews/**`
  - change metadata selection for one or more `docs/changes/<change-id>/change.yaml` files
  - lifecycle artifact selection for proposal, spec, test-spec, architecture, ADR, and plan paths
  - release metadata version inference from `docs/releases/<version>/**`
  - selector script changes select `selector.regression`
  - validation script changes select matching regression checks where available
  - workflow summaries, `AGENTS.md`, `CONSTITUTION.md`, templates, and schemas are classified or block explicitly
  - unclassified paths return `status: "blocked"` with an `unclassified-path` blocking result and never empty targeted proof
  - broad-smoke source records for mode, explicit flag, active plan, test spec, review-resolution, and release metadata context paths
  - examples assert stable check IDs, not prose categories
- Implementation steps:
  - define catalog data for every v1 check ID and command template
  - define selection request/result dataclasses or equivalent simple structures
  - implement path normalization to repository-relative POSIX paths and reject path traversal
  - implement changed-path resolution for explicit/local paths and Git ranges for PR/main modes
  - implement release mode and release path version inference
  - implement first-slice path classifier and affected-root derivation
  - implement source-attributed `broad_smoke` model and compatibility `broad_smoke_required` boolean
  - implement v1 unclassified blocking and keep `fallback` reserved but non-selected
  - implement CLI parsing, JSON stdout, stderr diagnostics, and exit-code mapping
  - add fixture-driven tests in `scripts/test-select-validation.py`
- Validation commands:
  - `python scripts/test-select-validation.py`
  - Negative-path selector proof: expected blocked selector cases are asserted by `python scripts/test-select-validation.py`; raw blocked selector commands are not milestone pass-gate commands.
  - `python scripts/select-validation.py --mode explicit --path skills/code-review/SKILL.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`
  - `git diff --check -- scripts tests docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md docs/changes/2026-04-25-test-layering-and-change-scoped-validation`
- Expected observable result:
  - contributors can run `python scripts/select-validation.py` and receive deterministic JSON selecting targeted proof for classified paths or an explicit block for unknown paths.
- Commit message: `M1: add validation selector`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - path classification may skip a governed surface if fixtures are incomplete
  - local mode may ignore untracked artifacts if changed-path discovery is too narrow
  - command placeholder substitution may produce a display command that the wrapper cannot execute safely
- Rollback/recovery:
  - revert selector scripts and fixtures while leaving existing explicit validators and broad `scripts/ci.sh` behavior intact
  - if path coverage is incomplete, block unclassified categories until mappings are added

### M2. CI wrapper selector consumption and broad-smoke mode

- Goal:
  - Make `scripts/ci.sh` consume selector output for normal modes, execute selected checks deterministically, and preserve a non-recursive broad-smoke path.
- Requirements:
  - `R3b`, `R3c`, `R4d`-`R4f`, `R5r`, `R16`-`R16d`, `R17`, `R26`
- Files/components likely touched:
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
  - `.github/workflows/ci.yml` if hosted CI needs explicit selector mode inputs
  - this plan
- Dependencies:
  - M1 selector JSON and check catalog
  - existing direct validator commands remain stable
- Tests to add/update:
  - wrapper accepts selector modes and forwards `--path`, `--base`, `--head`, `--release-version`, and `--broad-smoke`
  - wrapper fails on malformed selector JSON
  - wrapper fails on `status: "blocked"` without running partial selected checks
  - wrapper fails on `status: "fallback"` in v1 because no fallback set is defined
  - wrapper executes selected checks in deterministic catalog order
  - wrapper executes root-scoped/path-scoped commands with substituted paths
  - `bash scripts/ci.sh --mode broad-smoke` runs the repository broad-smoke list without recursively selecting `broad_smoke.repo`
  - PR/main mode wrapper examples use the same selector logic with different breadth
- Implementation steps:
  - restructure `scripts/ci.sh` into argument parsing, selector invocation, selected-check execution, and `broad-smoke` functions
  - preserve current broad check list as the non-recursive `--mode broad-smoke` implementation
  - capture selector stdout even for exit codes `2` and `3`
  - validate selector JSON before executing commands
  - execute commands as shell arrays derived from trusted catalog/check context rather than arbitrary `eval`
  - remove independent changed-root routing from `scripts/ci.sh` once selector output owns that scope
  - update hosted CI only if required to pass explicit PR/main SHA inputs
- Validation commands:
  - `python scripts/test-select-validation.py`
  - Negative-path wrapper proof: expected blocked wrapper cases are asserted by `python scripts/test-select-validation.py`; raw blocked wrapper commands are not milestone pass-gate commands.
  - `bash scripts/ci.sh --mode explicit --path specs/test-layering-and-change-scoped-validation.md`
  - `bash scripts/ci.sh --mode broad-smoke`
  - `git diff --check -- scripts .github docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`
- Expected observable result:
  - `scripts/ci.sh` becomes an execution wrapper for selector-selected proof, while `--mode broad-smoke` remains available for final handoff and main/release contexts.
- Commit message: `M2: wire ci wrapper to validation selector`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - shell JSON parsing may be brittle
  - wrapper mode migration may break existing local `bash scripts/ci.sh` habits
  - broad smoke may recurse if `broad_smoke.repo` is not handled as a wrapper-internal mode
- Rollback/recovery:
  - restore the previous broad wrapper path while keeping the selector available for explicit local use
  - if wrapper parsing is fragile, move JSON consumption into a small standard-library Python helper only after updating architecture or plan-review accepts the boundary

### M3. Workflow guidance, manual proof closeout, and generated outputs

- Goal:
  - Align contributor-facing workflow guidance and stage skills with targeted proof, broad-smoke triggers, manual-proof storage, and selector usage; regenerate derived skill/adapters if canonical skills change.
- Requirements:
  - `R1`-`R2c`, `R17`-`R21n`, `R22b`, acceptance criteria for workflow docs and affected stage skills
- Files/components likely touched:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md` or `AGENTS.md` only if their summaries become stale
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/workflow/SKILL.md` if stage routing summary needs alignment
  - `.codex/skills/`
  - `dist/adapters/`
  - `dist/adapters/manifest.yaml`
  - this plan and change-local artifacts
- Dependencies:
  - M1 selector command and JSON contract
  - M2 wrapper behavior
  - generated adapter target remains `0.1.1`
- Tests to add/update:
  - skill validation accepts updated canonical skill guidance
  - generated skill drift check catches stale `.codex/skills/`
  - adapter drift and validation catch stale public adapter output after shipped skill changes
  - docs/skills alignment checks use stable check IDs and do not imply broad smoke for every PR
  - `verify` guidance requires `verify-report.md` for manual proof and release metadata for release smoke
  - `implement` and `code-review` guidance request targeted proof before broad smoke
  - `pr` guidance does not duplicate detailed review findings in PR body
- Implementation steps:
  - update workflow docs to introduce selector usage, targeted proof, broad-smoke triggers, and manual proof record ownership
  - update stage skills to request selector-selected targeted proof and source-attributed broad-smoke evidence
  - update `verify` guidance to own manual-proof closeout validation using `verify-report.md` or release metadata
  - keep broad smoke required before final handoff for this planned initiative
  - regenerate `.codex/skills/` through `python scripts/build-skills.py`
  - regenerate public adapter packages through `python scripts/build-adapters.py --version 0.1.1` if adapter-shipped skills changed
  - do not hand-edit generated output
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `rg -n "select-validation|targeted proof|broad smoke|manual by design|verify-report.md|broad_smoke" specs/rigorloop-workflow.md docs/workflows.md skills .codex/skills dist/adapters`
  - `git diff --check -- specs docs skills .codex/skills dist AGENTS.md CONSTITUTION.md`
- Expected observable result:
  - contributors and agents see the same selector, targeted-proof, broad-smoke, and manual-proof contract in workflow docs and shipped skill guidance.
- Commit message: `M3: align validation selector workflow guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - docs may overclaim selector coverage before `ci.sh` consumes it
  - canonical skill wording may introduce tool-specific assumptions that adapter validation rejects
  - generated output may drift if regeneration is skipped
- Rollback/recovery:
  - revert canonical docs and skill guidance, then regenerate `.codex/skills/` and public adapters from the reverted sources
  - if a skill becomes non-portable, rewrite the tool-specific language rather than weakening adapter validation

### M4. Integration closeout and final validation

- Goal:
  - Complete integration proof, update lifecycle state, and prepare the change for `code-review`, `verify`, `explain-change`, and `pr`.
- Requirements:
  - all in-scope requirements, plus repository lifecycle closeout rules for planned initiatives
- Files/components likely touched:
  - `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`
  - `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/verify-report.md` if manual proof or final broad-smoke proof needs a standalone record
  - `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/explain-change.md` during later `explain-change`
  - `docs/plan.md`
  - this plan
- Dependencies:
  - M1-M3 complete
  - plan-review approved
  - matching test spec active
- Tests to add/update:
  - final selector tests cover every first-slice category
  - final wrapper proof demonstrates selected targeted checks and non-recursive broad smoke
  - final lifecycle validation covers touched top-level artifacts and active plan state
  - review-artifact closeout remains valid
- Implementation steps:
  - run all targeted checks selected for the final changed surfaces
  - run `bash scripts/ci.sh --mode broad-smoke` because the active plan records `broad_smoke_required: true`
  - update change metadata validation records with actual commands run
  - keep this plan's progress and validation notes current
  - when implementation is complete, update both `docs/plan.md` and this plan body consistently
  - leave `review-resolution.md` closed unless a later review creates new material findings
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh`
  - `bash scripts/ci.sh --mode broad-smoke`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.test.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`
  - `git diff --check -- .`
- Expected observable result:
  - the branch has targeted proof, broad-smoke proof for the planned initiative, closed review-resolution state, and synchronized lifecycle state.
- Commit message: `M4: close validation selector integration`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] broad smoke passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - broad smoke may reveal stale generated output from earlier milestones
  - final lifecycle validation may catch stale readiness wording in touched artifacts
  - new review findings may reopen `review-resolution.md`
- Rollback/recovery:
  - use selector-targeted checks to identify the failing surface, fix it, then rerun broad smoke
  - if CI wrapper integration must be deferred, revert M2 while keeping selector CLI and docs honest about adoption status

## Validation plan

- Before `plan-review`: validate artifact lifecycle, change metadata, and review artifact closeout for the planning artifacts.
- Before implementation: create and activate `specs/test-layering-and-change-scoped-validation.test.md`.
- Before `code-review`: run selector-targeted proof for the touched milestone surfaces and record exact commands.
- Before final `verify`: run broad smoke because this planned initiative records `broad_smoke_required: true`.
- Before `pr`: run review-artifact closeout validation if any material findings exist and ensure `docs/plan.md` and this plan body agree on lifecycle state.

## Risks and recovery

- Risk: the selector optimizes too aggressively and skips proof.
- Recovery: v1 unknown paths block; add explicit mappings and tests before allowing automatic proof.
- Risk: `scripts/ci.sh` becomes a second selector.
- Recovery: keep the check catalog and path classification in `scripts/validation_selection.py`; wrapper logic only executes selected checks.
- Risk: broad-smoke triggers lose source attribution.
- Recovery: require `broad_smoke.sources` entries in selector output and preserve handoff-stage trigger evidence.
- Risk: manual proof records remain unstructured.
- Recovery: make `verify` require the manual-proof table in `verify-report.md` for normal changes and release metadata for release smoke.
- Risk: generated adapter outputs drift after skill guidance changes.
- Recovery: regenerate from canonical skills and run adapter drift and validation checks.

## Dependencies

- `plan-review` must approve this plan before implementation.
- `specs/test-layering-and-change-scoped-validation.test.md` must be created and active before implementation.
- M2 depends on M1 selector JSON and check catalog.
- M3 depends on M1/M2 so docs and skills describe real selector and wrapper behavior.
- M4 depends on all implementation milestones and broad-smoke availability.
- No networked services, third-party packages, or local Claude Code/OpenCode/Codex installs are required for non-smoke validation.

## Progress

- [x] 2026-04-25: proposal accepted.
- [x] 2026-04-25: spec approved after spec-review updates.
- [x] 2026-04-25: architecture approved by `architecture-review-r2`.
- [x] 2026-04-25: execution plan created and indexed.
- [x] 2026-04-25: plan-review approved after resolving `PR1-F1`.
- [x] 2026-04-25: test spec active.
- [x] 2026-04-25: M1 complete. Selector core, catalog, CLI, path classification, broad-smoke source attribution, and selector regression tests are implemented.
- [x] 2026-04-25: M1 code-review fixes implemented for `CR1-F1` and `CR1-F2`; `code-review-r2` returned `clean-with-notes`.
- [x] 2026-04-25: M2 implemented. `scripts/ci.sh` now consumes selector JSON for normal modes, executes trusted catalog commands, preserves non-recursive `--mode broad-smoke`, and hosted CI passes PR/main ranges through the wrapper.
- [x] 2026-04-25: M2 code-review complete. `code-review-r3` found missing direct proof for tampered selector command rejection; `CR3-F1` was fixed with a focused wrapper regression and `code-review-r4` returned `clean-with-notes`.
- [x] 2026-04-25: M3 implemented. Workflow docs and affected stage skills now describe selector-selected targeted proof, triggered broad smoke, stable check IDs, and manual-proof ownership; generated `.codex/skills/` and public adapter skill outputs were regenerated from canonical skills.
- [x] 2026-04-25: M3 code-review complete. `code-review-r5` returned `clean-with-notes`.
- [x] 2026-04-25: M4 implemented. Selector-selected targeted proof, wrapper execution proof, planned broad smoke, review closeout validation, change metadata validation, lifecycle validation, and whitespace validation passed.
- [x] 2026-04-25: M4 code-review complete. `code-review-r6` returned `clean-with-notes`.
- [x] 2026-04-25: Verify passed. Classified review/change/plan surfaces passed through `scripts/ci.sh`, `docs/plan.md` was manually routed through lifecycle validation after the selector returned the expected v1 `unclassified-path` block, and planned broad smoke passed.
- [x] 2026-04-25: Explain-change completed at `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/explain-change.md`.
- [x] 2026-04-25: PR handoff prepared. Lifecycle state is closed in the plan body and `docs/plan.md`; review-resolution remains closed with no open findings.
- [x] 2026-04-25: Hosted PR CI coverage gap fixed. The selector now maps PR-handoff governance surfaces such as `.github/workflows/ci.yml`, `docs/workflows.md`, `docs/plan.md`, and change-local `explain-change.md` to deterministic checks instead of blocking PR mode; plan-index and change-local lifecycle routing include related change metadata so lifecycle validation is not a no-op.

## Decision log

- 2026-04-25: Use `scripts/select-validation.py` as a standalone selector and `scripts/validation_selection.py` as the shared implementation module. Rationale: one testable source of truth for local, PR, main, release, and future tooling.
- 2026-04-25: Keep `scripts/ci.sh` as the wrapper, not the selector. Rationale: shell remains orchestration while path classification and check selection are tested in Python.
- 2026-04-25: Record `broad_smoke.required` and `broad_smoke.sources` rather than relying on a bare flag. Rationale: broad-smoke requirements must be traceable to authoritative sources.
- 2026-04-25: Block unclassified paths in v1 with `unclassified-path`; do not implement fallback. Rationale: no deterministic conservative fallback set has been approved.
- 2026-04-25: Store normal manual proof in `verify-report.md` and release smoke proof in release metadata; make `verify` own closeout. Rationale: manual proof is handoff evidence, not selector state.
- 2026-04-25: Keep `scripts/ci.sh` unchanged in M1. Rationale: wrapper selector consumption is explicitly owned by M2, while M1 only provides the selector contract and regression surface.
- 2026-04-25: Use `0.1.1` as the M1 default adapter version for selector command substitution. Rationale: the active plan records generated adapter target `0.1.1`, and a later release-contract change can centralize that default.
- 2026-04-25: Treat direct files under `docs/releases/` as ambiguous release paths. Rationale: only paths nested under `docs/releases/<version>/...` may infer a release version, and v1 blocks ambiguous release paths instead of guessing.
- 2026-04-25: Keep no-argument `bash scripts/ci.sh` as legacy broad smoke while adding explicit `--mode` routing. Rationale: existing contributors and docs still rely on the stable wrapper command, while targeted proof uses explicit modes.
- 2026-04-25: Route `scripts/ci.sh` changes to `selector.regression`. Rationale: `python scripts/test-select-validation.py` now owns wrapper regression coverage as well as selector regression coverage.
- 2026-04-25: Do not create `verify-report.md` during M4. Rationale: M4 used automated selector, wrapper, broad-smoke, review-artifact, change-metadata, lifecycle, and whitespace proof only; no manual proof check was required.

## Surprises and discoveries

- M1: The selector can prove wrapper-blocking expectations only through the regression harness until M2 wires `scripts/ci.sh` to selector output.
- M1 code-review: `CR1-F1` found that direct `docs/releases/release-notes.md` paths were incorrectly accepted as release version `release-notes.md`; `CR1-F2` found missing direct proof for valid PR/main modes and representative first-slice categories.
- M2: `scripts/ci.sh` needed a selector classification so wrapper changes select the wrapper regression test surface instead of falling into manual routing.
- M2 code-review: `CR3-F1` showed that implemented catalog validation still needed direct security proof against tampered selector JSON command text.
- M3: A compact source-guidance alignment test was more useful than prose greps across generated output; generated-output drift checks prove `.codex/skills/` and `dist/adapters/` stayed synchronized after canonical skill changes.
- M3: `skills/pr/SKILL.md` remained unchanged because existing PR guidance already keeps review-resolution details to counts and a `review-resolution.md` link, and `scripts/test-review-artifact-validator.py` continues to assert that contract.

## Validation notes

- 2026-04-25: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation` passed after `architecture-review-r2`.
- 2026-04-25: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml` passed.
- 2026-04-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml` passed.
- 2026-04-25: `git diff --check -- docs/plan.md docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md specs/test-layering-and-change-scoped-validation.md docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-log.md docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md docs/changes/2026-04-25-test-layering-and-change-scoped-validation/reviews/architecture-review-r1.md docs/changes/2026-04-25-test-layering-and-change-scoped-validation/reviews/architecture-review-r2.md` passed.
- 2026-04-25: `plan-review-r1` found `PR1-F1`; the plan now routes negative-path selector and wrapper proof through `python scripts/test-select-validation.py` instead of raw expected-failure pass-gate commands.
- 2026-04-25: `plan-review-r2` approved the revised plan; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation` passed.
- 2026-04-25: `specs/test-layering-and-change-scoped-validation.test.md` was created as the active proof plan before implementation.
- 2026-04-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-layering-and-change-scoped-validation.test.md --path specs/test-layering-and-change-scoped-validation.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml` passed.
- 2026-04-25: M1 red check: `python scripts/test-select-validation.py` failed with `ModuleNotFoundError: No module named 'validation_selection'` before selector implementation existed.
- 2026-04-25: M1 focused selector proof passed: `python scripts/test-select-validation.py`.
- 2026-04-25: M1 classified-path smoke passed: `python scripts/select-validation.py --mode explicit --path skills/code-review/SKILL.md`.
- 2026-04-25: M1 change metadata validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M1 lifecycle validation passed: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M1 whitespace validation passed: `git diff --check -- scripts tests docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: M1 review-driven red check passed as expected before the production fix: `python scripts/test-select-validation.py` failed only on `test_release_path_without_version_directory_blocks` because the selector returned exit `0` instead of expected exit `2`.
- 2026-04-25: M1 review-driven selector regression passed after the release inference fix: `python scripts/test-select-validation.py` ran 16 tests and passed.
- 2026-04-25: M1 ambiguous release path probe returned the required block: `python scripts/select-validation.py --mode explicit --path docs/releases/release-notes.md` emitted `status: "blocked"`, `release-version-required`, and exit `2`.
- 2026-04-25: M1 review artifact structure validation passed after resolving `CR1-F1` and `CR1-F2`: `python scripts/validate-review-artifacts.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: M1 same-stage re-review completed: `code-review-r2` returned `clean-with-notes` and closed out `code-review-r1`.
- 2026-04-25: M1 review artifact closeout validation passed after `code-review-r2`: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: M1 change metadata validation passed after review-driven updates: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M1 lifecycle validation passed after review-driven updates: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.test.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M1 whitespace validation passed after review-driven updates: `git diff --check -- scripts docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: M2 red check: `python scripts/test-select-validation.py` failed against the old wrapper because `scripts/ci.sh` ignored `--mode` and ran the broad check list instead of selector-selected proof.
- 2026-04-25: M2 wrapper regression passed: `python scripts/test-select-validation.py` ran 23 tests and passed.
- 2026-04-25: M2 targeted wrapper proof passed: `bash scripts/ci.sh --mode explicit --path specs/test-layering-and-change-scoped-validation.md`.
- 2026-04-25: M2 wrapper self-routing proof passed: `bash scripts/ci.sh --mode explicit --path scripts/ci.sh`.
- 2026-04-25: M2 broad smoke passed: `bash scripts/ci.sh --mode broad-smoke`.
- 2026-04-25: M2 whitespace validation passed: `git diff --check -- scripts .github docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`.
- 2026-04-25: M2 code-review first pass `code-review-r3` found `CR3-F1`, missing direct proof that selector JSON command text cannot bypass trusted catalog command execution.
- 2026-04-25: M2 review-driven wrapper regression passed after the `CR3-F1` fix: `python scripts/test-select-validation.py` ran 24 tests and passed.
- 2026-04-25: M2 review-driven targeted wrapper proof passed: `bash scripts/ci.sh --mode explicit --path specs/test-layering-and-change-scoped-validation.md`.
- 2026-04-25: M2 review-driven wrapper self-routing proof passed: `bash scripts/ci.sh --mode explicit --path scripts/ci.sh`.
- 2026-04-25: M2 review-driven broad smoke passed: `bash scripts/ci.sh --mode broad-smoke`.
- 2026-04-25: M2 same-stage re-review completed: `code-review-r4` returned `clean-with-notes` and closed out `code-review-r3`.
- 2026-04-25: M2 review artifact closeout validation passed after `code-review-r4`: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: M2 change metadata validation passed after review closeout updates: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M2 lifecycle validation passed after review closeout updates: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M2 whitespace validation passed after review closeout updates: `git diff --check -- scripts .github docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: M3 red check: `python scripts/test-select-validation.py` failed on `test_workflow_guidance_aligns_with_validation_layering_contract` because workflow docs and stage skills did not yet name selector-selected targeted proof, broad smoke triggers, stable check IDs, and manual-proof ownership.
- 2026-04-25: M3 guidance alignment test passed after canonical docs and skill updates: `python scripts/test-select-validation.py` ran 25 tests and passed.
- 2026-04-25: M3 skill validation passed: `python scripts/validate-skills.py`.
- 2026-04-25: M3 skill validator fixtures passed: `python scripts/test-skill-validator.py`.
- 2026-04-25: M3 generated skill mirror refreshed: `python scripts/build-skills.py`.
- 2026-04-25: M3 generated skill drift check passed: `python scripts/build-skills.py --check`.
- 2026-04-25: M3 public adapter packages regenerated: `python scripts/build-adapters.py --version 0.1.1`.
- 2026-04-25: M3 adapter distribution fixtures passed: `python scripts/test-adapter-distribution.py`.
- 2026-04-25: M3 generated adapter drift check passed: `python scripts/build-adapters.py --version 0.1.1 --check`.
- 2026-04-25: M3 generated adapter validation passed: `python scripts/validate-adapters.py --version 0.1.1`.
- 2026-04-25: M3 guidance search proof passed: `rg -n "select-validation|targeted proof|broad smoke|manual by design|verify-report.md|broad_smoke" specs/rigorloop-workflow.md docs/workflows.md skills .codex/skills dist/adapters`.
- 2026-04-25: M3 change metadata validation passed after M3 updates: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M3 lifecycle validation passed after M3 updates: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-workflow.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M3 whitespace validation passed after M3 updates: `git diff --check -- specs docs skills .codex/skills dist scripts AGENTS.md CONSTITUTION.md`.
- 2026-04-25: M3 code-review completed: `code-review-r5` returned `clean-with-notes`.
- 2026-04-25: M3 review artifact closeout validation passed after `code-review-r5`: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: M3 change metadata validation passed after review closeout updates: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M3 lifecycle validation passed after review closeout updates: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-workflow.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M3 whitespace validation passed after review closeout updates: `git diff --check -- docs/changes/2026-04-25-test-layering-and-change-scoped-validation docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`.
- 2026-04-25: M4 selector inspection passed: `python scripts/select-validation.py --mode explicit --path scripts/select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh` returned `status: "ok"` and selected `selector.regression`.
- 2026-04-25: M4 targeted selector regression passed: `python scripts/test-select-validation.py` ran 25 tests and passed.
- 2026-04-25: M4 targeted wrapper proof passed: `bash scripts/ci.sh --mode explicit --path scripts/select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh`.
- 2026-04-25: M4 planned broad smoke passed: `bash scripts/ci.sh --mode broad-smoke`. The command emitted only pre-existing unrelated lifecycle warnings for `docs/proposals/2026-04-19-rigorloop-workflow-product.explore.md`.
- 2026-04-25: M4 review artifact closeout validation passed: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: M4 change metadata validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M4 lifecycle validation passed: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.test.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M4 whitespace validation passed: `git diff --check -- .`.
- 2026-04-25: M4 code-review completed: `code-review-r6` returned `clean-with-notes`.
- 2026-04-25: M4 review artifact closeout validation passed after `code-review-r6`: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: M4 change metadata validation passed after review closeout updates: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: M4 lifecycle validation passed after review closeout updates: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: Verify selector inspection found expected manual routing for `docs/plan.md`: `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-log.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/reviews/code-review-r6.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/plan.md` returned `status: "blocked"` with `unclassified-path` for `docs/plan.md`, while classified paths selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `broad_smoke.repo`.
- 2026-04-25: Verify manual-routing lifecycle proof for `docs/plan.md` passed: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: Verify full authoritative lifecycle proof passed: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.test.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/plan.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: Verify wrapper proof passed for classified review/change/plan surfaces: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-log.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/reviews/code-review-r6.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`. The active-plan trigger selected and passed `broad_smoke.repo`; only unrelated baseline lifecycle warnings were emitted for older proposal artifacts.
- 2026-04-25: Explain-change change metadata validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: Explain-change lifecycle validation passed: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/explain-change.md --path docs/plan.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: PR handoff change metadata validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: PR handoff lifecycle validation passed: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/explain-change.md --path docs/plan.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`.
- 2026-04-25: PR handoff review closeout validation passed: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation`.
- 2026-04-25: Hosted PR CI first run failed because PR mode blocked `.github/workflows/ci.yml`, `docs/workflows.md`, `docs/plan.md`, and change-local `explain-change.md`; this exposed a selector first-slice coverage gap.
- 2026-04-25: PR CI gap selector regression passed after the fix: `python scripts/test-select-validation.py` ran 26 tests and passed.
- 2026-04-25: PR CI gap targeted wrapper proof passed after the fix: `bash scripts/ci.sh --mode explicit --path .github/workflows/ci.yml --path docs/workflows.md --path docs/plan.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/explain-change.md --path scripts/validation_selection.py --path scripts/test-select-validation.py`. The lifecycle command included `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml` and validated 5 artifacts.

## Outcome and retrospective

- Done. M1, M2, M3, M4, code-review, verify, and explain-change are complete; the change is ready for PR handoff.

## Readiness

- Immediate next repository stage: `pr`.
- Next implementation milestone: none.

## Risks and follow-ups

- Follow-up: after implementation, decide whether a later spec should define a real conservative fallback set for `fallback` status.
- Follow-up: if selector adoption exposes repeated manual routing for governance files, add explicit category mappings rather than weakening unclassified-path blocking.
