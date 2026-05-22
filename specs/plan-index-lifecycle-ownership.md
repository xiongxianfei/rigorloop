# Plan Index Lifecycle Ownership

## Status
- approved

## Related proposal

- [Plan index lifecycle ownership](../docs/proposals/2026-04-20-plan-index-lifecycle-ownership.md)
- [Bounded Plan Index and Completed-Plan Archive](../docs/proposals/2026-05-22-bounded-plan-index-and-completed-plan-archive.md)

## Goal and context

This spec defines the repository-visible contract for keeping `docs/plan.md`, `docs/plan-archive.md`, and individual plan files synchronized when an initiative changes lifecycle state.

The goal is to prevent completed, blocked, or superseded initiatives from continuing to look active after the real lifecycle decision is already known while keeping the common-read plan index bounded. The repository treats `docs/plan.md` as the first-read index for active, blocked, recent done, and active supersession context. Older terminal history lives in `docs/plan-archive.md`. This spec makes lifecycle ownership, archival behavior, and closeout timing explicit.

## Glossary

- `common-read plan index`: `docs/plan.md`, the bounded first-read index for active work, blocked work, recent completed work, and active supersession context.
- `plan archive`: `docs/plan-archive.md`, the repository archive for older terminal plan-index history.
- `plan index surfaces`: `docs/plan.md` and `docs/plan-archive.md` considered together.
- `plan body`: the concrete initiative plan file under `docs/plans/`.
- `planned initiative`: work that has a concrete plan file under `docs/plans/` and an entry in the plan index surfaces.
- `lifecycle state`: the repository-visible initiative state recorded as `active`, `blocked`, `done`, `abandoned`, or `superseded` in the plan body lifecycle-state marker.
- `lifecycle closeout`: the update that moves a planned initiative to its correct lifecycle state in both the plan index and the plan body.
- `merge-dependent done transition`: a `Done` transition where the branch is not truly complete until the PR is merged.
- `Done (recent)`: the capped recent completed-plan window in `docs/plan.md`.
- `Done (archive)`: older completed-plan history in `docs/plan-archive.md`.
- `terminal lifecycle state`: `done`, `abandoned`, or `superseded`.
- `active supersession context`: a labeled `docs/plan.md` superseded entry with a replacement plan link and non-empty `active-context:` rationale that records why the supersession pointer still belongs in the common-read index.
- `structural common-read budget`: the bounded shape rule for `docs/plan.md`: complete Active and Blocked sections first, recent Done at or below the approved cap, one-line terminal summaries, and older terminal history in `docs/plan-archive.md`.

## Examples first

### Example E1: done transition before PR

Given a planned initiative completes all required implementation and verification work before PR creation
When the contributor prepares the review package
Then lifecycle closeout updates both the plan index surfaces and the plan body to `Done` before the PR is opened.

### Example E2: done transition after merge

Given a planned initiative is review-ready on the branch but repository policy treats merge as the deciding event for completion
When the PR merges
Then immediate post-merge cleanup may perform lifecycle closeout, provided that it updates both the plan index surfaces and the plan body promptly.

### Example E3: blocked initiative

Given a planned initiative cannot proceed because of an unresolved dependency or decision
When maintainers decide the work is blocked
Then the plan index surfaces and the plan body move to `Blocked` as soon as that decision is made rather than waiting for PR or merge.

### Example E4: superseded initiative

Given a newer plan replaces an older active plan
When the replacement decision is made
Then the older plan moves to `Superseded` in both the plan index surfaces and the plan body as part of that replanning change.

### Example E5: learn is not lifecycle authority

Given a contributor later runs `learn` and captures retrospective lessons
When that retrospective is written
Then it may add durable lessons, but it does not own plan-index bookkeeping and does not substitute for lifecycle closeout.

### Example E6: older completed work is archived

Given `docs/plan.md` already contains 10 recent Done entries
When another plan transitions to `Done`
Then `docs/plan.md` keeps at most 10 Done entries and the oldest displaced terminal entry remains locatable in `docs/plan-archive.md`.

### Example E7: recurring archival preserves terminal history

Given `docs/plan.md` or `docs/plan-archive.md` changes during routine archival
When validation runs
Then every plan file under `docs/plans/` with a terminal lifecycle state appears exactly once across `Done (recent)` and archived terminal history.

### Example E8: active and blocked work stay in the common-read index

