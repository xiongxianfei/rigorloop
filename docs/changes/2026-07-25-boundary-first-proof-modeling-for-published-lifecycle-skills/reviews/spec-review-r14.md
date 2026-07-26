# Boundary-First Proof Modeling Spec Review R14

Review ID: spec-review-r14
Stage: spec-review
Round: 14
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: focused runtime-attestation amendment
Reviewed artifact: specs/rigorloop-workflow.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR14-1, BFP-SR14-2, BFP-SR14-3, BFP-SR14-4
Immediate next stage: spec revision
Spec readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact runtime-attestation amendment; accepted R28y; accepted runtime ADR; T48-T50 candidate
Manifest owner: workflow orchestrator

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: BFP-SR14-1, BFP-SR14-2, BFP-SR14-3, BFP-SR14-4
- Immediate next stage: spec revision
- Spec readiness: not-ready
- Test-spec readiness: not-ready

## Findings

### BFP-SR14-1 - Mandatory runtime-owned thread metadata is incomplete

Finding ID: BFP-SR14-1
Severity: blocker

The amendment omits provider, logical workspace/cwd roles, instruction-source
projection, and cross-field equality with invocation profile values.

Required outcome: Represent every required runtime-owned metadata fact through
a bounded exact record and validate cross-field equality.

### BFP-SR14-2 - Attestation identity preimages are undefined

Finding ID: BFP-SR14-2
Severity: blocker

The amendment does not freeze canonicalization, bundle framing, pagination,
included method fields, logical path normalization, or classification
preimages.

Required outcome: Give every identity one deterministic, independently
testable, non-secret preimage.

### BFP-SR14-3 - Failure diagnostics lack a carrier and phase mapping

Finding ID: BFP-SR14-3
Severity: major

The successful attestation has no diagnostic field, the failure receipt is
undefined, several failure families are unmapped, and stop timing is
overgeneralized.

Required outcome: Define a bounded preflight result, exhaustive diagnostics,
and pre-thread, pre-turn, and in-turn timing.

### BFP-SR14-4 - Transitive binding is implicit

Finding ID: BFP-SR14-4
Severity: major

Operation selector and validation prose do not explicitly bind the nested
attestation through implementation manifest, input set, immutable run,
pointer, and report while allowing validation on another runtime.

Required outcome: Make that transitive binding and non-substitution behavior
normative.
