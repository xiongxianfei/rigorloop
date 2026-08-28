# Code Review M2 R3: Logging-Core Correction Rereview

Review ID: code-review-m2-r3
Stage: code-review
Round: r3
Reviewer: primary agent fresh-pass reviewer
Reviewer context ID: root-code-review-m2-r3-fresh-pass
Target: corrected M2 logging-core implementation
Reviewed artifact: M2 implementation/test diff bundle `sha256:c762477f97884546a4d41575bd0104579f179ca3634787f7478b500720501024`
Reviewed milestone: M2
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L0
Context separation mechanism: fresh-pass reset in direct isolated review
Author context excluded: false
Risk tier: elevated
Risk-tier triggers: privacy-sensitive-persistence; filesystem-corruption; destructive-cleanup; concurrency; bounded-blocking; evidence-overclaim
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Reviewed correction evidence: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md` at `sha256:6eda43f3f2729d071a195e6492a30703544b4173f2d981f2bbe77b941dc32693`
Formal criteria: code-review-v1; boundary-first-v1
Initial packet inventory: specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:8df259dc5e97efa06535f785c25d575c366e2864b1fd88abde96fba6075b4fd4; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:e9db2b413a93963e60c0a7b2901b2b34505cc8e61f0df5f79de2778865f0fba3; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:aabe1b6661fba79aa8273baf3dc8e0640bf6985963e60b17c3e3e66fd40682f8; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:cf0aa9233df1f3b035fa88be57fc491e39021e13e3895a95a15ffd7dde9e8c04; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:7270aef7ad6849aace6108704654beadd09676f80faae037cfd45fd473ea1d2d; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:6eda43f3f2729d071a195e6492a30703544b4173f2d981f2bbe77b941dc32693
Prompt template version: code-review-v1
Initial packet hash: sha256:c762477f97884546a4d41575bd0104579f179ca3634787f7478b500720501024
Manifest owner: direct-user-invocation
Forbidden initial context excluded: false
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: privacy-safe diagnostic event construction, bounded local persistence, lock acquisition and cleanup, and M2 proof completeness
Highest-impact failure modes: false recorded observability; stale lock and descriptor leak; deletion of an unowned lock; unsupported M2 closeout
Changed boundaries: normalized diagnostic facts to event builder, invocation degradation controller, and synchronous file sink
Evidence expected: exact R14/R15/R33 behavior and complete T02-T05 direct proof
Areas requiring direct inspection: diagnostic-event.js; log-sink.js; cli-observability.js; focused tests; M2 evidence; prior M2 dispositions
Areas intentionally out of scope: M3 lookup semantics except privacy-surface evidence; token benchmark; package publication; final verification
Risk classes considered: semantic isolation; privacy; filesystem containment; concurrency; recovery; bounded blocking; proof adequacy
Falsifiable review questions: Does clock failure report degraded? Does every post-open failure clean up? Can a replacement lock be deleted after the identity check? Does evidence directly prove every named T02-T05 partition?
Automated review: yes
Material findings: CLIOBS-M2-R3-F1, CLIOBS-M2-R3-F2, CLIOBS-M2-R3-F3, CLIOBS-M2-R3-F4
Immediate next stage: review-resolution
Automatic downstream handoff: none; direct review-only invocation
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Review inputs and actual-diff summary

The rereview inspected the full corrected `diagnostic-event.js`, `log-sink.js`, and `cli-observability.js` targets, the focused logging and invocation tests, the M2 evidence, the eight prior M2 findings and dispositions, current M2 lifecycle state, and exact R3-R17/R33-R34 plus T02-T05 obligations. The correction adds closed event shapes, bounded fallback, lock-inode candidate publication, monotonic lock adapters, guarded diagnostic writes, and additional fault tests. Fresh direct probes challenged timestamp degradation, acquisition cleanup, destructive cleanup races, and the claimed proof matrix.

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r3.md`; `review-log.md`; `review-resolution.md`
- Open blockers: four material M2 findings
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M2-R3-F1, CLIOBS-M2-R3-F2, CLIOBS-M2-R3-F3, CLIOBS-M2-R3-F4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r3.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M2-R3-F1, CLIOBS-M2-R3-F2, CLIOBS-M2-R3-F3, CLIOBS-M2-R3-F4
- Verify readiness: not-claimed

## Finding CLIOBS-M2-R3-F1

Finding ID: CLIOBS-M2-R3-F1
Severity: major
Location: `packages/rigorloop/dist/lib/diagnostic-event.js:54-59`; `packages/rigorloop/dist/lib/cli-observability.js:49-66`
Evidence: A direct invocation with a throwing injected wall clock, valid CLI version, and successful event sink returned semantic exit `0`, rendered `observability: recorded`, and wrote two ordinary `info` events. `timestamp()` silently substitutes `new Date()`, so the controller never observes the timestamp failure. R33 requires timestamp failure to degrade the affected diagnostic event; T02 expects the clock-failure boundary to produce a safe degraded outcome. The existing `event construction failure is diagnostic-only` test omits `cliVersion`, so it degrades because a required field is missing rather than because the clock failed.
Required outcome: A timestamp-source failure must be observable to the invocation controller as diagnostic degradation while preserving semantic execution and emitting no private clock error.
Safe resolution path: Return or throw a closed internal clock-failure signal from event construction, let the guarded event writer mark observability degraded, and add a controller-level regression with a valid event input proving degraded projection, bounded stderr, and the exact retained-event outcome.
needs-decision rationale: none

