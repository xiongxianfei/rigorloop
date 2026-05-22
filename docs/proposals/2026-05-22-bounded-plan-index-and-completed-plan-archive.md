# Bounded Plan Index and Completed-Plan Archive

## Status

accepted

## Problem

`docs/plan.md` is the plan index: a lightweight registry that orients an agent or contributor to current work. Its most frequent question is:

```text
What is active, what is blocked, and what is the next handoff?
```

The current shape answers that question, but it also keeps a growing `Done` section in the same common-read file. The current `Done` section already contains roughly 75 dense entries and grows by one entry per completed change. When an agent reads the first portion of the file to orient, it receives a small amount of live state and a large amount of completed-plan history it usually does not need.

This violates the index principle:

```text
An index should answer the reader's most frequent question first and cheaply.
Its common-read size should scale with active work, not accumulated history.
```

The current `Done` section is useful provenance, but it is append-only history. It should remain recoverable, but it should not dominate the file used for routine orientation.

The approved plan-index lifecycle spec already states that `docs/plan.md` is lifecycle bookkeeping for planned initiatives, not the body of a plan. The `plan` skill also states that `docs/plan.md` should remain an index rather than a second long-form plan body. The plan index should summarize and locate work, not restate every milestone, review, and closeout detail.

## Goals

- Keep `docs/plan.md` bounded and optimized for the live working set.
- Preserve every completed-plan entry by moving older `Done` entries to an archive, not deleting them.
- Keep `Active` and `Blocked` complete and first in `docs/plan.md`.
- Keep a bounded `Done (recent)` window in `docs/plan.md`.
- Move older completed-plan history to `docs/plan-archive.md`.
- Compress index entries to one scannable line: date, title, plan link, terminal state, and PR or disposition when available.
- Add an index policy comment so future contributors maintain the bounded shape.
- Update validation so completed plans remain locatable from either the main index or the archive.
- Preserve lifecycle semantics: moving an entry from `docs/plan.md` to `docs/plan-archive.md` does not change the plan's status, artifacts, review evidence, or completion state.

## Non-goals

- Do not delete completed plan records.
- Do not remove plan files from `docs/plans/`.
- Do not change the lifecycle state of any plan.
- Do not change milestone, review, verification, PR, or closeout semantics.
- Do not use the archive to hide active, blocked, unresolved, or ambiguous work.
- Do not convert `docs/plan.md` into a detailed plan body.
- Do not bulk-rewrite individual plan files.
- Do not change the `plan` skill's lifecycle role, milestone states, or handoff ownership in this proposal.
- Do not rely on a larger `sed` or read window as the fix.
- Do not make `docs/plan-archive.md` the first-read orientation file.

## Vision fit

fits the current vision

This proposal improves RigorLoop's artifact-first workflow by making the plan index more reliable as an orientation artifact. It preserves provenance while reducing common-read noise.

The proposal is falsified if any of the following happens:

```text
- a completed plan becomes unfindable from the plan index or archive;
- an active or blocked plan is moved out of the common-read file;
- Done history is deleted rather than archived;
- the archive split changes any plan lifecycle state;
- validators no longer detect missing or duplicate index entries;
- docs/plan.md grows with completed history instead of active work;
- index entries become too compressed to locate the owning plan.
```

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Keep the live working set first and cheap to read | in scope | Goals, Recommended direction |
| Move unbounded completed history out of `docs/plan.md` | in scope | Goals, Recommended direction |
| Preserve completed-plan provenance | in scope | Goals, Archive contract |
| Keep recent completed work visible | in scope | Done recent window |
| Compress index entries | in scope | Entry format |
| Add growth strategy to the index | in scope | Index policy |
| Avoid deleting completed plans | in scope | Non-goals, Rollout and rollback |
| Treat this as contract-touching work | in scope | Architecture impact, Next artifacts |
| Update validators if they parse `docs/plan.md` | in scope | Testing and verification strategy |
| Make recurring archival as safe as the first migration | in scope | Archive contract, Testing and verification strategy |
| Define what the common-read budget means | in scope | Archive contract, Testing and verification strategy |
| Keep the recent-window cap tunable with rationale | in scope | Archive contract, Decision log |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| `docs/plan.md` bounded index shape | core to this proposal | This is the central common-read problem. |
| `docs/plan-archive.md` completed-plan archive | core to this proposal | The archive preserves provenance while bounding the index. |
| Plan-index lifecycle spec amendment | same-slice dependency | The existing approved spec owns `docs/plan.md` lifecycle semantics. |
| Plan-index validator or artifact-lifecycle validator support | same-slice dependency | Completed plans need to remain findable after the split. |
| Migration proof for existing Done entries | same-slice dependency | The migration must prove preservation rather than deletion. |
| `skills/plan/SKILL.md` archive guidance | first-slice candidate | Skill wording should change if the spec assigns archive maintenance to plan bookkeeping. |
| Generated adapter validation after plan-skill edits | same-slice dependency | Generated public surfaces need proof only if canonical skill text changes. |
| Generated plan-index registry | deferable follow-up | This is a stronger long-term automation option, but larger than the immediate archive split. |
| CLI or scaffolding support for index/archive updates | deferable follow-up | Useful after the contract is approved and validated. |
| Bulk rewriting individual plan bodies | out of scope | The proposal preserves plan states and avoids unrelated plan-body churn. |

