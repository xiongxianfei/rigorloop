# Proposal Review: Learn Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-16-learn-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-16-learn-skill-simplification.md` at commit `93958552`
Review date: 2026-08-16
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: LRNSIM-PR1, LRNSIM-PR2, LRNSIM-PR3
- Open blockers: pre-session closeout ownership, derivative-route settlement, and session identity/retry behavior require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, mutate learn artifacts, or continue the workflow

## Overall assessment

The proposal selects a proportionate package direction: a compact universal `SKILL.md`, one conditional session-method reference, and no premature templates, assets, scripts, or runtime. The proposed reference follows the real `Frame` activation boundary, while trigger evidence, confirmation safety, ownership, sensitive-data handling, stops, claims, and resource selection remain inline.

The proposal also identifies a genuine contradiction in the current skill: confirmed classifications are said both to route without editing another authoritative surface and to update or create that surface directly. Separating classification confirmation from mutation authority is the right correction.

Three operational contracts remain incomplete. Pre-session closeout is treated as a `learn` operation even though the approved contract describes it as occurring when learn does not run as a session, leaving the actual write owner unclear. Route-only derivative results do not yet preserve the existing requirement that behavior-changing lessons reach their authoritative artifact. Finally, session creation has no closed create/resume/collision identity model, so a dated path can be overwritten or adopted ambiguously.

## What is strong

### Progressive disclosure follows the session boundary

The detailed `Frame -> Observe -> Classify -> Route` procedure is needed only after a real session begins. Keeping one reference for all four phases avoids artificial fragmentation.

### Universal safety remains inline

Trigger validity, evidence sufficiency, contributor confirmation, sensitive-data limits, ownership, stops, claims, and missing-resource behavior remain available before conditional procedure loads.

### The artifact model remains stable

Session history, curated topic guidance, and action-owning authoritative artifacts remain distinct. The proposal does not add migration, templates, a fixed taxonomy, or an executable learning engine.

### Acceptance measures actual loaded profiles

Both the compact pre-session assembly and the full session assembly must improve, while total package size remains separately visible. A shorter main file alone is not treated as sufficient evidence.

## Material findings

### LRNSIM-PR1 — Major: pre-session closeout is modeled as a learn-owned write without a closed owner

Finding ID: LRNSIM-PR1
Severity: major
Location: `Recommended Direction` sections `Use two closed operations` and `Use these ownership rules`
Evidence: The proposal makes `pre-session-trigger-closeout` a learn operation and permits it to write an exact trigger-owning tracked or review-visible surface when current authority exists. The approved contract instead defines this surface for the case where learn does not actually run as a session. The proposal does not identify the owning skill, the authority forms, permitted fields, or whether `learn` is allowed to mutate a review, incident, release, or workflow-owned record. This recreates the cross-owner ambiguity that the proposal is intended to remove.
Required outcome: Separate learn-session execution from trigger-owner closeout and give the pre-session mutation one deterministic owner.
Safe resolution path: Let `learn` perform a read-only pre-session assessment and return `session-required`, `follow-up-recommended`, `deferral-recommended`, or `no-learn-rationale-recommended`. The trigger-owning workflow, review, incident, release, or maintainer-authorized stage writes its own closeout surface under its existing contract. If a current orchestration contract explicitly invokes `learn` only to classify the trigger, retain `LR0` as a read-only assembly. An explicit direct `$learn` invocation remains `run-learn-session`. Do not grant `learn` a generic foreign-surface write set.
needs-decision rationale: none; stage ownership already supplies the safer boundary.

### LRNSIM-PR2 — Major: route-only derivative results can weaken mandatory authoritative updates

Finding ID: LRNSIM-PR2
Severity: major
Location: `Recommended Direction` sections `Use these ownership rules`, contributor-confirmation behavior, and the proposed amendment to R21-R24
Evidence: The approved learn contract requires artifact updates, decisions, directions, and process follow-ups to reach their authoritative surfaces, and R33 requires the affected authoritative artifact to be updated when a lesson changes behavior. The proposal changes these to route-only results but does not define whether a created route, a scheduled follow-up, or an actually completed owner mutation satisfies each requirement. It also lists both `routing-required` and `session-complete` without defining how unresolved mandatory work affects completion. A conforming implementation could record a route, declare the session complete, and never produce the required authoritative update.
Required outcome: Preserve authoritative-update obligations while keeping mutation authority with the owning skill or stage.
Safe resolution path: Distinguish `route-created`, `owner-action-pending`, `owner-action-complete`, and `blocked` results. The session records the destination and authority basis. When the current contract requires an immediate authoritative update, the session cannot claim routing completion until the owning skill completes and the session links the resulting identity. When scheduling is expressly permitted, the exact durable follow-up may satisfy the route while remaining open. Same-turn continuation uses the owning skill and its review gates; contributor confirmation alone never grants that authority.
needs-decision rationale: none; this reconciles R21-R24 and R33 without giving `learn` cross-owner writes.

### LRNSIM-PR3 — Major: session creation has no create, resume, collision, or retry identity contract

