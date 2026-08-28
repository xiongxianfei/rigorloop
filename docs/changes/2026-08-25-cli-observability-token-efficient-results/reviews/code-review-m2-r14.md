# Code Review M2 R14: Acquisition-Identity Correction Rereview

Review ID: code-review-m2-r14
Stage: code-review
Round: r14
Reviewer: fresh independent correction reviewer
Reviewer context ID: m2-r14-acquisition-correction-rereview
Author context ID: root-m2-r13-correction
Target: corrected frozen M2 logging-core implementation, tests, and evidence
Reviewed artifact: M2 implementation/test/evidence diff bundle `sha256:e6de92ecf6a84f9b20b05d28d0773d1b99b9c0c0060c4d882c05473e601c907f`
Reviewed milestone: M2
Review date: 2026-08-26
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Native review status: clean-with-notes
Review gate outcome: advance
Independence level: L1
Context separation mechanism: fresh artifact-first correction review with independent packet freezing, source inspection, and adversarial probes
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: privacy-sensitive-persistence; filesystem-containment; destructive-rotation; concurrent-writer-recovery; bounded-blocking; descriptor-lifetime; evidence-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
Formal criteria: code-review-rereview-v1; independent-review-gate-v1; requirement-fidelity-gate-v1; boundary-first-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:7a458a3630151894b752dd580fab68ceecbd437410e0c244eea2bdf4afdb8ede; packages/rigorloop/dist/lib/log-config.js@working-tree#sha256:6b6d8fb56077b3359ae47b21bc9aab401e2510beb985ffe5fc5d43a6da070b9a; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:65fd6fa394e24d389c079c44765ff0b46add4ab6223140191bd9dd63956f99d5; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:4f47224080fc9d2266be1af2d10051d87a7327118d7720166d69bfef74c89f3f; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:2b4a05ecead3421ed3c518876b04ead74e737957ca9d048f1e4d2df3e2e1719d
Prompt template version: code-review-v1
Initial packet hash: sha256:e6de92ecf6a84f9b20b05d28d0773d1b99b9c0c0060c4d882c05473e601c907f
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: bounded descriptor release after acquisition identity inspection or close faults, including descriptor-number reuse before the injected acquisition inspection
Highest-impact failure modes: closing a reused unowned descriptor; leaking an owned descriptor; weakening fail-closed lock retention; corrupting retained JSONL; stale evidence
Changed boundaries: trusted acquisition identity capture and owned synchronous filesystem descriptor release to stable diagnostic-only failure
Evidence expected: R3-R17/R33-R34 and T02-T05 proof, including acquisition inspection failure, seven known-identity throw-before-close positions, already-closed cleanup, same-number different-inode refusal, rotation, concurrency, privacy, containment, and semantic isolation
Areas requiring direct inspection: `diagnostic-event.js`; `log-config.js`; `log-sink.js`; `cli-observability.js`; T02-T05 tests; M2 evidence; R13 finding and disposition
Areas intentionally out of scope: M3 and M4 completion; lifecycle mutation; final verification; hosted CI; PR readiness
Risk classes considered: requirement fidelity; privacy; filesystem containment; identity reuse; destructive recovery; concurrency; descriptor lifetime; bounded work; semantic isolation; proof accuracy
Falsifiable review questions: Does acquisition establish trusted identity before injected inspection? Can close/reopen/throw close the replacement? Does every known-identity path end invalid? Does ordinary acquisition failure close the owned descriptor? Are rotation, containment, privacy, concurrency, and semantic isolation still intact?
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
- Artifacts changed: `reviews/code-review-m2-r14.md`; `review-log.md`; `review-resolution.md`
- Open blockers: elevated-risk corrected M2 requires a distinct second clean independent review on the identical hash
- Next stage: blocked pending distinct second independent code review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r14.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: blocked
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Correction verification

`CLIOBS-M2-R13-F1` is resolved on the reviewed hash. `acquire()` now captures the opened lock's device/inode through trusted native `fstatSync` before calling the injected identity inspection. If the trusted capture itself fails, native `closeSync` closes the still-owned descriptor. If the later injected inspection or injected close fails, `closeOwned` compares the trusted identity before any cleanup close and refuses a same-number different-inode replacement. The fixed lock remains deliberately retained and subsequent attempts fail closed.

The direct acquisition probe injected the later acquisition `fstatSync` failure, then made the close adapter close the lock descriptor, reopen a different inode on the same descriptor number, and throw. The append returned `RL_LOG_UNAVAILABLE`; `.rigorloop-log.lock` remained; a second append returned `RL_LOG_UNAVAILABLE`; and native `fstatSync` confirmed the replacement descriptor remained valid until the probe owner closed it. The focused tracked matrix separately proves ordinary acquisition failure closes its descriptor, all seven known-identity active-read/ordinary-validation/rotation throw-before-close positions end in `EBADF`, and active-file inspection failure closes both owned descriptors. Independent probes proved already-closed-then-throw ends in `EBADF` and known-identity same-number/different-inode mismatch leaves the replacement valid.

Holistic rereview found no adjacent regression. Event construction remains allowlist-only and size-bounded; prohibited values are absent; platform roots, permissions, symlink/non-directory classification, and six adjacent pathname-mutation checks fail closed; rotation remains pre-append and five-file bounded; real concurrent writers retain complete JSONL; lock attempts remain bounded; diagnostic failure remains semantically isolated; and the logging core adds no network, child process, database, timer, or surviving handle dependency.

