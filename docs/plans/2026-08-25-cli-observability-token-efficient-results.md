# CLI Observability and Token-Efficient Results Execution Plan

## Purpose / big picture

Implement the approved local observability and result-projection contract without changing v0.4.x default output or allowing diagnostics to affect semantic command behavior. The work separates compatibility-sensitive result normalization from privacy- and concurrency-sensitive filesystem logging, then integrates both through one invocation controller and proves the measured adoption gate without enabling a default switch in this change.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-25-cli-observability-and-token-efficient-results.md`
- Spec: `specs/cli-observability-and-token-efficient-results.md`
- Architecture: `docs/architecture/system/architecture.md` and `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`
- Test spec: `specs/cli-observability-and-token-efficient-results.test.md` (pending)

## Context and orientation

The published Node package is authored directly under `packages/rigorloop/dist/`. `dist/bin/rigorloop.js` dispatches top-level commands, while `dist/lib/lifecycle-cli.js` owns lifecycle command execution and rendering. `dist/lib/command-result.js` owns shared exit classification. Existing tests under `packages/rigorloop/test/` protect CLI, lifecycle, transaction, and package behavior. `scripts/validate-governed-lifecycle-cli.py` is the only production Python wrapper covered by the feature; it consumes lifecycle JSON for repository validation.

The implementation must keep existing handlers semantically stable while moving rendering behind one normalized result boundary. The file sink is user-state-local and synchronous, uses only Node built-ins, and is isolated from repository transactions. The v0.5.0 default decision remains outside this implementation: M4 records whether the approved gate passes but keeps concise output opt-in in v0.4.x.

## Non-goals

- Do not change lifecycle transition, settlement, workflow routing, repository transaction, or exit-code semantics.
- Do not add telemetry, hosted forwarding, a database, daemon, network path, repository log, expiry index, or automatic workflow continuation.
- Do not change v0.4.x default human or JSON output and do not remove detailed output.
- Do not interpret local logs as review, lifecycle, validation, verification, CI, or release evidence.

## Requirements covered

- R21-R28 and BND-COMPOSE-001: M1 owns the shared result model, compatibility renderers, concise formats, field applicability, and single-output proof.
- R3-R20, R33-R34, BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, and BND-ENV-001: M2 owns logging configuration, privacy, path safety, event schema, sink, concurrency, rotation, and degraded behavior.
- R1-R5, R15-R20, R27-R28, R31-R32 and INT-001 through INT-004: M3 owns invocation integration, severity mapping, exact lookup, command-family coverage, wrapper consumption, and semantic isolation.
- R29-R31, INT-005, and BND-COMPAT-001: M4 owns the versioned profile corpus, v0.4.x baseline, complete-interaction measurement, adoption decision, docs, and release-facing proof.
- AC1-AC11: M1-M4 provide direct proof; M5 performs final lifecycle closeout without adding implementation scope.

## Milestones

### M1. Shared result model and compatibility projections

- Milestone kind: implementation
- Goal: Establish one semantic command-result representation and pure renderers while preserving every existing v0.4.x output and exit contract.
- Requirements: R21-R28, AC6, AC7, AC10
- Architecture decisions: ADR-20260825 shared internal result and compatibility-adapter decision
- Files/components likely touched:
  - `packages/rigorloop/dist/lib/command-result.js`
  - new package-local result projection module under `packages/rigorloop/dist/lib/`
  - `packages/rigorloop/dist/lib/lifecycle-cli.js`
  - `packages/rigorloop/dist/bin/rigorloop.js`
  - `packages/rigorloop/test/cli.test.js`
  - lifecycle result tests under `packages/rigorloop/test/`
- Dependencies:
  - Approved spec and ADR identities.
- Tests and proof:
  - Snapshot or structural fixtures for every existing human, `--json`, and lifecycle JSON path.
  - Table-driven concise field-applicability tests for success, blocked, invalid, and internal outcomes.
  - Shared-fact equivalence and one-stdout-emission tests.
- Implementation steps:
  - Add a closed internal result shape without changing command semantics.
  - Extract compatibility renderers before adding concise-human, concise-JSON schema v2, and detailed-JSON selectors.
  - Route lifecycle and top-level handlers through pure rendering while retaining existing aliases and defaults.
  - Reject unknown formats and fields through closed vocabularies with unknown-value regressions.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
- Expected observable result: Existing v0.4.x invocations retain their output and exit behavior; explicit concise and detailed formats project one semantic result with the required fields.
- Completion criteria: All current package tests and new projection/compatibility tests pass; no default format changes.
- Required evidence: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m1-result-model.md`
- Review handoff: code-review of the complete M1 diff, compatibility fixtures, and result-schema ownership.
- Optional commit boundary: `M1: centralize CLI result projection without default drift`
- Risks:
  - Refactoring handler output may duplicate stdout or alter an existing schema.
