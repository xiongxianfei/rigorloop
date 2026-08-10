<!-- Template: proposal-skeleton-v1 -->
<!-- Skill: proposal -->

# Published-Skill-First Repository Simplification

## Owning change record

`docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml`

## Problem

RigorLoop's user-facing product is its published skills, packaged resources, adapters, and installer, but repository-owned validation has grown into a second large system.
Direct inspection on 2026-08-10 found about 8,648 lines of Markdown under `skills/` and about 100,322 lines of Python and shell under `scripts/`, with 69 Python scripts, 24 script-level test runners, and 42 routed check definitions.
A routine edit to one canonical skill currently selects seven checks spanning boundary simulation, skill structure, validator regression, local mirror generation, adapter archive construction, and prose auditing.

The problem is not that validation exists.
The problem is that checks, selectors, caches, schedulers, executable workflow models, and tests of those mechanisms can grow without a consistent test that they protect the published product better than a smaller product-level gate would.
This increases contributor cost, creates competing executable interpretations of prose contracts, and makes simplifying the repository harder because validation infrastructure validates other validation infrastructure.

## Goals

- Make canonical published skills and their packaged resources the primary product boundary for repository decisions.
- Define a strict admission and retention test for repository scripts based on named public, governance, package, or release failures.
- Consolidate publication proof into three deterministic product-level gates.
- Keep semantic skill quality in human or agent review rather than target-runtime acceptance tests.
- Preserve one bounded repository-governance check for stage-owned change records and closed-vocabulary safety.
- Retire overlapping validation orchestration in reversible slices backed by old-versus-new proof.
- Make routine skill contribution easier to understand without weakening installation, adapter parity, release integrity, or required lifecycle evidence.

## Non-goals

- Deleting scripts directly from this proposal or treating line-count reduction as sufficient evidence.
- Weakening the published workflow chain, review independence, formal review recording, or source-of-truth order.
- Rewriting published skill behavior merely to make existing validators easier to remove.
- Removing adapter-parity, release-integrity, unknown-value, or negative-path proof for deterministic product failures.
- Running Codex, Claude Code, or opencode to evaluate prompt routing, model selection, transcripts, or generated behavior as repository acceptance.
- Treating prose clarity, architecture quality, plan quality, test adequacy, or agent behavior as validator-owned judgments.
- Splitting maintainer tooling into a second repository as the first response.
- Deciding the future of the advertised automatic-workflow capability in this proposal; that product decision needs a separate proposal if executable modeling is to be retired.
- Releasing, publishing, tagging, or changing external state.

## Vision fit

fits the current vision

The direction reinforces RigorLoop's differentiator: durable, human-understandable skills and artifacts that make AI work traceable and reviewable.
It also addresses the vision's explicit failure condition in which teams ignore the artifacts because process cost grows without improving review quality.
The proposal preserves trustworthy automation where it protects a real boundary while refusing validation volume as a proxy for product quality.

## Context

`CONSTITUTION.md` requires trustworthy automation, repository-owned validation logic, thin GitHub Actions wrappers, deterministic generated output, and named verification evidence.
Those constraints require necessary scripts; they do not require every invariant to have its own parser, selector route, cache layer, scheduler, or regression program.

The active stage-owned lifecycle plan already records the intended precedence: canonical published skills are primary, scripts are subordinate, and a new validator is justified only when an unproved deterministic invariant cannot fit an existing owner.
The current repository nevertheless contains several substantial validation subsystems:

- skill validation, skill mirror generation, adapter generation, and package validation;
- lifecycle, change-metadata, and review-artifact validation;
- selector routing, validation caching, broad-smoke scheduling, and scheduler classification;
- workflow-automation state, policy, code-state, validation, and engine simulation;
- readability, documentation-prose, guide-system, README, and boundary-first checks;
- token-cost measurement, benchmark execution, report validation, and release transactions.

Some of these protect public failures directly.
Others exist primarily to select, accelerate, or cross-check other repository checks.
The proposal creates an explicit boundary for deciding which is which.

## Options Considered

### O0. Keep the current system

Continue maintaining all existing scripts and add new checks whenever a contract gap appears.

This has the lowest immediate migration risk, but it leaves the maintenance imbalance and self-reinforcing validation architecture untouched.
It is rejected because it does not address the user's simplification goal.

### O1. Freeze new validators only

Adopt a script-admission rule and prohibit new standalone validators unless no existing owner can protect the invariant.

This stops growth cheaply and should begin immediately, but it does not reduce existing contributor or CI complexity.
It is useful as a containment policy, not a complete solution.

### O2. Consolidate around product-level gates

