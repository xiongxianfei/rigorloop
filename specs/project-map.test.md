# Project Map Skill Contract Test Spec

## Status

active

## Related spec and plan

- Spec: [Project Map Skill Contract](project-map.md), approved after clean spec-review R1.
- Proposal: [Evidence-Bound and Incremental `project-map` Skill](../docs/proposals/2026-06-23-evidence-bound-incremental-project-map.md), accepted.
- Architecture: [System Architecture](../docs/architecture/system/architecture.md) and [container diagram](../docs/architecture/system/diagrams/container.mmd), approved after architecture-review R3.
- Plan: [Evidence-Bound and Incremental Project Map Skill](../docs/plans/2026-06-23-evidence-bound-incremental-project-map.md), active after plan-review R6.
- Change metadata: [change.yaml](../docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml).
- Existing project map: `docs/project-map.md` is not used as migrated proof for the revised contract.
- Related proof surfaces:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/select-validation.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/ci.sh`

## Testing strategy

- Unit: add validator helper and fixture assertions in `scripts/test-skill-validator.py` for controlled valid and invalid `project-map` contract fixtures.
- Integration: validate the canonical `skills/project-map/SKILL.md`, packaged skeleton asset, generated local skill mirror, and generated adapter package after the canonical source changes.
- End-to-end: no runtime E2E test is required because this change updates a published skill, Markdown skeleton asset, validators, fixtures, generated mirrors, and evidence artifacts rather than an application runtime.
- Smoke: use `scripts/ci.sh --mode explicit` and repository-owned validation commands for the changed lifecycle and skill surfaces.
- Manual: inspect behavior-preservation evidence, cold-read proof, material-claim examples, and representative output excerpts where natural-language nuance is not suitable for broad automated scoring.
- Contract: validate frontmatter, workflow-role shape, modes, metadata/freshness, evidence classes, root/area relationships, resource-map `COPY`, skeleton section coverage, no hidden skeleton policy, and no produced-output placeholders.
- Migration: verify existing project maps are not automatically migrated and generated public adapter bodies are not hand-edited.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1, R2 | T4, T16, T20 | contract, manual, smoke | Observation-only role, no readiness/review/PR claims, customer-project portability, and no maintainer-only published-skill requirements. |
| R3, R4, R5 | T1, T2, T4, T11 | unit, integration, contract | Normalized frontmatter, workflow-role block, and allowed stage handling. |
| R6, R7, R8, R9, R10, R11 | T1, T2, T5, T12 | unit, integration, contract | Invocation modes, result block, audit non-rewrite behavior, and mode-specific fixture coverage. |
| R12, R13, R14, R15 | T5, T20 | integration, smoke | Portable paths, placement lookup order, and workflow/content ownership boundary. |
| R16, R17, R18, R19, R20, R21, R22 | T1, T2, T5, T12 | unit, integration, contract | Map metadata fields and `current`/`partial`/`stale` semantics. |
| R23, R24, R25 | T5, T15 | integration, manual | Git SHA/date baseline, `<sha>+dirty`, inspected uncommitted paths, and Git-unavailable fallback. |
| R26, R27 | T5, T15 | integration, manual | Refresh triggers and unrelated-change non-staleness. |
| R28, R29 | T5, T15 | integration, manual | Correction note without a fourth status. |
| R30, R31, R32, R33 | T1, T2, T6, T13 | unit, integration, contract | Observed/inferred/unknown evidence classes and unknowns recorded as open questions. |
| R34, R35, R36 | T1, T2, T6, T13 | unit, integration, manual | Material path citation rule and worked material-versus-incidental claim examples. |
| R37, R38, R39 | T6, T13 | integration, manual | Observed architecture-rule threshold, single-instance wording, and source ranking. |
| R40, R41 | T6, T13 | integration, manual | Intent artifacts do not prove current behavior and conflicts are recorded as planned state plus risk/open question. |
| R42, R43, R44, R45, R46 | T7, T14 | integration, manual | Configured/executed command split, exit-code evidence, read-only command allowance, and go-ahead for build/test/network/mutating commands. |
| R47, R48 | T7, T14 | integration, manual | Runtime and data-flow evidence labels and no implied runtime observation from static inspection. |
| R49, R50, R51, R52, R53 | T1, T2, T8, T12 | unit, integration, contract | Root entry point, area-map registration table, links, and parent-map field. |
| R54, R55, R56, R57 | T8, T12 | integration, manual | Durable area boundaries, split floor, overlap ownership, and contradiction blocking. |
| R58, R59, R60 | T1, T2, T8, T10, T12 | unit, integration, contract | Required sections, `Area maps` when applicable, and scoped `Not observed` rationale. |
| R61, R62, R63, R64, R65 | T1, T2, T10, T11, T12, T18, T19 | unit, integration, smoke | Skeleton asset path, `COPY` resource-map entry, skeleton scope, no hidden policy, and no unfilled placeholders. |
| R66, R67, R68, R69, R70, R71 | T9, T13 | integration, manual | Diagram usage, observed nodes, cited edges, inferred labels, no decorative/planned components, and area-owned detailed diagrams. |
| R72, R73, R74, R75 | T9, T16 | integration, manual | Safe/unsafe downstream reliance and isolated invocation handoff boundaries. |
| R76, R77 | T9, T16 | integration, manual | Risks and open questions do not become execution commitments and route through owner surfaces. |
| R78, R79, R80 | T1, T2, T3, T16 | unit, contract, manual | First-slice scope, no full fixture suite, and no project-map artifact validator before the drift threshold. |
| R81 | T18, T19 | integration, smoke | Generated local mirror and generated adapter package include the revised skill and skeleton. |
| R82 | T20 | migration, smoke | Existing project maps are not automatically migrated. |
| R83 | T16 | manual | Behavior-preservation evidence covers the required preservation matrix. |
| R84 | T17 | manual | Cold-read proof covers small repo, monorepo or multi-service fixture, and stale map unless an accepted deferral exists. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T12, T13 | Root map representative output includes metadata, required sections, and material path citations. |
| E2 | T12 | Area map representative output includes parent map, root registration, and overlap handling. |
| E3 | T13 | Intent artifacts are cited only as planned/expected state and do not become current implementation evidence. |
| E4 | T14 | Configured commands are not described as executed or passing without execution evidence. |
| E5 | T15 | Dirty Git baseline records `<sha>+dirty` and inspected uncommitted paths. |
| E6 | T15 | A prior wrong-at-baseline map claim produces a correction note without inventing a new status. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T15 | Git-unavailable baseline fallback appears in canonical guidance or representative proof. |
| EC2 | T15 | Dirty working tree records `<sha>+dirty` and inspected uncommitted paths. |
| EC3 | T15 | Changed cited source makes affected map stale until refresh. |
| EC4 | T15 | Wrong-at-baseline refresh records a correction note. |
| EC5 | T8, T12 | Single-directory feature request does not create an area map without durable boundary and split floor. |
| EC6 | T13 | Directory-name inference loses to inspected contents. |
| EC7 | T14 | Configured command remains configured-only when not run. |
| EC8 | T14 | Static source trace is not labeled as runtime observation. |
| EC9 | T13 | Future service in a spec is not presented as deployed. |
| EC10 | T12 | Root and area overlap names one detail owner and one link-only reference. |
| EC11 | T12 | Empty required sections use `Not observed in the mapped scope.` plus rationale. |
| EC12 | T10, T12 | Representative produced output fails if skeleton placeholders remain. |

## Test cases

### T1. Controlled valid fixture accepts first-slice structural contract

- Covers: R3, R4, R5, R6, R7, R8, R9, R10, R11, R16, R17, R18, R19, R20, R21, R22, R30, R31, R32, R33, R34, R35, R36, R49, R50, R51, R52, R53, R58, R59, R60, R61, R62, R63, R64, R65, R78, R79, R80
- Level: unit
- Fixture/setup: Controlled valid fixture under `tests/fixtures/skills/` selected by M1; canonical `skills/project-map/SKILL.md` remains unenforced for new project-map requirements during M1.
- Steps: Run `python scripts/test-skill-validator.py -k project_map`.
- Expected result: The valid fixture passes normalized frontmatter, workflow-role, mode, metadata, evidence-class, root/area, resource-map, and required-heading checks.
- Failure proves: The validator helper cannot recognize the approved contract even in a controlled valid fixture.
- Automation location: `scripts/test-skill-validator.py`; fixture path selected during M1.

### T2. Controlled invalid fixtures return stable diagnostics

- Covers: R3, R4, R5, R6, R11, R16, R17, R30, R31, R32, R33, R34, R36, R49, R51, R52, R53, R58, R61, R62, R64, R65, R78, R79, R80
- Level: unit
- Fixture/setup: Controlled invalid fixtures missing one required field, resource, relationship, or policy boundary at a time.
- Steps: Run `python scripts/test-skill-validator.py -k project_map`.
- Expected result: Each invalid fixture fails inside the test helper and the test passes by asserting the expected diagnostic substring.
- Failure proves: Negative fixtures are not encoded as passing diagnostic checks or diagnostics are too unstable for reviewable enforcement.
- Automation location: `scripts/test-skill-validator.py`; `tests/fixtures/skills/`.

### T3. M1 keeps canonical project-map enforcement disabled

- Covers: R78, R79, R80
- Level: integration
- Fixture/setup: Repository state after M1 changes only validator helpers, tests, and controlled fixtures.
- Steps: Run `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, and `python scripts/select-validation.py --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills`.
- Expected result: Existing canonical skill validation remains green without requiring unchanged canonical `project-map` sources to satisfy the new contract.
- Failure proves: M1 is not independently closeable or has enabled canonical enforcement before canonical source and skeleton updates.
- Automation location: M1 validation commands in the active plan.

