# M3 Invocation Integration Evidence

- Subject: public invocation correlation, default severity policy, exact log inspection, additive common formats, and package-fixture integration
- Requirements: R1-R5, R15-R20, R27-R28, R31-R32
- Focused tests: `node --test packages/rigorloop/test/cli-observability.test.js packages/rigorloop/test/cli-invocation-observability.test.js packages/rigorloop/test/result-renderer.test.js`
- Package tests: `npm test --prefix packages/rigorloop` passed 171 tests before the added invocation cases and remains the milestone regression command.
- Compatibility: routine success remains quiet on stderr, `--json` remains detailed, explicit concise output is opt-in, and `--no-file-log` changes only observability.
- Inspection: `logs path` is read-only; `logs show` validates an exact random ID and searches only the bounded retained set.
- Result: passed
