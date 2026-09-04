# M4 implementation evidence: Canonical compact contract

Milestone: M4
Subject path: `docs/plans/2026-09-03-compact-current-state-change-record.md`
Subject identity: `sha256:0c18ba75e3139f28415889279a453f2769b963dc37dd5d96da565fda2da7f67e`
Validation result: passed

## Result

- Skill: implement
- Status: M4 implementation complete and ready for Code Review
- Completed scope: canonical governance and workflow guidance; architecture and ADR integration; root and package documentation; bounded-projection guidance across lifecycle skills; compact review, decision, evidence, and Verify templates; Python schema parity; compact-aware review, lifecycle, automation-state, query, context, and validation-selection behavior; and shared cross-runtime fixtures
- Compatibility: registered historical contracts retain their readers and explicitly scoped round files, logs, resolution ledgers, Git-backed readiness, request artifacts, and PR progression; compact changes inherit none of those requirements
- Public activation: withheld until M5 proves supported-package parity, complete-change validation, activation behavior, and rollback
- Current dependency: approved Design Review R11, Delivery Review R8, and accepted M3 Code Review
- Claim limitations: this evidence does not claim compact activation, supported-adapter release parity, final verification, release, push, or pull-request readiness

## Test-first evidence

The M4 slice began with a canonical-contract regression test and a shared eight-record compact fixture consumed by both Python and Node validators. The first failures exposed missing current-contract ownership language, absent Python support for compact coordinator and review records, legacy-only query and state-store assumptions, and validation-selection catalog gaps. Implementation then aligned the canonical sources and extended existing validators and readers without activating the writer.

Code Review identified two remaining semantic conflicts after structural tests passed: Route introduced PR handoff as mandatory before distinguishing compact behavior, and Verify applied Git-backed branch readiness generically. Both are now explicitly historical-compatibility behavior; compact completion is established by successful Verify against exact current-set identities and any later PR is optional.

## Required validation results

- `python scripts/test-change-metadata-validator.py` — passed, 111 tests.
- `python scripts/test-review-artifact-validator.py` — passed, 113 tests.
- `python scripts/test-artifact-lifecycle-validator.py` — passed, 165 tests.
- `python scripts/test-workflow-automation-state.py` — passed, 71 tests.
- `python scripts/test-workflow-automation.py` — passed, 78 tests.
- `python scripts/test-skill-validator.py` — passed, 365 tests.
- `python scripts/validate-skills.py` — passed, 20 canonical skills.
- `python scripts/build-skills.py --check` — passed using temporary generated output.
- `python scripts/validate-guide-system.py` — passed.
- `python scripts/validate-documentation-prose.py --mode audit` — passed with zero errors and zero warnings.

## Supplemental validation results

- `python scripts/test-compact-current-state-canonical-contract.py` — passed, 4 tests.
- `python scripts/test-query-change-record.py` — passed, 27 tests.
- `python scripts/test-select-validation.py` — passed, 155 tests.
- `node --test packages/rigorloop/test/compact-contract.test.js` — passed, 17 tests.
- `npm test --prefix packages/rigorloop` — passed, 456 tests total: 454 passed and 2 historical skips.
- `python scripts/validate-governed-lifecycle-cli.py` — passed for 38 governed changes with three baseline warnings and no failures or activation errors.
- `python scripts/validate-npm-package.py` — passed.
- `git diff --check` — passed.

## Contract evidence

- The canonical compact set is one coordinator, stable current review records, conditional material-decision and current-evidence surfaces, and a success-only Verify report; engineering artifacts remain authoritative at their canonical paths.
- The CLI is consistently described as a deterministic validation and recoverable transaction boundary, never as a permission principal. Skills retain semantic responsibility and submit transient operations carrying expected revision and file identities.
- Adjacent authoring correction returns directly to its owning review. Explicit correction route and return remain available only for non-adjacent correction; return establishes review readiness, and exact review settlement alone clears the correction.
- Compact state, recovery, resumption, review, and completion do not rely on Git, a branch, PR access, network access, machine-local logs, or disposable procedural artifacts.
- Python and Node validators consume the same valid compact record fixture. New compact closed vocabularies reject unknown values, stable reviews reject round-suffixed paths and legacy ledgers, and optional decision or evidence surfaces are absent rather than empty.
- Historical fixtures remain readable, legacy mutations remain on their registered contract, the implementing change remains v3 through closeout, and compact writer activation remains withheld.

## Recovery

M4 canonical, skill, template, Python-validation, query, and selection changes can be reverted together while retaining the reviewed M1 model and M2/M3 CLI implementation. Because compact creation remains withheld, no governed compact record depends on this candidate consumer set.
