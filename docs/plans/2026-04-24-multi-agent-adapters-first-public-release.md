# Multi-agent adapters and first public release plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-24
- Last updated: 2026-04-24
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved multi-agent adapter and first-public-release contract as a set of deterministic, reviewable slices. The work should let RigorLoop keep `skills/` as the only authored skill source while generating independently installable Codex, Claude Code, and opencode adapter packages under `dist/adapters/`.

The plan separates adapter logic, generated output, validation, release evidence, public docs, and manual smoke closeout so each slice has a coherent proof boundary. The first implementation target is `v0.1.0-rc.1`: structurally ready generated packages with incomplete smoke allowed only as `not-run` or externally `blocked` rows with reason and owner. The stable `v0.1.0` closeout remains maintainer-gated until every supported tool smoke row passes.

## Source artifacts

- Proposal: `docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md`
- Spec: `specs/multi-agent-adapters-first-public-release.md`
- Spec-review findings: resolved before this plan; RC gates, smoke matrix shape, and placeholder release-check rules are now explicit in the spec.
- Architecture: `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md`
- ADR: `docs/adr/ADR-20260424-generated-adapter-packages.md`
- Architecture-review findings: approved; carry forward the plan caution that release validation must stay target-version scoped so historical `v0.1.0-rc.1` metadata is not accidentally revalidated against a later `0.1.0` manifest.
- Test spec: `specs/multi-agent-adapters-first-public-release.test.md`
- Project map: none exists. Existing source layout is small enough for this plan to orient from scripts, docs, specs, and architecture.

## Context and orientation

- Canonical authored workflow content lives in `docs/`, `specs/`, `skills/`, `schemas/`, and `scripts/`.
- `skills/` is the canonical authored skill tree.
- `.codex/skills/` is generated local Codex runtime compatibility output and remains checked by `scripts/build-skills.py --check`.
- New public adapter packages will be generated under `dist/adapters/` and must not become another authored skill tree.
- Existing skill validation uses `scripts/skill_validation.py`, `scripts/validate-skills.py`, `scripts/test-skill-validator.py`, and `schemas/skill.schema.json`.
- Existing generated Codex drift logic is isolated in `scripts/build-skills.py`.
- `scripts/ci.sh` currently runs skill validation, skill validator fixtures, `.codex/skills` drift, change metadata fixtures, artifact lifecycle fixtures, and artifact lifecycle validation.
- `scripts/release-verify.sh` is currently a placeholder and contains the exact text that the approved spec now requires release verification to reject.
- `.github/workflows/release.yml` currently delegates to `scripts/release-verify.sh` and uses `gh release create --generate-notes`; the approved architecture requires tracked release notes instead.
- `README.md`, `docs/workflows.md`, and `AGENTS.md` currently describe the Codex-oriented first-release baseline and will need public adapter guidance once generated packages and validation exist.
- Ordinary contributors should be able to run repository-owned non-smoke validation without Codex, Claude Code, or opencode installed.

## Non-goals