Given a plan is active, blocked, review-requested, or resolution-needed
When contributors update plan-index surfaces
Then that plan remains visible in `docs/plan.md` and is not stored only in `docs/plan-archive.md`.

### Example E9: terminal superseded history is archived

Given a superseded plan no longer provides active replacement context
When plan-index maintenance compacts terminal history
Then `docs/plan.md` may keep only active supersession context and terminal superseded history remains recoverable from `docs/plan-archive.md`.

### Example E10: explicit terminal lifecycle marker

Given a plan body has a top-level `## Status` section with `Plan lifecycle state: done` and `Terminal disposition: merged`
When terminal-plan conservation validation runs
Then the plan is classified as terminal and must appear exactly once across `Done (recent)` and `Done (archive)`.

### Example E11: explicit nonterminal lifecycle marker

Given a plan body has a top-level `## Status` section with `Plan lifecycle state: active` and `Terminal disposition: none`
When terminal-plan conservation validation runs
Then the plan is classified as nonterminal and must not appear only in `docs/plan-archive.md`.

### Example E12: contradictory lifecycle marker

Given a plan body has a top-level `## Status` section with `Plan lifecycle state: active` and `Terminal disposition: merged`
When the plan file is in validation scope
Then validation fails.

### Example E13: legacy prose-only status

Given a plan body has a top-level `## Status` section that says only `This plan finished after PR #80 merged.`
When terminal-plan conservation validation runs
Then validators do not infer terminal state from that prose, and first-migration preservation depends on the change-local migration proof.

### Example E14: valid active supersession entry

Given `docs/plan.md` has a Superseded entry with a superseded plan link, `superseded by:` replacement plan link, and non-empty `active-context:` rationale
When plan-index validation runs
Then the entry may remain in the common-read index.

### Example E15: invalid main-index supersession entry

Given `docs/plan.md` has a Superseded entry with a superseded plan link and `superseded by:` replacement plan link but no `active-context:` rationale
When plan-index validation runs
Then validation fails because the entry lacks the structural marker that keeps superseded history in the common-read index.

## Plan body lifecycle-state marker

For validator-owned terminal-plan conservation, a plan body has a detected lifecycle state only when it contains a top-level `## Status` section with these exact fields:

```text
Plan lifecycle state: <active | blocked | done | abandoned | superseded>
Terminal disposition: <none | merged | closed | abandoned | superseded>
```

`Plan lifecycle state` is the source of truth for terminal-plan conservation. Validators do not infer terminal state from arbitrary prose elsewhere in the plan body.

Terminal lifecycle states are `done`, `abandoned`, and `superseded`. Nonterminal lifecycle states are `active` and `blocked`.

`Terminal disposition` is `none` for nonterminal states. For terminal states, it is one of `merged`, `closed`, `abandoned`, or `superseded`.

Legacy prose-only plan bodies are not parsed for terminal state. During the first archive migration, conservation for legacy terminal plans is proven by the change-local migration table. Future terminal-plan validation depends on the explicit lifecycle-state marker.

## Active supersession context

`docs/plan.md` may keep superseded entries only when they are still useful to orient current work.

A superseded entry in `docs/plan.md` includes:

- a link to the superseded plan;
- `superseded by: <replacement plan link>`;
- `active-context: <short rationale>`.

The `active-context:` field records the owner or editor judgment for why the supersession pointer still belongs in the common-read index. Validators enforce the structural fields. Code review owns the semantic quality of the rationale.

Superseded entries without `active-context:` move to `docs/plan-archive.md`. Terminal superseded entries in `docs/plan-archive.md` may record their replacement link, but they do not retain `active-context:`.

## Requirements

R1. This spec applies to planned initiatives only. Fast-lane work and unplanned single-slice work MUST NOT be forced to create or update plan-index lifecycle state solely because of this spec.

R2. The repository MUST treat `docs/plan.md` as common-read lifecycle bookkeeping for planned initiatives, not as the body of a plan.

R2a. The repository MUST treat `docs/plan-archive.md` as terminal lifecycle history for planned initiatives, not as the body of a plan.

R3. The repository MUST keep the plan index surfaces and the corresponding plan body synchronized when a planned initiative changes lifecycle state.

R3a. A nonterminal planned initiative MUST appear in exactly one current lifecycle section in `docs/plan.md`: `Active`, `Blocked`, or active `Superseded` context.

