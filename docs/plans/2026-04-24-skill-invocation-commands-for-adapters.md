# Skill invocation commands for adapter packages plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-24
- Last updated: 2026-04-24
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved `v0.1.1` adapter usability contract as a small patch release. The work should keep RigorLoop skills authored once, add a generated OpenCode command alias layer for the curated lifecycle command set, document native skill invocation for Claude Code and OpenCode, and preserve deterministic validation for generated adapter packages.

This plan starts after the proposal, spec, and architecture are settled. It does not change workflow semantics or canonical skill behavior.

## Source artifacts

- Proposal: `docs/proposals/2026-04-24-skill-invocation-commands-for-adapters.md`
- Spec: `specs/skill-invocation-commands-for-adapters.md`
- Spec review: complete; spec status is `approved`.
- Architecture: `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md`
- Architecture review: complete; architecture status is `approved`.
- Existing adapter architecture: `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md`
- Existing adapter ADR: `docs/adr/ADR-20260424-generated-adapter-packages.md`
- Test spec: `specs/skill-invocation-commands-for-adapters.test.md`
- Project map: none exists. Existing source layout is small enough for this plan to orient from scripts, docs, specs, and architecture.

## Context and orientation

- Canonical skills live under `skills/<skill-name>/SKILL.md`.
- Generated public adapter packages live under `dist/adapters/` and must not be hand-edited.
- Existing generated local Codex runtime output lives under `.codex/skills/` and is unrelated to OpenCode command aliases.
- `scripts/adapter_distribution.py` owns adapter configuration, manifest rendering/parsing, expected generated file maps, drift checks, adapter validation, release target support, release metadata validation, and security scans.
- `scripts/build-adapters.py` generates or checks `dist/adapters/`.
- `scripts/validate-adapters.py` validates generated package structure, manifest consistency, and generated-output security.
- `scripts/test-adapter-distribution.py` is the fixture-driven test surface for adapter generation, manifest parsing, validation, release metadata, and security edge cases.
- `scripts/release-verify.sh` currently supports `v0.1.0-rc.1` and `v0.1.0`; this feature requires `v0.1.1`.
- `scripts/adapter_templates/claude/CLAUDE.md` and `scripts/adapter_templates/opencode/AGENTS.md` are the authored thin entrypoint templates for user-facing invocation guidance.
- `README.md` is the public quick-start surface and must distinguish Claude Code native slash-skill usage from generated OpenCode command aliases.

## Non-goals

- Change canonical RigorLoop skill behavior.
- Add OpenCode command aliases for every portable skill.
- Add OpenCode aliases for `workflow`, `verify`, `explore`, `research`, `architecture`, `architecture-review`, `ci`, `explain-change`, `learn`, `project-map`, or `constitution`.
- Generate `.claude/commands/` wrappers for RigorLoop skills.
- Change Codex invocation behavior.
- Add marketplace, plugin, package-manager, or installer distribution.
- Add default OpenCode or Claude Code permissions, model settings, agent settings, or approval behavior.
- Document one-shot CLI forms that are not smoke-tested for the release.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R3` | Preserve canonical `skills/`, existing OpenCode `.opencode/skills/` generation, and generated-output ownership boundaries. |
| `R4`-`R14` | Curated OpenCode command alias set, deterministic thin wrapper rendering, and generated command files. |
| `R15`-`R18`, `R23`-`R27`, `R47` | Adapter drift checks, adapter validation, path/key consistency, unexpected alias rejection, and actionable error messages. |
| `R19`-`R22` | Extended `dist/adapters/manifest.yaml` `command_aliases.opencode` shape. |
| `R28`-`R39` | Claude/OpenCode entrypoint guidance and public README usage examples. |
| `R40`-`R44`, `R48` | `v0.1.1` release target support, release metadata, release notes, and command-alias smoke evidence validation. |
| `R45`-`R46` | Patch-level compatibility and non-smoke validation without requiring local Claude Code or OpenCode installs. |

## Milestones

### M1. Generate and validate OpenCode command aliases

- Goal:
  - Add deterministic OpenCode command alias generation, extended manifest metadata, drift checks, and adapter validation.
- Requirements:
  - `R1`-`R27`, `R46`-`R47`
- Files/components likely touched:
  - `scripts/adapter_distribution.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - `tests/fixtures/adapters/`
  - generated `dist/adapters/manifest.yaml`
  - generated `dist/adapters/opencode/.opencode/commands/`
- Dependencies:
  - approved spec and architecture
  - existing adapter distribution tests and generation helpers
  - no dependency on real OpenCode or Claude Code installations for non-smoke validation
