# Formal Review Recording Test Spec

## Status

- active

## Related spec and plan

- Spec: [Formal Review Recording](formal-review-recording.md), approved.
- Proposal: [Formal Review Recording](../docs/proposals/2026-05-04-formal-review-recording.md), accepted.
- Plan: [Formal Review Recording Implementation Plan](../docs/plans/2026-05-04-formal-review-recording.md), active.
- Architecture: not required. The approved spec and accepted plan reuse the existing `docs/changes/<change-id>/reviews/`, `review-log.md`, `review-resolution.md`, and review-artifact validator model without adding a new storage architecture, parser architecture, persistence layer, deployment path, or integration boundary.
- Spec-review: approved after the initial review-record root was split into material and no-material variants.
- Plan-review: approved after the paired `specs/review-finding-resolution-contract.test.md` and `specs/rigorloop-workflow.test.md` proof surfaces were added to M1 and M4.

## Testing strategy

- Use unit and integration tests around `scripts/test-review-artifact-validator.py` and `scripts/review_artifact_validation.py` for executable review artifact structure: allowed stages, unsupported `pr-review`, review-log indexing, material Finding ID traceability, and no-material detailed records without `review-resolution.md`.
- Use existing change metadata validation for `change.yaml.review` aggregate fields when a change-local root is created.
- Use manual contract review for contributor-facing workflow, governance, proposal/spec/plan source-of-truth boundaries, and no-empty-boilerplate rules that are not semantic validator behavior.
- Use focused skill-validator assertions only for stable contractual review guidance terms when canonical review-stage skills change.
- Use generated-output drift checks and adapter validation when canonical `skills/**` changes.
- Use explicit-path lifecycle validation and explicit-path CI for top-level lifecycle artifacts, workflow specs, matched test specs, change-local artifacts, validator scripts, skills, and generated output selected by the active plan.
- Treat broad smoke as unnecessary unless plan-review, test-spec review, code-review, review-resolution, verify, selector mode, release metadata, or a maintainer decision elevates it.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`-`R1b` | `T1`, `T2`, `T13` | integration, manual | Stage-neutral lifecycle stages and unsupported `pr-review` boundary |
| `R2`-`R2b` | `T2`, `T3`, `T4`, `T5`, `T6` | integration, manual | Detailed-record triggers and clean-review lightweight behavior |
| `R3`-`R3b` | `T2`, `T3`, `T4`, `T5`, `T11` | manual, integration | Artifact-local settlement only when no `R2` trigger applies |
| `R4`-`R4g` | `T4`, `T5`, `T15` | integration, manual | Material and no-material initial review-record roots plus final non-trivial pack |
| `R5`-`R5a` | `T3`, `T6` | manual | Isolated review-only omission and later reconstruction before tracked fixes |
| `R6`-`R6b` | `T4`, `T6`, `T10` | integration, manual | Material findings recorded before fixes, reconstructed repair, and no first-pass rewriting |
| `R7`-`R7a` | `T7` | manual, integration | Material finding boundary and non-material note behavior |
| `R8`-`R8c` | `T4`, `T5`, `T13` | integration | `review-log.md`, Review IDs, exact-once indexing, and no dangling ledger entries |
| `R9`-`R9b` | `T4`, `T9`, `T13` | integration, manual | Material Finding IDs originate in review records and are dispositioned traceably |
| `R10`-`R10c` | `T8` | integration, manual | `change.yaml.review` required fields and optional pointer boundaries |
| `R11`-`R11c` | `T1`, `T9` | manual, integration | PR comment promotion without automatic copying or unsupported `pr-review` stage |
| `R12`-`R12a`, `R13` | `T10` | integration, manual | Blocking first-pass outcomes need later review or explicit closeout; downstream handoff blocks while closeout is open |
| `R14`-`R14e` | `T3`, `T11` | manual | Final proposal/spec/architecture/ADR/plan status stays artifact-local |
| `R15`-`R15a` | `T12` | integration, manual | Canonical skill guidance and generated output stay aligned when skills change |
| `R16`-`R16b` | `T1`, `T4`, `T5`, `T13` | integration | Reuse existing structural validator and avoid semantic review-quality judgment |
| Security/privacy `MUST`s | `T14` | manual, integration | Review artifacts do not preserve secrets and structural validation requires no network or secrets |
| Performance `MUST` | `T14` | integration, manual | Upstream review records do not by themselves require broad smoke |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T4` | Upstream material `spec-review` findings open a material initial review-record root |
| `E2` | `T3`, `T11` | Clean `proposal-review` can settle in the reviewed artifact without empty review artifacts |
| `E3` | `T5`, `T10` | No-material `plan-review` `rethink` creates a detailed review file and no empty `review-resolution.md` |
| `E4` | `T9` | Material PR comment receives a stable Finding ID before review-resolution disposition |
| `E5` | `T8` | `change.yaml.review` remains aggregate metadata with optional pointers |
| `E6` | `T4`, `T13` | Detailed review files are indexed exactly once in `review-log.md` |

