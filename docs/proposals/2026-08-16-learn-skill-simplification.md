# Learn Skill Simplification

## Owning change record

`docs/changes/2026-08-16-learn-skill-simplification/change.yaml`

## Problem

The published `learn` skill correctly protects evidence quality, contributor confirmation, session recording, topic curation, and authoritative-artifact boundaries, but its flat 1,712-word, 12,375-byte procedure interleaves universal trigger and ownership safety with detailed periodic, incident, classification, routing, and topic-curation method. Every valid session needs the method, yet the current shape is harder to scan, duplicates ownership statements, and contains a cross-owner mutation contradiction. Simplification therefore requires both clearer ownership and a smaller actual session assembly; moving prose to another file is not sufficient.

The flat procedure also contains an authority ambiguity. Its handoff says confirmed derivative work is routed to an owning proposal, ADR, spec, workflow, skill, issue, or other authoritative artifact without editing it, while the `Route` phase says `learn` updates or creates those derivative artifacts. Contributor confirmation settles the learning classification, but it does not necessarily grant authority to mutate another lifecycle or external surface. A future implementation should not have to choose between those statements.

The existing artifact model remains sound. Session records belong under `docs/learn/sessions/`, confirmed durable topic guidance belongs under `docs/learn/topics/`, and behavior-changing actions belong to their authoritative owners. The problem is the common-path package and the execution boundary, not the three-surface model.

## Goals

- Reduce the actual learn-session loaded context while preserving evidence quality and fail-closed behavior.
- Keep trigger sufficiency, evidence standards, confirmation, sensitive-data safety, stops, claims, operation selection, and resource loading in a compact universal `SKILL.md`.
- Move the complete `Frame -> Observe -> Classify -> Route` session method behind one conditional reference.
- Define recorded session execution and later owner-result backlink recording as closed operations with non-overlapping authority.
- Separate contributor confirmation of a classification from authority to mutate another artifact or external tracker.
- Preserve learn ownership of session records and confirmed topic guidance while routing derivative work to its authoritative owner.
- Preserve the existing no-template, no-fixed-taxonomy, no-runtime-engine direction.
- Prove semantic and literal preservation, real loaded-profile reduction, and canonical-through-installed package parity deterministically.

## Non-goals

- Redesigning the approved learn artifact namespace or migrating historical learn records.
- Making `learn` mandatory after every change or adding it to automatic lifecycle progression.
- Creating session templates, topic templates, empty topics, or a fixed topic taxonomy.
- Building automated lesson classification, an issue-tracker integration, a background index, or a hosted runtime.
- Adding transaction-grade phase recovery, prepared side-effect manifests, polling, or an aggregate route-settlement engine.
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

This avoids package and contract edits and preserves every current phrase literally. It leaves the session procedure overloaded, retains the cross-owner mutation ambiguity, and provides no measurable context improvement.

### Option 2: Compress the existing file without adding resources

Editorial compression would reduce navigation and total package size. It would still load trigger-specific evidence matrices, all four phases, the classification table, routing rules, and topic curation for every invocation. It also makes semantic loss more likely because universal safety and conditional method remain interleaved.

### Option 3: Use one conditional session-method reference and close routing authority

Keep a compact universal file for operation classification, evidence thresholds, confirmation safety, ownership, stops, claims, resource selection, and the narrow owner-result backlink operation. Load one `references/session-method.md` only for `run-learn-session` after trigger, path, and sensitive-data preflight. Clarify that `learn` owns the session record and confirmed topic guidance, while other derivative mutations require separately valid owning-stage authority.

