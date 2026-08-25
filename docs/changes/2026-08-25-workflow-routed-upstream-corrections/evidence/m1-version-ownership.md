# M1 Version and Ownership Evidence

Milestone: M1
Validation result: passed

- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-migration-repair.test.js`: passed.
- `node --test packages/rigorloop/test/lifecycle-artifact-revision.test.js packages/rigorloop/test/lifecycle-ownership.test.js`: passed.
- `npm test --prefix packages/rigorloop`: passed with 175 tests.

The proof covers the version-2 migration, closed request vocabularies, cross-change ownership collisions, contradictory ownership records, and byte-preserving rejection.
