# M3 Adapter and Release Parity Evidence

Milestone: M3
Subject path: docs/plans/2026-09-02-refocus-workflow-into-route.md
Subject identity: sha256:825e74a85b56a43db8f8a47191882794d95dd27cf65ffe0e968358b7203b162d
Validation result: passed

## Result

- Skill: implement
- Status: implemented
- Completed scope: propagated the canonical route identity and mapped resources through supported adapter metadata, generation, clean-install validation, CLI installer diagnostics, migration documentation, and token-cost inventory.
- Artifacts changed: adapter manifest and documentation; adapter distribution generator and tests; CLI installer and tests; package documentation; current token benchmark manifest, prompt, and fixtures.
- Tests added or updated: route-only archive and invocation parity, real bundled v0.5.1 candidate identity, absence of retired guide resources, obsolete and mixed installed-package diagnostics, exact lockfile-managed migration and rollback, unrelated-target preservation, current token benchmark selection, and removal of workflow-guide fixtures.
- Validation result: all seven required M3 commands passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: no adapter archive, npm package, tag, release, or external publication was created or changed.

## Requirement and proof mapping

| Proof group | Result |
| --- | --- |
| TG-12 | All three supported adapter models generate and invoke `route`; current archives contain no `workflow` alias or retired guide resource. |
| TG-13 | Init rejects unmanaged, drifted, and mixed workflow packages safely; normal `init --write-state` replaces an exact lockfile-managed target with route while preserving unrelated targets and stored `workflow.automation` compatibility. |
| TG-14 | Canonical, generated, archived-candidate, and clean-install resource inventories and normalized bytes agree for route across all supported adapters. |
| TG-15 | Bundled v0.5.1 metadata matches freshly generated route-only candidate archives; recorded-source and historical release validation remains green; immutable v0.5.0 metadata retains SHA-256 `74f2d940ce8ef358092609884e9377d0a3955c731e7f437ca63d995862227885`; documentation labels v0.5.1 unpublished. |
| TG-16 | Existing generation, validation, archive, and clean-install regressions pass; a failed managed replacement restores the selected target, manifest, and lockfile byte-for-byte. |

The token-cost benchmark keeps the stable benchmark ID `workflow-route` for longitudinal comparison while changing its selected public skill and prompt to `route`. Current benchmark fixtures no longer carry `docs/workflows.md` as workflow authority.

## Test-first evidence

The initial adapter-distribution run failed with 57 errors and 7 failures because the closed adapter model and tests still required the deleted workflow package and guide resources. After migrating those inventories, the first full green-oriented run exposed one stale documentation assertion that expected preactivation wording. The documentation and its assertion were aligned with active v3, the focused regression passed, and the complete command was rerun successfully.

## Validation

All required M3 commands passed again after the R1 correction on 2026-09-02:

- `python scripts/test-adapter-distribution.py` — 156 tests passed in 385.604 seconds.
- `python scripts/test-build-skills.py` — 8 tests passed.
- `python scripts/test-skill-validator.py` — 352 tests passed.
- `python scripts/test-token-cost-measurement.py` — 25 tests passed.
- `python scripts/build-skills.py --check` — canonical generated-skill parity passed using temporary output.
- `npm test --prefix packages/rigorloop` — 367 tests: 365 passed and 2 explicitly historical tests skipped.
- `bash scripts/ci.sh --mode broad-smoke` — 12 checks passed in 446 seconds.

Additional focused proof:

- `node --test --test-name-pattern='TNP-005|managed workflow replacement|normal init replaces' packages/rigorloop/test/cli.test.js` — 3 candidate/migration tests passed.
- `python -m unittest scripts.test-adapter-distribution.AdapterDistributionTests.test_v0_5_1_bundled_candidate_metadata_matches_generated_route_only_archives` — passed.
- `git diff --check` — passed.

## R1 correction

- RFR-M3-CR1: Package and bundled metadata now use the unpublished v0.5.1 identity. The generated-candidate test compares the complete bundled metadata object with metadata recomputed from freshly generated archives and asserts every archive contains route and omits workflow. Published v0.5.0 metadata is unchanged.
- RFR-M3-CR2: No new replacement flag was added. An intact selected target recorded by `rigorloop.lock` can be replaced through normal `init --write-state`; exact pre-mutation drift validation remains mandatory. The replacement is rollback-protected, leaves unrelated target roots and lock entries unchanged, and failure proof restores the previous target and state bytes.

## Handoff

- Review target: M3 supported-adapter propagation and release-candidate validation surfaces.
- Requested next stage: `code-review`.
- Final verification, PR, and release readiness: not claimed.
