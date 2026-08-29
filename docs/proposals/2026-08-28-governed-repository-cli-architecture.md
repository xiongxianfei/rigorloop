# Governed Repository CLI Architecture

## Owning change record

Portable authoring: no owning change record exists yet. A governed change record should be created only after this proposal enters the managed workflow.

Proposal ID: `RL-PROP-CLI-ARCH-002`

## Status

- draft

## Problem

RigorLoop now has a local lifecycle CLI that can interpret governed state and guard supported `change.yaml` transitions, but its implementation and ownership boundary are too narrow for the intended governance model.

The implementation concentrates command routing, policy selection, repository access, evidence parsing, result projection, and transaction handling in a small number of increasingly large modules. The lifecycle transition evaluator also reads repository files directly even though the accepted architecture describes it as pure. Closed vocabularies and result classifications appear in multiple modules. This makes a local correction easy to implement but difficult to prove complete: recent fixes to milestone completion, replay identity, evidence binding, recovery, and result reporting repeatedly exposed adjacent defects that existing passing suites did not detect.

The ownership boundary also remains incomplete. The CLI guards lifecycle-state mutation, while review records, review logs, resolutions, explanations, verification reports, and other governed files under `docs/changes/<change-id>/` are still normally written directly. A transition can therefore depend on semantic evidence whose publication was outside the same guarded repository operation. Expanding the current single-file transaction by adding more conditionals to the existing dispatcher would increase coupling without establishing a clear public contract.

RigorLoop needs a modular CLI architecture in which callers request typed governed operations, a pure domain layer evaluates an immutable repository snapshot, and a repository transaction layer publishes the exact authorized write-set. The CLI should help users and agents complete valid work by providing concise context and recovery guidance; it should not become a generic file editor, semantic judge, or autonomous workflow engine.

## Goals

- Establish one modular internal architecture for CLI routing, application commands, lifecycle policy, repository snapshots, transactions, result projection, and observability.
- Make the CLI the supported publication boundary for governed files under `docs/changes/<change-id>/` after compatibility and migration gates are satisfied.
- Preserve semantic authorship: skills and humans produce proposals, reviews, resolutions, explanations, verification evidence, and other content, while the CLI validates and publishes supplied content without deciding its truth.
- Preserve workflow ownership of stage selection, correction routing, continuation, and automation intent.
- Replace the single-file mutation assumption with bounded, recoverable write-sets that can publish semantic evidence and matching lifecycle state coherently.
- Keep the lifecycle domain deterministic and independent of filesystem access, process state, rendering, and diagnostic logging.
- Provide typed, operation-oriented public commands with stable request, result, error, replay, and compatibility contracts.
- Keep default terminal and agent output short and useful, with detailed explanation and local diagnostic history available on demand.
- Give every rejected publication an actionable supported path when one can be determined mechanically, without weakening lifecycle integrity.
- Preserve Git-tracked, human-readable repository artifacts as durable truth and preserve fresh-checkout reconstruction.

## Non-goals

- Moving governed truth to a database, daemon, hosted control plane, or append-only external event service.
- Making the CLI decide semantic approval, review correctness, finding disposition, product intent, or engineering readiness.
- Letting the CLI choose workflow routes, invoke skills or agents, automatically continue stages, open pull requests, merge, release, or deploy.
- Introducing a generic file-write command, arbitrary YAML setter, unrestricted status setter, or broad repair escape hatch.
- Requiring portable skill use to create a governed change record or use the repository publication boundary.
- Claiming multi-repository or distributed transactional guarantees that local filesystems and Git cannot provide.
- Redesigning CLI installation, adapter distribution, local log retention, or the already approved concise-result behavior except where integration with the new command architecture requires compatibility-preserving adaptation.
- Converting every top-level artifact under `docs/proposals/`, `specs/`, `docs/architecture/`, `docs/adr/`, or `docs/plans/` into CLI-owned content in this proposal. Their change-local registration and lifecycle effects are in scope; broad top-level publication policy requires separate evaluation.

## Vision fit

fits the current vision