R3b. A plan body whose lifecycle state is `Done`, `Blocked`, or `Superseded` MUST NOT still present itself as an active or in-progress initiative through status or outcome/readiness wording.

R3c. A terminal planned initiative MUST appear exactly once across `Done (recent)` in `docs/plan.md` and terminal history in `docs/plan-archive.md`, except during a documented migration transaction that records and resolves duplication before readiness is claimed.

R3d. `docs/plan.md` MUST keep complete `Active` and `Blocked` sections before any Done history.

R3e. `docs/plan.md` MUST keep `Done (recent)` at or below the approved cap. The first approved cap is 10 entries unless a later approved spec amendment changes it.

R3f. `docs/plan.md` MUST link to `docs/plan-archive.md` whenever older terminal history exists.

R3g. A plan body has a validator-detected lifecycle state only when it contains a top-level `## Status` section with exactly one `Plan lifecycle state:` field and exactly one `Terminal disposition:` field.

R3h. The plan body lifecycle-state marker MUST use this shape:

```text
Plan lifecycle state: <active | blocked | done | abandoned | superseded>
Terminal disposition: <none | merged | closed | abandoned | superseded>
```

R3i. `Plan lifecycle state` is the source of truth for terminal-plan conservation. Validators MUST NOT infer terminal lifecycle state from arbitrary prose elsewhere in the plan body.

R3j. `Plan lifecycle state` values `done`, `abandoned`, and `superseded` are terminal lifecycle states.

R3k. `Plan lifecycle state` values `active` and `blocked` are nonterminal lifecycle states.

R3l. `Terminal disposition` MUST be `none` for nonterminal lifecycle states.

R3m. `Terminal disposition` MUST be one of `merged`, `closed`, `abandoned`, or `superseded` for terminal lifecycle states.

R3n. If the lifecycle-state marker fields are missing, the plan body has unknown lifecycle state for validator purposes. Validators MUST NOT guess lifecycle state from prose.

R3o. If lifecycle-state marker fields are contradictory, malformed, duplicated, or use unknown values, validation MUST fail when the plan file is in validation scope.

R3p. Legacy prose-only plan bodies MUST NOT be parsed for terminal state. During the first archive migration, conservation for legacy terminal plans MUST be proven by the change-local migration table. Future terminal-plan validation depends on the explicit lifecycle-state marker.

R4. Lifecycle-closeout ownership MUST be split as follows:
- `plan` creates or revises the plan file and its index entry when an initiative starts or is re-planned;
- `implement` keeps progress, decisions, discoveries, and validation notes current during execution;
- `verify` checks whether lifecycle state in the plan index surfaces and the plan body still matches reality before `branch-ready` is claimed;
- final lifecycle closeout updates both the plan index surfaces and the plan body when lifecycle state changes;
- `learn` captures durable lessons and MUST NOT be the authoritative owner of lifecycle-state bookkeeping.

R5. Final lifecycle closeout MUST update both:
- the initiative entry in the plan index surfaces; and
- the plan file's own lifecycle surfaces, including status and any outcome or readiness wording that would otherwise keep the plan looking active.

R6. When the outcome is already known before PR, lifecycle closeout SHOULD happen before PR creation rather than being deferred.

R6a. A `Done` transition MAY be completed in immediate post-merge cleanup only when merged state is the deciding event for completion.

R6b. `Blocked` and `Superseded` transitions MUST be recorded as soon as they are decided. They MUST NOT be deferred only because no PR has been opened or merged yet.

R7. `verify` MUST NOT treat a planned initiative as `branch-ready` when stale lifecycle state remains in either the plan index or the plan body.

R7a. For this spec, stale lifecycle state includes at minimum:
- a completed initiative still listed under `## Active`;
- a blocked or superseded initiative still listed under `## Active`;
- a plan index entry moved to `Done`, `Blocked`, or `Superseded` while the plan body still presents the initiative as active or in progress;
- a plan body marked complete, blocked, or superseded while the plan index surfaces still list the initiative under a conflicting lifecycle section;
- a terminal plan missing from both `Done (recent)` and `docs/plan-archive.md`;
- a terminal plan appearing more than once across `Done (recent)` and `docs/plan-archive.md` without a documented migration exception.

R8. Contributor-facing workflow guidance MUST make lifecycle ownership discoverable without requiring chat history.

