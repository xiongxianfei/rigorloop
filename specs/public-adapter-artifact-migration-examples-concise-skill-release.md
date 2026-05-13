# Public Adapter Artifact Migration, Examples Relocation, and Concise Skill Release

## Status

approved

## Related proposal

- [Public Adapter Artifact Migration, Examples Relocation, and Concise Skill Release](../docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md)

## Goal and context

This spec defines the externally observable release, packaging, compatibility, documentation, validation, and evidence contract for introducing downloadable public adapter archives while preserving the repository-tree adapter install path for one stable compatibility release.

The current latest public release as of 2026-05-13 is `v0.1.1`. That release keeps `dist/adapters/` as the public adapter install path and introduces no downloadable adapter archives. This spec therefore makes `v0.1.2` the archive-introduction release by default and keeps tracked generated public adapter skill bodies available during that release. A later stable release, expected to be `v0.1.3` unless versioning changes before planning, may remove tracked generated public adapter skill bodies only after the compatibility window has been satisfied.

This spec also defines the conditional handling for moving the retained skill-validator proof pack into `docs/examples/`, the bounded release-slice skill simplification contract, and the token-cost evidence required before publishing.

## Glossary

- `canonical skills`: authored skill source under `skills/`.
- `public adapter package`: generated installable adapter content for Codex, Claude Code, or opencode.
- `generated public adapter skill body`: generated skill text under adapter skill roots such as `dist/adapters/codex/.agents/skills/`.
- `repository-tree install path`: installing an adapter by copying a tracked `dist/adapters/<adapter>/` package from the repository tree.
- `release archive install path`: installing an adapter from a downloadable release archive asset.
- `archive-introduction release`: the first stable release that publishes downloadable adapter archives while preserving tracked adapter skill bodies.
- `untracking release`: a later stable release that removes tracked generated public adapter skill bodies after the compatibility window.
- `adapter artifact metadata`: tracked YAML release evidence under `docs/reports/adapter-artifacts/releases/<version>.yaml`.
- `adapter support matrix`: tracked adapter support metadata under `dist/adapters/manifest.yaml`.
- `install-contract README`: `dist/adapters/README.md`, the repository-tree surface that explains active adapter installation paths.
- `skill-validator proof pack`: the retained `docs/changes/0001-skill-validator/` example, fixture, and historical proof pack.
- `artifact-location map`: the project-local artifact placement table in `docs/workflows.md`.
- `release-critical scope`: work that must complete before the target release can publish.
- `deferable scope`: related work that may be included only when it does not block release readiness.

## Examples first

### Example E1: `v0.1.2` introduces adapter archives without removing the old install path

Given maintainers prepare `v0.1.2`
When release validation runs
Then per-adapter downloadable archives exist for Codex, Claude Code, and opencode
And `dist/adapters/**/skills` remains tracked for the stable compatibility release
And release notes explain both the repository-tree install path and the new archive install path.

### Example E2: `v0.1.3` removes tracked generated adapter skill bodies after the compatibility window

Given `v0.1.2` has shipped downloadable archives and install docs
When a later stable release removes tracked generated public adapter skill bodies
Then `dist/adapters/manifest.yaml` and `dist/adapters/README.md` remain tracked
And release validation confirms generated skill bodies are distributed through release archives instead of tracked source.

### Example E3: adapter artifact metadata validates archive evidence

Given `rigorloop-adapter-codex-v0.1.2.zip` is generated for release
When adapter artifact metadata is validated
Then the metadata records the release version, source commit, generator command, archive name, install root, SHA-256 checksum, and adapter validation result.

### Example E4: combined archive is optional

Given per-adapter archives exist for Codex, Claude Code, and opencode
When the release omits `rigorloop-adapters-v0.1.2.tar.gz`
Then release validation still passes if metadata records `combined_artifact.required: false`
And all required per-adapter archive evidence is valid.

### Example E5: unsafe skill-validator move is deferred

Given validators or selectors still depend on `docs/changes/0001-skill-validator/`
When the release slice cannot safely update those references
Then the proof pack remains at the old path with explicit retained-fixture rationale
And the release may proceed with a tracked follow-up.

### Example E6: safe skill-validator move updates references

Given all references to `docs/changes/0001-skill-validator/` can be updated in the same slice
When the proof pack moves to `docs/examples/changes/skill-validator/`
Then selectors and lifecycle validation classify the new path as example content
And active change-root validation no longer treats it as active lifecycle state.

### Example E7: skill simplification stays bounded

Given a release change updates public skills
When duplicated path guidance is removed
Then each affected skill keeps concise artifact-location lookup wording and its portable default path
And safety-critical review, verification, and material-finding guidance remains intact.

