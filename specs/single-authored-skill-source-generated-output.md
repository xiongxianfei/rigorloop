# Single Authored Skill Source and Generated Output

## Status

approved

## Related proposal

- [Single Authored Skill Source and Generated Adapter Output Cleanup](../docs/proposals/2026-05-12-single-authored-skill-source-and-generated-adapter-output-cleanup.md)

## Goal and context

This spec defines the source-of-truth, validation, migration, and release-artifact contract for RigorLoop skill output.

RigorLoop skills are authored once under `skills/`. Generated local runtime mirrors and public adapter packages are derived output. The repository currently tracks generated `.codex/skills/` and generated public adapter skill copies under `dist/adapters/`, which creates duplicate review surfaces and makes generated output look like authored source.

This spec changes that contract in stages:

- first, `.codex/skills/` becomes untracked repository-local generated output;
- later, public adapter skill copies under `dist/adapters/**/skills` move from day-to-day tracked Git state to generated release artifacts after compatibility and release evidence are ready;
- `dist/adapters/manifest.yaml`, `dist/adapters/README.md`, and adapter artifact metadata remain tracked support and release evidence surfaces.

This spec intentionally amends older generated-output expectations in the multi-agent adapter and skill-contract specs. Until public adapter skill copies are migrated, existing tracked `dist/adapters/**/skills` drift checks remain in force.

## Glossary

- `canonical skill source`: an authored skill file under `skills/<skill>/SKILL.md`.
- `local Codex mirror`: generated repository-local Codex runtime output under `.codex/skills/`.
- `public adapter package`: generated installable output for Codex, Claude Code, or opencode.
- `public adapter skill copy`: a generated skill body under a public adapter skill path such as `dist/adapters/codex/.agents/skills/<skill>/SKILL.md`.
- `tracked support metadata`: adapter support or release metadata intentionally kept in Git, including `dist/adapters/manifest.yaml`, `dist/adapters/README.md`, and adapter artifact metadata.
- `adapter artifact metadata`: tracked YAML release evidence stored under `docs/reports/adapter-artifacts/releases/<version>.yaml`.
- `release artifact`: a generated adapter archive uploaded as a release asset rather than committed to Git.
- `temp-output validation`: generation and validation performed against a temporary output directory or release artifact directory instead of tracked generated files.
- `repository-tree install path`: installation by copying tracked files from `dist/adapters/<adapter>/` in the repository tree.
- `artifact-install path`: installation by downloading a generated adapter archive from release assets.

## Examples first

### Example E1: `.codex/skills/` is untracked but generatable

Given `.codex/skills/` has been removed from tracked Git files
When a contributor runs the documented local mirror generation command
Then the command generates a Codex-compatible skill mirror from `skills/`
And validation passes against generated output
And no tracked `.codex/skills/<skill>/SKILL.md` file is required.

### Example E2: first slice leaves public adapters tracked

Given the first implementation slice removes `.codex/skills/` from tracked Git state
When the slice is complete
Then public adapter skill copies under `dist/adapters/` remain tracked
And existing public adapter installation from the repository tree continues to work.

### Example E3: tracked manifest remains text-only support metadata

Given public adapter skill copies later move to release artifacts
When `dist/adapters/manifest.yaml` remains tracked
Then it records adapter support metadata and skill inclusion decisions
And it does not contain generated skill bodies.

### Example E4: public adapter release artifacts are reproducible

Given release `v0.1.2` publishes generated adapter packages
When release validation completes
Then `docs/reports/adapter-artifacts/releases/v0.1.2.yaml` records the source commit, generator command, artifact archives, checksums, manifest path, validation command, and validation result
And reviewers can reproduce the generated archives from tracked sources at the recorded commit.

### Example E5: public adapter cleanup waits for compatibility window

Given release `v0.1.2` first provides downloadable adapter artifacts and installation docs
When public adapter skill copies are still tracked in `dist/adapters/`
Then release `v0.1.2` announces the repository-tree install path transition
And a later stable release may remove tracked public adapter skill copies only after the compatibility window has been satisfied.

### Example E6: release benchmark rejects local mirror as public source

Given a Token-Friendliness benchmark configuration uses `.codex/skills/` as the public skill source
When release benchmark validation runs
Then validation fails because public-surface benchmarks must use generated public adapter output or release artifact output, not the repository-local Codex mirror.

### Example E7: adapter archives are release assets, not committed files