## Finding CLIOBS-M2-R3-F2

Finding ID: CLIOBS-M2-R3-F2
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:57-75`
Evidence: A direct sink probe injected `fstatSync` failure immediately after the exclusive lock open. The call escaped without the stable `RL_LOG_UNAVAILABLE` code and left `.rigorloop-log.lock` behind. The newly opened descriptor is not retained for cleanup because `acquire()` constructs the returned object only after `fstatSync` succeeds. This converts one diagnostic fault into a stale lock that suppresses later events and contradicts R14, R15, T05, and the evidence claim that filesystem faults degrade only the affected operation without surviving handles.
Required outcome: Every acquisition failure after exclusive creation must close its descriptor, remove only its owned lock safely, return the stable unavailable classification, and leave later event attempts usable.
Safe resolution path: Make acquisition a guarded resource transaction: retain the descriptor and identity as soon as creation succeeds, close on every later failure, perform ownership-safe cleanup, normalize the outward error, and add `open`, `fstat`, and close-fault regressions that verify no surviving lock or descriptor and a successful subsequent append.
needs-decision rationale: none

## Finding CLIOBS-M2-R3-F3

Finding ID: CLIOBS-M2-R3-F3
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:126-131`
Evidence: `removeOwnedLock()` compares pathname identity and then calls `unlinkSync()` separately. A deterministic adapter that replaces the lock after the check but before the unlink caused the unowned replacement to be deleted (`replacement_survives:false`) while the original inode survived under another name. The existing replacement-lock test swaps the path before `removeOwnedLock()` checks it, so it does not cover the destructive check/use window. R14 explicitly prohibits removing an unowned lock, and the accepted M2 resolution requires handle/inode/token-bound cleanup.
Required outcome: Cleanup must never unlink a pathname whose current object is not the invocation-owned lock, including a replacement in the final destructive-operation window.
Safe resolution path: Use a cleanup protocol whose destructive step is bound to an invocation-unique owned name/token and whose pathname cannot target a replacement, or retain a failed owned lock rather than performing an unverifiable unlink. Add the exact between-check-and-unlink replacement regression and corresponding archive destructive-operation races.
needs-decision rationale: none

## Finding CLIOBS-M2-R3-F4

Finding ID: CLIOBS-M2-R3-F4
Severity: major
Location: `packages/rigorloop/test/cli-observability.test.js:146-160,321-348`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md`
Evidence: The T03 test checks only one in-memory serialized event and does not search active logs, archives, stderr, stdout, or lookup output as required. The six-writer test does not exercise concurrent rotation. No interruption fault, acquisition `fstat` fault, between-check destructive race, or successful post-fault retry is present. `_getActiveHandles()` does not enumerate ordinary synchronous file descriptors and therefore cannot prove the no-descriptor-leak claim. The evidence nevertheless states that active/archive privacy, interruption, all filesystem faults, and surviving-handle partitions are covered. A fresh C02 attempt also could not reproduce the recorded 33/33 result because the local package dependency was absent; it stopped at 19 pass/1 loader failure (`ERR_MODULE_NOT_FOUND: yaml`).
Required outcome: M2 evidence must be limited to directly demonstrated outcomes, and every named T02-T05 completion criterion must have identity-stable direct proof before M2 closeout.
Safe resolution path: Add retained/rendered privacy searches, concurrent rotation and process-interruption fixtures, acquisition and destructive-race fault tests, descriptor-count or subsequent-use proof appropriate to synchronous descriptors, and post-fault recovery tests. Restore dependencies with the repository-owned package install command, rerun exact C02 and C01, and refresh evidence with the actual identities and counts.
needs-decision rationale: none

## Checklist

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | R14, R15, and R33 fail under the reproduced clock and filesystem paths. |
| Test coverage | block | Named T02-T05 recovery, retained privacy, interruption, and concurrent-rotation paths remain unproved. |
| Edge cases | concern | The final unlink race and post-exclusive-open failure escape current tests. |
| Error handling | block | Acquisition failure strands a lock; timestamp failure is silently reported as recorded. |
| Architecture boundaries | concern | The sink still uses pathname check-then-unlink rather than an ownership-bound destructive operation. |
| Compatibility | pass | No reviewed correction changes the v0.4.x result projection or durable lifecycle contract. |
| Security/privacy | concern | No new private-value leak was reproduced, but retained-surface privacy proof is incomplete and unowned lock deletion remains possible. |
| Derived artifact currency | pass | No tracked generated logging-core artifact is required; local `node_modules` is intentionally untracked. |
| Unrelated changes | pass | The reviewed correction is bounded to logging events, sink/controller behavior, tests, and M2 evidence. |
| Validation evidence | concern | Prior 33/33 and 233/233 records are identity-bound, but the fresh C02 rerun stopped on the absent `yaml` dependency and direct probes contradict the evidence's completion claims. |

## Direct proof and handoff

The direct clock probe produced `recorded`, two events, and severities `info/info`. The acquisition probe left the lock after `fstat` failure. The unlink-race probe deleted the replacement lock. A fresh C02 attempt produced 19 passing tests and one loader failure because `yaml` was not installed locally. No implementation was changed during review.

This direct review remains isolated: there is no automatic downstream handoff. M2 stays `review-requested`; review-resolution and corrected implementation/rereview are required before workflow may close M2 or enter M3. Because this is an L0 fresh-pass review, it does not satisfy any separate L1 independent-review promotion requirement even after its findings are resolved.