### T4. Canonical project-map frontmatter and workflow role satisfy the published-skill contract

- Covers: R1, R2, R3, R4, R5
- Level: integration
- Fixture/setup: Updated `skills/project-map/SKILL.md` after M2.
- Steps: Run `python scripts/validate-skills.py skills/project-map/SKILL.md` and `python scripts/test-skill-validator.py -k project_map`.
- Expected result: Canonical validation passes; if `orientation` is unsupported, either an approved equivalent stage is used or the governing skill contract is amended first.
- Failure proves: The canonical skill is not normalized or relies on an unsupported workflow-role enum.
- Automation location: `scripts/skill_validation.py`; `scripts/test-skill-validator.py`.

### T5. Canonical project-map records modes, result, placement, metadata, and freshness

- Covers: R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29
- Level: integration
- Fixture/setup: Updated canonical `skills/project-map/SKILL.md`.
- Steps: Run project-map canonical tests and inspect validator assertions for required terms or structured sections.
- Expected result: The skill covers `create`, `refresh`, `area`, `audit`, result fields, portable paths, placement lookup, metadata fields, status meanings, baseline variants, refresh triggers, unrelated-change handling, and correction notes.
- Failure proves: The canonical skill omits lifecycle information needed for safe map freshness and downstream reliance.
- Automation location: `scripts/test-skill-validator.py -k project_map`.

