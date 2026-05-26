# CI-Maintenance Skill Identity and Workflow Authoring Contract

## Status

approved

## Related proposal

- [Rename `ci` to `ci-maintenance` and Add Risk-Scoped GitHub Workflow Authoring Support](../docs/proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md), accepted.
- Proposal review records:
  - [proposal-review-r1](../docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/proposal-review-r1.md)
  - [proposal-review-r2](../docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/proposal-review-r2.md)
  - [proposal-review-r3](../docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/proposal-review-r3.md)

## Goal and context

This spec defines the contract for renaming the CI infrastructure maintenance skill from `ci` to `ci-maintenance` and improving its GitHub Actions authoring/review behavior.

The change has two workstreams:

- `ci` becomes the canonical `ci-maintenance` skill identity.
- `ci-maintenance` gains structured GitHub Actions authoring and review guidance through one workflow skeleton asset and one risk-to-check reference.

The renamed skill is for maintaining CI infrastructure. It may author or review hosted CI workflow files, validation automation, and related platform configuration. It does not run validation, design tests, invent validation commands, wait for existing CI checks, or claim verify, branch, PR, or release readiness.

This spec intentionally resolves proposal-review observation `OBS-1`: this first slice uses a hard rename. No safe non-duplicating skill alias mechanism exists in the current skill registry or adapter layer. OpenCode command aliases exist for generated command wrappers, but they are not a general skill-name alias contract. `ci` therefore does not remain callable as a compatibility alias in this slice.

This spec also resolves proposal-review observation `OBS-2`: the risk map covers common changed-surface classes and must fail safe for unmapped surfaces. The skill must not claim to mitigate every possible CI risk.

## Glossary

- `ci-maintenance`: the canonical skill identity and workflow-stage name for CI infrastructure authoring and review.
- `legacy ci`: the former skill identity `ci`.
- `active skill directory`: a skill directory shipped or installed as an independently routable skill body.
- `non-duplicating alias`: a routing mechanism that maps a legacy name to a canonical skill without installing or exposing a second active skill body.
- `workflow skeleton asset`: `skills/ci-maintenance/assets/github-workflow-skeleton.yml`, a copy-and-fill GitHub Actions workflow structure.
- `risk-to-check reference`: `skills/ci-maintenance/references/risk-to-check-map.md`, decision guidance for mapping changed surfaces to PR and boundary checks.
- `changed-risk checks`: fast checks selected from changed paths and changed risk surfaces for pull requests.
- `boundary checks`: broader or more expensive checks that run on schedule, manual dispatch, release, or another protected boundary.
- `known validation command`: a command from an approved spec, approved or active test spec, plan validation section, existing package script, existing project CI convention, or explicit user input.
- `unmapped changed surface`: a changed path or configuration surface not covered by the portable core or project-specific extension rows in the risk-to-check reference.

## Examples first

Example E1: hard rename without duplicate active skills
Given a generated adapter includes the renamed skill
When a user lists installed skills
Then `ci-maintenance` is exposed as the active skill
And `ci` is not exposed as a second active skill body.

Example E2: stale identifier is rejected
Given the canonical skill source has been renamed
When validation checks skill front matter, handoff text, workflow docs, tests, and adapter metadata
Then references that use `ci` as the skill identifier fail validation
But generic uses of CI meaning continuous integration are allowed.

Example E3: workflow authoring uses known commands only
Given a project has package script `npm test` and a test spec naming `npm run lint`
When `ci-maintenance` authors a GitHub Actions workflow
Then it may wire those commands into scoped or boundary jobs
And it does not invent unrelated commands.

Example E4: missing command source blocks workflow authoring
Given a project has no spec, test spec, plan validation command, package script, CI convention, or explicit user command for validation
When `ci-maintenance` is asked to create a workflow
Then it reports a blocker instead of inventing `<test command>` content.

Example E5: portable risk map works outside RigorLoop
Given a non-RigorLoop repository changes source code and dependency lockfiles
When `ci-maintenance` reads the risk-to-check reference
Then it uses portable source-code and dependency rows
And it does not require RigorLoop skills, generated adapters, or lifecycle validators.

Example E6: unmapped surfaces fail safe
Given a change modifies container images or environment configuration not listed in the risk map
When `ci-maintenance` derives CI coverage
Then it flags the unmapped surface for reviewer judgment or routes it to a conservative boundary check
And it does not treat the surface as having no CI risk.