Finding ID: LRNSIM-PR3
Severity: major
Location: `Recommended Direction`, `Expected Behavior Changes`, and `Testing and Verification Strategy`
Evidence: The proposal says an explicit session creates one record at `docs/learn/sessions/YYYY-MM-DD-<slug>.md`, and tests one-time creation at `Frame`, but does not say how the skill distinguishes a new session from an identical retry or an unrelated existing file. The approved spec currently says create or update, so a same-day slug collision, interrupted Frame, changed evidence scope, or competing edit can be interpreted as safe resume or overwrite. Topic updates have established curation semantics, but the primary session transaction lacks an exact identity and collision rule.
Required outcome: Define a bounded session create/resume model that never adopts or overwrites unrelated evidence.
Safe resolution path: Bind a session attempt to the exact trigger, trigger type, normalized scope, canonical path, and initial evidence basis. Create only when the path is absent. Resume only when the existing record identifies the same attempt and its current content identity matches the retry basis. An existing mismatched record, changed attempt basis, ambiguous slug, or competing edit stops and requires a distinct path or explicit owner-directed revision. Record creation at Frame must persist enough identity for interrupted retry before later phase writes.
needs-decision rationale: none; identity-bound retry is necessary for the proposal's one-session-record claim.

## Architecture assessment

The bounded expectation remains `architecture-not-required` if the revisions reuse existing workflow ownership, learn session records, and file identities. Architecture becomes required only if resolution adds a new persistent routing state, transaction schema, automated cross-stage coordinator, external integration, or write owner.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-LRNSIM-001` | Explicit direct `$learn` always selects a recorded learn session. |
| `AC-LRNSIM-002` | Pre-session trigger assessment grants `learn` no generic authority to mutate another owner's surface. |
| `AC-LRNSIM-003` | The trigger-owning stage records scheduled follow-up, deferral, or no-learn closeout under its own authority. |
| `AC-LRNSIM-004` | Contributor confirmation and destination mutation authority remain independent. |
| `AC-LRNSIM-005` | Every derivative result distinguishes route creation, pending owner action, completed owner action, and blockage. |
| `AC-LRNSIM-006` | Mandatory behavior-changing updates are not satisfied by an unowned chat-only route. |
| `AC-LRNSIM-007` | Same-turn continuation invokes the owning skill and preserves its review and settlement gates. |
| `AC-LRNSIM-008` | Every learn session binds one exact trigger, scope, canonical path, and initial evidence basis. |
| `AC-LRNSIM-009` | Identical retry resumes only the same matching session attempt. |
| `AC-LRNSIM-010` | Mismatched, ambiguous, or concurrently changed session records are never adopted or overwritten. |
| `AC-LRNSIM-011` | Both real procedural assemblies decrease from the current flat baseline. |
| `AC-LRNSIM-012` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |
| `AC-LRNSIM-013` | No target-agent runtime or separate semantic-grading system is used for acceptance. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload and cross-owner routing ambiguity are concrete. |
| User value | pass | Trigger assessment and real sessions should become easier to scan without weakening durable learning. |
| Option diversity | pass | Flat, editorial, one-reference, fragmented, and executable alternatives are materially distinct. |
| Decision rationale | pass | One session-method reference is the appropriate package boundary. |
| Vision fit | pass | Durable, human-confirmed, Git-tracked learning remains primary. |
| Scope control | pass | Templates, migration, taxonomy, runtime, issue integration, and unrelated skills remain excluded. |
| Universal safety | pass | Evidence, confirmation, ownership, sensitive-data, stops, claims, and triggers remain inline. |
| Pre-session ownership | block | A non-session closeout may write another stage's surface without a closed owner contract. |
| Derivative settlement | block | Route-only output does not yet preserve mandatory authoritative-update semantics. |
| Session identity | block | Create, resume, collision, and interrupted retry are not deterministic. |
| Topic ownership | pass | Confirmed topic guidance remains learn-owned and non-authoritative. |
| Missing-resource behavior | pass | A required session reference fails closed before dependent procedure. |
| Testing boundary | pass | Static scenarios, package parity, and ordinary lifecycle review are proportionate. |
| Measurement | pass with revisions | LR0 remains valid only if its read-only invocation boundary is made explicit. |
| Architecture awareness | pass with revisions | Existing ownership should suffice if no new routing or transaction owner is introduced. |
| Readiness for spec | changes-requested | LRNSIM-PR1 through LRNSIM-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; every initial goal and scoped work item is represented without expanding into templates, engines, migrations, or unrelated skill work.

## Recommended Proposal Edits

- Make pre-session trigger assessment read-only for `learn` and assign closeout mutation to the trigger owner.
- Define derivative route settlement so mandatory authoritative updates remain enforceable through the owning skill.
- Add an exact session create/resume/collision and interrupted-retry model.
- Update scenarios, risks, profile definitions, rollout, and acceptance criteria, then run an independent rereview.

## Recommendation

- Recommendation: revise the proposal to resolve LRNSIM-PR1 through LRNSIM-PR3, then run a new independent proposal review against the committed revision. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `initial_intent_table_context`, `scope_budget_context`
- Gate outcomes: pass; initial intent and scope have explicit dispositions
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-16-learn-skill-simplification/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-16-learn-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-16-learn-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-learn-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-16-learn-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