## Edge case coverage

- Clean required `proposal-review` with artifact-local status and decision log only: `T3`, `T11`
- Clean required `spec-review` with readiness text and no detailed-record trigger: `T3`, `T11`
- `plan-review` with `rethink` and no material findings: `T5`, `T10`
- Material `architecture-review` before any change-local root exists: `T4`
- Isolated review-only finding with no tracked change and no durable capture request: `T3`, `T6`
- Isolated finding later driving tracked changes: `T6`
- Material PR comment added directly to `review-resolution.md` without durable Finding ID: `T9`, `T13`
- Unsupported `pr-review-r1.md` before a later spec extends the stage set: `T1`
- `change.yaml.review` optional pointers without dropping `status` or `unresolved_items`: `T8`
- Detailed review file with no material findings still needing `review-log.md`: `T5`, `T13`
- Reconstructed detailed review evidence needing reconstructed-record metadata: `T6`
- Final PR-ready handoff with only the initial review-record root and no durable Markdown reasoning: `T15`

## Milestone coverage map

| Milestone | Covered by | Notes |
| --- | --- | --- |
| `M1` Contract And Governance Alignment | `T2`, `T7`, `T8`, `T11`, `T16` | Governing contracts, matched governing test specs, and source-of-truth boundaries |
| `M2` Review Artifact Validator Coverage | `T1`, `T3`, `T4`, `T5`, `T6`, `T9`, `T10`, `T13`, `T14` | Executable structural review artifact proof |
| `M3` Review Skill Guidance And Generated Output | `T2`, `T7`, `T9`, `T10`, `T12`, `T14` | Review-stage operator guidance, generated mirrors, and adapters |
| `M4` Final Validation And Lifecycle Closeout | `T13`, `T14`, `T15`, `T16` | Full touched-surface validation and lifecycle handoff evidence |

## Test cases

### T1. Formal lifecycle stages are stage-neutral and `pr-review` is unsupported

- Covers: `R1`, `R1a`, `R1b`, `R11c`, `R16`, `R16a`
- Level: integration
- Fixture/setup:
  - `scripts/test-review-artifact-validator.py`
  - `scripts/review_artifact_validation.py`
  - temporary change roots or focused fixtures for `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`
  - one invalid temporary change root using `Stage: pr-review` or `reviews/pr-review-r1.md`
- Steps:
  - Add or update validator tests that create one canonical detailed review file and matching `review-log.md` entry for each supported formal lifecycle stage.
  - Assert the existing review-artifact validator accepts each supported stage.
  - Assert a dedicated `pr-review` stage fails until a later approved spec extends the allowed set.
  - Confirm implementation reuses `scripts/review_artifact_validation.py` rather than introducing a second parser model.
- Expected result:
  - All five formal lifecycle stages validate through one structural review-artifact validator, and `pr-review` remains invalid.
- Failure proves:
  - Review recording remains code-review-specific, accepts unsupported PR review records, or forks the validator model.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure <change-root>`

### T2. Detailed-record trigger guidance is stage-neutral and proportional

- Covers: `R2`, `R2a`, `R2b`, `R3b`
- Level: manual, integration
- Fixture/setup:
  - `specs/review-finding-resolution-contract.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
