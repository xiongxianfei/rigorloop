# Explain Change: RigorLoop CLI Durable Lockfile

## Summary

This change lets the existing `@xiongxianfei/rigorloop` CLI write durable `rigorloop.lock` state for the approved first lockfile-writing surface: verified Codex adapter initialization.

The first CLI slice intentionally emitted only `planned_lockfile` because a lockfile is durable project state. This change adds the approved contract for that durable state: strict `schema_version: 1` parsing, deterministic serialization, manifest hashing, source-mode recording for network and local archive installs, verified installed-tree hashing, and drift blocking before generated adapter files are replaced.

## Problem

`rigorloop init --adapter codex` could install verified Codex adapter output, but it could not durably record what was installed. That preserved the initial safety boundary, but left projects without a machine-owned record for generated adapter state, reproducibility checks, or later drift detection.

The approved proposal explicitly deferred durable `rigorloop.lock` writes until the lockfile authority, hash model, update behavior, and overwrite rules were specified. The lockfile spec now supplies that contract, so the implementation can replace planned-only output with real lockfile writes for the narrow Codex init surface.

## Decision Trail

- Proposal direction: keep npm/CLI as delivery and scaffolding, not source of truth; emit planned lockfile content only until a lockfile spec is accepted.
- Spec decision: `rigorloop.lock` is project-local, machine-owned generated-output state. It does not replace canonical workflow, skill, schema, release, or adapter metadata sources.
- Architecture and ADR decision: the CLI owns lockfile serialization, validation, drift comparison, and write ordering only for `rigorloop init --adapter codex` and `--from-archive` after verification succeeds.
- Plan split:
  - M1 added strict schema parsing, serialization, manifest hashing, and write-plan behavior.
  - M2 wrote or updated `rigorloop.lock` only after verified Codex install and installed-tree verification.
  - M3 blocked replacement when existing lockfile-recorded generated output was missing, drifted, or conflicted with expected file/directory shape.
- Review outcomes:
  - `CR1-F1` found unknown nested mapping fields were accepted; fixed in M1.
  - `CR3-F1` found unrelated files under `.agents/skills` could be recorded as generated output; fixed in M2.
  - `code-review-r5` approved M3 with no material findings.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `packages/rigorloop/dist/lib/lockfile.js` | Added strict lockfile parser, validator, deterministic serializer, and normalized SHA-256 helpers. | Supports complete `schema_version: 1` shape, strict unknown-field blocking, deterministic output, and normalized manifest hashing. | Spec R9-R17h, R23c-R23k, R34-R35, R40-R45c; ADR lockfile boundary. | TLF-001, TLF-003 through TLF-008; CR1-F1 regression tests. |
| `packages/rigorloop/dist/bin/rigorloop.js` | Replaced planned-only lockfile behavior with lockfile write planning, verified create/update, source-mode recording, installed-tree verification, drift checks, and conflict blockers. | Allows durable writes only after verified Codex install, prevents unsupported lockfile mutation, records network/local delivery mode, and blocks destructive replacement on drift. | Spec R1-R8, R18-R23bj, R24-R61, R62-R66; plan M1-M3. | TLF-012 through TLF-027, CR3-F1 tests, package test suite. |
| `packages/rigorloop/test/cli.test.js` | Added lockfile fixtures and CLI tests for parsing, serialization, planned output, network/local lockfile writes, failure no-write behavior, unsupported shape, drift, missing output, and path conflicts. | Makes each lockfile `MUST` observable at the package boundary and protects the review findings from regression. | Test spec TLF-001 through TLF-029; AC1-AC13. | Focused M1, M2, M3 test patterns and full `npm test --prefix packages/rigorloop`. |
| `specs/rigorloop-cli-lockfile.md` | Added the accepted durable lockfile contract. | Defines the public lockfile shape, hash algorithm, source semantics, update behavior, failure behavior, compatibility, and non-goals before implementation writes durable state. | Proposal lockfile boundary; spec-review SR1-F1 and SR2-F1. | `spec-review-r3` approved. |
| `specs/rigorloop-cli-lockfile.test.md` | Added test mapping for lockfile requirements, milestones, and acceptance criteria. | Ensures the implementation has direct proof for schema, source modes, no-write failures, drift, exit classes, and package-local execution. | Test-spec stage after approved plan. | Approved by user before implementation. |
| `docs/architecture/system/architecture.md` and `docs/architecture/system/diagrams/container.mmd` | Updated the canonical architecture package for CLI lockfile responsibility and boundary. | Records that `rigorloop.lock` is downstream generated-output state, not canonical source, and that the CLI package owns only the approved lockfile-writing surface. | Architecture doc source-of-truth order; ADR. | `architecture-review-r1` approved. |
| `docs/adr/ADR-20260516-rigorloop-cli-lockfile.md` | Added durable lockfile boundary decision. | Captures why durable lockfile writes are now allowed, why local archive uses `source: local-archive`, why unknown fields block, and why `--force` is not a repair mechanism. | Architecture stage. | `architecture-review-r1` approved. |
| `docs/plans/2026-05-16-rigorloop-cli-lockfile.md` and `docs/plan.md` | Added and maintained the active execution plan and plan index state. | Split implementation into reviewable milestones and now records that all implementation milestones are closed with `explain-change` next. | Workflow plan policy. | Plan review approved; code-review-r2/r4/r5 closed M1-M3. |
| `docs/follow-ups.md` | Updated follow-up state around the lockfile slice. | Reflects that the durable lockfile follow-up became active work while other CLI follow-ups remain deferred. | Follow-up register workflow. | Validated through selected CI. |
| `docs/changes/2026-05-15-rigorloop-cli-lockfile/**` | Added change metadata, review records, review log, review resolution, and this explanation. | Provides durable lifecycle evidence for spec review, architecture review, plan review, code review, material finding resolution, validation, and rationale. | Workflow review-recording and explain-change requirements. | Review artifact validation and selected CI passed. |

