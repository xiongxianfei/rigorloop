<!-- Template: implementation-result-skeleton-v1 -->
<!-- Skill: implement -->
<!-- Template status: normative -->

## Result

Milestone: M4
Validation result: passed

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Assembled one v3-only current candidate across governance, workflow documentation, canonical stage skills, boundary validation, adapter generation, and package-parity fixtures while preserving historical archives as read-only evidence.
- Artifacts changed: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, canonical workflow/code-review/CI/PR skills and resources, boundary and adapter validation modules, their focused tests, and `dist/adapters/README.md`.
- Tests added or updated: current-versus-staged governance parity, v3 skill handoff agreement, scoped Verify resource exclusion, semantic lifecycle-contract parsing, v2/v3 plan-owned boundary proof, composed-boundary examples, staged v3 archive completeness, and mixed-inventory rejection.
- Validation performed: every M4 plan command plus `git diff --check`.
- Validation result: passed.
- Open blockers: Code Review R1 findings await independent rereview after the corrections below.
- Next stage: code-review.
- Claim limitations: public activation and standalone-skill removal remain M5 work. This milestone does not edit the current adapter manifest, mutate historical release archives or change evidence, or start M5.

## Code Review M4 R1 correction

- `FV-M4-CR1`: canonical Verify and its three generated v3 candidates now have no pre-Verify explanation prerequisite. Verify creates the durable explanation only after a successful readiness decision; failure and inconclusive outcomes create none. Current workflow guidance has one executable v3 route. The implementing change's released-v2 closeout is a one-time preactivation bootstrap, not a general compatibility branch.
- `FV-M4-CR2`: the shared parsed-YAML mapping routine rejects duplicate keys before assignment at every nesting depth. Boundary validation delegates to that one parser and no longer maintains a raw-text or top-level-only duplicate checker.
- Direct regressions cover shared-parser nested duplicates and authority-relevant `artifact_states`, `plan`, `kind`, `role`, and `path` duplicates in both orders. V3 candidate tests scan every supported adapter for forbidden pre-Verify explanation clauses.
- Design Review R2 independently approved the latest-contract package. Delivery Review R3 independently approved the corrected execution sequence and reproduced all four immutable v2-bootstrap hashes. Their durable receipts record that formal CLI settlement is blocked by the already-open M4 Code Review findings; no lifecycle state was hand-edited.

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
| Current v3 candidate | Final Code Review and triggered CI route to Verify; successful Verify owns the final explanation and PR consumes that exact result. | Current governance, canonical skills, and temporary v3 adapter archives. |
| Implementing-change bootstrap | This change alone closes before activation through the last coherent released v2 package. | Approved plan amendment; no reusable current checker branch. |
| Historical v1/v2 | Readable evidence only; no progression authority and no migration. | Historical records and archives remain unchanged. |

## Verification-group evidence

- TG-15: Workflow, Code Review, CI Maintenance, Verify, and PR agree on one current v3 route, correction boundary, success-only explanation, and PR consumption. Historical v1/v2 readability is separate from executable authority.
- TG-16: scoped Verify continues to load none of the final-impact, evidence-applicability, or explanation resources. The inactive final-readiness profile maps all three, and explanation guidance loads only after a successful v3 readiness decision.
- TG-17: governed specs obtain boundary proof from the exact primary plan registered in parsed change metadata. Unsafe paths, missing plans, incomplete boundary/integration allocation, recursive duplicate mapping keys, malformed YAML, and unknown or non-current contracts fail closed.
- TG-18: temporary candidates for all supported adapters are generated from canonical sources and validated by exact archive inventory. Tests reject a mixed v3 archive containing an `explain-change` entrypoint and prove Verify resources are complete. The tracked current manifest and historical archives remain untouched.

## Unchanged-surface rationale

- Existing M1 schema and lifecycle metadata validation already define the closed v3 contract and forbid v3 explain-change state; M4 adds no duplicate schema vocabulary.
- Existing M3 runtime, routing, selector, and review validators provide the staged protocol foundation. M4 makes published governance and package projections v3-only; M5 removes remaining executable legacy runtime branches atomically.
- `dist/adapters/manifest.yaml` intentionally remains the active v2 inventory. Switching it or removing the canonical standalone skill belongs to the atomic M5 activation candidate.
- No generated public adapter skill body was hand-edited. Candidate output existed only in temporary test directories.

## Validation evidence

- `python scripts/test-skill-validator.py` — passed, 386 tests.
- `python scripts/validate-skills.py` — passed, 21 canonical skills.
- `python scripts/test-build-skills.py` — passed, 8 tests.
- `python scripts/build-skills.py --check` — passed using temporary generated output.
- `python scripts/test-boundary-first-validation.py` — passed, 69 tests.
- `python scripts/test-change-metadata-validator.py` — passed, 107 tests, including the direct recursive-duplicate parser regression and corrected single-mapping fixture.
- `python scripts/validate-boundary-first.py --check` — passed; active snapshot and rollback artifacts validated.
- `python scripts/test-adapter-distribution.py` — passed, 156 tests in 402.878 seconds.
- `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md` — passed with 0 errors and 48 pre-existing or review-visible warnings.
- `git diff --check` — passed.

## Review handoff

Review M4 as a v3-only package-assembly milestone. Confirm that no current checker or skill route selects v1/v2, the implementing change retains only its explicit released-v2 bootstrap, scoped Verify does not load final-readiness resources, plan-owned boundary proof uses the single recursive duplicate-safe parser, all three adapter candidates have an exact unmixed inventory, and no historical artifact or current release manifest changed.
