# Target-Native Init Commands Explain Change

## Summary

This change ships the `0.3.0` target-native init contract:

```bash
rigorloop init codex
rigorloop init claude
rigorloop init opencode
```

The public CLI no longer accepts `--adapter`. Default init is now install-only and does not create or update `rigorloop.yaml` or `rigorloop.lock`; managed project state is written only when users explicitly pass `--write-state`.

The release path is hardened at the same time. Packed-package pre-publish smoke now runs real non-dry-run installs for every target, and v0.3.0 post-publish evidence must record live registry/download proof with installed roots, tree hashes, file counts, command output summaries, public archive URLs, and npm version.

## Problem

The original public command made users think in terms of internal packaging:

```bash
npx @xiongxianfei/rigorloop@latest init --adapter codex
```

The accepted proposal identified two related issues:

- users initialize support for a tool, not an adapter;
- the publication incident came from release smoke that used dry-run proof and missed the real install metadata-validation path.

User-visible state files also created friction. Default init wrote `rigorloop.yaml` and `rigorloop.lock`, which made first-time users remove files manually when they only wanted target support installed.

## Decision Trail

| Decision point | Decision | Source |
| --- | --- | --- |
| Public command | Use `init <target>` with exact targets `codex`, `claude`, and `opencode`. | accepted proposal; `specs/target-native-init.md` TNI-R1 through TNI-R5 |
| Removed syntax | Remove `--adapter` entirely in `0.3.0`, with migration diagnostics. | user decision; TNI-R6 through TNI-R11 |
| Default state behavior | Make default init install-only and preserve existing state files byte-for-byte. | proposal state-file revision; TNI-R14 through TNI-R24 |
| Managed state | Write target-oriented `rigorloop.yaml` and `rigorloop.lock` only with `--write-state`. | TNI-R25 through TNI-R28; TNI-R50 through TNI-R69 |
| Internal naming boundary | Keep non-user-visible `dist/adapters/`, archive filenames, and package-bundled metadata naming as compatibility internals. | proposal and ADR boundary |
| Release smoke | Require real packed-package pre-publish smoke and structured live post-publish evidence. | TNI-R86 through TNI-R94; `TTNI-SMOKE-001` through `TTNI-SMOKE-003` |

## Diff Rationale By Area

| Area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| CLI parser and output | `packages/rigorloop/dist/bin/rigorloop.js` accepts `init <target>`, rejects `--adapter`, rejects unsupported aliases, and reports target-oriented output. | Match the public command contract and fail removed syntax before mutation. | M1 tests and clean `code-review-r2` |
| State files | Default init no longer writes state; `--write-state` writes manifest schema v2 and lockfile schema v3 with target-oriented keys. | Remove first-run state-file friction while preserving explicit managed-state behavior. | M1 tests, M2 state-safety tests |
| Existing state safety | Default init preserves state files byte-for-byte but parses existing state before target-root mutation when needed, blocking malformed, drifted, or conflicting state. | Byte preservation cannot mean unsafe mutation of managed roots. | M2 tests and clean `code-review-r4` |
| Target install roots | Codex installs `.agents/skills`, Claude installs `.claude/skills`, and opencode installs `.opencode/skills` plus `.opencode/commands` when declared. | Preserve target behavior while moving command language away from adapters. | Package CLI tests and packed-package smoke |
| Package metadata | The package now carries v0.3.0 release metadata and release index entries derived from generated release archives. | Bind package install behavior to the actual archives it installs. | `scripts/test-adapter-distribution.py`, `validate-release.py`, `release-verify.sh` |
| Public docs | Root README, package README, and v0.3.0 release notes teach `init <target>` and `@latest` for manual quick start, with pinned commands for automation. | Keep public docs aligned with the new command and user mental model. | docs sweep and release-note validation |
| Release validation | Packed package smoke runs real non-dry-run default and `--write-state` installs for all targets. | Prevent recurrence of dry-run-only release proof. | `scripts/test-npm-package-publication.py` |
| Post-publish evidence | v0.3.0 `target_init_smoke` evidence requires npm version, public archive URLs, installed roots, tree hashes, file counts, command output summary, and verification flags. | Ensure published live-smoke rows cannot pass with thin evidence. | `TNI-CR5-F1` resolution and clean `code-review-r6` |
| Lifecycle artifacts | Proposal, spec, test spec, architecture, ADR, plan, review log, review-resolution, and this explain-change record the decision and proof trail. | Make the behavior and release-safety change reviewable and durable. | lifecycle and review-artifact validation |