Given a release workflow generates `rigorloop-adapter-codex-v0.1.2.zip`
When the release is prepared
Then the archive is uploaded as a release asset
And Git tracks the checksum and metadata
But Git does not track the generated archive file by default.

## Requirements

### Source of truth

R1. Canonical skill source MUST be authored under `skills/<skill>/SKILL.md`.

R2. `.codex/skills/` MUST be treated as generated local Codex runtime output, not authored source.

R3. Public adapter skill copies under `dist/adapters/**/skills` MUST be treated as generated public adapter output, not authored source.

R4. Contributors MUST NOT hand-edit `.codex/skills/` or generated public adapter skill copies to change RigorLoop skill behavior.

R5. Skill behavior changes MUST be made through canonical skill source, templates, generator logic, or approved metadata surfaces, not through generated skill copies.

R6. The first implementation slice MUST remove only `.codex/skills/` from tracked generated skill state.

R7. The first implementation slice MUST NOT untrack, delete, or change public adapter skill copies under `dist/adapters/`.

R8. The first implementation slice MUST keep public adapter installation from the repository tree unchanged.

R9. The migration MUST NOT rewrite Git history to remove previously committed generated skill copies.

### Local Codex mirror generation and validation

R10. The repository MUST document a command that regenerates the local Codex mirror from canonical skill source.

R11. After `.codex/skills/` becomes untracked, `.gitignore` or equivalent repository ignore policy MUST exclude `.codex/skills/`.

R12. After `.codex/skills/` becomes untracked, validation MUST NOT require tracked `.codex/skills/<skill>/SKILL.md` files to exist.

R13. After `.codex/skills/` becomes untracked, validation MUST prove that the local Codex mirror can be generated from canonical sources.

R14. After `.codex/skills/` becomes untracked, checks whose only purpose is tracked-file equality between `skills/` and `.codex/skills/` MUST be retired or replaced.

R15. Replacement local mirror validation MUST use temp-output validation or an equivalent non-tracked generated output surface.

R16. Replacement local mirror validation MUST fail when generation from canonical source fails.

R17. Replacement local mirror validation MUST fail when generated local mirror output is structurally invalid for the local Codex runtime contract.

### Public adapter tracked metadata and release artifacts

R18. `dist/adapters/manifest.yaml` MUST remain tracked as adapter support metadata unless a later accepted proposal or approved spec supersedes this contract.

R19. `dist/adapters/manifest.yaml` MUST NOT contain generated skill body text.

R20. `dist/adapters/README.md` MUST be tracked or added before public adapter skill copies are removed from tracked Git state.

R21. `dist/adapters/README.md` MUST explain that canonical skills are authored under `skills/`.

R22. `dist/adapters/README.md` MUST explain that generated adapter archives are release assets after the public adapter migration.

R23. `dist/adapters/README.md` MUST identify `dist/adapters/manifest.yaml` as the tracked support matrix or equivalent support metadata surface.

R24. Adapter artifact metadata MUST be tracked under `docs/reports/adapter-artifacts/releases/<version>.yaml` for every public release that publishes generated adapter release artifacts after this contract is implemented.

R25. Adapter artifact metadata MUST include `schema_version`.

R26. Adapter artifact metadata MUST include the release version.

R27. Adapter artifact metadata MUST include the source commit used to generate the adapter artifacts.

R28. Adapter artifact metadata MUST include the generator command.

R29. Adapter artifact metadata MUST include the canonical skill source path or equivalent source description.

R30. Adapter artifact metadata MUST include the manifest or support metadata path used for the release.

R31. Adapter artifact metadata MUST list each generated adapter archive.

R32. Adapter artifact metadata MUST record a SHA-256 checksum for each generated adapter archive.

R33. Adapter artifact metadata MUST record the validation command and validation result.

R34. Adapter artifact metadata MUST record the validation date or timestamp.

R35. Adapter artifact metadata MUST be parseable as YAML.

R36. Release notes or release reports MUST link to or name the adapter artifact metadata file when generated adapter release artifacts are published.

R37. Generated adapter archives MUST NOT be committed to Git by default.

R38. Generated adapter archives MUST be uploaded as release assets or otherwise distributed through the approved release artifact channel.

R39. Every public release that distributes generated adapter artifacts MUST publish a separate downloadable archive for each supported adapter.

