# Evidence-Bound and Incremental Project Map Skill

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Start date: 2026-06-23
- Last updated: 2026-06-23
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved evidence-bound `project-map` contract without expanding the skill beyond current-state repository orientation. The work must normalize the published skill surface, add a packaged skeleton asset, prove the evidence/freshness/root-area contracts through focused fixtures, and show generated adapter inclusion while keeping future design, backlog ownership, and full project-map artifact validation out of scope.

## Source artifacts

- Proposal: `docs/proposals/2026-06-23-evidence-bound-incremental-project-map.md`
- Spec: `specs/project-map.md`
- Architecture: `docs/architecture/system/architecture.md`
- C4 container diagram: `docs/architecture/system/diagrams/container.mmd`
- Proposal review: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/proposal-review-r1.md`
- Spec review: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/spec-review-r1.md`
- Architecture review: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/architecture-review-r3.md`
- Review resolution: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md`
- Change metadata: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
- Test spec: `specs/project-map.test.md`

## Context and orientation

`project-map` currently exists as a lightweight orientation skill in `skills/project-map/SKILL.md`. It already says to describe what exists today, cite important claims, and separate observations from inferences, but it does not yet expose normalized frontmatter, workflow-role metadata, operating modes, map metadata/freshness, source-rank, root/area registration, correction notes, or a packaged skeleton asset.

Existing implementation anchors:

- `scripts/skill_validation.py` owns skill metadata validation, readability-contract checks, resource-map validation, approved asset rollout lists, and generated asset presence helpers.
- `scripts/test-skill-validator.py` owns skill-validator regression fixtures and already has project-map-focused assertions.
- `tests/fixtures/skills/skill-readability/` and `tests/fixtures/skills/published-design/` contain reusable patterns for readability, resource-map, asset, and generated-output fixture coverage.
- `scripts/build-skills.py --check` proves generated local Codex mirror parity from canonical `skills/`.
- `scripts/build-adapters.py` and `scripts/validate-adapters.py` prove adapter/release-candidate output behavior without hand-editing generated public adapter bodies.
- `docs/project-map.md` is an existing living reference but is not automatically migrated by this change.

## Non-goals

- Do not turn `project-map` into an architecture-design, backlog, plan, validation-gate, or implementation-readiness skill.
- Do not automatically migrate existing project maps, including `docs/project-map.md`.
- Do not add automatic repository graph generation, language-specific scanners, runtime tracing, remote indexing, telemetry, or network scanning.
- Do not add a dedicated project-map artifact validator in this slice unless two produced-map drift cases are already demonstrated before implementation.
- Do not hand-edit `.codex/skills/`, generated adapter package output, release archives, or installed target trees.
- Do not require RigorLoop repository-internal paths in the published `project-map` skill text.

## Requirements covered

- R1-R5: M1 scaffolds controlled fixture coverage for normalized role, frontmatter, workflow-role, and claim boundaries; M2 updates canonical `project-map` sources and enables canonical enforcement.
- R6-R15: M2 records create, refresh, area, audit, result output, placement, and workflow ownership boundaries.
- R16-R29: M2 records metadata, freshness, dirty baseline, refresh triggers, stale/partial/current meanings, and correction notes; M3 proves representative output.
- R30-R41: M2 records observed/inferred/unknown classes, material-claim examples, observed architecture-rule criteria, source-rank, and intent-versus-current conflict handling; M3 proves representative output.
- R42-R48: M2 records configured/executed command and runtime/data-flow evidence distinctions; M3 proves representative output.
- R49-R57: M2 records root/area map registration, durable-boundary split floor, parent-map, overlap, and contradiction behavior; M3 proves representative output.
- R58-R65: M1 scaffolds controlled fixture coverage for skeleton/resource-map behavior; M2 adds the skeleton asset, `Resource map`, and canonical enforcement; M3 validates produced-output evidence.
- R66-R71: M2 records the diagram contract inside `SKILL.md`; M3 proves no planned/decorative diagram behavior in representative output where diagrams appear.
- R72-R77: M2 records safe/unsafe downstream reliance, handoff, and risk/backlog boundaries.
- R78-R84: M1 validates first-slice fixture scaffolding without canonical enforcement; M2 records behavior-preservation evidence with canonical skill enforcement; M3/M4 validate representative output, generated adapter inclusion, no automatic migration, and cold-read proof.