- Steps:
  - Confirm affected workflow and review-stage guidance names every detailed-record trigger: material findings, stage-owned non-approval outcomes that block downstream progress or require revision, reconstructed review evidence, closeout evidence citation, and explicit reviewer or maintainer request.
  - Confirm stage-owned non-approval examples include `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, and equivalent blocking stage-specific outcomes.
  - Confirm clean reviews with no material findings are not made to create empty detailed files solely because the review was required.
  - Confirm artifact-local settlement is not described as sufficient when an `R2` trigger applies.
  - Add skill-validator assertions only for stable phrases when canonical skill changes make those phrases durable enough to check.
- Expected result:
  - Contributors receive the same proportional detailed-record trigger policy across governing docs and review-stage skills.
- Failure proves:
  - One stage still behaves as code-review-only, clean reviews become over-recorded, or an `R2` trigger can be bypassed by artifact-local text.
- Automation location:
  - Manual review during M1 and M3.
  - `python scripts/test-skill-validator.py` if stable skill assertions are added.
  - `bash scripts/ci.sh --mode explicit ...` for touched governance and skill paths.

### T3. Clean required reviews stay artifact-local when no detailed-record trigger applies

- Covers: `R2b`, `R3`, `R3a`, `R5`, `R14`, `R14a`, `R14b`, `R14c`, `R14d`
- Level: integration, manual
- Fixture/setup:
  - existing `scripts/test-review-artifact-validator.py` no-review-artifacts coverage
  - reviewed proposal, spec, architecture, ADR, or plan examples touched during implementation
  - workflow and review-stage guidance touched during M1 or M3
- Steps:
  - Validate that a change root without `reviews/`, `review-log.md`, or `review-resolution.md` still passes review-artifact structure checks.
  - Confirm guidance allows clean required reviews to settle through reviewed artifact status, decision log, readiness, follow-on artifacts, or closeout text.
  - Confirm isolated or review-only clean reviews do not require durable detailed files unless explicitly requested.
  - Confirm no touched guidance says proposal/spec/architecture/ADR/plan final status belongs in review files.
- Expected result:
  - Clean required reviews remain lightweight and artifact-local unless another detailed-record trigger applies.
- Failure proves:
  - The change adds empty boilerplate or makes review files a replacement source of truth for reviewed artifacts.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - Manual review during M1 and M3.

### T4. Material upstream findings create an initial review-record root with traceable dispositions

- Covers: `R2`, `R4`, `R4a`, `R4b`, `R4c`, `R4f`, `R6`, `R8`, `R8a`, `R8b`, `R8c`, `R9`, `R9a`, `R9b`
- Level: integration, manual
- Fixture/setup:
  - a temporary or committed fixture change root containing:
    - `change.yaml`
    - `review-log.md`
    - `review-resolution.md`
    - `reviews/spec-review-r1.md` or `reviews/architecture-review-r1.md`
  - at least one material `Finding ID:` in the detailed review file
- Steps:
  - Create the material upstream review fixture before applying review-driven fixes in the implementation slice that uses it.
  - Assert the detailed review file has exactly one stable `Review ID`.
  - Assert the `Review ID` appears exactly once in `review-log.md`.
  - Assert every material `Finding ID` appears in `review-resolution.md`.
  - Assert `review-resolution.md` does not reference unknown Finding IDs.
  - Add negative tests for missing `review-log.md`, missing `review-resolution.md`, missing Finding ID disposition, and unknown Finding ID disposition.
- Expected result:
  - Material upstream findings are preserved before fixes and can be traced from detailed review record to review-log to review-resolution.
- Failure proves:
  - Material findings can be acted on without durable review evidence or traceable disposition.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure <change-root>`
  - `python scripts/validate-review-artifacts.py --mode closeout <change-root>` when closeout is being claimed.

### T5. No-material non-approval reviews create detailed records without empty `review-resolution.md`

- Covers: `R2`, `R2a`, `R4`, `R4d`, `R4e`, `R8`, `R8a`, `R8b`
- Level: integration, manual
- Fixture/setup:
  - a temporary or committed fixture change root containing:
    - `change.yaml`
    - `review-log.md`
    - `reviews/plan-review-r1.md`
  - `reviews/plan-review-r1.md` has `Stage: plan-review`, `Status: rethink` or an equivalent blocking non-approval outcome, and no material `Finding ID:` lines
  - no `review-resolution.md` file
