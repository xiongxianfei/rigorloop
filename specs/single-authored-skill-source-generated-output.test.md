# Single Authored Skill Source and Generated Output Test Spec

## Status

active

## Related spec and plan

- Spec: [Single Authored Skill Source and Generated Output](single-authored-skill-source-generated-output.md), approved.
- Plan: [Single Authored Skill Source First Slice Plan](../docs/plans/2026-05-12-single-authored-skill-source-first-slice.md), active.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260512-generated-skill-output-release-artifacts](../docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md), accepted.

## Testing strategy

This contract is a generated-output, repository-packaging, CI, release, and documentation migration. The active plan implements only the first slice: untracking the repository-local `.codex/skills/` mirror while preserving public adapter output under `dist/adapters/`.

The first slice is verified through:

- unit and integration coverage for `scripts/build-skills.py` temp-output generation and `--check` semantics;
- selector and CI coverage for local mirror validation routing;
- canonical skill validation and generated local mirror structural validation;
- Git-state checks that `.codex/skills/` is untracked and ignored;
- documentation and contributor-guidance checks;
- adapter distribution checks proving public adapter skill copies remain tracked and validated;
- token-cost report validation checks that `.codex/skills/` cannot be used as a public benchmark source;
- artifact lifecycle validation for the source artifacts, plan, plan index, and this test spec.

Release-artifact distribution requirements are mapped to future release-artifact tests and manual release verification. They are not implementation scope for the first-slice plan.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| `R1` | `T1`, `T9`, `T10` |
| `R2` | `T1`, `T2`, `T6`, `T10` |
| `R3` | `T7`, `T9`, `T10` |
| `R4` | `T6`, `T7`, `T10` |
| `R5` | `T1`, `T6`, `T7` |
| `R6` | `T6`, `T7`, `T8` |
| `R7` | `T7`, `T8` |
| `R8` | `T7`, `T8`, `T11` |
| `R9` | `T6` |
| `R10` | `T2`, `T10` |
| `R11` | `T6` |
| `R12` | `T2`, `T3`, `T6` |
| `R13` | `T2`, `T3` |
| `R14` | `T2`, `T3`, `T4` |
| `R15` | `T2`, `T3` |
| `R16` | `T3`, `T5` |
| `R17` | `T3`, `T5` |
| `R18` | `T7`, `T11` |
| `R19` | `T11` |
| `R20` | `T12`, `T18` |
| `R21` | `T12` |
| `R22` | `T12`, `T18` |
| `R23` | `T12` |
| `R24`-`R36` | `T14`, `T15`, future release-artifact plan |
| `R37` | `T13`, `T16` |
| `R38`-`R42` | `T14`, `T16`, future release-artifact plan |
| `R43` | `T7`, `T8`, `T18` |
| `R44`-`R48` | `T18`, future release-artifact plan |
| `R49` | `T7`, `T8` |
| `R50` | `T17`, future public adapter cleanup plan |
| `R51` | `T4`, `T8` |
| `R52` | `T4` |
| `R53`-`R58` | `T15`, future release-artifact plan |
| `R59` | `T2`, `T3` |
| `R60` | `T2`, `T3`, `T6` |
| `R61` | `T9` |
| `R62` | `T9` |
| `R63` | `T9` |
| `R64` | `T17`, future public adapter cleanup plan |
| `R65` | `T9` |
| `R66` | `T9` |
| `R67` | `T10` |
| `R68` | `T10` |
| `R69` | `T10`, `T12` |
| `R70` | `T10`, `T12` |
| `R71` | `T10` |
| `R72` | `T10`, `T12`, `T18` |
| `R73` | `T10`, `T12` |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` | `T2`, `T3`, `T6` |
| `E2` | `T6`, `T7`, `T8`, `T10` |
| `E3` | `T11`, `T12` |
| `E4` | `T14`, `T15`, future release-artifact plan |
| `E5` | `T18`, future release-artifact plan |
| `E6` | `T9` |
| `E7` | `T13`, `T16`, future release-artifact plan |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` | `T2`, `T3` |
| `EC2` | `T7`, `T8` |
| `EC3` | `T14`, `T18`, future release-artifact plan |
| `EC4` | `T18`, future release-artifact plan |
| `EC5` | `T7`, `T8` |
| `EC6` | `T10`, `T12`, `T18` |
| `EC7` | `T9` |
| `EC8` | `T13`, `T16` |
| `EC9` | `T11` |
| `EC10` | `T12`, `T18` |
| `EC11` | `T15`, future release-artifact plan |
| `EC12` | `T14`, future release-artifact plan |

