# Learn Skill Simplification

## Owning change record

`docs/changes/2026-08-16-learn-skill-simplification/change.yaml`

## Problem

The published `learn` skill correctly protects evidence quality, contributor confirmation, session recording, topic curation, and authoritative-artifact boundaries, but it presents all 1,712 words and 12,375 UTF-8 bytes on every invocation. A pre-session trigger closeout therefore loads the complete periodic, incident, classification, routing, and topic-curation method even though no learn session begins.

The flat procedure also contains an authority ambiguity. Its handoff says confirmed derivative work is routed to an owning proposal, ADR, spec, workflow, skill, issue, or other authoritative artifact without editing it, while the `Route` phase says `learn` updates or creates those derivative artifacts. Contributor confirmation settles the learning classification, but it does not necessarily grant authority to mutate another lifecycle or external surface. A future implementation should not have to choose between those statements.

The existing artifact model remains sound. Session records belong under `docs/learn/sessions/`, confirmed durable topic guidance belongs under `docs/learn/topics/`, and behavior-changing actions belong to their authoritative owners. The problem is the common-path package and the execution boundary, not the three-surface model.

## Goals

- Reduce loaded context for both pre-session trigger closeout and real learn sessions while preserving evidence quality and fail-closed behavior.
- Keep trigger sufficiency, evidence standards, confirmation, sensitive-data safety, stops, claims, operation selection, and resource loading in a compact universal `SKILL.md`.
- Move the complete `Frame -> Observe -> Classify -> Route` session method behind one conditional reference.
- Define pre-session trigger closeout and real session execution as closed operations with non-overlapping write boundaries.
- Separate contributor confirmation of a classification from authority to mutate another artifact or external tracker.
- Preserve learn ownership of session records and confirmed topic guidance while routing derivative work to its authoritative owner.
- Preserve the existing no-template, no-fixed-taxonomy, no-runtime-engine direction.
- Prove semantic and literal preservation, real loaded-profile reduction, and canonical-through-installed package parity deterministically.

## Non-goals

- Redesigning the approved learn artifact namespace or migrating historical learn records.
- Making `learn` mandatory after every change or adding it to automatic lifecycle progression.
- Creating session templates, topic templates, empty topics, or a fixed topic taxonomy.
- Building automated lesson classification, an issue-tracker integration, a background index, or a hosted runtime.
- Lowering the evidence standard for maintainer-requested, incident, cadence, contributor-observed, or explicit sessions.
- Removing contributor confirmation or allowing topic files to become policy.
- Giving `learn` ownership of proposal, spec, ADR, workflow, skill, plan, review, verification, PR, release, or external-tracker state.
- Optimizing unrelated periodic or support skills.
- Using target-agent execution, transcript grading, or a separate manual semantic-review acceptance system.

## Vision fit

fits the current vision

The change supports durable lessons while reducing unnecessary procedural loading. It preserves Git-tracked learning evidence, human confirmation, authoritative ownership, and resumability without introducing the hosted runtime, autonomous project manager, or artifact-free behavior that the vision rejects.

## Context

The accepted `docs/proposals/2026-05-03-optimize-learn-skill.md` and approved `specs/learn-artifact-model.md` established the three-surface model and four ordered phases. This proposal extends that accepted direction rather than replacing it.

The current package contains only `skills/learn/SKILL.md`; it has no mapped references, assets, or scripts. The published-skill package architecture already supports conditional references and canonical-through-installed parity. Recent skill simplifications demonstrate that a reference is justified only by a real activation boundary and that main-file shrinkage alone is not sufficient evidence.

The governing lifecycle architecture assigns mutable state and artifact authoring to their owning stages. `learn` is periodic support work, not a general authority to edit lifecycle artifacts merely because it identified a lesson. The approved learn spec already says action-owning artifacts remain authoritative, but R21-R24 and the current skill need clarification so “route” cannot be interpreted as implicit cross-owner mutation.

## Options Considered

### Option 1: Keep the flat skill unchanged

This avoids package and contract edits and preserves every current phrase literally. It leaves pre-session closeout overloaded, retains the cross-owner mutation ambiguity, and provides no measurable context improvement.

