# ADR-20260828: Consolidated Review Package Topology

## Owning change record

`docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml`

## Context

RigorLoop stores artifact lifecycle state in one change-local `change.yaml`, uses the governed lifecycle CLI as the mechanical transition boundary, and keeps workflow routing separate from authoring and review judgment. Its pre-implementation topology nevertheless assigns separate progression reviews to specification, architecture, plan, and test specification even though each pair forms one engineering decision.

The approved consolidated-review-gates specification requires atomic Design Review and Delivery Review authority, precise finding ownership, deterministic aggregate package identity, no contributor-maintained per-document hashes, and one complete release cutover that retires old progression rather than maintaining two runtime mechanisms. The design must preserve ADR-20260729's sole mutable state owner, ADR-20260824's lifecycle transaction boundary, ADR-20260825's workflow-owned correction routing and artifact-collision rules, and the generated-skill distribution boundary.

## Decision

### Release cutover

Do not add a top-level `review_topology` field, activation manifest, legacy baseline, or runtime topology interpreter. While this change is implemented, the existing workflow remains authoritative. The reviewed release revision becomes one cutover that replaces the old progression graph and entrypoints with the consolidated workflow.

Release validation blocks cutover while a nonterminal governed change still depends on old progression or while canonical guidance, skills, schemas, CLI behavior, validators, fixtures, generated packages, or release metadata disagree. Historical review records remain readable but do not become package authority. Before any consolidated change begins, rollback is a normal reviewed code revert; after adoption begins, recovery is a forward correction or separately approved migration rather than destructive evidence rewriting.

`rigorloop new-change` therefore requires no topology selection and writes no topology metadata. The implementing change completes through the pre-cutover workflow; later changes use the consolidated workflow because only one stage graph is shipped after cutover.

### Stage-owned artifact editing

Keep artifact edit authority stage-based. `architecture` owns architecture documents, ADRs, and architecture authoring evidence; `spec` owns specifications; `plan` owns execution plans; `test-spec` owns proof-design artifacts; review skills own only their review findings and evidence; and `workflow` owns routing. This change introduces no cross-change canonical-path succession or current-revision ownership model. Existing artifact-path collision and guarded-withdrawal behavior remains unchanged.

This decision supersedes the earlier automatic canonical revision-succession direction recorded during development of this ADR. That direction was withdrawn because the current workflow has no required shared-path overwrite case and stage-owned editing is sufficient for the consolidated review topology.

### Package membership and identity

Keep component artifacts under `artifact_states` with their existing authoring owners. Add `review_packages.design` and `review_packages.delivery` as package-authority projections in the same `change.yaml`.

The design member set is derived in this order from current registered artifacts: primary architecture, primary specification, then every current ADR ordered by artifact ID. Registering an ADR is the architecture owner's explicit applicability decision. The delivery member set is primary plan followed by primary test specification. Unknown, missing, duplicate, unsafe, or extra required roles fail before review context is issued.

The lifecycle engine calculates `review-package-sha256-v1` from canonical UTF-8 JSON containing the algorithm version, package kind, ordered member records, and upstream binding. Each transient member record contains its artifact ID, normalized repository-relative path, and current SHA-256 content identity. The design upstream binding is the current accepted Proposal Review ID. The delivery upstream binding is the current approved design aggregate revision.

Only the package kind, ordered member artifact IDs, upstream binding, and aggregate package revision are persisted in package lifecycle and review records. Per-member paths and content hashes are recalculated from registered artifacts and are not duplicated as durable package fields. Any member-byte, membership, package-kind, or upstream-binding change produces a different aggregate revision and makes prior package authority stale.

### Package lifecycle and CLI boundary

Package authority lives only in `review_packages`; component artifact state remains inspectable authoring state and never independently authorizes progression. Each package projection carries a closed state, current aggregate revision, member IDs, upstream binding, latest review identity and outcome, correction targets, and evidence path. Design approval authorizes plan and test-specification authoring. Delivery approval authorizes implementation.

Extend the existing `rigorloop lifecycle` family rather than adding another top-level command. `context design-review` and `context delivery-review` return the complete current package context. Two new semantic mutation operations, `record-package-review` and `settle-review-package`, use the existing lifecycle revision, pure evaluator, lock, recovery, and single-`change.yaml` transaction adapter.

`record-package-review` validates package kind, stage authority, current upstream binding, recalculated aggregate revision, evidence identity, review round, outcome, findings, affected artifact IDs, and correction targets. `settle-review-package` rereads and recalculates the same inputs, settles the entire package or none of it, and grants authority only for `approved`. Exact duplicate requests are idempotent; stale requests fail unchanged. Non-approved outcomes remain visible and grant no progression. Workflow chooses all correction and continuation routes; the CLI only validates and persists closed selected operations.

### Normal workflow progression

