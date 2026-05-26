# CI-Maintenance Skill Identity and Workflow Authoring Test Spec

## Status

active

## Related Spec and Plan

- Spec: [ci-maintenance-skill.md](ci-maintenance-skill.md)
- Plan: [2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md](../docs/plans/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md)
- Architecture/ADRs: not applicable; the approved plan records architecture as intentionally not required because this change uses existing authored-skill, packaged-resource, validator, and generated-adapter boundaries.

## Testing Strategy

Unit coverage lives in `scripts/test-skill-validator.py` and focused helper assertions in `scripts/skill_validation.py`. It proves front matter, resource maps, stale identifier detection, skeleton defaults, risk-map structure, and review fixtures without depending on an AI model.

Integration coverage uses `python scripts/validate-skills.py`, `python scripts/build-skills.py --check --output-dir <tmp>/skills`, `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmp>`, and `python scripts/validate-adapters.py --root <tmp> --version v0.1.5` to prove canonical skill source, generated local skill output, and generated public adapter archives agree.

Smoke coverage uses the repository CI wrapper in explicit-path mode after implementation lands. The smoke path must include the renamed skill, validator files, adapter support files, this test spec, the feature spec, and any change-local proof artifacts.

Manual coverage is limited to review of behavior-preservation and generated-output proof, plus classification of stale `ci` grep results as identifier references or generic continuous-integration prose.

Contract and migration coverage focus on the hard rename: no active `ci` skill body, no first-slice alias claim, adopter-facing migration guidance, and generated adapters containing `ci-maintenance` plus resources.

