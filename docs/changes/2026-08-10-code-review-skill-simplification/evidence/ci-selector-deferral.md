# CI Selector Deferral Evidence

Stage: ci-maintenance
Date: 2026-08-11
Trigger: verify R1 selector-routing blocker `VR-CRSIM-002`

## Decision

The rule ledger and two acceptance fixtures remain one-change deterministic evidence with their approved paths and exact CMD1 and CMD11 proof.

They do not define a recurring evidence class, so the current change records a complete owner-approved unsupported deferral for each path instead of adding a code-review-specific registry entry or validator family.

The repository-maintainer owner is supported by the user's explicit instruction to refine the change until verification passes and the accepted proposal's requirement to keep these artifacts change-local.

## Selector maintenance

The existing selector already evaluates complete deferrals for immediate unregistered change-local evidence.

It now applies the same CRM-R17 through CRM-R19 mechanism to deterministic nested `change-local-unsupported` evidence.

Without a complete deferral, nested evidence continues to return blocking `manual-routing-required`.

With a complete deferral, the debt remains visible in `registration_debt` with `verify_readiness: owner-deferred` and does not silently acquire a validation route.

## Validation contract

- `python scripts/test-select-validation.py` owns selector regression proof.
- CMD1 remains the mandatory ledger and fixture proof.
- CMD11 remains the mandatory rule-cluster ownership and measurement proof.
- PR-mode selection must report no blocking results while retaining three visible owner-deferred debt records.
- PR-mode CI must execute every selected check successfully.

## Scope

No workflow file, check catalog entry, evidence-class registry entry, target runtime, permanent simplicity validator, or broad fixture route was added.

## Implementation evidence

- The new nested complete-deferral regression failed before the selector change and passed afterward.
- `python scripts/test-select-validation.py` passed 153 tests.
- Explicit selection of the ledger and two fixtures returned `status: ok`, no blocking results, and three visible `owner-deferred` registration-debt records.
- The full selector suite exposed a missing `selected checks` phrase in the simplified `code-review` contract; the smallest wording correction restored that governed semantic and exact measurements were refreshed in `simplification-measurements-r2.md`.
