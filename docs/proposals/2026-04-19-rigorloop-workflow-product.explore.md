# RigorLoop Workflow Product Exploration

## Status
- draft

## Problem restatement

RigorLoop is trying to solve a real AI engineering problem: AI-assisted delivery is often quick to draft but hard to review, audit, and trust because rationale, requirements, architecture decisions, tests, and verification evidence are scattered across chats and tooling. The repository already has artifact-oriented scaffolding, but it does not yet prove what shape of product RigorLoop should be. The key decision is not whether rigor matters. The key decision is how much workflow, tooling, and enforcement should exist in the first public version before adoption cost overwhelms value.

## Stakeholders and affected journeys

- Individual contributors who want a practical path from idea to PR without losing traceability.
- Maintainers and reviewers who need to understand why a change exists and what evidence supports it.
- Small teams that may adopt the workflow as a starter kit for multiple repositories.
- Tool-adapter authors who may want to connect Codex or other assistants without changing the core contract.
- Future contributors who will need to maintain templates, automation, docs, and examples.

## Facts, assumptions, and unknowns

### Facts

- The repository is still positioned as a generic template in `README.md`.
- The repo already contains plans, specs, test specs, workflows, scripts, and Codex skills.
- The current proposal direction favors an opinionated open-source workflow, not a hosted platform.
- The currently preferred audience is individual contributors.
- The currently preferred lifecycle is:
  - constitution / project-map when needed
  - explore
  - research when needed
  - proposal
  - proposal-review
  - spec
  - spec-review
  - architecture
  - architecture-review when needed
  - plan
  - plan-review
  - test-spec
  - implement
  - code-review
  - verify
  - ci when automation is missing or stale
  - explain-change
  - pr
  - learn

### Assumptions

- Git, pull requests, CI, and human review should remain the source of truth.
- The core workflow should stay tool-agnostic even if Codex-specific adapters exist.
- Not every change should require the full lifecycle.
- A starter kit is more aligned with the current repository than a standalone runtime product.

### Unknowns

- What reduced path should apply to trivial or low-risk work?
- How should explainable change history be divided across PR text, repository artifacts, and structured metadata?
- How much validation automation is helpful before it becomes ceremony?
- What sample change would best prove value to a skeptical contributor?
- Where does optional guidance end and enforceable workflow begin?

## Decision criteria

The strongest option should score well on:

- time to first real user value
- clarity of project identity
- adoption cost for individual contributors
- rigor and auditability for reviewers
- tool neutrality and portability
- maintainability of docs, templates, and automation
- ability to grow into stronger verification later without breaking the core model

## Options summary

| Option | Core idea | User value | Complexity | Adoption friction | Long-term upside |
| --- | --- | --- | --- | --- | --- |
| `O0` | Keep the repo as a generic template for now | Low | Low | Low | Low |
| `O1` | Publish a minimal workflow identity with mostly docs and a small artifact set | Medium | Low | Low | Medium |
| `O2` | Ship a reusable starter kit with a full reference loop, reduced path, and worked examples | High | Medium | Medium | High |
| `O3` | Add lightweight workflow validation tooling and reusable automation on top of the starter kit | High | Medium-High | Medium-High | High |
| `O4` | Build a workflow orchestration product that actively drives the lifecycle | Potentially very high | Very high | High | Very high |

## Options in detail

### `O0` Do nothing or defer

- Core idea:
  Keep the repository as a generic Codex-ready template until stronger market or user evidence exists.
- User value:
  Preserves flexibility and avoids overcommitting to a product direction.
- Implementation complexity:
  Low. Mostly no-op beyond maintaining the existing template.
- Architecture impact:
  Minimal. No new boundaries or contracts.
- Testing burden:
  Minimal. Template docs and existing scripts continue as-is.
- Rollout and rollback:
  No rollout needed. Rollback is irrelevant because little changes.
- Risks:
  The repo remains strategically vague and may never accumulate coherent evidence for a differentiated workflow product.
- What would make this option wrong:
  If the team already knows the problem is worth solving and delay mainly protects ambiguity rather than quality.

### `O1` Minimal safe change

- Core idea:
  Reposition the repo as RigorLoop in docs, define a narrow default workflow, and keep most advanced stages optional or advisory.
- User value:
  Gives contributors a clear message and a small amount of usable structure without much process overhead.
- Implementation complexity:
  Low. Mostly documentation, templates, and a small amount of example work.
- Architecture impact:
  Limited to repository docs, starter templates, and maybe a few helper scripts.
- Testing burden:
  Low to medium. Mostly documentation review and basic convention checks.
- Rollout and rollback:
  Easy to roll out with docs-first changes and easy to roll back if the framing misses the audience.
- Risks:
  May underdeliver on rigor, leave explainable history too vague, and fail to differentiate from other workflow templates.
- What would make this option wrong:
  If the core promise of RigorLoop depends on a visibly complete loop rather than a lightly branded template.

### `O2` Incremental product improvement

