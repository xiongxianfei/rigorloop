# CLI observability and token-efficient results test specification

## Owning change record

`docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

## Related spec and plan

- Spec: `specs/cli-observability-and-token-efficient-results.md`
- Plan: `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/cli-observability-and-token-efficient-results.md` | `spec` (`sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029`) | `spec-review-r2`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/spec-review-r2.md` |
| Architecture | `docs/architecture/system/architecture.md` | canonical owner `2026-08-24-governed-lifecycle-cli`, artifact `architecture` (`sha256:427828a44dd25d63f18e07c99eb4055330a26961f5de8d8297545a7d6455c6e7`) | Canonical `architecture-review-r4`; feature applicability `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/architecture-review-r1.md` |
| ADR | `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md` | `adr-cli-observability` (`sha256:8df259dc5e97efa06535f785c25d575c366e2864b1fd88abde96fba6075b4fd4`) | `architecture-review-r1`; accepted |
| Execution plan | `docs/plans/2026-08-25-cli-observability-token-efficient-results.md` | `plan` (`sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2`) | `plan-review-r3`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/plan-review-r3.md` |

## Testing strategy

Use pure renderer and event-builder contract tests first, then filesystem integration tests with temporary state roots, injected clocks, injected entropy, injected filesystem failures, and real child-process concurrency. End-to-end CLI tests exercise every command family and result channel. Characterization fixtures freeze v0.4.x output before new projections are added. A versioned six-profile harness measures complete agent interactions, including required follow-up commands, without treating reduced bytes as permission to omit continuation facts.

All proof is automated. Each implementation milestone introduces its tests before production behavior and must pass its focused commands plus the package regression command before review. Filesystem tests may write only to disposable temporary directories; governed-state equivalence tests compare repository bytes before and after enabled, disabled, and degraded logging. Environment-sensitive wall-clock timing is reported but never serves as the sole correctness assertion.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T06, T07 | integration | Exactly one start and terminal attempt; interruption permits start-only. |
| R2 | T01, T06 | contract, integration | Closed family vocabulary and release conformance for every public command. |
| R3 | T02, T06 | contract, integration | Closed severities and default thresholds. |
| R4 | T06 | end-to-end | Success, blocked, policy rejection, and internal failure severity/console matrix. |
| R5 | T02, T06 | contract, integration | Schema 1 common and completion fields. |
| R6 | T02 | contract | Grammar, uniqueness, and independence from supplied data. |
| R7 | T02 | contract | Family-specific allowlist and lifecycle-only extension refusal. |
| R8 | T03, T09 | contract, integration | Synthetic prohibited values are absent from all retained and rendered surfaces. |
| R9 | T02, T03 | contract | Control-character handling and bounded replacement event. |
| R10 | T04 | contract | Injected Linux, macOS, and Windows platform defaults. |
| R11 | T04, T05 | integration | Absolute override, component symlink refusal, containment, and path omission. |
| R12 | T04 | integration | Creation modes and refusal without permission repair. |
| R13 | T05 | integration | Pre-append rotation, five-file bound, and contained rename/delete. |
| R14 | T05 | integration | Complete concurrent JSONL, bounded acquisition, stale-lock degradation. |
| R15 | T05, T07, T08 | integration, end-to-end | Diagnostic failure preserves semantic result and emits one bounded fallback. |
| R16 | T01, T07, T17 | integration, smoke | Default on, flag/env disablement, semantic parity, and shipped option surface. |
| R17 | T01 | contract | Closed levels, CLI precedence, pre-dispatch failure, no raw value capture. |
| R18 | T08, T17 | end-to-end, smoke | Human/JSON path discovery is read-only, safely fails, and ships in the package. |
| R19 | T08, T17 | end-to-end, smoke | Exact grammar, five-file search, distinct stable outcomes, and packaged lookup. |
| R20 | T08 | end-to-end | No rerun, no recursive result inclusion, safe corrupt-line behavior. |
| R21 | T10 | contract | v0.4.x default output and JSON characterization. |
| R22 | T10, T11, T17 | contract, smoke | Explicit concise/detailed formats, legacy alias, and shipped help/package surface. |
| R23 | T11 | contract | Schema 2 closed applicability matrix and compact omission rules. |
| R24 | T11 | contract | Two-line human bound with required textual facts. |
| R25 | T11, T15 | contract, integration | One-pass next-operation sufficiency without inventories. |
| R26 | T10, T11 | contract | Complete detailed semantics and compatibility retention. |
| R27 | T11, T12 | contract, integration | Shared-fact, mutation, code, exit, and single-emission parity. |
| R28 | T07, T11, T16 | integration | Closed observability projection is diagnostic and non-authorizing. |
| R29 | T15 | integration | Exact profile vocabulary, immutable baseline identity, complete byte accounting. |
| R30 | T15 | integration | Median, per-profile, field, one-pass, version-drift, and no-default-switch gates. |
| R31 | T13 | integration | Wrapper preserves exit classification and suppresses duplicate success output. |
| R32 | T12, T14 | integration | Repository equivalence and fresh-checkout reconstruction without logs. |
| R33 | T02, T05 | contract, integration | UTC millisecond timestamp, monotonic integer duration, isolated clock failure. |
| R34 | T05, T08 | contract, integration | Fixed work and lookup inventories plus network, database, process, and open-handle guards. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T06, T10 | Default lifecycle status preserves output, keeps stderr quiet, and records correlated info events. |
| E2 | T11 | Changes-requested settlement retains all continuation-critical concise fields without inventory. |
| E3 | T06 | Expected governance rejection is warning in file and quiet on default stderr. |
| E4 | T07, T12 | Unwritable logging produces one fallback while semantic bytes, mutation, and exit stay equal. |
| E5 | T08 | Exact lookup returns only validated events and cannot execute lifecycle operations. |
| E6 | T05 | Boundary-crossing append rotates only the five owned names or degrades safely. |
| E7 | T15 | A 25% median result fails adoption and leaves defaults unchanged. |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 | T07 | Start remains complete JSON; no completion is invented after termination. |
| EC2 | T02, T03 | Oversized input is absent and one bounded safe error event replaces it. |
| EC3 | T04 | Symlinked root or component produces `RL_LOG_UNSAFE_PATH` and no fallback file. |
| EC4 | T05, T12 | Disk-full rotation preserves external paths and semantic behavior. |
| EC5 | T08 | Rotated-away valid ID is indistinguishable from never-recorded and returns only `RL_LOG_NOT_FOUND`. |
| EC6 | T06 | Console `off` suppresses stderr while file events remain searchable. |
| EC7 | T07 | No-file-log creates no file, keeps success quiet, and reports `disabled` only in new projections. |
| EC8 | T06 | Unknown command is `invalid-input` with a stable code and no raw token. |
| EC9 | T07 | Initialization failure makes no recorded claim and emits at most one safe fallback. |
| EC10 | T08 | Newer event schema is skipped as unsupported, never partially interpreted. |
| EC11 | T10, T12 | Detailed semantics and exit remain available while observability is degraded. |
| EC12 | T01 | A public command without a family fails the closed conformance table. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R2, R6, R7, R8, R9, R11, R15, R17, R18, R19, R20 | BND-INPUT-001 | T01, T02, T03, T04, T06, T08 | contract | automated | C01, C02, C03 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md` | M3 | - | - |
| PRF-002 | covered | R1, R13, R14, R15, R16, R18, R19, R20, R28, R32 | BND-STATE-001 | T05, T07, T08, T12, T14 | integration | automated | C01, C03, C05 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md` | M3 | - | - |
| PRF-003 | covered | R6, R7, R8, R11, R15, R18, R19, R20, R28, R32 | BND-AUTH-001 | T02, T03, T04, T08, T12, T14, T16 | integration | automated | C01, C03, C05 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md` | M3 | - | - |
| PRF-004 | covered | R1, R2, R3, R4, R5, R15, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31 | BND-COMPOSE-001 | T06, T07, T10, T11, T12, T13, T15 | end-to-end | automated | C01, C03, C04, C06 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | M4 | - | - |
| PRF-005 | covered | R1, R13, R14, R15, R19, R33 | BND-TEMPORAL-001 | T02, T05, T07, T08 | integration | automated | C01, C03 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md` | M2 | - | - |
| PRF-006 | covered | R9, R13, R14, R15, R19, R20, R32, R33 | BND-RECOVERY-001 | T02, T03, T05, T07, T08, T12, T14 | integration | automated | C01, C03, C05 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md` | M3 | - | - |
| PRF-007 | covered | R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31 | BND-COMPAT-001 | T10, T11, T13, T15, T17 | contract | automated | C01, C04, C06, C08, C10 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | M4 | - | - |
| PRF-008 | covered | R8, R10, R11, R12, R13, R14, R15, R16, R21, R22, R27, R31, R34 | BND-ENV-001 | T03, T04, T05, T07, T08, T10, T12, T13, T17 | integration | automated | C01, C03, C04, C05, C08 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | M4 | - | - |
| PRF-009 | covered | R8, R11, R15 | INT-001 | T03, T04, T07, T12 | integration | automated | C01, C03 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md` | M3 | - | - |
| PRF-010 | covered | R13, R14, R15 | INT-002 | T05, T12 | integration | automated | C01, C03 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md` | M2 | - | - |
| PRF-011 | covered | R21, R22, R27, R31 | INT-003 | T10, T11, T13 | end-to-end | automated | C01, C04 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | M4 | - | - |
| PRF-012 | covered | R19, R20, R32 | INT-004 | T08, T14 | end-to-end | automated | C01, C03, C05 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md` | M3 | - | - |
| PRF-013 | covered | R29, R30 | INT-005 | T15 | integration | automated | C06, C10 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | M4 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | `npm test --prefix packages/rigorloop` | existing/configured | package maintainers | cross-milestone | every implementation milestone review | nonzero blocks the milestone | zero tests is failure | milestone evidence report | package tests use temporary roots; no publication |
| C02 | `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` | planned-for-implementation | implement | M1-M3 | owning milestone review | nonzero blocks the owning milestone | zero tests is failure | M1-M3 focused test output | temporary repositories and log roots only |
| C03 | `python scripts/test-governed-lifecycle-cli-validator.py` | existing/configured | wrapper maintainers | M3 | M3 code review | nonzero blocks M3 | zero tests is failure | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md` | local child processes and temporary repositories |
| C04 | `python scripts/test-select-validation.py` | existing/configured | validation selector maintainers | M3-M4 | M3 and M4 code review | nonzero blocks the owning milestone | zero tests is failure | M3/M4 evidence report | selector fixtures only |
| C05 | `python scripts/validate-governed-lifecycle-cli.py` | existing/configured | workflow maintainers | M3-M5 | M3 and final closeout | nonzero blocks progression | not applicable | governed lifecycle validation output | repository validation; no mutation intended |
| C06 | `python scripts/measure-cli-result-bytes.py --profiles packages/rigorloop/test/fixtures/observability/token-profiles-v1.json --baseline docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json --check` | planned-for-implementation | implement | M4 | M4 code review | nonzero, missing profile, failed field gate, or failed continuation gate blocks adoption evidence | zero measured profiles is failure | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | local fixtures and child CLI processes; does not change defaults |
| C07 | `python scripts/select-validation.py --mode explicit --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/command-result.js --path packages/rigorloop/dist/lib/result-renderer.js --path packages/rigorloop/dist/lib/log-config.js --path packages/rigorloop/dist/lib/diagnostic-event.js --path packages/rigorloop/dist/lib/log-sink.js --path packages/rigorloop/dist/lib/cli-observability.js --path packages/rigorloop/dist/lib/log-inspection.js --path packages/rigorloop/dist/lib/lifecycle-cli.js --path packages/rigorloop/test/cli-observability.test.js --path packages/rigorloop/test/result-renderer.test.js --path scripts/validate-governed-lifecycle-cli.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json --path packages/rigorloop/test/fixtures/observability/token-profiles-v1.json` | existing/configured | validation selector maintainers | M4 | M4 code review | nonzero or `manual-routing-required` blocks M4 | not applicable | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | read-only changed-path selection |
| C08 | `python scripts/test-npm-package-publication.py NpmPackagePublicationTests.test_packed_package_observability_surface_matches_documentation` | planned-for-implementation | implement | M4 | M4 code review | nonzero blocks M4 package-surface proof | zero tests is failure | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | packs and installs locally in a disposable directory; no publication |
| C09 | `python scripts/validate-boundary-first.py --path specs/cli-observability-and-token-efficient-results.md --path specs/cli-observability-and-token-efficient-results.test.md` | existing/configured | test-spec | authoring | test-spec-review | nonzero blocks test-spec handoff | not applicable | test-spec authoring validation output | structural validation only |
| C10 | `python scripts/test-cli-result-measurement.py` | planned-for-implementation | implement | M4 | M4 code review | nonzero blocks M4 and token-adoption evidence | zero tests is failure | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | deterministic calculation and fixture tests; no default mutation |
| C11 | `bash scripts/ci.sh --mode broad-smoke --jobs 2` | ci-owned | repository CI maintainers | M5 | final verification | nonzero blocks final verification | selected zero-test checks fail | final verification evidence | broad local repository validation; tag-specific release verification remains release-owned |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T01, T10, T11 | none | C01, C02 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m1-result-model.md` | M1 code review | Characterization passes before refactoring; new projection cases first fail for missing behavior. |
| M2 | T02, T03, T04, T05 | none | C01, C02 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md` | M2 code review | Real child processes prove writer concurrency; injected adapters prove platform and fault partitions. |
| M3 | T06, T07, T08, T09, T12, T13, T14, T16 | none | C01, C02, C03, C04, C05 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md` | M3 code review | All public families, wrapper paths, privacy surfaces, and semantic isolation close here. |
| M4 | T15, T17 | none | C01, C04, C06, C07, C08, C10 | `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md` | M4 code review | Gate records pass/fail without changing v0.4.x defaults; packed commands and documentation examples are exercised. |
| M5 | T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17 | none | C01, C03, C04, C05, C06, C07, C08, C10, C11 | final stage-owned review and verification evidence | final verification | Reuses current milestone evidence only after identity and review freshness checks, then runs broad repository smoke; immutable tag verification remains a release-preparation gate. |

## Test cases

### T01. Closed configuration, family, and projection vocabularies

- Covers: R2, R16, R17, R21, R22, EC12, BND-INPUT-001
- Level: contract
- Command IDs: C01, C02
- Fixture/setup: Table of every allowed and unknown command family, severity, environment value, flag value, projection, and option/environment conflict.
- Steps: Resolve each configuration partition before dispatch, enumerate every public command through the family classifier, and request every known and unknown projection.
- Expected result: Known values normalize deterministically, CLI flags override environment values, unknown values fail closed with stable codes, and every public command has exactly one family.
- Failure proves: An open vocabulary, ambiguous precedence, or unclassified command can bypass the contract.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m1-result-model.md`
- Automation location: `packages/rigorloop/test/result-renderer.test.js`, `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M1 and M3

### T02. Event schema, identity, clock, size, and family allowlist

- Covers: R3, R5-R7, R9, R33, EC2, BND-INPUT-001, BND-TEMPORAL-001
- Level: contract
- Command IDs: C01, C02
- Fixture/setup: Injected deterministic clock, monotonic source, entropy source, every family extension, control strings, and 16 KiB boundary values.
- Steps: Build start and completion events for each family; repeat identities across independent invocations; cross the size and clock-failure boundaries.
- Expected result: Schema and fields are exact, IDs match the grammar and differ independently, lifecycle extensions do not escape their family, time fields are valid, and oversize or clock failure yields only a bounded safe degraded event.
- Failure proves: Events are open-ended, identifying, malformed, oversized, or coupled to an unreliable wall clock.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M2

### T03. Privacy and normalization across every retained surface

- Covers: R8, R9, AC8, EC2, BND-INPUT-001, BND-AUTH-001, BND-RECOVERY-001, BND-ENV-001, INT-001
- Level: integration
- Command IDs: C01, C02
- Fixture/setup: Unique synthetic credential, argv token, request body, fingerprint, remote URL, username, hostname, absolute repository path, newline, control character, and stack text in every admitted failure source.
- Steps: Exercise success, blocked, invalid, internal, unsafe-path, oversized, corrupt-line, rotation, debug, info, warning, and error paths; search stdout, stderr, active log, archives, and lookup output byte-for-byte.
- Expected result: Prohibited values and unsafe derivatives are absent everywhere; only allowlisted normalized fields remain.
- Failure proves: A diagnostic or recovery path leaks private or unbounded caller data.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M2

### T04. Platform path, containment, symlink, and permission policy

- Covers: R10-R12, R18, EC3, BND-INPUT-001, BND-AUTH-001, BND-ENV-001, INT-001
- Level: integration
- Command IDs: C01, C02
- Fixture/setup: Injected Linux, macOS, and Windows platform/environment adapters plus POSIX temporary roots with absent, safe, broad-mode, relative, escaping, root-symlink, component-symlink, file-symlink, and lock-symlink partitions.
- Steps: Resolve defaults and overrides, initialize each path, inspect created modes, and repeat against pre-existing entries.
- Expected result: Defaults match the platform contract; unsafe entries fail without fallback or permission repair; all owned paths stay under the resolved root; created POSIX entries are `0700`/`0600`.
- Failure proves: Logging can escape containment, follow a symlink, expose a repository path, or silently modify user permissions.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M2

### T05. Rotation, concurrent writers, lock bounds, and filesystem faults

- Covers: R13-R15, R33, R34, AC3, EC4, E6, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001, INT-002
- Level: integration
- Command IDs: C01, C02
- Fixture/setup: Temporary roots at every size boundary, real child-process writers, deterministic lock-attempt clock, live and stale locks, disk-full, short-write, rename, fsync, append, and interruption fault points, a sentinel outside the root, denied network/process adapters, loaded-module inspection, and an open-handle probe.
- Steps: Append below/at/above the boundary, contend and rotate from multiple processes, exhaust ten attempts and 1,000 ms, inject each fault, count ordinary-path filesystem operations, deny network connection and external-process creation, inspect the loaded module graph for database clients, assert no persistent handle survives completion, then parse retained records and inspect the sentinel.
- Expected result: At most five owned files exist; every retained line is complete; no outside path changes; lock work is bounded; the ordinary path performs only directory validation and two appends; lookup is filesystem-only; no network, database, daemon, child process, or surviving background handle is used; failures degrade only observability and never remove an unowned lock.
- Failure proves: Rotation or concurrency can corrupt diagnostics, escape containment, block unboundedly, or alter semantic operation behavior.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M2

### T06. Public invocation family, severity, threshold, and channel matrix

- Covers: R1-R5, R17, AC1, AC2, E1, E3, EC6, EC8, BND-INPUT-001, BND-COMPOSE-001
- Level: end-to-end
- Command IDs: C01, C02
- Fixture/setup: One public invocation for lifecycle, repository-setup, introspection, log-inspection, and invalid-input, crossed with success, ordinary blocked, expected rejection, and unexpected-error outcomes and each threshold.
- Steps: Run each child process, capture stdout/stderr, parse retained events, and compare sequence, family, severity, status, code, and exit.
- Expected result: Exactly one start and completion attempt per initialized invocation, deterministic severity, default quiet success/blocked behavior, no console duplication, and safe invalid-input recording.
- Failure proves: A public path escapes correlation, severity policy, or single-output ownership.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M3

### T07. Disabled, degraded, interrupted, and initialization-failure behavior

- Covers: R1, R15, R16, R28, EC1, EC7, EC9, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001, INT-001
- Level: end-to-end
- Command IDs: C01, C02
- Fixture/setup: Successful semantic commands with enabled, `--no-file-log`, environment-off, console-off, unwritable, unsafe, interrupted-after-start, and initialization-failure sinks.
- Steps: Execute each case and compare stdout, repository bytes, semantic exit, stderr count, retained records, and projection observability.
- Expected result: Semantic facts are identical; observability is exact; failures produce at most one non-recursive fallback unless console is off; interruption invents no completion.
- Failure proves: Diagnostic availability affects command truth or creates misleading evidence.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M3

### T08. Read-only log path and exact lookup outcomes

- Covers: R18-R20, R34, AC5, E5, EC5, EC10, BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, INT-004
- Level: end-to-end
- Command IDs: C01, C02
- Fixture/setup: Five retained files containing exact-ID events, other IDs, valid missing IDs, malformed IDs, corrupt related/unrelated lines, and a newer schema; repository mutation sentinels and a command spy.
- Steps: Run `logs path` in both formats and `logs show` for every partition, counting opened owned names and checking command-spy/repository state.
- Expected result: Lookup scans only five names, returns only validated exact events, distinguishes stable outcomes, emits bounded warnings for unrelated corruption, and never reruns or reconstructs a command.
- Failure proves: Inspection is broad, mutating, recursive, unsafe, or claims unknowable history.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M3

### T09. Synthetic-secret regression over active and rotated logs

- Covers: R8, AC8
- Level: integration
- Command IDs: C01, C02
- Fixture/setup: Generated unique synthetic secret supplied through every prohibited source while enough safe events force four rotations.
- Steps: Execute all command families and failures, rotate, run lookup, then scan every output and owned file.
- Expected result: The synthetic secret and its raw containing values occur zero times.
- Failure proves: A composed invocation or archive path bypasses event allowlisting.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M3

### T10. v0.4.x output characterization and detailed compatibility

- Covers: R21, R22, R26, AC6, E1, EC11, BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001
- Level: contract
- Command IDs: C01, C02
- Fixture/setup: Checked-in whitespace-normalized fixtures for every existing default human, top-level `--json`, and lifecycle `--format json` success and failure result.
- Steps: Run the unchanged commands before and after renderer extraction; compare parsed JSON, normalized human text, exit status, and explicit `detailed-json` output.
- Expected result: Existing defaults and aliases remain semantically identical in v0.4.x; explicit detailed output is complete.
- Failure proves: Result normalization introduced a compatibility regression.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m1-result-model.md`
- Automation location: `packages/rigorloop/test/result-renderer.test.js`
- Required by milestone: M1

