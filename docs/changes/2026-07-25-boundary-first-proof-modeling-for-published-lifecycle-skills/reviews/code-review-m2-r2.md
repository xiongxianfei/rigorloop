# Code Review M2 R2

Review ID: code-review-m2-r2

Stage: code-review

Round: 2

Reviewer: Codex code-review skill with context-separated independent reviewer

Target: commit range 093a0677..343478f2

Reviewed artifact: M2 correction commit range `093a0677..343478f2`

Status: blocked

Review status: blocked

Reviewed milestone: M2

Material findings: BFP-CR-M2-7, BFP-CR-M2-8

Immediate next stage: upstream contract resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-26

Context separation mechanism: separate-agent

Manifest owner: workflow orchestrator

## Evidence reviewed

- Governing R28y and R56 requirements and T49-T52 proof obligations.
- Architecture, ADR, active plan, M2 R1 review, and review resolution.
- Actual implementation and tests in the reviewed commit range.
- Immutable behavior run `run-91e41340b56169c06158eca244fb117c`.
- Focused boundary tests, canonical run validation, skill validation, generated
  skill parity, skill-validator tests, change metadata, review artifacts,
  lifecycle state, compilation, and diff integrity.

## Findings

### BFP-CR-M2-7 - Transient stage retry lacks evidence-first safety proof

Finding ID: BFP-CR-M2-7

Severity: major

Evidence:

- The coordinator retries an entire fresh stage invocation once after
  `_StageTurnTimeout`.
- The focused test proves only timeout classification. It does not prove retry
  count, terminal failure, non-retry of protocol/security failures, or output
  reconciliation.
- When stages own files, a timeout can happen after complete or partial output
  exists; blind reinvocation can repeat nondeterministic work.

Required outcome: Retry only an explicitly transient turn with no output
evidence. Reconcile complete output without reinvocation and fail closed on
partial output or non-retryable errors.

Safe resolution: Extract a testable stage retry/reconciliation coordinator and
prove timeout-then-success, two-timeout failure, non-retryable failure,
complete-output reconciliation, partial-output stop, and validation-only
no-reinvocation.

### BFP-CR-M2-8 - Publication ordering contradicts governing artifacts

Finding ID: BFP-CR-M2-8

Severity: blocker

Evidence:

- The implementation durably writes `prepared.json` before immutable-run
  installation.
- Named architecture and active-plan sequences say install the immutable run
  before writing the receipt.
- Other architecture language requires a prepared receipt before mutation.
- R1 resolution selected receipt-before-install without synchronizing the
  governing architecture and plan.

Required outcome: Establish one transaction ordering across the approved spec,
architecture, ADR, plan, tests, and implementation.

Recommended direction: Retain staged validation, then durable exclusive
receipt, then immutable installation, and formally amend and rereview the
governing artifacts before implementation proceeds.

## R1 reconciliation

`BFP-CR-M2-1` remains open as a failed remediation. R28y requires
workflow-orchestrated stage ownership, but the reviewed stage requests bind
individual stage skills without `workflow`, and the harness still supplies the
normative feature requirements, acceptance criteria, test cases, and validation
contract through its renderers. Resolution requires `workflow` orchestration,
complete stage-created files below the isolated output root, snapshot-before-
advance behavior, removal of substantive harness renderers, and regenerated
immutable evidence.

| Finding | Result |
| --- | --- |
| `BFP-CR-M2-1` | failed remediation |
| `BFP-CR-M2-2` | resolved |
| `BFP-CR-M2-3` | resolved |
| `BFP-CR-M2-4` | implementation crash window corrected; governing-order conflict recorded as `BFP-CR-M2-8` |
| `BFP-CR-M2-5` | resolved |
| `BFP-CR-M2-6` | resolved |

## Validation

Passed:

- `python scripts/test-boundary-proof.py` — 49 tests.
- Canonical validation of `run-91e41340b56169c06158eca244fb117c`.
- `python scripts/validate-skills.py`.
- `python scripts/build-skills.py --check`.
- `python scripts/test-skill-validator.py` — 259 tests.
- Change metadata, review structure, lifecycle, compilation, and diff checks.

Passing validation does not override the ownership, retry, or architecture
contract findings.

## Handoff

- Review result: blocked.
- Milestone state: resolution-needed.
- Next stage: upstream contract resolution, then review-resolution and M2
  implementation correction.
- M3, final verification, and PR handoff remain blocked.
