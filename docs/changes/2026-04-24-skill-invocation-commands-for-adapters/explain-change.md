# Skill invocation commands change explanation

## Summary

This change adds the `v0.1.1` adapter usability layer for invoking RigorLoop skills from OpenCode and Claude Code without changing canonical skill behavior.

The implementation generates thin OpenCode command aliases for the curated lifecycle command set, records exact alias paths in `dist/adapters/manifest.yaml`, validates alias drift and release metadata, documents tool-native invocation forms, records smoke-backed `v0.1.1` release metadata, and closes the lifecycle plan as done.

## Problem

RigorLoop already shipped generated adapter packages for Codex, Claude Code, and OpenCode, but users still needed clear tool-native invocation guidance. OpenCode also benefits from slash command aliases for common lifecycle stages, while non-aliased portable skills must remain available under `.opencode/skills/`.

The key risk was duplicating skill behavior or overclaiming one-shot CLI support. The approved contract required command aliases to stay thin, generated, validated, and backed by smoke evidence before public docs could show `opencode run --command ...`.

## Decision Trail

The accepted proposal selected a patch-level usability layer: add OpenCode command aliases for the curated lifecycle set only, keep Claude Code skill-native, and leave canonical skill bodies authored once under `skills/`.

The approved spec is `specs/skill-invocation-commands-for-adapters.md`. It defines `R1`-`R48`, including the curated OpenCode alias set, manifest alias path requirements, Claude `.claude/commands/` non-goal, README examples, `v0.1.1` release metadata, and smoke evidence rules.

The approved architecture is `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md`. It keeps `scripts/adapter_distribution.py` as the adapter generation and validation boundary, keeps `scripts/adapter_templates/` as authored thin entrypoints, and treats `dist/adapters/` as generated installable output.

The execution plan split the work into four milestones:

- M1 generated and validated OpenCode aliases and manifest metadata.
- M2 documented Claude Code and OpenCode invocation in README and adapter entrypoints.
- M3 added `v0.1.1` release metadata, release notes, release verification support, and smoke-backed one-shot examples.
- M4 closed lifecycle state in `docs/plan.md` and the concrete plan body.

## Diff Rationale By Area

| Area | Files | Change | Reason | Source / Evidence |
| --- | --- | --- | --- | --- |
| Alias generation and validation | `scripts/adapter_distribution.py` | Added `OPENCODE_COMMAND_ALIASES`, command rendering, expected files, manifest parsing, alias validation, stale body checks, unsafe body checks, `0.1.1` support, and release smoke validation. | Satisfies `R4`-`R27`, `R40`-`R44`, `R47`, `R48`; keeps aliases generated and thin. | `T1`-`T8`, `T12`, `T14`-`T16`; `python scripts/test-adapter-distribution.py`. |
| Release gate | `scripts/release-verify.sh` | Added `v0.1.1` as a supported release target. | Allows the patch release to use the same repository-owned release gate as earlier adapter releases. | `R48`, `T16`; `bash scripts/release-verify.sh v0.1.1`. |
| Tests | `scripts/test-adapter-distribution.py` | Added alias generation, manifest, validation, docs, release metadata, smoke evidence, and release-gate tests. | Proves the changed behavior and named edge cases through repository-owned tests that do not require ordinary contributors to install all supported tools. | `T1`-`T16`; 45 adapter distribution tests passed. |
| OpenCode generated output | `dist/adapters/opencode/.opencode/commands/*.md`, `dist/adapters/opencode/AGENTS.md` | Generated ten thin command aliases and updated OpenCode entrypoint guidance. | Provides the installable OpenCode package while keeping source-of-truth behavior in skills and templates. | `R3`-`R14`, `R31`-`R34`; `build-adapters.py --version 0.1.1 --check`. |
| Adapter manifest | `dist/adapters/manifest.yaml` | Recorded `command_aliases.opencode.count` and exact command alias paths. | Makes alias paths auditable and machine-checkable instead of relying on counts. | `R19`-`R22`; manifest validation tests. |
| Claude generated output | `dist/adapters/claude/CLAUDE.md` | Documented native Claude Code slash-skill usage and kept `.claude/commands/` absent. | Preserves Claude Code skill-native behavior and avoids wrapper duplication. | `R28`-`R30`; Claude entrypoint test. |
| Entrypoint templates | `scripts/adapter_templates/claude/CLAUDE.md`, `scripts/adapter_templates/opencode/AGENTS.md` | Authored thin reusable guidance for generated entrypoints, including smoke-backed OpenCode one-shot usage after M3. | Generated output must come from templates, not hand edits. | `R29`-`R34`; generated drift check. |
| Public docs | `README.md`, `docs/workflows.md` | Documented adapter package usage, tool-native examples, current `0.1.1` validation commands, and release target support. | Gives users correct invocation steps and keeps operational docs aligned with current generated output. | `R35`-`R39`, `R46`, `R48`; README/docs tests. |
| Release artifacts | `docs/releases/v0.1.1/release.yaml`, `docs/releases/v0.1.1/release-notes.md` | Added final release metadata, smoke rows, command alias notes, and verification instructions. | Stable `v0.1.1` claims require passing smoke and matching release notes. | `R40`-`R44`; `validate-release.py --version v0.1.1`. |
| Lifecycle artifacts | `docs/changes/.../change.yaml`, `docs/changes/.../explain-change.md`, `docs/plans/...`, `docs/plan.md` | Recorded requirements, tests, validation evidence, review status, verification status, and done lifecycle state. | Keeps traceability and plan lifecycle state synchronized before PR readiness. | `T17`; change metadata and artifact lifecycle validators. |