## Current Handoff Summary

- Current milestone: final closeout sequence
- Current milestone state: in-progress
- Last reviewed milestone: code-review-m4-r1
- Review status: clean-with-notes
- Remaining in-scope implementation milestones: none
- Next stage: pr
- Final closeout readiness: branch-ready
- Reason final closeout is or is not ready: all implementation milestones are closed, explain-change is recorded, and final local verify passed; PR handoff has not completed.

## Milestones

### M1. Project-Map Validator and Fixture Scaffolding

- Milestone state: closed
- Goal: Add reusable validator helpers and controlled fixtures for the approved project-map contract without enabling new enforcement against unchanged canonical `project-map` sources.
- Requirements: R3-R5, R36, R58-R65, R78-R80
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/skill-readability/`
  - `tests/fixtures/skills/published-design/`
  - `docs/changes/2026-06-23-evidence-bound-incremental-project-map/validator-fixtures.md`
- Dependencies:
  - approved plan after plan-review rerun
  - approved test spec
  - approved spec and architecture package
- Tests to add/update:
  - controlled valid fixture accepts normalized frontmatter and workflow-role fields
  - controlled valid fixture accepts `create`, `refresh`, `area`, and `audit` modes
  - controlled valid fixture accepts map metadata fields, observation/inference/unknown classification, root/area map relationship, skeleton `Resource map`, and required output headings
  - controlled invalid fixtures reject missing or incomplete contract fields with stable expected diagnostics
  - negative fixtures pass by asserting expected diagnostics; do not commit `expectedFailure`, temporarily skipped acceptance tests, or known failing canonical validation as M1 proof
  - existing canonical skill validation remains green with new project-map canonical enforcement disabled
- Implementation steps:
  - add the smallest project-map-specific validator helper or fixture assertions needed for stable controlled-fixture checks
  - reuse existing readability/resource-map/asset validation helpers where possible
  - document representative fixture intent in change-local validator evidence
  - keep checks structural and stable; avoid broad natural-language scoring
  - do not modify `skills/project-map/SKILL.md`, `skills/project-map/assets/project-map-skeleton.md`, generated skill output, or adapter packages
  - do not enable canonical checks that require unchanged `skills/project-map/SKILL.md` or a missing skeleton asset to satisfy the new contract
- Validation commands:
  - `python scripts/test-skill-validator.py -k project_map`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills`
- Expected observable result: controlled valid fixtures pass; controlled invalid fixtures fail with stable expected diagnostics; existing canonical skill validation remains green; no canonical `project-map` enforcement requiring M2 content is enabled; M1 can close and enter code review independently.
- Commit message: `M1: validate project-map contract fixtures`
- Milestone closeout:
  - validation passed
  - controlled valid and invalid fixtures prove expected helper behavior
  - canonical `project-map` sources remain unchanged
  - canonical enforcement requiring M2 content remains disabled
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - validator checks could overfit prose and reject useful future wording
  - first-slice checks could accidentally become a full produced-map artifact validator
- Rollback/recovery:
  - narrow validation to frontmatter, workflow-role presence, resource-map entry, skeleton structure, and representative fixture strings if prose-level checks prove brittle
  - if any check requires canonical `project-map` content before M2, disable that canonical enforcement and keep it as controlled fixture coverage only

### M2. Canonical Project-Map Skill, Skeleton, and Enforcement

