# Formal Review Recording Implementation Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-04
- Last updated: 2026-05-04
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: refactored
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow contracts, review artifact validation coverage, skill guidance, and generated skill or adapter output when canonical skills change. Focused selector-selected checks, artifact lifecycle validation, review artifact validator tests, skill validation, generated-output drift checks, adapter validation, and explicit-path CI are the required proof unless plan-review, test-spec, code-review, review-resolution, or verify elevates broad smoke.

## Purpose / Big Picture

Implement the approved formal review recording contract so detailed change-local review records are stage-neutral across `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.

The implementation must preserve material upstream review findings before fixes, support no-material detailed records for stage-owned non-approval outcomes and other R2 triggers, avoid empty `review-resolution.md` files for clean or no-material cases, and keep proposal/spec/architecture/plan status in the reviewed artifacts rather than in review records.

This is workflow-governance and repository-validation work. It changes contributor-visible review recording behavior, skill guidance, and validation coverage. It does not introduce runtime product behavior, storage services, deployment changes, external dependencies, or a new review artifact path taxonomy.

## Source Artifacts

- Proposal: [Formal Review Recording](../proposals/2026-05-04-formal-review-recording.md), accepted.
- Spec: [Formal Review Recording](../../specs/formal-review-recording.md), approved after spec-review on 2026-05-04.
- Spec-review outcome: approved with no material findings after R4 was split into material and no-material initial review-record roots.
- Architecture: not required. The approved work reuses the existing `docs/changes/<change-id>/reviews/`, `review-log.md`, and `review-resolution.md` model and the existing review-artifact validator. No new storage architecture, parser model, adapter architecture, or long-lived design boundary is introduced.
- Test spec: [Formal Review Recording Test Spec](../../specs/formal-review-recording.test.md), active after plan-review approval.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on repository-map claims for architecture, data flow, runtime flow, or ownership. Orientation comes from the approved proposal, approved spec, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, `specs/review-finding-resolution-contract.md`, current review-artifact validator code and tests, and bounded file inventories. If implementation later relies on broader repository-shape claims, refresh `docs/project-map.md` or record a narrower no-map rationale before relying on those claims.

## Context and Orientation

- `specs/formal-review-recording.md` is the approved feature contract for this initiative.
- `specs/review-finding-resolution-contract.md` is the existing detailed review record, review-log, review-resolution, and closeout validation contract. It already defines review IDs, material finding IDs, reconstructed records, review-log indexing, and review-resolution closeout rules.
- `scripts/review_artifact_validation.py` already has a stage set containing `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`. Current focused tests still lean on code-review-shaped fixtures, so the implementation needs representative upstream-stage and no-material coverage.
- Existing validator structure requires `review-log.md` whenever `reviews/` exists and requires material Finding IDs to be dispositioned in `review-resolution.md`. Clean or no-material detailed records can pass without a `review-resolution.md` file as long as no material Finding IDs exist.
- `specs/rigorloop-workflow.md`, `docs/workflows.md`, `CONSTITUTION.md`, and `AGENTS.md` already define material review finding closeout and baseline change-local artifact rules. They need alignment only where the formal review recording spec changes stage-neutral triggers, initial review-record roots, or no-material review-resolution behavior.
- `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/architecture-review/SKILL.md`, `skills/plan-review/SKILL.md`, and `skills/code-review/SKILL.md` currently share the generic material-finding completeness rule, but they do not yet consistently explain the detailed review record triggers from the approved spec.
- `skills/verify/SKILL.md`, `skills/explain-change/SKILL.md`, `skills/pr/SKILL.md`, and `skills/workflow/SKILL.md` may need concise alignment for upstream review records, no-material detailed records, and closeout blocking.
- Canonical authored skill sources live under `skills/`. Generated `.codex/skills/` and public adapter output under `dist/adapters/` must be refreshed only through repository generators.

## Non-Goals

- Do not create separate review directories per stage.
- Do not require detailed review files for every clean review.
- Do not create empty `review-resolution.md` files solely because `reviews/` exists.
- Do not add a dedicated `pr-review` stage or validator support in this initiative.
- Do not automatically copy maintainer PR comments into review records.
- Do not make review files the source of truth for proposal, spec, architecture, ADR, or plan status.
- Do not replace `review-resolution.md` with `change.yaml`.
- Do not add semantic review-quality judgment to structural validation.
- Do not migrate historical change packs unless they are touched, generated, or relied on as current authoritative guidance.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R1b` | Keep formal review stages stage-neutral in `specs/review-finding-resolution-contract.md`, workflow guidance, skill guidance, and validator/test coverage; keep `pr-review` unsupported. |
| `R2`-`R3b` | Document and test detailed-record triggers, clean artifact-local settlement, and the rule that artifact-local settlement does not replace detailed records when R2 applies. |
| `R4`-`R4g` | Align governing workflow/review contracts and tests for material and no-material initial review-record roots, including no empty `review-resolution.md` for no-material R2 triggers. |
| `R5`-`R6b` | Preserve isolated/review-only behavior, reconstructed record repair, first-pass history, and before-fix material finding recording in workflow guidance and validator proof. |
| `R7`-`R7a` | Keep the material finding boundary visible in review-stage skills and governing docs without making copyedits and non-actionable notes material by default. |
| `R8`-`R9b` | Preserve review-log indexing, stable Review IDs, material Finding ID origin, and review-resolution traceability through validator coverage. |
| `R10`-`R10c` | Confirm `change.yaml.review` keeps schema-required `status` and `unresolved_items`, with optional pointer fields remaining aggregate metadata rather than transcripts. |
| `R11`-`R11c` | Document PR comment promotion boundaries and keep dedicated `pr-review` unsupported unless a later spec extends the stage set. |
| `R12`-`R13` | Preserve same-stage re-review or explicit closeout for blocking first-pass outcomes and downstream blocking on open review-log findings or required review-resolution closeout. |
| `R14`-`R14e` | Preserve artifact-local status authority for proposals, specs, architecture artifacts, ADRs, and plans. |
| `R15`-`R15a` | Align canonical review-stage skills and regenerate `.codex/skills/` plus public adapter output if canonical skills change. |
| `R16`-`R16b` | Reuse the existing review-artifact validator and add focused regression coverage without adding semantic review-quality judgment. |

