# Stop Tracking Generated Public Adapter Skill Bodies

## Status

approved

## Related proposal

- [Stop Tracking Generated Public Adapter Skill Bodies for v0.1.3](../docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md)

## Goal and context

This spec defines the `v0.1.3` release contract for retiring tracked generated public adapter skill bodies after the `v0.1.2` archive-introduction compatibility release.

`v0.1.2` shipped per-adapter downloadable archives while keeping repository-tree adapter skill bodies under `dist/adapters/**/skills` for the compatibility window. `v0.1.3` completes the migration by making release archives the active public adapter install path and by keeping only adapter metadata and install guidance tracked under `dist/adapters/`.

The contract preserves `skills/` as the only authored skill source, preserves Codex, Claude Code, and opencode adapter support, and moves adapter validation from tracked generated skill trees to generated temporary or release-output directories.

## Relationship to prior adapter specs

This spec amends the approved public adapter packaging model for `v0.1.3` and later.

For `v0.1.3` and later, this spec supersedes prior requirements that treat generated public adapter skill bodies, adapter instruction entrypoints, and adapter command-wrapper fragments under `dist/adapters/<adapter>/` as tracked repository package output.

Superseded tracked-package expectations include requirements from:

- `specs/multi-agent-adapters-first-public-release.md`
- `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`

where those requirements expect generated adapter package contents under `dist/adapters/<adapter>/` to remain tracked, stale-checkable repository files.

This spec does not supersede adapter support itself.

The following obligations remain active:

- support Codex, Claude Code, and opencode adapters;
- generate public adapter output from canonical `skills/`;
- validate generated adapter output;
- publish or preserve release archive artifacts;
- record adapter artifact metadata and checksums;
- validate release archive structure;
- keep `dist/adapters/README.md` and `dist/adapters/manifest.yaml` as tracked support and install-guidance surfaces;
- keep public skill portability and token-cost benchmark source rules;
- preserve release smoke, adapter validation, and release verification obligations.

After this spec takes effect, generated public adapter skill bodies are validated from temporary build output or release artifact output, not from tracked `dist/adapters/**/skills` files.

## Glossary

- `canonical skills`: authored skill source under `skills/`.
- `generated public adapter skill body`: generated skill text under adapter skill roots such as `dist/adapters/codex/.agents/skills/`.
- `tracked adapter metadata`: repository-visible adapter metadata and install guidance that remains tracked under `dist/adapters/`.
- `release archive`: a downloadable adapter archive attached to a GitHub release.
- `public adapter output`: generated installable adapter package output for Codex, Claude Code, or opencode.
- `temporary adapter output`: generated adapter package output in a temporary or release-output directory outside tracked `dist/adapters/`.
- `archive-install model`: installing public adapters from release archives rather than copying tracked repository-tree skill bodies.
- `root guidance`: contributor and workflow guidance in `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md`.
- `install-contract surface`: `dist/adapters/README.md`, the tracked surface that points users to active public adapter installation.
- `support matrix`: `dist/adapters/manifest.yaml`.

## Examples first

### Example E1: `v0.1.3` retires tracked adapter skill bodies

