# Public Adapter Artifact Migration, Examples Relocation, and Concise Skill Release Test Spec

## Status

active

## Related spec and plan

- Spec: [Public Adapter Artifact Migration, Examples Relocation, and Concise Skill Release](public-adapter-artifact-migration-examples-concise-skill-release.md), approved.
- Plan: [Public Adapter Artifact Migration, Examples Relocation, and Concise Skill Release](../docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md), active and approved by plan-review R2.
- Proposal: [Public Adapter Artifact Migration, Examples Relocation, and Concise Skill Release](../docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md), accepted.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260512-generated-skill-output-release-artifacts](../docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml).
- Review records:
  - `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md`
  - `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r2.md`

## Testing strategy

This is a release packaging, validation, compatibility, documentation, and evidence change. Use repository-owned tests and release scripts rather than manual archive inspection as the primary proof.

- Unit and integration tests in `scripts/test-adapter-distribution.py` prove archive generation, archive validation, metadata schema validation, release validation, release notes, adapter README expectations, and compatibility-window behavior.
- Token-cost tests in `scripts/test-token-cost-measurement.py`, `scripts/test-token-cost-report-validation.py`, and `scripts/validate-token-cost-report.py` prove canonical static measurement and public adapter dynamic benchmark source behavior.
- Selector, lifecycle, review-artifact, and skill-validator tests prove optional proof-pack movement or retained-fixture rationale and bounded skill wording behavior.
- Release-gate smoke through `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.2` and final `bash scripts/release-verify.sh v0.1.2` proves maintainer-facing release readiness.
- Manual verification is allowed only for GitHub release attachment/publication, text quality, and downstream release-channel checks that cannot be proven before publication.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| `R1`-`R6` | `T1`, `T2`, `T4`, `T5`, `T7`, `T14` |
| `R7`-`R11` | `T15`, `T16`, manual follow-up release verification |
| `R12`-`R13` | `T1`, `T3`, `T14`, manual release-asset attachment |
| `R14`-`R19` | `T1`, `T2`, `T3`, `T14` |
| `R20`-`R22` | `T1`, `T4`, `T14` |
| `R23`-`R40` | `T4`, `T5`, `T14` |
| `R41`-`R42` | `T5`, `T14` |
| `R43`-`R51` | `T6`, `T7`, `T14` |
| `R52`-`R60` | `T5`, `T7`, `T14` |
| `R61`-`R62` | `T15`, `T16` |
| `R63` | `T14`, manual release output review |
| `R64`-`R69` | `T8`, `T9`, `T14` |
| `R70`-`R75` | `T10`, `T11`, `T14` |
| `R76`-`R81` | `T12`, `T13`, `T14` |
| `R82`-`R85` | `T7`, `T14` |
| `R86`-`R87` | `T15`, `T16` |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` | `T1`, `T2`, `T7`, `T14` |
| `E2` | `T15`, `T16` |
| `E3` | `T4`, `T5` |
| `E4` | `T4`, `T5` |
| `E5` | `T8`, `T14` |
| `E6` | `T9`, `T14` |
| `E7` | `T10`, `T11` |
| `E8` | `T12`, `T13`, `T14` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| Newer stable release exists before planning starts | `T17`, manual release version review |
| Same-release archive introduction and untracking requested | `T2`, `T15`, manual policy-exception review |
| One adapter archive validates and another fails | `T3`, `T5` |
| Combined archive omitted | `T4`, `T5` |
| Skill-validator proof pack cannot move safely | `T8`, `T14` |
| Proof pack moves but selector treats it as active lifecycle state | `T9` |
| Static token measurement passes but dynamic metadata uses `.codex/skills/` | `T13`, `T14` |
| Release notes mention archives but omit checksum or metadata location | `T7`, `T14` |
| Metadata source commit differs from release commit | `T5` |
| Public skill simplification removes material-finding guidance | `T11` |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| `M1. Generate adapter archives without removing tracked adapter skills` | `T1`, `T2`, `T3`, `T14` |
| `M2. Validate adapter artifact metadata and checksums` | `T4`, `T5`, `T14` |
| `M3. Update install contract, release notes, and artifact-location guidance` | `T6`, `T7`, `T10`, `T14` |
| `M4. Settle skill-validator proof pack and bounded skill wording` | `T8`, `T9`, `T10`, `T11`, `T14` |
| `M5. Produce token-cost and final release-readiness evidence` | `T12`, `T13`, `T14`, `T17` |
| `M6. Later untracking release gate` | `T15`, `T16` |

## Test cases

### T1. Per-adapter archives are generated with required names

- Covers: `R1`, `R2`, `R12`-`R16`, `R20`, `E1`
- Level: integration
- Fixture/setup: temporary `<release-output-dir>`, canonical `skills/`, `dist/adapters/manifest.yaml`
- Steps:
  - Run `python scripts/build-adapters.py --version v0.1.2 --output-dir <release-output-dir>`.
  - Assert the output directory contains `rigorloop-adapter-codex-v0.1.2.zip`, `rigorloop-adapter-claude-v0.1.2.zip`, and `rigorloop-adapter-opencode-v0.1.2.zip`.
  - Assert no generated archive files are created under tracked repository paths by default.
  - If a combined archive is generated, assert its name is `rigorloop-adapters-v0.1.2.tar.gz`.
- Expected result: required per-adapter archives exist in release output and are not committed.
- Failure proves: the archive-introduction release cannot publish required downloadable adapter artifacts.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/build-adapters.py`