## Requirement Coverage Map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| CIM-R1, CIM-R2, CIM-R3, CIM-R3a | TCIM-001, TCIM-002, TCIM-003, TCIM-026 | unit, integration | Canonical directory and front matter metadata. |
| CIM-R4, CIM-R5, CIM-R6 | TCIM-004, TCIM-005, TCIM-006, TCIM-027 | unit, manual | Stale identifier detection, generic CI allowance, misspelling rejection, and targeted grep review. |
| CIM-R7, CIM-R8, CIM-R9, CIM-R10, CIM-R11 | TCIM-007, TCIM-008, TCIM-009, TCIM-021, TCIM-025 | unit, migration, integration | Hard rename, no duplicate active skill, no alias claim, migration guidance, and adapter proof. |
| CIM-R12, CIM-R13, CIM-R14, CIM-R15, CIM-R16, CIM-R17, CIM-R18, CIM-R19 | TCIM-010, TCIM-011, TCIM-012, TCIM-013 | unit, contract | Skill role, claim boundaries, workflow-managed handoff, and isolated invocation behavior. |
| CIM-R20, CIM-R21, CIM-R22, CIM-R23 | TCIM-014, TCIM-026 | unit, integration | Resource map exists, uses `COPY` and `READ`, and names all packaged resources. |
| CIM-R24, CIM-R25, CIM-R26, CIM-R27, CIM-R28 | TCIM-015, TCIM-016, TCIM-017 | unit, contract | Skeleton is copy-and-fill structure with required placeholders and no invented SHAs or commands. |
| CIM-R29, CIM-R30, CIM-R31, CIM-R32, CIM-R33 | TCIM-018, TCIM-019, TCIM-020 | unit, contract | Risk map is decision guidance with portable/project-specific split and fail-safe language. |
| CIM-R34, CIM-R35, CIM-R36 | TCIM-015, TCIM-022, TCIM-023 | unit, contract | PR/boundary split, safe path filters, and slow-check review behavior. |
| CIM-R37, CIM-R37a, CIM-R37b | TCIM-015, TCIM-022 | unit, security | Least-privilege default and justified permission elevation. |
| CIM-R38 | TCIM-022 | unit, security | `pull_request_target` warning for untrusted code. |
| CIM-R39, CIM-R40 | TCIM-015, TCIM-020 | unit, contract | Cache requires stable invalidation key or omission guidance. |
| CIM-R41, CIM-R42, CIM-R43 | TCIM-015, TCIM-016 | unit, contract | Deterministic install placeholders, actionable failure output, and timeouts. |
| CIM-R44, CIM-R45 | TCIM-015, TCIM-022 | unit, security | Release trigger boundary and no deployment/release-publishing template in first slice. |
| CIM-R46, CIM-R47, CIM-R48, CIM-R49 | TCIM-011, TCIM-016, TCIM-024 | unit, contract | Allowed command sources, missing-command blocker, and placeholder preservation. |
| CIM-R50, CIM-R51, CIM-R52, CIM-R53, CIM-R54 | TCIM-022, TCIM-023, TCIM-024 | unit, contract | Workflow-review fixtures for permissions, path filters, slow PR checks, risk coverage, and blockers. |
| CIM-R55, CIM-R56 | TCIM-004, TCIM-005 | unit | Validator rejects stale identifier and handoff wording. |
| CIM-R57, CIM-R58, CIM-R59, CIM-R60, CIM-R61 | TCIM-014, TCIM-015, TCIM-018, TCIM-019, TCIM-020, TCIM-026 | unit, integration | Validator proves resource files, skeleton defaults, risk-map split, and fail-safe. |
| CIM-R62, CIM-R63, CIM-R64 | TCIM-025, TCIM-026 | integration, migration | Generated adapters include renamed skill/resources, exclude active `ci`, and are derived from canonical skills. |
| CIM-R65 | TCIM-028 | manual, smoke | No `.github/workflows/*.yml` behavior changes. |
| AC-CIM-001 through AC-CIM-005 | TCIM-001, TCIM-004, TCIM-007, TCIM-008, TCIM-009, TCIM-025 | unit, integration, migration | Canonical identity, no stale body references, adapter generation, and no alias claim. |
| AC-CIM-FM-001 through AC-CIM-FM-004 | TCIM-002, TCIM-003 | unit | Front matter metadata positive and negative cases. |
| AC-CIM-006 through AC-CIM-012 | TCIM-014, TCIM-015, TCIM-018, TCIM-019, TCIM-020, TCIM-022, TCIM-023, TCIM-028 | unit, manual | Resource map, skeleton, risk map, PR/boundary split, review fixtures, and no repo workflow changes. |
| AC-CIM-013 through AC-CIM-015 | TCIM-007, TCIM-008, TCIM-009, TCIM-021, TCIM-025 | unit, integration, migration | No duplicate active skills, no alias, and hard-rename migration guidance. |
| AC-CIM-016 through AC-CIM-018 | TCIM-011, TCIM-016, TCIM-024 | unit, contract | Command source boundary and missing-command blocker. |
| AC-CIM-019 through AC-CIM-023 | TCIM-004, TCIM-018, TCIM-019, TCIM-020 | unit, contract | Portable risk map, project-specific labeling, unmapped fail-safe, and stale-identifier validation. |
| AC-CIM-024 | TCIM-025, TCIM-026 | integration, migration | Generated adapter resource proof and no hand editing. |
| AC-CIM-SEQ-001 through AC-CIM-SEQ-004 | TCIM-029 | manual, contract | Spec, plan, and review evidence preserve workflow sequencing. |
| AC-CIM-PERM-001 through AC-CIM-PERM-004 | TCIM-015, TCIM-022, TCIM-030 | unit, security | Skeleton permissions and no contradictory permission wording. |

## Example Coverage Map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 hard rename without duplicate active skills | TCIM-007, TCIM-008, TCIM-025 | Validates canonical and generated surfaces. |
| E2 stale identifier is rejected | TCIM-004, TCIM-005, TCIM-027 | Allows generic continuous-integration prose. |
| E3 workflow authoring uses known commands only | TCIM-011, TCIM-016 | Positive command-source boundary. |
| E4 missing command source blocks workflow authoring | TCIM-024 | Negative fixture must return blocker. |
| E5 portable risk map works outside RigorLoop | TCIM-018, TCIM-019 | Portable core cannot require RigorLoop-specific files. |
| E6 unmapped surfaces fail safe | TCIM-020 | Unmapped Docker/env/secret surfaces cannot silently pass. |
| E7 review flags unsafe workflow defaults | TCIM-022, TCIM-023 | Permissions, path filters, and slow PR checks. |

