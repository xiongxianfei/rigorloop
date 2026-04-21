# Artifact Status Lifecycle Ownership

## Status
- accepted

## Problem

The repository just solved stale lifecycle state for plans, but the same failure mode still exists across other top-level workflow artifacts:

- proposals
- specs
- test specs
- architecture documents
- ADRs and closely related design artifacts

In practice, the repository recently needed a cleanup PR to normalize merged artifacts that still advertised `draft`, `reviewed`, `Proposed`, or forward-looking readiness text even though the underlying work was already accepted, approved, implemented, and merged.

That reveals a deeper workflow problem:

- status vocabularies exist, but they are scattered across skills rather than governed as one repository policy;
- the repository does not define who owns status transitions for each artifact class;
- `Readiness` and `Next artifacts` sections can remain in active-work wording after the artifact becomes historical;
- `verify` currently treats stale plan lifecycle state as blocking, but it does not yet do the same for other authoritative workflow artifacts.

As a result, artifact status metadata is not consistently trustworthy. A tracked `draft` may mean "still open," "reviewed but never normalized," or simply "nobody closed this out yet." That weakens the repository's source-of-truth order because approved specs and architecture are supposed to outrank lower-priority guidance.

## Goals

- Make status metadata on top-level workflow artifacts trustworthy again.
- Define explicit lifecycle ownership for proposal, spec, test-spec, architecture, and ADR status transitions.
- Clarify which statuses are active-work states versus stable historical states.
- Remove `reviewed` as a long-lived artifact state for authoritative direction, contract, and design artifacts.
- Clarify when active-work planning sections stop controlling interpretation and when a distinct closeout section must be added.
- Make stale artifact state visible during normal verification instead of requiring ad hoc cleanup PRs later.
- Keep the solution lightweight enough that contributors can follow it without a second registry or heavy automation layer.

## Non-goals

- Replacing artifact-local status lines with GitHub state, branch names, or PR state alone.
- Introducing a new repository-wide artifact index like `docs/plan.md` for every document type.
- Redesigning the substantive content structure of proposals, specs, test specs, or architecture docs beyond lifecycle and closeout guidance.
- Rewriting every historical artifact in the repository in the same change regardless of relevance.
- Building a large inference engine that guesses artifact state from commit history or chat transcripts.
- Making change-local artifacts such as `docs/changes/*`, `explain-change`, or `review-resolution` part of the same authoritative lifecycle model unless a later change explicitly promotes them into that role.
- Redefining the already-settled plan lifecycle model from the plan-index ownership change, except where the workflow summary needs to reference it consistently.
- Rewriting artifact history in place by erasing original `Next artifacts` intent instead of recording later closeout truth separately.

## Context

- `CONSTITUTION.md` treats approved specs and approved architecture/ADR documents as higher-priority sources of truth than workflow summaries or chat history.
- The repository already solved an analogous issue for plans by defining lifecycle ownership and making `verify` treat stale plan state as blocking.
- Proposal, spec, test-spec, and architecture skills already teach status vocabularies, but those vocabularies are not yet tied together by a repository-wide lifecycle contract.
- Current status vocabularies are already intentionally different by artifact class:
  - proposals: `draft`, `under review`, `accepted`, `rejected`, `superseded`
  - specs: `draft`, `reviewed`, `approved`, `superseded`
  - test specs: `draft`, `reviewed`, `active`, `complete`
  - architecture docs: `draft`, `reviewed`, `approved`, `superseded`
  - ADRs: `draft`, `proposed`, `accepted`, `active`, `deprecated`, `superseded`, `archived`, `abandoned`
- Those differences are not inherently bad, but without explicit ownership they drift into inconsistent meanings.
- The repository now wants `reviewed` to become a transitional review event rather than a long-lived artifact state. Long-lived states should normalize to a smaller settled set such as `approved`, `accepted`, `active`, `deprecated`, `superseded`, `archived`, `rejected`, and `abandoned`, with the allowed subset defined per artifact class.
- The recent cleanup PR proved the problem is systemic rather than isolated: multiple merged artifacts still looked pre-review or pre-implementation long after the work had landed.

