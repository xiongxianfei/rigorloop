# Multi-Agent Adapters and First Public Release Test Spec

## Status
- active

## Related spec and plan

- Spec: `specs/multi-agent-adapters-first-public-release.md`
- Plan: `docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`
- Proposal: `docs/proposals/2026-04-24-multi-agent-adapters-first-public-release.md`
- Architecture: `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md`
- ADR: `docs/adr/ADR-20260424-generated-adapter-packages.md`
- Spec-review findings: resolved in the approved spec. RC release gates, smoke row states, placeholder release-check rejection, and required release-check invocations are now explicit.
- Plan-review findings: approved on 2026-04-24 with no required plan edits.

## Testing strategy

- Unit tests exercise adapter configuration, constrained YAML helpers, portable-core validation, manifest records, release metadata parsing, security pattern checks, and release-gate decisions.
- Integration tests use filesystem fixtures and generated temporary trees to prove adapter generation, drift checks, adapter validation, release metadata validation, release verification, CI wiring, and generated-source boundaries.
- Contract tests inspect public docs, release notes, instruction entrypoints, and release scripts for required claims, source-of-truth wording, supported tools, and placeholder rejection.
- Manual smoke verifies real Codex, Claude Code, and opencode discovery behavior only after generated package structure and non-smoke release gates pass.
- Existing `scripts/build-skills.py --check` remains the proof for `.codex/skills/`; new adapter checks do not replace it.
- Tests must run with the Python standard library and repository files only. Non-smoke validation must not require network access, secrets, or installed agent tools.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`, `R7`, `R8` | `T1`, `T10`, `T19` | Canonical source and generated-output ownership boundaries. |
| `R2`-`R5`, `R14`, `R15` | `T1`, `T5`, `T6`, `T20` | Exact adapter set, package paths, and required entrypoints. |
| `R6`, `R35` | `T7`, `T8` | Deterministic rendering and manifest ordering. |
| `R9` | `T7`, `T9`, `T18` | Missing, stale, and unexpected generated output fails validation. |
| `R10` | `T6`, `T20` | Package roots are independently copyable and smokeable. |
| `R11`-`R13` | `T5`, `T12` | Thin templates, no duplicated skill bodies, generated-output notices. |
| `R16`-`R20`, `R28` | `T2`, `T3`, `T4`, `T9` | Portable-core structure, metadata, unsupported frontmatter, exclusion, and transform behavior. |
| `R21`-`R25` | `T3` | Codex-only invocation, config, install-location, tool/UI/approval/runtime, and `$skill` assumptions. |
| `R26`, `R27` | `T4`, `T8` | Generic artifact paths stay portable; Codex-valid non-portable skills can ship only with manifest reasons. |
| `R29`, `R29a`, `R29b` | `T8`, `T13`, `T15` | Manifest version for RC and stable package sets. |
| `R30`-`R34` | `T8`, `T9` | Manifest shape and generated tree consistency. |
| `R36`-`R38` | `T12`, `T16` | Public support matrix, canonical-versus-generated docs, and contributor-local expectations. |
| `R39`-`R42a` | `T13` | Required release metadata surface, fields, smoke rows, and validation rows. |
| `R43`-`R43f` | `T14`, `T17` | RC release gates, allowed incomplete smoke, and known smoke failure rejection. |
| `R44`-`R44d` | `T15`, `T20` | Stable release gates and passing smoke matrix. |
| `R45` | `T14`, `T15`, `T17` | Release maturity matches `v0.1.0-rc.1` or `v0.1.0`. |
| `R46`, `R46a`, `R47` | `T16`, `T17` | Placeholder release-check rejection, required check invocations, release notes and exclusion coverage. |
| `R48` | `T18` | CI includes adapter generation, portability, manifest, and drift validation. |
| `R49`, `R50` | `T19` | Existing `.codex/skills/` remains separate generated local mirror. |
| `R51` | `T12`, `T18` | No hosted runtime, marketplace, plugin registry, or orchestration service. |
| `R52` | `T11`, `T13`, `T17`, `T18` | Generation, validation, and release checks do not require secrets or network access. |
| `R53` | `T5`, `T11` | Generated packages do not broaden tool permissions by default. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T6`, `T7`, `T8` | Generated package roots and manifest exist with deterministic contents. |
| `E2` | `T2`, `T4`, `T6`, `T8` | Portable workflow skill appears in every adapter and manifest marks it portable. |
| `E3` | `T3`, `T4`, `T8` | Codex-only skill is excluded from non-Codex adapters and records a reason. |
| `E4` | `T5`, `T6`, `T20` | Claude Code package includes `CLAUDE.md` and `.claude/skills/` without body duplication. |
| `E5` | `T5`, `T6`, `T20` | opencode package includes `AGENTS.md` and `.opencode/skills/`. |
| `E6` | `T14`, `T17` | RC may pass before full smoke only when non-smoke gates pass. |
| `E7` | `T15`, `T20` | Stable release requires validation, notes, and passing smoke. |
| `E8` | `T14` | RC fails on any known smoke failure. |