### T11. Concise field applicability, shape, and shared-fact equivalence

- Covers: R22-R28, AC6, AC7, E2, BND-COMPOSE-001, BND-COMPAT-001, INT-003
- Level: contract
- Command IDs: C01, C02
- Fixture/setup: One internal result for every applicable/omitted concise field across success, blocked, invalid, stale, unexpected, mutation, and read outcomes.
- Steps: Render concise JSON, concise human, and detailed JSON; validate the closed matrix, compact encoding, line count, safe next operation, omitted empty values, and all shared facts.
- Expected result: Schema 2 contains exactly applicable fields; concise human is at most two non-empty lines; detailed information remains complete; all shared facts and exits agree.
- Failure proves: Concision loses continuation authority, invents facts, leaks detail, or diverges from the semantic result.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m1-result-model.md`
- Automation location: `packages/rigorloop/test/result-renderer.test.js`
- Required by milestone: M1

### T12. Logging-state semantic and repository-byte equivalence

- Covers: R15, R27, R32, AC4, AC11, E4, EC4, EC11, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001, INT-001, INT-002
- Level: integration
- Command IDs: C01, C02
- Fixture/setup: Identical temporary governed repositories and request inputs with recorded, disabled, unsafe-path, disk-full, rotation-failure, and lock-exhaustion diagnostic states.
- Steps: Run the same read and mutation in every state; compare semantic stdout after removing only the new observability field, exit class, repository tree bytes, and lifecycle result.
- Expected result: All semantic and repository results are identical; only the diagnostic projection and permitted fallback differ.
- Failure proves: Logging has become a transaction participant or lifecycle authority.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M3

### T13. Production Python wrapper single-consumption parity

- Covers: R27, R31, AC10, BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001, INT-003
- Level: integration
- Command IDs: C03, C04
- Fixture/setup: Child lifecycle results for success, blocked, usage, invalid repository, stale operation, and internal error in existing detailed and explicit concise structured formats.
- Steps: Run the production wrapper and capture output and exit classification; count successful child stdout occurrences.
- Expected result: The wrapper consumes structured output once, preserves every semantic exit classification, emits no duplicate successful stdout, and does not require a log lookup.
- Failure proves: Wrapper composition changes command meaning or defeats token savings.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md`
- Automation location: `scripts/test-governed-lifecycle-cli-validator.py`
- Required by milestone: M3

