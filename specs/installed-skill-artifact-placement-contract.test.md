# Installed-Skill Artifact Placement Contract Test Spec

## Status

active

## Related spec and plan

- Spec: [Installed-Skill Artifact Placement Contract](installed-skill-artifact-placement-contract.md)
- Plan: [Installed-Skill Artifact Placement Contract Plan](../docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md)
- Architecture/ADRs: not applicable; the approved plan records architecture as not required for this slice.
- Reviews: [spec-review-r1](../docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/spec-review-r1.md), [plan-review-r1](../docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/plan-review-r1.md)

## Testing strategy

Unit and contract tests own the first proof layer: `scripts/test-skill-validator.py` and `scripts/skill_validation.py` should fail on missing required placement strings, missing pre-change-pack behavior, missing plan-surface distinctions, and skill/workflow placement mismatches.

Integration-style repository checks prove the edited public skills remain valid, generated skill output is current, adapter output can be generated from canonical skills, and lifecycle artifacts stay coherent. Manual proof is limited to cold-read evidence and reviewer judgment that skill wording remains concise and does not duplicate exact schemas.

No end-to-end runtime smoke is required because this change modifies repository-authored Markdown skill contracts, workflow guidance, validation checks, and generated adapter archive proof. Adapter archive build and validation are the smoke boundary for installable output.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1, R2 | T1, T2, T5 | unit, contract | Placement block and portable-default ownership. |
| R3, R4, R5 | T1, T2, T8 | unit, contract | Formal review record paths for review skills. |
| R6, R7, R10 | T1, T3 | unit, contract | Review-log path and conditional review-resolution behavior. |
| R8, R9, R12, R13 | T1, T3, T8 | unit, contract | Change-pack-first and review fallback behavior. |
| R11 | T3, T8 | unit, manual | Isolated advisory carve-out. |
| R14, R15, R16, R17 | T4, T5 | unit, contract | Lookup precedence, partial workflow guide fallback, and block behavior. |
| R18, R19 | T6, T8 | unit, contract | Plan surface disambiguation. |
| R20, R21 | T4, T5 | unit, contract | Workflow map remains synchronized and secondary to skill contract for portable defaults. |
| R22, R23 | T7, T8 | unit, manual | Public skill portability and schema-boundary preservation. |
| R24, R25 | T9 | manual, contract | First-slice boundary. |
| R26, R27, R28 | T1, T4, T6 | unit | Skill-validation ownership and drift checks. |
| R29 | T10 | smoke | Generated installable output proof. |
| R30 | T8, T11 | manual, contract | Cold-read proof. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T8 | Proposal-review path and change-pack recording text. |
| E2 | T1, T3, T8 | Spec-review pre-change-pack behavior and clean review receipt behavior. |
| E3 | T4, T5 | Partial workflow guide fallback. |
| E4 | T6, T8 | Plan-surface wording. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T3, T8 | Formal review without change ID or pack blocks or creates/requests pack. |
| EC2 | T4, T5 | Partial workflow guide uses portable default. |
| EC3 | T4, T5 | Custom workflow-guide path wins only when safe. |
| EC4 | T3 | Clean receipt and review log without empty resolution. |
| EC5 | T3, T8 | Isolated advisory review does not force lifecycle artifact creation. |
| EC6 | T10 | Generated adapter archive stale or unvalidated blocks installed-skill readiness. |
| EC7 | T6 | Ambiguous plan wording is caught. |
| EC8 | T5 | Unsafe explicit path blocks. |

## Test cases

### T1. Review skills expose required formal placement contract

