# Code Review M2 R5: Contract-Aligned Logging-Core Rereview

Review ID: code-review-m2-r5
Stage: code-review
Round: r5
Reviewer: primary agent fresh-pass reviewer
Reviewer context ID: root-code-review-m2-r5-fresh-pass
Target: corrected M2 logging-core implementation
Reviewed artifact: M2 implementation/test diff bundle `sha256:0d3dd7524ac022763f7284e8892161c9a15ed2e62e9b7edd58b7d4c95c76ba35`
Reviewed milestone: M2
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L0
Context separation mechanism: fresh-pass artifact-and-criteria reset after correction
Author context excluded: false
Risk tier: elevated
Risk-tier triggers: filesystem-containment; pathname-mutation; concurrent-writer-recovery; privacy-sensitive-persistence; evidence-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Reviewed correction evidence: `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md` at `sha256:eaf5fa08170aba9f006818360d14a9c44390be93bffeeccdf456f820ae78e841`
Formal criteria: code-review-v1; boundary-first-v1
Initial packet inventory: specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/diagnostic-event.js@working-tree#sha256:7a458a3630151894b752dd580fab68ceecbd437410e0c244eea2bdf4afdb8ede; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:6bd67b056fb8e12ffee077f53ecd457da9c8a685c551a058e109dac0dabc05fb; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:b96167acdd3ac415ca02846758ff86a9b669ad7eaeb25055a6ecae364e826aa8; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:eaf5fa08170aba9f006818360d14a9c44390be93bffeeccdf456f820ae78e841
Prompt template version: code-review-v1
Initial packet hash: sha256:0d3dd7524ac022763f7284e8892161c9a15ed2e62e9b7edd58b7d4c95c76ba35
Manifest owner: direct-user-invocation
Forbidden initial context excluded: false
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: event schema enforcement, descriptor recovery, pre-mutation pathname validation, bounded locking, rotation, and M2 evidence
Highest-impact failure modes: divergence from the approved R11 check boundary; unsupported security claim; descriptor leakage; invalid event order; false M2 closeout
Changed boundaries: normalized facts to event builder, opened filesystem resources to cleanup, and validated path state to destructive operations
Evidence expected: direct R5/R11/R14/R15 proof plus exact T02-T05 and C01/C02 results
Areas requiring direct inspection: diagnostic-event.js; log-sink.js; focused tests; revised spec and ADR; M2 evidence; all prior M2 findings
Areas intentionally out of scope: M3 lookup behavior beyond retained-surface proof; token benchmark; package publication; final verification
Risk classes considered: semantic isolation; privacy; filesystem containment; concurrency; recovery; bounded blocking; proof adequacy
Falsifiable review questions: Are event and sequence closed as a pair? Does every post-open fault close? Does each pathname mutation receive the exact R11 root/component/owned-path check immediately before mutation? Does evidence avoid claims outside the approved threat model?
Automated review: yes
Material findings: CLIOBS-M2-R5-F1
Immediate next stage: review-resolution
Automatic downstream handoff: none; direct review-only invocation
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m2-r5.md`; `review-log.md`; `review-resolution.md`
- Open blockers: one material M2 finding
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M2-R5-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r5.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M2-R5-F1
- Verify readiness: not-claimed

## Finding CLIOBS-M2-R5-F1

Finding ID: CLIOBS-M2-R5-F1
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:112-162`
Evidence: Approved R11 requires the root, every existing component, and the affected owned path to be checked immediately before each owned pathname mutation. Rotation validates only the source object at lines 115-118, 123-126, and 130-133 before `unlinkSync` or `renameSync`; it does not rerun root/component validation or validate the destination at those mutation boundaries. Final candidate publication checks only lock identity at lines 161-162. The earlier complete-root validation at line 146 occurs before reading, candidate construction, write, fsync, and all rotation work, so it is not the required immediate pre-mutation check. Existing T04/T05 tests do not count or fault these per-mutation root/component checks.
Required outcome: Every supported `unlink` and `rename`, including final candidate publication, receives a deterministic root/component and affected-source/destination validation immediately before mutation, and direct tests fail if any boundary omits it.
Safe resolution path: Introduce one injected pre-mutation validator that reuses the approved no-follow and permission checks for the root, components, source, and existing destination; call it adjacent to every destructive pathname operation, then add operation-order/fault regressions and refresh M2 evidence.
needs-decision rationale: none

## Prior-finding reconciliation

The corrected target fully resolves `CLIOBS-M2-R3-F2`, `CLIOBS-M2-R3-F3`, `CLIOBS-M2-R4-F2`, and `CLIOBS-M2-R4-F3`. The approved R11/R14 and ADR corrections make stale-lock retention and the excluded same-user pathname-replacement actor explicit. `CLIOBS-M2-L1-F4`, `M2-L1B-F2`, `M2-L1B-F4`, `CLIOBS-M2-R3-F4`, `CLIOBS-M2-R4-F1`, and `CLIOBS-M2-R4-F4` remain open because the immediate per-mutation check and its proof are incomplete.

## Checklist

- Spec alignment: block; one R11 MUST is not implemented at each mutation boundary.
- Test coverage: concern; event/sequence and descriptor faults pass, but per-mutation validation ordering is unproved.
- Edge cases: concern; supported state can change between the early whole-root check and a later mutation.
- Error handling: pass for crossed sequences, descriptor faults, stale locks, and diagnostic isolation.
- Architecture boundaries: concern; implementation does not yet perform the check cadence required by the accepted ADR.
- Compatibility: pass within M2 scope.
- Security/privacy: concern; claims are now scoped honestly, but the supported fail-closed check boundary remains incomplete.
- Derived artifact currency: pass for the revised spec and ADR identities; package publication is out of M2 scope.
- Unrelated changes: pass for the reviewed target.
- Validation evidence: concern; C02 and C01 are green but lack direct proof of the missing R11 boundary.

## Validation

- Pre-fix identity-equal regressions: crossed event/sequence and active-file descriptor-closure tests failed before production correction.
- `node --test packages/rigorloop/test/cli-observability.test.js` — 25 passed, 0 failed after correction.
- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` — 39 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 240 passed, 0 failed.
- `python3 scripts/validate-boundary-first.py --path specs/cli-observability-and-token-efficient-results.md` — passed.
- `python3 scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-25-cli-observability-token-efficient-results` — passed before this occurrence.
- `git diff --check` — passed.

## Review sufficiency

This direct L0 review found a material defect, so promotion and elevated-risk clean-review agreement are not applicable. M2 remains in resolution and must receive bounded correction plus a fresh rereview. No automatic downstream handoff or verify readiness is claimed.