Example E7: review flags unsafe workflow defaults
Given a workflow grants broad token permissions, uses narrow path filters that skip affected checks, or runs a slow comprehensive suite on every PR without justification
When `ci-maintenance` reviews the workflow
Then it reports concrete findings with evidence, required outcome, and a safe revision path.

## Requirements

### Skill identity

CIM-R1. The canonical skill name MUST be `ci-maintenance`.

CIM-R2. The canonical authored skill source MUST move from `skills/ci/SKILL.md` to `skills/ci-maintenance/SKILL.md`.

CIM-R3. The `ci-maintenance` skill front matter MUST use `name: ci-maintenance`.

CIM-R3a. The canonical `ci-maintenance` skill front matter MUST include the published-skill metadata fields required by the current skill contract:

```yaml
name: ci-maintenance
version: "1.0.0"
schema-version: skill-readability-v1
```

If the published-skill contract names a newer current schema version before implementation, the implementation MUST use that current reviewed schema version instead of `skill-readability-v1`.

CIM-R4. Canonical skill source, workflow guidance, stage-chain references, handoff text, validator allowlists, tests, fixtures, generated skill metadata, and adapter metadata MUST NOT use `ci` as the skill identifier after the rename.

CIM-R5. Generic prose where `CI` means continuous integration MAY remain unchanged.

CIM-R6. The implementation MUST reject or flag the misspelling `ci-mantance` in touched skill-identifier surfaces.

CIM-R7. The first slice MUST use a hard rename from `ci` to `ci-maintenance`.

CIM-R8. The first slice MUST NOT ship, install, or expose both `ci` and `ci-maintenance` as active skill directories.

CIM-R9. The first slice MUST NOT claim `ci` remains callable as a compatibility alias.

CIM-R10. A future compatibility alias for `ci` MAY be added only through a later approved contract that defines a non-duplicating alias mechanism and tests routing ambiguity.

CIM-R11. Release-note or adopter-facing migration guidance MUST state that direct `ci` invocations should be updated to `ci-maintenance`.

### Skill role and claim boundary

CIM-R12. `ci-maintenance` MUST describe its role as authoring or reviewing CI infrastructure: hosted CI workflow files, validation automation, and related platform configuration.

CIM-R13. `ci-maintenance` MUST NOT run validation.

CIM-R14. `ci-maintenance` MUST NOT design tests.

CIM-R15. `ci-maintenance` MUST NOT invent validation commands.

CIM-R16. `ci-maintenance` MUST NOT wait for existing CI checks.

CIM-R17. `ci-maintenance` MUST NOT claim CI pass status, verify readiness, branch readiness, PR readiness, release readiness, or deployment readiness.

CIM-R18. In workflow-managed execution, successful `ci-maintenance` MUST hand off to `explain-change` unless a stop condition applies.

CIM-R19. Isolated or directly invoked `ci-maintenance` MUST report the CI infrastructure result without implying downstream continuation.

### Resource contract

CIM-R20. `ci-maintenance` MUST include a `Resource map` when it ships packaged resources.

CIM-R21. The `Resource map` MUST map `assets/github-workflow-skeleton.yml` with the verb `COPY`.

CIM-R22. The `Resource map` MUST map `references/risk-to-check-map.md` with the verb `READ`.

CIM-R23. The `Resource map` MUST name every packaged `ci-maintenance` resource and state when to use it.

CIM-R24. The workflow skeleton asset MUST be a copy-and-fill GitHub Actions workflow structure, not hidden policy prose.

CIM-R25. The workflow skeleton asset MUST include placeholders for PR changed-risk checks, boundary checks, least-privilege permissions, concurrency, job timeouts, action reference policy, deterministic install commands, validation commands, and dependency cache keys.

CIM-R26. The workflow skeleton asset MUST instruct through placeholders or surrounding skill text that action references use a full-length SHA or a project-policy-approved reference.

CIM-R27. The workflow skeleton asset MUST NOT include invented real action SHAs.

CIM-R28. The workflow skeleton asset MUST NOT include project-specific validation commands unless those commands are supplied by an allowed command source.

CIM-R29. The risk-to-check reference MUST be decision guidance, not a copy-and-fill output template.

CIM-R30. The risk-to-check reference MUST split portable core rows from project-specific extension rows.

