# Code Review M1 R16: Alternate Logs Projection Review

Review ID: code-review-m1-r16
Stage: code-review
Round: r16
Reviewer: independent subagent reviewer
Target: complete tracked branch diff against `fcbbfda44a89945ee06cfa0c1b16dcbd39984036`
Reviewed artifact: working-tree `sha256:8e1cad39aa8ec5117544fcf70a16e20123e4a4ab6e83b7215bb936415d3bd8dc`
Reviewed milestone: M1 with later milestone integration visible
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m1-r15-correction
Reviewer context ID: m1-independent-review-agent-r16
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: result-projection-authority; observability-fidelity; compatibility-proof; alternate-public-path
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Formal criteria: code-review-rereview-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:8df259dc5e97efa06535f785c25d575c366e2864b1fd88abde96fba6075b4fd4; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2
Prompt template version: code-review-v1
Initial packet hash: sha256:8e1cad39aa8ec5117544fcf70a16e20123e4a4ab6e83b7215bb936415d3bd8dc
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: accepted log inspection output formats
Highest-impact failure modes: manually serialized detailed output loses finalized observability
Changed boundaries: log handler versus common result projection
Evidence expected: public logs path/show format acceptance and rejection matrix
Areas requiring direct inspection: log handler; common renderer; public help; T10/T11 tests
Areas intentionally out of scope: hosted services; publication; release operations
Risk classes considered: semantic fidelity; observability; compatibility; alternate public path; proof adequacy
Falsifiable review questions: Does any accepted new output format bypass finalized projection?
Invocation manifest: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-invocation-code-review-m1-r16.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: packages/rigorloop/dist/bin/rigorloop.js; packages/rigorloop/dist/lib/result-renderer.js; packages/rigorloop/test/result-renderer.test.js
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
Material findings: CLIOBS-M1-L1-F12
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding CLIOBS-M1-L1-F12

Finding ID: CLIOBS-M1-L1-F12
Severity: major
Classification: failed-remediation of CLIOBS-M1-L1-F11
Location: `packages/rigorloop/dist/bin/rigorloop.js`; log inspection tests
Evidence: `logs path --format detailed-json --no-file-log` succeeded through manual serialization but omitted `observability: disabled`.
Required outcome: Accepted new projections use finalized projection semantics; alternatively, log inspection rejects undocumented `detailed-json` and retains only its R18 human/JSON contract.
Safe resolution path: Remove undocumented log detailed acceptance and add public path/show rejection tests.
needs-decision rationale: none

## Validation observed

- Exact C02 reruns: 20 passed after one nondeterministic concurrent-writer failure.
- Package tests: 217 passed.
- Public logs detailed probe reproduced missing observability.

## Handoff

Resolve F12, then repeat clean and distinct elevated-risk reviews. M1 cannot close on R16.
