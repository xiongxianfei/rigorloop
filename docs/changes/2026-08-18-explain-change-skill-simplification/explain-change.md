<!-- explain-change-skeleton-v1; normative -->

# Change explanation: Explain-Change Skill Simplification

Stage: explain-change
Status: current
Final diff identity: sha256:0d0f28d0862ce92efdab207de51ec381bca351777b231bf50063de3504915f41
Final review identity: sha256:da3229e506d461057d53cda6872b66f7f4cbe697bf9628837b5bc8b59f963bed
Reviewed subject revision: 8727f39fb03efb0d2cf0002a3e191de4a5c45c0c
Base revision: 11179cb7f91a4a149bd763bae6a3dfbbadb3f60f
Final-review recording revision: f61d9a9d5d21fe360ebabae84e93bb30cd21bb2d

## Summary

The explain-change skill now loads a compact universal contract for ordinary rationale work, one governed-workflow reference only when change-local authority applies, and one skeleton only for durable output. The implementation also makes the final review, explanation, and verify sequence executable: Git derives the reviewed subject `S`, final-review commit `R`, explanation commit `E`, and handoff separately while verification rejects reordered, broader, destructive, or ambiguous evidence tails.

The verification correction restores the universal material-finding summary contract in the shipped root skill. It requires a concise `review-resolution.md` link without duplicating transcript detail, while the conditional governed reference continues to own lifecycle closeout procedure.

## Problem

The former flat skill mixed universal diff explanation with governed lifecycle procedure and repeated durable layout, so small requests loaded irrelevant material. Its first simplified final-review rule then allowed only one explanation commit after the reviewed subject, which could not also preserve the formal final-review evidence required before explain-change. The initial implementation also compressed away parser- and workflow-consumed review-resolution wording, which the first verification correctly rejected.

## Decision trail

- The accepted proposal chose a compact `SKILL.md`, one governed reference, one copied skeleton, and no runtime generator.
- Spec R1-R44 defines portable/governed classification, whole-file durable output, workflow handback, exact `S -> R -> E` evidence ordering, and literal preservation.
- ADR-20260818 keeps the reviewed product identity base-to-`S`, derives later commit identities from Git, and reuses the existing change record and evidence owners.
- Plan M1-M4 separates preservation inventory, package extraction, package-chain proof, and ordered-tail implementation.
- Verification finding `EXCSIM-VERIFY-1` required restoration of the exact cross-skill review-resolution contract; commit `8727f39f` implemented it and final review `code-review-final-r3` found no material defect.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/explain-change/` | Replaced the flat procedure with a compact root, governed reference, and structural skeleton; restored concise review-resolution summary wording in the root. | Reduce all four loaded assemblies without weakening universal truthfulness, claims, or cross-skill literals. | R1-R21, R30-R44 | 11 `ExplainChangeSkillSimplificationTests`; M1-M3 evidence |
| `scripts/workflow_code_state.py` | Derives `S`, `R`, `E`, handoff, exact paths, semantic fields, and append-only shared-list deltas. | Make final-review reuse executable and prevent path-only lifecycle bypass. | R22-R29; ADR-20260818 | 18 real-Git code-state tests; M4 evidence |
| `scripts/workflow_automation.py` | Requires the complete ordered tail before verify readiness. | Keep partial `S -> R` recoverable for explain-change but ineligible for verify. | R26-R29 | 76 workflow-automation tests |
| Specs, architecture, plan, and test spec | Record the package boundary, identity model, recovery, and proof map. | Keep observable behavior, design ownership, execution, and validation traceable. | Approved lifecycle artifacts | Spec, architecture, plan, and test-spec reviews |
| Fixtures, validators, and preservation evidence | Cover classifications, resource assemblies, size gates, stage order, unknown fields, destructive lists, required review-resolution literals, and package parity. | Prove the simplified context and fail-closed compatibility boundaries. | R36-R44 | 419 skill tests; 103 review-artifact tests; 150 adapter tests |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| T01-T08, T12-T18 | Classification, resources, durable composition, closeout, claims, literal compatibility, size, and packaging remain closed. | contract/integration |
| T09-T11 | Reviewed basis, exact tail, partial retry, forbidden ancestry, and field ownership receive opposite outcomes. | integration |
| T19 | A real temporary Git repository executes `S -> R -> E -> verify` and preserves the pre-verify cutoff. | end-to-end |
| Verification regression | The canonical root contains `review-resolution.md`, `concise`, and `duplicate transcript`, and the broad review contract consumes them successfully. | focused regression |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `python scripts/test-skill-validator.py ExplainChangeSkillSimplificationTests` | 11 passed | final review `code-review-final-r3` |
| `python scripts/test-review-artifact-validator.py` | 103 passed | final review `code-review-final-r3` |
| `python scripts/test-workflow-code-state.py` | 18 passed | final review `code-review-final-r3` |
| `python scripts/validate-skills.py skills/explain-change/SKILL.md` and `python scripts/build-skills.py --check` | passed | final review `code-review-final-r3` |
| Full skill, build, and adapter suites | 419 skill tests with 16 documented skips, seven build tests, and 150 adapter tests passed | reviewed subject `8727f39f` |
| Change metadata, review closeout, documentation prose, and full-diff whitespace checks | passed; prose audit emitted only deliberate metadata-line warnings | final-review recording `f61d9a9d` |

## Review resolution summary

Four material findings have accepted and resolved dispositions, with zero unresolved findings: `EXCSIM-TSR1`, `EXCSIM-CR1`, `EXCSIM-CR2`, and `EXCSIM-CR3`. See [review-resolution.md](review-resolution.md) for the detailed records. Final review `code-review-final-r3` found no new material findings.

## Alternatives rejected

A flat inline rewrite would retain excessive common-path context. Multiple small references would increase routing and package drift. A single combined review/explanation commit would blur stage identity, while an explanation-only commit would leave formal review evidence uncommitted. A new transaction artifact, Git note, runtime generator, or Markdown-region parser would add persistence or ownership without solving a distinct first-version need.

## Scope control

The change does not add a model-runtime evaluator, prose grader, section-level refresh, generated skill source, new lifecycle state, new database or service, external integration, or target-agent acceptance run. Historical explanations are not migrated unless explicitly refreshed. The verification correction changes no lifecycle, architecture, persistence, or mutation owner.

## Risks and follow-ups

The principal residual risk is future schema evolution adding legitimate workflow fields that are not in the closed stage manifests; such a change should fail closed and update the governing spec, validator, and tests together. EC3 remains deliberately close to the frozen byte ceiling at 8,218 versus 8,224 bytes, while its word count falls from 1,175 to 1,035; the deterministic measurement test must run after later shipped-text edits.

## Workflow handback

Explanation status: current
Explanation basis: sha256:e1b1a17f9996a79a0ed1242c614f87932a33249021e9ba97b916f2391471f096
Validation-evidence cutoff: final-review-recording:f61d9a9d5d21fe360ebabae84e93bb30cd21bb2d
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