## Options considered

### Option 1. Keep ad hoc cleanup as needed

Continue fixing stale statuses only when someone notices them.

- Pros:
  - no new workflow rules
  - minimal immediate effort
- Cons:
  - already failed in practice more than once
  - keeps status metadata ambiguous
  - makes cleanup reactive instead of part of normal closeout
  - weakens trust in source-of-truth ordering

### Option 2. Remove status metadata from most artifacts

Stop relying on in-document status lines and treat merge state, branch state, or PR state as the artifact lifecycle source of truth.

- Pros:
  - eliminates some document-local drift
  - reduces per-file metadata maintenance
- Cons:
  - Git or PR state cannot represent `rejected`, `superseded`, or "accepted but not yet implemented" cleanly
  - makes historical repository artifacts less self-explanatory
  - weakens offline and file-local readability
  - pushes meaning back into chat or hosting-platform state

### Option 3. Define a repository-wide artifact lifecycle ownership model

Keep status metadata inside the artifacts, but define one repository contract for:

- allowed status meanings by artifact class;
- which stage owns each transition;
- which states are active-work-only versus stable historical states;
- when distinct closeout sections must be added so settled artifacts stop reading like active work without erasing earlier planning history;
- what `verify` must treat as stale for touched, referenced, generated, and authoritative artifacts for the changed area.

- Pros:
  - solves the root cause without introducing a second source of truth
  - keeps artifacts self-describing
  - aligns with the successful plan-lifecycle fix
  - creates a clean base for later automation if desired
- Cons:
  - requires touching workflow docs, skills, templates, and verification guidance
  - requires contributors to learn a slightly more explicit closeout model

### Option 4. Add a central machine-readable status registry or aggressive automation

Create a new status registry or CI-driven automation that becomes the authoritative lifecycle source for proposals, specs, architecture, and related artifacts.

- Pros:
  - strongest machine-enforced consistency in the long term
  - easier to run broad status audits
- Cons:
  - duplicates state across artifact bodies and the registry unless document-local status is removed
  - adds significant complexity before the ownership model is stable
  - risks solving a governance problem with premature tooling

## Recommended direction

Choose Option 3.

The repository should define a single artifact lifecycle ownership model for top-level workflow artifacts, then enforce it through workflow guidance, templates, and `verify`.

`specs/rigorloop-workflow.md` should define the invariants plus a compact lifecycle summary matrix. Per-artifact details should be delegated to canonical template/example surfaces and the matching authoring/review skills, rather than bloating the workflow spec with every artifact-specific rule.

The first enforcement step must include executable verification, not documentation alone.

RigorLoop v0.1 should include a minimal structural validator that checks artifact shape, required metadata, required sections, and generated-source boundaries for the in-scope artifact classes this change formalizes.

The validator should block only objective structural defects. Subjective quality issues should remain review comments until later enforcement phases.

The core best practice is:

1. Keep status as artifact-local source of truth.
2. Define explicit transition owners by artifact class.
3. Treat `reviewed` as a transitional review event, not a long-lived artifact state.
4. Treat `draft` and `under review` as active-work states that must not linger on settled artifacts.
5. Use a smaller long-lived status family for these authoritative artifacts: `approved`, `accepted`, `active`, `superseded`, `archived`, `rejected`, and `abandoned`, with the allowed subset defined per artifact class.
6. Preserve active-work planning history rather than rewriting it in place: `Next artifacts` records planned next steps while the artifact is active, and a distinct `Closeout` or `Follow-on artifacts` section records what actually happened after acceptance, approval, or closure.
7. Make `verify` block PR readiness when stale or inconsistent artifacts are touched, referenced, generated, or authoritative for the changed area.

The workflow-spec summary should stay compact and should identify, at minimum:

| Artifact | Required for | Authoring skill | Review skill | Settlement states | Closeout / terminal states | Closeout required when |
| --- | --- | --- | --- | --- | --- | --- |
| Proposal | non-trivial direction choice | `proposal` | `proposal-review` | `accepted` | `rejected`, `abandoned`, `superseded`, `archived` | when terminal or historical disposition is known |
| Spec | behavior changes | `spec` | `spec-review` | `approved` | `abandoned`, `superseded`, `archived` | when terminal or historical disposition is known |
| Architecture | boundary or system-shape changes | `architecture` | `architecture-review` | `approved` | `abandoned`, `superseded`, `archived` | when terminal or historical disposition is known |
| Test spec | behavior proof | `test-spec` | repository-defined review gate | `active` | `abandoned`, `superseded`, `archived` | when the test spec is no longer the active proof surface |
| ADR | long-lived design decision | ADR authoring flow | `architecture-review` when relevant | `accepted`, `active` | `deprecated`, `superseded`, `archived`, `abandoned` | when the decision is explicitly replaced, retired, or intentionally left behind |

The spec should then point to the canonical detailed contract surfaces already used by the repository, such as:

- proposal and review skills for proposal-state details
- `specs/feature-template.md` for feature-spec structure
- `specs/feature-template.test.md` and `test-spec` skill guidance for test-spec structure
- `docs/plans/0000-00-00-example-plan.md` for plan closeout structure
- architecture and ADR authoring guidance for design-state details

## Archived vs Superseded

`superseded` is reserved for artifacts that have been explicitly replaced by a newer authoritative artifact. A superseded artifact must identify its replacement with `superseded_by`.

`archived` is reserved for artifacts that are no longer current but remain useful for historical, audit, learning, or traceability purposes. Archived artifacts are not authoritative and do not require a replacement.

Do not use `archived` when the more precise status is `deprecated`, `rejected`, `abandoned`, `done`, or `superseded`.

An artifact is `superseded` when a newer artifact replaces it as the authoritative source.

Required meaning:

```text
This artifact is no longer authoritative because another artifact has replaced it.
```

Required replacement metadata, whether in frontmatter or equivalent explicit fields, should include:

```yaml
status: superseded
superseded_at: 2026-04-20
superseded_by: specs/rigorloop-workflow.md
superseded_reason: Replaced by the approved top-level workflow lifecycle specification.
```

Important rules:

- an archived artifact does not need a replacement
- a superseded artifact must point to its replacement
- if there is no replacement, the artifact should not be `superseded`

For practical distinction across the repository:

| Status | Means | Requires replacement pointer? | Can be relied on for current work? |
| --- | --- | ---: | ---: |
| `active` | currently in use | no | yes |
| `approved` / `accepted` | authorized for use | no | yes |
| `done` | completed execution artifact | no | sometimes, as result evidence |
| `superseded` | replaced by newer authority | yes | no |
| `archived` | retained historical record | no | no |
| `rejected` | considered and declined | no | no |
| `abandoned` | stopped before completion | no | no |
| `deprecated` | still exists but discouraged | optional | limited / conditional |

The recommended ownership split is:

- `proposal` creates proposal artifacts in `draft`
- `proposal-review` determines whether the proposal moves to `accepted`, `rejected`, or remains in revision
- when chat or review output establishes acceptance but the tracked proposal is still stale, the review stage or the immediate next depending stage must normalize the tracked artifact before that next stage may rely on it
- `spec` authors specs in `draft`
- `spec-review` is the gate after which relied-on specs must be normalized to `approved`; `reviewed` may remain only as a short-lived transitional state, not a durable tracked state for governing specs
- `test-spec` authors test specs in `draft`; once implementation is actively using the test spec as its proof surface, the artifact becomes `active`; once the implemented change is no longer an active proof-planning surface, the artifact becomes `archived` unless it is superseded or abandoned
- `architecture` authors design docs in `draft`
- `architecture-review` or equivalent accepted design closeout moves relied-on architecture docs to `approved`; `reviewed` is only a short-lived transitional event
- ADRs use the repository's lifecycle-managed ADR vocabulary: `draft`, `proposed`, `accepted`, `active`, `deprecated`, `superseded`, `archived`, and `abandoned`. Once the decision is adopted as repository direction, the ADR must leave `draft` or `proposed`; later retirement should use `deprecated`, `superseded`, `archived`, or `abandoned` according to the actual disposition
- later replacement work owns `superseded` transitions for older artifacts it replaces, and each superseded artifact must identify the newer authoritative replacement
- once an artifact reaches a settled state, closeout records should be added through distinct `Closeout` or `Follow-on artifacts` surfaces rather than by overwriting the original `Next artifacts` planning history

