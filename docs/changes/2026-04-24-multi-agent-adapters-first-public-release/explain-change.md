# Multi-agent adapters first public release change explanation

## M1 adapter portability core

M1 adds the shared adapter distribution core before any generated package output is written.

The new adapter model defines the approved first-public-release tools and target paths for Codex, Claude Code, and opencode. This keeps later generator and validator work tied to one source for adapter roots, instruction entrypoints, and per-tool skill locations.

The portable-core validator classifies one canonical `SKILL.md` at a time. It validates portable names and descriptions, permits explicitly transformed `argument-hint` metadata for non-Codex adapters, rejects unsupported frontmatter or Codex-only assumptions from non-Codex adapters, and records deterministic inclusion decisions for later manifest generation.

The fixture-driven tests cover the M1 proof surface from the active test spec: adapter path contracts, portable skill inclusion, invalid metadata rejection, Codex-only exclusion reasons, generic artifact path portability, explicit transforms, and deterministic manifest rendering for partial portability.

No `dist/adapters/` files are generated in M1. Generated adapter packages are planned for M2 after the adapter core is reviewable.

## M1 review resolution

The first M1 code-review pass found that manifest exclusion reasons could be rendered as invalid YAML when the human-readable reason contained `: `, such as `Uses unsupported frontmatter: codex-only-field.`.

The follow-up quotes generated manifest reason strings and escapes double-quoted YAML control characters before rendering. The adapter regression suite now includes the unsupported-frontmatter fixture as a manifest-rendering case so the colon-bearing reason path remains covered before M2 writes `dist/adapters/manifest.yaml`.

The rereview follow-up also makes the portable-core gate reuse the repository `SKILL.md` body checks before any adapter can include a skill. New `invalid-body` and `partial-portability` fixtures prove invalid Markdown instruction content is excluded from every adapter and that a skill explicitly incompatible with opencode can still be listed for Codex and Claude Code with a manifest reason.

## M2 adapter package generation

M2 turns the M1 portability decisions into tracked RC adapter package output.

The shared adapter distribution module now exposes deterministic expected-file generation, drift collection, and output synchronization for `dist/adapters/`. The generator reads canonical skills from `skills/`, renders thin adapter entrypoints from `scripts/adapter_templates/`, writes each included skill to the target adapter skill root, and renders `dist/adapters/manifest.yaml` for the requested version.

`scripts/build-adapters.py` is a thin CLI around those helpers. In write mode it synchronizes the generated tree and removes unexpected files; in check mode it fails on missing, stale, or unexpected generated adapter output. The first generated package set is tracked with manifest version `0.1.0-rc.1`.

The generated Codex package preserves canonical skill files under `.agents/skills/`. Claude Code and opencode packages drop the Codex-specific `argument-hint` frontmatter through the explicit M1 transform before writing `.claude/skills/` and `.opencode/skills/` files. The entrypoint templates stay thin: they identify the package as generated adapter output, point maintainers back to canonical sources, name the target skill directory, and do not duplicate skill bodies.

The M2 tests cover independent package roots, required entrypoints, template thinness, deterministic manifest versions, transform application, stale drift detection, unexpected generated file detection, and write-mode cleanup of unexpected generated files.

## M3 adapter validation and CI integration

M3 adds the repository-owned adapter validation gate around the generated package output.

`scripts/validate-adapters.py` validates the tracked `dist/adapters/` tree for a requested manifest version. The shared adapter distribution module now parses the constrained generated manifest, checks required adapter directories and instruction entrypoints, compares manifest records with canonical portability decisions, verifies generated skill files are listed in the manifest, rejects non-Codex metadata leaks such as `argument-hint`, and scans generated adapter files plus authored templates for high-signal security markers.

The security scan is intentionally narrow for this milestone. It rejects private key delimiters, common secret assignments, machine-local absolute paths, and explicit permission-bypass language without flagging ordinary skill text about permissions or secrets.

`scripts/ci.sh` now runs adapter regression tests, adapter drift checks, and adapter validation after the existing `.codex/skills/` drift check. It also filters `dist/adapters/*` from authored artifact lifecycle validation for the same reason `.codex/skills/*` is filtered: generated outputs are checked by drift and adapter validators, not by lifecycle artifact rules.

The artifact lifecycle validator now treats explicit `dist/adapters/*` inputs as generated output instead of accepting them as authored source. This preserves the source-of-truth boundary while still allowing CI to validate generated files through adapter-specific checks.

## M4 release metadata validation and RC evidence

M4 adds target-version-scoped validation for `docs/releases/<version>/release.yaml` and `release-notes.md`.

`scripts/validate-release.py --version v0.1.0-rc.1` reads only that versioned release directory, compares the release metadata to the generated `dist/adapters/manifest.yaml`, checks the expected Codex, Claude Code, and opencode adapter paths and entrypoints, validates RC and final smoke-row rules, checks release notes version and supported-tool consistency, and scans the release metadata and notes for high-signal security markers.

The `v0.1.0-rc.1` metadata records smoke rows as `not-run` with maintainer ownership because manual adapter smoke is intentionally later. It also records `placeholder_release_check: fail` because `scripts/release-verify.sh` is still the placeholder gate until M5. This keeps the release evidence truthful while allowing the metadata shape, notes consistency, generated package sync, and security checks to validate now.

