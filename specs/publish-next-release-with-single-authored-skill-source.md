# Publish Next Release With Single Authored Skill Source

## Status

approved

## Related proposal

- [Publish Next Release With Single Authored Skill Source](../docs/proposals/2026-05-12-publish-next-release-with-single-authored-skill-source.md)

## Goal and context

This spec defines the release contract for publishing the next RigorLoop stable release as a single-authored-source transition release.

The release must preserve `skills/` as the only authored skill source, keep `.codex/skills/` ignored and outside required release evidence, retain tracked public adapter packages under `dist/adapters/` as the public install path, and validate the public adapter output users receive.

This spec is intentionally narrower than the full generated-output migration. It does not remove tracked public adapter skill copies, does not require downloadable adapter archives for `v0.1.1`, and does not repeal non-release local Codex setup validation governed by `specs/single-authored-skill-source-generated-output.md`.

## Glossary

- `transition release`: the next stable release that keeps repository-tree adapter installation from `dist/adapters/` while `.codex/skills/` remains ignored local runtime state.
- `canonical skills`: authored skill source under `skills/`.
- `public adapter output`: generated installable adapter packages under `dist/adapters/` during the compatibility window.
- `public Codex adapter skills`: generated Codex adapter skill files under `dist/adapters/codex/.agents/skills/`.
- `local Codex runtime directory`: ignored local runtime install directory under `.codex/skills/`.
- `release evidence`: tracked release notes, reports, metadata, validation output, and public adapter output used to decide public release readiness.
- `maintainer-facing release gate`: the single command a maintainer runs to decide stable release readiness.
- `structured release validator`: the script that validates structured release metadata, reports, release notes, and related artifacts.
- `downloadable adapter archive`: a generated adapter archive attached to a public release asset rather than installed from the repository tree.

## Examples first

### Example E1: transition release validates public adapters

Given `v0.1.1` is prepared for stable release
When the maintainer runs the release gate
Then validation checks canonical skills, tracked public adapter packages under `dist/adapters/`, adapter install guidance, release notes, and token-cost metadata
And validation does not require `.codex/skills/` generation.

### Example E2: local Codex use follows the public adapter path

Given a contributor wants to use RigorLoop skills locally with Codex
When they set up local runtime skills
Then guidance tells them to generate or use the public Codex adapter output
And copy or install the adapter skills into `.codex/skills/`
And `.codex/skills/` remains ignored local runtime state.

### Example E3: no downloadable archives in the transition release

Given `v0.1.1` does not publish adapter archives
When release notes and adapter docs are reviewed
Then they state that no downloadable adapter archives are introduced
And `dist/adapters/` remains the public adapter install path.

### Example E4: optional adapter archives do not replace repository-tree install

Given a separate accepted plan publishes experimental adapter archives for `v0.1.1`
When release validation runs
Then archive metadata and checksums are validated
But `dist/adapters/` remains the required public install path for this transition release.

### Example E5: token-cost benchmark rejects `.codex/skills/`

Given token-cost release metadata identifies `.codex/skills/` as the dynamic public skill source
When token-cost release validation runs
Then validation fails because release benchmarks must use public Codex adapter output during the compatibility window.

## Requirements

### Source and release surfaces

R1. The transition release MUST treat `skills/` as the only authored skill source.

R2. The transition release MUST treat `.codex/skills/` as ignored local runtime state, not release evidence.

R3. The transition release MUST preserve tracked public adapter packages under `dist/adapters/` as the public adapter install path.

R4. The transition release MUST preserve public adapter support for Codex, Claude Code, and opencode unless a separate approved spec changes supported adapters.

R5. The transition release MUST NOT remove tracked public adapter skill copies under `dist/adapters/**/skills`.

R6. The transition release MUST NOT change skill behavior or skill wording as part of release packaging.

### Release validation

R7. `bash scripts/release-verify.sh <version>` MUST be the maintainer-facing final stable release gate for the transition release.

R8. `scripts/validate-release.py` MUST own structured validation for release metadata, token-cost reports, adapter evidence, release notes, and related release artifacts.

R9. The maintainer-facing release gate SHOULD delegate structured checks to `scripts/validate-release.py` so maintainers keep one final release command.

R10. Release validation MUST validate canonical skills under `skills/`.

R11. Release validation MUST validate tracked public adapter output under `dist/adapters/` while public adapter output remains tracked.

R12. Release validation MUST validate adapter manifest and adapter install documentation.

R13. Release validation MUST validate release token-friendliness metadata required for the target release.

R14. Release validation MUST validate tracked release notes for the target release.

R15. Release validation MUST confirm `.codex/skills/` is ignored and not tracked.

R16. Release validation MUST NOT require generating, building, or structurally validating `.codex/skills/` as release evidence.

R17. Optional local Codex smoke MAY install public Codex adapter output into `.codex/skills/`, but that smoke MUST remain separate from required release evidence.

R18. Release validation MUST fail when public adapter output cannot be generated from canonical skills or is structurally invalid.

