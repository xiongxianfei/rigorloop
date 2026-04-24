# Skill Invocation Commands for Adapter Packages

## Status
- approved

## Related proposal

- [Skill Invocation Commands for Adapter Packages](../docs/proposals/2026-04-24-skill-invocation-commands-for-adapters.md)

## Goal and context

This spec defines the `v0.1.1` adapter usability contract for invoking RigorLoop skills from Claude Code and OpenCode. It extends the generated adapter package contract from `v0.1.0` without changing canonical skill behavior, skill source ownership, or workflow semantics.

The change adds documentation for tool-native skill invocation and generates thin OpenCode command aliases for a curated lifecycle command set. Command aliases are a usability layer only. The canonical reusable behavior remains in `skills/<skill-name>/SKILL.md` and generated adapter skill copies under `.opencode/skills/` or `.claude/skills/`.

External tool contracts were checked against official docs on 2026-04-24:

- Claude Code skills can be invoked directly with `/skill-name`, and `.claude/commands/` has been merged into skills: <https://code.claude.com/docs/en/skills>
- OpenCode project skills are discovered from `.opencode/skills/<name>/SKILL.md` and loaded through the native `skill` tool: <https://opencode.ai/docs/skills>
- OpenCode project commands are markdown files under `.opencode/commands/`, are invoked as `/command-name`, and support `$ARGUMENTS`: <https://opencode.ai/docs/commands/>

## Glossary

- adapter package: a generated, tracked directory under `dist/adapters/<adapter>/` that can be copied into a project root.
- alias command: a generated OpenCode markdown command file that routes a user command to the matching RigorLoop skill.
- canonical skill: an authored RigorLoop skill under `skills/<skill-name>/SKILL.md`.
- command alias path: a repository-relative POSIX path to a generated OpenCode command alias file.
- curated lifecycle command set: the exact OpenCode command aliases approved for v1 usability: `proposal`, `proposal-review`, `spec`, `spec-review`, `plan`, `plan-review`, `test-spec`, `implement`, `code-review`, and `pr`.
- generated adapter output: deterministic files under `dist/adapters/`.
- skill invocation guidance: user-facing examples and instructions that explain how to invoke RigorLoop skills in a target tool.
- tool slug: the stable adapter key used in manifests and release metadata, such as `claude` or `opencode`.

## Examples first

### Example E1: OpenCode adapter includes curated command aliases

Given adapter generation runs for version `0.1.1`
When the `opencode` adapter package is generated
Then `dist/adapters/opencode/.opencode/commands/proposal.md` exists
And `dist/adapters/opencode/.opencode/commands/code-review.md` exists
And no command alias is generated for `workflow`, `verify`, `explore`, or any skill outside the curated lifecycle command set.

### Example E2: OpenCode skills remain fully available

Given the generated `opencode` adapter includes all portable skills under `.opencode/skills/`
When command aliases are generated
Then every included portable skill remains available under `dist/adapters/opencode/.opencode/skills/<skill-name>/SKILL.md`
And only the curated lifecycle command set receives matching `.opencode/commands/<skill-name>.md` aliases.

### Example E3: OpenCode command alias is thin

Given the generated `proposal` command alias exists
When a reviewer opens `dist/adapters/opencode/.opencode/commands/proposal.md`
Then the file contains only OpenCode command frontmatter and a short prompt that instructs OpenCode to load and follow the `proposal` skill
And the file does not duplicate the body of `skills/proposal/SKILL.md`.

### Example E4: manifest records exact command paths

Given adapter generation runs for version `0.1.1`
When `dist/adapters/manifest.yaml` is generated
Then it records the exact path `dist/adapters/opencode/.opencode/commands/proposal.md` for the `proposal` OpenCode command alias
And it records exact paths for all other curated OpenCode command aliases.

### Example E5: validation rejects unexpected aliases

Given `dist/adapters/opencode/.opencode/commands/verify.md` exists
And `verify` is not in the curated lifecycle command set
When adapter validation runs
Then validation fails with an error that identifies `opencode`, `verify`, and the unexpected command alias path.

### Example E6: validation rejects manifest drift

