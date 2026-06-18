# Workflow Skill Artifact-Location Map Test Spec

## Status

active

## Related spec and plan

- Spec: `specs/workflow-skill-artifact-location-map.md`
- Plan: `docs/plans/2026-06-18-workflow-skill-artifact-location-map.md`
- Proposal: `docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md`
- Spec review: `docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md`
- Plan review: `docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/plan-review-r1.md`
- Owner approval: approved for implementation on 2026-06-18.
- Architecture/ADRs: not applicable; the approved spec and plan classify this as workflow-governance, skill text, and validation work rather than runtime architecture work.

## Testing strategy

- Unit strategy: add focused parser and validation unit coverage in `scripts/test-skill-validator.py` and supporting helper tests for extracting the `Artifact registry` YAML block, parsing registry entries, comparing Markdown projections, and detecting malformed entries.
- Integration strategy: run `python scripts/validate-skills.py`, targeted skill validation, and lifecycle validation against the real `docs/workflows.md`, canonical `skills/`, and changed workflow artifacts so validation proves the repository surfaces agree.
- End-to-end strategy: use selected CI and adapter proof commands after canonical skill updates to prove the repository-owned validation path catches skill, workflow-map, and packaged-output drift.
- Smoke strategy: run `bash scripts/ci.sh --mode explicit ...` over the changed docs, skills, scripts, plan, spec, test spec, and change pack before implementation handoff and final closeout.
- Manual strategy: perform bounded cold-read checks against the finished `docs/workflows.md` and workflow skill to answer the required placement questions without chat history.
- Contract strategy: map every `MUST` requirement, example, and edge case to a stable test ID or explicit manual proof.
- Migration strategy: prove this slice does not move existing `docs/plans/*.md` files and that `docs/plans/YYYY-MM-DD-slug.md` remains the detailed plan-body contract.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R2`, `R3` | `T1`, `T14` | integration, manual | Workflow skill and guide ownership, refresh triggers, tracked-document status, and project-local map identity. |
| `R4`, `R5`, `R53` | `T2`, `T11` | integration, manual | Stage-skill content ownership and portable-default fallback for customer projects. |
| `R6`, `R7`, `R9`, `R10`, `R13` | `T3`, `T15` | unit, smoke | Canonical YAML registry structure, required fields, and validator source-of-truth behavior. |
| `R8`, `R8a`, `R8b` | `T4`, `T8` | unit | Exactly one placement representation for repository-local entries and structured non-path representation for PR handoff. |
| `R11`, `R12`, `R14` | `T5`, `T15` | unit, smoke | Markdown projection presence and registry/table contradiction detection. |
| `R15` | `T3`, `T6`, `T8`, `T9`, `T10` | unit, integration | Required artifact-type coverage in registry and projections. |
| `R16`, `R17`, `R18`, `R19`, `R20` | `T6`, `T7`, `T14` | integration, migration, manual | Plan index, detailed plan body, stale change-pack plan path rejection, historical plan retention, and governance alignment. |
| `R21`, `R42` | `T9`, `T15` | integration, smoke | Workflow skill defaults match the registry and drift is detected. |
| `R22`, `R23`, `R24`, `R25`, `R43`, `R44` | `T10`, `T15` | integration, smoke | Directly contradictory stage-skill text is edited and validated without style-only bulk edits. |
| `R26`, `R27`, `R28`, `R29`, `R30` | `T11` | unit, manual | Source rank, explicit-path limits, silent-map fallback, and unknown-artifact blocking. |
| `R31`, `R31a`, `R32`, `R33`, `R34` | `T12` | manual, integration | Formal evidence uses the change pack, detailed plan body remains outside it, and isolated advisory review remains available. |
| `R35`, `R36`, `R37`, `R37a`, `R38`, `R39`, `R46` | `T13` | unit, integration | Formal review records, review log, review resolution triggers, and invalid outside-change-pack customizations. |
| `R40`, `R41` | `T14` | manual, integration | Learn sessions remain historical rationale rather than live placement authority. |
| `R45`, `R47` | `T7`, `T11` | unit | Stale `docs/changes/<change-id>/plan.md` canonical path and unknown artifact types fail validation. |
| `R48`, `R52` | `T16` | integration, smoke | Adapter output proof uses repository-owned generation/checks and generated public adapter output is not hand-edited. |
| `R49` | `T14` | manual | Cold-read proof answers proposal-review placement, workflow-managed plan placement, and `docs/plan.md` purpose. |
| `R50`, `R51` | `T14`, `T15` | manual, smoke | Lifecycle order and artifact content schemas are preserved. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T3` | Valid registry contains `artifact_locations` and required fields. |
| `E2` | `T5`, `T6` | Markdown table agrees with `change_plan.path`. |
| `E3` | `T6`, `T14` | New workflow-managed plan path is `docs/plans/YYYY-MM-DD-slug.md`; `docs/plan.md` remains index. |
| `E4` | `T6` | Existing `docs/plans/*.md` files are retained and remain valid. |
| `E5` | `T13`, `T14` | Proposal-review record and review log route under the change pack. |
| `E6` | `T11` | Customer projects without a workflow guide use safe portable defaults or block. |
| `E7` | `T11` | Unknown artifact type blocks instead of path inference. |
| `E8` | `T8` | PR handoff can use `external_surface` or `policy` instead of `path`, but not zero or multiple placement representations. |
| `E9` | `T13` | Review customization stays under `docs/changes/<change-id>/reviews/` unless higher-priority authority permits otherwise. |

