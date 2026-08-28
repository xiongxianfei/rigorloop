# Code Review M2 R9: Unsafe-Component Correction Rereview

Review ID: code-review-m2-r9
Stage: code-review
Round: r9
Reviewer: fresh independent correction reviewer
Reviewer context ID: m2-r9-independent-correction-rereview
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
Context separation mechanism: fresh correction reviewer with exact frozen identities and direct adversarial proof
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: filesystem-containment; stable-error-mapping; destructive-rotation; concurrent-writer-recovery; evidence-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
Formal criteria: code-review-rereview-v1; independent-review-gate-v1; requirement-fidelity-gate-v1; boundary-first-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:7a458a3630151894b752dd580fab68ceecbd437410e0c244eea2bdf4afdb8ede; packages/rigorloop/dist/lib/log-config.js@working-tree#sha256:6b6d8fb56077b3359ae47b21bc9aab401e2510beb985ffe5fc5d43a6da070b9a; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:80d1a42bd1fbcd83408427ff687ec7b09419e7b3df4e1efcb61ee77f489a22d4; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:b749ddbd83df1061c049eb3c439be53fa53acd9934b3a368999052cdaeedfeec; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:3a08b11153c51a1aeaa8d088a0eb641278f3592c2e1308c0c1551aa54921c787
Prompt template version: code-review-v1
Initial packet hash: sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: existing-component containment validation and its interaction with root creation, lock acquisition, owned-path checks, and destructive mutation validation
Highest-impact failure modes: raw filesystem error escape; unsafe component accepted; correction rejecting valid roots; regression in six adjacent mutation checks; false resolution evidence
Changed boundaries: existing filesystem component shape to stable unsafe-path classification
Evidence expected: identity-equal T04 regression, exact source delta, focused T02-T05 tests, all-six mutation order, C02, and C01
Areas requiring direct inspection: `log-sink.js`; corrected T04 fixture; adjacent T05 mutation validation; M2 evidence; R8 finding and disposition
Areas intentionally out of scope: M3 integration beyond package regression evidence; M4 token and package proof; lifecycle advancement; final verification
Risk classes considered: requirement fidelity; filesystem containment; stable error mapping; recovery; concurrency; resource closure; proof adequacy
Falsifiable review questions: Does the original intermediate-regular-file fixture now return `RL_LOG_UNSAFE_PATH` without mutation? Is the production change limited to rejecting non-directories? Does the stricter component predicate reject valid owned files through a sibling path? Do all six destructive mutations retain adjacent root and source identity validation? Do focused and package suites remain green?
Automated review: yes
Material findings: none
Immediate next stage: distinct second independent clean review
Automatic downstream handoff: none; isolated review and elevated-risk second-review gate
Milestone closeout: blocked pending distinct second clean review of the corrected bundle
Required review-resolution: no
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r9.md`; `review-log.md`; `review-resolution.md`
- Open blockers: elevated-risk corrected M2 requires a distinct second clean review
- Next stage: blocked pending distinct second independent code review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r9.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: blocked
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Correction verification

`CLIOBS-M2-R8-F1` is resolved. The production delta adds only `|| !info.isDirectory()` to the existing-component rejection predicate. The identity-equal T04 fixture retains the original absolute nested root beneath an existing regular file and now proves `RL_LOG_UNSAFE_PATH`, unchanged `sentinel` bytes, and absence of the nested root. A separate direct reproduction returned `{"code":"RL_LOG_UNSAFE_PATH","sentinel":"sentinel","nestedExists":false}`.

The stricter predicate applies only while walking the selected root's components; owned log files remain validated separately as regular files. The exported append path still performed exactly six destructive mutations during a full rotation, and the direct operation trace confirmed root reinspection in each interval with the exact source `lstat` immediately preceding every unlink or rename. No adjacent R11/T05 regression was reproduced.

## Checklist coverage

- Spec alignment: pass; the correction implements the R11 non-directory component partition and stable unsafe-path result.
- Test coverage: pass; the original T04 reproduction is retained and the full T02-T05 suite passes.
- Edge cases: pass; absent nested roots, regular-file components, valid directories, owned regular files, and six destructive mutation intervals were exercised.
- Error handling: pass; raw `ENOTDIR` is replaced by `RL_LOG_UNSAFE_PATH` before creation or lock acquisition.
- Architecture boundaries: pass; the one-line predicate remains within the accepted non-following component walker.
- Compatibility: pass; C01 and C02 remain green and the correction changes only the unsupported unsafe path partition.
- Security/privacy: pass; sentinel bytes and containment remain unchanged, with no new serialized input.
- Derived artifact currency: pass for the corrected bundle identities; package parity remains M4-owned.
- Unrelated changes: pass; one production predicate, its exact T04 proof, and M2 evidence comprise the correction.
- Validation evidence: pass; focused, direct, C02, and C01 proofs agree with the corrected identities.

## Validation evidence challenged

- Direct focused suite: `node --test packages/rigorloop/test/cli-observability.test.js` passed 27/27.
- Direct R8 reproduction: returned `RL_LOG_UNSAFE_PATH`, preserved `sentinel`, and did not create the nested root.
- Direct R11/T05 operation probe: observed six mutations with adjacent root and exact-source validation.
- C02: `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` passed 41/41.
- C01: `npm test --prefix packages/rigorloop` passed 242/242.
- Temporary `packages/rigorloop/node_modules/` created for C01/C02 was removed from the worktree after validation.

## Clean-review sufficiency receipt

Review target identity: sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190
Governing artifacts inspected: constitution; approved feature spec R11-R15; approved test spec T04-T05; accepted ADR; active M2 plan and change state; corrected implementation, exact regression, evidence, and R8 disposition
Adversarial hypotheses tested: the original failure remains; stable classification masks mutation; the new predicate rejects valid paths; owned regular files are confused with root components; all-six mutation validation regresses; passing focused proof hides package regression
Direct proofs performed: exact T04 reproduction; focused 27-test logging suite; six-mutation operation trace; C02 41 tests; C01 242 tests; frozen identity checks
Validation evidence challenged: the evidence claim was matched to source identities and rerun commands rather than accepted from totals alone
Unreviewed surfaces: M3/M4 work, final cross-milestone coherence, hosted CI, and native non-POSIX execution remain downstream
Confidence: high for the corrected frozen M2 bundle and approved threat model
No-finding rationale: the exact R8 failure is corrected by the smallest predicate change, the identity-equal regression proves the stable boundary, and adjacent containment, mutation, concurrency, recovery, privacy, and package tests show no material regression

## Prior-finding reconciliation and handoff

`CLIOBS-M2-R8-F1` is resolved, and no new material finding was discovered. This is the first clean independent review of corrected bundle `sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190`. It does not advance lifecycle state or close M2. A distinct second clean independent review of this exact corrected target is still required before workflow may settle the milestone.