Given the manifest declares the OpenCode `spec` command alias path
And `dist/adapters/opencode/.opencode/commands/spec.md` is missing or has stale generated content
When adapter validation or adapter drift checking runs
Then validation fails before release verification can pass.

### Example E7: Claude Code stays skill-native

Given the Claude Code adapter package is generated
When the user reads `dist/adapters/claude/CLAUDE.md`
Then the file shows TUI slash-command examples such as `/proposal` and `/code-review`
And the package does not generate `.claude/commands/` wrappers for RigorLoop skills.

### Example E8: README examples distinguish TUI and one-shot usage

Given README adapter usage documentation is rendered for `v0.1.1`
When a user reads the Claude Code examples
Then Claude Code usage is shown with TUI slash-command examples unless a Claude one-shot form has been smoke-tested
And OpenCode usage may show both TUI slash-command aliases and `opencode run --command ...` examples when the one-shot form is smoke-tested.

## Requirements

R1. This change MUST preserve canonical skill ownership: authored RigorLoop skill behavior remains under `skills/<skill-name>/SKILL.md`.

R2. Generated command aliases MUST NOT become a source of truth for RigorLoop skill behavior.

R3. The OpenCode adapter package MUST continue to include all portable skills selected for the `opencode` adapter under:

```text
dist/adapters/opencode/.opencode/skills/<skill-name>/SKILL.md
```

R4. The OpenCode adapter package MUST generate command aliases only for the curated lifecycle command set:
- `proposal`;
- `proposal-review`;
- `spec`;
- `spec-review`;
- `plan`;
- `plan-review`;
- `test-spec`;
- `implement`;
- `code-review`;
- `pr`.

R5. The OpenCode adapter package MUST NOT generate command aliases for included portable skills outside the curated lifecycle command set.

R6. The OpenCode adapter package MUST NOT generate a command alias for a curated lifecycle command unless the matching skill is included in the `opencode` adapter package.

R7. Each generated OpenCode command alias MUST be written to:

```text
dist/adapters/opencode/.opencode/commands/<skill-name>.md
```

R8. Each generated OpenCode command alias file MUST use the command name as the markdown filename stem.

R9. Each generated OpenCode command alias MUST contain YAML frontmatter with a `description` field.

R10. Each generated OpenCode command alias body MUST be a thin prompt that instructs OpenCode to load and follow the matching RigorLoop skill.

R11. Each generated OpenCode command alias body MUST pass user-provided command arguments through `$ARGUMENTS`.

R12. Generated OpenCode command aliases MUST NOT duplicate the full body of the matching `SKILL.md`.

R13. Generated OpenCode command aliases MUST NOT include shell-output interpolation, file-reference interpolation, model overrides, agent overrides, or permission policy changes.

R14. Generated OpenCode command aliases MUST be deterministic for the same canonical skills, adapter templates, curated command set, and adapter version.

R15. Adapter drift checking MUST fail when an expected generated OpenCode command alias is missing, stale, or modified by hand.

R16. Adapter validation MUST fail when an unexpected OpenCode command alias exists under `dist/adapters/opencode/.opencode/commands/`.

R17. Adapter validation MUST fail when a generated OpenCode command alias maps to a skill that is absent from the generated `opencode` adapter skill tree.

R18. Adapter validation MUST fail when a generated OpenCode command alias exists for a skill outside the curated lifecycle command set.

R19. `dist/adapters/manifest.yaml` MUST record exact generated OpenCode command alias paths as repository-relative POSIX paths.

R20. `dist/adapters/manifest.yaml` MUST map each OpenCode command alias name to the exact generated command alias path.

R21. `dist/adapters/manifest.yaml` MUST use this command alias shape:

```yaml
command_aliases:
  opencode:
    count: 10
    aliases:
      proposal: dist/adapters/opencode/.opencode/commands/proposal.md
      proposal-review: dist/adapters/opencode/.opencode/commands/proposal-review.md
      spec: dist/adapters/opencode/.opencode/commands/spec.md
      spec-review: dist/adapters/opencode/.opencode/commands/spec-review.md
      plan: dist/adapters/opencode/.opencode/commands/plan.md
      plan-review: dist/adapters/opencode/.opencode/commands/plan-review.md
      test-spec: dist/adapters/opencode/.opencode/commands/test-spec.md
      implement: dist/adapters/opencode/.opencode/commands/implement.md
      code-review: dist/adapters/opencode/.opencode/commands/code-review.md
      pr: dist/adapters/opencode/.opencode/commands/pr.md
```

