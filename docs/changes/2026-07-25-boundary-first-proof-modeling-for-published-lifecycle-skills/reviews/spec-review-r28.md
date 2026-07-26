# Boundary-First Proof Modeling Spec Review R28

Review ID: spec-review-r28
Stage: spec-review
Round: 28
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R27 resolution candidate at cb0527c9
Reviewed artifact: `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R28-1, BFP-SR-R28-2, BFP-SR-R28-3
Immediate next stage: spec revision
Architecture assessment: required-after-approval
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:d3085bdbd14f79e145d0f04fe181d38398c8ff029697744ab0c9302531ea999f`

Reviewed test-spec identity: `sha256:d6269cc11cd994ff27e58e1f0efafaf8a87d141d2e66499de086e50a84009cbb`

## Findings

### BFP-SR-R28-1 - Transport matrix is not closed or uniquely routable

Finding ID: BFP-SR-R28-1
Severity: blocker

Several cross-field tuples remain undefined, uncertain liveness cannot safely
claim an inspected output, transport row sequencing is incomplete, and no
bounded termination receipt proves stop/reap before retry.

Required outcome: Add `uninspected`, define every admissible tuple and reject
all others vocabulary-first, define row cardinality and transitions, bind
confirmed stop to a durable termination receipt, and define exact failure
fixture and evidence rules.

### BFP-SR-R28-2 - Publication lacks an exhaustive durable state machine

Finding ID: BFP-SR-R28-2
Severity: blocker

Prose branches do not uniquely route simultaneous staging/target, stray
staging after pointing, unpointed target without receipt, durable temporary
pointer, null prior-pointer, or manual orphan recovery.

Required outcome: Define named publication states with exact predicates and
one action each for staging, receipt, target, temporary pointer, current
pointer, prior pointer, cleanup/fsync, and terminal result. Define a concrete
manual recovery record and authority.

### BFP-SR-R28-3 - Lifecycle metadata remains contradictory

Finding ID: BFP-SR-R28-3
Severity: major

The test spec still calls itself active, retains stale plan/spec-review
identities and implementation-ready wording, and T52 still says five-stage in
its steps.

Required outcome: Synchronize metadata to draft spec/test-spec,
active-but-resolution-needed plan state, latest review evidence, and the
four-stage lifecycle path using five skills.

## Positive assessment

The workflow/stage/harness ownership split and prohibition against
harness-authored normative content remain correct.

## Review result

The specification remains blocked until both state machines and metadata are
closed and independently rereviewed.
