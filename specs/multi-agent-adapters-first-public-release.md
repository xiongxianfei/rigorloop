# Multi-Agent Adapters and First Public Release

## Status
- approved

## Related proposal

- [Multi-Agent Adapters and First Public Release](../docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md)

## Goal and context

This spec defines the public compatibility contract for shipping RigorLoop as independently installable adapter packages for Codex, Claude Code, and opencode, followed by the first public `v0.1.0` release. RigorLoop workflow skills remain authored once from canonical repository sources; tool adapter packages are generated, validated, and smoke-tested rather than hand-maintained.

External tool contracts were checked against official docs on 2026-04-24:

- opencode project rules use `AGENTS.md`: <https://opencode.ai/docs/rules/>
- opencode project skills use `.opencode/skills/<name>/SKILL.md`: <https://opencode.ai/docs/skills>
- Claude Code project memory uses `CLAUDE.md`: <https://docs.anthropic.com/en/docs/claude-code/memory>
- Claude Code project skills use `.claude/skills/<skill-name>/SKILL.md`: <https://docs.claude.com/en/docs/claude-code/skills>

## Glossary

- adapter: a tool-specific generated package that exposes RigorLoop instructions and portable workflow skills to one agent tool.
- adapter package: a generated, tracked directory under `dist/adapters/<adapter>/` that can be installed without sibling adapter packages.
- canonical skill: an authored RigorLoop skill under `skills/<skill-name>/SKILL.md`.
- generated output: deterministic files derived from canonical sources or authored thin templates.
- instruction entrypoint: the adapter package file a tool reads for project-level operating guidance, such as `AGENTS.md` or `CLAUDE.md`.
- portable-core gate: validation that decides whether a canonical skill can be shipped in a non-Codex adapter package without Codex-only assumptions.
- smoke matrix: maintainer-run compatibility evidence for each supported adapter package.
- support matrix: the generated manifest and documentation that state which skills ship to which adapters and why excluded skills are excluded.

## Examples first

### Example E1: generated adapter packages

Given a maintainer builds adapter packages for release `0.1.0`
When generation succeeds
Then `dist/adapters/codex/`, `dist/adapters/claude/`, `dist/adapters/opencode/`, and `dist/adapters/manifest.yaml` exist with deterministic contents derived from canonical RigorLoop sources.

### Example E2: portable workflow skill

Given `skills/workflow/SKILL.md` passes the portable-core gate
When adapter generation runs
Then the generated manifest marks `workflow` as portable and lists `codex`, `claude`, and `opencode`
And each adapter package includes a generated `workflow/SKILL.md` under that adapter's project-skill path.

### Example E3: non-portable skill exclusion

Given `skills/some-codex-only-skill/SKILL.md` depends on Codex-only invocation syntax
When adapter generation runs
Then the skill is excluded from `dist/adapters/claude/` and `dist/adapters/opencode/`
And `dist/adapters/manifest.yaml` records `portable: false`, `adapters: [codex]`, and a human-readable reason.

### Example E4: Claude Code instruction entrypoint

Given a user installs the Claude Code adapter package into a project root
When Claude Code starts in that project
Then the generated `CLAUDE.md` provides thin RigorLoop operating guidance
And the reusable skills are available under `.claude/skills/<skill-name>/SKILL.md`
And `CLAUDE.md` does not duplicate the full bodies of those skills.

### Example E5: opencode instruction entrypoint and skills

Given a user installs the opencode adapter package into a project root
When opencode starts in that project
Then `AGENTS.md` provides project-level RigorLoop operating guidance
And `.opencode/skills/<skill-name>/SKILL.md` provides reusable workflow skills.

### Example E6: first public release gating

Given adapter generation, validation, docs, and release verification pass
When the maintainer-run smoke matrix has not passed for all supported adapters
Then the release may use `v0.1.0-rc.1`
But only when all non-smoke RC gates pass
And it must not use `v0.1.0`.

### Example E7: first public release

Given adapter generation, validation, documentation checks, release verification, and the maintainer-run smoke matrix all pass
When the project publishes the first public stable version
Then the release tag is `v0.1.0`
And the release notes match the manifest support matrix.

