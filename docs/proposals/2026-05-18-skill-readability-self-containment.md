# Proposal: Optimize Skills for User-Facing Readability and Self-Containment

## Status

accepted

Accepted after clean `proposal-review` round 3.

## Revision history

| Date | Revision | Driver |
|---|---|---|
| 2026-05-18 | Initial draft | Author |
| 2026-05-18 | Revision 1: addressed PRF-R2 and PRF-R4; acknowledged PRF-R1; contested PRF-R3 with rationale | `proposal-review` round 1 |
| 2026-05-18 | Revision 2: made output quality the primary success criterion; added falsifier, quality/clarity floors, terminology, and relationship to the accepted portability proposal | `proposal-review` quality-priority feedback |

See "Review response" section for the per-finding disposition.

---

## Problem

Users of RigorLoop receive only the installed adapter skill files (`.claude/skills/`, `.agents/skills/`, `.opencode/skills/`). They do not receive `specs/`, `schemas/`, `docs/workflows.md`, or any other repository content. For the user, **the skill is the contract** -- there is no other surface.

Today's skills do not fully honor that constraint. Specifically:

- A single skill repeats the same content within itself (e.g., the artifact-placement lookup order, the source-rank rule, evidence-collection guidance, the same enum values stated multiple times).
- Closed enums (Vision fit values, scope classifications, recording status, review verdicts) are narrated in prose rather than fenced, making them prone to silent rewording.
- Long enumerative lists (e.g., the 18 required proposal sections, the 10 review dimensions) are written as numbered prose, which is hard for a reader to scan in seconds.
- Skills mix workflow-wide context with skill-local rules without flagging which is which, leaving a user who has never read the workflow contract unsure what is binding on this skill versus the broader workflow.
- The `proposal` skill lists required sections but ships no fillable skeleton. By contrast, `proposal-review` already ships a fenced `Result` block, which is the correct artifact-first pattern.
- The maintainer has no routine practice of reading each installed skill cold -- without specs, docs, or repo context -- to verify that the skill is truly self-sufficient.

Because the skill is the entire surface area for the adopter, redundancy, prose enums, and unflagged workflow assumptions translate directly into adopter friction and silent drift.

### Priority order

The priority order for this proposal is:

```text
1. high-quality skill output
2. clear and concise skills
3. token cost
```

Token cost matters only as a constraint after quality and clarity are protected. A token-saving edit that weakens skill output quality or makes the skill harder to understand is a failed edit, regardless of savings.

## Goals

- Preserve or improve high-quality skill output before optimizing wording length, structure, or token cost.
- Make each installed skill self-contained for normative behavior, with no references to repository files the user cannot see.
- Make each skill internally non-redundant: each rule, enum, and lookup order is stated exactly once in the file, in the place a reader hits first.
- Replace prose enumerations and narrated enums with tables and code-fenced blocks so a user can locate any contract in seconds.
- Add a short "Workflow role" block at the top of every skill so a user who has never read the workflow understands this skill's place in it.
- Ship a fenced, fillable output skeleton at the bottom of every artifact-producing skill, modeled on the existing `proposal-review` `Result` block.
- Establish a recurring "cold-read" practice: install the adapter into a clean test project, read each skill without any repo context, and treat any unresolvable reference as a defect.
- Treat token cost as a tertiary constraint: measure it and avoid unnecessary regression, but never trade away output quality or clarity to save tokens.

## Non-goals

- Do not change the normative content of any skill (Vision fit rules, scope preservation, recording rules, review dimensions, etc.). This proposal is a readability and self-containment optimization, not a rules change.
- Do not introduce a new build-time include/partial mechanism. That is a related but separate optimization; it can be proposed afterward without blocking this work.
- Do not change adapter packaging, manifest format, or release-archive contracts.
- Do not retroactively rewrite legacy adapter archives. This applies to the canonical `skills/` source going forward; adapters are regenerated.
- Do not edit specs, schemas, or workflow docs as part of this proposal.
- Do not accept token savings that reduce behavior parity, rationale quality, required artifact coverage, or cold-read clarity.