## Edge case coverage

- `EC1`: missing `docs/workflows.md` fallback and blocker behavior: `T11`
- `EC2`: partial workflow guide entry precedence and fallback: `T11`
- `EC3`: registry/table mismatch: `T5`
- `EC4`: duplicate canonical paths for one artifact type: `T4`
- `EC5`: missing registry owner or required trigger: `T3`
- `EC6`: stale `docs/changes/<change-id>/plan.md` canonical plan body: `T7`
- `EC7`: formal lifecycle recording without change ID: `T12`
- `EC8`: explicit path conflicts with higher-priority constraints: `T11`
- `EC9`: stale generated adapter archive: `T16`
- `EC10`: unparseable YAML registry: `T3`
- `EC11`: learn session contradicts registry: `T14`
- `EC12`: Markdown row missing from YAML: `T5`
- `EC13`: YAML entry missing Markdown projection: `T5`
- `EC14`: customized proposal paths apply only when safe: `T11`
- `EC14a`: customized review filenames under change-pack reviews are valid: `T13`
- `EC14b`: formal review records under `docs/reviews/` fail without higher-priority authority: `T13`
- `EC15`: no safe portable default and absent workflow guide blocks: `T11`
- `EC16`: isolated advisory review may avoid lifecycle artifact creation: `T12`
- `EC17`: clean formal review records receipt and log without creating a new empty resolution file solely for cleanliness: `T13`
- `EC18`: material review finding before change pack requires creating or requesting the change pack: `T12`, `T13`
- `EC19`: approved spec wins over stale workflow guide: `T11`
- `EC20`: adapter validation not relevant is recorded as not applicable with rationale: `T16`

## Test cases

### T1. Workflow skill owns workflow-guide creation and refresh

- Covers: `R1`, `R2`, `R3`, `AC1`, `AC2`
- Level: integration
- Fixture/setup: `skills/workflow/SKILL.md`, `docs/workflows.md`, `scripts/test-skill-validator.py`
- Steps:
  - Add or update a skill-validator test that inspects `skills/workflow/SKILL.md`.
  - Assert the workflow skill states that it creates or refreshes `docs/workflows.md` when RigorLoop is adopted, artifact locations change, or accepted placement policy contradicts the guide.
  - Assert the skill and guide describe `docs/workflows.md` as tracked workflow contract documentation and the project-local artifact-location map.
  - Run `python scripts/test-skill-validator.py -k workflow`.
- Expected result: The test passes only when the workflow skill and guide expose ownership and map identity clearly.
- Failure proves: The workflow skill can drift back into a narrative router without deterministic guide ownership.
- Automation location: `scripts/test-skill-validator.py`

### T2. Workflow skill preserves stage-skill content ownership and portable defaults