## Context

The same analysis frames this as the same family of problem as noisy terminal output, verbose `change.yaml`, and oversized specs: volume should scale with reader need, not accumulated work or history. For an index, the common-read need is active and blocked work; full completed history is rare forensic context.

The recommended summary/archive split is:

```text
docs/plan.md:
  Active
  Blocked
  Done (recent)
  Superseded
  pointer to archive

docs/plan-archive.md:
  Done (archive)
```

The key preservation rule is:

```text
Archive, do not delete.
```

The approved `specs/plan-index-lifecycle-ownership.md` already establishes the plan index as lifecycle bookkeeping for planned initiatives, requires one lifecycle section per planned initiative, and requires synchronization between the plan index and plan body when lifecycle state changes. This proposal extends that contract so completed-plan history can move between the common-read index and a dedicated archive without changing lifecycle state.

## Options considered

### Option 1: Keep the current single-file index

Pros:

- No schema or validation change.
- No migration work.
- All history remains in one place.

Cons:

- `docs/plan.md` continues to grow without bound.
- The common orientation read gets noisier over time.
- Completed history crowds out live state.
- Dense Done entries remain expensive to scan.

### Option 2: Delete old `Done` entries

Pros:

- Smallest `docs/plan.md`.
- No archive maintenance.

Cons:

- Destroys provenance.
- Breaks reconstructability.
- Violates artifact-first lifecycle discipline.
- Makes prior completed plans harder to audit.

This option is rejected.

### Option 3: Keep one file but move `Done` below everything else

Pros:

- Preserves all history.
- Slightly improves first-screen orientation.

Cons:

- The file still grows unbounded.
- The agent still risks reading large historical sections when using a fixed read window.
- This does not solve dense entry shape.

This is insufficient.

### Option 4: Split completed history into `docs/plan-archive.md`

Pros:

- Keeps `docs/plan.md` bounded.
- Preserves completed-plan history.
- Keeps live working set first.
- Gives validators a clear place to check archived Done entries.
- Matches the summary/transcript pattern used elsewhere.

Cons:

- Requires a contract and validator update.
- Requires one migration of older Done entries.
- Requires contributors to follow the new archive policy.

### Option 5: Generate `docs/plan.md` from a machine-readable registry

Pros:

- Strongest long-term consistency.
- Could prevent duplicate or stale entries.
- Could generate archive and live index automatically.

Cons:

- Larger mechanism than needed for this immediate problem.
- Requires new registry source-of-truth decisions.
- More implementation and migration risk.

This remains a possible follow-up.

## Recommended direction

Choose Option 4.

Split the plan index into:

```text
docs/plan.md
docs/plan-archive.md
```

Use `docs/plan.md` as the bounded live orientation file. Use `docs/plan-archive.md` as append-only completed-plan history.

### Proposed `docs/plan.md` shape

```md
# Plan index

<!--
Index policy:
- Active and Blocked are complete and first.
- Done (recent) keeps the most recent 10 completed plans.
- Older Done entries move to docs/plan-archive.md.
- Done entries are one line: date, title, plan link, terminal state, PR/disposition.
- Do not place active, blocked, unresolved, or review-needed work in the archive.
-->

## Active

- <active plan entry>

## Blocked

- <blocked plan entry or None>

## Done (recent)

Full completed history: see [Plan archive](plan-archive.md).

- <recent done entry 1>
- <recent done entry 2>

## Superseded

- <active supersession entry or None>
```

### Proposed `docs/plan-archive.md` shape