Given `v0.1.2` is published with adapter archives
When `v0.1.3` is prepared
Then tracked files under `dist/adapters/codex/.agents/skills/**`, `dist/adapters/claude/.claude/skills/**`, and `dist/adapters/opencode/.opencode/skills/**` are removed
And `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain tracked.

### Example E2: validation uses generated output

Given tracked `dist/adapters/**/skills` no longer exists
When release validation runs
Then adapter packages are generated into a temporary release-output directory
And adapter validation checks that generated output
And validation does not require tracked generated skill bodies.

### Example E3: root guidance no longer advertises retired install paths

Given `CONSTITUTION.md`, `AGENTS.md`, or `docs/workflows.md` mentions compatibility-window repository-tree adapter skill bodies
When the `v0.1.3` release changes the active install model
Then the guidance is updated or version-qualified
And ordinary contributors are directed to `dist/adapters/README.md` or release archives for public adapter installation.

### Example E4: non-skill adapter output is treated consistently

Given adapter instruction entrypoints and opencode command wrappers are generated package output
When tracked generated adapter skill bodies are removed
Then generated adapter instruction entrypoints and command wrappers under adapter package roots are also not retained as tracked installable package fragments
And the release archives carry complete installable adapter packages.

### Example E5: token-cost benchmarks use public adapter output

Given token-cost benchmarks run for `v0.1.3`
When the benchmark source is recorded
Then it points to generated public adapter output or release archive output
And it does not point to `.codex/skills/`.

### Example E6: rollback before publication

Given `v0.1.3` validation cannot generate or validate adapter archives
When release readiness is evaluated
Then the release does not publish
And maintainers may restore tracked generated adapter skill bodies from generated output or defer untracking.

## Requirements

### Release phase and source ownership

R0. This spec applies to `v0.1.3` and later, or to the first release after `v0.1.2` that retires tracked generated public adapter skill bodies.

R0a. `v0.1.2` remains the compatibility-window release that shipped downloadable adapter archives while keeping tracked repository-tree adapter skill bodies.

R0b. This spec MUST NOT retroactively invalidate `v0.1.2` release evidence or historical tracked adapter package output.

R1. `v0.1.3` MUST be the first untracking release for generated public adapter skill bodies unless a newer target version is chosen by an accepted replacement proposal or release plan.

R2. The release MUST treat `v0.1.2` as satisfying the compatibility-window precondition because it shipped a stable public release with tracked repository-tree adapter packages, per-adapter release archives, adapter artifact metadata, checksums, and install guidance.

R3. `skills/` MUST remain the only authored skill source.

R4. Generated public adapter skill bodies MUST NOT be treated as authored source.

R5. The release MUST preserve public adapter support for Codex, Claude Code, and opencode.

R6. The release MUST NOT change workflow stage order.

R7. The release MUST NOT change public skill behavior except where wording is required to remove obsolete generated-output or retired install-path references.

### Tracked and untracked adapter surfaces

R8. After this migration, tracked files under `dist/adapters/` MUST be limited to:

```text
dist/adapters/README.md
dist/adapters/manifest.yaml
```

R9. Tracked generated public adapter skill bodies under `dist/adapters/codex/.agents/skills/**` MUST be removed.

R10. Tracked generated public adapter skill bodies under `dist/adapters/claude/.claude/skills/**` MUST be removed.

R11. Tracked generated public adapter skill bodies under `dist/adapters/opencode/.opencode/skills/**` MUST be removed.

R12. Generated adapter instruction entrypoints under `dist/adapters/codex/AGENTS.md`, `dist/adapters/claude/CLAUDE.md`, and `dist/adapters/opencode/AGENTS.md` MUST NOT remain tracked installable package fragments after this migration.

R13. Generated opencode command wrappers under `dist/adapters/opencode/.opencode/commands/**` MUST NOT remain tracked installable package fragments after this migration.

R14. Complete adapter packages, including instruction entrypoints, skills, and opencode command wrappers, MUST remain present in generated temporary adapter output and release archives.

R15. Generated adapter archives MUST NOT be committed to Git.

### Tracked adapter surface after migration

R15a. For `v0.1.3` and later, the tracked adapter support surface MUST be limited to:

```text
dist/adapters/README.md
dist/adapters/manifest.yaml
```

R15b. Additional tracked adapter metadata or template files MAY remain under `dist/adapters/` only when this spec or a later approved spec names them explicitly.

R15c. Generated public adapter output under the following paths MUST NOT remain tracked:

```text
dist/adapters/codex/.agents/skills/**
dist/adapters/claude/.claude/skills/**
dist/adapters/opencode/.opencode/skills/**
```

R15d. Generated adapter instruction entrypoints or command-wrapper fragments that are package output rather than source templates MUST NOT remain tracked.

### Public install contract

R16. `dist/adapters/README.md` MUST be the tracked install-contract surface for public adapter installation.

R17. `dist/adapters/README.md` MUST state that `skills/` is the canonical authored source.

R18. `dist/adapters/README.md` MUST state that generated public adapter skill bodies are not tracked source after `v0.1.3`.

R19. `dist/adapters/README.md` MUST state that `v0.1.3` and later public adapter installation uses GitHub release archives.

R20. `dist/adapters/README.md` MUST identify `dist/adapters/manifest.yaml` as the tracked adapter support matrix.

R21. `dist/adapters/README.md` MUST list per-adapter archive names or naming patterns for Codex, Claude Code, and opencode.

R22. `dist/adapters/README.md` MUST list target install roots for Codex, Claude Code, and opencode.

R23. `dist/adapters/README.md` MUST identify where adapter artifact metadata and checksums are recorded.

R24. `dist/adapters/README.md` MUST NOT present tracked `dist/adapters/**/skills` as the active public install path for `v0.1.3` or later.

R25. Historical compatibility-window wording MAY remain only when it is explicitly version-qualified.

### Root guidance alignment

R26. `CONSTITUTION.md` MUST be audited and updated or explicitly recorded as unaffected.

R27. `AGENTS.md` MUST be audited and updated or explicitly recorded as unaffected.

R28. `docs/workflows.md` MUST be audited and updated or explicitly recorded as unaffected.

R29. Updated root guidance MUST NOT direct ordinary users to install public adapters from retired tracked adapter skill-body paths as the active model.

R30. Updated root guidance SHOULD point ordinary contributors to `dist/adapters/README.md` as the install-contract surface instead of duplicating release archive details.

R31. Compatibility-window history in root guidance MUST be removed from active rules or made explicitly version-qualified.

R32. If any required guidance surface is unchanged, the implementation MUST record a short unaffected rationale in a tracked or review-visible surface.

### Adapter generation and validation

R33. Adapter validation MUST generate adapter output into a temporary or release-output directory outside tracked `dist/adapters/`.

R34. Adapter validation MUST validate generated temporary or release-output adapter packages for Codex, Claude Code, and opencode.

R35. Adapter validation MUST NOT require tracked files under `dist/adapters/**/skills`.

R36. Any drift check that compares canonical skills to tracked `dist/adapters/**/skills` MUST be retired or replaced with generated-output validation.

R37. Release validation MUST fail when tracked generated public adapter skill bodies remain under `dist/adapters/**/skills`.

R38. Release validation MUST fail when `dist/adapters/README.md` or `dist/adapters/manifest.yaml` is missing.

R39. Release validation MUST fail when generated temporary or release-output adapter packages are missing required adapter skills.

R40. Release validation MUST fail when generated opencode release output omits required command wrappers defined by the support matrix.

R41. Release validation MUST fail when generated adapter archives are missing, malformed, or do not install to their target roots.

### Validation replacement

R41a. Any prior validation rule that required tracked generated adapter package files under `dist/adapters/<adapter>/` to exist or match canonical generated output is superseded for `v0.1.3` and later.

R41b. Replacement validation MUST prove canonical skills validate from `skills/`.

R41c. Replacement validation MUST prove adapter packages can be generated from canonical skills.

R41d. Replacement validation MUST prove generated adapter output has the expected structure for Codex, Claude Code, and opencode.

R41e. Replacement validation MUST prove release archives contain the expected adapter files.

R41f. Replacement validation MUST prove adapter artifact metadata and checksums are valid.

R41g. Replacement validation MUST prove release verification no longer depends on tracked generated adapter skill bodies.

### Adapter artifact metadata and release evidence

R42. `v0.1.3` MUST include adapter artifact metadata under `docs/reports/adapter-artifacts/releases/v0.1.3.yaml`.

R43. Adapter artifact metadata MUST record the release version, source commit, release date, generator command, source skills, manifest path, per-adapter archive names, checksums, install roots, per-adapter result, validation command, validation result, and validation timestamp.

R44. Adapter artifact metadata MUST validate checksums against the generated or published adapter archives.

R45. `release.source_commit` MUST match the release commit input used by release validation unless an approved release policy exception is recorded.

R46. `v0.1.3` release notes MUST state that generated public adapter skill bodies are no longer tracked source.

R47. `v0.1.3` release notes MUST state that release archives are the active public adapter install path.

R48. `v0.1.3` release notes MUST identify where adapter artifact metadata and checksums are recorded.

R49. `v0.1.3` release notes MUST identify the maintainer-facing release gate.

R50. `bash scripts/release-verify.sh v0.1.3` MUST be the maintainer-facing final release gate.

R51. `scripts/validate-release.py` MUST own structured release metadata validation and MUST be delegated from the maintainer-facing release gate.

### Token-cost evidence

R52. `v0.1.3` MUST include token-cost Markdown and YAML evidence under `docs/reports/token-cost/releases/`.

R53. Static token-cost measurement MUST use canonical `skills/`.

R54. Dynamic token-cost benchmark inputs MUST use generated public adapter output or release archive output.

R55. Dynamic token-cost benchmark inputs MUST NOT use `.codex/skills/` as the public adapter skill source.

R56. Token-cost validation MUST fail when a dynamic public-surface benchmark records `.codex/skills/` as the skill source.

R57. A scoped benchmark-source validation MAY supplement but MUST NOT replace the `v0.1.3` token-cost release report unless an approved release policy exception is recorded.

### Deferred scope

R58. The release MUST NOT move `docs/changes/0001-skill-validator/` as part of this slice.

R59. The release MUST NOT perform broad progressive-loading or high-cost public skill optimization as part of this slice.

R60. The release MUST NOT introduce new token-cost threshold gates as part of this slice.

R61. The release MUST NOT rewrite Git history to remove previously tracked generated adapter output.

### Test-spec coverage

R62. The matching test spec MUST cover cross-spec supersession for the `v0.1.3` tracked-package model.

R63. The matching test spec MUST verify that tracked generated adapter skill bodies under `dist/adapters/**/skills` are not required for `v0.1.3` and later.

R64. The matching test spec MUST verify that prior tracked-package drift checks are retired or replaced by temporary-output or release-artifact validation.

R65. The matching test spec MUST verify that `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain tracked.