R22. The manifest `command_aliases.opencode.count` value MUST equal the number of entries under `command_aliases.opencode.aliases`.

R23. Adapter validation MUST fail when the manifest declares a command alias path that does not exist.

R24. Adapter validation MUST fail when the manifest omits an OpenCode command alias file that exists in the generated adapter package.

R25. Adapter validation MUST fail when a manifest command alias path points outside `dist/adapters/opencode/.opencode/commands/`.

R26. Adapter validation MUST fail when a manifest command alias key differs from the command alias filename stem.

R27. Adapter validation MUST fail when `command_aliases` includes command alias sections for unsupported tools or for tools that do not generate aliases in this spec.

R28. The Claude Code adapter package MUST NOT generate `.claude/commands/` wrappers for RigorLoop skills.

R29. The Claude Code adapter entrypoint MUST document native skill invocation with TUI slash-command examples.

R30. The Claude Code adapter entrypoint MUST NOT claim a Claude one-shot command form unless that form is explicitly smoke-tested for the release.

R31. The OpenCode adapter entrypoint MUST document that `.opencode/skills/` remains the reusable skill surface.

R32. The OpenCode adapter entrypoint MUST document that `.opencode/commands/` aliases are thin usability wrappers for the curated lifecycle command set.

R33. The OpenCode adapter entrypoint MUST include TUI slash-command examples for at least `proposal`, `spec`, `implement`, `code-review`, and `pr`.

R34. The OpenCode adapter entrypoint MAY include `opencode run --command ...` one-shot examples only when the release smoke matrix records a passing one-shot command alias smoke check.

R35. Public README usage examples MUST include TUI slash-command examples for Claude Code and OpenCode.

R36. Public README usage examples MUST include one-shot CLI examples only for tool-specific one-shot forms that are documented and smoke-tested for the release.

R37. Public README usage examples MUST distinguish Claude Code native `/skill-name` invocation from OpenCode generated command aliases.

R38. Public docs MUST NOT imply OpenCode command aliases exist for skills outside the curated lifecycle command set.

R39. Public docs MUST NOT imply Codex `$skill` syntax works in Claude Code or OpenCode.

R40. Release metadata for `v0.1.1` MUST record smoke evidence for OpenCode command alias behavior before a stable release claims the feature.

R40a. `docs/releases/v0.1.1/release.yaml` MUST use:
- `version: v0.1.1`;
- `release_type: final`;
- `manifest_version: 0.1.1`;
- the same supported tool, adapter path, instruction entrypoint, smoke row, and validation field shape defined by the first-public-release adapter metadata contract.

R41. OpenCode smoke evidence for this feature MUST include a command alias invocation for at least one generated alias.

R41a. OpenCode command alias smoke evidence MUST show that the alias caused the matching RigorLoop skill to be loaded, followed, or produce behavior specific to that skill. Merely proving that the command file exists is not sufficient smoke evidence.

R42. OpenCode smoke evidence for documenting `opencode run --command ...` MUST verify that exact one-shot command form.

R43. Claude Code smoke evidence is required only for documented Claude usage forms beyond native TUI slash-command examples.

R44. The `v0.1.1` release notes MUST describe the OpenCode command alias set and the Claude Code skill-native usage guidance.

R45. This change MUST be treated as patch-level only while it adds thin command aliases and documentation without changing canonical skill behavior, adapter source ownership, or workflow semantics.

R46. Repository-owned validation MUST not require ordinary contributors to have Claude Code or OpenCode installed locally for non-smoke checks.

R47. Validation and drift errors involving command aliases MUST identify the tool slug, command alias name, and path when that information is available.

R48. Release verification MUST support `v0.1.1` with adapter manifest version `0.1.1` before the `v0.1.1` tag can be published.

## Inputs and outputs

### Inputs