## Immediate Test-Spec Handoff

Plan-review has approved this plan, and `specs/formal-review-recording.test.md` is the active proof-planning surface for implementation.

The test spec maps every `MUST` in `specs/formal-review-recording.md` to concrete proof or justified manual verification before implementation begins. It explicitly covers:

- stage-neutral review stages and unsupported `pr-review`;
- clean artifact-local settlement without detailed review files;
- material initial review-record roots with `review-resolution.md`;
- no-material initial review-record roots without empty `review-resolution.md`;
- material Finding ID traceability from review records to `review-resolution.md`;
- same-stage later review or explicit closeout for non-approval outcomes;
- skill guidance and generated-output alignment when skills change.

Implementation milestones are test-first within their scope: add or update the relevant assertion or fixture before changing the paired contract, guidance, validator, or generated output.

## Milestones

### M1. Contract And Governance Alignment

- Goal: Align authoritative workflow and review-recording guidance with the approved formal review recording contract before changing validator or skill behavior.
- Requirements: `R1`-`R7a`, `R10`-`R14e`.
- Files/components likely touched:
  - `specs/review-finding-resolution-contract.md`
  - `specs/review-finding-resolution-contract.test.md`
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/proposals/2026-05-04-formal-review-recording.md`
  - `specs/formal-review-recording.md`
  - `docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - `docs/changes/2026-05-04-formal-review-recording/explain-change.md`
  - this plan
- Dependencies:
  - approved `specs/formal-review-recording.md`
  - accepted proposal
  - accepted plan-review
  - active matching test spec