## Test cases

### T1. Canonical skills remain the authored source

- Covers: `R1`, `R5`
- Level: unit
- Fixture/setup: canonical `skills/**/SKILL.md`, `scripts/skill_validation.py`, `scripts/validate-skills.py`
- Steps:
  - Run `python scripts/validate-skills.py`.
  - Keep or add assertions that generated local mirror paths are rejected as authored validation targets.
  - Confirm implementation does not use `.codex/skills/` or `dist/adapters/**/skills` as the source for canonical skill discovery.
- Expected result: canonical skill validation passes, and generated output is not accepted as authored source.
- Failure proves: generated skill copies can still become source-of-truth inputs.
- Automation location: `scripts/validate-skills.py`, `scripts/skill_validation.py`, `scripts/test-skill-validator.py`

### T2. Local mirror generation supports explicit temp output

- Covers: `R2`, `R10`, `R12`-`R15`, `R59`, `R60`, `E1`, `EC1`
- Level: integration
- Fixture/setup: canonical `skills/`; a temporary directory from `mktemp -d`
- Steps:
  - Add `--output-dir` support or equivalent explicit temp-output path to `scripts/build-skills.py`.
  - Run `tmpdir="$(mktemp -d)" && python scripts/build-skills.py --output-dir "$tmpdir/skills"`.
  - Validate generated output with `python scripts/validate-skills.py "$tmpdir/skills"` or an equivalent generated-output validation mode.
  - Assert no tracked `.codex/skills/<skill>/SKILL.md` file is required for the command to pass.
- Expected result: temp output contains a complete local Codex mirror generated from canonical `skills/`, and structural validation passes.
- Failure proves: the local mirror cannot be generated on demand after tracked files are removed.
- Automation location: `scripts/build-skills.py`, optional `scripts/test-build-skills.py`

### T3. Local mirror `--check` no longer performs tracked-file drift

- Covers: `R12`-`R17`, `R59`, `R60`, `E1`, `EC1`
- Level: unit
- Fixture/setup: temporary repository or temporary output directory with `.codex/skills/` absent
- Steps:
  - Run `python scripts/build-skills.py --check` after `.codex/skills/` has been removed from tracked state.
  - Assert `--check` generates or validates non-tracked output rather than comparing canonical files against tracked `.codex/skills/`.
  - Add a negative fixture where generated output is structurally invalid or generation fails.
- Expected result: `--check` passes without tracked `.codex/skills/` files and fails on generation or structural validation errors.
- Failure proves: validation still depends on tracked local mirror files or fails to catch invalid generated output.
- Automation location: `scripts/build-skills.py`, optional `scripts/test-build-skills.py`

### T4. Selector and CI keep local mirror validation on relevant changes

- Covers: `R14`, `R51`, `R52`
- Level: unit
- Fixture/setup: `scripts/validation_selection.py`, `scripts/ci.sh`, selector fixtures
- Steps:
  - Update selected-check labels and commands so local mirror proof is described as temp-output generation/validation, not tracked drift.
  - Assert canonical `skills/**`, `scripts/build-skills.py`, and skill validator changes select the local mirror proof.
  - Assert unrelated paths can skip adapter or local mirror work when the selector says they cannot affect generated output.
  - Confirm broad smoke still includes the local mirror proof command.