R40. A public release MAY publish a combined all-adapters archive in addition to the required per-adapter archives.

R41. The required per-adapter archive names SHOULD identify the adapter name and release version.

R42. The combined archive name, when present, SHOULD identify that it includes all adapters and the release version.

### Public adapter migration and compatibility

R43. Public adapter skill copies under `dist/adapters/**/skills` MUST remain tracked until at least one stable public release has provided downloadable adapter artifacts and release-artifact installation documentation.

R44. The release that first provides downloadable adapter artifacts while public adapter skill copies remain tracked MUST announce the repository-tree install path transition in release notes.

R45. The release that first removes tracked public adapter skill copies MUST document artifact-install instructions.

R46. The release that first removes tracked public adapter skill copies MUST preserve tracked adapter support metadata.

R47. The release that first removes tracked public adapter skill copies MUST preserve adapter support for Codex, Claude Code, and opencode unless a separate accepted proposal removes or changes adapter support.

R48. Public adapter skill copies MUST NOT be removed in the same stable release that first provides downloadable adapter artifacts unless an explicit approved exception records why the compatibility window is being shortened.

R49. While public adapter skill copies remain tracked, existing drift checks for `dist/adapters/**/skills` MUST remain active unless replaced by an approved equivalent validation path.

R50. After public adapter skill copies become untracked, tracked-file drift checks for those copies MUST be replaced by temp-output adapter generation and validation.

### CI and release validation

R51. Ordinary PR CI SHOULD build generated adapters when changed paths can affect canonical skills, adapter generation, adapter templates, adapter manifest or support metadata, release packaging, release metadata, or related specs.

R52. Ordinary PR CI MAY skip generated adapter builds for unrelated changes that cannot affect adapter output, release packaging, or public skill loading.

R53. Release validation MUST build generated adapters regardless of ordinary PR path-selection results.

R54. Release validation MUST validate generated adapter output against a temporary output directory, release artifact directory, or tracked adapter output while that output remains tracked.

R55. Release validation MUST fail when generated adapter output cannot be produced from canonical sources.

R56. Release validation MUST fail when generated adapter output is structurally invalid for a supported adapter.

R57. Release validation MUST fail when required adapter artifact metadata is missing or invalid for a release that publishes generated adapter artifacts.

R58. Release validation MUST fail when an adapter artifact checksum recorded in metadata does not match the generated or published artifact under validation.

R59. Validation commands that keep a `--check` mode after generated output is untracked MUST define `--check` as generation plus structural validation against non-tracked output for that untracked surface.

R60. `--check` behavior MUST NOT silently require tracked generated files for a generated output tree after that tree is intentionally untracked.

### Token-cost benchmark source behavior

R61. Static authored skill measurement MUST measure canonical `skills/` without counting duplicate generated local mirror or adapter skill copies as additional authored skill source.

R62. Dynamic public-surface token benchmarks MUST NOT use `.codex/skills/` as the public skill source.

R63. While public Codex adapter skill copies remain tracked, dynamic Codex public-surface benchmarks MAY use `dist/adapters/codex/.agents/skills/` as the public skill source.

R64. After public adapter skill copies become untracked, dynamic public-surface benchmarks MUST use generated temporary adapter output or release artifact output as the public skill source.

R65. Token-cost benchmark metadata MUST identify the skill source used for dynamic public-surface benchmarks.

R66. Token-cost benchmark validation MUST fail when benchmark metadata identifies `.codex/skills/` as the public skill source.

### Documentation and contributor guidance

R67. Contributor-facing docs MUST state that `skills/` is the only authored skill source.

R68. Contributor-facing docs MUST state that `.codex/skills/` is generated local runtime output after the first slice.

R69. Contributor-facing docs MUST state that public adapter skill copies are generated public adapter output.

R70. Contributor-facing docs MUST explain which generated output surfaces are tracked during the current migration phase.

R71. Contributor-facing docs MUST explain which command or validation path regenerates the local Codex mirror.

R72. Contributor-facing docs MUST explain when public adapters are installed from repository-tree output versus release artifacts.

R73. Contributor-facing docs MUST NOT imply that generated skill copies are authored source.

## Inputs and outputs

Inputs:

- canonical skill source under `skills/`;
- adapter templates or equivalent canonical adapter inputs;
- adapter manifest or support metadata;
- release version;
- release source commit;
- release artifact generation command;
- validation command outputs;
- release notes and release reports;
- token-cost benchmark configuration and metadata.