The repository should also define a general stale-state rule for touched artifacts. At minimum, stale state should include:

- a merged or otherwise closed artifact still marked `draft`, `under review`, `reviewed`, `active`, or `proposed` when the repository is already depending on it as settled guidance
- an artifact whose `Status` says it is settled while its active-work `Readiness` text still advertises pre-review, pre-implementation, or still-pending downstream stages
- an artifact that has reached settled state but still lacks the distinct closeout surface the workflow requires to record actual follow-on artifacts or final disposition
- a touched artifact that remains in a pre-approval state even though the current branch is already using it as an approved source of truth

This keeps the repository human-readable, avoids a second registry, and turns status normalization into ordinary workflow closeout rather than occasional archaeology.

The verify policy should be:

- `verify` blocks on stale or inconsistent artifacts that are touched, referenced, generated, or authoritative for the changed area.
- `verify` reports unrelated stale baseline artifacts as warnings.
- Baseline documentation debt must not block unrelated improvements, but no change may rely on a stale authoritative artifact.

For practical classification, the repository should treat artifact scope as:

| Artifact condition | Related to change? | Verify behavior |
| --- | ---: | --- |
| stale touched artifact | yes | block |
| stale referenced artifact | yes | block |
| stale generated output | yes | block |
| stale authoritative artifact for changed area | yes | block |
| stale artifact elsewhere | no | warn |
| unknown stale artifact | unclear | warn and ask for classification |
| stale artifact marked as accepted baseline debt | no | warn only |

At minimum, "referenced" or "authoritative for the changed area" should include:

- artifacts changed in the PR
- artifacts linked from `docs/changes/<change-id>/change.yaml`
- artifacts referenced by the PR body
- generated outputs that should match source
- specs governing changed behavior
- architecture docs governing changed boundaries
- test specs governing changed tests
- plans governing active implementation

Verify should check PR-body references only when a draft PR body already exists.

Before PR text exists, `verify` should check the pre-PR handoff surfaces instead:

- `docs/changes/<change-id>/change.yaml`
- `explain-change.md` or equivalent explain-change artifact
- the active plan
- touched, referenced, generated, and authoritative artifacts for the changed area

Final PR text must not introduce new authoritative artifact references without re-running `verify`.

The recommended first-release enforcement stack should be:

- docs define the contract
- the validator checks the contract
- `verify` runs the validator
- CI runs `verify`
- the PR reports the `verify` result

The minimal structural validator in this first change should block only high-confidence issues such as:

- invalid or unsupported status vocabulary for the artifact class
- missing required metadata or required sections
- empty required sections
- duplicate artifact identifiers where uniqueness is part of the contract
- invalid normalized artifact naming where the contract requires it
- placeholder text such as `TODO`, `TBD`, or `lorem ipsum`
- generated folders or generated outputs being treated as authored source of truth
- objective stale-state contradictions between status and required closeout sections

## Expected behavior changes