Retain a small publication core, one repository-governance check, and focused negative-path tests.
Replace overlapping selectors, caches, schedulers, and presentation validators with direct gate composition and human review where semantic judgment is required.

This best balances simplification, public safety, reviewability, and rollback.
It is the recommended direction.

### O3. Move validation machinery to a separate internal tool or repository

Keep the current functionality but move it out of the main product tree.

This creates a visually smaller repository, but it does not reduce conceptual complexity and introduces versioning and synchronization boundaries.
It is rejected as premature displacement of the problem.

### O4. Reset to skills and packaging only

Remove most lifecycle, workflow-automation, selector, cache, document-lint, and benchmark machinery in one compatibility break.

This offers the largest immediate reduction but makes hidden safety loss difficult to diagnose and rollback.
It is rejected as too broad and too hard to review safely.

## Recommended Direction

Adopt O1 as an immediate policy and execute O2 through separately reviewable retirement slices.

The governing principle is:

```text
Test what RigorLoop deterministically owns.
Review what requires semantic judgment.
Do not run an LLM to validate an LLM instruction file.
```

The retained publication core should expose three stable product-level gates:

1. **Gate A: canonical skill integrity** validates deterministic properties of canonical `skills/`: frontmatter, required structural sections, resource maps, mapped-resource existence, normalized relative paths, path traversal exclusion, packaged-resource completeness, unfilled placeholders, truly contractual closed vocabularies, and narrow forbidden claims with deterministic meaning. It does not decide whether prose is good or predict how an agent behaves.
2. **Gate B: published adapter and package parity** generates Codex, Claude Code, and opencode packages from canonical `skills/` and verifies expected skills and files, resource inventory, mapped-resource paths, canonical/generated byte parity, declared target-specific transformations, and archive contents. All three targets receive the same deterministic proof. No target runtime is started and no prompts are sent.
3. **Gate C: release integrity** reuses Gates A and B, then verifies version and package metadata, archive inventory, checksums, release metadata, required release notes and evidence, current generated-package parity, and rollback or release consistency. It does not rebuild an independent interpretation of skill or adapter correctness.

Installer testing is conditional rather than a fourth product gate.
If the installer only copies package contents already covered by parity, Gate B is sufficient.
If the installer performs meaningful RigorLoop-owned transformation or materialization logic, a narrow deterministic test may invoke it in an empty temporary directory and inspect resulting files.
That test does not start Codex, Claude Code, or opencode and does not send prompts.

Semantic skill quality remains review-owned.
Review checks description clarity, artifact and stage ownership, prerequisites, followable procedure, packaged-resource use, stop conditions, claim boundaries, output shape, and handoff.
Repository validation does not convert those judgments into semantic prose rules.

Repository lifecycle governance remains a separate bounded concern rather than a fifth publication product.
One change-record validation owner should cover stage-owned lifecycle shape, legal transitions, review references, and unknown closed-vocabulary values.
The design should prefer extending or consolidating into that owner over preserving several overlapping lifecycle parsers.

A script is admitted or retained only when its inventory record names:

- the public, governance, package, or release failure it prevents;
- why deterministic automation is appropriate;
- why an existing gate cannot own the invariant more simply;
- its invocation boundary, such as focused authoring, pull request, package build, or release;
- its repair-oriented failure output;
- the evidence required before retirement.

Checks that only select, cache, parallelize, classify, or regression-test validation orchestration should be presumed replaceable unless measured repository scale demonstrates that the extra subsystem is necessary.
The recommended defaults are zero new standalone validator CLIs, zero new selector or check-routing systems, and zero new validation caches or schedulers.
New logic may extend an existing clear owner when it protects a concrete deterministic invariant.

## Expected Behavior Changes

- Contributors editing canonical skills encounter a small, documented gate set tied to published outcomes rather than a dynamically selected list of internal mechanisms.
- GitHub Actions remain thin but call stable product gates directly or through a minimal transparent wrapper.
- Generated Codex, Claude Code, and opencode adapters remain derived from canonical `skills/` sources and receive equivalent deterministic inventory, resource, transformation, archive, and byte-parity proof.
- No target agent runtime is executed for repository acceptance, and no prompt, routing, transcript, model-selection, or behavioral certification subsystem remains.
- Installer materialization is tested only when it contains meaningful RigorLoop-owned filesystem logic that package parity cannot prove.
- Semantic skill quality is assessed through a concise review checklist rather than a semantic validator.
- Release validation remains conservative at the publication boundary while routine authoring avoids release-only benchmarks and transaction checks.
- Change-record validation remains available for repository governance, but overlapping lifecycle and review parsers are consolidated where their invariants share one owner.
- Adding a new script requires an explicit public-failure and ownership rationale rather than only a new check identifier.
- Retired checks leave a traceable compatibility and proof record rather than disappearing through unreviewed deletion.

