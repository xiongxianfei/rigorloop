# Formal Review Recording Test Spec

## Status

- active

## Related spec and plan

- Spec: [Formal Review Recording](formal-review-recording.md), approved.
- Original proposal: [Formal Review Recording](../docs/proposals/2026-05-04-formal-review-recording.md), accepted.
- Amendment proposal: [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md), accepted.
- Output guardrail proposal: [Review Skill Recording and Status Output Guardrail](../docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md), accepted.
- Historical plan: [Formal Review Recording Implementation Plan](../docs/plans/2026-05-04-formal-review-recording.md), done.
- Historical amendment plan: [Review Skill Material Finding Recording Execution Plan](../docs/plans/2026-05-07-review-skill-material-finding-recording.md), done.
- Current output guardrail plan: [Review Skill Recording and Status Output Guardrail Plan](../docs/plans/2026-05-12-review-skill-recording-output-guardrail.md), active.
- Architecture: not required. The approved spec and accepted plan reuse the existing `docs/changes/<change-id>/reviews/`, `review-log.md`, `review-resolution.md`, and review-artifact validator model without adding a new storage architecture, parser architecture, persistence layer, deployment path, or integration boundary.
- Spec-review: approved after the initial review-record root was split into material and no-material variants.
- Output guardrail architecture: no architecture impact; architecture-review approved the no-impact rationale on 2026-05-12 with no material findings.
- Output guardrail spec-review: approved after `SR1` revised `R30` to require status sync or `Status sync: blocked`.
- Output guardrail plan-review: approved on 2026-05-12 with no material findings; `test-spec` is the immediate next handoff before implementation.

## Testing strategy

- Use unit and integration tests around `scripts/test-review-artifact-validator.py` and `scripts/review_artifact_validation.py` for executable review artifact structure: allowed stages, unsupported `pr-review`, review-log indexing, material Finding ID traceability, and no-material detailed records without `review-resolution.md`.
- Use existing change metadata validation for `change.yaml.review` aggregate fields when a change-local root is created.
- Use manual contract review for contributor-facing workflow, governance, proposal/spec/plan source-of-truth boundaries, and no-empty-boilerplate rules that are not semantic validator behavior.
- Use focused skill-validator assertions only for stable contractual review guidance terms when canonical review-stage skills change.
- Use static assertions for the current amendment: canonical shared block existence, byte-equality across the five formal review skills, placement outside stage-specific guidance, isolated material-review output fields, broad material-finding trigger wording, governance alignment, and the structural-only first-slice boundary.
- Use static assertions for the 2026-05-12 output guardrail: review-status, recording-status, recording-blocker, status-sync, status-artifact, status-sync-blocker, complete material-finding shape, change ID selection, artifact-specific status targets, and generated-output alignment across the five formal review skills.
- Use manual contract checks for status-sync behavior that depends on review result interpretation, edit permission, or artifact-specific lifecycle ownership. The first slice does not add semantic runtime validation for whether a review result should have been clean or approving.
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
| `R17`-`R17e` | `T17`, `T20` | contract, integration | Isolation controls handoff only; material findings require durable change-local review records before fixes or reconstruction when late |
| `R18`-`R19a` | `T18` | contract, integration | Tracked artifact definition and operational materiality shortcut stay visible without replacing Constitution authority |
| `R20`-`R20c` | `T17` | contract, integration | Isolated material-review output names handoff status, Finding IDs, required review record path, record-before-fixing or reconstruction status, and owner-decision status |
| `R21`-`R21d` | `T19` | integration | Shared `## Isolation and Recording` block is canonical, byte-equal, and placement-safe |
| `R22`-`R22b` | `T18` | manual, integration | `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` teach the same broad rule |
| `R23` | `T20` | integration, manual | First-slice validation remains structural/static and does not add semantic edit-reference flagging |
| `R24`-`R24b` | `T21`, `T22` | integration, manual | Review verdict, recording status, and status sync stay separate |
| `R25`-`R28a` | `T21` | integration, manual | Recording status vocabulary, blockers, complete material-finding shape, and change ID selection |
| `R29`-`R31b` | `T22` | integration, manual | Status-sync vocabulary, edit-permission blocker, and artifact-specific target table |
| `R32`-`R33a` | `T21`, `T22`, `T23` | integration, manual | Formal review final output shape, consistent skill guidance, and generated output refresh |
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
| `E7` | `T17` | Direct material review findings create the material review-record root before edits |
| `E8` | `T17` | Late isolated-review capture is reconstructed with source, timing, evidence, Finding IDs, and fidelity-loss disclosure |
| `E9` | `T17` | Isolated material review output names the required recording obligation |
| `E10` | `T19` | Formal review skills share byte-identical `Isolation and Recording` guidance from the canonical template |
| `E11` | `T21` | Material finding output reports `Recording status: recorded` and required artifact paths |
| `E12` | `T21` | No-material detailed record reports recorded state without empty `review-resolution.md` |
| `E13` | `T22` | Clean proposal review synchronizes proposal status to `accepted` |
| `E14` | `T22` | Explicit no-edit isolated review blocks status sync and reports manual action |
| `E15` | `T22` | Ambiguous status target blocks status sync instead of guessing |
| `E16` | `T22` | Clean code-review result updates plan-owned milestone state rather than source status |

