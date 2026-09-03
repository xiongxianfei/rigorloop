# Execution Plan: Relax PR Evidence Tail Topology

## Purpose / big picture

Replace PR's one-direct-child evidence-tail proxy with a proportional final-state rule: the reviewed subject may precede the handoff by any contiguous Git suffix, but the cumulative suffix must contain only current, attributable final-review, workflow, and Verify evidence. Product or governing drift still blocks before external mutation.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-09-03-relax-pr-evidence-tail/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-09-03-relax-pr-evidence-tail.md`
- Spec: `specs/relax-pr-evidence-tail.md`
- Architecture: `docs/architecture/2026-09-03-relax-pr-evidence-tail.md`
- Approved Design package: `design-review-r1`
- Prior-contract test spec: none; v3 uses this plan's verification allocation.

## Context and orientation

The public rule is authored in `skills/pr/SKILL.md`, with governed readiness detail under `skills/pr/references/`. Verify's own exact two-file result registration remains defined by `skills/verify/references/successful-explanation-v3.md`; that narrower Verify-result tail must be distinguished from the broader PR-consumed evidence suffix. The approved `specs/relax-pr-evidence-tail.md` is the current authority for the exact clauses it explicitly supersedes in `specs/pr-skill-simplification.md`; unaffected prior requirements remain current without mutating that older change's governed artifact.

Focused public-contract regressions live in `scripts/test-skill-validator.py`. Supported adapter packages derive from canonical `skills/` through existing build and distribution tooling. Candidate release metadata under `packages/rigorloop/dist/metadata/` may require deterministic checksum refresh when canonical archive bytes change; generated adapter skill bodies are not authored or hand edited.

## Non-goals

- Permit any post-review product, test, specification, architecture, plan, dependency, configuration, generated-product, public-documentation, cross-change, stale, mixed, or unknown drift.
- Change Verify's ownership of `branch-ready` or its exact report-registration result.
- Add a lifecycle stage, stored tail identity, service, dependency, history rewrite, force push, merge action, or release publication.
- Redesign existing remote, PR, CI, refresh, draft, retry, or read-back behavior.
- Rewrite historical reports, reviews, merged PRs, or immutable release archives.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R1-R21, R24; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-001, INT-002, INT-003, INT-004 | M1 canonical contract, coupled Verify distinction, fail-closed regressions, and superseding-spec consumption |
| R22-R23; BND-COMPOSE-001, BND-COMPAT-001; INT-001, INT-004 | M2 generated candidate, adapter, and release-metadata parity |
| R1-R24; all eight boundary IDs; INT-001, INT-002, INT-003, INT-004 | TG-FINAL-01 and TG-FINAL-02 complete-change proof |

## Milestones

### M1. Implement the proportional canonical PR contract

- Milestone kind: implementation
- Engineering purpose: Establish the complete safety predicate and its negative cases in canonical source before refreshing derived package identities.
- Requirements: R1-R21, R24; all eight boundary IDs; INT-001, INT-002, INT-003, INT-004.
- Architecture responsibility: Verify basis consumer, evidence-suffix classifier, product-boundary guard, authority and current-state checks, recovery routing, and unchanged external-operation guard.
- Dependencies:
  - approved Design package `design-review-r1`;
  - current successful Verify basis and governed-readiness concepts;
  - canonical `skills/` source ownership.
- Implementation scope: Consume the approved focused specification alongside unaffected prior PR requirements, replace the fixed direct-child rule in the canonical PR skill and governed readiness guidance, clarify that Verify's exact result registration is narrower than PR's cumulative evidence suffix, and update focused public-contract tests. Do not mutate the older governed PR specification, executable lifecycle state, external mutation behavior, or generated adapter bodies.
- Files/components likely touched:
  - `skills/pr/SKILL.md` and `skills/pr/references/governed-pr-readiness.md`;
  - `skills/verify/references/successful-explanation-v3.md`;
  - `scripts/test-skill-validator.py`.
- Required verification:
  - TG-01 — Same-revision and one-or-more-commit descendant handoffs classify from the cumulative final diff as `none`, `evidence-only`, or `invalidating`, without commit-count, direct-parent, message, author, or stage-label authority.
  - TG-02 — Current attributable final-review, workflow, and Verify evidence can compose as evidence-only, while path membership alone, stale or cross-change evidence, mutable non-lifecycle fields, mixed changes, protected surfaces, non-ancestor relationships, and unknown outcomes fail closed.
  - TG-03 — Verify remains the sole branch-readiness owner, its report-registration pair remains exact, PR remains lifecycle-read-only, and product drift routes to the applicable owner and fresh review or Verify.
  - TG-04 — Existing remote identity, push, PR-state, CI, retry, draft, refresh, and read-back clauses remain present and unchanged in authority.
