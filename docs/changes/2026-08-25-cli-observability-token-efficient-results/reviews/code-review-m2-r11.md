# Code Review M2 R11: Explicit Independent Logging-Core Review

Review ID: code-review-m2-r11
Stage: code-review
Round: r11
Reviewer: fresh independent reviewer
Reviewer context ID: m2-r11-explicit-independent-review
Author context ID: root-m2-implementation-and-corrections
Target: corrected frozen M2 logging-core implementation, tests, and evidence
Reviewed artifact: M2 implementation/test/evidence diff bundle `sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190`
Reviewed milestone: M2
Review date: 2026-08-26
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Context separation mechanism: explicit fresh reviewer with artifact-first source and contract assessment before prior-review reconciliation
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: privacy-sensitive-persistence; filesystem-containment; destructive-rotation; concurrent-writer-recovery; bounded-blocking; descriptor-lifetime; evidence-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
Formal criteria: code-review-v1; independent-review-gate-v1; requirement-fidelity-gate-v1; boundary-first-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:7a458a3630151894b752dd580fab68ceecbd437410e0c244eea2bdf4afdb8ede; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:80d1a42bd1fbcd83408427ff687ec7b09419e7b3df4e1efcb61ee77f489a22d4; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:b749ddbd83df1061c049eb3c439be53fa53acd9934b3a368999052cdaeedfeec; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:3a08b11153c51a1aeaa8d088a0eb641278f3592c2e1308c0c1551aa54921c787
Prompt template version: code-review-v1
Initial packet hash: sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: strict event/configuration closure, no-follow contained persistence, six-site rotation/publication, bounded locking, concurrent writers, privacy, descriptor cleanup, and diagnostic-only recovery
Highest-impact failure modes: private-value persistence; path escape or identity substitution; incomplete JSONL; unowned lock deletion; unbounded lock wait; leaked file descriptors; logging changing semantic execution; unsupported evidence claims
Changed boundaries: allowlisted diagnostic facts to a synchronous five-file sink, and filesystem failure back to stable degraded observability
Evidence expected: exact R3-R17/R33-R34 and T02-T05 proof across privacy, containment, identity, six mutation intervals, every partial-rotation fault, concurrency, timing, recovery, descriptor cleanup, resource bounds, and semantic isolation
Areas requiring direct inspection: `diagnostic-event.js`; `log-config.js`; `log-sink.js`; `cli-observability.js`; focused logging and invocation tests; M2 evidence; current review dispositions
Areas intentionally out of scope: M3 feature completion beyond adjacent public-path and semantic-isolation proof; M4 benchmark/package proof; lifecycle state mutation; final verification and PR readiness
Risk classes considered: requirement fidelity; privacy; filesystem containment; stable errors; no-follow identity; destructive mutation cadence; partial recovery; concurrency; descriptor lifetime; bounded blocking; semantic isolation; proof accuracy
Falsifiable review questions: Are admitted event types closed and private inputs absent? Does each of six destructive mutations have adjacent validation? Can partial rotation corrupt retained files or alter an outside sentinel? Does every post-open failure close every descriptor? Can logging failure alter public semantic output or exit status? Are evidence identities and claims exact?
Automated review: yes
Material findings: CLIOBS-M2-R11-F1
Immediate next stage: review-resolution
Automatic downstream handoff: none; explicit isolated review stops on material finding
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r11.md`; `review-log.md`; `review-resolution.md`
- Open blockers: `CLIOBS-M2-R11-F1`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M2-R11-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r11.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M2-R11-F1
- Verify readiness: not-claimed

## Finding CLIOBS-M2-R11-F1

Finding ID: CLIOBS-M2-R11-F1
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:111-114`, with the same unguarded close pattern at `packages/rigorloop/dist/lib/log-sink.js:130-150` and `packages/rigorloop/dist/lib/log-sink.js:176-179`; insufficient regression at `packages/rigorloop/test/cli-observability.test.js:341-356`
Evidence: T05 requires the fault-injected logging core and open-handle probe to establish that no persistent handle survives completion. `readOwned()` performs one `io.closeSync()` in `finally`; if that close throws before closing, the outer append converts the error to `RL_LOG_UNAVAILABLE` and closes only the candidate lock descriptor. The direct public-module probe injected a first `closeSync` failure without closing its active-file descriptor and returned `{"code":"RL_LOG_UNAVAILABLE","leakedFd":22,"descriptor_survived_return":true}`; `fstatSync(22)` succeeded after `appendDiagnosticEvent()` returned. The tracked close-failure test calls the real `closeSync(fd)` before throwing, so it proves error classification after a successful close, not cleanup after a failed close. The same single-attempt pattern exists for rotation validation handles and the ordinary pre-publication active handle. This contradicts the M2 evidence claims that every post-open failure closes the descriptor and that close faults leave no surviving handle.
Required outcome: Every descriptor opened by the sink must be closed before the append attempt returns, including when the injected/platform close operation initially fails, or the approved T05/evidence contract must be narrowed through its owning upstream stage. Add identity-stable regressions that throw before closing for the active read, ordinary pre-publication validation, and rotation-held descriptor paths, assert the descriptor is no longer valid after return, and keep semantic output/exit behavior unchanged.
Safe resolution path: Centralize descriptor release in a bounded close helper that records the first close error, makes a safe bounded cleanup attempt through the trusted filesystem close primitive, and preserves `RL_LOG_UNAVAILABLE` plus stale-lock behavior. Use injected descriptors to assert `fstatSync` fails after each affected path returns, rerun C02 and C01, correct the M2 evidence claims and identities, freeze a new bundle hash, and obtain fresh holistic M2 rereview. If platform semantics make the cleanup guarantee impossible, route the T05 and evidence claim change to the owning test-spec/spec stage rather than silently weakening implementation proof.
needs-decision rationale: none; the current approved T05 contract and evidence already require no surviving descriptor, so implementation correction is directly actionable.