The direction strengthens RigorLoop's traceability and resumability by ensuring that governed evidence and the state derived from it are published through one explainable boundary. It keeps artifacts readable and diffable in Git, reduces mechanics carried in agent prompts, and preserves human and reviewer judgment. It does not introduce a hosted runtime, autonomous merge system, or replacement for engineers, CI, and Git.

## Context

The accepted [Governed Lifecycle CLI proposal](2026-08-24-governed-lifecycle-cli.md) selected the local `rigorloop` executable as the mandatory boundary for supported lifecycle transitions. The approved [Governed Lifecycle CLI specification](../../specs/governed-lifecycle-cli.md) and [transaction-boundary ADR](../adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md) deliberately limited first-release mutation to `change.yaml`; semantic Markdown remained stage-owned and was written before registration.

That first boundary remains valuable and should not be discarded. It established semantic operations, artifact identities, optimistic concurrency, deterministic interpretation, guarded repair, workflow routing ownership, and Git-native truth. The next problem is architectural: the implementation needs clearer internal separation, and the publication boundary needs to cover the change-local evidence on which lifecycle decisions depend.

Current implementation evidence motivates the proposal. The public binary combines unrelated command families in a large process entrypoint. Lifecycle behavior is selected by a large conditional evaluator that also performs repository reads and parses several Markdown evidence formats. Command and error vocabularies, terminal classification, permitted-operation calculation, and evidence interpretation cross module boundaries. This increases regression risk and makes it hard to prove that a result was derived from one complete snapshot.

This proposal extends rather than supersedes the first lifecycle CLI decision. Existing commands, request schemas, exit codes, concise results, logs, and repositories remain compatibility surfaces. The new direction should be adopted incrementally and should not declare direct change-local writes unsupported until typed publication operations, migration, package parity, and CI enforcement are available.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the CLI architecture rather than continue accumulating local fixes | in scope | Problem, Recommended Direction, Architecture Impact |
| Route governed operations under `docs/changes/` through the CLI | in scope | Goals, Recommended Direction, Expected Behavior Changes |
| Give the CLI a public operation-oriented command interface | in scope | Goals, Recommended Direction |
| Keep skills from carrying detailed lifecycle settlement mechanics | in scope | Goals, Expected Behavior Changes, Scope budget |
| Keep the CLI helpful instead of allowing lifecycle status to become an artificial deadlock | in scope | Goals, Recommended Direction, Risks and Mitigations |
| Preserve workflow as the owner of routing and continuation | in scope | Goals, Recommended Direction, Decision Log |
| Preserve semantic judgment with skills, agents, reviewers, and humans | in scope | Goals, Non-goals, Recommended Direction |
| Keep standard output concise and token-friendly while retaining detailed logs | in scope | Goals, Expected Behavior Changes, Testing and Verification Strategy |
| Avoid unnecessary subagents as an implementation requirement | out of scope | Non-goals; agent-review staffing is an invocation choice, not a CLI architecture responsibility |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Thin CLI entrypoint and command router | core to this proposal | Public command selection should not own domain policy, repository mutation, or rendering internals. |
| Typed application command handlers and one operation registry | core to this proposal | One registry removes duplicated command, authority, request, mutation, and projection vocabularies. |
| Immutable repository snapshot and pure lifecycle domain | core to this proposal | Deterministic evaluation requires all relevant facts to be captured before policy runs. |
| Bounded multi-file write-set and recovery journal | core to this proposal | Change-local evidence and matching lifecycle state need coherent publication and recovery. |
| Typed publication commands for change-local artifacts and evidence | core to this proposal | The CLI cannot be the `docs/changes/` boundary without safe semantic-content publication. |
| Compatibility aliases for existing `rigorloop lifecycle` operations | same-slice dependency | Existing skills, scripts, and users require a stable migration path. |
| Concise result projection and default local diagnostic logging integration | same-slice dependency | Every new command must preserve the already selected output and observability contract. |
| Migration of canonical governed skills | separate implementation slice | Skills should move only after public commands and compatibility behavior are proven. |
| Generated adapter and package parity | separate implementation slice | Distributed consumers need independent compatibility proof after canonical skill migration. |
| CI enforcement against unsupported direct change-local writes | separate implementation slice | Enforcement should follow command coverage, migration, and rollback readiness. |
| Retirement or convergence of overlapping Python validators | separate implementation slice | Protected failures must be preserved while authority moves toward one domain contract. |
| Top-level governed-artifact publication through the CLI | deferable follow-up | This proposal governs `docs/changes/`; broader authored-source ownership needs separate evidence and compatibility analysis. |
| Hosted authorization or distributed transactions | out of scope | These conflict with the local Git-native product boundary. |