- Steps:
  - Assert the no-material upstream detailed review fixture validates structurally without `review-resolution.md`.
  - Assert `reviews/` still requires `review-log.md`.
  - Assert the review-log entry indexes the detailed review exactly once and does not list open material findings.
  - Confirm workflow guidance says `review-resolution.md` is not required solely because `reviews/` exists.
- Expected result:
  - A no-material non-approval review event is discoverable without creating an empty resolution file.
- Failure proves:
  - The implementation either loses blocking review-event evidence or creates unnecessary empty resolution artifacts.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure <change-root>`

### T6. Reconstructed review evidence repairs late durable capture without rewriting first-pass history

- Covers: `R2`, `R5a`, `R6a`, `R6b`
- Level: integration, manual
- Fixture/setup:
  - existing reconstructed-record coverage in `specs/review-finding-resolution-contract.test.md`
  - review-artifact validator reconstructed-record tests if touched
  - workflow and review-stage guidance touched during M1 or M3
- Steps:
  - Confirm reconstructed detailed review records remain valid only when they carry reconstructed-record metadata required by the review finding resolution contract.
  - Confirm isolated or review-only findings that later drive tracked changes are recorded or reconstructed before fixes rely on them.
  - Confirm corrections, decisions, fixes, and validation evidence are recorded in `review-resolution.md`, a later review round, or another explicit closeout artifact rather than by rewriting the first-pass detailed review file.
  - If the paired review finding resolution test spec is not edited while its spec changes, record an unaffected rationale before downstream handoff.
- Expected result:
  - Late capture is repaired transparently, and first-pass review evidence remains historically honest.
- Failure proves:
  - The workflow can launder late fixes into a rewritten first-pass record or rely on untracked review findings.
- Automation location:
  - `python scripts/test-review-artifact-validator.py` when reconstructed validation changes.
  - Manual review against `specs/review-finding-resolution-contract.md` and its test spec.

### T7. Material finding boundary stays explicit and non-material notes do not require disposition

- Covers: `R7`, `R7a`, `R16b`
- Level: manual, integration
- Fixture/setup:
  - formal review skills
  - governing workflow and review finding resolution specs
  - review-artifact validator positive-note or no-Finding-ID fixture
- Steps:
  - Confirm material finding wording includes changes or blocks to tracked artifacts, required disposition, scope or risk change, follow-up creation, workflow or process problem, and blocker/major/review-outcome-changing classification.
  - Confirm minor copyedits, formatting nits, positive notes, and non-actionable observations do not require `review-resolution.md` disposition unless marked material.
  - Confirm validator behavior remains structural and does not attempt to decide whether review prose is materially correct.
  - Assert a detailed review with no `Finding ID:` lines does not require `review-resolution.md`.
- Expected result:
  - Human reviewers decide materiality using the governing boundary; the validator only checks structural consequences.
- Failure proves:
  - Non-material notes become process noise, or the validator overreaches into semantic review quality.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - Manual review during M1 and M3.

### T8. `change.yaml.review` remains aggregate metadata

- Covers: `R10`, `R10a`, `R10b`, `R10c`
- Level: integration, manual
- Fixture/setup:
  - `schemas/change.schema.json`
  - `scripts/validate-change-metadata.py`
  - `tests/fixtures/change-metadata/valid-basic/change.yaml`
  - `docs/changes/2026-05-04-formal-review-recording/change.yaml` once created
- Steps:
  - Confirm `review.status` and `review.unresolved_items` remain present in valid `change.yaml` records.
  - Confirm optional `review_log` and `review_resolution` pointers may be used when review artifacts exist.
  - Confirm `change.yaml` does not duplicate detailed review records, review transcripts, or detailed finding text.
  - Confirm no schema change constrains `review.status` beyond the current project vocabulary unless a later approved schema change does so.
  - Run change metadata validation on the created change-local `change.yaml` once M1 creates it.
- Expected result:
  - `change.yaml` remains a compact aggregate and pointer surface rather than a second review ledger.
- Failure proves:
  - Review records are duplicated into metadata or existing required review fields regress.
- Automation location:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - `python scripts/test-change-metadata-validator.py` if schema or validator behavior changes.

### T9. Material PR comments are promoted before disposition without adding `pr-review`

- Covers: `R9`, `R9a`, `R11`, `R11a`, `R11b`, `R11c`
- Level: manual, integration
- Fixture/setup:
  - workflow and review-stage guidance touched during M1 or M3
  - review-artifact validator fixture where `review-resolution.md` references an unknown Finding ID
  - invalid `pr-review` fixture from `T1`
- Steps:
  - Confirm maintainer PR comments are not automatically copied into `reviews/`.
  - Confirm a material PR comment requiring disposition must first appear in a durable review record with a stable `Finding ID`.
  - Confirm the durable record may be a supported formal lifecycle review record that cites the PR comment as evidence.
  - Assert `review-resolution.md` fails when it introduces a material Finding ID absent from detailed review records.
  - Assert a dedicated `pr-review` detailed file remains unsupported.
- Expected result:
  - PR comment issues can be durably closed without inventing an unsupported review stage or creating untraceable resolution IDs.
- Failure proves:
  - Maintainer PR comments can bypass the stable Finding ID contract or silently expand the stage set.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - Manual review during M1 and M3.

### T10. Blocking first-pass outcomes require later review or explicit closeout before downstream handoff

- Covers: `R12`, `R12a`, `R13`
- Level: integration, manual
- Fixture/setup:
  - review-artifact validator closeout-mode fixtures
  - `review-log.md` entries with open and closed findings
  - `review-resolution.md` records with open and closed closeout statuses
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
- Steps:
  - Assert closeout validation fails while `review-log.md` lists open material findings.
  - Assert closeout validation fails while required `review-resolution.md` closeout remains open.
  - Confirm first-pass blocking or revision outcomes require a same-stage later review round or explicit reviewer or owner closeout evidence naming the original `Review ID`.
  - Confirm `review-resolution.md` alone is not described as silently replacing required re-review or explicit closeout.
  - Confirm `verify`, final `explain-change`, and `pr` guidance block while open material findings or required closeout remain.
- Expected result:
  - Downstream handoff cannot proceed on unresolved review history or on a resolution file that lacks the required closeout evidence.
- Failure proves:
  - Review-resolution can become a paper closeout that bypasses actual re-review or owner closeout.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout <change-root>`
  - Manual review during M3 and M4.

