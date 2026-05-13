# Publish Next Release With Single Authored Skill Source Test Spec

## Status

active

## Related spec and plan

- Spec: [Publish Next Release With Single Authored Skill Source](publish-next-release-with-single-authored-skill-source.md), approved.
- Plan: [Publish Next Release With Single Authored Skill Source](../docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md), active and approved by plan-review R1.
- Proposal: [Publish Next Release With Single Authored Skill Source](../docs/proposals/2026-05-12-publish-next-release-with-single-authored-skill-source.md), accepted.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260512-generated-skill-output-release-artifacts](../docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml).
- Review records:
  - `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/spec-review-r2.md`
  - `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/architecture-review-r2.md`
  - `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/plan-review-r1.md`

## Testing strategy

This change is a release packaging, validation, and documentation slice. The primary risk is accidentally keeping `.codex/skills/` as a privileged release surface while claiming the release validates public adapter output.

Use:

- unit and integration tests in `scripts/test-adapter-distribution.py` for release gate dry-run behavior, release metadata validation, adapter README assertions, release-note assertions, tracked public adapter compatibility, and optional archive metadata behavior;
- existing token-cost metadata tests and `scripts/validate-token-cost-report.py` for public Codex adapter source enforcement;
- release-gate smoke through `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1` and final `bash scripts/release-verify.sh v0.1.1`;
- adapter drift and adapter structural validation for tracked public adapter output under `dist/adapters/`;
- lifecycle validation for the spec, test spec, architecture, plan, plan index, and change-local review evidence;
- manual inspection only for text quality of release notes and adapter install guidance.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| `R1` | `T1`, `T5`, `T8`, `T12` |
| `R2` | `T2`, `T3`, `T5`, `T10`, `T12` |
| `R3` | `T1`, `T4`, `T6`, `T12` |
| `R4` | `T4`, `T6`, `T12` |
| `R5` | `T4`, `T6`, `T12` |
| `R6` | `T4`, `T5`, `T12`, manual review |
| `R7` | `T1`, `T12` |
| `R8` | `T1`, `T2`, `T7`, `T12` |
| `R9` | `T1`, `T12` |
| `R10` | `T1`, `T12` |
| `R11` | `T1`, `T4`, `T6`, `T12` |
| `R12` | `T5`, `T7`, `T12` |
| `R13` | `T1`, `T7`, `T9`, `T12` |
| `R14` | `T5`, `T7`, `T12` |
| `R15` | `T2`, `T3`, `T12` |
| `R16` | `T1`, `T2`, `T3`, `T12` |
| `R17` | `T3`, `T5`, manual review |
| `R18` | `T4`, `T6`, `T12` |
| `R19` | `T4`, `T12` |
| `R20` | `T5`, `T11`, manual review |
| `R21` | `T5`, `T8`, manual review |
| `R22` | `T5`, `T8` |
| `R23` | `T5`, `T11` |
| `R24` | `T5`, `T11` |
| `R25` | `T5`, `T11` |
| `R26` | `T5`, `T8`, `T12` |
| `R27` | `T5`, `T8`, manual review |
| `R28` | `T8`, `T12` |
| `R29` | `T8`, `T12` |
| `R30` | `T8`, `T12` |
| `R31` | `T8`, `T12` |
| `R32` | `T9`, `T12` |
| `R33` | `T9`, `T12` |
| `R34` | `T9`, `T12` |
| `R35` | `T9`, `T12` |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` | `T1`, `T2`, `T4`, `T12` |
| `E2` | `T3`, `T5`, `T11` |
| `E3` | `T5`, `T8`, manual review |
| `E4` | `T8`, `T12` |
| `E5` | `T9`, `T12` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` no archives | `T5`, `T8`, `T12` |
| `EC2` optional archives | `T8`, `T12` |
| `EC3` local `.codex/skills/` exists but is ignored | `T2`, `T3`, `T12` |
| `EC4` `.codex/skills/` is tracked | `T2`, `T12` |
| `EC5` token-cost metadata points to `.codex/skills/` | `T9`, `T12` |
| `EC6` token-cost metadata points to public Codex adapter output | `T9`, `T12` |
| `EC7` adapter README omits `v0.1.1` install guidance | `T5`, `T11`, `T12` |
| `EC8` adapter README incorrectly requires archives | `T5`, `T8`, `T12` |
| `EC9` release validators disagree | `T1`, `T7`, `T12` |
| `EC10` release version changes | `T7`, `T12`, manual review |

## Test cases

### T1. `v0.1.1` release gate validates public output instead of `.codex/skills/`

