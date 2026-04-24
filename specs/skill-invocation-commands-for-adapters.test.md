# Skill Invocation Commands for Adapter Packages Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/skill-invocation-commands-for-adapters.md`
- Plan: `docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`
- Proposal: `docs/proposals/2026-04-24-skill-invocation-commands-for-adapters.md`
- Architecture: `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md`
- Existing adapter architecture: `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md`
- Existing adapter ADR: `docs/adr/ADR-20260424-generated-adapter-packages.md`
- Spec-review findings: resolved in the approved spec. The contract now distinguishes OpenCode command aliases from canonical skills, requires exact manifest paths, and gates one-shot examples on smoke evidence.
- Plan-review findings: resolved in the active plan on 2026-04-24. `docs/releases/v0.1.1/release-notes.md` is owned by M3, and M2 is limited to README plus adapter entrypoint documentation with no one-shot examples before M3 smoke evidence.

## Testing strategy

- Unit tests exercise the curated alias constant, deterministic command rendering, constrained manifest parsing, command alias path validation, release target registry, release metadata validation, and security pattern checks.
- Integration tests use temporary adapter output trees and generated `dist/adapters/` checks to prove exact command files, manifest entries, entrypoint docs, README examples, drift behavior, and generated package validation.
- Contract tests inspect public docs, generated entrypoints, release notes, release metadata, and release scripts for tool-specific invocation claims and smoke-gated one-shot examples.
- Release tests validate `v0.1.1` as a final patch release with adapter manifest version `0.1.1`, OpenCode command alias smoke evidence, and release notes consistency.
- Manual smoke is limited to real OpenCode command alias invocation and any additional tool-specific one-shot forms documented for the release.
- Non-smoke tests must run with repository files, Python standard library code, and shell scripts only. They must not require installed Claude Code, installed OpenCode, network access, secrets, or hosted CI.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`, `R2`, `R45` | `T1`, `T2`, `T17` | Canonical skills remain the source of truth and aliases stay patch-level wrappers. |
| `R3`, `R4`, `R5`, `R6` | `T1`, `T7` | OpenCode keeps portable skills while aliases are limited to the curated lifecycle set and never dangle. |
| `R7`, `R8` | `T1`, `T3`, `T5` | Alias paths and filename stems match the approved package layout. |
| `R9`, `R10`, `R11`, `R12`, `R13`, `R14` | `T2`, `T6`, `T14` | Alias body structure, `$ARGUMENTS`, determinism, no duplicated skill bodies, and unsafe content rejection. |
| `R15` | `T4`, `T6`, `T16` | Drift checks fail on missing, stale, or hand-edited command alias output. |
| `R16`, `R17`, `R18` | `T4`, `T5`, `T7` | Adapter validation rejects unexpected, dangling, and non-curated aliases. |
| `R19`, `R20`, `R21`, `R22` | `T3`, `T16` | Manifest records exact command alias paths and internally consistent counts. |
| `R23`, `R24`, `R25`, `R26`, `R27` | `T4`, `T5` | Manifest-declared aliases, undeclared files, constrained paths, key/stem matching, and unsupported tool sections. |
| `R28`, `R29`, `R30` | `T9`, `T11`, `T13` | Claude Code stays skill-native and avoids unsmoked one-shot claims. |
| `R31`, `R32`, `R33`, `R34` | `T10`, `T11`, `T13` | OpenCode entrypoint explains skills, thin aliases, TUI examples, and smoke-gated one-shot examples. |
| `R35`, `R36`, `R37`, `R38`, `R39` | `T11`, `T13` | README examples distinguish Claude and OpenCode forms and avoid unsupported syntax or alias claims. |
| `R40`, `R40a`, `R41`, `R41a`, `R42`, `R43`, `R44`, `R48` | `T12`, `T13`, `T16` | Release metadata, smoke evidence, release notes, one-shot claims, and `v0.1.1` release verification. |
| `R46` | `T8`, `T16` | Repository-owned non-smoke validation does not invoke Claude Code or OpenCode. |
| `R47` | `T4`, `T5`, `T6` | Command alias failures identify tool slug, alias name, and path when available. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T1`, `T7`, `T16` | OpenCode generates exactly the curated aliases and excludes non-curated skills. |
| `E2` | `T7` | Portable skills remain under `.opencode/skills/` even when only curated skills get aliases. |
| `E3` | `T2` | Alias files are thin wrappers and do not duplicate canonical skill bodies. |
| `E4` | `T3` | Manifest records exact command alias paths. |
| `E5` | `T4`, `T5` | Unexpected aliases such as `verify.md` fail validation. |
| `E6` | `T4`, `T6` | Missing or stale manifest-declared aliases fail validation or drift checks. |
| `E7` | `T9` | Claude Code entrypoint uses native slash-skill examples and no `.claude/commands/`. |
| `E8` | `T11`, `T13` | README separates TUI examples from smoke-gated one-shot examples. |