CIM-R31. RigorLoop-specific surfaces such as skills, generated adapters, release metadata, and repository validators MUST be labeled as project-specific examples, not universal public-skill requirements.

CIM-R32. The risk-to-check reference MUST include a fail-safe rule for unmapped changed surfaces: route them to an explicit reviewer flag, a conservative boundary check, or both.

CIM-R33. The risk-to-check reference MUST NOT imply that the listed rows mitigate all possible CI risk.

### GitHub Actions authoring behavior

CIM-R34. `ci-maintenance` MUST use this design principle when authoring GitHub Actions workflows: run fast changed-risk checks on every PR, and run heavy comprehensive checks at scheduled, release, manual, or other boundary points.

CIM-R35. PR workflows SHOULD use path filters only when the risk-to-check map proves the filters do not skip required checks.

CIM-R36. Broad, slow, flaky, environmental, or comprehensive checks SHOULD run on schedule, manual dispatch, release, protected-branch gates, or another boundary unless the change requires them for PR safety.

CIM-R37. GitHub Actions workflows authored or reviewed by `ci-maintenance` MUST default to least-privilege permissions.

For generic read-only CI, the default workflow-level permission is:

```yaml
permissions:
  contents: read
```

Any additional or broader job-specific permission MUST be required by a known workflow need and justified in the workflow rationale.

CIM-R37a. `ci-maintenance` MUST NOT add write permissions, token permissions, package permissions, pull request permissions, deployment permissions, or OIDC permissions unless the workflow purpose requires them and the rationale names the need.

CIM-R37b. When a job needs fewer permissions than the workflow default, `ci-maintenance` SHOULD reduce permissions at the job level. When a job needs more permissions, `ci-maintenance` SHOULD elevate only that job and record the reason.

CIM-R38. `ci-maintenance` MUST warn against `pull_request_target` for untrusted code unless the workflow is explicitly designed and reviewed for that security boundary.

CIM-R39. `ci-maintenance` MUST use dependency caches only when a stable invalidation key exists, normally a lockfile hash.

CIM-R40. If no stable cache invalidation key exists, `ci-maintenance` MUST omit dependency caching or report the cache as intentionally not used.

CIM-R41. `ci-maintenance` MUST prefer deterministic dependency installation commands from project convention or explicit command sources.

CIM-R42. `ci-maintenance` MUST make failure output actionable by preserving or recommending command names, failing check names, short reasons, and next diagnostic steps where the workflow can provide them.

CIM-R43. `ci-maintenance` MUST include job timeouts for authored GitHub Actions jobs.

CIM-R44. Release triggers MAY be added only when the workflow owns release validation or packaging.

CIM-R45. Deployment, secret-bearing release publishing, self-hosted runner policy, and organization-level Actions policy are outside this first slice.

### Command ownership

CIM-R46. Workflow validation commands MUST come from an approved spec, approved or active test spec, plan validation section, existing package script, existing project CI convention, or explicit user-provided command.

CIM-R47. If no reliable command source exists, `ci-maintenance` MUST report a blocker instead of guessing.

CIM-R48. Skeleton placeholders such as `<scoped validation command>` and `<comprehensive validation command>` MUST remain placeholders until filled from an allowed command source.

CIM-R49. `ci-maintenance` MAY point out that a project lacks a validation command, but it MUST NOT define the missing test contract itself.

### Review behavior

CIM-R50. Workflow review output MUST flag overbroad permissions when the workflow does not justify them.

CIM-R51. Workflow review output MUST flag path filters that skip required checks for mapped risk surfaces.

CIM-R52. Workflow review output MUST flag slow comprehensive checks on every PR when the proposal, spec, plan, or risk map does not justify them.

CIM-R53. Workflow review output MUST include risk coverage against changed surfaces.

CIM-R54. Workflow review output MUST state open blockers when required command sources, project context, or risk-surface mapping is insufficient.

### Validation and generated output

CIM-R55. Skill validation MUST reject stale `name: ci` or `role_name: ci` when they mean the skill identifier.

CIM-R56. Skill validation MUST reject stale handoff wording such as `when ci is run` when it means direct skill invocation.

CIM-R57. Skill validation MUST prove `assets/github-workflow-skeleton.yml` is present and mapped with `COPY`.

