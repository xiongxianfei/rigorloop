# Code Review M1 R4: Independent Result-Projection Review

Review ID: code-review-m1-r4
Stage: code-review
Round: r4
Reviewer: independent subagent reviewer
Target: complete tracked branch diff against `fcbbfda44a89945ee06cfa0c1b16dcbd39984036`
Reviewed artifact: working-tree `sha256:5675b1a983f5b2bc6c1b9f7efbfd3521c924779bb6f0fe988f9f0dfefca4859e`
Reviewed milestone: M1 with later milestone integration visible
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m1-correction
Reviewer context ID: m1-independent-review-agent
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: result-projection-authority; lifecycle-mutation-fidelity; compatibility-proof
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Formal criteria: code-review-rereview-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:8df259dc5e97efa06535f785c25d575c366e2864b1fd88abde96fba6075b4fd4; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2
Prompt template version: code-review-v1
Initial packet hash: sha256:5675b1a983f5b2bc6c1b9f7efbfd3521c924779bb6f0fe988f9f0dfefca4859e
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: shared result projection, legacy output compatibility, lifecycle/top-level format routing, continuation facts, and mutation equivalence
Highest-impact failure modes: invented lifecycle mutation, unsafe continuation advice, compatibility drift, missing concise fields, and public handlers outside the shared renderer
Changed boundaries: semantic result to renderer; lifecycle/top-level handlers to common renderer; controller to final correlation and observability fields
Evidence expected: complete compatibility characterization; field applicability matrix; dry-run/already-recorded proof; exact-one continuation proof; public single-emission tests
Areas requiring direct inspection: renderer; lifecycle mutation construction; top-level dispatch; new-change parsing; renderer and compatibility tests
Areas intentionally out of scope: sink containment, rotation, concurrency, hosted services, publication, and release operations
Risk classes considered: compatibility; composition; semantic fidelity; lifecycle authority; error handling; proof adequacy; hosted-services=not-applicable; live-publication=not-applicable
Falsifiable review questions: Can a no-write mutation report changed? Can multiple permitted operations invent one next action? Does every public semantic handler accept shared formats? Does T10/T11 fail for each invalid partition?
Invocation manifest: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-invocation-code-review-m1-r4.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: packages/rigorloop/dist/lib/result-renderer.js; packages/rigorloop/dist/lib/lifecycle-cli.js; packages/rigorloop/dist/bin/rigorloop.js; packages/rigorloop/dist/lib/new-change.js; packages/rigorloop/test/result-renderer.test.js
Requirement-fidelity matched path triggers: specs/; docs/changes/**/reviews/
Requirement-fidelity matched category triggers: closed enums; generated-output or package parity validators; review-recording contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > risk map > actual diff > direct probes > tests > prior-finding reconciliation
Requirement-property decomposition evidence: present
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Requirement-fidelity outcome: changes-requested
Material findings: CLIOBS-M1-L1-F1, CLIOBS-M1-L1-F2, CLIOBS-M1-L1-F3, CLIOBS-M1-L1-F4
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, invocation manifest, review log, review resolution, and workflow state
- Open blockers: CLIOBS-M1-L1-F1 through CLIOBS-M1-L1-F4
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M1-L1-F1, CLIOBS-M1-L1-F2, CLIOBS-M1-L1-F3, CLIOBS-M1-L1-F4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m1-r4.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md#code-review-m1-r4`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M1-L1-F1, CLIOBS-M1-L1-F2, CLIOBS-M1-L1-F3, CLIOBS-M1-L1-F4
- Verify readiness: not-claimed

## Findings

### Finding CLIOBS-M1-L1-F1

Finding ID: CLIOBS-M1-L1-F1
Severity: major
Location: `packages/rigorloop/dist/lib/result-renderer.js`; lifecycle mutation result construction
Evidence: The renderer reports `state_changed: true` for mutation statuses `planned` and `already-recorded`, although neither changes repository lifecycle bytes.
Required outcome: Derive `state_changed` from authoritative closed mutation facts so every no-write outcome is false and persisted transitions alone are true.
Safe resolution path: Use an explicit closed status mapping or an authoritative boolean and add every T11 mutation partition.
needs-decision rationale: none

### Finding CLIOBS-M1-L1-F2

Finding ID: CLIOBS-M1-L1-F2
Severity: major
Location: `packages/rigorloop/dist/lib/result-renderer.js`
Evidence: A result with multiple permitted operations emits the first item as `next_operation`, despite the exact-one requirement.
Required outcome: Omit `next_operation` for zero or multiple alternatives unless one explicit deterministic operation is supplied.
Safe resolution path: Prefer explicit output, otherwise accept exactly one unique corrective or permitted operation; add zero/one/multiple/conflict tests.
needs-decision rationale: none

### Finding CLIOBS-M1-L1-F3

Finding ID: CLIOBS-M1-L1-F3
Severity: major
Location: `packages/rigorloop/dist/bin/rigorloop.js`; `packages/rigorloop/dist/lib/new-change.js`
Evidence: `new-change ... --format concise-json` is accepted by top-level parsing but rejected when `new-change` reparses raw arguments.
Required outcome: Every applicable public semantic handler accepts the shared explicit projection formats while preserving legacy defaults.
Safe resolution path: Parse common output controls once or teach `new-change` the exact shared closed vocabulary without divergent precedence.
needs-decision rationale: none

### Finding CLIOBS-M1-L1-F4

Finding ID: CLIOBS-M1-L1-F4
Severity: major
Location: `packages/rigorloop/test/result-renderer.test.js`; test-spec T10 and T11
Evidence: Four renderer tests cover one synthetic blocked result and omit dry-run/already-recorded mutation, multiple continuation, invalid, stale, unexpected, read, mandatory-field, and complete compatibility partitions; F1-F3 remained green.
Required outcome: Implement T10/T11 at their approved breadth and make the new regressions fail against the prior implementation.
Safe resolution path: Add table-driven applicability fixtures and public compatibility characterization, then rerun C01 and C02.
needs-decision rationale: none

## Prior-finding reconciliation

CR1-CR5 and CR7-CR9 remain resolved. CR6 is failed-remediation because the evidence claimed complete proof while T10/T11 remained compressed. The local R3 no-finding assessment is superseded by this independent result.

## Handoff

Record and resolve F1-F4 through bounded implementation, then request a fresh L1 rereview. M1 remains review-requested; final closeout and verification are blocked.
