# M4 Preactivation Parity Evidence

## Result

Milestone: M4
Validation result: passed

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Staged coherent v2 governance, contract-keyed boundary routing, activation-readiness validation, and temporary supported-adapter publication proof while preserving the released v1 default.
- Artifacts changed: governing workflow guidance, the shared boundary compact scan and four remaining consumers, lifecycle-contract validation, adapter generation and clean-install validation, focused tests, adapter installation guidance, and this evidence.
- Tests added or updated: Added activation-prerequisite coverage for exact blocking IDs, post-Delivery-Review acceptance, and unknown lifecycle/stage values; added staged v2 archive, mixed-entrypoint, plan-resource, and clean-install checks; added normative governance and boundary-routing coherence checks.
- Validation performed: CMD-03, CMD-04, CMD-06, CMD-07, CMD-08, CMD-09, CMD-10, Python compilation, and `git diff --check`.
- Validation result: All required M4 commands passed. Documentation audit reported zero errors and 48 existing line-wrap warnings.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: The tracked activation manifest, released adapter manifest, default new-change contract, and active public skill inventory remain v1. M5 owns activation and removal of canonical standalone entrypoints.

## Planned milestone

- Change ID: `2026-08-31-retire-standalone-test-spec-stage`
- Plan identity: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`, sha256 `727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938`.
- Milestone ID: M4.
- Milestone state: implementation evidence complete; workflow review-requested handoff pending.
- Baseline or change-pack status: Design Review `design-review-r2` and Delivery Review `delivery-review-r3` remain current under this change's registered v1 contract.
- Milestone validation evidence: this file.
- Commit status: supplied by Git history after evidence recording.
- Code-review handoff: review normative-versus-historical scope, activation prerequisite closure, fail-closed vocabulary ordering, staged adapter exactness, clean-install parity, and unchanged active v1 behavior.

## Test-first record

The initial M4 tests failed because governance named only the v1 package, the shared boundary template routed every proof gap to test-spec, no activation-prerequisite audit existed, and adapter tooling had no staged v2 inventory. After adding the scoped implementation, focused tests passed.

The first staged clean-install check then exposed an opencode metadata mismatch: candidate metadata still declared the removed `test-spec` alias. The adapter candidate now carries the same contract-selected alias inventory through archive generation, metadata, installation, and validation; the clean-install check passes for all three adapters.

## Current-surface inventory

| Surface | M4 disposition | Evidence |
| --- | --- | --- |
| Constitution, agent guidance, workflow summary, workflow spec | Contract-keyed preactivation guidance added | Each names v1 plan-plus-test-spec, v2 plan-only, inactive v2, and historical compatibility. |
| Specification, plan, Delivery Review skills and assets | Already aligned in M3 | Full skill suite and generated-skill checks pass. |
| Shared boundary routing | Synchronized | Template plus workflow, spec, plan, test-spec, implement, code-review, and verify route gaps by contract. |
| Lifecycle contract validation | Extended | Candidate activation inventory reports exact blocking change IDs; lifecycle and stage vocabularies reject unknown values before readiness checks. |
| Adapter publication | Staged only | Temporary Codex, Claude Code, and opencode archives omit test-spec, include all eight plan references, reject mixed entries, and install cleanly. |
| Tracked adapter manifest and released v1 aliases | Unchanged with rationale | They describe the still-active v1 package and switch only in M5's coherent activation. |
| New-change scaffolding and active graph | Unchanged with rationale | M5 owns default v2 activation; M4 must not publish the new route. |
| Historical changes, test specs, reviews, release archives, and examples | Unchanged with rationale | They remain immutable evidence or released records and are not active authoring templates for v2. |

## Validation evidence

- `python scripts/test-change-metadata-validator.py`: 81 passed.
- `python scripts/test-artifact-lifecycle-validator.py`: 166 passed.
- `python scripts/test-review-artifact-validator.py`: 110 passed.
- `python scripts/test-skill-validator.py`: 379 passed.
- `python scripts/test-build-skills.py`: 8 passed.
- `python scripts/build-skills.py --check`: passed with temporary generated output.
- `python scripts/test-adapter-distribution.py`: 154 passed, including staged candidate archives and clean installs for Codex, Claude Code, and opencode.
- `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`: zero errors and 48 pre-existing warnings.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml --path docs/changes/2026-08-31-retire-standalone-test-spec-stage/evidence/m4-preactivation-parity.md --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`: passed with one existing workflow-spec lifecycle-language warning.
- `python -m py_compile scripts/artifact_lifecycle_contracts.py scripts/adapter_distribution.py`: passed.
- `git diff --check`: passed.

## Recovery

Revert M4 as one unit: governing preactivation text, shared routing copies, activation-prerequisite helper, staged adapter candidate support, tests, and evidence. The tracked v1 manifest and runtime default require no rollback because M4 does not change them.
