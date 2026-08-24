# Governed Lifecycle CLI for RigorLoop

## Owning change record

[Governed change record](../changes/2026-08-24-governed-lifecycle-cli/change.yaml)

Proposal ID: `RL-PROP-CLI-001`

## Problem

RigorLoop's governed lifecycle depends on humans, agents, skills, and workflow automation correctly interpreting and directly editing lifecycle metadata. A syntactically valid `change.yaml` can therefore describe an unsupported transition: an artifact can appear settled without a current review, a milestone can advance out of order, or stale evidence can be treated as current.

The current instruction and validation model reduces this risk but does not provide a deterministic mutation boundary. Prompt guidance remains probabilistic, lifecycle mechanics are repeated across skills and adapters, and validation often detects invalid state after it has already been written. As lifecycle rules become more precise, every caller effectively has to reimplement the state machine.

RigorLoop needs one local, executable boundary that interprets current governed state, validates a requested semantic operation, ties evidence to exact artifact identity, and either commits an atomic repository update or rejects the request with an actionable explanation.

## Goals

- Prevent known-invalid governed lifecycle transitions before repository state is mutated.
- Establish one canonical interpreter for recorded state, effective state, blockers, evidence freshness, and permitted operations.
- Replace field-level lifecycle edits with narrow, operation-oriented commands whose authority is explicit.
- Keep semantic judgment, durable recording, artifact settlement, and workflow continuation distinct.
- Reduce the lifecycle-mechanics instructions and repository-discovery work loaded into agent context while preserving stage-specific semantic guidance.
- Keep Git-tracked repository artifacts as the durable, inspectable, reconstructable source of truth.
- Give humans, agents, adapters, automation, and CI the same lifecycle interpretation and validation contract.
- Preserve portable skill use when no governed change record exists.

## Non-goals

- Building an autonomous coding agent, model runtime, or general-purpose workflow engine.
- Allowing the CLI to decide semantic correctness, infer approval from test success, resolve ambiguous findings, or perform unbounded review-and-fix loops.
- Automatically progressing the full lifecycle, opening or approving pull requests, merging, deploying, or replacing workflow routing.
- Replacing Git-tracked state with a hosted control plane, daemon, conversation state, user database, or required local cache.
- Requiring portable-mode skill users to create `change.yaml`.
- Providing a generic status setter or unrestricted repair escape hatch.
- Claiming protection against a malicious maintainer who can rewrite the binary, repository, history, and CI policy.

## Vision fit

fits the current vision

The proposal strengthens traceability, resumability, and reviewability by making invalid governed transitions harder to create while leaving the durable facts readable in Git. It also reinforces the vision's refusal to become a hosted agent runtime or autonomous merge system: the CLI enforces structural lifecycle integrity but does not replace engineering judgment, reviewers, workflow routing, or ownership.

## Context

RigorLoop already separates semantic judgment, durable recording, artifact settlement, and workflow continuation. The stage-owned lifecycle contract makes `docs/changes/<change-id>/change.yaml` the mutable coordination surface, while proposals, specs, architecture records, plans, reviews, explanations, and verification reports preserve durable intent and evidence.

The existing accepted [RigorLoop Scaffolding CLI and Machine-Readable Workflow proposal](2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md) established `@xiongxianfei/rigorloop` and the `rigorloop` executable as the human-, agent-, and CI-facing CLI boundary. That proposal intentionally selected a small CLI facade before a full workflow state machine. Subsequent work delivered initialization and change scaffolding, but governed transition authority remains distributed across skills, workflow code, validators, and direct metadata edits.

This proposal extends that accepted product direction. It does not replace the existing package or its scaffolding responsibilities. It proposes that the same local CLI become the mandatory boundary for supported governed lifecycle mutations after read-only interpretation, guarded operations, compatibility handling, and migration support are specified and proven.

