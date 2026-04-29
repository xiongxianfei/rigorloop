# C4, arc42, and Architecture Skill Quality Refinement

## Status

- accepted

## Problem

The accepted architecture method gives RigorLoop the right package shape: one canonical system architecture package, C4 diagrams, all 12 arc42 sections, ADR links, templates, and architecture skills that know how to author and review that package. The first canonical package is structurally present, but parts of it are not yet strong enough as architecture evidence, and the skill guidance is not yet specific enough to reliably prevent the same drift in future work.

The current diagram files under `docs/architecture/system/diagrams/` use generic Mermaid flowcharts instead of recognizable C4 notation. The context view includes internal repository concerns that belong below the context level, and the container view reads like a folder dependency graph rather than a C4 container view with actors, external systems, containers, technologies, and relationships.

The current directory shape is right, but the diagram-source policy is not yet explicit enough. Architecture diagrams should live as separate Mermaid source files under the package `diagrams/` directory, and `architecture.md` should reference them with clickable relative links instead of embedding Mermaid blocks or pointing at repo-root paths.

The current `docs/architecture/system/architecture.md` also has section-quality issues:

- the Building Block View is a flat catalog instead of a hierarchical white-box view of the system and important containers;
- the Architecture Decisions section paraphrases ADR rationale instead of keeping ADRs as the owner of durable decision detail;
- the Quality Requirements section names quality properties but does not express reviewable scenarios;
- the Deployment View repeats source layout information more than it explains repository packaging, generated outputs, publication, and execution boundaries.

These issues weaken review value even though the package has the expected files and headings.

The architecture and architecture-review skills already mention the approved method, but they still leave too much room for generic diagrams, flat building-block catalogs, duplicated ADR rationale, and non-scenario quality requirements. The method will not improve consistently unless the skills teach agents how to author and review the sharper version of the package.

## Goals

- Make the canonical context and container diagrams recognizable as C4 diagrams.
- Keep Mermaid `.mmd` diagram source while using C4 conventions clearly enough for review.
- Refine the container view before adding component diagrams.
- Standardize diagram placement under each package's `diagrams/` directory with one authored source file per diagram, using `.mmd` for default Mermaid diagrams.
- Require `architecture.md` to reference diagrams with relative links instead of embedded Mermaid blocks or image embeds.
- Add shared C4 styling guidance through `templates/diagram-styles.mmd`.
- Make arc42 section 5 explain building-block hierarchy rather than only listing folders.
- Keep arc42 section 9 concise and link-focused so ADRs remain the durable decision records.
- Improve arc42 section 10 with quality scenarios or an explicitly accepted equivalent.
- Clarify arc42 section 7 around repository packaging, generated artifacts, release evidence, and execution boundaries.
- Optimize `skills/architecture/SKILL.md` so architecture authors create C4-accurate diagrams, hierarchical Building Block Views, concise ADR summaries, and useful Quality Requirements.
- Keep `skills/architecture/SKILL.md` concise by putting full structure in templates and full worked examples in references when needed.
- Optimize `skills/architecture-review/SKILL.md` so reviewers catch generic flowcharts, wrong C4 levels, flat building-block catalogs, ADR duplication, weak quality scenarios, and deployment repetition.
- Keep architecture-review findings simple: finding, location, severity, and recommendation rather than mandatory C4-level classification.
- Keep `templates/architecture.md` aligned with the improved skill guidance so future packages start with the right shape.
- Preserve the accepted C4 plus arc42 plus ADR method rather than replacing it.
- Keep the refinement review-based unless a later approved spec adds enforcement automation.

## Non-goals

- Reopening the decision to use C4, arc42, and ADRs.
- Replacing Mermaid `.mmd` source as the first implementation diagram format.
- Embedding Mermaid diagram blocks directly inside `architecture.md`.
- Creating generated PNG, SVG, or screenshot files as authored diagram sources.
- Adding required architecture-package validators in this refinement.
- Changing validation command behavior, selector routing, generated-output behavior, or workflow stage order.
- Rewriting every legacy architecture artifact.
- Adding a component diagram before the refined container view and Building Block View prove that deeper detail is needed.
- Creating a new canonical architecture package path.
- Duplicating ADR rationale inside the canonical architecture document.
- Requiring every architecture document to keep a quality-scenario table when quality requirements are genuinely not applicable.
- Turning skills into long architecture textbooks instead of concise operational guidance.
- Putting a full worked architecture example in the `skills/architecture/SKILL.md` body.
- Requiring architecture-review findings to classify every issue by C4 level.
- Updating generated skill or adapter output by hand.

