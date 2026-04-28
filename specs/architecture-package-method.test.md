# Architecture Package Method Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/architecture-package-method.md`
- Plan: `docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Proposal: `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Architecture delta: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`
- ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Spec-review findings: approved on 2026-04-28 after lifecycle, workflow-pointer, and first-slice compatibility corrections.
- Architecture-review findings: approved on 2026-04-28 after lifecycle/status consistency corrections.
- Plan-review findings: approved after M5 was revised to create and populate a legacy architecture lifecycle normalization artifact that inventories every current `docs/architecture/` document.

## Testing strategy

- Lifecycle-regression tests prove the existing artifact lifecycle validator accepts the new canonical `docs/architecture/system/architecture.md` arc42 package shape without weakening legacy architecture validation or adding package-shape enforcement.
- Contract and manual review checks prove templates, governance, workflow guidance, the canonical package, C4 source diagrams, ADRs, and skill guidance match the approved C4, arc42, and ADR method.
- Selector and CI-wrapper checks route architecture support paths to existing lifecycle or regression checks so PR CI does not block on source-text diagrams, change-local architecture deltas, or lifecycle fixtures. This routing is not architecture package enforcement.
- Generated-output checks prove canonical skill changes are propagated only through `scripts/build-skills.py` and `scripts/build-adapters.py`.
- Final validation combines targeted pass gates, manual inventory proof, change metadata validation, artifact lifecycle validation, generated-output drift checks, and broad-smoke execution from the active plan.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R3` | `T1`, `T8`, `T15` | Focused spec ownership, workflow pointer only, and final proof surfaces. |
| `R4`-`R6` | `T5`, `T9`, `T15` | Canonical package source of truth, default path, and migration/supersession expectations. |
| `R7`-`R20` | `T2`, `T5`, `T6`, `T14`, `T15` | All 12 arc42 headings, lifecycle metadata, concise `Not applicable` rationale, section update conditions, ADR summary section, quality/risk/glossary coverage. |
| `R21`-`R29` | `T3`, `T5`, `T11`, `T15` | Default context/container diagrams, conditional diagrams, source-text requirement, Mermaid first implementation, and no binary-only source of truth. |
| `R30`-`R43` | `T4`, `T6`, `T9`, `T15` | Feature update scope, lowest-level C4 propagation, change-local delta paths, merge-back, same-PR review, runtime timing, and leaf-change exclusion. |
| `R44`-`R48` | `T7`, `T14`, `T15` | ADR trigger, required fields, status vocabulary, and append-only decision history. |
| `R49`-`R55` | `T2`, `T7`, `T8`, `T11`, `T15` | Template paths, live-artifact separation, `templates/` canonical-source boundary, governance updates, and workflow summary pointer. |
| `R56`-`R58` | `T10`, `T11`, `T15` | Architecture skill updates and generated output refresh through existing generators only. |
| `R59`-`R66` | `T6`, `T9`, `T15` | Architecture-method change as first real example, prospective adoption, legacy artifact handling, and populated legacy normalization follow-on. |
| `R67`-`R72` | `T12`, `T13`, `T15` | Review-based first implementation, deferred enforcement automation, no new dependencies, narrow lifecycle-validator compatibility, and CI-safe non-enforcement selector routing. |
| `R73`-`R75` | `T2`, `T3`, `T7`, `T8`, `T10`, `T14`, `T15` | No secrets, security/privacy guidance when relevant, and contributor-facing readability. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T5`, `T10`, `T15` | Generated adapter and packaging boundaries are represented in canonical architecture, skills, and final review evidence when affected. |
| `E2` | `T4`, `T13` | Leaf changes are not forced through architecture artifacts or enforcement automation. |
| `E3` | `T4`, `T6`, `T15` | Change-local delta remains working evidence and durable content is merged into the canonical package. |
| `E4` | `T5`, `T7` | Section 9 links ADRs and ADRs record context, decision, alternatives, consequences, and follow-up. |
| `E5` | `T2`, `T5` | All arc42 sections remain present while concise `Not applicable` rationale keeps the package lightweight. |
| `E6` | `T9`, `T15` | Legacy architecture documents are inventoried and classified before any normalized-all claim. |

## Edge case coverage

- EC1, component boundary inside an existing container: `T3`, `T5`, `T10`
- EC2, new external system or actor: `T3`, `T5`
- EC3, generated output or adapter packaging behavior: `T5`, `T10`, `T15`
- EC4, no durable decision after review: `T5`, `T7`
- EC5, independent durable decisions: `T7`
- EC6, rejected or abandoned delta content: `T4`, `T9`
- EC7, legacy architecture documents with older structure: `T9`, `T12`
- EC8, non-Mermaid diagram format needed later: `T3`, `T5`
- EC9, architecture-method change produces a delta: `T4`, `T6`
- EC10, future validator added for this method: `T12`, `T13`

## Acceptance criteria coverage map

| Acceptance criterion | Test IDs | Notes |
| --- | --- | --- |
| `AC1` | `T1`, `T15` | Accepted proposal is linked and remains in lifecycle validation scope. |
| `AC2` | `T1`, `T2`, `T5`, `T7`, `T8` | Spec-defined paths are implemented or reflected in templates and guidance. |
| `AC3` | `T2`, `T5`, `T12` | Ordered arc42 headings appear exactly once where required and validator compatibility is path-scoped. |
| `AC4` | `T3`, `T5` | Context/container diagrams are present and component/deployment diagrams remain conditional. |
| `AC5` | `T3`, `T13` | Required diagrams are source text and binary-only evidence is insufficient. |
| `AC6` | `T4`, `T6` | Merge-back behavior is explicit and reviewed. |
| `AC7` | `T7` | ADR triggers, fields, statuses, and append-only expectations are covered. |
| `AC8` | `T2`, `T8` | Templates live under `templates/` and governance declares the boundary. |
| `AC9` | `T6` | The first positive example is the architecture-method change itself. |
| `AC10` | `T9` | Legacy normalization follow-on inventories and classifies every current architecture document. |
| `AC11` | `T12`, `T13` | Required enforcement automation remains deferred. |
| `AC12` | `T12` | R71 lifecycle-validator compatibility is included before the canonical package is added. |
| `AC13` | `T11`, `T15` | Targeted validation, lifecycle validation, CI wrapper, and diff checks are named and executed. |

## Test cases

### T1. Workflow spec keeps only stage-level routing to the focused method spec

- Covers: `R1`-`R3`, `AC1`, `AC2`
- Level: contract, manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `specs/architecture-package-method.md`
- Steps:
  - Inspect `specs/rigorloop-workflow.md` after M2.
  - Confirm it says architecture-required work produces the architecture package defined by `specs/architecture-package-method.md` before planning continues.
  - Confirm it does not duplicate the full C4, arc42, ADR, template, or lifecycle contract.
  - Run lifecycle validation for both specs.
- Expected result:
  - The focused spec remains the detailed normative home and the workflow spec stays a routing/handoff surface.
- Failure proves:
  - The repository has competing normative homes for the architecture package method.
- Automation location:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/architecture-package-method.md --path specs/rigorloop-workflow.md`
  - manual contract review during M2 and code review

