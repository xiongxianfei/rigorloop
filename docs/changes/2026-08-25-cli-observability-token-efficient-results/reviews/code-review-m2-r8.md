# Code Review M2 R8: Second Independent Logging-Core Review

Review ID: code-review-m2-r8
Stage: code-review
Round: r8
Reviewer: distinct fresh independent reviewer
Reviewer context ID: m2-r8-second-independent-review
Author context ID: root-m2-implementation-and-corrections
Target: frozen M2 logging-core implementation, tests, and evidence
Reviewed artifact: M2 implementation/test/evidence diff bundle `sha256:a8ccc19505fef9e6243859dba71da3ecfd803575d43db2170b71922cb9c3d3f8`
Reviewed milestone: M2
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Context separation mechanism: distinct fresh reviewer with artifact-first risk mapping before prior-review reconciliation
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
Affected behavior: strict local diagnostic configuration, allowlisted event construction, path-component validation, candidate publication, bounded locking, rotation, concurrency, privacy, and degraded recovery
Highest-impact failure modes: private-value persistence; mutation outside the containment root; incomplete retained JSONL; deletion of an unowned lock; partial-rotation corruption; unbounded lock wait; incorrect unsafe-path classification; semantic failure caused by diagnostic I/O; unsupported evidence claims
Changed boundaries: normalized diagnostic facts to a synchronous five-file sink and filesystem failure back to stable diagnostic state
Evidence expected: exact R3-R17/R33-R34 and T02-T05 contract, privacy, path, fault, concurrency, timing, interruption, resource, and stable-error proof
Areas requiring direct inspection: `diagnostic-event.js`; `log-config.js`; `log-sink.js`; `cli-observability.js`; focused logging tests; invocation-isolation tests; M2 evidence; current review dispositions
Areas intentionally out of scope: M3 lookup integration beyond adjacent retained-surface/privacy evidence; M4 token benchmark and package proof; lifecycle advancement; final branch verification
Risk classes considered: semantic fidelity; privacy; filesystem containment; identity/no-follow behavior; concurrency; partial failure and recovery; bounded blocking; diagnostic isolation; proof adequacy
Falsifiable review questions: Can an existing non-directory component bypass the unsafe-path classification? Does every one of the six unlink/rename mutations receive root, component, source, and applicable destination validation with source identity checked last? Can any partial rotation corrupt retained JSONL or over-retain files? Can contention exceed its bounds or remove another writer's lock? Can logging failure alter semantic dispatch or leak prohibited values?
Automated review: yes
Material findings: CLIOBS-M2-R8-F1
Immediate next stage: review-resolution
Automatic downstream handoff: none; isolated second review stops on disagreement
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r8.md`; `review-log.md`; `review-resolution.md`
- Open blockers: `CLIOBS-M2-R8-F1`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M2-R8-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r8.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M2-R8-F1
- Verify readiness: not-claimed

## Finding CLIOBS-M2-R8-F1

Finding ID: CLIOBS-M2-R8-F1
Severity: minor
Location: `packages/rigorloop/dist/lib/log-sink.js:25-41`; missing regression in `packages/rigorloop/test/cli-observability.test.js`
Evidence: R11 requires every existing component to be inspected and observed non-files to degrade before mutation; T04 requires unsafe entries to fail through the containment policy. `checkExistingComponents()` rejects only symbolic links. With an absolute selected root whose intermediate component is an existing regular file, `appendDiagnosticEvent()` reaches `lstat(<file>/logs)` and leaks raw `ENOTDIR` instead of the stable `RL_LOG_UNSAFE_PATH` classification. The direct reproduction returned `{"threw":true,"code":"ENOTDIR"}`. No pathname mutation occurred, so this is a fail-closed classification defect rather than an escape.
Required outcome: Existing path components must be validated as directories and a non-directory component must fail deterministically with `RL_LOG_UNSAFE_PATH` before creation, lock acquisition, append, or rotation; T04 must include a direct intermediate-regular-file regression.
Safe resolution path: In the component walker, reject any existing intermediate component that is not a directory (as well as symlinks) with `unsafe()`, then add a focused T04 fixture using an absolute root below a regular-file component and assert `RL_LOG_UNSAFE_PATH`, unchanged sentinel bytes, and no created owned name. Rerun C02 and C01 and rereview the corrected frozen bundle.
needs-decision rationale: none

## No-additional-finding rationale

The held exclusive lock is also the unpublished candidate, so short writes and pre-publication failures do not damage the active JSONL. Device/inode checks bind each opened source to its final adjacent validation, and the approved ADR explicitly excludes replacement after that check. The direct partial-state probe executed each of the six pathname mutations and then threw: positions one through five retained four parseable named files plus the fail-closed lock, while final publication retained five parseable named files and no lock. Each case returned `RL_LOG_UNAVAILABLE`; no partial record or over-retention was reproduced. Existing tests directly cover stale locks, deterministic acquisition bounds, concurrent ordinary and rotation writers, replacement-lock preservation, privacy surfaces, descriptor closure, exact event sizing, and no surviving background handle.

## Checklist coverage

- Spec alignment: concern; R11's intermediate non-directory component partition returns the wrong stable class.
- Test coverage: concern; T04 lacks an intermediate regular-file component case. T02, T03, and the remaining T04/T05 partitions are directly represented.
- Edge cases: concern for the one path-shape partition; exact size, all six partial mutation positions, interruption, stale locks, and concurrent writers otherwise passed inspection or direct proof.
- Error handling: concern; raw `ENOTDIR` escapes the logging core where `RL_LOG_UNSAFE_PATH` is required.
- Architecture boundaries: pass; the synchronous candidate/lock design and explicitly bounded pathname threat model are preserved.
- Compatibility: pass within M2; the reproduced defect occurs before semantic integration and requires only stable diagnostic classification.
- Security/privacy: pass with the recorded fail-closed classification finding; no external mutation or private-value leak was reproduced.
- Derived artifact currency: pass for the frozen M2 identities; M4 package parity remains out of scope.
- Unrelated changes: pass; the reviewed target remains M2 logging core, tests, and evidence.
- Validation evidence: concern only for the missing T04 partition; C01/C02 totals and six-position recovery claims otherwise match direct evidence.

## Validation evidence challenged

- Frozen identity: the implementation and test hashes match the identities recorded for bundle `sha256:a8ccc19505fef9e6243859dba71da3ecfd803575d43db2170b71922cb9c3d3f8`.
- Direct intermediate-component probe: reproduced raw `ENOTDIR` for an absolute selected root below a regular file; the regular-file sentinel was not mutated.
- Direct partial-state rotation probe: after each of the six real pathname mutations, an injected failure yielded `RL_LOG_UNAVAILABLE`; all retained named records parsed, at most five retained names existed, and lock state was fail-closed.
- Prior C02/C01 evidence was inspected only after the blind-first risk map and implementation pass; the recorded 41/41 and 242/242 totals do not cover the reproduced T04 partition.

## Prior-finding reconciliation and handoff

The earlier M2 findings remain resolved on the frozen target, but this independently discovered finding is new. The first clean review cannot overrule second-review disagreement. No clean agreement is established, automatic continuation must stop, and M2 remains open for review-resolution, correction, and a fresh independent rereview. This review does not advance lifecycle state or claim verification, branch, CI, or PR readiness.
