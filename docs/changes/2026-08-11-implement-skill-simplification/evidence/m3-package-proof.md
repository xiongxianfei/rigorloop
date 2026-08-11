# M3 Profile and Package Proof

Milestone: M3
Date: 2026-08-11
Implementation owner: Codex implement context

## Result

The simplified implement package passes canonical, generated, archive, and temporary installed-tree validation. Profile measurements show material isolated and planned reductions, with a small justified armed-profile increase. Acceptance used repository-owned deterministic proof and independent semantic review only.

## Validation results

| Command | Result |
| --- | --- |
| CMD1 ledger and fixture proof | pass; 24 rules, 18 literals, eleven scenarios, unknown values rejected |
| CMD2 `validate-skills.py` | pass; one canonical implement skill and mapped resources validated |
| CMD3 `test-skill-validator.py` | pass; 291 tests, 16 skipped |
| CMD4 `test-build-skills.py` | pass; 7 tests |
| CMD5 `build-skills.py --check` | pass; temporary generated tree validated |
| CMD6 `test-adapter-distribution.py` | pass; 150 tests in 341.547 seconds |
| Original CMD7 synthetic version | expected fail-closed; archives built, all clean installs stopped before mutation with `metadata-trust-root-unavailable` |
| Revised CMD7 trusted `v0.3.6` | pass; Codex, Claude, and opencode archives and clean installed `implement` resources validated |
| CMD8 boundary-first validation | pass; active snapshot and trusted rollback artifacts validated |
| CMD9 change metadata | pass at each M3 handoff |
| CMD10 review artifacts | pass at each formal review handoff |

## Package integrity

The canonical package contains `SKILL.md`, the unchanged boundary reference, two mapped conditional references, and one mapped result asset. Temporary generation and adapter validation prove required inventory and byte parity without editing tracked generated bodies. The trusted command owns and removes its temporary directory.

## Failure and recovery proof

The synthetic fixture failure did not mutate an install target. The test-spec owner replaced only the invalid fixture identity with trusted immutable `v0.3.6`; independent test-spec-review R2 approved that correction before the positive command ran. No product behavior, validator family, network access, publication step, or target-agent runtime was introduced.

Rollback remains atomic: restore the pre-change canonical implement package and its pre-M2 consumer assertions, then regenerate derived packages through existing owners.

## Handoff

M3 is ready for independent code review. Final explain-change, holistic review, verification, branch, and PR readiness remain unclaimed.