## Vision fit

fits the current vision

VISION.md commits RigorLoop to making AI-assisted changes "easier to inspect, reason about, validate, and maintain" with explicit artifacts that reviewers can reconstruct without chat history. The user-facing skill is the most exposed artifact in the entire system; making it scannable, internally consistent, and self-contained directly strengthens that promise. The falsifier -- that teams ignore artifacts because they slow delivery without improving review quality -- is mitigated when the artifact a user reads on every invocation is tight rather than redundant.

### Quality falsifier

This proposal is falsified if the pilot pair (`proposal` and `proposal-review`) produces weaker output after the rewrite: a different verdict on representative existing artifacts, weaker rationale, missed required sections, scope-preservation regression, unclear handoff, or ambiguous rule ownership. Token savings do not offset any such quality regression.

## Context

- Adapters install only the skill files into the adopter's project. The rest of the repository (`specs/`, `schemas/`, `docs/`) is internal to the maintainer.
- The canonical authored source lives in `skills/`. Adapter archives under `dist/adapters/` are generated from this source.
- The `proposal` and `proposal-review` skills are the most visible examples of the issues this proposal addresses, but the pattern applies to every artifact-producing skill.
- The `proposal-review` skill's `Result` block is the existing example of the desired output-skeleton pattern; this proposal generalizes it rather than inventing a new convention.
- Token cost is paid per skill invocation. Internal redundancy is paid every run; the `benchmarks/token-cost/` infrastructure already exists to measure this.
- This proposal builds on the accepted `docs/proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md` proposal. That earlier proposal owns the broad public-skill portability and project-local guidance direction. This proposal is a follow-on that narrows the next decision to quality-first readability, self-containment, skeletons, tables, fenced enums, and cold-read verification.

### Terminology and affected surfaces

| Term | Meaning in this proposal |
|---|---|
| Installed skill | The skill file a user receives through an adapter install, such as `.claude/skills/`, `.agents/skills/`, or `.opencode/skills/`. |
| Canonical skill source | The authored repository source under `skills/<skill>/SKILL.md`; this is the surface implementation will edit. |
| Generated adapter output | Release/generated adapter artifacts derived from canonical skills; implementation validates regeneration but does not hand-edit generated bodies. |
| Repository-internal guidance | Maintainer-facing specs, schemas, workflow docs, reports, and governance artifacts in this repository; useful to develop RigorLoop, but not assumed present for adopters. |
| Project-local guidance | Guidance in the adopter's own project when present, such as local `AGENTS.md`, `VISION.md`, `docs/workflows.md`, or change artifacts. |

The intended implementation surface is canonical skill source under `skills/`, plus validation or measurement scripts only when the later spec and plan require them. Generated adapter output is validated from canonical source and is not hand-edited.

## Options considered

### Option 1: Do nothing; document the constraint and move on

Leave skills as-is, add a single section to `AGENTS.md` warning maintainers about the user-only-sees-skills constraint.

- **Pros:** Zero churn. No risk of breaking existing skill behavior.
- **Cons:** Does not address current redundancy, prose enums, or missing output skeletons. Adopter friction continues. The constraint stays a maintainer-side concern instead of being structurally enforced.

### Option 2: Move shared rules to specs and have skills reference them

Extract Vision fit, scope preservation, isolation/recording, and artifact placement into `specs/` and have skills link to them.

- **Pros:** Eliminates duplication in the source tree. Single source of truth for shared rules.
- **Cons:** **Breaks the core constraint.** Users do not receive `specs/`. Every reference would be a dangling pointer for the adopter. Skills would no longer be self-contained contracts.

### Option 3: Build-time composition (partials/includes)

Author shared rules as partials under `skills/_partials/`; have `scripts/build-skills.py` inline them at build time so the installed skill remains self-contained.

- **Pros:** Eliminates source duplication while preserving self-containment in the installed artifact. Honors both maintainer hygiene and user constraint.
- **Cons:** Introduces a new authoring concept and build mechanism. Couples this readability proposal to a build-pipeline change. Better pursued as a follow-up after the readability gains are realized and measured.