## Edge case coverage

- `EC1`: `T1`, `T7`
- `EC2`: `T1`, `T4`, `T7`
- `EC3`: `T6`
- `EC4`: `T4`, `T5`
- `EC5`: `T5`
- `EC6`: `T11`, `T13`
- `EC7`: `T11`, `T13`
- `EC8`: `T2`, `T14`
- `EC9`: `T5`
- `EC10`: `T2`, `T14`

## Test cases

### T1. OpenCode generation creates exactly the curated command alias set

- Covers: `R1`, `R2`, `R4`, `R5`, `R6`, `R7`, `R8`, `R14`, `R45`, `E1`, `EC1`, `EC2`
- Level: integration
- Fixture/setup:
  - canonical `skills/`
  - `scripts/adapter_distribution.py`
  - temporary generated adapter output root
- Steps:
  - Generate adapters for version `0.1.1`.
  - Collect files under `dist/adapters/opencode/.opencode/commands/`.
  - Assert the filenames are exactly `proposal.md`, `proposal-review.md`, `spec.md`, `spec-review.md`, `plan.md`, `plan-review.md`, `test-spec.md`, `implement.md`, `code-review.md`, and `pr.md`.
  - Assert no alias is generated for `workflow`, `verify`, `explore`, or any portable skill outside the curated lifecycle command set.
  - Assert generation fails or validation fails if a curated skill is not included in the OpenCode adapter package.
- Expected result:
  - OpenCode command aliases are generated only for the approved curated set and only when the matching OpenCode skill exists.
- Failure proves:
  - The generated package can overexpose aliases, create dangling aliases, or turn aliases into an unbounded behavior surface.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1`

### T2. OpenCode command alias bodies are deterministic thin wrappers

- Covers: `R1`, `R2`, `R9`, `R10`, `R11`, `R12`, `R13`, `R14`, `R45`, `E3`, `EC8`, `EC10`
- Level: unit, integration
- Fixture/setup:
  - generated OpenCode command aliases
  - matching canonical `skills/<skill-name>/SKILL.md` files
  - malicious or stale alias body fixtures
- Steps:
  - Render the command alias for each curated skill.
  - Assert each file has YAML frontmatter with a `description` field.
  - Assert the body instructs OpenCode to load and follow the matching RigorLoop skill.
  - Assert the body passes user input only through `$ARGUMENTS`.
  - Assert the body equals the deterministic renderer output for the same inputs.
  - Assert the body does not include the full matching `SKILL.md` content.
  - Assert bodies containing shell interpolation, file interpolation, model overrides, agent overrides, or permission settings fail validation.
- Expected result:
  - Each alias is a small deterministic prompt wrapper, not an authored skill copy or policy surface.
- Failure proves:
  - Command aliases can drift into a second source of truth or unsafe tool configuration.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T3. Manifest records exact OpenCode command alias paths and count

- Covers: `R7`, `R8`, `R19`, `R20`, `R21`, `R22`, `E4`
- Level: unit, integration
- Fixture/setup:
  - `dist/adapters/manifest.yaml`
  - constrained manifest parser and renderer in `scripts/adapter_distribution.py`
- Steps:
  - Generate adapters for version `0.1.1`.
  - Parse `dist/adapters/manifest.yaml`.
  - Assert `command_aliases.opencode.count` equals `10`.
  - Assert `command_aliases.opencode.aliases` maps every curated alias name to the exact repository-relative POSIX path under `dist/adapters/opencode/.opencode/commands/<skill-name>.md`.
  - Assert the parsed count equals the number of alias map entries.
- Expected result:
  - The manifest gives release validation an exact generated command alias map, not only a summary count.
- Failure proves:
  - The manifest cannot detect missing, extra, or misplaced alias output.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T4. Adapter validation rejects missing, unexpected, and dangling aliases

- Covers: `R15`, `R16`, `R17`, `R18`, `R23`, `R24`, `R47`, `E5`, `E6`, `EC2`, `EC4`
- Level: integration
- Fixture/setup:
  - valid generated adapter output
  - temporary copies with one declared alias removed
  - temporary copies with `dist/adapters/opencode/.opencode/commands/verify.md`
  - temporary copies with an alias whose matching OpenCode skill is missing
- Steps:
  - Run adapter validation against valid generated output.
  - Remove a manifest-declared alias file and rerun validation.
  - Add an undeclared alias file and rerun validation.
  - Add a non-curated alias file and rerun validation.
  - Remove a matching skill for a curated alias and rerun validation.
  - Inspect error text for `opencode`, the alias name, and the affected path when available.
- Expected result:
  - Valid output passes; each invalid tree fails on the specific alias consistency rule with actionable location detail.
- Failure proves:
  - Release gates can pass with missing, extra, or dangling command aliases.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T5. Manifest command alias validation rejects path, key, and unsupported-tool mismatches

- Covers: `R8`, `R18`, `R25`, `R26`, `R27`, `R47`, `E5`, `EC5`, `EC9`
- Level: unit, integration
- Fixture/setup:
  - manifest fixtures with invalid `command_aliases`
  - generated adapter output fixtures
- Steps:
  - Validate a manifest entry whose path is `.opencode/commands/proposal.md` instead of a repository-relative path.
  - Validate a manifest entry whose path points outside `dist/adapters/opencode/.opencode/commands/`.
  - Validate a manifest key such as `proposal-review` pointing to `plan-review.md`.
  - Validate a manifest that includes `command_aliases.claude` or any unsupported tool section.
  - Validate a manifest that declares a non-curated alias.
- Expected result:
  - Each malformed manifest fails with tool slug, alias name, and path when available.
- Failure proves:
  - The constrained manifest model is too loose to serve as release evidence.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T6. Adapter drift checking catches stale or hand-edited command alias output

- Covers: `R14`, `R15`, `R47`, `E6`, `EC3`
- Level: integration
- Fixture/setup:
  - generated `dist/adapters/`
  - temporary modified OpenCode command alias body
- Steps:
  - Generate adapters for version `0.1.1`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check` against clean output.
  - Modify `dist/adapters/opencode/.opencode/commands/proposal.md`.
  - Rerun check mode.
  - Inspect the failure for the modified path.