This gives the four-phase method one coherent owner, keeps later backlink recording on a much smaller path, and resolves the authority contradiction without adding a lifecycle or runtime owner. Because every valid session loads the reference, acceptance depends on strict reduction of the complete session assembly rather than on main-file shrinkage.

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
run-learn-session
record-learn-route-result
```

An explicit direct `$learn` invocation selects `run-learn-session` unless the request names one exact existing session route and owner-produced result to record. Repository inventory found no current call path that invokes `learn` solely to assess whether a trigger should begin a session, so `assess-learn-trigger` and its LR0 profile are removed from the first version. Trigger-owning workflow, review, incident, release, or maintainer processes decide whether to invoke learn and record their own pre-session follow-up, deferral, or no-learn closeout.

`record-learn-route-result` requires one exact session path, one existing stable route ID, and one owner-produced destination artifact or expressly permitted durable follow-up identity. It updates only that route's backlink and status in the learn-owned session record. It does not re-run `Frame`, `Observe`, or `Classify`; update topic guidance; discover or poll destinations; derive workflow state; or mutate any destination surface. Missing, stale, conflicting, or ambiguous session, route, or destination identity stops without writes.

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
  exact owner-result backlink in an existing session route

owner-bound derivative results:
  artifact update
  decision
  direction
  process follow-up
```

Contributor confirmation establishes the final learning classification. It does not by itself authorize an ADR, proposal, spec, workflow, skill, active-plan, issue, or external-system mutation. A derivative route records the exact destination, owning skill or stage, evidence basis, requested action, settlement state, and blocker. Same-turn continuation, when separately requested or workflow-authorized, uses the owning skill under its own contract and preserves that skill's review and settlement gates.

The focused spec amendment should clarify R21-R24 and R33 without changing the three-surface artifact model: “route to” means invoke, produce, or hand off to the owning surface under its authority, not grant `learn` a universal cross-owner write set and not weaken an existing mandatory authoritative update.

Represent derivative settlement per route rather than through one independently written aggregate value. Each confirmed derivative route records:

```text
route ID
source observation ID
classification and requested action
destination kind and owning skill or stage
evidence basis
settlement: pending-owner-action | complete | blocked
destination identity or blocker
```

A session may finish its durable record while an owner action remains pending. It may not mark that route complete until the authoritative artifact or an expressly permitted durable follow-up exists.

| Settlement | Meaning |
| --- | --- |
| `pending-owner-action` | The exact destination and owning skill are recorded, but the required owner mutation or permitted durable follow-up does not yet exist. |
| `complete` | The owning skill produced the authoritative artifact update, or the governing route explicitly permits and records the exact durable scheduled follow-up. |
| `blocked` | Authority, destination, evidence, or owner execution could not be resolved safely. |

When no derivative action is required, no route record is created. A displayed session summary may derive `not-required`, `pending-owner-action`, `complete`, or `blocked` from the current per-route values, but that aggregate is not a separate persistent state or workflow authority. When R33 requires a behavior-changing authoritative update, a chat-only route or an unowned recommendation cannot satisfy it. When the governing route permits scheduling, the route links the exact durable follow-up.

### Session identity, collision, and interruption

Every `run-learn-session` attempt binds:

```text
trigger identity and type
normalized scope
canonical session path
initial evidence-basis identity
```

Use this closed behavior:

| Existing state | Result |
| --- | --- |
| Canonical path absent | Create the session record with complete `Frame` content when entering `Frame`. |
| Human-readable dated slug already occupied | Select the lowest available deterministic numeric suffix within `docs/learn/sessions/`; never adopt the occupied file. |
| Existing completed session named explicitly for ordinary rerun | Return the existing result without repeating classification, topic writes, or route creation. |
| Existing incomplete or partially written session | Stop; do not infer phase completion or automatically resume. |
| Trigger, normalized scope, or evidence basis changed materially | Begin a new uniquely pathed session that may link the earlier record as evidence. |
| Existing file changed concurrently | Stop before further writes. |
| Identity cannot be established | Stop. |

The first version does not promise exact crash recovery across phase or side-effect boundaries. It uses ordinary content-identity and concurrent-write checks, performs topic updates only after contributor-confirmed classification is durably present, and fails closed when a prior write or effect is ambiguous. Explicit repair or transaction-grade recovery requires separate authority and, if persistent phase or effect state is introduced, architecture assessment. Topic curation retains its existing traceability and conflict rules.

## Expected Behavior Changes