- Merged proposals will not keep advertising `draft` or future `proposal-review` work after acceptance.
- Governing specs that the repository already relies on will not remain at `draft` or ambiguous transitional `reviewed` state.
- Test specs will show whether they are still active implementation proof surfaces or archived historical coverage artifacts.
- Architecture docs and ADRs will no longer lag behind the repository's adopted design state.
- Superseded artifacts will point to the newer authoritative replacement, while archived artifacts will remain useful history without pretending a replacement exists.
- `verify` will gain an explicit reason to block stale artifact metadata beyond plan lifecycle state, using the touched/referenced/generated/authoritative scope for the changed area.
- `verify` will block on stale touched, referenced, generated, and authoritative artifacts for the changed area, while reporting unrelated baseline debt as warnings.
- Settled artifacts will preserve their original `Next artifacts` planning history while recording actual downstream outcomes in a distinct closeout section.
- The first implementation will provide executable enforcement through a minimal structural validator, fixtures, `verify`, and CI wiring rather than relying on documentation alone.
- Reviewers will be able to trust artifact status and readiness text without reconstructing state from chat history.

## Architecture impact

This is mainly a workflow-governance change, but it does touch long-lived repository structure and validation boundaries.

Likely impacted surfaces:

- `specs/rigorloop-workflow.md`
- `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` if their workflow guidance changes
- proposal, spec, test-spec, architecture, architecture-review, proposal-review, spec-review, verify, pr, and workflow skills
- feature and test-spec templates, and any architecture/ADR authoring guidance
- repository-owned validation scripts if the repository chooses to enforce artifact-state rules structurally

This should not require application-runtime architecture changes. It should also stay small enough that a separate architecture artifact is unnecessary unless the validator expands beyond a focused repo-owned structural check plus fixtures and CI wiring.

## Testing and verification strategy

Likely proof surfaces:

- manual review of the workflow spec and guidance to confirm each artifact class has explicit status ownership and closeout rules
- a minimal structural validator that checks the first objective lifecycle and closeout invariants
- fixture cases that prove the validator accepts valid artifact state and rejects the intended high-confidence defects
- test-spec coverage for:
  - allowed lifecycle states by artifact class
  - transition-owner expectations
  - stale active-work wording detection
  - required closeout-surface presence and separation from active `Next artifacts` history
  - `superseded` versus `archived` distinction and required replacement-pointer behavior
  - verify-time blocking behavior for touched, referenced, generated, and authoritative artifacts
  - verify-time warning behavior for unrelated stale baseline artifacts
  - `superseded` handling for replaced artifacts
- repository validation commands that check:
  - allowed status vocabulary by file type
  - forbidden stale wording patterns in touched or authoritative settled artifacts
  - required closeout or follow-on sections for settled artifacts where the contract requires them
  - required `superseded_by` metadata or equivalent explicit replacement pointer for superseded artifacts
  - generated-source boundary enforcement
  - template/example alignment with the approved lifecycle model
- `verify` command execution that runs the validator as part of PR-readiness proof
- CI wiring that runs the same repo-owned verification entrypoint
- focused migration checks proving the repo no longer depends on merged artifacts that still present themselves as draft-only or pre-review

## Rollout and rollback

Rollout:

- define the artifact lifecycle matrix in the workflow contract
- align top-level governance guidance and authoring/review skills
- update relevant templates so new artifacts start with the right lifecycle structure
- add a minimal repo-owned structural validator in the same change
- add fixtures that prove the validator blocks only the intended objective defects
- extend `verify` expectations to stale non-plan artifact state, with blocking for touched, referenced, generated, and authoritative artifacts and warning-only treatment for unrelated baseline debt, as the minimum first enforcement step
- wire CI to run the same repo-owned verification path
- add the distinct closeout pattern to the in-scope templates and examples instead of rewriting active planning sections in place
- normalize already-known stale tracked artifacts that the new contract covers

Rollback:

- revert the workflow/governance change if the lifecycle model proves too rigid or confusing
- preserve any artifact metadata corrections that truthfully reflect repository history, even if the exact rule wording changes later

## Risks and mitigations

- Risk: the lifecycle model becomes too abstract or too many statuses remain ambiguous.
  - Mitigation: define status semantics and transition owners per artifact class in one explicit matrix.
- Risk: contributors assume every approval transition must happen inside the review stage itself.
  - Mitigation: define ownership for the transition, but allow the next depending stage to require tracked normalization before proceeding.