- Expected result:
  - Clean output passes; a hand-edited or stale alias fails check mode.
- Failure proves:
  - Tracked generated aliases can drift from canonical inputs without blocking release.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`

### T7. OpenCode keeps all included portable skills under `.opencode/skills/`

- Covers: `R3`, `R4`, `R5`, `R6`, `R16`, `R17`, `R18`, `E1`, `E2`, `EC1`, `EC2`
- Level: integration
- Fixture/setup:
  - canonical portable skills
  - generated OpenCode adapter package
  - manifest skill entries
- Steps:
  - Generate adapters for version `0.1.1`.
  - Assert every manifest skill entry that includes `opencode` has `dist/adapters/opencode/.opencode/skills/<skill-name>/SKILL.md`.
  - Assert command aliases are a subset of included OpenCode skills.
  - Assert included non-curated skills remain available as skills but do not have command aliases.
- Expected result:
  - Command aliases add a usability layer without reducing the reusable skill surface.
- Failure proves:
  - The alias feature changed portability behavior or hid non-aliased skills.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T8. Non-smoke validation does not require Claude Code or OpenCode installs

- Covers: `R46`
- Level: integration
- Fixture/setup:
  - repository-owned validation scripts
  - environment without Claude Code or OpenCode on `PATH`
- Steps:
  - Run non-smoke tests and validation scripts with no tool-specific binaries required.
  - Inspect adapter validation and release metadata validation code paths for subprocess calls to `claude`, `opencode`, or hosted services.
  - Confirm any real tool invocation appears only in manual smoke checklist or release evidence, not in non-smoke gates.
- Expected result:
  - Contributors can run non-smoke validation locally without installing Claude Code or OpenCode.
- Failure proves:
  - The repository has made ordinary contribution validation depend on external tools.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-release.py --version v0.1.1`

### T9. Claude Code adapter remains skill-native

- Covers: `R28`, `R29`, `R30`, `E7`, `EC7`
- Level: integration, contract
- Fixture/setup:
  - `scripts/adapter_templates/claude/CLAUDE.md`
  - generated `dist/adapters/claude/CLAUDE.md`
  - generated Claude adapter package
