# Code Review M2 R7: Independent Logging-Core Review

Review ID: code-review-m2-r7
Stage: code-review
Round: r7
Reviewer: fresh independent subagent reviewer
Reviewer context ID: m2-r7-independent-review
Author context ID: root-m2-implementation-and-corrections
Target: frozen M2 logging-core implementation, tests, and evidence
Reviewed artifact: M2 implementation/test/evidence diff bundle `sha256:a8ccc19505fef9e6243859dba71da3ecfd803575d43db2170b71922cb9c3d3f8`
Reviewed milestone: M2
Review date: 2026-08-25
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Native review status: clean-with-notes
Review gate outcome: advance
Independence level: L1
Context separation mechanism: separately spawned fresh reviewer with artifact-first assessment and prior author reasoning excluded
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: privacy-sensitive-persistence; filesystem-containment; destructive-rotation; concurrent-writer-recovery; bounded-blocking; evidence-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
Formal criteria: code-review-v1; independent-review-gate-v1; requirement-fidelity-gate-v1; boundary-first-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:7a458a3630151894b752dd580fab68ceecbd437410e0c244eea2bdf4afdb8ede; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:69fca318208953824303641cc81ba94254c3cfedb89e8aae2bc005810f3af64e; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:92ec1c6d06d0442a8b00fa9fe619372608a13d06268c0639bce655f258f3b439; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:ec1c412347c5d65d6a5b17a8ee40dc708d3d11d028242f883ee89cf297a4084a
Prompt template version: code-review-v1
Initial packet hash: sha256:a8ccc19505fef9e6243859dba71da3ecfd803575d43db2170b71922cb9c3d3f8
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: strict local diagnostic configuration, allowlisted event construction, non-following path validation, candidate publication, bounded locking, rotation, concurrency, privacy, and degraded recovery
Highest-impact failure modes: private-value persistence; mutation outside the containment root; incomplete retained JSONL; deletion of an unowned lock; partial-rotation corruption; unbounded lock wait; semantic failure caused by diagnostic I/O; unsupported evidence claims
Changed boundaries: normalized diagnostic facts to a synchronous five-file sink and diagnostic failure back to non-semantic invocation state
Evidence expected: exact R3-R17/R33-R34 and T02-T05 contract, privacy, path, fault, concurrency, timing, interruption, and resource proof
Areas requiring direct inspection: `diagnostic-event.js`; `log-config.js`; `log-sink.js`; `cli-observability.js`; focused logging tests; invocation-isolation tests; M2 evidence; current review dispositions
Areas intentionally out of scope: M3 lookup integration beyond adjacent retained-surface/privacy evidence; M4 token benchmark and package proof; lifecycle advancement; final branch verification
Risk classes considered: semantic fidelity; privacy; filesystem containment; identity/no-follow behavior; concurrency; partial failure and recovery; bounded blocking; diagnostic isolation; proof adequacy
Falsifiable review questions: Can any admitted value serialize a prohibited marker? Does every one of the six unlink/rename mutations receive root, component, source, and applicable destination validation with source identity checked last? Can any unsafe or ordinary I/O fault mutate an external path or corrupt retained JSONL? Can any partial rotation leave more than five retained log names or a partial record? Can contention exceed the attempt/deadline bounds or remove another writer's lock? Can logging failure alter semantic dispatch or exit status?
Automated review: yes
Material findings: none
Immediate next stage: distinct second independent clean code review
Automatic downstream handoff: none; isolated review and elevated-risk second-review gate
Milestone closeout: blocked pending distinct second clean review
Required review-resolution: no
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r7.md`; `review-log.md`; `review-resolution.md`
- Open blockers: elevated-risk M2 requires a distinct second clean review before milestone closeout
- Next stage: blocked pending distinct second independent code review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r7.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: blocked
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Findings and notes

No material finding or accepted fix is required on the frozen M2 target.

The retained test suite injects a rename failure at publication rather than at every intermediate archive rename. Because partial rotation is a high-impact recovery partition, this review directly faulted each of the five possible rename positions during a full rotation and the archive-deletion unlink position. Every case returned `RL_LOG_UNAVAILABLE`, retained only complete parseable JSON Lines, kept at most five retained log names, preserved containment, and retained the fixed lock fail-closed. This direct probe supports a clean result; adding the six-position probe as a durable regression would strengthen future evidence but is not required to correct the reviewed implementation.

## Contract and boundary assessment

- R3-R9 and R33: closed severity, event/sequence, identity, family extensions, scalar/list shapes, UTC millisecond timestamp, monotonic non-negative duration, control normalization, exact 16 KiB encoding, and constant-only oversized recovery are implemented and directly covered.
- R10-R12: platform defaults, absolute override handling, restrictive creation modes, broad-mode refusal without repair, root/owned-path symlink refusal, containment, and non-following file identity checks match the approved boundary. The implementation does not claim atomic containment against the explicitly excluded same-user or privileged pathname-replacement actor.
- R11 adjacent validation: the real exported append path performs six destructive pathname mutations on a full rotation: one oldest-archive unlink, four log renames, and final lock publication. Before each, `validateMutation` revalidates the absolute root, existing components, all owned entries including any existing destination, and then checks the source device/inode as the immediately preceding operation. An injected validation I/O fault prevents mutation.
- R13-R14: candidate construction in the held exclusive lock prevents partial active-file writes; rotation is before a boundary-crossing append; lock work is bounded to ten attempts and 1,000 ms; real child writers retain complete records; stale or unverifiable locks are retained without cleanup.
- R15-R17: unsafe, unavailable, clock, sink, and stderr failures remain diagnostic-only; exactly one bounded fallback is guarded per invocation unless console is `off`; file disabling and closed option/environment vocabularies preserve semantic output and exit behavior.
- R34: the core uses synchronous built-ins, no daemon/database/network/background worker, a fixed owned-name inventory, no unbounded directory traversal, and no surviving handle in the tested ordinary path.

## Validation evidence challenged

- Initial C02 attempt: 27 logging tests passed, while `result-renderer.test.js` could not load the absent local `yaml` dependency. This was an environment prerequisite failure, not a target failure.
- Dependency setup: `npm ci --prefix packages/rigorloop` completed with one package and no reported vulnerabilities.
- C02: `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` passed 41/41.
- C01: `npm test --prefix packages/rigorloop` passed 242/242.
- Direct partial-rotation probe: injected failure at rename calls 1 through 5 and at the oldest-archive unlink; all six partitions returned `RL_LOG_UNAVAILABLE`, retained complete parseable JSONL, kept no more than five log files, and retained `.rigorloop-log.lock`.
- The review-created untracked `packages/rigorloop/node_modules/` directory was removed after validation.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-25-cli-observability-token-efficient-results` passed with 41 reviews, 48 findings, 41 log entries, and 48 resolution entries.
- `git diff --check -- docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r7.md docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md` passed.

