# Architecture Package Method Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/architecture-package-method.md`
- Original rollout plan: `docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Current refinement plan: `docs/plans/2026-04-29-c4-arc42-package-quality.md`
- Current simplification plan: `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
- Proposal: `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Proposal refinement: `docs/proposals/2026-04-29-c4-arc42-package-quality.md`
- Simplification proposal: `docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md`
- Architecture delta: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`
- Package-quality architecture delta: `docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md`
- Canonical architecture package: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Simplification ADR: `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`
- Spec-review findings: approved on 2026-04-28 after lifecycle, workflow-pointer, and first-slice compatibility corrections.
- Spec-review findings for package-quality refinement: approved on 2026-04-29 after diagram source wording and architecture-review material-finding contract wording were corrected.
- Architecture-review findings: approved on 2026-04-28 after lifecycle/status consistency corrections.
- Architecture-review findings for package-quality refinement: approved on 2026-04-29 with no findings.
- Plan-review findings: approved after M5 was revised to create and populate a legacy architecture lifecycle normalization artifact that inventories every current `docs/architecture/` document.
- Plan-review findings for package-quality refinement: approved on 2026-04-29 after PR-F1 corrected M5 sequencing so `code-review` and `verify` remain downstream gates.
- Spec-review findings for simplification: approved on 2026-05-09 with no material findings.
- Architecture-review findings for simplification: approved on 2026-05-09 with no material findings.
- Plan-review findings for simplification: approved on 2026-05-09 after PR-F1 corrected per-milestone code-review sequencing.

## Testing strategy

