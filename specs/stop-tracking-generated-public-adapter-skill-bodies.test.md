# Stop Tracking Generated Public Adapter Skill Bodies Test Spec

## Status

active

## Related spec and plan

- Spec: [Stop Tracking Generated Public Adapter Skill Bodies](stop-tracking-generated-public-adapter-skill-bodies.md), approved.
- Plan: [Stop tracking generated public adapter skill bodies for v0.1.3](../docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md), active and approved by plan-review R1.
- Proposal: [Stop Tracking Generated Public Adapter Skill Bodies for v0.1.3](../docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md), accepted.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260513-v0-1-3-adapter-release-archive-install-surface](../docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml).
- Review records:
  - `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/reviews/spec-review-r2.md`
  - `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/reviews/plan-review-r1.md`

## Testing strategy

This is a release packaging, generated-output, validation, documentation, metadata, and evidence migration. The proof must focus on repository-owned scripts and tracked release artifacts.

- Unit and integration tests in `scripts/test-adapter-distribution.py` prove generated-output validation, tracked-path rejection, archive structure, adapter metadata, checksum validation, release notes, and install guidance behavior.
- Release validation tests in `scripts/validate-release.py`, `scripts/validate-release-ci.py`, and `scripts/release-verify.sh` prove the maintainer-facing release gate no longer depends on tracked generated adapter package trees for `v0.1.3`.
- Token-cost tests in `scripts/test-token-cost-report-validation.py`, `scripts/validate-token-cost-report.py`, `scripts/measure-skill-tokens.py`, and `scripts/run-token-cost-benchmarks.py` prove canonical static measurement and public adapter dynamic benchmark source behavior.
- Selector and lifecycle tests prove affected path routing, test-spec lifecycle, root-guidance audit coverage, and change metadata consistency.
- Manual verification is allowed only for final GitHub release publication and asset attachment. Local release readiness must be proven before publication.

## Requirement coverage map

| Requirement | Coverage |
| --- | --- |
| `R0`-`R2` | `T1`, `T2`, `T15`, manual release-state check |
| `R3`-`R7` | `T1`, `T3`, `T5`, `T10` |
| `R8`-`R15d` | `T3`, `T4`, `T5`, `T6`, `T16` |
| `R16`-`R25` | `T7`, `T15` |
| `R26`-`R32` | `T8`, `T15` |
| `R33`-`R41` | `T4`, `T5`, `T6`, `T9`, `T16` |
| `R41a`-`R41g` | `T1`, `T4`, `T5`, `T6`, `T9`, `T16` |
| `R42`-`R45` | `T9`, `T10`, `T11`, `T16` |
| `R46`-`R51` | `T12`, `T15`, `T16` |
| `R52`-`R57` | `T13`, `T14`, `T16` |
| `R58`-`R61` | `T17` |
| `R62`-`R68` | `T1`, `T4`, `T5`, `T6`, `T9`, `T16` |

## Example coverage map

| Example | Coverage |
| --- | --- |
| `E1` | `T3`, `T5`, `T15` |
| `E2` | `T4`, `T6`, `T16` |
| `E3` | `T7`, `T8`, `T12` |
| `E4` | `T3`, `T4`, `T5`, `T6` |
| `E5` | `T13`, `T14` |
| `E6` | `T2`, `T16`, manual release-state check |

## Edge case coverage

| Edge case | Coverage |
| --- | --- |
| `v0.1.3` already published or reserved | `T2`, manual release-state check |
| Required adapter archive missing | `T6`, `T9`, `T16` |
| Root guidance still presents tracked skill bodies as active | `T8`, `T15` |
| Generated output passes but tracked `dist/adapters/**/skills` remains | `T3`, `T5`, `T16` |
| Historical `v0.1.2` wording is present | `T7`, `T8`, `T12` |
| Dynamic benchmark records `.codex/skills/` | `T14` |
| Full token-cost report cannot be produced | `T13`, manual policy-exception review |
| Opencode archive omits command wrappers | `T4`, `T6`, `T16` |
| Maintainer wants to keep non-skill package fragments tracked | `T3`, `T5`, spec amendment required |
| Public skill behavior changes beyond retired-path wording | `T17`, manual diff review |

## Test cases

### T1. Cross-spec supersession is version-scoped and obligations remain active

