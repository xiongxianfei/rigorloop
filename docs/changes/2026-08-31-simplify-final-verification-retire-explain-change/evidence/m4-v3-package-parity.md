<!-- Template: implementation-result-skeleton-v1 -->
<!-- Skill: implement -->
<!-- Template status: normative -->

## Result

Milestone: M4
Validation result: passed

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Assembled one inactive v3 candidate across current governance, workflow documentation, canonical stage skills, boundary validation, adapter generation, and package-parity fixtures while retaining the active v2 package and historical archives.
- Artifacts changed: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, canonical workflow/code-review/CI/PR skills and resources, boundary and adapter validation modules, their focused tests, and `dist/adapters/README.md`.
- Tests added or updated: current-versus-staged governance parity, v3 skill handoff agreement, scoped Verify resource exclusion, semantic lifecycle-contract parsing, v2/v3 plan-owned boundary proof, composed-boundary examples, staged v3 archive completeness, and mixed-inventory rejection.
- Validation performed: every M4 plan command plus `git diff --check`.
- Validation result: passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: v3 remains inactive. This milestone does not change the default lifecycle contract, edit the current adapter manifest, remove `skills/explain-change/`, mutate historical release archives or change evidence, or start M5.

## Planned milestone

- Change ID: `2026-08-31-simplify-final-verification-retire-explain-change`
- Plan identity: `docs/plans/2026-08-31-simplify-final-verification-retire-explain-change.md`
- Milestone ID: M4
- Milestone state: implementing until Workflow records this evidence and requests Code Review.
- Baseline or change-pack status: M1-M3 are closed after clean Code Review; `specs/final-verification-contract-activation.yaml` remains `preactivation`.
- Milestone validation evidence: this file and the command results below.
- Commit status: recorded by the M4 implementation commit containing this evidence.
- Code-review handoff: review authority wording, progressive disclosure, semantic validator behavior, generated-package parity, and historical-scope preservation.

## Test-first and implementation record

- Added package-parity, boundary-proof, and adapter-candidate assertions before completing their implementation.
- The first full skill run identified four retained compatibility contracts: the exact v1 lifecycle name, the legacy Explain change table projection, the established final-review routing sentence, and the PR governed-profile size ceiling. The implementation retained those contracts and compressed the added PR guidance; the complete suite then passed.
- The boundary validator now parses the owning `change.yaml` semantically through the repository metadata validator, rejects duplicate or unknown lifecycle-contract values before consistency, and uses the registered primary plan as proof for stage-owned v2/v3 specifications.
- Composed examples now require every cited boundary to govern at least one cited example requirement. They no longer incorrectly require every requirement to belong to every boundary.
- Adapter tooling can build and exactly validate temporary Codex, Claude Code, and opencode v3 candidates. The candidate inventory omits `explain-change`, preserves all mapped Verify resources, and rejects stale or mixed entries.

## Current, staged, and historical inventory

| Inventory | Authority in M4 | Evidence |
| --- | --- | --- |
| Current v2 | Active for new governed changes during preactivation; retains standalone `explain-change` and existing Verify handoff. | Governance surfaces name `stage-owned-change-local-v2`; tracked `dist/adapters/manifest.yaml` remains unchanged. |
| Staged v3 | Inactive candidate; final Code Review and triggered CI route to Verify, successful Verify owns the final explanation, and PR consumes that exact result. | Contract-keyed governance/skills and temporary v3 adapter archives. |
| Exact v1/v2 continuations | Continue only for registered prior identities under their original contracts. | Existing activation manifests and compatibility tests. |
| Historical artifacts and releases | Readable evidence only; no new authority and no migration. | No historical change record, release archive, or generated release body was modified. |

## Verification-group evidence

- TG-15: current governance distinguishes active v2 from inactive v3; Workflow, Code Review, CI Maintenance, Verify, and PR agree on the v3 route, correction boundary, success-only explanation, and PR consumption. Historical v1/v2 language remains explicit.
- TG-16: scoped Verify continues to load none of the final-impact, evidence-applicability, or explanation resources. The inactive final-readiness profile maps all three, and explanation guidance loads only after a successful v3 readiness decision.
- TG-17: v2/v3 stage-owned specs obtain boundary proof from the exact primary plan registered in parsed change metadata. Unsafe paths, missing plans, incomplete boundary/integration allocation, duplicate mapping keys, malformed YAML, and unknown contracts fail closed. Legacy proof behavior remains available only to its prior contract.
- TG-18: temporary candidates for all supported adapters are generated from canonical sources and validated by exact archive inventory. Tests reject a mixed v3 archive containing an `explain-change` entrypoint and prove Verify resources are complete. The tracked current manifest and historical archives remain untouched.

## Unchanged-surface rationale

- Existing M1 schema and lifecycle metadata validation already define the closed v3 contract and forbid v3 explain-change state; M4 adds no duplicate schema vocabulary.
- Existing M3 runtime, routing, selector, and review validators already implement inactive v3 behavior. M4 changes their published governance and package projections without changing those settled semantics.
- `dist/adapters/manifest.yaml` intentionally remains the active v2 inventory. Switching it or removing the canonical standalone skill belongs to the atomic M5 activation candidate.
- No generated public adapter skill body was hand-edited. Candidate output existed only in temporary test directories.

## Validation evidence

- `python scripts/test-skill-validator.py` — passed, 385 tests.
- `python scripts/validate-skills.py` — passed, 21 canonical skills.
- `python scripts/test-build-skills.py` — passed, 8 tests.
- `python scripts/build-skills.py --check` — passed using temporary generated output.
- `python scripts/test-boundary-first-validation.py` — passed, 68 tests.
- `python scripts/validate-boundary-first.py --check` — passed; active snapshot and rollback artifacts validated.
- `python scripts/test-adapter-distribution.py` — passed, 156 tests.
- `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md` — passed with 0 errors and 48 pre-existing or review-visible warnings.
- `git diff --check` — passed.

## Review handoff

Review M4 as an inactive package-assembly milestone. Confirm that current v2 authority is unaltered, v3 wording is consistent across all current surfaces, scoped Verify does not load final-readiness resources, plan-owned boundary proof is semantic and fail-closed, all three adapter candidates have an exact unmixed inventory, and no historical artifact or current release manifest changed.