- Evidence expectations: Focused literal and mutation-style contract tests cover the closed vocabulary, unknown rejection, cumulative rather than per-commit judgment, allowed evidence categories, protected/mixed/stale/cross-change negatives, Verify-result distinction, and unchanged external protections.
- Implementation steps:
  - Update or add failing focused assertions for the proportional rule and unknown-value fail-closed behavior.
  - Treat the approved focused delta as current for its enumerated superseded clauses and retain unaffected requirements from the older PR contract as read-only input.
  - Update the canonical PR procedure and governed readiness reference with content-and-authority classification.
  - Clarify the coupled Verify reference so its exact report-registration result is not misread as limiting the complete PR evidence suffix to one commit or two paths.
  - Run focused canonical validation and inspect remaining current direct-child wording.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-boundary-first.py --check --path specs/relax-pr-evidence-tail.md`
- Expected observable result: The published canonical contract accepts any current evidence-only descendant suffix and rejects every protected, mixed, unknown, stale, or unattributable suffix before external mutation.
- Completion criteria: TG-01 through TG-04 pass; no current canonical PR requirement retains a fixed commit-count or direct-parent restriction; the Verify-result registration remains exact; external safeguards remain intact.
- Required evidence: `docs/changes/2026-09-03-relax-pr-evidence-tail/evidence/m1-proportional-pr-contract.md`
- Review handoff: Code Review of the exact safety predicate, allowed evidence authority, negative partitions, superseding-spec consumption, Verify distinction, and unchanged external protections.
- Optional commit boundary: `M1: implement proportional PR evidence suffix`
- Risks:
  - Broadening the suffix wording could accidentally trust paths or commit metadata instead of current governed authority.
  - Aligning Verify wording could weaken its exact report-registration integrity.
- Rollback/recovery:
  - Revert the complete M1 implementation slice together; do not leave the PR skill, Verify reference, and tests on mixed rules.

### M2. Prove generated adapter and candidate-metadata parity

- Milestone kind: implementation
- Engineering purpose: Propagate the reviewed canonical bytes through every supported adapter boundary and refresh only deterministic candidate identities affected by those bytes.
- Requirements: R22-R23; BND-COMPOSE-001, BND-COMPAT-001; INT-001, INT-004.
- Architecture responsibility: deployment view, canonical-to-generated parity, atomic current-package adoption, historical preservation, and rollback integrity.
- Dependencies:
  - accepted M1 implementation and Code Review;
  - repository-owned skill and adapter generators;
  - current unpublished candidate release metadata, if its canonical archive identities change.
- Implementation scope: Generate temporary supported-adapter candidates from canonical source, validate their public contract and resource parity, and refresh tracked candidate metadata and exact checksum expectations only when repository tooling proves they changed. Preserve historical release metadata and do not publish or hand edit generated bodies.
- Files/components likely touched:
  - `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json` when affected;
  - `packages/rigorloop/dist/metadata/releases.json` when affected;
  - `packages/rigorloop/test/cli.test.js` when an exact candidate checksum fixture changes;
  - existing adapter validation tests only if they lack coverage for the revised public wording.
- Required verification:
  - TG-05 — Codex, Claude Code, and opencode candidates contain the revised PR and coupled Verify contract with canonical resource parity.
  - TG-06 — Candidate archive, tree, inventory, release checksum, and exact test identities agree after canonical-byte changes; stale or mixed identities fail existing validation.
  - TG-07 — Historical release archives and metadata remain unchanged, failed generation leaves no authoritative partial output, and no derived skill body becomes tracked authored source.
- Evidence expectations: Temporary build inventories, deterministic adapter-distribution results, candidate metadata validation, changed-hash derivation, historical-diff inspection, and broad-smoke output.
- Implementation steps:
  - Run candidate generation and distribution tests against the accepted M1 canonical source.
  - Derive affected archive, tree, inventory, and release identities through existing tooling.
  - Update only exact current-candidate metadata and checksum fixtures proven stale.
  - Rerun package, adapter, selection, and broad repository validation from a clean tracked state.
- Validation commands:
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-select-validation.py`
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: Every supported generated candidate exposes the proportional evidence-suffix contract, and all current candidate identities agree without altering historical releases or publishing anything.
- Completion criteria: TG-05 through TG-07 pass; candidate metadata is either proven unaffected or coherently refreshed; broad smoke passes; no generated adapter body is hand edited or tracked.
- Required evidence: `docs/changes/2026-09-03-relax-pr-evidence-tail/evidence/m2-adapter-parity.md`
- Review handoff: Code Review of generated parity, exact metadata derivation, historical preservation, and complete validation evidence.
- Optional commit boundary: `M2: refresh PR evidence-tail adapter parity`
- Risks:
  - Canonical text changes can invalidate several nested release identities.
  - Temporary candidate output can be mistaken for authored or releasable state.