- Covers: `R0`-`R7`, `R41a`-`R41g`, `R62`
- Level: contract
- Fixture/setup: `specs/stop-tracking-generated-public-adapter-skill-bodies.md`, prior adapter specs, release validators
- Steps:
  - Assert the spec names `specs/multi-agent-adapters-first-public-release.md` and `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`.
  - Assert supersession is scoped to tracked-package and repository-tree install requirements for `v0.1.3` and later.
  - Assert adapter support, generation, archive, metadata, checksum, token-cost source, smoke, and release verification obligations remain active.
  - Add regression coverage proving `v0.1.2` historical evidence is not treated as invalid by `v0.1.3` validators.
- Expected result: old tracked-package expectations are superseded only for the `v0.1.3+` storage model.
- Failure proves: downstream implementation can accidentally remove adapter support or invalidate historical release evidence.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T2. Compatibility-window release precondition is checked before publication

- Covers: `R0a`, `R0b`, `R1`, `R2`, `E6`
- Level: contract, manual
- Fixture/setup: `docs/releases/v0.1.2/release-notes.md`, `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`, release asset evidence
- Steps:
  - Assert local release evidence records `v0.1.2` as the archive-introduction compatibility-window release.
  - Assert the `v0.1.3` release path does not require rewriting or invalidating `v0.1.2` release evidence.
  - Before publication, manually verify `v0.1.3` is not already published or reserved.
- Expected result: `v0.1.3` proceeds only after the compatibility-window precondition remains true.
- Failure proves: the release may shorten the compatibility window or target an already-used version.
- Automation location: `scripts/validate-release.py`; manual GitHub release-state check

### T3. Tracked adapter support surface is limited to README and manifest

- Covers: `R8`-`R15d`, `E1`, `E4`
- Level: integration
- Fixture/setup: repository Git index after M2
- Steps:
  - Run `git ls-files 'dist/adapters/**'`.
  - Assert only `dist/adapters/README.md` and `dist/adapters/manifest.yaml` are tracked under `dist/adapters/`.
  - Assert `git ls-files 'dist/adapters/**/skills/**'` returns no tracked files.
  - Assert generated entrypoints and opencode command wrappers under `dist/adapters/<adapter>/` are not tracked.
- Expected result: no partial generated adapter package fragments remain tracked.
- Failure proves: repository-tree install fragments can still be mistaken for active packages.
- Automation location: shell assertions, `scripts/test-adapter-distribution.py`

### T4. Generated temporary adapter output contains complete packages

- Covers: `R14`, `R33`-`R41`, `R41b`-`R41e`, `E2`, `E4`
- Level: integration
- Fixture/setup: temporary `<release-output-dir>`, canonical `skills/`, adapter templates
- Steps:
  - Run `python scripts/build-adapters.py --version v0.1.3 --output-dir <release-output-dir>`.
  - Assert complete Codex, Claude Code, and opencode adapter packages are generated into release output.
  - Assert generated packages include required skill bodies, instruction entrypoints, and opencode command wrappers where required by the support matrix.
  - Run `python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3`.
- Expected result: complete generated packages validate outside tracked `dist/adapters/`.
- Failure proves: untracking removed package contents instead of moving them to generated output.
- Automation location: `scripts/build-adapters.py`, `scripts/validate-adapters.py`, `scripts/test-adapter-distribution.py`

### T5. Release validation rejects tracked generated package fragments

- Covers: `R8`-`R15d`, `R35`-`R37`, `R41a`, `R41g`, `R63`-`R67`, `E1`, `E4`
- Level: integration
- Fixture/setup: temporary repository or fixture with tracked `dist/adapters/**/skills` and package fragments
- Steps:
  - Create a negative fixture where generated adapter skill bodies remain tracked for `v0.1.3`.
  - Create a negative fixture where generated adapter entrypoints or opencode command wrappers remain tracked under adapter package roots.
  - Run release validation for `v0.1.3`.
  - Assert validation fails with a clear tracked-package-retirement error.
  - Assert the same logic does not retroactively fail `v0.1.2` historical evidence.
- Expected result: `v0.1.3` cannot pass while tracked generated adapter package fragments remain.
- Failure proves: the migration can silently leave the old install tree active.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T6. Release archives validate without tracked adapter skill bodies

- Covers: `R33`-`R41`, `R41c`-`R41g`, `R66`, `R68`, `E2`, `E4`
- Level: integration
- Fixture/setup: release output from T4 plus negative archive fixtures
- Steps:
  - Validate generated release archives with `python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3`.
  - Remove a required adapter archive and assert validation fails.
  - Remove required skills from one archive and assert validation fails.
  - Remove opencode command wrappers and assert validation fails.
  - Corrupt or malformed archives and assert validation fails.