The published lifecycle stage order, artifact responsibilities, formal review recording, and adapter targets remain unchanged by this proposal.

## Architecture Impact

The change affects the boundary among canonical skills, repository validation, CI, adapter generation, npm packaging, lifecycle metadata, and release automation.
It is architecture-affecting because it changes validation ownership and removes executable paths that currently influence contributor and release behavior.

The target dependency direction is:

```text
skills/ and skill-local resources
  -> Gate A: deterministic skill integrity
  -> Gate B: Codex, Claude Code, and opencode generation and parity
  -> release integrity

change-local lifecycle records
  -> one bounded governance validator

semantic skill quality
  -> human or agent review
```

Selectors, caches, schedulers, prose linters, and workflow simulators should not sit between canonical skills and publication unless a later spec demonstrates a distinct necessary boundary.
An architecture assessment is expected to classify architecture work as required and identify the exact consolidation boundaries before planning.

## Testing and Verification Strategy

- Build an inventory mapping every retained script and routed check to a named failure, owner, invocation boundary, and proof surface.
- Create a coverage matrix that maps existing accepted and rejected deterministic fixtures to the proposed product gates before retiring their current owners.
- Run old and replacement gates against the same representative skill, adapter, package, lifecycle, and release changes during the transition.
- Preserve explicit negative cases for invalid metadata, missing resources, unsafe paths, unfilled placeholders, stale generated bytes, undeclared transformations, broken archives, version mismatch, illegal lifecycle transitions, dangling review records, and unknown contractual closed-vocabulary values.
- Validate Codex, Claude Code, and opencode through deterministic generation, expected inventory, mapped-resource presence, declared transformations, archive contents, and byte parity.
- When the installer has meaningful materialization logic, invoke only the installer in an empty temporary directory and inspect resulting files.
- Do not start a target agent runtime, send prompts, review runtime transcripts, grade LLM output, maintain model or runtime matrices, or retry nondeterministic model executions.
- Use a concise semantic review checklist for description, ownership, inputs, procedure, resources, stop conditions, claims, output, and handoff.
- Validate a release candidate without publishing it.
- Measure command count, runtime, changed lines, and maintenance ownership, but treat those as simplification evidence rather than substitutes for deterministic product proof.
- Remove a check only after its protected failures are either covered by a retained gate or explicitly removed from the approved contract.

## Rollout and Rollback

Begin with a no-new-validator admission policy and a read-only inventory.
Define the replacement gates before changing CI routing.
For each retirement slice, run the old and replacement proof paths together, record any coverage difference, then remove only the superseded implementation and fixtures.

Retire target-runtime behavior and journey evaluation first, followed by semantic prose validators, unnecessary selector indirection, unproven validation caches, broad-smoke scheduler complexity, duplicated lifecycle or review validators, and meta-tests whose main purpose is validation orchestration.
Handle lifecycle validator consolidation, release transactions, token-cost policy, boundary-first transition machinery, and workflow-automation simulation only in later slices with their governing contracts in scope.

Rollback restores the most recent retired slice and its direct CI invocation.
Canonical skill source, generated-package formats, public versions, and historical review evidence remain unchanged during rollback.
No slice rewrites published release history or relies on destructive migration.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| A retired check protected an undocumented failure | Public or governance regression | Require a failure inventory, old-versus-new execution, and explicit contract treatment before deletion. |
| Consolidation creates one unmaintainable validator | Complexity is moved rather than reduced | Organize by gate ownership and shared data model; reject unrelated semantic judgment from deterministic validators. |
| Human review applies semantic criteria inconsistently | Skill quality drifts | Use one concise review checklist and require reviewers to name concrete ownership, stop-condition, claim, resource, output, or handoff concerns. |
| CI simplification weakens release proof | Broken adapters or package publication | Keep all-target generation and byte parity, version, archive, checksum, and release metadata checks at the publication boundary. |
| A target runtime interprets valid skill text unexpectedly | Runtime behavior differs despite correct repository artifacts | Treat this as outside deterministic repository acceptance; investigate user-reported defects without creating routine LLM certification. |
| Installer logic is incorrectly assumed to be a pure copy | Installed files differ from package contents | Inventory installer behavior and retain a narrow filesystem materialization test only when meaningful transformation exists. |
| Script deletion conflicts with existing specs or plans | Source-of-truth violation | Amend or supersede governing contracts before retiring their proof paths; do not let implementation silently redefine policy. |
| Scope expands into redesigning the entire lifecycle | Long-running initiative with weak reviewability | Use the scope budget below and require separate proposals for product decisions such as executable workflow automation. |
| Metrics reward line deletion over correctness | Superficial simplification | Treat line and runtime reductions as secondary outcomes after public failure coverage is preserved. |