## Options Considered

### O1: Continue extending the current lifecycle modules

Add commands and special cases to the existing binary, lifecycle CLI, and operation evaluator. This minimizes immediate movement and preserves familiar test fixtures, but it retains filesystem access inside policy evaluation, duplicated vocabularies, a large dispatcher, and a single-file transaction assumption. It is likely to continue producing fixes that are locally correct but incomplete across replay, recovery, evidence binding, and projection. Reject as the target architecture.

### O2: Introduce a modular typed repository gateway inside the existing package

Keep one `rigorloop` binary and npm package, but divide it into a thin CLI shell, typed application handlers, a pure domain model, repository snapshot adapters, a bounded transaction manager, and shared result and observability adapters. Semantic authors provide candidate content; typed CLI operations validate and publish it with matching state. This preserves the product surface and Git-native model while creating enforceable internal boundaries. Select this option.

### O3: Expose generic document and state editing through the CLI

Provide commands that set arbitrary YAML paths or write arbitrary files under `docs/changes/`, then run validation afterward. This would technically route writes through the executable, but it would preserve caller-owned transition calculation and turn the CLI into a filesystem proxy. It would not solve authority, replay, or evidence-coherence problems. Reject.

### O4: Move workflow and lifecycle state to a daemon, database, or hosted service

A central service could coordinate distributed callers and enforce stronger authorization, but it would make repository reconstruction depend on external infrastructure, materially expand privacy and availability concerns, and conflict with RigorLoop's product vision. Reject.

## Recommended Direction

Choose O2: evolve the existing package into a modular, typed governed repository gateway.

The responsibility boundary should be:

```text
skills, agents, humans
  create semantic content and make judgments
            |
            v
workflow
  selects stage, route, and continuation intent
            |
            v
CLI application command
  validates a closed semantic operation request
            |
            v
pure lifecycle domain
  evaluates one immutable repository snapshot
            |
            v
transaction manager
  publishes the authorized bounded write-set
            |
            v
docs/changes/<change-id>/ + Git
  preserve durable state, evidence, and history
```

The public interface should use typed nouns and verbs rather than target states. The eventual specification should settle exact spelling, but the intended capability families are:

```text
rigorloop change status
rigorloop change context
rigorloop change validate
rigorloop change artifact publish
rigorloop change review record
rigorloop change finding resolve
rigorloop change evidence record
rigorloop change milestone start
rigorloop change milestone request-review
rigorloop change milestone complete
rigorloop change route correction
rigorloop change route return
rigorloop change repair inspect
rigorloop change repair apply
```

Existing `rigorloop lifecycle` commands should remain supported through an explicit compatibility layer during adoption. The compatibility layer should translate old requests into the same application commands; it should not maintain a second policy implementation.

Skills and humans should prepare semantic content without mutating its governed destination, then ask the CLI to publish it. A publication request should bind the change, operation, authority claim, candidate content or safe candidate path, expected lifecycle revision, expected prior identities, and allowed destination. The CLI should validate the complete request and calculate the resulting bounded write-set. It should never accept an unrestricted destination or field path.

The domain layer should consume an immutable normalized snapshot and return either a rejection or a typed operation result plus candidate write-set. It should have no filesystem, process, clock, logging, rendering, or network access. Evidence parsing should be implemented as typed parsers at the snapshot boundary, so policy consumes normalized review, finding, milestone, and validation facts rather than scanning Markdown repeatedly.