- Covers: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, E1, E2
- Level: unit
- Fixture/setup: `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, negative fixtures under `tests/fixtures/skills/`, `scripts/skill_validation.py`, `scripts/test-skill-validator.py`
- Steps:
  - Add validator assertions that `proposal-review` and `spec-review` contain an `Artifact placement` section or equivalent labeled placement block.
  - Assert `proposal-review` contains `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`.
  - Assert `spec-review` contains `docs/changes/<change-id>/reviews/spec-review-r<n>.md`.
  - Assert both review skills contain `docs/changes/<change-id>/review-log.md`.
  - Assert both review skills describe `review-resolution.md` as conditional rather than unconditional.
  - Assert both review skills state that formal lifecycle review requires creating or requesting a change pack before claiming `Recording status: recorded`.
- Expected result: `python scripts/test-skill-validator.py` fails on missing or stale review placement wording and passes with compliant skill text.
- Failure proves: A skill-only adopter cannot determine formal review placement from the installed skill.
- Automation location: `scripts/test-skill-validator.py`, `scripts/skill_validation.py`

### T2. Required placement blocks are concise and stage-owned

- Covers: R1, R2, R3, R4, R5, R23
- Level: unit
- Fixture/setup: First-slice public skill files and validator fixtures.
- Steps:
  - Assert placement blocks identify the stage-owned artifact or review record.
  - Assert placement blocks state portable defaults without copying the full `docs/workflows.md` table.
  - Assert placement text points exact schema and field behavior to specs, schemas, or validators rather than duplicating it.
- Expected result: Skills carry placement defaults while preserving progressive-disclosure boundaries.
- Failure proves: The implementation either leaves placement hidden or bloats skill text with schema detail.
- Automation location: `scripts/test-skill-validator.py`; reviewer check for schema duplication.

### T3. Formal review locality and isolated advisory behavior are both preserved

- Covers: R7, R8, R9, R10, R11, R12, R13, E2, EC1, EC4, EC5
- Level: unit
- Fixture/setup: Review skill files, formal review recording skill text, and existing review-artifact validation fixtures.
- Steps:
  - Assert review skills say formal lifecycle review creates or requests the change pack when missing.
  - Assert wording applies to clean and material reviews without making locality conditional on findings.
  - Assert clean reviews record a receipt and `review-log.md` without an empty `review-resolution.md`.
  - Assert isolated advisory reviews remain possible without lifecycle artifacts unless explicitly requested.
  - Assert proposal-stage wording identifies proposal authoring as the primary change-pack creation point for workflow-managed proposals, where applicable to first-slice skills.
- Expected result: Formal lifecycle recording has one change-local home, while casual advisory review remains lightweight.
- Failure proves: The change either leaves early lifecycle placement ambiguous or forces change packs for non-recorded advisory use.
- Automation location: `scripts/test-skill-validator.py`; review of `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, and affected proposal/plan wording.

### T4. Workflow-map synchronization and partial-guide fallback are checked

