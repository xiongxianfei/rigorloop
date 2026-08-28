# Code Review M2 R2: Distinct Logging-Core Review

Review ID: code-review-m2-r2
Stage: code-review
Round: r2
Reviewer: second independent subagent reviewer
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
Reviewer context ID: m2-second-independent-review-agent-r2
Context separation mechanism: simultaneous-separate-agent-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: privacy-sensitive-persistence; filesystem-containment; destructive-rotation; concurrency; diagnostic-isolation
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`
Formal criteria: code-review-second-review-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
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
Material findings: M2-L1B-F1, M2-L1B-F2, M2-L1B-F3, M2-L1B-F4
Immediate next stage: review-resolution
Automatic downstream handoff: none; isolated review
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding M2-L1B-F1

Finding ID: M2-L1B-F1
Severity: major
Location: `packages/rigorloop/dist/lib/diagnostic-event.js:19`
Evidence: Scalar allowlisted fields accept objects; an object supplied as lifecycle operation persisted a synthetic private sentinel.
Required outcome: Every admitted field has a closed type and shape; unsafe nested values cannot persist.
Safe resolution path: Add exact scalar, boolean, integer, and string-list validators plus privacy probes for every admitted surface.
needs-decision rationale: none

## Finding M2-L1B-F2

Finding ID: M2-L1B-F2
Severity: major
Location: `packages/rigorloop/dist/lib/log-sink.js:28`
Evidence: Path checks are not bound to later open/rename/unlink operations; replacing the held lock pathname caused cleanup to delete an unowned replacement.
Required outcome: No-follow operations and ownership-bound cleanup prevent deleting or following replaced paths.
Safe resolution path: Bind locks to unique token plus inode/handle, use no-follow open and post-open identity checks, and test deterministic replacement races.
needs-decision rationale: none

## Finding M2-L1B-F3

Finding ID: M2-L1B-F3
Severity: major
Location: `packages/rigorloop/dist/lib/cli-observability.js:47`
Evidence: File append degradation followed by a throwing stderr sink rejected before semantic dispatch (`dispatched:false`).
Required outcome: Diagnostic-console failures never abort or replace semantic execution.
Safe resolution path: Isolate all diagnostic writes and test throwing sinks before, during, and after dispatch, including console off.
needs-decision rationale: none

## Finding M2-L1B-F4

Finding ID: M2-L1B-F4
Severity: major
Location: `packages/rigorloop/test/cli-observability.test.js`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m2-logging-core.md`
Evidence: T02-T05 proof omits size, clock, privacy, path, permission, rotation, lock, fault, operation-count, and resource-guard partitions; evidence uses stale totals.
Required outcome: Complete the approved T02-T05 matrix and refresh evidence against exact corrected identities.
Safe resolution path: Add named injected and real-process tests, rerun C02/C01, and record truthful current proof.
needs-decision rationale: none

## Validation

C02 passed 20/20 and C01 passed 218/218, but direct privacy, lock-replacement, and stderr-failure probes reproduced material contract violations. No automatic downstream handoff.