- Covers: `R1`, `R3`, `R7`-`R13`, `R16`, `E1`, `EC9`
- Level: integration
- Fixture/setup:
  - `scripts/release-verify.sh`
  - existing dry-run tests in `scripts/test-adapter-distribution.py`
- Steps:
  - Run `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`.
  - Assert output includes `python scripts/validate-skills.py`.
  - Assert output includes `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Assert output includes `python scripts/validate-adapters.py --version 0.1.1`.
  - Assert output includes `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`.
  - Assert output includes `python scripts/validate-release.py --version v0.1.1`.
  - Assert output does not include `python scripts/build-skills.py --check` for `v0.1.1`.
- Expected result: The maintainer-facing gate delegates structured checks and validates public adapter output without making local Codex mirror generation required release evidence.
- Failure proves: the release gate still treats `.codex/skills/` as a privileged release surface or omits public adapter proof.
- Automation location: `scripts/test-adapter-distribution.py`

### T2. Release validation fails when `.codex/skills/` is tracked

- Covers: `R2`, `R15`, `R16`, `EC3`, `EC4`
- Level: integration
- Fixture/setup:
  - temporary repository fixture or mocked tracked-file list in `scripts/test-adapter-distribution.py`;
  - `adapter_distribution.validate_release_output`.
- Steps:
  - Add a positive fixture where `.codex/skills/` exists locally but is ignored/untracked.
  - Add a negative fixture where `.codex/skills/proposal/SKILL.md` appears in tracked files.
  - Run release validation for `v0.1.1`.
- Expected result: Ignored local runtime state is allowed; tracked `.codex/skills/` files fail release readiness.
- Failure proves: the release gate cannot enforce the source-of-truth boundary.
- Automation location: `scripts/test-adapter-distribution.py`

### T3. Release validation does not build or structurally validate `.codex/skills/`

- Covers: `R2`, `R15`-`R17`, `E2`, `EC3`
- Level: unit
- Fixture/setup:
  - dry-run release gate output;
  - release validation helper tests.
- Steps:
  - Assert `v0.1.1` required release commands omit `build-skills.py --check`.
  - Assert release validation only checks `.codex/skills/` ignored/untracked state.
  - Assert optional local Codex smoke evidence is not required by `validate-release.py`.
- Expected result: `.codex/skills/` is not built, generated, or structurally validated as release evidence.
- Failure proves: the release contract still has a local mirror dependency.
- Automation location: `scripts/test-adapter-distribution.py`

### T4. Tracked public adapter output remains current and valid

- Covers: `R3`-`R6`, `R11`, `R18`, `R19`, `E1`
- Level: integration
- Fixture/setup:
  - tracked `dist/adapters/**`;
  - `dist/adapters/manifest.yaml`.
- Steps:
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Assert tracked public adapter skill files still exist for Codex, Claude Code, and opencode.
- Expected result: Public adapter output is in sync with canonical skills, structurally valid, and still tracked for the compatibility window.
- Failure proves: public adapter install compatibility was weakened.
- Automation location: `scripts/build-adapters.py`, `scripts/validate-adapters.py`, `scripts/test-adapter-distribution.py`

### T5. Adapter README and contributor docs describe transition boundaries

- Covers: `R1`, `R2`, `R6`, `R12`, `R14`, `R20`-`R27`, `E2`, `E3`, `EC1`, `EC7`, `EC8`
- Level: contract
- Fixture/setup:
  - `dist/adapters/README.md`;
  - contributor docs that are updated in M2;
  - docs assertions in `scripts/test-adapter-distribution.py`.
- Steps:
  - Assert `dist/adapters/README.md` names `v0.1.1`.
  - Assert it states repository-tree package roots under `dist/adapters/` are the public install path.
  - Assert it states no downloadable adapter archives are required for `v0.1.1` unless separately published.
  - Assert it names `docs/reports/adapter-artifacts/releases/<version>.yaml`.
  - Assert it says `.codex/skills/` is not a public adapter install source.
  - Assert contributor-facing local Codex setup says to install or copy from public Codex adapter output into ignored `.codex/skills/`.
- Expected result: Public and contributor guidance makes the source boundary and transition install path unambiguous.
- Failure proves: users or contributors can follow stale `.codex` or archive guidance.
- Automation location: `scripts/test-adapter-distribution.py`; manual review for prose quality.

### T6. Repository-tree adapter install path remains usable for all supported adapters

- Covers: `R3`-`R5`, `R11`, `R18`, `E1`
- Level: integration
- Fixture/setup:
  - temporary downstream project root;
  - tracked package roots under `dist/adapters/codex/`, `dist/adapters/claude/`, and `dist/adapters/opencode/`.
- Steps:
  - Copy each adapter package root into a temporary project root.
  - Assert Codex entrypoint and `.agents/skills/` files exist.
  - Assert Claude Code entrypoint and `.claude/skills/` files exist.
  - Assert opencode entrypoint, `.opencode/skills/`, and command aliases exist.
  - Assert `.codex/skills/` is not used as the source for public installation.
- Expected result: Repository-tree install compatibility is intact for Codex, Claude Code, and opencode.
- Failure proves: the transition release changed the public install model.
- Automation location: `scripts/test-adapter-distribution.py`

### T7. Structured release validation checks release notes, docs, token metadata, and adapters

- Covers: `R8`, `R12`-`R14`, `R18`, `R19`, `EC9`, `EC10`
- Level: integration
- Fixture/setup:
  - `scripts/validate-release.py`;
  - `adapter_distribution.validate_release_output`;
  - `docs/releases/v0.1.1/release.yaml`;
  - `docs/releases/v0.1.1/release-notes.md`.
- Steps:
  - Run `python scripts/validate-release.py --version v0.1.1`.
  - Add or update tests that reject missing release notes for `v0.1.1`.
  - Add or update tests that reject stale or invalid public adapter output.
  - Add or update tests that reject missing or invalid required token-cost metadata.
  - Confirm `release-verify.sh` and `validate-release.py` agree on required `v0.1.1` checks.
- Expected result: Structured release validation owns release metadata, notes, adapter evidence, and token-cost evidence.
- Failure proves: the maintainer-facing gate and structured validator can drift.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`

### T8. Downloadable archives are optional and require metadata only when present

- Covers: `R21`, `R22`, `R26`-`R31`, `E3`, `E4`, `EC1`, `EC2`, `EC8`
- Level: unit
- Fixture/setup:
  - release metadata fixtures with no archive metadata;
  - release metadata fixtures that simulate optional archive publication.
- Steps:
  - Assert `v0.1.1` validation passes without `docs/reports/adapter-artifacts/releases/v0.1.1.yaml` when no archives are published.
  - Assert docs or release notes state no downloadable archives are introduced when metadata is absent.
  - Add an optional-archive fixture where metadata is present and includes schema version, release version, source commit, generator command, canonical skill source, manifest path, archive list, SHA-256 checksums, validation command, and validation result.
  - Add negative optional-archive fixtures with missing checksum or missing metadata.
  - Assert generated adapter archives are not committed.
- Expected result: Archives do not block `v0.1.1` by default, but optional archives cannot bypass metadata and checksum proof.
- Failure proves: the transition release either requires a follow-on migration too early or accepts unverifiable archives.
- Automation location: `scripts/test-adapter-distribution.py`

### T9. Token-cost metadata uses canonical skills and public Codex adapter output

- Covers: `R13`, `R32`-`R35`, `E5`, `EC5`, `EC6`
- Level: unit
- Fixture/setup:
  - `docs/reports/token-cost/releases/v0.1.1.yaml`;
  - token-cost validator fixtures.
- Steps:
  - Run `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`.
  - Assert static measurement command or metadata identifies canonical `skills/`.
  - Assert dynamic Codex source is `dist/adapters/codex/.agents/skills/` while tracked public adapter output remains available.
  - Assert a negative fixture with `.codex/skills/` as runner skill source fails.
- Expected result: Token-cost evidence measures the public release surface and rejects the local runtime directory.
- Failure proves: release evidence can accidentally measure duplicate local output instead of public adapter output.
- Automation location: `scripts/validate-token-cost-report.py`, token-cost validator tests.

### T10. Local Codex smoke remains optional and private

- Covers: `R2`, `R17`, security/privacy behavior
- Level: manual
- Fixture/setup:
  - optional local shell;
  - public Codex adapter output under `dist/adapters/codex/.agents/skills/`.
- Steps:
  - If a maintainer chooses local smoke, copy public Codex adapter skills into `.codex/skills/` locally.
  - Confirm `.codex/skills/` remains ignored and untracked.
  - Do not record machine-local `.codex/skills/` contents as release evidence.
- Expected result: Local smoke follows the same public adapter path as users and stays outside required release evidence.
- Failure proves: private local runtime state can leak into release proof.
- Automation location: manual optional check only.

### T11. Release notes and adapter docs are manually reviewable

- Covers: `R20`-`R25`, `R27`, `E2`, `E3`, `EC7`
- Level: manual
- Fixture/setup:
  - `docs/releases/v0.1.1/release-notes.md`;
  - `dist/adapters/README.md`.
- Steps:
  - Read release notes and adapter README.
  - Confirm the wording says `skills/` is canonical, `.codex/skills/` is ignored local runtime state, `dist/adapters/` remains the public install path, and archives are deferred unless separately published.
  - Confirm no wording says `.codex/skills/` is checked as release evidence.
- Expected result: Human-facing release text matches the validation contract.
- Failure proves: automated checks may pass while release communications remain misleading.
- Automation location: manual QA checklist plus targeted docs assertions in `scripts/test-adapter-distribution.py`.

### T12. Final release-readiness command pack passes

- Covers: `R1`-`R35`, `E1`-`E5`, all edge cases through integrated proof
- Level: smoke
- Fixture/setup:
  - completed M1 and M2 implementation;
  - tracked `dist/adapters/`;
  - tracked release notes and token-cost metadata.
- Steps:
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Run `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`.
  - Run `python scripts/validate-release.py --version v0.1.1`.
  - Run `bash scripts/release-verify.sh v0.1.1`.
  - Run lifecycle and review artifact validation named in the active plan.
  - Run `git diff --check --`.
- Expected result: Final release readiness proof passes without `.codex/skills/` generation as release evidence.
- Failure proves: one or more release contract surfaces are stale or inconsistent.
- Automation location: active plan M3 validation pack.

## Fixtures and data

- Existing release metadata: `docs/releases/v0.1.1/release.yaml`.
- Existing release notes: `docs/releases/v0.1.1/release-notes.md`.
- Existing token-cost metadata: `docs/reports/token-cost/releases/v0.1.1.yaml`.
- Public adapter output: `dist/adapters/`.
- Adapter manifest: `dist/adapters/manifest.yaml`.
- Adapter README: `dist/adapters/README.md`.
- Release validation fixtures inside `scripts/test-adapter-distribution.py`.
- Token-cost validator fixtures used by `scripts/validate-token-cost-report.py` tests.
- Temporary directories for repository-tree adapter install tests and optional local smoke.

## Mocking/stubbing policy

- Use `RELEASE_VERIFY_DRY_RUN=1` to test release-gate command selection without running expensive commands.
- Unit tests may stub or fixture tracked-file state for `.codex/skills/` to avoid mutating the real Git index.
- Do not mock `build-adapters.py --check`, `validate-adapters.py`, `validate-release.py`, or `validate-token-cost-report.py` in final release-readiness validation.
- Manual local Codex smoke is optional and must not be required for ordinary contributors.

## Migration or compatibility tests

- Verify public adapter packages for Codex, Claude Code, and opencode remain tracked under `dist/adapters/`.
- Verify repository-tree adapter installation remains documented and structurally usable.
- Verify `v0.1.1` does not require downloadable adapter archives.
- Verify optional archive metadata is validated only when archives are separately published.
- Verify historical release tests are preserved or intentionally scoped if `v0.1.0` retains older release-gate expectations.

## Observability verification

- `release-verify.sh v0.1.1` output should identify canonical skill validation, public adapter drift validation, adapter validation, token-cost validation, release metadata validation, and security categories.
- Release validation output should not describe `.codex/skills/` generation as release evidence.
- Token-cost metadata must identify the dynamic public skill source.

## Security/privacy verification

- Release validation continues rejecting private paths, secrets, credentials, private keys, and account-specific local setup in release notes or metadata.
- Optional local Codex smoke must not publish `.codex/skills/` contents as release evidence.
- Adapter archives, if optional fixtures simulate them, require checksum evidence and must not be committed to Git.
- Generated skill bodies should not be printed as routine release proof.

## Performance checks

- No new performance benchmark is required.
- Use dry-run release-gate tests for command selection.
- Final `bash scripts/release-verify.sh v0.1.1` may prioritize correctness over speed.

## Manual QA checklist

- Read `docs/releases/v0.1.1/release-notes.md` for source-boundary clarity.
- Read `dist/adapters/README.md` for version-specific repository-tree install guidance.
- Confirm no public text says `.codex/skills/` is a public adapter source or required release evidence.
- Confirm no public text says downloadable archives are required for `v0.1.1`.

## What not to test

- Do not test actual GitHub release publication, tagging, or upload behavior; release publication is out of scope.
- Do not require live Codex, Claude Code, or opencode execution from ordinary contributors.
- Do not test removal of tracked public adapter skill copies; that is a later migration.
- Do not test downloadable adapter archive publication as required `v0.1.1` behavior.
- Do not test skill wording or behavior changes because this slice must not change shipped skill behavior.

## Uncovered gaps

None.

## Next artifacts

```text
implement
code-review
explain-change
verify
pr
release notes
```

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for M1 implementation. Implementation may start with the reviewed plan and this test spec.