Outputs:

- generated local Codex mirror output under `.codex/skills/` when requested locally;
- tracked adapter support metadata under `dist/adapters/manifest.yaml`;
- tracked adapter install guidance under `dist/adapters/README.md`;
- tracked adapter artifact metadata under `docs/reports/adapter-artifacts/releases/<version>.yaml`;
- generated per-adapter release archives;
- optional combined adapter release archive;
- validation results for local mirror generation, adapter generation, adapter artifact metadata, and benchmark source selection.

## State and invariants

- `skills/` remains the only authored skill source.
- Generated output remains reproducible from tracked canonical sources.
- `.codex/skills/` is not required as tracked Git state after the first migration slice.
- Public adapter installation remains reliable during the migration.
- `dist/adapters/manifest.yaml` and `dist/adapters/README.md` are support and guidance surfaces, not generated skill body storage.
- Adapter release artifacts have durable tracked provenance metadata.
- Generated archives are not committed to Git by default.
- The migration changes future tracked state only; historical commits are not rewritten.

## Error and boundary behavior

1. If canonical skill source is missing for a generated skill, generation or validation MUST fail.
2. If `.codex/skills/` is absent from Git after untracking, validation MUST NOT fail solely because the tracked directory is absent.
3. If local mirror generation fails after `.codex/skills/` is untracked, validation MUST fail.
4. If public adapter skill copies are removed before the compatibility window is satisfied, validation or review MUST block release readiness.
5. If release artifact metadata is missing for a release that publishes generated adapter artifacts, release validation MUST fail.
6. If recorded artifact checksums do not match generated or published artifacts under validation, release validation MUST fail.
7. If a generated archive is committed without an approved exception, review or validation MUST treat it as a policy violation.
8. If a dynamic public-surface benchmark uses `.codex/skills/`, benchmark validation MUST fail.
9. If CI path selection skips adapter generation for a change that affects adapter output, release validation MUST still build and validate adapters before release readiness.
10. If old docs still instruct users to copy public adapter skill bodies from `dist/adapters/` after those bodies are untracked, documentation validation or review MUST block release readiness.

## Compatibility and migration

This spec uses staged migration.

M1 clarifies source boundaries in governance, workflow, and contributor-facing docs.

M2 removes tracked `.codex/skills/`, ignores it as local generated output, documents local regeneration, and replaces tracked local mirror drift checks with temp-output generation and validation.

M3 prepares public adapter release artifact packaging, metadata, checksums, release notes, install docs, and validation.

M4 removes tracked public adapter skill copies only after at least one stable public release has provided downloadable adapter artifacts and release-artifact installation docs while repository-tree public adapter skill copies remained available.

M5 updates token-cost benchmark sources and release evidence to use generated public adapter output or release artifact output intentionally.

Rollback before M4 MAY restore tracked `.codex/skills/` by reverting the ignore, validation, documentation, and generation changes for that slice.

Rollback after M4 MUST preserve the ability to generate adapter packages from `skills/` and either re-track generated adapter output temporarily or republish release artifacts from the last known good generated output.

This spec supersedes older requirements only where they require `.codex/skills/` to remain tracked after M2 or require public adapter skill copies to remain tracked after M4. Until a migration slice is completed, older tracked-output validation remains applicable for that surface.

## Observability

- Validation output SHOULD identify whether it validated canonical skills, local mirror temp output, tracked public adapter output, release artifact output, adapter metadata, or benchmark source metadata.
- Release reports or release notes MUST identify adapter artifact metadata when generated adapter release artifacts are published.
- Adapter artifact metadata MUST provide checksum and validation evidence suitable for review.
- CI logs SHOULD show when adapter build validation is skipped because changed paths are unrelated.
- CI logs SHOULD show when adapter build validation runs because changed paths are adapter-affecting.

## Security and privacy

- Generated adapter archives MUST NOT include secrets, credentials, private keys, machine-local paths, or account-specific setup.
- Adapter artifact metadata MUST NOT include secrets, credentials, private keys, or private local filesystem paths.
- Temporary output directories used for validation MUST NOT be treated as durable release evidence unless their outputs are captured through approved metadata, reports, or release assets.
- Release artifact checksums MUST be generated from the artifact content that is distributed to users.
- Public adapter archives MUST preserve the existing adapter permission posture unless a separate approved spec changes adapter permissions.