## Edge case coverage

- Clean required `proposal-review` with artifact-local status and decision log only: `T3`, `T11`
- Clean required `spec-review` with readiness text and no detailed-record trigger: `T3`, `T11`
- `plan-review` with `rethink` and no material findings: `T5`, `T10`
- Material `architecture-review` before any change-local root exists: `T4`
- Isolated review-only material finding, even when downstream handoff stops: `T17`
- Isolated finding later driving tracked changes: `T17`
- Material PR comment added directly to `review-resolution.md` without durable Finding ID: `T9`, `T13`
- Unsupported `pr-review-r1.md` before a later spec extends the stage set: `T1`
- `change.yaml.review` optional pointers without dropping `status` or `unresolved_items`: `T8`
- Detailed review file with no material findings still needing `review-log.md`: `T5`, `T13`
- Reconstructed detailed review evidence needing reconstructed-record metadata: `T6`
- Final PR-ready handoff with only the initial review-record root and no durable Markdown reasoning: `T15`
- Isolated material review output missing Finding IDs, record path, record-before-fixing or reconstruction status, or owner-decision status: `T17`
- Skill-specific guidance inserted inside the shared `## Isolation and Recording` block: `T19`
- Generated adapter output changed because of a material review finding as a tracked artifact edit: `T18`
- Clean `proposal-review` status sync from `draft` to `accepted`: `T22`
- Clean `spec-review` status sync from `draft` to `approved`: `T22`
- Clean `architecture-review` status sync using architecture or ADR lifecycle vocabulary: `T22`
- `plan-review` approval updating plan readiness/index state only when those surfaces own state: `T22`
- `code-review` clean result updating active plan or review-owned milestone state without editing source files solely for review status: `T22`
- Review-only request with explicit no-edit instructions reporting `Status sync: blocked`: `T22`
- Formal review output with `Recording status: not-required` and `Status sync: updated`: `T21`, `T22`
- Formal review output with `Recording status: recorded` and `Status sync: blocked`: `T21`, `T22`

## Milestone coverage map

| Milestone | Covered by | Notes |
| --- | --- | --- |
| `M1` Contract And Governance Alignment | `T2`, `T7`, `T8`, `T11`, `T16` | Governing contracts, matched governing test specs, and source-of-truth boundaries |
| `M2` Review Artifact Validator Coverage | `T1`, `T3`, `T4`, `T5`, `T6`, `T9`, `T10`, `T13`, `T14` | Executable structural review artifact proof |
| `M3` Review Skill Guidance And Generated Output | `T2`, `T7`, `T9`, `T10`, `T12`, `T14` | Review-stage operator guidance, generated mirrors, and adapters |
| `M4` Final Validation And Lifecycle Closeout | `T13`, `T14`, `T15`, `T16` | Full touched-surface validation and lifecycle handoff evidence |
| `2026-05-07` M1 proof map and static validator coverage | `T17`, `T18`, `T19`, `T20` | Broad material-finding rule, shared review-skill block, governance alignment, isolated output fields, and structural-only validator scope |
| `2026-05-07` M2 authored guidance | `T17`, `T18`, `T19` | Canonical shared block and copied formal review skill guidance |
| `2026-05-07` M3 generated output | `T12`, `T19` | Generated Codex mirrors and public adapters reflect canonical formal review skill changes |
| `2026-05-07` M4 closeout | `T13`, `T15`, `T16`, `T20` | Review artifacts, lifecycle state, paired governing test specs, and final validation remain synchronized |
| `2026-05-12` M1 recording-status guardrail | `T21`, `T23` | Review output recording status, blocker fields, complete finding shape, and static skill validation |
| `2026-05-12` M2 artifact-status sync guardrail | `T22`, `T23` | Status-sync output, artifact-specific targets, edit-permission blockers, and static skill validation |
| `2026-05-12` M3 generated output and closeout | `T12`, `T13`, `T14`, `T15`, `T23` | Generated skills/adapters, closeout evidence, change-local validation, and final explicit validation |

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