- Rollback/recovery:
  - Revert the M1 commit as one unit; no persisted log state or schema migration exists yet.

### M2. Privacy-safe bounded local logging core

- Milestone kind: implementation
- Goal: Implement strict logging configuration, allowlisted events, safe platform paths, synchronous append, rotation, and bounded concurrency independently of command integration.
- Requirements: R3-R17, R33, R34, AC1-AC4, AC8
- Architecture decisions: ADR-20260825 configuration, event-builder, synchronous-sink, containment, and lock decisions
- Files/components likely touched:
  - new logging configuration, event, sink, and observability modules under `packages/rigorloop/dist/lib/`
  - new unit and fault-injection tests under `packages/rigorloop/test/`
- Dependencies:
  - M1 internal result vocabulary supplies normalized safe facts.
- Tests and proof:
  - Closed severity, option precedence, ID grammar/randomness, schema, timestamp, duration, size, and command-family partitions.
  - Synthetic secret, path, environment, request, newline, and control-character absence across active and archived files.
  - Linux, macOS, and Windows path resolution fixtures plus symlink and permission refusal.
  - Concurrent writer, lock exhaustion, stale lock, interruption, disk-full, append, and every rotation boundary with complete JSON Lines proof.
- Implementation steps:
  - Build strict config resolution and random invocation identity using Node built-ins.
  - Build allowlist-only event construction with family extensions and 16 KiB fail-closed encoding.
  - Implement validated root creation, restrictive modes, non-following owned-path checks, and no implicit permission repair.
  - Implement per-event exclusive lock, five-file rotation, synchronous append, and non-recursive degraded reporting.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
- Expected observable result: Unit-level invocations can record complete safe events and degrade deterministically under every named filesystem or concurrency failure without touching repository state.
- Completion criteria: All event, privacy, path, concurrency, rotation, and fault-injection tests pass with no external dependency added.
- Required evidence: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md`
- Review handoff: code-review of M2 security, privacy, cross-platform path, concurrency, and recovery boundaries.
- Optional commit boundary: `M2: add bounded privacy-safe local logging core`
- Risks:
  - Cross-platform filesystem behavior may violate the no-follow or complete-line guarantee.
- Rollback/recovery:
  - Disable the unintegrated sink and revert M2. Test-created logs remain disposable temporary-fixture data.

### M3. Invocation integration, console policy, and log inspection

- Milestone kind: implementation
- Goal: Wrap every public command family in one invocation controller, expose safe log discovery and exact lookup, and preserve semantic results through direct and wrapper paths.
- Requirements: R1-R5, R15-R20, R27, R28, R31, R32, AC1, AC2, AC4, AC5, AC8, AC10, AC11
- Architecture decisions: ADR-20260825 invocation-controller and read-only inspection decisions
- Files/components likely touched:
  - `packages/rigorloop/dist/bin/rigorloop.js`
  - `packages/rigorloop/dist/lib/lifecycle-cli.js`
  - invocation orchestration and log-inspection modules under `packages/rigorloop/dist/lib/`
  - `scripts/validate-governed-lifecycle-cli.py`
  - CLI, lifecycle, and wrapper tests
- Dependencies:
  - M1 normalized results and M2 logging core.
- Tests and proof:
  - Start/completion and severity matrix for lifecycle, repository-setup, introspection, log-inspection, and invalid-input families.
  - Logging enabled, disabled, degraded, console-off, blocked mutation, validation error, unknown command, and unexpected-error end-to-end cases.
  - `logs path` and exact `logs show` found, missing, unavailable, corrupt-related, and corrupt-unrelated outcomes with no rerun.
  - Repository byte and exit-code equivalence with logging enabled, disabled, and failed.
  - Python wrapper single-output and aggregate exit-classification tests.
- Implementation steps:
  - Parse only strict logging controls before dispatch and install the invocation controller around `main()`.
  - Map normalized semantic outcomes to file severity and thresholded stderr without duplicating stdout.
  - Add read-only `logs path` and `logs show` commands against the bounded sink inventory.
  - Update the production Python wrapper to consume structured results once and keep concise successful output suppressed.
  - Prove a fresh checkout and lifecycle operation remain independent of logs.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-governed-lifecycle-cli-validator.py`
  - `python scripts/validate-governed-lifecycle-cli.py`
