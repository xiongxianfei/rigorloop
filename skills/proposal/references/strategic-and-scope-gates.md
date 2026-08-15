# Strategic and scope gates

Load once for any specialized predicate. It owns strategic gates, intent, scope budget, and follow-up routing, not governed state or handoff.

## Closed predicates

The only predicates are `vision_exception_context`, `standing_artifact_context`, `initial_intent_table_context`, and `scope_budget_context`. Apply each independent semantic judgment without mechanical inference or suppression.

## Vision exception or revision

For conflict, revision, or exception, record the vision relationship, unsupported direction, request, owner decision, and recommendation effect. Ordinary `Vision fit` remains universal.

## Standing artifact gate

Use `standing_artifact_context` for missing `VISION.md` on substantive work or missing `CONSTITUTION.md` on governance/source-of-truth work. A substantive proposal is any proposal that chooses product direction, user-facing behavior, workflow policy, architecture direction, compatibility policy, release policy, or contributor-visible contract. `VISION.md` absence blocks the first substantive proposal except vision bootstrap. `CONSTITUTION.md` absence blocks governance adoption except constitution bootstrap. Bootstrap proposals must identify the bootstrap exception in `Vision fit`.

Record the artifact, status, dependency, route, blocker, and owner.

## Initial intent preservation

Closed enum: initial goal treatment

Classify each broad-request goal as `in scope`, `out of scope`, `deferred follow-up`, `rejected option`, or `open question`, and record its destination.

## Scope budget for broad proposals

Closed enum: scope budget treatment

Use `scope_budget_context` when the user request contains two or more independent work items, the change touches more than one lifecycle family, the change could reasonably require more than one spec or implementation plan, the proposal includes release policy, workflow policy, generated output, public skill behavior, or validation policy, or `proposal-review` identifies silent narrowing, hidden follow-up risk, or multi-workstream scope.

Classify each item with one `scope budget treatment`: `core to this proposal`, `first-slice candidate`, `same-slice dependency`, `separate implementation slice`, `deferable follow-up`, `separate proposal`, or `out of scope`. Use the `scope budget treatment` enum above for allowed treatment values.

## Follow-up routing

Route deferred work through the follow-up ownership model rather than chat-only notes or `project-map` ownership. Preserve this boundary: workflow routes, `project-map` orients when present, action-owning artifacts track current work, and unowned cross-change follow-ups use the follow-up ownership surface.

## Completion

Complete applicable groups or name blockers; omit only inapplicable groups and never leave placeholders.