## Accessibility and UX

No UI behavior is introduced by this spec.

User-facing install guidance MUST remain clear enough for a user to choose the correct adapter archive without reading generated skill bodies in the repository tree.

## Performance expectations

- Generated-output validation SHOULD avoid requiring full repository-wide generated adapter builds for unrelated ordinary PRs.
- Release validation MUST prioritize correctness over speed and MUST build generated adapters even when ordinary PR CI would skip them.
- Temp-output validation SHOULD avoid committing or printing large generated output dumps as routine proof.
- Token-cost measurement SHOULD avoid counting duplicate generated skill bodies as authored source cost.

## Edge cases

1. A canonical skill changes while `.codex/skills/` is untracked: local mirror validation uses temp-output generation instead of tracked drift comparison.
2. A canonical skill changes while public adapter skill copies remain tracked: public adapter drift validation still applies to tracked adapter output.
3. A release publishes adapter artifacts before public adapter cleanup: metadata and checksums are tracked, but public adapter skill copies remain tracked during the compatibility window.
4. A release wants to remove public adapter skill copies before one stable release of artifact availability: the release is blocked unless an explicit approved exception shortens the compatibility window.
5. A user installs from `dist/adapters/` during the compatibility window: repository-tree installation remains supported.
6. A user installs after public adapter cleanup: documentation points to release artifacts and support metadata remains tracked.
7. A benchmark runner is configured with `.codex/skills/`: validation blocks because the local mirror is not the public skill source.
8. A generated archive appears in Git: review or validation flags it unless an approved exception exists.
9. `dist/adapters/manifest.yaml` includes generated skill body text: validation or review flags it because the manifest is metadata only.
10. `dist/adapters/README.md` is missing when public adapter skill copies are removed: validation or review blocks because tracked install guidance is required.
11. Adapter artifact metadata names a commit that differs from the release source under validation: release validation blocks or requires explicit correction.
12. A combined all-adapters archive is absent: release validation still passes if required per-adapter archives and metadata are valid.

## Non-goals

- Do not change skill wording or behavior as part of this contract.
- Do not remove Codex, Claude Code, or opencode adapter support.
- Do not remove adapter generation.
- Do not change workflow stage order.
- Do not require downstream users to generate adapters manually when release artifacts are the approved distribution path.
- Do not rewrite Git history to remove prior generated skill copies.
- Do not require generated adapter archives to be committed to Git.
- Do not define exact internal implementation details for generation scripts beyond observable command behavior, output surfaces, and validation results.

## Acceptance criteria

- `skills/` is documented and validated as the only authored skill source.
- `.codex/skills/` is removed from tracked Git state in the first implementation slice.
- `.codex/skills/` is ignored as generated local runtime output after the first slice.
- A documented command regenerates the local Codex mirror.
- Local mirror validation no longer depends on tracked `.codex/skills/` files after the first slice.
- Public adapter skill copies under `dist/adapters/` remain tracked during the first slice.
- `dist/adapters/manifest.yaml` remains tracked as support metadata and does not contain generated skill bodies.
- `dist/adapters/README.md` exists before public adapter skill copies are untracked.
- Adapter artifact metadata is tracked under `docs/reports/adapter-artifacts/releases/<version>.yaml` for releases that publish generated adapter archives.
- Release artifacts include separate per-adapter archives for every supported adapter.
- Generated adapter archives are not committed to Git by default.
- Public adapter skill copies remain tracked for at least one stable release after downloadable adapter artifacts and install docs are available.
- Release validation builds and validates generated adapters for releases.
- Ordinary PR CI runs adapter generation conditionally for adapter-affecting changes.
- Token-cost dynamic public-surface benchmarks do not use `.codex/skills/`.
- Generated-output validation uses temp or release output for untracked generated trees.

## Open questions

None.

## Next artifacts

- `spec-review`
- architecture or ADR update if review decides the release artifact and generated-output boundary needs a durable architecture record
- `plan`
- `plan-review`
- `test-spec`
- implementation
- `code-review`
- `explain-change`
- `verify`
- `pr`

## Follow-on artifacts

- Spec-review approved the contract with no material findings.
- Canonical architecture package update: `docs/architecture/system/architecture.md`
- Generated output migration ADR: `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md`
- Test spec: `specs/single-authored-skill-source-generated-output.test.md`

## Readiness

Approved and handed off to `architecture`.