- Steps:
  - Generate adapters for version `0.1.1`.
  - Assert no `.claude/commands/` directory or command wrapper file exists in the Claude adapter package.
  - Assert `CLAUDE.md` documents native TUI slash-command examples such as `/proposal` and `/code-review`.
  - Assert `CLAUDE.md` does not claim a Claude one-shot form unless matching release smoke evidence exists.
- Expected result:
  - Claude Code usage stays skill-native and avoids duplicate command wrappers.
- Failure proves:
  - The package confuses Claude Code skills with generated command files or overclaims unsmoked usage forms.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`

### T10. OpenCode adapter entrypoint documents skills, thin aliases, and TUI examples

- Covers: `R31`, `R32`, `R33`, `R34`, `R38`, `R39`
- Level: integration, contract
- Fixture/setup:
  - `scripts/adapter_templates/opencode/AGENTS.md`
  - generated `dist/adapters/opencode/AGENTS.md`
  - release smoke metadata
- Steps:
  - Generate adapters for version `0.1.1`.
  - Assert OpenCode `AGENTS.md` states `.opencode/skills/` remains the reusable skill surface.
  - Assert OpenCode `AGENTS.md` states `.opencode/commands/` contains thin aliases only for the curated lifecycle command set.
  - Assert TUI slash-command examples include at least `/proposal`, `/spec`, `/implement`, `/code-review`, and `/pr`.
  - Assert docs do not imply aliases exist for non-curated skills.
  - Assert `opencode run --command ...` examples are absent unless release smoke records a passing one-shot command alias check.
  - Assert Codex `$skill` syntax is not presented as working in OpenCode.
- Expected result:
  - Users can identify OpenCode's reusable skill surface, curated command aliases, and supported TUI invocation form.
- Failure proves:
  - Generated entrypoint guidance can mislead users about where behavior lives or which syntax applies.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `rg -n '/proposal|/spec|/implement|/code-review|/pr|opencode run --command|\\.opencode/commands|\\.opencode/skills|\\$skill' scripts/adapter_templates dist/adapters`

### T11. README examples distinguish Claude and OpenCode invocation forms

- Covers: `R34`, `R35`, `R36`, `R37`, `R38`, `R39`, `R42`, `R43`, `E8`, `EC6`, `EC7`
- Level: contract
- Fixture/setup:
  - `README.md`
  - release metadata and notes when one-shot examples are present
- Steps:
  - Inspect README adapter usage examples.
  - Assert Claude Code examples use native TUI slash-skill forms unless a Claude one-shot form is smoke-tested.
  - Assert OpenCode examples include TUI slash-command aliases for the curated lifecycle command set.
  - Assert README distinguishes Claude native skills from OpenCode generated aliases.
  - Assert README does not claim aliases for non-curated OpenCode skills.
  - Assert README does not claim Codex `$skill` syntax works in Claude Code or OpenCode.
  - If README includes one-shot CLI examples, assert matching passing smoke evidence exists for that exact form.
- Expected result:
  - Public examples are accurate for each tool and do not document unsmoked one-shot forms.
- Failure proves:
  - The public quick-start can teach unsupported syntax or release claims.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `rg -n '/proposal|/spec|/implement|/code-review|opencode run --command|claude .*proposal|\\$skill' README.md`

### T12. `v0.1.1` release metadata and notes require command alias smoke evidence

- Covers: `R40`, `R40a`, `R41`, `R41a`, `R42`, `R43`, `R44`, `R48`, `E8`
- Level: unit, integration, smoke
- Fixture/setup:
  - `docs/releases/v0.1.1/release.yaml`
  - `docs/releases/v0.1.1/release-notes.md`
  - release metadata fixtures for missing, insufficient, and passing smoke evidence
- Steps:
  - Add `v0.1.1` as a final release target with manifest version `0.1.1`.
  - Validate release metadata with the required first-public-release metadata shape.
  - Assert `release.yaml` uses `version: v0.1.1`, `release_type: final`, and `manifest_version: 0.1.1`.
  - Assert release notes describe the exact OpenCode command alias set and Claude Code skill-native usage guidance.
  - Assert release validation rejects OpenCode command alias smoke evidence that proves only file existence.
  - Assert release validation accepts OpenCode evidence that a generated alias invocation loaded, followed, or produced behavior specific to the matching skill.
  - Assert documented `opencode run --command ...` examples require smoke evidence for that exact one-shot command form.
- Expected result:
  - Stable release validation blocks `v0.1.1` unless release metadata, notes, manifest version, and command alias smoke evidence are coherent.
- Failure proves:
  - The release can claim command alias support without behavioral evidence.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.1`
  - maintainer-run OpenCode smoke for documented one-shot forms

