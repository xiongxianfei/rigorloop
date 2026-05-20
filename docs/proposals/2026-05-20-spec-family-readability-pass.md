# Proposal: Spec-Family Readability Pass

## Status

accepted

Accepted after clean `proposal-review` round 2.

## Depends on

This proposal depends on [Test-Spec Contract Normalization](./2026-05-20-test-spec-contract-normalization.md) landing first. That proposal brings `test-spec` up to the published-skill design contract with front matter, a Workflow role block, an output skeleton, and surfaced stop conditions.

Dependency status: satisfied for proposal authoring because PR #77 merged to `main` before this proposal branch was created. Implementation still waits for proposal review, spec review if triggered, plan, plan review, and the plan's explicit confirmation that the normalized `test-spec` baseline is present.

Applying readability to a still-non-compliant `test-spec` would mix presentation work with leftover compliance gaps.

## Problem

After `test-spec` normalization lands, all three spec-family skills, `spec`, `spec-review`, and `test-spec`, share the same contract baseline. They still carry readability gaps that are presentation-only:

- `spec` lists required sections as a run-on prose list.
- `spec` and `spec-review` fence some closed enums in their skeletons, but narrate others in prose.
- `test-spec` has a required-sections list that is numbered prose and status enums that are not fenced.
- The three skills do not yet share a consistent section order, so a reader moving between them re-orients each time.

With RigorLoop in external use, the installed skill is the contract a real adopter reads. Prose enumerations and narrated enums impose a hidden scanning cost on every adopter who inspects these skills.

## Goals

- Tabulate prose enumerations across all three skills: required-section lists, review-dimension lists, and test-case coverage expectations.
- Fence remaining closed enums so each enum's values appear once in one authoritative block.
- Align section ordering across the three skills so they read as one family.
- Preserve every rule, enum value, stop condition, output obligation, and lifecycle boundary unchanged.

Priority order:

```text
1. preserved skill output quality
2. spec-family readability
3. cross-skill consistency
```

Token cost is not a driver. This proposal changes presentation only.

## Non-goals

- Do not change any normative rule, enum value, stop condition, output obligation, or lifecycle boundary in any of the three skills.
- Do not change any skill's routing description behavior.
- Do not add, remove, or reorder any required section's content; only its presentation and position relative to the family convention may change.
- Do not introduce `assets/`, `references/`, or `scripts/` packaging. Packaging for the spec family is a separate follow-on.
- Do not resolve cross-skill duplicated blocks such as artifact placement, evidence collection, or full-file read guidance. That is the deferred build-time partials concern.
- Do not change the readability of the artifacts these skills produce. The published-skill design contract governs artifact output skeletons; artifact-output readability is a separate concern.
- Do not retroactively rewrite generated adapter archives.

## Vision fit

fits the current vision

`VISION.md` commits RigorLoop to making artifacts easier to inspect, reason about, validate, and maintain. With external adopters present, the installed skill is the contract a real user reads. Prose enumerations and narrated enums impose a hidden cost on every adopter who inspects these skills. This pass closes that cost without changing what any skill does.

The proposal is falsified if the readability pass causes any of:

```text
- a normative rule, stop condition, or output obligation changes meaning;
- a closed enum loses or gains a value during fencing;
- a lifecycle boundary is weakened or dropped;
- any of the three skills produces a different verdict, structure, or
  required-section coverage on a representative input;
- routing behavior changes.
```

Readability gains do not offset any of these failures.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Make the `spec` skill readable | in scope | Goals, Recommended direction |
| Make the `spec-review` skill readable | in scope | Goals, Recommended direction |
| Make the `test-spec` skill readable | in scope | Goals, Recommended direction |
| Make generation and testing specifications readable, interpreted as skill readability | in scope | Goals |
| Make generation and testing specifications readable, interpreted as produced-artifact readability | deferred follow-up | Non-goals, Scope budget, Follow-on artifacts |
| Apply assets or references packaging to the spec family | deferred follow-up | Non-goals, Scope budget |
| Resolve cross-skill duplicated blocks | deferred follow-up | Non-goals, Scope budget |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Tabulate `spec` required-section prose | core to this proposal | This is one of the direct readability gaps. |
| Tabulate `spec-review` review dimensions | core to this proposal | This makes review verdict guidance scannable without changing verdict values. |
| Tabulate `test-spec` required sections and coverage expectations | core to this proposal | This is the readability half intentionally deferred by the normalization proposal. |
| Fence remaining closed enums in `spec`, `spec-review`, and `test-spec` | core to this proposal | The family should expose enum values once in authoritative fenced blocks. |
| Align section ordering across the three skills | core to this proposal | Cross-skill consistency is one of the stated goals, subject to behavior parity. |
| Regenerate or validate current adapter output from canonical `skills/` | same-slice dependency | Canonical skill changes should be reflected in current generated adapter output unless the plan records an explicit deferral. |
| Apply assets, references, or scripts packaging to the spec family | separate proposal | Packaging has different mechanics and risk from presentation-only readability. |
| Resolve duplicated shared blocks through build-time partials | separate proposal | This changes the skill authoring mechanism and should not be bundled with presentation edits. |
| Improve readability of produced spec or test-spec artifacts | separate proposal | This changes produced artifacts rather than the skill text itself. |