- Lifecycle-regression tests prove the existing artifact lifecycle validator accepts the new canonical `docs/architecture/system/architecture.md` arc42 package shape without weakening legacy architecture validation or adding package-shape enforcement.
- Contract and manual review checks prove templates, governance, workflow guidance, the canonical package, C4 source diagrams, ADRs, and skill guidance match the approved C4, arc42, and ADR method.
- Selector and CI-wrapper checks route architecture support paths to existing lifecycle or regression checks so PR CI does not block on source-text diagrams, change-local architecture deltas, or lifecycle fixtures. This routing is not architecture package enforcement.
- Generated-output checks prove canonical skill changes are propagated only through `scripts/build-skills.py` and `scripts/build-adapters.py`.
- Final validation combines targeted pass gates, manual inventory proof, change metadata validation, artifact lifecycle validation, generated-output drift checks, and broad-smoke execution from the active plan.
- The 2026-04-29 package-quality refinement adds contract and manual review checks for one-source diagram policy, relative links, C4 semantic styling, component-diagram discipline, hierarchical Building Block View content, link-focused ADR summaries, quality scenarios, concise skills, and architecture-review finding shape.
- The current refinement remains review-based for C4 sufficiency and architecture package shape; existing validators prove lifecycle, selector routing, skill shape, generated-output drift, adapter validity, and broad-smoke health.
- The 2026-05-09 simplification keeps C4, arc42, and ADRs while changing the normal architecture authoring and review surfaces. Contract and static checks prove architecture authoring chooses no-impact rationale, canonical update, ADR, or proposal/spec blocker instead of normal change-local deltas.
- Architecture-review simplification proof starts with review-surface classification and then applies surface-specific checks for canonical architecture updates, ADRs, no-impact rationale, and proposal/spec gaps.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R3` | `T1`, `T8`, `T15` | Focused spec ownership, workflow pointer only, and final proof surfaces. |
| `R4`-`R6` | `T5`, `T9`, `T15` | Canonical package source of truth, default path, and migration/supersession expectations. |
| `R7`-`R20` | `T2`, `T5`, `T6`, `T14`, `T15` | All 12 arc42 headings, lifecycle metadata, concise `Not applicable` rationale, section update conditions, ADR summary section, quality/risk/glossary coverage. |
| `R21`-`R29` | `T3`, `T5`, `T11`, `T15` | Default context/container diagrams, conditional diagrams, source-text requirement, Mermaid first implementation, and no binary-only source of truth. |
| `R30`-`R43` | `T4`, `T5`, `T6`, `T9`, `T15`, `T23` | Feature update scope, lowest-level C4 propagation, non-normal change-local delta status, canonical current truth, same-PR review, runtime timing, and leaf-change exclusion. |
| `R44`-`R48` | `T7`, `T14`, `T15` | ADR trigger, required fields, status vocabulary, and append-only decision history. |
| `R49`-`R55` | `T2`, `T7`, `T8`, `T11`, `T15` | Template paths, live-artifact separation, `templates/` canonical-source boundary, governance updates, and workflow summary pointer. |
| `R56`-`R58` | `T10`, `T11`, `T15`, `T21`, `T25` | Architecture skill updates, architecture-review surface classification, and generated output refresh through existing generators only. |
| `R59`-`R66` | `T6`, `T9`, `T15`, `T23` | Architecture-method change as first real example, prospective adoption, legacy artifact handling, populated legacy normalization follow-on, and no reliance on normal change-local delta authoring. |
| `R67`-`R72` | `T12`, `T13`, `T15` | Review-based first implementation, deferred enforcement automation, no new dependencies, narrow lifecycle-validator compatibility, and CI-safe non-enforcement selector routing. |
| `R73`-`R75` | `T2`, `T3`, `T7`, `T8`, `T10`, `T14`, `T15` | No secrets, security/privacy guidance when relevant, and contributor-facing readability. |
| `R76`-`R86` | `T16`, `T22` | Separate authored diagram source files, relative links, default `.mmd` diagrams, generated image boundary, inherited diagram lifecycle, and change-local diagram lifecycle. |
| `R87`-`R95` | `T17`, `T22` | C4 semantics for native Mermaid C4 or flowchart/graph diagrams, shared role styling, technology labels, intent-labeled relationships, context/container level discipline, and component-diagram threshold. |
| `R96`-`R104` | `T18`, `T22` | Hierarchical Building Block View, concise ADR links, no duplicated ADR rationale, quality scenarios, `Not applicable` rationale, and Deployment View packaging/execution boundary content. |
| `R105`-`R107` | `T16`, `T18`, `T22` | Shared diagram style template and architecture template guidance for diagram links, separate sources, hierarchy, deployment, and ADR summaries. |
| `R108`-`R111` | `T19`, `T21`, `T22`, `T23`, `T25` | Concise architecture skill content, smallest-valid-surface output shape, minimal C4 snippets, ADR triggers, and external location for full worked examples. |
| `R112`-`R118` | `T20`, `T21`, `T22`, `T24`, `T25` | Architecture-review finding fields, severity vocabulary, location requirement, no mandatory C4-level taxonomy, material-finding contract preservation, and optional future category field boundary. |
| `R119`-`R124` | `T20`, `T21`, `T24`, `T25` | Architecture-review surface classification, no delta requirement for canonical architecture updates, ADR review, no-impact rationale credibility, and proposal/spec gap routing. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T5`, `T10`, `T15` | Generated adapter and packaging boundaries are represented in canonical architecture, skills, and final review evidence when affected. |
| `E2` | `T4`, `T13` | Leaf changes are not forced through architecture artifacts or enforcement automation. |
| `E3` | `T4`, `T6`, `T15`, `T23` | Existing change-local delta remains historical evidence, new deltas are legacy-closeout or explicit exceptional evidence only, and durable current truth lives in the canonical package. |
| `E4` | `T5`, `T7` | Section 9 links ADRs and ADRs record context, decision, alternatives, consequences, and follow-up. |
| `E5` | `T2`, `T5` | All arc42 sections remain present while concise `Not applicable` rationale keeps the package lightweight. |
| `E6` | `T9`, `T15` | Legacy architecture documents are inventoried and classified before any normalized-all claim. |
| `E7` | `T16` | Architecture documents link separate diagram source files by relative path without embedding or duplicating Mermaid source. |
| `E8` | `T17` | Mermaid flowchart diagrams carry C4 role classes, technology labels, and intent-labeled relationships. |
| `E9` | `T17`, `T18` | Component diagrams remain conditional and are added only when refined container and Building Block prose are insufficient. |
| `E10` | `T20` | Architecture-review findings use finding, location, severity, and recommendation, while material findings also keep repository-wide evidence and resolution fields. |
| `E11` | `T23`, `T24` | Architecture records accepted design in canonical surfaces or ADRs while proposal/spec own unresolved direction or behavior. |

## Edge case coverage