### Example E8: RC blocked by known smoke failure

Given `docs/releases/v0.1.0-rc.1/release.yaml` records `smoke.opencode.result: fail`
When release verification runs for `v0.1.0-rc.1`
Then release verification fails because known smoke failures block RC publication.

## Requirements

R1. RigorLoop workflow skills MUST be authored from canonical repository sources rather than separately authored per adapter package.

R2. The system MUST generate tracked adapter packages for exactly these first-public-release adapters:
- `codex`;
- `claude`;
- `opencode`.

R3. The generated Codex adapter package MUST use this externally visible layout:

```text
dist/adapters/codex/
  AGENTS.md
  .agents/
    skills/
      <skill-name>/
        SKILL.md
```

R4. The generated Claude Code adapter package MUST use this externally visible layout:

```text
dist/adapters/claude/
  CLAUDE.md
  .claude/
    skills/
      <skill-name>/
        SKILL.md
```

R5. The generated opencode adapter package MUST use this externally visible layout:

```text
dist/adapters/opencode/
  AGENTS.md
  .opencode/
    skills/
      <skill-name>/
        SKILL.md
```

R6. Generated adapter package contents MUST be deterministic for the same canonical inputs, release version, templates, and portability decisions.

R7. Generated adapter package contents MUST NOT be treated as canonical authored workflow source.

R8. Contributors MUST NOT hand-edit generated adapter package contents to change RigorLoop behavior.

R9. The repository MUST provide validation that fails when generated adapter packages are missing, stale, or contain unexpected files relative to the canonical generation contract.

R10. Each adapter package MUST be independently installable by copying that package's contents into a project root without requiring files from sibling adapter packages.

R11. Each instruction entrypoint MUST be generated from an authored thin template or equivalent canonical thin source.

R12. Instruction entrypoints MUST provide project-level operating guidance for the target tool without duplicating full generated skill bodies.

R13. Instruction entrypoints MUST identify the package as generated adapter output and point maintainers to the canonical repository source for edits.

R14. `dist/adapters/claude/CLAUDE.md` MUST be generated and MUST NOT be omitted from the Claude Code adapter package.

R15. `dist/adapters/opencode/AGENTS.md` and `dist/adapters/opencode/.opencode/skills/` MUST both be generated for opencode support.

R16. A canonical skill MUST pass the portable-core gate before it is shipped in the Claude Code or opencode adapter package.

R17. The portable-core gate MUST require every portable skill to use an Agent Skills-compatible `SKILL.md` structure with YAML frontmatter and Markdown instruction content.

R18. The portable-core gate MUST require the generated skill name to:
- be 1 to 64 characters;
- use lowercase alphanumeric tokens separated by single hyphens;
- not start or end with a hyphen;
- not contain consecutive hyphens;
- match the generated skill directory name.

R19. The portable-core gate MUST require the generated skill description to be non-empty, portable across the target adapters, and no longer than 1024 characters.

R20. The portable-core gate MUST reject or transform target adapter output when a canonical skill contains frontmatter unsupported by the target adapter.

R21. The portable-core gate MUST reject a skill from non-Codex adapters when the skill requires Codex-only invocation syntax.

R22. The portable-core gate MUST reject a skill from non-Codex adapters when the skill depends on `agents/openai.yaml`.

R23. The portable-core gate MUST reject a skill from non-Codex adapters when the skill references `.codex/skills` as the only install location.

R24. The portable-core gate MUST reject a skill from non-Codex adapters when the skill assumes Codex-only tools, UI, approval behavior, or runtime permissions.

R25. The portable-core gate MUST reject a skill from non-Codex adapters when the skill has a hidden dependency on Codex-specific `$skill` invocation.

R26. The portable-core gate MUST allow generic RigorLoop stage names and artifact paths when they are not tied to a Codex-only runtime.

R27. A non-portable skill MAY ship in the Codex adapter package when it is valid for Codex and its non-portability reason is recorded in the manifest.

R28. A skill that fails portability for an adapter MUST either be excluded from that adapter package or transformed through an explicitly validated target-specific transform.

R29. `dist/adapters/manifest.yaml` MUST include a top-level `version` value that matches the adapter package release version under verification.

