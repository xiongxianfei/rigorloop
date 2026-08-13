# CI Selector Deferral Evidence

Stage: ci-maintenance
Date: 2026-08-13
Trigger: final PR-mode selector returned five `manual-routing-required` blockers

## Decision

The semantic ledger, literal ledger, scenario inventory, and two negative fixtures remain one-change deterministic evidence with exact approved T1-T12, CMD1, and MP1 proof. They do not define recurring evidence classes.

The repository maintainer defers registration for each exact path instead of adding a plan-review-specific registry entry, selector branch, validator family, or broad fixture route. This preserves the approved non-goals against permanent simplicity infrastructure and target-runtime acceptance.

## Validation contract

- T1, T12, and CMD1 remain mandatory for both ledgers and both negative fixtures.
- T2-T10 retain the scenario, lifecycle, resource, and asset proof.
- MP1 remains the independent semantic-completeness check.
- PR-mode selection must retain five visible `owner-deferred` debts and return no blocking result.
- PR-mode CI and broad smoke must pass.

## Scope

No workflow file, check catalog, evidence-class registry, selector code, validator family, target runtime, or broad-smoke policy changed. The deferrals apply only to the five named paths.

## Result

- Skill: ci-maintenance
- Status: updated
- Workflow file: not applicable
- PR checks: existing selector and CI commands unchanged
- Boundary checks: existing broad smoke unchanged
- Risk coverage: exact-path deferrals retain direct approved proof
- Open blockers: selector rerun and focused review
- Next stage: code-review