The decision requested is to approve this direction for downstream specification and architecture assessment. Approval would establish the product and authority boundary, not settle the exact command vocabulary, state representation, concurrency algorithm, schema migration, or implementation plan.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Make a local CLI mandatory for governed lifecycle transitions | in scope | Goals, Recommended Direction, Expected Behavior Changes |
| Prevent invalid transitions through precondition checks and guarded mutation | in scope | Problem, Recommended Direction, Testing and Verification Strategy |
| Centralize effective-state interpretation and diagnostics | in scope | Goals, Recommended Direction |
| Reduce agent operating complexity and workflow-mechanics token consumption | in scope | Goals, Recommended Direction, Testing and Verification Strategy |
| Preserve Git-tracked artifacts as durable truth | in scope | Goals, Recommended Direction, Architecture Impact |
| Serve humans, agents, adapters, automation, and CI through one contract | in scope | Goals, Recommended Direction |
| Keep portable-mode skill use independent of governed lifecycle state | in scope | Non-goals, Expected Behavior Changes |
| Include inspection, context, evidence recording, settlement, milestone transitions, validation, migration, and repair in the first release | in scope | Recommended Direction, Scope budget |
| Keep semantic review, orchestration, automatic progression, PR execution, and merging outside the first release | in scope | Non-goals, Recommended Direction |
| Detect stale operations and document branch and concurrency behavior | in scope | Architecture Impact, Open Questions, Testing and Verification Strategy |
| Demonstrate lifecycle-integrity improvement and measurable token reduction | in scope | Testing and Verification Strategy, Readiness |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Canonical read-only status, blockers, and allowed-operation interpretation | core to this proposal | Every guarded operation depends on a shared effective-state model. |
| Operation-specific context for governed stages and reviews | first-slice candidate | It can reduce discovery cost and validate the interpreter before mutation is enabled. |
| Review, finding, and validation-evidence registration | first-slice candidate | These are narrow semantic recording operations needed before settlement can be guarded. |
| Artifact settlement and implementation-milestone transitions | first-slice candidate | These are the principal high-value mutation boundaries, subject to the transition inventory. |
| Repository validation and stable machine-readable diagnostics | same-slice dependency | Local and CI enforcement need the same interpreter and error model. |
| Schema migration, legacy diagnostics, and controlled repair | same-slice dependency | Mandatory mutation cannot be adopted safely without a documented recovery path. |
| Published governed-skill migration | separate implementation slice | Skill packages should migrate only after the read and mutation contracts are proven. |
| CI enforcement of the mandatory boundary | separate implementation slice | Enforcement follows compatibility testing and skill migration. |
| Token baseline and post-migration measurement | separate implementation slice | Measurement spans representative skills and adapters and should not obscure core transition implementation. |
| Automatic lifecycle progression and agent orchestration | out of scope | Workflow routing and semantic execution remain separate responsibilities. |
| Pull-request execution, merging, deployment, or hosted authorization | out of scope | These materially broaden the product and trust boundary. |

## Options Considered

### O1: Continue direct `change.yaml` mutation with stronger instructions

This has the lowest implementation cost and keeps all mechanics visible in skill text. It leaves transition enforcement probabilistic, duplicates rules across callers, consumes agent context, and makes lifecycle evolution costly. Reject for governed transitions.

### O2: Permit direct edits and rely on schema and repository validation

This strengthens CI and local detection while preserving the existing write model. It is useful as defense in depth, but it validates state after callers calculate and write mutations, does not naturally express operation intent or narrow authority, and is weak at stale-operation handling. Retain validation as a CLI capability, but reject it as the complete boundary.

### O3: Make the existing local CLI the guarded transition boundary

Callers request semantic operations; the CLI reads current repository state, validates identity, evidence, authority, freshness, and predecessor rules, derives the permitted result, writes atomically, and validates the result. This centralizes deterministic lifecycle mechanics without moving durable truth out of Git. It adds a compatibility-sensitive executable dependency and requires careful migration, concurrency, packaging, and recovery design. Select this option.

### O4: Put lifecycle mechanics in a shared library only

A library could centralize logic for one runtime and may be a useful internal implementation boundary. It does not by itself provide a language-independent contract for humans, skills, shell automation, adapters, and CI. Treat a reusable internal library as an architecture option beneath O3, not as the public interface.