- Tests to add/update:
  - generation test that produces exactly the 10 curated OpenCode aliases
  - generation test proving no aliases for `workflow`, `verify`, or other non-curated skills
  - manifest rendering/parsing test for `command_aliases.opencode.count` and exact alias paths
  - validation test for missing declared alias
  - validation test for unexpected extra alias
  - validation test for alias outside the curated set
  - validation test for alias whose manifest key and filename stem disagree
  - validation test for alias path outside `dist/adapters/opencode/.opencode/commands/`
  - validation test for alias that maps to a missing OpenCode skill
  - validation test for stale or unsafe alias body
  - validation test that `.claude/commands/` wrappers are not generated
- Implementation steps:
  - add a single `OPENCODE_COMMAND_ALIASES` tuple in `scripts/adapter_distribution.py`
  - add command-alias rendering that produces a thin prompt wrapper using `$ARGUMENTS`
  - include generated OpenCode command aliases in `expected_adapter_files(...)`
  - extend manifest rendering to include `command_aliases.opencode`
  - extend manifest parsing with a constrained command alias model
  - extend adapter validation to compare manifest-declared aliases against generated command files
  - extend security validation for command alias body constraints
  - regenerate `dist/adapters/` with version `0.1.1`
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `git diff --check -- scripts tests dist docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`
- Expected observable result:
  - `dist/adapters/opencode/.opencode/commands/` contains exactly the curated aliases, `dist/adapters/manifest.yaml` records exact paths, and repository-owned validation fails on alias drift or mismatch.
- Commit message: `M1: add opencode command alias generation`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - manifest parsing may become too broad if the command alias shape is not kept constrained
  - validation may only prove file existence unless it also checks deterministic body content
  - generated output may be hand-edited accidentally
- Rollback/recovery:
  - revert command alias generation, manifest extension, tests, and generated command files without touching canonical skills
  - rerun `python scripts/build-adapters.py --version 0.1.1` rather than hand-editing generated adapter output

### M2. Add tool-native invocation documentation

- Goal:
  - Update public docs and generated entrypoints so users know how to invoke skills in Claude Code and OpenCode without assuming cross-tool syntax parity.
- Requirements:
  - `R28`-`R39`
- Files/components likely touched:
  - `scripts/adapter_templates/claude/CLAUDE.md`
  - `scripts/adapter_templates/opencode/AGENTS.md`
  - `README.md`
  - generated `dist/adapters/claude/CLAUDE.md`
  - generated `dist/adapters/opencode/AGENTS.md`
  - `scripts/test-adapter-distribution.py`
- Dependencies:
  - M1 command aliases and manifest output
  - spec requirement that Claude Code stays skill-native
- Tests to add/update:
  - entrypoint test proving Claude examples use native `/skill-name` and no `.claude/commands/`
  - entrypoint test proving OpenCode docs describe `.opencode/skills/` as primary and `.opencode/commands/` as thin aliases
  - README/doc assertion for TUI slash-command examples
  - README/doc assertion that OpenCode examples do not claim aliases outside the curated set
  - README/doc assertion that one-shot examples are absent until M3 smoke evidence exists
  - README/doc assertion that Codex `$skill` syntax is not implied for Claude Code or OpenCode
- Implementation steps:
  - add "Using RigorLoop skills" guidance to Claude Code and OpenCode entrypoint templates
  - document Claude Code native `/skill-name` usage without one-shot examples unless smoke evidence exists
  - document OpenCode TUI aliases for the curated lifecycle set
  - document OpenCode `.opencode/skills/` availability for non-aliased portable skills
  - add README adapter usage examples for Claude Code and OpenCode
  - keep M2 documentation limited to README and generated adapter entrypoints; do not create or update `docs/releases/v0.1.1/release-notes.md` in this milestone
  - prohibit `opencode run --command ...` one-shot examples in README and entrypoints until M3 records passing smoke evidence for that exact form
  - regenerate adapter output after template changes
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `rg -n '/proposal|/spec|/implement|/code-review|opencode run --command|\\.opencode/commands|\\.opencode/skills|\\.claude/commands|\\$skill' README.md scripts/adapter_templates dist/adapters`
  - `git diff --check -- README.md scripts/adapter_templates dist docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`
- Expected observable result:
  - users can read README or generated entrypoints and understand Claude Code slash-skill invocation, OpenCode curated command aliases, and the limits of one-shot examples.
- Commit message: `M2: document adapter skill invocation`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - docs may overclaim one-shot support before smoke is complete
  - users may infer aliases exist for every skill
  - examples may confuse Claude Code native slash skills with OpenCode generated aliases