### T2. Architecture template preserves lifecycle metadata and all 12 arc42 sections

- Covers: `R7`-`R20`, `R49`, `R51`-`R53`, `R75`, `AC2`, `AC3`, `AC8`
- Level: contract, manual
- Fixture/setup:
  - `templates/architecture.md`
- Steps:
  - Inspect `templates/architecture.md`.
  - Confirm it starts with repository lifecycle status metadata before the arc42 section sequence.
  - Confirm it contains these headings exactly once and in order: `Introduction and Goals`, `Architecture Constraints`, `Context and Scope`, `Solution Strategy`, `Building Block View`, `Runtime View`, `Deployment View`, `Crosscutting Concepts`, `Architecture Decisions`, `Quality Requirements`, `Risks and Technical Debt`, and `Glossary`.
  - Confirm template guidance allows concise content and `Not applicable` with rationale without renaming or removing sections.
  - Confirm the file is under `templates/`, not under `docs/architecture/`.
- Expected result:
  - Contributors have a scaffold that preserves the official arc42 section model while staying lightweight.
- Failure proves:
  - The template can create non-conforming architecture packages or blur templates with live artifacts.
- Automation location:
  - manual contract review during M2 and code review

### T3. C4 diagram source files are reviewable and default only to context and container

- Covers: `R21`-`R29`, `R73`-`R75`, `AC4`, `AC5`
- Level: manual, selector proof
- Fixture/setup:
  - `docs/architecture/system/diagrams/context.mmd`
  - `docs/architecture/system/diagrams/container.mmd`