## Edge case coverage

- Edge case 1, Codex-specific `argument-hint` frontmatter: `T3`, `T4`, `T9`
- Edge case 2, `.codex/skills` as only install location: `T3`
- Edge case 3, `$proposal` or other required Codex-only invocation syntax: `T3`
- Edge case 4, generic `docs/` and `specs/` artifact paths: `T4`
- Edge case 5, copied adapter package without siblings: `T6`, `T20`
- Edge case 6, release before all tool smoke checks pass: `T14`
- Edge case 7, stable release before manual smoke evidence exists: `T15`
- Edge case 8, official tool docs change after implementation: `T12`, `T20`
- Edge case 9, skill portable for only some adapters: `T4`, `T8`, `T9`
- Edge case 10, `.codex/skills/` drifts while `dist/adapters/codex/` is in sync: `T19`
- Edge case 11, RC metadata records `result: fail`: `T14`
- Edge case 12, RC `not-run` row without owner: `T14`
- Edge case 13, stable metadata records `result: blocked`: `T15`

## Test cases

### T1. Adapter model defines exact supported tools and package paths
- Covers: `R1`, `R2`, `R3`, `R4`, `R5`, `R7`, `R8`, `R14`, `R15`
- Level: unit
- Fixture/setup:
  - `scripts/adapter_distribution.py`
- Steps:
  - Load the adapter model.
  - Assert the supported adapters are exactly `codex`, `claude`, and `opencode`.
  - Assert each adapter root, instruction entrypoint, and skill path matches the spec.
  - Assert source roots are canonical `skills/` plus authored templates, not generated package paths.
- Expected result:
  - The adapter model exposes only the approved tools and paths.
- Failure proves:
  - Generator and validator logic can drift from the approved public package contract.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T2. Portable-core metadata validation accepts only portable skill shape
- Covers: `R16`, `R17`, `R18`, `R19`, `R31a`, `E2`
- Level: unit
- Fixture/setup:
  - `tests/fixtures/adapters/portable-basic/`
  - `tests/fixtures/adapters/invalid-name/`
  - `tests/fixtures/adapters/invalid-description/`
- Steps:
  - Validate a portable skill with YAML frontmatter and Markdown body.
  - Validate invalid skill names for uppercase, underscores, leading or trailing hyphen, consecutive hyphens, over 64 characters, and directory mismatch.
  - Validate missing, empty, target-specific, and over-1024-character descriptions.
- Expected result:
  - Portable fixtures pass; invalid metadata fixtures fail with skill name, adapter, path, and failed rule.
- Failure proves:
  - Non-portable or invalid skill metadata can leak into adapter packages.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T3. Portable-core validation rejects Codex-only assumptions
- Covers: `R20`, `R21`, `R22`, `R23`, `R24`, `R25`, `E3`
- Level: unit
- Fixture/setup:
  - `tests/fixtures/adapters/unsupported-frontmatter/`
  - `tests/fixtures/adapters/codex-invocation/`
  - `tests/fixtures/adapters/agents-openai/`
  - `tests/fixtures/adapters/codex-install-only/`
  - `tests/fixtures/adapters/codex-tool-assumption/`
  - `tests/fixtures/adapters/codex-dollar-skill/`
- Steps:
  - Run portable-core validation for Claude Code and opencode targets.
  - Verify unsupported non-Codex metadata is rejected or explicitly transformed.
  - Verify Codex-only invocation syntax, `agents/openai.yaml`, `.codex/skills`-only install guidance, Codex-only tools/UI/approval/runtime assumptions, and `$skill` dependencies fail non-Codex portability.
- Expected result:
  - Each non-portable fixture is excluded or transformed only through an explicitly asserted rule and human-readable reason.
