# Architecture authoring evidence

- Stage: `architecture`
- Assessment: `architecture-required`
- Canonical artifact: `docs/architecture/system/architecture.md`
- Component diagram: `docs/architecture/system/diagrams/component-published-skill-validation.mmd`
- Updated context and container views: `docs/architecture/system/diagrams/context.mmd`, `docs/architecture/system/diagrams/container.mmd`
- Durable decision: `docs/adr/ADR-20260810-published-skill-first-validation-architecture.md`
- Changed arc42 sections: related artifacts, Introduction and Goals, Architecture Constraints, Context and Scope, Solution Strategy, Building Block View, Runtime View, Deployment View, Crosscutting Concepts, Architecture Decisions, Quality Requirements, Risks and Technical Debt, Glossary, Next artifacts, Readiness
- Architecture-review R1 correction: section 7 now directly records Gate B package outputs, Gate C release composition, conditional filesystem-only materialization, target-runtime exclusion, and transitional old execution paths
- Unchanged with rationale: security and privacy remains repository-local and credential-free
- Project-map reliance: bypassed for target-state design because `docs/project-map.md` is a 2026-07-28 current-state orientation that explicitly records selectors, caches, and Codex runtime benchmarks this change proposes to retire; direct canonical architecture and source inspection were used
- Status: `review-required` after accepted PSR-AR1-001 correction
- Next stage: `architecture-review`