R19. Release validation MUST fail when tracked public adapter output is stale during the compatibility window.

### Adapter installation documentation

R20. `dist/adapters/README.md` MUST include version-aware `v0.1.1` guidance that repository-tree package roots under `dist/adapters/` are the public install path.

R21. `dist/adapters/README.md` MUST state that no downloadable adapter archives are required for `v0.1.1` unless separately published.

R22. `dist/adapters/README.md` MUST identify `docs/reports/adapter-artifacts/releases/<version>.yaml` as the adapter artifact metadata path when adapter archives exist.

R23. `dist/adapters/README.md` MUST state that `.codex/skills/` is not a public adapter install source.

R24. Contributor-facing local Codex setup guidance MUST tell contributors to install or copy from public Codex adapter output into `.codex/skills/`.

R25. Contributor-facing local Codex setup guidance MUST tell contributors to keep `.codex/skills/` untracked and edit canonical skills under `skills/`.

### Adapter archives and metadata

R26. `v0.1.1` MUST NOT require downloadable adapter archives.

R27. If no adapter archives are published for `v0.1.1`, release notes or adapter docs MUST state that no downloadable adapter archives are introduced and `dist/adapters/` remains the public install path.

R28. If a separate accepted plan publishes adapter archives for `v0.1.1`, those archives MUST be optional convenience assets and MUST NOT replace repository-tree installation from `dist/adapters/`.

R29. If adapter archives are published for `v0.1.1`, adapter artifact metadata MUST be tracked under `docs/reports/adapter-artifacts/releases/v0.1.1.yaml`.

R30. If adapter artifact metadata is tracked for `v0.1.1`, it MUST include schema version, release version, source commit, generator command, canonical skill source, manifest path, archive list, SHA-256 checksums, validation command, and validation result.

R31. Generated adapter archives MUST NOT be committed to Git by default.

### Token-cost evidence

R32. Static token-cost measurement for the transition release MUST measure canonical `skills/`.

R33. Dynamic public-surface token-cost benchmarks for Codex MUST use public Codex adapter output while public adapter output remains tracked.

R34. Dynamic public-surface token-cost benchmarks MUST NOT read or install from `.codex/skills/`.

R35. Token-cost metadata validation MUST fail when release benchmark metadata identifies `.codex/skills/` as the public skill source.

## Inputs and outputs

Inputs:

- release version, expected to be `v0.1.1` unless a newer stable version is already used before planning;
- canonical skill source under `skills/`;
- tracked public adapter output under `dist/adapters/`;
- adapter support metadata under `dist/adapters/manifest.yaml`;
- adapter install guidance under `dist/adapters/README.md`;
- release notes under `docs/releases/<version>/release-notes.md`;
- token-cost release metadata under `docs/reports/token-cost/releases/<version>.yaml`;
- optional adapter artifact metadata under `docs/reports/adapter-artifacts/releases/<version>.yaml` only when adapter archives are published.

Outputs:

- release validation result from `bash scripts/release-verify.sh <version>`;
- structured release validation result from `scripts/validate-release.py`;
- validated public adapter packages under `dist/adapters/`;
- release notes that describe the single-authored-source transition;
- token-cost release evidence that uses canonical skills and public adapter output;
- optional local Codex smoke result, if a maintainer chooses to run it outside required release evidence.

## State and invariants

- `skills/` remains the only authored skill source.
- `.codex/skills/` remains ignored local runtime state and is not tracked release evidence.
- `dist/adapters/` remains tracked generated public adapter output for this transition release.
- Public adapter output remains reproducible from canonical skills.
- The transition release does not change the public adapter install model and the authored skill source model in the same step.
- Release evidence proves the public adapter path works.

## Error and boundary behavior

- If `.codex/skills/` is tracked, release validation MUST fail.
- If release validation requires `.codex/skills/` generation as release evidence, the release gate MUST be treated as stale and not release-ready.
- If tracked public adapter output is missing, stale, or structurally invalid, release validation MUST fail.
- If release notes are missing for the target release, release validation MUST fail.
- If token-cost metadata is missing when required for the target release, release validation MUST fail.
- If token-cost metadata uses `.codex/skills/` as public skill source, release validation MUST fail through token-cost metadata validation.
- If adapter archives are not published for `v0.1.1`, release validation MUST NOT fail solely because adapter artifact metadata is absent.
- If adapter archives are published without required metadata or checksum evidence, release validation MUST fail.
- If a newer stable release version replaces `v0.1.1` before planning, downstream artifacts MUST update release-note, token-cost, adapter metadata, and validation paths consistently.

## Compatibility and migration

This spec is a transition-release slice.

The release preserves repository-tree adapter installation from `dist/adapters/` for users who follow the existing public install model.

The release does not shorten the compatibility window for public adapter skill copies. Public adapter skill copies remain tracked until a later stable release satisfies the release-artifact compatibility requirements in `specs/single-authored-skill-source-generated-output.md`.