- Tests to add/update:
  - Add or update the matching test spec first for contract/guidance assertions.
  - Add or update `specs/review-finding-resolution-contract.test.md` when `specs/review-finding-resolution-contract.md` changes.
  - Add or update `specs/rigorloop-workflow.test.md` when `specs/rigorloop-workflow.md` changes.
  - If either governing spec changes but its matching test spec is intentionally unchanged, record an unaffected rationale in this plan or the change-local artifacts before downstream handoff.
  - Add stable content assertions only where the test spec makes them concrete enough to avoid brittle prose checks.
- Implementation steps:
  - Replace code-review-specific or material-only formal review recording wording with stage-neutral detailed-record triggers.
  - Add material and no-material initial review-record root rules where the governing contracts need them.
  - Keep `review-resolution.md` conditional and explicitly avoid empty files for no-material R2 triggers.
  - Confirm `change.yaml.review.status` and `change.yaml.review.unresolved_items` remain required and that any pointer fields stay optional aggregate metadata.
  - Keep `specs/review-finding-resolution-contract.test.md` and `specs/rigorloop-workflow.test.md` aligned with their paired governing specs, or record an explicit unaffected rationale if no test-spec edit is needed.
  - Record unaffected or deferred affected-surface rationale in this plan, the change-local pack, or the implementation notes when a listed surface does not need edits.