## Checklist coverage

- Spec alignment: pass; R3-R17 and R33-R34 remain satisfied within the approved ADR threat boundary.
- Test coverage: pass; T02-T05 directly exercise the corrected acquisition composition and the adjacent privacy, path, mutation, rotation, concurrency, and bounded-resource paths.
- Edge cases: pass; identity-not-yet-injected, identity-known, already-invalid, matching, mismatched, ordinary, and rotating descriptor states were directly challenged.
- Error handling: pass; trusted acquisition capture plus one bounded identity-aware cleanup preserves stable degradation without an unowned close or owned leak.
- Architecture boundaries: pass; the synchronous built-in sink, fixed owned names, fail-closed lock retention, and explicit pathname-race limitation are unchanged.
- Compatibility: pass; C01 passed and diagnostic failure did not alter semantic result or exit behavior.
- Security/privacy: pass; no prohibited-value persistence, outside-path mutation, permission repair, or unowned descriptor close was found.
- Derived artifact currency: pass for all twelve frozen constituents; M4 package parity remains outside this milestone review.
- Unrelated changes: pass; the correction is confined to acquisition identity capture, its regression proof, and M2 evidence.
- Validation evidence: pass; independent direct probes, C02, C01, constituent hashes, and evidence claims agree.

## Validation evidence challenged

- Frozen packet: the SHA-256 of the exact 1,692-byte semicolon-separated 12-entry inventory recorded above, with no trailing newline, is `sha256:e6de92ecf6a84f9b20b05d28d0773d1b99b9c0c0060c4d882c05473e601c907f`.
- Targeted descriptor matrix: 4/4 passed for seven known-identity pre-close positions, ordinary acquisition failure, acquisition same-number replacement safety, and active-file validation cleanup.
- Direct acquisition close/reopen/throw probe: `{"code":"RL_LOG_UNAVAILABLE","lock_retained":true,"replacement_valid":true,"second_attempt":"RL_LOG_UNAVAILABLE"}`.
- Direct already-closed and known-identity mismatch probes: `{"already_closed_code":"RL_LOG_UNAVAILABLE","already_closed_post":"EBADF","known_identity_mismatch_code":"RL_LOG_UNAVAILABLE","known_identity_replacement":"valid"}`.
- C02, `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js`: passed 43/43 after the locked dependency installation. The initial dependency-free attempt passed all 29 logging tests but correctly failed to load the renderer because `yaml` was absent; it was not counted as validation success.
- C01, `npm test --prefix packages/rigorloop`: passed 244/244.
- Source inspection and the C02 matrix confirmed all six rotation/publication mutations receive adjacent validation, validation failure performs zero guarded mutations, and retained concurrency output remains complete JSONL.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-25-cli-observability-token-efficient-results`: passed with 48 reviews, 51 findings, 48 log entries, and 51 resolution entries.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r14.md --path docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md --path docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`: blocked on the untouched `change.yaml` because `workflow.automation.stop_reason` is missing. This prevents lifecycle-readiness claims but does not contradict the direct M2 implementation verdict; this isolated review is forbidden from repairing routing state.
- `git diff --check`: passed. Temporary locked dependencies were removed from the worktree after validation, and `packages/rigorloop/node_modules` is absent.

## Clean-review sufficiency receipt

Review target identity: sha256:e6de92ecf6a84f9b20b05d28d0773d1b99b9c0c0060c4d882c05473e601c907f
Governing artifacts inspected: constitution; approved feature spec R3-R17/R33-R34 and boundary/interaction model; approved test spec T02-T05; accepted ADR; active plan M2; current change record; implementation, tests, M2 evidence, R13 finding, and current disposition
Adversarial hypotheses tested: acquisition inspection fails before injected identity; close/reopen/throw closes an unowned inode; ordinary acquisition failure leaks; seven known-identity descriptors survive; already-closed cleanup retries unsafely; identity mismatch is ignored; trusted cleanup weakens lock retention; correction regresses privacy, containment, mutation cadence, rotation, concurrency, bounded work, or semantic isolation
Direct proofs performed: corrected acquisition close/reopen/throw probe; four-test targeted descriptor matrix; already-closed-then-throw probe; known-identity same-number replacement probe; C02 43 tests; C01 244 tests; twelve-constituent hashing; source and diff inspection
Validation evidence challenged: recorded totals and M2 evidence were mapped back to named T02-T05 tests and supplemented with independent descriptor-validity probes
Unreviewed surfaces: M3/M4 completion, final cross-milestone coherence, hosted CI, non-POSIX runtime execution, and final verification remain downstream
Confidence: high for the corrected frozen M2 bundle and approved local filesystem threat model
No-finding rationale: trusted identity is now captured before the injected acquisition failure can reuse the descriptor, every supported later cleanup is identity-bound and bounded, all owned descriptors are released without closing replacements, and adjacent M2 contract proofs remain green.

## Prior-finding reconciliation and handoff

`CLIOBS-M2-R13-F1` is resolved, and no new material finding was discovered. This is the first clean independent review of corrected bundle `sha256:e6de92ecf6a84f9b20b05d28d0773d1b99b9c0c0060c4d882c05473e601c907f`. It does not advance lifecycle state or close M2. A distinct second clean independent review of this exact corrected target is still required before workflow may settle the milestone.