- Expected observable result: Every supported invocation is correlated and searchable by default, routine success remains quiet on stderr, and logging cannot alter semantic output, repository state, or exit status.
- Completion criteria: All command families and inspection outcomes have end-to-end proof; wrapper and lifecycle parity checks pass.
- Required evidence: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md`
- Review handoff: code-review of the complete public CLI, lookup, wrapper, and failure-isolation diff.
- Optional commit boundary: `M3: integrate observable CLI invocations and lookup`
- Risks:
  - Early parser failures or thrown errors may escape terminal-event recording or print duplicate diagnostics.
- Rollback/recovery:
  - Revert M3 to disconnect logging while retaining independently tested M1/M2 modules; local logs are disposable and need no migration.

### M4. Versioned token profile, adoption decision, and documentation

- Milestone kind: implementation
- Goal: Create deterministic complete-interaction measurements, record the v0.4.x baseline and result, document operation, and keep defaults unchanged unless a separately reviewed v0.5.0 decision is authorized.
- Requirements: R29-R31, AC6-AC10
- Architecture decisions: ADR-20260825 compatibility-gated adoption decision
- Files/components likely touched:
  - `packages/rigorloop/test/fixtures/observability/token-profiles-v1.json`
  - `docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json`
  - repository-owned measurement script and tests under `scripts/`
  - `packages/rigorloop/README.md`
  - release-facing validation selection only when required by changed-path ownership
- Dependencies:
  - M3 complete direct and wrapper interactions.
- Tests and proof:
  - Exact six-profile fixture vocabulary, normalized byte accounting, baseline identity, unweighted median, per-profile regression, one-pass continuation, and fixture-version drift tests.
  - Human examples for default quiet success, warning lookup, console-off, no-file-log, and explicit concise/detailed formats.
  - Packed-package smoke proving logs and formats are present in the published package surface.
- Implementation steps:
  - Add the v1 profile manifest and immutable v0.4.x detailed baseline.
  - Implement deterministic measurement over stdout, stderr, and required follow-up interactions.
  - Record pass/fail for the 30% median, 10% per-profile, field, and no-lookup gates without changing v0.4.x defaults.
  - Document configuration, platform paths, rotation, severity, lookup, privacy, and recovery behavior.
  - Run changed-path selection and add only the validation routing demanded by existing ownership rules.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/select-validation.py --mode explicit --path packages/rigorloop --path scripts/validate-governed-lifecycle-cli.py --path docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json --path packages/rigorloop/test/fixtures/observability/token-profiles-v1.json`
  - the exact measurement command defined by the approved test specification
  - `bash scripts/release-verify.sh v0.4.1`