## Edge Case Coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 generic `CI` prose | TCIM-004, TCIM-027 | Manual grep classification plus negative validator scope. |
| EC2 stale `name: ci` | TCIM-003, TCIM-004 | Front matter failure. |
| EC3 `ci.yml` workflow filename | TCIM-028 | Filename does not change unless it is a skill-reference surface. |
| EC4 future alias support | TCIM-009 | First slice still forbids alias. |
| EC5 non-RigorLoop repository | TCIM-018, TCIM-019 | Portable risk core remains usable. |
| EC6 Dockerfile/env/secrets unmapped surface | TCIM-020 | Fail-safe route. |
| EC7 no lockfile | TCIM-015, TCIM-020 | Cache omission guidance. |
| EC8 no validation command | TCIM-024 | Block instead of inventing commands. |
| EC9 release publishing or deployment secrets | TCIM-022 | Out-of-scope workflow warning. |
| EC10 project policy allows action tags | TCIM-017 | Policy-approved references allowed; invented SHAs forbidden. |
| EC11 generated adapter omits resource | TCIM-026 | Generated-output validation fails. |
| EC12 stale direct `ci` invocation | TCIM-004, TCIM-005, TCIM-027 | Flag unless historical or migration guidance. |

## Test Cases

### TCIM-001. Canonical skill directory is renamed

- Covers: CIM-R1, CIM-R2, AC-CIM-001
- Level: integration
- Fixture/setup: Implementation branch after M1.
- Steps: Confirm `skills/ci-maintenance/SKILL.md` exists and `skills/ci/SKILL.md` is not an active canonical skill source.
- Expected result: The canonical authored skill source is `skills/ci-maintenance/SKILL.md`; no active authored `skills/ci/SKILL.md` remains.
- Failure proves: The rename was not treated as an identifier migration.
- Automation location: `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md`; targeted filesystem assertion in `scripts/test-skill-validator.py`.

### TCIM-002. Published skill front matter is normalized

- Covers: CIM-R3, CIM-R3a, AC-CIM-FM-001, AC-CIM-FM-002, AC-CIM-FM-003
- Level: unit
- Fixture/setup: Valid `ci-maintenance` skill fixture or canonical skill.
- Steps: Parse front matter and inspect `name`, `version`, and `schema-version`.
- Expected result: Front matter contains `name: ci-maintenance`, a non-empty `version`, and `schema-version: skill-readability-v1` unless the current reviewed contract names a newer schema.
- Failure proves: Published skill metadata is incomplete or stale after the rename.
- Automation location: `scripts/test-skill-validator.py`; `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md`.

### TCIM-003. Missing or stale front matter fails validation

- Covers: CIM-R3, CIM-R3a, AC-CIM-FM-004, EC2
- Level: unit
- Fixture/setup: Invalid fixtures for `name: ci`, missing `version`, and missing `schema-version`.
- Steps: Run skill validator tests against each invalid fixture.
- Expected result: Each invalid fixture fails with a clear validation error.
- Failure proves: Validator can ship a renamed skill without required published-skill metadata.
- Automation location: `tests/fixtures/skills/`; `scripts/test-skill-validator.py`.

### TCIM-004. Stale `ci` identifier references fail while generic CI prose passes

- Covers: CIM-R4, CIM-R5, CIM-R55, AC-CIM-002, AC-CIM-023, EC1, EC12
- Level: unit
- Fixture/setup: Positive fixture with generic continuous-integration prose; negative fixtures with stale skill identifier references.
- Steps: Run validator tests and targeted stale-reference scans.
- Expected result: `name: ci`, `role_name: ci`, direct `ci` invocation text, and `skills/ci/` identifier references fail when they mean the skill; generic `CI` prose and `scripts/ci.sh` references pass.
- Failure proves: The rename can leave routing or handoff ambiguity, or the validator is overbroad.
- Automation location: `scripts/test-skill-validator.py`; manual classification for targeted `rg` output.

