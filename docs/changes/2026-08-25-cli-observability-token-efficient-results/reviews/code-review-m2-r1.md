# Code Review M2 R1: Logging Core

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: independent subagent reviewer
Target: M2 logging-core implementation
Reviewed artifact: working-tree `sha256:7fc64f763c3121af4f473875cab16c8fc1a739b082f88f00f801412700d29b38`
Reviewed milestone: M2
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m2-implementation
Reviewer context ID: m2-independent-review-agent-r1
Context separation mechanism: simultaneous-separate-agent-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: privacy-sensitive-persistence; filesystem-corruption; concurrency; bounded-blocking; evidence-overclaim
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Formal criteria: code-review-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Risk-tier classifier: affected-path-and-contract-surface-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:8df259dc5e97efa06535f785c25d575c366e2864b1fd88abde96fba6075b4fd4; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2
Prompt template version: code-review-v1
Initial packet hash: sha256:7fc64f763c3121af4f473875cab16c8fc1a739b082f88f00f801412700d29b38
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: privacy-safe bounded diagnostic event construction, local persistence, locking, rotation, and recovery
Highest-impact failure modes: private-value persistence; corrupt retained JSONL; unowned lock deletion; semantic-dispatch abortion; unbounded lock wait
Changed boundaries: normalized diagnostic facts to JSONL sink and invocation degradation controller
Evidence expected: exact T02-T05 contract, fault, filesystem, concurrency, privacy, and bounded-work proof
Areas requiring direct inspection: diagnostic-event.js; log-sink.js; cli-observability.js; logging-core tests; M2 evidence
Areas intentionally out of scope: M3 lookup semantics except adjacent diagnostic-isolation behavior; token benchmark; publication
Risk classes considered: semantic fidelity; privacy; filesystem containment; concurrency; recovery; bounded blocking; diagnostic isolation; proof adequacy
Falsifiable review questions: Can unsafe shapes or private markers persist? Can combined faults corrupt JSONL? Can cleanup remove an unowned lock? Can diagnostic failure abort dispatch?
Requirement-fidelity affected paths: packages/rigorloop/dist/lib/diagnostic-event.js; packages/rigorloop/dist/lib/log-sink.js; packages/rigorloop/dist/lib/cli-observability.js; packages/rigorloop/test/cli-observability.test.js
Requirement-fidelity matched path triggers: specs/; docs/changes/**/reviews/
Requirement-fidelity matched category triggers: closed enums; generated-output or package parity validators; review-recording contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > risk map > actual diff > direct probes > tests > milestone evidence
Requirement-property decomposition evidence: R3-R17/R33-R34 and T02-T05 mapped to configuration, event, path, rotation, lock, fault, privacy, and resource partitions
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Requirement-fidelity outcome: changes-requested
Material findings: CLIOBS-M2-L1-F1, CLIOBS-M2-L1-F2, CLIOBS-M2-L1-F3, CLIOBS-M2-L1-F4
Immediate next stage: review-resolution
Automatic downstream handoff: none; isolated review
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding CLIOBS-M2-L1-F1

Finding ID: CLIOBS-M2-L1-F1
Severity: major
Location: `packages/rigorloop/dist/lib/diagnostic-event.js:27`
Evidence: Throwing clocks escape; incomplete completion events and negative duration are accepted; an oversized fallback reached 21,222 bytes and retained a synthetic private marker.
Required outcome: Validate mandatory fields, closed types, non-negative duration and timestamps, and emit only a fixed privacy-safe fallback at or below 16 KiB.
Safe resolution path: Add closed validators and independently validate a constant-only fallback; add clock, duration, mandatory-field, size, and private-value regressions.
needs-decision rationale: none

## Finding CLIOBS-M2-L1-F2

Finding ID: CLIOBS-M2-L1-F2
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:83`
Evidence: A partial write followed by truncate failure returned `RL_LOG_UNAVAILABLE` but left the active file with an unparsable seven-byte tail.
Required outcome: Every append/rollback failure leaves retained files containing complete JSONL records only.
Safe resolution path: Use a recoverable append protocol or durable tail recovery and add combined write/truncate/fsync/close fault tests.
needs-decision rationale: none

## Finding CLIOBS-M2-L1-F3

Finding ID: CLIOBS-M2-L1-F3
Severity: minor
Location: `packages/rigorloop/dist/lib/log-sink.js:43`
Evidence: Held-lock acquisition returned after 1,002 ms; the implementation uses fixed waits and non-injectable wall-clock time despite the 1,000 ms bound.
Required outcome: Enforce at most ten attempts and a 1,000 ms total monotonic budget while preserving unowned locks.
Safe resolution path: Inject monotonic time/wait adapters, cap every wait by remaining budget, and add exact attempt/deadline tests.
needs-decision rationale: none

## Finding CLIOBS-M2-L1-F4

Finding ID: CLIOBS-M2-L1-F4
Severity: major
Location: `packages/rigorloop/test/cli-observability.test.js`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md`
Evidence: Six focused tests omit material T02-T05 matrices, while evidence overclaims the contradicted 16 KiB bound and cites stale test totals.
Required outcome: Implement the approved T02-T05 proof map and bind truthful evidence to the corrected target.
Safe resolution path: Add table-driven contract/fault tests, run exact C02/C01, and refresh M2 evidence with current identities and results.
needs-decision rationale: none

## Validation

C02 passed 20/20 and C01 passed 218/218, but direct adversarial probes reproduced all findings. No automatic downstream handoff.