- Build a hosted RigorLoop service, control plane, marketplace package, plugin registry publication, or installer distribution.
- Guarantee identical runtime behavior across Codex, Claude Code, and opencode.
- Make every existing skill portable in the first public release.
- Require ordinary contributors to install all supported tools locally.
- Add secrets, API keys, private credentials, or default permission-bypass configuration.
- Replace Git, pull requests, CI, human review, or the existing RigorLoop lifecycle.
- Retire `.codex/skills/` in this initiative. It remains a separate generated local Codex mirror until a later accepted lifecycle change retires or migrates it.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R15` | `scripts/adapter_distribution.py`, `scripts/build-adapters.py`, `scripts/adapter_templates/`, generated `dist/adapters/{codex,claude,opencode}/`, and `dist/adapters/manifest.yaml` |
| `R16`-`R28` | portable-core validation in `scripts/adapter_distribution.py`, adapter regression fixtures, generated skill transforms or exclusions, and manifest exclusion reasons |
| `R29`-`R35` | generated manifest writer, deterministic ordering, generated package drift check, and `scripts/validate-adapters.py` |
| `R36`-`R38` | `README.md`, `docs/workflows.md`, `AGENTS.md`, and release notes support matrix wording |
| `R39`-`R42a` | `docs/releases/<version>/release.yaml`, `docs/releases/<version>/release-notes.md`, and `scripts/validate-release.py` |
| `R43`-`R47` | `scripts/validate-release.py`, `scripts/release-verify.sh`, tracked release notes, RC and final smoke rules, placeholder release-check rejection |
| `R48` | `scripts/ci.sh`, adapter regression tests, adapter generation drift check, adapter validation, and GitHub workflow wrappers |
| `R49`-`R50` | continued `scripts/build-skills.py --check` proof for `.codex/skills/`, docs explaining `.codex/skills/` versus `dist/adapters/codex/`, and ADR-backed boundaries |
| `R51`-`R53` | no hosted runtime, no network/secrets requirement, standard-library generation and validation, security scans over generated adapters, templates, release metadata, and release notes |

## Milestones

### M1. Adapter core and portable-core validation

- Goal:
  - Add the shared adapter model and portable-core validation logic without writing generated packages yet.
- Requirements:
  - `R1`, `R6`-`R9`, `R16`-`R28`, `R31a`, `R35`, `R51`-`R53`
- Files/components likely touched:
  - `scripts/adapter_distribution.py`
  - `scripts/test-adapter-distribution.py`
  - `tests/fixtures/adapters/`
  - `scripts/skill_validation.py` only if existing frontmatter helpers need a safe shared extraction
- Dependencies:
  - approved proposal, spec, architecture, and ADR
  - existing canonical skill validator behavior
  - no dependency on real Codex, Claude Code, or opencode installations
- Tests to add/update:
  - fixtures for a portable skill
  - fixtures for invalid names and descriptions
  - fixtures for unsupported frontmatter
  - fixtures for `$skill` or Codex-only invocation assumptions
  - fixtures for `.codex/skills` as the only install location
  - fixtures for `agents/openai.yaml`
  - fixtures for Codex-only tool, UI, approval, or permission assumptions
  - fixtures for explicit exclusion or validated transform behavior
- Implementation steps:
  - define the first-public-release adapter set: `codex`, `claude`, `opencode`
  - define each adapter package root, instruction entrypoint, and project-skill path in one shared model
  - implement portable skill-name validation with the approved lowercase hyphenated pattern and 64-character limit
  - implement portable description validation with the approved non-empty and 1024-character limit
  - implement portable-core body and metadata checks for Codex-only assumptions named in the spec
  - represent adapter inclusion, exclusion, transform, and human-readable reason in one deterministic data structure
  - implement constrained YAML rendering/parsing helpers only for the manifest and release metadata shapes approved by the architecture
  - keep all checks standard-library only and independent of network access or tool installations
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py`
  - `git diff --check -- scripts tests docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- Expected observable result:
  - repository-owned tests can classify canonical or fixture skills as portable, excluded, or transformable for each adapter without creating `dist/adapters/`
- Commit message: `M1: add adapter portability core`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - portable-core checks may become too heuristic if body matching is vague
  - transform behavior may silently hide tool-specific assumptions
  - YAML helper scope may grow beyond the approved constrained shapes
- Rollback/recovery:
  - revert the new shared adapter module and fixtures without touching canonical skills or generated output
  - if a required transform cannot be made deterministic and testable, exclude the skill with a manifest reason instead of guessing

### M2. Adapter package generation and tracked RC outputs

- Goal:
  - Generate tracked adapter-specific packages and `dist/adapters/manifest.yaml` for `0.1.0-rc.1`.
- Requirements:
  - `R2`-`R15`, `R27`-`R35`, `R49`-`R50`
- Files/components likely touched:
  - `scripts/build-adapters.py`
  - `scripts/adapter_templates/codex/AGENTS.md`
  - `scripts/adapter_templates/claude/CLAUDE.md`
  - `scripts/adapter_templates/opencode/AGENTS.md`
  - `dist/adapters/manifest.yaml`
  - `dist/adapters/codex/AGENTS.md`
  - `dist/adapters/codex/.agents/skills/*/SKILL.md`
  - `dist/adapters/claude/CLAUDE.md`
  - `dist/adapters/claude/.claude/skills/*/SKILL.md`
  - `dist/adapters/opencode/AGENTS.md`
  - `dist/adapters/opencode/.opencode/skills/*/SKILL.md`
- Dependencies:
  - M1 adapter model and portability decisions
  - accepted architecture decision that `dist/adapters/` and `.codex/skills/` are separate generated surfaces
- Tests to add/update:
  - generator check-mode tests in `scripts/test-adapter-distribution.py`
  - fixture assertions for required package paths and entrypoints
  - fixture assertions for deterministic manifest ordering and version
- Implementation steps:
  - add thin authored instruction entrypoint templates for each adapter
  - implement `python scripts/build-adapters.py --version <version>`
  - implement `python scripts/build-adapters.py --version <version> --check`
  - render skill files into each adapter's target project-skill path
  - render entrypoints from thin templates without duplicating skill bodies
  - generate `dist/adapters/manifest.yaml` with version, skill portability, adapter inclusion lists, and exclusion reasons
  - remove unexpected generated files in write mode and fail on unexpected files in check mode
  - generate the first tracked package set with manifest version `0.1.0-rc.1`
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.0-rc.1`
  - `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`
  - `test -f dist/adapters/codex/AGENTS.md`
  - `test -f dist/adapters/claude/CLAUDE.md`
  - `test -f dist/adapters/opencode/AGENTS.md`
  - `test -f dist/adapters/manifest.yaml`
  - `git diff --check -- scripts tests dist docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- Expected observable result:
  - the repository contains independently copyable generated adapter package roots for Codex, Claude Code, and opencode, plus a generated `0.1.0-rc.1` manifest
- Commit message: `M2: generate rc adapter packages`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - checked-in generated output may be noisy
  - `dist/adapters/codex/` may be confused with `.codex/skills/`
  - entrypoint templates may accidentally duplicate large skill bodies
- Rollback/recovery:
  - remove `dist/adapters/`, `scripts/build-adapters.py`, and adapter templates while leaving canonical `skills/` and `.codex/skills/` untouched
  - if generated output becomes stale, rerun the generator rather than hand-editing generated files

### M3. Adapter validation, security checks, and CI integration

- Goal:
  - Add repository-owned validation for generated adapter packages and wire the non-smoke adapter checks into CI.
- Requirements:
  - `R7`-`R10`, `R16`-`R35`, `R48`, `R51`-`R53`
- Files/components likely touched:
  - `scripts/validate-adapters.py`
  - `scripts/adapter_distribution.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/ci.sh`
  - `scripts/artifact_lifecycle_validation.py`
  - `tests/fixtures/adapters/`
- Dependencies:
  - M1 portability logic
  - M2 generated adapter packages
- Tests to add/update:
  - validation fixture for missing adapter directories
  - validation fixture for missing instruction entrypoints
  - validation fixture for manifest/file mismatches
  - validation fixture for unsupported metadata leaks in non-Codex adapters
  - validation fixture for generated secret markers or machine-local paths
  - validation fixture for generated `dist/adapters/*` not being treated as authored lifecycle source
- Implementation steps:
  - implement `python scripts/validate-adapters.py --version <manifest-version>`
  - validate adapter root existence, entrypoint existence, skill paths, manifest version, generated skill counts, and manifest/file consistency
  - validate portable-core inclusion decisions against generated files
  - validate unsupported metadata is removed, transformed, or excluded where required
  - add security scanning for common secret markers, private key delimiters, absolute machine-local paths, and placeholder permission-bypass language
  - update `scripts/ci.sh` to run adapter regression tests, adapter drift checks, and adapter validation
  - keep `scripts/ci.sh` filtering generated `dist/adapters/*` out of authored artifact lifecycle validation
  - extend artifact lifecycle handling if needed so generated adapter paths are not accepted as authored lifecycle-managed inputs
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.0-rc.1`
  - `bash scripts/ci.sh`
  - `git diff --check -- scripts tests dist docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- Expected observable result:
  - ordinary contributors can run local non-smoke checks that prove generated adapters are in sync, structurally valid, security-scanned, and not treated as authored lifecycle source
- Commit message: `M3: validate adapter package outputs`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - CI may become noisy if generated paths are sent to authored artifact lifecycle validation
  - security scanning may be either too weak to catch obvious leaks or too broad for release notes and examples
  - adapter validation may duplicate generator logic in a way that misses shared bugs
- Rollback/recovery:
  - revert CI wiring first if it blocks unrelated contributors
  - keep `build-adapters.py --check` as the minimum drift proof while validator defects are fixed
  - narrow false-positive security patterns with explicit fixtures rather than bypassing security validation

### M4. Release metadata validator and RC release artifacts

- Goal:
  - Add target-version-scoped release metadata validation and create the `v0.1.0-rc.1` release evidence artifacts.
- Requirements:
  - `R39`-`R47`, `R52`-`R53`
- Files/components likely touched:
  - `scripts/validate-release.py`
  - `scripts/adapter_distribution.py`
  - `scripts/test-adapter-distribution.py`
  - `docs/releases/v0.1.0-rc.1/release.yaml`
  - `docs/releases/v0.1.0-rc.1/release-notes.md`
  - `tests/fixtures/adapters/`
- Dependencies:
  - M2 generated `0.1.0-rc.1` adapter packages
  - M3 adapter validation
  - architecture-review caution that release validation must stay target-version scoped
- Tests to add/update:
  - release metadata fixture with one smoke row per supported tool
  - failing fixture for mismatched manifest version
  - failing fixture for mismatched supported tools across release notes, release metadata, manifest, and generated paths
  - failing fixture for RC smoke `fail`
  - failing fixture for RC `not-run` or `blocked` without reason or owner
  - failing fixture for missing required smoke row fields
  - failing fixture for final release smoke that is not all `pass`
- Implementation steps:
  - implement `python scripts/validate-release.py --version v0.1.0-rc.1`
  - require release metadata path `docs/releases/<version>/release.yaml`
  - require release notes path `docs/releases/<version>/release-notes.md`
  - validate release metadata shape, release type, manifest version, supported tools, adapter paths, instruction entrypoints, smoke rows, and validation rows
  - validate release notes version is exactly the target tag
  - compare release metadata, release notes, manifest, and generated adapter paths for the same supported tools
  - implement RC smoke allowances for `not-run` and externally `blocked` rows with reason and owner
  - implement final smoke strictness for all `pass` rows
  - create `docs/releases/v0.1.0-rc.1/release.yaml` with `not-run` smoke rows and owner/reason fields
  - create tracked `docs/releases/v0.1.0-rc.1/release-notes.md` describing the generated adapter package set, support matrix, exclusions, and known limitations
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.0-rc.1`
  - `python scripts/validate-adapters.py --version 0.1.0-rc.1`
  - `git diff --check -- scripts tests docs/releases docs/changes/2026-04-24-multi-agent-adapters-first-public-release docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- Expected observable result:
  - the repository has authoritative RC release metadata and release notes that validate against the generated `0.1.0-rc.1` adapter package set without requiring manual smoke to pass
- Commit message: `M4: add rc release metadata validation`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - release metadata could become another stale authored source
  - validating historical RC metadata against a later final manifest could create false failures
  - release notes may describe unsupported tools or skills not present in the manifest
- Rollback/recovery:
  - keep `validate-release.py` scoped to one requested tag and the package state at that tag
  - if metadata and manifest disagree, fix the generator or metadata before changing release claims
  - remove RC release artifacts before tag publication if the generated package set is not ready

### M5. Public docs, release gate replacement, and workflow integration

- Goal:
  - Replace placeholder release checks with repository-specific gates and update public guidance for generated adapter packages.
- Requirements:
  - `R36`-`R38`, `R43`-`R48`, `R51`-`R53`
- Files/components likely touched:
  - `scripts/release-verify.sh`
  - `.github/workflows/release.yml`
  - `README.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `docs/releases/v0.1.0-rc.1/release-notes.md`
  - `docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- Dependencies:
  - M1 through M4 complete
  - tracked RC release metadata and notes exist
- Tests to add/update:
  - release verification invocation coverage through `scripts/test-adapter-distribution.py` or shell-level focused checks
  - documentation checks for support matrix and canonical-versus-generated wording
  - placeholder text rejection checks
- Implementation steps:
  - replace the placeholder `scripts/release-verify.sh` with a real orchestrator
  - make `scripts/release-verify.sh` accept an explicit version argument and fall back to `GITHUB_REF_NAME` in GitHub Actions
  - invoke skill validation, skill regression validation, `.codex/skills` drift check, adapter distribution regression tests, adapter generation drift check, adapter validation, release metadata validation, and security checks
  - fail release verification when placeholder release-check text remains
  - fail release verification when any required repository-specific check is missing from the orchestrator
  - update `.github/workflows/release.yml` to pass the tag to release verification and create GitHub releases from tracked `docs/releases/<tag>/release-notes.md`
  - update public documentation to describe adapter installation by copying one adapter package root into a project
  - update public documentation to distinguish `skills/`, `.codex/skills/`, and `dist/adapters/`
  - state that ordinary contributors do not need all supported tools installed locally for non-smoke validation
  - document that RC may be published before full smoke only when non-smoke gates pass and no known smoke failures exist
- Validation commands:
  - `bash scripts/release-verify.sh v0.1.0-rc.1`
  - `bash scripts/ci.sh`
  - `! rg -n 'Replace this script with repository-specific release checks|TODO: release checks|placeholder release check' scripts/release-verify.sh`
  - `rg -n 'codex|claude|opencode|dist/adapters|\\.codex/skills|not need all supported tools' README.md docs/workflows.md AGENTS.md docs/releases/v0.1.0-rc.1/release-notes.md`
  - `git diff --check -- scripts .github README.md docs AGENTS.md dist`
- Expected observable result:
  - `bash scripts/release-verify.sh v0.1.0-rc.1` is the authoritative RC release gate and passes with structurally ready generated packages plus allowed incomplete smoke rows
- Commit message: `M5: replace release gate for rc adapters`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - release verification may accidentally claim hosted CI passed without observed evidence
  - docs may imply marketplace or package-manager distribution
  - `release.yml` may still use generated GitHub notes instead of tracked notes
- Rollback/recovery:
  - revert release workflow changes if tag publishing behavior is unsafe
  - keep release verification local-only until the shell gate is deterministic
  - narrow documentation claims to generated project-local adapter packages if any install claim is over-broad

### M6. Maintainer smoke and stable `v0.1.0` closeout

- Goal:
  - Convert the structurally ready RC package set into a stable `v0.1.0` release only after maintainer smoke passes for every supported tool.
- Requirements:
  - `R29b`, `R39`-`R47`, especially `R44`-`R45`
- Files/components likely touched:
  - `dist/adapters/manifest.yaml`
  - `dist/adapters/{codex,claude,opencode}/`
  - `docs/releases/v0.1.0/release.yaml`
  - `docs/releases/v0.1.0/release-notes.md`
  - `docs/plan.md`
  - `docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- Dependencies:
  - M1 through M5 complete
  - maintainer has access to Codex, Claude Code, and opencode smoke environments
  - every smoke row result can be recorded as `pass` with non-empty tool version and evidence
- Tests to add/update:
  - no new automated tests expected unless smoke reveals a validator or generator defect
  - update fixtures only when a smoke finding exposes an automated validation gap
- Implementation steps:
  - run the maintainer smoke matrix against each generated adapter package
  - record one `pass` smoke row per supported tool in `docs/releases/v0.1.0/release.yaml`
  - regenerate adapter packages and manifest for version `0.1.0`
  - create stable release notes with version exactly `v0.1.0`
  - run final release verification for `v0.1.0`
  - update this plan and `docs/plan.md` lifecycle state only when the stable release readiness outcome is known
- Manual smoke checks:
  - Codex adapter package can be copied into a clean project root and exposes `AGENTS.md` plus `.agents/skills/<skill>/SKILL.md`
  - Claude Code adapter package can be copied into a clean project root and exposes `CLAUDE.md` plus `.claude/skills/<skill>/SKILL.md`
  - opencode adapter package can be copied into a clean project root and exposes `AGENTS.md` plus `.opencode/skills/<skill>/SKILL.md`
- Validation commands:
  - `python scripts/build-adapters.py --version 0.1.0`
  - `python scripts/build-adapters.py --version 0.1.0 --check`
  - `python scripts/validate-adapters.py --version 0.1.0`
  - `python scripts/validate-release.py --version v0.1.0`
  - `bash scripts/release-verify.sh v0.1.0`
  - `git diff --check -- dist docs/releases/v0.1.0 docs/plan.md docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- Expected observable result:
  - the stable package set has manifest version `0.1.0`, all supported smoke rows pass, and `bash scripts/release-verify.sh v0.1.0` succeeds
- Commit message: `M6: prepare stable adapter release`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - maintainer smoke may reveal a real tool-discovery incompatibility
  - the stable version bump can make old RC metadata look stale if validators are not target-version scoped
  - final release notes may overstate unsupported skills or tool behavior
- Rollback/recovery:
  - if any smoke row fails, do not publish `v0.1.0`; keep or publish only RC artifacts with the known failure resolved before retesting
  - if smoke is externally blocked, keep stable release blocked and use RC metadata with owner and reason only when no known smoke failures exist
  - if the stable manifest is generated prematurely, regenerate `0.1.0-rc.1` before RC verification or keep the stable change isolated until smoke passes

## Validation plan

| Validation level | When | Required before implementation handoff? | Purpose |
| --- | --- | ---: | --- |
| Planning validation | after this plan is created | yes | Prove the plan and index are lifecycle-valid and formatting-clean. |
| Milestone targeted validation | before each milestone closeout | yes | Prove the milestone's concrete behavior and touched files. |
| CI wrapper validation | after CI wiring and before RC readiness | yes | Prove ordinary contributor non-smoke validation works through `scripts/ci.sh`. |
| RC release verification | before `v0.1.0-rc.1` tag readiness | yes | Prove all non-smoke release gates pass and incomplete smoke rows are allowed only under RC rules. |
| Manual smoke matrix | before `v0.1.0` readiness | yes | Prove every supported tool has passing maintainer smoke evidence. |

- Planning-stage validation:
  - `git diff --check -- docs/plan.md docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md specs/multi-agent-adapters-first-public-release.md docs/architecture/2026-04-24-multi-agent-adapter-distribution.md docs/adr/ADR-20260424-generated-adapter-packages.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md --path docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md --path specs/multi-agent-adapters-first-public-release.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/adr/ADR-20260424-generated-adapter-packages.md`
- Milestone validation:
  - run the validation commands listed in the relevant milestone before marking that milestone complete
  - update `Validation notes` with command, result, and any material failure or retry
- Final release validation:
  - `bash scripts/release-verify.sh v0.1.0-rc.1` is required before RC tag readiness
  - `bash scripts/release-verify.sh v0.1.0` plus passing manual smoke evidence is required before stable tag readiness

## Risks and recovery

- Risk: generated `dist/adapters/` becomes a second authored source of truth.
  - Recovery: keep generator drift checks mandatory, filter generated adapter paths out of authored lifecycle validation, and update docs to say canonical edits happen in `skills/` and templates only.
- Risk: portable-core validation silently ships misleading non-Codex skills.
  - Recovery: default uncertain tool-specific assumptions to exclusion with a manifest reason unless an explicit tested transform exists.
- Risk: `.codex/skills/` and `dist/adapters/codex/` drift independently.
  - Recovery: keep separate drift checks for `scripts/build-skills.py --check` and `scripts/build-adapters.py --check`.
- Risk: release verification remains a checklist by another name.
  - Recovery: make `scripts/release-verify.sh` invoke concrete repository-owned commands and reject placeholder wording or missing required invocations.
- Risk: RC and final release metadata conflict as versions change.
  - Recovery: validate one requested tag at a time and run release verification against the package state at the intended tag.
- Risk: manual smoke is blocked by tool access.
  - Recovery: allow only RC `blocked` rows with external/tool-access reason and owner; keep stable `v0.1.0` blocked until all rows pass.
- Risk: security scans produce noisy false positives.
  - Recovery: tune patterns with failing fixtures and keep explicit allowlist decisions narrow and reviewed.

## Dependencies

- `plan-review` must complete before implementation starts.
- `specs/multi-agent-adapters-first-public-release.test.md` must be created and active before production code changes begin.
- M2 depends on M1 adapter classification and deterministic rendering helpers.
- M3 depends on generated output existing from M2.
- M4 depends on generated RC packages and adapter validation.
- M5 depends on release metadata validation and RC release artifacts.
- M6 depends on maintainer-run manual smoke for Codex, Claude Code, and opencode.
- No milestone requires ordinary contributors to install Codex, Claude Code, or opencode for non-smoke validation.
- No milestone should add third-party dependencies unless a later architecture update explicitly approves the dependency.

## Progress

- [x] 2026-04-24: proposal accepted.
- [x] 2026-04-24: spec approved after spec-review.
- [x] 2026-04-24: architecture approved and ADR accepted after architecture-review.
- [x] 2026-04-24: execution plan created and indexed.
- [x] 2026-04-24: planning-stage validation passed.
- [x] 2026-04-24: plan-review approved with no required edits.
- [x] 2026-04-24: test spec active.
- [x] 2026-04-24: M1 adapter core and portable-core validation complete.
- [x] 2026-04-24: M1 code-review finding accepted and fixed; manifest exclusion reasons are now quoted.
- [x] 2026-04-24: M1 rereview findings accepted and fixed; invalid skill bodies and partial portability now have direct tests.
- [x] 2026-04-24: M2 adapter package generation and tracked RC outputs implemented.
- [x] 2026-04-24: M3 adapter validation, security checks, and CI integration implemented.
- [x] 2026-04-24: M4 release metadata validation and `v0.1.0-rc.1` release artifacts implemented.
- [x] 2026-04-24: M4 first-pass code-review completed with `clean-with-notes`; no required changes.
- [x] 2026-04-24: M4 verify passed; the next implementation slice is M5.
- [x] 2026-04-24: M5 public docs, release gate replacement, and workflow integration implemented.
- [ ] M6 complete.

## Decision log

- 2026-04-24: Plan targets `v0.1.0-rc.1` first, then stable `v0.1.0` after manual smoke passes. This matches the approved release distinction between structural package readiness and smoke-verified final release.
- 2026-04-24: Keep `.codex/skills/` and `dist/adapters/codex/` as separate generated surfaces with separate drift checks. This avoids making generated output the source for other generated output.
- 2026-04-24: Put shared adapter behavior in `scripts/adapter_distribution.py` and keep CLI scripts thin. This follows the existing repository pattern of reusable validation helpers plus small entrypoints.
- 2026-04-24: Keep release validation target-version scoped. This carries forward the architecture-review caution and prevents later stable-version work from invalidating historical RC evidence outside its tag context.
- 2026-04-24: M1 treats `argument-hint` frontmatter as an explicit non-Codex transform and unknown frontmatter as a non-Codex exclusion. This keeps current Codex metadata support while preventing unsupported metadata from leaking into Claude Code or opencode outputs.
- 2026-04-24: M1 does not write `dist/adapters/`. It only classifies skills and renders deterministic manifest content in memory so package generation remains isolated to M2.
- 2026-04-24: Quote generated manifest exclusion reasons. This keeps human-readable reasons parseable when they contain YAML-sensitive punctuation such as `: `.
- 2026-04-24: Reuse the repository `SKILL.md` validator for portable-core body checks. This avoids creating a second definition of Agent Skills-compatible Markdown structure.
- 2026-04-24: Treat explicit target-adapter incompatibility text, such as `not compatible with opencode`, as a target-specific exclusion reason. This covers partial portability without weakening the portable-core gate for other adapters.
- 2026-04-24: M2 keeps `scripts/build-adapters.py` as a thin CLI and puts generation, drift, and synchronization behavior in `scripts/adapter_distribution.py`. This preserves the existing repo pattern of shared Python helpers plus small entrypoints.
- 2026-04-24: M2 uses authored thin templates under `scripts/adapter_templates/` for instruction entrypoints and writes the rendered versions into `dist/adapters/`. The templates identify generated output and canonical edit locations without duplicating skill bodies.
- 2026-04-24: M2 preserves Codex adapter skill files as canonical skill text and applies the explicit `argument-hint` drop transform only for included non-Codex adapter skill files.
- 2026-04-24: M3 validates generated adapters through a dedicated `scripts/validate-adapters.py` CLI instead of expanding `scripts/build-adapters.py --check` into a broader validator. Drift and semantic validation remain separate checks.
- 2026-04-24: M3 keeps security scanning high-signal and standard-library only. The scanner rejects private key delimiters, common secret assignments, machine-local absolute paths, and explicit permission-bypass wording without treating ordinary references to permissions or secrets as failures.
- 2026-04-24: M3 filters `dist/adapters/*` out of authored artifact lifecycle validation in `scripts/ci.sh` while still checking those paths through adapter drift and adapter validation.
- 2026-04-24: M4 keeps `scripts/validate-release.py` target-version scoped. It validates only `docs/releases/<version>/` for the requested tag and compares that metadata to the generated adapter package set for the matching manifest version.
- 2026-04-24: M4 records `placeholder_release_check: fail` in `docs/releases/v0.1.0-rc.1/release.yaml` because `scripts/release-verify.sh` is intentionally still a placeholder until M5. The release metadata validator checks that this row matches reality instead of allowing a false pass claim.
- 2026-04-24: M5 keeps `scripts/release-verify.sh` as the single repository-owned release gate. It accepts a tag or `GITHUB_REF_NAME`, derives the adapter manifest version by removing the leading `v`, and rejects targets outside `v0.1.0-rc.1` and `v0.1.0`.
- 2026-04-24: M5 tests release verification orchestration through a script dry-run mode, while the milestone validation still runs the actual `bash scripts/release-verify.sh v0.1.0-rc.1` gate. This avoids recursive full-gate execution inside `scripts/test-adapter-distribution.py` without weakening the real release proof.
- 2026-04-24: M5 release workflow creation uses tracked `docs/releases/<tag>/release-notes.md` and marks RC tags as prereleases instead of relying on generated GitHub notes.

## Surprises and discoveries

- 2026-04-24: The test-first red state was the expected missing `scripts/adapter_distribution.py` module after adding `scripts/test-adapter-distribution.py`; no spec or architecture gap was found.
- 2026-04-24: An earlier M1 milestone commit attempt was blocked by a read-only `.git` filesystem. The filesystem became writable later, so the milestone closeout commit was retried.
- 2026-04-24: M1 code review found that the unsupported-frontmatter exclusion reason included `: ` and therefore needed manifest-rendering coverage, not just portability-decision coverage.
- 2026-04-24: M1 rereview found two preventable proof gaps: valid frontmatter with invalid Markdown body could pass as portable, and the named partial-portability fixture from `T4` had not been added.
- 2026-04-24: The M2 test-first red state was the expected missing adapter generation helper imports after extending `scripts/test-adapter-distribution.py`.
- 2026-04-24: The current canonical `skills/` set has 22 skills, and every skill passes the portable-core gate for all three first-public-release adapters after the explicit non-Codex `argument-hint` transform. The generated RC manifest therefore has no current canonical skill exclusions.
- 2026-04-24: The M3 test-first red state split into two expected failures: adapter validation APIs were missing, and the artifact lifecycle validator did not yet classify `dist/adapters/*` as generated output for explicit-path validation.
- 2026-04-24: `bash scripts/ci.sh` in local diff mode now validates adapter outputs while passing only authored, non-generated changed paths to artifact lifecycle validation. The final observed local lifecycle command excluded generated adapter output and validated the touched authored plan/change artifacts plus scripts.
- 2026-04-24: The M4 test-first red state was the expected missing `validate_release_output` import after adding release metadata validation tests.
- 2026-04-24: M4 revealed an honesty boundary between metadata validation and release verification. Metadata can validate while recording `placeholder_release_check: fail`; M5 owns replacing the placeholder release gate and changing that row to `pass`.
- 2026-04-24: M4 parser cleanup found that smoke row fields must be explicitly present, even when an empty string is allowed for RC evidence. A regression case now rejects missing required smoke fields.
- 2026-04-24: M5 test-first red check failed in the expected places: placeholder release script text, missing tracked release-notes workflow behavior, missing public contributor/tool wording, and RC metadata still recording `placeholder_release_check: fail`.
- 2026-04-24: `bash scripts/release-verify.sh v0.1.0-rc.1` is now the first full non-smoke RC release gate. It does not claim hosted CI passed; it only proves the local repository-owned checks.

## Validation notes

- 2026-04-24: Planning-stage formatting passed with `git diff --check -- docs/plan.md docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md specs/multi-agent-adapters-first-public-release.md docs/architecture/2026-04-24-multi-agent-adapter-distribution.md docs/adr/ADR-20260424-generated-adapter-packages.md`.
- 2026-04-24: Lifecycle validation passed with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md --path docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md --path specs/multi-agent-adapters-first-public-release.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/adr/ADR-20260424-generated-adapter-packages.md`. The validator reported `validated 4 artifact files in explicit-paths mode`; `docs/plan.md` and concrete plan files are checked by the formatting proof and lifecycle references, while the lifecycle validator currently classifies proposal, spec, architecture, and ADR files.
- 2026-04-24: Test-spec authoring validation passed with `git diff --check -- specs/multi-agent-adapters-first-public-release.test.md docs/plan.md docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md specs/multi-agent-adapters-first-public-release.md docs/architecture/2026-04-24-multi-agent-adapter-distribution.md docs/adr/ADR-20260424-generated-adapter-packages.md`.
- 2026-04-24: Test-spec lifecycle validation passed with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/multi-agent-adapters-first-public-release.test.md --path docs/plan.md --path docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md --path docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md --path specs/multi-agent-adapters-first-public-release.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/adr/ADR-20260424-generated-adapter-packages.md`.
- 2026-04-24: M1 test-first red check passed as expected with `python scripts/test-adapter-distribution.py`, which failed because `scripts/adapter_distribution.py` did not exist yet.
- 2026-04-24: M1 adapter regression tests passed with `python scripts/test-adapter-distribution.py`.
- 2026-04-24: M1 canonical skill validation passed with `python scripts/validate-skills.py`.
- 2026-04-24: M1 change metadata validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M1 formatting validation passed with `git diff --check -- scripts tests docs/changes/2026-04-24-multi-agent-adapters-first-public-release docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`.
- 2026-04-24: M1 milestone commit command prepared as `git add ... && git commit -m "M1: add adapter portability core"`.
- 2026-04-24: M1 review-fix red check passed as expected with `python scripts/test-adapter-distribution.py`, which failed because the unsupported-frontmatter manifest reason was not quoted.
- 2026-04-24: M1 review-fix adapter regression tests passed with `python scripts/test-adapter-distribution.py`.
- 2026-04-24: M1 review-fix canonical skill validation passed with `python scripts/validate-skills.py`.
- 2026-04-24: M1 review-fix change metadata validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M1 review-fix formatting validation passed with `git diff --check -- scripts tests docs/changes/2026-04-24-multi-agent-adapters-first-public-release docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`.
- 2026-04-24: M1 review-fix lifecycle validation passed with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/multi-agent-adapters-first-public-release.test.md --path docs/plan.md --path docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md --path docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md --path specs/multi-agent-adapters-first-public-release.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/adr/ADR-20260424-generated-adapter-packages.md --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M1 rereview-fix red check passed as expected with `python scripts/test-adapter-distribution.py`, which failed on the new invalid-body and partial-portability cases before the implementation fix.
- 2026-04-24: M1 rereview-fix adapter regression tests passed with `python scripts/test-adapter-distribution.py`.
- 2026-04-24: M1 rereview-fix canonical skill validation passed with `python scripts/validate-skills.py`.
- 2026-04-24: M1 rereview-fix change metadata validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M1 rereview-fix formatting validation passed with `git diff --check -- scripts tests docs/changes/2026-04-24-multi-agent-adapters-first-public-release docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`.
- 2026-04-24: M1 rereview-fix lifecycle validation passed with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/multi-agent-adapters-first-public-release.test.md --path docs/plan.md --path docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md --path docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md --path specs/multi-agent-adapters-first-public-release.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/adr/ADR-20260424-generated-adapter-packages.md --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M2 test-first red check passed as expected with `python scripts/test-adapter-distribution.py`, which failed because adapter generation helpers were not implemented yet.
- 2026-04-24: M2 adapter regression tests passed with `python scripts/test-adapter-distribution.py`.
- 2026-04-24: M2 RC adapter generation passed with `python scripts/build-adapters.py --version 0.1.0-rc.1`.
- 2026-04-24: M2 RC adapter drift check passed with `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`.
- 2026-04-24: M2 required entrypoint checks passed with `test -f dist/adapters/codex/AGENTS.md`, `test -f dist/adapters/claude/CLAUDE.md`, `test -f dist/adapters/opencode/AGENTS.md`, and `test -f dist/adapters/manifest.yaml`.
- 2026-04-24: M2 change metadata validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M2 formatting validation passed with `git diff --check -- scripts tests dist docs/changes/2026-04-24-multi-agent-adapters-first-public-release docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`.
- 2026-04-24: M3 adapter-validation red check passed as expected with `python scripts/test-adapter-distribution.py`, which failed because `validate_adapter_output` was not implemented yet.
- 2026-04-24: M3 lifecycle red check passed as expected with `python scripts/test-artifact-lifecycle-validator.py`, which failed because explicit `dist/adapters/*` paths were not yet rejected as generated output.
- 2026-04-24: M3 adapter regression tests passed with `python scripts/test-adapter-distribution.py`.
- 2026-04-24: M3 generated adapter drift check passed with `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`.
- 2026-04-24: M3 generated adapter validation passed with `python scripts/validate-adapters.py --version 0.1.0-rc.1`.
- 2026-04-24: M3 artifact lifecycle regression tests passed with `python scripts/test-artifact-lifecycle-validator.py`.
- 2026-04-24: M3 CI wrapper validation passed with `bash scripts/ci.sh`. The CI output included `python scripts/test-adapter-distribution.py`, `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`, and `python scripts/validate-adapters.py --version 0.1.0-rc.1`.
- 2026-04-24: M3 change metadata validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M3 formatting validation passed with `git diff --check -- scripts tests dist docs/changes/2026-04-24-multi-agent-adapters-first-public-release docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`.
- 2026-04-24: M4 release-validation red check passed as expected with `python scripts/test-adapter-distribution.py`, which failed because `validate_release_output` was not implemented yet.
- 2026-04-24: M4 adapter and release regression tests passed with `python scripts/test-adapter-distribution.py`.
- 2026-04-24: M4 release metadata validation passed with `python scripts/validate-release.py --version v0.1.0-rc.1`.
- 2026-04-24: M4 adapter validation still passed with `python scripts/validate-adapters.py --version 0.1.0-rc.1`.
- 2026-04-24: M4 formatting validation passed with `git diff --check -- scripts tests docs/releases docs/changes/2026-04-24-multi-agent-adapters-first-public-release docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`.
- 2026-04-24: M4 change metadata validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M4 lifecycle validation passed with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/explain-change.md --path docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md --path docs/releases/v0.1.0-rc.1/release.yaml --path docs/releases/v0.1.0-rc.1/release-notes.md`.
- 2026-04-24: M4 CI wrapper validation passed with `bash scripts/ci.sh`.
- 2026-04-24: M4 post-commit release metadata validation passed with `python scripts/validate-release.py --version v0.1.0-rc.1`.
- 2026-04-24: M4 post-commit lifecycle validation passed with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/explain-change.md --path docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md --path docs/releases/v0.1.0-rc.1/release.yaml --path docs/releases/v0.1.0-rc.1/release-notes.md`.
- 2026-04-24: M4 post-commit CI wrapper validation passed with `bash scripts/ci.sh`; push-main artifact lifecycle validation reported unrelated pre-existing proposal warnings and passed.
- 2026-04-24: M4 final verification passed with `python scripts/test-adapter-distribution.py`, `python scripts/validate-release.py --version v0.1.0-rc.1`, `python scripts/validate-adapters.py --version 0.1.0-rc.1`, `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`, explicit artifact lifecycle validation for the M4 release artifacts, `git diff --check -- HEAD~2..HEAD`, and `bash scripts/ci.sh`.
- 2026-04-24: M5 test-first red check passed as expected with `python scripts/test-adapter-distribution.py`, which failed on the placeholder release script, missing tracked-notes workflow behavior, missing public docs wording, and RC metadata still recording the placeholder gate as `fail`.
- 2026-04-24: M5 adapter distribution and release-gate regression tests passed with `python scripts/test-adapter-distribution.py`.
- 2026-04-24: M5 actual RC release verification passed with `bash scripts/release-verify.sh v0.1.0-rc.1`.
- 2026-04-24: M5 CI wrapper validation passed with `bash scripts/ci.sh`.
- 2026-04-24: M5 placeholder text rejection passed with `bash -c "! rg -n 'Replace this script with repository-specific release checks|TODO: release checks|placeholder release check' scripts/release-verify.sh"`.
- 2026-04-24: M5 public docs coverage check passed with `rg -n 'codex|claude|opencode|dist/adapters|\\.codex/skills|not need all supported tools' README.md docs/workflows.md AGENTS.md docs/releases/v0.1.0-rc.1/release-notes.md`.
- 2026-04-24: M5 formatting validation passed with `git diff --check -- scripts .github README.md docs AGENTS.md dist`.
- 2026-04-24: M5 change metadata validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M5 lifecycle validation passed with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/explain-change.md --path docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md --path docs/releases/v0.1.0-rc.1/release.yaml --path docs/releases/v0.1.0-rc.1/release-notes.md --path README.md --path docs/workflows.md --path AGENTS.md`.
- 2026-04-24: M5 review-resolution update added the missing T12/E8 public-doc statement that adapter compatibility claims are versioned and external tool contract changes require lifecycle revision before changing release claims.
- 2026-04-24: M5 review-resolution regression passed with `python scripts/test-adapter-distribution.py`.
- 2026-04-24: M5 review-resolution docs evidence check passed with `rg -n 'external tool contracts|before changing release claims|codex|claude|opencode|dist/adapters|\\.codex/skills|not need all supported tools' README.md docs/workflows.md AGENTS.md docs/releases/v0.1.0-rc.1/release-notes.md`.
- 2026-04-24: M5 review-resolution formatting validation passed with `git diff --check -- README.md docs/releases/v0.1.0-rc.1/release-notes.md scripts/test-adapter-distribution.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml docs/changes/2026-04-24-multi-agent-adapters-first-public-release/explain-change.md docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`.
- 2026-04-24: M5 review-resolution release verification passed with `bash scripts/release-verify.sh v0.1.0-rc.1`.
- 2026-04-24: M5 review-resolution CI wrapper validation passed with `bash scripts/ci.sh`.
- 2026-04-24: M5 review-resolution change metadata validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: M5 review-resolution lifecycle validation passed with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml --path docs/changes/2026-04-24-multi-agent-adapters-first-public-release/explain-change.md --path docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md --path docs/releases/v0.1.0-rc.1/release.yaml --path docs/releases/v0.1.0-rc.1/release-notes.md --path README.md --path docs/workflows.md --path AGENTS.md`.
- 2026-04-24: M5 verify passed with `bash scripts/release-verify.sh v0.1.0-rc.1`, `bash scripts/ci.sh`, placeholder text rejection, docs evidence `rg`, `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`, explicit artifact lifecycle validation, and `git diff --check -- 8e28920..HEAD`.
- 2026-04-24: M5 verify observed unrelated pre-existing proposal warnings from `bash scripts/ci.sh` push-main lifecycle validation; the CI wrapper still passed and validated five related artifact files.
- 2026-04-24: M5 explain-change closeout validation passed with change metadata validation, explicit artifact lifecycle validation, and `git diff --check` for the change-local explanation, change metadata, and plan body.
- 2026-04-24: Branch code-review regression tests failed as expected with `python scripts/test-adapter-distribution.py` before the fix. The new failures covered the over-broad `.codex/skills` install-location rule and missing/malformed canonical skill source handling.
- 2026-04-24: Branch code-review regression tests passed after the fix with `python scripts/test-adapter-distribution.py`.
- 2026-04-24: Branch code-review adapter drift validation passed with `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`.
- 2026-04-24: Branch code-review adapter validation passed with `python scripts/validate-adapters.py --version 0.1.0-rc.1`.
- 2026-04-24: Branch code-review release verification passed with `bash scripts/release-verify.sh v0.1.0-rc.1`.
- 2026-04-24: Branch code-review CI wrapper validation passed with `bash scripts/ci.sh`.
- 2026-04-24: Branch code-review change metadata validation passed with `python scripts/validate-change-metadata.py docs/changes/2026-04-24-multi-agent-adapters-first-public-release/change.yaml`.
- 2026-04-24: Branch code-review explicit artifact lifecycle validation passed for the touched change-local artifacts, plan, adapter script, adapter tests, and new adapter fixture with `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.
- 2026-04-24: Branch code-review formatting validation passed with `git diff --check -- scripts tests docs`.

## Review record

- 2026-04-24: First-pass `code-review` for `d112f98..e3bc21e` returned `clean-with-notes`.
  - Review surface: M4 release metadata validator, RC release artifacts, regression tests, change-local artifacts, and active plan updates.
  - Findings: no blocking or required-change findings.
  - Direct proof: `python scripts/test-adapter-distribution.py`, `python scripts/validate-release.py --version v0.1.0-rc.1`, `python scripts/validate-adapters.py --version 0.1.0-rc.1`, explicit lifecycle validation, and `bash scripts/ci.sh` passed against tracked branch state.
  - Residual risk: M4 is not RC-publication-ready until M5 replaces the placeholder release gate and changes `placeholder_release_check` to `pass`.
- 2026-04-24: First-pass `code-review` for `8e28920..4c9b1dc` returned `changes-requested`.
  - Review surface: M5 release gate replacement, release workflow, public docs, regression tests, change-local artifacts, and active plan updates.
  - Finding: public docs did not state the T12/E8 rule that adapter compatibility claims are versioned and external tool contract changes must go through the lifecycle before changing release claims.
  - Resolution: README and RC release notes now carry the missing claim-boundary wording, and `scripts/test-adapter-distribution.py` asserts the wording remains present.
- 2026-04-24: Second-pass `code-review` for `8e28920..76ab918` returned `clean-with-notes`.
  - Review surface: complete M5 release gate replacement plus the review-resolution fix.
  - Findings: no blocking or required-change findings remain.
  - Direct proof: `python scripts/test-adapter-distribution.py`, `bash scripts/release-verify.sh v0.1.0-rc.1`, `bash scripts/ci.sh`, change metadata validation, explicit lifecycle validation, docs evidence `rg`, and diff checks passed after review resolution.
- 2026-04-24: Branch-level `code-review` after M5 closeout returned `changes-requested`.
  - Review surface: full branch diff from the tracked upstream through M5 explain-change closeout.
  - Findings: `.codex/skills` references were over-rejected when adapter alternatives were present, and missing or malformed canonical skill inputs were not directly blocking adapter generation and validation.
  - Resolution: added regression tests for both findings, narrowed the `.codex/skills` only-install-location rule, and made canonical skill source errors fail generation and validation directly.

## Outcome and retrospective

This plan is active. M1 through M5 are complete and verified; M6 remains open.

Plan review is complete and the matching test spec is active.

## Readiness

Immediate next repository stage: `code-review` rerun for the branch-level review findings.

Next expected milestone after review and verification: M6, maintainer smoke and stable `v0.1.0` closeout.

## Risks and follow-ups

- Follow-up after stable release: decide whether `.codex/skills/` should remain as a local generated mirror or eventually be replaced by `dist/adapters/codex/`.
- Follow-up after first external use: reassess whether generated packages should move to package-manager, plugin, or marketplace distribution.
- Follow-up if many skills are excluded: create a portability-improvement initiative rather than weakening the portable-core gate.