## Context

This proposal is the second of a two-proposal sequence. Normalization came first through [Test-Spec Contract Normalization](./2026-05-20-test-spec-contract-normalization.md). This proposal applies consistent readability treatment once all three spec-family skills share the same structural baseline.

The prior unified proposal bundled normalization and readability. Review feedback identified that as scope mixing and recommended splitting the work. This proposal is the readability half of that split.

`spec` and `spec-review` were normalized earlier. `test-spec` was normalized by PR #77. After that merge, all three skills have enough shared structure for a coordinated readability pass.

## Normalized baseline gate

Before implementation begins, the plan must confirm that `skills/test-spec/SKILL.md` contains the normalized baseline from Test-Spec Contract Normalization:

| Check | Required state |
|---|---|
| Front matter | Includes `version` and `schema-version`. |
| Workflow role | Present and names upstream, downstream, and must-not-claim boundaries. |
| Stop conditions | Surfaced as a visible section. |
| Output skeleton | Fenced and reflects the existing required test-spec shape. |
| Behavior-preservation evidence | Normalization review is closed or explicitly accepted. |

If any item is absent, this proposal stops and routes back to normalization resolution instead of applying readability changes.

## Options considered

### Option 1: Do nothing

Leave the readability gaps after normalization.

Pros: zero effort and no immediate regression risk.

Cons: prose enumerations and narrated enums persist; the family reads inconsistently; adopter scanning cost compounds.

### Option 2: Readability per skill, three separate passes

Tabulate and fence each skill in its own proposal.

Pros: smallest individual changes.

Cons: three proposals for one consistent treatment; the family-consistency goal is hard to achieve piecemeal; lifecycle overhead is larger than the work warrants.

### Option 3: One readability pass across all three skills

Tabulate, fence, and align section ordering across `spec`, `spec-review`, and `test-spec` in one proposal, after normalization.

Pros: the family ends consistent in one pass; shared section ordering is achievable; review can compare the three skills side by side; the change remains presentation-only.

Cons: touches three skill files in one change, mitigated by per-skill proof and behavior parity for each skill.

## Recommended direction

Choose Option 3.

Apply readability across all three skills in one pass, after normalization. Treat this as presentation-only work with behavior parity verified per skill.

Concrete changes:

| Change | Applies to | Description |
|---|---|---|
| Tabulate required-section lists | `spec`, `test-spec` | Convert run-on or numbered prose lists to tables with section name and applicability guidance. Preserve the same sections and content. |
| Tabulate review dimensions | `spec-review` | Convert the dimension list to a table with the same verdict guidance. |
| Tabulate test-case coverage expectations | `test-spec` | Convert coverage expectation prose to a scannable table while preserving each obligation. |
| Fence remaining closed enums | all three | Fence settlement result in `spec`, review-dimension verdicts in `spec-review`, and status enums in `test-spec`, using the existing values. |
| Align section ordering | all three | Apply a shared section order where it improves scanning without changing rule priority or meaning. |

This proposal will not attempt:

```text
- normative rule, enum value, stop condition, or output obligation changes;
- routing or description changes;
- packaging through assets, references, or scripts;
- build-time partials or duplicated-block resolution;
- changes to produced artifacts' readability.
```

## Section-ordering boundary

The family section order is a readability convention, not a behavior override.

Shared section-order decision: align to the order `spec` and `spec-review` already share, then fit normalized `test-spec` into that family order.

Recommended shared order:

```text
1. Front matter
2. Purpose / short skill summary
3. Workflow role
4. Stop conditions / blocking conditions
5. Inputs and source-of-truth handling
6. Operating procedure / rules
7. Required artifact sections or review dimensions
8. Closed enums
9. Output expectations / fenced output skeleton
10. Validation and preservation checks
11. Handoff / next-stage boundaries
```

The shared order does not require identical section names. Comparable sections should be easy to find across the family.

Per-skill fit:

| Skill | Section-order treatment |
|---|---|
| `spec` | Keep its existing family shape; tabulate required sections; fence remaining enums; keep output expectations and handoff boundaries intact. |
| `spec-review` | Keep its existing family shape; tabulate review dimensions; fence verdict enums; keep review status, material-finding, and recording boundaries intact. |
| `test-spec` | After normalized baseline confirmation, keep surfaced stop conditions early, then operating procedure, required test-spec sections, closed enums, output skeleton, validation, and handoff. |

Behavior-significant order must be preserved unless the preservation matrix records why the move is safe.

Stop conditions, must-not-claim boundaries, and validation obligations must remain early enough that a cold reader sees them before following the normal output procedure.

Section-order alignment is best effort. It must yield to behavior parity, stop-condition visibility, and lifecycle claim-boundary clarity.

If strict family ordering conflicts with behavior clarity for a skill, prefer behavior clarity and record the exception with:

- skill;
- section;
- family-order expectation;
- chosen placement;
- reason the exception preserves behavior clarity.

## Enum authority map

For each changed skill, implementation must record an enum authority map:

| Skill | Enum | Existing source | Authoritative destination | Values | Duplicate handling |
|---|---|---|---|---|---|
| `spec` | settlement result | prose | fenced enum block | exact values from the current skill | later prose references the block |
| `spec-review` | review-dimension verdict | prose | fenced enum block or table authority | `pass`, `concern`, `block` | table cells may reference values, not restate the full list |
| `test-spec` | status enum | prose or skeleton | fenced enum block | exact values from the normalized current skill | skeleton uses a placeholder or references the block |

Every closed enum value set must appear once in an authoritative block or table. Later instructions should reference the enum by name instead of restating the full value list.

Acceptance criteria:

```text
- No closed enum value set appears as a duplicate full list in the same skill.
- Each fenced enum has a before/after value-set proof.
```

## Content-preservation proof

For each changed skill, implementation must record a preservation matrix:

| Source content | Existing location | New location | Change type | Preservation proof |
|---|---|---|---|---|
| Required section list | prose list | table | tabulated | same section names and obligations |
| Review dimension | prose item | table row | tabulated | same dimension and verdict guidance |
| Closed enum | prose sentence or skeleton | fenced block or table authority | fenced | same value set |
| Stop condition | existing section | reordered section if moved | moved | same condition and priority |
| Output obligation | existing output guidance | unchanged or moved | moved or unchanged | same required output |

Representative-input behavior parity is required, but it supplements this matrix. It does not replace source-content preservation.

## Expected behavior changes

- A reader scanning any of the three skills finds required sections and enums in tables and fenced blocks, not long prose runs.
- The three skills share section ordering and read as one family where behavior parity allows.
- No skill produces different output on a representative input. A spec, review, or test spec generated before and after this pass is equivalent in verdict, structure, and coverage.
- No routing behavior changes.

## Architecture impact

| Surface | Impact |
|---|---|
| `skills/spec/SKILL.md` | Required sections tabulated; remaining enums fenced; section order aligned; normative content unchanged. |
| `skills/spec-review/SKILL.md` | Review dimensions tabulated; remaining enums fenced; section order aligned; normative content unchanged. |
| `skills/test-spec/SKILL.md` | Required sections tabulated; status enums fenced; section order aligned; normative content unchanged. |
| `scripts/validate-skills.py` | No intended change. |
| Adapter outputs | Current generated output should be regenerated or validated from canonical `skills/`; generated skill bodies are not hand-edited. |
| Skill packaging and build pipeline | No intended change. |

## Testing and verification strategy

| Level | What is verified | How |
|---|---|---|
| Behavior parity per skill | Each skill produces equivalent output on a representative input before and after. | Run each skill against a representative input and compare verdict, structure, and coverage. |
| Enum preservation | Every fenced enum contains exactly the values it had when narrated. | Record a before-to-after enum-preservation matrix. |
| Section-content preservation | Tabulation moves content into tables without rewording rules. | Code review checks each table cell against its prose source. |
| Section-order consistency | The three skills share the agreed section order where behavior parity allows. | Manual review across the family. |
| Adapter currency | Current generated adapter output reflects canonical skill changes or has an explicit deferral. | Run repository-owned adapter build or validation checks named by the plan. |
| Cold-read | A fresh reader can locate each skill's sections, enums, and structure without external context. | Cold-read by a non-author or reviewer acting from the installed-skill perspective. |