## Context

The accepted proposal `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`, approved spec `specs/architecture-package-method.md`, and accepted ADR `docs/adr/ADR-20260428-architecture-package-method.md` establish the architecture method.

That method requires one canonical architecture package at:

```text
docs/architecture/system/architecture.md
docs/architecture/system/diagrams/context.mmd
docs/architecture/system/diagrams/container.mmd
```

It also keeps the first implementation review-based and explicitly defers required package-shape enforcement automation. This proposal should therefore refine the real package and its guidance without introducing a new automation gate.

The review feedback behind this proposal identifies a useful distinction: the package is present and lifecycle-correct, but its first C4 and arc42 content does not yet satisfy the architecture communication goals of the method.

The current `skills/architecture/SKILL.md` and `skills/architecture-review/SKILL.md` include the package paths, all 12 arc42 sections, default C4 diagrams, ADR rules, and evidence collection guidance. They need to become more prescriptive at the points where review found drift:

- C4 diagrams should be C4 diagrams, not ordinary flowcharts with architecture labels.
- Diagram files should be one authored source file per diagram under the relevant package's `diagrams/` directory, using `.mmd` for default Mermaid diagrams.
- Architecture documents should link diagrams by relative path and should not inline or duplicate diagram source.
- Context diagrams should show the system under review as one system, not internal containers.
- Container diagrams should show major containers, technologies, and relationships, not only folder dependencies.
- Component diagrams should be added only after the refined container view leaves an important container-internal question unanswered.
- Building Block View should decompose structure hierarchically.
- Architecture Decisions should summarize and link ADRs without restating their rationale.
- Quality Requirements should prefer lightweight scenarios over property lists.
- Deployment View should describe packaging, publication, generated artifacts, and execution boundaries without repeating the source layout.
- The architecture skill should teach process, the architecture template should teach structure, and any full worked example should teach style from a reference file rather than the skill body.
- Architecture-review should emphasize severity and location over C4-level taxonomy because many findings are consistency, decision, documentation, or lifecycle issues rather than pure context/container/component issues.

## Options considered

### Option 0: Leave the package and skills as-is

Advantages:

- no documentation churn;
- no risk of introducing new wording inconsistencies;
- the current package already has the required file and heading shape.
- the current skills already mention the approved method at a high level.

Disadvantages:

- the diagrams remain generic flowcharts rather than recognizable C4 views;
- reviewers cannot quickly distinguish actors, the system under review, external systems, and containers;
- arc42 sections keep duplicating or flattening information instead of adding architecture value;
- architecture authors can repeat the same mistakes because the skills do not give enough concrete guardrails;
- architecture reviewers can approve shape compliance without catching content-quality drift;
- the first real package remains weak evidence for the accepted method.

### Option 1: Convert only the diagrams to C4

Advantages:

- fixes the most visible problem;
- keeps the diff small;
- improves reviewer scanability quickly.

Disadvantages:

- leaves the flat Building Block View unchanged;
- leaves diagram-source placement, relative-link, naming, reuse, and lifecycle conventions under-specified;
- leaves ADR detail duplicated in arc42 section 9;
- leaves quality requirements without reviewable scenarios;
- leaves the architecture skills too broad to prevent future non-C4 diagrams;
- makes the package look more C4-compliant while arc42 content remains weaker than the method expects.

### Option 2: Rewrite the whole canonical architecture package without changing skills

Advantages:

- could produce a polished end-state in one pass;
- gives every arc42 section a fresh review;
- can remove accumulated duplication broadly.

Disadvantages:

- high review cost for a docs-only refinement;
- easy to exceed the actual problem;
- risks changing accepted architecture meaning while trying to improve presentation;
- improves one package but leaves future agents without the sharper authoring and review guidance;
- makes it harder for reviewers to isolate the intended quality corrections.

### Option 3: Focused package and skill refinement

Advantages:

- addresses the concrete review findings directly;
- keeps the accepted package path and method intact;
- treats the architecture skills as the mechanism that prevents repeat drift;
- makes the diagram-source policy explicit without changing the canonical package path;
- follows C4 level discipline by fixing context and container views before drilling into components;
- limits package changes to diagrams, section 5, section 7, section 9, section 10, and any necessary guidance updates;
- aligns the template, authoring skill, and review skill around the same expected artifact quality;
- keeps routine architecture-skill use concise and token-conscious;
- lets reviewers compare before and after evidence clearly;
- preserves the review-based first-adoption model.

Disadvantages:

- still requires careful architecture review;
- may expose small follow-on wording gaps in the spec, template, or architecture-review skill;
- may require generated `.codex/skills/` and `dist/adapters/` output refresh through the existing generator if canonical skill guidance changes;
- does not produce automated enforcement.

### Option 4: Add architecture-package validation now

Advantages:

- could prevent future generic flowcharts or missing section details;
- makes violations easier to catch consistently.

Disadvantages:

- conflicts with the accepted first-adoption strategy of stabilizing real package shape before enforcement;
- risks encoding immature content judgments as brittle checks;
- cannot easily validate C4 sufficiency, ADR ownership, or quality-scenario usefulness without false confidence.

## Recommended direction

Choose Option 3.

Refine the current canonical architecture package and the architecture skills together. Keep `docs/architecture/system/architecture.md` as the long-lived source of truth and keep Mermaid `.mmd` source diagrams under `docs/architecture/system/diagrams/`. Update the diagram source to use recognizable C4 semantics.

Adopt this diagram-source policy:

- Each architecture package has a `diagrams/` subdirectory next to `architecture.md`.
- Each diagram has exactly one authored source file. For default Mermaid diagrams, that source file is an `.mmd` file.
- `architecture.md` references diagrams with clickable relative links such as `[diagrams/context.mmd](diagrams/context.mmd)`, not embedded Mermaid blocks and not image embeds.
- Diagram filenames use lowercase kebab-case and indicate the C4 level or arc42 section, such as `context.mmd`, `container.mmd`, `component-validation.mmd`, `runtime-adapter-generation.mmd`, or `deployment.mmd`.
- Reused diagrams are linked from their single authored source instead of copied across packages.
- Generated images, if ever produced for publication, live under a generated or ignored location such as `diagrams/rendered/` and are never edited by hand.
- Diagram lifecycle follows the parent architecture package; individual diagram source files do not carry independent status metadata.
- Change-local diagrams mirror the same `docs/changes/<change-id>/diagrams/<name>.mmd` layout and become historical evidence after merge-back.

Use C4 semantics in v1. Native Mermaid `C4Context` and `C4Container` syntax may be used when practical, but stable Mermaid `flowchart` or `graph` syntax remains acceptable when it expresses C4 roles through the shared styling convention. Add `templates/diagram-styles.mmd` as the shared class definition source for C4 roles:

```mermaid
classDef person fill:#08427b,stroke:#073b6f,color:#fff
classDef system fill:#1168bd,stroke:#0e5aa7,color:#fff
classDef external fill:#999,stroke:#666,color:#fff
classDef container fill:#438dd5,stroke:#3c7fc0,color:#fff
```

Diagrams should apply those classes consistently. Container labels should include technology in the form `Name<br/>[Technology]`, and relationships should be labeled with intent rather than using bare arrows.

Do not add a component diagram in the first refinement unless the refined container view and Building Block View still leave an important review question unanswered. After the container view is corrected, ask whether a reviewer can understand the container's responsibility, important collaborators, and change impact from the container diagram plus section 5 prose. If yes, prose wins. If one container needs more than about three sentences of internal explanation in the Building Block View, that is a signal that a component diagram may earn its place.

The validation subsystem is the likely first candidate for a future component diagram because `select-validation.py`, `validation_selection.py`, `ci.sh`, individual validators, and check IDs have internal relationships contributors must understand when adding new check types. The generation subsystem is less likely to need one in this refinement because its container-level flow is simpler: edit canonical sources, run generation, validate generated output.

The refinement should make these changes:

- `context.mmd`: show contributors or reviewers as people, RigorLoop as the single system under review, and external systems or consumers outside the system boundary.
- `container.mmd`: show the major repository containers with technology annotations such as Markdown artifacts, Python scripts, Mermaid diagram source, templates, generated adapter output, and GitHub Actions wrappers where relevant.
- `architecture.md`: reference diagrams with relative links such as `diagrams/context.mmd` and `diagrams/container.mmd`.
- Building Block View: describe the system as a Level 1 white-box and decompose important areas such as lifecycle artifacts, validation and generation scripts, canonical skills, generated adapters, and release evidence.
- Architecture Decisions: keep one-line ADR summaries and links only; move non-ADR justifications to the plan, explain-change, or relevant change-local evidence.
- Quality Requirements: express the most important qualities as lightweight scenarios with stimulus, environment, response, and response measure where practical.
- Deployment View: explain repository packaging, local execution, generated adapter distribution, release metadata, and CI wrapper boundaries without repeating every source path already covered by the Building Block View.

The skill refinement should make these changes:

- `skills/architecture/SKILL.md`: teach authors to use C4 semantics explicitly, choose the correct C4 level, keep diagrams in separate authored source files, use `.mmd` for default Mermaid diagrams, link diagrams by relative path, apply the shared style classes, avoid context/container mixing, refine container views before adding component views, structure Building Block View hierarchically, keep ADR summaries link-focused, and write compact quality scenarios.
- `skills/architecture-review/SKILL.md`: add review checks for embedded or duplicated diagrams, non-C4 flowcharts, wrong diagram level, premature component diagrams, missing C4 classes or technology annotations, unlabeled or mixed relationship types, flat building-block catalogs, ADR rationale duplication, weak quality requirements, and deployment/source-layout repetition. Findings should use a simple structure: finding, location, severity, and recommendation.
- `templates/architecture.md`: guide authors toward relative diagram links, hierarchical building blocks, concise deployment boundary content, ADR link summaries, and a commented quality-scenario scaffold for arc42 section 10.
- `templates/diagram-styles.mmd`: provide the shared C4 role styling block used by Mermaid flowchart or graph diagrams.

Keep the architecture skill body concise. It should include one short output shape, one minimal C4 context snippet, one minimal C4 container snippet, one ADR trigger list, and one "when to use / when not to use" section. It should not include a full worked architecture example. Use this content split:

```text
skills/architecture/SKILL.md
  = concise process instructions and required outputs

templates/architecture.md
  = full 12-section arc42 template

templates/adr.md
  = ADR template

skills/architecture/references/architecture-example.md
  = complete worked example, only if needed
```

The architecture skill should include this output shape:

```markdown
## Output

Produce or update:

- `docs/changes/<change-id>/architecture.md` for change-local deltas, or
- the canonical architecture package when maintaining the baseline
- C4 Context diagram
- C4 Container diagram
- ADRs when durable decisions are introduced

Use `templates/architecture.md` for the full 12-section arc42 structure.
```

The guiding rule is: the skill teaches the process, the template teaches the structure, and the example teaches style.

Architecture-review findings should not require C4-level classification. Location carries the needed traceability, and severity carries the workflow consequence. The default finding shape should be:

```text
- Finding: <one-sentence description>
- Location: <file path and section/line, or diagram name>
- Severity: blocker | material | minor
- Recommendation: <what should change>
```

This simple shape does not replace the repository-wide material-finding contract. Material architecture-review findings must also record evidence, required outcome, and a safe resolution path or `needs-decision` rationale.

If later review evidence shows that severity and location lose important trend signal, add a small category field through a later approved change. A category taxonomy such as `structure`, `decision`, `consistency`, `documentation`, and `lifecycle` would be more actionable than mandatory C4-level classification.

Update `specs/architecture-package-method.md` narrowly as the focused normative home for the diagram policy, skill-content policy, template additions, and review finding format. For example, the spec update should clarify that C4 diagrams use C4 semantics through native Mermaid C4 syntax or equivalent shared styling conventions, and that arc42 Quality Requirements prefer concise scenarios. Do not add required validators in this proposal's first slice.

The quality-scenario scaffold should be present as a Markdown comment in `templates/architecture.md`, not as required rendered content. The scaffold should show the shape of a real scenario using stimulus, environment, response, and measure, then tell authors to delete the comment and replace it with real scenarios or write `Not applicable` with a one-line rationale. This keeps arc42 section 10 useful without forcing table noise into every architecture artifact.

## Expected behavior changes