### T17. Isolated material reviews require change-local records and complete final output

- Covers: `R2c`, `R2d`, `R5a`, `R17`-`R17e`, `R20`-`R20c`, `E7`, `E8`, `E9`, edge cases 5, 6, 13, 14, 15
- Level: contract, integration
- Fixture/setup:
  - `templates/shared/review-isolation-and-recording.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `scripts/test-review-artifact-validator.py`
- Steps:
  - Add static assertions that an isolated material-review output states no automatic downstream handoff, material Finding IDs, required review record path, whether the record must be created before fixing or reconstructed, and whether owner decision is needed.
  - Assert the output makes the next action clear without requiring enum-style action strings.
  - Assert the formal review skills do not offer review-output-only or artifact-local-only settlement for material findings.
  - Add or update review-artifact fixture coverage proving a direct material review record creates `change.yaml`, `review-log.md`, `review-resolution.md`, and `reviews/<stage>-r<n>.md` before fixes, or uses reconstructed-record metadata when fixes already began.
- Expected result:
  - Isolated review requests stop downstream handoff but still make the material-finding recording obligation explicit and enforceable.
- Failure proves:
  - Direct review requests can still be misread as exempt from material-finding recording.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`

### T18. Tracked artifact and materiality guidance uses the broad repository-file rule

- Covers: `R18`-`R19a`, `R22`-`R22b`, edge case 17
- Level: contract, integration
- Fixture/setup:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `templates/shared/review-isolation-and-recording.md`
  - the five formal review skills
- Steps:
  - Assert contributor-facing guidance defines tracked artifact as any version-controlled repository file whose change will be committed or reviewed as part of the work.
  - Assert examples include lifecycle artifacts, governance files, workflow summaries, skills, specs, schemas, scripts, generated outputs, README content, and change-local artifacts.
  - Assert ephemeral chat output, local scratch files, and unversioned drafts are excluded from tracked artifact edits.
  - Assert governance and operating guidance teach the same broad rule: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.
  - Assert the operational materiality shortcut is present without narrowing `CONSTITUTION.md` authority.
- Expected result:
  - Contributors cannot avoid recording by treating generated outputs, skills, governance files, or README content as outside tracked work.
- Failure proves:
  - The material-finding trigger can drift by file category or by conflicting governance guidance.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - manual guidance review in M1 and M4

### T19. Shared `Isolation and Recording` block is canonical and placement-safe

- Covers: `R21`-`R21d`, `E10`, edge case 16
- Level: integration
- Fixture/setup:
  - `templates/shared/review-isolation-and-recording.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert the canonical template file exists and contains one `## Isolation and Recording` block.
  - Extract the block from the `## Isolation and Recording` heading up to, but not including, the next `##` heading in the canonical source and each formal review skill.
  - Assert each copied skill block is byte-equal to the canonical template block.
  - Assert stage-specific review guidance appears only above or below the copied block, never inside it.
  - Assert `code-review` does not introduce an additive code-review-specific exception for isolation-versus-recording.
- Expected result:
  - All five formal review skills expose the same recording rule while preserving stage-specific guidance outside the shared block.
- Failure proves:
  - Manual copy-paste has drifted or a stage-specific exception weakened the shared rule.
- Automation location:
  - `python scripts/test-skill-validator.py`

### T20. First-slice validation remains structural and static

- Covers: `R16a`, `R16b`, `R23`
- Level: integration, manual
- Fixture/setup:
  - `scripts/test-skill-validator.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/review_artifact_validation.py`
  - current amendment plan
- Steps:
  - Confirm M1 adds static/shared-block assertions and structural review-artifact validation only.
  - Confirm implementation does not add semantic automation that judges whether a finding's evidence is persuasive, a suggested resolution is best, or a final action is substantively correct.
  - Confirm implementation does not add first-slice semantic flagging for tracked artifact edits that reference unresolved review findings.
  - Reuse the existing review-artifact parser and tests rather than introducing a second parser model for upstream review stages.
- Expected result:
  - The first implementation slice catches structural drift without expanding into semantic review-quality automation.
- Failure proves:
  - The implementation exceeded the approved validator scope or forked review-artifact validation.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - manual M1/M4 review

### T21. Formal review output reports recording status separately from review verdict

- Covers: `R24`-`R28a`, `R32`, `E11`, `E12`, edge cases 24 and 25
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `scripts/test-skill-validator.py`
  - representative material and no-material review artifact fixtures from `T4` and `T5`