### Example E8: release token-cost evidence uses public adapter output

Given `v0.1.2` token-cost benchmarks run
When dynamic Codex benchmark metadata is validated
Then the benchmark source is public adapter release output or generated temporary public adapter output
And `.codex/skills/` is rejected as the public skill source.

## Requirements

### Release phase contract

R1. `v0.1.2` MUST be treated as the archive-introduction release unless a newer stable version is published or reserved before planning.

R2. The archive-introduction release MUST publish separate downloadable adapter archives for Codex, Claude Code, and opencode.

R3. The archive-introduction release MUST keep generated public adapter skill bodies under `dist/adapters/**/skills` tracked.

R4. The archive-introduction release MUST keep repository-tree installation from `dist/adapters/<adapter>/` available as a compatibility path.

R5. The archive-introduction release MUST document the release archive install path as the forward migration path.

R6. The archive-introduction release MUST NOT remove tracked generated public adapter skill bodies unless an accepted proposal or approved spec explicitly amends the compatibility window and records why the shortened window is acceptable.

R7. The first untracking release MUST occur after at least one stable release has shipped downloadable adapter archives and release-archive install documentation.

R8. The first untracking release MUST remove tracked generated public adapter skill bodies under `dist/adapters/**/skills`.

R9. The first untracking release MUST keep `dist/adapters/manifest.yaml` tracked as the adapter support matrix.

R10. The first untracking release MUST keep `dist/adapters/README.md` tracked as install guidance.

R11. The first untracking release MUST preserve adapter support for Codex, Claude Code, and opencode unless a separate accepted proposal changes supported adapters.

R12. Generated adapter archives MUST NOT be committed to Git by default.

R13. Generated adapter archives MUST be attached to the public release or otherwise distributed through the approved release artifact channel.

### Adapter archive names and install roots

R14. The archive-introduction release MUST publish a Codex archive named `rigorloop-adapter-codex-<version>.zip`.

R15. The archive-introduction release MUST publish a Claude Code archive named `rigorloop-adapter-claude-<version>.zip`.

R16. The archive-introduction release MUST publish an opencode archive named `rigorloop-adapter-opencode-<version>.zip`.

R17. The Codex archive MUST install skills under `.agents/skills/` relative to the target project root.

R18. The Claude Code archive MUST install skills under `.claude/skills/` relative to the target project root.

R19. The opencode archive MUST install skills under `.opencode/skills/` relative to the target project root.

R20. A combined all-adapters archive MAY be published in addition to the required per-adapter archives.

R21. If the combined archive is not required, adapter artifact metadata MUST record `combined_artifact.required: false`.

R22. If a combined archive is published, metadata MUST record its archive name, SHA-256 checksum, and included adapter list.

### Adapter artifact metadata

R23. Every release that publishes downloadable adapter archives under this contract MUST track adapter artifact metadata at `docs/reports/adapter-artifacts/releases/<version>.yaml`.

R24. Adapter artifact metadata MUST be parseable YAML.

R25. Adapter artifact metadata MUST use `schema_version: 1` until a later approved spec changes the schema.

R26. Adapter artifact metadata MUST include `release.version`.

R27. Adapter artifact metadata MUST include `release.source_commit`.

R28. Adapter artifact metadata MUST include `release.date`.

R29. Adapter artifact metadata MUST include `generator.command`.

R30. Adapter artifact metadata MUST include `generator.source_skills` with the canonical source path or equivalent source description.

R31. Adapter artifact metadata MUST include `generator.manifest` pointing to `dist/adapters/manifest.yaml` or the active support matrix path.

R32. Adapter artifact metadata MUST include an `artifacts` list with one entry per required adapter archive.

R33. Each artifact entry MUST include `adapter`, `archive`, `sha256`, `install_root`, and `result`.

R34. Each required artifact entry `result` MUST be `pass` for release-ready metadata.

R35. The required adapter names in metadata MUST include `codex`, `claude`, and `opencode` unless a separate accepted proposal changes supported adapters.

R36. Adapter artifact metadata MUST include a `combined_artifact` section.

R37. Adapter artifact metadata MUST include `validation.command`.

R38. Adapter artifact metadata MUST include `validation.result`.

R39. Adapter artifact metadata MUST include `validation.validated_at`.

R40. `validation.result` MUST be `pass` for release-ready metadata.

R41. Release validation MUST fail when required adapter artifact metadata is missing, malformed, internally inconsistent, or records a non-passing required artifact result.

R42. Release validation MUST fail when a recorded SHA-256 checksum does not match the generated or published artifact under validation.