- Steps:
  - Inspect both canonical diagram files after M3.
  - Confirm both files are Mermaid `.mmd` source text committed to the repository.
  - Confirm the context diagram shows external actors/systems and the repository system boundary.
  - Confirm the container diagram shows the main repository containers/artifact groups needed for this method.
  - Confirm no generated image, screenshot, or external link is the only source of truth.
  - Run selector inspection for the `.mmd` paths and confirm they route to existing lifecycle context checks without adding C4 content validation.
- Expected result:
  - Required C4 diagrams are diffable source files, selector routing is deterministic for PR CI, and manual review remains the proof surface for diagram sufficiency in this first slice.
- Failure proves:
  - Structural review depends on non-diffable or untracked diagram evidence.
- Automation location:
  - `python scripts/select-validation.py --mode explicit --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd`
  - manual architecture/code-review inspection

### T4. Change-local architecture delta remains working evidence only

- Covers: `R30`-`R43`, `R59`-`R61`, `E2`, `E3`, EC9, `AC6`, `AC9`
- Level: manual, contract
- Fixture/setup:
  - `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`
  - `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/`
  - `docs/architecture/system/architecture.md`
- Steps:
  - Confirm the change-local delta identifies itself as change-local working architecture, not canonical architecture.
  - Confirm durable accepted content is represented in `docs/architecture/system/architecture.md` before final completion.
  - Confirm the delta remains historical evidence after merge-back and does not instruct downstream work to treat it as the current architecture source.
  - Confirm abandoned or rejected delta content is not merged unless a later accepted change adopts it.
- Expected result:
  - The change-local artifact supports review without competing with the canonical package.
- Failure proves:
  - Downstream work could rely on stale or change-local architecture truth.
- Automation location:
  - manual architecture-review, code-review, and verify inspection

### T5. Canonical architecture package uses the official arc42 package shape

- Covers: `R4`-`R29`, `R37`-`R39`, `R59`-`R61`, `R73`-`R75`, `AC2`-`AC7`, `AC9`
- Level: contract, lifecycle, manual
- Fixture/setup:
  - `docs/architecture/system/architecture.md`
  - `docs/architecture/system/diagrams/context.mmd`
  - `docs/architecture/system/diagrams/container.mmd`
  - `docs/adr/ADR-20260428-architecture-package-method.md`
- Steps:
  - Inspect the canonical architecture file after M3.
  - Confirm lifecycle metadata appears before the arc42 section sequence.
  - Confirm all 12 official arc42 headings appear in order and every `Not applicable` entry has rationale.
  - Confirm sections 1 through 5 contain current-system content.
  - Confirm section 6, 7, and 8 cover runtime, packaging/execution boundaries, and cross-cutting rules relevant to this repository change.
  - Confirm section 9 summarizes and links `docs/adr/ADR-20260428-architecture-package-method.md`.
  - Confirm sections 10, 11, and 12 name quality attributes, risks/technical debt, and glossary terms or justified non-applicability.
  - Run lifecycle validation for the canonical package and ADR.
- Expected result:
  - The canonical package becomes the current architecture source of truth with complete arc42 structure and linked decision history.
- Failure proves:
  - The first real package does not satisfy the method it is adopting.
