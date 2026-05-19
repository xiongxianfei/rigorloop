# Published Skill Design Plan Family Routing Coverage

Change: `2026-05-19-published-skill-design-plan-family`
Milestone: M1
Date: 2026-05-19
Scope: `plan`, `plan-review`

## Purpose

Define deterministic routing evidence for the plan-family rollout. These prompt
fixtures evaluate description coverage and transcript behavior. They do not
claim deterministic runtime model auto-selection.

## Coverage contract

| Field | Required | Meaning |
|---|---:|---|
| positive triggers | yes | Concrete contexts that must be represented in `description`. |
| near misses | conditional | Nearby tasks that should be bounded when relevant. |
| competing skills | conditional | RigorLoop skills that should handle nearby tasks instead. |
| should-not-trigger classes | yes | Prompt classes that the skill should not claim. |

## `plan`

### Routing table

| Field | Coverage |
|---|---|
| Positive triggers | Create or revise an execution plan; sequence approved proposal/spec/architecture into milestones; split risky or multi-file work into reviewable implementation slices; define validation commands, recovery, dependencies, and handoff state. |
| Casual positives | "Make a plan for this approved spec"; "break this into milestones"; "sequence the implementation work"; "update the active execution plan." |
| Edge positives | Plan after clean spec-review but before test-spec; replan when current milestone scope changes; settle approved upstream status metadata before relying on it; create a plan for a change that needs milestone-aware handoff. |
| Near misses | Product direction, proposal writing, spec authoring, test-spec authoring, implementation, code review, verification, PR handoff, final lifecycle closeout. |
| Competing skills | `proposal`, `spec`, `test-spec`, `implement`, `code-review`, `verify`, `pr`, `workflow`. |
| Should-not-trigger classes | Generic task advice; simple one-step tasks; requests to write code immediately; requests to review a diff; requests to verify branch readiness; requests to open a PR. |

### Prompt fixtures

| Type | Prompt | Expected evidence |
|---|---|---|
| obvious positive | "Create an execution plan for this approved skill-contract rollout." | `description` should cover creating an execution plan after approved sources are stable. |
| casual positive | "Can you break this reviewed spec into implementation milestones?" | `description` should cover milestone-based planning. |
| edge positive | "The spec is approved and architecture is not needed; update the active plan so M1 can start after test-spec." | `description` and body should support planning after stable source artifacts and before implementation. |
| near negative | "Write the feature spec for this proposal." | `spec` should handle this, not `plan`. |
| competing skill | "Implement M1 from the current plan." | `implement` should handle this, not `plan`. |
| should not trigger | "Summarize the active plan in two sentences." | No plan artifact creation or revision is implied. |

### Current routing assessment

Current `description` is concise and includes execution-plan, stable-source, and
milestone triggers. M3 should add clearer near-miss boundaries for competing
lifecycle stages without turning the description into a synonym dump.

## `plan-review`

### Routing table

| Field | Coverage |
|---|---|
| Positive triggers | Review a concrete execution plan; challenge self-contained context, milestone sequencing, scope, dependencies, validation, recovery, architecture alignment, and readiness before implementation. |
| Casual positives | "Review this plan"; "sanity-check the implementation plan"; "is this plan ready for test-spec?" |
| Edge positives | Review a plan with conditional validator work; review a milestone plan before test-spec; review whether a plan preserves scope and handoff boundaries. |
| Near misses | Proposal review, spec review, architecture review, code review, final verification, PR readiness, implementation fixes, generic plan summary. |
| Competing skills | `proposal-review`, `spec-review`, `architecture-review`, `code-review`, `verify`, `pr`, `implement`. |
| Should-not-trigger classes | Requests to create the plan from scratch; requests to implement milestones; requests to review code diff; requests to verify branch readiness; requests to open a PR. |

### Prompt fixtures

| Type | Prompt | Expected evidence |
|---|---|---|
| obvious positive | "Review this concrete execution plan before implementation." | `description` should cover execution plan review before implementation. |
| casual positive | "Can you sanity-check whether this plan is ready for test-spec?" | `description` should cover readiness challenge for test-driven implementation. |
| edge positive | "This plan has M1 evidence, M2 validation, and M3 skill rewrite; review the sequencing and scope." | `description` and body should cover milestone sequencing, scope, dependencies, and validation. |
| near negative | "Review this feature spec for missing requirements." | `spec-review` should handle this, not `plan-review`. |
| competing skill | "Review the implementation diff for M1." | `code-review` should handle this, not `plan-review`. |
| should not trigger | "Summarize this plan without judging it." | A formal plan review is not requested. |

### Current routing assessment

Current `description` is concise and includes the main review dimensions. M3
should add explicit near-miss language for competing review and downstream
stages, especially `code-review`, `verify`, and `pr`.

## Static validation boundary

M2 may validate this file's existence and bounded phrases if useful. It must
not score natural-language quality broadly and must not claim model runtime
auto-selection.
