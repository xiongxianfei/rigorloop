# Code Review M2 R12: Descriptor-Lifetime Correction Rereview

Review ID: code-review-m2-r12
Stage: code-review
Round: r12
Reviewer: fresh independent correction reviewer
Reviewer context ID: m2-r12-descriptor-correction-rereview
Author context ID: root-m2-r11-correction
Target: corrected frozen M2 logging-core implementation, tests, and evidence
Reviewed artifact: M2 implementation/test/evidence diff bundle `sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff`
Reviewed milestone: M2
Review date: 2026-08-26
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Native review status: clean-with-notes
Review gate outcome: advance
Independence level: L1
Context separation mechanism: fresh artifact-first correction review before prior-finding reconciliation
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: privacy-sensitive-persistence; filesystem-containment; destructive-rotation; concurrent-writer-recovery; bounded-blocking; descriptor-lifetime; evidence-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
Formal criteria: code-review-rereview-v1; independent-review-gate-v1; requirement-fidelity-gate-v1; boundary-first-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:7a458a3630151894b752dd580fab68ceecbd437410e0c244eea2bdf4afdb8ede; packages/rigorloop/dist/lib/log-config.js@working-tree#sha256:6b6d8fb56077b3359ae47b21bc9aab401e2510beb985ffe5fc5d43a6da070b9a; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:6390ebe735b91123fa8b3e759a47a7d7381bffc045de1eee28c5095494c641a9; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:54431690ea256ce082200cde842e783ee2ce207d469af6697376392caa888506; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:8ddafcefb79fa2f748f5c252e3b14794e5b429131c98470884a1f9abaa02ec5e
Prompt template version: code-review-v1
Initial packet hash: sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: bounded descriptor release after injected close failure and its interaction with active reads, ordinary validation, rotation, identity reuse, stable degradation, and retained-log integrity
Highest-impact failure modes: leaked owned descriptor; closing a reused unowned descriptor; suppressing the first close failure; incomplete retained JSONL; containment or semantic-isolation regression; stale evidence
Changed boundaries: owned synchronous filesystem descriptor release to stable diagnostic-only failure
Evidence expected: exact R3-R17/R33-R34 and T02-T05 proof, including active-read, ordinary-validation, five rotation-held close-before-release faults, already-closed-then-throw, identity mismatch, and adjacent privacy/filesystem/concurrency guarantees
Areas requiring direct inspection: `log-sink.js`; T02-T05 tests; M2 evidence; R11 finding and disposition; adjacent controller isolation
Areas intentionally out of scope: M3 feature completion; M4 benchmark/package proof; lifecycle routing; final verification; PR readiness
Risk classes considered: requirement fidelity; privacy; filesystem containment; identity reuse; destructive recovery; concurrency; descriptor lifetime; bounded work; semantic isolation; proof accuracy
Falsifiable review questions: Does a first close failure leave any owned descriptor valid? Does an already-invalid descriptor avoid unsafe retry? Can a synchronously reused descriptor be closed despite inode mismatch? Are all five rotation-held paths covered? Did the helper regress stable errors, retained completeness, contention, or semantic results?
Automated review: yes
Material findings: none
Immediate next stage: distinct second independent clean review
Automatic downstream handoff: none; explicit isolated review and elevated-risk second-review gate
Milestone closeout: blocked pending distinct clean agreement on the corrected hash
Required review-resolution: no
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r12.md`; `review-log.md`; `review-resolution.md`
- Open blockers: elevated-risk corrected M2 requires a distinct second clean independent review on the identical hash
- Next stage: blocked pending distinct second independent code review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r12.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: blocked
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Correction verification

`CLIOBS-M2-R11-F1` is resolved on the reviewed hash. Every sink-owned descriptor release now passes through `closeOwned`. When the injected close reports failure, the helper preserves that first error, checks descriptor validity with the trusted native `fstatSync`, treats native `EBADF` as proof that no cleanup close is needed, refuses a known device/inode mismatch, and otherwise makes exactly one trusted native `closeSync` attempt before propagating failure. The public append boundary continues to return the stable `RL_LOG_UNAVAILABLE` classification.

The identity-stable T05 matrix directly throws before close for active read, ordinary pre-publication validation, the oldest archive, archives three through one, and active rotation. All seven cases returned `RL_LOG_UNAVAILABLE` and native `fstatSync` reported `EBADF` after return. A separate already-closed-then-throw probe also returned `RL_LOG_UNAVAILABLE` with post-return `EBADF`. A separate close/reopen probe forced reuse of the same descriptor number for a different inode; the helper detected the mismatch and left the replacement descriptor valid, proving it did not close an unowned reused identity.

The correction does not broaden the accepted filesystem threat model or alter pathname mutation ownership. The full focused and package suites retained the T02-T05 privacy, restrictive-path, six-site adjacent validation, rotation completeness, real concurrent-writer, lock-bound, interruption, resource-bound, and semantic-isolation proofs. Source inspection found no new network, process, database, timer, asynchronous worker, or unbounded traversal path.

## Checklist coverage

- Spec alignment: pass; R3-R17 and R33-R34 remain satisfied within the approved ADR threat boundary.
- Test coverage: pass; the correction has direct active-read, ordinary-validation, and five rotation-held pre-close fault proof, plus independent already-closed and reused-identity probes.
- Edge cases: pass; open, already invalid, known matching, known mismatched, ordinary, rotating, and acquisition-related descriptor states were inspected.
- Error handling: pass; one trusted inspection and at most one trusted cleanup attempt preserve stable diagnostic degradation and avoid an unowned close.
- Architecture boundaries: pass; the synchronous built-in sink, five fixed names, fail-closed lock retention, and stated pathname-race limitation are unchanged.
- Compatibility: pass; C01 passed and public semantic output and exit behavior remain isolated from diagnostic faults.
- Security/privacy: pass; no private-value or outside-path mutation regression was found, and mismatched descriptor reuse is refused.
- Derived artifact currency: pass for the frozen M2 identities; M4 package parity remains out of scope.
- Unrelated changes: pass; the reviewed correction is limited to descriptor release, exact regression proof, and M2 evidence.
- Validation evidence: pass; recorded identities, focused totals, full-suite totals, and adversarial probes agree.

## Validation evidence challenged

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js`: passed 42/42 after locked dependency installation.
- `npm test --prefix packages/rigorloop`: passed 243/243.
- Direct already-closed-then-throw probe: `RL_LOG_UNAVAILABLE`; the faulted descriptor returned native `EBADF` after append.
- Direct reused-identity probe: the close adapter closed the active descriptor, reopened a different inode on the same descriptor number, and threw; append returned `RL_LOG_UNAVAILABLE`, while native `fstatSync` still succeeded on the replacement until the probe explicitly closed it.
- `sha256sum` checks matched every implementation and test identity recorded in `m2-logging-core.md`; the reviewed bundle identity is `sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff`.
- `git diff --check`: passed before review recording.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-25-cli-observability-token-efficient-results`: passed with 46 reviews, 50 findings, 46 log entries, and 50 resolution entries.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r12.md --path docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md --path docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`: blocked on the untouched `change.yaml` because `workflow.automation.stop_reason` is missing. This prevents lifecycle-readiness claims but does not contradict the directly established M2 implementation verdict; this review is forbidden from repairing lifecycle routing state.
- Temporary `packages/rigorloop/node_modules/` created for C01/C02 was removed after validation.

