<!-- explain-change-skeleton-v1; normative -->

# Change explanation: Explain-Change Skill Simplification

Stage: explain-change
Status: current
Final diff identity: sha256:cad006e6a562627cff91efce84d1a56d676085672b925b2de8dd8ce3eb139dff
Final review identity: sha256:220c6bd87e091788c2a2fd732b413544a39564107612c7312c5334d296ff493a
Reviewed subject revision: 7a6dab806f91a12aef811a89a7c4a59829dab71c
Base revision: 11179cb7f91a4a149bd763bae6a3dfbbadb3f60f
Final-review recording revision: ec4fca20ec5a21815c38d429b26107a1d1120a7c

## Summary

The explain-change skill now loads a compact universal contract for ordinary rationale work, one governed-workflow reference only when change-local authority applies, and one skeleton only for durable output. The implementation also makes the final review, explanation, and verify sequence executable: Git derives the reviewed subject `S`, final-review commit `R`, explanation commit `E`, and handoff separately while verification rejects reordered, broader, destructive, or ambiguous evidence tails.

The final lifecycle correction normalizes the proposal’s accepted status and follow-on list and removes duplicate ownership of the canonical architecture artifact. These are governance corrections inside the reviewed subject; they do not alter shipped explain-change behavior.

## Problem

The former flat skill mixed universal diff explanation with governed lifecycle procedure and repeated durable layout, so small requests loaded irrelevant material. Its first simplified final-review rule then allowed only one explanation commit after the reviewed subject, which could not also preserve the formal final-review evidence required before explain-change. Earlier lifecycle closeout also left proposal status and canonical architecture ownership inconsistent with the authored and reviewed documents.

## Decision trail

- The accepted proposal chose a compact `SKILL.md`, one governed reference, one copied skeleton, and no runtime generator.
- Spec R1-R44 defines portable/governed classification, whole-file durable output, workflow handback, exact `S -> R -> E` evidence ordering, and literal preservation.
- ADR-20260818 keeps the reviewed product identity base-to-`S`, derives later commit identities from Git, and reuses the existing change record and evidence owners.
- Plan M1-M4 separates preservation inventory, package extraction, package-chain proof, and ordered-tail implementation.
- Proposal review R4 and architecture review R2 approve the final lifecycle corrections; final code review `code-review-final-r4` finds no material implementation defect.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/explain-change/` | Replaced the flat procedure with a compact root, governed reference, and structural skeleton while retaining the concise review-resolution summary contract. | Reduce all four loaded assemblies without weakening universal truthfulness, claims, or cross-skill literals. | R1-R21, R30-R44 | 11 `ExplainChangeSkillSimplificationTests`; M1-M3 evidence |
| `scripts/workflow_code_state.py` | Derives `S`, `R`, `E`, handoff, exact paths, semantic fields, and append-only shared-list deltas. | Make final-review reuse executable and prevent path-only lifecycle bypass. | R22-R29; ADR-20260818 | 18 real-Git code-state tests; M4 evidence |
| `scripts/workflow_automation.py` | Requires the complete ordered tail before verification readiness. | Keep partial `S -> R` recoverable for explain-change but ineligible for verify. | R26-R29 | 76 workflow-automation tests |
| Specs, architecture, ADR, plan, and test spec | Record package boundaries, identity, recovery, ownership, execution, and proof. | Keep observable behavior and durable design decisions traceable. | Approved lifecycle artifacts | Independent proposal, spec, architecture, plan, and test-spec reviews |
| Fixtures, validators, and preservation evidence | Cover classifications, resource assemblies, size gates, stage order, unknown fields, destructive lists, required literals, and package parity. | Prove the simplified context and fail-closed compatibility boundaries. | R36-R44 | Focused and full repository-owned validation suites |
| Proposal and architecture lifecycle evidence | Normalized accepted proposal status and preserved sole canonical architecture ownership. | Remove final PR-lifecycle contradictions without creating another artifact owner. | Proposal review R4; architecture review R2 | Metadata, review-closeout, and final holistic review evidence |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| T01-T08, T12-T18 | Classification, resources, durable composition, closeout, claims, literal compatibility, size, and packaging remain closed. | contract/integration |
| T09-T11 | Reviewed basis, exact tail, partial retry, forbidden ancestry, and field ownership receive opposite outcomes. | integration |
| T19 | A real temporary Git repository executes `S -> R -> E -> verify` and preserves the pre-verify cutoff. | end-to-end |
| Lifecycle closeout | Proposal state, review records, and canonical architecture ownership are internally consistent. | governance validation |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `python scripts/test-skill-validator.py ExplainChangeSkillSimplificationTests` | 11 passed | final review `code-review-final-r4` |
| `python scripts/test-workflow-code-state.py` | 18 passed | final review `code-review-final-r4` |
| `python scripts/test-workflow-automation.py` | 76 passed | final review `code-review-final-r4` |
| `python scripts/build-skills.py --check` | passed | final review `code-review-final-r4` |
| Change metadata, review closeout, and full-diff whitespace checks | passed | final-review recording `ec4fca20` |
| Full skill, build, adapter, boundary, and documentation suites | previously passed on the implementation subject and selected for fresh final verify | reviewed subject `7a6dab80` |

## Review resolution summary

Four material findings have accepted and resolved dispositions, with zero unresolved findings: `EXCSIM-TSR1`, `EXCSIM-CR1`, `EXCSIM-CR2`, and `EXCSIM-CR3`. See [review-resolution.md](review-resolution.md) for the detailed records. Final review `code-review-final-r4` found no new material findings.

## Alternatives rejected

A flat inline rewrite would retain excessive common-path context. Multiple small references would increase routing and package drift. A single combined review/explanation commit would blur stage identity, while an explanation-only commit would leave formal review evidence uncommitted. A new transaction artifact, Git note, runtime generator, or Markdown-region parser would add persistence or ownership without solving a distinct first-version need.

## Scope control

The change does not add a model-runtime evaluator, prose grader, section-level refresh, generated skill source, new lifecycle state, new database or service, external integration, or target-agent acceptance run. Historical explanations are not migrated unless explicitly refreshed. The lifecycle corrections change no implementation, persistence, or mutation owner.

## Risks and follow-ups

The principal residual risk is future schema evolution adding legitimate workflow fields that are not in the closed stage manifests; such a change should fail closed and update the governing spec, validator, and tests together. EC3 remains deliberately close to the frozen byte ceiling at 8,218 versus 8,224 bytes, while its word count falls from 1,175 to 1,035; the deterministic measurement test must run after later shipped-text edits.

## Workflow handback

Explanation status: current
Explanation basis: sha256:c2e6112ee626470e1b1b28c50c3501c0376c8249a6a3a9e5ec749d59adfcd832
Validation-evidence cutoff: final-review-recording:ec4fca20ec5a21815c38d429b26107a1d1120a7c
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