- Validation commands:
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md docs/proposals/2026-05-04-formal-review-recording.md specs/formal-review-recording.md specs/formal-review-recording.test.md specs/review-finding-resolution-contract.md specs/review-finding-resolution-contract.test.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/plan.md docs/plans/2026-05-04-formal-review-recording.md docs/changes/2026-05-04-formal-review-recording`
- Expected observable result: contributors can read the workflow and review-recording contracts and know when formal lifecycle reviews create detailed records, when `review-resolution.md` is required, and where final artifact status lives.
- Commit message: `M1: align formal review recording contracts`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: guidance edits may accidentally make every clean review require detailed artifacts or make review files look authoritative for artifact status.
- Rollback/recovery: revert only the affected guidance and return to the approved feature spec for narrower wording before validator or skill changes proceed.

### M2. Review Artifact Validator Coverage

- Goal: Add focused test-first proof that the existing review artifact model supports upstream formal stages, material and no-material detailed records, and unsupported `pr-review` boundaries.
- Requirements: `R1a`, `R1b`, `R4`-`R4e`, `R8`-`R9b`, `R11c`, `R16`-`R16b`.
- Files/components likely touched:
  - `scripts/test-review-artifact-validator.py`
  - `scripts/review_artifact_validation.py` only if tests expose a contract mismatch
  - `tests/fixtures/review-artifacts/**` only if fixture reuse is clearer than inline temporary fixtures
  - `docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - this plan
- Dependencies:
  - M1 contract wording stable
  - active matching test spec
- Tests to add/update:
  - Add an upstream-stage material record, such as `spec-review-r1`, with material Finding ID traceability to `review-resolution.md`.
  - Add a no-material upstream record, such as `plan-review-r1` with `Status: rethink`, indexed by `review-log.md` and no `review-resolution.md` file.
  - Add or preserve unknown-stage rejection for `pr-review`.
  - Add or preserve material Finding ID failures when `review-resolution.md` is missing or introduces unknown IDs.
- Implementation steps:
  - Write failing tests or fixtures for representative upstream-stage review records.
  - Reuse the existing validator parser and stage set unless a concrete test failure shows a required gap.
  - Keep validation structural. Do not add semantic review-quality judgment.
  - If a validator behavior change is needed, keep it scoped to the approved stage, review-log, and review-resolution relationship rules.
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-04-24-review-finding-resolution-contract`
  - `python scripts/select-validation.py --mode explicit --path scripts/test-review-artifact-validator.py --path scripts/review_artifact_validation.py --path specs/formal-review-recording.test.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-review-artifact-validator.py --path scripts/review_artifact_validation.py --path specs/formal-review-recording.test.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - `git diff --check -- scripts/test-review-artifact-validator.py scripts/review_artifact_validation.py tests/fixtures/review-artifacts docs/plans/2026-05-04-formal-review-recording.md docs/changes/2026-05-04-formal-review-recording`
- Expected observable result: repository-owned tests demonstrate that upstream detailed review files are valid, no-material detailed records do not need `review-resolution.md`, material findings still require traceable dispositions, and `pr-review` remains unsupported.
- Commit message: `M2: cover upstream formal review records`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks: tests could lock in overly specific prose or fixture shapes beyond the structural contract.
- Rollback/recovery: remove brittle assertions and replace them with stable field/path/relationship checks mapped to requirement IDs in the test spec.

### M3. Review Skill Guidance And Generated Output

- Goal: Align review-stage skills and downstream closeout guidance so contributors know when to create detailed review records and how to route material findings or no-material non-approval outcomes.
- Requirements: `R2`-`R7a`, `R11`-`R15a`.
- Files/components likely touched:
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `scripts/test-skill-validator.py` if stable skill wording assertions are needed
  - `.codex/skills/**` generated output for changed skills
  - `dist/adapters/**` generated output for changed skills
  - `docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - this plan
- Dependencies:
  - M1 contract wording stable
  - M2 validator proof for representative detailed records
  - active matching test spec
- Tests to add/update:
  - Add focused skill-validator assertions only for stable contractual phrases, such as `stage-owned non-approval outcome`, `initial review-record root`, `review-log.md`, `review-resolution.md`, `material findings`, and `pr-review`.
  - Keep broad review-quality instructions as manual proof in the test spec when automation would be brittle.
- Implementation steps:
  - Update formal review skills to describe detailed-record triggers: material findings, stage-owned non-approval outcomes that block downstream progress or require revision, reconstructed evidence, closeout evidence citation, and explicit request.
  - Clarify that clean reviews can settle artifact-locally and that no-material detailed records need `review-log.md` but not empty `review-resolution.md`.
  - Clarify that material findings still need evidence, required outcome, safe resolution or `needs-decision`, and disposition in `review-resolution.md`.
  - Clarify PR comment promotion without adding a dedicated `pr-review` stage.
  - Regenerate `.codex/skills/` and public adapter output through repository generators.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/select-validation.py --mode explicit --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path skills/workflow/SKILL.md --path skills/verify/SKILL.md --path skills/explain-change/SKILL.md --path skills/pr/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path skills/workflow/SKILL.md --path skills/verify/SKILL.md --path skills/explain-change/SKILL.md --path skills/pr/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - `git diff --check -- skills scripts/test-skill-validator.py .codex/skills dist/adapters docs/plans/2026-05-04-formal-review-recording.md docs/changes/2026-05-04-formal-review-recording`
- Expected observable result: review-stage skill users see the same detailed-record triggers and routing boundaries as the approved spec, and generated outputs match canonical skill sources.
- Commit message: `M3: align formal review skills`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks: skill wording may become too long or duplicate the feature spec instead of giving operator guidance.
- Rollback/recovery: revert the affected canonical skill sections, rerun generators, and keep M1 contracts as the source of truth while narrower skill wording is reviewed.

### M4. Final Validation And Lifecycle Closeout

- Goal: Prove the full implementation surface is coherent, update lifecycle state, and prepare the change for code review, verify, explain-change, and PR handoff.
- Requirements: `R1`-`R16b`.
- Files/components likely touched:
  - `docs/plan.md`
  - this plan
  - `docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - `docs/changes/2026-05-04-formal-review-recording/explain-change.md`
  - `specs/review-finding-resolution-contract.test.md` if `specs/review-finding-resolution-contract.md` was touched
  - `specs/rigorloop-workflow.test.md` if `specs/rigorloop-workflow.md` was touched
  - review or review-resolution artifacts if triggered by downstream review
- Dependencies:
  - M1-M3 complete
  - generated output is in sync if skills changed
  - no material review findings remain open
- Tests to add/update:
  - No new feature behavior tests beyond M1-M3 unless code-review, verify, or test-spec identifies a missing proof.
- Implementation steps:
  - Run selector-selected validation for all touched paths.
  - Run explicit artifact lifecycle validation, review artifact tests, skill checks, generated-output drift checks, adapter validation, and explicit-path CI.
  - Include `specs/review-finding-resolution-contract.test.md` and `specs/rigorloop-workflow.test.md` in final lifecycle and CI validation whenever their corresponding governing specs were touched, or record an unaffected rationale if a paired test spec intentionally remains unchanged.
  - Update `docs/plan.md`, this plan progress, validation notes, surprises, and outcome.
  - Update explain-change with final rationale and validation evidence.
  - Stop for code-review and downstream gates; do not skip review-resolution if material findings appear.
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path skills/workflow/SKILL.md --path skills/verify/SKILL.md --path skills/explain-change/SKILL.md --path skills/pr/SKILL.md --path scripts/test-review-artifact-validator.py --path scripts/review_artifact_validation.py --path scripts/test-skill-validator.py --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
  - `git diff --check --`
- Expected observable result: all touched authoritative and generated surfaces agree on the formal review recording contract, and the change has durable validation evidence ready for review handoff.
- Commit message: `M4: close formal review recording implementation`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks: final validation may reveal stale lifecycle-managed artifacts or generated output drift from referenced surfaces.
- Rollback/recovery: fix stale touched or referenced artifacts before verify; if the implementation must be abandoned, mark this plan blocked or superseded and restore the previous review recording guidance consistently.

## Validation Plan

- Use selector-selected targeted proof first for each milestone.
- Use `specs/formal-review-recording.test.md` as the requirement-to-test proof map once it is authored and active.
- Run repository-owned review artifact, skill, lifecycle, generated-output drift, adapter validation, and explicit-path CI commands named in the milestone that touches each surface.
- Use broad smoke only if `plan-review`, `test-spec`, `code-review`, `review-resolution`, `verify`, or an explicit maintainer decision adds a higher-priority trigger.
- Do not claim hosted CI status unless a hosted run is observed.

## Risks And Recovery

- Risk: contributors start creating detailed files for every clean review.
  - Recovery: keep clean review settlement artifact-local and test that no empty detailed record is required solely because a review was required.
- Risk: no-material detailed records accidentally create empty `review-resolution.md` files.
  - Recovery: keep the M2 test fixture for no-material upstream records without `review-resolution.md` and preserve the existing review-log requirement.
- Risk: review files become a second source of truth for proposal, spec, architecture, ADR, or plan status.
  - Recovery: keep artifact-local status authority explicit in governing docs and skills.
- Risk: validator changes overreach into semantic review-quality judgment.
  - Recovery: limit validator checks to paths, required fields, stable IDs, stage set, review-log relationships, and review-resolution Finding ID relationships.
- Risk: generated output drifts after skill edits.
  - Recovery: rerun `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1`, then rerun drift checks.
- Risk: proposal/spec/workflow guidance drift during implementation.
  - Recovery: update affected authoritative artifacts in the same milestone or record a deferral with owner and follow-up before downstream handoff.

## Dependencies

- `docs/proposals/2026-05-04-formal-review-recording.md` is accepted.
- `specs/formal-review-recording.md` is approved.
- `plan-review` must accept this plan before implementation.
- `specs/formal-review-recording.test.md` must be authored and active before implementation.
- Generated output depends on `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1` if canonical skills change.
- Adapter validation uses version `0.1.1`.
- No external service, network dependency, new package dependency, or issue tracker is required.

## Progress

- [x] 2026-05-04: Plan created, spec status normalized to `approved`, accepted proposal aligned with the spec's initial review-record root terminology, and `docs/plan.md` index updated.
- [x] 2026-05-04: Plan-review finding `FRR-PLAN-1` resolved by adding the existing matching test specs for `specs/review-finding-resolution-contract.md` and `specs/rigorloop-workflow.md` to M1 likely touched files, test update rules, validation commands, and M4 final validation when paired governing specs are touched.
- [x] 2026-05-04: Test spec authored at `specs/formal-review-recording.test.md` and marked active after plan-review approval.
- [x] 2026-05-04: M1 implemented by updating paired test specs first, then aligning review-resolution, workflow, operational, and governance wording with the approved stage-neutral formal review recording contract.

## Decision Log

- 2026-05-04: Architecture artifact not required -> the approved spec reuses existing review artifact paths and validator architecture without adding a new storage or parser model.
- 2026-05-04: Keep implementation in four milestones -> contract alignment, validator coverage, skill/generated output alignment, and final closeout are reviewable slices with distinct proof surfaces.
- 2026-05-04: Test spec comes after plan-review -> repository workflow requires concrete plan context before `test-spec` authoring for this non-trivial workflow change.

## Surprises And Discoveries

- `docs/project-map.md` is absent; this plan records a no-map rationale and does not rely on project-map claims.
- `scripts/review_artifact_validation.py` already recognizes all formal lifecycle review stages named by the approved spec.
- Existing validator tests include a clean review with `review-log.md` and no `review-resolution.md`, but representative upstream-stage no-material coverage still belongs in the test spec and M2.
- The change metadata validator rejects an empty inline `validation: []` placeholder. M1 records explicit validation entries instead.

## Validation Notes

- 2026-05-04: Planning-stage selector check passed:
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md`
- 2026-05-04: Planning-stage lifecycle validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md`
- 2026-05-04: Planning-stage whitespace scan found no trailing whitespace or tab matches:
  - `rg -n "[[:blank:]]$|\\t" docs/proposals/2026-05-04-formal-review-recording.md specs/formal-review-recording.md docs/plan.md docs/plans/2026-05-04-formal-review-recording.md`
- 2026-05-04: Test-spec-stage selector check passed with `broad_smoke_required: false`:
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md`
- 2026-05-04: Test-spec-stage lifecycle validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md`
- 2026-05-04: Test-spec-stage explicit CI passed:
  - `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md`
- 2026-05-04: Test-spec-stage whitespace and diff checks passed:
  - `rg -n "[[:blank:]]$|\\t|broad[_]smoke[_]required: true|broad[ ]smoke[ ]required" docs/proposals/2026-05-04-formal-review-recording.md specs/formal-review-recording.md specs/formal-review-recording.test.md docs/plan.md docs/plans/2026-05-04-formal-review-recording.md`
  - `git diff --check -- docs/proposals/2026-05-04-formal-review-recording.md specs/formal-review-recording.md specs/formal-review-recording.test.md docs/plan.md docs/plans/2026-05-04-formal-review-recording.md`
- 2026-05-04: Initial M1 change metadata validation failed because the placeholder `validation: []` was rejected by the repository metadata validator:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-formal-review-recording/change.yaml`
- 2026-05-04: M1 selector check passed with `broad_smoke_required: false`; selected checks were `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`:
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
- 2026-05-04: M1 lifecycle validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
- 2026-05-04: M1 metadata validation passed after replacing the empty placeholder with explicit validation records:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-formal-review-recording/change.yaml`
- 2026-05-04: M1 explicit CI passed with selector-selected checks:
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
- 2026-05-04: M1 whitespace and diff checks passed:
  - `rg -n '[[:blank:]]$|\\t' CONSTITUTION.md AGENTS.md docs/workflows.md docs/proposals/2026-05-04-formal-review-recording.md specs/formal-review-recording.md specs/formal-review-recording.test.md specs/review-finding-resolution-contract.md specs/review-finding-resolution-contract.test.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/plan.md docs/plans/2026-05-04-formal-review-recording.md docs/changes/2026-05-04-formal-review-recording`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md docs/proposals/2026-05-04-formal-review-recording.md specs/formal-review-recording.md specs/formal-review-recording.test.md specs/review-finding-resolution-contract.md specs/review-finding-resolution-contract.test.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/plan.md docs/plans/2026-05-04-formal-review-recording.md docs/changes/2026-05-04-formal-review-recording`

## Outcome And Retrospective

- Active. M1 contract and governance alignment is complete. M2 validator coverage has not started.

## Readiness

- Ready for M2 implementation.
- M1 is complete and committed as a milestone slice, but the full feature is not yet ready for final code review, verify, or PR handoff.
- Later implementation should continue with M2 and keep this plan's progress, decisions, discoveries, and validation notes current.

## Risks And Follow-Ups

- Follow-up: implement M2 validator coverage.