- Rollback/recovery:
  - revert template and README edits, regenerate adapter output, and leave command aliases undocumented until smoke evidence is ready

### M3. Add `v0.1.1` release verification and smoke evidence

- Goal:
  - Add `v0.1.1` release metadata, release notes, release target support, and smoke validation for command alias claims.
- Requirements:
  - `R34`, `R36`, `R40`-`R44`, `R48`
- Files/components likely touched:
  - `scripts/adapter_distribution.py`
  - `scripts/validate-release.py`
  - `scripts/release-verify.sh`
  - `scripts/test-adapter-distribution.py`
  - `docs/releases/v0.1.1/release.yaml`
  - `docs/releases/v0.1.1/release-notes.md`
  - `README.md`
  - `docs/workflows.md`
- Dependencies:
  - M1 generated command aliases and manifest metadata
  - M2 docs that should only publish one-shot examples with smoke evidence
  - maintainer access to OpenCode for manual smoke
- Tests to add/update:
  - release target test for `v0.1.1` with manifest version `0.1.1`
  - release validation test rejecting unsupported `v0.1.1` before registry support
  - release validation test rejecting insufficient OpenCode alias smoke evidence
  - release notes consistency test for command alias set
  - release verification dry-run test or assertion that required checks include `v0.1.1` paths
- Implementation steps:
  - add `v0.1.1` to the release target registry as a final release with manifest version `0.1.1`
  - update `scripts/release-verify.sh` to allow `v0.1.1`
  - extend release validation to require command alias metadata and command alias smoke evidence for `v0.1.1`
  - create `docs/releases/v0.1.1/release.yaml`
  - create `docs/releases/v0.1.1/release-notes.md`
  - run OpenCode smoke for at least one generated command alias
  - include `opencode run --command ...` examples in README, entrypoints, and release notes only if that exact form passes smoke
  - update workflow docs if validation commands need to move from `0.1.0` to `0.1.1`
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-release.py --version v0.1.1`
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`
  - `opencode run --dir <adapter-install-root> --command proposal "Confirm the proposal skill was loaded and followed."`
  - `git diff --check -- scripts docs README.md dist docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`
- Expected observable result:
  - `v0.1.1` release verification can validate generated command aliases, release metadata, release notes, and OpenCode command alias smoke evidence.
- Commit message: `M3: prepare v0.1.1 command alias release`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - OpenCode smoke may be blocked by local account/tool configuration
  - smoke evidence may prove the command exists but not that the matching skill was followed
  - docs may need to omit one-shot examples if smoke cannot verify them
- Rollback/recovery:
  - keep `v0.1.1` release artifacts untagged until smoke passes
  - if one-shot smoke fails, remove one-shot examples and release only TUI alias documentation

### M4. Lifecycle artifacts, final validation, and PR readiness

- Goal:
  - Create the required change-local artifact pack, run final validation, and close the implementation lane through review handoff readiness.
- Requirements:
  - all in-scope requirements, plus repository lifecycle and validation rules
- Files/components likely touched:
  - `docs/changes/2026-04-24-skill-invocation-commands-for-adapters/change.yaml`
  - `docs/changes/2026-04-24-skill-invocation-commands-for-adapters/explain-change.md`
  - `docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`
  - `docs/plan.md`
  - any touched authoritative artifacts whose Follow-on artifacts or readiness changed
- Dependencies:
  - M1 through M3 complete
  - matching test spec active before implementation begins
- Tests to add/update:
  - artifact lifecycle explicit-path validation for touched lifecycle artifacts
  - final generated-output drift and adapter validation checks
- Implementation steps:
  - create `docs/changes/<change-id>/change.yaml`
  - create durable reasoning in `docs/changes/<change-id>/explain-change.md`
  - update plan progress, validation notes, decisions, and surprises
  - update Follow-on artifacts for proposal, spec, and architecture if additional downstream artifacts were created
  - run the final validation set
  - prepare for `code-review` after implementation completes
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-release.py --version v0.1.1`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-skill-invocation-commands-for-adapters.md --path specs/skill-invocation-commands-for-adapters.md --path specs/skill-invocation-commands-for-adapters.test.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/changes/2026-04-24-skill-invocation-commands-for-adapters/change.yaml --path docs/changes/2026-04-24-skill-invocation-commands-for-adapters/explain-change.md`
  - `bash scripts/ci.sh`
  - `git diff --check`
- Expected observable result:
  - the branch has complete implementation evidence, lifecycle artifacts, and validation results ready for `code-review`.