### T6. Canonical project-map records evidence classes, material claims, and source ranking

- Covers: R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41
- Level: integration
- Fixture/setup: Updated canonical `skills/project-map/SKILL.md`.
- Steps: Run project-map canonical tests and inspect deterministic assertions for evidence class names, material-claim examples, observed-rule threshold, source-rank ordering, and current-versus-intent conflict handling.
- Expected result: Important current-state claims require repository paths, inference is visibly labeled, unknowns route to open questions, directory names alone are insufficient for material claims, and intent artifacts never prove current behavior.
- Failure proves: The skill can still present unsupported inference or future plans as authoritative current state.
- Automation location: `scripts/test-skill-validator.py -k project_map`.

### T7. Canonical project-map records command and runtime evidence boundaries

- Covers: R42, R43, R44, R45, R46, R47, R48
- Level: integration
- Fixture/setup: Updated canonical `skills/project-map/SKILL.md`.
- Steps: Run project-map canonical tests and inspect assertions for configured/executed command language, exit-code evidence, read-only command allowance, go-ahead for mutating/network/build/test commands, and runtime/data-flow evidence labels.
- Expected result: Configured commands are not described as executed or working unless run, executed commands record exit codes, and static tracing is not implied to be runtime observation.
- Failure proves: The skill still permits unauditable command or runtime claims.
- Automation location: `scripts/test-skill-validator.py -k project_map`.

### T8. Canonical project-map records root and area map contract

- Covers: R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60
- Level: integration
- Fixture/setup: Updated canonical `skills/project-map/SKILL.md` and skeleton asset.
- Steps: Run canonical project-map tests and inspect assertions for root entry point, area registration table columns, parent map, durable-boundary split floor, overlap ownership, contradiction blocking, required headings, and `Not observed` rationale.
- Expected result: Root and area maps have deterministic relationships and area maps do not become one-feature transcripts.
- Failure proves: Area maps can become orphaned, duplicative, or contradictory.
- Automation location: `scripts/test-skill-validator.py -k project_map`.