### TCIM-005. Stale direct-invocation handoff wording fails validation

- Covers: CIM-R4, CIM-R56, AC-CIM-003, EC12
- Level: unit
- Fixture/setup: Invalid fixture containing direct handoff text such as `when ci is run` or `when \`ci\` is run`.
- Steps: Run validator tests.
- Expected result: The fixture fails unless the reference is explicitly historical or migration guidance.
- Failure proves: A renamed skill can still tell users to invoke the legacy skill.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-006. Misspelled skill identifier is rejected

- Covers: CIM-R6
- Level: unit
- Fixture/setup: Invalid fixture containing `ci-mantance` in a skill-identifier surface.
- Steps: Run validator tests.
- Expected result: The misspelling fails validation.
- Failure proves: The implementation can introduce a second bad identifier during migration.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-007. First slice uses hard rename only

- Covers: CIM-R7, CIM-R8, AC-CIM-013, E1
- Level: integration
- Fixture/setup: Canonical skills and generated adapter output after M3.
- Steps: Inspect canonical skill directories and generated adapter skill inventory.
- Expected result: `ci-maintenance` is active; `ci` is not an active skill body.
- Failure proves: The first slice shipped duplicate active routing surfaces.
- Automation location: `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmp>`; `python scripts/validate-adapters.py --root <tmp> --version v0.1.5`; `scripts/test-skill-validator.py`.

### TCIM-008. Duplicate active skill bodies fail generated-adapter validation

- Covers: CIM-R8, CIM-R63, AC-CIM-013, E1
- Level: integration
- Fixture/setup: Generated-output or compact fixture containing both active `ci` and `ci-maintenance` skill bodies.
- Steps: Run adapter validation or fixture-level validation.
- Expected result: Validation fails and identifies duplicate active skill exposure.
- Failure proves: Generated adapters can expose ambiguous routing after the rename.
- Automation location: `scripts/test-skill-validator.py` fixture and `scripts/validate-adapters.py` generated-output validation.

### TCIM-009. First slice does not claim `ci` remains callable

- Covers: CIM-R9, CIM-R10, AC-CIM-005, AC-CIM-014, EC4
- Level: unit
- Fixture/setup: Canonical skill text, adapter metadata, and migration guidance.
- Steps: Search authored skill and adapter support text for compatibility-alias claims.
- Expected result: No first-slice text claims `ci` remains callable; future alias support is described only as requiring a later approved contract.
- Failure proves: The hard rename is undermined by undocumented compatibility behavior.
- Automation location: `scripts/test-skill-validator.py`; targeted `rg` review.

### TCIM-010. Skill role is CI infrastructure authoring and review

- Covers: CIM-R12
- Level: unit
- Fixture/setup: Canonical `skills/ci-maintenance/SKILL.md`.
- Steps: Validate role and usage text.
- Expected result: The skill describes hosted CI workflow files, validation automation, and platform configuration authoring/review.
- Failure proves: The renamed skill still reads like a generic local test runner.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-011. Claim boundary forbids running validation, designing tests, waiting for CI, or claiming readiness

- Covers: CIM-R13, CIM-R14, CIM-R15, CIM-R16, CIM-R17, CIM-R46, E3
- Level: unit
- Fixture/setup: Canonical skill and negative wording fixtures.
- Steps: Validate claim-boundary text and forbidden readiness claims.
- Expected result: The skill states the boundaries and does not claim CI pass, verify readiness, branch readiness, PR readiness, release readiness, or deployment readiness.
- Failure proves: `ci-maintenance` can overclaim downstream proof or validation ownership.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-012. Workflow-managed success hands off to explain-change

