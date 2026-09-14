# Token-cost feature retirement

## Purpose / big picture

Remove the inconclusive token-cost measurement/reporting subsystem and its qualification dependencies. Preserve useful source-safety, output-contract and release protection without maintaining token-only fixtures or fake passing checks.

## Current Handoff Summary

- Owning change record: [repository cleanup](../changes/2026-09-13-current-design-repository-cleanup/change.json).

Mutable work and review state lives in the owning record; this plan covers the token-cost slice only.

## Source artifacts

- Direction: explicit user request to retire the inconclusive feature.
- Design: [Validation VAL-SR-25 and VAL-DEC-08](../design/engineering/validation.md#token-cost-feature-retirement), linked Skill, Engineering, Packaging and Release sections.
- Prior-contract test specs: token-only obligations superseded by VAL-SR-25; independently useful source safety and current CLI/release contracts remain applicable.

## Context and orientation

Validation selection schedules token commands. Adapter qualification loads the report validator and constructs runtime benchmark context; release-verify carries a historical report gate. Token tools own exclusive report, benchmark and session fixtures. Some adapter safety tests use token reports incidentally. Current CLI tests independently cover result shape, omissions and failure behavior; the frozen byte-profile wrapper already rejects measurement execution.

## Non-goals

No retirement of CLI result contracts, source safety, ordinary test runtime reporting, required review or publication permissions. No unrelated cleanup implementation or claim that the entire cleanup branch is complete. No external benchmark execution or publication.

## Requirements covered

VAL-SR-25 and VAL-DEC-08; preserved VAL-SR-03–05/17/24, Skill SKL-SR-07, Packaging candidate integrity and Release qualification boundaries.

## Milestones

### TOKEN-1 — Remove producers and consumers coherently

- Kind: implementation.
- Goal: supported authoring, validation and qualification require no token artifacts.
- Scope: token tools and tests, including `packages/rigorloop/test/helpers/record-store-tokenize.py` and token-measurement exports/entry point in `record-store-interactions.mjs`; token fixture/report/benchmark trees; selector/catalog rules; adapter qualification and incidental fixtures; release wrapper gate; current documentation references.
- Dependencies: independent approval of the scoped Design and this Delivery package.
- Implementation: establish retained consumer failure/success assertions first; remove token-only tests and branches; reconcile consumers; preserve shared helpers only for demonstrated retained readers; remove exclusive files with Git provenance; repair live references.
- Completion: no retained entry point invokes removed tools, no fake token result, no mandatory token artifact; retained invalid source/candidate checks still reject and valid candidates pass without token reports.
- TG-TOKEN: selector tests demonstrate deleted paths reach retained consumer checks without removed IDs; adapter tests demonstrate source-safety failures and qualification without reports; release tests and wrapper syntax preserve qualification and early failure.
- Commands: `python scripts/test-select-validation.py`; `python scripts/test-adapter-distribution.py`; `python scripts/test-release-transaction.py`; `python scripts/test-skill-validator.py`; `npm test --prefix packages/rigorloop`; `bash -n scripts/release-verify.sh`; selected repository wrapper validation after inspecting its scope; `git diff --check`.
- Evidence: exact slice diff and removals, source identities/patches, retained-test disposition, actual commands/results, independent review.
- Recovery: restore producer and consumers together from the captured pre-slice snapshot/Git; do not revert unrelated accumulated user work or manufacture passing checks.

## Final review checkpoint

Kind: lifecycle-closeout. After TOKEN-1 and required corrections, independently review the complete token-retirement delta and its interactions, then conduct distinct scoped Verify. This does not approve the wider accumulated cleanup diff. Any wider cleanup closure still requires its own full review and Verify.

## Change-level verification

TG-TOKEN-INTEGRATED covers VAL-SR-25: no report generation/agent execution through retained entry points; valid supported qualification without token files; invalid source/candidate still rejects; deleted paths cannot select removed commands; current CLI result tests remain intact. Reconcile live imports, shell calls, docs and fixtures; historical records retain original bytes and meaning.

## Risks and recovery

Token report parsing is imported by adapter qualification; remove that dependency before deleting the module. Historical fixture use can hide source-safety coverage; retain the same negative observations with independent setup. Preserve uncommitted report/source bytes before removal. Broad legacy documentation references are historical unless current commands or reliance remain; do not rewrite judgments.

## Dependencies

Use current selector/executor and supported package tooling. M4 is included in full feature retirement. No runtime benchmark or external service is needed.

## Decision log

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-09-13 | One producer/consumer implementation milestone | Intermediate tool removal would break selector, adapter and release consumers. |