### T14. Fresh-checkout lifecycle reconstruction and non-authority

- Covers: R32, AC11, BND-STATE-001, BND-AUTH-001, BND-RECOVERY-001, INT-004
- Level: integration
- Command IDs: C01, C05
- Fixture/setup: A fresh temporary checkout without user-state logs plus adversarial copied log events claiming approval, settlement, and revisions outside the checkout.
- Steps: Derive status, attempt governed settlement using repository evidence only, then repeat with absent, copied, and contradictory local logs.
- Expected result: Status and transition eligibility depend only on tracked repository artifacts; logs and observability fields grant no authority.
- Failure proves: Machine-local diagnostics became governed truth.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M3

### T15. Versioned complete-interaction token adoption gate

- Covers: R25, R29, R30, AC9, E7, BND-COMPOSE-001, BND-COMPAT-001, INT-005
- Level: integration
- Command IDs: C06, C10
- Fixture/setup: Exact six-profile v1 manifest, immutable v0.4.x detailed baseline, pass/fail threshold fixtures, missing/renamed/added/changed profile fixtures, and required-field/lookup spies.
- Steps: Measure normalized stdout plus stderr plus every required follow-up; calculate six per-profile reductions and their unweighted median; enforce growth, field, no-lookup, and fixture-identity gates.
- Expected result: Only an unchanged profile set meeting all gates reports eligible; 25% median, more than 10% growth, missing fields, required lookup, or fixture drift reports ineligible and never changes defaults.
- Failure proves: The project can claim token savings by omitting interaction cost or continuation facts.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md`
- Automation location: `scripts/test-cli-result-measurement.py`, `scripts/measure-cli-result-bytes.py`
- Required by milestone: M4

### T16. Observability projection cannot authorize lifecycle operations

- Covers: R28, R32, AC11, BND-AUTH-001
- Level: integration
- Command IDs: C01, C05
- Fixture/setup: Valid and invalid lifecycle requests augmented with every `observability` value and forged invocation IDs in caller-controlled data.
- Steps: Attempt validation, recording, and settlement with each diagnostic value and compare lifecycle decisions to the unaugmented requests.
- Expected result: Unknown request fields fail closed where applicable; otherwise diagnostic state is ignored as authority and never changes settlement eligibility.
- Failure proves: A diagnostic correlation field crossed into lifecycle authorization.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md`
- Automation location: `packages/rigorloop/test/cli-observability.test.js`
- Required by milestone: M3