The transaction manager should own locking, stale-revision comparison, path safety, staging, durable recovery state, deterministic replacement ordering, post-write validation, rollback, and reconciliation. Because portable filesystems do not provide atomic multi-file replacement, the product should describe this as recoverable bounded publication rather than filesystem-wide atomicity. Git remains responsible for branch divergence and integration conflicts.

The CLI should distinguish semantic work from governed publication. A structurally invalid publication can be rejected without preventing a skill or human from drafting a correction. Status and context should identify the current facts, the rejected invariant, and a supported corrective or workflow-routing operation when deterministically known. The CLI should not demand an unrelated status transition merely because a caller wants to inspect or prepare work.

Default output should remain concise and result-oriented. Successful commands should normally report the outcome, affected identity, and next supported operation in a few lines or a small stable JSON object. Detailed evidence, write-set, rule explanations, and diagnostics should be opt-in, while the approved bounded rotating local log remains the diagnostic history and never becomes lifecycle evidence.

## Expected Behavior Changes

- Supported governed files under `docs/changes/<change-id>/` are eventually published through typed CLI operations rather than written directly by governed skills or workflow automation.
- A review operation can publish the review record, update the review log, and register matching lifecycle facts as one recoverable bounded transaction.
- A resolution, explanation, verification report, or other supported change-local artifact can be published only to the destination owned by its operation and stage.
- Lifecycle policy evaluates normalized facts from one immutable snapshot instead of reading files opportunistically during transition evaluation.
- Existing lifecycle commands and request files continue through a compatibility adapter until their documented retirement conditions are met.
- Rejected publication leaves governed destination bytes unchanged or produces an explicit recoverable state; it does not strand callers without a named diagnostic or repair path when recovery is mechanically knowable.
- Read-only status, context, validation, log lookup, and draft preparation remain available even when mutation is blocked, except when safe interpretation itself is impossible.
- Workflow continues to choose routes and continuation; the CLI validates and records only the requested closed operation.
- Skills retain semantic guidance but remove repository discovery, destination selection, hash comparison, YAML mutation, review-round bookkeeping, settlement, and transaction-recovery procedure once the matching CLI operation is available.
- Human output stays short by default, machine output remains versioned and bounded, and detailed diagnostics remain available without expanding routine agent context.

## Architecture Impact

Architecture assessment is required. The proposal changes the public command taxonomy, internal package boundaries, domain purity, repository access, transaction scope, governed write ownership, compatibility behavior, skill integration, validator authority, and CI enforcement model.

The durable architecture should define six boundaries:

1. A thin process shell that parses global options, selects one command, delegates execution, and maps the result to stdout, stderr, logs, and exit status.
2. One closed operation registry that owns operation identity, request schema, authority class, mutability class, handler, compatibility aliases, and result projection.
3. Application handlers that orchestrate snapshot acquisition, domain evaluation, and publication without embedding lifecycle policy.
4. A pure domain composed of typed transition handlers and shared invariants, with exhaustive closed-vocabulary rejection and no repository access.
5. Repository adapters that resolve safe paths and parse governed YAML and Markdown into normalized immutable facts.
6. A transaction adapter that commits a bounded write-set through a versioned recovery journal and verifies the complete post-operation snapshot.

The architecture should preserve one deployable package and one public executable. A service split, plugin system, framework migration, or new persistent database is not justified by this direction.

The existing transaction ADR should be amended or superseded because it explicitly limits the transaction adapter to replacing only `change.yaml` and allows semantic Markdown to be written before CLI registration. The canonical architecture should also correct the current discrepancy between the declared pure evaluator and its repository-reading implementation.

## Testing and Verification Strategy

The downstream proof model should test architectural boundaries as well as individual transitions.