- Expected result: archive validation is strong without requiring tracked adapter skill bodies.
- Failure proves: archive installability is not protected after untracking.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-adapters.py`

### T7. Adapter README is the install-contract surface

- Covers: `R16`-`R25`, `E3`
- Level: contract
- Fixture/setup: `dist/adapters/README.md`
- Steps:
  - Assert it states `skills/` is canonical authored source.
  - Assert it identifies `dist/adapters/manifest.yaml` as the support matrix.
  - Assert it states generated public adapter skill bodies are not tracked source after `v0.1.3`.
  - Assert it states `v0.1.3` and later public adapter installation uses GitHub release archives.
  - Assert it lists archive names or naming patterns and target install roots for Codex, Claude Code, and opencode.
  - Assert it identifies adapter artifact metadata and checksum location.
  - Assert any `v0.1.2` compatibility-window wording is explicitly historical.
- Expected result: ordinary users can find the active adapter install path without inspecting generated internals.
- Failure proves: install guidance can preserve stale repository-tree behavior.
- Automation location: `scripts/test-adapter-distribution.py`

### T8. Root guidance audit blocks stale active install wording

- Covers: `R26`-`R32`, `E3`
- Level: contract
- Fixture/setup: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`
- Steps:
  - Assert each required root guidance surface is updated or has an explicit tracked/review-visible unaffected rationale.
  - Assert active rules do not direct ordinary users to install public adapters from retired tracked skill-body paths.
  - Assert root guidance points contributors to `dist/adapters/README.md` rather than duplicating archive details.
  - Assert historical compatibility-window wording is removed from active rules or version-qualified.
- Expected result: root guidance and workflow guidance match the `v0.1.3` install model.
- Failure proves: contributors can follow retired install instructions after tracked packages are removed.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`, manual text review

### T9. Adapter artifact metadata validates source commit, checksums, and archive proof

- Covers: `R42`-`R45`, `R41f`, `R68`
- Level: integration
- Fixture/setup: `docs/reports/adapter-artifacts/releases/v0.1.3.yaml`, generated release output
- Steps:
  - Assert metadata records release version, source commit, date, generator command, source skills, manifest, archive names, checksums, install roots, per-adapter results, validation command/result, and timestamp.
  - Run validation with `--release-commit <commit>` and assert `release.source_commit` matches.
  - Assert checksum mismatch fails.
  - Assert missing archive metadata fails.
  - Assert an intentional source-commit mismatch fails unless an approved policy exception is recorded.
- Expected result: release artifact metadata is reproducible and tied to the validation commit.
- Failure proves: release evidence can point at the wrong source or wrong archives.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T10. Canonical skills remain the authored source

- Covers: `R3`, `R4`, `R41b`
- Level: unit, integration
- Fixture/setup: `skills/`, generated adapter output
- Steps:
  - Run `python scripts/validate-skills.py`.
  - Assert adapter generation reads canonical `skills/`, not generated adapter output or `.codex/skills/`.
  - Assert generated public adapter skill bodies are not accepted as authored skill validation roots.
- Expected result: authored skill validation and adapter generation continue to start from `skills/`.
- Failure proves: generated output can become a competing source of truth.
- Automation location: `scripts/validate-skills.py`, `scripts/build-adapters.py`, `scripts/test-skill-validator.py`

### T11. Adapter artifact metadata rejects source-commit mismatch

- Covers: `R45`
- Level: unit
- Fixture/setup: metadata fixture with wrong `release.source_commit`
- Steps:
  - Run `python scripts/validate-release.py --version v0.1.3 --release-output-dir <release-output-dir> --release-commit <expected-commit>` against a fixture with a different source commit.
  - Assert validation fails.
  - Add a separate fixture with an approved policy exception only if the implementation records that exception.
- Expected result: source commit mismatch is directly validated.
- Failure proves: metadata can intentionally or accidentally point to the wrong archive source commit.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T12. v0.1.3 release notes describe retirement and release archives

- Covers: `R46`-`R51`, `E3`
- Level: contract, integration
- Fixture/setup: `docs/releases/v0.1.3/release-notes.md`, `docs/releases/v0.1.3/release.yaml`
- Steps:
  - Assert release notes state generated public adapter skill bodies are no longer tracked source.
  - Assert release notes state release archives are the active public adapter install path.
  - Assert release notes identify adapter metadata/checksum location.
  - Assert release notes name `bash scripts/release-verify.sh v0.1.3` as the maintainer-facing final gate.
  - Assert `validate-release.py` owns structured release metadata validation and is delegated from `release-verify.sh`.
- Expected result: release notes and gate ownership are clear before publication.
- Failure proves: downstream users or maintainers can miss the install-path migration.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`, `scripts/release-verify.sh`