R29a. The manifest `version` MUST be `0.1.0-rc.1` for the first release candidate package set.

R29b. The manifest `version` MUST be `0.1.0` for the first public stable release package set.

R30. `dist/adapters/manifest.yaml` MUST include a `skills` mapping keyed by skill name.

R31. Each manifest skill entry MUST include:
- `portable`, as a boolean;
- `adapters`, as the list of adapter names where the skill is included.

R31a. In the first-public-release manifest, `portable: true` means the skill passes the portable-core gate for all supported first-public-release adapters.

R32. Each manifest skill entry with `portable: false` MUST include a human-readable `reason`.

R33. The manifest MUST NOT list an adapter for a skill unless that adapter package contains the generated skill at the adapter's project-skill path.

R34. The manifest MUST NOT omit a generated skill that exists in any adapter package.

R35. The manifest MUST be deterministic for the same canonical inputs and release version.

R36. The public documentation MUST include a support matrix for Codex, Claude Code, and opencode that matches `dist/adapters/manifest.yaml`.

R37. The public documentation MUST distinguish canonical authored sources from generated adapter package output.

R38. The public documentation MUST state that ordinary contributors do not need all supported tools installed locally to contribute.

R39. The authoritative first-public-release metadata surface MUST be `docs/releases/<version>/release.yaml`.

R40. `docs/releases/<version>/release.yaml` MUST include:
- `version`;
- `release_type`;
- `manifest_version`;
- `supported_tools`;
- `adapter_paths`;
- `instruction_entrypoints`;
- `smoke`;
- `validation`.

R40a. `version` MUST be the release tag, including the leading `v`.

R40b. `release_type` MUST be `rc` for `v0.1.0-rc.1` and `final` for `v0.1.0`.

R40c. `manifest_version` MUST match `dist/adapters/manifest.yaml` without the leading `v`.

R40d. For the first public release, `supported_tools` MUST list exactly:
- `codex`;
- `claude`;
- `opencode`.

R40e. `adapter_paths` MUST map each supported tool to its generated adapter package path:
- `codex`: `dist/adapters/codex/`;
- `claude`: `dist/adapters/claude/`;
- `opencode`: `dist/adapters/opencode/`.

R40f. `instruction_entrypoints` MUST map each supported tool to its generated instruction entrypoint:
- `codex`: `dist/adapters/codex/AGENTS.md`;
- `claude`: `dist/adapters/claude/CLAUDE.md`;
- `opencode`: `dist/adapters/opencode/AGENTS.md`.

R41. The `smoke` mapping in `docs/releases/<version>/release.yaml` MUST include exactly one row for each supported tool.

R41a. Each smoke row MUST include:
- `result`;
- `tool_version`;
- `evidence`;
- `reason`;
- `owner`.

R41b. Each smoke row `result` MUST be one of:
- `pass`;
- `fail`;
- `not-run`;
- `blocked`.

R41c. A smoke row with `result: pass` MUST include non-empty `tool_version` and non-empty `evidence`, and it MAY use an empty `reason`.

R41d. A smoke row with `result: fail` MUST include non-empty `tool_version`, non-empty `evidence`, non-empty `reason`, and non-empty `owner`.

R41e. A smoke row with `result: not-run` MUST include `tool_version: unknown`, empty `evidence`, non-empty `reason`, and non-empty `owner`.

R41f. A smoke row with `result: blocked` MUST include `tool_version: unknown` unless the tool version is known, MAY include evidence, and MUST include non-empty `reason` and non-empty `owner`.

R42. The `validation` mapping in `docs/releases/<version>/release.yaml` MUST include at least:
- `generated_sync`;
- `release_notes_consistency`;
- `placeholder_release_check`;
- `security`.

R42a. Each required validation value MUST be `pass` or `fail`.

R43. RC release means the generated package is structurally ready for public trial.

R43a. A `v0.1.0-rc.1` release MAY be published before full manual adapter smoke has passed only when all non-smoke release gates pass.

