# Code Review M1 R1: CLI Observability and Token-Efficient Results

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Codex isolated direct reviewer with fresh-assumption reset
Status: changes-requested
Review date: 2026-08-25
Review mode: isolated direct review with an intentional fresh-assumption reset
Target: branch diff from `bcc7ef14ae45e8df737d8a97e72eff3a3823446b` to `ca112ac6028ad265cbf111f99ad2d4618b6a72b6`
Diff identity: `sha256:7fdc8b445397922feba03da3f5ff6aefffd01d38a6d137a6ed78d366c64a6d7d`
Reviewed milestone: M1, with M2-M4 implementation present in the actual branch diff
Governing artifacts: `specs/cli-observability-and-token-efficient-results.md`, `specs/cli-observability-and-token-efficient-results.test.md`, `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`, and `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m1-r1.md`, `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`, and `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Open blockers: six material implementation and proof findings
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M1-CR1, CLIOBS-M1-CR2, CLIOBS-M1-CR3, CLIOBS-M1-CR4, CLIOBS-M1-CR5, CLIOBS-M1-CR6
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M1-CR1, CLIOBS-M1-CR2, CLIOBS-M1-CR3, CLIOBS-M1-CR4, CLIOBS-M1-CR5, CLIOBS-M1-CR6
- Verify readiness: not-claimed

## Actual-diff summary

The diff adds a shared result renderer, local JSONL logging, invocation correlation, log inspection commands, a token-profile gate, tests, and package documentation. The lifecycle record still identifies M1 as `implementing`, while the branch already contains M2-M4 commits. This review therefore assesses the complete observable implementation sufficiently to identify cross-milestone defects but closes no milestone or routing state.

## Findings

### CLIOBS-M1-CR1 — Logging initialization failures change semantic execution

Finding ID: CLIOBS-M1-CR1
Severity: major
Location: `packages/rigorloop/dist/lib/log-config.js:39-42` and `packages/rigorloop/dist/lib/cli-observability.js:25-30,49-56`
Evidence: `RIGORLOOP_LOG_DIR=relative node packages/rigorloop/dist/bin/rigorloop.js version` exits 4 without running `version`, although R15 requires logging configuration or availability failure not to change semantic behavior or exit status. An injected throwing clock causes `buildDiagnosticEvent` to throw before `dispatch`; the direct probe reported `dispatch_called=false`, contradicting R15 and R33.
Required outcome: Every logging-path and event-construction failure other than the explicitly closed invalid-level inputs must degrade observability without preventing or changing semantic dispatch, stdout, repository bytes, or exit status.
Safe resolution path: Separate strict option-vocabulary rejection from sink/path degradation, guard event creation inside the non-semantic observability boundary, preserve one bounded fallback diagnostic, and add public and injected regressions for unsafe path, clock, entropy, encoding, and event-builder failures.
needs-decision rationale: none

### CLIOBS-M1-CR2 — Log lookup mutates an absent store

Finding ID: CLIOBS-M1-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:21-24,80-82` and `packages/rigorloop/dist/lib/log-inspection.js:7-18`
Evidence: `readRetainedLogs` calls `ensureSafeLogRoot`, which creates a missing directory. A direct lookup against an absent path returned `RL_LOG_NOT_FOUND` and left `lookup_created=yes`. That violates R20's read-only inspection boundary and makes an absent store indistinguishable from an existing empty store through mutation.
Required outcome: Log inspection must validate and read an existing bounded store without creating directories, files, locks, or governed or diagnostic state.
Safe resolution path: Split non-mutating root validation from writer initialization, use the non-mutating path in `logs path`/`logs show`, return the specified unavailable/not-found result without creation, and add byte/path inventory assertions around every inspection outcome.
needs-decision rationale: none

### CLIOBS-M1-CR3 — Rendering precedes terminal observability

Finding ID: CLIOBS-M1-CR3
Severity: major
Location: `packages/rigorloop/dist/lib/cli-observability.js:55-65`, top-level handlers in `packages/rigorloop/dist/bin/rigorloop.js`, and `packages/rigorloop/dist/lib/lifecycle-cli.js`
Evidence: `dispatch` renders semantic output inside existing handlers before the controller builds and attempts the completion event. A completion-write failure therefore occurs after a concise result has already reported `observability: recorded`; the controller cannot revise the emitted projection to `degraded`. This contradicts R15, R27, R28, BND-COMPOSE-001, and the ADR's single-result/controller boundary.
Required outcome: One semantic result must return to the invocation controller, completion observability must be resolved before new projections render, and stdout must be emitted exactly once without changing legacy defaults.
Safe resolution path: Refactor handlers to return a normalized result plus legacy rendering metadata, let the controller attempt terminal logging and finalize observability, then render once; add completion-only sink-failure tests for concise human/JSON and detailed compatibility paths.
needs-decision rationale: none

### CLIOBS-M1-CR4 — Partial append can corrupt retained JSONL

