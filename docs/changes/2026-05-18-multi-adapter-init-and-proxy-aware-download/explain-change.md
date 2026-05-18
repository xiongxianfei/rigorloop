# Explain Change: Multi-Adapter Init and Proxy-Aware Adapter Download

## Summary

This change expands the RigorLoop CLI from Codex-only adapter init to descriptor-driven init for Codex, Claude Code, and opencode. It preserves Codex under `.agents/skills`, verifies release or local adapter archives against CLI-bundled trusted metadata, writes schema v2 lockfiles for mixed single-root and multi-root adapters, and adds proxy-safe network download diagnostics with `--from-archive` fallback guidance.

The change also records the contract, architecture decision, milestone plan, test spec, review findings, review-resolution closeout, package README guidance, and final implementation review evidence needed before final verification.

## Problem

RigorLoop already had public adapter archives for Codex, Claude Code, and opencode, but `rigorloop init` only accepted `--adapter codex`. Enterprise users also had a network adoption problem: Node `fetch()` can fail in proxied environments unless Node env-proxy support is available and enabled. The CLI needed to support the public adapter surface without weakening archive verification, lockfile integrity, or proxy privacy.

## Decision Trail

| Decision point | Outcome | Source |
|---|---|---|
| Proposal direction | Chose contract-first multi-adapter init plus proxy-aware diagnostics, while preserving verified release archives and local archive fallback. | `docs/proposals/2026-05-18-multi-adapter-init-and-proxy-aware-download.md` |
| Codex path | Kept Codex at `.agents/skills`; no `.codex/skills` migration. | `MAI-R8` through `MAI-R10`, ADR |
| Adapter descriptors | Replaced Codex constants with descriptors for `codex`, `claude`, and `opencode`. | `MAI-R1` through `MAI-R16`, M1 |
| Trust boundary | Kept CLI-bundled official metadata as the trust root for network and local archive installs. | `MAI-R17` through `MAI-R28`, M1 and M3 |
| opencode roots | Treated opencode as metadata-driven: skills only for compatible older archives, skills plus commands when aliases are declared. | `MAI-R21d` through `MAI-R21f`, `MAI-R39` through `MAI-R46c`, M3 |
| Lockfile schema | Added schema v2 mixed single-root and multi-root entries while preserving valid schema v1 Codex upgrade only after drift checks. | `MAI-R55` through `MAI-R76`, M2 |
| Proxy behavior | Added bounded diagnostics and Node env-proxy status reporting; did not add Undici dispatcher support. | `MAI-R77` through `MAI-R85`, ADR, M4 |
| Output behavior | Preserved stable JSON and human output contracts. | `MAI-R86` through `MAI-R91`, M4 |
| Generated output | Used temporary adapter build and validation when adapter metadata/output changed. | `MAI-R92` through `MAI-R95`, M3 |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `specs/multi-adapter-init-and-proxy-aware-download.md` | Added the approved behavior contract for supported adapters, metadata, extraction safety, lockfile schema v2, proxy diagnostics, output, and acceptance criteria. | Required because this is public CLI behavior, durable lockfile behavior, and security-sensitive archive handling. | Proposal, spec reviews | `spec-review-r2`, `spec-review-r3` |
| `specs/multi-adapter-init-and-proxy-aware-download.test.md` | Added the requirement-to-test map and concrete `TMAI-*` cases. | Ensures every major contract surface has fixture-backed proof before implementation. | Test spec, plan | User approval of test spec, package tests |
| `docs/architecture/system/architecture.md`, diagrams, ADR | Recorded descriptor ownership, bundled metadata trust root, schema v2 lockfile boundary, and proxy diagnostics boundary. | This change crosses CLI, metadata, lockfile, generated output, and network-diagnostic architecture boundaries. | Architecture, ADR | `architecture-review-r1` |
| `packages/rigorloop/dist/lib/adapters.js` | Added descriptor registry and archive naming helpers for `codex`, `claude`, and `opencode`. | Replaces Codex-only constants and makes supported adapter scope testable. | `MAI-R1` through `MAI-R16`, M1 | `TMAI-001` |
| `packages/rigorloop/dist/lib/official-archive-url.js` | Generalized official archive URL validation beyond Codex. | Network mode must fetch only metadata-selected official archive URLs. | `MAI-R17` through `MAI-R24`, M1 | URL helper and network tests |
| `packages/rigorloop/dist/lib/lockfile.js` | Added strict schema v2 parsing and serialization, multi-root opencode fields, mixed adapter sorting, and schema v1 Codex compatibility. | opencode needs per-root hashes; existing valid Codex lockfiles must remain compatible without silently preserving unknown fields. | `MAI-R55` through `MAI-R76`, M2 | `TMAI-021`, `TMAI-022`, `TMAI-024`, `TMAI-025`, `TMAI-026` |
| `packages/rigorloop/dist/bin/rigorloop.js` | Generalized init planning, metadata validation, archive acquisition, extraction, tree hashing, manifest writes, lockfile writes, dry-run output, network fetch diagnostics, and proxy env-proxy status detection. | Implements the approved CLI behavior while keeping verification before durable success claims. | M1 through M4 | `npm test --prefix packages/rigorloop` |
| `packages/rigorloop/dist/metadata/*.json` | Added/updated bundled metadata for Codex, Claude Code, and opencode archive artifacts and release metadata. | CLI needs trusted package-compatible metadata for all supported adapters. | `MAI-R17` through `MAI-R28`, M1 and M3 | Metadata and archive tests |
| `packages/rigorloop/test/cli.test.js` | Added descriptor, metadata, archive, manifest, lockfile, opencode, proxy, output-mode, and package README tests. | Package tests are the main hermetic proof surface for this CLI package. | Test spec M1 through M5 | 107 package tests passed |
| `packages/rigorloop/README.md` | Updated public package usage for `codex|claude|opencode`, runtime roots, `--from-archive`, and Node env-proxy fallback guidance. | Package docs were Codex-only and would mislead users after the CLI expanded. | M5 | `M5-DOC-001` |
| `docs/changes/...` review artifacts | Recorded formal proposal, spec, architecture, plan, code-review, and review-resolution evidence. | Required by formal lifecycle recording and material-finding closeout contracts. | Governance and workflow rules | `validate-review-artifacts.py` |
| `docs/learn/sessions/*.md` | Captured two maintainer-triggered lessons on proxy fetch guidance and opencode metadata truth-table review misses. | These were explicit learn invocations during the initiative and document process lessons without changing authoritative behavior. | Learn skill invocations | Lifecycle validation for learn sessions |
| `.gitignore` | Ignored `.agents/` local runtime output. | Adapter init can create local runtime state that should not become tracked source. | Architecture generated-output boundary | Diff review |

