# Boundary-First Proof Modeling Test-Spec Review R15

Review ID: test-spec-review-r15
Stage: test-spec-review
Round: 15
Reviewer: Codex test-spec-review skill with context-separated independent reviewer
Target: specs/rigorloop-workflow.test.md
Reviewed artifact: R45/R18/R15 M2 proof-map candidate at 90f98bb2
Status: changes-requested
Review status: changes-requested
Material findings: BFP-TSR15-1
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent

Reviewed commit: `90f98bb2`

Reviewed test-spec identity: `sha256:fbe9968bf717eda270f5ef01c0213c95cf736ac7401b869a4dbb6d86118a044a`

## Result

Changes requested with one material finding. M2 remains paused.

The v2, opaque-v1, child-denial, workspace-integrity, envelope,
materialization, retry, command, and milestone proof is otherwise complete.
T51 does not yet prove that complete staged-run and current-input validation
must pass before prepared-receipt creation.

## Material findings

### BFP-TSR15-1 — Publication proof does not enforce staged validation before receipt creation

Finding ID: BFP-TSR15-1

Severity: major

Location: `specs/rigorloop-workflow.test.md`, T51

Evidence:

- R45 requires complete staged-run and current-input validation before the
  prepared receipt is written.
- The approved plan orders staged build and validation before durable receipt,
  immutable installation, installed-run validation, pointer replacement, and
  cleanup.
- T51 covers interruptions around receipt and installation but does not
  explicitly require the validation gate immediately before receipt creation.
- T51 lacks malformed, incomplete, identity-mismatched, and stale staging
  cases that prove no receipt, installation, or pointer mutation occurs.

Required outcome:

Make T51 prove this exact order:

1. build and fsync the working/staged run;
2. validate the complete staged run and current input identities;
3. exclusively write and fsync the prepared receipt;
4. install and validate the immutable run;
5. replace and fsync the pointer;
6. reconcile and clean up the receipt.

Add invalid and stale staged-run cases plus an interruption after successful
staged validation but before receipt creation.

Safe resolution:

Revise only T51 setup, steps, and expected result. Invalid staging must leave
no prepared receipt, immutable installation, pointer mutation, or lifecycle
reinvocation. No upstream redesign is required.

## Readiness

Not ready for implementation. Revise T51 and rerun test-spec review R16.