## Tests Added Or Changed

- TLF-001 proves a complete valid `schema_version: 1` lockfile parses and serializes deterministically.
- TLF-003 proves dry-run includes planned lockfile output and writes nothing.
- TLF-004 through TLF-007 prove malformed, invalid, unknown, unsupported, and future lockfile shapes block or fail with the approved exit classes.
- TLF-008 proves manifest hash normalization is stable across line endings.
- TLF-012 proves network install writes `source: release-archive` with the approved lockfile fields.
- TLF-013 and TLF-014 prove local archive install writes `source: local-archive`, records only the basename, and avoids local path or machine-data leakage.
- TLF-015 proves reinstall through a different delivery mode updates the matching Codex entry after verification.
- TLF-020 and TLF-021 prove failed verification does not create or update `rigorloop.lock`.
- TLF-023 and TLF-024 prove drifted generated files block replacement and preserve both modified output and existing lockfile bytes.
- TLF-025 proves a missing generated output root represented in the lockfile blocks before replacement.
- TLF-026 and TLF-027 prove generated output file/directory conflicts exit with mutation-conflict behavior.
- CR1-F1 tests prove unknown nested mapping keys block before mutation.
- CR3-F1 tests prove extra, modified, or partial installed trees cannot be recorded as verified generated output.

The test level is package-level CLI testing because the behavior is externally observable through command output, exit codes, filesystem writes, and project files.

## Validation Evidence Available Before Final Verify

Implementation-stage and review-stage validation recorded in the active plan includes:

- `npm test --prefix packages/rigorloop -- --test-name-pattern 'TLF-'`
- `npm test --prefix packages/rigorloop`
- `npm test --prefix packages/rigorloop -- --test-name-pattern 'TLF-005|TLF-006|TLF-007'`
- `npm test --prefix packages/rigorloop -- --test-name-pattern 'CR3-F1|T26 adapter file|TLF-020|TLF-021'`
- `npm test --prefix packages/rigorloop -- --test-name-pattern 'TLF-023|TLF-024|TLF-025|TLF-026|TLF-027'`
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-cli-lockfile`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `bash scripts/ci.sh --mode explicit ...`
- `git diff --check -- ...`

The latest selected CI after code-review-r5 passed review artifact validation, artifact lifecycle validation, change metadata regression and validation, and `rigorloop_cli.test`.

Final `verify` has not run yet and is the next required owning stage after this explanation.

## Review Resolution Summary

Review resolution is recorded in `docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md`.

- Findings resolved: 4.
- Unresolved findings: 0.
- Accepted and resolved findings: `SR1-F1`, `SR2-F1`, `CR1-F1`, `CR3-F1`.
- Clean implementation reviews: `code-review-r2` approved M1, `code-review-r4` approved M2, and `code-review-r5` approved M3.

## Alternatives Rejected

- Keep planned-only lockfile output: rejected for this slice because the accepted lockfile spec now authorizes durable writes after verification.
- Treat local archive installs as `source: release-archive`: rejected because the lockfile records install delivery mode, while both modes still share the same official metadata trust model.
- Preserve unknown YAML fields in the first schema: rejected because unknown shape should block until migration or preservation behavior is specified.
- Let `--force` replace arbitrary lockfile state: rejected because it would erase durable generated-output state without an approved repair or recovery contract.
- Record whatever exists under `.agents/skills`: rejected after `CR3-F1` because the lockfile must record verified generated Codex output, not unrelated user files.

## Scope Control

This change does not add `new-change`, `status`, `validate`, lockfile migration or repair commands, workflow YAML lockfile entries, generated workflow docs lockfile entries, public npm publication, or lockfile writes for Claude/opencode adapters.

The lockfile remains downstream generated-output state only. Canonical workflow, skills, schemas, adapter metadata, and release evidence stay in repository-authored or release-evidence surfaces.

## Risks And Follow-Ups

- Lockfile write failure after adapter install can still leave generated output installed without recorded lockfile state. The CLI must report that failure explicitly; repair behavior needs a later spec.
- Changed-file lists for drift are not implemented; the current required blocker uses tree hash and file count. Path-level drift reporting remains optional future work under the spec's `SHOULD`.
- Lockfile migration, repair, `status`, `validate`, non-Codex adapters, and generated workflow output entries remain follow-ups.
- Public npm publication remains blocked until release hardening is specified and accepted.

## Current Readiness

All implementation milestones are closed. The active plan's next stage is `verify` after this `explain-change` artifact is recorded and validated. This explanation does not claim final verification, branch readiness, PR readiness, or hosted CI completion.