- Expected observable result: A reproducible report states whether concise defaults qualify for v0.5.0, while the shipped v0.4.x defaults remain unchanged and users can operate the new logging surface from package documentation.
- Completion criteria: Profile and package validation pass; measurement includes all follow-ups; no unauthorized default switch or release mutation occurs.
- Required evidence: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md`
- Review handoff: code-review of benchmark integrity, documentation truth, package contents, and compatibility claim boundaries.
- Optional commit boundary: `M4: prove CLI token and package compatibility`
- Risks:
  - A favorable fixture or omitted follow-up could overstate savings.
- Rollback/recovery:
  - Preserve the baseline as historical evidence, keep concise formats opt-in, and revert only measurement or docs defects; no runtime default depends on a failed gate.

### M5. Final lifecycle closeout

- Milestone kind: lifecycle-closeout
- Goal: Reconcile all milestone reviews and evidence, explain the complete change, run final verification, and prepare PR handoff only after implementation is complete.
- Requirements: AC1-AC11
- Architecture decisions: none
- Files/components likely touched:
  - change-local review, explanation, verification, and routing evidence only
- Dependencies:
  - M1-M4 implementation milestones closed with clean code review and any material findings resolved.
- Tests and proof:
  - Final holistic code review over the complete implementation range.
  - Selected validation, lifecycle consistency, review closeout, package, and release-safety proof from the test specification.
- Implementation steps:
  - Reconcile milestone evidence and material findings.
  - Run final code review, explain-change, verify, and PR stages under their own authorities.
- Validation commands:
  - Commands selected by the approved test specification and final `verify` stage.
- Expected observable result: The branch has coherent artifact-to-code-to-test evidence and a truthful PR handoff.
- Completion criteria: Final review and verification are recorded with no unresolved blockers; PR preparation remains a separate stage-owned action.
- Required evidence: stage-owned final review, `explain-change.md`, verification evidence, and PR summary.
- Review handoff: final holistic code-review, then explain-change and verify.
- Optional commit boundary: `M5: close CLI observability lifecycle evidence`
- Risks:
  - Closeout could reuse stale identities after a late correction.
- Rollback/recovery:
  - Pause, invalidate stale evidence, rerun the owning review or validation, and do not claim PR readiness.

## Validation plan

- `npm test --prefix packages/rigorloop`: package behavior, lifecycle, logging, projection, concurrency, lookup, and compatibility proof.
- `python scripts/test-governed-lifecycle-cli-validator.py`: production wrapper behavior and structured child-result consumption.
- `python scripts/validate-governed-lifecycle-cli.py`: repository-wide governed lifecycle compatibility.
- `python scripts/select-validation.py --mode explicit ...`: existing changed-path ownership and exact required-check selection.
- `bash scripts/release-verify.sh v0.4.1`: packed package and release-surface compatibility without publication.
- Test-spec-owned measurement command: exact six-profile byte and continuation gate.

## Risks and recovery

- Risk: Diagnostic logging changes semantic behavior under failure.
  - Recovery: Keep the sink behind a non-throwing boundary, prove byte/exit equivalence, and disable file logging without reverting semantic handlers.
- Risk: Privacy leaks through debug, parser, corrupt-line, or error paths.
  - Recovery: Fail event construction closed from an allowlist, use synthetic-secret tests across every retained and rendered surface, and block release on any leak.
- Risk: Concurrent rotation corrupts logs or touches external paths.
  - Recovery: Serialize all owned-file operations under the bounded lock, use temporary fixture roots for fault injection, and revert M2/M3 if containment proof fails.
- Risk: Result normalization drifts current users or wrappers.
  - Recovery: Preserve old renderers as compatibility adapters and revert M1 independently before logging integration.
- Risk: Token targets incentivize missing semantics.
  - Recovery: Field and one-pass gates override byte reduction; keep concise output opt-in whenever any gate fails.

## Dependencies

- Node runtime and the existing `@xiongxianfei/rigorloop` package boundary; no new production dependency is approved.
- Existing lifecycle and command-result contracts remain authoritative for semantic behavior and exit classes.
- The test specification must map every MUST, boundary, interaction, and acceptance criterion before M1 implementation.
- Milestones execute in order because M2 consumes normalized facts, M3 composes M1/M2, and M4 measures complete M3 interactions.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-25 | Isolate result normalization in M1 before filesystem logging. | Compatibility failures can be reviewed and rolled back independently of persistence and concurrency. | One large end-to-end logging milestone. |
| 2026-08-25 | Combine configuration, event privacy, append, and rotation in one logging-core milestone. | They share the same containment and degraded-observability invariant and cannot be safely integrated separately. | Per-module milestones that would not yield an independently valid sink. |
| 2026-08-25 | Integrate all command families and log inspection in M3. | Start/completion, severity, single output, and lookup require the same invocation controller and end-to-end fixtures. | Lifecycle-only integration followed by divergent top-level wrappers. |
| 2026-08-25 | Record adoption evidence without changing v0.4.x defaults. | The spec reserves default replacement for v0.5.0 and requires measured proof first. | Immediate concise-default migration. |

## Readiness

- See the owning change record for current workflow state.