- Milestone state: closed
- Goal: Update the canonical `project-map` skill and add its skeleton asset, then enable the approved contract checks against those canonical sources.
- Requirements: R1-R77
- Files/components likely touched:
  - `skills/project-map/SKILL.md`
  - `skills/project-map/assets/project-map-skeleton.md`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md`
- Dependencies:
  - M1 fixture/helper scaffolding closed after code review
  - approved test spec
  - approved architecture package
  - canonical project-map baseline evidence recorded
- Tests to add/update:
  - canonical `project-map` opts into `skill-readability-v1`
  - canonical `project-map` requires and satisfies a `Resource map` entry for `assets/project-map-skeleton.md`
  - skeleton contains all required sections and no hidden policy
  - resource-map `COPY` entry names fields to fill and prohibits unfilled placeholders
  - corrupting a required canonical field or mapped resource fails with a stable diagnostic
- Implementation steps:
  - normalize frontmatter with `version`, `schema-version`, portable description, and `argument-hint`
  - add workflow-role, operating modes, artifact placement, metadata/freshness, evidence/source-rank, command/runtime evidence, root/area map, diagram, downstream reliance, and stop-condition guidance
  - include material versus incidental claim examples in skill text
  - add `assets/project-map-skeleton.md` with headings, metadata fields, area-map table headers, evidence-trail shape, and short fill instructions only
  - keep evidence-ranking rules, inference policy, refresh triggers, future-design prohibitions, handoff rules, and claim boundaries in `SKILL.md`
  - avoid maintainer-only repository paths in shipped skill text
  - enable canonical validation enforcement only after canonical `SKILL.md` and the skeleton asset have been updated together
  - record behavior-preservation evidence for orientation-only role and existing eleven-section coverage
- Validation commands:
  - `python scripts/test-skill-validator.py -k project_map`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py skills/project-map/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: `skills/project-map/SKILL.md` satisfies the approved contract; `assets/project-map-skeleton.md` exists and is explicitly mapped with `COPY`; canonical enforcement is enabled; valid canonical sources pass; removing or corrupting a required canonical field/resource fails; full skill validation passes; behavior-preservation evidence confirms the orientation-only role and existing eleven-section coverage remain intact.
- Commit message: `M2: normalize project-map skill and skeleton`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - the skill could become too long for common-path use
  - the skeleton could accidentally own policy that belongs in `SKILL.md`
- Rollback/recovery:
  - move only reusable output structure into the skeleton and trim explanatory duplication from the skill body while preserving normative contract coverage
  - if canonical enforcement exposes an unrelated generic validator defect, keep the canonical skill/skeleton update atomic and fix or explicitly block the validator defect before M2 review handoff

## Test-first milestone boundary

Test-first development does not require a committed milestone to remain red.

M1 encodes the contract using controlled valid and invalid fixtures. Invalid fixtures produce expected diagnostics, so the test suite remains green.

M2 updates canonical sources and enables the corresponding canonical enforcement atomically.

Any temporary local red-test run is development evidence, not a milestone closeout state.

## Milestone validation boundary

| Milestone | Contract boundary | Required closeout state |
| --- | --- | --- |
| M1 | Validator helpers and controlled fixtures | All fixture and existing canonical validation passes; new canonical enforcement remains disabled |
| M2 | Canonical skill, skeleton asset, and canonical enforcement | Full skill validation passes against updated canonical sources |
| M4 | Generated skill and adapter inclusion | Generated/package parity passes |

Hard rule: no milestone may require a validation failure to remain unresolved until a later milestone while also claiming that the current milestone's validation passed.

### M3. Representative Output and Preservation Evidence

- Milestone state: closed
- Goal: Add focused representative evidence that proves behavior preservation, output shape, evidence classes, freshness, area-map relationships, correction notes, and cold-read usability without building a broad artifact validator.
- Requirements: R16-R48, R49-R65, R72-R84
- Files/components likely touched:
  - `docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md`
  - `docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md`
  - `docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/` or another existing fixture root selected by the test spec
- Dependencies:
  - M2 skill and skeleton complete
  - test-spec names representative output assertions
- Tests to add/update:
  - root map output includes required metadata and all required sections
  - area map output names parent map and root registration table
  - observed, inferred, and unknown claims are visibly distinct
  - configured commands are not described as executed
  - correction note appears when prior map was wrong at baseline
  - future intent artifact is not represented as current implementation
  - representative outputs contain no unfilled placeholders
- Implementation steps:
  - record behavior-preservation matrix for orientation-only role, current-state focus, section structure, path citations, observation/inference split, narrow-area support, risk routing, handoff, and customer-project mode
  - record cold-read proof for a small repository, a monorepo or multi-service fixture, and an intentionally stale map, or record any accepted deferral before implementation closeout
  - add small representative outputs or fixture snippets that prove the first-slice expectations
  - keep output fixtures scoped to representative drift-prone cases rather than every PMAP check in the proposal
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md`
- Expected observable result: reviewers can inspect concise evidence proving the revised skill preserves the original orientation behavior while strengthening evidence, freshness, and root/area contracts.
- Commit message: `M3: prove project-map output behavior`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - output examples could drift into large transcripts
  - cold-read proof could rely on chat-only reasoning