- Failure proves:
  - Adapter packages can ship skills that depend on Codex-only behavior.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T4. Adapter inclusion decisions preserve generic workflow skills and explain exclusions
- Covers: `R26`, `R27`, `R28`, `R31a`, `R32`, `E2`, `E3`
- Level: unit
- Fixture/setup:
  - `tests/fixtures/adapters/generic-artifact-paths/`
  - `tests/fixtures/adapters/partial-portability/`
  - `tests/fixtures/adapters/transformable-frontmatter/`
- Steps:
  - Validate a skill that references generic `docs/` and `specs/` paths.
  - Validate a skill portable to Codex and Claude Code but not opencode.
  - Validate a skill whose unsupported frontmatter is explicitly transformed for non-Codex adapters.
  - Inspect the generated inclusion decisions and reasons.
- Expected result:
  - Generic RigorLoop artifact paths stay portable; partial portability records the exact adapter list and reason; transforms are explicit and tested.
- Failure proves:
  - The portable-core gate is either too strict for generic RigorLoop content or too vague for exclusions.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T5. Thin instruction entrypoint templates render without duplicating skill bodies
- Covers: `R11`, `R12`, `R13`, `R14`, `R15`, `R53`, `E4`, `E5`
- Level: integration
- Fixture/setup:
  - `scripts/adapter_templates/codex/AGENTS.md`
  - `scripts/adapter_templates/claude/CLAUDE.md`
  - `scripts/adapter_templates/opencode/AGENTS.md`
  - generated `dist/adapters/*` entrypoints
- Steps:
  - Generate adapters for `0.1.0-rc.1`.
  - Assert each generated entrypoint exists at the required package path.
  - Assert entrypoints identify generated adapter output and point maintainers to canonical sources.
  - Assert generated entrypoints do not include full skill body sections from generated `SKILL.md` files.
  - Assert entrypoints do not include default permission-bypass configuration.
- Expected result:
  - Each tool has a thin generated entrypoint with no duplicated skill bodies and no default permission broadening.
- Failure proves:
  - Entry points are drifting into another authored workflow body or unsafe tool config surface.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`

### T6. Adapter generation creates independently installable package roots
- Covers: `R2`, `R3`, `R4`, `R5`, `R10`, `R14`, `R15`, `E1`, `E4`, `E5`
- Level: integration
- Fixture/setup:
  - canonical `skills/`
  - `scripts/adapter_templates/`
  - temporary generated output root
- Steps:
  - Run `python scripts/build-adapters.py --version 0.1.0-rc.1`.
  - Assert `dist/adapters/codex/`, `dist/adapters/claude/`, and `dist/adapters/opencode/` exist.
  - Copy each adapter package root into an empty temporary project directory without siblings.
  - Assert each copied project contains its required entrypoint and target skill tree.
- Expected result:
  - Every adapter package can stand alone when copied into a project root.
- Failure proves:
  - The generated package layout does not satisfy independent installability.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.0-rc.1`

### T7. Adapter generation is deterministic and drift-checked
- Covers: `R6`, `R9`, `R35`, `E1`
- Level: integration
- Fixture/setup:
  - generated `dist/adapters/`
  - temporary modified generated file
  - temporary unexpected generated file
- Steps:
  - Run generation twice for the same version and inputs.
  - Compare generated file bytes or expected file maps.
  - Modify one generated file and run `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`.
  - Add one unexpected generated file and run check mode again.
- Expected result:
  - Same inputs produce identical output; stale or unexpected generated files fail check mode with paths.
- Failure proves:
  - Generated adapter output cannot be trusted as tracked release material.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`

### T8. Generated manifest matches version, skill records, and generated files
- Covers: `R27`, `R29`, `R29a`, `R29b`, `R30`, `R31`, `R31a`, `R32`, `R33`, `R34`, `R35`, `E1`, `E2`, `E3`
- Level: integration
- Fixture/setup:
  - `dist/adapters/manifest.yaml`
  - generated adapter package roots
- Steps:
  - Generate RC packages and inspect `dist/adapters/manifest.yaml`.
  - Assert RC manifest version is `0.1.0-rc.1`.
  - Generate stable packages in an isolated output and assert manifest version is `0.1.0`.
  - Assert every manifest skill entry has `portable` and `adapters`.
  - Assert every non-portable entry has a human-readable `reason`.
  - Assert each listed adapter contains the generated skill path and no generated skill is omitted from the manifest.
- Expected result:
  - Manifest version, portability, adapter lists, reasons, and generated files are internally consistent.
- Failure proves:
  - The generated support matrix cannot be used as release evidence.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.0-rc.1`

