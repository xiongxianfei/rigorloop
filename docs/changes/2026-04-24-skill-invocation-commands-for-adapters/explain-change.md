# Skill invocation commands change explanation

## M1 OpenCode command alias generation

M1 adds the generated OpenCode command alias layer required by the approved `v0.1.1` adapter contract.

The shared adapter distribution module now has a single `OPENCODE_COMMAND_ALIASES` tuple for the curated lifecycle command set. Adapter generation uses that tuple to render deterministic markdown command files under `dist/adapters/opencode/.opencode/commands/`. Each generated command file is a thin wrapper with YAML `description` frontmatter, an instruction to load and follow the matching RigorLoop skill, and `$ARGUMENTS` pass-through. The renderer does not copy canonical skill bodies or add model, agent, permission, shell, or file-reference behavior.

The generated manifest now includes `command_aliases.opencode.count` and exact repository-relative alias paths for the same curated set. The manifest parser was extended with a constrained `CommandAliasSection` model so validation can compare declared aliases against generated files instead of relying on counts alone.

Adapter validation now rejects missing aliases, unexpected aliases, non-curated aliases, aliases whose matching OpenCode skill is absent, manifest paths outside `dist/adapters/opencode/.opencode/commands/`, key/stem mismatches, unsupported command alias tool sections, stale alias bodies, and unsafe alias content. Claude Code remains wrapper-free; validation rejects a generated `.claude/commands/` directory.

The tracked adapter output was regenerated for adapter package version `0.1.1`, and the adapter default plus CI adapter drift checks now target `0.1.1`. Existing `v0.1.0` release validation remains covered by isolated release metadata fixtures because the tracked adapter tree now represents the next patch package rather than the already shipped stable package.

M1 intentionally does not add README usage examples, adapter entrypoint invocation guidance, `v0.1.1` release metadata, release notes, or OpenCode smoke evidence. Those remain owned by M2 and M3 in the active plan.

## M2 tool-native invocation documentation

M2 adds the README and generated entrypoint guidance needed for users to invoke the generated adapter skills without assuming cross-tool syntax parity.

The Claude Code entrypoint template now documents native Claude Code slash commands for project skills, with TUI examples for `/proposal`, `/spec`, `/implement`, `/code-review`, and `/pr`. It keeps Claude Code skill-native by leaving `.claude/skills/` as the install surface and by not generating or documenting `.claude/commands/` wrappers.

The OpenCode entrypoint template now distinguishes `.opencode/skills/` as the reusable skill surface from `.opencode/commands/` as a thin command-alias layer for only the curated lifecycle set. It includes the same TUI slash-command examples and explicitly says that non-aliased portable skills remain available as skills.

The README now mirrors those tool-specific examples, updates adapter validation commands to the current `0.1.1` generated package version, and avoids one-shot CLI examples because M3 has not yet recorded smoke evidence for any one-shot command form.

## M3 v0.1.1 release metadata and smoke-backed one-shot usage

M3 turns the command-alias package into a release-verifiable `v0.1.1` patch target.

Release validation now recognizes `v0.1.1` as a final release with adapter manifest version `0.1.1`. For manifest versions that support OpenCode command aliases, release notes validation requires the OpenCode alias set, Claude Code skill-native guidance, and the smoke-backed `opencode run --command proposal` one-shot form. Release smoke validation now rejects vague OpenCode evidence and requires evidence that the one-shot command alias loaded or followed the matching `proposal` skill and carried command arguments through.

The repository release gate now accepts `v0.1.1`, and `docs/releases/v0.1.1/release.yaml` records passing maintainer smoke for Codex, Claude Code, and OpenCode. The OpenCode row records `1.14.22` and evidence that `opencode run --command proposal` was smoke-tested through a copied adapter root, loaded the `proposal` skill, and repeated `ARGUMENT_MARKER_M3_SMOKE` from the command arguments.

The `v0.1.1` release notes describe the generated adapter package set, all supported tools, the exact curated OpenCode command aliases, Claude Code skill-native usage, and the smoke evidence. README and the generated OpenCode entrypoint now include the OpenCode one-shot example because M3 supplied matching smoke evidence. Claude Code one-shot examples remain omitted because no Claude one-shot command form is part of this release contract.

The workflow summary now points current structural release checks at `0.1.1` and lists `v0.1.1` as a supported release verification target, keeping public operational docs aligned with the generated adapter package version.