- Risk: verification expands into intrusive repository-wide scanning on every change.
  - Mitigation: scope stale-state blocking to touched, referenced, generated, and authoritative artifacts for the changed area, while treating unrelated baseline debt as warnings.
- Risk: the validator expands into subjective or brittle enforcement too early.
  - Mitigation: keep the first validator limited to objective structural defects and leave subjective quality to review comments.
- Risk: contributors may erase planning history while trying to normalize settled artifacts.
  - Mitigation: define and template a distinct `Closeout` or `Follow-on artifacts` pattern instead of rewriting `Next artifacts` in place.
- Risk: contributors may use `archived` and `superseded` interchangeably, weakening replacement traceability.
  - Mitigation: reserve `superseded` for explicit replacement and require a replacement pointer; reserve `archived` for useful history with no direct replacement.
- Risk: retroactive cleanup expands the scope too much.
  - Mitigation: separate the policy change from any large historical cleanup campaign, and normalize old artifacts incrementally or in focused follow-ups.

## Open questions

- None blocking proposal review.

## Decision log

- 2026-04-20: Rejected ad hoc cleanup as the primary strategy. Reason: the repository already needed a dedicated cleanup PR after merged artifact metadata drifted away from reality.
- 2026-04-20: Rejected removing artifact-local statuses. Reason: Git and PR state do not replace file-local explanations for accepted, rejected, superseded, or completed workflow artifacts.
- 2026-04-20: Chose repository-wide artifact lifecycle ownership as the leading direction. Reason: it solves the root cause while preserving artifact-local traceability and matches the successful plan-lifecycle approach.
- 2026-04-20: Deferred any large central registry or aggressive automation. Reason: the ownership model should stabilize before the repository adds a second layer of state management.
- 2026-04-20: Chose workflow-spec invariants plus a compact lifecycle summary, with per-artifact detail delegated to canonical template/example surfaces and skills. Reason: this keeps the workflow contract discoverable without turning it into a second copy of every artifact-specific authoring rule.
- 2026-04-20: Decided that `reviewed` is a transitional review event, not a long-lived artifact state. Reason: relied-on artifacts should normalize into a smaller durable status family instead of leaving review outcomes as indefinite steady state.
- 2026-04-20: Decided that `verify` should block on touched, referenced, generated, and directly authoritative artifacts for the changed area, and warn on unrelated stale baseline artifacts. Reason: stale authoritative guidance must not be relied on, but unrelated documentation debt should not block otherwise-correct work.
- 2026-04-20: Decided that the first enforcement step should include a dedicated minimal structural validator, fixtures, `verify`, and CI wiring in the same change. Reason: the repository needs executable verification from the start, but the validator should stay limited to objective structural defects rather than subjective quality scoring.
- 2026-04-20: Decided not to rewrite planning history in place. Reason: `Next artifacts` should preserve what was planned while active, and distinct `Closeout` or `Follow-on artifacts` sections should record what actually happened after settlement.
- 2026-04-20: Decided that `superseded` means explicitly replaced by a newer authoritative artifact, while `archived` means historically valuable but no longer current. Reason: the repository needs replacement traceability without forcing every no-longer-current artifact to pretend it has a direct successor.

## Next artifacts

- `proposal-review`: challenge whether the lifecycle matrix is the right scope and whether any artifact classes or transitions are missing.
- `spec`: define the normative artifact lifecycle contract, including status meanings, transition ownership, and stale-state rules.
- `test-spec`: map the lifecycle rules to structural and verification checks.
- `architecture`: only if the validator or CI design expands beyond a focused repo-owned structural check, fixtures, and thin CI wiring.
- `plan`: sequence the workflow-doc, skill, template, and validation updates once the contract is stable.

## Follow-on artifacts

- `specs/artifact-status-lifecycle-ownership.md`
- `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md`

## Readiness

Proposal review is complete. This proposal was accepted and now governs the artifact-status lifecycle ownership spec work.

No further proposal-stage action is pending for this artifact.