R66. The matching test spec MUST verify that generated public adapter archives validate without tracked adapter skill bodies.

R67. The matching test spec MUST verify that release validation fails if it still requires tracked `dist/adapters/**/skills`.

R68. The matching test spec MUST verify that release validation still requires generated adapter output validation, metadata, checksums, and release archive proof.

## Inputs and outputs

Inputs:

- release version `v0.1.3`;
- canonical skills under `skills/`;
- adapter support matrix at `dist/adapters/manifest.yaml`;
- install-contract surface at `dist/adapters/README.md`;
- root guidance in `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md`;
- release notes under `docs/releases/v0.1.3/release-notes.md`;
- adapter artifact metadata under `docs/reports/adapter-artifacts/releases/v0.1.3.yaml`;
- token-cost reports under `docs/reports/token-cost/releases/v0.1.3.md` and `.yaml`;
- generated temporary or release-output adapter packages;
- per-adapter release archives.

Outputs:

- tracked source tree without generated public adapter skill bodies;
- tracked `dist/adapters/README.md` and `dist/adapters/manifest.yaml`;
- generated and validated per-adapter release archives;
- adapter artifact metadata with checksums;
- root guidance aligned with the archive-install model;
- release notes explaining the retired repository-tree adapter skill-body path;
- token-cost release evidence;
- passing maintainer release gate.