### T13. Release and docs validation reject unsupported one-shot claims

- Covers: `R30`, `R34`, `R36`, `R42`, `R43`, `EC6`, `EC7`
- Level: integration, contract
- Fixture/setup:
  - README fixtures or temporary docs containing one-shot claims
  - release metadata fixtures with absent, failing, and passing smoke rows
- Steps:
  - Validate docs that mention `opencode run --command proposal ...` without passing OpenCode one-shot smoke evidence.
  - Validate docs that mention a Claude one-shot command form without passing Claude one-shot smoke evidence.
  - Validate docs that mention only TUI slash-command examples.
  - Validate docs that mention one-shot examples with matching passing smoke evidence.
- Expected result:
  - Unsourced one-shot claims fail; TUI-only docs and smoke-backed one-shot docs pass.
- Failure proves:
  - Documentation can overclaim behavior that maintainers have not smoke-tested.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.1`

### T14. Security checks reject unsafe alias content and private data

- Covers: `R13`, `EC8`, `EC10`
- Level: unit, integration
- Fixture/setup:
  - generated command alias fixtures
  - unsafe alias fixtures containing shell interpolation, file interpolation, model settings, agent settings, permission settings, secrets, machine-local paths, or copied skill bodies
- Steps:
  - Run generated-output security checks on valid command aliases.
  - Run the same checks on unsafe alias fixtures.
  - Assert `$ARGUMENTS` is allowed only as prompt text.
  - Assert unsafe interpolation, settings, secrets, and duplicated skill bodies fail.
- Expected result:
  - Valid wrappers pass and unsafe wrappers fail before release verification.
- Failure proves:
  - Generated command aliases can broaden permissions, leak private data, or embed unrelated behavior.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T15. Generated adapter package validation passes for the full `v0.1.1` package

- Covers: `R3`-`R27`, `R46`, `R47`
- Level: integration
- Fixture/setup:
  - generated `dist/adapters/`
  - `dist/adapters/manifest.yaml`
- Steps:
  - Generate adapters for version `0.1.1`.
  - Run adapter drift check in `--check` mode.
  - Run adapter validation for version `0.1.1`.
  - Inspect validation output only when failures occur.
- Expected result:
  - The generated package, manifest, command aliases, entrypoints, skill files, and security checks pass as one package-level proof.
- Failure proves:
  - Individual unit checks are insufficient to prove the shipped generated tree is coherent.
- Automation location:
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T16. Release verification supports `v0.1.1` and invokes required checks

- Covers: `R15`, `R19`, `R20`, `R21`, `R22`, `R40a`, `R46`, `R48`
- Level: integration
- Fixture/setup:
  - `scripts/release-verify.sh`
  - `scripts/validate-release.py`
  - `docs/releases/v0.1.1/`
  - generated `dist/adapters/`
- Steps:
  - Assert `scripts/release-verify.sh` accepts `v0.1.1`.
  - Run release verification in dry-run mode for `v0.1.1`.
  - Assert required checks include skill validation, skill regression validation, adapter generation drift check, adapter validation, release metadata validation, and security checks.
  - Assert release verification rejects `v0.1.1` when the generated manifest version is not `0.1.1`.
- Expected result:
  - `v0.1.1` can be verified through the repository release path before tagging.
- Failure proves:
  - The release target is not wired into the same non-smoke gates as earlier adapter releases.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`

### T17. Patch-level compatibility and lifecycle evidence remain coherent

- Covers: `R1`, `R2`, `R45`
- Level: manual, integration
- Fixture/setup:
  - `docs/plan.md`
  - `docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`
  - change-local artifacts under `docs/changes/2026-04-24-skill-invocation-commands-for-adapters/`
  - existing release target tests for `v0.1.0-rc.1` and `v0.1.0`
- Steps:
  - Confirm implementation does not change canonical skill bodies, workflow semantics, or adapter source ownership except through approved docs and generated outputs.
  - Confirm existing `v0.1.0-rc.1` and `v0.1.0` release target tests still pass.
  - Confirm lifecycle artifacts cite this test spec and record actual validation evidence.
  - Confirm final review surfaces explain the change as patch-level only.