- Expected result: relevant paths select local mirror validation; unrelated paths do not force unnecessary generated-output checks.
- Failure proves: CI can skip required local mirror proof or keep stale drift terminology.
- Automation location: `scripts/test-select-validation.py`, `scripts/ci.sh`

### T5. Local mirror validation fails on invalid generated output

- Covers: `R16`, `R17`
- Level: unit
- Fixture/setup: temporary generated output with missing or malformed `SKILL.md`
- Steps:
  - Create or simulate generated output with a missing skill, malformed frontmatter, or invalid required section.
  - Run the generated-output validation path used by `build-skills.py --check`.
  - Assert the command exits non-zero and identifies the invalid generated mirror.
- Expected result: invalid generated output fails validation.
- Failure proves: temp-output validation is generation-only and does not prove runtime structure.
- Automation location: optional `scripts/test-build-skills.py`, `scripts/validate-skills.py`

### T6. `.codex/skills/` is untracked, ignored, and restorable on demand

- Covers: `R2`, `R4`, `R6`, `R9`, `R11`, `R12`, `R60`, `E1`, `E2`
- Level: integration
- Fixture/setup: repository Git state after M2
- Steps:
  - Assert `test -z "$(git ls-files .codex/skills)"`.
  - Assert `git check-ignore .codex/skills/proposal/SKILL.md` succeeds.
  - Run `python scripts/build-skills.py` and confirm it recreates `.codex/skills/` locally without adding tracked files.
  - Run `python scripts/build-skills.py --check`.
  - Confirm no history-rewrite command or history-cleanup artifact is introduced.
- Expected result: `.codex/skills/` is no longer tracked, is ignored, and can be regenerated locally.
- Failure proves: the first-slice migration did not actually remove the local mirror from day-to-day Git state or broke local runtime regeneration.
- Automation location: shell validation in plan, `scripts/build-skills.py`

### T7. Public adapter skill copies remain tracked and validated

- Covers: `R3`, `R4`, `R6`-`R8`, `R18`, `R43`, `R49`, `E2`, `EC2`, `EC5`
- Level: integration
- Fixture/setup: tracked `dist/adapters/**` output
- Steps:
  - Assert tracked public adapter skill files still exist with `git ls-files 'dist/adapters/*/.*/skills/*/SKILL.md'`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Confirm implementation did not delete, untrack, or restructure public adapter skill copies.
- Expected result: public adapter packages remain tracked, in sync, and structurally valid.
- Failure proves: the first slice broke the compatibility window or repository-tree adapter installation.
- Automation location: `scripts/build-adapters.py`, `scripts/validate-adapters.py`, `scripts/test-adapter-distribution.py`

### T8. Repository-tree adapter install path remains usable

- Covers: `R7`, `R8`, `R43`, `R49`, `E2`, `EC2`, `EC5`
- Level: integration
- Fixture/setup: temporary downstream project root
- Steps:
  - Copy each tracked adapter package root from `dist/adapters/<adapter>/` into a temporary project root.
  - Confirm expected entrypoint and skill root files exist for Codex, Claude Code, and opencode.
  - Confirm `.codex/skills/` is not used as the public Codex adapter install source.
- Expected result: repository-tree adapter installation remains available for all supported adapters.
- Failure proves: the first slice silently changed public adapter installation behavior.
- Automation location: `scripts/test-adapter-distribution.py`

### T9. Token-cost public source validation rejects `.codex/skills/`

- Covers: `R61`-`R66`, `E6`, `EC7`
- Level: unit
- Fixture/setup: token-cost report metadata fixtures
- Steps:
  - Add or keep a valid fixture with `runner.skill_source: dist/adapters/codex/.agents/skills/`.
  - Add a negative fixture with `runner.skill_source: .codex/skills/`.
  - Run `python scripts/test-token-cost-report-validation.py`.
  - Run `python scripts/validate-token-cost-report.py` against the valid fixture.
