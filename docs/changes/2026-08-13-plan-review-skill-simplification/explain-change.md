# Why the Plan-Review Skill Changed

## Summary

The change makes ordinary plan review shorter without weakening formal recording or the reviewed-plan settlement transaction. Universal judgment remains in `SKILL.md`; governed candidate validation and settlement retry load only when governed evidence exists; two assets own repeated result and finding structure.

## Problem

The former 1,877-word common path loaded portable judgment, governed lifecycle mutation, automation details, and inline output structure together. This made every review pay for conditional procedure, duplicated ownership, and made retry semantics harder to audit.

## Decision trail

The accepted proposal selected one governed reference plus the existing boundary reference and two structural assets. Proposal review required an exhaustive transaction state machine, separate semantic judgment from transaction output, and one deterministic retained-evidence final state. The approved spec encoded these as R1-R55; the plan implemented preservation inventories in M1, the package boundary in M2, and measurement and package parity in M3. The architecture assessment concluded `architecture-not-required` because existing package and lifecycle ownership did not change.

## Diff rationale by area

| Area | Change | Reason | Contract and proof |
| --- | --- | --- | --- |
| `skills/plan-review/SKILL.md` | Shortened the universal path while retaining judgment, recording, evidence, boundary, stop, claim, and handoff rules. | Portable review must remain self-sufficient and safe. | R1-R3, R18-R26, R37-R46; T2, T4, T10. |
| Governed reference | Added candidate validation, initial-review mapping, exact settlement retry, recovery, and workflow-managed procedure. | Governed mutation has a real conditional authority boundary and must not be inferred from loading. | R4-R17, R27-R36; T3-T8. |
| Result asset | Added universal operation and recording groups plus conditional judgment, settlement, boundary, and automation groups. | Transaction execution must not manufacture a semantic status, and repeated labels need one owner. | R42-R47; T9. |
| Finding asset | Added the standard review-family finding block. | Every material finding must have one byte-consistent structural owner. | R18, R43; T11. |
| Validator tests | Added profile, vocabulary, transaction, asset, authority, and inventory assertions; migrated incidental inline-output consumers to assets/references. | Prove the new ownership model without freezing obsolete prose. | R48-R55; T1-T12. |
| Change-local evidence | Added ledgers, static scenarios, measurements, semantic review, package proof, and milestone reviews. | Demonstrate no rule disappeared and distinguish relocation from deletion. | R48-R55; MP1-MP4. |

## Tests added or changed

`PlanReviewSkillSimplificationContractTests` proves the four profiles, closed vocabularies, governed retry contract, final-verify authority checks, structural-only assets, review-family finding parity, and fail-closed inventories. Existing review-family, lifecycle, boundary, readability, package, and adapter tests continue to enforce shared behavior. Static fixtures cover all 23 required lifecycle and failure scenarios; no target-agent runtime was used.

## Validation evidence available before final verify

- `python scripts/test-skill-validator.py`: 324 tests passed; 16 skipped.
- `python scripts/test-build-skills.py`: 7 tests passed.
- `python scripts/build-skills.py --check`: passed.
- `python scripts/validate-skills.py skills/plan-review/SKILL.md`: passed.
- `python scripts/validate-boundary-first.py --check --path specs/plan-review-skill-simplification.md`: passed.
- `python scripts/test-adapter-distribution.py`: 150 tests passed.
- Temporary `v0.1.5` adapter build and selected clean-install validation for `plan-review`: passed.
- Change metadata and review-artifact structure validation: passed.

Hosted CI status is not yet claimed; final verify still owns readiness.

## Review resolution summary

Six proposal-review findings were accepted and closed across two revision rounds. They established the initial/retry state machine, separated transaction and judgment output, retained basis evidence, added the universal recording group, closed result paths, and kept assets structural. All later proposal, spec, plan, test-spec, milestone, and final code reviews are clean. See [review-resolution.md](review-resolution.md).

## Alternatives rejected

Inline-only compression could not remove conditional governed procedure from portable loading. Asset-only extraction left transaction policy mixed into the common path. Multiple small references fragmented one transaction. A new executable review engine or target-runtime test system would expand architecture and nondeterministic acceptance beyond the problem.

## Scope control

The change adds no runtime, scheduler, state store, lifecycle owner, new validator family, tokenizer dependency, permanent size gate, or target-agent acceptance. It does not alter the existing boundary projection or authorize plan-review to initialize `planned_work`, edit plans, advance workflow, or open PRs.

## Risks and follow-ups

The total package grows because conditional procedure and structural assets are packaged explicitly. This is acceptable and disclosed: portable loading falls 25.4% by words, governed loading falls 7.9%, while total package words grow 5.3%. Future edits must keep the common path and governed reference from duplicating ownership. No follow-up is required before final verify.

## Verify readiness

All implementation milestones and required reviews are closed, material findings are resolved, and durable rationale now exists. The change is eligible for formal `verify`; branch readiness and PR readiness are not yet claimed.
