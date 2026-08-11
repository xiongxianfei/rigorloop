# M2 verify package refactor evidence

## Scope

M2 replaces the monolithic `verify` common path with a self-sufficient universal contract and one conditionally loaded final-readiness procedure.

Changed package surfaces:

- `skills/verify/SKILL.md`
- `skills/verify/references/branch-readiness-verification.md`
- focused contract assertions in `scripts/test-skill-validator.py`

The existing boundary-first reference remains byte-identical at SHA-256 `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f`.

## Test-first evidence

Before the package edit, `python scripts/test-skill-validator.py VerifySkillSimplificationContractTests` ran five focused tests and failed four with one error because the new outcomes, profiles, fail-safe wording, and branch-readiness reference did not yet exist.

After implementation, the same five tests pass. The full skill-validator suite passes 302 tests with 16 intentional skips.

## Contract result

- Closed outcomes: `scoped-verification`, `branch-readiness`, and `workflow-final-verification`.
- Closed loaded-package profiles: `VP0-scoped`, `VP0B-scoped-boundary`, `VP1-final-readiness`, and `VP1B-final-readiness-boundary`.
- Execution authority remains independently classified as `isolated` or `governed-final`.
- Universal item-level evidence truthfulness, claim boundaries, external-action limits, review closeout, and missing-resource stops remain inline.
- The new reference owns only final evidence applicability, completeness, aggregation, verdict calculation, and mode-specific completion.
- A missing triggered reference stops dependent work; an untriggered reference neither loads nor blocks.

## Validation

| Command | Result | Important output |
| --- | --- | --- |
| `python scripts/test-skill-validator.py VerifySkillSimplificationContractTests` before implementation | expected fail | 5 tests: 4 failures and 1 missing-reference error |
| `python scripts/test-skill-validator.py VerifySkillSimplificationContractTests` after implementation | pass | 5 tests passed |
| `python scripts/validate-skills.py skills/verify/SKILL.md` | pass | canonical verify skill validated |
| `python scripts/test-skill-validator.py` | pass | 302 tests passed; 16 skipped |
| `python scripts/test-build-skills.py` | pass | 7 tests passed; generated resource inventory valid |
| `python scripts/build-skills.py --check` | pass | temporary generated skill tree validated |
| `git diff --check` | pass | no whitespace errors |

All commands ran from the repository root. No target-agent runtime, network action, publication action, or tracked generated adapter edit occurred.
