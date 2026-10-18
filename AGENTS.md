# AGENTS.md

## Start here

This file owns repository authority, operating rules and cleanup policy. [VISION.md](VISION.md) owns project purpose.
Use [Architecture composition](design/architecture/composition.md) and [ownership](design/support/ownership.md) to find the responsible Module or Interface; read only the models and retained contracts needed for the task.
For test design or script changes, use the single [system test design](design/support/test-design/system-test-design.md) and [shared test-quality rules](design/support/test-design/rules.md). Update central scenarios only for changed behavior, risks or expected observations. Keep executable mappings and current gaps in Validation; do not create separate model test designs.
Before implementation, read the governing contract, applicable architecture decisions, owning plan and verification allocation, then the files to change.
Inspect the relevant source directly. Use README and the architecture overview for navigation; no map creation, refresh or absence rationale is required.

## Authority and ownership

External runtime instructions and direct user instructions govern within their applicable precedence. Within repository artifacts, use AGENTS.md, then the owning requirements/design and applicable decisions, then the selected plan, implementation and informal discussion. VISION.md governs project direction below these rules. Expose conflicts and material assumptions; do not silently blend rules or broaden authority. Customer projects retain their own selected governance; installation and saved records do not adopt policy or grant permission.

Each rule has one owner. Link to detailed contracts instead of copying them. Define observable behavior, compatibility, edge cases and acceptance before implementation; reconcile affected consumers in the same change. Use proportionate plans for consequential work and existing tools where suitable. Generated output must be reproducible from canonical sources.

Keep secrets and private machine data out of source and logs. Preserve unrelated work. External mutations and destructive actions require applicable authorization; review, verification and installation do not supply it.

## Workflow

- Use one standard workflow. Requirement, Design and Delivery reviews are optional; usable owner-selected bases and proportionate delivery intent are required before dependent work. A selected basis is not independent approval.
- Complete implementation receives one independent whole-change Code Review, with correction reassessment in the same gate, followed by distinct successful Verify. Milestones need no approval. A save, merge, PR or passing check does not replace these gates.
- Record actual review subjects, findings, support and limitations, including clean outcomes. Material findings must be recorded before driving corrections. Preserve unresolved obligations and relied-on support; do not record every action or retain every superseded run. Completion retains a compact historical account, not a continuously refreshed health claim.

- Use `rigorloop change context --root . --change ID --format json` for the selected current handoff and `route` for semantic routing. The local executable is `node packages/rigorloop/dist/bin/rigorloop.js`.
- Follow [Workflow](design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md) and [Assessment](design/architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md) for progression, ownership and review gates.
- Read `docs/plan.md` as navigation; concrete plans live under `docs/plans/`, and mutable state belongs to the selected Change in the project-local SQLite store through the supported CLI. The adoption plan alone retains its explicit private prior-executable bootstrap procedure until qualified migration.
- Use scoped CLI reads, Review preparation and explicit task recording under [CLI](design/architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md) and [Records](design/architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md). Do not routinely reconstruct record stores or resume retired formats.
- Keep review judgments, findings, assessed-subject manifests and execution results in operational records, not `design/`. For the document-based exception below, use its private local review location; model sources retain only applicable rationale and concise provenance.
- Use `bugfix` for defects, `ci-maintenance` for CI configuration changes and `pr` for a ready external handoff. Individual skill requests stay isolated unless broader progression is authorized.

The existing [requirement-first refactor](design/requirements/workflow-refactor.md) permits document-based analysis/review without governed CLI recording or a separate reviewer. Identify author assessments honestly and retain their records privately under `.rigorloop/artifacts/reviews/`. This scoped exception does not waive independent implementation review, final Verify or external-action authority. Earlier customer records require qualified explicit import when needed; installing a CLI does not migrate or activate them. Preserve required originals and selected dependencies.

## Editing conventions