### T11. Artifact-local status remains the source of truth

- Covers: `R14`, `R14a`, `R14b`, `R14c`, `R14d`, `R14e`
- Level: manual
- Fixture/setup:
  - touched proposal, spec, architecture/ADR guidance if any, and plan guidance
  - `docs/proposals/2026-05-04-formal-review-recording.md`
  - `specs/formal-review-recording.md`
  - `docs/plans/2026-05-04-formal-review-recording.md`
- Steps:
  - Confirm proposal status remains in proposal files.
  - Confirm spec status remains in spec files.
  - Confirm architecture and ADR status remains in architecture artifacts or ADRs when those artifacts exist.
  - Confirm plan status remains in the plan body and plan index.
  - Confirm review files are described as review event evidence and finding closeout, not final artifact settlement.
- Expected result:
  - Review artifacts cannot override accepted proposals, approved specs, approved architecture, accepted ADRs, or active plans.
- Failure proves:
  - The change creates competing authority for lifecycle status.
- Automation location:
  - Manual review during M1 and M4.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`

### T12. Canonical review skills and generated output stay aligned

- Covers: `R15`, `R15a`
- Level: integration, manual
- Fixture/setup:
  - canonical review-stage skills under `skills/`
  - generated `.codex/skills/**`
  - generated public adapters under `dist/adapters/**`
  - skill and adapter generation scripts
- Steps:
  - Confirm canonical review-stage skills consistently describe detailed-record triggers when updated for this behavior.
  - Add skill-validator assertions only for stable contractual wording that should not drift.
  - Regenerate `.codex/skills/` and public adapter output through repository generators after canonical skill changes.
  - Run generated-output drift checks and adapter validation.
- Expected result:
  - Runtime skill mirrors and public adapters match canonical authored skill guidance.
- Failure proves:
  - Contributors using generated skill surfaces receive stale or contradictory review recording instructions.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`

### T13. Review artifact structural failure matrix remains executable

- Covers: `R8`, `R8a`, `R8b`, `R8c`, `R9`, `R9a`, `R16`, `R16a`, `R16b`
- Level: integration
- Fixture/setup:
  - existing and new review-artifact validator fixtures or temporary roots for malformed review structures
- Steps:
  - Assert missing `review-log.md` fails whenever `reviews/` exists.
  - Assert zero, duplicate, or malformed `Review ID` values fail.
  - Assert missing, duplicate, or dangling review-log entries fail.
  - Assert material Finding IDs missing from `review-resolution.md` fail.
  - Assert `review-resolution.md` Finding IDs that do not exist in review records fail.
  - Assert malformed resolution links fail.
  - Assert failure output remains actionable enough to identify the path, Review ID or Finding ID when available, validation mode, and short reason.
- Expected result:
  - The structural validator continues to protect traceability relationships while avoiding semantic review-quality judgment.
- Failure proves:
  - Malformed detailed review records can pass or the validator becomes too vague for contributors to repair.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`

### T14. Security, privacy, performance, and broad-smoke boundaries hold

- Covers: security/privacy `MUST`s, performance `MUST`
- Level: manual, integration
- Fixture/setup:
  - review artifacts and change-local artifacts created during this initiative
  - validation commands selected by the plan
  - generated output if canonical skills change
- Steps:
  - Inspect committed review records, `review-log.md`, `review-resolution.md`, `change.yaml`, and explain-change content for secrets, credentials, private keys, or sensitive runtime values.
  - Confirm PR comment promotion preserves only needed closeout evidence and does not copy sensitive context unnecessarily.
  - Confirm structural review artifact validation runs without network access or repository secrets.
  - Confirm review artifact validation remains targeted and lightweight.
  - Confirm upstream review records alone do not turn the plan broad-smoke field on.
- Expected result:
  - Review recording does not expose sensitive data, depend on network secrets, or force broad smoke without an authoritative trigger.
- Failure proves:
  - The review recording process creates privacy risk, operational coupling, or validation cost beyond the approved contract.
- Automation location:
  - Manual review during M4.
  - `python scripts/test-review-artifact-validator.py`
  - `bash scripts/ci.sh --mode explicit ...`

### T15. Final non-trivial handoff includes durable reasoning beyond any initial review-record root

- Covers: `R4a`, `R4g`
- Level: manual, integration
- Fixture/setup:
  - `docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - `docs/changes/2026-05-04-formal-review-recording/explain-change.md`
  - active plan and plan index
- Steps:
  - Confirm any initial review-record root is treated as review-event preservation, not the final non-trivial pack.
  - Confirm final handoff includes `change.yaml` plus durable Markdown reasoning such as `explain-change.md`.
  - Confirm `explain-change.md` links the proposal, spec, active test spec, active plan, material review records when present, and validation evidence.
  - Confirm `docs/plan.md` and the plan body agree on final lifecycle state before PR readiness is claimed.
- Expected result:
  - Final handoff has enough durable reasoning to review the implementation without treating the initial review root as a complete change pack.
- Failure proves:
  - The implementation can reach PR readiness with only review-event breadcrumbs and no durable rationale.
- Automation location:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-formal-review-recording/change.yaml`
  - Manual review during M4.

### T16. Paired governing test specs stay aligned when governing specs change

- Covers: plan M1, plan M4
- Level: manual, integration
- Fixture/setup:
  - `specs/review-finding-resolution-contract.md`
  - `specs/review-finding-resolution-contract.test.md`
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - active plan and change-local artifacts
- Steps:
  - If `specs/review-finding-resolution-contract.md` changes, update `specs/review-finding-resolution-contract.test.md` for new or changed proof expectations, or record an unaffected rationale before downstream handoff.
  - If `specs/rigorloop-workflow.md` changes, update `specs/rigorloop-workflow.test.md` for new or changed proof expectations, or record an unaffected rationale before downstream handoff.
  - Include touched governing specs and paired test specs in M1 selected validation, lifecycle validation, explicit CI, and diff checks.
  - Include them again in M4 final lifecycle and CI validation when their corresponding governing specs were touched.
- Expected result:
  - Governing workflow/review contracts do not drift from their matching test specs.
- Failure proves:
  - The implementation changes authoritative workflow behavior without updating or consciously preserving its proof surface.
- Automation location:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `bash scripts/ci.sh --mode explicit ...`
  - Manual M1 and M4 plan closeout review.

## Fixtures and data

- Prefer temporary change roots in `scripts/test-review-artifact-validator.py` for focused validator scenarios.
- Add committed fixtures under `tests/fixtures/review-artifacts/**` only when reuse is clearer than inline temporary setup.
- Reuse existing review-artifact fixture conventions for `Review ID`, `Stage`, `Status`, `Finding ID`, `review-log.md`, and `review-resolution.md` syntax.
- Reuse existing change metadata fixtures under `tests/fixtures/change-metadata/**` for schema and `change.yaml` behavior.
- Use `docs/changes/2026-05-04-formal-review-recording/change.yaml` and `docs/changes/2026-05-04-formal-review-recording/explain-change.md` as durable traceability fixtures once M1 creates the change-local pack.

## Mocking/stubbing policy

- Use temporary filesystem roots for review-artifact validator tests.
- Do not mock the review-artifact parser, change metadata validator, lifecycle validator, skill validator, or generated-output drift checks when those tools are the behavior under test.
- Do not use network, hosted CI, repository secrets, or external services for local proof.
- Manual review may inspect stable prose requirements, but it must cite concrete files and sections in plan or change-local validation notes.

## Migration or compatibility tests

- No historical change pack migration is required unless a historical artifact is touched, generated, or relied on as current authoritative guidance.
- Existing clean artifact-local review settlements remain compatible when no detailed-record trigger applied.
- Existing review-artifact validation for `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review` remains the target stage set.
- Rollback compatibility is covered by keeping the new behavior on existing review artifact paths and validator code paths rather than adding a second path taxonomy.

## Observability verification

- `T4`, `T5`, and `T13` verify that detailed review files can be found through `review-log.md`.
- `T10` verifies that open material findings and open review-resolution closeout block downstream handoff.
- `T13` verifies failure output remains actionable by naming path, Review ID or Finding ID when available, validation mode, and short reason.
- Successful validation may report counts for detailed reviews, findings, log entries, and closeout state, but exact counts are not required unless implemented as stable validator output.

## Security/privacy verification

- `T14` verifies no review artifacts or promoted PR comment evidence include secrets, credentials, private keys, or sensitive runtime values.
- `T14` verifies structural validation does not require network access or repository secrets.
- Skill and workflow guidance should avoid instructing contributors to copy full PR comment transcripts when narrow evidence is enough for closeout.

## Performance checks

- `T14` verifies review-artifact validation remains lightweight and targeted.
- M4 validation uses explicit-path CI and selected checks first.
- Broad smoke is out of scope unless a higher-priority trigger elevates it.

## Manual QA checklist

- [ ] Review governing contract wording for stage-neutral detailed-record triggers.
- [ ] Review clean review wording for no empty detailed files, no empty `review-log.md`, and no empty `review-resolution.md` solely because a review was required.
- [ ] Review no-material non-approval wording for `review-log.md` without mandatory empty `review-resolution.md`.
- [ ] Review artifact-local status authority for proposals, specs, architecture artifacts, ADRs, and plans.
- [ ] Review PR comment promotion wording for stable Finding IDs and unsupported `pr-review`.
- [ ] Review changed review-stage skills for the same trigger and closeout vocabulary as the approved spec.
- [ ] Review generated output drift checks after canonical skill edits.
- [ ] Review final change-local artifacts for durable reasoning and no sensitive values.

## What not to test

- Do not test semantic correctness or quality of review findings; structural validation only verifies paths, required fields, IDs, logs, and closeout relationships.
- Do not test a new `pr-review` stage as valid behavior; it is explicitly unsupported until a later approved spec extends the stage set.
- Do not require detailed review files for every clean review.
- Do not add a separate directory taxonomy per review stage.
- Do not migrate historical change packs that are not touched, generated, or relied on as current authoritative guidance.
- Do not test hosted CI status unless a hosted run is actually observed.

## Uncovered gaps

- None.

## Next artifacts

- M1 implementation under [Formal Review Recording Implementation Plan](../docs/plans/2026-05-04-formal-review-recording.md).
- Code review after implementation milestones complete.
- Review-resolution if material findings are produced.
- Verify.
- Explain-change.
- PR.

## Follow-on artifacts

- None yet.

## Readiness

This test spec is the active proof-planning surface for implementation. Implementation may proceed under the active plan starting with M1.