- EC1, component boundary inside an existing container: `T3`, `T5`, `T10`
- EC2, new external system or actor: `T3`, `T5`
- EC3, generated output or adapter packaging behavior: `T5`, `T10`, `T15`
- EC4, no durable decision after review: `T5`, `T7`
- EC5, independent durable decisions: `T7`
- EC6, rejected or abandoned delta content: `T4`, `T9`, `T23`
- EC7, legacy architecture documents with older structure: `T9`, `T12`
- EC8, non-Mermaid diagram format needed later: `T3`, `T5`
- EC9, architecture-method change uses direct canonical update and ADR instead of normal delta authoring: `T4`, `T6`, `T23`
- EC10, future validator added for this method: `T12`, `T13`
- EC11, architecture document links to a diagram outside its package: `T16`
- EC12, Mermaid native C4 syntax is impractical in the review surface: `T17`
- EC13, component diagram requested before the container view is clear: `T17`, `T18`
- EC14, quality requirement cannot be made measurable: `T18`
- EC15, review finding spans multiple C4 levels or contradicts another arc42 section: `T20`
- EC16, architecture work has no architecture impact: `T23`, `T24`
- EC17, architecture work exposes unsettled direction or behavior: `T23`, `T24`

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
| `AC14` | `T16`, `T22` | One authored source file per diagram, default Mermaid `.mmd`, and relative links from `architecture.md`. |
| `AC15` | `T17`, `T22` | C4 semantics through native Mermaid C4 or shared flowchart/graph styling. |
| `AC16` | `T16`, `T22` | `templates/diagram-styles.mmd` and commented quality-scenario scaffold. |
| `AC17` | `T17`, `T18`, `T22` | Container-first component diagram discipline and Building Block View hierarchy. |
| `AC18` | `T19`, `T21`, `T22` | Concise architecture-skill content and full worked examples outside the skill body. |
| `AC19` | `T20`, `T22` | Simple architecture-review finding shape, material-finding contract preservation, and no mandatory C4-level classification. |
| `AC20` | `T21`, `T22` | Generated `.codex/skills/` and `dist/adapters/` output refreshed through existing generators when canonical skill guidance changes. |
| `AC21` | `T4`, `T19`, `T23`, `T25` | Change-local architecture deltas are removed from the normal authoring path while preserving historical, legacy-closeout, and explicit exceptional evidence. |
| `AC22` | `T20`, `T24`, `T25` | Architecture-review classifies the review surface first and does not require a change-local delta for canonical architecture updates. |

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

### T4. Change-local architecture deltas are historical or exceptional evidence only

- Covers: `R30`-`R43`, `R59`-`R61`, `E2`, `E3`, EC6, EC9, `AC6`, `AC9`, `AC21`
- Level: manual, contract
- Fixture/setup:
  - `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`
  - `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/`
  - `docs/architecture/system/architecture.md`
  - `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`
- Steps:
  - Confirm existing change-local architecture deltas are treated as historical evidence, not the normal authoring path for new architecture work.
  - Confirm new architecture work in the simplification change uses direct canonical architecture updates and an ADR instead of a normal change-local delta.
  - Confirm durable accepted content is represented in `docs/architecture/system/architecture.md` when current system shape changes.
  - Confirm the historical delta does not instruct downstream work to treat it as the current architecture source.
  - Confirm abandoned or rejected delta content is not merged unless a later accepted change adopts it.
  - Confirm any new delta language allows only legacy closeout or explicit exceptional evidence.
- Expected result:
  - Existing change-local artifacts remain valid history without competing with the canonical package or remaining a default recommendation.
- Failure proves:
  - Downstream work could rely on stale or change-local architecture truth, or contributors could keep treating deltas as a normal architecture skill output.
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

### T6. Architecture-method change is the first positive example using canonical surfaces

- Covers: `R30`-`R43`, `R59`-`R61`, `E3`, EC9, `AC6`, `AC9`
- Level: manual, contract
- Fixture/setup:
  - canonical architecture package and diagrams
  - `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`
  - active plan M3 closeout evidence
- Steps:
  - Confirm the implementation uses the architecture-method change itself as the first positive example.
  - Confirm no synthetic example is the only positive example.
  - Confirm simplification durable architecture content is represented directly in the canonical package and ADR.
  - Confirm final readiness does not treat a change-local architecture delta as canonical downstream guidance.
- Expected result:
  - The method is dogfooded on this real change using canonical architecture and ADR surfaces before enforcement automation is considered.
- Failure proves:
  - The rollout is based on an artificial example or continues to rely on normal change-local delta authoring.
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
  - Inspect `skills/architecture/SKILL.md` for canonical package guidance, historical or exceptional delta boundaries, all 12 arc42 sections, C4 context/container diagrams, ADR triggers, leaf-change exclusion, and full-file-read guidance.
  - Inspect `skills/architecture-review/SKILL.md` for C4 sufficiency, all 12 arc42 sections, Runtime View and Deployment View conditions, surface classification, legacy status, ADR completeness, and full-file-read guidance.
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

### T16. Diagram-source policy and template scaffolding are reviewable

