# Boundary-First Proof Modeling Spec Review R38

Review ID: spec-review-r38
Stage: spec-review
Round: 38
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R37 resolution candidate at 8412db17
Reviewed artifact: `specs/rigorloop-workflow.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R38-1, BFP-SR-R38-2, BFP-SR-R38-3, BFP-SR-R38-4
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:d87481f7477fdf0284d422cf546f9c97aa121a093c04e63e762313dde585c9a1`

Reviewed test-spec identity: `sha256:84614dbc8ac28f4f011f9ec5ed1cfe063b3548113df0b4ee296fb9fcdc6a3e2e`

Reviewed plan identity: `sha256:c25113227b8f9d0e0ebf828e559c0030a47ee36fcc45742c54f691a5740e9cf3`

## Findings

### BFP-SR-R38-1 - Lifecycle artifact policy is not constructible or manifest-bound

Finding ID: BFP-SR-R38-1
Severity: blocking
Location: R28y lifecycle artifact policy and behavior manifest
Evidence: The policy names a prose matrix without an exact JSON field/row
schema or ordering, while transport rows require its identity and the
behavior manifest does not bind the policy.
Required outcome: Define one byte-deterministic policy object and bind it
through manifest selection, input-set identity, generation, validation, and
every transport row.
Safe resolution: Freeze exact policy and nested row fields, content-state IDs,
ordering, and limits; add the object to the implementation manifest and reject
unknown, duplicate, reordered, stale, or substituted content before invocation.

### BFP-SR-R38-2 - Malformed and oversized candidate observations are ambiguous

Finding ID: BFP-SR-R38-2
Severity: major
Location: R28y candidate-set observation grammar
Evidence: Invalid JSON cannot supply the required JSON shape projection,
oversized fields permit multiple empty-or-null encodings, and aggregate byte
accounting does not say whether it includes the overflowing message.
Required outcome: Give every parse state one exact representation and define
raw-byte accounting and parse/size precedence.
Safe resolution: Add a closed malformation kind, reserve shape projection for
parseable schema-invalid JSON, assign every nullable/list field exactly, check
size before parse, and include the full first overflowing message in the
aggregate count.

### BFP-SR-R38-3 - Post-materialization failures lack replayable evidence

Finding ID: BFP-SR-R38-3
Severity: blocking
Location: R28y byte reread and content-state validation
Evidence: Byte or content-state mismatches downgrade to contradictory and
discard temporary files, but no durable value-free record proves the observed
reread identities or structural validation result.
Required outcome: Preserve bounded evidence that distinguishes a real
materialization/content validation failure from an asserted status.
Safe resolution: Add exact materialization and content-validation
observations with expected/observed byte identities, validator identities,
closed outcomes/diagnostics, and canonical identities; never retain raw failed
content.

### BFP-SR-R38-4 - Second changes-requested review lacks a terminal trace

Finding ID: BFP-SR-R38-4
Severity: major
Location: R28y review variants and complete branch grammar
Evidence: Review attempt two may return `changes-requested`, but the trace
grammar permits attempt two only when approved and has no budget-exhausted
terminal state.
Required outcome: Map every allowed review variant to exactly one transition
or terminal state.
Safe resolution: Add `correction-budget-exhausted` terminal branches for
second-review changes-requested, preserve the open resolution, prohibit
another authoring attempt, and compute fail with a stable diagnostic.

## Review result

BFP-SR-R37-3 is resolved. BFP-SR-R37-1 and BFP-SR-R37-2 are materially
improved but remain incomplete through the four findings above. The spec is
not ready for architecture or test-spec revision until R38-1 through R38-4
are resolved and independently rereviewed.
