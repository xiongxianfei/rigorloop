# Learn session method

Use this reference only for `run-learn-session`. It owns the detailed `Frame -> Observe -> Classify -> Route` method; `SKILL.md` owns trigger eligibility, authority, stops, and claims.

## Prepare the session

Resolve the trigger, trigger type, normalized scope, initial evidence-basis identity, and canonical path `docs/learn/sessions/YYYY-MM-DD-<slug>.md` before writing.

For a new session, choose the base slug when absent. On collision, choose the lowest available suffix (`-2`, `-3`, and so on), then recheck absence immediately before creation. A new attempt never adopts an occupied path.

The first creation must contain complete `Frame` content. Do not create an empty transaction shell. If an existing record is partial, malformed, or lacks a complete Frame, `learn` must not resume, repair, adopt, or overwrite it. Stop and preserve it. A later attempt uses a new unique path.

When the same complete session identity, trigger, scope, and evidence basis already exists, return idempotent success. If the basis changed, start a new session at a new unique path and link the earlier session when useful; do not reinterpret it as an identical retry.

## Frame

Record the trigger and trigger type, scope, evidence in scope, explicit exclusions, prior learnings reviewed, and session path. For periodic learn sessions, also record time window start, time window end, and window basis.

## Observe

Inspect bounded evidence for patterns, surprises, drift, and gaps. Every observation is evidence-bound. Check relevant prior sessions, topic guidance, action-owning artifacts, ADRs, proposals, plans, and workflow material before proposing duplicate guidance. Record an explicit no-observation result when none exists.

For incident response, inspect the incident, affected contracts, reviews, verification, and postmortem actions while minimizing sensitive detail. For explicit invocation, inspect named artifacts and those directly implied by the stated pattern.

## Classify and confirm

Give each observation exactly one primary classification:

- `observation`
- `durable-lesson`
- `artifact-update`
- `decision`
- `direction`
- `process-follow-up`
- `no-durable-lesson`

Secondary routes are destinations or derivative actions, not extra primary classifications. Record observation ID, proposed and final primary classification, secondary routes, confirmed-by, and rationale.

Contributor confirmation uses `pending`, `confirmed`, or `rejected`. Persist candidate classifications as `pending` before stopping for confirmation. Only `confirmed` items may proceed to topic effects or routes. `rejected` preserves the decision and rationale without applying effects.

## Route

- `observation`: session record only.
- `durable-lesson`: add or curate a topic entry with date, lesson, source-session link, primary classification, and secondary routes.
- `artifact-update`, `decision`, `direction`, or `process-follow-up`: create an owner-bound route; do not mutate the destination. `direction` normally routes to proposal work. A process follow-up routes to an issue, a current change-local follow-up, or a proposal—not `docs/roadmap.md` and not a plan edit.
- `no-durable-lesson`: record its rationale and whether a follow-up was scheduled.

Assign stable route IDs in encounter order as `ROUTE-NNN`. Each route records classification, destination kind and path or external identity, owning skill or process, requested action, evidence-basis identity, and settlement. Use only `pending-owner-action`, `complete`, or `blocked`.

A route is `complete` only when an exact owner-result identity exists. Completion kind is `authoritative-artifact` or `durable-scheduled-follow-up`; scheduling counts only when the route contract permits it. Otherwise retain `pending-owner-action` or record an evidenced blocker. The session method must not poll and must not mutate the destination.

Apply learn-owned topic effects idempotently and link them from the session. Record routes before claiming session completion. A complete session may still contain pending routes; derive the aggregate route result as `not-required` when none exist, `blocked` when any route is blocked, `complete` when all are complete, and otherwise `pending-owner-action`.

## Session completion

The session is complete when Frame, Observe, Classify, confirmation disposition, topic effects, route records, and any no-learn rationale are durable and internally consistent. Completion says only that learning was recorded. Destination owners retain mutation, review, and settlement authority.