- Automation location:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260428-architecture-package-method.md --path specs/architecture-package-method.md`
  - manual architecture/code-review inspection

### T6. Architecture-method change is the first positive example and is merged back

- Covers: `R30`-`R43`, `R59`-`R61`, `E3`, EC9, `AC6`, `AC9`
- Level: manual, contract
- Fixture/setup:
  - change-local architecture delta and diagrams
  - canonical architecture package and diagrams
  - active plan M3 closeout evidence
- Steps:
  - Confirm the implementation uses the architecture-method change itself as the first positive example.
  - Confirm no synthetic example is the only positive example.
  - Confirm M3 records merge-back of durable content from the delta into the canonical package.
  - Confirm final readiness does not treat the change-local delta as canonical downstream guidance.
- Expected result:
  - The method is dogfooded on this real change before enforcement automation is considered.
- Failure proves:
  - The rollout is based on an artificial or unmerged example.
- Automation location:
  - manual M3 closeout review and verify inspection

### T7. ADR template and architecture-method ADR cover durable decision rules

- Covers: `R44`-`R48`, `R50`-`R52`, `R73`-`R75`, `AC7`, `E4`, EC4, EC5
- Level: lifecycle, contract, manual
- Fixture/setup:
  - `templates/adr.md`
  - `docs/adr/ADR-20260428-architecture-package-method.md`
- Steps:
  - Inspect `templates/adr.md` for title, status, context, decision, alternatives considered, consequences, and follow-up fields.
  - Confirm the template lists or references the approved ADR status vocabulary.
  - Confirm the accepted architecture-method ADR contains required fields and records the durable method decision.
  - Confirm accepted or active ADR guidance is append-only for decision history and supersedes/deprecates later rather than silently rewriting old decisions.
  - Run lifecycle validation for the ADR.
- Expected result:
  - Durable architecture decisions have a clear separate artifact shape and the first method decision is recorded.
- Failure proves:
  - Important architecture decisions can still be buried in prose or rewritten without trace.
- Automation location:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/adr/ADR-20260428-architecture-package-method.md`
  - manual contract review

### T8. Governance and workflow docs declare the templates source boundary

- Covers: `R2`, `R3`, `R49`-`R55`, `R70`, `R75`, `AC2`, `AC8`
- Level: selector, integration, manual
- Fixture/setup:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `templates/architecture.md`
  - `templates/adr.md`
- Steps:
  - Confirm `CONSTITUTION.md` and `AGENTS.md` include `templates/` as canonical authored workflow content after M2.
  - Confirm `docs/workflows.md` gives concise contributor guidance and points to `specs/architecture-package-method.md`.
  - Confirm `specs/rigorloop-workflow.md` remains a stage-level pointer rather than a duplicate package contract.
  - Confirm no new external dependency is introduced for templates, guidance, Markdown, Mermaid, or ADR authoring.
  - Run selector and CI wrapper commands for the touched governance, workflow, spec, and template paths.
- Expected result:
  - Contributors can distinguish templates from live artifacts and find the normative package contract.
- Failure proves:
  - The new template boundary is ambiguous or undocumented.
- Automation location:
  - `python scripts/select-validation.py --mode explicit --path templates/architecture.md --path templates/adr.md --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`
  - `bash scripts/ci.sh --mode explicit --path templates/architecture.md --path templates/adr.md --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`

### T9. Legacy architecture normalization follow-on inventories every current architecture document