- Steps:
  - Add static assertions that every formal review skill final output shape includes `Review status`, `Material findings`, `Recording status`, `Recording blocker`, `Review record`, `Review log`, `Review resolution`, `Open blockers`, and `Immediate next stage`.
  - Assert each formal review skill includes the exact recording-status vocabulary: `not-required`, `recorded`, and `blocked`.
  - Assert each formal review skill states that `Recording status` is not the review verdict.
  - Assert blocked recording output requires `Recording blocker` and the smallest action needed to create or update required recording artifacts.
  - Assert material-finding output guidance names complete finding shape: Finding ID, Severity, Location, Evidence, Required outcome, and Safe resolution path or `needs-decision` rationale.
  - Assert `Location` guidance accepts file/section, file/line, artifact and milestone/requirement ID, missing expected artifact path, or not-present rationale.
  - Assert change ID selection order is present or referenced for recording-required reviews without an obvious active change root.
  - Manually check that no-material detailed-record output can report `Recording status: recorded` with a review record and `review-log.md` without requiring an empty `review-resolution.md`.
- Expected result:
  - Reviewers can tell whether required recording artifacts were not required, recorded, or blocked without confusing that state with the review outcome.
- Failure proves:
  - A formal review skill can still report material findings or no-material detailed-record triggers without making durable recording completion observable.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - Manual review during 2026-05-12 M1

### T22. Clean or approving formal review output reports status sync separately from review verdict

- Covers: `R24`-`R24b`, `R29`-`R31b`, `R32`, `E13`-`E16`, edge cases 18-25
- Level: integration, manual
- Fixture/setup:
  - the five formal review skills
  - `scripts/test-skill-validator.py`
  - representative reviewed artifact examples for proposal, spec, architecture/ADR, active plan, and code-review milestone state
  - explicit no-edit review-only instruction examples
- Steps:
  - Add static assertions that every formal review skill final output shape includes `Status sync`, `Status artifact`, and `Status sync blocker`.
  - Assert each formal review skill includes the exact status-sync vocabulary: `not-required`, `updated`, and `blocked`.
  - Assert each formal review skill states that `Status sync` is not the review verdict and is not downstream workflow continuation.
  - Assert `Status sync: blocked` requires `Status sync blocker` with the intended next status, blocker, and smallest manual action.
  - Assert `Status sync: updated` requires the status artifact path and exact status field or section changed.
  - Assert explicit no-edit instructions block status sync even when the review result is clean or approving.
  - Assert formal review skills preserve artifact-specific targets: proposal `accepted`, spec `approved`, architecture `approved`, ADR `accepted` or `active` according to local lifecycle field, plan review/readiness state for `plan-review`, and active-plan or review-owned milestone state for clean `code-review`.
  - Manually confirm status-sync guidance does not tell review skills to edit source files solely to record code-review status.
- Expected result:
  - Clean or approving review output either updates the reviewed artifact's owned lifecycle/status/readiness/closeout surface or reports a concrete status-sync blocker.
- Failure proves:
  - Chat review approval can drift from durable artifact lifecycle state, or review skills can overstep isolated/no-edit boundaries.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - Manual review during 2026-05-12 M2

### T23. Formal review skill output guardrail stays consistent through generated outputs

- Covers: `R32`-`R33a`, plan 2026-05-12 M1-M3
- Level: integration, manual
- Fixture/setup:
  - canonical formal review skills
  - generated `.codex/skills/**`
  - generated `dist/adapters/**`
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - skill and adapter generation scripts
  - current change root `docs/changes/2026-05-12-review-skill-recording-output-guardrail/`
- Steps:
  - Confirm all five formal review skills contain equivalent final output fields for review status, recording status, recording blocker, status sync, status artifact, status sync blocker, review record, review log, review resolution, open blockers, and immediate next stage.
  - Confirm status-output wording lives outside the shared `## Isolation and Recording` block unless a later approved change explicitly updates the shared template and all copied blocks.
  - Run skill validator tests and skill validation after canonical skill changes.
  - Regenerate `.codex/skills/` and public adapters after canonical skill changes.
  - Run generated-output drift checks and versioned adapter validation.
  - Validate change metadata and review artifacts for the current change root during closeout.
- Expected result:
  - Canonical and generated formal review skills expose the same recording/status-sync guardrail, and the change-local evidence proves validation and closeout.