```md
# Plan archive

Completed plan history moved out of the common-read plan index.

## Done (archive)

- <archived done entry>
```

### Entry format

Active entries should be status-bearing, but not transcript-like:

```md
- [<YYYY-MM-DD Title>](plans/<file>.md) - <current milestone/state>; next: <next stage>; blockers: <none or short blocker>.
```

Example:

```md
- [2026-05-21 Compact Change Validation Metadata](plans/2026-05-21-compact-change-validation-metadata.md) - M3 resolution-needed; next: review-resolution; blockers: CVM-M3-CR1..CR3.
```

Blocked entries should use this shape:

```md
- [<YYYY-MM-DD Title>](plans/<file>.md) - blocked: <reason>; owner/next decision: <owner or artifact>.
```

Done entries should be one scannable line:

```md
- [<YYYY-MM-DD Title>](plans/<file>.md) - done; PR <# or link>; terminal state: <merged | closed | abandoned | superseded>.
```

Example:

```md
- [2026-05-20 Spec-Family Assets Progressive Disclosure](plans/2026-05-20-spec-family-assets-progressive-disclosure.md) - done; PR #80 merged.
```

Avoid dense milestone recaps such as:

```text
M1/M2/M3 closed after code review; explain-change recorded; verify passed;
PR opened; final closeout pending...
```

That detail belongs in the plan body, change metadata, review log, and PR record.

### Archive contract

The first-slice default keeps the most recent 10 `Done` entries in `docs/plan.md`. Ten is enough recent context to answer "what just shipped" without pushing Active and Blocked out of the common orientation read. The cap is advisory at the proposal stage; the spec confirms or tunes the final value. Older `Done` entries move to `docs/plan-archive.md`.

Archive when either is true:

```text
- Done (recent) exceeds 10 entries;
- docs/plan.md exceeds the common-read budget defined by the approved plan-index contract.
```

For the first slice, the common-read budget should be defined derivatively instead of as a separate line count:

```text
Active and Blocked are complete and first;
Done (recent) is at or below the approved cap;
Done entries are one-line summaries rather than milestone transcripts;
older completed history is in the archive.
```

This makes the budget enforceable by structure and avoids a brittle line-count target that drifts with the legitimate size of active work.

Use newest-first ordering in `Done (recent)` and in `Done (archive)`. Recent context is more useful than old context, and matching order keeps the two surfaces easy to compare.

Keep only active supersession context in `docs/plan.md`. Terminal superseded history moves to `docs/plan-archive.md` with the rest of terminal completed-plan history.

The `plan` skill or plan-index maintenance workflow should update both files when transitioning a plan to `Done` and when the recent window exceeds the cap. The current `plan` skill already instructs agents to update `docs/plan.md` and the plan body together when starting, replacing, transitioning, or before PR review. This proposal extends that rule to include `docs/plan-archive.md` when archival is triggered.

The initial migration proof is not enough by itself. Routine archival after the first split is the same count-conservation operation as the one-time migration. The standing validator should verify on every change touching `docs/plan.md` or `docs/plan-archive.md` that every plan file under `docs/plans/` with a terminal lifecycle state appears exactly once across `Done (recent)` and `Done (archive)`.

The validator should enforce structural shape, including per-entry one-line shape and required plan links. Code review should own semantic quality, including whether a summary is clear, truthful, and not hiding material lifecycle state.

### Plan-index contract changes

Amend the plan-index lifecycle contract with these rules:

```text
1. docs/plan.md is the common-read plan index.
2. Active and Blocked sections appear before Done history and remain complete.
3. Done history in docs/plan.md is bounded to the recent window.
4. Older Done entries live in docs/plan-archive.md.
5. Every completed plan remains locatable from either docs/plan.md or docs/plan-archive.md.
6. Active, blocked, review-requested, or resolution-needed plans do not move to the archive.
7. Index entries are summaries, not milestone transcripts.
8. Each index entry links to the owning plan file.
9. The archive is append-only except for deduplication, formatting normalization, or correcting broken links.
10. The terminal-plan conservation check runs whenever docs/plan.md or docs/plan-archive.md changes, not only during initial migration.
11. Terminal superseded history is archived; docs/plan.md keeps only active supersession context.
```

## Expected behavior changes

- `docs/plan.md` becomes bounded and focused on active orientation.
- Agents reading the first part of `docs/plan.md` reliably see all Active and Blocked work.
- Recent completed work remains visible.
- Older completed work remains recoverable in `docs/plan-archive.md`.
- Dense Done paragraphs are compressed into one-line entries.
- Validators can verify that every completed plan remains findable.
- No plan lifecycle state changes.