## State and invariants

- `skills/` is the only authored skill source.
- Generated adapter output is reproducible from canonical sources.
- `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain tracked.
- Generated public adapter skill bodies are release artifacts or temporary validation output, not tracked source.
- `.codex/skills/` remains local runtime state and not a public adapter install source.
- Release archives remain the public adapter install surface for `v0.1.3` and later.
- Adapter support for Codex, Claude Code, and opencode remains intact.

## Error and boundary behavior

- If `v0.1.2` archive assets or metadata are found not to exist, `v0.1.3` untracking MUST stop until the compatibility-window precondition is restored or a policy exception is accepted.
- If generated adapter output cannot be built, the release MUST NOT publish.
- If generated adapter output validates but release archives are missing, the release MUST NOT publish.
- If any required root guidance surface remains stale without an unaffected rationale, the release MUST NOT be considered ready.
- If token-cost benchmark tooling cannot produce `v0.1.3` release evidence, release readiness MUST follow the existing token-cost waiver or exception process.
- If release validation still requires tracked `dist/adapters/**/skills`, implementation MUST update validation before untracking can proceed.
- If generated package output omits a required adapter, release validation MUST fail.
- If rollback is needed before publication, tracked adapter skill bodies MAY be regenerated from `skills/` and restored in a follow-up decision.

## Compatibility and migration

`v0.1.2` remains the stable compatibility release that supports both repository-tree adapter packages and release archives. `v0.1.3` retires repository-tree generated adapter skill-body installation and makes release archives the active public adapter install path.

Historical docs may mention `v0.1.1` or `v0.1.2` behavior, but active contributor and install guidance must not describe tracked generated adapter skill bodies as the current install model.

The migration is not a breaking change for users who use `v0.1.2` release archives or switch to `v0.1.3` release archives. Users who copied adapter skill trees from the repository branch must switch to release archives.

Rollback before `v0.1.3` publication is to restore generated adapter output from canonical `skills/`, keep `dist/adapters/**/skills` tracked, and defer release publication. Rollback after publication requires a new release or documented recovery because already-published release assets should remain immutable.

## Observability

- Release validation output SHOULD identify whether tracked adapter skill bodies are expected for the release version.
- Release validation output SHOULD identify the temporary or release-output directory used for adapter validation.
- Release validation output SHOULD identify the adapter artifact metadata path.
- Release validation output SHOULD identify root-guidance audit results.
- Release notes MUST make the active install path clear to downstream users.
- Token-cost reports MUST identify the public adapter skill source used for dynamic benchmarks.

## Security and privacy

- Adapter archives and metadata MUST NOT include secrets, credentials, private keys, private tokens, or machine-local install paths.
- Release metadata MUST NOT rely on private local files that ordinary maintainers cannot inspect.
- Checksums MUST be used to detect archive mismatch or unintended replacement.
- Validation SHOULD avoid printing full generated skill bodies or archive contents in normal output.
- Root guidance MUST NOT instruct users to copy from private local runtime directories such as `.codex/skills/`.

## Accessibility and UX

No end-user UI is introduced.

Documentation UX requirements:

- `dist/adapters/README.md` must make the active install path easy to find;
- release notes must state that tracked repository-tree generated skill bodies have been retired;
- historical compatibility wording must be version-qualified;
- ordinary contributors should not need to inspect generated adapter package internals to find the install path.

## Performance expectations

- Adapter generation and validation SHOULD keep normal output concise.
- Release validation SHOULD summarize generated-output checks instead of printing generated skill bodies.
- Token-cost measurement SHOULD use summary reports by default and keep raw benchmark detail in the report artifacts or run output.

## Edge cases

1. `v0.1.3` is already published or reserved: downstream artifacts must choose the next release version through an accepted update.
2. A required adapter archive is missing: release validation fails.
3. `dist/adapters/README.md` is updated but `CONSTITUTION.md` still presents tracked adapter skill bodies as active: release readiness fails unless a tracked unaffected rationale is valid.
4. Generated adapter output passes but tracked `dist/adapters/**/skills` remains in Git: release validation fails.
5. A root guidance file mentions `v0.1.2` compatibility behavior as history: allowed only when clearly version-qualified.
6. Token-cost dynamic benchmarks accidentally use `.codex/skills/`: token-cost validation fails.
7. The release cannot produce a full `v0.1.3` token-cost report: release readiness requires an approved policy exception.
8. A generated opencode archive omits command wrappers: adapter archive validation fails.
9. A maintainer wants to keep non-skill adapter entrypoint files tracked: this spec must be amended before implementation because `v0.1.3` tracks only README and manifest under `dist/adapters/`.
10. Public skill text needs behavior changes unrelated to retired generated-output references: split that work into a separate proposal or spec.

## Non-goals

- Do not remove support for Codex, Claude Code, or opencode.
- Do not change workflow stage order.
- Do not move `docs/changes/0001-skill-validator/`.
- Do not optimize high-cost public skills.
- Do not add new token-cost threshold gates.
- Do not change public skill behavior beyond removing obsolete generated-output or install-path references.
- Do not rewrite Git history.
- Do not commit generated adapter archives.
- Do not make `.codex/skills/` a public install source.
- Do not retain partial tracked adapter packages under `dist/adapters/` after the migration.

## Acceptance criteria

- The proposal status is settled to `accepted` before downstream reliance.
- The spec explicitly names the prior adapter specs it supersedes.
- The supersession is scoped to tracked-package and repository-tree install requirements for `v0.1.3` and later.
- Historical `v0.1.2` compatibility-window evidence remains valid.
- Adapter support obligations remain active.
- Release archive generation, metadata, checksums, and validation obligations remain active.
- `dist/adapters/**/skills` has no tracked files.
- `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain tracked.
- No other files under `dist/adapters/` remain tracked unless this spec is amended.
- Validation no longer expects tracked `dist/adapters/**/skills` after migration.
- Generated temporary or release-output adapter packages validate for Codex, Claude Code, and opencode.
- Per-adapter `v0.1.3` release archives exist and validate.
- `docs/reports/adapter-artifacts/releases/v0.1.3.yaml` exists and validates.
- `docs/releases/v0.1.3/release-notes.md` exists and explains archive installation and repository-tree skill-body retirement.
- `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` are updated or have explicit unaffected rationale.
- `dist/adapters/README.md` points ordinary users to release archives and metadata/checksum locations.
- Token-cost Markdown and YAML reports exist for `v0.1.3`.
- Dynamic token-cost benchmark source is generated public adapter output or release archive output, not `.codex/skills/`.
- `bash scripts/release-verify.sh v0.1.3` passes before publication.

## Open questions

None.

## Next artifacts

```text
spec-review
architecture if validation or release boundaries need a design record
architecture-review if architecture is created or changed
plan
plan-review
test-spec
implement
code-review
explain-change
verify
pr
release
```

## Follow-on artifacts

- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md)
- ADR: [ADR-20260513-v0-1-3-adapter-release-archive-install-surface](../docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md)

## Readiness

Approved after `spec-review-r2` completed with no material findings and closed `SGPA-SR1`.