- Rollback/recovery:
  - reduce examples to stable excerpts with explicit source assumptions and move any unresolved proof gap into an accepted deferral before M3 closes

### M4. Generated Adapter Proof and Lifecycle Closeout Preparation

- Milestone state: closed
- Goal: Prove generated output includes the revised `project-map` skill and skeleton asset, update compact change evidence, and prepare the completed implementation for final review gates.
- Requirements: R2, R61-R65, R78-R84
- Files/components likely touched:
  - `docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
  - generated-output proof under `docs/changes/2026-06-23-evidence-bound-incremental-project-map/` if needed by the test spec
  - no hand-edited generated adapter output
- Dependencies:
  - M1-M3 closed
  - test-spec complete
- Tests to add/update:
  - generated local skill output includes `project-map` skeleton asset
  - adapter validation or release-candidate proof includes `project-map` skeleton asset for supported targets
  - change metadata records actual validation commands and no unverified success claims
- Implementation steps:
  - run generated local mirror check from canonical source
  - build adapter/release-candidate output into a temporary directory and validate it without committing generated bodies
  - record generated adapter inclusion proof if the test spec requires a standalone evidence file
  - update change metadata with completed validation commands and changed files
  - leave final lifecycle closeout to downstream `explain-change`, `verify`, and `pr` gates
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-project-map-adapter-proof`
  - `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-project-map-adapter-proof`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path skills/project-map/SKILL.md --path skills/project-map/assets/project-map-skeleton.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
  - `git diff --check --`
- Expected observable result: canonical skill, skeleton, representative proof, generated output, adapter inclusion, and change metadata are ready for final code-review and downstream lifecycle gates.
- Commit message: `M4: prove project-map generated inclusion`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - adapter proof may require current package version alignment
  - temporary generated output could be mistaken for tracked source
- Rollback/recovery:
  - keep generated proof in `/tmp` or change-local evidence only; if adapter generation fails for unrelated baseline reasons, record the exact blocker and stop before claiming M4 closeout

## Validation plan