### T2. Archive contents use correct install roots and preserve tracked adapter skills

- Covers: `R3`-`R6`, `R17`-`R19`, `E1`
- Level: integration
- Fixture/setup: archives from T1, tracked `dist/adapters/**/skills`
- Steps:
  - Inspect or extract each generated archive into a temporary project root.
  - Assert Codex archive content installs under `.agents/skills/`.
  - Assert Claude Code archive content installs under `.claude/skills/`.
  - Assert opencode archive content installs under `.opencode/skills/`.
  - Run `git ls-files 'dist/adapters/**/skills/**'` and assert tracked generated adapter skill bodies remain present for `v0.1.2`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check` during M1 to prove archive generation did not mutate the tracked compatibility adapter packages.
- Expected result: archives are installable and the repository-tree compatibility path remains tracked.
- Failure proves: archive generation broke install roots or skipped the required compatibility window.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/build-adapters.py`

### T3. Adapter archive validation rejects missing or invalid required archives

- Covers: `R14`-`R19`, `R56`, `R59`
- Level: integration
- Fixture/setup: valid release-output directory from T1 plus negative fixtures with one missing or malformed archive
- Steps:
  - Run `python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.2` on valid output.
  - Remove one required archive and assert validation fails.
  - Corrupt one archive or remove its expected install root and assert validation fails.
