# Code Review M2 R4: Logging-Core Correction Rereview

Review ID: code-review-m2-r4
Stage: code-review
Round: r4
Reviewer: independent agent reviewer
Reviewer context ID: m2-r4-independent-review
Target: corrected M2 logging-core implementation
Reviewed artifact: M2 implementation/test diff bundle `sha256:a44b241a35c3c12082d5a47e7c71e61ac8893db624f778a271860d1e3168ba98`
Reviewed milestone: M2
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Context separation mechanism: separate-agent blind-first review
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: privacy-sensitive-persistence; filesystem-containment; destructive-rotation; concurrency; recovery; cross-platform-behavior; evidence-overclaim
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Reviewed correction evidence: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md` at `sha256:dea6dcace0a11a7d79cbd063d1fcca78474b2fc7d3dd1e40cc04110490193f64`
Formal criteria: code-review-v1; boundary-first-v1
Initial packet inventory: specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:8df259dc5e97efa06535f785c25d575c366e2864b1fd88abde96fba6075b4fd4; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:1727bf2c95fb804f9184f0124a9880f0a3b249fcb7d008dac9b76bac04c3fab8; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:753b48cc7c77dbdd5b54ba1164375f0fb62ac9f974378e09bda988aff012bb11; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:c3e073cfb1129d3a5e592cdedfb9eed2db4e84edd586e9fcd1b4b7d8c9e0bef3; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:dea6dcace0a11a7d79cbd063d1fcca78474b2fc7d3dd1e40cc04110490193f64
Prompt template version: code-review-v1
Initial packet hash: sha256:a44b241a35c3c12082d5a47e7c71e61ac8893db624f778a271860d1e3168ba98
Manifest owner: direct-user-invocation
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: diagnostic event schema, owned-path persistence, rotation, lock publication, post-open recovery, and M2 proof completeness
Highest-impact failure modes: mutation of a substituted external directory; publication or deletion of unowned files; descriptor leakage and poisoned retries; invalid event ordering; unsupported M2 closeout
Changed boundaries: normalized diagnostic facts to event builder, validated filesystem paths to destructive operations, and synchronous resource acquisition to cleanup
Evidence expected: exact R5/R11/R14/R15 behavior and complete T02-T05 direct proof
Areas requiring direct inspection: diagnostic-event.js; log-sink.js; focused tests; M2 evidence; all prior M2 dispositions
Areas intentionally out of scope: M3 lookup behavior except retained-surface safety; token benchmark; package publication; final verification
Risk classes considered: semantic isolation; privacy; filesystem containment; destructive operations; concurrency; resource recovery; proof adequacy
Falsifiable review questions: Can a validated pathname be replaced before rename or unlink? Does every post-open fault close its descriptor and permit later use? Are event and sequence closed as a pair? Does evidence prove every claimed T02-T05 boundary?
Automated review: yes
Material findings: CLIOBS-M2-R4-F1, CLIOBS-M2-R4-F2, CLIOBS-M2-R4-F3, CLIOBS-M2-R4-F4
Immediate next stage: review-resolution
Automatic downstream handoff: none; direct review-only invocation
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r4.md`; `review-log.md`; `review-resolution.md`
- Open blockers: four material M2 findings
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M2-R4-F1, CLIOBS-M2-R4-F2, CLIOBS-M2-R4-F3, CLIOBS-M2-R4-F4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r4.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M2-R4-F1, CLIOBS-M2-R4-F2, CLIOBS-M2-R4-F3, CLIOBS-M2-R4-F4
- Verify readiness: not-claimed

## Finding CLIOBS-M2-R4-F1