- Trigger-owning stages decide whether to invoke learn; `learn` does not expose an unobserved assessment operation.
- An explicit `$learn` invocation loads the session reference after preflight and creates one uniquely pathed session record with complete Frame content.
- A session with no observations or no durable lesson remains a valid recorded outcome.
- Candidate classifications can be recorded without contributor confirmation, but topic and derivative routing stops.
- Confirmed durable lessons may update the relevant topic guidance under learn ownership.
- Confirmed artifact, decision, direction, and process-follow-up classifications produce exact owner-bound routes, distinguish pending from completed owner action, and never treat contributor confirmation as mutation authority.
- A mandatory behavior-changing route is complete only after the owning artifact update exists; an expressly schedulable route may instead link one exact durable follow-up.
- A same-day slug collision receives a deterministic unique suffix; a partial record, ambiguous side effect, or concurrent edit stops rather than being inferred, resumed, adopted, or overwritten.
- A later exact owner result may update only the matching per-route backlink and status through `record-learn-route-result`.
- A missing or invalid conditional reference stops before session creation or dependent judgment.
- Existing learn sessions, topic files, namespace guidance, and selector behavior remain compatible.

## Architecture Impact

The expected assessment is `architecture-not-required` after a bounded check. The change uses the existing published-skill package model, existing learn artifact namespace, existing stage ownership, and existing generated-package pipeline. It adds no service, persistence mechanism, schema owner, background job, external integration, or runtime component.

Architecture work becomes necessary if safe implementation requires persistent phase or prepared-effect state, a new transaction artifact, automated route discovery or polling, a cross-stage coordinator, external integration, a session schema owner, a template system, or an executable policy engine. Stable route rows and exact backlinks inside the existing Markdown session record do not themselves require a new ADR.

## Testing and Verification Strategy

Create a change-local semantic-rule ledger and literal-compatibility ledger before refactoring. Classify every current behaviorally significant rule as retained inline, moved to the session reference, clarified through the learn-spec amendment, intentionally retired, or otherwise dispositioned with evidence.

Use deterministic contract scenarios for:

- explicit invocation selecting a real session;
- explicit session invocation and trigger-owner pre-session closeout remaining outside learn;
- bounded inventory proving no trigger-assessment caller exists;
- one-time session creation with complete Frame content;
- deterministic same-day suffix collision, partial record, changed basis, unrelated existing file, ambiguous prior effect, and concurrent edit;
- missing session reference;
- no observations and no durable lesson;
- isolated single event versus repeated or systemic evidence;
- candidate classification without contributor confirmation;
- confirmed durable lesson and topic curation;
- stable per-route records for artifact update, decision, direction, and process follow-up;
- later exact owner-result backlink recording, idempotent repeat, mismatched route, ambiguous destination, and forbidden destination mutation;
- mandatory behavior-changing update versus expressly permitted durable scheduling;
- topic conflict with higher-priority authority;
- sensitive incident evidence;
- periodic-window evidence and explicit bounded evidence;
- canonical, generated, archived, release-candidate, and clean-installed package parity.

Measure the two real procedural profiles using normalized LF content, Unicode whitespace-separated words, and UTF-8 bytes:

| Profile | Loaded procedure |
| --- | --- |
| `LR0-route-result` | `SKILL.md`; exact owner-result backlink recording |
| `LR1-learn-session` | `SKILL.md` plus `references/session-method.md`; every valid session |

