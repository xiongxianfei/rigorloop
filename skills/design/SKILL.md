---
name: design
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Create or revise living Designs that reconcile required behavior, technical realization, decisions and acceptance intent. Use for engineering authorship and scoped legacy-document amendments before independent Design Review.
argument-hint: [approved direction, affected model, or authorized design correction]
---

# Design authoring

## Workflow role

- role_name: design
- stage: authoring
- upstream: approved direction or an explicitly authorized scoped correction
- downstream: independent design-review, then plan under current review authority
- summary: Reconcile the smallest justified set of owning engineering contracts.
- ownership: Author affected Designs, authorized legacy amendments and author-owned evidence.
- must_not_claim: review approval, implementation permission, final verification, publication or customer adoption.

## Scope and authority

Select responsibility owners before selecting files. A model is a coherent responsibility, not automatically a feature, team, class or old document. Give each obligation and shared interaction one current owner; consumers reference that owner. Features normally revise their affected models. Preserve approved product direction and existing governance, assessment, test-adequacy and execution owners.

Classify the invocation before mutation. With no governed signal, use an explicit safe target or the living-model default below without lifecycle claims. An explicit change identity, structured owning-change reference or workflow-managed context is a governed signal even when malformed. Require one safe, agreeing current identity and load the governed procedure. Missing, stale, conflicting, escaped or malformed governed signals stop dependent authoring; do not fall back to portable mode.

Resolve project authority and existing exact targets first. For a new model, the portable default is `docs/design/M/M.md`, with matching stable model ID M. Creation requires an absent target; revision requires the existing intended target. Never overwrite another responsibility or infer project policy from an installed skill. Unmigrated sources keep their declared contracts unless migration is separately approved.

## Reconciliation procedure

1. Read the approved direction, affected owners and relied-on evidence. Explain required observable outcomes, invariants, interfaces, compatibility, authority, failures, retries, recovery and prohibited side effects where material. Keep stable requirement identities.
2. Reconcile behavior with technical realization: structure, dependencies, operational flows and constraints. A feasibility issue that materially changes an approved product goal returns to its direction owner with evidence and alternatives. Implementation convenience cannot authorize weakening that goal.
3. Identify changed producers, consumers, shared assumptions and system-wide obligations. Reconcile each affected relationship or explain an evidence-backed unaffected disposition. Load only relevant owners and interactions.
4. Explain how important claims can be assessed. Use walkthroughs, counterexamples and targeted feasibility evidence proportional to uncertainty. Expose assumptions and unresolved decisions. Structural validation alone is neither credibility nor approval.
5. Define representative realization conditions and observable expected outcomes, including integrated properties that local checks cannot establish. Design owns intent and observation boundaries; Delivery allocates concrete checks, commands, milestones and evidence; implementation supplies fixtures/assertions. Actual results stay in evidence records.
6. Preserve meaningful decisions and references. Inspect exact completed subjects, including changed relied-on examples and their owners. Hand independent Design Review the reconciled package, relevant interactions, decisions, evidence, assumptions and applicability impacts. The author cannot settle another actor's judgment.

Scenarios are not an exhaustive test whitelist. Additional cases may derive from justified obligations and hazards; absence from scenarios never authorizes deleting a test. Apply the project's existing Test criteria and review policy when adopted.

## Boundary scan

Before a behavior-changing decision, and when cited boundaries or interactions matter, ask:

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility or external condition can change the outcome?

Do not wait for the user to name the method. The scan alone does not create another record, identifier series or exhaustive scenario inventory. Living models use their model-owned scenario table; retained feature records use the conditional legacy method. Unknown ownership or an unowned normative outcome stops the affected decision.

A pre-implementation verification-allocation gap routes to `plan`. Historical contracts grant no current progression authority.

## Generated Markdown readability

Write normal Markdown paragraphs with complete sentences. Do not split a sentence across physical source lines merely for wrapping. Use stable IDs and tables for repeated mappings. Diagrams are optional and should clarify the claim. Do not require manual-proof contracts from readability guidance.

## Resource map

- READ `references/model-authoring.md` when creating or revising a living model or its examples.
- READ `references/technical-design.md` when significant structure, interfaces, runtime, deployment, trust or quality choices need explanation.
- READ `references/system-composition.md` when several owners, a shared contract or a system-wide claim is affected.
- READ `references/legacy-source-reconciliation.md` when amending an unmigrated source, reconciling invocation coexistence or performing an explicitly approved authority migration.
- READ `references/boundary-first-method-v1.md` when interpreting or authoring a retained feature-format boundary record.
- READ `references/boundary-first-feature-authoring-v1.md` for a substantive amendment remaining under that feature format, after its compact method.
- READ `references/legacy-technical-authoring.md` when amending retained architecture or ADR content under its project contract.
- READ `references/governed-design-authoring.md` when one valid governed change is explicitly selected; validate authority before writing.
- READ `references/test-quality.md` when adopted criteria apply to verification intent.
- COPY `assets/design-skeleton.md` when creating a living model. Fill its stable engineering sections and required tables; remove placeholders and inapplicable optional sections.
- COPY `assets/legacy-architecture-skeleton.md` only when creating or rebuilding a retained architecture under a project contract that permits the generic aid.
- COPY `assets/legacy-adr-skeleton.md` only when creating or rebuilding a retained ADR under a project contract that permits the generic aid.
- COPY `assets/diagram-styles.mmd` when a relevant diagram needs the shared styling aid.

Load only triggered resources. Confirm required packaged methods and transitive assets are readable, consistent and contained in the installation before dependent work. Missing package guidance is a distribution defect: stop rather than reconstruct it. Missing or conflicting project-specific authority requires the project owner; a generic template cannot supply it. Continue independently authorized unaffected work where possible.

## Output skeleton

```md
Design subjects: <exact affected owners, paths and identities>
Reconciled intent: <requirements, realization, decisions and interactions>
Assessment basis: <walkthroughs, feasibility evidence, assumptions and unresolved questions>
Verification intent: <representative local and integrated outcomes and observation boundaries>
Preservation and impacts: <reference mappings, affected examples/consumers and applicability restrictions>
Handoff: <independent Design Review subject set or bounded owning-stage blocker>
```

## Expected output

Produce the owning Designs or explicitly scoped legacy amendments and a truthful exact-subject handoff. Include affected examples alongside their owners even when parent text is unchanged; an earlier model-only approval cannot establish current assessment of an edited relied-on example. Mechanical identities and selection support the responsible actor's applicability judgment; they do not automatically invalidate reviews or add a gate. Keep mutable workflow state and actual results out of Design.