- Expected result: public adapter skill source passes while `.codex/skills/` fails with a clear validation error.
- Failure proves: benchmarks can accidentally measure the repository-local mirror as public skill output.
- Automation location: `scripts/validate-token-cost-report.py`, `scripts/test-token-cost-report-validation.py`

### T10. Contributor docs explain the current source boundary

- Covers: `R1`-`R5`, `R10`, `R67`-`R73`, `EC6`
- Level: contract
- Fixture/setup: `README.md`, `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`
- Steps:
  - Update contributor-facing docs to state `skills/` is the only authored skill source.
  - State `.codex/skills/` is generated local runtime output after the first slice.
  - State public adapter skill copies remain generated public adapter output and remain tracked during the compatibility window.
  - Document the local mirror regeneration command.
  - Run `python scripts/validate-readme.py README.md`.
  - Run scoped lifecycle and whitespace validation.
- Expected result: docs explain current migration state without implying generated skill copies are authored source.
- Failure proves: contributors can still mistake generated output for canonical source or public install guidance can become stale.
- Automation location: docs plus `scripts/validate-readme.py`

### T11. Adapter manifest remains tracked metadata without generated skill bodies

- Covers: `R18`, `R19`, `E3`, `EC9`
- Level: unit
- Fixture/setup: `dist/adapters/manifest.yaml`
- Steps:
  - Assert `dist/adapters/manifest.yaml` is tracked.
  - Parse or inspect the manifest as metadata.
  - Assert it does not contain generated skill body headings or full `SKILL.md` content.
  - Run adapter validation.
