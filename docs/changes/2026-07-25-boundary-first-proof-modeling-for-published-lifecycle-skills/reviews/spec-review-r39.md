# Boundary-First Proof Modeling Spec Review R39

Review ID: spec-review-r39
Stage: spec-review
Round: 39
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R38 resolution candidate at ca01208a
Reviewed artifact: `specs/rigorloop-workflow.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R39-1
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:d232ac03fd7de1d4a2bb27bc9a8547f79eb0d67744928f76e0545de8d500e847`

Reviewed test-spec identity: `sha256:84614dbc8ac28f4f011f9ec5ed1cfe063b3548113df0b4ee296fb9fcdc6a3e2e`

Reviewed plan identity: `sha256:3fe82cabfc664d18761ce99d9850a8813f1801d4fc1330487c6609739c887243`

## Finding

### BFP-SR-R39-1 - Raw candidate-message limit has no exact policy source

Finding ID: BFP-SR-R39-1
Severity: major
Location: R28y lifecycle/canary artifact policies and candidate parser
Evidence: Policy `envelope_byte_limit` bounds canonical JSON, while the
collector applies an unnamed per-message raw-byte limit before parsing.
Whitespace-heavy, escaped, malformed, and canary messages therefore have no
deterministic raw size boundary.
Required outcome: Define the maximum raw candidate-message size, the maximum
post-parse canonical envelope size, and their lifecycle/canary selection.
Safe resolution: Add `candidate_message_byte_limit` to both policy objects,
check it before parse, retain `envelope_byte_limit` for post-parse canonical
bytes, accept equality, and classify one byte over deterministically.

## Review result

R38-1 through R38-4 and the residual R37 findings are resolved. Resolve this
single byte-boundary ambiguity and rerun spec-review. Approval then requires
architecture/ADR synchronization before test-spec or implementation.