## Clean-review sufficiency receipt

Review target identity: sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff
Governing artifacts inspected: constitution; approved feature spec R3-R17/R33-R34; approved test spec T02-T05; accepted ADR; active plan M2; current change record; implementation, tests, evidence, R11 finding, and prior M2 dispositions
Adversarial hypotheses tested: first close failure leaks; already-closed retry is unsafe; descriptor-number reuse closes an unowned inode; one rotation-held descriptor escapes; stable failure changes semantic output; correction regresses privacy, containment, mutation cadence, concurrency, or bounded resources
Direct proofs performed: seven-case pre-close regression matrix; already-closed-then-throw probe; same-number different-inode reuse probe; C02 42 tests; C01 243 tests; source and identity inspection; diff validation
Validation evidence challenged: test totals were mapped to exact T02-T05 cases and supplemented with independent validity and identity-reuse probes
Unreviewed surfaces: M3/M4 completion, final cross-milestone coherence, hosted CI, non-POSIX runtime execution, and final verification remain downstream
Confidence: high for the corrected frozen M2 bundle and approved threat model
No-finding rationale: the corrected helper closes every still-owned descriptor after one injected close failure, avoids retrying an already-invalid descriptor, refuses a demonstrably reused identity, preserves stable failure behavior, and leaves the adjacent M2 contract green under focused and full-package proof.

## Prior-finding reconciliation and handoff

`CLIOBS-M2-R11-F1` is resolved, and no new material finding was discovered. This is the first clean independent review of corrected bundle `sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff`. It does not advance lifecycle state or close M2. A distinct second clean independent review of this exact corrected target is still required before workflow may settle the milestone.