- Domain tests should construct immutable snapshots directly and prove that transition evaluation performs no filesystem, process, clock, network, rendering, or logging operations.
- Operation-registry tests should cover every registered command, compatibility alias, authority class, request schema, result projector, and unknown vocabulary value.
- Snapshot tests should prove exact parsing and identity binding for change metadata, review records, review logs, resolutions, explanations, verification reports, and supported evidence classes, including duplicate or contradictory occurrences.
- Write-set tests should prove destination ownership, prior-identity checks, deterministic ordering, idempotent replay, conflicting replay rejection, and refusal of arbitrary paths or fields.
- Fault-injection tests should interrupt each journal, staging, replacement, sync, validation, rollback, and cleanup boundary and prove either complete publication, verified restoration, or an actionable recoverable state.
- Compatibility tests should run existing lifecycle requests through the compatibility adapter and compare state, errors, exit codes, concise output, logs, and repository bytes with the established contract.
- End-to-end skill tests should prove that representative proposal, review, resolution, implementation, explanation, and verification flows can publish their owned artifacts without direct governed writes.
- CI enforcement tests should distinguish supported CLI publication, unrelated manual documentation edits, legacy compatibility state, and detectable unsupported direct mutation.
- Token measurements should compare the complete loaded skill instructions plus CLI context and output before and after migration; savings should not be claimed by removing semantic review guidance.
- Fresh-checkout tests should reconstruct effective state from tracked repository artifacts without logs, journals, caches, or prior agent sessions.

## Rollout and Rollback

Adoption should use compatibility gates rather than a big-bang rewrite.

First, freeze existing lifecycle command behavior and protected failure fixtures while introducing the internal operation registry and pure snapshot-driven domain behind compatibility adapters. Next, add bounded change-local publication operations and multi-file recovery without making them mandatory. Then migrate canonical skills and generated packages operation by operation, proving parity and token impact. Finally, enable repository and CI enforcement only when every governed writer in scope has a supported typed command and a documented recovery path.

Before enforcement, rollback means disabling new publication commands and returning migrated callers to the still-supported lifecycle compatibility contract. After enforcement, rollback requires a coordinated package, skill, schema, and CI compatibility release. Rollback should never instruct users to bypass governance using arbitrary YAML or direct change-local edits.

Transaction-format changes should be versioned. A newer CLI may reconcile only recovery states it understands exactly; unknown journals, unknown write-set operations, unsupported schema versions, or ambiguous file identities should remain untouched and produce bounded repair guidance.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| The CLI becomes a gate that prevents useful semantic work | Govern publication rather than drafting; keep read-only context available; return the exact blocker and supported corrective or routing operation when mechanically known. |
| The CLI becomes a generic workflow engine | Keep stage selection and continuation in workflow, semantic judgment in skills and humans, and restrict CLI handlers to closed structural operations. |
| Multi-file publication creates a false atomicity claim | Describe and test recoverable bounded transactions, use a durable versioned journal, and reserve distributed conflict handling for Git. |
| A larger transaction surface increases data-loss risk | Require exact prior identities, safe destination ownership, deterministic staging and replacement, fault injection, verified rollback, and fail-closed reconciliation. |
| Typed commands grow into an unmanageable public surface | Group commands by stable domain nouns, use one operation registry, add commands only for recurring owned operations, and retain detailed schemas behind concise help. |
| Compatibility adapters become a permanent second architecture | Translate old commands into the same application handlers and define evidence-based retirement conditions; never duplicate transition policy. |
| Markdown parsing remains fragile | Parse supported artifact forms once at the snapshot boundary, normalize them into typed facts, reject duplicates and contradictions, and maintain fixture-backed format contracts. |
| The executable hides lifecycle meaning | Keep durable artifacts readable, publish versioned request/result schemas and transition documentation, and make diagnostics cite evidence and invariant identities. |
| Skills lose important semantic guidance in pursuit of token savings | Remove only mechanical discovery, mutation, settlement, and recovery procedure; measure total context and explicitly preserve semantic criteria. |
| Direct writes continue after enforcement | Migrate every in-scope writer first, detect unsupported changes in CI where repository evidence allows, and provide typed repair instead of undocumented bypass instructions. |
| Existing passing tests conceal cross-boundary defects | Add architecture-boundary, adversarial replay, parser-ambiguity, and transaction fault matrices in addition to per-command happy-path tests. |
| The refactor delays user value | Preserve the existing public binary and commands, deliver internal separation behind compatibility adapters, and activate publication families independently when proven. |