### Adapter install guidance

R43. `dist/adapters/README.md` MUST state that `skills/` is the canonical authored source.

R44. `dist/adapters/README.md` MUST identify `dist/adapters/manifest.yaml` as the adapter support matrix.

R45. `dist/adapters/README.md` MUST state that the archive-introduction release provides release archives while keeping tracked adapter skill bodies for the compatibility window.

R46. `dist/adapters/README.md` MUST state that generated adapter skill bodies are not tracked source after the later untracking release.

R47. `dist/adapters/README.md` MUST describe the active install path for each release phase.

R48. `dist/adapters/README.md` MUST list the per-adapter archive naming pattern.

R49. `dist/adapters/README.md` MUST list target install roots for Codex, Claude Code, and opencode.

R50. `dist/adapters/README.md` MUST identify where checksums and adapter artifact metadata are recorded.

R51. `dist/adapters/README.md` MUST avoid stale defensive wording that treats repository-local `.codex/skills/` as a public install source.

### Release validation

R52. `bash scripts/release-verify.sh <version>` MUST be the maintainer-facing final release gate.

R53. `scripts/validate-release.py` MUST own structured release metadata validation and be callable from the maintainer-facing release gate.

R54. The archive-introduction release gate MUST validate canonical skills under `skills/`.

R55. The archive-introduction release gate MUST validate tracked public adapter output under `dist/adapters/` while the compatibility window is active.

R56. The archive-introduction release gate MUST validate generated adapter archives and adapter artifact metadata.

R57. The archive-introduction release gate MUST validate release notes for the target release.

R58. The archive-introduction release gate MUST validate token-cost report metadata for the target release.

R59. The archive-introduction release gate MUST fail when required per-adapter archives are missing.

R60. The archive-introduction release gate MUST fail when release notes do not explain the new archive install path and the retained compatibility path.

R61. The first untracking release gate MUST fail when tracked generated public adapter skill bodies remain under `dist/adapters/**/skills`.

R62. The first untracking release gate MUST fail when `dist/adapters/manifest.yaml` or `dist/adapters/README.md` is missing.

R63. Release validation output SHOULD summarize canonical skill validation, tracked adapter validation when applicable, archive validation, artifact metadata validation, token-cost validation, release notes validation, and security-sensitive scan results.

### Skill-validator proof pack and examples

R64. The skill-validator proof pack MAY move from `docs/changes/0001-skill-validator/` to `docs/examples/changes/skill-validator/` only when references, selectors, validators, docs, and release guidance can be updated safely in the same implementation slice.

R65. If the skill-validator proof pack moves, references to the old path in validation selection, lifecycle validation, tests, docs, and release guidance MUST be updated in the same slice.

R66. If the skill-validator proof pack moves, `docs/examples/README.md` MUST state or continue to state that examples are non-normative and not active lifecycle state.

R67. If the skill-validator proof pack moves, selector routing and lifecycle validation MUST classify `docs/examples/changes/skill-validator/` as example or fixture content rather than active lifecycle state.

R68. If the skill-validator proof pack cannot move safely in the release slice, the implementation MUST retain the old path with explicit retained-fixture rationale in a tracked or review-visible surface.

R69. Retaining the old skill-validator proof pack path with rationale MUST NOT block the archive-introduction release.

### Artifact-location guide and skill simplification

R70. `docs/workflows.md` MUST remain the project-local artifact-location guide.

R71. When adapter artifact metadata becomes a release evidence surface, `docs/workflows.md` SHOULD identify `docs/reports/adapter-artifacts/releases/` as the adapter artifact metadata location.

R72. Public stage skill simplification in this release migration MUST be limited to concise artifact-location lookup wording, each skill's portable default path, and removal of obsolete generated-output references.

R73. Public stage skill simplification in this release migration MUST NOT remove safety-critical review, verification, material-finding, security, or release guidance.

R74. Public stage skills SHOULD use the project artifact-location map before broad-searching governing documents solely for artifact paths.

R75. Progressive-loading optimization beyond artifact-location lookup wording MAY run as a separate implementation slice only when the plan explicitly sequences it after release packaging readiness.

### Token-cost evidence

R76. The archive-introduction release MUST include Token-Friendliness Markdown and YAML reports for the target version.

R77. Static token-cost measurement MUST measure canonical `skills/`.

R78. Dynamic Codex token-cost benchmarks MUST use public adapter release output or generated temporary public adapter output.

R79. Dynamic Codex token-cost benchmarks MUST NOT use `.codex/skills/` as the public skill source.

R80. Token-cost report metadata validation MUST fail when `.codex/skills/` is recorded as the public skill source for dynamic public-surface benchmarks.

