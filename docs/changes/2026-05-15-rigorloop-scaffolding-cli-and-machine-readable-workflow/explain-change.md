# Explain Change - RigorLoop CLI package and Codex init

Date: 2026-05-15
Change ID: 2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow
Status: explain-change recorded before final verify

## Summary

This change adds the first RigorLoop CLI slice: a local `@xiongxianfei/rigorloop` package candidate with one `rigorloop` binary, `--help`, `version`, and `init --adapter codex` support.

The implementation intentionally stops at the approved first slice. It scaffolds `rigorloop.yaml`, plans but does not write durable `rigorloop.lock`, installs only the Codex adapter from a verified release archive, and keeps public npm publication, `new-change`, `status`, `validate`, durable lockfile writes, other adapters, and workflow YAML canonicality out of scope.

## Problem

The proposal identified an adoption gap: RigorLoop had repository-local workflow artifacts, validators, skills, and release adapter archives, but users still needed too much repository knowledge to initialize a project or install adapter files safely.

The accepted first slice narrowed that broad direction to one implementable contract:

- package name: `@xiongxianfei/rigorloop`
- binary: `rigorloop`
- command surface: `--help`, `version`, `init --adapter codex`, `init --adapter codex --dry-run --json`
- safe scaffold planning and `rigorloop.yaml` generation
- verified Codex adapter archive installation
- planned lockfile output only

## Decision Trail

| Source | Decision or requirement | Effect on the diff |
|---|---|---|
| Proposal | npm is a delivery channel, not source of truth | The package ships CLI code and metadata, not canonical skills or adapter archives. |
| Proposal review | First accepted slice must be narrow | The implementation excludes future commands and workflow YAML work. |
| Spec R1-R20 | Define package identity, command surface, JSON envelope, stdout/stderr, and exit codes | Added the package skeleton, binary, command dispatcher, JSON result shape, and result-class exit mapping. |
| Spec R21-R48 | Define non-destructive init, dry-run, manifest shape, write planning, and no durable lockfile | Added explicit write planning, `rigorloop.yaml` rendering, dry-run behavior, overwrite refusal, and warning-only planned lockfile output. |
| Spec R49-R61c | Define bundled metadata, official archive URL enforcement, archive verification, extraction, and failure classes | Added bundled metadata, archive SHA/size/tree-hash verification, path/symlink safety checks, official URL validation, and expected verification exit code `3`. |
| Spec R76-R79 | Block public npm publication and preserve source-of-truth boundaries | Kept the package private and documented publication as blocked. |
| ADR | Use bundled official adapter metadata for the compatible release and release archives as adapter source | Added `dist/metadata/releases.json` and `adapter-artifacts-v0.1.3.json`; installed from release ZIPs rather than generated source in npm. |
| Plan M1 | Establish command contract first | Added package skeleton, binary, help/version, dispatch, result envelope, and exit-code helper. |
| Plan M2 | Add init planning and manifest scaffold | Added non-destructive action/artifact planning, `.agents` and `.agents/skills` directory planning, and `rigorloop.yaml` scaffold writes. |
| Plan M3 | Add verified Codex archive install | Added metadata validation, archive download/local archive modes, extraction safety, tree hash, and official archive URL enforcement. |