### T13. Token-cost release report exists and uses canonical static source

- Covers: `R52`, `R53`, `R57`
- Level: integration
- Fixture/setup: `docs/reports/token-cost/releases/v0.1.3.md`, `.yaml`, canonical `skills/`
- Steps:
  - Run `python scripts/measure-skill-tokens.py`.
  - Assert static measurement source is canonical `skills/`.
  - Assert `docs/reports/token-cost/releases/v0.1.3.md` and `.yaml` exist.
  - Run `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.3.yaml`.
  - Assert a scoped benchmark-source check does not replace the full report unless an approved exception is recorded.
- Expected result: `v0.1.3` has release token-cost evidence based on canonical static skills.
- Failure proves: release token-cost evidence is missing or measured from generated copies.
- Automation location: `scripts/measure-skill-tokens.py`, `scripts/validate-token-cost-report.py`, `scripts/test-token-cost-report-validation.py`

### T14. Dynamic token-cost benchmark source is public adapter output

- Covers: `R54`-`R56`, `E5`
- Level: integration
- Fixture/setup: generated public adapter output or release archive output, token-cost runner, negative metadata fixture
- Steps:
  - Run `python scripts/run-token-cost-benchmarks.py --release v0.1.3 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir <run-output-dir> --skill-source <public-adapter-skill-source>`.
  - Assert `<public-adapter-skill-source>` points to generated public adapter release output or temporary public adapter output.
  - Assert metadata records that source.
  - Run a negative fixture with `.codex/skills/` as `skill_source` and assert token-cost validation fails.
- Expected result: dynamic benchmarks exercise the public adapter surface and reject local runtime state.
- Failure proves: token-cost evidence can measure `.codex/skills/` instead of public adapters.
- Automation location: `scripts/run-token-cost-benchmarks.py`, `scripts/validate-token-cost-report.py`, `scripts/test-token-cost-report-validation.py`

### T15. Release validation audits docs and tracked-path state

- Covers: `R16`-`R32`, `R46`-`R51`, all acceptance criteria
- Level: integration
- Fixture/setup: full repository tree after implementation
- Steps:
  - Run release validation with `python scripts/validate-release.py --version v0.1.3 --release-output-dir <release-output-dir> --release-commit <commit>`.
  - Assert it fails when `dist/adapters/README.md` or `dist/adapters/manifest.yaml` is missing.
  - Assert it fails when root guidance has stale active repository-tree install wording.
  - Assert it fails when release notes omit the retired skill-body path or archive install path.
- Expected result: release validation catches stale public guidance and missing tracked support surfaces.
- Failure proves: final release can pass with broken user-facing install guidance.
- Automation location: `scripts/validate-release.py`, `scripts/test-adapter-distribution.py`

### T16. Maintainer release gate proves complete v0.1.3 readiness

- Covers: `R37`-`R41g`, `R42`-`R57`, `R68`, `E2`, `E6`
- Level: smoke, integration
- Fixture/setup: full `v0.1.3` release evidence and generated release output
- Steps:
  - Run `bash scripts/release-verify.sh v0.1.3`.
  - Assert it delegates structured release metadata validation to `scripts/validate-release.py`.
  - Assert it validates canonical skills, generated adapter output, release archives, metadata, checksums, release notes, root guidance, token-cost report, and tracked generated-body absence.
  - Assert it exits non-zero if required release artifacts are missing.
- Expected result: the maintainer-facing final release gate passes only when all release evidence is coherent.
- Failure proves: publication readiness can be claimed without the required migration proof.
- Automation location: `scripts/release-verify.sh`, `scripts/validate-release.py`

### T17. Deferred work remains out of scope

- Covers: `R58`-`R61`
- Level: contract, manual
- Fixture/setup: implementation diff
- Steps:
  - Assert `docs/changes/0001-skill-validator/` is not moved in this slice.
  - Assert no broad progressive-loading or high-cost skill optimization is included.
  - Assert no new token-cost threshold gates are added.
  - Assert no Git history rewrite or generated archive commits are introduced.
  - Assert public skill text changes are limited to obsolete generated-output or retired install-path references.