CIM-R58. Skill validation MUST prove `references/risk-to-check-map.md` is present and mapped with `READ`.

CIM-R59. Skill validation MUST prove the workflow skeleton includes least-privilege permissions, concurrency, PR trigger structure, boundary-check structure, timeout placeholders, action-reference placeholders, command placeholders, and cache placeholders or cache omission guidance.

CIM-R60. Skill validation MUST prove the risk map separates portable core guidance from project-specific extensions.

CIM-R61. Skill validation MUST prove the risk map includes an unmapped-surface fail-safe.

CIM-R62. Generated adapter validation MUST prove generated public adapter packages include `ci-maintenance` and its packaged resources.

CIM-R63. Generated adapter validation MUST prove no generated adapter exposes `ci` as an active skill body in this first slice.

CIM-R64. Generated adapter output MUST be regenerated or checked from canonical skills and MUST NOT be hand-edited.

CIM-R65. No actual repository `.github/workflows/*.yml` behavior MUST change in this slice.

## Inputs and outputs

Inputs:

- accepted proposal and proposal-review records;
- existing `skills/ci/SKILL.md`;
- workflow guidance that names `ci-maintenance`;
- `specs/skill-contract.md` resource-map, published-skill portability, and generated-output rules;
- current adapter generation and validation surfaces;
- project package scripts, test specs, plans, and CI conventions when `ci-maintenance` runs in a target project;
- changed paths or user-requested CI scope.

Outputs:

- canonical skill source at `skills/ci-maintenance/SKILL.md`;
- no active canonical skill source at `skills/ci/SKILL.md`;
- packaged asset `skills/ci-maintenance/assets/github-workflow-skeleton.yml`;
- packaged reference `skills/ci-maintenance/references/risk-to-check-map.md`;
- updated workflow docs, skill references, validators, tests, fixtures, and generated adapter proof;
- adopter-facing migration guidance for the hard rename;
- no repository CI workflow behavior change in this slice.

## State and invariants

- `ci-maintenance` is the only canonical active skill identity for CI infrastructure maintenance.
- `ci` is not an active skill identity after this slice.
- A skill rename is an identifier migration, not prose cleanup.
- `SKILL.md` owns operating policy and claim boundaries.
- `assets/github-workflow-skeleton.yml` owns only reusable workflow structure.
- `references/risk-to-check-map.md` owns situational decision guidance and must not become hidden policy.
- Public skill text must remain portable to non-RigorLoop repositories.
- Generated adapter output remains derived from canonical skill source.
- No repository CI workflow behavior changes are part of this slice.

## Error and boundary behavior

- If validation finds stale `ci` identifier references, readiness is blocked until the references are updated or classified as generic continuous-integration prose.
- If generated adapters expose both `ci` and `ci-maintenance` as active skills, readiness is blocked.
- If a workflow cannot be authored without inventing validation commands, `ci-maintenance` reports a blocker.
- If changed paths include an unmapped surface, `ci-maintenance` flags it for reviewer judgment, routes it to a conservative boundary check, or both.
- If a project lacks a stable cache invalidation key, `ci-maintenance` omits caching rather than creating a stale-prone cache.
- If a workflow needs secrets, privileged permissions, `pull_request_target`, self-hosted runners, deployment, or release publishing, this first-slice skill contract does not authorize a generic template; the workflow needs separate design/review.
- If adapter validation cannot prove packaged resources are included, readiness is blocked.

## Compatibility and migration

This first slice is a hard rename.

Existing direct invocations or adopter documentation that use `ci` must migrate to `ci-maintenance`. Release notes or adopter-facing migration guidance must say:

```md
The CI workflow authoring/review skill has been renamed from `ci` to
`ci-maintenance` to match its workflow role. Use `ci-maintenance` when invoking
the skill directly. Existing `ci` references should be updated.
```

The current repository does not provide a safe non-duplicating skill alias mechanism. The implementation must not emulate compatibility by shipping both `ci` and `ci-maintenance` active skill directories.

Rollback is to restore `ci` as the canonical skill identity only if adapter generation or routing breaks and cannot be resolved. Rollback must not leave duplicate active skills. The risk map and workflow skeleton may be deferred only if the rename must be isolated.

## Observability

