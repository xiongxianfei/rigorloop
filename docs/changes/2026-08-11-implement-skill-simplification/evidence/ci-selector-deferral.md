# CI Selector Deferral Evidence

Stage: ci-maintenance
Date: 2026-08-11
Trigger: final verify selector returned five `manual-routing-required` blockers

## Decision

The semantic ledger, literal ledger, and three static fixtures remain one-change deterministic evidence with exact approved CMD1 and MP0/MP1 proof. They do not define recurring evidence classes.

The change therefore records a complete repository-maintainer deferral for each exact path instead of adding an implement-specific registry entry, selector branch, validator family, or broad fixture route. This follows the repository's existing owner-deferral contract and the approved non-goal against permanent simplicity infrastructure.

## Validation contract

- CMD1 remains mandatory for both ledgers and all three fixtures.
- MP0 and MP1 remain the semantic completeness checks.
- Existing focused consumer assertions remain mandatory for migrated literal owners.
- PR-mode selection must retain five visible `owner-deferred` registration-debt records and return no blocking result.
- PR-mode CI must execute every selected check successfully.

## Scope

No workflow file, check catalog, evidence-class registry, selector code, test, target runtime, permanent simplicity validator, or broad-smoke policy changed. The deferrals apply only to the five named paths and cannot match other evidence.

## Handoff

CI maintenance has recorded routing ownership only. Validation execution and branch-ready judgment remain owned by `verify`.