## Diff Rationale by Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `packages/rigorloop/package.json` | Adds package candidate metadata, one `rigorloop` bin, private publication state, and test script. | Establish the first package boundary without public npm publication. | Spec R1-R5, R76-R79; ADR package boundary | T1, T28; package tests passed. |
| `packages/rigorloop/README.md` | Documents the package as a first-slice local package candidate and states publication remains blocked. | Avoid implying npm publication readiness. | Spec R76; ADR publication boundary | T28; selected CI passed. |
| `packages/rigorloop/dist/bin/rigorloop.js` | Implements command parsing, help/version, JSON/human output, init planning, manifest rendering, bundled metadata loading, archive verification, extraction, tree hash, planned lockfile output, and result handling. | This is the first-slice CLI implementation. It keeps behavior observable, non-destructive by default, and constrained to Codex init. | Spec R1-R75; ADR; Plan M1-M3 | T1-T44; package tests and smoke commands passed. |
| `packages/rigorloop/dist/lib/command-result.js` | Adds result-class-based exit-code mapping. | `status: error` can mean either expected verification failure or internal failure; public exit code must come from failure class. | Spec R12; CR1-F1 | T11; code-review-r2 closed M1. |
| `packages/rigorloop/dist/lib/official-archive-url.js` | Adds exact official GitHub release archive URL validation. | Bundled metadata must not expand network fetches to arbitrary URLs. | Spec R50g-R50h; CR8-F1 | T15 official/non-official URL tests; code-review-r9 closed M3. |
| `packages/rigorloop/dist/metadata/releases.json` | Adds package-bundled release index for `v0.1.3` and bundled metadata hash. | Provides the trusted in-package metadata root without requiring a separate release metadata asset. | ADR; CR6-F2; CR7-F1 | T16 metadata hash/missing trust root tests. |
| `packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.3.json` | Adds official Codex adapter metadata: release, archive URL, SHA-256, size, install root, tree hash, and validation result. | Allows network and local archive installs to verify the same release artifact without making npm the adapter archive source. | Spec R49-R55; ADR | T15, T18, T29, T35-T39. |
| `packages/rigorloop/test/cli.test.js` | Adds package, command, init, manifest, write-plan, metadata, archive, URL, tree-hash, and no-lockfile tests. | The first slice has public command and filesystem contracts; tests prove both success paths and expected failure classes. | Test spec T1-T44 | `npm test --prefix packages/rigorloop` passed. |
| `scripts/validation_selection.py` and `scripts/test-select-validation.py` | Adds selector routing and regression coverage for `packages/rigorloop`. | Selected CI must not fail open for the new package path. | Plan M1 validation need; test spec T46 | `python scripts/test-select-validation.py` and selected CI passed. |
| `specs/rigorloop-cli-package-and-codex-init.md` | Defines the first-slice contract and later review-driven clarifications for local archive metadata, exit codes, bundled metadata, and official URL validation. | The implementation changes observable CLI behavior and needed a stable contract before coding. | Spec stage; SR1-F1-SR1-F3; CR7-F1; CR8-F1 | Spec-review-r2 approved; lifecycle validation passed. |
| `specs/rigorloop-cli-package-and-codex-init.test.md` | Maps requirements to T1-T46, including dry-run, archive verification, official URL validation, and no-lockfile behavior. | Ensures each important public requirement has executable or reviewable proof. | Test-spec stage | User approved test spec; selected CI passed. |
| `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md` | Records the package, metadata, release archive, no-lockfile, and no-publication architecture boundary. | The CLI crosses package, filesystem, metadata, and release-artifact trust boundaries. | Architecture stage | Architecture-review-r1 approved. |
| `docs/architecture/system/architecture.md` and diagrams | Adds the CLI package/Codex init boundary to the system architecture package. | Keeps the long-lived architecture map aligned with the new package and release archive flow. | Architecture stage | Artifact lifecycle and selected CI passed. |
| `docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md` and `docs/plan.md` | Tracks M1-M3 execution, validation evidence, review findings, and current handoff state. | Planned initiatives use the active plan as the current lifecycle state owner. | Plan and workflow contract | Plan-review-r1 approved; selected CI passed. |
| `docs/changes/.../review-log.md`, `review-resolution.md`, and `reviews/*.md` | Records proposal, spec, architecture, plan, and code review evidence plus dispositions for material findings. | Material review findings must have durable evidence, disposition, and validation. | Workflow/review contract | Review artifact validation and closeout validation passed. |
| `docs/follow-ups.md` | Keeps deferred slices registered instead of folding them into the first slice. | The proposal is broad, but the first implementation must stay narrow. | Proposal review | Proposal-review and lifecycle validation passed. |

## Tests Added or Changed

The active test spec maps requirements to T1-T46. The package tests implement the first-slice proof surface:

- T1-T5: package metadata, help/version, unsupported command and adapter behavior.
- T6-T11: JSON envelope, human output, quiet/debug/no-color behavior, and exit-code mapping.
- T12-T14: dry-run purity, required adapter selection, and deterministic local archive path validation.
- T15-T19: bundled metadata, official archive URL enforcement, version compatibility, local archive mode, and missing metadata blockers.
- T20-T27: actual init writes, manifest behavior, write planning, existing directories, overwrite refusal, and force limits.
- T29-T40: release metadata validation, traversal, install-root, symlink, checksum, size, tree-hash, source repository, and validation-result failures.
- T41-T44: no durable lockfile writes and `rigorloop-tree-hash-v1` behavior.
- T45-T46: source-of-truth boundary and selected CI coverage.