## Tests Added Or Changed

| Test or proof | What it proves | Why this level is appropriate |
|---|---|---|
| `TMAI-001` | Supported adapters are exactly `codex`, `claude`, and `opencode`; Codex remains `.agents/skills`. | Descriptor behavior is a small package-level contract. |
| `TMAI-003` through `TMAI-012` | Unsupported adapters, trusted metadata, wrong archive, URL, checksum, and compatibility failures block safely. | Fixture-backed CLI tests exercise user-visible command behavior without live network. |
| `TMAI-017` through `TMAI-028` | Manifest and lockfile schema v2 behavior, schema v1 upgrade, drift blocking, and mixed entries. | Lockfile and manifest state are durable project outputs. |
| `TMAI-014`, `TMAI-016`, `TMAI-020` | opencode declared aliases, commands-root guard, older skills-only warnings, and dry-run no-mutation behavior. | opencode has the highest multi-root risk. |
| `TMAI-029` through `TMAI-032` | Network fetch success/failure, bounded proxy diagnostics, redaction, and archive verification preservation. | Proxy behavior must be hermetic and privacy-safe. |
| `CR-M4-R1-F1` regression | `node --use-env-proxy` is detected through `process.execArgv`. | Direct CLI invocation proves the exact missed runtime path. |
| `M5-DOC-001` | Package README documents multi-adapter init, runtime roots, local archive fallback, and proxy guidance without claiming `.codex/skills` or Undici dispatcher support. | M5 needed package-facing documentation proof separate from `TMAI-033`. |
| Adapter generation validation | `scripts/build-adapters.py` and `scripts/validate-adapters.py` passed for v0.1.5 temporary output. | Required because adapter metadata/output changed in M3. |

## Validation Evidence Available Before Final Verify

Recorded validation includes:

- `npm test --prefix packages/rigorloop`
- `python scripts/build-adapters.py --version 0.1.5 --output-dir /tmp/rigorloop-adapter-plan-check`
- `python scripts/validate-adapters.py --version 0.1.5 --root /tmp/rigorloop-adapter-plan-check`
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `git diff --check ...`
- Selected `bash scripts/ci.sh --mode explicit ...` runs for each implementation, review-resolution, and review-recording slice.

Hosted CI and final `verify` have not been claimed by this stage.

## Review Resolution Summary

`docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md` is closed.

- Reviews covered: 17 lifecycle review rounds plus the M5 rerun record in the change-local review log.
- Findings resolved: 15.
- Unresolved findings: 0.
- Dispositions: all material findings were accepted and resolved.

Key implementation review findings resolved:

- `CR-M2-R1-F1` and `CR-M2-R2-F1`: older opencode skills-only roots must be metadata-driven in real and dry-run planning.
- `CR-M3-R1-F1` and `CR-M3-R2-F1`: opencode skills-only compatibility and commands-root metadata must be explicitly validated.
- `CR-M4-R1-F1`: `--use-env-proxy` runtime flag detection must inspect `process.execArgv`.
- `CR-M5-R1-F1`: package README proof needed a distinct `M5-DOC-001` identifier.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Patch constants to accept more adapter names | Would miss opencode command aliases, schema v2 lockfile shape, metadata-specific roots, and compatibility tests. |
| Move Codex to `.codex/skills` | Rejected because Codex remains `.agents/skills` for this contract and migration risk is unnecessary. |
| Bundle adapter archives into npm | Rejected because npm is the CLI delivery channel; adapter archives remain verified release artifacts. |
| Trust user-supplied metadata for local archives | Rejected because the CLI owns metadata trust and verifies local archives against bundled official metadata. |
| Add programmatic Undici dispatcher support now | Rejected as out of first-slice scope; this change uses Node env-proxy status diagnostics and `--from-archive` fallback. |
| Treat opencode as skills-only | Rejected because opencode command aliases under `.opencode/commands` are a generated runtime surface when metadata declares them. |

## Scope Control

Preserved non-goals:

- No `rigorloop status`, `rigorloop validate`, workflow YAML, or generated workflow docs.
- No Codex migration to `.codex/skills`.
- No npm-bundled adapter archives.
- No user-supplied metadata option.
- No programmatic Undici proxy dispatcher support.
- No lockfile repair command.
- No live GitHub or live proxy dependency in normal tests.
- No hand-editing generated adapter package output as a source of truth.

## Risks And Follow-Ups

- Final `verify` still needs to run after this explanation.
- PR handoff is not ready until verify passes and the plan/index state is synchronized for PR readiness.
- Proxy support remains diagnostics-first; programmatic proxy dispatcher support would require a later proposal/spec if needed.
- Release smoke for real public archives remains a release-stage concern; normal tests intentionally stay hermetic.
