# Simplified RigorLoop Proposal Contract Execution Plan

## Purpose / big picture

Implement the approved direction-level proposal contract across canonical proposal authoring, Proposal Review, governance, validation, examples, and supported publication paths. The work keeps proposal decisions concise while preserving proportional feasibility, independent review, governed lifecycle ownership, historical readability, and downstream Design authority.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-30-simplify-rigorloop-proposal-contract.md`
- Spec: `specs/simplified-proposal-contract.md`
- Architecture: `docs/architecture/2026-08-30-simplified-proposal-contract.md`
- Test spec: `specs/simplified-proposal-contract.test.md`

## Context and orientation

Canonical proposal behavior is authored in `skills/proposal/`, `skills/proposal-review/`, repository governance, and proposal-specific validation. The proposal skeleton and review-result asset own reusable structure; references own conditional authoring and review procedure. Existing build and adapter tooling projects canonical skill sources into supported release archives, so generated packages are validated rather than hand-edited.

The implementation must distinguish current simplified proposals from untouched settled historical proposals without adding a document version, reverse ownership pointer, compatibility interpreter, content-hash requirement, or CLI command. The approved Design package is `design-review-r2`.

The prerequisite CLI retry correction in `packages/rigorloop/` restores review settlement mechanics and is already independently reviewed. It is not part of the proposal-contract behavior milestones below, but remains in the final holistic diff and validation scope.

## Non-goals

- Redesign Design Review, Delivery Review, Code Review, Verify, or lifecycle stage order.
- Add proposal-owned status, ownership, version, hash, CLI, rollout, architecture, implementation-plan, or verification-plan fields.
- Rewrite settled historical proposals or hand-edit generated adapter packages.
- Impose a fixed proposal length, word count, or token budget.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| SPC-R1-SPC-R14, SPC-R19-SPC-R20; BND-INPUT-001, BND-STATE-001, BND-AUTH-001; INT-001-INT-002 | M1 canonical authoring, review, governance, and lifecycle-boundary contract |
| SPC-R15-SPC-R17; BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001; INT-003 | M2 current-path validation, historical readability, diagnostics, and examples |
| SPC-R17-SPC-R18; BND-COMPOSE-001; INT-003 | M3 canonical-to-published package parity and cutover proof |
| SPC-AC1-SPC-AC8 | Matching test specification and milestone evidence across M1-M3 |

## Milestones

### M1. Implement the canonical proposal and review contract

- Milestone kind: implementation
- Goal: Make canonical proposal authoring, Proposal Review, reusable structures, and governance express one concise direction-approval contract.
- Requirements: SPC-R1-SPC-R14, SPC-R19-SPC-R20; BND-INPUT-001, BND-STATE-001, BND-AUTH-001; INT-001-INT-002.
- Architecture decisions: one-way `change.yaml` ownership, review-owned routine vision alignment, no new CLI or lifecycle field.
- Files/components likely touched:
  - `skills/proposal/SKILL.md`, its asset, and its directly affected references
  - `skills/proposal-review/SKILL.md`, its result asset, and its directly affected references
  - `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `specs/skill-contract.md` where their current proposal contract conflicts
- Dependencies:
  - approved Design package `design-review-r2`
  - existing proposal and Proposal Review resource ownership
- Tests and proof:
  - focused skill-contract assertions for the seven required sections, conditional impact, proportional feasibility, downstream-detail exclusion, vision-alignment outcome, isolation, and lifecycle ownership
  - resource-map and placeholder validation for both canonical skill packages
- Implementation steps:
  - update focused tests before canonical prose where feasible
  - replace the legacy proposal structure with the seven required sections and conditional impact section
  - update Proposal Review judgment and result structure to record one vision-alignment outcome without demanding downstream detail
  - align governance and workflow summaries with the same approval boundary
- Validation commands:
  - `python scripts/validate-skills.py skills/proposal/SKILL.md`
  - `python scripts/validate-skills.py skills/proposal-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/skill-contract.md`
