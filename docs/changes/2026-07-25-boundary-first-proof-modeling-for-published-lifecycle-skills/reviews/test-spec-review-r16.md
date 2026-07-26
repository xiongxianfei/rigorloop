# Boundary-First Proof Modeling Test-Spec Review R16

Review ID: test-spec-review-r16
Stage: test-spec-review
Round: 16
Reviewer: Codex test-spec-review skill with context-separated independent reviewer
Target: specs/rigorloop-workflow.test.md
Reviewed artifact: R45/R18/R15 M2 proof-map candidate at 1e728c98
Status: changes-requested
Review status: changes-requested
Material findings: BFP-TSR16-1
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent

Reviewed commit: `1e728c98`

Reviewed test-spec identity:
`sha256:f71006d8f0901896ea003e9cd3601bd0ab1fd11c524e69652c191ac2606b2fa0`

## Result

Changes requested with one material finding. M2 remains paused.

The R16 candidate resolves BFP-TSR15-1 by proving the staged-run validation
gate. T51 still omits the distinct working-run validation gate before the
working run is renamed to staging.

## Material findings

### BFP-TSR16-1 — T51 moves the working run before proving its required validation gate

Finding ID: BFP-TSR16-1

Severity: major

Location: `specs/rigorloop-workflow.test.md`, T51

Evidence:

- T51 orders working-run build and fsync, staging rename and fsync, then
  complete staged-run and current-input validation.
- R45 separately requires validation of all working-run events, bundles,
  snapshots, inventories, and metrics before the staging rename.
- The approved plan also requires temporary-run validation before staging.
- T51 has no fresh-publication negative proof that invalid working-run
  contents prevent the staging rename.

Required outcome:

Make T51 prove both validation gates in order:

1. build and fsync the working run;
2. validate its events, bundles, snapshots, inventories, and metrics;
3. rename and fsync it as non-authoritative staging;
4. validate the complete staged run and current input identities;
5. write and fsync the prepared receipt;
6. install and validate, point, reconcile, and clean up.

Add malformed or inconsistent working-run cases proving failure before staging
rename, receipt creation, installation, pointer mutation, or lifecycle
reinvocation.

Safe resolution:

Amend only T51 setup, steps, and expected result. Preserve the staged-run
negative cases and post-staged-validation interruption, and add the separate
working-run gate plus its post-validation/pre-rename interruption.

## Readiness

Not ready for implementation. Revise T51 and rerun test-spec review R17.