- Skill validation output should identify stale identifier references, missing resources, wrong resource-map verbs, resource-map coverage gaps, skeleton default gaps, risk-map portability gaps, and unmapped-surface fail-safe gaps by stable check or clear file/path message.
- Adapter validation output should identify whether `ci-maintenance` and packaged resources are present in generated output.
- Change-local evidence should record behavior-preservation proof for skill identity, workflow role, handoff wording, generated adapter output, public docs, and unchanged repository CI workflows.
- Release notes should record the hard rename and migration guidance.

## Security and privacy

- Authored GitHub Actions workflows default to least-privilege token permissions.
- `ci-maintenance` must warn against secrets in untrusted PR workflows.
- `pull_request_target` is forbidden for untrusted code unless the workflow is explicitly designed and reviewed for that boundary.
- The skeleton must not invent full-length action SHAs, secret names, credentials, tokens, or privileged permissions.
- Dependency caching must use stable invalidation keys or be omitted.
- Public skill text must not require RigorLoop repository-internal paths in non-RigorLoop projects.

## Accessibility and UX

No user-interface accessibility behavior is changed. The user-facing behavior is skill discoverability and output readability:

- direct skill invocation uses `ci-maintenance`;
- workflow authoring and review output should be concise, concrete, and structured around workflow file, PR checks, boundary checks, risk coverage, blockers, and tradeoffs.

## Performance expectations

- The skill contract optimizes authored workflows for fast PR feedback by selecting changed-risk checks for PRs and moving broad checks to boundary triggers.
- The spec does not set a universal wall-clock limit because target projects differ.
- Authored workflows should include job timeout placeholders or values so hung jobs do not run indefinitely.
- Heavy checks should not run on every PR unless required for PR safety and justified by the project risk map or governing artifacts.

## Edge cases

EC1. A file contains `CI` as a generic continuous-integration phrase; validation does not require changing it to `ci-maintenance`.

EC2. A file contains `name: ci` in skill front matter; validation fails because it is a stale skill identifier.

EC3. A workflow file is named `ci.yml`; the file is not renamed solely because the skill was renamed unless the file is a skill-reference surface.

EC4. The adapter layer later gains safe alias support; this spec still requires a hard rename for this first slice until a later approved contract changes compatibility behavior.

EC5. A non-RigorLoop repository has no skills or generated adapters; the portable risk-map core still applies without requiring RigorLoop-specific rows.

EC6. A project changes a Dockerfile, environment variable policy, or secrets-related config not listed in the risk map; the unmapped-surface fail-safe applies.

EC7. A project has no lockfile; dependency caching is omitted or blocked for explicit decision rather than guessed.

EC8. A project has no reliable validation command; workflow authoring blocks instead of inventing commands.

EC9. A workflow needs release publishing or deployment secrets; this first slice does not supply a generic template for that workflow.

EC10. A project policy allows trusted major-version action tags instead of SHA pinning; the skill may use a policy-approved reference and record that policy instead of inventing SHAs.

EC11. Generated adapter output includes `ci-maintenance` but omits the packaged asset or reference; adapter validation fails.

EC12. A route table, fixture, or workflow doc still says direct `ci` invocation; validation flags it unless it is explicitly historical or migration guidance.

## Non-goals

- No repository `.github/workflows/*.yml` behavior changes.
- No deployment or release-publishing workflow template.
- No self-hosted runner policy.
- No organization-level GitHub Actions policy.
- No language-specific workflow skeletons.
- No security scanner integration.
- No generated CI workflow linter beyond the scoped validator checks named in this spec.
- No direct validation execution by `ci-maintenance`.
- No test design by `ci-maintenance`.
- No compatibility alias implementation in this first slice.

## Acceptance criteria