## Checklist coverage

- Spec alignment: pass; the frozen core matches R3-R17/R33-R34 within the approved threat model.
- Test coverage: pass with note; T02-T05 cover the named contract, privacy, path, rotation, concurrency, interruption, and resource partitions, supplemented by the direct six-position partial-rotation probe.
- Edge cases: pass; exact size boundaries, absent/existing entries, every destructive rotation position, interruption, stale locks, and independent writer processes were challenged.
- Error handling: pass; unsafe state is distinguishable, ordinary I/O becomes unavailable, retained records remain complete, and diagnostic failure does not alter semantic execution.
- Architecture boundaries: pass; configuration, allowlisted builder, synchronous sink, and invocation controller retain their ADR-owned responsibilities.
- Compatibility: pass within M2; file logging can degrade or disable without changing semantic output or exit behavior.
- Security/privacy: pass; prohibited markers are absent from admitted surfaces, owned paths stay contained, permissions fail closed, and the review makes no race-proof claim.
- Derived artifact currency: pass for the exact M2 evidence identities; packaging remains M4-owned.
- Unrelated changes: pass; the reviewed M2 target is confined to logging-core behavior, tests, and evidence.
- Validation evidence: pass; exact C01/C02 results were rerun, claims were challenged with additional recovery probes, and no unreviewed M2 behavior capable of changing this verdict remains.

## Clean-review sufficiency receipt

Review target identity: sha256:a8ccc19505fef9e6243859dba71da3ecfd803575d43db2170b71922cb9c3d3f8
Governing artifacts inspected: constitution; approved feature spec R3-R17/R33-R34; approved test spec T02-T05; accepted ADR; active plan M2; current change record; implementation, tests, evidence, prior M2 review records, and review resolution
Adversarial hypotheses tested: unsafe values can escape the allowlist; one of six destructive mutations lacks adjacent validation; a followed or replaced path escapes containment; unsafe and ordinary I/O faults are conflated unsafely; partial rotation corrupts or over-retains logs; concurrent writers produce partial lines; stale-lock recovery removes another writer's lock; logging changes semantic execution; passing totals conceal missing proof
Direct proofs performed: C02; C01; existing exact size, privacy, path, mutation-order, failure, concurrency, interruption, and handle tests; five rename-position plus unlink-position partial-rotation fault probe; target identity and node_modules-removal checks
Validation evidence challenged: passing test counts were compared to the source protocol and supplemented with a direct six-position partial-rotation recovery probe
Unreviewed surfaces: M3 full invocation and lookup integration, M4 token and package proof, final cross-milestone coherence, hosted CI, and native execution on non-POSIX platforms remain downstream
Confidence: high for the frozen M2 contract and approved threat model
No-finding rationale: all falsifiable M2 privacy, containment, identity, mutation-cadence, recovery, concurrency, bounded-work, semantic-isolation, and proof-adequacy hypotheses passed direct inspection or execution without a reproduced material defect

The review began from the governing contract and frozen source/tests before prior review content. It attempted to falsify privacy allowlists, exact schema/identity, R11 validation cadence across all six destructive mutations, non-follow/identity behavior, containment, unsafe versus ordinary I/O handling, short writes, partial rotation, stale-lock recovery, independent-writer completeness, lock bounds, semantic isolation, and resource limits. Passing suites were not accepted alone: the review inspected the implementation protocol and added a six-position partial-rotation fault probe. No material defect was reproduced. M3 integration, M4 packaging/token proof, final lifecycle state, and final verification remain outside this milestone-local conclusion.

## Prior-finding reconciliation and handoff

All prior M2 material findings have resolved dispositions consistent with the frozen target. The blind-first review independently reached the same no-material-defect conclusion as the later reconciliation: closed event shapes and bounded fallback are present; candidate publication prevents active-file corruption; lock cleanup never removes an unowned replacement; all post-open tested descriptors close; crossed event/sequence pairs fail; each destructive mutation receives adjacent validation; and current evidence identities and counts are accurate.

This is the first clean independent agreement on elevated-risk M2. It does not advance lifecycle state or close M2. A distinct second clean independent review is required before workflow may settle the milestone; any disagreement stops automatic continuation.
