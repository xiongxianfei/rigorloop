# Code Review M2 R6: Adjacent Pathname-Validation Correction

Review ID: code-review-m2-r6
Stage: code-review
Round: r6
Reviewer: Codex direct contract-first reviewer
Reviewer context ID: root-code-review-m2-r6-context-reset
Author context ID: root-code-review-m2-r5-correction
Target: corrected M2 logging-core implementation
Reviewed artifact: M2 implementation/test/evidence diff bundle `sha256:a8ccc19505fef9e6243859dba71da3ecfd803575d43db2170b71922cb9c3d3f8`
Reviewed milestone: M2
Review date: 2026-08-25
Recording status: recorded
Status: inconclusive
Review status: inconclusive
Native review status: inconclusive
Review gate outcome: inconclusive
Independence level: L0
Context separation mechanism: fresh artifact-and-criteria reset after production freeze
Author context excluded: false
Risk tier: elevated
Risk-tier triggers: filesystem-containment; pathname-mutation; concurrent-writer-recovery; privacy-sensitive-persistence; evidence-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Formal criteria: code-review-rereview-v1; independent-review-gate-v1; boundary-first-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/lib/log-sink.js@working-tree#sha256:69fca318208953824303641cc81ba94254c3cfedb89e8aae2bc005810f3af64e; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:92ec1c6d06d0442a8b00fa9fe619372608a13d06268c0639bce655f258f3b439; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md@working-tree#sha256:ec1c412347c5d65d6a5b17a8ee40dc708d3d11d028242f883ee89cf297a4084a
Prompt template version: code-review-v1
Initial packet hash: sha256:a8ccc19505fef9e6243859dba71da3ecfd803575d43db2170b71922cb9c3d3f8
Manifest owner: direct-user-invocation
Forbidden initial context excluded: false
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: pre-mutation root/component/owned-path validation, archive rotation, final publication, and M2 evidence
Highest-impact failure modes: mutation after incomplete validation; external-path mutation; partial rotation; false M2 closeout
Changed boundaries: validated filesystem state to destructive pathname operations
Evidence expected: direct R11/T05 operation-order and fault proof plus C01/C02 results
Areas requiring direct inspection: `log-sink.js`; focused T05 tests; current R11/ADR boundary; M2 evidence; seven prior open dispositions
Areas intentionally out of scope: M3 lookup integration; M4 token benchmark and packaging; final branch verification
Risk classes considered: filesystem containment; concurrency; recovery; failure isolation; proof adequacy
Falsifiable review questions: Does every pathname mutation receive root/component/source/destination validation? Is source identity checked last? Does inspection failure prevent every mutation? Do the evidence claims remain inside the approved threat model?
Automated review: yes
Material findings: none
Immediate next stage: blocked pending an L1-or-higher independent code review
Automatic downstream handoff: none; direct review-only invocation
Milestone closeout: blocked
Required review-resolution: no
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: inconclusive
- Artifacts changed: `reviews/code-review-m2-r6.md`; `review-log.md`; `review-resolution.md`
- Open blockers: L0 cannot advance an automated elevated-risk lifecycle review
- Next stage: blocked pending independent code-review
- Review status: inconclusive
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m2-r6.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: blocked
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Findings

No blocking or required-change finding was identified in the corrected target.

## Prior-finding reconciliation

- `CLIOBS-M2-L1-F4`, `M2-L1B-F4`, `CLIOBS-M2-R3-F4`, and `CLIOBS-M2-R4-F4` are resolved: the current T02-T05 suite directly covers the named privacy, identity, fault, timing, concurrency, interruption, and resource partitions, and the evidence carries current target hashes and exact test counts.
- `M2-L1B-F2` and `CLIOBS-M2-R4-F1` are resolved within the approved threat model: owned files use no-follow open plus device/inode comparison, failed publication performs no pathname cleanup, and destructive sources are rechecked adjacent to mutation. The accepted spec and ADR explicitly exclude a same-user or privileged process replacing a pathname after that check.
- `CLIOBS-M2-R5-F1` is resolved: one injected validator checks the root, existing components, every owned entry including an existing destination, and the exact source identity before all six mutation sites.

## Validation evidence challenged

- Pre-correction identity-equal T05 proof: 25 passed and the two new adjacent-validation tests failed.
- Post-correction focused T02-T05: 27/27 passed.
- C02: `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` passed 41/41.
- C01: `npm test --prefix packages/rigorloop` passed 242/242.
- `python3 scripts/validate-boundary-first.py --path specs/cli-observability-and-token-efficient-results.md` passed.
- `git diff --check` passed.
- The initial C02 attempt failed only because the worktree dependency was absent; after `npm ci --prefix packages/rigorloop`, the unchanged command passed. The untracked `packages/rigorloop/node_modules/` directory was removed afterward.

## Checklist coverage

- Spec alignment: pass; the corrected mutation cadence matches R11 and the ADR's explicitly non-race-proof boundary.
- Test coverage: pass for the M2 correction; public sink execution counts all six mutations and a root-inspection fault proves fail-before-mutation behavior.
- Edge cases: pass for absent destinations, existing destinations, archive deletion, archive renames, active rotation, and final publication.
- Error handling: pass; unsafe state retains `RL_LOG_UNSAFE_PATH`, ordinary inspection failures map to `RL_LOG_UNAVAILABLE`, and neither performs the guarded mutation.
- Architecture boundaries: pass; one sink-local validator owns the check cadence without claiming atomic containment against the excluded actor.
- Compatibility: pass within M2; no public command or result contract changed.
- Security/privacy: pass within the approved R11 threat model; no absolute path is serialized and observed unsafe state fails closed.
- Derived artifact currency: pass for the current M2 evidence identities; package publication remains M4-owned.
- Unrelated changes: pass; production changes are confined to the reviewed sink boundary and its tests.
- Validation evidence: pass for the correction, but insufficient for lifecycle advancement because this reviewer is L0.

## Review sufficiency assessment

The local fresh-pass review found no new material defect. The mutation-order test exercises the real exported append path and proves that each mutation interval contains root, source, and rename-destination inspection, with source identity inspection immediately adjacent to mutation. The injected inspection-fault test proves the first destructive operation is not reached. The corrected evidence does not claim protection from an actor able to replace pathnames after validation.

This substantive assessment cannot produce an automated advance outcome. The same context authored the correction, so the review is L0 under `specs/review-independence-and-criticality.md`; elevated-risk M2 still requires a fresh L1-or-higher review and the contract-required distinct clean agreement before closeout.

## Handoff

All 48 recorded material findings now have final resolved dispositions, and no new finding was identified. M2 remains `review-requested`; no workflow state was advanced. The next safe action is an L1-or-higher independent M2 code review. M3, final explanation, verification, and PR readiness remain blocked.
