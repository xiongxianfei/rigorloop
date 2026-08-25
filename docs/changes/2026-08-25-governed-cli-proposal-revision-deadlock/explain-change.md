<!-- explain-change-skeleton-v1; normative -->

# Change explanation: Governed CLI proposal revision deadlock

Stage: explain-change
Status: current
Final diff identity: `8bf931bff643c47c37ee814cbbb0aefdf219f16a..c26133b3997afb2736b917fb938a8615ae885766` (`sha256:413f901a315fc8480d639bd52fc7b396bcf479c29b7e74b72985b081c7a4f66e`)
Final review identity: `code-review-final-r2` recorded by revision `6a1eb41c`

## Summary

The governed lifecycle CLI now treats a `changes-requested` review as a handback to the artifact owner even when the review's material findings remain open. It settles the exact artifact to `revision-required`, exposes `record-artifact-revision` as the next operation, and selects the next durable review round after revision. Positive approval still cannot settle while material findings are open.

## Problem

The settlement implementation applied the unresolved-finding guard before it interpreted the review outcome. That made the guard correct for approval but incorrect for `changes-requested`: the very findings that justified a revision request prevented the CLI from recording that revision request. Status then returned no permitted operation, so proposal and other governed artifact revisions could deadlock at the review boundary.

## Decision trail

- Lifecycle rule: `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md` SLA-R025 requires `changes-requested` to map to `revision-required`.
- CLI contract: `specs/governed-lifecycle-cli.md` R9, R10, R15, R18, R19, and R22 govern interpreted status, context, evidence binding, atomic mutation, and idempotence.
- Proof map: `specs/governed-lifecycle-cli.test.md` T08 covers exact settlement and unresolved-evidence boundaries.
- Architecture: `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md` keeps interpretation and guarded mutation in the existing local CLI boundary.
- Stable plan: `docs/plans/2026-08-24-governed-lifecycle-cli.md` remains unchanged because this is a bounded conformance repair.
- Final review: `docs/changes/2026-08-25-governed-cli-proposal-revision-deadlock/reviews/code-review-final-r2.md`.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `lifecycle-operations.js` | Derive the review outcome before applying the open-finding guard; guard only positive settlement; synchronize summary state and clear superseded authoring evidence. | Negative settlement must preserve findings while returning the artifact to its owner. | SLA-R025; CLI R15, R19, R22 | `lifecycle-evidence.test.js` |
| `lifecycle-read.js` | Distinguish finding-only blockers from fatal blockers, expose the owner revision operation, and calculate the next durable review round. | Status and context must describe the operation that can actually make progress without bypassing an independent blocker. | CLI R9, R10 | `lifecycle-read.test.js` |
| Lifecycle evidence tests | Add the `changes-requested` regression while retaining positive-settlement rejection and byte preservation. | Prove both sides of the finding boundary directly. | Test spec T08 | Focused and full package tests |
| Lifecycle read tests | Cover revision routing, fatal-blocker suppression, and r1-to-r2 advancement. | Prevent a correct mutation from remaining operationally unreachable. | CLI R9, R10 | Focused and full package tests |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| BUGFIX-SETTLE-NEGATIVE | `changes-requested` plus `F-1` settles to `revision-required` and exposes revision authoring. | Integration |
| T08-positive guard | Approved review plus `F-1` remains blocked and leaves `change.yaml` byte-identical. | Integration |
| BUGFIX-STATUS-ROUTE | A revision-required artifact permits authoring, while an additional fatal blocker permits nothing. | Integration |
| BUGFIX-ROUND-NEXT | A durable `spec-review-r1.md` causes the next review context to select `r2`. | Integration |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `node --test test/lifecycle-artifact-revision.test.js test/lifecycle-evidence.test.js test/lifecycle-read.test.js` | passed; 12 tests | `e0509568` |
| `npm test` | passed; 162 tests | `e0509568` |
| `python3 scripts/validate-npm-package.py` | passed from repository root | `e0509568` |
| Change metadata validation | passed | `6a1eb41c` parent state |
| Review structure and closeout validation | passed; two clean receipts and no findings | `6a1eb41c` parent state |

The first package-validator attempt was invoked from `packages/rigorloop` and failed because the script expects repository-root-relative paths. It was rerun from the repository root and passed; the incorrect invocation is not used as evidence.

## Review resolution summary

No material finding was recorded in either code-review receipt, so `review-resolution.md` is not required. The review log is `docs/changes/2026-08-25-governed-cli-proposal-revision-deadlock/review-log.md`.

## Alternatives rejected

- Requiring finding resolution before recording `changes-requested` was rejected because it makes the handback transition depend on work that only the handback can authorize.
- Treating every open-finding blocker as ignorable was rejected because positive approval must remain blocked.
- Reopening the merged CLI initiative's lifecycle record was rejected because this correction has its own branch, evidence root, and review history while linking to the existing approved contract.
- Adding a generic status override or repair escape hatch was rejected because the operation engine must derive state from the recorded review outcome.

## Scope control

This correction does not change command names, request schemas, workflow routing authority, review semantics, evidence identity, concurrency, transaction recovery, skill text, adapters, or the approved lifecycle specifications. It does not resolve findings automatically or infer semantic approval.

## Risks and follow-ups

The finding parser continues to consume the existing `Open findings:` ledger format; this PR does not redesign review-log serialization. Review was same-session under the user's no-subagent instruction, so independent human PR review remains valuable. Hosted CI is not yet observed at this explanation stage.

## Workflow handback

Explanation status: current
Explanation basis: `8bf931bff643c47c37ee814cbbb0aefdf219f16a..c26133b3997afb2736b917fb938a8615ae885766`; final review `code-review-final-r2` recorded by `6a1eb41c`
Validation-evidence cutoff: `6a1eb41c`
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