The test level is intentionally mostly unit/integration-style package testing because the first slice is a CLI/filesystem contract with deterministic temp-project behavior. Real smoke checks were still run for default network install and local archive install with the official `v0.1.3` Codex archive.

## Validation Evidence Available Before Final Verify

These commands passed during implementation and review closeout:

- `npm test --prefix packages/rigorloop`
- `node packages/rigorloop/dist/bin/rigorloop.js --help`
- `node packages/rigorloop/dist/bin/rigorloop.js version`
- `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --dry-run --json`
- real default network install smoke: `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --json`
- real local archive smoke: `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.3.zip --json`
- `python scripts/test-select-validation.py`
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `bash scripts/ci.sh --mode explicit ...`
- `git diff --check --`

This is pre-verify evidence only. It does not claim branch-ready, PR-body-ready, PR-open-ready, hosted CI-final status, or final verification.

## Review Resolution Summary

Review resolution is recorded in `docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md`.

Material findings recorded and resolved:

- Spec review: 3 accepted and resolved findings.
- Code review: 6 accepted and resolved findings across M1-M3.
- Deferred or needs-decision findings: 0.
- Open findings in `review-log.md`: 0.

Key review-driven fixes:

- SR1-F1: local `--from-archive` uses bundled official metadata and no `--metadata` flag.
- SR1-F2: first-slice `rigorloop.yaml` shape is explicit.
- SR1-F3 and CR1-F1: expected verification failures use result-class exit mapping rather than internal-error exit code.
- CR4-F1: write plans include both `.agents` and `.agents/skills` before mutation.
- CR6-F1 and CR6-F2: runtime metadata source overrides were removed and metadata bytes are verified before parsing.
- CR7-F1: default install no longer depends on a missing release metadata asset.
- CR8-F1: default network install validates exact official GitHub release archive URLs before fetch.

## Alternatives Rejected

- Separate `@rigorloop/cli`, `@rigorloop/create`, or `create-rigorloop` packages were not implemented because the accepted first-slice UX uses one package: `@xiongxianfei/rigorloop`.
- Bundling adapter archives inside npm was rejected because generated adapter archives are release artifacts, not canonical npm source.
- Requiring a user-facing `--metadata` flag was rejected because local archive mode should remain `--from-archive <path>` and verify against package-bundled official metadata.
- Writing durable `rigorloop.lock` was rejected for this slice because lockfile authority, hash ownership, and update rules need a separate accepted spec.
- Porting repository Python validators into TypeScript was rejected because `validate` is a future CLI slice, not part of first Codex init.
- Implementing `new-change`, `status`, `validate`, other adapters, workflow YAML canonicality, generated workflow docs, frozen drift checks, and public npm release hardening was rejected as out of scope for this first slice.

## Scope Control

The change preserves these non-goals:

- no public npm publication;
- no durable `rigorloop.lock`;
- no canonical adapter skill source inside npm;
- no adapter installation from `.codex/skills`;
- no `new-change`, `status`, or `validate` command;
- no workflow YAML canonicality change;
- no generated workflow docs or frozen drift checks;
- no readiness overclaims for branch, PR body, PR open, or hosted CI.

## Risks and Follow-Ups

Remaining risks:

- The package is still a candidate local package; public npm publication remains blocked until release hardening is accepted.
- Durable drift detection is limited because `rigorloop.lock` is planned output only.
- Network install depends on GitHub release archive availability; local `--from-archive` remains the fallback.
- Only Codex adapter installation is implemented.

Tracked follow-ups include durable lockfile behavior, npm release hardening, `new-change`, `status`, `validate`, other adapters, workflow YAML canonicality, generated workflow docs, and frozen drift checks.

## Readiness

Implementation milestones M1-M3 are complete and reviewed. This explain-change artifact is now recorded for downstream review.

The change is ready for the `verify` stage to decide branch readiness. It is not branch-ready or PR-ready until `verify` and later PR ownership produce that evidence.
