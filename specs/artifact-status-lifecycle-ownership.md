# Artifact Status Lifecycle Ownership

## Status
- approved

## Related proposal

- [Artifact status lifecycle ownership](../docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md)

## Goal and context

This spec defines the repository-visible contract for keeping top-level workflow artifacts truthful about their lifecycle state after review, adoption, activation, deprecation, supersession, archival, or abandonment.

The repository already fixed stale lifecycle bookkeeping for execution plans. The same drift still exists across proposals, feature specs, test specs, architecture documents, and ADRs. Artifacts that the repository already depends on can still advertise `draft`, `reviewed`, `complete`, or `proposed`, and forward-looking readiness text can remain stale long after review or merge. This spec defines the allowed status model, transition ownership, closeout pattern, verification policy, and first enforcement expectations needed to make those artifacts trustworthy again without adding a second central registry.

## Glossary

- `in-scope artifact`: a top-level tracked workflow artifact covered by this spec: proposal, feature spec, test spec, architecture document, or ADR.
- `active-work state`: a status that means the artifact is still being authored, reviewed, or actively used as a live proof-planning surface.
- `settlement`: the point at which an artifact's review or adoption outcome becomes durable enough to rely on as current guidance.
- `settled current guidance`: an artifact whose review outcome is complete and whose content may still be relied on for current work.
- `historical closed artifact`: an artifact that remains useful for history, audit, or traceability but is no longer current authoritative guidance.
- `terminal or historical state`: a no-longer-current artifact state such as `rejected`, `abandoned`, `superseded`, or `archived`; related artifact classes outside this spec may use analogous terminal states such as `done`.
- `closeout surface`: explicit tracked text that records what actually happened after an artifact settled, such as `Follow-on artifacts`, `Closeout`, or equivalent per-artifact wording.
- `authoritative artifact for the changed area`: a spec, architecture document, test spec, or active plan that governs the behavior, boundary, proof surface, or execution state touched by the current change.
- `pre-PR handoff surfaces`: the tracked surfaces available before final PR text exists, including `docs/changes/<change-id>/change.yaml`, the explain-change artifact, the active plan, and touched, referenced, generated, or authoritative artifacts for the changed area.
- `stale artifact state`: tracked status or closeout text that no longer matches how the repository is actually relying on the artifact.
- `replacement pointer`: explicit metadata or equivalent labeled text that identifies the authoritative artifact that superseded an older one.

## Examples first

### Example E1: accepted proposal remains current direction

Given proposal review accepts a workflow-direction proposal
When the repository starts spec work from that proposal
Then the proposal status becomes `accepted`, it no longer reads as "ready for proposal-review", it may remain current direction rather than historical archive, and it does not require immediate closeout solely because it settled.

### Example E2: approved spec remains current guidance

Given a feature spec passes `spec-review`
When later implementation and verification rely on it
Then the spec status becomes `approved`, and the artifact may remain authoritative current guidance without being rewritten to sound historical.

### Example E3: superseded architecture document names its replacement

Given a newer architecture document replaces an older system-shape document
When the older document is closed out
Then the older document status becomes `superseded` and it explicitly identifies the replacement artifact instead of being left ambiguous or merely marked `archived`.

### Example E4: verify runs before PR text exists

Given a contributor changes workflow-governance artifacts and has not yet written a draft PR body
When `verify` runs
Then it checks the pre-PR handoff surfaces rather than blocking on missing PR text, and final PR text must not add new authoritative artifact references without re-running `verify`.

### Example E5: unrelated stale baseline artifact warns only

Given an unrelated older proposal elsewhere in the repository still has stale readiness wording
When the current change does not touch it, reference it, or rely on it as authoritative guidance
Then `verify` reports it as baseline debt warning rather than blocking the unrelated improvement.

### Example E6: test spec moves from active proof surface to archive

Given a test spec is the active proof-planning surface during implementation
When the implementation and verification are complete and the test spec is no longer an active planning surface
Then the test spec transitions from `active` to `archived`, unless a newer test spec supersedes it or the work is abandoned.

## Requirements

R1. This spec applies to the following top-level tracked workflow artifacts:
- proposals under `docs/proposals/`
- feature specs under `specs/` that define behavior contracts
- test specs under `specs/*.test.md`
- architecture documents under `docs/architecture/`
- ADRs under `docs/adr/`

R1a. This spec MUST NOT redefine the already-approved plan lifecycle model, and it MUST NOT promote change-local artifacts such as `docs/changes/*`, explain-change artifacts, or review-resolution artifacts into top-level authoritative lifecycle state solely through this change.