### Option 2: Compress the existing file without adding resources

Editorial compression would reduce navigation and total package size. It would still load trigger-specific evidence matrices, all four phases, the classification table, routing rules, and topic curation for every invocation. It also makes semantic loss more likely because universal safety and conditional method remain interleaved.

### Option 3: Use one conditional session-method reference and close routing authority

Keep a compact universal file for operation classification, evidence thresholds, confirmation safety, ownership, stops, claims, and resource selection. Load one `references/session-method.md` only when a real session reaches `Frame`. Clarify that `learn` owns the session record and confirmed topic guidance, while other derivative mutations require separately valid owning-stage authority.

This creates one genuine progressive-disclosure boundary, retains the complete method for sessions, and resolves the authority contradiction without adding a new lifecycle or runtime owner.

### Option 4: Split session classification and routing into separate references

Two references would create smaller individual files. Every real session normally proceeds through both classification and routing or stops at confirmation, so the second split provides little loaded-context benefit and increases navigation and missing-resource states.

### Option 5: Add templates, scripts, or an executable learning engine

A template could stabilize session shape, and executable machinery could enforce vocabularies and routing. The approved artifact model deliberately rejected templates until repeated usage proves a stable need, and learning remains judgment-heavy. A new engine would add disproportionate policy, testing, and architecture surface.

## Recommended Direction

Choose Option 3:

```text
compact universal skills/learn/SKILL.md
+ references/session-method.md
+ no assets
+ no scripts
```

Use two closed operations:

```text
pre-session-trigger-closeout
run-learn-session
```

An explicit direct `$learn` invocation selects `run-learn-session`. Pre-session closeout applies only when current workflow, incident, review, release, or maintainer authority asks to close a known trigger without beginning a session and identifies the tracked or review-visible owning surface. Unknown, conflicting, or ambiguous operation evidence stops before writes.

Once `Frame` begins, the invocation is a learn session, the conditional reference is loaded, and a dated session record is required even when no observation or durable lesson results. It cannot fall back to no-record trigger closeout.

The compact universal file remains responsible for:

- valid triggers and operation selection;
- trigger sufficiency versus durable-evidence sufficiency;
- single-event and systemic-gap boundaries;
- contributor-confirmation requirements;
- learn-owned versus externally owned writes;
- sensitive-data safety;
- canonical paths;
- missing-resource behavior;
- universal stops, claims, outputs, and handoff limits.

The session reference owns:

- detailed `Frame`, `Observe`, `Classify`, and `Route` procedure;
- periodic, incident, contributor-observed, and explicit evidence selection;
- the seven-value primary-classification vocabulary and secondary-route model;
- classification decision records;
- session outcomes, no-observation, no-durable-lesson, and confirmation-pending behavior;
- topic creation, curation, conflict, supersession, absorption, and traceability;
- derivative-route construction after confirmation.

Use these ownership rules:

```text
learn-owned writes:
  session record
  confirmed topic guidance

conditionally authorized pre-session write:
  only the exact existing trigger-owning tracked or review-visible surface

route-only derivative results:
  artifact update
  decision
  direction
  process follow-up
```

Contributor confirmation establishes the final learning classification. It does not by itself authorize an ADR, proposal, spec, workflow, skill, active-plan, issue, or external-system mutation. A derivative route records the exact destination, owning skill or stage, evidence basis, requested action, and blocker. Same-turn continuation, when separately requested or workflow-authorized, uses the owning skill under its own contract.

The focused spec amendment should clarify R21-R24 and their outputs without changing the three-surface artifact model: “route to” means produce or hand off to the owning surface under its authority, not grant `learn` a universal cross-owner write set.

Use closed session results such as:

```text
trigger-closed-before-session
no-observations
no-durable-lesson
observations-recorded
confirmation-required
routing-required
session-complete
blocked
```

The downstream specification may adjust labels, but it must preserve distinct outcomes for pre-session closeout, empty evidence, pending confirmation, routed ownership, and blocked execution.

## Expected Behavior Changes