The plan should name the representative inputs and the exact adapter validation commands. The implementation proof must include per-skill preservation matrices for moved, tabulated, fenced, or reordered content. Representative-input behavior parity supplements that deterministic source-to-destination proof.

## Rollout and rollback

Rollout:

1. Confirm Test-Spec Contract Normalization has merged.
2. Review this proposal through `proposal-review`.
3. Write or amend the relevant spec only if proposal review or spec review identifies a contract gap.
4. Plan per-skill milestones or one milestone with per-skill proof packets.
5. Complete `plan-review`.
6. Implement readability per skill, preserving behavior.
7. Run code review with enum, section-content, and behavior-parity proof.
8. Verify validators and adapter currency from canonical `skills/`.
9. Prepare the PR.

Rollback:

- Each skill change can be reverted independently from Git history.
- Tabulation and fencing are presentation-only; reverting restores prior prose without behavior change.
- No packaged resources are added, so there is no adapter-packaging rollback surface.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Tabulation rewords a rule for the table | Tables preserve source wording as closely as possible; code review checks each cell against its prose source. |
| Fencing an enum drops or adds a value | Record an enum-preservation matrix before code review. |
| Section reordering moves a rule out of context | Reorder sections only where behavior parity and rule priority remain clear; defer risky ordering changes. |
| Three-file change blurs into uneven treatment | Use per-skill proof packets and behavior parity for each skill. |
| Work begins before normalization is truly present | Rollout begins with explicit confirmation that PR #77's normalized `test-spec` baseline is on the branch. |
| Scope creeps into packaging or duplicated-block resolution | Scope budget routes those work items to separate proposals. |

## Open questions

None.

Produced-artifact readability is deferred follow-up. This proposal covers published skill readability only. If the owner intended produced spec or test-spec artifacts rather than the skill files, that requires a separate proposal because it changes output expectations rather than published skill readability.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-20 | Split readability from normalization | Compliance and presentation work have different risk profiles; bundling was flagged as scope mixing. | Unified proposal |
| 2026-05-20 | Depend on normalization landing first | Applying readability to a non-compliant `test-spec` would mix presentation with leftover compliance gaps. | Run in parallel with normalization |
| 2026-05-20 | Use one pass across all three skills | Family consistency is achievable in one coordinated pass. | Three separate per-skill readability proposals |
| 2026-05-20 | Classify produced-artifact readability as deferred follow-up | The user's wording has both a skill-readability and produced-artifact-readability interpretation; this proposal covers published skill readability only. | Silently scope to skills only; keep artifact readability open during planning |
| 2026-05-20 | Exclude packaging and duplicated-block resolution | These mechanisms have different risk and validation surfaces. | Bundle packaging or partials here |
| 2026-05-20 | Align to the `spec` and `spec-review` family order, fitting normalized `test-spec` into that structure | The family already has a readable baseline; `test-spec` should join that order after normalization. | Invent a new order for all three skills |
| 2026-05-20 | Treat section-order alignment as best effort | Family consistency improves scanability, but it must not reorder meaning or hide lifecycle boundaries. | Hard validator-style section-order requirement |

## Next artifacts

```text
proposal-review
spec amendment only if a contract gap surfaces
spec-review when a spec amendment is created
plan
plan-review
test-spec
implementation milestones or per-skill proof packets
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

Deferred follow-up candidates are recorded in the scope budget: spec-family packaging, build-time partials for duplicated blocks, produced spec and test-spec artifact readability, and broader lifecycle skill section-ordering conventions.

## Readiness

Accepted after `proposal-review` R2. The focused spec has been drafted at `specs/spec-family-readability-pass.md`; downstream review now belongs to that spec artifact.

Implementation remains gated on spec review, plan approval, and explicit confirmation that the normalized `test-spec` baseline from PR #77 is present.

## Core invariant

```text
This pass changes presentation, never behavior.

All three spec-family skills read consistently with tabulated lists and fenced
enums. Every rule, enum value, stop condition, output obligation, and lifecycle
boundary is preserved. Each skill produces equivalent output on a representative
input after the pass as before it.
```
