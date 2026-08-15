# M2 Proposal Package Implementation

## Scope completed

M2 replaces the monolithic proposal procedure with a compact universal `SKILL.md`, two conditional references, and one structural skeleton. It also extends the validator allowlist for the approved resources, migrates coupled assertions to their owners, and adds six focused tests.

## Tests first

`ProposalSkillSimplificationTests` was added before the package resources. Its first run discovered six tests and failed five with one setup error because the reference directory, assembly vocabulary, operation contracts, reset procedure, and conditional groups did not yet exist. After the atomic package change, all six tests passed.

## Contract result

- Exactly four assemblies are declared: `PA0-portable`, `PA0G-portable-gated`, `PA1-governed`, and `PA1G-governed-gated`.
- Portable operations use exact file state and write only the proposal artifact.
- Governed candidate selection is separate from reference-owned mutation authority.
- Governed create, revise, retry, downstream-reliance, and authorized stale-reset behavior has one owner.
- The four strategic predicates are closed, independent semantic judgments and load one reference once.
- The skeleton owns the universal structure and four independent conditional groups without owning policy.
- Required-resource defects stop dependent work without reconstruction.
- Existing exact literals and universal evidence, vision, readability, claim, and handoff contracts remain covered.

## Loaded-profile check

The pre-refactor baseline was 2,122 words and 14,796 UTF-8 bytes for every assembly. The first implementation reduced every word total but left PA1G at 15,913 bytes; code review recorded `PRSIM-M2-CR1`. Corrected procedural totals are PA0 1,092 words/8,435 bytes, PA0G 1,440/11,253, PA1 1,473/11,468, and PA1G 1,821/14,286. Every assembly is below both baselines. Exact LF-normalized identities remain owned by M3.

## Accepted correction PRSIM-M2-CR1

Repeated summaries were tightened only in the three procedural owners. No rule, literal, asset group, validator behavior, operation, authority boundary, failure result, or handoff changed. CMD2-CMD4 pass after the correction, and the context-reset rereview must confirm the final byte and word totals.

## Validation

- CMD2 `validate-skills`: passed.
- CMD3 focused test class: six tests passed.
- CMD4 full skill-validator suite: 342 tests passed with 16 documented skips.
- CMD5 build-skill tests: seven tests passed.
- CMD6 generated-skill check: passed.
- CMD9 boundary-first validation: passed for the approved spec.
- CMD10 change metadata validation: passed.
- CMD11 review artifact structure validation: passed.
- `git diff --check`: passed.

## Handoff

M2 is implementation-complete and ready for formal milestone code review. This evidence does not claim M2 closure, M3 package parity, final holistic review, verification, branch readiness, or PR readiness.