- Covers: `R4`-`R6`, `R37`-`R39`, `R61`-`R66`, `AC10`, EC6, EC7
- Level: manual, lifecycle
- Fixture/setup:
  - `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
  - current `docs/architecture/` tree
- Steps:
  - Run `find docs/architecture -type f | sort`.
  - Confirm every path in that output appears in the follow-on normalization artifact.
  - Confirm every inventoried document is classified as `current canonical content`, `superseded`, `archived/historical snapshot`, or another explicitly documented historical status.
  - Confirm each classification has rationale, canonical replacement or merge-back target where applicable, and remaining follow-up work.
  - Confirm repository guidance does not claim all legacy architecture artifacts are already normalized until this follow-on work is complete.
  - Run lifecycle validation for the follow-on artifact.
- Expected result:
  - Legacy documents are not silently normalized or ignored.
- Failure proves:
  - The repository could overstate the state of its architecture baseline.
- Automation location:
  - `find docs/architecture -type f | sort`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
  - manual inventory comparison

### T10. Architecture skills teach and review the C4, arc42, ADR package method

- Covers: `R56`-`R58`, `R73`-`R75`, `AC4`, `AC5`, `AC7`, `AC11`, EC1, EC3
- Level: contract, integration, generated-output proof
- Fixture/setup:
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - generated `.codex/skills/`
  - generated `dist/adapters/`
- Steps:
  - Inspect `skills/architecture/SKILL.md` for canonical package, change-local delta, all 12 arc42 sections, C4 context/container diagrams, ADR triggers, merge-back, leaf-change exclusion, and full-file-read guidance.
  - Inspect `skills/architecture-review/SKILL.md` for C4 sufficiency, all 12 arc42 sections, Runtime View and Deployment View conditions, change-local merge-back, legacy status, ADR completeness, and full-file-read guidance.
  - Run skill validation and skill regression tests.
  - Refresh generated `.codex/skills/` with `python scripts/build-skills.py` and public adapters with `python scripts/build-adapters.py --version 0.1.1`.
  - Run generated-output drift and adapter validation checks.
- Expected result:
  - Canonical and generated skill surfaces consistently teach and review the approved method.
- Failure proves:
  - Contributors or downstream adapter users can receive stale architecture guidance.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T11. Selector and CI routing cover supported implementation surfaces

- Covers: `R49`-`R58`, `R73`-`R75`, `AC8`, `AC13`
- Level: selector, smoke
- Fixture/setup:
  - completed M2 and M4 changed paths
  - existing selector and CI wrapper
- Steps:
  - Run selector for template, governance, workflow, spec, canonical skill, generated skill, adapter manifest, and adapter output paths.
  - Confirm supported paths select expected lifecycle, template, governance, workflow, skill, adapter, and generated-output checks.
  - Run the exact M2 and M4 CI wrapper commands from the plan.
  - Confirm `.mmd` diagram paths and change-local architecture paths are manual-routed where selector support is intentionally absent.
- Expected result:
  - Supported validation routing is exercised and unsupported diagram/change-local paths are explicitly manual-routed.
- Failure proves:
  - Implementation evidence could miss a supported proof surface or fail open on unsupported paths.
- Automation location:
  - `python scripts/select-validation.py --mode explicit ...`
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit ...`

### T12. Lifecycle-validator compatibility is path-scoped and non-enforcing

- Covers: `R7`-`R12`, `R67`-`R72`, `AC3`, `AC11`, `AC12`, EC7, EC10
- Level: unit, integration
- Fixture/setup:
  - `scripts/artifact_lifecycle_contracts.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/artifact-lifecycle/`
- Steps:
  - Add a canonical system architecture fixture with lifecycle metadata and all 12 official arc42 sections.
  - Assert that fixture passes only at `docs/architecture/system/architecture.md`.
  - Assert existing legacy architecture fixtures still require the older architecture contract unless explicitly out of scope.
  - Assert missing status, invalid lifecycle status, placeholders, stale readiness, terminal closeout, and generated-output rejection behavior remain unchanged.
  - Assert compatibility does not require C4 diagram files, ADR presence, or package-shape validation.
  - Run the M1 pass-gate commands.
- Expected result:
  - The new canonical arc42 package can be added without turning the first implementation into a broader enforcement validator.