R8a. At minimum, the repository's workflow summary and plan guidance MUST describe:
- that `docs/plan.md` is an index rather than a plan body;
- that `docs/plan-archive.md` stores older terminal plan history;
- that `implement` owns ongoing plan-body updates during execution;
- that final lifecycle closeout owns state transitions in both the plan index surfaces and the plan body; and
- that `verify` challenges stale lifecycle state before `branch-ready`.

R9. When this rule is adopted, previously stale plan-index or plan-body lifecycle state that is already known to be wrong SHOULD be corrected as part of the migration to the clarified ownership model.

R10. The common-read plan index MUST use a structural common-read budget rather than a separate whole-file line-count budget.

R10a. The structural common-read budget MUST be satisfied when:
- `Active` and `Blocked` are complete and appear before Done history;
- `Done (recent)` is at or below the approved cap;
- terminal entries are one-line summaries rather than milestone transcripts;
- older terminal history is in `docs/plan-archive.md`.

R11. Done and archived terminal entries MUST include a link to the owning plan file.

R11a. Terminal entries SHOULD include date/title, terminal state, and PR or disposition when available.

R12. `Done (recent)` and archived terminal history SHOULD sort newest-first unless a later approved spec amendment changes the ordering.

R13. Active, blocked, review-requested, resolution-needed, or otherwise nonterminal plans MUST NOT be stored only in `docs/plan-archive.md`.

R14. The plan archive MUST be append-only except for deduplication, formatting normalization, correcting broken links, or migrating terminal entries under this spec.

R15. Validation MUST check terminal-plan conservation whenever `docs/plan.md` or `docs/plan-archive.md` changes.

R15a. Terminal-plan conservation means every plan file under `docs/plans/` whose explicit lifecycle-state marker has terminal lifecycle state appears exactly once across `Done (recent)` and archived terminal history.

R15b. Validation MUST check that recent and archived terminal entries link to existing plan files.

R15c. Validation MUST check that `Done (recent)` does not exceed the approved cap.

R15d. Validation MUST check terminal entry one-line shape and required plan-link shape. Code review owns semantic summary quality that cannot be reliably decided structurally.

R16. The initial archive migration MUST record a change-local migration proof with pre-migration count, post-migration recent count, post-migration archive count, link preservation, duplicate status, and count conservation.

R17. Terminal superseded history MUST move to `docs/plan-archive.md` when it no longer provides active supersession context in `docs/plan.md`.

R17a. `docs/plan.md` MAY keep active supersession context when it helps readers understand active or recently replaced work.

R17b. A superseded entry in `docs/plan.md` MUST include:
- a link to the superseded plan;
- `superseded by: <replacement plan link>`;
- `active-context: <short rationale>`.

R17c. The `active-context:` field records the owner or editor judgment for why the supersession pointer still belongs in the common-read index.

R17d. Validators MUST enforce the `superseded by:` and `active-context:` structural fields for superseded entries in `docs/plan.md`.

R17e. Validators MUST NOT infer active supersession context from unlabeled prose.

R17f. Code review owns the semantic quality of the `active-context:` rationale.

R17g. Superseded entries without an `active-context:` marker MUST be moved to `docs/plan-archive.md`.

R17h. Terminal superseded entries in `docs/plan-archive.md` MAY record their replacement link, but they MUST NOT use `active-context:`.

R17i. When the replacement plan is no longer active or the pointer no longer helps orient current work, contributors MUST remove the `active-context:` marker and move the entry to the archive.

## Inputs and outputs

### Inputs

- `docs/plan.md`
- `docs/plan-archive.md`
- the concrete plan file under `docs/plans/`
- explicit plan body lifecycle-state markers
- the workflow summary and plan guidance surfaces that tell contributors how to manage plans
- validator output for plan-index surfaces
- change-local migration proof for archive migration
- the actual initiative outcome known at closeout time

### Outputs

- a synchronized plan-index entry under the correct live or archived lifecycle surface
- a synchronized plan body whose status and readiness wording match that lifecycle state
- workflow guidance that makes ownership of those updates explicit
- validation evidence that terminal plans remain findable exactly once across recent and archived history
- migration proof for the initial archive split

## State and invariants