- A pre-session trigger closeout uses the compact skill only and does not load or reconstruct the full session method.
- An explicit `$learn` invocation loads the session reference before `Frame` writes and creates one session record at the canonical dated path.
- A session with no observations or no durable lesson remains a valid recorded outcome.
- Candidate classifications can be recorded without contributor confirmation, but topic and derivative routing stops.
- Confirmed durable lessons may update the relevant topic guidance under learn ownership.
- Confirmed artifact, decision, direction, and process-follow-up classifications produce exact owner-bound routes rather than implicitly editing another authoritative surface.
- A missing or invalid conditional reference stops before session creation or dependent judgment.
- Existing learn sessions, topic files, namespace guidance, and selector behavior remain compatible.

## Architecture Impact

The expected assessment is `architecture-not-required` after a bounded check. The change uses the existing published-skill package model, existing learn artifact namespace, existing stage ownership, and existing generated-package pipeline. It adds no service, persistence mechanism, schema owner, background job, external integration, or runtime component.

Architecture work becomes necessary if safe implementation requires a new durable routing record, cross-stage transaction, automated issue-tracker integration, session schema owner, template system, or executable policy engine. Clarifying route-only ownership to match the existing stage-owned architecture does not itself require a new ADR.

## Testing and Verification Strategy

Create a change-local semantic-rule ledger and literal-compatibility ledger before refactoring. Classify every current behaviorally significant rule as retained inline, moved to the session reference, clarified through the learn-spec amendment, intentionally retired, or otherwise dispositioned with evidence.

Use deterministic contract scenarios for:

- explicit invocation selecting a real session;
- authorized pre-session follow-up, deferral, and no-learn closeout;
- ambiguous operation or missing owning surface;
- one-time session creation at `Frame`;
- missing session reference;
- no observations and no durable lesson;
- isolated single event versus repeated or systemic evidence;
- candidate classification without contributor confirmation;
- confirmed durable lesson and topic curation;
- artifact update, decision, direction, and process follow-up routing without unauthorized mutation;
- topic conflict with higher-priority authority;
- sensitive incident evidence;
- periodic-window evidence and explicit bounded evidence;
- canonical, generated, archived, release-candidate, and clean-installed package parity.

Measure two primary procedural profiles using normalized LF content, Unicode whitespace-separated words, and UTF-8 bytes:

| Profile | Loaded procedure |
| --- | --- |
| `LR0-trigger-closeout` | `SKILL.md` |
| `LR1-learn-session` | `SKILL.md` plus `references/session-method.md` |

Both LR0 and LR1 must decrease from the current flat baseline of 1,712 words and 12,375 bytes. Main-file reduction alone is insufficient. Report the complete package separately, require one loaded owner for every duplicate rule cluster, and do not let a fixed percentage override semantic preservation.

Use existing skill validation, build checks, adapter-distribution tests, selector checks, boundary checks when applicable, change-metadata validation, and repository CI. Do not run Codex, Claude Code, opencode, or another target-agent runtime as acceptance. Ordinary lifecycle review remains review, not a separately graded semantic acceptance system.

## Rollout and Rollback

Roll out in one compatibility-preserving package slice after an approved focused spec amendment and test specification:

1. Freeze current semantic rules, literal consumers, resource inventory, and LR0/LR1 baseline.
2. Clarify learn operation and derivative ownership in the approved learn contract and affected workflow guidance only where necessary.
3. Add the mapped session reference and compact the universal skill.
4. Add deterministic contract scenarios and update existing validators rather than introducing a new validator family.
5. Prove canonical-through-installed resource parity and both profile reductions.

Existing session and topic documents remain unchanged. No data migration or reverse synchronization is required.

Rollback restores the flat `SKILL.md`, removes the mapped reference, and restores the prior contract wording and package inventory from the same reviewed revision. Historical sessions and topic guidance remain valid because their artifact model does not change.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal evidence or confirmation safety moves behind the session trigger. | Freeze rule ownership first and require universal stops, evidence thresholds, confirmation, ownership, and claims inline. |
| LR1 becomes as large as or larger than the current flat skill. | Make LR1 reduction a primary acceptance surface rather than treating main-file shrinkage as success. |
| Route-only clarification accidentally prevents useful same-turn action. | Permit separately authorized continuation through the owning skill and record the destination in the session. |
| Contributor confirmation is mistaken for write authority. | Represent classification confirmation and destination authority as independent decisions. |
| Pre-session closeout writes into another stage without authority. | Require an exact existing owning surface and current authority; otherwise return a route or blocker without mutation. |
| The reference becomes another policy owner or duplicates inline safety. | Use a rule ledger and one loaded owner per rule cluster; references remain subordinate to `learn`. |
| No-template structure becomes inconsistent across sessions. | Preserve required semantic fields in the session reference and current spec; revisit an asset only through a later evidence-backed proposal. |
| Package resources drift across adapters. | Reuse current canonical, generated, archive, release-candidate, and clean-install parity checks. |