Downloadable adapter archives remain a follow-on migration by default. A later release may make archives the primary install path only after release artifacts, checksums, metadata, install docs, release notes, validation, and compatibility-window evidence are complete.

Rollback for this transition release is to defer publication, fix release validation or documentation, and keep `dist/adapters/` as the public install path. Rollback MUST NOT re-track `.codex/skills/` unless a maintainer explicitly postpones the migration in a reviewed artifact.

## Observability

- Release validation output SHOULD identify whether it validated canonical skills, tracked public adapter output, release notes, token-cost metadata, adapter install docs, and `.codex/skills/` tracked-state absence.
- Release validation output SHOULD NOT describe `.codex/skills/` generation as release evidence.
- Release notes MUST describe the single-authored-source transition.
- Release notes or adapter docs MUST state whether adapter archives are absent or separately published for the target release.
- Token-cost metadata MUST identify the dynamic public skill source used for benchmarks.

## Security and privacy

- Release artifacts and metadata MUST NOT include secrets, credentials, private keys, private local paths, or account-specific setup.
- Optional local Codex smoke MUST NOT publish machine-local `.codex/skills/` contents as release evidence.
- Adapter archives, if published, MUST be generated from public repository sources and MUST include checksum evidence.
- Release validation SHOULD avoid printing large generated skill bodies as routine proof.

## Accessibility and UX

No UI behavior is introduced.

User-facing install guidance MUST clearly distinguish:

- authored source: `skills/`;
- public adapter install path for `v0.1.1`: `dist/adapters/`;
- local Codex runtime state: `.codex/skills/`;
- future artifact install path: downloadable adapter archives only after a later migration.

## Performance expectations

- Release validation MAY prioritize correctness over speed.
- Release validation SHOULD avoid unnecessary `.codex/skills/` generation because `.codex/skills/` is not release evidence.
- Static token-cost measurement SHOULD avoid counting duplicate generated skill bodies as authored source cost.

## Edge cases

1. `v0.1.1` publishes no adapter archives: validation passes when `dist/adapters/` is valid and docs or release notes state repository-tree install remains the public path.
2. `v0.1.1` publishes optional adapter archives: validation also requires adapter artifact metadata and checksums, but repository-tree install remains valid.
3. `.codex/skills/` exists locally but is ignored: release validation may pass if it is untracked and not used as release evidence.
4. `.codex/skills/` is tracked: release validation fails.
5. Token-cost metadata points to `.codex/skills/`: token-cost validation fails.
6. Token-cost metadata points to `dist/adapters/codex/.agents/skills/`: token-cost validation may pass when all other metadata is valid.
7. `dist/adapters/README.md` omits `v0.1.1` repository-tree install guidance: release readiness fails.
8. `dist/adapters/README.md` says archives are required for `v0.1.1` without a separate accepted archive plan: release readiness fails.
9. `release-verify.sh` and `validate-release.py` disagree: release readiness fails until the scripts have a clear delegation contract or one validator is corrected.
10. A later plan changes the target from `v0.1.1` to another version: all release evidence paths and docs must change together.

## Non-goals

- Do not remove tracked public adapter skill copies under `dist/adapters/**/skills`.
- Do not remove support for Codex, Claude Code, or opencode.
- Do not require downloadable adapter archives for `v0.1.1`.
- Do not change skill behavior or skill wording.
- Do not introduce a package manager, hosted registry, or installer.
- Do not replace non-release local Codex setup validation governed by the generated-output spec.
- Do not publish, tag, merge, or deploy as part of this spec.
- Do not rewrite Git history.

## Acceptance criteria

- `skills/` is documented and validated as the only authored skill source for the release.
- `.codex/skills/` is ignored, untracked, and absent from required release evidence.
- Release validation validates canonical skills.
- Release validation validates tracked public adapter output under `dist/adapters/`.
- Release validation does not require `.codex/skills/` generation.
- `bash scripts/release-verify.sh <version>` remains the maintainer-facing release gate.
- `scripts/validate-release.py` owns structured release validation delegated from the release gate.
- `dist/adapters/README.md` includes version-aware `v0.1.1` repository-tree install guidance.
- Release notes state that `dist/adapters/` remains the public adapter install path.
- Release notes or adapter docs state that downloadable adapter archives are not required for `v0.1.1` unless separately published.
- Token-cost static measurement uses canonical `skills/`.
- Codex dynamic token-cost benchmarks use public Codex adapter output, not `.codex/skills/`.
- Public adapter support for Codex, Claude Code, and opencode remains valid.
- No skill behavior changes are introduced by this release packaging slice.

## Open questions

None.

## Next artifacts

```text
architecture-review
plan
test-spec
implementation
code-review
explain-change
verify
pr
release notes
```

## Follow-on artifacts

None yet.

Expected follow-on work:

- Public adapter release-artifact migration.
- Adapter artifact metadata report for the first release that publishes downloadable adapter archives.
- Later stable release that retires tracked public adapter skill copies after the compatibility window.

## Readiness

Approved by spec-review and ready for architecture-review after the canonical architecture update.
