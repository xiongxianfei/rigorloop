# M4 Token and Package Proof

- Subject: versioned six-profile CLI result measurement, v0.4.x detailed baseline, operation documentation, and package validation
- Requirements: R29-R31, AC6-AC10
- Measurement: `python scripts/measure-cli-result-bytes.py --profiles packages/rigorloop/test/fixtures/observability/token-profiles-v1.json --baseline docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json --check`
- Measurement tests: `python scripts/test-cli-result-measurement.py`
- Result: the v1 corpus passes the 30% median, per-profile growth, required-field, and one-pass gates. This records eligibility for a separate v0.5.0 review; `default_changed` remains false and v0.4.x defaults are unchanged.
- Package documentation: configuration, platform-local storage, bounded rotation, exact lookup, privacy boundary, recovery controls, and explicit result projections are documented.
