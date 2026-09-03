# Optional Discovery Skills Architecture

## Owning change record

- `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/change.yaml`

## Related artifacts

- Proposal: [Refine Explore and Research as Optional Discovery Skills](../proposals/2026-09-03-refine-explore-research-optional-discovery-skills.md)
- Specification: None yet; specification reconciliation follows this architecture.
- Plan: None yet.
- ADRs: No new ADR. This design applies the existing canonical-skill, self-contained-resource, copied-shared-block, and generated-adapter boundaries already owned by `specs/skill-contract.md` and the canonical system architecture.

## Introduction and Goals

This architecture refines two existing public support capabilities without adding lifecycle stages. `explore` becomes the divergent option-discovery package; `research` becomes the convergent evidence package. Both create concise standalone Git artifacts when explicitly invoked, and both hand conclusions to an identified decision owner without acquiring that owner's authority.

The design keeps each installed skill package self-contained, consolidates stable authority and handoff rules through the repository's copied shared-block mechanism, moves detailed methods behind conditional resources, updates Route's semantic selection guidance, and preserves canonical-to-adapter reproducibility.

## Architecture Constraints

- `skills/` remains the only authored public-skill source; generated runtime trees and adapter archives remain derived output.
- Public skill packages must be self-contained. A mapped resource may not escape the installed skill root.
- Shared public policy follows `specs/skill-contract.md`: one canonical source under `templates/shared/`, verbatim copies in consuming packages, and repository-owned drift validation.
- The skill-contract specification must explicitly admit the new stable discovery-support block before implementation claims conformance; the current closed first-set list cannot be bypassed.
- Explore and Research remain on-demand support operations, not lifecycle stages, review packages, settlement owners, or automatic progression targets.
- Explicit invocation creates one standalone Git-tracked artifact; ordinary local reasoning or fact checking performed by another stage does not implicitly invoke either skill.
- Supporting artifacts do not mutate lifecycle-managed proposal, specification, architecture, plan, implementation, review, or verification artifacts.
- Default artifact paths are repository-relative, portable, date-prefixed, and non-overwriting.
- Published skill text must not expose maintainer-only canonical paths, shared-copy mechanics, validator internals, adapter paths, or generated-output procedures.
- Existing historical artifacts and release archives remain immutable evidence.

## Context and Scope

```text
User or owning stage
        |
        +-- option-space uncertainty --> explore package --> docs/explorations/...md
        |
        +-- factual uncertainty ------> research package --> docs/research/...md
        |
        +-- both ---------------------> explore, then bounded research
        |
        +-- neither ------------------> owning stage continues directly

supporting artifact --adopt/reject/qualify--> owning lifecycle artifact and normal review
```

The system boundary is the repository's published skill, artifact, validation, generation, and adapter-distribution system. There is no new service, process, database, network boundary, lifecycle transition, or privileged runtime. A separate C4 diagram would duplicate the authority flow without adding useful structural detail.

## Solution Strategy

1. Replace the broad overlapping core instructions with narrow public contracts: Explore expands directions; Research establishes decision-relevant facts.
2. Add a stable discovery-support shared block for artifact identity, evidence labels, authority, stopping, contradiction routing, and handoff.
3. Package a verbatim copy of that block in both skill roots and validate byte parity with the canonical contributor source.
4. Give each skill a copy-and-fill artifact skeleton plus only the conditional method references justified by its reasoning mode.
5. Change Explore's default output root from proposal storage to `docs/explorations/`; keep Research in `docs/research/` but remove inline output from explicit invocation.
6. Expand Route's semantic trigger guidance so agents can select Explore, Research, both in dependency order, or neither.
7. Amend the governing skill and workflow contracts, fixtures, validation, documentation, benchmarks where applicable, and adapter generation as one coherent public-package change.

## Building Block View

### Canonical shared discovery policy

`templates/shared/discovery-support.md` is the maintainer-owned canonical block. It defines only stable rules common to both reasoning modes:

- topic and supported decision;
- owning stage or change when known;
- inputs examined and important assumptions;
- separation of established facts, inference, and assumptions;
- remaining uncertainty and material stopping condition;
- non-mutation of downstream-owned artifacts and lifecycle state;
- contradiction routing and recommended next owner;
- standalone Git artifact preservation for explicit invocation.

The public copies are `skills/explore/references/discovery-support.md` and `skills/research/references/discovery-support.md`. Each skill's Resource map loads its local copy for every explicit invocation. Public wording describes the behavior without naming canonical-copy or validator mechanics.

### Explore package

```text
skills/explore/
├── SKILL.md
├── assets/
│   └── exploration-skeleton.md
└── references/
    ├── discovery-support.md
    ├── option-discovery-methods.md
    └── high-impact-decision-method.md
```

