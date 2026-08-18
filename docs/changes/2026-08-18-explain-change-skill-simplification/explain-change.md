<!-- explain-change-skeleton-v1; normative -->

# Change explanation: Explain-Change Skill Simplification

Stage: explain-change
Status: current
Final diff identity: sha256:53978a43d81090a60c0085ec82b935ed913e98ac57c1a9dc8623f87ec6947c2e
Final review identity: sha256:a1d8bf3ae732843299068ba3492061a4ebba35f1dffe77a8381244af10e823f9
Reviewed subject revision: 2817aab0e75cc339138009c574581bf3e22f919f
Base revision: 11179cb7f91a4a149bd763bae6a3dfbbadb3f60f
Final-review recording revision: 9daf13fca5d3719f767d65f581f56c1a7e0b8351

## Summary

The explain-change skill now loads a compact universal contract for ordinary rationale work, one governed-workflow reference only when change-local authority applies, and one skeleton only for durable output. The implementation also makes the final review, explanation, and verify sequence executable: Git derives the reviewed subject `S`, final-review commit `R`, explanation commit `E`, and handoff separately while verification rejects reordered, broader, destructive, or ambiguous evidence tails.

## Problem

The former flat skill mixed universal diff explanation with governed lifecycle procedure and repeated durable layout, so small requests loaded irrelevant material. Its first simplified final-review rule then allowed only one explanation commit after the reviewed subject, which could not also preserve the formal final-review evidence required before explain-change. Shared `change.yaml` paths also needed field- and list-level ownership so a nominally allowed file could not conceal another stage's mutation.

## Decision trail

- The accepted proposal chose a compact `SKILL.md`, one governed reference, one copied skeleton, and no runtime generator.
- Spec R1-R44 defines portable/governed classification, whole-file durable output, workflow handback, and exact `S -> R -> E` evidence ordering.
- ADR-20260818 keeps the reviewed product identity base-to-`S`, derives later commit identities from Git, and reuses the existing change record and evidence owners.
- Plan M1-M4 separates preservation inventory, package extraction, package-chain proof, and ordered-tail implementation.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/explain-change/` | Replaced the flat procedure with a compact root, governed reference, and structural skeleton. | Reduce all four loaded assemblies without weakening universal truthfulness or claims. | R1-R21, R30-R44 | `ExplainChangeSkillSimplificationTests`; M1-M3 evidence |
| `scripts/workflow_code_state.py` | Derives `S`, `R`, `E`, handoff, exact paths, semantic fields, and append-only shared-list deltas. | Make final-review reuse executable and prevent path-only lifecycle bypass. | R22-R29; ADR-20260818 | 18 real-Git code-state tests; M4 evidence |
| `scripts/workflow_automation.py` | Requires the complete ordered tail before verify readiness. | Keep partial `S -> R` recoverable for explain-change but ineligible for verify. | R26-R29 | 76 workflow-automation tests |
| Specs, architecture, plan, and test spec | Record the package boundary, identity model, recovery, and proof map. | Keep observable behavior, design ownership, execution, and validation traceable. | Approved lifecycle artifacts | Spec, architecture, plan, and test-spec reviews |
| Fixtures and validators | Cover classifications, resource assemblies, size gates, stage order, unknown fields, destructive lists, and package parity. | Prove both the simplified context and fail-closed boundary behavior. | R36-R44 | 418 skill tests; 150 adapter tests; build checks |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| T01-T08, T12-T18 | Classification, resources, durable composition, closeout, claims, compatibility, size, and packaging remain closed. | contract/integration |
| T09-T11 | Reviewed basis, exact tail, partial retry, forbidden ancestry, and field ownership receive opposite outcomes. | integration |
| T19 | A real temporary Git repository executes `S -> R -> E -> verify` and preserves the pre-verify cutoff. | end-to-end |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| Approved CMD-01-CMD-12 ledger | Passed | reviewed subject `2817aab0e75cc339138009c574581bf3e22f919f` |
| Skill validator | 418 passed; 16 documented skips | reviewed subject |
| Adapter distribution | 150 passed | reviewed subject |
| Workflow state, workflow automation, code state, and build tests | 65, 76, 18, and 7 passed | reviewed subject |
| Skill, generated build, boundary, metadata, prose, review-closeout, and diff checks | Passed | final review `code-review-final-r2` |

## Review resolution summary

`EXCSIM-TSR1`, `EXCSIM-CR1`, `EXCSIM-CR2`, and `EXCSIM-CR3` have final accepted/resolved dispositions in [review-resolution.md](review-resolution.md). The final holistic review found no material findings.

## Alternatives rejected

A flat inline rewrite would retain excessive common-path context. Multiple small references would increase routing and package drift. A single combined review/explanation commit would blur stage identity, while an explanation-only commit would leave formal review evidence uncommitted. A new transaction artifact, Git note, runtime generator, or Markdown-region parser would add persistence or ownership without solving a distinct first-version need.

## Scope control

The change does not add a model-runtime evaluator, prose grader, section-level refresh, generated skill source, new lifecycle state, new database or service, external integration, or target-agent acceptance run. Historical explanations are not migrated unless explicitly refreshed.

## Risks and follow-ups

The principal residual risk is future schema evolution adding legitimate workflow fields that are not in the closed stage manifests; such a change should fail closed and update the governing spec, validator, and tests together. The EC3 assembly remains deliberately close to the frozen byte ceiling at 8,212 versus 8,224 bytes, while its word count falls from 1,175 to 1,038; future governed guidance should preserve that measured boundary or explicitly revise it.

## Workflow handback

Explanation status: current
Explanation basis: sha256:31280ebc4fee48f5d3808dcabf33678c72fad3d735d233afb60cd91455565105
Validation-evidence cutoff: reviewed-subject:2817aab0e75cc339138009c574581bf3e22f919f
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
