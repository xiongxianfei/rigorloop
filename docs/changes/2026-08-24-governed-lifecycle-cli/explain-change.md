# Change explanation: Governed Lifecycle CLI for RigorLoop

Stage: explain-change
Status: current
Final diff identity: base `18a204bb9fa3d6260b19d45896aaa62e89ac0eec`, reviewed subject `96defb9fe4029a76041e216f8e7e320dece8558d`, diff `sha256:1b12a424fdb3ac8ff6dfd020dcc85e053c2abb4eb032da7e4a68d28998be02af`
Final review identity: `code-review-final-r1` recorded by commit `c2fa02e3`

## Summary

RigorLoop now has a local Node CLI that is the deterministic interpreter and guarded mutation boundary for supported governed lifecycle operations. Git-tracked `change.yaml` and semantic artifacts remain durable truth. Governed authoring and review skills call semantic CLI operations instead of carrying detailed status-edit and settlement procedures.

## Problem

Direct lifecycle-field edits made every human or agent responsible for interpreting transition prerequisites, artifact identity, evidence freshness, review findings, milestone order, and atomic updates. The duplicated mechanics increased prompt size and allowed plausible but unsupported state transitions.

## Decision trail

- Proposal: `docs/proposals/2026-08-24-governed-lifecycle-cli.md`
- Contract: `specs/governed-lifecycle-cli.md`
- Architecture: `docs/architecture/system/architecture.md`
- Transaction ADR: `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`
- Plan: `docs/plans/2026-08-24-governed-lifecycle-cli.md`
- Proof map: `specs/governed-lifecycle-cli.test.md`
- Final review: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-final-r1.md`

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `packages/rigorloop/dist/lib/lifecycle-*` | Added parsing, canonical interpretation, semantic operations, exact identities, optimistic concurrency, atomic replacement, recovery, migration, and repair. | Enforce lifecycle invariants once without hidden state or arbitrary setters. | Spec R1-R27, ADR transaction boundary | Package lifecycle suites; M1-M5 evidence |
| `packages/rigorloop/dist/bin/rigorloop.js` | Added `rigorloop lifecycle` dispatch and help. | Expose one human, agent, adapter, and CI contract. | Spec R3-R10 | Package CLI tests |
| Governed authoring and review references | Replaced field-level mutation procedure with context, registration, review, and settlement calls. | Reduce agent mechanics while retaining semantic criteria and authority limits. | Spec R28-R34 | M6 skill, adapter, and token evidence |
| `scripts/validate-governed-lifecycle-cli.py` and `scripts/ci.sh` | Added public-validator CI enforcement with exact baseline fingerprinting. | Detect unsupported governed state without a parallel interpreter. | Spec R23, R30; T21 | M7 enforcement evidence |
| Proposal, spec, architecture, ADR, plan, and proof map | Recorded product boundary, compatibility, migration, recovery, commands, and proof obligations. | Keep implementation reviewable and traceable. | Workflow contract | Stage reviews and review log |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| T01-T05 | Closed contracts, safe YAML, status/context/validate, deterministic diagnostics | contract/integration |
| T06-T17 | Authoring, evidence, settlement, milestones, concurrency, atomicity, recovery, migration, and authority | integration |
| T18-T20 | Semantic preservation, adapter parity, and mechanics-token reduction | contract/integration |
| T21-T25 | CI enforcement, deterministic composition, containment, package smoke, and full lifecycle composition | end-to-end/smoke |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `npm test --prefix packages/rigorloop` | passed, 160 tests | reviewed subject `96defb9f` |
| Canonical skill validation and build checks | passed, including 446 skill tests | M6 evidence |
| `python3 scripts/test-adapter-distribution.py` | passed, 150 tests | M6 evidence |
| Protected lifecycle/change/review validator suites | passed, 170 + 63 + 103 tests | M7 evidence |
| `python3 scripts/validate-governed-lifecycle-cli.py` | passed for 28 changes with one exact known baseline warning | M7 evidence |
| `python3 scripts/measure-lifecycle-skill-tokens.py` | passed; mechanics down 45.7%, mechanics plus CLI context down 30.0% | M6 evidence |

## Review resolution summary

All nine material findings from earlier proposal, spec, architecture, and M1 code-review rounds have closed dispositions and validation in `review-resolution.md`; `review-log.md` has no open finding. Later milestone and final reviews are clean-with-notes. Direct reviews follow the recorded user override and make no independence claim.

## Alternatives rejected

Direct YAML editing, schema-only validation, per-skill lifecycle engines, a hosted control plane, and an autonomous workflow runner were rejected because they weaken guarded transition intent, duplicate mechanics, or expand beyond the Git-first local product boundary.

## Scope control

The CLI does not make semantic judgments, route workflow, invoke agents, edit semantic artifacts, open or merge pull requests, deploy, or provide hosted authorization. Portable skill use remains available without `change.yaml`.

## Risks and follow-ups

The local boundary is not a malicious-maintainer security perimeter. One unrelated historical change remains structurally valid but blocked by its exact recorded workflow blocker and ten findings; CI fingerprints that known baseline and fails on drift. Final branch readiness remains owned by `verify`.

## Workflow handback

Explanation status: current
Explanation basis: `18a204bb9fa3d6260b19d45896aaa62e89ac0eec..96defb9fe4029a76041e216f8e7e320dece8558d`, final review recording commit `c2fa02e3`
Validation-evidence cutoff: final review recording commit `c2fa02e3`
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