R81. Token-cost reports SHOULD identify whole-skill reads, largest command-output events, adapter artifact packaging impact, and result quality when the available benchmark tooling supports those fields.

### Release notes

R82. The archive-introduction release notes MUST state that per-adapter release archives are available.

R83. The archive-introduction release notes MUST state that tracked `dist/adapters/**/skills` remain available for the compatibility window.

R84. The archive-introduction release notes MUST identify where checksums and adapter artifact metadata are recorded.

R85. The archive-introduction release notes MUST name the maintainer-facing release gate command for the target release.

R86. The first untracking release notes MUST state that generated public adapter skill bodies are no longer tracked source.

R87. The first untracking release notes MUST describe release-archive installation as the active public adapter install path.

## Inputs and outputs

Inputs:

- release version;
- canonical skills under `skills/`;
- adapter support matrix under `dist/adapters/manifest.yaml`;
- adapter install guidance under `dist/adapters/README.md`;
- generated public adapter packages;
- generated adapter archives;
- adapter artifact metadata under `docs/reports/adapter-artifacts/releases/<version>.yaml`;
- release notes under `docs/releases/<version>/release-notes.md`;
- token-cost reports under `docs/reports/token-cost/releases/<version>.md` and `.yaml`;
- optional moved or retained skill-validator proof pack;
- project artifact-location guide under `docs/workflows.md`.

Outputs:

- release-ready per-adapter downloadable archives;
- tracked adapter artifact metadata with checksums;
- release notes explaining compatibility and installation;
- validation result from `bash scripts/release-verify.sh <version>`;
- structured release validation result from `scripts/validate-release.py`;
- token-cost release evidence;
- updated install guidance;
- moved example proof pack or retained-fixture rationale.

## State and invariants

- `skills/` remains the only authored skill source.
- Generated public adapter skill bodies are never authored source.
- The archive-introduction release keeps both install paths available.
- The untracking release occurs only after the archive install path has shipped in a stable release, unless a reviewed policy exception exists.
- `dist/adapters/manifest.yaml` and `dist/adapters/README.md` remain tracked support surfaces.
- Required release artifacts are reproducible from tracked sources at the recorded source commit.
- Adapter artifact metadata checksums match the archives they describe.
- Examples under `docs/examples/**` are non-normative and not active lifecycle state.

## Error and boundary behavior

- If a required per-adapter archive is missing, release validation MUST fail.
- If adapter artifact metadata omits a required adapter, release validation MUST fail.
- If adapter artifact metadata contains an invalid checksum, release validation MUST fail.
- If generated archives include adapter output for an unsupported adapter, release validation SHOULD warn unless a support matrix conflict makes the release unsafe.
- If generated archives omit adapter output for a supported adapter, release validation MUST fail.
- If archive generation fails, the release MUST keep the prior repository-tree install model and defer archive publication.
- If `dist/adapters/**/skills` is removed during the archive-introduction release without an approved compatibility exception, release validation MUST fail.
- If the skill-validator proof pack move breaks validators or selectors, the move MUST be reverted or deferred with retained-fixture rationale.
- If public skill simplification removes safety-critical behavior, the release slice MUST restore the behavior or stop before release readiness.
- If token-cost dynamic benchmark tooling is unavailable for a final public release, the existing token-cost waiver contract governs whether release may proceed.

## Compatibility and migration

The migration uses a two-release compatibility path by default:

```text
v0.1.2:
  publish downloadable adapter archives
  keep dist/adapters/**/skills tracked
  update install docs and release notes
  record artifact metadata and checksums
  validate tracked adapters and release archives

v0.1.3 or later:
  stop tracking dist/adapters/**/skills
  keep dist/adapters/manifest.yaml and dist/adapters/README.md
  require release-archive install path
```

Users of the existing repository-tree install path can continue using `dist/adapters/<adapter>/` during the archive-introduction release. Users can adopt release archives during that same release. The later untracking release removes the repository-tree generated skill body install path after the archive path has been available in a stable release.

Rollback for the archive-introduction release is to keep `dist/adapters/**/skills` tracked, defer archives, and keep the `v0.1.1` install model. Rollback for the untracking release is to restore tracked generated adapter skill bodies only if the archive install path or release metadata is not release-ready before publication.

## Observability

- Release validation output SHOULD identify which adapter archives were validated.
- Release validation output SHOULD identify the adapter artifact metadata path.
- Release validation output SHOULD identify whether tracked adapter skill bodies are expected for the target phase.
- Release notes MUST make the install path for the target release clear to downstream users.
- Token-cost reports MUST identify the public skill source used for dynamic benchmarks.
- Retained fixture rationale, when used, MUST be discoverable from tracked or review-visible evidence.