Both LR0 and LR1 must decrease from the current flat baseline of 1,712 words and 12,375 bytes. LR1 is the primary simplification surface because every valid session loads it. Main-file reduction alone is insufficient. Report the complete package separately, require one loaded owner for every duplicate rule cluster, and do not let a fixed percentage override semantic preservation.

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-LRNSIM-001` | An explicit direct `$learn` invocation selects a recorded learn session. |
| `AC-LRNSIM-002` | No current repository caller invokes learn solely for trigger assessment, so the first version exposes no assessment operation. |
| `AC-LRNSIM-003` | The trigger-owning stage decides whether to invoke learn and records pre-session closeout under its own authority. |
| `AC-LRNSIM-004` | Contributor confirmation and destination mutation authority remain independent. |
| `AC-LRNSIM-005` | Every derivative route has one stable route ID and pending, complete, or blocked status. |
| `AC-LRNSIM-006` | A mandatory behavior-changing update is not satisfied by a chat-only or unowned route. |
| `AC-LRNSIM-007` | Same-turn continuation invokes the owning skill and preserves its review and settlement gates. |
| `AC-LRNSIM-008` | Every session records one exact trigger, scope, unique canonical path, and initial evidence basis. |
| `AC-LRNSIM-009` | A same-day slug collision receives the lowest available deterministic numeric suffix. |
| `AC-LRNSIM-010` | Partial, ambiguous, unrelated, or concurrently changed session records are never inferred, resumed, adopted, or overwritten automatically. |
| `AC-LRNSIM-011` | Every claimed real loaded profile decreases from the current flat baseline. |
| `AC-LRNSIM-012` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |
| `AC-LRNSIM-013` | No target-agent runtime or separate semantic-grading system is used for acceptance. |
| `AC-LRNSIM-014` | `record-learn-route-result` requires one exact session, route ID, and owner-produced destination or permitted follow-up identity. |
| `AC-LRNSIM-015` | Owner-result recording updates only the matching learn-owned route backlink and status. |
| `AC-LRNSIM-016` | Owner-result recording never repeats classification, changes topic guidance, discovers destinations, derives workflow state, or mutates destination surfaces. |
| `AC-LRNSIM-017` | The first version makes no transaction-grade arbitrary-interruption recovery claim. |
| `AC-LRNSIM-018` | Persistent phase state, effect manifests, polling, or a cross-stage coordinator require separate architecture assessment. |

Use existing skill validation, build checks, adapter-distribution tests, selector checks, boundary checks when applicable, change-metadata validation, and repository CI. Do not run Codex, Claude Code, opencode, or another target-agent runtime as acceptance. Ordinary lifecycle review remains review, not a separately graded semantic acceptance system.

## Rollout and Rollback

Roll out in one compatibility-preserving package slice after an approved focused spec amendment and test specification:

1. Freeze current semantic rules, literal consumers, resource inventory, and LR0/LR1 baseline.
2. Clarify trigger-owner closeout, unique session paths, fail-closed interruption, stable route IDs, and narrow owner-result backlink recording in the approved learn contract and affected workflow guidance only where necessary.
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
| Owner-bound routing accidentally prevents useful same-turn action. | Permit separately authorized continuation through the owning skill, preserve its gates, and record the resulting destination identity in the session. |
| Contributor confirmation is mistaken for write authority. | Represent classification confirmation and destination authority as independent decisions. |
| An artificial trigger-assessment path survives solely to justify progressive disclosure. | Remove it after the bounded inventory found no current caller and measure only real profiles. |
| A recorded derivative route is mistaken for completed mandatory work. | Use stable per-route status and require an exact owner-produced artifact or expressly permitted durable follow-up identity. |
| Session recovery expands into a transaction engine. | Make partial or ambiguous state fail closed and defer persistent phase/effect recovery to separate architecture-bearing work. |
| Owner-result backlink recording expands into polling or workflow settlement. | Require an explicit exact destination identity and limit the write to one route row in the session record. |
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
| 2026-08-16 | Initially select read-only pre-session trigger assessment. | This closed the first review's cross-owner write concern, but the operation was superseded on 2026-08-17 after inventory found no caller. | Generic learn-owned writes into review, incident, release, workflow, or plan surfaces. |
| 2026-08-16 | Separate session recording from derivative-route settlement. | A durable session may exist while an owning-stage action remains pending, but pending work must not be reported as routed complete. | Treat route creation as completion; give learn cross-owner mutation authority. |
| 2026-08-16 | Initially select identity-bound session retry. | This closed blind adoption, but exact resume was superseded on 2026-08-17 by deterministic unique paths and fail-closed partial-state handling. | Blind create-or-update; separate transaction artifact. |
| 2026-08-17 | Remove `assess-learn-trigger` from the first version. | A bounded repository inventory found guidance for trigger-owner closeout but no call path invoking learn solely for assessment. | Preserve an artificial public operation; invent a request envelope without a caller. |
| 2026-08-17 | Use fail-closed interruption instead of transaction-grade phase recovery. | Exact arbitrary-interruption resume requires persistent phase and side-effect state beyond this simplification's value case. | Prepared phase manifest; inferred Markdown-phase completion. |
| 2026-08-17 | Add narrow `record-learn-route-result` backlink recording. | Existing session traceability needs later owner-produced links, but not polling, aggregate settlement, or cross-owner mutation. | No later backlink; reconciliation engine. |

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