| ID | Criterion |
|---|---|
| AC-CIM-001 | Canonical skill name is `ci-maintenance`. |
| AC-CIM-002 | No canonical skill body uses `ci` as the skill identifier after rename. |
| AC-CIM-003 | All workflow-stage and handoff references use `ci-maintenance`. |
| AC-CIM-004 | Adapter generation includes `ci-maintenance` and its resources. |
| AC-CIM-005 | No compatibility alias is claimed in this first slice; adopter migration guidance documents the hard rename. |
| AC-CIM-FM-001 | `skills/ci-maintenance/SKILL.md` front matter includes `name: ci-maintenance`. |
| AC-CIM-FM-002 | `skills/ci-maintenance/SKILL.md` front matter includes a non-empty `version` field. |
| AC-CIM-FM-003 | `skills/ci-maintenance/SKILL.md` front matter includes `schema-version` matching the current published-skill contract, expected first-slice value `skill-readability-v1`. |
| AC-CIM-FM-004 | Validation fails if the renamed skill omits either `version` or `schema-version`. |
| AC-CIM-006 | `SKILL.md` maps `assets/github-workflow-skeleton.yml` with `COPY`. |
| AC-CIM-007 | `SKILL.md` maps `references/risk-to-check-map.md` with `READ`. |
| AC-CIM-008 | The skeleton includes least-privilege permissions, concurrency, PR trigger structure, boundary-check structure, cache placeholders or cache omission guidance, action-reference placeholders, command placeholders, and timeout placeholders. |
| AC-CIM-009 | The risk map derives checks from changed surfaces. |
| AC-CIM-010 | The skill distinguishes PR checks from schedule, release, manual, or other boundary checks. |
| AC-CIM-011 | Workflow-review fixtures catch overbroad permissions, unsafe path filters, and unjustified slow PR checks. |
| AC-CIM-012 | No actual repository workflow behavior changes in this slice. |
| AC-CIM-013 | No generated adapter contains both an active `ci` skill and an active `ci-maintenance` skill. |
| AC-CIM-014 | Tests prove `ci` is not exposed as a callable compatibility alias in this first slice. |
| AC-CIM-015 | Release notes or adopter guidance document the hard rename and migration path. |
| AC-CIM-016 | The skill states that validation commands must come from approved project sources or explicit user input. |
| AC-CIM-017 | A workflow-authoring fixture with missing validation commands returns a blocker instead of inventing commands. |
| AC-CIM-018 | The skeleton placeholders do not weaken the boundary that `ci-maintenance` does not run validation or design tests. |
| AC-CIM-019 | `risk-to-check-map.md` separates portable core guidance from project-specific extensions. |
| AC-CIM-020 | RigorLoop-specific rows are labeled as project-specific examples, not universal public-skill requirements. |
| AC-CIM-021 | The public skill can be used in a non-RigorLoop repository without requiring RigorLoop-specific files or validators. |
| AC-CIM-022 | The risk map includes a fail-safe rule for unmapped changed surfaces. |
| AC-CIM-023 | Skill validation rejects stale `ci` identifier references while allowing generic continuous-integration prose. |
| AC-CIM-024 | Generated adapter validation proves packaged `ci-maintenance` resources are present and generated output was not hand-edited. |
| AC-CIM-SEQ-001 | The spec's `Next artifacts` list follows the repository workflow order: `spec-review -> architecture/architecture-review when required -> plan -> plan-review -> test-spec -> implementation`. |
| AC-CIM-SEQ-002 | The spec does not list `test-spec` as the immediate next artifact after `spec-review`. |
| AC-CIM-SEQ-003 | If architecture is skipped, the plan or spec records why architecture is not required. |
| AC-CIM-SEQ-004 | `plan-review` remains the normal immediate handoff into `test-spec`. |
| AC-CIM-PERM-001 | The workflow skeleton defaults to least-privilege permissions. |
| AC-CIM-PERM-002 | Generic read-only CI uses `permissions: contents: read`. |
| AC-CIM-PERM-003 | Additional or broader job-specific permissions require a named workflow need and rationale. |
| AC-CIM-PERM-004 | The spec does not use contradictory wording such as "narrower elevation." |

## Open questions

None blocking for spec-review.

## Next artifacts

Planned next artifacts:

```text
spec-review
architecture, if required
architecture-review, if architecture is required
plan
plan-review
test-spec
implementation
code-review
review-resolution, when triggered
explain-change
verify
pr
```

Architecture is required only if proposal-review or spec-review identifies a runtime, packaging, generated-adapter, release-boundary, workflow-data-flow, or security/trust-boundary change that needs a separate architecture artifact.

If architecture is intentionally not required, record the rationale before planning.

Do not route directly from `spec-review` to `test-spec`. `plan-review` remains the normal immediate handoff into `test-spec`.

This change touches public skill identity, packaged resources, generated adapters, validators, workflow guidance, and release-note migration behavior. The plan must settle implementation sequencing and generated-output proof before test-spec relies on the final milestone structure.

## Follow-on artifacts

None yet

## Readiness

Ready for `plan`.