- Canonical skills under `skills/<skill-name>/SKILL.md`.
- Adapter templates under `scripts/adapter_templates/`.
- The curated lifecycle command set defined in this spec.
- Adapter version, expected to be `0.1.1` for the first release of this feature.
- Existing adapter manifest inputs and portability decisions.
- Release metadata under `docs/releases/v0.1.1/release.yaml`.

### Outputs

- Generated OpenCode command aliases under `dist/adapters/opencode/.opencode/commands/`.
- Updated `dist/adapters/manifest.yaml` with `command_aliases.opencode.aliases`.
- Updated generated Claude Code and OpenCode entrypoints with skill invocation guidance.
- Updated README usage examples.
- Release notes and smoke evidence for `v0.1.1`.
- Validation and drift-check output for command alias consistency.

## State and invariants

- Canonical skill bodies remain authored once under `skills/`.
- `dist/adapters/` remains generated public adapter package output.
- `.codex/skills/` remains the existing generated local Codex runtime mirror and is not affected by OpenCode command aliases.
- OpenCode command aliases are derived from the curated lifecycle command set and included OpenCode skills.
- The manifest must describe generated command aliases exactly enough for validation to detect missing, stale, unexpected, or misplaced alias files.
- Claude Code remains skill-native; RigorLoop must not add duplicate Claude command wrappers for skills.

## Error and boundary behavior

- If a curated lifecycle command's matching skill is excluded from the OpenCode adapter, generation or validation MUST fail rather than generate a dangling command alias.
- If the manifest declares a command alias path but the file is missing, validation MUST fail.
- If a command alias file exists but the manifest does not declare it, validation MUST fail.
- If a command alias body differs from the deterministic thin template, drift checking MUST fail.
- If a command alias attempts to use OpenCode shell interpolation, file references, model overrides, agent overrides, or permission settings, validation MUST fail.
- If OpenCode or Claude Code is unavailable locally, non-smoke validation MUST still be runnable through repository-owned scripts.
- If smoke for `opencode run --command ...` cannot be run, README and release notes MUST NOT document that one-shot form as supported for the release.

## Compatibility and migration

- Existing `v0.1.0` adapter package installs remain valid and continue to work without command aliases.
- Users upgrading to `v0.1.1` may copy the updated OpenCode adapter package into their project to get `.opencode/commands/` aliases.
- The OpenCode command alias addition is backward-compatible because it does not remove `.opencode/skills/` or change skill bodies.
- The Claude Code adapter remains backward-compatible because it keeps `.claude/skills/` and does not introduce duplicate `.claude/commands/`.
- Rollback before release may remove generated OpenCode command aliases, manifest command alias metadata, and invocation docs.
- Rollback after release must be handled through a follow-up patch release or release note; published `v0.1.1` tag history must not be rewritten.

## Observability

- Adapter generation and validation commands MUST print command alias errors with enough detail to locate the affected generated path.
- Release metadata MUST capture manual smoke result, tool version, evidence, reason, and owner for any command alias smoke row or for the tool-level smoke row that includes command alias evidence.
- Release notes MUST expose the supported command alias set to users.
- README examples MUST make the supported invocation forms visible without requiring users to inspect generated files.

## Security and privacy

- Generated command aliases MUST NOT include secrets, credentials, tokens, private keys, machine-local paths, or maintainer-specific environment assumptions.
- Generated command aliases MUST NOT run shell commands or inject shell output.
- Generated command aliases MUST NOT add OpenCode model, agent, or permission settings.
- Generated command aliases MUST pass user-provided arguments only as prompt text through `$ARGUMENTS`.
- Generated command aliases MUST NOT broaden tool permissions beyond the target user's existing OpenCode configuration.

## Accessibility and UX

- Human-facing docs MUST include copyable TUI slash-command examples.
- Tool-specific examples MUST use the spelling and command form the target tool expects.
- README and generated entrypoints MUST identify which OpenCode lifecycle stages have slash aliases and which skills remain available only through skill discovery or natural-language prompting.
- Claude Code examples MUST use native skill slash commands and avoid implying generated Claude command files exist.

## Performance expectations

- Adapter generation and validation for command aliases MUST scale linearly with the number of generated command aliases.
- Repository-owned non-smoke validation MUST avoid invoking Claude Code or OpenCode.
- Adding command aliases MUST not materially increase generated adapter package size by duplicating skill bodies.