`SKILL.md` owns the central question, routing boundary, authority exclusions, proportional option rule, required artifact outcome, stopping condition, and handoff. `exploration-skeleton.md` owns output structure only: decision or problem, facts/assumptions/unknowns, options, criteria, comparison, research questions, and handoff. `option-discovery-methods.md` loads when reframing or deliberate option generation is needed. `high-impact-decision-method.md` loads only for strategically broad or difficult-to-reverse decisions that warrant deeper stakeholder, reversibility, and failure analysis.

The proportional rule requires enough materially different options to expose the decision space. A credible status-quo or defer option is included when relevant; no quota or predefined option taxonomy is imposed.

### Research package

```text
skills/research/
├── SKILL.md
├── assets/
│   └── research-skeleton.md
└── references/
    ├── discovery-support.md
    ├── source-and-repository-method.md
    └── experiment-and-confidence-method.md
```

`SKILL.md` owns the central question, routing boundary, authority exclusions, bounded-question and stopping rules, evidence/confidence requirement, required artifact outcome, and handoff. `research-skeleton.md` owns output structure only: supported decision, questions, evidence and source quality, findings, confidence, implications, uncertainty, and handoff. `source-and-repository-method.md` loads when source selection, freshness, repository-first investigation, or external research needs more than the core rule. `experiment-and-confidence-method.md` loads only when benchmarks, experiments, or non-trivial confidence assessment are required.

Research may recommend an answer to a bounded factual question. The artifact must label the basis and confidence, and it cannot approve or mutate the broader proposal, design, delivery, implementation, or verification decision.

### Route guidance

Route remains the semantic selector and does not invoke discovery automatically by default. Its public description and on-demand support guidance distinguish:

| Condition | Route |
| --- | --- |
| problem, value, scope, or materially different directions are unclear | `explore` |
| a material decision depends on an uncertain or volatile fact | `research` |
| option comparison depends on unresolved facts | `explore`, then bounded `research` |
| direction and material facts are sufficiently settled | neither |

The lifecycle CLI does not gain discovery stages, artifact kinds, or transition operations. Route identifies the supported owner from semantic context and returns there after the support artifact is complete.

### Artifact boundary

An explicit Explore invocation resolves one absent default target at `docs/explorations/YYYY-MM-DD-slug.md`; an explicit Research invocation resolves one absent default target at `docs/research/YYYY-MM-DD-slug.md`. Explicit safe user or project-local placement may override the portable default. Collision, ambiguity, path escape, or an unrelated existing target stops rather than overwriting.

The artifacts are ordinary Git-tracked supporting documents. They contain no lifecycle status, approval state, review package, settlement field, or independent progression authority. When a governed decision relies on a conclusion, the owning stage cites or incorporates the relevant conclusion in its own artifact and submits that artifact through its normal review.

## Runtime View

### Explore-only flow

1. The caller identifies the problem or decision and the intended owner when known.
2. Explore resolves an absent standalone artifact path and loads the shared support rule.
3. It separates facts, assumptions, and unknowns, then generates and compares a proportional set of materially distinct options.
4. It records research questions only where facts could materially change the comparison.
5. It writes the artifact and hands it to the identified owner without approving the leading option or advancing lifecycle state.

### Research-only flow

1. The caller identifies the supported decision and bounded factual questions.
2. Research resolves an absent standalone artifact path, loads the shared support rule, and defines evidence-changing and stopping conditions.
3. It examines repository evidence first when appropriate, then authoritative fresh external evidence or a bounded experiment when needed.
4. It records findings, source quality, confidence, implications, and remaining uncertainty.
5. It hands the result to the identified owner without mutating or approving that owner's artifact.

### Combined flow

Explore records factual questions that could change its option comparison. Research receives only those bounded questions, records independent evidence, and returns the findings to the same decision owner. The owner decides whether to revise the comparison, select a direction, adopt the fact, request more work, or proceed without either recommendation.

### Contradiction and stopping

If a support artifact contradicts an approved upstream decision, the skill records the contradiction and routes it to that decision's owner; it does not edit the governed artifact. Each skill stops when further work is unlikely to materially change the supported decision, when evidence is unavailable, when scope would expand, or when owner judgment is required.

## Deployment View

The change ships as Markdown skill packages, shared contributor guidance, assets, specifications, validators, fixtures, and documentation through the existing repository and adapter build path. It adds no executable dependency, service, daemon, credential, storage engine, or external telemetry.