- Covers: `R76`-`R86`, `R101`, `R105`-`R107`, `E7`, EC11, `AC14`, `AC16`
- Level: contract, manual, selector
- Fixture/setup:
  - `docs/architecture/system/architecture.md`
  - `docs/architecture/system/diagrams/context.mmd`
  - `docs/architecture/system/diagrams/container.mmd`
  - `templates/architecture.md`
  - `templates/diagram-styles.mmd`
- Steps:
  - Inspect `docs/architecture/system/architecture.md` and `templates/architecture.md`.
  - Confirm package diagrams are linked with clickable relative Markdown links such as `diagrams/context.mmd` and `diagrams/container.mmd`.
  - Confirm `architecture.md` does not embed Mermaid blocks for package diagrams and does not duplicate diagram source.
  - Confirm default package diagrams are separate `.mmd` files under the package `diagrams/` directory and use lowercase kebab-case names.
  - Confirm diagram source files do not carry independent lifecycle status metadata.
  - Confirm generated images, if any are introduced later, are not treated as authored diagram sources.
  - Confirm `templates/diagram-styles.mmd` exists and `templates/architecture.md` includes a section 10 quality-scenario scaffold as a Markdown comment, not rendered placeholder content.
  - Run the M1 selector and CI wrapper commands from `docs/plans/2026-04-29-c4-arc42-package-quality.md`.
- Expected result:
  - Authors have canonical source-file and template scaffolding that preserves one authored diagram source per diagram and relative links from architecture documents.
- Failure proves:
  - Diagram source can be duplicated, embedded, rendered as placeholder content, or confused with generated output.
- Automation location:
  - `rg -n "diagram-styles|diagrams/context\\.mmd|diagrams/container\\.mmd|Quality scenarios|Building Block View|Architecture Decisions|Deployment View" templates/architecture.md templates/diagram-styles.mmd`
  - M1 selector and CI wrapper commands from `docs/plans/2026-04-29-c4-arc42-package-quality.md`
  - manual code-review inspection

### T17. C4 diagram semantics remain visible in source

- Covers: `R87`-`R95`, `E8`, `E9`, EC12, EC13, `AC15`, `AC17`
- Level: manual, contract
- Fixture/setup:
  - `docs/architecture/system/diagrams/context.mmd`
  - `docs/architecture/system/diagrams/container.mmd`
  - `templates/diagram-styles.mmd`
  - `docs/architecture/system/architecture.md`
- Steps:
  - Inspect Mermaid diagram source after M1 and architecture-stage updates.
  - Confirm flowchart or graph diagrams use shared or equivalent C4 role classes for people, the system under review, external systems, and containers.
  - Confirm container labels include relevant technologies in the `Name<br/>[Technology]` form.
  - Confirm relationships are labeled with intent.
  - Confirm the context diagram treats RigorLoop as one system under review and does not decompose internal containers.
  - Confirm the container diagram shows major containers, relevant actors or external systems, technology annotations, and intent-labeled relationships.
  - Confirm no component diagram is added unless the refined container diagram and Building Block View cannot explain important internals.
- Expected result:
  - Reviewers can distinguish C4 roles and levels from committed text source without requiring image rendering.
- Failure proves:
  - Diagrams have regressed into generic flowcharts or component detail was added before the container view earned it.
- Automation location:
  - manual architecture/code-review inspection
  - M1 template/style inspection command

### T18. arc42 content quality is hierarchical, link-focused, and scenario-aware

- Covers: `R96`-`R104`, `R107`, `E9`, EC14, `AC17`
- Level: manual, contract
- Fixture/setup:
  - `docs/architecture/system/architecture.md`
  - `templates/architecture.md`
  - `docs/adr/ADR-20260428-architecture-package-method.md`
- Steps:
  - Inspect the Building Block View in the canonical package and template guidance.
  - Confirm the Building Block View describes a system-level white-box view and decomposes important containers or responsibilities when needed, rather than acting as only a flat folder catalog.
  - Confirm section 9 links ADRs concisely and does not duplicate detailed ADR rationale.
  - Confirm Quality Requirements use lightweight scenarios when substantive quality requirements are present, or `Not applicable` with a one-line rationale when genuinely irrelevant.
  - Confirm Deployment View explains packaging, publication or distribution, generated artifacts, release evidence, and execution boundaries when relevant without repeating source layout details unnecessarily.
- Expected result:
  - The package and template guide contributors toward reviewable arc42 content rather than prose-only or table-only placeholders.
- Failure proves:
  - The architecture package can look structurally complete while missing hierarchy, decision ownership, deployment boundaries, or usable quality evidence.