- Architecture reviewers can distinguish context-level and container-level concerns at a glance.
- Architecture documents point to diagrams with relative links, and diagram source is not duplicated or embedded.
- The canonical context diagram stops showing internal validation and generated-output concerns as context-level elements.
- The canonical container diagram becomes an architecture view rather than a folder graph.
- Component diagrams are deferred unless the refined container view and Building Block View cannot explain important internals.
- The Building Block View supports hierarchical review of important parts of the repository system.
- ADRs remain the source of detailed decision rationale, while arc42 section 9 becomes a navigational summary.
- Quality requirements become easier to evaluate because they include concrete review scenarios.
- Architecture templates make quality-scenario authoring easier without rendering placeholder content.
- Deployment and publication boundaries are clearer for generated adapters, release evidence, local validation, and GitHub Actions wrappers.
- Architecture authors get skill guidance that shows how to produce the intended package quality, not just the intended package files.
- The architecture skill stays short enough for routine use and does not carry a full worked example in its body.
- Architecture reviewers get skill guidance that names the specific quality failures to catch before planning.
- Architecture-review findings use severity and location for flow control and traceability instead of requiring a C4-level taxonomy.
- Future architecture packages start from a template that nudges toward C4 semantics and arc42 scenario quality.
- Future diagrams share visual C4 role conventions through `templates/diagram-styles.mmd`.

## Architecture impact

This change affects the canonical architecture package and the architecture-method skill guidance around diagram quality and arc42 section content.

Primary touched surfaces are expected to be:

- `docs/architecture/system/architecture.md`
- `docs/architecture/system/diagrams/context.mmd`
- `docs/architecture/system/diagrams/container.mmd`
- `specs/architecture-package-method.md`
- `skills/architecture/SKILL.md`
- `skills/architecture-review/SKILL.md`
- `templates/architecture.md`
- `templates/diagram-styles.mmd`

Conditional touched surfaces are:

- `skills/architecture/references/architecture-example.md`, only if a complete worked example is needed
- generated `.codex/skills/` and `dist/adapters/` output, refreshed only through the existing generator when canonical skill guidance changes.

This proposal does not introduce a new system boundary or a new architecture method. A new ADR should not be necessary unless the follow-on spec chooses a durable diagram-source or enforcement decision that supersedes the accepted architecture-method ADR.

## Testing and verification strategy

The first proof should remain review-based:

- proposal review should confirm the scope is a refinement, not a method replacement;
- spec review should cover the focused `specs/architecture-package-method.md` update;
- architecture review should inspect the revised diagrams and arc42 sections directly;
- code review should verify that skill, template, spec, architecture, and generated-output changes stay aligned;
- verify should run the exact validation commands named by the eventual plan and test spec.

Likely implementation validation should include path-scoped selector and CI commands for the touched proposal, spec, architecture, diagram, template, skill, and generated-output paths. If canonical skills change, generated `.codex/skills/` and `dist/adapters/` output should be refreshed through the existing generator and checked for drift. If Mermaid C4 rendering is not covered by existing scripts, review evidence should record the manual or tool-based diagram inspection used, including whether the `.mmd` files use the shared C4 classes and whether `architecture.md` links them by relative path.

## Rollout and rollback

Rollout should proceed through the normal lifecycle:

1. accept this proposal after proposal-review;
2. update `specs/architecture-package-method.md` as the focused spec that owns the diagram policy, skill-content policy, template additions, and review finding format;
3. update the canonical package diagrams and affected arc42 sections;
4. add `templates/diagram-styles.mmd` and update `templates/architecture.md` with relative diagram-link guidance;
5. update `skills/architecture/SKILL.md` and `skills/architecture-review/SKILL.md` so future authors and reviewers apply the same quality bar;
6. refresh generated `.codex/skills/` and `dist/adapters/` output through the existing generator when canonical skill guidance changes;
7. run architecture-review, plan-review, test-spec, implement, code-review, verify, explain-change, and PR as required by the workflow.

