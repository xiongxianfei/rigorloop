# M1 Retirement-Ledger Evidence

## Scope

M1 freezes admission of new validation subsystems, inventories the current
selector catalog and its owning scripts, and records the exact prospective
R26 skill-contract disposition. It changes no acceptance command and removes
no validator, selector, cache, scheduler, fixture, or historical evidence.

## Test-first proof

`scripts/test-retirement-ledger.py` was added before its implementation and
initially failed with `ModuleNotFoundError: retirement_ledger`. The smallest
implementation is an importable module used by the regression test, not a new
standalone validator CLI.

## Inventory and decisions

- Selector catalog IDs inventoried: 44; each has exactly one ledger owner.
- Ledger owner groups: Gate A, Gate B, Gate C, governance, and public product.
- R26 prospective dispositions: 21 exact clause or clause-portion entries.
- Explicitly retained routing clauses: R35c and R35d.
- Explicitly retained deterministic parity includes R50a and R50b.
- Removal-eligible entries: 0. Every entry remains `inventoried` until its
  planned milestone supplies dual proof, exact active-contract disposition,
  and a rollback point.
- Selector, cache, scheduler/broad-smoke, prose/readability, and token-cost
  paths remain active or paused; M1 does not guess their later disposition.
- Historical prompt, transcript, clean-install, and behavior-parity evidence
  remains readable. It is not a prospective acceptance obligation for changes
  governed by the published-skill-first spec.

## Admission result

The default budget is zero new standalone validator CLIs, selector systems,
validation caches, and validation schedulers. The ledger schema is implemented
inside an existing validation-library surface. Contributor guidance routes
semantic skill quality to formal review.

## Validation

- `python scripts/test-retirement-ledger.py` — pass, 11 tests.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-08-10-published-skill-first-repository-simplification/retirement-ledger.yaml --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/workflows.md` — pass; two lifecycle-managed artifacts validated and non-governed paths safely ignored.
- `python scripts/test-skill-validator.py` — pass, 285 tests, 16 skipped.
- `python scripts/test-select-validation.py` — pass, 150 tests in 65.20 seconds.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml` — pass.
- `git diff --check` — pass.

## Rollback

Revert the single M1 commit. Because M1 removes no invocation or executable
owner, rollback cannot reduce current repository acceptance coverage.