R43b. Release verification for `v0.1.0-rc.1` MUST require:
- generated adapter outputs are in sync with canonical skills;
- `dist/adapters/manifest.yaml` version is exactly `0.1.0-rc.1`;
- release notes version is exactly `v0.1.0-rc.1`;
- release notes, manifest, and generated adapter paths list the same supported tools;
- Codex, Claude Code, and opencode adapter directories exist;
- required adapter instruction entrypoints exist;
- generated skill counts match the release manifest;
- portable-skill filtering has no unapproved exclusions or inclusions;
- release-check scripts are not placeholders;
- security checks pass;
- no generated output drift exists;
- no unsupported tool-specific metadata leaks into adapters where it is not allowed;
- `docs/releases/v0.1.0-rc.1/release.yaml` exists with one smoke row per supported tool.

R43c. The only release gate that MAY remain incomplete for `v0.1.0-rc.1` is full manual adapter smoke.

R43d. Known smoke failures MUST block `v0.1.0-rc.1` publication.

R43e. A `not-run` smoke row MAY be allowed for `v0.1.0-rc.1` only when it includes a non-empty reason and owner.

R43f. A `blocked` smoke row MAY be allowed for `v0.1.0-rc.1` only when the reason identifies an external or tool-access blocker and includes an owner.

R44. Final release means the generated package is structurally ready and smoke-verified.

R44a. A `v0.1.0` release MUST satisfy all RC release gates.

R44b. A `v0.1.0` release MUST NOT be published unless every smoke row result is `pass`.

R44c. A `v0.1.0` release MUST NOT allow smoke row results `fail`, `not-run`, or `blocked`.

R44d. A `v0.1.0` release MUST use release notes that match the adapter support matrix, portability exclusions, and known limitations.

R45. Release verification MUST check that the tag under verification matches the release maturity:
- `v0.1.0-rc.1` for the first public release candidate;
- `v0.1.0` for the first public stable release.

R46. Release verification MUST fail if release-check scripts still contain placeholder text, including:
- `Replace this script with repository-specific release checks`;
- `TODO: release checks`;
- `placeholder release check`.

R46a. Release verification MUST fail if no repository-specific release check invokes:
- skill validation;
- skill regression validation;
- adapter generation drift check;
- adapter validation;
- release metadata validation;
- security checks.

R47. Release verification MUST check that release notes or release metadata describe the generated adapter packages and any non-portable skill exclusions.

R48. Repository CI MUST include adapter generation, portability, manifest, and drift validation once this feature is implemented.

R49. Existing `.codex/skills/` compatibility output MUST remain generated and not hand-edited while it remains in the repository.

R50. The architecture artifact for this feature MUST define whether `.codex/skills/` is preserved as a local development mirror, generated from the new adapter contract, or superseded with migration guidance.

R51. This feature MUST NOT add a hosted runtime, marketplace package, plugin registry publication, or agent orchestration service.

R52. This feature MUST NOT require secrets, API keys, or private credentials for generation, validation, or release verification.

R53. This feature MUST NOT broaden adapter package permissions by default through generated tool-specific permission configuration.

## Inputs and outputs

Inputs:

- canonical skills under `skills/<skill-name>/SKILL.md`;
- authored thin instruction entrypoint templates or equivalent canonical thin sources;
- adapter configuration that names the supported adapters;
- release version, either `0.1.0-rc.1` or `0.1.0`;
- portability validation rules;
- release notes or release metadata for tag verification;
- `docs/releases/<version>/release.yaml`;
- maintainer-run smoke matrix evidence recorded in release metadata.

Outputs:

- `dist/adapters/codex/AGENTS.md`;
- `dist/adapters/codex/.agents/skills/<skill-name>/SKILL.md`;
- `dist/adapters/claude/CLAUDE.md`;
- `dist/adapters/claude/.claude/skills/<skill-name>/SKILL.md`;
- `dist/adapters/opencode/AGENTS.md`;
- `dist/adapters/opencode/.opencode/skills/<skill-name>/SKILL.md`;
- `dist/adapters/manifest.yaml`;
- `docs/releases/v0.1.0-rc.1/release.yaml` when preparing the first release candidate;
- `docs/releases/v0.1.0/release.yaml` when preparing the first public stable release;
- validation output for generation, portability, manifest consistency, drift, smoke evidence, and release readiness;
- contributor-facing documentation describing installable adapter packages and the support matrix.

