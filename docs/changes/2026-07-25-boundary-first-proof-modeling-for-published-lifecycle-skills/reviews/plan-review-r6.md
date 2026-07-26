# Boundary-First Proof Modeling Plan Review R6

Review ID: plan-review-r6
Stage: plan-review
Round: 6
Reviewer: Codex plan-review skill with context-separated independent reviewer
Target: M2 plan projection after architecture-review R8
Reviewed artifact: docs/plans/2026-07-25-boundary-first-proof-modeling.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-PL6-1, BFP-PL6-2, BFP-PL6-3
Immediate next stage: plan revision
Implementation readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact M2 plan candidate; approved R13 specs; accepted R8 architecture and runtime ADR; current M1-M4 plan
Manifest owner: workflow orchestrator

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: BFP-PL6-1, BFP-PL6-2, BFP-PL6-3
- Recording status: recorded
- Recording blocker: none
- Immediate next stage: plan revision
- Implementation readiness: not-ready
- Test-spec readiness: not-ready

## Findings

### BFP-PL6-1 - Runtime identity is not bound across every execution boundary

Finding ID: BFP-PL6-1
Severity: major

Evidence:

- The plan binds an executable and schema but does not capture launcher and
  runtime-package raw-byte/filesystem identities before and after every schema
  generation, sandbox probe, app-server negotiation, and lifecycle invocation.

Required outcome:

Prove the same immutable launcher and runtime package generate the schema,
serve app-server, run probes, and execute the accepted turn.

Safe resolution:

Add before/after identity checks, replacement/removal/mutation tests, identity
fields in promotion evidence, and an unstable-identity failure stop.

### BFP-PL6-2 - Closed feature and protocol-item mapping is underspecified

Finding ID: BFP-PL6-2
Severity: major

Evidence:

- The plan omits the exact permitted command-tool vocabulary and exactly-once
  mapping proof for every feature row and generated item variant.

Required outcome:

Give test-spec authors a closed mapping that cannot silently broaden when the
generated schema changes.

Safe resolution:

Name `shell_tool`, `unified_exec`, `shell_snapshot`, and isolated-workspace
file-change/apply-patch events; require exactly one of three classifications;
test missing, duplicate, unknown, and unclassified mappings.

### BFP-PL6-3 - Lifecycle and protocol descriptions are stale or ambiguous

Finding ID: BFP-PL6-3
Severity: minor

Evidence:

- The source list points to plan-review R3, and the pagination wording can be
  read as applying to methods other than `experimentalFeature/list`.

Required outcome:

Make the current gate and protocol behavior unambiguous.

Safe resolution:

Point to plan-review R6 and separate fully paginated feature retrieval from
the exact closed results required from other methods.

## Prior-Finding Reconciliation

All prior plan findings remain resolved. M1-M4 ownership, preflight-first
sequencing, baseline capture, publication recovery, and promotion commands
remain aligned.
