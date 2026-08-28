# Code Review M1 R13: Elevated-Risk Second Review

Review ID: code-review-m1-r13
Stage: code-review
Round: r13
Reviewer: second independent subagent reviewer
Target: locked M1 implementation identities from R12
Reviewed artifact: working-tree `sha256:30ae71253850d9c3b6ea46094a2574856623ad657493960aa22fa8f0e02caad9`
Reviewed milestone: M1 with later milestone integration visible
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m1-r11-correction
Reviewer context ID: m1-second-independent-review-agent-r13
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: lifecycle-mutation-fidelity; result-projection-authority; compatibility-proof
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Formal criteria: code-review-second-review-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:8df259dc5e97efa06535f785c25d575c366e2864b1fd88abde96fba6075b4fd4; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2
Prompt template version: code-review-v1
Initial packet hash: sha256:154e5ead1adfbdb442d1b318500f3b7268cefdf4d43557e57c086569114e2025
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: detailed and concise mutation-fact equivalence
Highest-impact failure modes: authoritative state mutation discarded by explicit detailed projection
Changed boundaries: internal semantic result to compatibility and explicit detailed projectors
Evidence expected: dual-projection mutation tests across T11 partitions
Areas requiring direct inspection: result renderer; lifecycle result facts; T10/T11 tests
Areas intentionally out of scope: hosted services; publication; release operations
Risk classes considered: semantic fidelity; compatibility; projection equivalence; proof adequacy
Falsifiable review questions: Does explicit detailed JSON retain every applicable mutation fact visible in concise JSON?
Invocation manifest: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-invocation-code-review-m1-r13.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: packages/rigorloop/dist/lib/lifecycle-cli.js; packages/rigorloop/dist/lib/result-renderer.js; packages/rigorloop/test/result-renderer.test.js
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
Calibration record ID: code-review-m1-r13-elevated-second-review
Review skill: code-review
Fixture mode: not-applicable
Sampling phase: rollout
Sample rate: 100%
Standard clean outcomes independently reviewed: 1
Sample-rate reduction requested: no
Second reviewer type: separate-agent-L1
Second review required: yes
Second-review disagreement: material-finding
Automatic continuation: no
Critical authority kind: n/a
Critical authority satisfied: no
Recurrence detection: detected
Novel defect detection: detected
Material disagreements: 1
Severity disagreements: 1
Evidence gaps: detailed failure-state mutation projection absent
Downstream escape: no
False-positive rate: 0%
Inconclusive rate: 0%
Receipt quality: complete
Review duration: 480s
Material findings: CLIOBS-M1-L1-F10
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding CLIOBS-M1-L1-F10

Finding ID: CLIOBS-M1-L1-F10
Severity: major
Classification: failed-remediation of CLIOBS-M1-L1-F1 and CLIOBS-M1-L1-F4
Location: `packages/rigorloop/dist/lib/lifecycle-cli.js`; `packages/rigorloop/dist/lib/result-renderer.js`; `packages/rigorloop/test/result-renderer.test.js`
Evidence: A retained-recovery failure carries a non-enumerable authoritative `state_changed: true`; concise renders it, while explicit `detailed-json` serializes the result directly and discards it.
Required outcome: Explicit detailed projection retains applicable authoritative mutation facts while legacy `json` remains v0.4.x-compatible; T11 compares mutation truth across projections for ordinary and repair partitions.
Safe resolution path: Separate the legacy JSON compatibility adapter from explicit detailed projection and add dual-projection mutation regressions.
needs-decision rationale: none

## Validation observed

- Exact C02: 18 passed.
- Package tests: 215 passed.
- Direct dual-projection retained-recovery probe showed concise true and detailed absent.
- Legacy T10 compatibility remained exact.

## Handoff

Resolve `CLIOBS-M1-L1-F10`, then repeat fresh clean and distinct second-clean reviews. M1 cannot close on R13.