### Option 4: In-skill restructure for readability and self-containment

Rewrite each artifact-producing skill so that within the single file: each rule appears exactly once; closed enums are fenced; long enumerations become tables; a "Workflow role" block sits at the top; and a fenced output skeleton sits at the bottom. Establish a cold-read practice for verification. Defer build-time deduplication to a separate proposal.

- **Pros:** Directly addresses the user-facing problem. No new tooling. No constraint violations. Low blast radius (no normative content changes). Establishes the verification practice that protects the constraint going forward. Leaves Option 3 available as a follow-up.
- **Cons:** Maintainer-side duplication across skills is not yet eliminated; that remains a separate concern. Requires editorial pass across multiple skills.

## Recommended direction

Choose **Option 4**.

It is the smallest change that resolves the user-facing quality and clarity problem without introducing new tooling or breaking the self-containment constraint. Option 3 (build-time composition) is the natural follow-up once Option 4 has shipped and the cold-read practice is in place to catch regressions.

### Quality and clarity floors

Any token-saving edit must satisfy both floors before it can be accepted.

| Floor | Required evidence |
|---|---|
| Quality floor | Behavior-parity fixtures for the pilot pair produce the same verdicts and preserve required sections, scope preservation, rationale strength, handoff boundaries, and failure-path handling. |
| Clarity floor | A cold-read of the installed skill finds the workflow role, valid enums, required sections, output skeleton, handoff, stop conditions, and workflow-wide versus skill-local rule boundaries without repository-internal context. |

If a change improves token cost but breaches either floor, the change is reverted or revised until the floor is restored.

### Concrete changes per artifact-producing skill

| Change | Description |
|---|---|
| Add "Workflow role" block at top | One short paragraph stating where this skill sits in the lifecycle and what hands off to/from it. No external references. |
| Deduplicate within the file | Each rule, lookup order, enum, and guideline stated exactly once. |
| Fence all closed enums | Vision fit values, scope classifications, recording status, review verdicts, status enums -- all in code-fenced blocks. |
| Tabulate enumerative lists | Required sections, review dimensions, decision-quality checklist, and similar lists become tables. |
| Add fenced output skeleton at bottom | Every artifact-producing skill ships a fillable output skeleton, modeled on `proposal-review`'s `Result` block. |
| Flag workflow-wide vs skill-local | Where a rule is workflow-wide rather than skill-local, mark it inline (e.g., "Workflow rule:") so the user can tell. |
| Front-matter additions | Add `version` and `schema-version` fields so the installed artifact carries its contract version. |

### Candidate "Workflow role" block fields (input to spec, per PRF-R2)

The spec will decide the final shape. As starting input, the candidate fields are:

| Field | Purpose | Constraint |
|---|---|---|
| `role_name` | Stage identity (e.g., `proposal`, `proposal-review`) | Required; matches skill name |
| `stage` | Lifecycle position (authoring, review, verification, etc.) | Required; closed enum |
| `upstream` | What hands off to this skill | Optional; descriptive |
| `downstream` | What this skill hands off to | Optional; descriptive |
| Free-form summary | One-line plain prose describing the role | Required; <= 2 lines |

The spec may collapse, extend, or replace these. They are seeded here so the spec stage does not start from zero.

### Token-cost regression budget (tertiary constraint; input to spec)

Candidate starting policy for the pilot:

```text
target:    zero token regression vs prior skill body
tolerance: up to +5% if (a) readability gain is demonstrable
           and (b) the increase is recorded in the change-local pack
hard cap:  +10%; exceeding this blocks rollout until the spec is revised
```

The spec will confirm or revise these thresholds. Recorded as candidate policy so the spec stage has a concrete starting point. These thresholds do not authorize any quality or clarity regression.

### Verification practice

Add a documented "cold-read" step to the skill release process:

1. Build adapters into a temporary directory.
2. Install one adapter into a fresh, empty project.
3. Open each installed skill in isolation, with no other repo context visible.
4. For each skill, confirm: every reference resolves to something the user can see; every rule's scope (skill-local vs workflow-wide) is clear; every enum is fenced; every required artifact has a fillable skeleton.
5. Any unresolvable reference, ambiguous rule, or missing skeleton is a defect.

## Expected behavior changes

- A user opening an installed skill sees a "Workflow role" block first and understands the skill's lifecycle position in one paragraph.
- A user scanning for valid enum values finds them in a fenced block, not embedded in prose.
- A user looking at the bottom of an artifact-producing skill finds a fillable skeleton matching the contract above.
- A user does not encounter the same rule twice in one file.
- A user does not encounter references to `specs/`, `docs/workflows.md`, `schemas/`, or other paths they do not have.
- No change to skill normative behavior. A proposal that passed today's rules passes the rewritten rules. A review verdict that today says `approved` still says `approved`.

## Architecture impact

- Touches only files under `skills/` and the build/regeneration that produces `dist/adapters/`.
- No change to `scripts/build-skills.py` logic, schemas, manifest, or adapter archive format.
- Front-matter additions (`version`, `schema-version`) are additive and ignored by existing consumers; no breaking change.
- No runtime behavior change. Stage boundaries, workflow handoff behavior, and recording rules are unchanged.

## Testing and verification strategy

| Level | What is verified | How |
|---|---|---|
| Structural | Every artifact-producing skill has a "Workflow role" block, fenced enums, and an output skeleton. | `scripts/validate-skills.py` extension. |
| Anti-redundancy | A given enum's values appear in only one fenced block per skill. | New lint check, optional initially. |
| Self-containment | No installed skill references a path the user does not receive. | Cold-read step plus a deny-list check for forbidden references (e.g., `specs/`, `docs/workflows.md`). |
| Behavior parity | A representative set of existing passing proposals and reviews still pass after rewrite. | Run them against the rewritten skill rules as fixtures. |
| Quality falsifier | The pilot does not produce weaker verdicts, rationale, required-section coverage, scope preservation, handoff clarity, or rule ownership than the baseline. | Compare representative baseline outputs before and after the rewrite; any regression blocks acceptance regardless of token cost. |
| Clarity floor | A reader can locate workflow role, enums, required sections, skeleton, handoff, stop conditions, and rule scope without repository-internal context. | Cold-read verification on installed adapter output. |
| Token cost | Each rewritten skill stays within the candidate budget above. | Compare against `benchmarks/token-cost/`. |

## Rollout and rollback

### Rollout

1. Pilot on `proposal` and `proposal-review` first; ship them in one change.
2. Run the cold-read verification on the pilot pair.
3. Measure token-cost delta against the candidate budget (see Recommended Direction) and record it in the change-local pack.
4. If the pilot passes verification and stays within the budget, extend the rewrite to the remaining artifact-producing skills, one per change.

### Rollback