- Expected result:
  - The branch remains a scoped `v0.1.1` patch release feature with traceable validation evidence.
- Failure proves:
  - The change silently expanded beyond thin command aliases and documentation.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-skill-invocation-commands-for-adapters.md --path specs/skill-invocation-commands-for-adapters.md --path specs/skill-invocation-commands-for-adapters.test.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`

## Fixtures and data

- Reuse `tests/fixtures/adapters/` for portable, transformable, and non-portable skill cases.
- Add command alias fixtures only when a case cannot be expressed by mutating a temporary generated output tree.
- Use temporary directories for missing, extra, stale, dangling, and unsafe generated command alias trees.
- Use release metadata fixtures for missing smoke, insufficient smoke, one-shot smoke, unsupported one-shot claims, and passing `v0.1.1` final release metadata.
- Use real repository docs for README and generated entrypoint contract checks when feasible.

## Mocking/stubbing policy

- Do not mock repository generation or validation helpers when testing their contracts; use temporary filesystem trees instead.
- Do not invoke real Claude Code or OpenCode in automated non-smoke tests.
- Represent tool smoke evidence with release metadata fixtures for automated validation tests.
- Use maintainer-run manual smoke only for proving actual OpenCode command alias behavior and documented one-shot forms.

## Migration or compatibility tests

- Keep existing `v0.1.0-rc.1` and `v0.1.0` release target tests passing while adding `v0.1.1`.
- Assert existing `.opencode/skills/` and `.claude/skills/` package paths remain unchanged.
- Assert the manifest extension is additive and does not remove existing `version` or `skills` entries.
- Assert Claude Code does not gain `.claude/commands/` wrappers.
- Assert rollback before release can remove generated command aliases, command alias manifest metadata, docs, and release artifacts without changing canonical skills.

## Observability verification

- Validation failures for command aliases must include the `opencode` tool slug, command alias name, and path when available.
- Drift failures must name the stale, missing, or unexpected generated command alias path.
- Release validation failures must distinguish missing smoke evidence, insufficient behavior evidence, unsupported one-shot claims, and manifest version mismatch.
- Release metadata must capture tool version, evidence, reason, and owner for smoke rows that carry command alias evidence.

## Security/privacy verification

- Security checks must reject secrets, credentials, tokens, private keys, and maintainer-specific paths in generated command aliases.
- Security checks must reject shell interpolation, file interpolation, model settings, agent settings, permission settings, and duplicated skill bodies in aliases.
- Security checks must allow `$ARGUMENTS` only as prompt text.
- Smoke evidence must summarize behavior and tool versions without committing private logs, session tokens, or account details.

## Performance checks

- Command alias generation and validation must run linearly in the number of command aliases plus generated adapter files.
- Automated tests should not add external process calls to Claude Code or OpenCode.
- Generated command alias files must stay small enough that package size growth comes from ten thin wrappers, not duplicated skill bodies.

## Manual QA checklist

- Install or copy `dist/adapters/opencode/` into a clean temporary project.
- Run OpenCode in that project and invoke at least one generated alias through the TUI, such as `/proposal`.
- Confirm the observed output shows behavior specific to the matching RigorLoop skill, not only command file discovery.
- If README or release notes document `opencode run --command ...`, run that exact command form and record the tool version and evidence in `docs/releases/v0.1.1/release.yaml`.
- Do not document Claude Code one-shot usage unless an equivalent Claude one-shot smoke has passed and is recorded.

## What not to test

- Do not test OpenCode internals beyond documented project skills, project commands, and `$ARGUMENTS` behavior.
- Do not test Claude Code command-wrapper behavior because this feature explicitly avoids `.claude/commands/`.
- Do not test marketplace, plugin, package-manager, or installer distribution.
- Do not test changes to canonical skill behavior because this feature must not change skill semantics.
- Do not require ordinary contributors to run real tool smoke locally.

## Uncovered gaps

None. Any failure to automate real OpenCode behavior remains covered by the manual smoke checklist and release metadata gates.

## Next artifacts

- `implement` for M1 through M4 in `docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`.
- Change-local artifacts under `docs/changes/2026-04-24-skill-invocation-commands-for-adapters/` during implementation.
- `code-review` after implementation and validation.

## Follow-on artifacts

- None yet.

## Readiness

This active test spec is the current proof-planning surface for `specs/skill-invocation-commands-for-adapters.md` and `docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md`.

Immediate next repository stage: `implement`.