### T9. Canonical project-map records diagram, downstream reliance, and follow-up boundaries

- Covers: R66, R67, R68, R69, R70, R71, R72, R73, R74, R75, R76, R77
- Level: integration
- Fixture/setup: Updated canonical `skills/project-map/SKILL.md`.
- Steps: Run project-map canonical tests and inspect assertions for diagram rules, safe/unsafe reliance, next-stage options, no automatic downstream stage, and risk/follow-up routing.
- Expected result: Diagrams stay evidence-bound, downstream skills know when source inspection is required, and risk entries do not become execution commitments.
- Failure proves: The skill overstates map authority or turns orientation evidence into workflow commitments.
- Automation location: `scripts/test-skill-validator.py -k project_map`.

### T10. Skeleton asset owns only output structure

- Covers: R58, R59, R60, R61, R62, R63, R64, R65
- Level: integration
- Fixture/setup: `skills/project-map/assets/project-map-skeleton.md` after M2.
- Steps: Run canonical project-map tests and `python scripts/validate-skills.py skills/project-map/SKILL.md`.
- Expected result: The skeleton contains headings, metadata fields, table headers, placeholders, and short fill instructions, but not evidence-ranking rules, inference policy, refresh triggers, future-design prohibitions, handoff rules, or claim boundaries.
- Failure proves: Policy has leaked from `SKILL.md` into a copy-and-fill asset, making the skill harder to audit and maintain.
- Automation location: `scripts/test-skill-validator.py`; `scripts/skill_validation.py`.

### T11. Canonical enforcement rejects corrupted project-map fields or resources

- Covers: R3, R4, R5, R61, R62, R64, R65, R78
- Level: unit
- Fixture/setup: Temporary canonical-like fixtures generated or copied inside validator tests.
- Steps: Corrupt one canonical requirement at a time, such as missing workflow role, missing `COPY` resource-map entry, missing skeleton asset, or hidden skeleton policy.
- Expected result: The validator reports the expected diagnostic and the negative test passes by asserting it.
- Failure proves: Canonical enforcement cannot catch the approved first-slice failures.
- Automation location: `scripts/test-skill-validator.py -k project_map`.

### T12. Representative root and area map outputs prove structure and registration

- Covers: R16, R17, R18, R19, R20, R21, R22, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R65, E1, E2, EC3, EC5, EC10, EC11, EC12
- Level: manual
- Fixture/setup: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md` or equivalent M3 fixture snippets.
- Steps: Inspect root and area map excerpts for metadata, required sections, parent-map field, root registration table, overlap ownership, durable-boundary rationale, `Not observed` rationale, and absence of unfilled placeholders.
- Expected result: Representative outputs are concise, complete enough for the approved contract, and not a full artifact validator.
- Failure proves: The skeleton and skill do not produce the intended map shape in representative output.
- Automation location: M3 evidence artifact; optional fixture assertions in `scripts/test-skill-validator.py`.

### T13. Representative outputs prove evidence labels and current-versus-intent handling

- Covers: R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R66, R67, R68, R69, R70, R71, E1, E3, EC6, EC9
- Level: manual
- Fixture/setup: Representative output excerpts and material-claim examples recorded during M3.
- Steps: Inspect claims labeled observed, inference, and unknown; verify material claims cite repository paths; verify future specs/proposals are not current-state proof; verify any diagram nodes and inferred edges are evidence-bound.
- Expected result: The output distinguishes what exists, what is inferred, what is unknown, and what is only planned.
- Failure proves: The revised skill still allows authoritative-sounding unsupported current-state claims.
- Automation location: M3 evidence artifact; optional fixture assertions in `scripts/test-skill-validator.py`.

### T14. Representative outputs prove command and runtime evidence auditability

- Covers: R42, R43, R44, R45, R46, R47, R48, E4, EC7, EC8
- Level: manual
- Fixture/setup: Representative output excerpt containing configured command, executed command if any, and runtime or data-flow statement.
- Steps: Inspect that configured commands are recorded as configured only when not run, executed commands include exit codes, and runtime/data-flow statements identify static trace, test demonstration, execution observation, or partial inference.
- Expected result: The output never claims command success or runtime observation without actual execution evidence.
- Failure proves: The skill remains unsafe for downstream agents that rely on test, build, or runtime claims.
- Automation location: M3 evidence artifact; optional fixture assertions in `scripts/test-skill-validator.py`.

### T15. Representative outputs prove baselines, stale maps, and correction notes

- Covers: R23, R24, R25, R26, R27, R28, R29, E5, E6, EC1, EC2, EC3, EC4
- Level: manual
- Fixture/setup: Representative outputs for Git available, Git unavailable, dirty working tree, stale map, and wrong-at-baseline correction cases.
- Steps: Inspect baseline format, last-reviewed date, inspected uncommitted paths, refresh-trigger reasoning, unrelated-change handling, and correction note fields.
- Expected result: Freshness is auditable and wrong prior claims are identified as corrections rather than hidden under `stale`.
- Failure proves: Map freshness and prior reliance risk remain ambiguous.
- Automation location: M3 evidence artifact; optional fixture assertions in `scripts/test-skill-validator.py`.

### T16. Behavior-preservation evidence covers the approved matrix

- Covers: R1, R2, R72, R73, R74, R75, R76, R77, R78, R79, R80, R83
- Level: manual
- Fixture/setup: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md`.
- Steps: Inspect the matrix for orientation-only role, current-state focus, eleven-section structure, material path citations, observation/inference split, narrow-area support, risk routing, handoff behavior, and customer-project mode.
- Expected result: Behavior preservation is explicit and does not claim implementation completion, review approval, validation success, branch readiness, or PR readiness.
- Failure proves: The revised skill changed the original mandate or overclaimed downstream readiness.
- Automation location: M3 evidence artifact plus lifecycle validation over the evidence file.

