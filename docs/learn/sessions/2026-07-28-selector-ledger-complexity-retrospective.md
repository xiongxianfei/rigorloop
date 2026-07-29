# Learn Session: Selector Ledger Complexity Retrospective

## Result

- Skill: learn
- Status: captured; candidate classifications awaiting contributor confirmation
- Artifacts changed: this session record only
- Open blockers: contributor confirmation is required before changing the specification
- Next stage: none by default
- Session path: `docs/learn/sessions/2026-07-28-selector-ledger-complexity-retrospective.md`
- Lessons captured: 0 confirmed durable lessons
- Follow-ups: candidate specification simplification; not routed

## Frame

- Trigger: explicit maintainer question asking why the draft specification has so many selectors and whether every selector is necessary.
- Trigger type: explicit maintainer request / contributor observation / repeated specification-review findings.
- Date: 2026-07-28
- Scope:
  - the normative amendment registry in `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`;
  - selector-related findings `SLA-SR5` and `SLA-SR8`;
  - the exact-selector contract in `specs/single-bounded-review-fix-workflow-automation.md`;
  - the four source specifications named by the registry.
- Evidence in scope:
  - disposition counts by source specification and category;
  - the registry's default rule for unlisted selectors;
  - the review evidence that led to the selector ledger;
  - `BRF-R098e` through `BRF-R098h` and their acceptance surfaces.
- Explicit exclusions:
  - no amendment to the draft specification;
  - no change to reciprocal notices or source specifications;
  - no closure or reopening of existing review findings;
  - no workflow, validator, or skill policy change;
  - no claim that a mechanical count proves which individual rebound rules are semantically affected.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-07-27-boundary-first-proof-review-finding-retrospective.md`
- Session record path: `docs/learn/sessions/2026-07-28-selector-ledger-complexity-retrospective.md`

## Observe

### O1 - The selector volume is a review-resolution mechanism, not core feature behavior

The first review found that the draft used broad precedence language and left exact normative conflicts for implementation to decide. Its safe resolution path requested a closed selector-level disposition ledger. The second review confirmed that the resulting tables contained 323 valid existing selectors.

The large ledger therefore came from solving exact cross-spec precedence under the current automation contract. The core feature does not intrinsically need 323 selector references to express:

```text
governed artifacts are immutable to peer and downstream stages
mutable workflow state lives in change-local metadata
review stages record settlement without editing reviewed content
```

### O2 - Thirty-one `preserved-unchanged` entries are redundant under the draft's own default

The registry says:

```text
Selectors not listed remain unchanged.
```

It nevertheless lists 31 selectors as `preserved-unchanged`:

| Source specification | `preserved-unchanged` |
| --- | ---: |
| `artifact-status-lifecycle-ownership.md` | 6 |
| `single-source-of-workflow-state.md` | 10 |
| `rigorloop-workflow.md` | 0 |
| `single-bounded-review-fix-workflow-automation.md` | 15 |
| **Total** | **31** |

These entries add volume without changing precedence. Under a delta-ledger model, omission already communicates the same result.

### O3 - Most of the ledger is `preserved-rebound`, and that category is too broad to accept mechanically

The full disposition count is:

| Disposition | Selectors |
| --- | ---: |
| `superseded` | 64 |
| `preserved-rebound` | 228 |
| `preserved-unchanged` | 31 |
| **Total** | **323** |

The source totals are:

| Source specification | Selectors |
| --- | ---: |
| `artifact-status-lifecycle-ownership.md` | 46 |
| `single-source-of-workflow-state.md` | 106 |
| `rigorloop-workflow.md` | 64 |
| `single-bounded-review-fix-workflow-automation.md` | 107 |

Some rebound entries are necessary because their live subject genuinely moves from artifact-local status, active-plan handoff, or parent authorization to a change-local owner or target consent. Other rows group broad families of review, evidence, validation, migration, and reporting requirements merely because they operate near the changed state.

Selector existence and uniqueness checks cannot prove that all 228 selectors change subject. A requirement-by-requirement semantic audit is required before retaining them.

### O4 - The current approved automation contract makes a chosen affected set exact, but it does not require every adjacent selector to be affected

`BRF-R098e` requires a disposition for every selector declared affected and rejects ambiguity, duplicates, and obsolete subjects. This is a valuable fail-closed rule once the affected set is correct.

It does not require the new specification to classify every selector in every related specification. The new specification expanded the affected set by treating broad requirement families as rebound. The exactness requirement and the breadth of the chosen set are separate decisions.

### O5 - The smallest safe simplification is a changed-selector delta ledger

A simpler contract can retain deterministic precedence:

1. List every truly `superseded` selector.
2. List only a `preserved-rebound` selector whose normative subject, owner, input, output, or authorization basis actually changes.
3. Omit `preserved-unchanged`; omission means unchanged.
4. Keep exact public aliases only when their behavior or state binding changes.
5. Validate uniqueness, existence, reciprocal pointers, and absence of known conflicting legacy authorities.

This keeps exact change control without restating the unaffected contract.

If the remaining rebound set is still large after semantic audit, replacing selector-level precedence with source-level amendment clauses would require an explicit amendment to `BRF-R098e` through `BRF-R098h`. It must not be achieved by restoring open-ended phrases such as “where conflicting.”

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | `observation` | `observation` | none | repository evidence | The review records establish why the ledger was introduced. |
| O2 | `artifact-update` | pending confirmation | draft specification | pending contributor confirmation | Removing unchanged entries is a behavior-preserving specification simplification. |
| O3 | `observation` | `observation` | semantic audit before revision | repository evidence | Counts prove concentration in rebound entries but not each entry's necessity. |
| O4 | `observation` | `observation` | none | approved contract and draft registry | Exactness applies to the affected set; it does not determine the set's breadth. |
| O5 | `artifact-update` | pending confirmation | draft specification, then `spec-review` | pending contributor confirmation | The delta-ledger approach changes the specification's amendment and validation contract. |

## Route

No derivative routing was performed because contributor confirmation is not yet available for the candidate specification updates.

No topic file, specification, review record, reciprocal notice, workflow, validator, or skill was changed by this session.