- Failure proves:
  - The guardrail is present only in canonical files, only in generated files, or inconsistently copied across review skills.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-skill-recording-output-guardrail`

## Fixtures and data

- Prefer temporary change roots in `scripts/test-review-artifact-validator.py` for focused validator scenarios.
- Add committed fixtures under `tests/fixtures/review-artifacts/**` only when reuse is clearer than inline temporary setup.
- Reuse existing review-artifact fixture conventions for `Review ID`, `Stage`, `Status`, `Finding ID`, `review-log.md`, and `review-resolution.md` syntax.
- Reuse existing change metadata fixtures under `tests/fixtures/change-metadata/**` for schema and `change.yaml` behavior.
- Use `docs/changes/2026-05-04-formal-review-recording/change.yaml` and `docs/changes/2026-05-04-formal-review-recording/explain-change.md` as durable traceability fixtures once M1 creates the change-local pack.
- Use `templates/shared/review-isolation-and-recording.md` as the canonical shared-block source for the 2026-05-07 amendment.
- Use `docs/changes/2026-05-07-review-skill-material-finding-recording/**` as current change-local evidence for material review recording and closeout behavior.
- Use `docs/changes/2026-05-12-review-skill-recording-output-guardrail/**` as current change-local evidence for review output recording/status-sync guardrails, status-sync proof, and final closeout.

## Mocking/stubbing policy

- Use temporary filesystem roots for review-artifact validator tests.
- Do not mock the review-artifact parser, change metadata validator, lifecycle validator, skill validator, or generated-output drift checks when those tools are the behavior under test.
- Do not use network, hosted CI, repository secrets, or external services for local proof.
- Manual review may inspect stable prose requirements, but it must cite concrete files and sections in plan or change-local validation notes.

## Migration or compatibility tests

- No historical change pack migration is required unless a historical artifact is touched, generated, or relied on as current authoritative guidance.
- Existing clean artifact-local review settlements remain compatible when no detailed-record trigger applied.
- Existing review-artifact validation for `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review` remains the target stage set.
- Existing review outputs do not need retroactive recording-status or status-sync fields unless touched, regenerated, or relied on as current authoritative guidance.
- The 2026-05-12 implementation must preserve artifact-specific lifecycle vocabulary and must not add a universal review-approved artifact state.
- Rollback compatibility is covered by keeping the new behavior on existing review artifact paths and validator code paths rather than adding a second path taxonomy.

## Observability verification

- `T4`, `T5`, and `T13` verify that detailed review files can be found through `review-log.md`.
- `T10` verifies that open material findings and open review-resolution closeout block downstream handoff.
- `T13` verifies failure output remains actionable by naming path, Review ID or Finding ID when available, validation mode, and short reason.
- `T21` verifies review output makes recording state observable.
- `T22` verifies review output makes artifact-status sync observable.
- `T23` verifies canonical and generated review skills expose the same output guardrail.
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
- [ ] Review changed formal review skills for byte-identical `## Isolation and Recording` guidance from the canonical template.
- [ ] Review isolated material-review output guidance for handoff status, Finding IDs, required review record path, record-before-fixing or reconstruction status, and owner-decision status.
- [ ] Review `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` for the same broad material-finding rule.
- [ ] Review generated output drift checks after canonical skill edits.
- [ ] Review final change-local artifacts for durable reasoning and no sensitive values.
- [ ] Review all five formal review skills for separate `Review status`, `Recording status`, and `Status sync` fields.
- [ ] Review complete material-finding shape guidance for `Location`, evidence, required outcome, and safe resolution or `needs-decision` rationale.
- [ ] Review artifact-specific status-sync targets for proposal, spec, architecture, ADR, plan-review, and code-review.
- [ ] Review explicit no-edit and ambiguous-target status-sync blocker behavior.

## What not to test

- Do not test semantic correctness or quality of review findings; structural validation only verifies paths, required fields, IDs, logs, and closeout relationships.
- Do not test a new `pr-review` stage as valid behavior; it is explicitly unsupported until a later approved spec extends the stage set.
- Do not require detailed review files for every clean review.
- Do not add a separate directory taxonomy per review stage.
- Do not migrate historical change packs that are not touched, generated, or relied on as current authoritative guidance.
- Do not test hosted CI status unless a hosted run is actually observed.
- Do not add semantic runtime validation that decides whether a review should have returned a clean or approving result.
- Do not test one universal artifact status for all clean reviews; artifact-specific lifecycle vocabulary remains the contract.

## Uncovered gaps

- None.

## Next artifacts

- Implementation M1 under [Review Skill Recording and Status Output Guardrail Plan](../docs/plans/2026-05-12-review-skill-recording-output-guardrail.md).
- Code review after implementation milestones complete.
- Review-resolution if material findings are produced.
- Verify.
- Explain-change.
- PR.

## Follow-on artifacts

- None yet.

## Readiness

This test spec is an active proof-planning surface for the formal review recording and 2026-05-12 review skill output guardrail amendments. Implementation may proceed under the active 2026-05-12 plan starting with M1.