## Security and privacy

- Adapter archives and metadata MUST NOT include secrets, credentials, private keys, private tokens, machine-local paths, or account-specific install details.
- SHA-256 checksum recording MUST be used to detect archive mismatch or unintended replacement.
- Release validation SHOULD avoid printing full generated skill bodies or archive contents as routine output.
- Archive generation SHOULD use repository-owned scripts and public tracked source.
- Release metadata MUST NOT rely on private local files that ordinary maintainers cannot inspect.

## Accessibility and UX

No end-user UI is introduced. Documentation UX requirements are:

- install guidance MUST distinguish current compatibility release behavior from later untracking release behavior;
- adapter archive names and install roots MUST be easy to find in `dist/adapters/README.md`;
- release notes MUST avoid implying that `.codex/skills/` is a public install source.

## Performance expectations

- Release validation SHOULD keep normal output concise and summarize generated-output checks instead of printing full generated skill bodies.
- Token-cost measurement SHOULD report static and dynamic evidence without requiring reviewers to inspect raw benchmark logs by default.
- Archive generation SHOULD be deterministic for the same source commit, manifest, templates, and generator command.

## Edge cases

1. A newer stable release exists before planning starts: downstream artifacts must use the next appropriate version and update paths, archive names, reports, and release notes consistently.
2. A maintainer wants same-release archive introduction and untracking: an accepted policy exception must record why the compatibility window is shortened.
3. One adapter archive validates and another fails: the release is not ready.
4. The combined archive is omitted: the release can proceed when per-adapter archives pass and metadata marks the combined archive as not required.
5. The skill-validator proof pack cannot move safely: retain it with rationale and do not block archive publication.
6. The proof pack moves but one selector still treats it as active lifecycle state: validation must fail or the release must defer the move.
7. Token-cost static measurement passes but dynamic metadata uses `.codex/skills/`: token-cost validation must fail.
8. Release notes mention archives but omit checksums or metadata location: release validation must fail.
9. Archive metadata records a source commit different from the release commit under validation: release validation must fail unless a reviewed release policy permits that mismatch.
10. Public skill simplification removes material-finding guidance: the change must be restored or split out for review before release readiness.

## Non-goals

- Do not change RigorLoop workflow stage order.
- Do not remove Codex, Claude Code, or opencode support.
- Do not rewrite Git history to remove previously committed generated skill copies.
- Do not make `.codex/skills/` a public adapter install source.
- Do not require a combined all-adapters archive.
- Do not make skill-validator proof pack movement a hard blocker for archive publication.
- Do not perform broad progressive-loading optimization as part of the release-critical archive slice.
- Do not remove safety-critical skill behavior to reduce token cost.
- Do not define implementation internals beyond public paths, release artifacts, validation behavior, and metadata contracts.

## Acceptance criteria

- `v0.1.2` release artifacts include required per-adapter archives for Codex, Claude Code, and opencode.
- `v0.1.2` keeps tracked generated public adapter skill bodies under `dist/adapters/**/skills`.
- Adapter artifact metadata exists at `docs/reports/adapter-artifacts/releases/v0.1.2.yaml` and validates against this spec.
- `dist/adapters/README.md` explains canonical source, support matrix, archive names, install roots, compatibility-window behavior, and metadata/checksum location.
- Release notes explain the archive-introduction release and retained compatibility path.
- Token-cost Markdown and YAML reports exist for `v0.1.2` and use canonical `skills/` plus public adapter output rather than `.codex/skills/`.
- `bash scripts/release-verify.sh v0.1.2` passes before publication.
- The skill-validator proof pack is either moved with references updated or retained with explicit rationale and follow-up.
- Any public skill simplification is limited to artifact-location lookup wording, portable defaults, and obsolete generated-output references.
- A later untracking release validates that generated public adapter skill bodies are no longer tracked while manifest and README remain tracked.

## Open questions

- Does archive generation need a dedicated architecture record, or can architecture review confirm that the spec and plan are sufficient?
- Should the first untracking release be exactly `v0.1.3`, or should the plan use "next stable release after archive introduction" until release timing is known?
- Which optional items, if any, should be included in `v0.1.2` after archive publication readiness is proven?

These questions do not block spec review; they should be settled during architecture and planning.

## Next artifacts

```text
architecture if packaging design needs it
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

- Spec review: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md`
- Architecture update: `docs/architecture/system/architecture.md`

## Readiness

Approved after clean spec-review. Canonical architecture has been updated for the adapter archive introduction and later untracking flow.