- Covers: `R4`, `R5`, `R53`, `AC13`
- Level: integration
- Fixture/setup: `skills/workflow/SKILL.md`, `skills/plan/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`
- Steps:
  - Add or update validator coverage that checks workflow-skill text for the boundary: workflow owns the project-local map, stage skills own content, schemas, stage rules, and portable defaults.
  - Inspect directly affected stage skills to ensure their portable default text remains present where safe.
  - Run `python scripts/test-skill-validator.py -k workflow`.
  - Run `python scripts/validate-skills.py skills/workflow/SKILL.md skills/plan/SKILL.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md`.
- Expected result: The workflow skill does not claim artifact content ownership and directly affected stage skills remain valid self-contained skills.
- Failure proves: The change over-centralizes placement or weakens skill-only adopter portability.
- Automation location: `scripts/test-skill-validator.py`; `scripts/validate-skills.py`

### T3. Artifact registry YAML parses and contains required fields

- Covers: `R6`, `R7`, `R9`, `R10`, `R13`, `R15`, `E1`, `EC5`, `EC10`, `AC3`, `AC6`
- Level: unit
- Fixture/setup: valid and invalid `docs/workflows.md` samples or inline fixtures in `scripts/test-skill-validator.py`
- Steps:
  - Add a parser test that extracts the fenced YAML block in `## Artifact registry`.
  - Assert the top-level key is `artifact_locations`.
  - Assert every required registry entry has `owner` and `required_when` or an equivalent trigger field.
  - Add negative fixtures for invalid YAML and missing owner or trigger.
  - Run `python scripts/test-skill-validator.py`.
- Expected result: Valid registry fixtures pass; unparseable registry or missing required fields fail with artifact-type-specific diagnostics.
- Failure proves: Validators cannot rely on the registry as the machine-checkable source of truth.
- Automation location: `scripts/test-skill-validator.py`

### T4. Registry entries have exactly one placement representation

- Covers: `R8`, `R8a`, `R8b`, `EC4`, `AC6`, `AC19`
- Level: unit
- Fixture/setup: registry fixtures with valid `path`, valid `external_surface`, valid `policy`, no placement representation, and multiple placement representations
- Steps:
  - Add tests that repository-local entries such as `proposal`, `spec`, `test_spec`, `plan_index`, `change_plan`, and review artifacts require exactly one `path`.
  - Add tests that `pr_handoff` accepts exactly one of `path`, `external_surface`, or `policy`.
  - Add negative fixtures for zero placement representations and multiple placement representations.
  - Run `python scripts/test-skill-validator.py`.
- Expected result: Valid single-representation entries pass; duplicate, missing, or ambiguous placement entries fail.
- Failure proves: The registry can encode ambiguous artifact locations.
- Automation location: `scripts/test-skill-validator.py`

### T5. Markdown artifact-location projections match the YAML registry

- Covers: `R11`, `R12`, `R14`, `E2`, `EC3`, `EC12`, `EC13`, `AC4`, `AC5`
- Level: unit
- Fixture/setup: real `docs/workflows.md` plus mismatch fixtures in `scripts/test-skill-validator.py`
- Steps:
  - Add or update tests that parse the Markdown artifact-location table rows in `docs/workflows.md`.
  - Compare each projected artifact type and path-like placement against the canonical YAML registry.
  - Add negative fixtures for a row path that contradicts YAML, a Markdown row missing from YAML, and a YAML entry missing from Markdown without a documented machine-only reason.
  - Run `python scripts/test-skill-validator.py`.
- Expected result: Registry/table agreement passes; mismatches fail with the artifact type and conflicting placement.
- Failure proves: The human guide can contradict the machine-checkable registry.
- Automation location: `scripts/test-skill-validator.py`

### T6. Plan surfaces preserve the repository-standard `docs/plans/` contract

