# Code Review M2 R13: Distinct Descriptor-Cleanup Review

Review ID: code-review-m2-r13
Stage: code-review
Round: r13
Reviewer: distinct fresh independent reviewer
Reviewer context ID: m2-r13-second-clean-review
Author context ID: root-m2-r11-correction
Target: corrected frozen M2 logging-core implementation, tests, and evidence
Reviewed artifact: M2 implementation/test/evidence diff bundle `sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff`
Reviewed milestone: M2
Review date: 2026-08-26
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Context separation mechanism: distinct fresh artifact-first review with independent source inspection and adversarial probes
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: privacy-sensitive-persistence; filesystem-containment; destructive-rotation; concurrent-writer-recovery; bounded-blocking; descriptor-lifetime; evidence-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
Formal criteria: code-review-v1; independent-review-gate-v1; requirement-fidelity-gate-v1; boundary-first-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:7a458a3630151894b752dd580fab68ceecbd437410e0c244eea2bdf4afdb8ede; packages/rigorloop/dist/lib/log-config.js@working-tree#sha256:6b6d8fb56077b3359ae47b21bc9aab401e2510beb985ffe5fc5d43a6da070b9a; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:6390ebe735b91123fa8b3e759a47a7d7381bffc045de1eee28c5095494c641a9; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:54431690ea256ce082200cde842e783ee2ce207d469af6697376392caa888506; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:8ddafcefb79fa2f748f5c252e3b14794e5b429131c98470884a1f9abaa02ec5e
Prompt template version: code-review-v1
Initial packet hash: sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: bounded descriptor release after injected acquisition and close faults, including descriptor-number reuse before ownership identity is captured
Highest-impact failure modes: closing a reused unowned descriptor; leaked owned descriptor; suppressing stable degradation; stale proof claiming identity-safe cleanup
Changed boundaries: owned synchronous filesystem descriptor release to stable diagnostic-only failure
Evidence expected: exact R13-R15/R34 and T05 proof for every post-open failure state, including known and not-yet-known descriptor identity
Areas requiring direct inspection: `log-sink.js`; T05 descriptor tests; M2 evidence; R11/R12 review and disposition
Areas intentionally out of scope: implementation correction; M3 and M4 completion; lifecycle mutation; final verification; PR readiness
Risk classes considered: requirement fidelity; privacy; filesystem containment; identity reuse; destructive recovery; concurrency; descriptor lifetime; bounded work; semantic isolation; proof accuracy
Falsifiable review questions: Can acquisition fail before identity capture and then close a reused descriptor? Does trusted cleanup distinguish known and unknown original identity? Do the seven known-identity paths imply safety for acquisition cleanup?
Automated review: yes
Material findings: CLIOBS-M2-R13-F1
Immediate next stage: review-resolution
Automatic downstream handoff: none; explicit isolated review stops on material finding
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r13.md`; `review-log.md`; `review-resolution.md`
- Open blockers: `CLIOBS-M2-R13-F1`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M2-R13-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r13.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M2-R13-F1
- Verify readiness: not-claimed

## Finding CLIOBS-M2-R13-F1

Finding ID: CLIOBS-M2-R13-F1
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:78-86`, specifically `closeOwned(fd, null, io)` after acquisition `fstatSync` fails, and missing coverage after `packages/rigorloop/test/cli-observability.test.js:422`
Evidence: `acquire()` opens the exclusive lock and calls the injected `io.fstatSync(fd)` before it has recorded an identity. If that inspection throws, cleanup calls `closeOwned(fd, null, io)`. A direct probe made the injected close adapter close that owned descriptor, reopen a different file on the same descriptor number, and throw. Because `expected` was null, `closeOwned` accepted the replacement and its trusted native `closeSync` closed the unowned replacement. The append returned stable `RL_LOG_UNAVAILABLE`, but native `fstatSync(replacementFd)` returned `EBADF`. The seven tracked throw-before-close cases and the R12 different-inode probe all exercise paths with a known expected identity, so they do not cover this acquisition state.
Required outcome: Cleanup after every post-open acquisition fault must release the originally owned descriptor without closing a different inode that reuses its descriptor number, including when the injected first identity inspection fails. Add identity-stable proof for acquisition `fstatSync` failure combined with close/reopen/throw reuse, while retaining stable `RL_LOG_UNAVAILABLE`, fail-closed lock retention, and the existing seven known-identity cleanup cases.
Safe resolution path: Capture an identity through a trusted bounded inspection before invoking a fallible injected close when acquisition has not established one, or otherwise use a bounded cleanup design that can distinguish the original descriptor from same-number reuse. Rerun the acquisition-failure, seven-path, already-closed, same-number/different-inode, focused C02, and package C01 proofs; refresh M2 evidence and the frozen bundle identity; then obtain fresh holistic independent review agreement on the new hash.
needs-decision rationale: none; T05's post-open cleanup and unowned-resource safety boundary make this directly actionable within M2.

## Actual-diff and boundary assessment

- Descriptor cleanup: concern. Known-identity active-read, ordinary-validation, rotation, already-closed, and reused-inode paths are handled, but acquisition cleanup before identity capture can close an unowned reused descriptor.
- Spec and test alignment: concern. T05 requires post-open fault and no-surviving-resource proof, while the evidence states that a mismatched reused descriptor is never closed without limiting that claim to known identity.
- Privacy, containment, mutation cadence, rotation, concurrency, and semantic isolation: no contrary material issue was established before the stop condition; these surfaces remain subject to holistic rereview after correction.
- Evidence adequacy: concern. R12's clean receipt and M2 evidence overgeneralize the known-identity probe to the acquisition path.

## Checklist coverage

- Spec alignment: concern; the unowned replacement close conflicts with the R14/T05 fail-closed resource boundary.
- Test coverage: concern; acquisition `fstatSync` failure checks a close count but not same-number replacement identity.
- Edge cases: concern; identity-unknown acquisition cleanup is unproved and directly fails.
- Error handling: concern; the stable error is correct, but trusted cleanup closes the wrong descriptor.
- Architecture boundaries: concern; the bounded synchronous sink crosses descriptor ownership under one supported injected post-open fault composition.
- Compatibility: pass for the observed stable error classification; no semantic exit change was found by this probe.
- Security/privacy: concern; descriptor ownership is violated, although this probe found no private-value persistence or pathname escape.
- Derived artifact currency: pass for identity matching only; the current evidence claim is semantically stale.
- Unrelated changes: pass; the reviewed target is the frozen M2 bundle.
- Validation evidence: concern; the direct failing acquisition-reuse probe invalidates clean promotion regardless of passing broader suites.

## Validation evidence challenged

- Independent `sha256sum` verification matched all twelve manifest constituents and the supplied frozen aggregate identity `sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff`.
- Direct acquisition identity-reuse probe: append returned `RL_LOG_UNAVAILABLE`; after the injected acquisition `fstatSync` failure and close/reopen/throw sequence, native `fstatSync` on the replacement descriptor returned `EBADF`, proving the sink closed the reused unowned descriptor.
- C02 and C01 were not rerun after the material finding because the formal review stop condition forbids continuing toward a clean handoff; their prior passing results cannot override the direct failure.

## Prior-finding reconciliation and handoff

R12 and R13 do not establish distinct clean agreement on the identical frozen hash. R12 is clean, but R13 finds `CLIOBS-M2-R13-F1` on that exact target. This isolated review records the finding and stops: there is no lifecycle advancement, automatic downstream handoff, verification claim, CI claim, or PR-readiness claim. Review-resolution and implementation correction must precede a new frozen identity and fresh holistic rereview.