### T17. Cold-read proof covers small, large, and stale-map cases

- Covers: R84
- Level: manual
- Fixture/setup: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md`.
- Steps: Inspect proof for a small repository, monorepo or multi-service fixture, and intentionally stale map, or inspect an accepted pre-implementation deferral with rationale.
- Expected result: A reader can see that the revised skill works across bounded repository shapes without requiring a full project-map artifact validator.
- Failure proves: Cold-read confidence is chat-only or narrower than the approved first-slice requirement.
- Automation location: M3 evidence artifact plus lifecycle validation over the evidence file.

### T18. Generated local skill mirror includes the project-map skeleton

- Covers: R61, R62, R63, R64, R65, R81
- Level: smoke
- Fixture/setup: Canonical skill and skeleton complete after M2.
- Steps: Run `python scripts/build-skills.py --check`.
- Expected result: Generated local skill output is in parity with canonical `skills/project-map/` and includes `assets/project-map-skeleton.md`.
- Failure proves: The packaged skeleton is not reproducibly generated from canonical source.
- Automation location: `scripts/build-skills.py --check`.

### T19. Generated adapter proof includes the project-map skeleton

- Covers: R61, R62, R63, R64, R65, R81
- Level: smoke
- Fixture/setup: Temporary output directory `/tmp/rigorloop-project-map-adapter-proof`.
- Steps: Run `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-project-map-adapter-proof` and `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-project-map-adapter-proof`.
- Expected result: Generated adapter package validation passes and the revised `project-map` skill plus skeleton asset are present in generated output.
- Failure proves: Adapter consumers will not receive the packaged skeleton or generated output is stale.
- Automation location: M4 validation commands.

### T20. Migration and generated-output boundaries hold

- Covers: R1, R2, R12, R13, R14, R15, R20, R21, R22, R72, R73, R74, R75, R76, R77, R82
- Level: manual
- Fixture/setup: Repository after M4.
- Steps: Inspect `git diff --name-only`, change metadata, and generated-output proof.
- Expected result: Existing `docs/project-map.md` is not automatically migrated, generated public adapter bodies are not hand-edited, and downstream reliance remains conditional on map freshness and direct source inspection.
- Failure proves: The implementation exceeded the approved migration and source-of-truth boundary.
- Automation location: `git diff --name-only`; `docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`; M4 validation notes.

### T21. Lifecycle and selected CI checks cover the touched surfaces

- Covers: R78, R81, R82, R83, R84
- Level: smoke
- Fixture/setup: Each milestone closeout with changed files recorded.
- Steps: Run milestone-specific validation commands from the active plan, including change metadata, artifact lifecycle, selected CI, and `git diff --check --`.
- Expected result: Reviewers can tie validation evidence to changed files and lifecycle state without stale plan/index disagreement.
- Failure proves: The change may be functionally correct but not reviewable under the repository workflow contract.
- Automation location: Active plan validation commands and `docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`.

## Fixtures and data

- Controlled skill fixtures under `tests/fixtures/skills/` for M1 valid and invalid project-map contract cases.
- Canonical skill source: `skills/project-map/SKILL.md`.
- Skeleton asset: `skills/project-map/assets/project-map-skeleton.md`.
- Representative output evidence: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md`.
- Behavior-preservation evidence: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md`.
- Cold-read proof: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md`.
- Temporary generated adapter proof: `/tmp/rigorloop-project-map-adapter-proof`.