## Tests And Proof

The test spec maps the approved requirements into CLI, state, archive, docs, release, migration, security, and smoke proof.

Key proof surfaces added or updated:

- `packages/rigorloop/test/cli.test.js`
  - canonical target parsing;
  - removed `--adapter` and mixed syntax rejection before mutation;
  - named alias rejection;
  - default install-only behavior;
  - `--write-state` target-oriented state output;
  - opencode skills and commands install roots;
  - existing-state safety, drift, conflict, malformed-state, and legacy-state behavior.
- `scripts/test-npm-package-publication.py`
  - packed package help and package content expectations;
  - real non-dry-run packed-package smoke for every target;
  - default no-state and explicit `--write-state` smoke paths.
- `scripts/test-adapter-distribution.py`
  - v0.3.0 release-gate behavior;
  - release notes and public docs expectations;
  - metadata/archive coherence;
  - post-publish live-smoke evidence detail enforcement.

## Review Resolution Summary

Review resolution is closed in `review-resolution.md`.

Material findings resolved:

- `TINIT-PR1-F1`: clarified user-visible state-file key terminology.
- `TNI-SR1`, `TNI-SR2`, `TNI-SR3`: fixed spec conflicts around dry-run planning, state-file key terminology, and existing-state safety.
- `TNI-PLR1-F1`: corrected the `release-verify.sh` invocation in the plan.
- `TNI-CR1-F1`: added direct parser-edge tests for rejected aliases and mixed removed syntax.
- `TNI-CR3-F1`: added direct default-init and state-safety proof for opencode, drift/conflict blocking, and legacy state preservation.
- `TNI-CR5-F1`: enforced detailed v0.3.0 post-publish live-smoke evidence.

Clean reviews:

- proposal-review R2/R3;
- spec-review R2/R3;
- architecture-review R1;
- plan-review R2;
- code-review R2, R4, and R6.

## Validation Evidence Available Before Final Verify

Key validation already recorded in the active plan and change metadata includes:

- `npm test --prefix packages/rigorloop`
- `python scripts/test-npm-package-publication.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/validate-release.py --version v0.3.0 --release-output-dir /tmp/tmp.cWJYJ5cs7M --release-commit 02a9d7d6d514fc99908abf32898494dbbbae00c9`
- `RELEASE_OUTPUT_DIR=/tmp/tmp.cWJYJ5cs7M RELEASE_COMMIT=02a9d7d6d514fc99908abf32898494dbbbae00c9 bash scripts/release-verify.sh v0.3.0`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `git diff --check --`

M4 adds broad selected validation over the touched product, script, docs, spec, plan, and change-local surfaces. This is not final verification; the `verify` stage still owns final branch readiness.

## Scope Control

Preserved boundaries:

- no new npm package name;
- no default top-level `rigorloop codex` command;
- no target aliases such as `claude-code`, `open-code`, `openai`, or `codex-cli`;
- no generated skill behavior changes;
- no full internal rename of `dist/adapters/`, archive filenames, or package-bundled metadata fields;
- no live registry/download success claim before publication;
- no claim that dry-run output proves install success.

## Risks And Follow-Ups

- Live registry/download smoke remains pending until the npm package and GitHub release archives are externally observable.
- Historical internal adapter naming remains by design and can be revisited in a separate compatibility-sensitive proposal.
- Final `verify` still needs to assess artifact-code-test coherence, lifecycle state, stale artifacts, and PR readiness.

## Readiness

Implementation milestones M1, M2, and M3 are closed after clean code reviews. M4 records this durable rationale and broad selected validation before handing the milestone to `code-review`.

Next stage after M4 implementation handoff: `code-review`.
