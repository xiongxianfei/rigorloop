# Change explanation: Workflow-Routed Upstream Corrections

Stage: explain-change
Status: current
Final diff identity: `sha256:1c73954f8f4e87859192efb92bdd52139ec90a230fb35b2382a7a61b7dac1e2d` for `bcc7ef14ae45e8df737d8a97e72eff3a3823446b..ffc03485ea6a8f48d5f8d4a89d051f7d669312b7`
Final review identity: `b7bfef853bed4cbcbdd2d0b994b417fa59128c43`

## Summary

RigorLoop now gives workflow a guarded way to route an in-progress change back to one exact upstream artifact, return after that revision receives an exact approving review, and withdraw a proved duplicate architecture or ADR registration. The CLI—not individual authoring skills—validates lifecycle state, evidence, authority, ownership, freshness, and atomic mutation. Authoring skills receive only a short route-required handback, keeping lifecycle mechanics centralized and token-friendly.

## Problem

The earlier lifecycle boundary correctly rejected a downstream skill that tried to revise a settled upstream artifact, but it offered no supported way for workflow to suspend the downstream state, request the correction, and restore the preserved work afterward. A separate duplicate artifact registration also demonstrated that path ownership needed repository-wide collision prevention and a narrow recovery operation. Direct YAML edits would bypass the CLI and could lose milestone, blocker, review, or evidence identity.

## Decision trail

- [Proposal](../../proposals/2026-08-25-workflow-routed-upstream-corrections.md) selected workflow-owned routing, CLI-enforced mutation, and guarded duplicate withdrawal.
- [Specification](../../../specs/workflow-routed-upstream-corrections.md) defines R1-R32, including exact evidence, stale-operation, authority, output, and compatibility behavior.
- [Architecture](../../architecture/2026-08-25-workflow-routed-upstream-corrections.md) places the new operations in the existing lifecycle contract, read model, operation engine, and atomic transaction boundary.
- [ADR](../../adr/ADR-20260825-workflow-routed-correction-and-artifact-ownership.md) selects explicit coordination schema version 2 and repository-indexed artifact ownership.
- [Plan](../../plans/2026-08-25-workflow-routed-upstream-corrections.md) delivered the change as version/ownership, correction routing, and withdrawal/consumer milestones.
- [Test specification](../../../specs/workflow-routed-upstream-corrections.test.md) maps every requirement to T01-T10 and the repository validation gates.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `lifecycle-contract.js` | Adds the three operations, stable diagnostics, request fields, authority rules, and closed vocabularies. | Callers request semantic operations; they cannot assign arbitrary status. | Spec R1-R6, R20-R21, R30-R31 | T01, T06; `lifecycle-contract.test.js` |
| `lifecycle-operations.js` | Implements exact route snapshots, reviewed return, cross-change ownership, guarded withdrawal, scoped settlement, and milestone projection fixes. | Prevent unsupported corrections while preserving the exact downstream state and semantic artifacts. | Spec R7-R25; ADR | T02-T06, T08, T10 |
| `lifecycle-read.js` and CLI presentation | Interprets active corrections, validates stored coordination, separates immediate from deferred operations, and emits bounded diagnostics. | Humans and agents need one concise canonical interpretation without loading lifecycle mechanics. | Spec R26-R28, R32 | T07, T10; `lifecycle-read.test.js` |
| Package tests | Adds route, ownership, and withdrawal suites and expands contract, evidence, migration, milestone, read, and transaction coverage. | Every new invariant and closed vocabulary needs executable refusal and success proof. | Test spec T01-T10 | 178 package tests passed |
| Governed skill references | Adds a two-line route-required handback to upstream authoring skills and keeps route/return/withdrawal mechanics in workflow. | Preserve semantic skill focus and reduce repeated lifecycle instructions. | Spec R3, R29; proposal token boundary | T09; skill validation and broad smoke |
| Documentation and governed artifacts | Documents public operations, workflow behavior, decisions, reviews, and milestone evidence. | Keep Git-contained truth and make the behavior reviewable from a fresh checkout. | Proposal, spec, workflow contract | Metadata, review-artifact, documentation, and lifecycle validators |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| T01-T02 | Version migration, closed vocabularies, and collision-safe repository ownership. | contract and integration |
| T03-T05 | Exact correction route, review-occurrence settlement, and identity-bound return with source restoration. | integration |
| T06 | Guarded duplicate withdrawal and the complete unsafe-withdrawal refusal matrix. | integration |
| T07 | Concise human/JSON context with separate immediate and deferred operations. | contract and integration |
| T08 | Stale envelopes and transaction faults preserve prior bytes or named recovery state. | integration |
| T09-T10 | Skill authority separation, fresh-checkout reconstruction, and valid receipt exclusion from active ownership. | repository contract and integration |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `npm test --prefix packages/rigorloop` | pass, 178 tests | implementation commit `ffc03485` |
| `python3 scripts/validate-change-metadata.py docs/changes/2026-08-25-workflow-routed-upstream-corrections/change.yaml` | pass | final-review state before this explanation |
| `python3 scripts/validate-review-artifacts.py docs/changes/2026-08-25-workflow-routed-upstream-corrections` | pass, 18 reviews and 5 resolved findings | final-review commit `b7bfef85` |
| `rigorloop lifecycle validate --change 2026-08-25-workflow-routed-upstream-corrections --format json` | pass; no blockers, stale evidence, or lifecycle errors | final-review state before this explanation |
| `bash scripts/ci.sh --mode broad-smoke --jobs 2` | pass, 11 checks | M3 implementation evidence before final review |
| `git diff --check` | pass | final-review state before this explanation |

## Review resolution summary

All five material proposal and specification findings are closed with accepted dispositions in [review-resolution.md](review-resolution.md). They tightened the same-slice recovery commitment, source-blocker suspension, exact return evidence, non-circular receipt identity, and state/authority boundary. Milestone reviews and the [final review](reviews/code-review-final-r1.md) found no additional material issues.

## Alternatives rejected

Direct lifecycle YAML editing was rejected because it bypasses guarded mutation and can corrupt preserved state. Allowing authoring skills to select or execute routes was rejected because workflow owns routing. Automatically returning after file or test success was rejected because only an exact current approving review can authorize return. General artifact deletion or arbitrary repair was rejected in favor of architecture/ADR-only withdrawal with provable canonical ownership.

## Scope control

The change does not add semantic approval, autonomous orchestration, automatic workflow progression, generic status setting, artifact deletion, distributed locking, hosted authorization, or release publication. Portable skill mode remains independent of governed lifecycle state. Applying the new operations to other active branches is a separate follow-on after this feature is verified.

## Risks and follow-ups

Repository-wide ownership discovery is linear in governed change records; this is acceptable for the local first release and has no hidden cache. Local atomicity does not replace Git branch integration controls. Release archive generation and versioned adapter metadata must be updated only during the next release preparation, not by rewriting the immutable `v0.4.1` archive on this feature branch.

## Workflow handback

Explanation status: current
Explanation basis: implementation `ffc03485ea6a8f48d5f8d4a89d051f7d669312b7` plus final review `b7bfef853bed4cbcbdd2d0b994b417fa59128c43`
Validation-evidence cutoff: final review on 2026-08-25
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
