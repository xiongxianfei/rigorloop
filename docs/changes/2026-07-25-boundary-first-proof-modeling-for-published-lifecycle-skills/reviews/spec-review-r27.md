# Boundary-First Proof Modeling Spec Review R27

Review ID: spec-review-r27
Stage: spec-review
Round: 27
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: focused R28y and T51-T52 amendment at f0288e01
Reviewed artifact: `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R27-1, BFP-SR-R27-2, BFP-SR-R27-3
Immediate next stage: spec revision
Architecture assessment: required-after-approval
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:594e1f83bba8a1c84531ce96e870800c55694efb7226d5a0d1cf3d93a8bff819`

Reviewed test-spec identity: `sha256:1e75a3992ed1bf02ab40965a30a432556241f47055d230e6963b4bc665a3ace8`

## Findings

### BFP-SR-R27-1 - Timeout reconciliation conflicts with the closed event grammar

Finding ID: BFP-SR-R27-1
Severity: blocker

T52 adds transport timeout and retry behavior that R28y does not normatively
define. Existing event `attempt` values are lifecycle correction attempts and
cannot also identify transport retries.

Required outcome: Define a separate evidence-first transport invocation
protocol. Stop the original invocation before retry, reconcile valid complete
output without reinvocation, permit at most one retry only for absent output
plus a retryable transient diagnostic, fail closed on partial/extra/
contradictory/protocol/security evidence, pause on uncertain liveness, and
record transport attempts without weakening lifecycle-event grammar.

### BFP-SR-R27-2 - Publication states remain inconsistent and incomplete

Finding ID: BFP-SR-R27-2
Severity: blocker

The prepared receipt labels a prospective immutable manifest path as a current
evidence reference before that path exists. The pre-pointer failure invariant
incorrectly says the immutable run is unchanged after installation may have
occurred, and orphan staging has no closed recovery transition.

Required outcome: Distinguish the staged-manifest current reference from the
prospective immutable target descriptor; define every durable staging,
receipt, immutable-run, current-pointer, and prior-pointer combination;
classify orphan staging deterministically; correct the failure invariant; and
define receipt cleanup plus directory fsync.

### BFP-SR-R27-3 - Test-spec lifecycle metadata overstates authority

Finding ID: BFP-SR-R27-3
Severity: major

The feature spec is draft, but the amended test spec remains active and still
calls the governing feature spec approved.

Required outcome: Mark the test-spec amendment as draft, stop describing its
governing spec as approved, approve the feature-spec amendment first, then
perform architecture and independent test-spec review before reactivation.

## Positive assessment

The workflow/stage/harness ownership split is sound and must remain:

- `workflow` owns routing;
- the stage-owning skill supplies complete artifact bytes or review judgment;
- the harness enforces paths, captures, validates, compares, and publishes.

## Review result

The amendment is not ready for architecture or implementation until all three
findings are resolved and spec-review is rerun. T52 should also call this a
four-stage lifecycle path using five participating skills.