## Tests Added Or Changed

The main regression surface is `scripts/test-adapter-distribution.py` because adapter generation, manifest parsing, release metadata, and generated output validation are all implemented in repository-owned Python helpers.

| Test IDs | What The Tests Prove |
| --- | --- |
| `T1`-`T4` | OpenCode alias generation creates exactly the curated aliases, no aliases for non-curated skills, and thin deterministic wrapper bodies. |
| `T5`-`T8` | Manifest-declared aliases, missing files, unexpected files, path mismatches, key/stem mismatches, dangling aliases, and unsupported alias tool sections fail validation. |
| `T9`-`T11` | Claude Code remains skill-native; OpenCode docs distinguish `.opencode/skills/` from `.opencode/commands/`; README avoids Codex `$skill` syntax for Claude/OpenCode. |
| `T12`-`T13` | `v0.1.1` release metadata rejects weak OpenCode smoke evidence and permits one-shot docs only when smoke-backed. |
| `T14` | Unsafe alias content, stale body content, and security-sensitive markers fail validation. |
| `T15`-`T16` | Full generated adapter validation and release verification support `0.1.1` / `v0.1.1`. |
| `T17` | Lifecycle artifacts and plan state remain coherent through closeout. |

Manual smoke complemented the automated tests. OpenCode `1.14.22` loaded the `proposal` skill through `opencode run --pure --dir <copied-adapter-root> --command proposal` and repeated `ARGUMENT_MARKER_M3_SMOKE`, proving command execution and argument pass-through. Codex and Claude Code smoke verified adapter entrypoints and the `workflow` skill path.

## Verification Evidence

Final verification from current HEAD `59fdfc4` passed:

- `bash scripts/release-verify.sh v0.1.1`
- `bash scripts/ci.sh`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-24-skill-invocation-commands-for-adapters/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-skill-invocation-commands-for-adapters.md --path specs/skill-invocation-commands-for-adapters.md --path specs/skill-invocation-commands-for-adapters.test.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/plans/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/changes/2026-04-24-skill-invocation-commands-for-adapters/change.yaml --path docs/changes/2026-04-24-skill-invocation-commands-for-adapters/explain-change.md --path docs/plan.md`
- `git diff --check`

CI reported unrelated baseline proposal warnings during push-main artifact validation, but the touched artifact set and generated outputs validated successfully.

## Alternatives Rejected

Generating aliases for every portable OpenCode skill was rejected because the spec limits aliases to the curated lifecycle command set and keeps other skills available under `.opencode/skills/`.

Generating `.claude/commands/` wrappers was rejected because Claude Code remains skill-native for this release.

Duplicating skill bodies inside command aliases or entrypoints was rejected because canonical skill behavior must remain authored once under `skills/`.

Documenting Claude Code one-shot examples was rejected because no Claude one-shot form is in the smoke-backed release contract.

Publishing OpenCode one-shot examples before smoke was rejected during M2. The examples were added only after M3 recorded passing `opencode run --command proposal` smoke evidence.

## Scope Control

The change does not alter canonical skill behavior, workflow semantics, Codex invocation behavior, model settings, permission settings, marketplace packaging, installer distribution, or hosted runtime behavior.

The adapter output under `dist/adapters/` remains generated. The source-of-truth edits are in `skills/`, `scripts/adapter_distribution.py`, adapter templates, specs, release artifacts, and lifecycle documentation.

## Risks And Follow-Ups

Remaining risk is external tool behavior drift. If OpenCode or Claude Code changes skill or command discovery semantics, the adapter contract should be updated through the same proposal/spec/architecture/release lifecycle before release claims change.

No implementation blocker remains. The branch is verified and lifecycle-closed, but PR creation should happen from a review branch rather than directly from `main`.

## PR Handoff

Reviewer focus should be the release safety path: generated alias validation, release metadata validation, smoke evidence, and whether public docs accurately distinguish Claude Code native skills from OpenCode command aliases.

The branch is `branch-ready` from the verification gate. `pr-open-ready` belongs to the PR stage and should first restack or create an appropriate review branch because the current branch is `main`.
