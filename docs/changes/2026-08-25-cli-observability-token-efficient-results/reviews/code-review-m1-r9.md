# Code Review M1 R9: Retained-Recovery Rereview

Review ID: code-review-m1-r9
Stage: code-review
Round: r9
Reviewer: independent subagent reviewer
Target: complete tracked branch diff against `fcbbfda44a89945ee06cfa0c1b16dcbd39984036`
Reviewed artifact: working-tree `sha256:e73d28c3fd6945075149c38e6221579d626b3d3a60ecbf80f5b3df46f855bd67`
Reviewed milestone: M1 with later milestone integration visible
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m1-r8-correction
Reviewer context ID: m1-independent-review-agent
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: lifecycle-mutation-fidelity; recovery-semantics; result-projection-authority; compatibility-proof
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Formal criteria: code-review-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:8df259dc5e97efa06535f785c25d575c366e2864b1fd88abde96fba6075b4fd4; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2
Prompt template version: code-review-v1
Initial packet hash: sha256:e73d28c3fd6945075149c38e6221579d626b3d3a60ecbf80f5b3df46f855bd67
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: lifecycle mutation failure projection when recovery bytes persist
Highest-impact failure modes: persisted lifecycle-owned recovery bytes reported unchanged
Changed boundaries: lifecycle transaction failure to concise result projection
Evidence expected: real recovery-prepared and verified-rollback fault proof
Areas requiring direct inspection: lifecycle CLI catch; transaction recovery; T11 tests
Areas intentionally out of scope: hosted services; publication; release operations
Risk classes considered: semantic fidelity; lifecycle authority; recovery; error handling; proof adequacy
Falsifiable review questions: Can a transaction failure persist lifecycle-owned bytes while reporting `state_changed: false`?
Invocation manifest: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-invocation-code-review-m1-r9.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: packages/rigorloop/dist/lib/lifecycle-cli.js; packages/rigorloop/dist/lib/lifecycle-transaction.js; packages/rigorloop/test/result-renderer.test.js
Requirement-fidelity matched path triggers: specs/; docs/changes/**/reviews/
Requirement-fidelity matched category triggers: closed enums; review-recording contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > risk map > actual diff > direct probes > tests > prior-finding reconciliation
Requirement-property decomposition evidence: present
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Requirement-fidelity outcome: changes-requested
Material findings: CLIOBS-M1-L1-F8
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding CLIOBS-M1-L1-F8

Finding ID: CLIOBS-M1-L1-F8
Severity: major
Classification: failed-remediation of CLIOBS-M1-L1-F7, CLIOBS-M1-L1-F1, and CLIOBS-M1-L1-F4
Location: `packages/rigorloop/dist/lib/lifecycle-cli.js`; `packages/rigorloop/dist/lib/lifecycle-transaction.js`; `packages/rigorloop/test/result-renderer.test.js`
Evidence: A real transaction fault after recovery preparation retained `.rigorloop-lifecycle-recovery.json`, but the catch path blanket-set concise `state_changed: false`.
Required outcome: Compare lifecycle-owned bytes before and after caught post-evaluation failures so busy and verified rollback report false, retained recovery/candidate/lock or changed `change.yaml` report true, and pre-evaluation failures omit the field.
Safe resolution path: Capture the lifecycle-owned path set before transaction execution and compare it after failure; add real transaction fault regressions for retained recovery and verified rollback.
needs-decision rationale: none

## Validation observed

- Exact C02: 18 passed.
- Package tests: 215 passed.
- A real `after-recovery-prepared` fault reproduced retained recovery bytes with `state_changed: false`.
- Exact T10 compatibility and detailed aliases remained correct.

## Prior-finding reconciliation

F2, F3, F5, F6, CR1-CR5, and CR7-CR9 remain resolved. F1/F4/F7 and CR6 recur through retained failure-state persistence.

## Handoff

Resolve `CLIOBS-M1-L1-F8`, then run a fresh clean L1 review and its required distinct second clean review. M1 cannot close on R9.
