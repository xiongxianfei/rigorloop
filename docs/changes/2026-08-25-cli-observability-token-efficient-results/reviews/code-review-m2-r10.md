# Code Review M2 R10: Distinct Corrected-Bundle Review

Review ID: code-review-m2-r10
Stage: code-review
Round: r10
Reviewer: distinct fresh independent reviewer
Reviewer context ID: m2-r10-distinct-independent-review
Author context ID: root-m2-r8-correction
Target: corrected frozen M2 logging-core implementation, tests, and evidence
Reviewed artifact: M2 implementation/test/evidence diff bundle `sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190`
Reviewed milestone: M2
Review date: 2026-08-25
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Native review status: clean-with-notes
Review gate outcome: advance
Independence level: L1
Context separation mechanism: separately spawned fresh reviewer with contract-and-source assessment completed before prior R9 verdict reconciliation
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: filesystem-containment; stable-error-mapping; destructive-rotation; concurrent-writer-recovery; privacy-sensitive-persistence; evidence-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
Formal criteria: code-review-rereview-v1; independent-review-gate-v1; requirement-fidelity-gate-v1; boundary-first-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:7a458a3630151894b752dd580fab68ceecbd437410e0c244eea2bdf4afdb8ede; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:80d1a42bd1fbcd83408427ff687ec7b09419e7b3df4e1efcb61ee77f489a22d4; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:b749ddbd83df1061c049eb3c439be53fa53acd9934b3a368999052cdaeedfeec; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:3a08b11153c51a1aeaa8d088a0eb641278f3592c2e1308c0c1551aa54921c787
Prompt template version: code-review-v1
Initial packet hash: sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: strict diagnostic configuration and events, existing-component classification, non-following contained persistence, six-site rotation/publication, bounded locks, concurrent writers, privacy, and non-semantic failure recovery
Highest-impact failure modes: raw filesystem errors escaping stable classification; mutation after unsafe component discovery; private data persistence; path escape or identity substitution; incomplete JSONL after partial rotation; unowned lock deletion; unbounded contention; logging changing semantic execution; stale evidence approving the wrong target
Changed boundaries: observed filesystem component state to stable unsafe/unavailable classification, and allowlisted events to synchronous five-file publication
Evidence expected: exact R3-R17/R33-R34 and T02-T05 proof, with direct correction reproduction plus full containment, identity, failure, concurrency, privacy, and bounded-resource challenge
Areas requiring direct inspection: corrected component walker; `diagnostic-event.js`; `log-sink.js`; `cli-observability.js`; T02-T05 tests; invocation failure isolation; M2 evidence and target identities
Areas intentionally out of scope: M3 full invocation/lookup integration beyond adjacent privacy and semantic-isolation evidence; M4 token/package proof; lifecycle state mutation; final verification and PR readiness
Risk classes considered: requirement fidelity; filesystem containment; stable error mapping; no-follow identity; destructive mutation cadence; partial recovery; concurrency; privacy; resource bounds; diagnostic isolation; evidence currency
Falsifiable review questions: Does an intermediate regular file return `RL_LOG_UNSAFE_PATH` before creation while preserving sentinel bytes? Does every destructive operation have adjacent root/source/destination checks with source identity last? Can injected ordinary inspection error mutate any path? Can any unlink or rename fault leave partial or over-retained logs? Can device/inode mismatch publish? Can concurrent writers, privacy inputs, or background resources violate T02-T05? Are evidence hashes identical to the reviewed target?
Automated review: yes
Material findings: none
Immediate next stage: workflow-owned M2 settlement and next-milestone routing when authorized
Automatic downstream handoff: none; isolated review does not mutate lifecycle state
Milestone closeout: closed by distinct clean review agreement; authoritative state unchanged
Required review-resolution: no
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r10.md`; `review-log.md`; `review-resolution.md`
- Open blockers: none within the M2 review gate; workflow settlement remains unperformed
- Next stage: workflow-owned M2 settlement, then implement M3 when authorized by current state
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r10.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: closed
- Remaining implementation milestones: M3, M4
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Findings and agreement

No material finding or required correction was identified on frozen target `sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190`.

After the independent verdict was formed, R9 was inspected for reconciliation. R9 and R10 are distinct clean L1 reviews of the identical bundle hash. The required distinct clean agreement is therefore established. This review records that gate result only; it does not edit `change.yaml`, advance routing, or claim final verification.

## Correction and full-boundary assessment

- Intermediate regular-file correction: `checkExistingComponents()` rejects both symlinks and non-directories before `mkdirSync` or lock acquisition. The independent reproduction returned `RL_LOG_UNSAFE_PATH`, preserved exact `R10_SENTINEL` bytes, and left the nested root absent.
- Six adjacent mutations: a full rotation produced exactly six destructive operations—oldest unlink, four log renames, and candidate-lock publication. Every interval contained root, source, and applicable destination `lstat`; source identity was checked as the immediately preceding operation.
- No-follow identity: owned entries are checked before open, opened with `O_NOFOLLOW` where available, checked after open by device/inode, and checked again before destructive mutation. An injected post-open inode mismatch returned `RL_LOG_UNSAFE_PATH` without replacing the active record.
- Error mapping: observed symlink/non-directory/identity violations return `RL_LOG_UNSAFE_PATH`. An injected ordinary root-inspection `EIO` returned `RL_LOG_UNAVAILABLE` and performed zero unlink/rename mutations.
- Partial rotation and recovery: independent faults at oldest unlink and each of five rename positions returned `RL_LOG_UNAVAILABLE`, left no more than five retained log names, kept every retained line parseable, and retained the unpublished lock fail-closed when publication did not finish.
- Concurrency and completeness: real child-process ordinary and rotation writers retained complete JSONL; short write, disk full, fsync, close, rename, interruption, stale lock, descriptor, and replacement-lock paths remain directly covered.
- Privacy and event contract: closed field shapes, exact event/sequence pairs, independent 16-hex identity, control normalization, fixed oversized recovery, exact 16 KiB bound, and prohibited-marker absence passed focused proof.
- Resources and semantics: the core contains no network/database/daemon/timer/background-worker dependency, leaves no new active handle in the ordinary test, bounds lock attempts/time, and diagnostic sink/stderr failures do not replace semantic dispatch or exit behavior.
- Evidence currency: every implementation, test, and M2 evidence hash matches the corrected identities recorded above and the aggregate reviewed hash supplied for this review.

## Validation evidence challenged

- Initial C02 attempt: all 27 logging tests passed; `result-renderer.test.js` failed to load because the worktree-local `yaml` dependency was absent.
- `npm ci --prefix packages/rigorloop` installed the one declared dependency with no reported vulnerability.
- C02: `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` passed 41/41.
- C01: `npm test --prefix packages/rigorloop` passed 242/242.
- Independent boundary probe passed regular-file classification/sentinel/no-creation, all six adjacent mutation intervals, ordinary `EIO` unavailable/no-mutation behavior, and unlink plus every five-position rename recovery partition.
- Independent identity/privacy probe passed post-open inode mismatch refusal without active replacement and prohibited-marker absence.
- `python3 scripts/validate-boundary-first.py --path specs/cli-observability-and-token-efficient-results.md` passed.
- `git diff --check -- packages/rigorloop/dist/lib/log-sink.js packages/rigorloop/test/cli-observability.test.js docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-25-cli-observability-token-efficient-results` passed with 44 reviews, 49 findings, 44 log entries, and 49 resolution entries.
- `git diff --check -- docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r10.md docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md` passed.
- The review-created untracked `packages/rigorloop/node_modules/` directory was removed and confirmed absent.

Two early reviewer-authored probes exited nonzero because their injected harnesses were malformed: one intentionally throwing unlink adapter was not caught, and one synthetic `Stats` object lost its `isFile()` prototype and therefore mapped to unavailable. Neither reproduced a production defect. The corrected probes above passed unchanged production code and are the evidence used for this verdict.

## Checklist coverage

- Spec alignment: pass; corrected R11 classification and full R3-R17/R33-R34 behavior match the approved contract and threat model.
- Test coverage: pass; T02-T05 include the correction fixture and named event, privacy, path, mutation, failure, concurrency, interruption, and resource partitions.
- Edge cases: pass; intermediate non-directory, exact sizes, all six destructive mutations, every partial-rotation fault position, stale locks, identity mismatch, and interruption were directly challenged.
- Error handling: pass; unsafe conditions and ordinary I/O have stable distinct mappings, mutations stop before unsafe state, and retained records remain complete.
- Architecture boundaries: pass; configuration, allowlisted builder, synchronous sink, and invocation controller preserve ADR ownership without a race-proof containment claim.
- Compatibility: pass within M2; logging failure/disablement remains non-semantic and no default result projection changes here.
- Security/privacy: pass within the approved local threat model; prohibited markers are absent, paths remain contained, modes fail closed, and no unowned cleanup occurs.
- Derived artifact currency: pass for the corrected M2 identities; M4 remains responsible for package publication proof.
- Unrelated changes: pass; the correction is the one predicate change, one T04 fixture, and current M2 evidence.
- Validation evidence: pass; exact suites were rerun and supplemented with independent correction, mutation, identity, recovery, and privacy probes.

## Clean-review sufficiency receipt

Review target identity: sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190
Governing artifacts inspected: constitution; approved feature spec R3-R17/R33-R34; approved test spec T02-T05; accepted ADR; active plan M2; current change record; corrected implementation, tests, and M2 evidence; prior R8/R9 records only after independent verdict formation
Adversarial hypotheses tested: regular-file component leaks raw ENOTDIR; sentinel or nested path mutates; one of six destructive operations lacks adjacent validation; post-open identity substitution publishes; ordinary inspection EIO mutates; partial rotation corrupts or over-retains logs; concurrent writers produce partial records; stale-lock recovery removes another lock; private markers serialize; resources escape bounds; evidence hashes are stale
Direct proofs performed: regular-file correction reproduction; six-operation order trace; ordinary-EIO no-mutation probe; unlink and five rename-position recovery probe; post-open inode mismatch probe; prohibited-marker probe; C02; C01; boundary validation; relevant diff check; target hash and node_modules-absence checks
Validation evidence challenged: passing totals were checked against source behavior and supplemented with direct correction, identity, every-mutation, and every-partial-rotation-position probes
Unreviewed surfaces: M3 full public integration and lookup, M4 token/package proof, workflow lifecycle mutation, final cross-milestone coherence, hosted CI, and native execution on non-POSIX platforms remain downstream
Confidence: high for the corrected frozen M2 bundle and approved threat model
No-finding rationale: the R8 failure is unreproducible after the exact bounded correction, every full-M2 falsifiable boundary hypothesis passed direct inspection or execution, current evidence matches exact target identities, and no contradictory behavior or proof gap remains

## Handoff

Distinct clean agreement is established between R9 and R10 on the identical corrected bundle hash. The M2 code-review gate is clean. Because this invocation is isolated and explicitly forbids lifecycle advancement, `change.yaml` remains `review-requested`; workflow owns any later milestone settlement and routing to M3.