- Automation location:
  - manual architecture/code-review inspection
  - M1 template inspection command

### T19. Architecture skill stays concise and process-focused

- Covers: `R108`-`R111`, `R32`-`R39`, `AC18`, `AC21`
- Level: contract, integration
- Fixture/setup:
  - `skills/architecture/SKILL.md`
  - optional `skills/architecture/references/architecture-example.md`
  - generated `.codex/skills/architecture/SKILL.md`
  - generated adapter skill output after M4
- Steps:
  - Inspect `skills/architecture/SKILL.md` after M2.
  - Confirm it includes one short output shape that directs authors to choose the smallest valid architecture surface: no-impact rationale, canonical architecture package update, ADR creation or update, or blocked routing to proposal/spec readiness.
  - Confirm it does not direct authors to create change-local architecture deltas as a normal authoring path.
  - Confirm it preserves portable canonical architecture wording instead of imposing RigorLoop-only architecture paths on downstream projects.
  - Confirm it includes one minimal C4 context snippet, one minimal C4 container snippet, one ADR trigger list, and one when-to-use/when-not-to-use section.
  - Confirm it does not include a full worked architecture example in the skill body.
  - Confirm any full worked example, if added, lives under a reference path such as `skills/architecture/references/architecture-example.md`.
  - Confirm scan-sensitive evidence guidance and full-file-read guidance remain present.
  - Run the M2 skill validation and CI wrapper commands from the plan.
- Expected result:
  - Architecture authors receive compact process guidance while structure lives in templates and style examples live in references.
- Failure proves:
  - The skill can become too verbose, omit required authoring cues, or drift from generated output.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - M2 selector and CI wrapper commands from `docs/plans/2026-04-29-c4-arc42-package-quality.md`

### T20. Architecture-review finding format preserves material-finding safeguards

- Covers: `R112`-`R124`, `E10`, E11, EC15, EC16, EC17, `AC19`, `AC22`
- Level: contract, integration
- Fixture/setup:
  - `skills/architecture-review/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `scripts/test-review-artifact-validator.py`
- Steps:
  - Inspect `skills/architecture-review/SKILL.md` after M3.
  - Confirm architecture-review first classifies the review surface as `canonical-architecture-update`, `ADR`, `no-architecture-impact-rationale`, or `proposal-or-spec-gap`.
  - Confirm it does not require a change-local architecture delta for a canonical architecture update.
  - Confirm canonical architecture updates are reviewed against changed canonical sections, diagrams, and ADR links directly.
  - Confirm ADR surfaces are reviewed for context, decision, alternatives, consequences, and compatibility with canonical architecture.
  - Confirm no-impact rationale is checked for credibility.
  - Confirm unsettled direction routes to proposal or proposal revision and unsettled behavior routes to spec or spec revision.
  - Confirm architecture-review findings record finding, location, severity, and recommendation.
  - Confirm severity values are `blocker`, `material`, and `minor`.
  - Confirm finding location can be a file path and section or line, or a diagram name.
  - Confirm the skill does not require mandatory C4-level classification.
  - Confirm the simple architecture-review format explicitly does not replace the repository-wide material-finding contract.
  - Confirm material findings still require evidence, required outcome, and a safe resolution path or `needs-decision` rationale.
  - Confirm any later finding category remains out of scope unless a later approved change adds it.
- Expected result:
  - Architecture-review remains lightweight for ordinary findings and complete for material findings.
- Failure proves:
  - Reviews could lose required material-finding evidence or spend effort on a noisy C4-level taxonomy.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - M3 selector and CI wrapper commands from `docs/plans/2026-04-29-c4-arc42-package-quality.md`

### T21. Generated architecture skill outputs are refreshed through generators

- Covers: `R58`, `R108`-`R124`, `AC20`, `AC21`, `AC22`
- Level: integration, generated-output proof
- Fixture/setup:
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `.codex/skills/architecture/SKILL.md`
  - `.codex/skills/architecture-review/SKILL.md`
  - `dist/adapters/`
- Steps:
  - Edit canonical skill sources only during M2 and M3.
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run generated skill and adapter drift checks.
  - Run adapter drift check and adapter validation, normally `python scripts/build-adapters.py --check` and `python scripts/validate-adapters.py --version 0.1.1`.
  - Run adapter distribution and validation checks.
  - Confirm generated `.codex/skills/` and `dist/adapters/` changes match generator output and are not hand-edited.
- Expected result:
  - Codex runtime skill mirrors and public adapter packages carry the canonical architecture skill changes deterministically.
- Failure proves:
  - Downstream agent runtimes can receive stale or hand-edited guidance.
- Automation location:
  - M4 generator, drift, adapter validation, selector, CI wrapper, and diff commands from `docs/plans/2026-04-29-c4-arc42-package-quality.md`

### T22. Package-quality refinement final validation covers every changed surface

- Covers: `R76`-`R124`, `AC14`-`AC22`
- Level: smoke, lifecycle, selector, manual
- Fixture/setup:
  - completed M1 through M5 in `docs/plans/2026-04-29-c4-arc42-package-quality.md`
  - this active test spec
  - `docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`
  - touched templates, skills, generated outputs, architecture package, and diagrams
- Steps:
  - Run every milestone pass-gate command named in `docs/plans/2026-04-29-c4-arc42-package-quality.md`.
  - Run final lifecycle validation for the proposal refinement, focused spec, this test spec, canonical architecture package, change-local architecture delta, active plan, plan index, and change metadata.
  - Run final skill validation, generated skill drift checks, adapter drift checks, adapter validation, adapter distribution tests, selector tests, and broad smoke.
  - Run final selector and CI wrapper commands over all touched source, lifecycle, template, skill, generated-output, diagram, plan, and change metadata paths named in M5.
  - Confirm no required architecture-package enforcement automation, C4-file enforcement, ADR-presence enforcement, or new external dependency was introduced.
  - Confirm plan validation notes and change metadata name the commands actually run.
  - Confirm simplification validation includes adapter drift check plus adapter validation after canonical skill changes.
- Expected result:
  - The package-quality refinement is ready for `code-review`; `verify`, `explain-change`, and PR readiness remain later gates.
- Failure proves:
  - The refinement has unresolved lifecycle, generated-output, skill, template, or review-based architecture evidence drift.
- Automation location:
  - commands named in M5 of `docs/plans/2026-04-29-c4-arc42-package-quality.md`

### T23. Architecture authoring chooses the smallest valid surface

- Covers: `R32`-`R39`, `R43`, `R56`, `R59`-`R61`, `R108`-`R110`, E2, E3, E11, EC6, EC9, EC16, EC17, `AC21`
- Level: contract, integration, manual
- Fixture/setup:
  - `skills/architecture/SKILL.md`
  - `docs/architecture/system/architecture.md`
  - `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`
  - `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