## Architecture impact

| Surface | Impact |
| --- | --- |
| `docs/plan.md` | Becomes bounded common-read index with recent Done window. |
| `docs/plan-archive.md` | New archive for older completed plans. |
| `skills/plan/SKILL.md` | May need updated wording to mention archive maintenance when Done exceeds the cap. |
| `specs/plan-index-lifecycle-ownership.md` | Should define the archive contract because this approved spec owns plan-index lifecycle semantics. |
| `specs/plan-index-lifecycle-ownership.test.md` | Should add migration, archive, cap, and link-preservation coverage if validator behavior changes. |
| `scripts/validate-artifact-lifecycle.py` | May need to treat `docs/plan-archive.md` as an accepted plan-index surface. |
| Plan-index validator, if present | Should validate archive references, recent-window cap, and no active work in archive. |
| Individual plan files | No direct change. |
| Adapter output | No change unless `skills/plan/SKILL.md` changes and generated skills are rebuilt. |
| CLI behavior | No change. |

## Testing and verification strategy

| Check ID | What is verified |
| --- | --- |
| `PIX-001` | `docs/plan.md` contains complete `Active` section. |
| `PIX-002` | `docs/plan.md` contains complete `Blocked` section. |
| `PIX-003` | `docs/plan.md` has a `Done (recent)` section with no more than the approved cap. |
| `PIX-004` | `docs/plan.md` links to `docs/plan-archive.md`. |
| `PIX-005` | `docs/plan-archive.md` exists when older Done entries exist. |
| `PIX-006` | Every archived Done entry links to an existing plan file. |
| `PIX-007` | Every recent Done entry links to an existing plan file. |
| `PIX-008` | No active, blocked, review-requested, or resolution-needed plan appears only in archive. |
| `PIX-009` | Every completed plan entry from the pre-migration Done list remains present in either recent Done or archive. |
| `PIX-010` | No completed plan appears in both recent Done and archive unless duplication is explicitly allowed for a transition window. |
| `PIX-011` | Done entries follow one-line compact shape and include a valid owning plan link. |
| `PIX-012` | Active entries remain status-bearing and include next stage or blocker. |
| `PIX-013` | `docs/plan.md` satisfies the structural common-read budget: complete Active/Blocked first, Done (recent) at or below cap, archive pointer present, and no milestone-transcript Done entries. |
| `PIX-014` | Archive migration preserves count and links of completed entries. |
| `PIX-015` | On every change touching `docs/plan.md` or `docs/plan-archive.md`, every plan file under `docs/plans/` with a terminal lifecycle state appears exactly once across Done (recent) and Done (archive). |

Suggested validation commands:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path docs/plan.md \
  --path docs/plan-archive.md

