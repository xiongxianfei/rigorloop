# Spec and Test-Spec Structural Hygiene

## Status

accepted

## Priority order

```text
1. preserved normative content
2. improved navigability
3. encoded growth strategy
4. coupled spec/test-spec parity
```

Token cost is not a driver for this proposal. The amendment is navigation-only.

## Problem

`specs/skill-contract.md` is 949 lines at the proposal base and has 45 R-family clauses, 35 acceptance criteria, and 16 examples. `specs/skill-contract.test.md` is 1351 lines and mirrors every spec amendment with test coverage. Both files are internally well-formed.

Both files are now large enough that readers cannot easily locate which rules or tests apply to their current slice of work without scanning. The spec names three slice labels (`baseline normalization first slice`, `published-skill design pilot`, and `assets-first plan pilot`), but the Requirements section, acceptance criteria, and the test spec's Test cases section do not group clauses by slice. A reader landing on R44 cannot tell which slice it belongs to without consulting the slice-terminology section and parent proposals.

Concretely:

- The Requirements section is a single flat sequence from R1 to R45.
- The acceptance criteria are a single flat list.
- The test spec's 36 test-case subsections are a single flat sequence.
- The test spec's Acceptance criteria coverage map mirrors the spec's flat list.
- Cross-references survive because IDs are stable, but the structural correspondence is invisible to a reader.

Recent informal spec-review recorded OBS-1 and OBS-2 against the spec for these navigability gaps. The findings were non-blocking and deferred to the next amendment. This proposal is that amendment.

The cost being addressed is navigability, not correctness. The fix is correspondingly light: regroup existing content under new headers without changing any clause, ID, criterion, or test case.

## Goals

- Group R-clauses in `specs/skill-contract.md` by slice with H3 subsection headers inside the Requirements section.
- Group acceptance criteria in `specs/skill-contract.md` by slice with H3 subsection headers.
- Add a short navigation index near the top of `specs/skill-contract.md` mapping each slice label to its R-clause band.
- Mirror the slice grouping in `specs/skill-contract.test.md` Acceptance criteria coverage map and Test cases section.
- Codify the structural-hygiene practice as a small normative addition so future amendments inherit the discipline.
- Preserve every clause ID, every acceptance criterion text, every test-case ID, and every cross-reference unchanged.

## Non-goals

- Do not change any R-clause text, R-clause ID, or R-clause numbering.
- Do not change any acceptance criterion text or position within its slice.
- Do not change any test-case ID, body, fixture, or coverage mapping.
- Do not add, remove, or merge any clauses, criteria, or test cases.
- Do not change example text or example IDs.
- Do not split `specs/skill-contract.md` or `specs/skill-contract.test.md` into multiple files.
- Do not push operational detail, such as R36g-R36j or R45b filenames, into test-spec or plan in this proposal.
- Do not modify any skill, adapter, validator, or build script.
- Do not change cross-references between spec clauses, acceptance criteria, examples, or test cases.
- Do not weaken any normative requirement.
- Do not bundle this work with content amendments. If a content change is identified during this work, record it as a follow-up proposal instead of absorbing it.

## Vision fit

fits the current vision

`VISION.md` commits RigorLoop to making artifacts easier to inspect, reason about, validate, and maintain. A normative contract that is large but ungrouped imposes a hidden cost on every reader who consults it. This structural-hygiene amendment closes that cost without changing what the contract says.

The proposal is falsified if the restructuring causes any of:

```text
- a clause ID change, renaming, or renumbering;
- a clause text edit beyond whitespace and header placement;
- a missing cross-reference after restructuring;
- a structural validator failure introduced by the restructuring;
- a test-case body or coverage mapping change;
- an apparent contract weakening detected by spec-review or downstream stages.
```

Navigation improvements that introduce any of these failures would ship content changes under a hygiene label, which is exactly the failure mode this proposal exists to prevent.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Make the spec easier to navigate | in scope | Goals, Recommended direction |
| Make the test spec consistent with the regrouped spec | in scope | Goals, Recommended direction |
| Avoid changing normative content during hygiene work | in scope | Non-goals, Vision fit falsifier |
| Codify the practice for future amendments | in scope | Recommended direction, Scope budget |
| Avoid splitting either file into multiple files | out of scope | Non-goals |
| Push operational detail downstream, including R36g-R36j and R45b | deferred follow-up | Non-goals, Deferred follow-up candidates |
| Apply structural fingerprint discipline to specs themselves | deferred follow-up | Deferred follow-up candidates |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Add navigation index and slice grouping to `specs/skill-contract.md` | core to this proposal | This is the primary navigability change. |
| Mirror grouping in `specs/skill-contract.test.md` | same-slice dependency | Spec and test-spec structure are coupled by cross-references and coverage maps. |
| Add a growth-strategy clause | core to this proposal | The proposal intentionally codifies future structural hygiene expectations. |
| Group the Examples section by slice | open question | Examples are named in the navigation index, but the proposal has not yet settled whether their section also receives slice headers. |
| Split the spec or test spec into multiple files | separate proposal | Splitting is an ownership-boundary decision, not a navigation-only edit. |
| Move operational details from spec into downstream artifacts | separate proposal | That is a content and ownership change, not structural hygiene. |
| Add structural-fingerprint enforcement for specs | separate proposal | This would create new validation behavior and should not ride with a navigation-only amendment. |