- Each skill rewrite lands as its own change with the prior version retrievable from Git.
- No persistent state or migration is involved; reverting the skill file restores prior behavior.
- Front-matter additions are additive; rolling back removes them without affecting downstream consumers.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Editorial rewrite accidentally changes a normative rule. | Behavior-parity fixtures: rerun representative artifacts against the rewritten skill and confirm identical verdicts. |
| Token optimization erodes output quality or clarity. | Treat token cost as tertiary. Require the quality and clarity floors before accepting any token-saving edit; revert savings that breach either floor. |
| Cold-read practice becomes ceremony and stops catching defects. | Encode the most common cold-read findings as automated checks (forbidden-path lint, fenced-enum lint, skeleton-present lint). |
| Front-matter additions confuse existing adapters. | Make them additive and unread by current consumers; document them in the skill schema before use. |
| Token cost increases instead of decreases. | Measure on the pilot before extending. Block extension if pilot exceeds the candidate budget. |
| Skills diverge from each other as separate changes land. | Cold-read step explicitly compares stylistic consistency across the pilot pair; subsequent skills inherit the pilot pattern. |
| Scope creeps into the deferred build-time composition work. | Non-goals make this explicit; build-time composition is a separate later proposal. |

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| High-quality skill output (highest priority) | in scope | Goals; Quality and clarity floors; Testing and verification strategy; Vision fit falsifier |
| Clear and concise skills (second priority) | in scope | Goals; Recommended direction; Quality and clarity floors; Verification practice |
| Token cost (lowest priority) | in scope as constraint, not driver | Goals; Token-cost regression budget; Risks and mitigations |
| Practice 2: keep skills self-explanatory but tight | in scope | Goals, Recommended direction |
| Practice 3: use tables for enumerative content | in scope | Recommended direction (Tabulate enumerative lists) |
| Practice 5: fence closed enums | in scope | Recommended direction (Fence all closed enums) |
| Practice 6: distinguish skill-local from workflow-wide rules | in scope | Recommended direction (Workflow role block; Flag workflow-wide vs skill-local) |
| Practice 7: ship a fillable output skeleton | in scope | Recommended direction (Add fenced output skeleton) |
| Practice 10: test the user's experience via cold-read | in scope | Recommended direction (Verification practice) |
| Build-time composition (Option 3 / partials) | deferred follow-up | Options considered, Non-goals, Follow-on artifacts |
| Move shared rules to specs (Option 2) | rejected option | Options considered |

## Review response

Response to `proposal-review` round 1.

| Finding | Disposition | Action taken |
|---|---|---|
| **PRF-R1** -- Pilot scope needs definition | Accepted, no proposal edit required | The proposal already classifies the full-rollout subset as a spec-resolvable open question, which is the correct disposition per the proposal skill's contract ("open questions do not block writing a spec"). Spec will enumerate. No proposal-stage edit needed. |
| **PRF-R2** -- Workflow role block template | Accepted with proposal edit | Added "Candidate Workflow role block fields" subsection under Recommended Direction as input to the spec. The spec stage decides the final shape; the proposal now seeds the candidate fields so the spec does not start from blank. |
| **PRF-R3** -- Forbidden-path lint enforcement | **Contested** | The proposal explicitly defers lint enforcement policy (warning vs CI-blocking) to the `plan` stage, which is the correct stage for rollout-policy decisions. A proposal-stage finding here conflates plan-level detail with proposal-level direction. Reclassifying as an observation for the plan stage rather than a proposal-blocking finding. |
| **PRF-R4** -- Token-cost regression budget | Accepted with proposal edit | Added "Token-cost regression budget" subsection under Recommended Direction with candidate thresholds (zero target, +5% tolerance with rationale, +10% hard cap). The spec stage may revise; the proposal now provides a starting point per review best practice. |
| **PRF-1** -- Title/framing signals priority inversion | Accepted with proposal edit | Added the explicit priority order (`quality > clarity > token cost`) to Problem and Goals; reframed token cost as a tertiary constraint, not a driver. The title already leads with readability and self-containment rather than token cost. |
| **PRF-2** -- No falsifier for quality claim | Accepted with proposal edit | Added a Vision fit falsifier and a quality-falsifier row in Testing and verification strategy. |
| **PRF-3** -- Relationship to prior portability proposal unclear | Accepted with proposal edit | Added Context relationship text that makes this proposal a follow-on to the accepted customer-portable public skills proposal, not a replacement. |
| **PRF-4** -- Token-friendly guidance needs quality floor | Accepted with proposal edit | Added Quality and clarity floors; clarified that token-budget thresholds do not authorize quality or clarity regression. |
| **PRF-5** -- Customer-portable public terminology overloaded | Accepted with proposal edit | Added Terminology and affected surfaces mapping installed skills, canonical source, generated adapter output, repository-internal guidance, and project-local guidance. |
| **PRF-6** -- Local guidance versus portable contract boundary unclear | Accepted with proposal edit | Defined project-local guidance and repository-internal guidance; stated canonical implementation and generated-output boundaries. |

