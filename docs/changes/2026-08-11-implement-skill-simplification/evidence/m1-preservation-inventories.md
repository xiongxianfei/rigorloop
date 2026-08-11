# M1 Preservation Inventories

Milestone: M1
Date: 2026-08-11
Status: implementation-complete; review pending

## Scope

M1 records the current semantic rules, duplication clusters, exact-string consumers, invocation scenarios, negative closed-vocabulary fixtures, and profile-size baseline before canonical skill prose moves.

## Inventory audit

- The full 395-line baseline `skills/implement/SKILL.md` was read section by section.
- All 35 level-two heading markers, including repeated headings inside the two fenced output examples, were reconciled into 24 behaviorally significant rule rows; repeated result headings are owned by one asset row and the output blocks are counted as two complete inline structures.
- Exact consumers were inspected in `scripts/test-skill-validator.py`, `scripts/review_independence_skill_phrases.py`, skill validation, workflow/lifecycle specs, and adapter/package tests.
- Eighteen compatibility rows distinguish normative literals, parser/package contracts, incidental test coupling, and migration treatment.
- Repository search matches that merely name `skills/implement/SKILL.md` as a changed or validation surface are not literal consumers and are excluded from the literal ledger.
- No semantic rule is classified obsolete and no contract change is required.

## Deterministic fixture coverage

The scenario fixture contains exactly the eleven approved identities. Each record has non-empty required and forbidden outcomes. The two negative fixtures use values outside their closed vocabularies so CMD1 proves unknown values fail before destination or treatment consistency.

## Baseline integrity

The canonical package remains unchanged from commit `53df8ce2`:

- `SKILL.md`: `b7839e959175acc05b93d3a1f4c5c612e95fcd579eb9b02551f6be40c528a301`
- boundary reference: `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f`

## Aligned surfaces

- `skills/implement/`: unaffected with rationale; M1 must precede prose movement.
- `scripts/test-skill-validator.py`: unaffected with rationale; focused assertions belong to M2 after the inventories establish their required behavior.
- Adapter/package validation: unaffected with rationale; no mapped resource has changed yet.

## Handoff

M1 is ready for independent code review after CMD1, change-metadata validation, artifact lifecycle synchronization, and diff checks pass. This evidence does not close the milestone or claim downstream readiness.