Finding ID: CLIOBS-M1-CR4
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:65-77`
Evidence: `appendFileSync` is used without recording the pre-append size or truncating on a partial-write failure. A disk-full or injected short-write can therefore leave a truncated final JSONL record, contrary to R14 and the T05 complete-record recovery requirement. The current tests exercise only a successful rotation.
Required outcome: A failed append or rotation must leave every retained line complete, remain within the owned directory, and degrade observability without changing the semantic command.
Safe resolution path: Use a recoverable append protocol under the owned lock—record the prior size and truncate on failed append, with contained rollback for rotation—or an equivalent proven design; add short-write, disk-full, rename, append, and interruption fault injection plus concurrent-writer proof.
needs-decision rationale: none

### CLIOBS-M1-CR5 — Token gate trusts asserted measurements

Finding ID: CLIOBS-M1-CR5
Severity: major
Location: `scripts/measure-cli-result-bytes.py:19-49` and `packages/rigorloop/test/fixtures/observability/token-profiles-v1.json:5-10`
Evidence: The measurement command reads pre-entered `concise_bytes`, `lookup_required`, and `required_fields_present` values and then treats those assertions as measured gates. It never invokes the CLI, captures stdout/stderr, normalizes UTF-8 bytes, or executes required follow-ups. Changing the asserted numbers can manufacture eligibility. This does not satisfy R29-R30, T15, C06, or INT-005.
Required outcome: The v1 gate must measure the exact six real complete interactions, count normalized stdout plus stderr and required follow-ups, derive field and one-pass results from captured outputs, and fail closed on fixture/version drift.
Safe resolution path: Make profiles own executable fixture inputs and expected semantics, run each detailed and concise interaction in controlled repositories, calculate all gates from captured output, keep the v0.4.x baseline immutable, and add threshold, rename/add/remove, follow-up, and field-regression tests.
needs-decision rationale: none

### CLIOBS-M1-CR6 — Milestone evidence overstates direct proof

Finding ID: CLIOBS-M1-CR6
Severity: major
Location: `packages/rigorloop/test/cli-observability.test.js`, `packages/rigorloop/test/cli-invocation-observability.test.js`, and milestone evidence `evidence/m2-logging-core.md`, `evidence/m3-invocation-integration.md`, `evidence/m4-token-and-package-proof.md`
Evidence: The implemented tests cover a successful append/rotation, one successful invocation/lookup, concise opt-in, and a threshold case, but the approved proof map requires T01-T17, including platform path partitions, symlink and permission refusal, secret scans, real concurrent writers, lock exhaustion/stale lock, filesystem faults, corrupt lookup partitions, semantic repository-byte equivalence, wrapper parity, fresh-checkout non-authority, and packed-package smoke. The evidence reports broad requirement groups as passed without those direct proofs, and C04 failed while C08 was interrupted.
Required outcome: Every claimed proof obligation must have current direct automated evidence, milestone reports must distinguish passed/failed/not-run truthfully, and required C01-C10 commands must complete as specified before clean review.
Safe resolution path: Implement the missing T01-T17 partitions, correct milestone evidence to actual command results, rerun C01-C10, resolve or explicitly isolate selector baseline failures, and submit each review-requested milestone in plan order.
needs-decision rationale: none

## Checklist

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CLIOBS-M1-CR1 through CR5 identify direct R14, R15, R20, R27-R30 violations. |
| Test coverage | block | CLIOBS-M1-CR6; most approved T01-T17 partitions have no implementation. |
| Edge cases | block | Clock, unsafe path, partial append, completion failure, concurrency, and lookup mutation are missing or incorrect. |
| Error handling | block | Diagnostic initialization can suppress semantic dispatch and append failure can corrupt JSONL. |
| Architecture boundaries | block | Rendering remains inside handlers before completion observability is known. |
| Compatibility | concern | Existing package tests pass, but the required complete legacy/new projection matrix and packed smoke are incomplete. |
| Security/privacy | concern | Allowlisting exists, but the required all-surface synthetic-secret and unsafe-path proofs are absent. |
| Derived artifact currency | block | The token report is assertion-driven, and release verification did not complete. |
| Unrelated changes | concern | M2-M4 implementation is present while governed state still identifies M1 as implementing. |
| Validation evidence | block | Focused and package tests passed, but C04 failed and C08 was interrupted; evidence overstates coverage. |

## Direct proof run during review

```text
RIGORLOOP_LOG_DIR=relative node packages/rigorloop/dist/bin/rigorloop.js version
Result: exit 4; semantic version command did not run.

findInvocationEvents(<absent-directory>, "0000000000000000")
Result: RL_LOG_NOT_FOUND; absent directory was created.

runObservedCli(["version"], dispatch, { now: throwingClock, file logging off })
Result: clock exception escaped; dispatch_called=false.
```

## Handoff

This direct review is isolated. There is no automatic downstream handoff. Record and disposition all six findings in `review-resolution.md`, fix them under implementation authority, move only the actual current milestone to `review-requested` through workflow, and rerun `code-review-m1-r2`. No owner decision is required for the findings as written.