- Covers: CIM-R18
- Level: unit
- Fixture/setup: Canonical skill handoff section.
- Steps: Inspect handoff rule for workflow-managed execution.
- Expected result: Successful workflow-managed `ci-maintenance` hands off to `explain-change` unless a stop condition applies.
- Failure proves: The renamed skill breaks the standard lifecycle handoff.
- Automation location: `scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.

### TCIM-013. Isolated direct invocation stays isolated

- Covers: CIM-R19
- Level: unit
- Fixture/setup: Canonical skill handoff section.
- Steps: Inspect direct-invocation rule.
- Expected result: Isolated or directly invoked `ci-maintenance` reports CI infrastructure results without implying downstream continuation.
- Failure proves: Direct use can silently enter workflow-managed downstream stages.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-014. Resource map names skeleton and risk-map resources with correct verbs

- Covers: CIM-R20, CIM-R21, CIM-R22, CIM-R23, CIM-R57, CIM-R58, AC-CIM-006, AC-CIM-007
- Level: unit
- Fixture/setup: Canonical skill and invalid resource-map fixtures.
- Steps: Parse resource map entries and compare packaged files.
- Expected result: `assets/github-workflow-skeleton.yml` is mapped with `COPY`; `references/risk-to-check-map.md` is mapped with `READ`; no packaged resource is omitted.
- Failure proves: Packaged resources can drift from the skill contract or be hidden.
- Automation location: `scripts/test-skill-validator.py`; `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md`.

### TCIM-015. Workflow skeleton has required safe defaults and placeholders

- Covers: CIM-R24, CIM-R25, CIM-R34, CIM-R37, CIM-R39, CIM-R40, CIM-R41, CIM-R42, CIM-R43, CIM-R44, AC-CIM-008, AC-CIM-010, AC-CIM-PERM-001, AC-CIM-PERM-002, EC7
- Level: unit
- Fixture/setup: `skills/ci-maintenance/assets/github-workflow-skeleton.yml`.
- Steps: Inspect skeleton YAML text for PR trigger structure, boundary trigger/job structure, `permissions: contents: read`, concurrency, job timeouts, action-reference placeholders, deterministic install placeholders, validation command placeholders, and cache-key or cache-omission guidance.
- Expected result: All required skeleton elements are present and the skeleton is copy-and-fill structure, not hidden policy prose.
- Failure proves: Authored workflows can start from an unsafe, slow, or incomplete shape.
- Automation location: `scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.

### TCIM-016. Skeleton does not invent commands

- Covers: CIM-R15, CIM-R28, CIM-R46, CIM-R48, AC-CIM-016, AC-CIM-018, E3
- Level: unit
- Fixture/setup: Skeleton asset and invalid skeleton fixture with project-specific commands not supplied by allowed sources.
- Steps: Validate skeleton placeholders and command-source language.
- Expected result: Validation command placeholders remain placeholders unless filled from an allowed command source.
- Failure proves: The skill can encode invented validation commands into reusable templates.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-017. Skeleton does not invent action SHAs

- Covers: CIM-R26, CIM-R27, EC10
- Level: unit
- Fixture/setup: Skeleton asset and invalid fixture with fabricated full-length SHA or unapproved concrete action reference.
- Steps: Validate action reference placeholders.
- Expected result: The skeleton uses `<full-length-sha-or-policy-approved-ref>` style placeholders or equivalent policy-approved placeholder language; it does not invent real SHAs.
- Failure proves: The skill can create misleading immutable-action claims.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-018. Risk map is reference guidance with portable core and project-specific extensions

- Covers: CIM-R29, CIM-R30, CIM-R31, AC-CIM-019, AC-CIM-020, AC-CIM-021, E5, EC5
- Level: unit
- Fixture/setup: `skills/ci-maintenance/references/risk-to-check-map.md`.
- Steps: Inspect headings and rows.
- Expected result: The file is decision guidance, includes a portable core, labels RigorLoop skills/adapters/validators as project-specific examples, and does not require RigorLoop files in non-RigorLoop repositories.
- Failure proves: The public skill leaks repository-specific requirements into adopter projects.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-019. Risk map derives checks from changed surfaces