- Expected result: manifest remains tracked support metadata and does not embed generated skill text.
- Failure proves: tracked metadata is becoming another generated skill-body copy.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-adapters.py`

### T12. Adapter README exists before public adapter cleanup

- Covers: `R20`-`R23`, `R69`-`R73`, `E3`, `EC6`, `EC10`
- Level: contract
- Fixture/setup: `dist/adapters/README.md`
- Steps:
  - Add `dist/adapters/README.md` if absent, or verify it exists if added by a prior milestone.
  - Assert it names canonical skills under `skills/`.
  - Assert it identifies `dist/adapters/manifest.yaml` as support metadata.
  - Assert it describes release artifact installation as the later public adapter migration path without retiring repository-tree installation in the first slice.
- Expected result: tracked adapter guidance exists before future public adapter cleanup.
- Failure proves: users will lose a visible support/install surface when generated adapter skill bodies are eventually untracked.
- Automation location: docs review; optional static assertion in `scripts/test-adapter-distribution.py`

### T13. Generated adapter archives are not committed in the first slice

- Covers: `R37`, `E7`, `EC8`
- Level: integration
- Fixture/setup: repository Git state
- Steps:
  - Run `! git ls-files | rg '(^|/)rigorloop-adapter-.*\.(zip|tar\.gz)$'`.
  - Confirm implementation did not add generated archive files under `dist/`, `docs/`, or release artifact directories.
- Expected result: no generated adapter archives are tracked.
- Failure proves: binary/generated release artifacts are being committed instead of distributed as release assets.
- Automation location: shell validation in plan

### T14. Adapter artifact metadata schema is validated when release artifacts are introduced

- Covers: `R24`-`R36`, `R38`-`R42`, `E4`, `E7`, `EC3`, `EC11`, `EC12`
- Level: future integration
- Fixture/setup: future `docs/reports/adapter-artifacts/releases/<version>.yaml` fixture and generated adapter archives
- Steps:
  - In the future release-artifact plan, add valid and invalid metadata fixtures.
  - Validate required fields: `schema_version`, release version, source commit, generator command, canonical source, manifest path, archives, SHA-256 checksums, validation command, validation result, and validation timestamp.
  - Validate required separate per-adapter archives and optional combined archive behavior.
- Expected result: release artifact metadata is parseable, complete, and tied to generated artifacts.
- Failure proves: generated release artifacts are not reproducible or reviewable after public adapter cleanup.
- Automation location: future adapter artifact metadata validator and release validation

### T15. Release validation validates generated adapters and artifact metadata

- Covers: `R53`-`R58`, `R24`-`R36`, `E4`, `EC11`
- Level: future integration
- Fixture/setup: future release output directory with generated adapters, archives, metadata, and release notes
- Steps:
  - In the future release-artifact plan, run release validation against generated adapter output.
  - Assert release validation fails when adapter output cannot be generated.
  - Assert release validation fails when adapter structure is invalid.
  - Assert release validation fails when metadata is missing, invalid, or checksum mismatched.
- Expected result: public release readiness depends on generated adapter and metadata proof.
- Failure proves: release artifacts can diverge from canonical `skills/` or metadata can lie about distributed archives.
- Automation location: future `scripts/validate-release.py`, `scripts/release-verify.sh`, or adapter artifact validator

### T16. Release artifact distribution uses assets, not committed archives

- Covers: `R37`-`R42`, `E7`, `EC8`
- Level: future release smoke
- Fixture/setup: future release workflow output
- Steps:
  - Generate per-adapter archives and optional combined archive in release workflow or CI artifact storage.
  - Upload archives as release assets.
  - Track metadata and checksums only.
  - Assert no archive files are committed to Git without an approved exception.
- Expected result: release assets distribute archives while Git tracks metadata evidence.
- Failure proves: generated archives are being treated as authored repository content.
- Automation location: future release workflow and release validation

### T17. Public adapter cleanup replaces tracked drift with temp-output validation

- Covers: `R50`, `R64`
- Level: future integration
- Fixture/setup: future repository state after public adapter skill copies are untracked
- Steps:
  - Remove tracked public adapter skill copies only after the compatibility window is satisfied.
  - Generate adapter output into a temporary directory or release artifact directory.
  - Run adapter structural validation against that generated output.
  - Run dynamic public-surface benchmarks from generated adapter output or release artifact output.
- Expected result: public adapter validation no longer depends on tracked skill-copy drift after cleanup.
- Failure proves: public adapter migration removed tracked files without replacing validation.
- Automation location: future `scripts/build-adapters.py`, `scripts/validate-adapters.py`, token-cost benchmark runner

### T18. Compatibility window blocks premature public adapter removal

- Covers: `R20`, `R22`, `R43`-`R48`, `R72`, `E5`, `EC3`, `EC4`, `EC6`, `EC10`
- Level: future contract/manual
- Fixture/setup: release notes, adapter artifact metadata, tracked public adapter output, install docs
- Steps:
  - Before any public adapter skill-copy removal, verify at least one stable public release already provided downloadable adapter artifacts and release-artifact install docs while tracked `dist/adapters/**/skills` remained available.
  - Verify release notes announced the repository-tree install path transition.
  - Verify the release that removes tracked public adapter skill copies documents artifact-install instructions and preserves support metadata.
  - Block removal unless an explicit approved exception shortens the compatibility window.
- Expected result: users who copy from `dist/adapters/` receive a compatibility window before repository-tree skill bodies disappear.
- Failure proves: public adapter distribution was broken without migration evidence.
- Automation location: future release validation plus manual release review

### T19. Lifecycle and plan state stay synchronized

- Covers: workflow closeout integrity for all in-scope requirements
- Level: integration
- Fixture/setup: proposal, spec, architecture, ADR, plan, plan index, test spec, and change-local artifacts when created
- Steps:
  - Run explicit artifact lifecycle validation over the source artifacts, active plan, plan index, and this test spec.
  - During implementation, update the active plan's `Current Handoff Summary`, progress, decisions, surprises, and validation notes after each milestone state change.
  - Before PR handoff, ensure `docs/plan.md` and the plan body agree on active/done state.
- Expected result: lifecycle artifacts remain consistent and downstream readiness is not claimed from stale plan state.
- Failure proves: implementation evidence is not durable or reviewable.
- Automation location: `scripts/validate-artifact-lifecycle.py`, plan updates, `git diff --check`

## Fixtures and data

Likely new or updated fixtures:

- temporary generated skill trees under `mktemp -d` for local mirror validation;
- optional invalid generated skill fixture for structural validation failure;
- selector fixtures in `scripts/test-select-validation.py`;
- token-cost report fixtures under `tests/fixtures/token-cost/reports/`;
- optional adapter-distribution assertions using tracked `dist/adapters/manifest.yaml` and adapter package roots.

Generated temp directories must not be committed.

## Mocking/stubbing policy

- Prefer real repository scripts over mocks for generation and validation.
- Use temporary directories for generated-output tests.
- Use fixture metadata for token-cost validator negative cases.
- Do not require Codex, Claude Code, or opencode runtime binaries for this first slice; adapter structure is validated through repository-owned scripts.
- Future release-artifact workflow tests may stub upload mechanics, but checksum validation must run against real generated archive files.

## Migration or compatibility tests

The first-slice migration compatibility proof is:

- `.codex/skills/` removed from tracked state and ignored;
- `python scripts/build-skills.py` regenerates `.codex/skills/` on demand;
- `python scripts/build-skills.py --check` validates non-tracked output;
- public adapter skill copies remain tracked and pass adapter drift/structure validation;
- repository-tree adapter installation remains usable.

Future public adapter cleanup must use `T14`-`T18` before tracked public adapter skill copies are removed.

## Observability verification

- `build-skills.py --check` output should identify that it validated generated local mirror output from canonical skills.
- Selector and CI output should use wording that does not imply `.codex/skills/` tracked drift after M2.
- Adapter validation output should still identify tracked public adapter output while that output remains tracked.
- Token-cost validation errors should name `.codex/skills/` as an invalid public benchmark source when used.

## Security/privacy verification

- No generated adapter archives are committed.
- No generated-output metadata or docs should include secrets, credentials, private keys, account-specific paths, or private local filesystem paths.
- Temporary output paths are validation surfaces, not durable release evidence.
- Release-artifact security checks remain future release-plan scope.

## Performance checks

- Temp-output validation should avoid printing full generated skill bodies in routine success output.
- Ordinary path selection should not force full adapter builds for unrelated changes.
- Release validation remains correctness-first in future release-artifact work.

## Manual QA checklist

- Confirm README and workflow docs explain the current migration phase accurately.
- Confirm `.codex/skills/` can be regenerated locally after it is removed from Git.
- Confirm `dist/adapters/` remains usable as a repository-tree install surface.
- Confirm no public adapter release-artifact claims are made before release packaging exists.

## What not to test

- Do not test public adapter archive upload in the first slice; release artifact packaging is future scope.
- Do not test removal of `dist/adapters/**/skills` in the first slice; the spec forbids it.
- Do not require Claude Code or opencode runtime smoke for this first slice; repository adapter validation is the supported proof.
- Do not snapshot full generated skill bodies as the primary behavioral proof.
- Do not test Git history rewriting; the required behavior is that no history rewrite is performed.

## Uncovered gaps

None for the first-slice implementation plan.

Future public adapter release-artifact migration still needs implementation tests for archive creation, checksum metadata, release notes, compatibility-window enforcement, and temp-output public adapter validation.

## Next artifacts

- implementation
- code-review for each implementation milestone
- review-resolution if triggered
- explain-change
- verify
- pr

## Follow-on artifacts

None yet.

## Readiness

This test spec is the active proof surface for the first-slice implementation. The active plan `Current Handoff Summary` owns the next workflow action.
