# M1 Result Model Evidence

- Subject: shared CLI result projection and lifecycle renderer integration
- Requirements: R21-R28, AC6, AC7, AC10
- Test-first observation: `node --test packages/rigorloop/test/result-renderer.test.js` initially failed with `ERR_MODULE_NOT_FOUND` for the intentionally absent renderer.
- Correction round: `code-review-m1-r1` findings `CLIOBS-M1-CR1` and `CLIOBS-M1-CR3` moved all command output behind the invocation controller. New projections are rendered only after terminal observability is known, and they use the controller's semantic exit code.
- Direct regression proof: unsafe logging configuration preserves dispatch; event construction failure preserves dispatch; completion-sink failure produces a degraded projection; concise projection exit code equals the process exit code; mutation-state, continuation-cardinality, mandatory-field, result-class, and public `new-change` format partitions are characterized.
- Validation: exact C02 passed 14 tests; the expanded focused command passed 32 tests; `npm test --prefix packages/rigorloop` passed 211 tests.
- Compatibility: legacy `human` and `json` renderings remain unchanged; `detailed-json` aliases detailed JSON and concise formats are additive.
- Result: R4 correction proof passed; fresh same-stage L1 code rereview remains required.