- Commit message: `M4: close command alias release lifecycle`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - lifecycle artifacts can become stale while generated output changes
  - broad CI may fail on unrelated local work if explicit-path validation is not used carefully
- Rollback/recovery:
  - keep lifecycle artifacts consistent with the actual branch state
  - if final validation fails, fix the failure before moving to `code-review`

## Validation plan

- Use `python scripts/test-adapter-distribution.py` as the main fixture and regression proof for generated command aliases, manifest parsing, adapter validation, release target validation, and release notes checks.
- Use `python scripts/build-adapters.py --version 0.1.1 --check` as the generated adapter drift proof.
- Use `python scripts/validate-adapters.py --version 0.1.1` as the package structure, manifest, and security proof.
- Use `python scripts/validate-release.py --version v0.1.1` and `bash scripts/release-verify.sh v0.1.1` as the release proof.
- Use explicit-path artifact lifecycle validation when local untracked or unrelated work exists.
- Use maintainer-run OpenCode smoke for command alias behavior before claiming `v0.1.1` stable release readiness.

## Risks and recovery

- Risk: the OpenCode command alias wrapper does not reliably trigger matching skill behavior.
  Recovery: remove one-shot claims, keep only TUI guidance, or revise the alias prompt before release.
- Risk: manifest parsing becomes too complex.
  Recovery: keep only the exact `command_aliases.opencode` shape and reject unsupported sections.
- Risk: release validation overfits to `v0.1.1`.
  Recovery: keep existing `v0.1.0-rc.1` and `v0.1.0` target entries and add tests for all supported target versions.
- Risk: generated output noise makes review hard.
  Recovery: keep milestone commits grouped by generator logic, docs, release artifacts, and lifecycle closeout.
- Risk: tool docs or CLI behavior change before release.
  Recovery: update the spec or architecture before implementation if official behavior no longer matches the approved contract.

## Dependencies

- The approved spec and architecture are required before implementation.
- `plan-review` must happen before `test-spec`.
- The matching test spec must be active before implementation begins.
- OpenCode must be available to the maintainer for final command alias smoke evidence.
- Claude Code one-shot examples stay out of scope unless smoke evidence is added explicitly.

## Progress

- [x] Proposal accepted.
- [x] Spec approved.
- [x] Architecture approved.
- [x] Execution plan created.
- [x] Plan review complete.
- [x] Test spec active.
- [x] M1 complete.
- [x] M2 complete.
- [x] M3 complete.
- [ ] M4 complete.

## Decision log

- 2026-04-24: Use a separate architecture extension for command aliases rather than rewriting the `v0.1.0` distribution architecture in place. Rationale: this is a patch-level generated package extension with its own manifest and smoke details.
- 2026-04-24: Split implementation into alias generation, user-facing docs, release verification, and lifecycle closeout. Rationale: each slice has a distinct validation boundary and can be reviewed coherently.
- 2026-04-24: Keep `docs/releases/v0.1.1/release-notes.md` fully owned by M3, not M2. Rationale: release notes and one-shot examples require M3 release metadata and smoke evidence.
- 2026-04-24: Move `DEFAULT_ADAPTER_VERSION` and CI adapter drift checks to `0.1.1` in M1. Rationale: tracked `dist/adapters/` now represents the generated package version with command aliases, so repository-owned adapter checks must validate the current generated tree rather than historical `0.1.0` output.
- 2026-04-24: Include the OpenCode `opencode run --command proposal` one-shot example in README, the OpenCode adapter entrypoint, and `v0.1.1` release notes after maintainer smoke proved that the alias loads the `proposal` skill and passes arguments through.

## Surprises and discoveries

- 2026-04-24: Planning was blocked until the command alias architecture extension existed because the approved spec explicitly named `architecture` as the immediate next stage.
- 2026-04-24: Plan review found ambiguous release-notes ownership between M2 and M3; the plan now keeps M2 to README plus generated entrypoint docs and gates release notes and one-shot examples on M3 smoke evidence.
- 2026-04-24: Regenerating tracked adapter output for `0.1.1` made repository-current adapter CLI and CI checks stale while historical `v0.1.0` release validation still needed coverage. The M1 fix moved current adapter checks to `0.1.1` and kept `v0.1.0` release validation covered through isolated fixtures, leaving `v0.1.1` release metadata to M3.
- 2026-04-24: OpenCode command alias smoke needed both command execution and argument pass-through evidence. Repeating `ARGUMENT_MARKER_M3_SMOKE` in the OpenCode response gave release validation a concrete behavior signal beyond file discovery.