Canonical `skills/` content is validated first. Local Codex candidates and supported Codex, Claude Code, and opencode release candidates are generated into temporary or release-output locations, with resource containment and raw-byte parity checks. Tracked `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain the adapter support surface; release archives remain generated output and historical archives are not rewritten.

Rollback before publication restores the prior coherent skill packages, shared-block inventory, routing text, specs, tests, docs, and generated candidate expectations together. After publication, recovery uses a corrective release; immutable prior archives remain available.

## Crosscutting Concepts

### Authority and ownership

Explore and Research own only their supporting artifacts. Proposal, Design, Delivery, Implementation, Verify, and other identified owners retain their existing decisions, artifacts, review gates, and lifecycle mutations. Recommendations are advisory until adopted by an owner.

### Evidence semantics

Both skills use explicit labels or prose distinctions for established evidence, inference, assumptions, confidence, and remaining uncertainty. Research requires sourced findings; Explore may rely on declared assumptions and must route material factual gaps to Research rather than promote them to facts.

### Progressive disclosure

The core skill files contain the shortest sufficient routing and authority contract. Every explicit invocation loads the small shared support reference and the relevant output skeleton. Specialized methods load only when the decision or evidence type triggers them. Missing triggered resources fail closed.

### Validation

Repository-owned checks cover metadata, required core clauses, resource-map completeness, safe containment, placeholder removal, shared-block byte parity, forbidden authority claims, proportional Explore wording, standalone artifact guarantees, Route trigger coverage, adapter inventory, and generated/installed parity. Semantic reviews judge whether the two modes remain distinct and whether handoffs preserve owner authority.

### Compatibility

Existing exploration and research artifacts remain historical evidence. Current explicit invocations adopt the new paths and standalone contract. The skill names and invocation surface remain stable; no lifecycle or persisted-state migration occurs.

### Security and privacy

Artifacts remain repository-relative and must not capture secrets, credentials, unnecessary private raw input, or machine-local paths. External research follows existing source and citation policy; adapter generation retains current archive-safety and resource-containment checks.

## Architecture Decisions

No new ADR is required. The accepted proposal owns the product-level separation and artifact direction. This architecture applies existing durable decisions for canonical `skills/` ownership, packaged skill-local resources, copied shared blocks with drift checks, repository-owned validation, generated adapter output, and stage authority. A later departure from those established boundaries would require an ADR.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| routing clarity | a request has unclear options, uncertain facts, both, or neither | Route guidance selects the matching support mode without making either mandatory |
| proportionality | a small decision has only status quo and one credible change | Explore accepts the two materially distinct options and creates no quota filler |
| inspectability | Research is explicitly invoked for one bounded question | one standalone artifact records sources, confidence, implications, uncertainty, and handoff |
| authority safety | a finding contradicts an accepted proposal or design | the support artifact records and routes the contradiction; the accepted artifact and lifecycle state remain unchanged |
| package integrity | either skill is generated and installed for a supported adapter | every mapped local resource is contained and byte-consistent with canonical inputs |
| maintainability | a common authority or handoff rule changes | one canonical shared block and both checked public copies change coherently |
| compatibility | repositories retain older discovery artifacts | historical files remain readable while new invocations use the refined contract |
| efficiency | the supported decision is already sufficiently clear | Route skips both skills and adds no supporting artifact |

## Risks and Technical Debt

- A new shared block increases validator and synchronization surface. Keeping it limited to stable common rules and enforcing exact parity bounds that cost.
- The distinction between an explicit Research invocation and a stage-local fact check is semantic. Clear routing examples and review fixtures are needed; static text checks alone cannot prove model selection quality.
- More standalone artifacts can create documentation noise. Optional triggers, concise skeletons, non-overwrite rules, and material stopping conditions constrain accumulation.
- Supporting Implementation or Verify could be mistaken for repair or approval authority. Both packages must state that the owning stage remains unchanged and that contradictions route back without mutation.
- The current project map names proposals and research but not the new exploration root. Implementation should refresh only the affected map rows if the map remains current at that point.
- Post-adoption usefulness cannot be proved before use. A separately owned follow-up should evaluate decision support and overhead without treating invocation count as the target.

## Glossary

- **Explore:** the optional divergent support skill that expands and compares materially different directions.
- **Research:** the optional convergent support skill that establishes bounded decision-relevant facts with explicit confidence.
- **Supporting artifact:** a Git-tracked exploration or research record with no independent lifecycle authority.
- **Decision owner:** the lifecycle stage or other named owner that may adopt, reject, or qualify supporting conclusions.
- **Explicit invocation:** a direct request to run the Explore or Research skill, as distinct from incidental reasoning inside another stage.
- **Shared discovery block:** the stable public authority, artifact, stopping, and handoff rules copied into both self-contained packages.

## Next artifacts

- Specification reconciliation.
- Design Review of this architecture and the specification as one exact package.

## Follow-on artifacts

- None yet.

## Readiness

The architecture is ready for specification reconciliation. It does not authorize planning or implementation until the exact Design package is approved.