git diff --check --
```

If a plan-index validator exists or is added:

```bash
python scripts/validate-plan-index.py docs/plan.md docs/plan-archive.md
```

If the implementation creates change metadata:

```bash
python scripts/validate-change-metadata.py docs/changes/<change-id>/change.yaml
```

If `skills/plan/SKILL.md` changes:

```bash
python scripts/validate-skills.py skills/plan/SKILL.md
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version <version> --output-dir <tmpdir>
python scripts/validate-adapters.py --root <tmpdir> --version <version>
```

### Migration proof

Before moving entries, create a change-local migration table:

```text
docs/changes/<change-id>/plan-index-migration.md
```

It should record:

| Pre-migration entry | New location | Plan link | Terminal state | Preserved? |
| --- | --- | --- | --- | --- |
| `<entry title>` | `docs/plan.md` or `docs/plan-archive.md` | `<path>` | `<state>` | yes/no |

The migration proof should show:

```text
pre-migration Done count
post-migration Done (recent) count
post-migration Done (archive) count
sum matches pre-migration count
no broken plan links
no duplicate completed entries unless explicitly justified
```

This is the main behavior-preservation proof.

## Rollout and rollback

Rollout:

1. Approve proposal.
2. Amend the plan-index lifecycle spec or equivalent.
3. Add or update test spec and validator expectations for archive split.
4. Plan the migration.
5. Create `docs/plan-archive.md`.
6. Move older Done entries from `docs/plan.md` to archive.
7. Compact recent and archived Done entries to one-line shape.
8. Update `docs/plan.md` with index policy comment and archive pointer.
9. Update `skills/plan/SKILL.md` if required by the accepted contract, migration, and validator behavior.
10. Run plan-index, lifecycle, metadata, skill, adapter, and diff validation as applicable.
11. Code-review migration proof and semantic entry quality.
12. Explain change, verify, and hand off to PR.

Rollback:

- Move archived entries back into `docs/plan.md` from `docs/plan-archive.md`.
- Restore previous `docs/plan.md` from Git if needed.
- Remove `docs/plan-archive.md` only after confirming all entries are restored.
- Revert any validator, spec, or skill changes that depended on the archive split.
- Do not delete plan files.
- Do not change lifecycle state during rollback.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| A completed plan becomes unfindable. | Require migration proof with pre/post counts and link validation. |
| Active or blocked work is archived. | Validator and review checks reject nonterminal states in archive. |
| Done recent window grows unbounded again. | Add index policy plus validator cap. |
| Archive becomes a second noisy index. | Apply one-line entry shape to archive too. |
| Details are lost during entry compaction. | Keep details in plan files, change metadata, review records, and PRs. |
| Validator misses archive file. | Update lifecycle or plan-index validator scope to include `docs/plan-archive.md`. |
| Contributors append new Done entries to the archive incorrectly. | Explain the rule in `docs/plan.md` policy comment and `plan` skill wording. |
| Generated skills drift if `plan` skill changes. | Rebuild or validate generated skills and adapters from canonical `skills/`. |

## Open questions

None.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-22 | Treat `docs/plan.md` as a bounded common-read index. | The frequent question is active/blocked state, not full completed history. | Keep one unbounded file. |
| 2026-05-22 | Archive older Done entries instead of deleting them. | Completed history is provenance. | Delete old entries. |
| 2026-05-22 | Keep a recent Done window. | Recent completions are useful context, but the window should be bounded. | Move all Done entries to archive. |
| 2026-05-22 | Use one-line Done entries. | Index entries should locate artifacts, not restate plan bodies. | Keep dense milestone-recapping paragraphs. |
| 2026-05-22 | Treat archive split as contract-touching. | Plan index is lifecycle-owned and likely validated. | Freehand edit. |
| 2026-05-22 | Use 10 as the proposal's recent Done cap candidate. | This keeps enough recent context to answer "what just shipped" without pushing Active and Blocked out of the common orientation read. | Cap of 5; unbounded Done. |
| 2026-05-22 | Define common-read budget structurally, not as a separate whole-file line count. | Active and Blocked size can legitimately vary; the enforceable budget is complete live state first, capped recent Done, one-line summaries, and archive split. | Fixed whole-file line budget. |
| 2026-05-22 | Sort `Done (recent)` and `Done (archive)` newest-first. | Newest-first matches the value of recent context and keeps archive comparison straightforward. | Oldest-first archive ordering. |
| 2026-05-22 | Keep only active supersession context in `docs/plan.md`; archive terminal superseded history. | The common-read index should carry live replacement context, not historical terminal supersessions. | Keep all superseded history in the common-read index. |
| 2026-05-22 | Enforce entry structure with validators and semantic entry quality with code review. | Link and one-line shape are structural; truthful, useful summaries need reviewer judgment. | Validator-only semantic quality; code-review-only structural enforcement. |
| 2026-05-22 | Sequence first-slice implementation as spec and validator first, index migration next, and plan-skill wording if needed. | The migration should run against the accepted contract and proof mechanism before contributor guidance changes are finalized. | Migrate first; update plan skill before validator support. |

## Next artifacts

```text
spec amendment: plan-index lifecycle ownership / archive contract
spec-review
test-spec if validator behavior changes
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- `specs/plan-index-lifecycle-ownership.md`
- `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/proposal-review-r1.md`

Candidate future proposals after the first slice:

- Generated plan-index registry if archive maintenance remains manual.
- Plan-index validator if no dedicated validator exists after the archive split.
- Compact lifecycle index shape across other index files.
- CLI or scaffolding support that updates `docs/plan.md` and the archive automatically.

## Readiness

Accepted; downstream spec amendment drafted at `specs/plan-index-lifecycle-ownership.md`.

## Core invariant

```text
docs/plan.md is the bounded live plan index.

It should answer active and blocked state first and cheaply. Completed history is
preserved, but older Done entries move to docs/plan-archive.md so common-read
size scales with active work, not total project history.

No completed plan may become unfindable.
```