Finding ID: CLIOBS-M2-R4-F1
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:16-50,101-129,136-156`
Evidence: Deterministic replacement probes demonstrated three check/use failures. Replacing `.rigorloop-log.lock` after identity validation caused the unowned replacement to be published as `rigorloop.jsonl`. Replacing `rigorloop.4.jsonl` after validation caused the unowned replacement to be unlinked. Replacing the validated root with a symlink during candidate writing rotated files in the external target before the sink returned `RL_LOG_UNAVAILABLE`.
Required outcome: Root, publication, archive deletion, and archive rename operations remain containment- and identity-bound through every destructive action.
Safe resolution path: Use an ownership-bound persistence protocol for each destructive action. If the Node filesystem interface cannot enforce the approved invariant, return the constraint to the architecture owner rather than weakening R11 or R14 implicitly.
needs-decision rationale: none

## Finding CLIOBS-M2-R4-F2

Finding ID: CLIOBS-M2-R4-F2
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:57-98`
Evidence: Injecting failure on the second `fstatSync()` inside `openOwned()` returned `RL_LOG_UNAVAILABLE` but left an open descriptor to `rigorloop.jsonl`. The corrected acquisition path closes its descriptor, but intentionally retains the fixed lock, so the regression proves that the next append is also unavailable. This does not satisfy the accepted R3 outcome of no surviving descriptor or lock and a usable later attempt.
Required outcome: Every post-open failure closes its descriptor, and recovery behavior either satisfies the accepted retry disposition or is formally revised with governing justification.
Safe resolution path: Treat `openOwned()` and acquisition as explicit resource transactions, test descriptor counts, and prove successful subsequent use for every recoverable post-open fault.
needs-decision rationale: none

## Finding CLIOBS-M2-R4-F3

Finding ID: CLIOBS-M2-R4-F3
Severity: minor
Location: `packages/rigorloop/dist/lib/diagnostic-event.js:43-45,92-109`
Evidence: Direct construction accepted `invocation-start` with `sequence: 2` and `invocation-complete` with `sequence: 1`, although the schema fixes start at sequence 1 and completion at sequence 2.
Required outcome: Event kind and sequence are validated as a closed pair.
Safe resolution path: Reject mismatched event/sequence pairs before serialization and add exact mismatch and unknown-value regressions.
needs-decision rationale: none

## Finding CLIOBS-M2-R4-F4

Finding ID: CLIOBS-M2-R4-F4
Severity: major
Location: `packages/rigorloop/test/cli-observability.test.js`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md:22-38,56`
Evidence: The tests do not cover the reproduced root replacement, final publication, archive unlink, or `openOwned()` descriptor-leak paths. `_getActiveHandles()` does not prove synchronous descriptor closure. The evidence claims replacement-lock race safety, post-open descriptor closure, and no surviving handle despite the reproduced counterexamples, and its handoff describes eight findings although the correction target contains twelve.
Required outcome: Add direct proof for all reproduced boundaries and restrict evidence claims to demonstrated outcomes.
Safe resolution path: Add exact regressions for the direct probes, rerun C02 and C01, refresh target identities and counts, and reconcile all twelve prior findings truthfully.
needs-decision rationale: none

## Prior-finding reconciliation

Six prior findings are fully resolved: `CLIOBS-M2-L1-F1`, `CLIOBS-M2-L1-F2`, `CLIOBS-M2-L1-F3`, `M2-L1B-F1`, `M2-L1B-F3`, and `CLIOBS-M2-R3-F1`. Six remain open or only partially resolved: `CLIOBS-M2-L1-F4`, `M2-L1B-F2`, `M2-L1B-F4`, `CLIOBS-M2-R3-F2`, `CLIOBS-M2-R3-F3`, and `CLIOBS-M2-R3-F4`.

## Checklist

- Spec alignment: concern; R11/R14 and fixed event ordering fail.
- Test coverage: block; reproduced races and descriptor leak lack regressions.
- Edge cases: concern; destructive-operation windows remain.
- Error handling: concern; one post-open descriptor leaks and recovery contradicts its accepted disposition.
- Architecture boundaries: block; validated root and identity are not bound to the operation.
- Compatibility: pass within M2 scope.
- Security/privacy: block; rotation can mutate a substituted external root.
- Derived artifact currency: pass/not applicable.
- Unrelated changes: pass for the reviewed M2 bundle.
- Validation evidence: concern; passing suites are contradicted by direct probes.

## Validation

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` — 37 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 238 passed, 0 failed.
- `git diff --check` — passed.
- Direct adversarial probes reproduced mismatched event/sequence acceptance, unowned publication, unowned archive deletion, an `openOwned()` descriptor leak, and external-root rotation. A real held-lock attempt completed in 978.011 ms.

## Review sufficiency

This is a distinct L1 review of an elevated-risk target. Because it found material defects, clean-review agreement and milestone promotion are not applicable. M2 remains in review-resolution and requires bounded correction followed by fresh independent rereview. No workflow continuation or verify readiness is claimed.
