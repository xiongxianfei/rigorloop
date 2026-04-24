# Skill Invocation Commands for Adapter Packages

## Status
- accepted

## Problem

RigorLoop v0.1.0 ships generated adapter packages for Codex, Claude Code, and opencode, but the generated entrypoints only say where reusable workflow skills are installed. They do not show users how to invoke those skills in each tool's native interaction model.

That leaves a practical adoption gap:

- Claude Code users can directly invoke skills as slash commands, but RigorLoop does not currently document that adapter-specific behavior.
- opencode users get project skills under `.opencode/skills/`, but opencode exposes skills through its `skill` tool and model-driven discovery rather than a documented user-facing `/skill-name` shortcut.
- Users may incorrectly assume Codex-style `$skill` syntax, Claude-style `/skill-name` syntax, and opencode command behavior are interchangeable.

## Goals

- Document the best-practice way to use RigorLoop skills in Claude Code and opencode.
- Add a direct, low-friction command path for the curated opencode lifecycle command set.
- Keep canonical skill bodies authored once under `skills/`.
- Keep adapter-specific invocation help thin, generated, and validated.
- Avoid duplicating skill bodies inside `CLAUDE.md`, `AGENTS.md`, or command wrappers.
- Preserve existing adapter installability and smoke-test expectations.

## Non-goals

- Redesigning the RigorLoop skill lifecycle or skill body structure.
- Adding marketplace, plugin, or package-manager distribution.
- Claiming identical skill invocation semantics across Claude Code and opencode.
- Adding tool-specific secrets, model configuration, or default permission policies.
- Replacing automatic skill discovery with command-only behavior.
- Changing Codex behavior except where shared documentation needs to avoid misleading cross-tool claims.

## Context

The accepted multi-agent adapter release established this generated package model:

- Claude Code adapter: `dist/adapters/claude/CLAUDE.md` plus `.claude/skills/<skill-name>/SKILL.md`.
- opencode adapter: `dist/adapters/opencode/AGENTS.md` plus `.opencode/skills/<skill-name>/SKILL.md`.
- Canonical skill content remains under `skills/`; adapter packages are generated output.

Official tool behavior differs in ways the adapter docs should respect:

- Claude Code skills live under `.claude/skills/<skill-name>/SKILL.md` for project-local use. Claude Code can load matching skills automatically, and the skill `name` also becomes a direct `/skill-name` slash command.
- Claude Code still supports `.claude/commands/`, but current docs position skills as the recommended path for reusable procedures because skills support supporting files and richer behavior.
- opencode skills live under `.opencode/skills/<skill-name>/SKILL.md` for project-local use, and opencode also detects compatible `.claude/skills/` and `.agents/skills/` paths.
- opencode lists skills to the model through its `skill` tool. The agent loads a skill by calling that tool; users normally prompt for the skill by name or intent.
- opencode custom commands live under `.opencode/commands/` or config and are invoked as `/command-name`. Command templates can pass arguments through `$ARGUMENTS`.