- Rollback/recovery:
  - Remove temporary output and revert only current-candidate metadata and fixtures with M2; leave historical releases untouched and require a later corrective release after publication.

## Change-level verification

### TG-FINAL-01. Post-review drift safety

- Covers: R1-R21, R24; M1; all eight boundary IDs; INT-001, INT-002, INT-003, INT-004.
- Demonstrate: Current final state rather than commit topology controls readiness; any number of attributable evidence commits may proceed, while every protected, mixed, stale, cross-change, unknown, or non-ancestor outcome blocks without lifecycle mutation or external write.
- Evidence expectations: Closed outcome matrix, current-authority checks, same-revision and multi-commit examples, negative mutations, unchanged Verify ownership, and external-operation clause inspection.
- Non-applicability: Milestone-local proof is sufficient for implementation mechanics but final verification must relate the revised contract to the exact reviewed branch and current lifecycle evidence.

### TG-FINAL-02. Canonical-to-adapter compatibility

- Covers: R22-R23 and the complete current contract; M1-M2; BND-COMPOSE-001, BND-COMPAT-001, BND-RECOVERY-001; INT-001, INT-004.
- Demonstrate: Canonical source, generated skills, supported adapter candidates, current candidate metadata, and exact tests agree atomically, while historical release evidence remains unchanged and mixed versions fail.
- Evidence expectations: Canonical and generated byte checks, adapter inventories, metadata validation, clean tracked diff, broad smoke, and historical-path exclusion.
- Non-applicability: Milestone-local proof is insufficient because package-current confidence spans authored, generated, archive, and release-metadata boundaries.

## Validation plan

- Focused skill tests prove the public proportional predicate, closed vocabulary, authority boundaries, and regression wording.
- Canonical validators and boundary-first validation prove package readability, resource integrity, and the approved specification map.
- Adapter generation and distribution tests prove supported-package parity without hand-edited output.
- Package tests prove exact candidate metadata and CLI distribution behavior.
- Selection validation proves the changed canonical, spec, metadata, and test surfaces retain repository-owned verification coverage.
- Broad smoke runs only after focused failures are resolved and supplies integrated final evidence; hosted CI and release publication remain later external observations.

## Risks and recovery

- Risk: A looser topology rule becomes a looser content rule.
  - Recovery: Preserve a closed classification, exact current authority checks, and whole-suffix invalidation for any mixed or unknown surface.
- Risk: The terms Verify evidence tail and PR evidence suffix become conflated.
  - Recovery: State explicitly that Verify's result is the exact report-registration pair while PR may consume additional current final-review and workflow evidence.
- Risk: Candidate checksums drift incompletely.
  - Recovery: Derive all identities through current tooling and validate archive, tree, inventory, release checksum, and exact fixtures together.

## Dependencies

- Accepted proposal and approved exact Design package `design-review-r1`.
- M1 must receive Code Review before M2 changes derived candidate identities.
- Each implementation milestone receives direct evidence and Code Review before the next milestone or final Verify.
- No standalone test-spec is created; this plan's TG groups are the v3 verification allocation.
- Generated adapters derive from canonical `skills/`; generated bodies and historical releases are not authored or rewritten.
- External research, new dependencies, hosted mutation, release publication, and PR opening are not required to implement this repository-owned contract.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-03 | Separate canonical safety-contract work from generated candidate parity. | The second slice depends on reviewed canonical bytes and has an independent metadata rollback boundary. | One mixed milestone; one milestone per edited file. |
| 2026-09-03 | Keep Verify's exact result tail and name the broader PR comparison an evidence suffix. | This relaxes only the PR topology proxy without weakening successful Verify registration. | Broaden Verify's own result registration; retain ambiguous shared terminology. |
| 2026-09-03 | Consume the focused delta as current authority for its enumerated superseded clauses without editing the older governed PR spec. | This preserves change-local artifact ownership while keeping unaffected prior requirements current. | Cross-change spec mutation; duplicate the complete prior contract into the focused delta. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done. Delivery Review must approve this exact primary plan before implementation begins.