R2. Each in-scope artifact MUST keep its lifecycle status inside the artifact itself as tracked source of truth. Git branch state, PR state, merge state, or chat-only review outcomes MUST NOT be treated as sufficient replacements for artifact-local lifecycle state.

R3. `specs/rigorloop-workflow.md` MUST define the repository-wide invariants for artifact lifecycle ownership and MUST include a compact artifact lifecycle summary table.

R3a. The summary table defined by `R3` MUST include, at minimum, the columns:
- `Artifact`
- `Required for`
- `Authoring skill`
- `Review skill`
- `Settlement states`
- `Closeout or terminal states`

R3b. The compact summary table defined by `R3` MUST cover, at minimum, the following rows:
- Proposal: required for non-trivial direction choice; authoring skill `proposal`; review skill `proposal-review`; settlement states `accepted`; closeout or terminal states `rejected`, `abandoned`, `superseded`, `archived`
- Spec: required for behavior changes; authoring skill `spec`; review skill `spec-review`; settlement states `approved`; closeout or terminal states `abandoned`, `superseded`, `archived`
- Architecture: required for boundary or system-shape changes; authoring skill `architecture`; review skill `architecture-review`; settlement states `approved`; closeout or terminal states `abandoned`, `superseded`, `archived`
- Test spec: required for behavior proof; authoring skill `test-spec`; review surface repository-defined; settlement states `active`; closeout or terminal states `abandoned`, `superseded`, `archived`
- ADR: required for long-lived design decisions; authoring flow ADR-specific; review surface `architecture-review` when relevant; settlement states `accepted`, `active`; closeout or terminal states `deprecated`, `superseded`, `archived`, `abandoned`

R3c. Per-artifact detail beyond the compact summary table MUST be delegated to canonical template, example, or skill surfaces rather than duplicated in full inside `specs/rigorloop-workflow.md`.

R4. The durable status vocabulary for proposals MUST be limited to:
- `draft`
- `under review`
- `accepted`
- `rejected`
- `abandoned`
- `superseded`
- `archived`

R5. The durable status vocabulary for feature specs MUST be limited to:
- `draft`
- `approved`
- `abandoned`
- `superseded`
- `archived`

R5a. The durable status vocabulary for architecture documents MUST be limited to:
- `draft`
- `approved`
- `abandoned`
- `superseded`
- `archived`

R5b. The durable status vocabulary for ADRs MUST be limited to:
- `draft`
- `proposed`
- `accepted`
- `active`
- `deprecated`
- `superseded`
- `archived`
- `abandoned`

R5c. The durable status vocabulary for test specs MUST be limited to:
- `draft`
- `active`
- `abandoned`
- `superseded`
- `archived`

R6. `reviewed` MUST be treated as a transitional review event, not a long-lived relied-on artifact state, for proposals, feature specs, test specs, and architecture documents.

R6a. `complete` MUST NOT remain the long-lived status of a settled test spec after this contract is adopted. A settled test spec MUST instead be classified as:
- `active` while it remains the current proof-planning surface for live implementation or review work;
- `archived` when it remains useful history but is no longer the active proof-planning surface;
- `superseded` when a newer test spec replaces it; or
- `abandoned` when the governed work stops before completion.

R7. Settled current guidance and historical closed artifacts MUST remain distinct concepts.

R7a. `accepted`, `approved`, and `active` MAY still be relied on as current guidance for the repository when the artifact remains operative.

R7b. `deprecated`, `superseded`, `archived`, `rejected`, and `abandoned` MUST be treated as no longer current authoritative guidance.

R7c. Settlement MUST NOT be treated as immediate closeout.

R7d. Artifacts in settled current states such as `accepted`, `approved`, and `active` MUST record the decision metadata required by their class contract, but they MUST NOT be required to add immediate `Closeout` or `Follow-on artifacts` sections solely because settlement occurred.

R7e. Distinct closeout surfaces become required when an artifact enters a terminal or historical state, or earlier only when the detailed class contract explicitly requires recording actual downstream artifacts before terminal closeout.