- Expected result: the release stays focused on adapter untracking and release evidence.
- Failure proves: implementation silently broadens beyond approved scope.
- Automation location: manual diff review, `git diff --name-status`, `git ls-files '*.zip' '*.tar.gz'`

### T18. Lifecycle artifacts remain synchronized

- Covers: workflow proof surfaces and plan closeout requirements
- Level: integration
- Fixture/setup: proposal, spec, test spec, architecture, ADR, plan, change metadata, review artifacts
- Steps:
  - Run `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies`.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml`.
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path ...` over touched lifecycle artifacts.
  - Run `git diff --check --`.
- Expected result: lifecycle state and review evidence remain coherent through planning, implementation, and final closeout.
- Failure proves: workflow evidence is stale or internally inconsistent.
- Automation location: lifecycle validators and `git diff --check`

## Fixtures and data

- Existing canonical skills under `skills/`.
- Adapter support matrix: `dist/adapters/manifest.yaml`.
- Adapter install-contract surface: `dist/adapters/README.md`.
- Generated release output directory from `python scripts/build-adapters.py --version v0.1.3 --output-dir <release-output-dir>`.
- Negative fixture directories for tracked package fragments, missing archives, malformed archives, missing opencode commands, bad checksums, and bad source commit metadata.
- Release evidence under `docs/releases/v0.1.3/`.
- Adapter artifact metadata under `docs/reports/adapter-artifacts/releases/v0.1.3.yaml`.
- Token-cost evidence under `docs/reports/token-cost/releases/v0.1.3.*` and `docs/reports/token-cost/runs/v0.1.3/`.

## Mocking/stubbing policy

- Prefer real temporary directories and generated adapter output over mocks.
- Use synthetic negative fixtures for malformed metadata, missing archives, tracked generated package fragments, and `.codex/skills/` token-cost source regressions.
- Do not mock checksum validation when generated archives are available; validate against real generated archive bytes.
- Dynamic token-cost benchmarks may use the existing runner dry-run mode only when the plan or release policy records why live Codex execution is unavailable.

## Migration or compatibility tests

- `T1`, `T2`, and `T5` prove `v0.1.2` compatibility-window evidence remains valid while `v0.1.3` changes the tracked-package model.
- `T3` and `T5` prove tracked generated adapter package fragments are removed only for the new release model.
- `T7`, `T8`, and `T12` prove users are directed from repository-tree package copying to release archives.
- `T16` proves the final release gate applies the new validation model.

## Observability verification

- `T15` and `T16` verify release validation identifies missing tracked support surfaces, stale root guidance, missing archives, metadata/checksum problems, and tracked generated-body regressions.
- `T13` and `T14` verify token-cost reports identify static source and dynamic public adapter skill source.
- Normal validation output should summarize generated-output checks without printing full generated skill bodies.

## Security/privacy verification

- `T9` verifies metadata uses reproducible source commit and checksum evidence rather than private local state.
- `T14` verifies dynamic benchmarks do not use private local `.codex/skills/` as the public adapter source.
- `T16` verifies release archives and metadata validation are part of the release gate.
- Manual review checks that release metadata, token-cost evidence, and generated-output logs do not commit secrets, credentials, private tokens, or machine-local install paths.

## Performance checks

- No hard performance gate is introduced.
- Adapter generation, adapter validation, release validation, and token-cost validation should keep normal output concise.
- Token-cost reports may record warnings, but this slice does not add new token-cost threshold gates.

## Manual QA checklist

- Confirm `v0.1.3` is not already published or reserved before publication.
- Confirm GitHub release assets are attached after publication.
- Confirm release archive names match release notes and adapter artifact metadata.
- Confirm `dist/adapters/README.md` is understandable as the install-contract surface.
- Confirm root guidance does not preserve stale active install rules.
- Confirm deferred work was not bundled into this release slice.

## What not to test

- Do not test moving `docs/changes/0001-skill-validator/`; it is explicitly out of scope.
- Do not test broad progressive-loading or high-cost skill optimization; that requires a separate slice.
- Do not add hard token-cost threshold gates; this release only records required token-cost evidence.
- Do not test Git history rewriting; history rewrite is prohibited.
- Do not require ordinary contributors to have every supported adapter tool installed locally for non-smoke validation.

## Uncovered gaps

None. If implementation discovers that required release archives, token-cost reports, or source-commit validation cannot be produced with existing scripts, return to plan or spec before weakening coverage.

## Next artifacts

```text
implement
code-review
explain-change
verify
pr
release
```

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for implementation. The active plan `Current Handoff Summary` owns the next workflow action.