### T9. Adapter validation rejects structural and metadata violations
- Covers: `R9`, `R16`-`R20`, `R28`, `R30`-`R34`
- Level: integration
- Fixture/setup:
  - generated package fixtures with missing adapter directory
  - missing instruction entrypoint fixture
  - manifest/file mismatch fixture
  - generated skill with unsupported target metadata fixture
- Steps:
  - Run `python scripts/validate-adapters.py --version 0.1.0-rc.1` against valid generated output.
  - Run adapter validation against each invalid fixture.
  - Inspect failure messages for adapter name, skill name, and path where applicable.
- Expected result:
  - Valid generated output passes; each invalid fixture fails on the named rule.
- Failure proves:
  - Release gates may pass with missing packages, missing entrypoints, or invalid target metadata.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.0-rc.1`

### T10. Generated adapter paths are not treated as authored lifecycle sources
- Covers: `R7`, `R8`, `R37`, `R48`
- Level: integration
- Fixture/setup:
  - generated `dist/adapters/*`
  - `scripts/ci.sh`
  - `scripts/validate-artifact-lifecycle.py`
- Steps:
  - Include generated adapter paths in a simulated changed-file set.
  - Run the same artifact lifecycle scope logic used by `scripts/ci.sh`.
  - Assert generated `dist/adapters/*` paths are filtered from authored artifact lifecycle validation.
  - Assert adapter drift and adapter validation still check those generated files.
- Expected result:
  - Generated adapter files are validated as generated output, not as authored lifecycle artifacts.
- Failure proves:
  - CI can either reject generated files for the wrong reason or let generated drift bypass checks.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh`

### T11. Security and privacy checks reject secrets, machine-local paths, and permission bypasses
- Covers: `R51`, `R52`, `R53`
- Level: integration
- Fixture/setup:
  - generated adapter files
  - adapter templates
  - release metadata and release notes fixtures
  - invalid fixtures containing secret markers, private key delimiters, absolute machine-local paths, and permission-bypass language
- Steps:
  - Run adapter validation and release validation against clean generated output.
  - Run validation against each security fixture.
  - Confirm validation runs without network access or secrets.
- Expected result:
  - Clean files pass; secret, private key, machine-local path, and permission-bypass fixtures fail.
- Failure proves:
  - Generated packages or release artifacts can leak sensitive or unsafe operational instructions.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.0-rc.1`
  - `python scripts/validate-release.py --version v0.1.0-rc.1`

### T12. Public documentation describes support matrix and generated ownership accurately
- Covers: `R36`, `R37`, `R38`, `R51`
- Level: contract
- Fixture/setup:
  - `README.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - release notes under `docs/releases/<version>/release-notes.md`
  - `dist/adapters/manifest.yaml`
- Steps:
  - Inspect public docs for Codex, Claude Code, and opencode support.
  - Confirm docs distinguish `skills/`, `.codex/skills/`, and `dist/adapters/`.
  - Confirm docs state ordinary contributors do not need all supported tools installed locally.
  - Confirm docs do not claim hosted runtime, marketplace, plugin registry, package-manager distribution, or identical behavior across tools.
  - Confirm docs say adapter claims are versioned and must be revised through lifecycle if external tool contracts change.
- Expected result:
  - Public docs match the generated support matrix and the approved source-of-truth boundary.
- Failure proves:
  - The project can overstate compatibility or mislead contributors about generated files.
- Automation location:
  - focused `rg` checks from the plan
  - manual review during M5

### T13. Release metadata shape validates for one target version
- Covers: `R39`, `R40`, `R40a`, `R40b`, `R40c`, `R40d`, `R40e`, `R40f`, `R41`, `R41a`, `R41b`, `R41c`, `R41d`, `R41e`, `R41f`, `R42`, `R42a`
- Level: integration
- Fixture/setup:
  - `docs/releases/v0.1.0-rc.1/release.yaml`
  - `docs/releases/v0.1.0-rc.1/release-notes.md`
  - valid and invalid release metadata fixtures
- Steps:
  - Run `python scripts/validate-release.py --version v0.1.0-rc.1`.
  - Assert the validator reads the exact versioned release metadata and release notes paths.
  - Assert required fields and smoke rows are present for exactly `codex`, `claude`, and `opencode`.
  - Assert validation rows include at least `generated_sync`, `release_notes_consistency`, `placeholder_release_check`, and `security`.
  - Run invalid-shape fixtures and assert failures name the missing or invalid field.
- Expected result:
  - One target version's release metadata validates exactly against the approved schema.
- Failure proves:
  - Release evidence can be missing, unversioned, or structurally ambiguous.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.0-rc.1`

### T14. RC release gates allow incomplete smoke only under approved conditions
- Covers: `R43`, `R43a`, `R43b`, `R43c`, `R43d`, `R43e`, `R43f`, `R45`, `E6`, `E8`
- Level: integration
- Fixture/setup:
  - valid RC metadata with `not-run` smoke rows and owner/reason
  - invalid RC metadata with smoke `fail`
  - invalid RC metadata with `not-run` missing owner
  - invalid RC metadata with `blocked` reason that is not external or tool-access related
- Steps:
  - Run release validation for the valid RC fixture.
  - Run release validation for each invalid RC fixture.
  - Run release verification for `v0.1.0-rc.1` after non-smoke gates pass.
- Expected result:
  - Valid incomplete RC smoke passes; any known failure or incomplete row without reason and owner fails.
- Failure proves:
  - RC publication can either be blocked too strictly or allowed with known incompatible smoke results.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.0-rc.1`
  - `bash scripts/release-verify.sh v0.1.0-rc.1`

### T15. Stable release gates require all smoke rows to pass
- Covers: `R29b`, `R44`, `R44a`, `R44b`, `R44c`, `R44d`, `R45`, `E7`
- Level: integration and manual
- Fixture/setup:
  - `docs/releases/v0.1.0/release.yaml`
  - `docs/releases/v0.1.0/release-notes.md`
  - final metadata fixtures with `pass`, `not-run`, `blocked`, and `fail` smoke rows
- Steps:
  - Run final release validation with all smoke rows `pass` and non-empty tool version/evidence.
  - Run final release validation with any `not-run`, `blocked`, or `fail` row.
  - Run `bash scripts/release-verify.sh v0.1.0` only after manual smoke evidence is recorded.
- Expected result:
  - Final metadata passes only when every supported tool smoke row is `pass` and release notes match the support matrix.
- Failure proves:
  - Stable release can be published before smoke-verified compatibility exists.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.0`
  - `bash scripts/release-verify.sh v0.1.0`

### T16. Release notes and placeholder release checks are enforced
- Covers: `R36`, `R43b`, `R46`, `R46a`, `R47`
- Level: integration
- Fixture/setup:
  - `scripts/release-verify.sh`
  - release notes fixtures
  - `docs/releases/<version>/release-notes.md`
- Steps:
  - Assert release notes version is exactly the target tag.
  - Assert release notes, manifest, release metadata, and generated paths list the same supported tools.
  - Assert release notes or release metadata describe generated adapter packages and non-portable exclusions.
  - Assert release verification fails if release-check scripts contain `Replace this script with repository-specific release checks`, `TODO: release checks`, or `placeholder release check`.
  - Assert release verification fails if no repository-specific release check invokes each required validation command category.
- Expected result:
  - Release notes are version-consistent, support-matrix-consistent, and the release gate is not a placeholder.
- Failure proves:
  - Public release claims can diverge from generated packages or run through a non-authoritative checklist.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.0-rc.1`
  - `bash scripts/release-verify.sh v0.1.0-rc.1`

### T17. Release verification orchestrates required checks and GitHub release uses tracked notes
- Covers: `R43b`, `R45`, `R46a`, `R47`, `R52`
- Level: integration
- Fixture/setup:
  - `scripts/release-verify.sh`
  - `.github/workflows/release.yml`
  - generated adapters
  - release metadata and notes
- Steps:
  - Run `bash scripts/release-verify.sh v0.1.0-rc.1`.
  - Inspect command output or a shell-test harness to confirm it invokes skill validation, skill regression validation, `.codex/skills` drift check, adapter regression tests, adapter generation drift check, adapter validation, release metadata validation, and security checks.
  - Run without an argument in a controlled environment with `GITHUB_REF_NAME=v0.1.0-rc.1`.
  - Inspect `.github/workflows/release.yml` to confirm GitHub release creation uses `docs/releases/<tag>/release-notes.md` rather than generated notes.
- Expected result:
  - Release verification is a concrete repository-owned gate, and hosted release publication consumes tracked notes.
- Failure proves:
  - The tag workflow can publish from stale or unverifiable release evidence.
- Automation location:
  - `bash scripts/release-verify.sh v0.1.0-rc.1`
  - shell-focused assertions in `scripts/test-adapter-distribution.py` or a later shell test helper if added

### T18. CI runs adapter non-smoke validation without requiring agent tools
- Covers: `R38`, `R48`, `R51`, `R52`
- Level: smoke
- Fixture/setup:
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml`
  - generated adapter packages
- Steps:
  - Run `bash scripts/ci.sh` in a local environment without Codex, Claude Code, or opencode installed.
  - Inspect output to confirm CI runs adapter regression tests, `build-adapters.py --check`, and `validate-adapters.py`.
  - Confirm CI still runs existing skill validation, skill regression validation, `.codex/skills` drift, change metadata fixtures, and artifact lifecycle fixtures.
- Expected result:
  - Non-smoke CI passes without network access, secrets, or installed agent tools.
- Failure proves:
  - Ordinary contributors cannot validate supported adapter package structure locally.
- Automation location:
  - `bash scripts/ci.sh`

### T19. `.codex/skills/` remains a separate generated local mirror
- Covers: `R49`, `R50`
- Level: integration
- Fixture/setup:
  - `skills/`
  - `.codex/skills/`
  - `dist/adapters/codex/`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
- Steps:
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`.
  - Modify `.codex/skills/` in a temporary test context and assert only `build-skills.py --check` detects that mirror drift.
  - Modify `dist/adapters/codex/` in a temporary test context and assert adapter drift detects that package drift.
  - Assert neither generated surface is used as source for the other.
- Expected result:
  - Both generated surfaces derive from `skills/` through separate explicit check paths.
- Failure proves:
  - The repository can accidentally make generated output the source for another generated output.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.0-rc.1 --check`

### T20. Maintainer smoke verifies tool discovery for each adapter package
- Covers: `R10`, `R41c`, `R44`, `R44b`, `R44c`, `E4`, `E5`, `E7`
- Level: manual smoke
- Fixture/setup:
  - generated `dist/adapters/codex/`
  - generated `dist/adapters/claude/`
  - generated `dist/adapters/opencode/`
  - clean temporary project roots
  - maintainer-accessible Codex, Claude Code, and opencode environments
- Steps:
  - Copy `dist/adapters/codex/` into a clean project root and verify `AGENTS.md` plus `.agents/skills/<skill>/SKILL.md` are discoverable by Codex.
  - Copy `dist/adapters/claude/` into a clean project root and verify `CLAUDE.md` plus `.claude/skills/<skill>/SKILL.md` are discoverable by Claude Code.
  - Copy `dist/adapters/opencode/` into a clean project root and verify `AGENTS.md` plus `.opencode/skills/<skill>/SKILL.md` are discoverable by opencode.
  - Record tool version and evidence in the corresponding release metadata smoke row.
- Expected result:
  - Every supported tool has a `pass` smoke row with non-empty tool version and evidence before stable `v0.1.0`.
- Failure proves:
  - The stable release claim is not smoke-verified.
- Automation location:
  - Manual maintainer smoke matrix recorded in `docs/releases/v0.1.0/release.yaml`

### T21. Command output is observable and validation remains practical
- Covers: observability requirements, performance expectations, `R48`
- Level: integration
- Fixture/setup:
  - adapter generation and validation commands
  - release validation command
  - CI wrapper
- Steps:
  - Run adapter generation, adapter validation, release validation, and release verification commands.
  - Inspect output for release version, adapter package paths, included/excluded skill counts, manifest path/version, release metadata path, named release gate failures, and smoke row failures.
  - Run commands over the full repository skill set and confirm they complete without invoking supported agent tools.
- Expected result:
  - Commands produce actionable failure messages and remain practical for ordinary local use.
- Failure proves:
  - Failures will be difficult to debug, or validation is too expensive or tool-dependent for contributors.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh`

## Fixtures and data

- Add adapter fixtures under `tests/fixtures/adapters/`.
- Use minimal `SKILL.md` fixture trees for portable, invalid, Codex-only, generic, partial-portability, transformable, and security cases.
- Use generated-output fixtures or temporary directories for missing entrypoints, missing adapter roots, manifest/file mismatches, stale generated files, and unexpected generated files.
- Use release fixtures for valid RC metadata, valid final metadata, invalid smoke results, missing owner/reason, mismatched versions, mismatched tools, placeholder release checks, and unsupported validation values.
- Use temporary project roots for independent-installability checks.
- Real `docs/releases/v0.1.0-rc.1/` and `docs/releases/v0.1.0/` files are release evidence, not generic fixtures. Tests may create separate fixture copies for negative cases.

## Mocking/stubbing policy

- Do not mock filesystem layout, generated files, manifests, release metadata, or CLI command invocation boundaries. Those are the core integration risks.
- Do not mock `skills/` and generated adapter path relationships; use real temporary directories or repository paths.
- Do not invoke or stub Codex, Claude Code, or opencode in ordinary automated tests. Manual smoke owns real tool discovery.
- Shell command orchestration may be tested through a controlled environment and temporary fixture commands only if the test still proves the real `scripts/release-verify.sh` invokes the required repository-owned check categories.
- Network, secrets, hosted CI status, and external account access must not be required for automated tests.

## Migration or compatibility tests

- `T10` verifies generated `dist/adapters/*` paths are not treated as authored lifecycle-managed sources.
- `T19` verifies `.codex/skills/` remains a separate generated local Codex mirror and is not sourced from `dist/adapters/codex/`.
- `T12` verifies documentation distinguishes repository-local `.codex/skills/` from public `dist/adapters/codex/`.
- `T14` and `T15` verify RC and final release metadata use different smoke strictness.
- `T13`, `T14`, and `T15` verify release validation is target-version scoped.

## Observability verification

- `T2`, `T3`, `T9`, `T13`, `T14`, `T15`, `T16`, and `T21` require failures to name the relevant skill, adapter, path, version, release gate, or smoke row.
- `T21` verifies command output includes the release version, adapter paths, included/excluded skill counts, manifest path/version, release metadata path, and named release-gate failures.

## Security/privacy verification

- `T11` verifies generated adapter files, templates, release metadata, and release notes do not contain common secret markers, private key delimiters, machine-local paths, or default permission-bypass language.
- `T5` verifies generated instruction entrypoints do not add default permission-bypass configuration.
- `T13`, `T17`, and `T18` verify release and CI validation do not require network access, secrets, or installed agent tools for non-smoke gates.
- Manual smoke evidence in `docs/releases/<version>/release.yaml` must not include credentials, session tokens, or private tool logs.

## Performance checks

- `T21` is the performance sanity check. It runs generation and validation over the repository skill set and confirms validation remains practical without supported agent tools installed.
- No benchmark threshold is required for `v0.1.0-rc.1`. If performance becomes a material risk, a later spec update should define explicit thresholds.

## Manual QA checklist

- Run `T20` for Codex before stable `v0.1.0`.
- Run `T20` for Claude Code before stable `v0.1.0`.
- Run `T20` for opencode before stable `v0.1.0`.
- Record each passing smoke row with non-empty `tool_version` and `evidence`.
- If any row fails, do not publish stable `v0.1.0`.
- If any row is externally blocked, stable `v0.1.0` remains blocked; RC metadata may record the blocker only when there is no known smoke failure and the row includes reason and owner.

## What not to test

- Do not automate real Codex, Claude Code, or opencode sessions in ordinary CI; maintainer smoke owns real tool behavior.
- Do not test marketplace, package-manager, plugin-registry, hosted orchestration, or installer flows because they are non-goals.
- Do not test identical runtime behavior across tools because the spec explicitly does not guarantee it.
- Do not require every existing skill to become portable; test exclusion reasons and manifest consistency instead.
- Do not test third-party YAML libraries; the architecture requires repository-owned constrained parsing or existing parsing style.
- Do not treat generated adapter package contents as authored lifecycle artifacts; test generated drift and adapter validation instead.

## Uncovered gaps

- None that block implementation.

The only intentionally manual gap is real tool discovery smoke for Codex, Claude Code, and opencode. That gap is covered by the required maintainer smoke matrix before stable `v0.1.0`.

## Next artifacts

- `implement` for M1 in `docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`.
- Change-local artifacts under `docs/changes/<change-id>/` during implementation.

## Follow-on artifacts

None yet.

## Readiness

This active test spec is the current proof-planning surface for `specs/multi-agent-adapters-first-public-release.md` and `docs/plans/2026-04-24-multi-agent-adapters-first-public-release.md`.

Immediate next repository stage: `implement`.