- Expected observable result: new proposal and Proposal Review invocations use the simplified direction-level contract, while governed state remains change-record-owned and direct review remains isolated.
- Completion criteria: canonical skills, assets, references, and governance agree; focused and broad skill tests pass; no forbidden proposal-owned metadata or downstream decision requirement remains.
- Required evidence: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m1-canonical-contract.md`
- Review handoff: independent code review of M1 canonical and governance changes.
- Optional commit boundary: `M1: implement simplified proposal contract`
- Risks:
  - legacy universal rules may continue to demand detailed design or routine vision content
- Rollback/recovery:
  - correct the canonical source and its focused assertion together before rereview; generated outputs remain untouched in this milestone

### M2. Enforce current proposals while preserving settled history

- Milestone kind: implementation
- Goal: Make proposal validators, review validation, fixtures, and examples enforce the simplified current contract without rewriting or rejecting untouched settled historical proposals.
- Requirements: SPC-R3-SPC-R7, SPC-R10-SPC-R11, SPC-R15-SPC-R17; BND-INPUT-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001; INT-001-INT-003.
- Architecture decisions: current-path enforcement plus existing historical readability, with no document version marker or compatibility interpreter.
- Files/components likely touched:
  - `scripts/artifact_lifecycle_contracts.py` and proposal-related lifecycle validation
  - proposal and review validator tests under `scripts/test-*.py`
  - existing proposal fixtures, conformance examples, and review evidence examples
- Dependencies:
  - M1 and its independent code review are closed
- Tests and proof:
  - valid ordinary, material-impact, nested-heading, portable, governed, and vision-review cases
  - missing, duplicated, misordered, unknown, empty-feasibility, forbidden-status, reverse-pointer, routine-vision, and undisclosed-conflict cases
  - untouched settled historical proposals remain readable; unsettled or changed current proposals use the simplified contract
  - unknown closed-vocabulary vision outcomes fail before consistency checks
- Implementation steps:
  - add failing current-contract and historical-readability fixtures first
  - update existing proposal classification and structural checks at their current ownership point
  - extend review validation only where the vision-alignment outcome needs deterministic structural proof
  - update examples without rewriting settled historical evidence
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-08-30-simplify-rigorloop-proposal-contract.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-08-30-simplify-rigorloop-proposal-contract`
- Expected observable result: malformed current proposals fail with precise diagnostics, valid portable and governed proposals pass, and untouched settled historical proposals remain readable.
- Completion criteria: positive, negative, compatibility, ownership, and unknown-value tests pass without a new version, hash, interpreter, or CLI surface.
- Required evidence: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m2-validation-and-compatibility.md`
- Review handoff: independent code review of M2 validators, fixtures, examples, and compatibility behavior.
- Optional commit boundary: `M2: validate simplified proposals and history`
- Risks:
  - compatibility handling may accidentally exempt changed or unsettled proposals from the current contract
- Rollback/recovery:
  - keep current-path fixtures failing closed, narrow only the historical selection rule, and rerun the same validator commands

### M3. Prove canonical-to-published contract parity

- Milestone kind: implementation
- Goal: Prove supported skill builds and adapter release archives project the canonical simplified contract consistently before cutover.
- Requirements: SPC-R17-SPC-R18; BND-COMPOSE-001, BND-RECOVERY-001; INT-003.
- Architecture decisions: canonical skills are authored under `skills/`; generated archives are derived and validated through existing tooling.
- Files/components likely touched:
  - existing skill-build and adapter-distribution tests only where proposal-specific coverage is missing
  - release-validation inputs or metadata required by the existing generation path
  - change-local M3 parity evidence
- Dependencies:
  - M1-M2 and their independent code reviews are closed
- Tests and proof:
  - canonical resources build without drift
  - generated proposal and Proposal Review packages contain the expected assets and references
  - supported temporary adapter archives and clean-install checks project the same contract
  - a missing or stale generated resource blocks validation
- Implementation steps:
  - extend existing distribution proof only where it does not directly select both changed skills
  - build supported packages in temporary output and validate archive contents and clean-install parity
  - validate the published v0.4.1 evidence through its recorded source without rewriting historical release identities
  - record cutover parity without committing generated skill bodies or repository-local installed copies
- Validation commands:
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.4.1 --recorded-source-auto`
- Expected observable result: canonical skill packages and supported publication paths agree on the simplified proposal contract with no hand-edited generated output.
- Completion criteria: build, drift, archive, adapter, and release validation pass, and no mixed-contract publication surface remains.
- Required evidence: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m3-publication-parity.md`
- Review handoff: independent code review of M3 distribution proof and the complete implementation interaction.
- Optional commit boundary: `M3: prove simplified proposal publication parity`
- Risks:
  - generic distribution checks may pass without selecting both changed skill packages
- Rollback/recovery:
  - correct canonical resources or existing generator metadata, regenerate temporary outputs, and repeat parity validation

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Complete holistic review, rationale, verification, and PR handoff after all implementation milestones close.
- Requirements: SPC-AC1-SPC-AC8.
- Architecture decisions: no additional design decision.
- Files/components likely touched:
  - final review evidence, `explain-change.md`, and `verify-report.md` under the owning change root
- Dependencies:
  - M1-M3 and required review resolution are closed
- Tests and proof:
  - final holistic diff review and the complete approved test-spec command set
- Implementation steps:
  - obtain final holistic code review, resolve and rereview findings when required, explain the actual diff, and run final verification
- Validation commands:
  - run every required command from `specs/simplified-proposal-contract.test.md`
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- Expected observable result: the complete implementation and evidence set support truthful PR handoff.
- Completion criteria: final review is clean, rationale and verification are current, and no lifecycle blocker remains.
- Required evidence: final review receipt, closed review resolution when required, explanation, and verify report.
- Review handoff: `verify`, then `pr` only when requested or workflow-authorized.
- Optional commit boundary: `closeout: verify simplified proposal contract`
- Risks:
  - a cross-milestone inconsistency may invalidate earlier evidence
- Rollback/recovery:
  - return to the owning milestone, correct and rereview it, then repeat holistic closeout

## Validation plan

- Skill validation owns canonical structure, resource maps, output assets, and focused proposal behavior.
- Artifact and review validation own current proposal structure, governed ownership, vision-outcome shape, and historical readability.
- Build and adapter validation own canonical-to-generated parity without making generated packages authored truth.
- The matching test specification will map every requirement, boundary, interaction, edge case, and acceptance criterion to exact automated proof or a justified review check.
- Final CI runs only after milestone-local proof and review pass.

## Risks and recovery

- Risk: proposal concision removes information needed for direction approval. Recovery: retain proportional feasibility and material-impact disclosure, then route behavioral or architectural detail to Design.
- Risk: current-versus-historical selection becomes ambiguous. Recovery: fail current work closed and narrow historical readability to untouched settled evidence.
- Risk: Proposal Review continues to request downstream detail. Recovery: make premature downstream settlement itself reviewable and prove the exclusion in focused tests.
- Risk: canonical and published packages diverge. Recovery: block cutover, correct canonical sources or generator metadata, and rerun existing build and adapter checks.

## Dependencies

- Accepted proposal and approved Design package `design-review-r2`.
- Existing proposal, Proposal Review, lifecycle validation, skill build, adapter generation, and release-validation owners.
- Matching test specification and Delivery Review before implementation.
- No new dependency, service, CLI command, lifecycle field, or publication mechanism.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-30 | Use three implementation milestones plus lifecycle closeout. | Canonical contract, compatibility validation, and publication parity have distinct proof and review boundaries. | One broad implementation milestone; file-by-file milestones. |
| 2026-08-30 | Change canonical skills and governance before validators and publication proof. | Validators and generated packages should project one settled canonical contract. | Edit generated packages first; activate mixed contracts temporarily. |
| 2026-08-30 | Preserve history through bounded selection rather than per-proposal markers. | The approved design forbids version fields and compatibility interpreters. | Rewrite historical proposals; add document versions. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; Delivery Review, implementation and code review, explanation, verification, and PR handoff remain.
