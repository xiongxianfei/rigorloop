# M1 implementation evidence: Compact authoritative model

Milestone: M1
Subject path: `docs/plans/2026-09-03-compact-current-state-change-record.md`
Subject identity: `sha256:6a27b852d9e803c3e226d8e01aed413a612f340e815da397ec333702f6f7149c`
Validation result: passed

## Result

- Skill: implement
- Status: M1 R2 correction complete and handed to Code Review
- Completed scope: eight closed schema identities and vocabularies; safe compact YAML and Markdown-front-matter parsing; reusable, surface, operation, result, and recovery validation; exact whole-set lifecycle identity; complete-set reference validation; byte-accurate limits; JSON Schema payload closure; and bounded attributable read-only projections
- Writer activation: withheld; no public compact mutation or creation command exists
- Corrected findings: `CCSR-M1-CR1` through `CCSR-M1-CR5`
- Review dependency: Design Review R4 and Delivery Review R4 are current and settled
- Next stage: Code Review M1 R3
- Claim limitations: this evidence does not claim Code Review acceptance, transaction writing, public compact CLI readiness, final verification, release, or external readiness

## Test-first evidence

The focused baseline originally failed because the compact contract and projection modules did not exist. Code Review R1 then produced direct failing vectors for the three missing Projection identities, UTF-8 multibyte overflow, all eight surface schemas, all fifteen operation payload variants, result-kind contradictions, absent lifecycle-contract identity, and JSON Schema closure. Each failed against the pre-correction implementation and now passes.

## Validation results

- `node --test packages/rigorloop/test/compact-contract.test.js packages/rigorloop/test/compact-projection.test.js` — passed, 19 tests.
- `npm test --prefix packages/rigorloop` — passed, 395 tests and 2 historical skips.
- `node --test packages/rigorloop/test/lifecycle-correction-route.test.js` — passed, 13 tests and 2 historical skips.
- `python scripts/test-change-metadata-validator.py` — passed, 107 tests.
- `python scripts/validate-boundary-first.py --check --path specs/compact-current-state-change-record.md` — passed.
- Draft 2020-12 metaschema validation of `schemas/compact-current-state-v1.schema.json` — passed.
- `python scripts/validate-documentation-prose.py --mode audit --path docs/plans/2026-09-03-compact-current-state-change-record.md` — passed with zero errors and warnings.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-09-03-compact-current-state-change-record` — passed before finding closeout.
- `git diff --check` — passed.

## Boundary and compatibility evidence

- Closed vocabulary validation precedes record-specific consistency validation, and every new vocabulary has an `unknown_value` regression.
- YAML aliases, anchors, merges, custom tags, duplicate keys, multiple documents, and non-finite numbers use the existing fail-closed lifecycle parser.
- Text and path limits use UTF-8 byte length. Candidate inline content and whole documents retain the 8 MiB bound.
- Every Projection carries `change_id`, `lifecycle_contract`, and `lifecycle_revision`; invalid or missing identities fail closed.
- The executable validator and JSON Schema close all fifteen operation payload variants and the three candidate-file partitions.
- Read-only projection success rejects mutation revisions, affected paths, changed bytes, non-success status, and mismatched result change identity.
- The lifecycle revision vector fixes exact coordinator bytes, the required contract field, sentinel replacement, UTF-8 path ordering, row identities, compact JSON encoding, and trailing LF.
- Equal current snapshots with two versus 2,000 disposable procedural-history rows produce equal projections.
- The full existing package suite passes, and compact writers remain absent from the public command surface.

## Review finding resolution

- `CCSR-M1-CR1`: resolved by the approved Specification correction and corresponding Projection implementation, schema, and tests.
- `CCSR-M1-CR2`: resolved by byte-accurate Text validation, exact operation and candidate JSON schemas, result consistency checks, and complete table-driven vectors.
- `CCSR-M1-CR3`: resolved by binding M1 to Design Review R4 and settling the exact corrected plan through Delivery Review R4.
- `CCSR-M1-CR4`: resolved by exact authoritative-path membership, bidirectional review/decision/evidence checks, current Verify evidence resolution, and prototype-safe identity lookup.
- `CCSR-M1-CR5`: resolved by calendar-valid UTC timestamps, exact milestone operation endpoints, transaction-private recovery content roots, and inline candidate identity verification.
- The full-suite routing regression discovered during correction was fixed so a package with multiple correction owners cannot rereview after only one owner returns; focused and full regression suites pass.
- The M1 handoff exposed and fixed a workflow projection regression: advancing an approved Delivery Review into Implementation now projects Code Review as the next stage, matching milestone start and completion invariants.

## Recovery

The compact reader, schema, projection, fixtures, and tests can be reverted together. Because public compact writing remains withheld, no compact repository state requires migration or recovery.
