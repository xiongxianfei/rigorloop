# Explain Change: Proposal-Review Skill Simplification

## Summary

The change makes ordinary proposal review load less procedure while keeping the full review contract. `SKILL.md` remains self-sufficient for advisory judgment and universal safety; durable recording and specialized proposal gates now load only when their evidence predicates apply. Existing assets remain the structural output owners, and repository validators and adapter packaging now understand the complete package.

## Problem

The previous 2,295-word `SKILL.md` mixed ordinary advisory review with formal recording, lifecycle settlement, automated correction, vision exceptions, standing-artifact bootstrap, and broad scope-budget procedure. This made every invocation pay the full context cost and repeated output and settlement structures in multiple places.

## Decision trail

The accepted proposal selected a compact universal skill plus two conditional references and the existing assets. The specification closed recording and automation modes, specialized predicates, resource assemblies, output groups, failure behavior, semantic preservation, and package parity in R1-R37. The architecture assessment found no architecture change because the existing packaged-skill model already owns mapped references and assets. The plan implemented preservation inventories in M1, the package refactor in M2, and measurement plus package proof in M3.

## Diff rationale by area

| Area | Change | Reason | Contract and evidence |
| --- | --- | --- | --- |
| `skills/proposal-review/SKILL.md` | Shortened the universal path and added closed modes, predicates, assemblies, triggers, and fail-safe resource mapping. | Preserve direct advisory capability while avoiding unconditional formal and exceptional procedure. | R1-R8, R14-R28; M2; `evidence/m2-package-refactor.md` |
| Recording reference | Added change-root selection, durable recording, retry, formal settlement, and workflow-managed automation procedure. | Give durable side effects one conditional owner without granting authority merely by loading it. | R9-R13, R16-R17; MP1 |
| Conditional-gates reference | Added vision-exception, standing-artifact, scope-budget, composition, and ambiguity procedure. | Load detailed exceptional judgment only when review evidence activates a gate. | R18-R20, R22-R24 |
| Result asset | Added one core and four conditional structural groups. | Keep labels and repeated result structure in one asset without moving policy into it. | R25-R27 |
| Validator and tests | Allowed the two references, extended structural labels, and migrated consumers from literal `SKILL.md` assumptions to package owners. | Preserve package integrity while preventing tests from becoming accidental prose-policy owners. | R29-R31, R34-R37 |
| Change-local fixtures and ledgers | Added 21 semantic dispositions, 16 literal dependencies, 25 scenarios, and invalid closed-value fixtures. | Prove no significant rule or real compatibility dependency silently disappeared. | M1, CMD1, MP0 |
| Measurement and package evidence | Added per-resource and per-assembly words/bytes, semantic review, and generated/archive/install parity. | Distinguish ordinary context savings from total maintenance footprint and prove every supported adapter contains the package. | R32-R35, R37; M3, MP1 |

## Tests added or changed

The proposal-review package contract checks closed modes, assemblies, predicates, references, and structural result groups. Existing validator consumers now inspect the owning reference when procedure moved and preserve shared portability, evidence-access, vision, scope, isolation, settlement, and closed-vocabulary contracts. Static fixtures cover clean advisory, late recording, generated-root collision, formal manual and automated review, invalid mode pairs, each specialized gate, combined and late predicates, blocked output groups, missing resources, and package parity.

The test level remains deterministic because the contract concerns published text structure, ownership, routing, and packaging. No model runtime, prompt journey, transcript grading, semantic classifier, permanent size gate, or tokenizer dependency was added.

## Validation evidence available before final verify

- `python scripts/validate-skills.py skills/proposal-review/SKILL.md` passed.
- `python scripts/test-skill-validator.py` passed 311 tests with 16 skipped.
- `python scripts/test-build-skills.py` passed 7 tests.
- `python scripts/build-skills.py --check` passed.
- `python scripts/test-adapter-distribution.py` passed the adapter distribution suite.
- CMD7 built and clean-installed Codex, Claude, and opencode `v0.3.6` archives for `proposal-review` and passed Gate B.
- `python scripts/validate-boundary-first.py --check --path specs/proposal-review-skill-simplification.md` passed.
- Change metadata and review closeout validation passed.
- Hosted CI has not been observed; all evidence above is local.

## Review resolution summary

Seven material findings across proposal, test-spec, and implementation review have accepted and resolved dispositions in `review-resolution.md`. The implementation finding `PRRSIM-CR-M2-R1-001` identified validator-preserved duplicate placement and settlement prose. The correction kept one canonical placement statement and settlement section, migrated the incidental heading consumer, passed focused and full validation, and was independently closed by `code-review-m2-r2`. No open or `needs-decision` findings remain.

## Alternatives rejected

Editorial compression alone would leave conditional procedure in every invocation. One large reference would combine distinct recording and proposal-gate triggers. Many small references would increase navigation and ownership complexity. A generic review engine or target-runtime acceptance system would introduce new architecture and nondeterministic proof unrelated to the content refactor.

## Scope control

The change does not alter proposal status, severity, materiality, review readiness, lifecycle ownership, continuation authority, change metadata schema, runtime state, adapter model, or PR behavior. It does not add a new skill, selector, scheduler, service, persistence mechanism, permanent simplicity validator, or release action.

## Risks and follow-ups

`PRR0-core` decreases 10.2% in words and 9.5% in bytes, below the advisory 30-45% target. The total package grows 35.2% in words because conditional procedure and result applicability are explicit. This tradeoff is accepted by R33: further reduction must not hide universal portability, evidence, vision, scope, materiality, status, or safety contracts. Final verify still needs to rerun the named suite against the final reviewed branch and report hosted CI as unobserved.

## Verify readiness

All implementation milestones and the final holistic code review are closed, review resolution is closed, and this rationale describes the final reviewed diff. The change is eligible for governed final verification; branch readiness is not claimed here.