## Edge cases

EC1. A portable skill such as `workflow` exists under `.opencode/skills/` but is not in the curated lifecycle command set; no `.opencode/commands/workflow.md` alias is generated.

EC2. A curated lifecycle skill is accidentally excluded from the OpenCode adapter; generation or validation fails because the alias would be dangling.

EC3. A maintainer hand-edits `dist/adapters/opencode/.opencode/commands/proposal.md`; `python scripts/build-adapters.py --check` fails on drift.

EC4. A stray generated file `dist/adapters/opencode/.opencode/commands/verify.md` exists; adapter validation fails because `verify` is outside the curated lifecycle command set.

EC5. The manifest declares `proposal: .opencode/commands/proposal.md`; adapter validation fails because command alias paths must be repository-relative paths under `dist/adapters/opencode/.opencode/commands/`.

EC6. README documents `opencode run --command proposal ...` before that form is smoke-tested; release verification or docs validation fails.

EC7. README documents `claude -p "/proposal ..."` without a passing Claude one-shot smoke check; release verification or docs validation fails.

EC8. A generated OpenCode command alias includes `!` shell interpolation or `@` file reference interpolation; adapter validation fails.

EC9. A command alias file name and manifest key disagree, such as key `proposal-review` pointing to `plan-review.md`; adapter validation fails.

EC10. A generated OpenCode command alias includes the full text of the matching `SKILL.md`; validation fails because aliases must remain thin wrappers.

## Non-goals

- Changing canonical RigorLoop skill behavior.
- Adding command aliases for every portable skill.
- Adding `workflow`, `verify`, `explore`, `research`, `architecture`, `architecture-review`, `ci`, `explain-change`, `learn`, `project-map`, or `constitution` to the OpenCode alias set in v1.
- Generating `.claude/commands/` wrappers for RigorLoop skills.
- Changing Codex invocation behavior.
- Adding marketplace, plugin, or package-manager distribution.
- Adding default OpenCode permissions, Claude Code permissions, model settings, or tool approvals.
- Making one-shot CLI examples for a tool without smoke evidence for that exact form.

## Acceptance criteria

- AC1. `dist/adapters/opencode/.opencode/commands/` contains exactly the 10 curated lifecycle command aliases and no others.
- AC2. Each generated OpenCode command alias is a thin deterministic wrapper that instructs OpenCode to load and follow the matching skill and passes `$ARGUMENTS`.
- AC3. All included portable OpenCode skills remain present under `.opencode/skills/`.
- AC4. `dist/adapters/manifest.yaml` records exact command alias paths using the required `command_aliases.opencode.aliases` shape.
- AC5. Adapter validation rejects missing, stale, unexpected, misplaced, or dangling command aliases.
- AC6. The Claude Code adapter documents native `/skill-name` usage and does not generate `.claude/commands/` wrappers.
- AC7. README includes TUI slash-command examples for Claude Code and OpenCode, and includes only smoke-tested one-shot CLI examples.
- AC8. `v0.1.1` release metadata and release notes describe the supported command alias set and include required smoke evidence for claimed one-shot command forms.
- AC9. Repository-owned validation commands can verify non-smoke behavior without requiring Claude Code or OpenCode to be installed locally.
- AC10. Release verification supports `v0.1.1`, requires manifest version `0.1.1`, and rejects `v0.1.1` when OpenCode command alias smoke evidence is missing or insufficient.

## Open questions

None.

## Next artifacts

- `spec-review` for this spec.
- Architecture update for the manifest command alias data model and generated OpenCode command package surface.
- Execution plan for `v0.1.1` adapter command aliases.
- Test spec mapping these requirements to fixture, validation, drift, documentation, and smoke checks.

## Follow-on artifacts

- Architecture: `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md`
- Execution plan: `docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`
- Test spec: `specs/skill-invocation-commands-for-adapters.test.md`

## Readiness

Spec review is complete and this spec is approved.

The architecture is approved and the execution plan is active.

Plan review is complete and the matching test spec is active.

Immediate next repository stage: `implement`.
