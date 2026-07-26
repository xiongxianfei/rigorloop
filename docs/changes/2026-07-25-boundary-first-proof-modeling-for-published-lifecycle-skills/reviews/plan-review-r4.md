# Boundary-First Proof Modeling Plan Review R4

Review ID: plan-review-r4
Stage: plan-review
Round: 4
Reviewer: Codex plan-review skill with context-separated reviewer
Target: commit `3905b559` against `ebb59fef`
Reviewed artifact: docs/plans/2026-07-25-boundary-first-proof-modeling.md
Status: changes-requested
Review status: changes-requested
Material findings: none new; BFP-PL4 and BFP-PL5 remain open
Immediate next stage: plan revision
Implementation readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact plan diff; approved R13 specs; accepted R4 architecture/ADR; M1 code-review findings; current test specs
Manifest owner: workflow orchestrator

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: none new; BFP-PL4 and BFP-PL5 remain open
- Recording status: recorded
- Recording blocker: none
- Immediate next stage: plan revision
- Implementation readiness: not-ready
- Test-spec readiness: not-ready

## Findings

No new findings.

## Prior-Finding Reconciliation

### BFP-PL4 - M1-M4 ownership is restored but feasibility ownership is inconsistent

Severity: major
Result: partially-resolved

Evidence:

- The milestone table and bodies restore synthetic M1, fresh upstream M2,
  downstream preservation M3, and aggregation M4.
- The risk section still routes `environment-unavailable` to M1 and
  `validation-m1.md`.
- The dependency section still assigns runtime feasibility to M1.
- M2 says to implement the preflight and then run it before any harness
  mutation, although implementing the preflight is itself a bounded harness
  mutation.

Required outcome:

Assign the minimal feasibility probe, its evidence, and failure stop
consistently to M2. Distinguish the bounded preflight implementation from all
subsequent full-harness and published-skill mutation.

Safe resolution:

Make `check-environment` the first M2 implementation slice, record it in
`validation-m2.md`, run it before any other harness or skill mutation, and stop
M2 with `environment-unavailable` on failure.

### BFP-PL5 - M4 release and parity evidence remains underspecified

Severity: major
Result: partially-resolved

Evidence:

- The controlled fixture, baseline, upstream generation, preservation, and
  report generation/validation boundaries are now exact.
- M4 does not name `dist/adapters/manifest.yaml`.
- M4 does not name the exact durable canonical/generated/packed/installed
  parity-manifest output paths.
- M4 does not name the release-validation test file or an executable
  `scripts/validate-release.py` command.

Required outcome:

Enumerate exact adapter/release inputs, generated evidence paths, release
fixture files, and release-validation and regression commands.

Safe resolution:

Add the tracked adapter manifest, four durable parity-manifest paths, the exact
release fixture and test owner, and a non-publishing release-validation command
using the active release fixture/version.

## Readiness

- Implementation readiness: not-ready
- Test-spec readiness: not-ready
- Immediate next stage: plan revision, then independent plan-review R5