- Expected result: all required per-adapter archives must exist and match expected structure.
- Failure proves: release validation can pass with incomplete or unusable adapter artifacts.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-adapters.py`

### T4. Adapter artifact metadata schema validates per-adapter and optional combined artifacts

- Covers: `R20`-`R40`, `E3`, `E4`
- Level: unit, integration
- Fixture/setup: `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`, generated release-output directory
- Steps:
  - Create a valid metadata fixture with `schema_version: 1`.
  - Assert required `release`, `generator`, `artifacts`, `combined_artifact`, and `validation` fields are accepted.
  - Assert the required adapters are `codex`, `claude`, and `opencode`.
  - Assert `combined_artifact.required: false` passes when no combined archive exists.
  - If a combined archive exists, assert its name, checksum, and included adapters are validated.
- Expected result: metadata is parseable, complete, and precise for required and optional artifacts.
- Failure proves: adapter evidence can drift from the release contract.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T5. Release validation fails on malformed metadata, non-pass results, checksum mismatch, or missing archives

- Covers: `R34`, `R40`-`R42`, `R53`, `R56`, `R59`, `E3`, `E4`
- Level: unit, integration
- Fixture/setup: metadata fixtures with missing fields, bad adapter names, non-pass results, wrong source commit, and invalid SHA-256
- Steps:
  - Run structured validation against each negative metadata fixture.
  - Assert missing required adapter entries fail.
  - Assert `result: fail` for any required adapter fails.
  - Assert `validation.result: fail` fails.
  - Assert checksum mismatch fails against the generated archive.
  - Assert source commit mismatch fails unless a reviewed release policy explicitly allows it.
- Expected result: release validation rejects invalid or unreproducible adapter artifact metadata.
- Failure proves: release evidence is not trustworthy.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T6. Adapter README states the install contract for both release phases

- Covers: `R43`-`R51`
- Level: contract
- Fixture/setup: `dist/adapters/README.md`
- Steps:
  - Assert it states `skills/` is canonical authored source.
  - Assert it identifies `dist/adapters/manifest.yaml` as the adapter support matrix.
  - Assert it says `v0.1.2` provides release archives while keeping tracked adapter skill bodies for the compatibility window.
  - Assert it says generated adapter skill bodies are not tracked source after the later untracking release.
  - Assert it lists per-adapter archive naming patterns and target install roots.
  - Assert it identifies the checksum and metadata location.
  - Assert it does not treat `.codex/skills/` as a public install source.
- Expected result: users can install adapters from the correct release surface for the phase they are using.
- Failure proves: install guidance can break adapter users or preserve stale `.codex` wording.
- Automation location: `scripts/test-adapter-distribution.py`

### T7. Release notes and release validation describe archive introduction and retained compatibility

- Covers: `R5`, `R57`, `R60`, `R82`-`R85`, `E1`
- Level: contract, integration
- Fixture/setup: `docs/releases/v0.1.2/release-notes.md`, optional `docs/releases/v0.1.2/release.yaml`
- Steps:
  - Assert release notes state per-adapter release archives are available.
  - Assert release notes state tracked `dist/adapters/**/skills` remain available for the compatibility window.
  - Assert release notes identify checksum and adapter artifact metadata location.
  - Assert release notes name `bash scripts/release-verify.sh v0.1.2`.
  - Assert `python scripts/validate-release.py --version v0.1.2 --release-output-dir <release-output-dir>` fails when release notes omit the archive path or retained compatibility path.
- Expected result: release notes match the archive-introduction release contract.
- Failure proves: users can miss the new archive path or lose the old compatibility path unexpectedly.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T8. Unsafe skill-validator proof-pack move is deferred with rationale

- Covers: `R64`, `R68`, `R69`, `E5`
- Level: integration, manual
- Fixture/setup: `docs/changes/0001-skill-validator/`, change-local evidence or tracked rationale surface
- Steps:
  - Search references to `docs/changes/0001-skill-validator/`.
  - If references cannot be safely updated in M4, assert the old path remains.
  - Assert a tracked or review-visible rationale states it is a retained validator fixture and historical proof pack, not active lifecycle state.
  - Assert release validation does not fail solely because the proof pack remains with rationale.
- Expected result: unsafe movement is deferred without blocking archive publication.
- Failure proves: example migration can derail the release or leave ambiguous active-looking state.
- Automation location: `scripts/test-skill-validator.py`, `scripts/test-artifact-lifecycle-validator.py`, manual reference review

### T9. Safe skill-validator proof-pack move updates references and routing

- Covers: `R64`-`R67`, `E6`
- Level: integration
- Fixture/setup: optional moved path `docs/examples/changes/skill-validator/`
- Steps:
  - If the proof pack moves, assert all references to the old path in tests, selectors, validators, docs, and release guidance are updated.
  - Assert `docs/examples/README.md` says examples are non-normative and not active lifecycle state.
  - Run selector and lifecycle tests proving the moved path is example or fixture content.
  - Run `python scripts/select-validation.py --mode explicit --path docs/examples/changes/skill-validator/change.yaml` when the path exists.
- Expected result: moved proof pack is classified as example content and does not look active.
- Failure proves: moving the proof pack created stale references or false lifecycle state.
- Automation location: `scripts/test-select-validation.py`, `scripts/test-artifact-lifecycle-validator.py`, `scripts/select-validation.py`

### T10. Workflow guide records adapter artifact metadata location

- Covers: `R70`, `R71`, `R74`, `E7`
- Level: contract
- Fixture/setup: `docs/workflows.md`
- Steps:
  - Assert `docs/workflows.md` remains the artifact-location guide.
  - Assert the artifact-location table identifies `docs/reports/adapter-artifacts/releases/` as adapter artifact metadata location when metadata becomes a release surface.
  - Assert the table remains a path map and does not define exact metadata schema.
- Expected result: contributors can find adapter artifact metadata without broad-searching release docs.
- Failure proves: path ownership drifted or the workflow guide competed with specs.
- Automation location: `scripts/test-skill-validator.py`, manual review

### T11. Public skill simplification stays bounded and preserves safety-critical guidance

- Covers: `R72`-`R75`, `E7`
- Level: contract
- Fixture/setup: affected `skills/*/SKILL.md`, generated adapter output when skills change
- Steps:
  - Assert changed public skills use concise project artifact-location lookup wording.
  - Assert each changed skill retains its portable default path where relevant.
  - Assert obsolete generated-output references are removed only when they are stale.
  - Assert safety-critical review, verification, material-finding, security, and release guidance remains present.
  - Assert broad progressive-loading optimization is not included unless sequenced after release packaging readiness.
- Expected result: public skills are shorter where safe without losing required behavior.
- Failure proves: token reduction weakened workflow safety or broadened release scope.
- Automation location: `scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, manual review

### T12. Token-cost release evidence uses canonical static source and public adapter dynamic source

- Covers: `R76`-`R79`, `R81`, `E8`
- Level: integration
- Fixture/setup: `docs/reports/token-cost/releases/v0.1.2.md`, `docs/reports/token-cost/releases/v0.1.2.yaml`, generated public adapter output
- Steps:
  - Run `python scripts/measure-skill-tokens.py` and assert static measurement uses canonical `skills/`.
  - Run `python scripts/run-token-cost-benchmarks.py --release v0.1.2 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir <run-output-dir> --skill-source <public-adapter-skill-source>`.
  - Assert `<public-adapter-skill-source>` points at generated public adapter release output or generated temporary public adapter output, not `.codex/skills/`.
  - Assert the report includes available whole-skill reads, largest command-output events, adapter packaging impact, and result quality fields when supported.
- Expected result: token-cost evidence measures the public release surface without using local runtime state.
- Failure proves: release token evidence is not comparable or uses an internal source.
- Automation location: `scripts/test-token-cost-measurement.py`, `scripts/run-token-cost-benchmarks.py`

### T13. Token-cost report validation rejects `.codex/skills/` as public skill source

- Covers: `R80`, `E8`
- Level: unit
- Fixture/setup: token-cost metadata fixture with `runner.skill_source: .codex/skills/`
- Steps:
  - Run `python scripts/validate-token-cost-report.py <negative-report.yaml>`.
  - Assert validation fails with an error that `.codex/skills/` is repository-local runtime state, not public adapter output.
  - Run validation on a report using public adapter output and assert it passes.
- Expected result: token-cost metadata cannot pass when it records `.codex/skills/` as the public source.
- Failure proves: dynamic benchmark evidence can use the wrong surface.
- Automation location: `scripts/test-token-cost-report-validation.py`, `scripts/validate-token-cost-report.py`

### T14. Final `v0.1.2` release gate validates all archive-introduction evidence

- Covers: `R1`-`R6`, `R23`-`R60`, `R63`-`R85`, `E1`, `E3`-`E8`
- Level: smoke, integration
- Fixture/setup: release-ready repository state and generated `<release-output-dir>`
- Steps:
  - Run canonical skill validation.
  - Run adapter drift and tracked adapter validation.
  - Generate and validate release archives.
  - Validate adapter artifact metadata and checksums.
  - Validate token-cost reports.
  - Validate release notes and structured release metadata.
  - Run `bash scripts/release-verify.sh v0.1.2`.
  - Run lifecycle and change metadata validation for touched authoritative artifacts.
- Expected result: `v0.1.2` is release-ready locally with archives, metadata, checksums, token-cost evidence, release notes, canonical skills, and tracked adapter compatibility.
- Failure proves: the release is not ready to publish.
- Automation location: `scripts/release-verify.sh`, `scripts/validate-release.py`, milestone validation commands

### T15. Later untracking release validation fails when generated adapter skill bodies remain tracked

- Covers: `R7`-`R11`, `R61`, `R86`, `E2`
- Level: unit, integration
- Fixture/setup: later untracking release fixture after stable archive release is modeled
- Steps:
  - Simulate an untracking release version after `v0.1.2`.
  - Include tracked files under `dist/adapters/**/skills/**`.
  - Run structured release validation for the untracking release.
  - Assert validation fails because tracked generated adapter skill bodies remain.
  - Assert release notes for the untracking release state generated public adapter skill bodies are no longer tracked source.
- Expected result: later untracking cannot complete while generated adapter skill bodies remain tracked.
- Failure proves: the repository can claim untracking without doing it.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T16. Later untracking release keeps adapter manifest and README

- Covers: `R9`-`R11`, `R62`, `R87`, `E2`
- Level: unit, integration
- Fixture/setup: later untracking release fixture
- Steps:
  - Remove `dist/adapters/manifest.yaml` in a negative fixture and assert release validation fails.
  - Remove `dist/adapters/README.md` in a negative fixture and assert release validation fails.
  - Assert release notes describe release-archive installation as the active public adapter install path.
  - Assert supported adapters remain Codex, Claude Code, and opencode unless a separate accepted proposal changes support.
- Expected result: the untracking release removes generated skill bodies but retains adapter metadata and install guidance.
- Failure proves: untracking removed the repository support surface too broadly.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T17. Release version selection is reviewed before final evidence is generated

- Covers: `R1`, edge case newer stable release
- Level: manual, contract
- Fixture/setup: release notes, artifact metadata, token-cost report paths, archive names
- Steps:
  - Before M5 final evidence, confirm no newer stable release or reserved version supersedes `v0.1.2`.
  - If the target version changes, assert archive names, metadata paths, token-cost paths, release notes, and validation commands all use the same target.
- Expected result: release evidence uses one coherent target version.
- Failure proves: artifacts can be generated for inconsistent versions.
- Automation location: manual release checklist plus release validation consistency tests where feasible

## Fixtures and data

- Temporary release output directory for generated archives.
- `dist/adapters/manifest.yaml` support matrix.
- `dist/adapters/**` tracked public adapter packages.
- `docs/reports/adapter-artifacts/releases/v0.1.2.yaml` metadata fixture.
- Positive and negative adapter metadata fixtures in `scripts/test-adapter-distribution.py` or `tests/fixtures/adapters/`.
- Token-cost fixtures under `tests/fixtures/token-cost/`.
- Optional moved proof pack under `docs/examples/changes/skill-validator/`.
- Retained proof pack under `docs/changes/0001-skill-validator/`.

## Mocking/stubbing policy

- Use temporary directories for generated archives and release-output validation.
- Use synthetic metadata fixtures for missing-field, checksum-mismatch, and non-pass-result tests.
- Do not mock archive structure validation when the standard library can inspect generated zip or tar files.
- Do not mock `git ls-files` behavior for final release checks; use direct command evidence or repository helper injection only in unit tests.
- Token-cost dynamic benchmark tests may use dry-run or fixture JSONL for regression coverage, but final release evidence must use the release benchmark command or a recorded waiver.

## Migration or compatibility tests

- `T1`-`T4` prove `v0.1.2` adds archives.
- `T2`, `T6`, and `T14` prove tracked `dist/adapters/**/skills` remains available during `v0.1.2`.
- `T15` and `T16` prove the later untracking release removes generated skill bodies only after archive-install compatibility exists.

## Observability verification

- `T14` checks release validation output summarizes canonical skill validation, tracked adapter validation, archive validation, metadata validation, token-cost validation, release notes validation, and security-sensitive scan results when supported.
- `T7` checks release notes identify the release gate command and metadata/checksum location.

## Security/privacy verification

- `T5` and `T14` cover checksum mismatch and reproducibility failures.
- `T11` checks safety-critical public skill guidance remains.
- `T12` and `T13` prevent local `.codex/skills/` paths from becoming public benchmark evidence.
- Final release validation must avoid committing generated archives and must not require private local paths.

## Performance checks

- `T12` and `T13` cover token-cost measurement and report validation.
- No runtime performance benchmark is required for adapter archive generation beyond deterministic, reproducible generation and concise validation output.

## Manual QA checklist

- Confirm release notes are understandable for users installing from repository-tree adapters or release archives.
- Confirm GitHub release assets are attached after publication and match checksums in metadata.
- Confirm target release version is still `v0.1.2` before final evidence is generated.
- Confirm any retained skill-validator proof-pack rationale is discoverable from tracked or review-visible evidence.
- Confirm any public skill wording changes are behavior-preserving.

## What not to test

- Do not test actual GitHub release publication in unit tests; use manual release-asset verification.
- Do not test unsupported adapter tools.
- Do not test broad progressive-loading optimization unless a later plan explicitly brings it into scope.
- Do not test deleting historical Git commits or rewriting history.
- Do not require a combined archive when metadata marks it not required.

## Uncovered gaps

None. Publication-time asset attachment remains manual release verification rather than an implementation blocker.

## Next artifacts

```text
implement M1
code-review M1
review-resolution when triggered
implement M2
code-review M2
review-resolution when triggered
implement M3
code-review M3
review-resolution when triggered
implement M4
code-review M4
review-resolution when triggered
implement M5
code-review M5
explain-change
verify
pr
release handoff
```

## Follow-on artifacts

None yet.

## Readiness

Active proof-planning surface for the public adapter artifact migration. The current handoff is `implement M1`; implementation is bounded by this test spec and the active plan.