- Steps:
  - Inspect `skills/architecture/SKILL.md` after M2.
  - Confirm the skill tells authors to choose the smallest valid architecture action.
  - Confirm no-impact work records a rationale in plan, spec, change metadata, or PR evidence instead of requiring architecture package edits.
  - Confirm unclear direction or design routes to proposal or proposal revision.
  - Confirm unclear behavior routes to spec or spec revision.
  - Confirm clear architecture impact updates the canonical architecture package directly.
  - Confirm durable architecture decisions create or update ADRs.
  - Confirm routine authoring does not create architecture deltas and does not use architecture to own unresolved option selection.
  - Run stale wording scan for normal delta output in `skills/architecture/SKILL.md`.
- Expected result:
  - Architecture authoring records accepted design and durable decisions without introducing unaccepted design truth or normal temporary architecture deltas.
- Failure proves:
  - The architecture skill can still own speculative design exploration or require change-local deltas as a normal surface.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `rg -n 'change-local architecture delta|merge-back|working architecture lives|docs/changes/<change-id>/architecture.md' skills/architecture/SKILL.md`
  - manual code-review inspection during M2

### T24. Architecture-review classifies the review surface before applying checks

- Covers: `R57`, `R119`-`R124`, E11, EC15, EC16, EC17, `AC22`
- Level: contract, integration, manual
- Fixture/setup:
  - `skills/architecture-review/SKILL.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/architecture-review-r1.md`
  - `scripts/test-skill-validator.py`
  - `scripts/test-review-artifact-validator.py`
- Steps:
  - Inspect `skills/architecture-review/SKILL.md` after M3.
  - Confirm review begins by classifying the surface as `canonical-architecture-update`, `ADR`, `no-architecture-impact-rationale`, or `proposal-or-spec-gap`.
  - Confirm canonical architecture update review does not require a change-local architecture delta.
  - Confirm canonical update review checks changed canonical sections, diagrams, and ADR links directly.
  - Confirm ADR review checks context, decision, alternatives, consequences, and compatibility with canonical architecture.
  - Confirm no-impact rationale review checks credibility.
  - Confirm proposal/spec gaps route unresolved direction to proposal and unresolved behavior to spec.
  - Confirm C4, arc42, ADR completeness, and material-finding safeguards remain present where relevant.