### O5: Introduce a hosted control plane or autonomous workflow runner

These approaches could provide stronger centralized authorization or end-to-end automation. They conflict with RigorLoop's Git-first, repository-contained positioning, expand availability and security concerns, and mix transition integrity with orchestration and semantic authority. Reject for this initiative.

## Recommended Direction

Choose O3: extend the existing `rigorloop` executable into the mandatory operation boundary for supported governed lifecycle transitions.

The responsibility split is:

```text
humans and agents       make semantic engineering judgments
stage and review skills define stage-specific reasoning and artifacts
workflow                decides routing and bounded continuation
RigorLoop CLI           interprets and enforces valid governed operations
repository artifacts    preserve decisions, contracts, findings, and evidence
Git                     preserves durable history and integration state
```

The public interface should be operation-oriented. A caller requests actions such as inspecting effective status, obtaining stage context, recording review or validation evidence, recording a finding disposition, settling the matching artifact, or starting or completing an eligible milestone. The CLI derives any lifecycle mutation; callers do not select arbitrary target states.

The first release should cover six capability groups:

1. Read-only discovery, effective status, blockers, artifact and milestone identity, allowed operations, and shared human/machine output.
2. Minimal operation-specific context that binds the exact change, target, approved inputs, review round, authorized output, blockers, and permitted recording action.
3. Registration of supplied semantic review outcomes, findings, review rounds, validation evidence, and the exact artifact revisions to which they apply.
4. Authorized artifact settlement and implementation-milestone transitions after evidence, freshness, ordering, and authority checks pass.
5. Local and CI repository validation for schema compatibility, lifecycle combinations, evidence references, stale approvals, and detectable unsupported mutations.
6. Explicit migration, stale-operation, repair, and refusal behavior for supported legacy or damaged states.

Every mutation should behave as one all-or-nothing transaction: read and validate current state, validate the operation and its evidence basis, compute the result, write affected files atomically, validate the resulting repository, and return a deterministic result. Rejection should include a stable code, attempted operation, blocking invariant, relevant identities, effective state, and deterministically known corrective operations without inventing a semantic resolution.

Recording, settlement, and continuation remain separate authority boundaries. Recording an approved review judgment does not automatically revise the reviewed artifact, settle unrelated artifacts, choose the next stage, or run it. Workflow may request continuation through the CLI, but the CLI only determines whether the requested structural operation is valid.

Portable skills remain usable without a governed change record. The CLI becomes mandatory only when a caller mutates governed lifecycle state under the supported RigorLoop contract.

## Expected Behavior Changes

- Published governed skills and supported automation stop directly assigning lifecycle fields and instead request supported CLI operations.
- Humans and agents can inspect recorded state and effective state separately; stale evidence can make an apparently settled raw state effectively blocked.
- Known-invalid settlement, evidence registration, and milestone operations are rejected before mutation.
- Review and proof evidence is bound to exact artifact identity and revision, so later edits invalidate reliance where the specified lifecycle rules require it.
- A stale caller cannot silently overwrite lifecycle state that changed after its context was calculated.
- Accepted and rejected operations produce stable, versioned machine results and equivalent human explanations from the same interpreter.
- A fresh supported checkout reconstructs effective state without conversation history, external databases, daemons, or uncommitted caches.
- CI can validate governed-state integrity non-interactively and detect unsupported or inconsistent state where repository evidence permits.
- Governed agent invocations load less deterministic lifecycle procedure and receive smaller operation-specific context, while semantic review and engineering guidance remains intact.
- Portable skill invocations that do not mutate governed state remain independent of the CLI lifecycle contract.

## Architecture Impact

Architecture assessment is required. The proposal changes a long-lived cross-component boundary among the CLI package, lifecycle schemas and validators, workflow routing, stage and review skills, generated adapter packages, CI, and change-local artifacts.

The downstream architecture should decide:

- whether lifecycle interpretation is implemented as a reusable library beneath the CLI and how existing Python validators and Node CLI code converge without creating competing authorities;
- whether `change.yaml` remains primarily a snapshot, gains an event or operation ledger, or uses a bounded hybrid;
- how artifact revision identity, evidence freshness, lifecycle revision, optimistic concurrency, retries, and crash-safe multi-file writes work;
- how repository schema versions, CLI versions, published skill packages, generated adapters, and migration commands declare compatibility;
- how unsupported manual mutation is detected without claiming a cryptographic security perimeter;
- how branch divergence and merge conflicts interact with locally atomic operations;
- where workflow routing ends and CLI transition authorization begins;
- how controlled repair remains narrow and auditable without becoming an arbitrary state setter.

The architecture must preserve repository-contained durable truth. Machine-local locks, temporary files, or caches may support safe execution, but they cannot be required to reconstruct governed status after a fresh checkout.

## Testing and Verification Strategy

Build a transition-conformance suite before making mutation mandatory. Fixtures should cover every supported valid transition and known invalid predecessor, including unresolved findings, stale evidence, missing artifacts, wrong artifact identity, incompatible review rounds, repeated operations, conflicting retries, out-of-order milestones, stale lifecycle revisions, unsupported schema versions, legacy migration, and unsafe repair requests.

Read-only interpretation should be implemented and compared with current workflow and validator behavior before guarded mutation is enabled. Human and machine output should be generated from one internal result and checked for equivalent state, blocker, identity, and allowed-operation facts.

Determinism tests should apply the same operation to identical fixtures and compare lifecycle diffs and structured results, excluding only documented provenance fields. Fault-injection tests should interrupt each mutating write boundary and prove that failure or rejection leaves no partial governed transition. Fresh-checkout tests should reconstruct effective state without prior machine or agent state.

Integration proof should cover representative Codex, Claude Code, and opencode packages consuming the same structured context and registering equivalent governed results. CI proof should exercise the non-interactive validation command against valid, invalid, stale, manually corrupted, and version-incompatible fixtures.

Token measurement should establish pre-migration baselines for representative governed stage invocations, then separately report removed mechanical instructions, retained semantic guidance, CLI context returned to the agent, and total loaded tokens. The provisional objective is at least a 30% reduction in workflow-mechanics tokens without reducing stage-specific semantic guidance or review rigor; proposal review and downstream specification may revise the threshold if the measured baseline shows it is unsuitable.

## Rollout and Rollback

Roll out in bounded slices:

1. Specify the transition matrix, effective-state model, identities, authority boundaries, compatibility contract, threat model, and concurrency model.
2. Deliver read-only discovery, status, context, diagnostics, and validation; compare them with current behavior without changing mutation ownership.
3. Add narrowly scoped guarded recording, settlement, milestone, migration, and repair operations with conformance and fault-injection proof.
4. Migrate governed skills and generated adapter packages to request CLI context and operations; measure token and behavior changes.
5. Enable CI checks and declare direct governed lifecycle mutation unsupported after compatible tooling and migration paths exist.

Each slice should remain reversible. Before mandatory enforcement, rollback means disabling the new operation path and retaining the current validated direct-edit workflow. After enforcement, rollback requires a coordinated compatibility release that restores the prior supported contract; it must not instruct users to bypass the boundary with undocumented YAML edits. Repository schema migration must be explicit, versioned, and reversible where data preservation permits.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Lifecycle meaning becomes hidden in executable code | Keep readable durable state and evidence, publish transition documentation and conformance fixtures, and make status explain its supporting artifacts and rules. |
| The command surface becomes a large field-level workflow API | Expose a small semantic operation vocabulary, prohibit an arbitrary state setter, and add operations only for demonstrated lifecycle needs. |
| CLI, repository schema, skills, and adapters diverge | Version machine contracts, declare compatibility, reject unsupported combinations clearly, and provide explicit migrations. |
| Users or agents continue direct edits | Remove such instructions from governed skills, validate in CI, detect unsupported transitions where evidence allows, and provide supported recovery operations. |
| Token savings merely shift complexity into verbose CLI output | Return minimal operation-specific context, retain expandable diagnostics, and measure total loaded procedure plus returned context. |
| Mandatory installation creates adoption friction | Extend the existing packaged CLI, provide deterministic version/setup diagnostics, and keep portable-mode use independent. |
| Mechanical validity is mistaken for semantic correctness | Document that the CLI validates structure, identity, evidence, and authority—not engineering truth—and never infer approval from test success. |
| Atomic local writes are mistaken for distributed transactions | State the supported concurrency model, reject stale local operations, and rely on Git and protected integration workflows for branch-level conflicts. |
| Existing validator and workflow logic competes with the CLI | Define one canonical lifecycle library or explicit authority hierarchy in architecture, then migrate callers incrementally with parity fixtures. |
| Repair becomes an unrestricted bypass | Limit repair to named recoverable conditions, require explicit evidence and diagnostics, and refuse unknown or unsafe states. |