- Covers: CIM-R30, AC-CIM-009, E5
- Level: unit
- Fixture/setup: Risk map reference.
- Steps: Validate table shape includes changed surface, PR coverage, boundary coverage, and notes or equivalent columns.
- Expected result: The map supports deriving PR and boundary checks from changed surfaces rather than generic checklist memory.
- Failure proves: The workflow authoring guidance remains nondeterministic.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-020. Unmapped changed surfaces fail safe

- Covers: CIM-R32, CIM-R33, CIM-R39, CIM-R40, CIM-R61, AC-CIM-022, E6, EC6, EC7
- Level: unit
- Fixture/setup: Risk map reference and fixture for Dockerfile/environment/secrets surface.
- Steps: Validate fail-safe language and fixture outcome.
- Expected result: Unmapped surfaces route to reviewer judgment, a conservative boundary check, or both; the map does not claim total risk coverage.
- Failure proves: New risk surfaces can silently receive no CI coverage.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-021. Hard-rename migration guidance is present

- Covers: CIM-R11, AC-CIM-015
- Level: migration
- Fixture/setup: `dist/adapters/README.md`, release-note surface, or adopter-facing migration note updated in M3.
- Steps: Inspect migration guidance.
- Expected result: Guidance says the skill was renamed from `ci` to `ci-maintenance` and direct invocations should be updated.
- Failure proves: Adopters do not receive the breaking-change migration path.
- Automation location: manual review plus targeted `rg`; change-local behavior-preservation proof.

### TCIM-022. Workflow review fixtures flag unsafe workflow defaults

- Covers: CIM-R35, CIM-R37, CIM-R37a, CIM-R37b, CIM-R38, CIM-R44, CIM-R45, CIM-R50, AC-CIM-011, AC-CIM-PERM-003, E7, EC9
- Level: unit
- Fixture/setup: Compact workflow review fixtures with overbroad permissions, unjustified `pull_request_target`, and out-of-scope secret-bearing release/deploy behavior.
- Steps: Run validator fixture tests.
- Expected result: Review output or validator fixture expectations flag the unsafe defaults with evidence, required outcome, and safe resolution path.
- Failure proves: The review half of the skill cannot catch high-risk workflow defaults.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-023. Workflow review fixtures flag unsafe path filters and slow PR checks

- Covers: CIM-R35, CIM-R36, CIM-R51, CIM-R52, CIM-R53, AC-CIM-011, E7
- Level: unit
- Fixture/setup: Compact workflow review fixtures with path filters that skip mapped risks and broad slow checks on every PR without justification.
- Steps: Run validator fixture tests.
- Expected result: Fixtures require findings for unsafe path filters and unjustified slow PR checks, and include risk coverage against changed surfaces.
- Failure proves: The skill can produce fast but under-covering or unnecessarily slow PR workflows.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-024. Missing validation command source returns blocker

- Covers: CIM-R47, CIM-R49, CIM-R54, AC-CIM-017, E4, EC8
- Level: unit
- Fixture/setup: Workflow-authoring fixture with no approved spec, active test spec, plan command, package script, CI convention, or explicit user command.
- Steps: Run validator fixture tests.
- Expected result: The expected output is blocked and does not invent commands.
- Failure proves: `ci-maintenance` can fabricate a project validation contract.
- Automation location: `scripts/test-skill-validator.py`.

### TCIM-025. Generated adapters expose `ci-maintenance` and not active `ci`

- Covers: CIM-R62, CIM-R63, AC-CIM-004, AC-CIM-013, AC-CIM-014, E1
- Level: integration
- Fixture/setup: Temporary adapter output directory.
- Steps: Run `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`; inspect generated inventory if validation output is not sufficiently explicit.
- Expected result: Generated adapters include `ci-maintenance`, do not expose active `ci`, and pass adapter validation.
- Failure proves: Canonical rename did not reach public generated adapters.
- Automation location: `scripts/build-adapters.py`; `scripts/validate-adapters.py`; generated-output proof artifact.