- Covers: `R15`, `R16`, `R17`, `R18`, `R19`, `R20`, `E2`, `E3`, `E4`, `AC7`, `AC8`, `AC9`, `AC10`
- Level: integration
- Fixture/setup: `docs/workflows.md`, `CONSTITUTION.md`, `specs/rigorloop-workflow.md`, `skills/plan/SKILL.md`, existing `docs/plans/*.md`
- Steps:
  - Assert the registry documents `docs/plan.md` as the plan index only.
  - Assert the registry and Markdown projection document `docs/plans/YYYY-MM-DD-slug.md` as the detailed workflow-managed plan-body path.
  - Assert `docs/changes/<change-id>/plan.md` is not present as a competing canonical plan-body path.
  - Confirm existing `docs/plans/*.md` files are not moved or deleted by the slice.
  - Confirm `CONSTITUTION.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `skills/plan/SKILL.md` still align on `docs/plans/`.
  - Run `python scripts/test-skill-validator.py -k workflow`.
  - Run `git diff --name-status -- docs/plans`.
- Expected result: The repository has one canonical detailed plan-body location and no migration of existing plan files.
- Failure proves: The plan-location ambiguity remains or historical plan bodies were accidentally migrated.
- Automation location: `scripts/test-skill-validator.py`; manual diff inspection for no migration.

### T7. Stale change-pack plan-body path fails validation

- Covers: `R18`, `R24`, `R45`, `EC6`, `AC8`, `AC10`
- Level: unit
- Fixture/setup: negative workflow-map and skill-text fixtures that use `docs/changes/<change-id>/plan.md` as canonical detailed plan-body path
- Steps:
  - Add a failing fixture where the registry says `change_plan.path: docs/changes/<change-id>/plan.md`.
  - Add a failing fixture where workflow or directly affected stage-skill text claims `docs/changes/<change-id>/plan.md` is canonical for detailed plan bodies.
  - Allow non-canonical historical, rejected-alternative, or explanatory references when clearly labeled.
  - Run `python scripts/test-skill-validator.py`.
- Expected result: Canonical stale plan-body placement fails; clearly non-canonical historical or rejected references do not fail.
- Failure proves: Validators cannot catch the exact drift that motivated the corrected owner decision.
- Automation location: `scripts/test-skill-validator.py`

### T8. PR handoff registry representation is deterministic

- Covers: `R8a`, `R8b`, `R15`, `E8`, `AC19`
- Level: unit
- Fixture/setup: `pr_handoff` registry fixtures
- Steps:
  - Add tests where `pr_handoff` uses `external_surface: pull_request_body`.
  - Add tests where `pr_handoff` uses `policy: project_pr_process`.
  - Add negative fixtures where `pr_handoff` omits all placement fields or includes more than one of `path`, `external_surface`, and `policy`.
  - Run `python scripts/test-skill-validator.py`.
- Expected result: PR handoff is deterministic without forcing a repository-local `pr.md` path.
- Failure proves: The registry can leave PR handoff placement ambiguous.
- Automation location: `scripts/test-skill-validator.py`

### T9. Workflow skill default paths match the registry

- Covers: `R15`, `R21`, `R42`, `AC14`, `AC16`
- Level: integration
- Fixture/setup: `docs/workflows.md`, `skills/workflow/SKILL.md`
- Steps:
  - Add validation that extracts workflow skill default path guidance for required artifact types.
  - Compare workflow skill defaults to the `docs/workflows.md` registry.
  - Include `docs/plans/YYYY-MM-DD-slug.md`, `docs/plan.md`, `docs/changes/<change-id>/reviews/<stage>-r<n>.md`, `review-log.md`, `review-resolution.md`, `explain-change.md`, `verify-report.md`, and learn-session paths.
  - Run `python scripts/test-skill-validator.py -k workflow`.
  - Run `python scripts/validate-skills.py skills/workflow/SKILL.md`.
- Expected result: Workflow skill defaults and the project-local registry agree for all required artifact types.
- Failure proves: The workflow skill and `docs/workflows.md` can drift while both appear individually valid.
- Automation location: `scripts/test-skill-validator.py`; `scripts/validate-skills.py`

### T10. Directly affected stage skills do not contradict the registry

- Covers: `R22`, `R23`, `R24`, `R25`, `R43`, `R44`, `AC15`, `AC16`
- Level: integration
- Fixture/setup: `docs/workflows.md`, `skills/plan/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/workflow/SKILL.md`
- Steps:
  - Add validation for first-slice affected skills: `workflow`, `plan`, `proposal-review`, and `spec-review`.
  - Assert `plan` does not name `docs/changes/<change-id>/plan.md` as canonical detailed plan-body placement.
  - Assert proposal-review and spec-review formal records route under `docs/changes/<change-id>/reviews/<stage>-r<n>.md`.
  - Confirm the implementation did not bulk-edit unrelated lifecycle skills for wording style only.
  - Run `python scripts/test-skill-validator.py -k workflow`.
  - Run `python scripts/validate-skills.py skills/workflow/SKILL.md skills/plan/SKILL.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md`.
- Expected result: Direct contradictions fail and unrelated stage skills are not churned for style-only consistency.
- Failure proves: The dual-layer placement model remains confusing or the slice expands beyond approved scope.
- Automation location: `scripts/test-skill-validator.py`; `scripts/validate-skills.py`; `git diff --stat`

### T11. Source-rank and ambiguity behavior are explicit and enforceable

- Covers: `R26`, `R27`, `R28`, `R29`, `R30`, `R53`, `E6`, `E7`, `EC1`, `EC2`, `EC8`, `EC14`, `EC15`, `EC19`, `AC12`, `AC13`
- Level: unit
- Fixture/setup: workflow-guide and skill-text fixtures for source rank, absent guide, partial guide, unknown artifact, and explicit-path conflict
- Steps:
  - Assert `docs/workflows.md` states the source rank in the approved order.
  - Assert explicit user paths and change IDs remain subordinate to governance, schema, safety, security, and compatibility constraints.
  - Add tests or manual checks for absent guide fallback to safe portable defaults.
  - Add tests for partial guide fallback when an artifact type is omitted.
  - Add negative tests where an unknown artifact type such as `release_attestation` would otherwise be inferred from naming convention.
  - Run `python scripts/test-skill-validator.py`.
- Expected result: Known artifact types route through the approved source rank; unknown or unsafe placement blocks instead of guessing.
- Failure proves: Skills can infer paths from chat, naming convention, or stale lower-priority guidance.
- Automation location: `scripts/test-skill-validator.py`; manual review of skill wording where behavior is guidance-only.

### T12. Formal lifecycle evidence creates or identifies the change pack

- Covers: `R31`, `R31a`, `R32`, `R33`, `R34`, `EC7`, `EC16`, `EC18`
- Level: manual
- Fixture/setup: `docs/workflows.md`, `skills/workflow/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/plan/SKILL.md`
- Steps:
  - Review workflow and affected stage-skill guidance for formal lifecycle recording.
  - Confirm formal recording requires creating or identifying `docs/changes/<change-id>/` before change metadata, review records, review log, review resolution, explain-change, verify report, or change-local PR handoff evidence.
  - Confirm the detailed plan body itself is not required to live under the change pack.
  - Confirm missing change ID blocks or routes to change-ID creation.
  - Confirm isolated advisory review remains possible without lifecycle artifacts when formal recording is not claimed.
- Expected result: Change-pack-first evidence is explicit without moving plan bodies or eliminating isolated advisory behavior.
- Failure proves: Formal review/evidence placement remains ambiguous or advisory review gets over-recorded.
- Automation location: Manual review during M1; lifecycle validation over touched artifacts.

### T13. Formal review placement and review closeout rules are validated

- Covers: `R35`, `R36`, `R37`, `R37a`, `R38`, `R39`, `R46`, `E5`, `E9`, `EC14a`, `EC14b`, `EC17`, `EC18`, `AC11`, `AC20`
- Level: integration
- Fixture/setup: registry fixtures, `docs/workflows.md`, `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, review-artifact validator
- Steps:
  - Add tests that formal review records route under `docs/changes/<change-id>/reviews/`.
  - Assert proposal-review and spec-review default filenames use `proposal-review-r<n>.md` and `spec-review-r<n>.md`.
  - Add a valid fixture for customized filenames under `docs/changes/<change-id>/reviews/`.
  - Add an invalid fixture for routing formal review records to `docs/reviews/` without higher-priority authority.
  - Confirm review logs use `docs/changes/<change-id>/review-log.md`.
  - Confirm review resolution is required only for material findings, blocking outcomes, accepted dispositions, or another governing trigger.
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map`.
- Expected result: Valid change-local review placement passes; outside-change-pack review placement fails unless explicitly authorized by a higher-priority source.
- Failure proves: Review placement remains ambiguous or review-resolution becomes unconditional boilerplate.
- Automation location: `scripts/test-skill-validator.py`; `scripts/validate-review-artifacts.py`

### T14. Cold-read proof preserves workflow behavior and non-authority boundaries

- Covers: `R1`, `R16`, `R17`, `R31a`, `R40`, `R41`, `R49`, `R50`, `R51`, `E3`, `E5`, `EC11`, `AC17`, `AC18`
- Level: manual
- Fixture/setup: final `docs/workflows.md`, `skills/workflow/SKILL.md`, `docs/changes/2026-06-17-workflow-skill-artifact-location-map/behavior-preservation.md`
- Steps:
  - Cold-read the final workflow guide and workflow skill without using chat history.
  - Answer: proposal-review records go under `docs/changes/<change-id>/reviews/proposal-review-r<n>.md` unless a higher-priority source permits another path.
  - Answer: workflow-managed detailed plan bodies go under `docs/plans/YYYY-MM-DD-slug.md`.
  - Answer: `docs/plan.md` is the global lifecycle index, not a concrete plan body.
  - Confirm lifecycle stage order remains unchanged.
  - Confirm the change does not redefine proposal, spec, plan, review, verify, PR, or learn artifact content schemas.
  - Confirm learn sessions are only historical rationale unless the current rule also exists in `docs/workflows.md`, an approved spec, schema, or owning stage-skill guidance.
- Expected result: A maintainer can answer required placement questions from tracked artifacts, and no lifecycle or schema boundary changed.
- Failure proves: The change still depends on chat history or changes semantics outside the approved scope.
- Automation location: Manual cold-read proof in `docs/changes/2026-06-17-workflow-skill-artifact-location-map/behavior-preservation.md`

### T15. Selected CI proves changed workflow, skill, validation, and lifecycle surfaces together

- Covers: `R6`-`R15`, `R21`-`R25`, `R42`-`R47`, `R50`, `R51`, `AC3`-`AC6`, `AC11`-`AC16`, `AC18`
- Level: smoke
- Fixture/setup: changed workflow guide, skills, validation scripts, spec, test spec, plan, and change pack
- Steps:
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path specs/workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.test.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md`.
  - Run `git diff --check -- docs/workflows.md skills/workflow/SKILL.md skills/plan/SKILL.md skills/proposal-review/SKILL.md skills/spec-review/SKILL.md scripts/skill_validation.py scripts/test-skill-validator.py specs/workflow-skill-artifact-location-map.test.md docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md`.
  - Run selected CI with explicit paths for all changed implementation and lifecycle surfaces.