## Actual-diff and boundary assessment

- Privacy and type closure: pass. Event family, severity, event/sequence pair, completion status, non-negative integer fields, string/list shapes, lifecycle operations, entropy, clock failure, and the newline-inclusive 16 KiB boundary are closed; prohibited synthetic values were absent from retained and public surfaces.
- Root/component/path containment and stable error classes: pass for the named supported partitions. Existing symlink, non-directory, broad-mode, identity-change, and injected ordinary-I/O paths fail before guarded mutation as `RL_LOG_UNSAFE_PATH` or `RL_LOG_UNAVAILABLE`; the approved ADR limitation against same-user post-check replacement is preserved.
- Six adjacent mutations and no-follow identity: pass. Full rotation showed oldest unlink, four archive renames, and candidate publication, each with adjacent root/source/applicable-destination inspection and final source device/inode validation.
- Lock timing and recovery: pass. Acquisition is capped at ten attempts and nine waits inside the 1,000 ms monotonic budget, does not steal stale locks, and retains unverifiable or failed candidates.
- Partial rotation faults: pass. Direct faults at mutation positions one through six each returned `RL_LOG_UNAVAILABLE`, retained only complete parseable owned JSONL, preserved the outside sentinel, and retained the fail-closed candidate lock.
- Descriptor cleanup: concern. The direct close-before-release fault leaves an active-file descriptor live after the API returns; the existing test and evidence overstate this boundary.
- Concurrency and semantic isolation: pass in the executed public/package suite. Six real writers passed both ordinary and rotation-boundary cases; logging recorded/disabled/degraded states preserved lifecycle semantics and repository bytes.
- Proof accuracy: concern. File identities match the frozen bundle, but the descriptor-cleanup statements in `m2-logging-core.md` and the clean conclusions in R9/R10 are disproved by the direct probe.

## Checklist coverage

- Spec alignment: concern; R13-R15 behavior is otherwise satisfied, but the approved T05 recovery/resource proof requires descriptor closure after injected faults.
- Test coverage: concern; the close-failure test closes successfully before throwing and therefore misses the reproduced leak in three close sites.
- Edge cases: concern only for close-before-release faults; exact sizes, six mutation positions, interruption, stale locks, and concurrent writers have direct proof.
- Error handling: concern; stable `RL_LOG_UNAVAILABLE` is returned, but resource cleanup is incomplete.
- Architecture boundaries: pass; the synchronous candidate/lock design, five owned names, and explicit pathname threat limitation remain intact.
- Compatibility: pass within reviewed scope; public package tests preserve existing projections and semantic exit classifications.
- Security/privacy: concern because leaked descriptors violate the resource boundary, although no private-value disclosure or containment escape was reproduced.
- Derived artifact currency: pass for the frozen M2 identities; M4 package parity remains out of scope.
- Unrelated changes: pass; the reviewed target remains the M2 implementation/test/evidence bundle.
- Validation evidence: concern; C01/C02 pass, but the adversarial descriptor probe disproves one material T05/evidence claim.

## Validation evidence challenged

- `node --test packages/rigorloop/test/cli-observability.test.js packages/rigorloop/test/cli-invocation-observability.test.js`: 46/49 passed before dependencies were installed; the three failures reported only missing locked package `yaml`, while all 27 logging-core T02-T05 cases passed.
- `npm ci --prefix packages/rigorloop --ignore-scripts && npm test --prefix packages/rigorloop`: passed 242/242 after installing the locked dependency; generated `packages/rigorloop/node_modules` was removed immediately afterward.
- Direct close-before-release probe: returned `RL_LOG_UNAVAILABLE` and proved `descriptor_survived_return:true`; the leaked descriptor was explicitly closed by the probe after observation.
- Direct six-position partial-rotation probe: all six positions returned `RL_LOG_UNAVAILABLE`, retained complete parseable named logs, preserved the outside sentinel, and retained the fail-closed lock.
- Frozen identity: every implementation/test/evidence hash matches bundle `sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190`.

## Prior-finding reconciliation and handoff

Earlier accepted findings remain resolved on their stated boundaries, but R9/R10's clean agreement is no longer sufficient because this fresh review found a material defect on the identical hash. `CLIOBS-M2-R11-F1` requires review-resolution, implementation correction, evidence correction, a new frozen target, and holistic rereview of M2. This explicit invocation is isolated: there is no automatic downstream handoff, no lifecycle advancement, and no claim of verification, branch, CI, or PR readiness.