- Covers: R14, R15, R20, R21, R28, E3, EC2, EC3
- Level: unit
- Fixture/setup: `docs/workflows.md`, `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, `scripts/test-skill-validator.py`
- Steps:
  - Add a deterministic check comparing first-slice skill-stated defaults to the matching `docs/workflows.md` artifact-location rows.
  - Assert `docs/workflows.md` describes itself as a project-local map and customization surface, not the only portable placement contract.
  - Assert skill wording says the workflow guide takes precedence for artifacts it specifies.
  - Assert skill wording says portable defaults fill gaps in present but partial workflow guides.
  - Add or update a negative fixture where workflow-map and skill defaults disagree, and assert validation fails.
- Expected result: Skill/workflow drift is caught, and partial workflow guides compose with portable defaults.
- Failure proves: Dual placement surfaces can drift or a partial project guide can suppress safe defaults.
- Automation location: `scripts/test-skill-validator.py`, `scripts/skill_validation.py`

### T5. Lookup precedence and unsafe-path blocking are enforceable

- Covers: R14, R15, R16, R17, R20, EC2, EC3, EC8
- Level: contract
- Fixture/setup: Skill text fixtures for lookup order, `docs/workflows.md`, and review examples.
- Steps:
  - Assert lookup wording orders explicit path/change ID, active metadata, governing spec/schema constraints, workflow guide for the artifact it specifies, portable default, and block on ambiguity.
  - Assert explicit user paths do not override governance, schema, security, or safety constraints.
  - Assert missing project-local workflow guidance falls through to safe portable defaults.
  - Assert unresolved placement ambiguity produces block wording rather than guessing.
- Expected result: The implemented wording supports custom project paths without weakening safety.
- Failure proves: A user path or workflow-map custom path can override stronger constraints, or missing map rows cause ambiguity.
- Automation location: `scripts/test-skill-validator.py`; manual review for safety wording.

### T6. Plan-surface ambiguity is detected

- Covers: R18, R19, AC8, E4, EC7
- Level: unit
- Fixture/setup: `skills/plan/SKILL.md`, `skills/plan-review/SKILL.md` if touched, other first-slice skills with plan wording, negative fixture with ambiguous "the plan" wording.
- Steps:
  - Assert affected skill text distinguishes `docs/workflows.md`, `docs/plan.md`, `docs/plans/YYYY-MM-DD-slug.md`, `docs/changes/<change-id>/change.yaml`, and change-local evidence where relevant.
  - Assert ambiguous instructions such as "update the plan" fail in validator fixtures when the intended surface can be known.
  - Assert user-facing wording uses surface names appropriate to the action: workflow map, plan index, plan body, change metadata, or review evidence.
- Expected result: Adopters can tell which plan surface to read or update.
- Failure proves: The installed skill still leaves "the plan" ambiguous.
- Automation location: `scripts/test-skill-validator.py`, `scripts/skill_validation.py`

### T7. Public-skill portability and schema-boundary checks stay intact

- Covers: R22, R23, AC11
- Level: unit
- Fixture/setup: Public skill files, existing portability checks in `scripts/test-skill-validator.py`.
- Steps:
  - Assert public skill text does not require RigorLoop repository-internal docs, scripts, reports, generated mirrors, adapter paths, or maintainer-only implementation mechanics to answer basic placement questions.
  - Assert generated-output and adapter details stay in contributor or validation surfaces rather than becoming required adopter knowledge.
  - Assert review-record field schemas and disposition semantics are not duplicated in placement blocks.
- Expected result: Installed skills are self-contained for placement without leaking maintainer internals.
- Failure proves: The public contract still depends on repository-local knowledge or duplicates schema-level truth.
- Automation location: `scripts/test-skill-validator.py`; manual review for schema-boundary quality.

### T8. Cold-read proof answers the three adopter questions

- Covers: R1-R19, R22, R30, E1, E2, E4, EC1, EC5
- Level: manual
- Fixture/setup: Installed or generated skill text for `proposal-review`, `spec-review`, and relevant plan-surface skills; cold-read record in `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/behavior-preservation.md` or equivalent change-local proof.
- Steps:
  - From skill text alone, answer: "Where does a proposal-review record go?"
  - From skill text alone, answer: "Where does a spec-review record go before a change pack exists?"
  - From skill text alone, answer: "Which plan surface should I update?"
  - Record the exact paths and sections used as evidence.
- Expected result: The answers are discoverable without reading RigorLoop repository-local docs.
- Failure proves: The installed-skill contract remains incomplete for the adopter scenario that motivated the change.
- Automation location: manual proof recorded in change-local evidence; optional helper assertions in `scripts/test-skill-validator.py`.

### T9. First-slice boundary is preserved

- Covers: R24, R25
- Level: manual
- Fixture/setup: Git diff, plan milestones, touched files.
- Steps:
  - Confirm the implementation updates `proposal-review`, `spec-review`, required plan-surface wording, `docs/workflows.md`, validators, and generated-output proof only as required.
  - Confirm it does not bulk-migrate historical artifacts.
  - Confirm it does not add CLI scaffolding for change-pack creation.
  - Confirm it does not redesign review schemas or add build-time shared partials.
- Expected result: The implementation stays inside the approved first-slice boundary.
- Failure proves: The change silently expands beyond proposal and spec scope.
- Automation location: code review and `git diff --name-only`

### T10. Generated installable output includes revised skill bodies

- Covers: R29, AC10, EC6
- Level: smoke
- Fixture/setup: Canonical `skills/`, temporary adapter output directory, adapter manifest or current release guidance.
- Steps:
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version <current-or-next-version> --output-dir <tmpdir>`, using the version selected by current repository release guidance or plan validation notes.
  - Run `python scripts/validate-adapters.py --root <tmpdir> --version <current-or-next-version>`.
  - Inspect generated installable skill output or validation evidence to confirm revised `proposal-review` and `spec-review` bodies are present.
