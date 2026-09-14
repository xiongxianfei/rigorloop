# Historical retirement-ledger removal

## Purpose / big picture

Remove the obsolete ledger subsystem and its current validation dependencies while retaining checks of supported behavior.

## Current Handoff Summary

- Owning change record: [repository cleanup](../changes/2026-09-13-current-design-repository-cleanup/change.json).

Mutable lifecycle state lives only in the owning record. This plan covers the ledger slice of VAL-SR-23.

## Source artifacts

- Direction: the user's selected next cleanup batch, within the existing repository cleanup.
- Design: [Validation historical check retirement](../design/engineering/validation.md#historical-check-retirement), VAL-SR-23, and [System consolidation map](../design/system.md#necessary-design-consolidation-map).
- Prior-contract test spec: published-skill-first repository simplification retains non-ledger obligations; ledger-specific prescriptions are superseded by the selected Design. Historical IDs and judgments remain unchanged.

## Context and orientation

The ledger library is read only by its dedicated test. The test validates the August 10 frozen ledger's private schema, historical catalog and transition narrative. The selector still schedules that test through a main catalog entry and retirement/archive routes. Current record-retirement and metadata checks independently protect supported storage boundaries. Inspect source directly: the project map is not relied on for this inventory.

## Non-goals

No spec-read-log retirement, broader fixture cleanup, new ledger, replacement parser, alteration of historical judgments or claim of whole-cleanup completion. No runtime, package or release behavior changes beyond removing this obsolete check dependency.

## Requirements covered

VAL-SR-23 ledger portion maps to LEDGER-1 / TG-LEDGER. Retain VAL-SR-03–05/13 and TEST-SR-07–10/12 through current selection, unknown-vocabulary rejection and protection-preserving maintenance.

## Milestones

### LEDGER-1. Remove ledger producers and consumers

- Milestone kind: implementation.
- Engineering purpose: retire the library, exclusive test/data and scheduling atomically.
- Architecture responsibility: Engineering Validation catalog and existing executor; System historical-source disposition.
- Dependencies: exact scoped Design and Delivery reviews.
- Implementation scope: remove `scripts/retirement_ledger.py`, `scripts/test-retirement-ledger.py` and `docs/changes/2026-08-10-published-skill-first-repository-simplification/retirement-ledger.json`; reconcile `scripts/validation_selection.py`, `scripts/test-select-validation.py` and live ledger-only test-spec reliance.
- Required verification: TG-LEDGER proves removed catalog IDs cannot execute, deleted paths select retained checks, main composition remains valid, archival exclusion/current rejection and unknown-vocabulary failures retain their assertions.
- Implementation steps: capture Git identities and uncommitted bytes; establish expected selector proof first; remove producers and catalog/fingerprint/routes together; retain current record-retirement/metadata checks; reconcile current references.
- Evidence expectations: exact removal provenance, scoped working-tree delta, useful-proof disposition and actual command outcomes.
- Completion criteria: no live consumer imports or schedules the removed library/test; no fake pass; removed paths still get meaningful consumer checks; retained negative proof passes.
- Review handoff: independent fresh review of the entire ledger delta, including interaction with previous token retirement.
- Recovery: restore this coherent unit from the pre-slice snapshot and Git without reverting unrelated accumulated cleanup.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: LEDGER-1 implementation and required corrections complete.
- Assessment: fresh independent whole-slice Code Review, followed by distinct scoped Verify.
- Evidence: exact subjects, reviewer independence, finding dispositions and actual checks.

The wider cleanup still needs its own whole-change review and final Verify.

## Change-level verification

TG-LEDGER-INTEGRATED uses the existing selector/executor wrapper to show archived and deleted paths schedule retained proof without invoking the removed command. Full selector and executor suites protect mode composition and closed vocabularies; record-retirement and metadata checks exercise actual rejection/archival boundaries. No separate broad runtime suite is needed because product/runtime/package sources are unchanged.

## Validation plan

- `python scripts/test-select-validation.py`: current catalog, routing, deleted paths, main composition and unknown-value proof.
- `python scripts/test-validation-execution.py`: actual executor and composed mode protection.
- `bash scripts/ci.sh --mode explicit --path scripts/retirement_ledger.py --path scripts/test-retirement-ledger.py --path docs/changes/2026-08-10-published-skill-first-repository-simplification/retirement-ledger.json --jobs 4`: retained record-retirement and metadata boundary proof through the real wrapper.
- `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-14-retirement-ledger-removal.md --path specs/published-skill-first-repository-simplification.test.md`: touched prose.
- `node scripts/validate-record-store.mjs docs/changes/2026-09-13-current-design-repository-cleanup/change.json` and `git diff --check`: record integrity and whitespace.

## Risks and recovery

Historical-only assertions must not be mistaken for required current proof. Retain meaningful catalog checks in the existing selector suite and current malformed-input/record-retirement tests. Preserve the original ledger and any local edits through exact Git provenance and patches before deletion. Restore consumers and producers together if needed.

## Dependencies

Use the existing catalog and executor. This is a scoped cleanup delivery inside an accumulated working-tree change; final branch integration is separate.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-14 | One ledger-only implementation slice | Its exclusive producer and consumers form one small recoverable unit. | Bundling unrelated legacy fixtures or retaining a synthetic passing ledger check. |

## Readiness

See the owning change record for workflow state.