- Expected result: The repository-owned validation path passes only when the map, skills, validation code, and lifecycle artifacts agree.
- Failure proves: A local isolated check missed cross-surface drift.
- Automation location: `scripts/test-skill-validator.py`; `scripts/validate-skills.py`; `scripts/validate-artifact-lifecycle.py`; `scripts/ci.sh`

### T16. Adapter proof is current when workflow skill packaging is in scope

- Covers: `R48`, `R52`, `EC9`, `EC20`, `AC16`
- Level: smoke
- Fixture/setup: canonical `skills/workflow/SKILL.md`, adapter build scripts, `dist/adapters/README.md`, `dist/adapters/manifest.yaml`
- Steps:
  - Determine whether the changed canonical workflow skill is packaged for public adapters in this slice.
  - If packaged, run `python scripts/build-skills.py --check`.
  - If packaged, run `python scripts/test-build-skills.py`.
  - If packaged, run `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`.
  - Confirm generated public adapter skill bodies are not hand-edited in the tracked source tree.
  - If adapter proof is not relevant, record `not applicable` with rationale in the plan or change evidence.
- Expected result: Packaged workflow skill output is reproducibly current or explicitly not applicable with rationale; generated public adapter output is not hand-edited.
- Failure proves: Installed-skill behavior can drift from canonical workflow skill text or generated output was edited outside repository-owned generation.
- Automation location: `scripts/build-skills.py`; `scripts/test-build-skills.py`; `scripts/test-adapter-distribution.py`; manual diff inspection for generated-output boundaries.