- Core idea:
  Ship RigorLoop as a reusable starter kit with a full reference lifecycle, an explicitly reduced path for small changes, concrete examples, and a clear explain-change pattern.
- User value:
  Gives individual contributors a credible end-to-end workflow while keeping adoption practical.
- Implementation complexity:
  Medium. Requires stronger docs, examples, artifact definitions, and enough validation to keep the flow coherent.
- Architecture impact:
  Affects README, workflows, proposals, specs, test specs, templates, helper scripts, and CI convention checks.
- Testing burden:
  Medium. Requires example-driven verification and artifact-consistency checks.
- Rollout and rollback:
  Docs-first rollout is still feasible. Rollback can relax enforcement while keeping the starter-kit framing.
- Risks:
  The workflow may feel heavy if the reduced path is not crisp. Documentation can drift from automation if validation stays too weak.
- What would make this option wrong:
  If real users only want one isolated capability such as spec generation or change explanation, not a disciplined workflow.

### `O3` Architectural or tooling-oriented option

- Core idea:
  Keep the starter-kit model, but add reusable workflow validation tooling such as CI checks, schemas, or a CLI that understands artifact relationships and stage expectations.
- User value:
  Increases trust that teams are actually following the workflow instead of only documenting it.
- Implementation complexity:
  Medium to high. Requires stable contracts, more scripting, and stronger cross-artifact logic.
- Architecture impact:
  Introduces a tooling layer that sits between repository artifacts and CI enforcement.
- Testing burden:
  Medium to high. Needs fixture repos, regression tests, and compatibility coverage.
- Rollout and rollback:
  Should be opt-in at first. Rollback means turning automation advisory or removing enforcement.
- Risks:
  Tooling may calcify too early, encode unstable policy, or create vendor-shaped assumptions in a supposedly generic workflow.
- What would make this option wrong:
  If the workflow contract is still moving or if users cannot justify the extra setup burden.

### `O4` High-risk / high-upside option

- Core idea:
  Build RigorLoop as an active orchestration product that manages lifecycle stages, agent handoffs, artifact creation, and explainable history automatically.
- User value:
  Could offer the strongest end-to-end experience and the clearest automation story.
- Implementation complexity:
  Very high. This is a product build, not a documentation-first starter kit.
- Architecture impact:
  Major. Requires runtime design, state management, integrations, security boundaries, and operational ownership.
- Testing burden:
  Very high. Requires end-to-end workflow testing, error recovery testing, security review, and compatibility work.
- Rollout and rollback:
  Difficult to roll out safely and difficult to unwind once teams depend on it.
- Risks:
  Platform trap, vendor lock-in, unclear maintainer burden, and loss of the tool-agnostic Git-first posture.
- What would make this option wrong:
  If the project's real strength is workflow design and artifact discipline rather than operating a workflow platform.

## Comparative observations

- `O0` is honest but strategically weak. It protects optionality at the cost of identity.
- `O1` is the safest public repositioning, but it risks sounding better than it behaves.
- `O2` is the strongest fit with the current repo and the current proposal because it keeps the starter-kit posture while making the workflow concrete.
- `O3` is attractive only after `O2` defines stable artifacts and stage boundaries.
- `O4` has the highest upside only if the project intends to become a platform company or runtime, which current context does not support.

## What remains unsolved after each option

- `O0`: the core product question remains unsolved.
- `O1`: explainable history and real rigor remain underspecified.
- `O2`: the reduced path and enforcement threshold still need careful definition.
- `O3`: user willingness to adopt more tooling remains uncertain.
- `O4`: nearly everything except ambition remains unsolved.

## Recommendation

Recommend a staged sequence centered on `O2`.

- Use `O2` as the product direction:
  RigorLoop should be a reusable starter kit with a complete reference lifecycle, a reduced path for small changes, clear examples, and explainable change history patterns.
- Borrow the restraint of `O1` for initial rollout:
  start documentation-first and avoid pretending every stage is mandatory before the contract is defined.
- Defer `O3` until the spec and examples prove which artifact relationships are stable enough to automate.
- Reject `O4` for now:
  it changes the nature of the project from workflow product to platform product.

This recommendation best balances user value, repository fit, tool neutrality, and incremental delivery.

## Research questions before freezing the contract

- Which concrete sample change should serve as the first proof-of-value example for an individual contributor?
- What is the smallest reduced path that still preserves trust for trivial or low-risk work?
- Which explain-change information belongs in PR text, which belongs in reusable artifacts, and which belongs in structured metadata?
- Which workflow stages are advice, which are defaults, and which should eventually be enforced?
- What minimal CI or script checks provide real value without making adoption brittle?
- How should the starter kit separate generic workflow rules from Codex-specific guidance?

## Readiness

This exploration is ready to strengthen the current proposal and to inform `research` on explainable history representation, reduced-path design, and lightweight automation. If those questions are answered narrowly, the project can move into `spec` without reopening the overall product direction.