- Expected result: Generated installable output derives from canonical skills and contains the revised placement contract.
- Failure proves: The repository source changed but the installed-skill artifact users receive is stale or unproven.
- Automation location: `scripts/build-skills.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`

### T11. Behavior-preservation matrix records contract preservation

- Covers: R30, AC9, AC11, AC12
- Level: manual
- Fixture/setup: `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/behavior-preservation.md`
- Steps:
  - Record baseline and new proof for proposal-review recording, spec-review recording, plan references, `docs/workflows.md`, custom paths, review schema ownership, and generated adapters.
  - Confirm each row reaches the preservation result required by the proposal.
  - Link validation evidence for skill text, workflow-map sync, cold-read proof, and generated output.
- Expected result: Reviewers can reconstruct what behavior was preserved or strengthened without chat history.
- Failure proves: The implementation lacks durable proof that the new placement contract preserved existing boundaries.
- Automation location: manual artifact plus artifact lifecycle validation.

## Fixtures and data

- Negative skill fixtures under `tests/fixtures/skills/` for missing placement section, missing review-record path, missing pre-change-pack behavior, ambiguous plan wording, and skill/workflow placement mismatch.
- Canonical public skill files under `skills/`.
- `docs/workflows.md` as the project-local artifact-location map.
- Temporary adapter output under `/tmp` or another untracked temporary directory for generated-output proof.
- Change-local behavior-preservation and cold-read evidence under `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/`.

## Mocking/stubbing policy

Use small text fixtures for negative skill-validation cases. Do not mock repository-owned build or adapter validation commands for final proof; run them against canonical source and temporary generated output. Manual cold-read proof may quote short path strings and section names but should not depend on chat-only context.

## Migration or compatibility tests

- T4 and T5 cover existing project-local workflow maps and partial guide fallback.
- T9 covers no bulk migration of historical artifacts.
- T10 covers generated installable output compatibility.
- T11 covers behavior preservation for custom paths, schema ownership, and generated adapters.

## Observability verification

- Skill-validation output must name missing placement strings, missing pre-change-pack behavior, plan-surface ambiguity, or skill/workflow mismatch clearly enough to fix.
- Review logs and `change.yaml` must record validation evidence for this change.
- Generated adapter validation output must be recorded in change-local metadata or validation notes when M3 runs.

## Security/privacy verification

- T5 verifies explicit paths cannot override governance, schema, security, or safety constraints.
- T7 verifies public skills do not expose repository-private internals, local runtime paths, generated mirrors, or maintainer-only implementation details as required adopter knowledge.
- Final diff review checks generated temporary output is not committed and no secrets or host-specific paths are introduced.

## Performance checks

Validation should remain deterministic and text/fixture based. No benchmark is required. If skill validation becomes noticeably slow, record the command timing in validation notes and narrow checks to stable strings and fixture roots.

## Manual QA checklist

- [ ] Read `proposal-review` as a skill-only adopter and answer where formal proposal-review records go.
- [ ] Read `spec-review` as a skill-only adopter and answer what happens before a change pack exists.
- [ ] Read affected plan wording and identify whether the instruction means workflow map, plan index, plan body, change metadata, or review evidence.
- [ ] Confirm `docs/workflows.md` is a synchronized project-local map, not the only placement contract.
- [ ] Confirm exact review-record schema details remain outside the placement blocks.

## What not to test and why

- Do not test full review-record schema redesign; it is out of scope and owned by formal review recording specs and validators.
- Do not test CLI scaffolding for creating change packs; the proposal explicitly defers that work.
- Do not test historical artifact migration; the first slice does not move existing records.
- Do not rely on snapshots alone for skill text; behavioral assertions must check required path strings and boundary wording.
- Do not run live external install smoke; repository-owned generated adapter validation is the installable-output proof for this slice.

## Uncovered gaps

None. If implementation discovers that current adapter version selection is ambiguous, record a plan validation-note blocker or return to plan before claiming M3 generated-output proof.

## Next artifacts

```text
implement M1
code-review M1
implement M2
code-review M2
implement M3
code-review M3
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Active proof surface for implementation. The active plan `Current Handoff Summary` owns the next workflow action.