## Open Questions

None.

## Decision Log

| Date | Decision | Rationale | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-16 | Preserve the existing three-surface learn artifact model. | The namespace and authority model are already approved and used; the current problem is package loading and route execution authority. | New namespace, historical migration, topic-only or session-only model. |
| 2026-08-16 | Use one conditional session-method reference. | Every real session needs the four phases, classification, routing, and curation method; further splitting adds navigation without a second useful activation boundary. | Inline-only compression, two references, fragmented references. |
| 2026-08-16 | Keep templates and scripts out of the first simplification. | The approved contract rejects premature templates, and the procedure is judgment-heavy rather than mechanically executable. | Session asset, topic asset, learning engine. |
| 2026-08-16 | Separate classification confirmation from destination authority. | Human agreement that an observation is an artifact update does not automatically authorize mutation of that artifact. | Treat contributor confirmation as universal write authority. |
| 2026-08-16 | Route derivative authoritative work to its owner. | This aligns periodic support work with existing stage-owned lifecycle architecture while retaining session traceability. | Cross-owner writes directly from `learn`; topic files as policy. |
| 2026-08-16 | Require both actual procedural profiles to shrink. | Moving prose to a reference is not simplification if every real session loads the same or more context. | Main-file-only target; fixed percentage target. |

## Next Artifacts

- Independent `proposal-review` of value, operation closure, route ownership, scope, risks, measurement, and spec readiness.
- Focused amendment to `specs/learn-artifact-model.md` and its test specification after proposal approval.
- Bounded architecture assessment, expected `architecture-not-required` unless implementation discovers new persistence or ownership.
- Execution plan and focused proof map after the amended contract is approved.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent proposal review. It does not claim proposal acceptance or specification readiness.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `learn` skill after the prior skill-simplification sequence. | in scope | Problem, Goals, Recommended Direction |
| Identify the best package and progressive-disclosure solution. | in scope | Options Considered, Recommended Direction |
| Preserve evidence quality, contributor confirmation, and durable learning behavior. | in scope | Goals, Expected Behavior Changes, Risks and Mitigations |
| Clarify whether `learn` should mutate derivative authoritative artifacts. | in scope | Recommended Direction, Expected Behavior Changes |
| Avoid strange or unnecessary templates, scripts, runtimes, and acceptance machinery. | in scope | Non-goals, Testing and Verification Strategy |
| Create a new branch, author a proposal, and perform proposal review. | in scope | Owning change record, Readiness, Next Artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact universal learn contract | core to this proposal | It is the primary common-path simplification. |
| One conditional session-method reference | core to this proposal | It implements the genuine session activation boundary. |
| Operation and write-boundary closure | core to this proposal | Progressive disclosure is unsafe without deterministic side effects. |
| Focused learn contract amendment | same-slice dependency | Route ownership must be settled before skill behavior changes. |
| Existing learn test-spec amendment | same-slice dependency | The proof map must reflect operation, authority, and resource behavior. |
| Existing selector and package validation | same-slice dependency | New mapped resources and retained learn paths require parity proof. |
| Workflow and governance summaries | first-slice candidate | Update only when the approved contract changes their current guidance. |
| Historical learn-session migration | out of scope | The artifact model and historical documents remain compatible. |
| Session or topic templates | out of scope | Existing approved direction rejects them until evidence justifies a later proposal. |
| Automated learning engine or issue integration | out of scope | They introduce disproportionate runtime and architecture scope. |
| Other skill simplifications | separate proposal | Each skill needs its own activation-boundary and preservation analysis. |