Sources consulted on 2026-04-24:

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [opencode agent skills](https://opencode.ai/docs/skills)
- [opencode commands](https://opencode.ai/docs/commands/)
- [opencode rules](https://opencode.ai/docs/rules)

## Options considered

### Option 1: Documentation only

Add usage examples to README, workflow docs, and generated adapter entrypoints.

Advantages:

- Smallest change.
- No new generated package surface.
- Avoids command-wrapper behavior that may vary across opencode versions.

Disadvantages:

- opencode users still need to type natural-language prompts such as "Use the proposal skill...".
- The adapter still lacks slash-style parity for the lifecycle stages.
- The "how do I use this skill now?" answer remains less direct for opencode than for Claude Code.

### Option 2: Generate command wrappers for both Claude Code and opencode

Generate `.claude/commands/<skill-name>.md` and `.opencode/commands/<skill-name>.md` files that route to the matching skill.

Advantages:

- Gives both adapters explicit command files.
- Makes command discovery symmetric in the generated tree.
- Could provide consistent command descriptions and argument examples.

Disadvantages:

- Duplicates Claude Code behavior because Claude Code already turns skill names into slash commands.
- Risks command-versus-skill precedence ambiguity in Claude Code.
- Adds generated files without adding much user value for Claude Code.

### Option 3: Skill-first docs plus opencode-only command aliases

Use tool-native skill invocation for Claude Code and generate thin opencode command aliases for the curated lifecycle command set.

Claude Code examples would use the native skill slash command:

```text
/proposal Add command aliases for using RigorLoop skills
/spec Define command alias behavior for adapter packages
/code-review Review the current diff against the approved spec
```

opencode examples would support both natural-language skill use and generated command aliases:

```text
Use the proposal skill to evaluate command aliases for RigorLoop adapters.
/proposal Add command aliases for using RigorLoop skills
```

Generated opencode command files would be thin prompts, not skill copies:

```text
.opencode/commands/proposal.md
---
description: Use the RigorLoop proposal skill.
---

Load and follow the `proposal` skill for this request:

$ARGUMENTS
```

Advantages:

- Matches each tool's documented best practice.
- Avoids redundant Claude command files.
- Gives opencode users a direct slash-style workflow without changing skill bodies.
- Keeps command wrappers generated, deterministic, and easy to validate.

Disadvantages:

- Adds a new opencode adapter package surface.
- Requires validation to catch stale command wrappers, missing wrappers, and wrapper/body drift.
- May require smoke updates for opencode TUI and `opencode run --command`.

### Option 4: Rely on automatic discovery only

Leave generated packages unchanged and expect users to ask naturally for the desired workflow stage.

Advantages:

- No implementation work.
- Preserves the smallest generated package footprint.
- Avoids command-wrapper maintenance.

Disadvantages:

- The adapter remains less usable for new users.
- The public package does not teach tool-native skill usage.
- Users are more likely to invent unsupported invocation syntax.

## Recommended direction

Choose Option 3.

RigorLoop should treat skills as the primary capability surface and commands as optional invocation affordances. For Claude Code, the best practice is to rely on native skill slash commands because the skill `name` is already the command. Adding `.claude/commands/` wrappers would duplicate the same surface and risk precedence confusion.

For opencode, RigorLoop should keep `.opencode/skills/` as the real skill package for all included portable skills and add generated `.opencode/commands/<skill-name>.md` aliases only for this curated lifecycle command set:

- `proposal`
- `proposal-review`
- `spec`
- `spec-review`
- `plan`
- `plan-review`
- `test-spec`
- `implement`
- `code-review`
- `pr`

Those aliases should exist only to make common lifecycle stages easy to invoke from the TUI or `opencode run --command`; they should not contain skill instructions beyond "load and follow the matching skill."

The generated opencode adapter should therefore become:

```text
dist/adapters/opencode/
  AGENTS.md
  .opencode/
    commands/
      <skill-name>.md
    skills/
      <skill-name>/
        SKILL.md
```

The Claude Code adapter should stay skill-native:

```text
dist/adapters/claude/
  CLAUDE.md
  .claude/
    skills/
      <skill-name>/
        SKILL.md
```

Both generated entrypoints should include a short "Using RigorLoop skills" section with examples. The section should explain the native invocation form, show the common lifecycle stage commands, and warn users not to assume Codex `$skill` syntax in non-Codex tools.

The adapter manifest should record exact generated command alias paths, not just counts. Counts may be included as derived summary fields, but validation must treat the declared paths as authoritative for generated command coverage.

## Expected behavior changes

- Claude Code users will see examples such as `/workflow`, `/proposal`, `/spec`, `/implement`, `/code-review`, `/verify`, and `/pr` in the generated `CLAUDE.md`.
- opencode users will see examples for natural-language skill loading and generated slash command aliases in the generated `AGENTS.md`.
- opencode adapter installs will include `.opencode/commands/<skill-name>.md` aliases for the curated lifecycle command set only.
- All included portable skills will remain available under `.opencode/skills/`.
- `dist/adapters/manifest.yaml` will record exact generated command alias paths.
- `opencode run --command <skill-name> "<task>"` can become the documented one-shot command path after smoke verification.
- Adapter validation will fail when manifest-declared command aliases are missing, stale, hand-edited, mapped to skills not included in the opencode adapter, or accompanied by unexpected aliases.
- Release smoke for opencode will include at least one command-alias invocation check before claiming stable support for this feature.

## Architecture impact

This change would extend the generated adapter package contract but would not change canonical skill ownership.

Likely touched components:

- `scripts/adapter_distribution.py`: add opencode command output modeling and validation.
- `scripts/build-adapters.py`: generate/check the expanded opencode package tree through existing helpers.
- `scripts/validate-adapters.py`: validate command aliases against manifest and generated skill set.
- `scripts/adapter_templates/claude/CLAUDE.md`: add tool-native usage examples.
- `scripts/adapter_templates/opencode/AGENTS.md`: add skill and command usage examples.
- `dist/adapters/opencode/.opencode/commands/`: generated command alias output.
- `dist/adapters/manifest.yaml`: add exact command alias path metadata, with optional derived count summaries.
- `docs/workflows.md` and `README.md`: document adapter usage at the user-facing level.
- `docs/releases/<version>/release.yaml`: record smoke evidence for opencode command aliases before a stable release that claims them.

## Testing and verification strategy

- Add fixture tests that generate opencode command aliases for the curated lifecycle command set.
- Add validation tests for missing command aliases, extra command aliases, wrong command body, and command aliases generated for excluded opencode skills.
- Add drift tests so `python scripts/build-adapters.py --check` fails when command aliases are stale.
- Add docs checks or focused assertions that Claude Code usage docs show native `/skill-name` examples without generating duplicate `.claude/commands/` wrappers.
- Add manifest tests proving exact command alias paths are recorded and validated.
- Add README/doc checks proving TUI slash-command examples are present, and one-shot CLI examples appear only for tools whose one-shot form has been documented and smoke-tested.
- Run existing skill validation and adapter validation:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/test-adapter-distribution.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version <version> --check
python scripts/validate-adapters.py --version <version>
```

- For manual smoke, verify:

```bash
claude -p "/proposal Add a small RigorLoop usage clarification"
opencode run --dir <adapter-install-root> --command proposal "Add a small RigorLoop usage clarification"
```

The exact smoke commands should be confirmed in the follow-on spec because CLI handling of slash commands and custom command aliases is tool-owned behavior.

For README examples, include both TUI slash-command examples for human use and one-shot CLI examples only when that one-shot form is documented and smoke-tested. For this proposal, opencode may include both TUI and `opencode run --command ...` forms. Claude Code examples should use TUI slash-command forms unless a Claude one-shot form is explicitly smoke-tested for the release.

## Rollout and rollback

Rollout should land behind normal generated-output validation:

- First, update the spec and test spec for adapter command aliases.
- Then update generator and validation code.
- Regenerate adapter packages.
- Smoke opencode command alias behavior before claiming stable support.

Because `v0.1.0` has already shipped, this proposal targets `v0.1.1`. The change is patch-level as long as it only adds thin command aliases and usage documentation without changing skill behavior, adapter package ownership, or workflow semantics.

Rollback is straightforward before release: remove generated opencode command aliases and revert template/docs changes. After release, rollback should be handled as a patch release note or a follow-up compatibility fix rather than rewriting released tags.

## Risks and mitigations

- Risk: opencode command aliases are mistaken for the canonical skill source.
  Mitigation: generated command files must be thin and must point to the named skill; canonical skill bodies remain under `skills/`.

- Risk: Claude Code command wrappers conflict with native skill slash commands.
  Mitigation: do not generate `.claude/commands/` wrappers for RigorLoop skills.

- Risk: command aliases drift from skill inclusion decisions.
  Mitigation: validate exact command alias paths from the manifest and generated opencode skill tree.

- Risk: users assume every tool supports the same syntax.
  Mitigation: generated entrypoints should explicitly document Claude `/skill-name`, opencode prompt-or-command alias behavior, and Codex-specific syntax separately.

- Risk: opencode command behavior changes in a future release.
  Mitigation: keep aliases thin, smoke representative usage, and avoid depending on undocumented internals.

## Open questions

None. The maintainer resolved the proposal-level scope choices on 2026-04-24:

- Generate opencode command aliases only for the curated lifecycle command set: `proposal`, `proposal-review`, `spec`, `spec-review`, `plan`, `plan-review`, `test-spec`, `implement`, `code-review`, and `pr`.
- Keep all included portable skills available under `.opencode/skills/`.
- Record exact command alias paths in `dist/adapters/manifest.yaml`; counts may be included only as derived summaries.
- Target `v0.1.1` because `v0.1.0` has already shipped.
- Include TUI slash-command examples in README and one-shot CLI examples only for documented and smoke-tested one-shot forms.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-04-24 | Draft proposal to add adapter-specific skill invocation guidance and opencode command aliases. | v0.1.0 proved installable adapters, but usage is still under-documented for non-Codex tools. | Leaving users to infer invocation behavior from generated paths alone. |
| 2026-04-24 | Prefer native Claude Code `/skill-name` usage over generated `.claude/commands/` wrappers. | Claude Code already exposes skill names as slash commands, so extra command files add duplication. | Symmetric command wrappers for both Claude Code and opencode. |
| 2026-04-24 | Consider generated opencode command aliases as thin prompts over real skills. | opencode has native custom slash commands, but skill loading itself is model/tool-mediated. | Copying skill bodies into commands or relying only on natural-language prompts. |
| 2026-04-24 | Generate opencode command aliases only for the curated lifecycle command set. | The aliases are a usability layer for common lifecycle stages, not a replacement for full skill discovery. | Generating aliases for every portable skill. |
| 2026-04-24 | Record exact command alias paths in the adapter manifest. | Release and adapter validation need deterministic package evidence, not only summary counts. | Relying only on generated file counts or ad hoc validation. |
| 2026-04-24 | Target `v0.1.1`. | `v0.1.0` has already shipped, and this is patch-level when limited to thin aliases and docs. | Retagging `v0.1.0` or waiting for a broader adapter redesign. |
| 2026-04-24 | README examples should include TUI slash-command forms and smoke-tested one-shot CLI forms. | Human usage and automation usage are both first-order adoption paths, but unverified one-shot examples would overclaim. | Documenting only TUI usage or documenting un-smoked one-shot forms. |

## Next artifacts

- Focused spec for adapter skill invocation commands and documentation behavior.
- A matching test spec for command generation, validation, drift, and smoke coverage.
- Architecture update only if the spec chooses manifest-visible command metadata or changes adapter package boundaries beyond opencode command aliases.

## Follow-on artifacts

- Spec: `specs/skill-invocation-commands-for-adapters.md`
- Architecture: `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md`
- Execution plan: `docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`

## Readiness

Accepted. The follow-on spec and architecture are approved, and the execution plan is active.
