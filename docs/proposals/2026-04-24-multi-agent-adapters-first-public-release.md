# Multi-Agent Adapters and First Public Release

## Status
- accepted

## Problem

RigorLoop now has a working first-release baseline for Codex-oriented use, but the public project value is broader than one agent interface. Contributors who use opencode or Claude Code should be able to apply the same RigorLoop workflow without manually translating instructions, copying skills into tool-specific directories, or guessing which generated surfaces are safe to edit.

The repository also still treats release automation conservatively. `scripts/release-verify.sh` explicitly says it is a placeholder, which means the project should not tag a first public version while the release gate cannot prove the basic compatibility and documentation claims that the tag would advertise.

## Goals

- Support Codex, opencode, and Claude Code from the same canonical RigorLoop workflow sources.
- Keep `skills/` and the existing authored workflow artifacts as the source of truth.
- Generate or synchronize tool-specific adapter output deterministically so compatibility files do not become competing authored surfaces.
- Track adapter-specific generated packages that include both project skills and thin instruction entrypoints.
- Ship only skills that pass a portability gate for the target adapter package.
- Make each adapter package independently installable and smoke-tested.
- Publish an adapter manifest that records version, skill portability, supported adapters, and exclusion reasons.
- Document a clear support matrix for the first public version.
- Replace the placeholder release check with repository-specific first-public-release verification.
- Use `v0.1.0-rc.1` before compatibility smoke passes and `v0.1.0` after compatibility smoke passes.

## Non-goals

- Building a hosted agent orchestration platform.
- Mandating one model vendor, editor, or agent interface.
- Replacing Git, pull requests, CI, or human review.
- Publishing package-manager, plugin-marketplace, or installer distributions in the first public version.
- Rewriting the whole repository into a larger `method/`, `adapters/`, or `dist/` layout before the adapter contract proves useful.
- Guaranteeing identical runtime behavior across all agent tools when their discovery, permission, and invocation semantics differ.
- Adding tool-specific secrets, API keys, or account setup to the repository.
- Shipping every existing RigorLoop skill before it passes the portable-core gate.
- Requiring ordinary contributors to have Codex, opencode, and Claude Code installed locally.

## Context

The accepted project direction defines RigorLoop as a Git-first starter kit for AI-assisted software delivery with explicit artifacts, review gates, and explainable change history. The approved first-release architecture already separates canonical workflow content from generated Codex compatibility output:

- canonical authored sources live in `docs/`, `specs/`, `skills/`, `schemas/`, and `scripts/`;
- `.codex/skills/` is generated compatibility output and is not hand-edited;
- CI checks generated-skill drift through repository-owned scripts.

This proposal extends that pattern to additional agent tools instead of changing the source-of-truth model.

Current external compatibility facts need to be captured in a follow-on research/spec artifact before implementation, but the direction is already clear enough to propose:

- opencode documents project rules through `AGENTS.md` and project skills under `.opencode/skills/<name>/SKILL.md`, with compatibility fallbacks for `.claude/skills/` and `.agents/skills/`.
- Claude Code documents project memory through `CLAUDE.md` and project skills under `.claude/skills/<name>/SKILL.md`.
- Both tools support filesystem-based `SKILL.md` concepts closely enough that RigorLoop can plausibly generate adapter copies from canonical `skills/`, while still validating each tool's supported metadata and discovery rules.

Sources consulted on 2026-04-24:

- [opencode rules](https://opencode.ai/docs/rules/)
- [opencode agent skills](https://opencode.ai/docs/skills)
- [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills)

Maintainer decisions recorded on 2026-04-24:

| Question | Decision |
| --- | --- |
| Generated directories | Track adapter-specific generated packages with both project skills and thin instruction entrypoints. |
| `CLAUDE.md` | Generate it from an authored thin template. Do not omit it, but do not duplicate skill bodies inside it. |
| OpenCode support | Use both `AGENTS.md` and `.opencode/skills/`. |
| Existing skills | Do not assume all skills are portable. Ship only skills that pass a portability gate. |
| First public tag | Use `v0.1.0` after compatibility smoke passes. Use `v0.1.0-rc.1` before smoke passes. |
| Manual smoke | A maintainer-run smoke matrix is enough; contributors should not need all tools locally. |

## Options considered

### Option 1: Tag the current Codex-oriented baseline as the first public version

This would publish quickly and avoid additional adapter work.

Advantages:

- Lowest immediate effort.
- Avoids taking on tool-specific compatibility risk before release.
- Uses the already completed first-release baseline.

Disadvantages:

- Undercuts the project direction of a tool-agnostic workflow.
- Leaves opencode and Claude Code users to translate the workflow manually.
- Risks publishing a first version while release verification is still explicitly placeholder.

### Option 2: Add handwritten opencode and Claude Code docs only

This would add `CLAUDE.md`, opencode notes, and README guidance without generated skill adapters.

Advantages:

- Simple to review.
- Gives non-Codex users a starting point.
- Avoids changing generator scripts immediately.

Disadvantages:

- Creates duplicated guidance that can drift from canonical workflow sources.
- Does not make RigorLoop skills available through each tool's native discovery path.
- Provides weak evidence for a first public release because the compatibility claim remains mostly manual.

### Option 3: Generate first-class adapter packages for Codex, opencode, and Claude Code

This keeps canonical workflow content in the existing source locations and extends deterministic generated output to each supported tool. Adapter surfaces include tracked packages under `dist/adapters/`, project skill output for each tool, and thin instruction entrypoints such as `AGENTS.md` or `CLAUDE.md`.

Advantages:

- Aligns with the existing architecture decision instead of adding parallel authored trees.
- Gives each supported tool a native discovery path.
- Makes compatibility drift testable in CI.
- Provides a credible first public release boundary.
- Lets each adapter package be installed and smoked independently.

Disadvantages:

- Requires a spec for tool-specific filesystem paths, supported metadata fields, and validation behavior.
- May expose differences between RigorLoop skills and each tool's skill semantics.
- Adds generated output that reviewers must understand as derived distribution.
- Requires a portability gate before skills can ship in non-Codex adapter packages.

### Option 4: Wait for packaged plugins or marketplaces before release

This would delay the first public version until RigorLoop can distribute through tool-native package or plugin mechanisms.

Advantages:

- Could create a cleaner install story later.
- Might reduce checked-in generated output over time.
- Positions RigorLoop for broader distribution channels.

Disadvantages:

- Too large for the first public release.
- Adds marketplace-specific maintenance before the core workflow has enough external usage.
- Delays useful support for contributors who can already consume project-local files.

## Recommended direction

Choose Option 3.

RigorLoop should ship its first public version only after it supports Codex, opencode, and Claude Code through a deterministic adapter-generation contract backed by validation. The core workflow remains tool-agnostic and authored once. Tool-specific package directories and entrypoint files become generated adapter output from canonical source and authored thin templates, not new sources of truth.

The generated adapter package layout should be:

```text
dist/adapters/codex/
  AGENTS.md
  .agents/
    skills/
      <skill-name>/
        SKILL.md

dist/adapters/claude/
  CLAUDE.md
  .claude/
    skills/
      <skill-name>/
        SKILL.md

dist/adapters/opencode/
  AGENTS.md
  .opencode/
    skills/
      <skill-name>/
        SKILL.md
```

For opencode, `AGENTS.md` provides project-level operating guidance and `.opencode/skills/` provides reusable workflow skills.

The first release should include a generated manifest:

```yaml
version: 0.1.0
skills:
  workflow:
    portable: true
    adapters: [codex, claude, opencode]
  code-review:
    portable: true
    adapters: [codex, claude, opencode]
  some-codex-only-skill:
    portable: false
    adapters: [codex]
    reason: Uses Codex-only metadata or invocation assumptions.
```

For v1, RigorLoop should define a portable-core gate. A skill is portable only if it:

- uses Agent Skills-compatible `SKILL.md` structure;
- has portable `name` and `description`;
- does not require Codex-only invocation syntax;
- does not depend on `agents/openai.yaml`;
- does not reference `.codex/skills` as the only install location;
- does not assume Codex-only tools, UI, or approval behavior;
- uses generic stage names and artifact paths;
- has no hidden dependency on Codex-specific `$skill` invocation.

Only skills that pass portability validation should ship in the relevant adapter package. Skills with tool-specific assumptions should be excluded or transformed with explicit validation.

The first public release should be conservative. It should claim project-local workflow and skill support for the three named tools, a documented support matrix, deterministic drift checks, and repository-specific release verification. It should not claim marketplace packaging, model-specific optimization, hosted orchestration, or identical behavior across tools.

This direction directly addresses the current gap: the project has enough workflow substance to release, but its public claim should not be Codex-only when the intended audience includes AI-assisted contributors using different agent interfaces.

## Expected behavior changes

- The README and workflow docs will describe RigorLoop as usable with Codex, opencode, and Claude Code.
- Contributors will know which files are canonical and which tool-specific files are generated adapter output.
- `dist/adapters/manifest.yaml` will describe the generated adapter package version, portable skills, supported adapters, and exclusion reasons.
- Adapter packages under `dist/adapters/` will be independently installable and smoke-tested.
- opencode users will get project-local RigorLoop instructions and skill discovery without manually copying Codex output.
- Claude Code users will get project-local RigorLoop instructions and skill discovery without manually converting `AGENTS.md` or `skills/`.
- Existing RigorLoop skills that fail the portable-core gate will not ship in unsupported adapters until they are fixed or explicitly transformed.
- Repository validation will detect stale adapter output for every supported tool.
- Release verification will stop advertising a placeholder checklist and will check the first-public-release support surfaces before tag publication.
- `v0.1.0-rc.1` will remain the pre-smoke release candidate boundary; `v0.1.0` will be used only after compatibility smoke passes.

## Architecture impact

The expected architecture impact is an extension of the current canonical-versus-generated boundary.

Components likely touched:

- `skills/` as the canonical source for reusable RigorLoop skills.
- Authored thin instruction templates used to generate adapter entrypoints.
- `dist/adapters/codex/AGENTS.md` and `dist/adapters/codex/.agents/skills/` as the public Codex adapter package.
- `dist/adapters/claude/CLAUDE.md` and `dist/adapters/claude/.claude/skills/` as the public Claude Code adapter package.
- `dist/adapters/opencode/AGENTS.md` and `dist/adapters/opencode/.opencode/skills/` as the public opencode adapter package.
- `dist/adapters/manifest.yaml` as the generated support matrix and portability record.
- `scripts/build-skills.py` or a successor adapter-generation script.
- `scripts/ci.sh` and release verification scripts.
- `README.md`, `docs/workflows.md`, `AGENTS.md`, and release documentation.
- Artifact lifecycle validation rules so generated adapter packages are not treated as authored lifecycle-managed sources.
- Existing `.codex/skills/` compatibility output and ADR guidance, which the follow-on architecture must either preserve as a local development mirror or supersede explicitly.

Expected boundaries:

- Canonical workflow contract stays in `specs/` and `docs/`.
- Canonical skill content stays in `skills/`.
- Tool-specific adapter output is reproducible and drift-checked.
- Generated adapter paths are not used as authored lifecycle-managed sources.
- Each adapter package is installable without requiring unrelated adapter package files.
- Maintainer-run smoke evidence is sufficient for release readiness; ordinary contributors do not need every supported tool locally.
- Release automation remains a verification and publishing surface, not a workflow-definition surface.

## Testing and verification strategy

Follow-on specs should map compatibility and release claims to concrete checks:

- Fixture tests for adapter generation across Codex, opencode, and Claude Code.
- Drift checks that fail when any generated adapter output is missing, stale, or unexpectedly edited.
- Validation that shared `SKILL.md` metadata stays inside the supported common subset, or that tool-specific transforms are explicitly tested.
- Portable-core validation that excludes or transforms skills with Codex-only assumptions.
- Manifest validation for version, portability flags, adapter lists, and exclusion reasons.
- Per-adapter install smoke checks against `dist/adapters/codex/`, `dist/adapters/claude/`, and `dist/adapters/opencode/`.
- Artifact lifecycle validation that ignores generated adapter output as authored source while still detecting stale authoritative artifacts.
- Documentation checks for the support matrix and source-of-truth wording.
- Release verification that checks tag format, release notes, current branch/commit expectations, local CI proof, generated adapter sync, smoke evidence, and absence of placeholder release wording.
- Maintainer-run manual smoke matrix for the supported tools, with contributors allowed to rely on the recorded matrix instead of installing all tools locally.

## Rollout and rollback

Rollout should proceed through the normal downstream lifecycle:

- Write the compatibility and release spec.
- Review the spec before implementation.
- Add architecture for adapter roots, generated-output ownership, and release verification boundaries.
- Plan the implementation as one or more reviewable milestones.
- Implement adapter generation, validation, docs, and release checks.
- Publish `v0.1.0-rc.1` before full compatibility smoke passes if an RC is useful.
- Publish `v0.1.0` only after compatibility smoke passes and the release notes match the support matrix.

Rollback before tagging is straightforward: revert generated adapter output, generator changes, documentation claims, and release-script changes.

Rollback after tagging should avoid deleting history. If a released adapter claim is wrong, publish a corrective patch release or release note that narrows the support matrix, then fix the generator or docs in the next version.

## Risks and mitigations

- Risk: Tool-specific skill semantics diverge enough that byte-for-byte skill copies are misleading.
  Mitigation: The spec should define the shared subset and require tool-specific transforms or exclusions when a field is unsupported or changes behavior.
- Risk: Generated adapter output creates review noise and obscures the real authored change.
  Mitigation: Keep generated roots clearly documented, deterministic, and covered by drift checks; group generated changes separately in PR summaries.
- Risk: Root instruction files duplicate workflow rules and drift from `CONSTITUTION.md`, `specs/`, or `docs/workflows.md`.
  Mitigation: Keep entrypoints thin and point to canonical artifacts instead of restating full contracts.
- Risk: First public release claims more compatibility than the repository can prove.
  Mitigation: Use a conservative support matrix and make release verification check the exact advertised surfaces.
- Risk: Release automation publishes from the wrong commit or with stale notes.
  Mitigation: Replace the placeholder release script with explicit checks for tag format, target branch/commit expectations, CI evidence, generated drift, and release-note consistency.
- Risk: Agent tools change their discovery rules after the proposal is written.
  Mitigation: Keep external-tool facts in the research/spec artifacts, cite official docs, and treat adapter paths as versioned compatibility surfaces that can change in later releases.
- Risk: Security-sensitive tool permissions are accidentally broadened by generated adapters.
  Mitigation: Do not add permissive tool access metadata by default; require explicit spec coverage before adding tool-specific permission fields.
- Risk: The new `dist/adapters/codex/` package conflicts with existing `.codex/skills/` assumptions.
  Mitigation: The architecture artifact should explicitly decide whether `.codex/skills/` remains a local development compatibility mirror, becomes generated from the same adapter contract, or is superseded.
- Risk: Excluding non-portable skills makes the first adapter packages feel incomplete.
  Mitigation: Publish the exclusion reason in `dist/adapters/manifest.yaml` and treat portability fixes as follow-up work instead of silently shipping misleading skills.

## Open questions

None at the proposal level.

The maintainer resolved the prior proposal-level questions on 2026-04-24. Follow-on spec and architecture work should still define detailed transform behavior, the exact portable-core validator contract, the smoke matrix format, and how existing `.codex/skills/` compatibility output relates to the new `dist/adapters/codex/` package.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-04-24 | Draft a new initiative for multi-agent adapter support plus first public release readiness. | The existing first-release baseline is Codex-oriented and the release verifier is still placeholder, so the public tag needs a stronger compatibility and release boundary. | Tagging the current baseline as-is would overstate readiness. |
| 2026-04-24 | Recommend generated adapter outputs from canonical RigorLoop sources. | This extends the approved source-of-truth architecture and keeps compatibility drift testable. | Handwritten tool docs would drift; marketplace packaging is premature. |
| 2026-04-24 | Keep first public release claims conservative. | The project can credibly claim project-local workflow and skill support before claiming packaged distribution or identical runtime behavior. | Broad platform or plugin-marketplace claims would exceed current evidence. |
| 2026-04-24 | Accept source-authored-once workflow content, generated adapter packages, independent installability, and smoke-tested adapter packages as the initiative direction. | The maintainer resolved the core proposal tradeoff in favor of generated adapter packages rather than handwritten per-tool copies. | Handwritten docs-only support and current-baseline tagging remain insufficient. |
| 2026-04-24 | Use `dist/adapters/codex/`, `dist/adapters/claude/`, and `dist/adapters/opencode/` as tracked generated package roots. | Public adapter packages need a stable installable tree that can be validated independently. | Root-level generated files alone would blur repository operating guidance with package output. |
| 2026-04-24 | Generate `CLAUDE.md` from an authored thin template and use both `AGENTS.md` and `.opencode/skills/` for opencode. | Tool entrypoints should exist where users expect them, but they should not duplicate skill bodies or compete with canonical workflow docs. | Omitting `CLAUDE.md` or relying only on skills would make adoption less direct. |
| 2026-04-24 | Gate shipped skills through a portable-core validator. | Existing skills may contain Codex-only invocation, tool, UI, approval, or install-location assumptions. | Assuming all current skills are portable would create misleading adapter packages. |
| 2026-04-24 | Use `v0.1.0-rc.1` before compatibility smoke passes and `v0.1.0` after smoke passes. | The release sequence should distinguish generated package readiness from fully smoked public compatibility. | Tagging `v0.1.0` before smoke would overstate release confidence. |
| 2026-04-24 | Use a maintainer-run smoke matrix as the manual compatibility proof. | Maintainers can verify supported tools without requiring every contributor to install all toolchains locally. | Contributor-local all-tool smoke would raise adoption friction without improving baseline release evidence. |

## Next artifacts

- `specs/multi-agent-adapters-first-public-release.md`
- `specs/multi-agent-adapters-first-public-release.test.md`
- `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md`
- `docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- Change-local artifacts under `docs/changes/<change-id>/` during implementation.

## Follow-on artifacts

- `specs/multi-agent-adapters-first-public-release.md`
- `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md`
- `docs/adr/ADR-20260424-generated-adapter-packages.md`
- `docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- `specs/multi-agent-adapters-first-public-release.test.md`

## Readiness

This proposal is accepted.

The compatibility and release spec and architecture are approved, the execution plan exists, and the matching test spec is active.

Immediate next repository stage: `implement`.