### T17. Packed CLI surface and documented operations

- Covers: R16, R18, R19, R22, AC5-AC7, AC10, BND-COMPAT-001, BND-ENV-001
- Level: smoke
- Command IDs: C08
- Fixture/setup: Locally packed `@xiongxianfei/rigorloop` archive installed into a disposable directory, package README examples, isolated user-state root, and no repository-local dependency resolution.
- Steps: Run packaged help and version output; execute documented default logging, console-off, no-file-log, `logs path`, exact `logs show`, concise-human, concise-json, detailed-json, and legacy JSON examples; compare documented flags and outcomes with executable help and result schemas.
- Expected result: The published package contains every required command and renderer; documented examples execute with the specified channels and formats; legacy formats remain available; no example depends on the source checkout or changes defaults.
- Failure proves: Repository tests pass while the distributed package or user guidance omits or misstates the supported observability surface.
- Evidence artifact: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m4-token-and-package-proof.md`
- Automation location: `python scripts/test-npm-package-publication.py NpmPackagePublicationTests.test_packed_package_observability_surface_matches_documentation`
- Required by milestone: M4

## Fixtures and data

- `packages/rigorloop/test/fixtures/observability/token-profiles-v1.json` owns exactly the six R29 complete-interaction profiles and their required continuation fields.
- `docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json` owns immutable normalized baseline bytes and fixture identity for those profiles.
- Package-local fixtures cover existing v0.4.x output, command families, concise applicability, event-schema partitions, rotation sizes, corruption, and synthetic private values.
- Filesystem and governed-repository fixtures are created under per-test temporary directories. No test writes to the real platform user-state directory.
- Injected platform, environment, clock, monotonic, entropy, and filesystem adapters make cross-platform and failure partitions deterministic. Real child processes are used where lock and append concurrency itself is the behavior under proof.

## Mocking/stubbing policy

Mock only external nondeterminism and fault surfaces: time, entropy, platform path selection, environment access, and filesystem failure points. Do not mock event validation, containment, rotation ordering, result projection, lifecycle transition evaluation, child-process exit classification, or public CLI parsing when those behaviors are under proof. Concurrency proof must use actual processes sharing one temporary log root.

## Migration or compatibility tests

T10 freezes v0.4.x output and alias behavior. T15 treats any profile or fixture change as a new benchmark version and baseline. Lookup tests skip an unsupported newer event schema as a whole. No repository migration is expected because diagnostic state is external and disposable; fresh-checkout proof verifies that assumption.

## Observability verification

T02 and T06 validate schema, timestamps, sequence, family, severity, thresholds, and correlation. T05 validates bounded retention and concurrency. T07 validates disabled and degraded states. T08 validates safe discovery and lookup. T12 proves that observability remains semantically isolated.

## Security/privacy verification

T03 and T09 inject unique synthetic prohibited values through every caller and failure surface and assert byte-level absence from stdout, stderr, active logs, archives, lookup results, and bounded diagnostics. T04 proves containment, no-follow behavior, restrictive creation, and refusal without permission repair. No real credentials or personal data are used.

## Performance checks

T05 asserts the closed lock-attempt and time budgets with an injected monotonic clock, counts filesystem operations on the non-rotation path, denies network and external-process creation, rejects database modules in the runtime dependency graph, and proves no background handle survives completion. T08 asserts lookup opens only the five named files. T15 measures normalized complete-interaction bytes. Append and lookup durations may be reported from representative runs, but no environment-sensitive wall-clock threshold is the sole correctness gate.

## Manual QA checklist

Not applicable. Every normative outcome and user-facing example has automated contract, integration, end-to-end, or smoke proof. Documentation examples are exercised through package and release validation rather than accepted by visual inspection alone.

## What not to test and why

- Hosted retention, forwarding, telemetry, aggregation, and tailing are non-goals.
- Malicious control by a user who can rewrite the binary and filesystem is outside the local integrity model.
- Changing concise defaults is not performed; M4 proves only eligibility or ineligibility for a later v0.5.0 decision.
- Removal of detailed output, autonomous workflow progression, and new lifecycle semantics are excluded by the governing spec.
- Wall-clock performance across arbitrary machines is not a correctness contract.

## Uncovered gaps

None. Every normative requirement, example, edge case, applicable boundary, selected interaction, and acceptance criterion has direct automated proof assigned no later than its owning implementation milestone.

## Next artifacts

- Independent test-spec review.
- M1 implementation only after test-spec settlement.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`; this document does not authorize implementation until that review is recorded and the exact artifact identity is settled.