- `docs/plan.md` remains the bounded common-read index, not the body of a plan.
- `docs/plan-archive.md` remains terminal history, not the body of a plan.
- Each planned initiative has one current lifecycle state in the plan index surfaces.
- The plan body and plan index surfaces describe the same lifecycle state.
- Active and blocked plans remain complete and visible in `docs/plan.md`.
- Terminal plan detection uses only the explicit plan body lifecycle-state marker.
- Superseded entries kept in `docs/plan.md` carry structural active supersession context.
- Older terminal history remains recoverable in `docs/plan-archive.md`.
- `learn` remains retrospective and non-authoritative for lifecycle-state bookkeeping.
- Post-merge cleanup is an exception for merge-dependent `Done` transitions, not the default rule for all lifecycle changes.

## Error and boundary behavior

- If a contributor claims `branch-ready` while the plan index surfaces and plan body disagree about lifecycle state, the initiative is not ready.
- If a `Done` transition is clearly known before PR and still left under `## Active`, that is stale lifecycle state.
- If an initiative becomes `Blocked` or `Superseded`, waiting for a later merge or retrospective to update the plan state is incorrect.
- If a repository has no planned initiative for the work, this spec does not require creating one just to satisfy lifecycle-closeout rules.
- If a plan is replaced by a new plan, the old plan may remain tracked, but it must be marked `Superseded` rather than silently left `Active`.
- If archival would move active, blocked, review-requested, resolution-needed, or ambiguous work out of `docs/plan.md`, the archive update is invalid.
- If routine archival would create a missing or duplicated terminal entry, validation fails until the union of recent and archived terminal history is corrected.
- If `docs/plan-archive.md` is absent while older terminal history exists, the archive split is incomplete.
- If lifecycle-state marker fields are missing, validators do not infer terminal state from plan-body prose.
- If lifecycle-state marker fields are malformed, duplicated, contradictory, or unknown, validation fails when the plan file is in validation scope.
- If a superseded entry in `docs/plan.md` lacks `superseded by:` or non-empty `active-context:`, validation fails.
- If an archived superseded entry retains `active-context:`, validation fails because the marker is reserved for common-read active supersession context.

## Compatibility and migration

- This change is compatibility-sensitive because it affects contributor-visible workflow behavior and what later work must treat as active guidance.
- Adoption SHOULD correct any already-known stale plan-index, plan-archive, or plan-body state so the new rule starts from a truthful baseline.
- Existing plan body structure does not need to be redesigned; this spec changes lifecycle ownership, archive placement, and timing, not the overall plan format.
- The first archive migration MUST preserve every pre-migration Done entry in either `Done (recent)` or `docs/plan-archive.md`.
- Legacy prose-only terminal entries from the first migration MUST be preserved through the change-local migration table rather than broad prose terminal inference.
- Rollback, if needed, moves archived entries back into `docs/plan.md` before removing `docs/plan-archive.md`. Truthfully corrected lifecycle state SHOULD be preserved.

## Observability

- Manual review MUST be able to compare `docs/plan.md`, `docs/plan-archive.md`, and the corresponding plan body and determine whether lifecycle state is synchronized.
- Workflow and plan-guidance artifacts MUST make the ownership split discoverable to contributors.
- Verification results MUST name the specific lifecycle-state evidence reviewed when this rule is relevant to `branch-ready`.
- Validation output MUST make missing terminal entries, duplicate terminal entries, broken plan links, cap violations, and active-work-in-archive violations visible.
- Validation output MUST make malformed lifecycle-state markers, contradictory terminal dispositions, missing active supersession fields, and archived `active-context:` markers visible.

## Security and privacy

- This spec MUST NOT introduce automation or workflow claims that fake merge state, CI state, or review completion.
- Lifecycle-state bookkeeping MUST remain in tracked repository artifacts rather than hidden in chat-only or host-local state.
- The archive MUST NOT introduce secrets, private local paths, credentials, or host-only state.

## Accessibility and UX

- Contributor-facing plan-index guidance MUST keep the first-read orientation path clear: read `docs/plan.md` for active, blocked, recent done, and active supersession context; follow the archive link only for older terminal history.
- The archive pointer in `docs/plan.md` MUST use a normal Markdown link to `docs/plan-archive.md`.

## Performance expectations

- Lifecycle-state checks SHOULD remain lightweight manual or structural review steps that fit normal contributor closeout and verification work.
- Terminal-plan conservation checks SHOULD run only when `docs/plan.md`, `docs/plan-archive.md`, or plan bodies relevant to terminal-state detection change.
- This spec does not require continuous background synchronization.

## Edge cases