## Mocking/stubbing policy

- Use controlled Markdown fixtures instead of invoking a model or relying on chat transcripts.
- Negative fixtures must pass by asserting expected diagnostics; do not commit expected-failure tests, temporary skips, or canonical checks known to fail until a later milestone.
- Use temporary directories for generated/corrupted fixture checks.
- Do not mock repository-owned validators when the real script can run against a bounded fixture.

## Migration or compatibility tests

- T20 verifies existing project maps are not automatically migrated.
- T18 and T19 verify generated local mirrors and adapters include the skeleton from canonical source.
- Published `project-map` text must remain customer-portable and must not require RigorLoop repository-internal paths.
- Generated public adapter skill bodies must remain generated output, not hand-edited tracked source.

## Observability verification

- Produced representative maps expose metadata, status, baseline, coverage, exclusions, known gaps, evidence labels, cited paths, configured/executed command distinctions, executed command exit codes, open questions, and correction notes.
- Validation evidence is recorded in the active plan and compact change metadata using the exact commands run and their results.
- No telemetry, remote scanning, or external indexing is introduced or tested.

## Security/privacy verification

- T7 and T14 cover command go-ahead for mutating, network, build, or test execution.
- Published skill text must not require secrets, credentials, private tokens, host-specific paths, or maintainer-only repository internals.
- Adapter proof uses local temporary output and repository-owned validation, not remote package publication.

## Performance checks

- No performance benchmark is required because the change is static skill guidance, fixtures, validators, and generated packaging.
- Manual review checks that the root-map contract remains concise, area maps are used only for durable boundaries, and no full repository scan or full project-map artifact validator is introduced.

## Manual QA checklist

- Confirm material-claim examples include at least two or three worked material versus incidental examples.
- Confirm skeleton asset contains only structure and short fill instructions.
- Confirm representative outputs are concise and contain no unfilled placeholders.
- Confirm the cold-read proof covers small, large, and stale-map scenarios or records an accepted deferral.
- Confirm behavior-preservation evidence does not claim architecture approval, implementation readiness, verification, branch readiness, PR readiness, or final lifecycle closeout.
- Confirm plan body, plan index, and change metadata agree on the current next stage before downstream handoff.

## What not to test and why

- Do not test automatic repository graph generation, language-specific scanners, runtime tracing, remote indexing, or telemetry; they are out of scope.
- Do not build a dedicated project-map artifact validator in the first slice unless the approved drift threshold is met.
- Do not require a full project-map fixture suite for every proposal PMAP check; the approved plan uses focused controlled fixtures plus representative outputs.
- Do not test every repository file or every possible language/runtime flow; the skill is evidence-bound and scope-bounded.
- Do not test automatic migration of existing project maps; migration is explicitly out of scope.
- Do not rely on model-output snapshots as the sole proof of behavioral requirements.

## Uncovered gaps

None. Nuanced prose boundaries are covered by manual evidence artifacts rather than broad natural-language scoring.

## Next artifacts

```text
implement M1. Project-Map Validator and Fixture Scaffolding
code-review M1
implement M2. Canonical Project-Map Skill, Skeleton, and Enforcement
code-review M2
implement M3. Representative Output and Preservation Evidence
code-review M3
implement M4. Generated Adapter Proof and Lifecycle Closeout Preparation
code-review M4
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Active proof-planning surface for the approved project-map plan. Current Handoff Summary names the next stage as `implement M1`; this test spec does not claim implementation completion, review approval, verification, branch readiness, PR readiness, or final lifecycle closeout.