- Make the smallest complete change, preserve user work and avoid unrelated refactors.
- For internal refactors, update all affected consumers and delete obsolete code and paths in the same change. Do not add or retain compatibility layers, deprecated shims, or dual-write logic for obsolete internals. Preserve compatibility required by agreed external contracts, including public interfaces and data migrations.
- Follow [System's directory layout](design/architecture/composition.md#repository-directory-layout); preserve stable model IDs and declared example ownership.
- Edit canonical sources in `design/`, `rem/`, `docs/`, `skills/`, `schemas/`, `scripts/` and `templates/`; `skills/` is the only authored skill source.
- Keep architecture and ADR scaffolds in `templates/`. Use `skills/plan/assets/plan-skeleton.md` for plans; do not create duplicate scaffolds or overwrite an unrelated initiative's plan.
- Do not hand-edit generated adapter output. Keep local `.codex/skills/` untracked; use [adapter guidance](dist/adapters/README.md) and [Packaging](design/architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md).
- Treat published skills as user-facing: keep repository-maintainer mechanics out of their instructions. Add a skill only for a distinct recurring responsibility, artifact, gate or operational process.
- Edit `VISION.md` for project vision; README content between the vision markers is generated from it.
- Closed-vocabulary validators must reject unknown values before consistency checks, unless intentional fall-through is documented. Add an unknown-value regression test for each new closed vocabulary.
- Use Git history for retired material under the [cleanup policy](#repository-cleanup-and-historical-retention); reconcile live dependencies before deleting files.

## Validation and handoff

Follow [CONTRIBUTING.md](CONTRIBUTING.md#validation-scope), the owning plan and [Validation](design/support/validation.md).
Reuse existing commands; start with the smallest relevant checks and complete the required scope before claiming readiness.

```bash
bash scripts/ci.sh
```

For packaging or release work, follow the owning [Packaging](design/architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md) and [Release](design/architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/release.md) checks, including tracked release notes and actual candidate evidence.
Report what changed, commands actually run, results and material limitations; reconcile governed records when applicable. Missing or stale proof cannot become success; hosted CI claims require observing the hosted run. Bug fixes need regression protection or an explicit failure reproduction. Actual results and judgments remain operational records, not design documents.

## Repository cleanup and historical retention

Keep current contracts, implementation, useful validation and material needed by active work or current reliance. Retire obsolete documents and exclusive code/resources once surviving obligations and consumers are reconciled; Git history is the recovery source, without archive copies in the current tree. Preserve uncommitted work, stable requirement identities and external compatibility. Do not rewrite historical judgments or retarget approvals. Active findings and required evidence remain available until resolved or coherently replaced. Report removal scope and checks; this repository policy imposes no Git requirement on customer projects.

## Core Engineering Principles

1. **Self-contained knowledge.** Make each substantive document understandable on its own: explain the problem, essential terms, prerequisites, mechanisms, examples, and boundaries. Link to deeper material without requiring readers to follow links to understand the core argument. Keep canonical definitions in one place; avoid needless duplication.

2. **Reader-centered quality.** Evaluate whether a reader can explain *what happens, how, why, and when*; apply the knowledge to a realistic problem; predict likely outcomes and failure modes; and recognize opportunities to improve results. Correctness and clear reasoning matter more than polished prose.

3. **Goal-oriented work.** Identify the intended reader outcome before substantial work. Choose the smallest sufficient change; prioritize important knowledge gaps and useful results. Avoid speculative infrastructure, redundant research, unnecessary documentation, and rituals that do not advance the goal. Do not skip essential verification to save effort.

4. **Reuse before invention.** Look for established theory, standards, sources, methods, libraries, and tools before building alternatives. Prefer suitable, proven approaches; weigh fitness, reliability, cost, maintenance, and lock-in. Create custom solutions only when a material requirement justifies them.

5. **Mechanisms before memorization.** Explain causal relationships, relevant variables, assumptions, boundary conditions, and trade-offs. Show how the mechanism informs decisions and practical action. Surface possible improvements and testable hypotheses, clearly separating proposed innovations from demonstrated results.

6. **Delete obsolete internal compatibility.** When replacing internal code, paths, workflows, or knowledge structures, migrate affected uses and remove superseded implementations. Do not add internal legacy shims, deprecated aliases, dual-write logic, or competing canonical documents. Assess *external* contracts separately and honor actual obligations. Preserve unique evidence, provenance, and historically useful knowledge; remove obsolete representations, not valuable facts.

7. **Fix the problem class.** For defects or inconsistencies, identify the underlying cause and check for related instances. Make the smallest coherent change that addresses the confirmed class; add proportionate checks or regression coverage where useful. Do not turn isolated issues into speculative redesigns.

8. **Think before acting.** Before substantive work, clarify the intended outcome, inspect relevant context, challenge important assumptions, and consider dependencies, risks, and the simplest sound approach. Scale planning to the task: small, reversible changes need no formal plan; consequential or hard-to-reverse changes deserve more analysis. Avoid analysis that does not improve the decision.

9. **Test the core first; validate by risk.** First verify the main outcome: for software, the changed behavior; for knowledge, whether a reader can use it to reason through a representative problem. Expand to affected dependencies, contracts, edge cases, or regressions when the likelihood and impact of failure justify it. Prefer focused checks over redundant tests or unrelated full suites; never omit essential verification merely to save time.