## State and invariants

- Canonical skill content remains authored under `skills/`.
- Adapter package files under `dist/adapters/` are generated output.
- The manifest and generated adapter packages describe the same skill inclusion set.
- A skill excluded from an adapter package has a visible reason when the manifest marks it non-portable.
- RC release metadata may record incomplete smoke only as `not-run` or externally blocked rows with reason and owner.
- The first stable public release remains blocked until all supported adapter package smoke checks pass.
- Generated package validation does not replace human review, pull requests, CI, or RigorLoop lifecycle artifacts.
- `.codex/skills/` remains generated output for as long as it remains in the repository.

## Error and boundary behavior

- Missing canonical skill source MUST fail generation or validation.
- Duplicate portable skill names MUST fail portability validation.
- A generated skill whose directory name does not match its frontmatter `name` MUST fail validation.
- A generated skill with a missing or empty `description` MUST fail validation.
- A generated skill with unsupported target adapter frontmatter MUST fail validation unless an explicit transform removes or rewrites that frontmatter.
- A manifest entry that lists an adapter without a corresponding generated skill MUST fail validation.
- A generated skill missing from the manifest MUST fail validation.
- A non-portable skill without a manifest reason MUST fail validation.
- Missing generated instruction entrypoints MUST fail adapter package validation.
- Stale generated adapter output MUST fail drift validation.
- Missing release metadata MUST fail release verification.
- Release metadata with mismatched supported tools, adapter paths, instruction entrypoints, manifest version, or release notes version MUST fail release verification.
- Release metadata with an unsupported smoke result value MUST fail release verification.
- Release metadata for `v0.1.0-rc.1` with any `fail` smoke result MUST fail release verification.
- Release metadata for `v0.1.0-rc.1` with a `not-run` or `blocked` smoke result missing reason or owner MUST fail release verification.
- Release metadata for `v0.1.0` with any smoke result other than `pass` MUST fail release verification.
- A release verification run for `v0.1.0` with missing or failing smoke matrix entries MUST fail.
- A release verification run for `v0.1.0` with placeholder release-check wording still present MUST fail.
- A contributor without all supported tools installed locally MUST still be able to run repository-owned non-smoke validation.

## Compatibility and migration

- The existing canonical source-of-truth model remains unchanged: `skills/`, `docs/`, `specs/`, `schemas/`, and `scripts/` remain authored sources.
- Existing `.codex/skills/` output remains generated output and must not become a second authored skill tree.
- The new public adapter package surface is `dist/adapters/`.
- Documentation must explain whether Codex users should install from `dist/adapters/codex/`, continue using repository-local `.codex/skills/`, or both, based on the approved architecture.
- The feature must be rollback-safe before tag publication by reverting generated adapter output, templates, validation changes, docs, and release verification changes.
- After tag publication, incorrect adapter claims must be corrected through a patch release or release note rather than by rewriting the released tag.

## Observability

- Generation and drift-check commands MUST print which adapter packages were checked or written.
- Portability validation failures MUST name the skill, adapter, and failed portable-core rule.
- Manifest validation failures MUST name the skill and inconsistent adapter package path.
- Release verification failures MUST name the failed release gate.
- Smoke matrix evidence MUST be contributor-visible in `docs/releases/<version>/release.yaml` before `v0.1.0-rc.1` or `v0.1.0`.

## Security and privacy

- Generation, validation, and drift checks MUST run without network access and without secrets.
- Generated adapter packages MUST NOT contain credentials, tokens, private keys, or machine-local paths.
- Generated instruction entrypoints MUST NOT instruct tools to bypass Git, pull requests, CI, or human review.
- Generated adapter packages MUST NOT enable broad tool permissions or approval bypasses by default.
- Release verification MUST NOT claim hosted CI passed unless the hosted run was actually observed.

## Accessibility and UX

No graphical UI is introduced. Documentation and command output should remain plain-text and readable in terminals and pull request review.

## Performance expectations

- Generation and validation SHOULD scale linearly with the number of canonical skills and generated adapter files.
- Repository-owned non-smoke validation SHOULD remain practical for ordinary contributors to run locally without installing all supported agent tools.