## Open Questions

1. How is the active change selected when several governed changes exist?
2. What exact public operation and command vocabulary is small enough for the first release?
3. How are human and machine output schemas versioned and kept equivalent?
4. How is caller role or operation authority represented, and which controls depend on trusted CI or branch protection?
5. Should durable lifecycle state be snapshot-based, event-based, or a bounded hybrid?
6. Which artifact hashes, Git identities, and lifecycle revisions bind context and evidence?
7. Which mutations invalidate review, settlement, milestone, explanation, or verification evidence?
8. What optimistic-concurrency and branch-divergence behavior is supported?
9. How do legacy repositories migrate, and what narrow emergency repairs are safe?
10. How are CLI, repository schema, canonical skills, generated adapter archives, and CI versions coordinated?
11. Which status facts belong in minimal agent context and which remain detailed diagnostics?
12. What is the exact enforcement boundary between CLI transition validity and workflow routing?
13. How should existing Node CLI code and Python lifecycle validation converge on one interpretation without a disruptive rewrite?

## Decision Log

| Decision | Outcome | Rationale |
| --- | --- | --- |
| Proposal identity | `RL-PROP-CLI-001` | Preserves the requested stable proposal identifier. |
| Product direction | Use the existing local `rigorloop` CLI as the governed transition boundary | Reuses the established language-independent interface for humans, agents, adapters, and CI. |
| Durable truth | Keep governed state and evidence in Git-tracked repository artifacts | Preserves inspectability, reconstruction, and project vision. |
| Public mutation model | Semantic operations only; no unrestricted field or target-state setter | Lets the CLI derive valid transitions and enforce narrow authority. |
| First-release boundary | Status/context, recording, settlement, milestones, validation, migration, and repair | Addresses lifecycle integrity while excluding autonomous orchestration and PR execution. |
| Semantic authority | Remains with humans, agents, stage skills, and review skills | Structural enforcement cannot establish engineering truth. |
| Workflow authority | Routing and bounded continuation remain workflow responsibilities | Prevents the CLI from becoming an autonomous workflow runner. |
| Architecture disposition | Architecture assessment required | The change affects cross-component, compatibility, persistence, concurrency, and trust boundaries. |
| Token objective | Measure a provisional 30% reduction in lifecycle-mechanics tokens | Makes the secondary objective falsifiable without sacrificing semantic guidance. |

## Next Artifacts

- Independent proposal review focused on product boundary, scope, relationship to the accepted scaffolding CLI direction, trust claims, migration, and readiness for specification.
- Feature specification defining observable operations, state interpretation, error and output contracts, compatibility, migration, and acceptance criteria.
- Architecture assessment and likely architecture update or ADR covering the canonical lifecycle engine, transaction model, persistence shape, concurrency, packaging, and component ownership.
- Execution plan and transition-focused test specification after proposal, spec, and architecture settlement.

## Follow-on Artifacts

None yet

## Readiness

The proposal is ready for independent `proposal-review`. It is not accepted, specification-ready, architecture-approved, implementation-ready, verified, or PR-ready.

Proposal review should specifically challenge whether the first-release scope is still too broad, whether migration and repair are inseparable from mandatory enforcement, whether the existing CLI/package boundary can host the transition engine safely, and whether the token objective is measurable without distorting semantic guidance.