R8. Lifecycle transition ownership for in-scope artifacts MUST be explicit and MUST follow this model:
- `proposal` authors new proposals in `draft`
- `proposal-review` determines whether the proposal is accepted, rejected, or returned for revision
- when chat or review output establishes acceptance or rejection but the tracked proposal is still stale, `proposal-review` or the immediate next depending stage MUST normalize the tracked proposal before that next stage may rely on it
- `spec` authors feature specs in `draft`
- `spec-review` determines whether a relied-on feature spec is ready to normalize to `approved`
- when the tracked feature spec is still stale after review, `spec-review` or the immediate next depending stage MUST normalize the tracked spec before implementation, planning, or test-spec work relies on it
- `architecture` authors design artifacts in `draft`
- `architecture-review` or equivalent accepted design closeout normalizes relied-on architecture artifacts to `approved`
- `test-spec` authors new test specs in `draft`
- once implementation or review is actively using a test spec as the governing proof surface, the tracked test spec MUST normalize to `active`
- once a test spec is no longer the active proof-planning surface, the closeout change that settles the governed work MUST normalize it to `archived`, `superseded`, or `abandoned`
- ADRs MAY be drafted by contributors or agents in `draft` or `proposed`, but durable ADR transitions such as `accepted`, `active`, `deprecated`, `superseded`, `archived`, and `abandoned` MUST be owned by a maintainer, architecture owner, design authority, or explicitly delegated role
- later replacement work owns `superseded` transitions for the older artifacts it replaces

R9. In-scope artifact guidance MUST distinguish planned next steps from actual settled outcomes.

R9a. `Next artifacts` MUST remain the planned next steps while an artifact is still active.

R9b. Once an artifact reaches a settled state, the artifact MUST preserve its earlier `Next artifacts` history.

R9c. A distinct `Closeout` or `Follow-on artifacts` surface becomes required when an artifact enters a terminal or historical state, or earlier when the detailed class contract explicitly requires recording actual downstream artifacts before terminal closeout.

R9d. `Follow-on artifacts` MUST record actual downstream artifacts, replacement, or final disposition. It MUST NOT record merely expected or planned downstream work.

R9e. A `Follow-on artifacts` section MAY be omitted until actual follow-on artifacts exist. If the section is present before any follow-on artifacts exist, it MUST explicitly say `None yet`.

R9f. A settled artifact MUST NOT keep readiness wording that still advertises earlier pending stages such as `proposal-review`, `spec-review`, implementation, or PR preparation when those are no longer the true next step.

R10. `superseded` and `archived` MUST have distinct meanings.

R10a. `superseded` MUST be reserved for an artifact that has been explicitly replaced by a newer authoritative artifact.

R10b. A superseded artifact MUST include an explicit replacement pointer through `superseded_by` metadata or equivalent labeled text inside the artifact.

R10c. A superseded artifact SHOULD also record the supersession date and reason through `superseded_at` and `superseded_reason` metadata or equivalent labeled text.

R10d. `archived` MUST be reserved for an artifact that is no longer current but remains useful for history, audit, learning, or traceability and has no direct replacement requirement.

R10e. `archived` MUST NOT be used when the more precise state is `deprecated`, `rejected`, `abandoned`, `done`, or `superseded`.

R11. `verify` MUST block on stale or inconsistent in-scope artifacts that are touched, referenced, generated, or authoritative for the changed area.

R11a. `verify` MUST report unrelated stale baseline artifacts as warnings rather than blockers.

R11b. Baseline documentation debt MUST NOT block unrelated improvements, but no change may rely on a stale authoritative artifact.

R11c. For this spec, artifacts related to the current change include at minimum:
- artifacts changed in the PR
- artifacts linked from `docs/changes/<change-id>/change.yaml`
- artifacts referenced by the PR body when a draft PR body already exists
- generated outputs that should match source
- specs governing changed behavior
- architecture documents governing changed boundaries
- test specs governing changed tests
- plans governing active implementation

R11d. Before final PR text exists, `verify` MUST use the pre-PR handoff surfaces instead of requiring PR-body references.

R11e. Final PR text MUST NOT introduce new authoritative artifact references without re-running `verify`.

R12. At minimum, stale or inconsistent artifact state under this spec includes:
- a proposal, feature spec, architecture document, or ADR that the repository is already relying on as settled guidance while its tracked status still says `draft`, `under review`, `reviewed`, or `proposed`
- a test spec that the repository is already relying on as settled historical evidence while its tracked status still says `complete`
- a settled artifact whose status and readiness text disagree about whether review, implementation, or PR preparation is still pending
- an artifact in a terminal or historical state that still lacks the required `Closeout` or `Follow-on artifacts` surface defined by its detailed contract surface
- a `Follow-on artifacts` section that is present before actual follow-on artifacts exist but is empty or does not explicitly say `None yet`
- a superseded artifact that lacks an explicit replacement pointer
- a generated output surface being treated as the authored source of truth for lifecycle state

R13. The first enforcement step for this contract MUST include executable verification, not documentation alone.

R13a. The first enforcement step MUST include all of the following in the same change:
- documentation that defines the contract
- a minimal structural validator
- fixtures that prove the validator behavior
- `verify` integration that runs the validator
- CI wiring that runs the same repo-owned verification path

