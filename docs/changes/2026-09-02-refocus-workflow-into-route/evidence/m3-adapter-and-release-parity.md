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
- Tests added or updated: route-only archive and invocation parity, absence of retired guide resources, obsolete and mixed installed-package diagnostics, obsolete archive rejection, current token benchmark selection, and removal of workflow-guide fixtures.
- Validation result: all seven required M3 commands passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: no adapter archive, npm package, tag, release, or external publication was created or changed.

## Requirement and proof mapping

| Proof group | Result |
| --- | --- |
| TG-12 | All three supported adapter models generate and invoke `route`; current archives contain no `workflow` alias or retired guide resource. |
| TG-13 | Init rejects obsolete installed workflow packages for Codex, Claude Code, and opencode, rejects mixed route/workflow installations, rejects an obsolete workflow archive before extraction, identifies `route` as replacement, and preserves stored `workflow.automation` compatibility. |
| TG-14 | Canonical, generated, archived-candidate, and clean-install resource inventories and normalized bytes agree for route across all supported adapters. |
| TG-15 | Recorded-source and historical release validation remains green; current adapter documentation and tests distinguish immutable historical archives from the current unpublished candidate. |
| TG-16 | Existing generation, validation, archive, clean-install, and interruption regressions pass; rejected obsolete or mixed input leaves the project tree unchanged. |

The token-cost benchmark keeps the stable benchmark ID `workflow-route` for longitudinal comparison while changing its selected public skill and prompt to `route`. Current benchmark fixtures no longer carry `docs/workflows.md` as workflow authority.

## Test-first evidence

The initial adapter-distribution run failed with 57 errors and 7 failures because the closed adapter model and tests still required the deleted workflow package and guide resources. After migrating those inventories, the first full green-oriented run exposed one stale documentation assertion that expected preactivation wording. The documentation and its assertion were aligned with active v3, the focused regression passed, and the complete command was rerun successfully.

## Validation

All required M3 commands passed on 2026-09-02:

- `python scripts/test-adapter-distribution.py` — 155 tests passed in 354.232 seconds.
- `python scripts/test-build-skills.py` — 8 tests passed.
- `python scripts/test-skill-validator.py` — 352 tests passed.
- `python scripts/test-token-cost-measurement.py` — 25 tests passed.
- `python scripts/build-skills.py --check` — canonical generated-skill parity passed using temporary output.
- `npm test --prefix packages/rigorloop` — 365 tests: 363 passed and 2 explicitly historical tests skipped.
- `bash scripts/ci.sh --mode broad-smoke` — 11 checks passed in 407 seconds.

Additional focused proof:

- `node --test --test-name-pattern='RT-R30' packages/rigorloop/test/cli.test.js` — 3 installer migration tests passed.
- `python -m unittest -v scripts.test-adapter-distribution.AdapterDistributionTests.test_public_adapter_readme_documents_archive_install_contract` — passed.
- `git diff --check` — passed.

## Handoff

- Review target: M3 supported-adapter propagation and release-candidate validation surfaces.
- Requested next stage: `code-review`.
- Final verification, PR, and release readiness: not claimed.
