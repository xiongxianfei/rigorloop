# Targeted recording Design Review

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: `cli` = `docs/design/cli.md`; `workflow` = `docs/design/workflow.md`. Each model combines its requirements, architecture and decisions; no separate ADR is applicable to this amendment.
- Upstream review ID: `proposal-review-r1`, recorded at `docs/changes/2026-09-07-targeted-recording-primary-cli-review-recording/reviews/proposal-review-r1.md`.
- Review ID and round: `targeted-recording-design-review`, first pass.
- Material findings: TR-DR-001.
- Correction targets: `cli`, Design authoring.
- Recording status: recorded
- Settlement status: withheld
- Open blockers: no selected governed change or formal settlement authority; the independent substantive assessment also requires the correction below.
- Immediate next stage: Design authoring owner; no automatic downstream handoff.
- Claim limitations: advisory-durable, isolated review of the two model amendments under the user's direct Design-and-review request. No lifecycle settlement, Delivery eligibility, implementation, verification, publication or release approval is established.

## Finding TR-DR-001

- Finding ID: TR-DR-001
- Severity: medium
- Location: `docs/design/cli.md`, Bounded queries and scope, and Primary result schema, diagnostics and preview (lines 193–215 in the first-pass subject).
- Evidence: The primary envelope promises stable versioned JSON, but `data.header` refers to a “status header defined above” that is described only in prose. The names and shapes of grouped counts, missing-count representation, and context registry/applicability identities are not defined. Context item `kind` and `target` also lack a closed query-specific mapping, and the exact-show item shape is not explicitly bound to the context wrapper. Consequently, independent implementations can produce incompatible schema-version-2 JSON while satisfying the current prose, particularly for a registered missing evidence/review file where count uncertainty must remain distinguishable from zero entries.
- Required outcome: Define the exact nested query contract: header and count shapes, context registry identities, item kind/target mapping, and status/show scope accounting. Specify the outcome of showing an entry whose registered containing file is missing, so absence of readable content cannot become a false target-absence claim. Preserve bounded output and storage-only meaning.
- Safe resolution path: The CLI Design author can add a compact closed schema definition and a missing-content example governed by CLI-SR-14/17. Reconcile it with existing Workflow record types without changing storage schemas or inventing readiness semantics, then submit both unchanged/changed model members for independent rereview.
- needs-decision rationale: none; this is completion of the already authorized query contract.
- Finding scope: artifact-local
- Affected artifact IDs: cli
- Owning stages: Design authoring

## Assessment basis

The package preserves the user's purpose-specific catalogue and shared engine boundary. Targeted operations accept explicit decisions; registry construction does not infer applicability. Findings remain review-scoped, blockers remain change-level, and reporter disposition differs from correction ownership. Verify failure and later Route correction can be recorded successively after completed work.

Lossless source-span construction, stale-revision checks before no-op recognition, declared decision-basis reads, batch overlap rejection, and recovery from prepared bytes form a coherent architecture. Advanced exact-byte writes retain their shared safety path. Preview reserves nothing. External-tool concurrency limits and historical contract separation remain explicit. Implementation must still prove byte preservation and safety; structural model validation cannot establish those outcomes.

The static context projections, omission disclosure, revision-bound continuation and pre-publication output budgeting are appropriate. TR-DR-001 concerns their machine contract completeness, not an objection to bounded reading or a demand for Delivery's concrete test implementation. Adoption allocation retains consuming skills/resources, supported adapters, schemas, examples and complete-interaction token measurement without silently deferring a required dependency.

Both complete model files, the complete proposal and prior Proposal Review, the user's command instructions, and applicable Constitution authority were read. Boundary method and feature-authoring guidance were consumed; the Workflow-owned model mapping deliberately replaces historical four-table serialization while retaining all eight dimensions and composed-hazard review. Two pre-existing broken historical proposal links in the Workflow inventory were not relied on to infer current state or close prior obligations. No current-code correctness or project-map inference was needed.

## Independence and authority

Actual contributors are the user, who supplied the direction and command requirements, and parent Codex agent `/root`, which authored the two amendments. Reviewer `/root/targeted_design_review` is a separately delegated agent that did not author or edit either model. It independently selected this finding and wrote this first-pass record before any correction. The author confirmed that the package remained unchanged throughout the review. This provenance is an independently conducted review, not a new role label on the author.

Recording mode is `advisory-durable`; settlement is `none`. The exact two-member package comes from the direct user request and model drafting basis. The earlier Proposal Review records approval of direction but no lifecycle settlement. No new root was explicitly selected for recording, and historical workflow context was reported unavailable due to unrelated `RL_CONTEXT_CHANGE_INVALID`; this record does not fabricate a registered package or substitute advisory evidence for formal settlement. Models and lifecycle records were not modified by the reviewer.

## Validation

- `python scripts/validate-markdown-readability.py docs/reviews/2026-09-07-targeted-recording-design-review.md`: passed.
- `git diff --no-index --check /dev/null docs/reviews/2026-09-07-targeted-recording-design-review.md`: no whitespace diagnostics; exit 1 denotes the new-file comparison.

No runtime behavior was changed or tested by this review.