R13aa. First-release identifier validation applies only to lifecycle-managed artifact classes whose contracts define identifiers: skills, proposals, top-level specs, ADRs, and change metadata. Other Markdown files MUST NOT be required to carry artifact identifiers unless they explicitly opt in with `artifact_id` or an equivalent future contract field.

R13b. The minimal structural validator required by `R13a` MUST block only objective structural defects, including at minimum:
- invalid status vocabulary for the artifact class
- missing required metadata or required sections defined by the detailed contract surface for that artifact class
- empty required sections
- placeholder text such as `TODO`, `TBD`, or `lorem ipsum`
- duplicate artifact identifiers where uniqueness is required by the class contract
- invalid normalized naming where the class contract requires it
- generated folders or generated outputs being treated as authored source of truth
- objective contradictions between status, readiness, and required closeout surfaces

R13c. Subjective writing-quality or judgment-based lifecycle issues SHOULD remain review comments until a later explicitly approved enforcement phase defines stronger automation.

R14. The canonical template, example, and skill surfaces for the in-scope artifact classes MUST be updated so contributors can discover the lifecycle contract without reading chat history.

R14a. Detailed per-artifact guidance MUST define, for that artifact class:
- the allowed status vocabulary
- who owns the main transitions
- which forward-looking and closeout sections are required
- how `verify` should treat stale status or closeout drift for that artifact type

R14b. Canonical authored guidance MUST remain the source of truth. Generated compatibility output such as `.codex/skills/` MUST remain derived and MUST NOT be hand-edited as the authoritative lifecycle surface.

R15. Adoption of this contract MUST normalize already-known stale relied-on artifacts in scope rather than leaving the repository to depend on contradictory status state.

R15a. At minimum, migration for relied-on or touched artifacts MUST normalize:
- proposals left in `draft` or `under review` after acceptance or rejection
- feature specs or architecture documents left in `reviewed`
- test specs left in long-lived `complete`
- ADRs left in `draft` or `proposed` after the decision is already adopted

R15b. Migration of unrelated stale baseline artifacts MAY be phased, provided `verify` reports them as warnings and the current change does not rely on them as authoritative guidance.

## Inputs and outputs

### Inputs

- in-scope top-level workflow artifacts under `docs/proposals/`, `specs/`, `docs/architecture/`, and `docs/adr/`
- `specs/rigorloop-workflow.md`
- canonical artifact templates, examples, and skills for the in-scope classes
- generated compatibility output when it mirrors canonical guidance
- `docs/changes/<change-id>/change.yaml`, explain-change artifacts, active plans, and draft PR text when those surfaces reference in-scope artifacts

### Outputs

- a repository-wide artifact lifecycle summary in `specs/rigorloop-workflow.md`
- per-artifact guidance that defines allowed statuses, transition ownership, and closeout structure
- in-scope artifacts whose status and readiness text reflect their real repository role
- explicit replacement pointers for superseded artifacts
- verification behavior that blocks related stale authoritative artifacts and warns on unrelated baseline debt
- executable structural validation, fixtures, and CI wiring for the first enforcement step

## State and invariants

- Artifact-local lifecycle status remains the tracked source of truth.
- Settled current guidance remains distinct from historical closed artifacts.
- `reviewed` is transient review output, not durable repository status.
- A superseded artifact identifies its replacement; an archived artifact does not require one.
- `Next artifacts` preserves active planning history; `Closeout` or `Follow-on artifacts` records what actually happened after settlement.
- `verify` blocks on stale related authoritative artifacts and warns on unrelated stale baseline debt.
- Canonical guidance remains separate from generated compatibility output.

## Error and boundary behavior

- If review acceptance exists only in chat and the tracked artifact still shows stale active-work status, the next depending stage MUST normalize the artifact before relying on it.
- If a draft PR body does not yet exist, `verify` MUST use the pre-PR handoff surfaces instead of failing solely because PR text is absent.
- If final PR text later adds a new authoritative artifact reference, the existing verify result is stale until `verify` is re-run.
- If an artifact becomes historical without a direct replacement, it may be `archived` but not `superseded`.
- If a newer artifact replaces an older one, the older artifact MUST NOT be merely `archived`; it must become `superseded` and point to the replacement.
- If the repository still contains unrelated stale baseline artifacts, the current change may proceed only when it does not rely on them as authoritative guidance and `verify` reports them as warnings.

## Compatibility and migration