## Open Questions

- What numeric admission budget, if any, should accompany the qualitative script-admission rule without encouraging check gaming?
- Which existing lifecycle validator should become the single repository-governance owner after architecture review?
- Which token-cost checks are release-critical, and which can become optional maintainer analysis?
- Does the current installer perform meaningful RigorLoop-owned filesystem transformation beyond copying package contents?
- What transition duration is sufficient for old-versus-new gate comparison before each retirement?

These questions affect the later spec and architecture but do not change the selected direction.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Simplify the repository | in scope | Problem, Goals, Recommended Direction, Rollout and Rollback |
| Focus on published skills | in scope | Goals, Vision fit, Recommended Direction, Expected Behavior Changes |
| Avoid adding too many check scripts | in scope | Problem, O1, script-admission rule |
| Keep necessary scripts | in scope | three product gates, bounded governance validator, Testing and Verification Strategy |
| Do not execute any target agent runtime for repository acceptance | in scope | Recommended Direction, Testing and Verification Strategy, Risks and Mitigations |
| Keep semantic skill quality review-owned | in scope | Recommended Direction and Expected Behavior Changes |
| Start a new branch | in scope | workflow execution evidence outside the stable proposal |
| Create a proposal and proposal review | in scope | Owning change record, Readiness, and formal review artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Product-boundary and script-admission policy | core to this proposal | It is the decision that governs all later retention and retirement work. |
| Three deterministic publication gates | core to this proposal | They define the complete product proof surface without target-runtime execution. |
| Semantic skill review checklist | same-slice dependency | Removing semantic validators needs an explicit human or agent review owner. |
| Optional installer materialization test | same-slice dependency | It remains only when installer logic performs deterministic transformation not covered by package parity. |
| Target-runtime behavior, prompt, routing, transcript, and model certification | out of scope | These are nondeterministic semantic evaluations and would recreate validation-system growth. |
| One bounded change-record governance validator | core to this proposal | The constitution still requires trustworthy lifecycle evidence and closed-vocabulary validation. |
| Selector, cache, scheduler, and presentation-check retirement | first-slice candidate | These mechanisms are the clearest orchestration overhead and can be compared without changing published semantics. |
| Lifecycle and review-validator consolidation | separate implementation slice | It affects authoritative state and formal review evidence, so it needs focused compatibility proof. |
| Release-transaction and token-cost simplification | separate implementation slice | These checks execute at a higher-risk publication boundary. |
| Executable workflow-automation engine retirement | separate proposal | README-visible automatic workflow behavior requires an explicit product decision. |
| Split maintainer tooling into another repository | out of scope | It moves complexity and adds synchronization without first proving removal is unsafe. |
| One-step bulk deletion | out of scope | It prevents bounded proof and safe rollback. |

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-10 | Make published skills and installable distribution the primary product boundary. | That is the user-facing value and the repository's documented architectural intent. | Treating validation infrastructure as a co-equal product. |
| 2026-08-10 | Freeze new standalone validators, then consolidate around three deterministic product gates and one governance owner. | This stops growth immediately while preserving product and lifecycle invariants the repository actually owns. | Freeze only; bulk reset; separate tooling repository. |
| 2026-08-10 | Require named failure ownership and retirement evidence for every script. | Necessary validation should be explainable through the failure it prevents, not its historical presence. | Line-count quotas alone; undocumented maintainer judgment. |
| 2026-08-10 | Exclude executable workflow-automation retirement from this proposal. | It is an advertised capability and needs a separate product decision rather than incidental deletion. | Silent retirement inside validation cleanup. |
| 2026-08-10 | Do not execute Codex, Claude Code, or opencode for repository acceptance. | The repository deterministically owns instruction files, generated packages, archives, release metadata, and optional installer filesystem behavior—not model interpretation. | Codex-only behavior testing; three-target runtime matrices; packaging plus LLM certification. |
| 2026-08-10 | Keep semantic skill quality review-owned. | Description clarity, followability, ownership, stop conditions, and handoff require judgment and should not become semantic validator logic. | Prompt suites, transcript grading, semantic prose validators. |

## Next Artifacts

- Formal proposal review for this direction.
- An approved feature spec defining the product gates, script-admission contract, compatibility expectations, and retirement evidence.
- An architecture assessment followed by architecture and architecture review when confirmed required.
- An execution plan and test specification after the spec and architecture settle.

## Follow-on Artifacts

None yet

## Readiness

The revised proposal is ready for `proposal-review` R2.
It does not authorize script deletion, CI changes, spec authoring, implementation, release, or publication.