Rollback is straightforward because the first slice is documentation, skill guidance, templates, and generated guidance refresh. Revert the touched proposal, spec, architecture, template, skill, generated `.codex/skills/`, and generated `dist/adapters/` files. No runtime data migration or release artifact rollback is expected.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| The refinement becomes a broad rewrite of the architecture package | Limit the first implementation to the identified diagrams and arc42 sections unless review finds a blocking inconsistency. |
| Mermaid C4 syntax is unsupported or renders poorly in the target review surfaces | Keep Mermaid `.mmd` source, but allow equivalent C4 conventions in Mermaid when native C4 syntax is not viable and record the reason. |
| A component diagram is added before the container view is trustworthy | Require the first slice to refine the container view first and add components only when a specific unanswered review question remains. |
| Quality scenarios become too heavy for a documentation-focused repository | Use a small number of high-value scenarios and keep the rest concise. |
| Template examples leak into rendered architecture docs as placeholder content | Put the quality-scenario example in a Markdown comment and require authors to replace it or mark the section not applicable with rationale. |
| ADR summaries drift from ADR content | Keep section 9 to one-line summaries plus links and avoid paraphrasing decision rationale. |
| Diagram styling is copied inconsistently | Add `templates/diagram-styles.mmd` as the shared source and have skills/templates tell authors to reuse it. |
| Markdown authors accidentally embed Mermaid blocks in `architecture.md` | Make separate authored source files, `.mmd` for default Mermaid diagrams, and relative links part of the proposal, template, and review checklist. |
| Spec, template, and skill guidance diverge | Touch all three only when needed, and keep wording aligned around the same diagram and arc42 expectations. |
| Skill guidance becomes too long to use during ordinary architecture work | Keep only the output shape, minimal C4 snippets, ADR trigger list, and use/skip guidance in the skill body; put full examples in references. |
| C4-level finding classification slows reviews or creates noisy taxonomy disputes | Use finding, location, severity, and recommendation by default; add a small category field later only if evidence shows lost signal. |
| Generated runtime guidance drifts from canonical skill sources | Refresh generated output only through the existing generation path and validate generated drift. |
| Reviewers mistake this as new enforcement automation | State explicitly in the spec, plan, and PR that validation remains review-based unless a later approved contract adds automation. |

## Open questions

- None.

## Decision log

- 2026-04-29: Drafted proposal to refine the first canonical C4 and arc42 package quality while preserving the accepted architecture method.
- 2026-04-29: Expanded scope to include architecture and architecture-review skill optimization because package quality problems will repeat if authoring and review skills stay too generic.
- 2026-04-29: Added the diagram-source policy: separate authored source files under `diagrams/`, `.mmd` for default Mermaid diagrams, relative links from `architecture.md`, C4 semantics with native Mermaid C4 optional, shared styling in `templates/diagram-styles.mmd`, and lifecycle inherited from the parent package.
- 2026-04-29: Chose a commented quality-scenario scaffold in `templates/architecture.md` so arc42 section 10 shows the right shape without requiring placeholder rendered content.
- 2026-04-29: Chose to refine the container view first and add component diagrams only if the corrected container view plus Building Block View leaves a concrete review question unanswered.
- 2026-04-29: Chose concise architecture-skill examples: one output shape, minimal C4 context/container snippets, ADR triggers, and use/skip guidance; full worked examples belong in references when needed.
- 2026-04-29: Chose simple architecture-review findings with finding, location, severity, and recommendation instead of mandatory C4-level classification.
- 2026-04-29: Rejected leaving the package as-is because the current diagrams and selected arc42 sections weaken review value.
- 2026-04-29: Rejected immediate validation automation because the accepted architecture-method rollout intentionally keeps first adoption review-based.

## Next artifacts

- proposal-review for this proposal;
- focused spec update to `specs/architecture-package-method.md` owning the diagram policy, skill-content policy, template additions, and review finding format;
- architecture delta or direct canonical package update for the refined diagrams and arc42 sections;
- architecture and architecture-review skill updates;
- template updates for architecture package authoring and shared diagram styling;
- plan and test spec for implementation sequencing and validation commands.

## Follow-on artifacts

- `proposal-review`: approved on 2026-04-29 with no material findings after spec ownership, generated-output scope, and readiness wording were corrected.
- Focused spec update: `specs/architecture-package-method.md` approved by `spec-review` on 2026-04-29.
- Architecture update: canonical package and change-local architecture delta approved by `architecture-review` on 2026-04-29.
- Execution plan: `docs/plans/2026-04-29-c4-arc42-package-quality.md` approved by `plan-review` on 2026-04-29 after PR-F1 corrected M5 sequencing.
- Test spec update: `specs/architecture-package-method.test.md` active on 2026-04-29 for R76-R118 and AC14-AC20.

## Readiness

This proposal is accepted. The focused spec update, architecture update, execution plan, and test spec update are approved or active, and implementation is the current handoff stage.