EC1. A plan may remain `Active` during implementation even if all code is written, as long as required verification or review gates are still intentionally outstanding and completion is not yet claimed.

EC2. A plan may move to `Done` after merge when repository policy or branch protection makes merge the deciding event for completion.

EC3. A plan that is abandoned because a replacement plan exists must move to `Superseded` even if no user-visible code shipped from it.

EC4. A plan that pauses for an external dependency or product decision must move to `Blocked` without waiting for a future retrospective.

EC5. A repository MAY later automate lifecycle-state enforcement, but automation is not required by this spec and does not replace the ownership model defined here.

EC6. A plan may be recently completed and remain in `Done (recent)` until the cap is exceeded.

EC7. A terminal plan may move from `Done (recent)` to `docs/plan-archive.md` without any change to the plan body's lifecycle state.

EC8. A terminal superseded plan may remain in `docs/plan.md` only while it provides active supersession context; otherwise, it belongs in the archive.

EC9. During a migration transaction, a terminal entry may be temporarily duplicated only when the migration proof records the duplication and final validation resolves it before readiness is claimed.

EC10. A legacy prose-only terminal plan is not parsed as terminal by standing validation; first-migration preservation is proven by the migration table.

EC11. A plan body with `Plan lifecycle state: active` and `Terminal disposition: merged` has contradictory marker fields and fails validation when in scope.

EC12. A terminal plan duplicated across `Done (recent)` and `docs/plan-archive.md` fails validation unless a documented migration transaction resolves the duplication before readiness is claimed.

EC13. A superseded main-index entry that lacks `active-context:` fails validation.

EC14. An archived superseded entry that retains `active-context:` fails validation.

## Non-goals

- Replacing `docs/plan.md` with a new planning system.
- Redesigning the internal section structure of every plan file.
- Turning `learn` into a mandatory bookkeeping stage.
- Requiring post-merge cleanup for every lifecycle transition.
- Replacing plan files under `docs/plans/`.
- Changing milestone, review, verification, PR, or closeout semantics.
- Introducing a generated plan-index registry in this first slice.
- Introducing large CI automation or continuous background synchronization as part of the initial archive split.

## Acceptance criteria

- Contributors can tell from repository guidance that `docs/plan.md` is the lifecycle index and that plan bodies carry initiative detail.
- The ownership split between `plan`, `implement`, `verify`, final lifecycle closeout, and `learn` is explicit and non-conflicting.
- A completed, blocked, or superseded planned initiative does not remain under `## Active` once the real lifecycle decision is known.
- A planned initiative does not present conflicting lifecycle state between `docs/plan.md` and its plan body.
- `verify` treats stale lifecycle state as blocking `branch-ready` for planned initiatives.
- The post-merge exception is limited to merge-dependent `Done` transitions rather than becoming the default for all lifecycle changes.
- `docs/plan.md` lists complete Active and Blocked sections before Done history.
- `docs/plan.md` keeps `Done (recent)` at or below the approved cap.
- `docs/plan.md` links to `docs/plan-archive.md` when older terminal history exists.
- `docs/plan-archive.md` preserves older terminal plan history.
- Every terminal plan is locatable exactly once across recent and archived terminal history after migration.
- Archive migration proof records pre/post counts, link preservation, and duplicate status.
- Active, blocked, review-requested, resolution-needed, or ambiguous work is not stored only in the archive.
- Plan body terminal detection uses only the explicit `## Status` lifecycle-state marker and does not infer terminal state from prose.
- Plans with terminal lifecycle state appear exactly once across `Done (recent)` and `Done (archive)`.
- Plans with nonterminal lifecycle state do not appear only in the archive.
- Missing, malformed, duplicated, contradictory, or unknown lifecycle-state fields produce stable validation errors when the plan file is in validation scope.
- Legacy prose-only terminal entries from the first migration are preserved through the change-local migration table rather than prose inference.
- Every superseded entry kept in `docs/plan.md` includes a superseded-plan link, a replacement-plan link, and a non-empty `active-context:` rationale.
- Superseded entries without `active-context:` are archived as terminal superseded history.
- The validator enforces structural supersession fields, while code review owns semantic rationale quality.
- Archived superseded entries remain findable and may record their replacement link, but do not retain `active-context:`.

## Open questions

None.

## Next artifacts

spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr

## Follow-on artifacts

None yet.

## Readiness

Spec review approved in `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/spec-review-r2.md`. Ready for planning and test-spec refresh.