### TCIM-026. Generated output packages `ci-maintenance` resources from canonical source

- Covers: CIM-R57, CIM-R58, CIM-R59, CIM-R62, CIM-R64, AC-CIM-024, EC11
- Level: integration
- Fixture/setup: Temporary generated local skill mirror and temporary adapter archives.
- Steps: Run `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-cim-test-skills/skills`; build temporary adapters; inspect or validate generated resource files.
- Expected result: Generated output contains `assets/github-workflow-skeleton.yml` and `references/risk-to-check-map.md` under `ci-maintenance`, and the proof comes from generation, not hand edits.
- Failure proves: Packaged resources can be lost between canonical skill source and public adapters.
- Automation location: `scripts/build-skills.py`; `scripts/build-adapters.py`; `scripts/validate-adapters.py`.

### TCIM-027. Stale-reference scan is reviewed, not blindly replaced

- Covers: CIM-R4, CIM-R5, CIM-R6, EC1, EC12
- Level: manual
- Fixture/setup: Implementation diff after M1 and M3.
- Steps: Run the plan's targeted `rg` scan and classify each result as stale identifier, generic CI prose, script name, historical/migration note, or false positive.
- Expected result: Stale identifier results are fixed; allowed generic or historical uses are documented or left unchanged.
- Failure proves: The rename either misses identifier surfaces or over-edits unrelated CI language.
- Automation location: manual review supported by `rg -n "name: ci|role_name: ci|skills/ci/SKILL.md|skills/ci/|when ci is run|when \`ci\` is run|ci-mantance" skills docs specs AGENTS.md`.

### TCIM-028. Repository workflow behavior remains unchanged

- Covers: CIM-R65, AC-CIM-012, EC3
- Level: manual
- Fixture/setup: Implementation diff.
- Steps: Inspect `git diff -- .github/workflows` and any workflow filename changes.
- Expected result: No `.github/workflows/*.yml` behavior changes appear in this slice; `ci.yml` is not renamed solely because the skill was renamed.
- Failure proves: The change exceeded the approved first-slice boundary.
- Automation location: manual diff review; `git diff -- .github/workflows`.

### TCIM-029. Lifecycle sequencing remains plan-review before test-spec before implementation

- Covers: AC-CIM-SEQ-001, AC-CIM-SEQ-002, AC-CIM-SEQ-003, AC-CIM-SEQ-004
- Level: contract
- Fixture/setup: Spec, plan, plan-review record, and this test spec.
- Steps: Validate lifecycle artifacts and inspect `Next artifacts`, architecture-skip rationale, and plan-review evidence.
- Expected result: Spec routes through plan and plan-review before test-spec; architecture skip rationale is recorded; implementation remains downstream of test-spec.
- Failure proves: The lifecycle ordering regression from `CIM-SR2` returned.
- Automation location: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; manual artifact review.

### TCIM-030. Permissions wording stays internally consistent

- Covers: AC-CIM-PERM-004
- Level: unit
- Fixture/setup: Spec, skill, skeleton, and validator fixture text.
- Steps: Search for contradictory wording such as `narrower elevation`.
- Expected result: No contract or skill text uses contradictory permission wording.
- Failure proves: The `CIM-SR3` regression returned.
- Automation location: `scripts/test-skill-validator.py`; targeted `rg "narrower elevation|narrower job-specific elevation"`.

### TCIM-031. Change-local behavior-preservation proof is complete

- Covers: CIM-R11, CIM-R65, AC-CIM-012, AC-CIM-015, AC-CIM-024
- Level: manual
- Fixture/setup: `docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/behavior-preservation.md` and `generated-output-proof.md` after M3.
- Steps: Review proof matrices for skill identity, workflow role, handoff wording, generated adapters, repository CI workflow behavior, workflow authoring quality, and public docs.
- Expected result: Proof records corrected identity, unchanged repository workflow behavior, generated resource packaging, and migration guidance.
- Failure proves: Required preservation evidence is incomplete even if code-level tests pass.
- Automation location: manual review; lifecycle validation for artifact presence.