The M4 regression tests cover valid RC metadata, manifest-version and supported-tool mismatches, RC smoke failures, missing required smoke fields, final-release smoke strictness, release-note security scanning, and the repository `validate-release.py` CLI path. The final verification pass reran the adapter distribution tests, adapter validation, release metadata validation, change metadata validation, explicit lifecycle validation for the release artifacts, formatting checks, and `bash scripts/ci.sh`.

M4 intentionally does not make `v0.1.0-rc.1` publication-ready. The remaining release gate replacement and public documentation work belongs to M5, and stable `v0.1.0` remains blocked on maintainer smoke in M6.

## M5 release gate replacement and public docs

M5 replaces the checklist-only release script with a repository-owned release gate for `v0.1.0-rc.1` and `v0.1.0`.

`scripts/release-verify.sh` now accepts an explicit tag or falls back to `GITHUB_REF_NAME`, derives the adapter manifest version from the tag, rejects unsupported release targets, checks that the release script is not still a placeholder, and invokes the required repository-owned checks: skill validation, skill regression validation, `.codex/skills` drift, adapter regression tests, adapter drift, adapter validation, release metadata validation, and the security scans embedded in adapter and release validation.

`.github/workflows/release.yml` now passes the tag to release verification and creates GitHub releases from `docs/releases/<tag>/release-notes.md` instead of generated notes. RC tags are marked prerelease and are not marked latest.

The public docs now describe the generated Codex, Claude Code, and opencode adapter packages under `dist/adapters/`, show the support matrix paths, explain how to install one adapter by copying its package root into a project, and distinguish canonical `skills/`, generated public `dist/adapters/`, and generated local `.codex/skills/`. They also state that ordinary contributors do not need all supported tools installed locally for non-smoke validation, and that adapter compatibility claims must be revised through the lifecycle before release claims change when external tool contracts change.

The `v0.1.0-rc.1` release metadata now records `placeholder_release_check: pass`, because the placeholder release gate has been replaced. The RC release notes now identify `bash scripts/release-verify.sh v0.1.0-rc.1` as the release gate and keep manual adapter smoke as the remaining limitation before stable `v0.1.0`.

The M5 tests cover the release script dry-run command contract, fallback to `GITHUB_REF_NAME`, tracked release notes in the GitHub workflow, public docs source-boundary wording, external tool contract lifecycle wording, and the updated release metadata placeholder status. The actual release gate was also run directly for `v0.1.0-rc.1`.

Post-review M5 verification reran `bash scripts/release-verify.sh v0.1.0-rc.1`, `bash scripts/ci.sh`, placeholder text rejection, public docs evidence checks, change metadata validation, explicit artifact lifecycle validation, and `git diff --check -- 8e28920..HEAD`. The CI wrapper passed with unrelated pre-existing proposal warnings from push-main lifecycle validation. Stable `v0.1.0` remains blocked on M6 maintainer smoke.

## Post-review adapter contract hardening

The branch-level code review found two adapter contract gaps after M5 closeout. First, the portable-core `.codex/skills` rule was too broad: `R23` rejects `.codex/skills` only when it is the only install location, so adapter-aware explanatory references must remain portable. The fix adds the `codex-install-with-alternatives` fixture and narrows the non-Codex exclusion rule to allow `.codex/skills` when the same skill also identifies public adapter package alternatives.

Second, adapter generation and validation could treat missing or malformed canonical skill input as empty or excluded output. The fix adds regression coverage for malformed canonical skills and missing skill roots, makes adapter output synchronization fail before writing generated files when canonical skill validation fails, and makes adapter validation report canonical source errors directly.

The post-review regression pass first failed on those new cases, then passed after the implementation fix. The follow-up validation reran `python scripts/test-adapter-distribution.py`, `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`, `python scripts/validate-adapters.py --version 0.1.0-rc.1`, `bash scripts/release-verify.sh v0.1.0-rc.1`, `bash scripts/ci.sh`, change metadata validation, explicit artifact lifecycle validation, and formatting checks.

## M6 stable release closeout

M6 records the maintainer smoke matrix and moves the generated adapter package set from RC to stable `0.1.0`.

The smoke checks copied each adapter package root into a clean project root and verified that the tool could see the expected instruction entrypoint and `workflow` skill path. The recorded tool versions are `codex-cli 0.124.0`, `2.1.119 (Claude Code)`, and `opencode 1.14.22`; the stable release metadata records one passing smoke row for each supported tool.

The adapter generator default, CI wrapper, public validation commands, generated entrypoints, and `dist/adapters/manifest.yaml` now target `0.1.0`. Historical RC release artifacts remain version-scoped under `docs/releases/v0.1.0-rc.1/`; the active stable release artifacts live under `docs/releases/v0.1.0/`.

The stable release notes keep the support matrix aligned with the manifest and avoid claiming hosted runtime, registry publication, package-manager installation, or guaranteed identical runtime behavior across tools. The final release gate `bash scripts/release-verify.sh v0.1.0` passed after generated adapter drift, adapter validation, release metadata validation, release notes consistency, security scans, and the full CI wrapper passed.

## M6 post-verify lifecycle closeout

After the M6 code-review returned `clean-with-notes` and verify returned `ready`, the plan lifecycle moved from Active to Done in both `docs/plan.md` and the concrete plan body. This closeout does not create new release behavior; it records that the already-reviewed stable adapter package set, smoke evidence, release metadata, release notes, generated-output drift checks, and CI wrapper are synchronized.

The next workflow stage is `pr`. Hosted CI and actual tag publication remain downstream evidence, not claims made by this explanation artifact.
