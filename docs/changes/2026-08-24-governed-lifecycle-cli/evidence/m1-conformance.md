# M1 Conformance Evidence

## Scope

M1 freezes the lifecycle operation vocabulary, request schema, YAML input domain, deterministic serialization, lifecycle revision algorithm, shared conformance fixture, protected-failure inventory, and package dependency boundary. No lifecycle CLI command or mutation path is exposed.

## Changes

- Added the pure `lifecycle-contract.js` module and shared conformance fixture.
- Added parser, request, canonicalization, identity, and unknown-value tests.
- Added a Python fixture consumer to prove cross-language fixture loading.
- Pinned `yaml@2.9.0` and updated package publication policy to admit only that reviewed runtime dependency.
- Updated the existing package metadata test and required tarball inventory.

## Validation

- `node --test packages/rigorloop/test/lifecycle-contract.test.js`: passed, 11 tests.
- `npm test --prefix packages/rigorloop`: passed, 128 tests.
- `python3 scripts/test-lifecycle-cli-conformance.py`: passed, six invalid YAML fixtures and ten protected failure classes.
- `python3 scripts/test-artifact-lifecycle-validator.py`: passed, 170 tests.
- `python3 scripts/test-change-metadata-validator.py`: passed, 63 tests.
- `python3 scripts/test-review-artifact-validator.py`: passed, 103 tests.
- `python3 scripts/test-npm-package-publication.py -k package_policy`: passed.
- `python3 scripts/validate-npm-package.py`: passed.
- `npm audit --prefix packages/rigorloop --audit-level=moderate`: passed with zero vulnerabilities.

The first attempted `yaml@2.8.1` install surfaced GHSA-48c2-rrv3-qjmp through `npm audit`; the dependency was moved to the patched exact `2.9.0` release before handoff.

## Unchanged surfaces

- `rigorloop lifecycle` dispatch is intentionally absent until M2 read-only behavior is complete.
- Existing Python transition behavior is unchanged; it consumes the protected-failure inventory only through the new bounded conformance test.
- Skills, adapters, workflow guidance, and CI enforcement are unchanged until M6 and M7.

## Handoff

M1 implementation is ready for independent code review. This evidence does not close the milestone or claim verification readiness.