- Expected result:
  - Architecture-review reviews the actual surface under consideration and blocks unresolved direction or behavior back to the owning upstream stage.
- Failure proves:
  - Architecture-review can keep applying the old delta/merge-back checklist or can settle product direction outside proposal/spec.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - manual code-review inspection during M3

### T25. Simplification final validation covers source, generated, adapter, and review surfaces

- Covers: `R32`-`R39`, `R56`-`R58`, `R61`, `R85`-`R86`, `R108`-`R124`, `AC20`-`AC22`
- Level: smoke, lifecycle, selector, contract
- Fixture/setup:
  - completed M1 through M4 in `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
  - this active test spec
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - touched canonical skill sources, generated `.codex/skills/`, generated `dist/adapters/`, architecture package, ADR, and review artifacts
- Steps:
  - Run every milestone pass-gate command named in `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`.
  - Run final lifecycle validation for the accepted proposal, approved spec, this test spec, canonical architecture package, ADR, active plan, plan index, and change metadata.
  - Run final skill validation, generated skill drift check, adapter drift check, adapter validation, adapter distribution tests, selected validation, and diff checks.
  - Confirm generated `.codex/skills/` and `dist/adapters/` changes came from `python scripts/build-skills.py` and `python scripts/build-adapters.py`.
  - Confirm `python scripts/build-adapters.py --check` and `python scripts/validate-adapters.py --version 0.1.1` pass after canonical skill changes.
  - Confirm review-resolution is closed and material findings are resolved or explicitly dispositioned.
- Expected result:
  - The simplification implementation is ready for milestone code-review and final lifecycle gates according to the active plan.
- Failure proves:
  - The simplification has unresolved source, generated-output, adapter, lifecycle, review, or validation drift.
- Automation location:
  - commands named in M4 and M5 of `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`

## Fixtures and data

- Existing lifecycle fixtures under `tests/fixtures/artifact-lifecycle/`.
- New lifecycle fixture for a valid canonical arc42 architecture package under `tests/fixtures/artifact-lifecycle/`.
- Existing valid legacy architecture fixture under `tests/fixtures/artifact-lifecycle/valid-architecture/`.
- Existing invalid lifecycle fixtures for missing or invalid status, stale readiness, terminal closeout, placeholders, generated output rejection, and superseded-without-pointer behavior.
- Current legacy architecture inventory from `find docs/architecture -type f | sort`.
- The architecture-method change-local delta and diagrams under `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/`.
- The package-quality change-local delta under `docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md`.
- The current package-quality plan under `docs/plans/2026-04-29-c4-arc42-package-quality.md`.
- The current simplification plan under `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`.
- The simplification ADR under `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`.
- Shared C4 style scaffolding under `templates/diagram-styles.mmd`.
- Generated skill and adapter outputs refreshed from canonical skill sources through existing repository commands.

## Mocking/stubbing policy

- Prefer real repository fixtures, temporary filesystem fixtures, and existing CLI commands over mocks for lifecycle validation, selector routing, skill validation, adapter generation, and change metadata validation.
- Do not mock final selector output, lifecycle validation, generated-output drift checks, or adapter validation in final milestone proof.
- Manual review is the intended first-slice proof for C4 diagram sufficiency, package completeness beyond lifecycle compatibility, historical or exceptional change-local evidence classification, no-sensitive-data review, and legacy inventory comparison.
- Unit tests may construct small Markdown fixture trees when that is clearer than mutating the live repository tree.

## Migration or compatibility tests

- Legacy architecture documents under `docs/architecture/*.md` continue to validate against the older lifecycle contract until normalized: `T9`, `T12`.
- The new canonical path `docs/architecture/system/architecture.md` validates with the official arc42 section model after M1: `T5`, `T12`.
- `.codex/skills/` and `dist/adapters/` remain generated output and are refreshed only through existing generators: `T10`, `T11`, `T21`, `T25`.
- Existing change-local architecture deltas remain historical evidence while new deltas are legacy-closeout or explicit exceptional evidence only: `T4`, `T23`.
- The 2026-04-29 refinement keeps Mermaid `.mmd` as the default diagram source format while allowing native Mermaid C4 syntax or equivalent flowchart/graph C4 role styling: `T16`, `T17`.
- The 2026-04-29 refinement adds no required package-shape, C4-file, ADR-presence, or C4-visual-sufficiency enforcement automation: `T17`, `T20`, `T22`.
- First implementation does not change runtime behavior, public APIs, release artifacts, or command behavior outside the narrow lifecycle compatibility and CI-safe non-enforcement selector routing allowed by `R71` and `R72`: `T12`, `T13`, `T15`.
- Rollback remains documentation and generated-output rollback only; no runtime data migration is required: `T15`.

## Observability verification

- No runtime logs, metrics, traces, or audit events are required.
- Observable proof is repository artifact state, lifecycle status, selector output, generated-output drift checks, adapter drift checks, adapter validation, plan validation notes, change metadata, architecture/code-review inspection of C4 sufficiency, and final validation commands.
- Review evidence should use stable requirement IDs, test IDs, file paths, and command names rather than large raw excerpts.

## Security/privacy verification

- Touched architecture artifacts, diagrams, templates, ADRs, workflow guidance, and skill guidance must not include secrets, credentials, private keys, tokens, or machine-local debug-only data: `T14`.
- Security or privacy boundaries must be described when the architecture change affects trust boundaries, permissions, data exposure, or secret handling: `T14`.
- No test requires network access, hosted CI, credentials, or installed external agent tools.

## Performance checks

- No runtime performance benchmark is required because this method changes documentation, workflow guidance, templates, lifecycle compatibility, skills, and generated outputs rather than a service runtime.
- Review overhead is checked qualitatively by confirming the package remains concise, keeps component/deployment diagrams conditional, keeps architecture skill examples short, and avoids required enforcement automation in the first slice: `T2`, `T3`, `T13`, `T19`, `T20`.

## Manual QA checklist

- Confirm `templates/architecture.md` and `docs/architecture/system/architecture.md` use all 12 official arc42 headings in order.
- Confirm section 9 of the canonical package links `docs/adr/ADR-20260428-architecture-package-method.md`.
- Confirm the context and container diagrams are Mermaid source text.
- Confirm existing change-local deltas are historical evidence and not the canonical source for downstream work.
- Confirm normal architecture authoring now uses no-impact rationale, direct canonical architecture update, ADR, or proposal/spec blocker.
- Confirm architecture-review classifies the review surface before applying checks and does not require a change-local delta for canonical architecture updates.
- Confirm `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` inventories every path from `find docs/architecture -type f | sort`.
- Confirm `.codex/skills/` and `dist/adapters/` changes came from generator commands.
- Confirm the implementation did not add required architecture package enforcement automation or new external dependencies.
- Confirm `architecture.md` references diagram source files with relative links and does not embed Mermaid package diagrams.
- Confirm `templates/diagram-styles.mmd` contains shared C4 role classes and Mermaid diagrams apply those roles or an explicitly equivalent block.
- Confirm `templates/architecture.md` includes the section 10 quality-scenario scaffold as a comment.
- Confirm `skills/architecture/SKILL.md` includes only the required concise examples and no full worked architecture example.
- Confirm `skills/architecture-review/SKILL.md` uses the simple finding shape while preserving material-finding evidence, outcome, and safe-resolution requirements.
- Confirm `python scripts/build-adapters.py --check` and `python scripts/validate-adapters.py --version 0.1.1` pass after published skill text changes.
- Confirm plan validation notes and change metadata name the commands actually run.

## What not to test

- Do not add or require package-shape, required C4-file, ADR-presence, or full architecture-package enforcement automation in this first implementation.
- Do not test runtime services, databases, public APIs, or network behavior; the approved change has no such surface.
- Do not require hosted CI status or installed Codex, Claude Code, or opencode tools as proof.
- Do not test image rendering of diagrams as the source of truth; committed source-text diagrams are the required proof.
- Do not use broad smoke as a substitute for milestone-specific tests and manual review checks.
- Do not require native Mermaid C4 syntax when shared flowchart or graph styling expresses C4 roles clearly.
- Do not require a full worked architecture example inside `skills/architecture/SKILL.md`.
- Do not require architecture-review findings to classify every issue by C4 level.
- Do not test change-local architecture deltas as a normal architecture authoring output for new work.

## Uncovered gaps

- No uncovered spec gaps. Requirements that are intentionally not automated in the first implementation are covered by explicit manual review, selector inspection, lifecycle compatibility tests, or final validation evidence.

## Next artifacts

- `implement` for M1 in `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`.
- `code-review` after each M1 through M4 implementation milestone completes targeted validation.
- `explain-change`, `verify`, and `pr` after all in-scope implementation milestone review loops are closed.

## Follow-on artifacts

- None yet.

## Readiness

This test spec is active as the proof map for the architecture package method rollout, the 2026-04-29 package-quality refinement, and the 2026-05-09 architecture skill surface simplification.

Immediate next repository stage: `implement`.
