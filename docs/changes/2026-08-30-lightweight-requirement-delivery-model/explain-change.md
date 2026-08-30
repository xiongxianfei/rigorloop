# Change explanation: Lightweight Requirement-to-Delivery Model

Stage: explain-change
Status: current
Final diff identity: `origin/main...234f10d806f2d283aa5df4e8e895a1d1369f25f2`
Final review identity: `code-review-m4-r2` at `96e5da7fbc77598c3f435878e99fdbb55d7005de`

## Summary

This change gives RigorLoop one concise conceptual path from an incoming need to implementation evidence. It treats the incoming need as RR, the approved proposal as IR, specification requirements as durable SRs, architecture as SR realization, and planning as proportional allocation into work. It reuses existing artifacts and review gates; RR, IR, and AR do not become new records or lifecycle stages.

## Problem

Proposal, specification, architecture, plan, implementation, and verification already form a requirement-to-delivery chain, but contributors had to infer their relationship. Equating RR/IR/SR/AR with Epic/Feature/Story/Task would also confuse requirement refinement with work decomposition and encourage unnecessary hierarchy.

## Decision trail

- Proposal Review `proposal-review-r1` approved the lightweight conceptual model without new RR, IR, or AR artifacts.
- Design Review `design-review-r2` approved the architecture/specification package and its stage ownership, authority boundary, and nine selected skill consumers.
- Delivery Review `delivery-review-r2` approved three implementation milestones plus lifecycle closeout and the exact proof map.
- Final holistic Code Review `code-review-m4-r2` reviewed subject `234f10d806f2d283aa5df4e8e895a1d1369f25f2` and found no material issue.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `templates/shared/requirement-to-delivery-model.md` | Define RR → IR → SR → AR, separate work decomposition, proportionality, many-to-many allocation, traceability, and authority limits | Give all stages one concise conceptual vocabulary | RTD-R1–RTD-R10, RTD-R13–RTD-R16 | RTD-T01–RTD-T04; M1 evidence |
| Four authoring skills and local references | Add conditional loading and stage-local responsibility for proposal, spec, architecture, and plan | Make existing artifacts expose their role without adding entities | RTD-R2–RTD-R10 | M1 focused tests and skill validation |
| Five review/verification skills and local references | Add the traceability question owned by each existing gate | Strengthen semantic traceability without expanding review authority | RTD-R11, RTD-R12, RTD-R15, RTD-R20 | RTD-T05–RTD-T06; M2 evidence |
| `scripts/skill_validation.py` | Fail closed when a selected local copy is missing or differs from the canonical source | Keep canonical and published skill packages coherent through an existing validator | RTD-R13, RTD-R14, RTD-R18–RTD-R20 | RTD-T07; M3 evidence |
| `scripts/test-skill-validator.py` | Prove model shape, stage integration, optional hierarchy, two-way allocation, authority exclusion, nine-copy parity, and public-validator failure | Protect the lightweight contract and its packaging boundary | RTD-AC1–RTD-AC10 | 369 passing tests |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| RTD-T01–RTD-T04 | Core model, stage ownership, proportional hierarchy, many-to-many allocation, and existing artifact fields | Contract and integration |
| RTD-T05–RTD-T06 | Gate-local forward/reverse traceability with unchanged authority | Skill integration |
| RTD-T07 | Missing and drifted selected copies fail through the public validator | Validator regression |
| RTD-T08 | Temporary generated packages, archives, and clean installs carry mapped resources | Build and adapter integration |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `python scripts/test-skill-validator.py` | 369 passed | M3 R2 |
| `python scripts/test-build-skills.py` | 8 passed | M3 R1 |
| `python scripts/build-skills.py --check` | Passed with temporary output | M3 R2 |
| `python scripts/test-adapter-distribution.py` | 152 passed | M3 R1 |
| Ten-path documentation prose audit | 0 errors, 0 warnings | M2 R1 |
| Review structure, closeout, and change metadata | Passed with five resolved findings | M4 R2 |

## Review resolution summary

All five material findings have accepted, resolved dispositions in `review-resolution.md`. They cover design activation metadata, delivery trace ownership and timing, a concrete many-to-many example, and public-validator integration proof. `code-review-m4-r2` is the clean final holistic review.

## Alternatives rejected

- New RR, IR, or AR artifacts and identifiers were rejected because existing input, proposal, specification, architecture, and plan surfaces already own the needed decisions.
- Equating RR/IR/SR/AR with Epic/Feature/Story/Task was rejected because requirement refinement and work decomposition are separate many-to-many dimensions.
- Mandatory Epic, Feature, Story, and Task levels were rejected in favor of adding only work levels that improve delivery decisions.
- A new lifecycle stage, database, semantic traceability engine, or standalone validator was rejected as unnecessary ceremony.

## Scope control

This change does not remove test-spec, redistribute proof design, alter review-gate order or authority, add machine-readable traceability, integrate external trackers, retrofit historical artifacts, commit generated adapter packages, or change release behavior.

## Risks and follow-ups

The residual risk is terminology being treated as mandatory new structure. The shared authority boundary, proportional example, stage-local load conditions, and negative tests constrain that interpretation. Any future lifecycle entity or machine-readable traceability mechanism still requires a separate approved proposal.

## Workflow handback

Explanation status: current
Explanation basis: `origin/main...234f10d806f2d283aa5df4e8e895a1d1369f25f2`; final review `code-review-m4-r2`
Validation-evidence cutoff: `96e5da7fbc77598c3f435878e99fdbb55d7005de`
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