## Validation notes

- 2026-04-24: Plan-stage validation passed for initial artifact creation.
- 2026-04-24: Plan-review revision applied to move `docs/releases/v0.1.1/release-notes.md` ownership fully to M3 and prohibit one-shot examples before M3 smoke evidence.
- 2026-04-24: Test spec created at `specs/skill-invocation-commands-for-adapters.test.md`; `git diff --check` and explicit-path artifact lifecycle validation passed.
- 2026-04-24: M1 tests were added first; `python scripts/test-adapter-distribution.py` initially failed with `ImportError` for missing `OPENCODE_COMMAND_ALIASES`, then passed after alias generation, manifest parsing, validation, and generated-output updates.
- 2026-04-24: M1 validation passed with `python scripts/test-adapter-distribution.py`, `python scripts/build-adapters.py --version 0.1.1`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/build-adapters.py --check`, `python scripts/validate-adapters.py --version 0.1.1`, `git diff --check -- scripts tests dist docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`, and `bash scripts/ci.sh`.
- 2026-04-24: M1 code-review fix added direct T5 coverage for a manifest-declared non-curated OpenCode alias. Validation passed with `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_opencode_command_alias_manifest_validation_rejects_mismatches`, `python scripts/test-adapter-distribution.py`, and `bash scripts/ci.sh`.
- 2026-04-24: M1 clean re-review completed with `clean-with-notes`. Verify found stale review metadata, so the change metadata and plan readiness were updated before rerunning validation.
- 2026-04-24: M2 tests were added first; focused entrypoint and README invocation tests initially failed because the docs lacked tool-native invocation guidance, then passed after README and adapter template updates.
- 2026-04-24: M2 validation passed with `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_claude_entrypoint_documents_native_skill_invocation AdapterDistributionTests.test_opencode_entrypoint_documents_skills_and_thin_aliases AdapterDistributionTests.test_readme_distinguishes_claude_and_opencode_invocation_forms`, `python scripts/build-adapters.py --version 0.1.1`, `python scripts/test-adapter-distribution.py`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, the documented `rg` check, `git diff --check`, and `bash scripts/ci.sh`.
- 2026-04-24: M2 code-review completed with `clean-with-notes`; no required-change findings remained before verification.
- 2026-04-24: M2 verification passed on tracked state with `bash scripts/ci.sh`; lifecycle validation reported only unrelated baseline proposal warnings.
- 2026-04-24: M3 maintainer smoke passed for Codex `codex-cli 0.124.0`, Claude Code `2.1.119 (Claude Code)`, and OpenCode `1.14.22`. OpenCode smoke used `opencode run --pure --dir <copied-adapter-root> --command proposal` and verified that the `proposal` skill loaded and repeated `ARGUMENT_MARKER_M3_SMOKE` from the command arguments.
- 2026-04-24: M3 tests were added first for `v0.1.1` release target support, OpenCode command alias smoke evidence, release verification support, and smoke-backed docs. The focused test set initially failed because `v0.1.1` release artifacts and one-shot docs were not yet wired, then passed after release validation, metadata, notes, and template updates.
- 2026-04-24: M3 validation passed with `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_v0_1_1_release_metadata_requires_command_alias_smoke_evidence AdapterDistributionTests.test_validate_release_cli_accepts_repository_v0_1_1_artifacts AdapterDistributionTests.test_release_verify_script_supports_v0_1_1 AdapterDistributionTests.test_opencode_entrypoint_documents_skills_and_thin_aliases AdapterDistributionTests.test_readme_distinguishes_claude_and_opencode_invocation_forms`, `python scripts/build-adapters.py --version 0.1.1`, `python scripts/test-adapter-distribution.py`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/validate-release.py --version v0.1.1`, `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`, `git diff --check -- README.md scripts docs dist`, and `bash scripts/ci.sh`.

## Outcome and retrospective

M1 through M3 are implemented. OpenCode command aliases are generated, listed exactly in `dist/adapters/manifest.yaml`, and validated for drift, manifest consistency, dangling aliases, stale bodies, and unsafe content. README and generated Claude/OpenCode entrypoints document tool-native TUI invocation forms. Because M3 smoke verified the OpenCode command alias one-shot path, README, the OpenCode entrypoint, and `v0.1.1` release notes now include `opencode run --command proposal`.

## Readiness

M3 is implemented and ready for code-review. M4 remains the final lifecycle closeout milestone after review and verification.

## Risks and follow-ups

- Follow-up: complete code-review, verify, and M4 lifecycle closeout before PR readiness.