- `python scripts/test-skill-validator.py`: skill contract, skeleton, and representative fixture regression coverage.
- `python scripts/validate-skills.py`: canonical skill validation.
- `python scripts/build-skills.py --check`: generated local Codex mirror parity from canonical skill source.
- `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-project-map-adapter-proof`: temporary adapter/release-candidate generation proof.
- `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-project-map-adapter-proof`: generated adapter inclusion and package validation proof.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`: compact change metadata validation.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map`: formal review evidence validation.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/plan.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`: lifecycle wording and status validation for touched planning/change surfaces.
- `bash scripts/ci.sh --mode explicit ...`: selected repository checks for the final touched path set.
- `git diff --check --`: whitespace validation.

## Risks and recovery

- Risk: The revised skill becomes too large and slows common-path orientation.
  - Recovery: keep detailed output structure in the skeleton asset, keep only policy and workflow rules in `SKILL.md`, and trim duplicate explanation during M2 review.
- Risk: Validator checks overfit natural language.
  - Recovery: validate stable metadata, headings, resource maps, asset presence, and representative fixture assertions rather than arbitrary prose.
- Risk: Area-map examples fragment the root-map model.
  - Recovery: keep root registration mandatory in every area-map example and make one map own detailed overlap.
- Risk: Generated adapter proof depends on release tooling affected by unrelated active work.
  - Recovery: use temporary output, record the exact command failure, and stop M4 rather than hand-editing generated output or claiming adapter inclusion.
- Risk: Existing `docs/project-map.md` does not satisfy the revised map contract.
  - Recovery: keep it explicitly unmigrated; do not rely on it as proof of produced-map compliance.

## Dependencies

- Proposal, spec, and architecture are approved or accepted enough for planning.
- Plan-review must approve this revised execution plan before test-spec.
- Test-spec must map requirements and representative proofs before implementation starts.
- The active published-skill resource-integrity work may affect generic resource-map and generated-asset validation; implementation must re-read current `scripts/skill_validation.py` and validator tests before M1.
- M1 has no dependency on M2 and must close with passing validation before M2 begins.
- M2 depends on M1 closing cleanly and owns canonical content plus enforcement.
- M4 depends on M2 closing cleanly before generated output and adapter inclusion proof.
- Adapter proof uses temporary generated output and must not require hand-editing generated adapter bodies.

## Progress

- 2026-06-23: Created execution plan after accepted proposal, approved spec, corrected architecture package, and clean architecture-review R3.
- 2026-06-23: Revised plan to resolve PMAP-PLAN1-F1 by separating M1 fixture/helper scaffolding from M2 canonical project-map source and enforcement.
- 2026-06-23: Plan-review R2 approved the revised plan and closed PMAP-PLAN1-F1.
- 2026-06-23: Plan-review R4 approved the synchronized plan after PMAP-PLAN2-F1 corrected the plan index next stage.
- 2026-06-23: Plan-review R6 approved the readiness wording correction after PMAP-PLAN3-F1.
- 2026-06-23: Created active test spec `specs/project-map.test.md` and synchronized the next stage to `implement M1`.
- 2026-06-23: User approved the active test spec; next stage remains `implement M1`.
- 2026-06-23: Implemented M1 controlled project-map validator fixture scaffolding and handed the milestone to code-review.
- 2026-06-23: Code-review M1 R1 recorded `clean-with-notes`; M1 closed and next stage is `implement M2`.
- 2026-06-23: Implemented M2 canonical `project-map` skill normalization, skeleton asset, canonical validation enforcement, and behavior-preservation evidence; handed M2 to code-review.
- 2026-06-23: Code-review M2 R1 recorded `clean-with-notes`; M2 closed and next stage is `implement M3`.
- 2026-06-23: Implemented M3 representative output assertions, representative root and area map excerpts, correction-note proof, cold-read proof, and registered the new project-map output proof evidence class; handed M3 to code-review.
- 2026-06-23: Code-review M3 R1 recorded `clean-with-notes`; M3 closed and next stage is `implement M4`.
- 2026-06-23: Implemented M4 generated local skill parity proof, temporary adapter archive proof, generated skeleton inclusion evidence, and no-migration boundary evidence; handed M4 to code-review.
- 2026-06-23: Code-review M4 R1 recorded `clean-with-notes`; M4 closed and the next stage is the final closeout sequence starting with explain-change.
- 2026-06-23: Recorded explain-change rationale in `docs/changes/2026-06-23-evidence-bound-incremental-project-map/explain-change.md`; next stage is verify.
- 2026-06-23: Final local verify passed, recorded `docs/changes/2026-06-23-evidence-bound-incremental-project-map/verify-report.md`, and established branch-ready evidence for PR handoff. Hosted CI was not observed.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-23 | Split implementation into validator, skill/skeleton, representative evidence, and generated-proof milestones. | The spec spans published skill text, packaged assets, validation, evidence artifacts, and adapter inclusion; separating them keeps each review focused. | One monolithic implementation milestone; a broad produced-map artifact validator in the first slice. |
| 2026-06-23 | Keep existing project maps unmigrated in this plan. | The approved spec makes migration a non-goal and treats existing maps as satisfying the revised contract only after intentional refresh. | Auto-refreshing `docs/project-map.md` during skill implementation. |
| 2026-06-23 | Keep M1 and M2 separate but make M1 fixture-only and M2 canonical-plus-enforcement. | PMAP-PLAN1-F1 showed the prior boundary was not independently closeable because M1 expected failures only M2 could fix. Controlled negative fixtures preserve test-first proof without committing a red milestone. | Committing expected-failure tests; temporarily skipped acceptance tests; merging all validation and canonical source work into one broad milestone. |
| 2026-06-23 | Use workflow-role stage `support` for `project-map`. | The governing readability contract does not currently allow `orientation`, and `support` is the approved equivalent for this living-reference orientation skill. | Silently introducing unsupported `orientation`; amending the generic contract in this slice. |

## Surprises and discoveries

- `docs/project-map.md` exists but predates the revised metadata/status contract and should not be treated as migrated proof.
- Existing validator infrastructure already has readability, resource-map, asset, and generated-presence hooks that should be reused before adding new project-map-specific machinery.
- The planned selector command using `--path tests/fixtures/skills` initially exposed a selector classification gap for the fixture directory. M1 fixed the selector so the approved directory-form command now passes instead of relying only on concrete fixture file paths.
- M2 canonical enforcement reused the M1 structural helper with canonical opt-in after the canonical skill and skeleton were updated together.

## Validation notes

- 2026-06-23: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml` passed.
- 2026-06-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml` passed.
- 2026-06-23: `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml` passed selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `guide_system.validate`.
- 2026-06-23: `git diff --check --` passed.
- 2026-06-23: PMAP-PLAN1-F1 plan-revision validation passed: `git diff --check -- docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/plan.md docs/changes/2026-06-23-evidence-bound-incremental-project-map`; `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/plan.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md` passed.
- 2026-06-23: PMAP-PLAN2-F1 state-sync validation passed: `git diff --check -- docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/plan.md docs/changes/2026-06-23-evidence-bound-incremental-project-map`; `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/plan.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r3.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r4.md`; `bash scripts/ci.sh --mode explicit --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/plan.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r3.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r4.md` passed.
- 2026-06-23: Test-spec stage validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/project-map.test.md --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `bash scripts/ci.sh --mode explicit --path specs/project-map.test.md --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `git diff --check -- specs/project-map.test.md docs/plan.md docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml` passed.
- 2026-06-23: M1 validation passed: `python scripts/test-skill-validator.py -k project_map`; `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/select-validation.py --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills`; `python scripts/test-build-skills.py`; `python scripts/test-select-validation.py ValidationSelectionTests.test_first_slice_representative_categories_route_or_block_safely` passed.
- 2026-06-23: M1 final handoff validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/validator-fixtures.md`; `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path tests/fixtures/skills/project-map-contract/valid/SKILL.md --path tests/fixtures/skills/project-map-contract/valid/assets/project-map-skeleton.md --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/validator-fixtures.md`; `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py scripts/validation_selection.py scripts/test-select-validation.py tests/fixtures/skills/project-map-contract/valid/SKILL.md tests/fixtures/skills/project-map-contract/valid/assets/project-map-skeleton.md docs/plan.md docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml docs/changes/2026-06-23-evidence-bound-incremental-project-map/validator-fixtures.md` passed.
- 2026-06-23: Code-review M1 R1 recorded clean review with no material findings in `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m1-r1.md`.
- 2026-06-23: Code-review M1 R1 lifecycle validation passed: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map`; `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m1-r1.md`; `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m1-r1.md`; `git diff --check -- docs/plan.md docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m1-r1.md` passed.
- 2026-06-23: M2 implementation validation passed: `python scripts/test-skill-validator.py -k project_map` passed 11 tests; `python scripts/test-skill-validator.py` passed 225 tests; `python scripts/validate-skills.py skills/project-map/SKILL.md` passed; `python scripts/validate-skills.py` passed for 23 skill files; `python scripts/build-skills.py --check` passed.
- 2026-06-23: M2 lifecycle and selected CI validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md`; `git diff --check -- skills/project-map/SKILL.md skills/project-map/assets/project-map-skeleton.md scripts/skill_validation.py scripts/test-skill-validator.py docs/plan.md docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md`; `bash scripts/ci.sh --mode explicit --path skills/project-map/SKILL.md --path skills/project-map/assets/project-map-skeleton.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md` passed selected checks `skills.validate`, `skills.regression`, `skills.generation_regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `guide_system.validate`.
- 2026-06-23: Code-review M2 R1 recorded clean review with no material findings in `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m2-r1.md`.
- 2026-06-23: Code-review M2 R1 lifecycle validation passed: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map`; `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m2-r1.md`; `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m2-r1.md`; `git diff --check -- docs/plan.md docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m2-r1.md` passed.
- 2026-06-23: M3 implementation validation passed: `python scripts/test-skill-validator.py -k project_map` passed 14 tests; `python scripts/test-skill-validator.py` passed 228 tests; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md` passed.
- 2026-06-23: M3 selected CI initially blocked because `cold-read-proof.md` and `representative-project-map-outputs.md` were deterministic unregistered evidence paths; registered `project-map-output-proof` and reran `python scripts/test-select-validation.py ValidationSelectionTests.test_registered_change_evidence_patterns_and_exact_names_match_once`, which passed.
- 2026-06-23: M3 final selected CI and whitespace validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md`; `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md` passed selected checks `skills.regression`, `skills.generation_regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `guide_system.validate`, and `selector.regression`.
- 2026-06-23: Code-review M3 R1 recorded clean review with no material findings in `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m3-r1.md`.
- 2026-06-23: Code-review M3 R1 lifecycle validation passed: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map`; `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m3-r1.md`; `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m3-r1.md`; `git diff --check -- docs/plan.md docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m3-r1.md` passed.
- 2026-06-23: M4 generated-output validation passed: `python scripts/build-skills.py --check`; `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-project-map-adapter-proof`; `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-project-map-adapter-proof`; direct archive inspection found `project-map/assets/project-map-skeleton.md` in the Codex, Claude, and opencode adapter archives.
- 2026-06-23: M4 lifecycle and selected CI validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/generated-output-proof.md`; `git diff --check -- docs/plan.md docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml docs/changes/2026-06-23-evidence-bound-incremental-project-map/generated-output-proof.md`; `git diff --name-only -- docs/project-map.md dist/adapters .codex/skills .agents/skills .claude/skills .opencode/skills` produced no paths; `bash scripts/ci.sh --mode explicit --path skills/project-map/SKILL.md --path skills/project-map/assets/project-map-skeleton.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/generated-output-proof.md` passed selected checks `skills.validate`, `skills.regression`, `skills.generation_regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `guide_system.validate`, and `selector.regression`.
- 2026-06-23: Code-review M4 R1 recorded clean review with no material findings in `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m4-r1.md`.
- 2026-06-23: Code-review M4 R1 lifecycle validation passed: `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map`; `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m4-r1.md`; `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m4-r1.md`; `git diff --check -- docs/plan.md docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m4-r1.md` passed.
- 2026-06-23: Explain-change validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/explain-change.md`; `git diff --check -- docs/plan.md docs/plans/2026-06-23-evidence-bound-incremental-project-map.md docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml docs/changes/2026-06-23-evidence-bound-incremental-project-map/explain-change.md`; `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/explain-change.md` passed selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `guide_system.validate`.
- 2026-06-23: Final verify validation passed: `python scripts/query-change-record.py 2026-06-23-evidence-bound-incremental-project-map summary`; `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/`; `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py`; `python scripts/build-skills.py --check`; `python scripts/test-select-validation.py`; `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-project-map-adapter-proof`; `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-project-map-adapter-proof`; direct archive inspection confirmed `project-map/assets/project-map-skeleton.md` in Codex, Claude, and opencode adapter archives; `git diff --name-only -- docs/project-map.md dist/adapters .codex/skills .agents/skills .claude/skills .opencode/skills` produced no paths; full-surface selected CI passed `skills.validate`, `skills.regression`, `skills.generation_regression`, `skills.drift`, `adapters.drift`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `guide_system.validate`, and `selector.regression`; `git diff --check --` passed.

## Outcome and retrospective

- Final local verify passed and branch-ready evidence is recorded. PR handoff remains.

## Readiness

- See `Current Handoff Summary`.
- Ready for `pr` per `Current Handoff Summary`. Readiness is not Done; PR handoff and hosted CI/human review remain.