## Fixtures and Data

- Positive canonical skill fixture or canonical `skills/ci-maintenance/SKILL.md`.
- Negative front matter fixtures: stale `name: ci`, missing `version`, missing `schema-version`.
- Negative stale-reference fixtures: `role_name: ci`, direct invocation `when ci is run`, direct invocation ``when `ci` is run``, `ci-mantance`.
- Positive generic CI prose fixture with `CI` and `scripts/ci.sh`.
- Skeleton fixtures: valid skeleton, missing permissions, missing concurrency, missing timeout, missing command placeholder, invented command, invented SHA.
- Risk-map fixtures: valid portable/project-specific split, missing portable core, RigorLoop rows unlabeled, missing unmapped-surface fail-safe.
- Workflow review fixtures: overbroad permissions, `pull_request_target` on untrusted code, unsafe path filters, slow comprehensive PR checks, missing command source.
- Generated-output proof data from temporary `build-skills.py` and `build-adapters.py` output directories.

## Mocking/Stubbing Policy

Use compact static fixtures for validator tests. Do not invoke an AI agent to test skill reasoning. Use temporary directories for generated local skill mirrors and public adapter archives. Do not hand-edit generated adapter output to create passing proof.

## Migration or Compatibility Tests

Migration coverage is required for the hard rename:

- `TCIM-007` and `TCIM-008` prove no duplicate active `ci` and `ci-maintenance` skill bodies.
- `TCIM-009` proves no first-slice alias claim.
- `TCIM-021` proves adopter-facing hard-rename guidance.
- `TCIM-025` proves generated adapters expose `ci-maintenance` and not active `ci`.

No compatibility alias behavior is tested as supported behavior in this first slice.

## Observability Verification

Validator failures should name the missing or stale contract surface: front matter metadata, stale identifier reference, resource-map verb, missing resource, skeleton default, risk-map split, unmapped-surface fail-safe, or generated adapter resource gap.

Generated-output proof should record the exact commands, temporary output roots, and pass/fail summaries for local skill mirror generation and adapter archive validation.

## Security/Privacy Verification

Security-focused tests verify least-privilege `permissions: contents: read`, justified broader permissions, warning against `pull_request_target` for untrusted code, no invented action SHAs, no invented secrets/tokens, no secret-bearing release/deploy template in the first slice, and cache omission when no stable invalidation key exists.

## Performance Checks

No runtime benchmark is required. Performance coverage is contract-level: the skeleton and review fixtures must preserve fast PR changed-risk checks, boundary placement for heavy checks, concurrency cancellation, and job timeouts.

## Manual QA Checklist

- Confirm targeted stale-reference scan results are classified and resolved.
- Confirm no `.github/workflows/*.yml` behavior changes are present.
- Confirm migration guidance is adopter-facing and does not claim an alias.
- Confirm behavior-preservation and generated-output proof artifacts are complete after M3.
- Confirm generated adapter proof uses temporary output from canonical skills.

## What Not to Test and Why

- Do not test actual hosted GitHub Actions execution; this slice changes skill authoring/review behavior, not repository CI workflow behavior.
- Do not test deployment or release-publishing workflows; they are out of scope.
- Do not test self-hosted runner or organization-level Actions policy.
- Do not test language-specific workflow skeletons.
- Do not test AI-generated workflow quality through model calls; deterministic fixtures and contract checks are the approved proof surface.
- Do not test a `ci` compatibility alias as supported behavior; the first slice is a hard rename.

## Uncovered Gaps

None. All `MUST` requirements, examples, edge cases, acceptance criteria, migration claims, and security boundaries have planned coverage.

## Next Artifacts

```text
implementation
code-review
review-resolution, when triggered
ci-maintenance, when triggered
explain-change
verify
pr
```

## Follow-on Artifacts

None yet.

## Readiness

Active proof surface for M1. Downstream work should use the `TCIM-*` cases and validation commands here; this test spec does not claim implementation completion, review approval, verification, branch readiness, or PR readiness.