## Context

- `specs/skill-contract.md` has absorbed four substantive amendments in roughly two weeks.
- `specs/skill-contract.test.md` has mirrored every amendment with test coverage.
- The spec's prior informal spec-review recorded OBS-1, grouping requirements by slice, and OBS-2, grouping acceptance criteria by slice, as non-blocking observations to be addressed in the next amendment.
- The spec's Slice terminology section already names three slice labels and three R-clause bands.
- The test spec's structure currently mirrors the spec's flat structure rather than its slice structure.
- The user's draft named `specs/skill-contract_test.md`; this proposal corrects that to the repository's canonical `specs/skill-contract.test.md` filename.
- Three substantive amendments are currently in flight or recent: the assets-first plan pilot, downstream skill normalization for review-class skills, and the published-skill design plan family rollout. This proposal touches only spec and test-spec structure.

## Options considered

### Option 1: Do nothing; defer hygiene indefinitely

Leave `specs/skill-contract.md` and `specs/skill-contract.test.md` as-is; revisit only if a maintainer raises a blocking concern.

Pros:

- Zero immediate coordination.
- Zero edit risk.

Cons:

- Navigability cost compounds with every future amendment.
- OBS-1 and OBS-2 remain unaddressed.
- Future maintainers landing on the spec face an undifferentiated file.

### Option 2: Direct implementation; skip the proposal stage

Edit `specs/skill-contract.md` and `specs/skill-contract.test.md` directly to apply the structural changes without a proposal.

Pros:

- Fastest path.
- Smallest immediate effort.

Cons:

- Skips the workflow contract for direction-setting spec amendments.
- Leaves no proposal-stage audit trail.
- Sets a precedent that small structural changes can bypass the gate.

### Option 3: Plan-only; skip the proposal but write a plan

Treat the direction as already decided and write only a plan.

Pros:

- Plan-review still gates execution.
- Less overhead than a proposal.

Cons:

- Plans execute settled direction; this direction should be recorded before execution.
- Plan-review evaluates sequencing, not whether the direction is the right one.

### Option 4: Proposal-first; restructure both files together in one slice

Write this proposal. Pair `specs/skill-contract.md` and `specs/skill-contract.test.md` in one amendment because their structures are coupled. Execute through the normal review and planning chain.

Pros:

- Records the decision in the right place.
- Preserves the workflow precedent for spec-contract amendments.
- Couples the spec and test-spec restructuring so cross-references stay aligned.
- Allows the growth-strategy practice to become part of the contract.

Cons:

- Requires more lifecycle stages than direct implementation.
- Requires proposal-review before the amendment proceeds.

### Option 5: Split the spec into multiple files

Split `specs/skill-contract.md` into a root spec plus child specs for each slice. Apply the same pattern to the test spec.

Pros:

- Strongest navigability improvement.
- Each child spec stays smaller.

Cons:

- Premature while ownership remains clear.
- Touches downstream references and contributor expectations.
- Much higher coordination cost than the observed problem requires.

## Recommended direction

Choose Option 4.

It is the smallest change that resolves the navigability cost without violating the spec's own amendment discipline. Option 5 remains available as a future proposal if ownership pain develops; this amendment does not block that future direction.

Concrete edits to `specs/skill-contract.md`:

| Change | Description |
|---|---|
| Add navigation index | Insert a short subsection after Glossary mapping each slice label to its R-clause band, example range, and parent proposal reference. |
| Group Requirements by slice | Add H3 headers inside the Requirements section: `### Foundational (R1-R7)`, `### Baseline normalization first slice (R8-R26)`, `### Published-skill design pilot (R27-R36)`, `### Assets-first plan pilot (R37-R45)`. Place each existing R-clause under its corresponding header without changing clause text, ID, or order. |
| Group Acceptance criteria by slice | Add the same four H3 headers inside the Acceptance criteria section. Place each existing acceptance criterion under its corresponding header without changing criterion text or order. |
| Add growth-strategy clause | Add a short subsection under Goal and context titled `Spec growth strategy` stating the per-amendment structural-hygiene convention and the splitting trigger. |