Add one workflow-owned `advance-stage` semantic operation inside the existing `rigorloop lifecycle` family. It records a normal lifecycle transition after the current authoring, review, or other governed stage has completed. It is not a generic status setter.

The request names the expected lifecycle revision, current stage, requested next stage, and `stage_authority: workflow`. The lifecycle engine admits only an edge in the single closed stage graph and verifies the exact completion authority for the source stage. Authoring transitions require the current registered artifact revision and authoring evidence. Review transitions require the current settled artifact or package authority. Milestone transitions continue using their existing milestone-specific operations. Corrections continue using `route-correction` and `return-correction` rather than pretending to be forward progress.

On success, the operation atomically synchronizes `workflow_state.current_stage`, `workflow_state.next_stage`, and every active automation-stage projection governed by the same transition. It does not alter artifact or package judgment, invent semantic evidence, or modify another stage's content. The existing registered completion facts are sufficient; normal advancement adds no separate completion document, per-document hash, handoff receipt, or reservation.

Settlement and advancement remain separate. `settle-artifact` and `settle-review-package` record review authority but never continue workflow by themselves. A direct or review-only invocation therefore remains isolated after settlement. Workflow-managed execution may invoke `advance-stage` after settlement or authoring completion when continuation is authorized. An invalid edge, missing or stale completion authority, unresolved blocker, stale lifecycle revision, or contradictory automation projection fails unchanged. An exact replay against the resulting state reports `already-recorded` without duplicating transition state.

Read-only context and status expose `advance-stage` only when the current source stage is complete and one requested forward edge can be validated. Cutover replaces the old graph with this consolidated graph; it does not leave either workflow dependent on direct `change.yaml` routing edits.

### Review and distribution boundaries

Add `design-review` and `delivery-review` as distinct canonical review skills because each owns a recurring formal decision and evidence contract. They may share mapped review-method references and structural assets, but each `SKILL.md` owns its package-specific inputs, criteria, findings, settlement, stops, and claim limits. At cutover, remove `spec-review`, `architecture-review`, `plan-review`, and `test-spec-review` as public progression entrypoints; do not retain them as aliases that can manufacture package approval.

The `proposal` template and skill add one embedded Feasibility section, and `proposal-review` evaluates it without creating another artifact or gate. Workflow routes through the consolidated graph after cutover. Code Review, Explain Change, Verify, PR, independent-review evidence, and review-resolution retain their current owners and consume current package authority.

Canonical skills remain the only authored skill source. Adapter generation, manifests, packed archives, and release validation carry the two new skills and omit the four retired progression skills at cutover. No target-runtime execution, external service, database, or new production dependency is introduced.

## Alternatives considered

- Persist every member hash: rejected because the engine can recalculate member identities and duplicated hashes expand stale bookkeeping.
- Settle each component independently: rejected because sequential settlement exposes partial authority.
- Infer membership from review prose: rejected because prose cannot provide a closed deterministic input.
- Add a package-manifest document per review: rejected because it creates another authored artifact and lifecycle owner.
- Add new top-level CLI commands: rejected because package review belongs inside the existing lifecycle transaction boundary.
- Let settlement advance workflow automatically: rejected because it would collapse review judgment with workflow continuation and violate isolated manual review behavior.
- Add a generic status setter or keep direct routing edits: rejected because arbitrary field mutation would bypass the closed stage graph, completion authority, optimistic concurrency, and synchronized automation projections.
- Add cross-change canonical revision ownership or automatic path succession: rejected because the current workflow has no required shared-path overwrite case and existing stage ownership plus artifact-collision behavior is sufficient.
- Migrate active legacy changes automatically: rejected because historical individual approvals do not prove coherent package judgment.

## Consequences

- Contributors keep separate artifacts without maintaining package-member hashes.
- One aggregate revision makes freshness compact while preserving exact recalculation and artifact-level traceability.
- Package review adds schema, engine, request, status, fixture, and validator work but reuses the existing single-file transaction boundary.
- Normal continuation gains one explicit workflow-owned operation; this adds a closed transition graph and fixtures while preventing completed artifacts from leaving stale workflow routing.
- Any byte change causes rereview in the first slice, including editorial changes.
- Explicit ADR registration makes applicability deterministic but reviewers must still detect omitted relevant ADRs semantically.
- Old review skills remain authoritative only while this implementing change is in progress and are retired at cutover.
- The implementing change reaches closeout through the pre-cutover gate sequence.

## Follow-up

- Run `architecture-review` on this revised ADR before relying on its package topology.
- Plan package-review CLI operations, normal stage advancement, skills, routing, validators, generated adapters, and the atomic release cutover.
- Create the matching boundary-first proof map before implementation, including unknown-vocabulary, aggregate identity, stale input, atomic settlement, isolated settlement, authorized stage advancement, invalid-edge rejection, synchronized automation projection, correction routing, legacy-dependent cutover blocking, pre-adoption revert, and generated-parity cases.