- This is a contributor-visible workflow and governance change, so adoption is compatibility-sensitive.
- Adoption MUST not create a second central lifecycle registry.
- Existing relied-on artifacts with stale lifecycle states MUST be normalized as part of the migration for this contract.
- Existing test specs currently marked `complete` MUST be reclassified to `active`, `archived`, `superseded`, or `abandoned` according to their real role.
- Existing proposals, specs, architecture documents, and ADRs MUST move away from stale transitional statuses such as `draft`, `under review`, `reviewed`, or `proposed` when the repository already depends on them as settled guidance.
- Rollback, if required, is a reversal of the lifecycle-governance rule change, but truthfully corrected artifact status history SHOULD be preserved.

## Observability

- Contributors MUST be able to determine the allowed status model and transition ownership from tracked repository artifacts without reading chat history.
- Manual review MUST be able to inspect an in-scope artifact and tell whether its status, readiness text, and closeout surface agree.
- `verify` results MUST identify which related artifacts were checked, which ones blocked readiness, and which unrelated stale artifacts were reported only as warnings.
- The workflow summary and per-artifact guidance surfaces MUST make the pre-PR versus draft-PR reference rule discoverable.

## Security and privacy

- This spec MUST NOT require hidden host-local state, private PR drafts, or chat-only evidence as the source of truth for artifact lifecycle state.
- Verification and validation surfaces MUST remain repo-owned and reproducible.
- The contract MUST NOT weaken the canonical-versus-generated boundary by allowing generated artifact mirrors to become authoritative.

## Performance expectations

- The first enforcement step SHOULD remain lightweight enough for normal contributor workflows.
- Structural validation SHOULD focus on objective defects and deterministic checks rather than repository-wide subjective scoring.
- Verify-time artifact classification SHOULD remain scoped to touched, referenced, generated, or authoritative artifacts for the changed area, plus warning-only baseline reporting.

## Edge cases

EC1. A proposal may be `accepted` and still remain current direction even after a spec, plan, or implementation exists.

EC2. A feature spec or architecture document may be `approved` and remain current authoritative guidance without needing to become `archived`.

EC3. A test spec may remain `active` across multiple implementation or review passes while the change is still live work.

EC4. An artifact may be `archived` without a direct replacement when it remains useful history but no newer artifact replaced it.

EC5. An artifact that is explicitly replaced by a newer authoritative artifact must be `superseded`, not merely `archived`.

EC6. Unrelated stale baseline artifacts outside the changed area should warn without blocking, unless the current change begins to rely on them.

EC7. If a draft PR body already exists when `verify` runs, its artifact references join the verify scope; otherwise the pre-PR handoff surfaces govern.

EC8. An accepted proposal or approved spec may remain current guidance without any immediate `Follow-on artifacts` section, provided its status and readiness text are truthful and no terminal closeout has occurred.

EC9. If a `Follow-on artifacts` section appears before any actual downstream artifact exists, the section must say `None yet` rather than remaining empty.

## Non-goals

- Creating a second repository-wide artifact index like `docs/plan.md` for proposals, specs, architecture docs, or ADRs.
- Replacing artifact-local lifecycle state with GitHub-only or branch-only state.
- Rewriting every historical artifact in the repository in one migration regardless of relevance.
- Enforcing subjective artifact quality or prose style through the first structural validator.
- Redefining the plan lifecycle contract already governed by `specs/plan-index-lifecycle-ownership.md`.
- Promoting change-local artifacts such as `docs/changes/*`, explain-change artifacts, or review-resolution artifacts into top-level authoritative lifecycle state through this spec alone.

## Acceptance criteria

- Contributors can identify the allowed statuses, transition owners, and closeout expectations for proposals, feature specs, test specs, architecture documents, and ADRs from tracked repository artifacts.
- The repository no longer relies on `reviewed` as a durable status for proposals, feature specs, test specs, or architecture documents.
- The repository no longer relies on long-lived `complete` test-spec status after adoption of this contract.
- Settled current guidance remains distinguishable from historical closed artifacts.
- Settlement does not force immediate closeout for `accepted`, `approved`, or `active` artifacts, while terminal or historical artifacts carry the required closeout surfaces.
- Superseded artifacts identify their replacements, while archived artifacts do not require replacement pointers.
- `verify` blocks on stale or inconsistent related authoritative artifacts and warns on unrelated stale baseline artifacts.
- The first enforcement step includes documentation, a minimal structural validator, fixtures, `verify`, and CI wiring.
- The contract remains artifact-local and does not introduce a second lifecycle registry.

## Open questions

None.

## Readiness

This spec is approved.

Spec review is complete. The contract now governs architecture, planning, test-spec, and implementation work for this feature.

No further spec-review-stage action is pending for this artifact.