**Rationale for contesting PRF-R3:** The proposal skill's contract is that a proposal answers "why this change, why now, why this approach" -- not "exactly how, with what thresholds, in what enforcement mode." Enforcement policy is a `plan`-stage concern. The proposal correctly identified this as an open question and routed it to `plan`. A finding should fire only if the proposal failed to identify the question or deferred it to the wrong stage; neither applies here.

If `proposal-review` round 2 confirms that PRF-R3 belongs at proposal stage, the disposition will be revisited.

## Open questions

- Which subset of artifact-producing skills counts as in-scope for the full rollout after the pilot? (Resolvable in `spec`. PRF-R1.)
- Should the "Workflow role" block use the candidate fields above, a reduced set, or remain free-form prose constrained only by length? (Resolvable in `spec`. PRF-R2.)
- Should the forbidden-path lint be a hard CI failure or a warning during the rollout window? (Resolvable in `plan`. PRF-R3.)
- Is the candidate token-cost budget (zero target / +5% tolerance / +10% hard cap) appropriate for the pilot, or should it be tightened or loosened? (Resolvable in `spec`. PRF-R4.)

None of these block writing a spec.

## Decision log

| Date | Decision | Reason | Alternatives Rejected |
|---|---|---|---|
| 2026-05-18 | Adopt in-skill restructure (Option 4) | Smallest change that resolves user-facing problem without violating the skills-are-the-contract constraint. | Option 1 (do nothing); Option 2 (move to specs -- breaks user constraint); Option 3 (build-time composition -- deferred) |
| 2026-05-18 | Pilot on `proposal` and `proposal-review` before extending | These are the most visible examples of the issues; piloting limits blast radius. | All-at-once rewrite |
| 2026-05-18 | Defer build-time composition (Option 3) as a follow-up proposal | Couples a tooling change to a readability change; keeps blast radius small and lets cold-read practice mature first. | Bundle Option 3 with Option 4 |
| 2026-05-18 | Seed candidate Workflow role fields (PRF-R2) | Reviewer-recommended; gives spec a starting point rather than a blank slate. | Leave entirely to spec |
| 2026-05-18 | Seed candidate token-cost budget (PRF-R4) | Reviewer-recommended; aligns with best practice of proposing a starting bracket for any spec-resolvable numeric question. | Leave entirely to spec |
| 2026-05-18 | Contest PRF-R3 (lint enforcement) as plan-stage, not proposal-stage | Lint enforcement policy is a `plan`-level rollout concern; the proposal correctly identified and routed it. | Accept finding and pre-decide at proposal stage |
| 2026-05-18 | Make output quality the primary success criterion | User priority order ranks high-quality skill output above clarity and token cost. | Treat token cost as co-equal or primary |
| 2026-05-18 | Declare this proposal a follow-on to the accepted customer-portable public skills proposal | The accepted proposal owns broad portability and project-local guidance; this proposal narrows the next decision to quality-first readability and self-containment. | Supersede or duplicate the accepted proposal |

## Next artifacts

- `proposal-review` round 2 on this revised proposal.
- `spec`: `specs/skill-readability-contract.md` -- defines the structural contract (Workflow role block, fenced enums, tables, output skeleton, front-matter additions), the cold-read verification step, and confirms or revises the candidate Workflow role fields and token-cost budget seeded in this proposal.
- `plan`: rollout plan covering pilot pair, subsequent per-skill changes, and the lint enforcement policy (warning vs CI-blocking) per PRF-R3.
- `test-spec`: behavior-parity fixtures, structural lint checks, forbidden-path lint.

## Follow-on artifacts

- Proposal review: `docs/changes/2026-05-18-skill-readability-self-containment/reviews/proposal-review-r3.md`
- Spec: `specs/skill-readability-contract.md`

## Readiness

Accepted and ready for focused `spec` authoring.

### Core invariant

```text
The installed skill is the entire user-facing contract. Each skill states each rule exactly once, fences every closed enum, ships a fillable output skeleton, flags workflow-wide rules inline, and contains no references to repository content the user does not receive. Output quality is the primary success criterion, clarity and concision are secondary, and token cost is a constraint that cannot justify degrading either floor.
```