## Edge cases

1. A canonical skill contains Codex-specific `argument-hint` frontmatter: the generated non-Codex skill output is either transformed to remove unsupported metadata or the skill is excluded from non-Codex adapters with a manifest reason.
2. A canonical skill body says "install this under `.codex/skills`" without naming a generic or target-specific alternative: the skill fails the portable-core gate for Claude Code and opencode.
3. A canonical skill uses `$proposal` or similar Codex-only invocation syntax as a required trigger: the skill fails the portable-core gate for Claude Code and opencode.
4. A canonical skill references `docs/` and `specs/` artifact paths generically: the skill may remain portable because those are RigorLoop artifact paths, not Codex runtime paths.
5. A generated adapter package is copied without its sibling packages: the copied package still contains its instruction entrypoint and target project-skill tree.
6. A maintainer wants to release before all tool smoke checks pass: only `v0.1.0-rc.1` is allowed.
7. A maintainer wants to release `v0.1.0` after generated validation passes but before manual smoke evidence exists: release verification fails.
8. A tool-specific official doc changes after the adapter is implemented: the affected adapter contract must be revised through the normal lifecycle before changing release claims.
9. A skill is portable for Claude Code but not opencode: the manifest lists only the adapters where the skill is generated and records a reason when it is non-portable overall.
10. Existing `.codex/skills/` output drifts from its generation contract while `dist/adapters/codex/` is in sync: validation fails for the generated surface that drifted.
11. `v0.1.0-rc.1` release metadata records `result: fail` for one tool: release verification fails because known smoke failures block RC publication.
12. `v0.1.0-rc.1` release metadata records `result: not-run` without an owner: release verification fails because incomplete RC smoke requires a reason and follow-up owner.
13. `v0.1.0` release metadata records `result: blocked`: release verification fails because final release requires all smoke rows to pass.

## Non-goals

- Building a hosted RigorLoop service.
- Publishing package-manager, marketplace, or plugin-registry distributions in this release.
- Guaranteeing identical runtime behavior across Codex, Claude Code, and opencode.
- Making every existing skill portable in the first public release.
- Requiring ordinary contributors to install all supported agent tools locally.
- Adding secrets, API keys, or account-specific setup to generated packages.
- Replacing Git, pull requests, CI, human review, or the existing RigorLoop lifecycle.

## Acceptance criteria

- A generated `dist/adapters/` tree exists with Codex, Claude Code, and opencode packages matching R3 through R5.
- `dist/adapters/manifest.yaml` exists and satisfies R29 through R35.
- Portable-core validation enforces R16 through R28.
- Adapter package drift validation fails for missing, stale, or unexpected generated output.
- Public documentation describes installation, canonical-versus-generated ownership, and the support matrix.
- Release verification rejects placeholder release checks.
- Release verification rejects RC publication when any non-smoke RC gate fails.
- Release verification rejects RC publication when any smoke row is `fail`.
- Release verification rejects RC publication when `not-run` or `blocked` smoke rows lack required reason and owner fields.
- Release verification rejects `v0.1.0` when any supported adapter lacks passing smoke evidence.
- `docs/releases/v0.1.0-rc.1/release.yaml` and `docs/releases/v0.1.0/release.yaml` satisfy the required release metadata shape when their corresponding releases are prepared.
- `v0.1.0-rc.1` is allowed before full smoke only when all non-smoke RC gates pass.
- `v0.1.0` is allowed only when adapter generation, validation, documentation, release notes, and smoke matrix evidence all pass.
- No generated adapter package contains secrets, machine-local paths, or default permission-bypass configuration.

## Open questions

None.

## Next artifacts

- `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md`
- `docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- `specs/multi-agent-adapters-first-public-release.test.md`
- Change-local artifacts under `docs/changes/<change-id>/` during implementation.

## Follow-on artifacts

- `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md`
- `docs/adr/ADR-20260424-generated-adapter-packages.md`
- `docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- `specs/multi-agent-adapters-first-public-release.test.md`

## Readiness

Spec review is complete and this spec is approved.

The required architecture is approved, the execution plan exists, and the matching test spec is active.

Immediate next repository stage: `implement`.