- Failure proves:
  - Compatibility either fails the canonical package or weakens unrelated lifecycle validation.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`

### T13. First implementation does not add forbidden enforcement or dependencies

- Covers: `R67`-`R72`, `R43`, `AC11`, EC2, EC10
- Level: code review, manual, selector proof
- Fixture/setup:
  - full implementation diff
  - validation selector output
  - dependency metadata, if any
- Steps:
  - Inspect the diff for new required structural architecture validators, required C4 diagram file checks, ADR-presence enforcement, or package-shape enforcement.
  - Confirm no new external dependency is added solely for Markdown templates, Mermaid diagrams, ADRs, or architecture guidance.
  - Confirm lifecycle-validator changes are limited to accepting `docs/architecture/system/architecture.md` with the official arc42 shape.
  - Confirm command output and command exit behavior are not changed by M1.
  - Confirm selector routing for architecture diagrams, change-local architecture deltas, and lifecycle fixtures uses only existing non-enforcement lifecycle or regression checks.
  - Confirm leaf changes remain exempt from architecture package updates.
- Expected result:
  - The first slice stays review-based and proportional.
- Failure proves:
  - The implementation exceeds the approved automation and dependency boundary.
- Automation location:
  - code review, verify inspection, `python scripts/test-select-validation.py`, and M1 regression tests

### T14. Architecture artifacts, templates, diagrams, and ADRs avoid sensitive data and stay readable

- Covers: `R18`-`R20`, `R44`-`R48`, `R73`-`R75`
- Level: manual, security/privacy
- Fixture/setup:
  - touched Markdown architecture, template, ADR, workflow, governance, and skill files
  - touched `.mmd` diagrams
- Steps:
  - Inspect touched architecture artifacts, diagrams, templates, ADRs, and skill guidance for secrets, credentials, private keys, tokens, and machine-local debug-only data.
  - Confirm security/privacy concerns are described when a change affects trust boundaries, permissions, data exposure, or secret handling.
  - Confirm headings, paths, and prose are clear enough for ordinary repository review tools.
- Expected result:
  - Architecture documentation remains safe to publish and efficient to review.
- Failure proves:
  - The first package method rollout leaked sensitive data or produced hard-to-review guidance.
- Automation location:
  - manual code-review and verify inspection

### T15. Final validation proves artifact, generated-output, and lifecycle coherence

- Covers: `R1`-`R75`, `AC1`-`AC13`
- Level: smoke, lifecycle, selector, manual
- Fixture/setup:
  - completed M1 through M5 implementation
  - active plan and this test spec
  - change metadata
- Steps:
  - Run every milestone pass-gate command named in `docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md`.
  - Run final change metadata validation.
  - Run final artifact lifecycle validation for the proposal, spec, this test spec, ADR, canonical architecture, active plan, legacy normalization follow-on artifact, and change metadata.
  - Run `bash scripts/ci.sh --mode broad-smoke` before final PR readiness.
  - Run PR-mode selector or CI proof against the actual branch diff to confirm architecture support paths do not block as unclassified.
  - Run `git diff --check -- .`.
  - Confirm plan validation notes and change metadata name the commands actually run.
- Expected result:
  - The branch is ready for code-review and verify after all implementation milestones satisfy their targeted proof.
- Failure proves:
  - The rollout has unresolved lifecycle, validation, generated-output, or documentation drift.
- Automation location:
  - commands named in the active execution plan

## Fixtures and data

- Existing lifecycle fixtures under `tests/fixtures/artifact-lifecycle/`.
- New lifecycle fixture for a valid canonical arc42 architecture package under `tests/fixtures/artifact-lifecycle/`.
- Existing valid legacy architecture fixture under `tests/fixtures/artifact-lifecycle/valid-architecture/`.
- Existing invalid lifecycle fixtures for missing or invalid status, stale readiness, terminal closeout, placeholders, generated output rejection, and superseded-without-pointer behavior.
- Current legacy architecture inventory from `find docs/architecture -type f | sort`.
- The architecture-method change-local delta and diagrams under `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/`.
- Generated skill and adapter outputs refreshed from canonical skill sources through existing repository commands.

## Mocking/stubbing policy

- Prefer real repository fixtures, temporary filesystem fixtures, and existing CLI commands over mocks for lifecycle validation, selector routing, skill validation, adapter generation, and change metadata validation.
- Do not mock final selector output, lifecycle validation, generated-output drift checks, or adapter validation in final milestone proof.
- Manual review is the intended first-slice proof for C4 diagram sufficiency, package completeness beyond lifecycle compatibility, change-local merge-back, no-sensitive-data review, and legacy inventory comparison.
- Unit tests may construct small Markdown fixture trees when that is clearer than mutating the live repository tree.

## Migration or compatibility tests

- Legacy architecture documents under `docs/architecture/*.md` continue to validate against the older lifecycle contract until normalized: `T9`, `T12`.
- The new canonical path `docs/architecture/system/architecture.md` validates with the official arc42 section model after M1: `T5`, `T12`.
- `.codex/skills/` and `dist/adapters/` remain generated output and are refreshed only through existing generators: `T10`, `T11`.
- First implementation does not change runtime behavior, public APIs, release artifacts, or command behavior outside the narrow lifecycle compatibility and CI-safe non-enforcement selector routing allowed by `R71` and `R72`: `T12`, `T13`, `T15`.
- Rollback remains documentation and generated-output rollback only; no runtime data migration is required: `T15`.

## Observability verification

- No runtime logs, metrics, traces, or audit events are required.
- Observable proof is repository artifact state, lifecycle status, selector output, generated-output drift checks, adapter validation, plan validation notes, change metadata, and final validation commands.
- Review evidence should use stable requirement IDs, test IDs, file paths, and command names rather than large raw excerpts.

## Security/privacy verification

- Touched architecture artifacts, diagrams, templates, ADRs, workflow guidance, and skill guidance must not include secrets, credentials, private keys, tokens, or machine-local debug-only data: `T14`.
- Security or privacy boundaries must be described when the architecture change affects trust boundaries, permissions, data exposure, or secret handling: `T14`.
- No test requires network access, hosted CI, credentials, or installed external agent tools.

## Performance checks

- No runtime performance benchmark is required because this method changes documentation, workflow guidance, templates, lifecycle compatibility, skills, and generated outputs rather than a service runtime.
- Review overhead is checked qualitatively by confirming the package remains concise, keeps component/deployment diagrams conditional, and avoids required enforcement automation in the first slice: `T2`, `T3`, `T13`.

## Manual QA checklist

- Confirm `templates/architecture.md` and `docs/architecture/system/architecture.md` use all 12 official arc42 headings in order.
- Confirm section 9 of the canonical package links `docs/adr/ADR-20260428-architecture-package-method.md`.
- Confirm the context and container diagrams are Mermaid source text.
- Confirm the change-local delta is historical after merge-back and not the canonical source for downstream work.
- Confirm `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` inventories every path from `find docs/architecture -type f | sort`.
- Confirm `.codex/skills/` and `dist/adapters/` changes came from generator commands.
- Confirm the implementation did not add required architecture package enforcement automation or new external dependencies.
- Confirm plan validation notes and change metadata name the commands actually run.

## What not to test

- Do not add or require package-shape, required C4-file, ADR-presence, or full architecture-package enforcement automation in this first implementation.
- Do not test runtime services, databases, public APIs, or network behavior; the approved change has no such surface.
- Do not require hosted CI status or installed Codex, Claude Code, or opencode tools as proof.
- Do not test image rendering of diagrams as the source of truth; committed source-text diagrams are the required proof.
- Do not use broad smoke as a substitute for milestone-specific tests and manual review checks.

## Uncovered gaps

- No uncovered spec gaps. Requirements that are intentionally not automated in the first implementation are covered by explicit manual review, selector inspection, lifecycle compatibility tests, or final validation evidence.

## Next artifacts

- `implement` for M1 through M5 in `docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md`.
- `code-review` after implementation completes and plan validation notes are current.
- `verify` after code-review is clean or findings are resolved.
- `explain-change` and `pr` after verify reports branch readiness.

## Follow-on artifacts

- None yet.

## Readiness

This test spec is active as the proof map for the architecture package method rollout.

Immediate next repository stage: `implement`.