## Open Questions

1. Should the long-term public namespace be `rigorloop change`, retain `rigorloop lifecycle`, or expose `change` while keeping `lifecycle` as a compatibility alias?
2. Which exact file classes under `docs/changes/<change-id>/` belong in the first publication slice, and which require later typed operations?
3. Should candidate semantic content be accepted through standard input, a repository-external temporary path, a CLI-created staging path, or more than one of these interfaces?
4. What recovery-journal representation and replacement ordering best support bounded multi-file publication across supported platforms?
5. Which post-write validator is authoritative for each change-local file class while Python and Node validation still coexist?
6. How should CI distinguish a legitimate CLI-produced diff from a semantically equivalent direct edit without introducing hidden signatures or external state?
7. What compatibility window and deprecation evidence are required before retiring individual lifecycle request forms or direct governed writers?
8. Should top-level governed artifact publication eventually use the same repository gateway, or remain stage-owned direct writes with CLI registration?
9. Which commands need ergonomic flags in addition to versioned request objects, and how can both forms normalize into one request schema?
10. What size and file-count limits should bound one local transaction without preventing legitimate formal review and verification evidence?

## Decision Log

| Decision | Outcome | Rationale |
| --- | --- | --- |
| Relationship to the first lifecycle CLI | Extend, do not replace | Existing lifecycle identity, authority, concurrency, repair, and compatibility decisions remain useful. |
| Product boundary | One local `rigorloop` executable and package | Preserves the established language-independent interface and deployment model. |
| Internal architecture | Thin shell, typed application handlers, pure domain, repository adapters, transaction adapter | Separates policy from I/O and makes cross-boundary behavior independently testable. |
| Governed write boundary | Supported `docs/changes/<change-id>/` publication goes through typed CLI operations after activation | Aligns evidence publication with the state that depends on it. |
| Semantic authority | Remains with skills, agents, reviewers, workflow, and humans according to stage ownership | Structural validity cannot establish semantic truth. |
| Workflow authority | Workflow selects routing and continuation; CLI validates and persists the supplied closed operation | Prevents the CLI from becoming an autonomous workflow engine. |
| Mutation model | Bounded typed write-set; no generic setter or arbitrary writer | Preserves narrow authority and deterministic replay. |
| Consistency claim | Recoverable local publication, not distributed or filesystem-wide atomicity | Accurately reflects portable filesystem and Git constraints. |
| Compatibility | Existing lifecycle commands translate into the new application layer during adoption | Avoids a disruptive public rewrite and competing policy engines. |
| Output model | Concise default projection plus opt-in details and bounded local logs | Protects human usability and agent token cost without losing diagnostics. |
| Architecture disposition | Canonical architecture update and transaction ADR amendment or supersession required | The proposal changes public interfaces, persistence scope, trust boundaries, and component ownership. |

## Next Artifacts

- Independent proposal review focused on product boundary, user value, scope, compatibility, transaction risk, workflow separation, and whether governing all `docs/changes/` publication is justified.
- Feature specification defining public operations, governed file classes, candidate-content interfaces, request and result schemas, failure behavior, compatibility, activation, and acceptance criteria.
- Architecture assessment and authoring covering the operation registry, pure domain, snapshot model, repository adapters, bounded write-set journal, compatibility layer, and validator convergence.
- Architecture review before execution planning because the decision changes persistence, public interfaces, security-sensitive filesystem behavior, and long-lived component boundaries.
- Execution plan and traceable test specification only after proposal, specification, and architecture settlement.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. The proposal records a selected direction and preserves the initial goals, but it is not accepted, specification-ready, architecture-approved, plan-ready, implementation-ready, verified, or PR-ready.

Proposal review should challenge whether the `docs/changes/` publication boundary is proportionate, whether draft-versus-publication separation remains usable, whether bounded multi-file recovery can be made safe enough for the value it provides, whether compatibility aliases avoid policy duplication, and whether the CLI/workflow boundary is explicit enough to prevent future deadlocks.