## Fixtures and data

- Real repository surfaces:
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `specs/rigorloop-workflow.md`
  - `specs/installed-skill-artifact-placement-contract.md`
  - `skills/workflow/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
- New or updated validation fixtures:
  - Valid `artifact_locations` YAML registry with required entries and fields.
  - Invalid YAML registry fixture.
  - Missing `owner` and missing `required_when` fixtures.
  - Duplicate or missing placement representation fixtures.
  - Registry/table mismatch fixtures.
  - Missing Markdown projection and missing YAML entry fixtures.
  - Stale `docs/changes/<change-id>/plan.md` canonical plan-body fixture.
  - Unknown artifact type fixture such as `release_attestation`.
  - Formal review outside-change-pack fixture such as `docs/reviews/proposal-review-r1.md`.
  - Valid customized review filename under `docs/changes/<change-id>/reviews/`.
  - PR handoff `external_surface` and `policy` fixtures.
- Existing real artifacts used as compatibility data:
  - existing `docs/plans/*.md` files
  - `docs/changes/2026-06-17-workflow-skill-artifact-location-map/`

## Mocking/stubbing policy

Do not mock repository artifacts or generated outputs. Use real files for integration and smoke coverage. Unit tests may use inline or fixture Markdown/YAML snippets to exercise parser failures and drift cases, but those fixtures must mirror the documented `docs/workflows.md` registry shape.

## Migration or compatibility tests

- `T6` proves existing `docs/plans/*.md` files are not migrated and remain valid plan bodies.
- `T7` rejects the stale `docs/changes/<change-id>/plan.md` canonical plan-body contract.
- `T11` and `T13` preserve project-local customization only within the approved source-rank and review-placement boundaries.
- `T16` preserves generated-output boundaries and adapter compatibility when packaging is in scope.

## Observability verification

- Validator failures must name the failing artifact type and cause for registry parse errors, missing fields, duplicate placement representation, registry/table mismatch, stale plan path, invalid formal review path, unknown artifact type, and adapter drift.
- Cold-read proof must be recorded in change-local evidence and answer the three required placement questions without relying on chat history.
- Review and lifecycle validation must continue to expose this change's formal review outcomes through `review-log.md`, `review-resolution.md`, and clean review receipts.

## Security/privacy verification

- `T11` verifies explicit user paths remain subordinate to governance, schema, safety, security, and privacy constraints.
- Manual review confirms the registry does not require secrets, credentials, private data, host-specific paths, machine-local usernames, external telemetry, or artifact locations outside the repository.
- Generated public adapter output is validated through repository-owned scripts and is not hand-edited.

## Performance checks

- Parser and drift checks should use bounded parsing of `docs/workflows.md` and directly relevant skill files.
- Validation should not broad-scan generated output unless adapter proof is triggered by canonical packaged skill changes.
- No benchmark is required; this change is documentation, skill text, and static validation rather than runtime behavior.

## Manual QA checklist

- Cold-read `docs/workflows.md` and answer where proposal-review records go.
- Cold-read `docs/workflows.md` and answer where workflow-managed detailed plan bodies go.
- Cold-read `docs/workflows.md` and answer what `docs/plan.md` is for.
- Confirm a maintainer can distinguish the plan index, concrete plan body, and change-local evidence pack.
- Confirm formal review records are visibly under `docs/changes/<change-id>/reviews/`.
- Confirm `docs/workflows.md` stays readable as Markdown while exposing the YAML registry.
- Confirm no learn session is cited as live placement authority unless the same current rule appears in an approved source.

## What not to test and why

- Do not test lifecycle stage order changes because this spec explicitly forbids changing stage order.
- Do not test proposal, spec, plan, review, verify, PR, or learn content schemas because this spec changes placement guidance and validation, not artifact content schemas.
- Do not test a new CLI scaffold because change-pack scaffolding is out of scope.
- Do not test migration of existing `docs/plans/*.md` files into change packs because migration is explicitly out of scope.
- Do not assert a universal repository-local `pr.md` file because PR handoff may use `external_surface` or `policy`.
- Do not snapshot the entire `docs/workflows.md` file as the primary proof; validate the stable registry and table contracts instead.

## Uncovered gaps

None. Requirements that are guidance-only are covered by manual contract review and cold-read proof; validator-observable requirements are mapped to unit, integration, or smoke tests.

## Next artifacts

```text
implementation
code-review
review-resolution when triggered
ci-maintenance when triggered
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

This test spec is the active proof-planning surface for M1 through M3 in `docs/plans/2026-06-18-workflow-skill-artifact-location-map.md`. The M1 execution slice should add or update the tests named here before changing production validation logic or canonical workflow/skill behavior.
