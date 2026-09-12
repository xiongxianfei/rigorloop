# Validation M1 execution evidence

Owning change: [unified Validation](change.json). Engineering base: `26ac6404`.

Cache dispatch, helper mode, cache flags, selector registration and measurement acceptance are removed. Repeated supported lifecycle commands execute the validator and observe newly invalid current records. Retired flags/modes and the measurement filename reject without touching old cache or input bytes. Current v3 complete-set, unknown-vocabulary, encoding, containment and integrity negatives remain.

Removed `scripts/validation_cache.py`, `scripts/test-validation-cache.py` and fourteen exclusive measurement fixtures. These protected intentionally retired cache-hit/measurement behavior; no current obligation requires reproducing it. Surviving rejection/current-run tests replace that boundary. Historical source/evidence bytes remain recoverable unchanged at the engineering base; normative source consolidation remains M5.

The exact root `.rigorloop-validation-cache/` contained one regular `validation-cache.json`, schema 1, eleven valid disposable cache records and no symlinks or unrelated entries. The file SHA-256 was `38cd0db670097cc67494d05df1625f0559167dd83f343316dd30b4be04dc50c6`; it was rechecked immediately before unlink, followed by removal of the empty directory and exclusive ignore entry. Other cache destinations were not removed. Routine validation preserves sentinel cache bytes.

Independent first-pass finding `validation-m1-historical-catalog` exposed a current historical-inventory consumer. The exact retired cache ID is now preserved in the test's historical projection while absent from the executable catalog. Ledger bytes and unknown-ID rejection are unchanged. Output-format regressions now invoke a surviving current-record test instead of the removed measurement case.

Commands and observed results:

- Baseline `python scripts/test-artifact-lifecycle-validator.py`: 112 passed before retirement.
- New retired measurement input regression failed before implementation because the old reader decoded invalid bytes. It passes after filename-first rejection.
- `python scripts/test-change-metadata-validator.py`: 7 passed.
- `python scripts/test-artifact-lifecycle-validator.py`: 108 passed, including actual repeated execution and retired-input no-write proof.
- `python scripts/test-select-validation.py`: initial run exposed obsolete output-case references and the historical projection; corrected complete run: 167 passed.
- `npm --prefix packages/rigorloop test`: 423 passed, one historical-inventory consumer failed before correction. `python scripts/test-retirement-ledger.py`: corrected 17 passed; `node --test packages/rigorloop/test/record-retirement.test.js`: all 25 passed, including that exact consumer. Other CLI engineering inputs were unchanged by the correction.
- `git diff --check`: passed.

This evidence covers M1 only. It does not claim later executor/case integration, final Verify, PR readiness or a runtime improvement.
