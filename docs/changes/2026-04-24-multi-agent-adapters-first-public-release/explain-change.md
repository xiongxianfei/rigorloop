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