Concrete edits to `specs/skill-contract.test.md`:

| Change | Description |
|---|---|
| Group Test cases by slice | Add H3 headers inside the Test cases section matching the spec's four slice groups. Place each existing test-case subsection under its corresponding header without changing any test-case ID, body, or coverage mapping. |
| Group Acceptance criteria coverage map by slice | Add the same four H3 headers inside the Acceptance criteria coverage map section. Preserve every existing coverage row unchanged. |
| Group Requirement coverage map | Mirror the slice grouping in the Requirement coverage map unless spec-review identifies a clearer parity structure. |

Candidate navigation index:

```text
## Spec navigation

This spec covers four concerns, organized by slice:

| Slice | Clause band | Examples | Parent proposal |
|---|---|---|---|
| Foundational | R1-R7 | E1, E3 | Skill Contract Optimization |
| Baseline normalization first slice | R8-R26 | E1, E2, E4, E5, E6, E7 | Single Workflow Lane |
| Published-skill design pilot | R27-R36 | E8-E12 | Published Skill Design Contract |
| Assets-first plan pilot | R37-R45 | E13-E16 | Assets-First Progressive Disclosure Pilot |

Cross-cutting glossary entries appear in the Glossary section.
Slice terminology disambiguation appears in the Slice terminology section.
```

Candidate growth-strategy clause:

```text
## Spec growth strategy

This spec amends through accretion: each accepted amendment adds an
R-clause band to a single file rather than splitting the file. Accretion
is sustainable while ownership remains clear and the file remains
navigable.

Structural hygiene MUST be applied per-amendment when this spec exceeds
~1200 lines or has absorbed more than ~6 slice families. Hygiene work
groups clauses by slice, adds navigation aids, and prunes stale cross-
references. Hygiene work MUST NOT change clause text, ID, or
numbering.

Splitting this spec into multiple files MUST be pursued via a separate
proposal that defends the ownership boundary along which the split
occurs. Splits MUST NOT happen as part of a content amendment.
```

The exact thresholds may be revised at spec-amendment time. The principle stands either way: hygiene is per-amendment; splits require their own proposal.

## Expected behavior changes

- A reader landing on `specs/skill-contract.md` can locate any slice's R-clauses, acceptance criteria, and examples faster.
- A reader landing on `specs/skill-contract.test.md` can locate any slice's test cases faster.
- A future maintainer drafting a new amendment can find the correct R-clause band to extend.
- The growth-strategy clause provides explicit guidance for when to apply hygiene and when to propose a split.
- No clause content, criterion content, test-case body, validator behavior, or downstream artifact reference changes.

## Architecture impact

| Surface | Impact |
|---|---|
| `specs/skill-contract.md` | Headers, navigation index, and growth-strategy clause added; existing normative content otherwise unchanged. |
| `specs/skill-contract.test.md` | Headers added; existing test cases and coverage rows otherwise unchanged. |
| `scripts/validate-skills.py`, `scripts/test-skill-validator.py` | No change. |
| `scripts/build-skills.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py` | No change. |
| Adapter outputs under `dist/adapters/` | No change. Specs are not shipped to adopters. |
| Skill files under `skills/` | No change. |
| Cross-references from other artifacts to spec clauses | No change. IDs are preserved. |

## Testing and verification strategy

| Level | What is verified | How |
|---|---|---|
| Content preservation | No R-clause text, ID, or order changed | Diff before and after; every R-clause line appears unchanged except for whitespace and header placement. |
| Acceptance criterion preservation | No acceptance criterion text or order changed | Diff discipline applied to the acceptance criteria section. |
| Test-case preservation | No test-case ID, body, or coverage mapping changed | Diff discipline applied to the test spec. |
| Cross-reference integrity | Every reference to an R-clause from another artifact still resolves | Search across `docs/`, `skills/`, and `specs/` for R-clause references; confirm all resolve to unchanged IDs. |
| Navigation index correctness | Every R-clause band in the index correctly enumerates its slice's clauses | Manual cold-read and spec-review. |
| Growth-strategy readability | The clause states the threshold, per-amendment hygiene practice, and split-via-proposal rule clearly | Cold-read and spec-review. |
| Structural validation | Existing validators continue to pass on touched lifecycle artifacts | Run the repo-owned explicit-path validation selected by the active plan or, before a plan exists, focused lifecycle and diff hygiene checks for the proposal. |

## Rollout and rollback

Rollout:

1. Review this proposal through `proposal-review`.
2. Amend `specs/skill-contract.md` with slice grouping, a navigation index, and the growth-strategy clause.
3. Run `spec-review`.
4. Amend `specs/skill-contract.test.md` with mirrored grouping and any approved coverage-map grouping.
5. Plan and plan-review the amendment execution if required by the workflow state at that point.
6. Implement the approved structural edits to both files.
7. Code-review verifies content preservation through diff discipline.
8. Verify cross-references and existing validators.
9. Prepare PR handoff.

The plan covers implementation execution and code-review handoff. Spec and test-spec amendments are drafted before planning because their structures are small and coupled; the plan does not redo the authoring stages.

Rollback:

- Both files have prior versions retrievable from Git.
- No downstream artifact references the file structure; downstream references rely on clause IDs.
- Reverting either file restores prior structure without affecting runtime behavior.
- If the growth-strategy clause is rolled back, no orphaned implementation dependency remains because nothing yet depends on it.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| A clause is silently moved to the wrong slice during regrouping | Prepare a mapping table before edits; code-review verifies the mapping. |
| A cross-reference breaks because a clause appears under a different header | Preserve all IDs; verification searches for R-clause references and confirms resolution. |
| The navigation index drifts from actual clause bands | Make the index part of the spec; future spec-review checks it during amendments. |
| The growth-strategy thresholds are wrong | Treat thresholds as reviewable in the spec amendment; the principle can be accepted even if the exact numbers change. |
| Scope creeps into content edits | Keep non-goals explicit; record any content improvements as deferred follow-up proposals. |
| The two in-scope files diverge structurally | Treat spec and test-spec grouping as the same slice and review them together. |

## Open questions

- What exact threshold numbers belong in the growth-strategy clause? Candidate: 1200 lines or 6 slice families, whichever comes first.
- Should the Requirement coverage map in the test spec be grouped by slice, or are Test cases and Acceptance criteria coverage map sufficient? Candidate: group the Requirement coverage map too for parity.
- Should the navigation index include cross-cutting concerns such as Glossary, Slice terminology, Edge cases, and Non-goals, or only the R-clause bands? Candidate: R-clause bands only.
- Should the growth-strategy clause apply to all RigorLoop specs or only to `skill-contract.md`? Candidate: apply per-spec when a spec exceeds the threshold.

None of these block proposal-review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-19 | Treat structural hygiene as proposal-stage work | Spec amendments by precedent go through proposal-review; skipping the gate would set the wrong precedent. | Direct implementation; plan-only |
| 2026-05-19 | Pair spec and test-spec restructuring in one proposal | The two files are coupled by cross-references and coverage maps. | Sequential proposals |
| 2026-05-19 | Forbid content changes in the hygiene amendment | Bundling content changes with structural changes would mix scope. | Allow incidental content cleanup |
| 2026-05-19 | Codify the growth-strategy practice as a normative addition | Without codification, future maintainers must rederive the practice. | One-time hygiene pass without codification |
| 2026-05-19 | Defer spec splitting to a separate future proposal | Splits are ownership-driven, not size-driven; ownership is still clear. | Split now |

## Next artifacts

```text
proposal-review
spec amendment: specs/skill-contract.md
spec-review
test-spec amendment: specs/skill-contract.test.md
plan
plan-review
implementation milestones for spec and test-spec structure
code-review
explain-change
verify
pr
```

## Deferred follow-up candidates

- Proposal to push operational detail, including R36g-R36j and R45b filenames, from spec into test-spec or plan artifacts.
- Proposal to apply structural-fingerprint discipline to specs themselves.
- Proposal to extend slice-based grouping to other RigorLoop specs exceeding the growth-strategy threshold.
- Proposal to split `specs/skill-contract.md` if and when ownership pain develops.
- Proposal to add a closed-enum verb set for specs, analogous to COPY/READ/RUN in skill resource maps.

## Follow-on artifacts

- Proposal-review: [proposal-review-r1](../changes/2026-05-19-spec-and-test-spec-structural-hygiene/reviews/proposal-review-r1.md).
- Spec amendment: [Skill Contract](../../specs/skill-contract.md).

## Readiness

Accepted after `proposal-review-r1`. Ready for `specs/skill-contract.md` amendment and `spec-review`.

## Core invariant

```text
Structural hygiene amendments change navigation, never content.

Every R-clause keeps its number. Every acceptance criterion keeps its text.
Every test case keeps its ID and body. Every cross-reference resolves
unchanged.

The proposal's success criterion is that a reader can find any slice's
contract surfaces faster after the amendment, without any downstream
artifact noticing the spec changed.
```
